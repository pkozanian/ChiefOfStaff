#!/usr/bin/env python3
"""Behavioral eval harness for the Chief of Staff — runs the real agent (`claude -p`).

For each scenario: copy the repo to a throwaway temp dir, seed preconditions, run `claude -p` there,
and assert on the resulting files / output. NON-DETERMINISTIC and token-costly — run locally, never
in CI. The real `memory/` is never touched (all work happens in the temp copy).

Usage:
  python3 tests/eval/run_eval.py                 # run all scenarios (Tier 1: on Claude)
  python3 tests/eval/run_eval.py --only intake   # run one
  python3 tests/eval/run_eval.py --dry-run       # exercise copy/seed/assert plumbing WITHOUT calling claude
  python3 tests/eval/run_eval.py --retries 1     # retry a failed scenario once (non-determinism)
  python3 tests/eval/run_eval.py --host codex --filter codex-   # Tier 2: run on `codex exec` (GPT)
  CHIEFOFSTAFF_EVAL_MODEL=opus python3 tests/eval/run_eval.py   # override the eval model (default: sonnet)
  CHIEFOFSTAFF_EVAL_MODEL_CODEX=gpt-5.6-terra python3 tests/eval/run_eval.py --host codex
  CHIEFOFSTAFF_EVAL_HOST=codex python3 tests/eval/run_eval.py   # same as --host codex
  CHIEFOFSTAFF_EVAL_DUMP=/tmp/cos-eval python3 tests/eval/run_eval.py --only onboard-terse   # keep a failure's transcript + memory/

Requires the `claude` CLI on PATH and an authenticated session (unless --dry-run) — `claude` is the
fixed grader for judged scenarios regardless of --host. `--host codex` additionally requires the
`codex` CLI, authenticated, on PATH.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scenarios  # noqa: E402
from scenarios import SCENARIOS, Ctx, Scenario  # noqa: E402

# The product tree — `src/` is exactly what an executive unzips, so copying it (rather than the
# whole repo) means every scenario runs against the real artifact: no CONTRIBUTING.md, no tests/,
# no docs/, no nested dist/. That's a property of the layout now, not something a seed fakes up.
REPO = Path(__file__).resolve().parent.parent.parent / "src"

# Frozen reference "today" for the evals. The fixtures are authored as-of this date (their
# commitments.md files anchor on it), so pinning it makes every time-relative scenario
# (overdue / due / this-week / current) deterministic no matter when the suite is run — the
# agent otherwise reasons off the real system clock and the fixtures would rot. Override with
# CHIEFOFSTAFF_EVAL_TODAY=YYYY-MM-DD to test the suite at a different clock position. See tests/README.md.
EVAL_TODAY = os.environ.get("CHIEFOFSTAFF_EVAL_TODAY", "2026-07-27")

# Which model the eval runs on (both the scenario agent and the judge). Default: Sonnet — the evals
# exercise the product on the model users typically run, and keep the higher-volume eval work cheap.
# Override with CHIEFOFSTAFF_EVAL_MODEL=opus (etc.) when a run needs it.
EVAL_MODEL = os.environ.get("CHIEFOFSTAFF_EVAL_MODEL", "sonnet")
# Where to keep a FAILED scenario's full transcript and resulting memory/ tree for diagnosis (the
# temp copy is deleted on return). Unset = keep nothing.
EVAL_DUMP = os.environ.get("CHIEFOFSTAFF_EVAL_DUMP", "")
# Tier 2's model, pinned so a cross-host comparison is like-for-like rather than "whatever each CLI
# defaults to". `gpt-5.6-terra` is the everyday-workhorse tier of the GPT-5.6 line (sol = detail and
# polish, terra = workhorse, luna = repeatable), i.e. the structural analogue of sonnet on the Claude
# side. Verified live against codex-cli 0.147.0 with a ChatGPT-account login.
#
# Do NOT assume an API model id works here: a ChatGPT account rejects `gpt-5.1-codex` AND
# `gpt-5.1-codex-mini` with "not supported when using Codex with a ChatGPT account". Confirm any new
# id with a one-line `codex exec --model <id> "Reply with exactly: PONG"` before pinning it.
EVAL_MODEL_CODEX = os.environ.get("CHIEFOFSTAFF_EVAL_MODEL_CODEX", "gpt-5.6-terra")

# The ChatGPT desktop app bundles the CLI rather than putting it on PATH, so look there before
# giving up. Override with CHIEFOFSTAFF_CODEX_BIN if it lives somewhere else.
_BUNDLED_CODEX = "/Applications/ChatGPT.app/Contents/Resources/codex"


def _codex_bin() -> str | None:
    explicit = os.environ.get("CHIEFOFSTAFF_CODEX_BIN")
    if explicit:
        return explicit if Path(explicit).exists() else None
    return shutil.which("codex") or (_BUNDLED_CODEX if Path(_BUNDLED_CODEX).exists() else None)


CODEX_BIN = _codex_bin()


def pin(prompt: str) -> str:
    """Prepend the frozen reference date so the agent treats it as 'today' for date reasoning."""
    return (
        f"Today's date is {EVAL_TODAY}. Use this as \"today\" for any date reasoning "
        f"(overdue, due, this/next week, current); ignore any other date.\n\n{prompt}"
    )


def copy_repo(dest: Path) -> None:
    shutil.copytree(
        REPO, dest, dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
    )
    # ensure the sandbox memory/ starts clean except its .keep folder-keeper
    mem = dest / "memory"
    for p in list(mem.rglob("*")):
        if p.is_file() and p.name != ".keep":
            p.unlink()


class RunnerBlocked(RuntimeError):
    """The CLI never produced an agent turn — a quota/auth/transport failure, not a behaviour.

    These must never be graded. A rate-limited `claude -p` prints "You've hit your session limit ·
    resets 2:40pm" **to stdout and exits 0**, so nothing marked it an error and the assertions
    scored that notice as if it were the agent's reply. It silently manufactures failures: a whole
    baseline-vs-change comparison once came back "identical" only because both sides were rate
    limited and neither had run the agent at all.
    """


# Quota/auth notices the CLIs emit *instead of* a turn. Matched against the full captured output.
_BLOCKED_RE = re.compile(
    r"you've hit your (session|usage) limit"
    r"|(session|usage|rate) limit (reached|exceeded)"
    r"|too many requests"
    r"|invalid api key|authentication_error|not logged in",
    re.IGNORECASE,
)


def _check_not_blocked(label: str, text: str, returncode: int) -> None:
    """Raise if `text` is a quota/auth notice rather than an agent turn."""
    if _BLOCKED_RE.search(text or ""):
        first = (text or "").strip().splitlines()[0][:160]
        raise RunnerBlocked(f"{label}: {first}")
    if returncode != 0 and not (text or "").strip():
        raise RunnerBlocked(f"{label}: exit={returncode} with no output")


def run_claude(cwd: Path, prompt: str, session: dict | None = None) -> str:
    """Run one headless turn. skip-permissions is safe here — cwd is a throwaway temp copy.

    `session` (a dict) turns on multi-turn: the first call records the session id in it, later calls
    `--resume` that id. JSON output is requested only then, because it is the only way to learn the id."""
    cmd = ["claude", "-p", prompt, "--model", EVAL_MODEL, "--dangerously-skip-permissions",
           "--strict-mcp-config"]
    if session is not None:
        cmd += ["--output-format", "json"]
        if session.get("id"):
            cmd += ["--resume", session["id"]]
    proc = subprocess.run(
        cmd, cwd=str(cwd), capture_output=True, text=True, timeout=600, check=False,
        # As with codex below: `claude -p` reads any non-TTY stdin and appends it to the prompt.
        # Inherited stdin (a driver's `while read` loop, a piped runner) silently contaminates the
        # scenario prompt -- observed as the agent reporting "your message included two extra lines".
        stdin=subprocess.DEVNULL,
    )
    text = proc.stdout
    if session is not None:
        try:
            data = json.loads(proc.stdout)
            session["id"] = data.get("session_id") or session.get("id")
            text = str(data.get("result", ""))
        except json.JSONDecodeError:
            pass  # a non-JSON failure — fall through and let the checks below report it
    out = text + ("\n" + proc.stderr if proc.stderr else "")
    _check_not_blocked("claude", out, proc.returncode)
    # Surface failures so CI logs show WHY (auth errors, refused flags, empty output).
    if proc.returncode != 0 or not text.strip():
        snippet = out.strip().replace("\n", " ")[:500] or "(no output)"
        print(f"      [claude exit={proc.returncode}] {snippet}", flush=True)
    return out


def run_codex(cwd: Path, prompt: str, session: dict | None = None) -> str:
    """Run one headless turn via `codex exec` (Tier 2 — proves GPT actually follows our prose, not
    just that the brain branches correctly). workspace-write is required because scenarios write
    memory/ files. With `session`, later turns go through `codex exec resume <id>`; the id is read
    from the banner codex prints to stderr on every run."""
    common = ["--model", EVAL_MODEL_CODEX,
              # The sandbox is a temp copy of src/, not a git repo; without this codex refuses to start
              # ("Not inside a trusted directory and --skip-git-repo-check was not specified").
              "--skip-git-repo-check"]
    if session is not None and session.get("id"):
        cmd = [CODEX_BIN, "exec", "resume", *common, "-c", 'sandbox_mode="workspace-write"',
               session["id"], prompt]
    else:
        cmd = [CODEX_BIN, "exec", *common, "--sandbox", "workspace-write", prompt]
    proc = subprocess.run(
        cmd, cwd=str(cwd), capture_output=True, text=True, timeout=600, check=False,
        # Without this codex waits on stdin ("Reading additional input from stdin...") and appends
        # whatever it finds to the prompt.
        stdin=subprocess.DEVNULL,
    )
    if session is not None and not session.get("id"):
        m = re.search(r"session id:\s*([0-9a-f-]{36})", proc.stderr or "", re.I)
        if m:
            session["id"] = m.group(1)
        else:
            print("      [codex] no session id in the banner — later turns will start fresh sessions",
                  flush=True)
    # UNLIKE the claude path, return stdout ONLY. codex streams a banner to stderr on every run
    # (version, workdir, model, session id) plus its reasoning; folding that into the graded text
    # made assertions and the judge score the banner rather than the reply. stdout is documented as
    # the final agent message alone, which is exactly what we want to grade.
    _check_not_blocked("codex", proc.stdout + "\n" + (proc.stderr or ""), proc.returncode)
    if proc.returncode != 0 or not proc.stdout.strip():
        snippet = (proc.stderr or proc.stdout).strip().replace("\n", " ")[:500] or "(no output)"
        print(f"      [codex exit={proc.returncode}] {snippet}", flush=True)
    return proc.stdout


def run_agent(cwd: Path, prompt: str, host: str, session: dict | None = None) -> str:
    """Dispatch to the runner for `host` ('claude' or 'codex')."""
    return run_codex(cwd, prompt, session) if host == "codex" else run_claude(cwd, prompt, session)


def judge_output(question: str, output: str, votes: int = 3) -> bool:
    """LLM judge for prose scenarios — majority vote over `votes` calls, in a neutral cwd.

    The grader is asked to QUOTE the relevant span and finish with a `VERDICT:` line, rather than to
    emit a single bare word. That is not cosmetic. Forcing a one-token answer made the grader wrong
    about a third of the time even on trivially checkable questions: asked "does the text contain the
    word 'Plugins'?" about text plainly containing it, votes came back YES/YES/NO. At a ~1/3 per-vote
    error rate, majority-of-3 flips a correct answer roughly a quarter of the time — which showed up
    as "flaky judges" and cost real debugging. Quote-then-verdict scored correctly on the same inputs,
    including the negative control.

    A call that fails or returns no VERDICT line is reported, not silently counted as NO — a broken
    grader and a genuine "no" must not look the same.
    """
    prompt = (
        "You are grading one test case. Read the OUTPUT carefully, then decide.\n\n"
        f"Question: {question}\n\n--- OUTPUT TO GRADE ---\n{output[:6000]}\n--- END ---\n\n"
        "Quote the single most relevant span from the OUTPUT, then give your verdict.\n"
        "Finish with a final line of exactly `VERDICT: YES` or `VERDICT: NO`."
    )
    yes = 0
    for _ in range(votes):
        proc = subprocess.run(
            ["claude", "-p", prompt, "--model", EVAL_MODEL, "--dangerously-skip-permissions", "--strict-mcp-config"],
            cwd=tempfile.gettempdir(), capture_output=True, text=True, timeout=300, check=False,
            stdin=subprocess.DEVNULL,
        )
        # A rate-limited grader returns a quota notice with no VERDICT line, which would otherwise
        # count as NO — biasing every graded scenario toward failure exactly when the account is
        # throttled. Blocked is not a verdict.
        _check_not_blocked("judge", proc.stdout + "\n" + (proc.stderr or ""), proc.returncode)
        verdicts = re.findall(r"VERDICT:\s*(YES|NO)", proc.stdout.upper())
        if not verdicts:
            snippet = (proc.stderr or proc.stdout).strip().replace("\n", " ")[:200] or "(no output)"
            print(f"      [judge call produced no VERDICT line, counted as NO] {snippet}", flush=True)
        elif verdicts[-1] == "YES":
            yes += 1
    return yes * 2 > votes

def run_scenario(sc: Scenario, dry: bool, host: str) -> tuple[bool, list[str]]:
    with tempfile.TemporaryDirectory(prefix=f"cos-eval-{sc.key}-") as td:
        root = Path(td) / "CoS"
        copy_repo(root)
        sc.seed(root / "memory")
        if sc.turns:
            session: dict = {}
            replies = []
            for i, turn in enumerate((pin(sc.prompt), *sc.turns)):
                shown = sc.prompt if i == 0 else turn
                reply = "" if dry else run_agent(root, turn, host, session)
                replies.append(f"── turn {i} · principal: {shown}\n{reply}")
            stdout = "\n\n".join(replies)
        else:
            stdout = "" if dry else run_agent(root, pin(sc.prompt), host)
        ctx = Ctx(root=root, stdout=stdout)
        lines, ok_all = [], True
        for label, fn in sc.assertions:
            try:
                ok = bool(fn(ctx))
            except Exception as e:  # noqa: BLE001
                ok, label = False, f"{label} (error: {e})"
            ok_all &= ok
            lines.append(f"      {'✅ PASS' if ok else '❌ FAIL'}  {label}")
        screened_out = bool(sc.judge_screen) and not any(
            w.lower() in stdout.lower() for w in sc.judge_screen)
        for label, question in sc.judge:
            if screened_out and not dry:
                # None of the words the judged behaviour requires are present, so it cannot be
                # present either. Pass without a judge call — see Scenario.judge_screen.
                ok = True
                lines.append(f"      ✅ PASS  [judge] {label} (screened: no {'/'.join(sc.judge_screen)})")
                continue
            ok = False if dry else judge_output(question, stdout)
            ok_all &= ok
            lines.append(f"      {'✅ PASS' if ok else '❌ FAIL'}  [judge] {label}")
        if dry:
            lines.append("      (dry-run: claude not called; file/output assertions may be trivially false)")
        elif not ok_all:  # show what the agent produced so failures are diagnosable
            lines.append("      ─ agent output (first 700 chars):")
            for ol in (stdout.strip()[:700] or "(empty)").splitlines():
                lines.append(f"        │ {ol}")
            if EVAL_DUMP:
                # Keep the whole transcript and the memory tree the run left behind — 700 chars is
                # not enough to diagnose a multi-turn scenario, and the temp dir is gone on return.
                dump = Path(EVAL_DUMP) / sc.key
                shutil.rmtree(dump, ignore_errors=True)
                dump.mkdir(parents=True, exist_ok=True)
                (dump / "transcript.txt").write_text(stdout, encoding="utf-8")
                if (root / "memory").exists():
                    shutil.copytree(root / "memory", dump / "memory")
                lines.append(f"      ─ full transcript + memory/ kept at {dump}")
        return ok_all, lines


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="run a single scenario by key")
    ap.add_argument("--filter", dest="filter", help="run all scenarios whose key contains this substring (e.g. 'mem-')")
    ap.add_argument("--dry-run", action="store_true", help="skip claude; test the harness plumbing")
    ap.add_argument("--retries", type=int, default=0, help="retry a failing scenario N times")
    ap.add_argument("--host", choices=["claude", "codex"],
                     default=os.environ.get("CHIEFOFSTAFF_EVAL_HOST", "claude"),
                     help="which agent CLI runs the scenarios: 'claude' (Tier 1, default) or "
                          "'codex' (Tier 2, via `codex exec`). Also settable via CHIEFOFSTAFF_EVAL_HOST. "
                          "Grading always runs on `claude` regardless of this flag.")
    args = ap.parse_args()

    # Seeds follow the runner: seeds that don't pin an explicit host (seed_onboarded and friends)
    # read this so their seeded meta.md matches which agent CLI is about to read it. Scenarios that
    # test a SPECIFIC host branch (seed_pending_codex, seed_onboarded_codex) stay explicit regardless.
    scenarios.ACTIVE_HOST = "codex" if args.host == "codex" else "claude-code"

    if not args.dry_run:
        # `claude` is the fixed grader for judged scenarios no matter which host runs the scenario
        # itself — a fixed grader across model families is the point, so this check applies even
        # under --host codex. Fail here with a clear reason rather than obscurely inside the judge.
        if shutil.which("claude") is None:
            print("ERROR: `claude` CLI not found on PATH. Install it (or use --dry-run) — `claude` is "
                  "required as the fixed grader for LLM-judged scenarios, regardless of --host.",
                  file=sys.stderr)
            return 2
        if args.host == "codex" and CODEX_BIN is None:
            print("ERROR: `codex` CLI not found on PATH — required for --host codex.\n"
                  "  Install it with `npm i -g @openai/codex`, then authenticate (`codex login`).\n"
                  "  Or drop --host codex to run Tier 1 on Claude instead (the default).",
                  file=sys.stderr)
            return 2

    sel = SCENARIOS
    if args.only:
        sel = [s for s in sel if s.key == args.only]
    if args.filter:
        sel = [s for s in sel if args.filter in s.key]
    if not sel:
        picked = args.only or args.filter
        print(f"No scenario matches {picked!r}", file=sys.stderr)
        return 2

    # Name the exact model in the header: a cross-host comparison is only meaningful if you can see
    # which tier each side actually ran, and the defaults differ per CLI.
    runner_label = ("DRY RUN" if args.dry_run else
                    (f"live codex exec, model {EVAL_MODEL_CODEX}" if args.host == "codex"
                     else f"live claude -p, model {EVAL_MODEL}"))
    print(f"Chief of Staff — behavioral eval ({runner_label})", flush=True)
    failed = []
    # A scenario restricted to another host is SKIPPED, not failed: it can't be observed here (the
    # brain corrects a seeded host to the real one), so running it would produce a meaningless red.
    skipped = [sc for sc in sel if sc.only_hosts and args.host not in sc.only_hosts]
    sel = [sc for sc in sel if not sc.only_hosts or args.host in sc.only_hosts]
    for sc in skipped:
        print(f"  ⏭  SKIP  {sc.key} — needs --host {'/'.join(sc.only_hosts)}", flush=True)
    n = len(sel)
    for i, sc in enumerate(sel, 1):
        print(f"\n[{i}/{n}] {sc.key} — {sc.title}" + ("  (LLM-graded)" if sc.graded else ""), flush=True)
        if not args.dry_run:
            print(f"      … running agent{' + judge' if sc.judge else ''} (~30–90s)…", flush=True)
        t0 = time.time()
        # A quota/auth block aborts the whole run. Retrying can't clear a session limit, and
        # continuing would report every remaining scenario as a behavioural failure when in fact
        # none of them ran — the failure mode that made a previous comparison worthless.
        try:
            ok, lines = run_scenario(sc, args.dry_run, args.host)
            attempt = 0
            while not ok and attempt < args.retries and not args.dry_run:
                attempt += 1
                print(f"      … retry {attempt}/{args.retries}…", flush=True)
                ok, lines = run_scenario(sc, args.dry_run, args.host)
        except RunnerBlocked as e:
            print(f"\n{'=' * 48}")
            print(f"⛔ BLOCKED at {sc.key} ({i}/{n}) — {e}")
            print("   The CLI returned a quota/auth notice instead of an agent turn, so nothing")
            print("   after this point could be evaluated. No result is reported for the remaining")
            print(f"   {n - i} scenario(s) — they did NOT pass and did NOT fail; they never ran.")
            if failed:
                print(f"   Scenarios that genuinely failed before the block: {', '.join(failed)}")
            return 3
        print("\n".join(lines), flush=True)
        if not args.dry_run:
            print(f"      done in {time.time() - t0:.0f}s", flush=True)
        if not ok:
            failed.append(sc.key)

    print(f"\n{'=' * 48}")
    if args.dry_run:
        print("Dry run complete — plumbing exercised (copy/seed/assert). Run without --dry-run for real results.")
        return 0
    if failed:
        print(f"❌ FAILED scenarios: {', '.join(failed)}")
        return 1
    print(f"✅ OK — all {n} scenarios passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
