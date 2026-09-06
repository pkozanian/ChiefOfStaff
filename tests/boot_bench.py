#!/usr/bin/env python3
"""Live boot benchmark — what a bare "hi" actually costs before the principal sees a word.

`tests/boot_profile.py` is a STATIC estimator: it adds up file sizes and guesses at read counts.
Every boot number this repo has ever acted on came from that kind of arithmetic, and the
boot-latency work was misranked twice as a result — once per host family. This runs the real
agent against a real fixture and reports what happened.

    python3 tests/boot_bench.py                        # 3 runs, working tree, heavy fixture
    python3 tests/boot_bench.py --vs HEAD              # A/B: working tree vs HEAD, interleaved
    python3 tests/boot_bench.py --vs main --reps 5
    python3 tests/boot_bench.py --fixture saas-cto --trace
    python3 tests/boot_bench.py --list

NON-DETERMINISTIC and token-costly, like the eval suite — run it locally, never in CI. Each rep is
a fresh throwaway copy of the tree under test, so the real `memory/` is never touched.

Requires the `claude` CLI on PATH and an authenticated session. Claude Code only for now: Codex
emits a different event schema (`codex exec --json`), and the two hosts' operation counts are not
comparable anyway — Codex batches reads in `for f in` loops where Claude Code reads one file at a
time. Cross-host comparison is deltas within a host, never absolute numbers between them.

WHY FOUR NUMBERS AND NOT ONE. BOOT PROTOCOL step 10 prints a **loading tip** before the greeting,
on purpose, to fill the read window while wave 2 loads. So the first visible output and the
greeting are different events, and a single "time to respond" would score that feature as a
speedup. T_first and T_done are reported apart so it can't.

WHY A/B IS INTERLEAVED. Two measured runs of the same boot chose different strategies — one made 19
`Read` calls, the other 4 `Bash` calls — and the strategy difference moved the numbers further than
the change under test did. Running all of A and then all of B confounds the change with whatever
drifted in between (throttling, model routing, the agent's own coin flips). A/B/A/B does not remove
the variance, but it stops it landing on one side.

WHY TOOL INPUTS ARE RECORDED. `Bash×4` is opaque: four shell calls might read six files or sixty.
Without the inputs there is no way to tell a genuine reduction from a re-shuffle, which is exactly
the question that stalled the first measurement.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parent
sys.path.insert(0, str(TESTS / "eval"))
import run_eval  # noqa: E402  — the rate-limit guard, the frozen date, the model pin
import scenarios  # noqa: E402  — the fixture version alignment, shared with the eval seeds

FIXTURES = TESTS / "fixtures"

# A bare greeting is the whole point: it is the cheapest thing a principal can say, so everything
# it costs is boot. Not configurable — a different prompt measures a different thing and the
# numbers would silently stop being comparable across runs.
PROMPT = "hi"


# ------------------------------------------------------------------ fixtures
def fixture_memory(name: str) -> Path:
    """Resolve a fixture name to its memory tree.

    Two layouts exist and both are legitimate: the persona trees under `tests/fixtures/memory/<name>/`
    (used by the `mem-*` evals) and the standalone `tests/fixtures/<name>/memory/` trees
    (`onboarded`, `team`, used by the structural checks). Try both rather than making the caller
    know which kind they asked for.
    """
    for candidate in (FIXTURES / "memory" / name, FIXTURES / name / "memory"):
        if candidate.is_dir():
            return candidate
    raise SystemExit(f"no fixture {name!r} — try --list")


def list_fixtures() -> list[str]:
    names = {p.name for p in (FIXTURES / "memory").iterdir() if p.is_dir()}
    names |= {p.name for p in FIXTURES.iterdir() if p.is_dir() and (p / "memory").is_dir()}
    return sorted(names)


# ------------------------------------------------------------------ trees under test
def copy_tree(src: Path, dest: Path) -> None:
    """Copy a product tree and empty its `memory/`, ready for a fixture to be seeded in.

    Deliberately parallel to `run_eval.copy_repo`, which hardcodes `src/` in the working tree. A/B
    needs the same operation against a tree checked out from an arbitrary ref, so the source is a
    parameter here rather than a module constant.
    """
    shutil.copytree(src, dest, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    mem = dest / "memory"
    for p in list(mem.rglob("*")):
        if p.is_file() and p.name != ".keep":
            p.unlink()


def prepare_ref(ref: str, into: Path) -> Path:
    """Extract `<ref>:src/` into `into` and return the product root.

    `git archive` rather than `git worktree`: it needs no lock, leaves no state behind if this
    process dies, and cannot disturb the working tree the other side of the A/B is measuring.
    """
    into.mkdir(parents=True, exist_ok=True)
    tar = subprocess.run(["git", "archive", ref, "src"], cwd=str(ROOT),
                         capture_output=True, check=False)
    if tar.returncode != 0:
        raise SystemExit(f"git archive {ref} failed: {tar.stderr.decode()[:300]}")
    subprocess.run(["tar", "-x", "-C", str(into)], input=tar.stdout, check=True)
    return into / "src"


# ------------------------------------------------------------------ one run
@dataclass
class Op:
    """One tool call, with enough of its input to tell a real reduction from a re-shuffle."""
    name: str
    detail: str

    @staticmethod
    def summarize(name: str, inp: dict) -> "Op":
        if name == "Read":
            span = ""
            if inp.get("offset") or inp.get("limit"):
                span = f" [{inp.get('offset', 0)}:+{inp.get('limit', '?')}]"
            return Op(name, f"{inp.get('file_path', '?')}{span}")
        if name == "Bash":
            return Op(name, " ".join((inp.get("command") or "").split()))
        if name in ("Grep", "Glob"):
            return Op(name, f"{inp.get('pattern', '?')} in {inp.get('path', '.')}")
        return Op(name, json.dumps(inp, separators=(",", ":")))


@dataclass
class Run:
    """One boot: the event stream, timestamped as it arrives."""
    t_first: float | None = None   # first assistant text — may be the loading tip, not the greeting
    t_done: float = 0.0            # end of turn
    turns: int = 0                 # assistant messages = model round-trips; what latency tracks
    ops: list[Op] = field(default_factory=list)
    tok_in: int = 0
    tok_out: int = 0
    # Characters emitted per kind, accumulated as the stream arrives. Output tokens are attributed
    # across these buckets in proportion at the end — the API reports one output_tokens per message,
    # not per block, so a within-message split has to be inferred. Chars/token is close enough to
    # constant across prose, reasoning and JSON for the shares to be meaningful; the totals are not.
    ch_think: int = 0      # extended reasoning
    ch_narr: int = 0       # prose written BEFORE the final message — commentary, not the answer
    ch_tool: int = 0       # tool-call parameters (JSON), e.g. a long absolute path per Read
    ch_final: int = 0      # the last text block: the greeting the principal actually waited for
    first_text: str = ""   # what the first text block SAID — a timestamp alone cannot tell a
                           # loading tip from a greeting, and BOOT-31's whole claim is that the tip
                           # arrives while wave 2 is still loading

    def attribute(self) -> dict[str, int]:
        """Estimate tok_out by bucket, and report what the stream does NOT account for.

        An earlier version split tok_out across the visible buckets in proportion — which silently
        charged every unaccounted token to whichever block happened to be longest, and reported
        "88% tool parameters" for 21 short file paths. The buckets are now estimated independently
        at ~4 chars/token, and the remainder is named rather than distributed. That remainder is
        output the API billed with no corresponding text, thinking, or tool_use block in the
        stream — reasoning that was emitted but not surfaced. It is usually the largest bucket,
        which is the point: it cannot be seen, so it must at least be counted.
        """
        est = {"thinking": self.ch_think // 4, "narration": self.ch_narr // 4,
               "tool params": self.ch_tool // 4, "greeting": self.ch_final // 4}
        est["unsurfaced"] = max(0, self.tok_out - sum(est.values()))
        return est

    @property
    def by_tool(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for op in self.ops:
            out[op.name] = out.get(op.name, 0) + 1
        return out

    @property
    def files(self) -> set[str]:
        """Distinct paths opened by `Read`. Shell reads are NOT counted — that is the point of the
        trace: a `Bash` call's file count is invisible here and has to be read off its command."""
        return {op.detail.split(" [")[0] for op in self.ops if op.name == "Read"}


def open_tip_gate(mem: Path) -> None:
    """Delete `last_tip:` from the seeded `meta.md`, so boot step 10's once-a-day gate is OPEN.

    Every committed fixture stamps `last_tip: 2026-07-27`, which is exactly the date `run_eval`
    pins as today — so the gate is shut in every default run, and a boot that prints no tip proves
    nothing about the tip. Stripping the line at seed time keeps one fixture in the repo instead of
    two ~380KB trees differing by a single line."""
    meta = mem / "meta.md"
    if meta.exists():
        kept = [ln for ln in meta.read_text(encoding="utf-8").splitlines(True)
                if not re.match(r"^\s*(?:-\s+\*\*)?last_tip:", ln)]
        meta.write_text("".join(kept), encoding="utf-8")


def bench_once(product_root: Path, fixture_mem: Path, tip_eligible: bool = False) -> Run:
    """Copy the tree under test, seed the fixture, run one turn, timestamp the stream."""
    with tempfile.TemporaryDirectory(prefix="cos-bench-") as td:
        root = Path(td) / "CoS"
        copy_tree(product_root, root)
        shutil.copytree(fixture_mem, root / "memory", dirs_exist_ok=True)
        if tip_eligible:
            open_tip_gate(root / "memory")
        # A fixture pinned to an older release makes boot run the MIGRATION PASS before it greets
        # anyone — 33 releases of CHANGELOG blocks, reconciliation, and proposed writes. Benched
        # unaligned, `onboarded` took 186s and 287s against ~55s aligned: that is a measurement of
        # the migration, not of boot. Align it here for the same reason the eval seeds do.
        scenarios._align_onboarded_against(root / "memory")

        r = Run()
        raw: list[str] = []
        t0 = time.monotonic()
        proc = subprocess.Popen(
            ["claude", "-p", run_eval.pin(PROMPT),
             "--output-format", "stream-json", "--verbose",
             "--model", run_eval.EVAL_MODEL,
             "--dangerously-skip-permissions", "--strict-mcp-config"],
            cwd=str(root), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1,
            # As in run_eval: `claude -p` appends any non-TTY stdin to the prompt, so an inherited
            # pipe silently contaminates it.
            stdin=subprocess.DEVNULL,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            raw.append(line)
            now = time.monotonic() - t0
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue  # the CLI can interleave non-JSON notices; the guard below catches them
            if ev.get("type") == "assistant":
                # Ops and round-trips are NOT the same number: one assistant turn can carry several
                # tool_use blocks, which the host runs in parallel. Wall-clock tracks turns; token
                # cost tracks ops. Reporting only ops hides which one a change actually moved.
                r.turns += 1
                for block in ev.get("message", {}).get("content", []) or []:
                    kind = block.get("type")
                    if kind == "tool_use":
                        inp = block.get("input") or {}
                        r.ops.append(Op.summarize(block.get("name", "?"), inp))
                        r.ch_tool += len(json.dumps(inp))
                    elif kind == "thinking":
                        r.ch_think += len(block.get("thinking") or "")
                    elif kind == "text" and block.get("text", "").strip():
                        # Everything written so far becomes narration; only the LAST text block is
                        # the greeting. Roll the previous candidate back as each new one arrives.
                        r.ch_narr += r.ch_final
                        r.ch_final = len(block["text"])
                        if r.t_first is None:
                            r.t_first = now
                            r.first_text = " ".join(block["text"].split())[:160]
            elif ev.get("type") == "result":
                r.t_done = now
                u = ev.get("usage") or {}
                # Cache reads are real input the model had to be given; counting only
                # `input_tokens` would report a warm run as nearly free and hide the corpus.
                r.tok_in = (u.get("input_tokens", 0)
                            + u.get("cache_creation_input_tokens", 0)
                            + u.get("cache_read_input_tokens", 0))
                r.tok_out = u.get("output_tokens", 0)
        err = proc.stderr.read() if proc.stderr else ""
        proc.wait()
        text = "".join(raw) + "\n" + err
        # A rate-limited `claude -p` exits 0 having produced no turn. Unguarded, that is a boot with
        # no reads and no tokens — i.e. it reports a throttled account as a spectacular speedup.
        # run_eval.py carries the scar: a whole before/after comparison once came back "identical"
        # because both sides were limited and neither had run the agent at all.
        run_eval._check_not_blocked("claude", text, proc.returncode)
        if not r.t_done:
            raise run_eval.RunnerBlocked(
                f"no result event (exit={proc.returncode}): {text.strip()[:300] or '(no output)'}")
        return r


# ------------------------------------------------------------------ reporting
HDR = (f"{'run':>5}{'T_first':>10}{'T_done':>9}{'TURNS':>7}{'OPS':>6}{'FILES':>7}"
       f"{'TOK_in':>10}{'TOK_out':>9}  tools")


def row(label: str, r: Run) -> str:
    first = f"{r.t_first:.1f}s" if r.t_first is not None else "—"
    tools = ", ".join(f"{n}×{c}" for n, c in sorted(r.by_tool.items()))
    return (f"{label:>5}{first:>10}{r.t_done:>8.1f}s{r.turns:>7}{len(r.ops):>6}{len(r.files):>7}"
            f"{r.tok_in:>10}{r.tok_out:>9}  {tools}")


def summary(label: str, runs: list[Run]) -> str:
    firsts = [r.t_first for r in runs if r.t_first is not None]
    return (f"{label:>5}{(f'{statistics.median(firsts):.1f}s' if firsts else '—'):>10}"
            f"{statistics.median([r.t_done for r in runs]):>8.1f}s"
            f"{statistics.median([r.turns for r in runs]):>7.0f}"
            f"{statistics.median([len(r.ops) for r in runs]):>6.0f}"
            f"{statistics.median([len(r.files) for r in runs]):>7.0f}"
            f"{statistics.median([r.tok_in for r in runs]):>10.0f}"
            f"{statistics.median([r.tok_out for r in runs]):>9.0f}")


def trace(runs: list[Run], label: str) -> None:
    print(f"\n── trace: {label}, run 1 of {len(runs)} ──")
    for i, op in enumerate(runs[0].ops, 1):
        print(f"  {i:>3}. {op.name:<6} {op.detail[:140]}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Measure what a bare 'hi' costs at boot.")
    ap.add_argument("--fixture", default="heavy",
                    help="fixture memory tree to boot against (default: heavy — 15 specialists, "
                         "the shape that makes boot cost visible)")
    ap.add_argument("--reps", type=int, default=3,
                    help="runs per side (default 3; one run is a sample, not a measurement)")
    ap.add_argument("--vs", metavar="REF",
                    help="A/B the working tree against a git ref, interleaved A/B/A/B")
    ap.add_argument("--vs-fixture", metavar="NAME",
                    help="A/B two fixtures on the SAME tree, interleaved — for isolating one "
                         "property of the principal's memory (a tracker's closed rows, a roster's "
                         "size) while everything else is held identical")
    ap.add_argument("--tip-eligible", action="store_true",
                    help="strip `last_tip` from the seeded memory so boot step 10's once-a-day "
                         "gate is open — required to measure the loading tip at all (BOOT-31)")
    ap.add_argument("--trace", action="store_true",
                    help="print every tool call with its input for the first run of each side")
    ap.add_argument("--list", action="store_true", help="list available fixtures and exit")
    args = ap.parse_args()

    if args.list:
        print("\n".join(list_fixtures()))
        return 0

    if args.vs and args.vs_fixture:
        raise SystemExit("--vs and --vs-fixture measure different things; pick one")
    mem = fixture_memory(args.fixture)
    ver = (ROOT / "src" / "VERSION").read_text(encoding="utf-8").strip()
    print(f"BOOT BENCH  src/ v{ver}  fixture={args.fixture}  model={run_eval.EVAL_MODEL}  "
          f"prompt={PROMPT!r}  reps={args.reps}"
          + (f"  A=working tree  B={args.vs}" if args.vs else ""))

    with tempfile.TemporaryDirectory(prefix="cos-bench-ref-") as refdir:
        sides: list[tuple[str, Path]] = [("A", ROOT / "src")]
        if args.vs:
            sides.append(("B", prepare_ref(args.vs, Path(refdir))))
        mems = {"A": mem}
        if args.vs_fixture:
            sides.append(("B", ROOT / "src"))
            mems["B"] = fixture_memory(args.vs_fixture)

        results: dict[str, list[Run]] = {k: [] for k, _ in sides}
        print(f"\n{HDR}\n" + "-" * 96)
        try:
            # Interleaved: A/B/A/B, not all of A then all of B. Whatever drifts between runs —
            # throttling, routing, the agent's own choices — then lands on both sides equally.
            for i in range(1, args.reps + 1):
                for key, tree in sides:
                    r = bench_once(tree, mems.get(key, mem), args.tip_eligible)
                    results[key].append(r)
                    print(row(f"{key}{i}", r))
        except run_eval.RunnerBlocked as e:
            print(f"\nBLOCKED: {e}\nNothing further was measured. A partial A/B is worse than "
                  f"none — the sides no longer have equal exposure. Rerun when the account is clear.")
            return 1

        print("-" * 96)
        for key, _ in sides:
            print(summary(f"med {key}" if (args.vs or args.vs_fixture) else "med", results[key]))

        if args.vs or args.vs_fixture:
            a, b = results["A"], results["B"]
            def d(f) -> str:
                av, bv = statistics.median([f(r) for r in a]), statistics.median([f(r) for r in b])
                if bv == 0:
                    return f"{av - bv:+.0f}"
                return f"{av - bv:+.0f} ({(av - bv) / bv * 100:+.0f}%)"
            print(f"\nA − B:  ops {d(lambda r: len(r.ops))}   files {d(lambda r: len(r.files))}   "
                  f"tok_in {d(lambda r: r.tok_in)}   t_done {d(lambda r: r.t_done)}s")
            print("A single-digit rep count does not separate a real change from the agent's own "
                  "strategy variance. Read the traces before believing a delta.")

        print("\nWhere the output tokens went (T_done tracks these, not the reads):")
        for key, _ in sides:
            runs = results[key]
            share: dict[str, int] = {}
            for r in runs:
                for k, v in r.attribute().items():
                    share[k] = share.get(k, 0) + v
            n, tot = len(runs), sum(share.values()) or 1
            print(f"  {'side ' + key if (args.vs or args.vs_fixture) else 'mean'}: "
                  + "   ".join(f"{k} {v // n:,} ({v * 100 // tot}%)" for k, v in share.items())
                  + f"   [{tot // n:,} tok ≈ {tot / n / 93:.0f}s at 93 tok/s]")

        if args.trace:
            for key, _ in sides:
                trace(results[key], "working tree" if key == "A" else str(args.vs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
