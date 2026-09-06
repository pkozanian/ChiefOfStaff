#!/usr/bin/env python3
"""Structural test suite for Chief of Staff.

Deterministic checks on the markdown files and conventions — no LLM, stdlib only.
Run: python3 tests/run.py   (exit 0 = all pass, non-zero = failures)
"""
from __future__ import annotations

import ast
import fnmatch
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# The product tree. `src/` IS the artifact: what ships is exactly this subtree (scripts/build-dist.sh
# copies it verbatim), so every "does the product do X" check below is rooted here, not at the repo
# root. Repo-level things (fixtures, git, the website) stay on ROOT.
SRC = ROOT / "src"
BRAIN = SRC / "brain"
COMMANDS = SRC / ".claude" / "commands"
SKILLS = SRC / ".agents" / "skills"

ALLOWED_TYPES = {"role", "playbook", "profile", "person", "project", "preference", "context", "log", "commitment", "okr", "decision", "team-member", "delegation", "desk"}

# ---------------------------------------------------------------- result plumbing
FAILURES: list[str] = []
CHECKS = 0


def check(name: str, ok: bool, detail: str = "", behavior: str = "") -> None:
    """Record one assertion.

    `behavior` is the tests/behaviors.md ID this assertion covers. It is deliberately UNUSED at
    runtime — check #17 reads it out of this file's source with `ast`, so a check() sitting in a
    branch that did not execute still counts as annotated. Collecting it at runtime instead would
    report every conditional check as unannotated. Do not "clean up" the unused parameter.
    """
    global CHECKS
    CHECKS += 1
    if ok:
        print(f"  ✅ PASS  {name}")
    else:
        print(f"  ❌ FAIL  {name}" + (f" — {detail}" if detail else ""))
        FAILURES.append(name if not detail else f"{name}: {detail}")


def section(title: str) -> None:
    print(f"\n{title}")


# ---------------------------------------------------------------- helpers
def brain_md_files() -> list[Path]:
    return sorted(p for p in BRAIN.rglob("*.md"))


def parse_frontmatter(path: Path) -> dict[str, str] | None:
    """Parse the file's OWN leading `---...---` block into a flat dict.

    Only the leading block — never code-fence examples further down.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    body = text[3:end]
    fm: dict[str, str] = {}
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def frontmatter_body(path: Path) -> str:
    """Text after the file's own closing frontmatter `---` line (the whole file if it has none)."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    nl = text.find("\n", end + 1)
    return text[nl + 1:] if nl != -1 else ""


def strip_code_fences(text: str) -> str:
    """Blank out fenced code blocks so example links/frontmatter are ignored."""
    out, in_fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def tracked_md_files() -> list[Path]:
    files = []
    for rel in git(["ls-files", "*.md"]).splitlines():
        p = ROOT / rel
        if p.exists():
            files.append(p)
    return files


def git(args: list[str]) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True, text=True, check=False,
    ).stdout


# ---------------------------------------------------------------- coverage helpers
def required_functional_files() -> set[str]:
    """The functional surface the behavior registry must state (product-relative posix paths, i.e. as
    they appear inside src/ and therefore inside the shipped folder)."""
    files = {p.relative_to(SRC).as_posix() for p in BRAIN.rglob("*.md")}
    files.add("CLAUDE.md")
    files.add("AGENTS.md")
    files.add("CHIEFOFSTAFF.md")
    files |= {p.relative_to(SRC).as_posix() for p in COMMANDS.glob("*.md")}
    return files


# ---------------------------------------------------------------- behavior registry helpers
# The eleven areas are fixed by the design doc. A twelfth is a spec change, not a local decision.
BEHAVIOR_AREAS = {"BOOT", "ONB", "ROLE", "MEM", "CAP", "PLAY", "TEAM", "DESK", "HOST", "REL", "REPO"}
BEHAVIOR_ID = re.compile(r"^[A-Z]{3,4}-\d{2}$")
ID_SHAPED = re.compile(r"^[A-Z]{3,4}-\d+$")  # looks like an ID but may fail BEHAVIOR_ID (wrong digit count)


def parse_behaviors(path: Path) -> tuple[list[tuple[str, dict[str, str]]], list[tuple[str, str]]]:
    r"""Parse tests/behaviors.md → (rows, malformed).

    `rows` is ordered [(id, {'behavior','stated_in','covered'})]. A LIST, not a dict: a duplicate ID
    is a failure the caller must report, and a dict would silently swallow it.

    `malformed` is [(id, detail)] for lines whose ID cell is ID-shaped but otherwise wrong — either the
    ID itself is malformed (e.g. a mistyped digit count) or the column count is. Reported, never
    skipped. A row silently dropped VANISHES from the registry — passing every transpose rule because
    nothing knows it was ever there. This exact bug was found in the file this registry replaces: three
    of its rows carried an unescaped `|` in prose, and the tooling truncated them without a word.
    Escape it as `\|` in the registry. The same vanishing happens to a gap row whose ID is mistyped
    (`BOOT-03` → `BOOT-003`): it looks like a behavior row but fails BEHAVIOR_ID, so it is reported
    here rather than silently skipped like a header or a prose table.

    An EMPTY `Covered by` is meaningful — it is how an untested behavior is recorded — so rows are
    kept on ID shape and column count, never on truthiness.
    """
    rows: list[tuple[str, dict[str, str]]] = []
    malformed: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        # Split on unescaped pipes only, then unescape — GitHub renders `\|` as a literal pipe inside
        # a cell, so a parser that splits on it would disagree with what the file visibly says.
        cells = [c.strip().replace("\\|", "|")
                 for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        bid = cells[0].strip("` ")
        if not BEHAVIOR_ID.match(bid):
            if ID_SHAPED.match(bid):  # ID-shaped but not <AREA>-<NN> — a mistyped ID, not a header/prose row
                malformed.append((bid, f"ID-shaped but not <AREA>-<NN>: {bid!r} — check for a typo"))
            continue  # skips the header, the separator, and any prose table
        if len(cells) != 4:
            malformed.append((bid, f"parsed {len(cells)} columns — escape any literal `|` in a cell as `\\|`"))
            continue
        rows.append((bid, {"behavior": cells[1], "stated_in": cells[2].strip("` "),
                           "covered": cells[3]}))
    return rows, malformed


def parse_coverage_summary(path: Path) -> dict[str, tuple[int, int, int]]:
    r"""Parse behaviors.md's "Where the coverage is" table → {area or 'Total': (rows, covered, gaps)}.

    That table is the only integrity guard a GAP row has, which is why rule 7 reconciles it with the
    parsed rows. A COVERED row is held from both sides — rules 2 and 3 are bidirectional, so its
    scenario or its annotated check() notices the moment the row stops claiming it. Nothing claims a
    gap row. Mistype one's ID (`BOOT-03` → `BOOT-003`) and BEHAVIOR_ID rejects it, the behavior would
    VANISH from the registry with every other rule staying green — parse_behaviors() now reports this
    directly as malformed (R23), and rule 7 remains as a second guard: reconciling the counts also
    stops the hand-maintained table from drifting as a side effect.
    """
    out: dict[str, tuple[int, int, int]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # `BOOT` boot + routing | 23 | 8 | 15   —   or the bolded **Total** row
        m = re.match(r"^(?:\*\*)?(?:`([A-Z]{3,4})`|(Total))", cells[0]) if len(cells) == 4 else None
        nums = [re.fullmatch(r"\**(\d+)\**", c) for c in cells[1:]] if m else []
        if m and all(nums):
            out[m.group(1) or "Total"] = (int(nums[0].group(1)), int(nums[1].group(1)),  # type: ignore[union-attr]
                                          int(nums[2].group(1)))  # type: ignore[union-attr]
    return out


def covered_tokens(cell: str) -> tuple[set[str], bool]:
    """Split a `Covered by` cell into ({eval keys or globs}, carries a bare `check` marker).

    `check` is a bare marker, not `check:<ID>`: a structural citation can only ever name its own
    row's ID, so spelling it out again would be a second copy to keep in sync for no information.
    """
    pats = set(re.findall(r"eval:([A-Za-z0-9_*?\[\]-]+)", cell))
    return pats, bool(re.search(r"(?<![\w:-])check(?![\w:-])", cell))


def _check_calls() -> list[ast.Call]:
    """Every `check(...)` call site in this file, parsed from source."""
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    return [n for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "check"]


def _behavior_kw(node: ast.Call) -> ast.keyword | None:
    return next((kw for kw in node.keywords if kw.arg == "behavior"), None)


def _is_literal_id(kw: ast.keyword | None) -> bool:
    return kw is not None and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str) \
        and bool(kw.value.value)


def annotated_check_behaviors() -> set[str]:
    """Behavior IDs annotated on check() calls. Static — see check()'s docstring for why."""
    return {str(_behavior_kw(n).value.value) for n in _check_calls()  # type: ignore[union-attr]
            if _is_literal_id(_behavior_kw(n))}


def unannotated_check_sites() -> list[int]:
    """Line numbers of check() calls with no behavior= a static reader can resolve.

    A `behavior=` that is a name or expression rather than a string literal counts as UNANNOTATED
    here, because it is invisible to annotated_check_behaviors() — and the two scanners disagreeing
    would fire a false "no check() call carries behavior=X" on a call that demonstrably does. They are
    kept in lockstep through _is_literal_id(); non_literal_check_behaviors() reports the offender by
    line so the failure explains itself instead of pointing at the registry.
    """
    return sorted(n.lineno for n in _check_calls() if not _is_literal_id(_behavior_kw(n)))


def non_literal_check_behaviors() -> list[int]:
    """Line numbers of check() calls whose behavior= exists but is not a string literal."""
    return sorted(n.lineno for n in _check_calls()
                  if _behavior_kw(n) is not None and not _is_literal_id(_behavior_kw(n)))


# ---------------------------------------------------------------- 17. behavior coverage registry
def test_behaviors() -> None:
    section("17. Behavior coverage registry")
    reg = ROOT / "tests" / "behaviors.md"
    if not reg.exists():
        check("tests/behaviors.md exists", False, "registry missing", behavior="REPO-21")
        return
    parsed, malformed = parse_behaviors(reg)
    check("registry has rows", bool(parsed), "no well-formed rows parsed", behavior="REPO-21")
    for bid, detail in malformed:
        check(f"{bid} row is well-formed", False, detail, behavior="REPO-22")

    rows: dict[str, dict[str, str]] = {}
    for bid, meta in parsed:
        if bid in rows:
            check(f"{bid} unique", False, "duplicate ID — IDs are permanent and never reused",
                  behavior="REPO-23")
        rows[bid] = meta

    # rule 1 — known area, resolvable "Stated in"
    for bid, meta in sorted(rows.items()):
        check(f"{bid} area known", bid.split("-")[0] in BEHAVIOR_AREAS,
              f"unknown prefix {bid.split('-')[0]!r}", behavior="REPO-24")
        stated = meta["stated_in"]
        if stated != "repo policy":
            check(f"{bid} stated-in resolves", (SRC / stated).exists(), f"no such file: src/{stated}",
                  behavior="REPO-25")

    # rule 3 — structural, both directions
    annotated = annotated_check_behaviors()
    marked = {bid for bid, meta in rows.items() if covered_tokens(meta["covered"])[1]}
    for bid in sorted(annotated - marked):
        check(f"check behavior {bid} is registered", False,
              "annotated in run.py but its row is missing or does not carry the `check` marker",
              behavior="REPO-26")
    for bid in sorted(marked - annotated):
        check(f"{bid} `check` marker is backed", False,
              f'row claims a structural check, but no check() call carries a literal '
              f'behavior="{bid}"', behavior="REPO-26")
    for lineno in non_literal_check_behaviors():
        check(f"run.py:{lineno} behavior= is a string literal", False,
              "check #17 reads behavior= from source; a name or expression is invisible to it",
              behavior="REPO-27")

    # rule 2 — eval, both directions
    # An import failure must not swallow the rules that follow. Rules 4 and 6 and the annotation gate
    # do not touch SCENARIOS, and silently skipping them would hide a real regression behind an
    # unrelated eval-suite breakage — including rule 4, the gate that replaces old check #9.
    sys.path.insert(0, str(ROOT / "tests" / "eval"))
    scenarios_loaded = True
    try:
        from scenarios import SCENARIOS  # type: ignore
    except Exception as e:  # noqa: BLE001
        check("load eval scenarios", False, str(e), behavior="REPO-28")
        SCENARIOS = []  # type: ignore[assignment]
        scenarios_loaded = False
    keys = {s.key for s in SCENARIOS}
    declared: dict[str, set[str]] = {}
    for s in SCENARIOS:
        for bid in s.behaviors:
            declared.setdefault(bid, set()).add(s.key)

    if scenarios_loaded:
        for bid in sorted(declared):
            check(f"scenario behavior {bid} registered", bid in rows,
                  "named in a scenario's behaviors= but absent from behaviors.md",
                  behavior="REPO-28")

        for bid, meta in sorted(rows.items()):
            pats, _ = covered_tokens(meta["covered"])
            matched: set[str] = set()
            for pat in sorted(pats):
                hits = {k for k in keys if fnmatch.fnmatch(k, pat)}
                check(f"{bid} eval:{pat} matches a scenario", bool(hits), "no scenario key matches",
                      behavior="REPO-28")
                matched |= hits
            back = declared.get(bid, set())
            for k in sorted(matched - back):
                check(f"{bid} ↔ {k}", False,
                      f"row cites {k}, but that scenario's behaviors= does not name {bid}",
                      behavior="REPO-28")
            for k in sorted(back - matched):
                check(f"{bid} ↔ {k}", False,
                      f"scenario {k} names {bid}, but the row does not cite it",
                      behavior="REPO-28")

    # rule 4 — every functional file is stated by at least one behavior.
    # This is what replaces old check #9's registration gate: add a brain file and name no behavior
    # for it, and the suite still fails.
    stated = {meta["stated_in"] for meta in rows.values()}
    for rel in sorted(required_functional_files() - stated):
        check(f"{rel} named by a behavior", False,
              "no behaviors.md row states it — name what the file promises, then cover it",
              behavior="REPO-31")

    # rule 5 — no orphan scenarios (the ONLY later rule that needs SCENARIOS)
    claimed = set().union(*declared.values()) if declared else set()
    for k in sorted(keys - claimed) if scenarios_loaded else []:
        check(f"scenario '{k}' claimed by a behavior", False,
              "orphan — add it to a row's Covered by and to its behaviors=",
              behavior="REPO-32")

    # annotation completeness — every check() call site carries a behavior=. This gate covers itself:
    # the three checks added here are annotated like every other, so removing their rows fails rule 3.
    for lineno in unannotated_check_sites():
        check(f"run.py:{lineno} check() annotated", False, "missing behavior=",
              behavior="REPO-33")

    # rule 6 — the gap report. Never fatal: a gap you can see is the point of this file, and failing
    # on it would only buy a thin test written to clear the cell.
    untested = sorted(bid for bid, meta in rows.items() if not meta["covered"].strip())
    print(f"\n  ℹ️  {len(rows)} behaviors registered, {len(untested)} untested")
    tallies: dict[str, tuple[int, int, int]] = {}
    for area in {b.split("-")[0] for b in rows}:
        n = sum(1 for b in rows if b.split("-")[0] == area)
        gaps = sum(1 for b in rows if b.split("-")[0] == area and not rows[b]["covered"].strip())
        tallies[area] = (n, n - gaps, gaps)
    # Per-area breakdown, printed so behaviors.md's hand-maintained summary table is verifiable
    # against a run at a glance. Two hand-kept copies would drift the first time someone adds a row
    # without touching the table.
    for area in sorted(BEHAVIOR_AREAS):
        if area in tallies:
            print(f"      {area:<5} {tallies[area][0]:>3} rows  {tallies[area][1]:>3} covered  "
                  f"{tallies[area][2]:>3} gaps")
    if untested:
        print(f"      untested: {', '.join(untested)}")

    # rule 7 — the summary table is a CHECKSUM on the rows, not decoration: it is the only thing that
    # notices a gap row going missing. See parse_coverage_summary() for why gap rows are the hole.
    tallies["Total"] = tuple(sum(c) for c in zip(*tallies.values()))  # type: ignore[assignment]
    summary = parse_coverage_summary(reg)
    for key in sorted(set(summary) | set(tallies)):
        check(f"summary table {key} matches the rows", summary.get(key) == tallies.get(key),
              f"table says {summary.get(key)}, rows say {tallies.get(key)} (rows/covered/gaps)",
              behavior="REPO-34")


# ---------------------------------------------------------------- 1. frontmatter
def test_frontmatter() -> None:
    section("1. Frontmatter validity")
    required = {"name", "description", "type"}
    names: dict[str, Path] = {}
    for p in brain_md_files():
        rel = p.relative_to(ROOT)
        fm = parse_frontmatter(p)
        if fm is None:
            check(f"{rel} has frontmatter", False, "no leading --- block", behavior="REPO-01")
            continue
        missing = required - fm.keys()
        check(f"{rel} required keys", not missing,
              f"missing {sorted(missing)}" if missing else "", behavior="REPO-01")
        # layer/version were removed from the schema: tree is implied by path, release lives in
        # VERSION. Guard so they can't creep back into brain frontmatter.
        strays = {"layer", "version"} & fm.keys()
        check(f"{rel} no layer/version", not strays,
              f"remove {sorted(strays)}" if strays else "", behavior="REPO-02")
        check(f"{rel} type valid", fm.get("type") in ALLOWED_TYPES,
              f"type={fm.get('type')!r}", behavior="REPO-03")
        nm = fm.get("name", "")
        if nm in names:
            check(f"{rel} name unique", False,
                  f"'{nm}' also in {names[nm].relative_to(ROOT)}", behavior="REPO-04")
        else:
            names[nm] = p


# ---------------------------------------------------------------- 2. index completeness
def test_index() -> None:
    """Every brain file is REACHABLE from index.md by link traversal — not necessarily listed in it.

    Transitive, not direct, because the index is a router for what to load on demand and not every
    file is independently routable. `onboarding/steps/*` are only ever reached from
    `onboarding/flow.md` when the interview arrives at that step; listing them in the index would
    both cost tokens in an always-loaded file and imply a load trigger they don't have.

    This is the same invariant the brain already asks of the principal's own tree
    (`brain/schemas/memory-file.md` → "Reachability invariant"), and it is strictly stronger than
    the old direct-listing check at what that check was for: catching orphans in nested trees.
    """
    section("2. Index completeness (reachable from brain/index.md)")
    index = BRAIN / "index.md"

    def links_in(p: Path) -> set[str]:
        """Markdown links to .md files, resolved relative to the linking file, brain-relative."""
        out = set()
        for href in re.findall(r"\]\(([^)]+\.md)\)", p.read_text(encoding="utf-8")):
            target = (p.parent / href.split("#")[0]).resolve()
            try:
                out.add(target.relative_to(BRAIN.resolve()).as_posix())
            except ValueError:
                pass                      # points outside brain/ — check 3 owns that case
        return out

    # walk the graph from the index
    reachable: set[str] = set()
    queue = sorted(links_in(index))
    direct = set(queue)
    while queue:
        rel = queue.pop()
        if rel in reachable:
            continue
        reachable.add(rel)
        p = BRAIN / rel
        if p.exists():
            queue.extend(sorted(links_in(p) - reachable))

    for rel in sorted(direct):
        check(f"index → {rel} exists", (BRAIN / rel).exists(), "missing target",
              behavior="REPO-06")
    for p in brain_md_files():
        if p.name == "index.md":
            continue
        rel = p.relative_to(BRAIN).as_posix()
        check(f"{rel} reachable from index", rel in reachable,
              "no link path from brain/index.md — an orphan the router can never load",
              behavior="REPO-05")


# ---------------------------------------------------------------- 3. link resolution
def test_links() -> None:
    section("3. Link resolution")
    link_re = re.compile(r"\]\(([^)]+)\)")
    fixtures = (ROOT / "tests" / "fixtures").resolve()
    problems = 0
    for p in tracked_md_files():
        if p.resolve().is_relative_to(fixtures):
            continue  # static fixture memory trees — test data, not product links to validate
        body = strip_code_fences(p.read_text(encoding="utf-8"))
        body = re.sub(r"`[^`]*`", "", body)  # drop inline-code example links
        for raw in link_re.findall(body):
            href = raw.split()[0].strip()  # drop optional title
            if href.startswith(("http://", "https://", "#", "mailto:")):
                continue
            href = href.split("#", 1)[0]
            if not href or not href.endswith(".md"):
                continue
            if href.startswith("memory/") or "/memory/" in href:
                continue  # runtime-created
            target = (p.parent / href).resolve()
            if not target.exists():
                problems += 1
                check(f"{p.relative_to(ROOT)} → {href}", False, "dangling link",
                      behavior="REPO-07")
    check("all in-repo markdown links resolve", problems == 0, f"{problems} dangling",
          behavior="REPO-07")


# ---------------------------------------------------------------- 4. naming guards
def test_naming() -> None:
    section("4. Naming consistency (regression guards)")
    stale = re.compile(r"\b(canonical|instance)\b", re.IGNORECASE)
    # "canonical action(s)" is sanctioned connector-discovery vocabulary (the provider's real action
    # names) — exempt only that exact phrase; a stray "canonical"/"instance" anywhere else still fails.
    allowed = re.compile(r"canonical\s+actions?\b", re.IGNORECASE)
    wiki = re.compile(r"\[\[")
    stale_hits, wiki_hits = [], []
    # Files that legitimately DESCRIBE the guard rather than being governed by it: this suite
    # documents the banned words, and the root dev specialists (.agents/personas/) are prompts that
    # explain conventions (including this one) to an agent — plus "canonical" is unrelated, ordinary
    # SEO vocabulary there (`<link rel="canonical">`), not the brain's naming convention.
    EXEMPT_DIRS = (ROOT / "tests", ROOT / ".agents" / "personas")
    for p in tracked_md_files():
        if any(p.resolve().is_relative_to(d.resolve()) for d in EXEMPT_DIRS):
            continue
        text = p.read_text(encoding="utf-8")
        # drop md emphasis so bold (**canonical** action) doesn't split the sanctioned phrase, then
        # remove that phrase before scanning for stray terminology.
        scan = allowed.sub("", re.sub(r"[*_]", "", text))
        if stale.search(scan):
            stale_hits.append(str(p.relative_to(ROOT)))
        if wiki.search(text):
            wiki_hits.append(str(p.relative_to(ROOT)))
    check("no 'canonical'/'instance' terminology", not stale_hits, ", ".join(stale_hits),
          behavior="REPO-08")
    check("no [[wikilinks]]", not wiki_hits, ", ".join(wiki_hits), behavior="REPO-09")


# ---------------------------------------------------------------- 4b. connector-discovery contract
def test_connectors_contract() -> None:
    """The connector/plugin discovery policy is a behavioral contract we ship. The eval sandbox runs
    with --strict-mcp-config (no real connectors), so it can't exercise lazy tool exposure; instead we
    assert the contract's load-bearing anchors are present so it can't silently regress. Tokens are
    matched case-insensitively against the file text (md emphasis stripped)."""
    section("4b. Connector-discovery contract (both hosts)")

    def scannable(rel: str) -> str:
        # strip md emphasis and collapse whitespace so line-wrapped phrases ("fresh\n  session") match
        raw = re.sub(r"[*_`]", "", (BRAIN / rel).read_text(encoding="utf-8"))
        return re.sub(r"\s+", " ", raw).lower()

    # The two files are asserted in separate loops so each can carry its own literal `behavior=`:
    # the host-neutral contract is HOST-02, the per-host procedures are HOST-35. A shared helper
    # would have to pass `behavior` through as a name, which check #17 cannot read (REPO-27).
    rel = "integrations/connectors.md"  # host-neutral shared contract
    text = scannable(rel)
    for tok in ["inconclusive", "at least two", "canonical", "not yet surfaced",
                "authentication required", "connection failure", "genuinely unavailable",
                "fallback order", "browser or computer-use", "graceful degradation", "resume",
                "disconnected"]:
        check(f"{rel} states '{tok}'", tok.lower() in text, "discovery-contract anchor missing",
              behavior="HOST-02")
    # The Codex half of the status check used to name only the Plugins tab — a UI the agent has no
    # way to read, so it arrived at "check what's connected" with nothing to run and fell through to
    # asking the principal. Reported from a real Codex onboarding that called a live Gmail
    # "unverified". These anchor the executable check that replaced it.
    # "callable tools" alone is NOT a valid anchor here: the phrase already appears further down
    # ("a host's callable tools can be exposed lazily"), so a check on it passes green with this
    # bullet deleted. Caught by introducing the violation, per AGENTS.md doctrine #4.
    for tok in ["inspecting your callable tools", "positive evidence", "read-only status or profile"]:
        check(f"{rel} states '{tok}'", tok.lower() in text,
              "the Codex status check must name an action the agent can run, not a UI tab",
              behavior="HOST-37")

    rel = "integrations/hosts.md"  # per-host procedures (host logic must not leak across hosts)
    text = scannable(rel)
    for tok in ["connector/plugin discovery", "/mcp", "needs-auth", "failed", "pending", "connected",
                "deferred", "canonical action", "blocked", "login", "disconnected", "fresh session"]:
        check(f"{rel} states '{tok}'", tok.lower() in text, "discovery-contract anchor missing",
              behavior="HOST-35")


# ---------------------------------------------------------------- 5. release metadata
def test_release_metadata() -> None:
    section("5. Release metadata")
    # Brain files no longer carry a per-file version — the release lives solely in VERSION (+ its
    # CHANGELOG header). (The stray-key guard in check #1 keeps `version:` out of brain frontmatter.)
    version = (SRC / "VERSION").read_text(encoding="utf-8").strip()
    check("VERSION non-empty", bool(version), "empty VERSION file", behavior="REL-02")
    changelog = (SRC / "CHANGELOG.md").read_text(encoding="utf-8")
    # `main` carries a `-dev` pre-release suffix between releases (e.g. `0.12.0-dev`); that work lives
    # under `## [Unreleased]`. A clean release VERSION must have its own `## [x.y.z]` header.
    if "-" in version:  # pre-release / dev build
        check("CHANGELOG has [Unreleased] (dev VERSION)", "[Unreleased]" in changelog,
              f"VERSION {version!r} is a -dev build but no ## [Unreleased] section",
              behavior="REL-03")
    else:
        check(f"CHANGELOG has [{version}]", f"[{version}]" in changelog, "no matching version header",
              behavior="REL-01")
        # Cutting a release FORCES a migration decision. The convention was unenforced, and that is
        # exactly how 0.15.0 shipped the removal of the per-specialist `clearance:`/`## Reads` charter
        # fields with no statement at all — the first-boot pass migrated straight past it. Silence is
        # no longer an answer: the section must carry a `### Migration notes` block saying something,
        # even if that something is "No action required." (which 0.20.0 and 0.22.0 already do).
        #
        # This one inspects only the version currently in VERSION, and stays quiet on `-dev` so
        # day-to-day work is unaffected. Every other entry is covered by the total pass below.
        body = changelog.split(f"## [{version}]", 1)[-1].split("\n## [", 1)[0]
        check(f"[{version}] states its migration position",
              "### Migration notes" in body,
              "a release must carry a ### Migration notes block — say 'No action required.' if so, "
              "but say it (CONTRIBUTING.md -> Migration directive)",
              behavior="REL-01")

    # Every entry states a migration position, not just the one in VERSION. The original check was
    # deliberately narrow ("so history needs no retroactive churn"); the 0.30.0 backfill did that
    # churn, and two silent releases (0.15.0's clearance/## Reads, 0.18.0's persona rename) are why
    # it was worth doing. The migration pass resolves a span by walking entries oldest->newest and
    # keeping the newest statement per subject key, so a missing block is a hole in that walk.
    CLASSES = ("**No action required.**", "**Required — writes at boot.**",
               "**Required — no write.**", "**Optional convergence.**")
    SCOPES = {"charter", "meta", "frontmatter", "path", "preference", "member", "override"}
    key_re = re.compile(r"^- \*\*`([a-z]+):([A-Za-z0-9_./<>-]+)`\*\*")
    # A prefix test ("- **`") cannot distinguish a subject key from ordinary bold-code-span prose:
    # 0.19.0's own entry opens two lines that way — `**`memory/integrations.md` (new, ...)**` and
    # `**`memory/meta.md` gains ...**` — and that release's account may not be edited to satisfy this
    # check. Require the colon-joined `scope:name` shape inside the span before treating a line as a
    # key candidate. Accepted tradeoff: a key whose *name* contains whitespace is now skipped silently
    # rather than reported malformed — verified against every line matching the old prefix in this
    # file: 39 genuine keys matched, 10 non-keys rejected, no new false positive or negative.
    key_candidate = re.compile(r"^- \*\*`[^`\s]+:[^`\s]+`\*\*")
    sup_re = re.compile(r"\*\*Supersedes ([0-9]+\.[0-9]+\.[0-9]+)\.\*\*")

    def _vkey(v: str) -> tuple:
        return (999, 999, 999) if v == "Unreleased" else tuple(int(x) for x in v.split("."))

    sections = re.split(r"^## \[", changelog, flags=re.M)[1:]
    entries = {s.split("]", 1)[0]: s for s in sections}
    check("CHANGELOG has entries to scan", bool(entries), "no ## [x.y.z] sections found",
          behavior="REL-31")
    chains: dict = {}  # subject key -> [(entry version, does its bullet declare a supersede)]
    for ver, body in entries.items():
        # The legacy `### Migration` heading is accepted: older entries used it, and moving or
        # renaming one would be rewriting history (CONTRIBUTING.md -> Don't rewrite history).
        # findall, not search: a duplicated block is how a backfill goes wrong quietly, and the pass
        # would only ever read the first one.
        blks = re.findall(r"^### Migration(?: notes)?\s*$(.*?)(?=^### |\Z)", body, re.M | re.S)
        check(f"[{ver}] has a migration block", bool(blks),
              "every entry must state a migration position (CONTRIBUTING.md -> Migration directive)",
              behavior="REL-31")
        if not blks:
            continue
        check(f"[{ver}] has exactly one migration block", len(blks) == 1,
              f"found {len(blks)}; the pass reads only the first, so a second is dead text",
              behavior="REL-31")
        blk = blks[0]
        first = next((ln for ln in blk.splitlines() if ln.strip()), "")
        check(f"[{ver}] opens with a classification line",
              any(first.startswith(c) for c in CLASSES),
              f"first line must be one of {CLASSES} (em-dash, not hyphen) - got {first[:60]!r}",
              behavior="REL-32")
        # Group the block into bullets before reading keys: a `**Supersedes X.Y.Z.**` almost always
        # lands on a wrapped continuation line, so the key and its supersede have to be read together.
        bullets: list = []
        cur = None
        for ln in blk.splitlines():
            if ln.startswith("- "):
                cur = [ln]
                bullets.append(cur)
            elif cur is not None and ln.startswith("  ") and ln.strip():
                cur.append(ln)
            else:
                cur = None
        for bullet in bullets:
            ln = bullet[0]
            if key_candidate.match(ln):
                km = key_re.match(ln)
                check(f"[{ver}] subject key well-formed", km is not None,
                      f"expected - **`<scope>:<name>`** - got {ln[:60]!r}", behavior="REL-33")
                if km:
                    check(f"[{ver}] subject scope {km.group(1)!r} known", km.group(1) in SCOPES,
                          f"scope must be one of {sorted(SCOPES)}", behavior="REL-33")
                    chains.setdefault(f"{km.group(1)}:{km.group(2)}", []).append(
                        (ver, bool(sup_re.search("\n".join(bullet)))))
        for sup in sup_re.findall(blk):
            check(f"[{ver}] supersedes {sup}, which exists", sup in entries,
                  "a supersede must name a real entry", behavior="REL-34")
            if sup in entries:
                check(f"[{ver}] supersedes {sup}, which is older", _vkey(sup) < _vkey(ver),
                      "supersession is forward-only: the later entry names the earlier one",
                      behavior="REL-34")

    # A key appearing on more than one entry IS an order-dependent chain — that repetition is the only
    # way the file has of expressing one. The pass keeps the newest statement per key and discards the
    # rest, so the newest bullet has to be written to cover everything the earlier ones said; declaring
    # `**Supersedes X.Y.Z.**` is what forces that to be a decision rather than an accident. Without it
    # nothing distinguishes a deliberate chain from two unrelated subjects that happen to share a key,
    # and the older statement is dropped in silence — which is how 0.12.0's `_quarantined/` relocation
    # was nearly lost behind 0.13.0's reachability exemption for the same path.
    for key, occs in sorted(chains.items()):
        if len(occs) < 2:
            continue
        seen = ", ".join(v for v, _ in sorted(occs, key=lambda o: _vkey(o[0])))
        newest_ver, declared = max(occs, key=lambda o: _vkey(o[0]))
        check(f"chain {key!r} declares its supersede at [{newest_ver}]", declared,
              f"stated on {seen}; the newest statement wins the span walk, so it must say "
              "**Supersedes X.Y.Z.** and cover what the earlier ones said "
              "(CONTRIBUTING.md -> Migration directive)",
              behavior="REL-39")


# ---------------------------------------------------------------- 6. override targets
def test_override_targets() -> None:
    section("6. Override-target mirror paths")
    text = (BRAIN / "role" / "defaults.md").read_text(encoding="utf-8")
    targets = set(re.findall(r"memory/overrides/([A-Za-z0-9_./-]+\.md)", text))
    check("defaults.md declares override targets", bool(targets), "none found",
          behavior="ROLE-05")
    for rel in sorted(targets):
        mirror = BRAIN / rel
        check(f"override memory/overrides/{rel} mirrors brain/{rel}", mirror.exists(),
              "no brain counterpart", behavior="ROLE-05")


# ---------------------------------------------------------------- 7. slash commands
def test_commands() -> None:
    section("7. Slash-command validity")
    cmds = sorted(COMMANDS.glob("*.md"))
    check("slash commands exist", bool(cmds), "no .claude/commands/*.md", behavior="REPO-10")
    for p in cmds:
        fm = parse_frontmatter(p) or {}
        check(f"{p.name} has description", bool(fm.get("description")), "missing description",
              behavior="REPO-10")
        body = p.read_text(encoding="utf-8")
        for ref in re.findall(r"`(brain/[A-Za-z0-9_./-]+\.md)`", body):
            check(f"{p.name} → {ref}", (SRC / ref).exists(), "referenced brain path missing",
                  behavior="REPO-11")
    # CLAUDE.md, AGENTS.md, and CHIEFOFSTAFF.md are functional too — their inline `brain/…` refs must resolve
    for fname in ("CLAUDE.md", "AGENTS.md", "CHIEFOFSTAFF.md"):
        text = (SRC / fname).read_text(encoding="utf-8")
        for ref in sorted(set(re.findall(r"`(brain/[A-Za-z0-9_./-]+\.md)`", text))):
            check(f"{fname} → {ref}", (SRC / ref).exists(), "referenced brain path missing",
                  behavior="REPO-11")


# ---------------------------------------------------------------- 7b. neutral skills parity
def test_neutral_skills() -> None:
    """`.agents/skills/<name>/SKILL.md` and `.claude/commands/<name>.md` are two independent
    delegations into the same brain file — one for the vendor-neutral location other tools read, one
    for Claude Code. Neither is generated from the other, so nothing stops one side being added,
    renamed, or re-described alone. This is that guard."""
    section("7b. Neutral skills mirror the slash commands")

    skills = {p.parent.name: p for p in SKILLS.glob("*/SKILL.md")}
    cmds = {p.stem: p for p in COMMANDS.glob("*.md")}
    check("every slash command has a neutral skill", not (set(cmds) - set(skills)),
          f"missing under .agents/skills/: {sorted(set(cmds) - set(skills))}", behavior="REPO-36")
    check("every neutral skill has a slash command", not (set(skills) - set(cmds)),
          f"missing under .claude/commands/: {sorted(set(skills) - set(cmds))}", behavior="REPO-36")
    for name in sorted(set(skills) & set(cmds)):
        sfm = parse_frontmatter(skills[name]) or {}
        cfm = parse_frontmatter(cmds[name]) or {}
        check(f"{name}: one description, both sides",
              sfm.get("description") == cfm.get("description"),
              "the two sides describe the same command differently", behavior="REPO-36")
        check(f"{name}: frontmatter name matches its directory", sfm.get("name") == name,
              f"got {sfm.get('name')!r}", behavior="REPO-37")
        for ref in re.findall(r"`(brain/[A-Za-z0-9_./-]+\.md)`", skills[name].read_text(encoding="utf-8")):
            check(f"{name} → {ref}", (SRC / ref).exists(), "referenced brain path missing",
                  behavior="REPO-37")
        check(f"{name}: same body on both sides",
              frontmatter_body(skills[name]) == frontmatter_body(cmds[name]),
              "the two published copies diverged in body text", behavior="REPO-38")


# ---------------------------------------------------------------- 8. gitignore behavior
def test_gitignore() -> None:
    section("8. Gitignore behavior")

    def ignored(rel: str) -> bool:
        # core.excludesFile=/dev/null disables the developer's PERSONAL global ignore file. Without
        # it this check reports what's ignored on one machine rather than what this repo guarantees —
        # which is how `src/.claude/settings.local.json` once looked covered here while being covered
        # only by a global `**/.claude/…` rule that CI and every other clone lacked.
        r = subprocess.run(
            ["git", "-C", str(ROOT), "-c", "core.excludesFile=/dev/null", "check-ignore", "-q", rel],
            check=False)
        return r.returncode == 0

    check("memory/ contents ignored", ignored("src/memory/scratch-probe.md"), "not ignored",
          behavior="REPO-12")
    check("memory/.keep tracked", not ignored("src/memory/.keep"), "unexpectedly ignored",
          behavior="REPO-12")
    check("brain/ tracked", not ignored("src/brain/index.md"), "brain unexpectedly ignored",
          behavior="REPO-13")
    check("commands tracked", not ignored("src/.claude/commands/onboard.md"), "commands must ship",
          behavior="REPO-13")
    # Local runtime state must be ignored in BOTH trees — the repo root (working on Chief of Staff) and
    # src/ (running it from the source tree). A rule with a mid-path slash is anchored to the repo
    # root, so these need `**/`; asserting both sides is what catches that mistake.
    for tree in ("", "src/"):
        where = "root" if not tree else "src"
        check(f"settings.local.json ignored ({where})",
              ignored(f"{tree}.claude/settings.local.json"), "not ignored", behavior="REPO-14")
        check(f"scheduled_tasks.lock ignored ({where})",
              ignored(f"{tree}.claude/scheduled_tasks.lock"), "not ignored", behavior="REPO-14")
    # Agents split by tree (unlike the rule above): root .agents/personas/ holds the versioned
    # development specialists — tracked, not ignored (`.claude/agents` is a symlink to it).
    # src/.claude/agents/ holds the generated per-principal shims — runtime output, always ignored.
    check("dev specialists tracked (root)", not ignored(".agents/personas/brain-rigor-critic.md"),
          "unexpectedly ignored", behavior="REPO-15")
    check("generated agents ignored (src)", ignored("src/.claude/agents/probe.md"), "not ignored",
          behavior="REPO-15")


# ---------------------------------------------------------------- 8b. dev/dist boundary
def test_site_not_in_src() -> None:
    """No web tooling may take root in `src/`.

    `scripts/build-dist.sh` is `cp -R src/. "$STAGE/"` — whatever sits in `src/` ships to executives
    inside `cos.zip`. This check was written when the site lived in this repo and an Astro project
    rooted here would have created `src/pages/`, `src/layouts/`, `src/content/` and shipped every one
    of them into a principal's folder. The site has its own repo now, so that specific accident is
    gone, but the assertion is kept and costs nothing: `src/` is the manifest, and any tool that
    claims these conventional directory names would ship its scaffolding to every principal.

    Nothing else would catch it. The link checker only looks at markdown, and the archive-shape check
    counts files rather than naming them, so a stray `src/pages/` would ship silently.
    """
    section("9b. No web tooling takes root in src/ (it would ship inside cos.zip)")
    forbidden = ["pages", "layouts", "components", "content", "styles"]
    for name in forbidden:
        check(f"src/{name}/ absent", not (ROOT / "src" / name).is_dir(),
              f"Astro convention directory inside the shipped tree — it would land in cos.zip",
              behavior="REPO-16")
    for pat in ("content.config.*", "astro.config.*", "package.json"):
        hits = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "src").glob(pat))
        check(f"src/{pat} absent", not hits, f"found {hits}", behavior="REPO-16")


def test_dist_boundary() -> None:
    """`src/` is the artifact: it's copied verbatim into the ZIP, so it must be self-contained.

    The link checker (#3) already catches a broken *link* out of `src/`. This catches the other half —
    prose that names something the user doesn't have (`CONTRIBUTING.md`, `tests/run.py check #12`,
    `.gitignore`) or that explains the product in terms of the repo that built it ("a fresh clone", "a
    git pull"). Both were invisible before the split, because the suite only ever saw the dev tree.
    """
    section("8b. Dev/dist boundary (src/ is self-contained)")

    # Paths that exist only in the development repo, plus source-control framing an installed folder
    # has no notion of. Matched case-insensitively against prose with code fences stripped.
    FORBIDDEN = [
        ("CONTRIBUTING.md", "the developer guide isn't shipped"),
        ("tests/", "the test suite isn't shipped"),
        ("scripts/", "build scripts aren't shipped"),
        (".github/", "CI config isn't shipped"),
        (".gitignore", "there's no .gitignore in an install"),
        ("git-ignored", "an install isn't a git repo — say what's true of the folder"),
        ("git pull", "an install updates via /update, not git"),
        ("git clone", "an install is unzipped, not cloned"),
        ("fresh clone", "an install is unzipped, not cloned"),
    ]
    # CHANGELOG.md is exempt: it is released history, and CONTRIBUTING.md forbids rewriting it. Its
    # older entries legitimately describe the repo as it was.
    EXEMPT = {"CHANGELOG.md"}

    # The substring tokens above are defeated by punctuation: the tree read `git` pull — with the
    # words separated by a backtick — for four releases, and "git pull" never matched. A word-boundary
    # regex catches the tool by name however it is marked up, and provably without false positives:
    # GitHub/GitLab (connectors), .keep, "legitimate" and "digits" all fail the trailing boundary.
    GIT_RE = re.compile(r"\bgit\b", re.I)

    shipped = sorted(p for p in SRC.rglob("*.md") if p.relative_to(SRC).as_posix() not in EXEMPT)
    check("src/ has shipped markdown to scan", bool(shipped), "no .md found under src/",
          behavior="REPO-17")
    for p in shipped:
        rel = p.relative_to(SRC).as_posix()
        raw = strip_code_fences(p.read_text(encoding="utf-8"))
        body = raw.lower()
        for token, why in FORBIDDEN:
            check(f"{rel} omits '{token}'", token.lower() not in body, why, behavior="REPO-17")
        hit = GIT_RE.search(raw)
        check(f"{rel} never names git", hit is None,
              f"'{hit.group(0)}' — an install is an unzipped folder, not a checkout" if hit else "",
              behavior="REPO-17")


# ---------------------------------------------------------------- 8c. the /update copy-list delivers all of src/
def test_update_delivers_src() -> None:
    """An existing install updates itself by running the copy recipe in the brain it already has. If a
    file is added to `src/` but not to that recipe, the ZIP ships it and **no existing install ever
    receives it** — a silent, permanent drift that used to be caught by nobody. Assert the recipe names
    every top-level entry of the artifact."""
    section("8c. /update delivers everything in src/")

    recipe = (BRAIN / "integrations" / "updates.md").read_text(encoding="utf-8")
    # Every shipped top-level entry must be named in the recipe, dotted or not, file or directory. The
    # old form admitted a dotted entry only if it was a directory, so a dotted top-level FILE (e.g. a
    # future src/.mcp.json) was skipped silently and could be left out of the recipe with a green
    # suite — the exact drift this check exists to catch. .DS_Store is a Finder artifact, never
    # shipped, and excluded explicitly rather than by the dotted-file rule it would otherwise trip.
    top = {p.name for p in SRC.iterdir() if p.name != ".DS_Store"}
    for entry in sorted(top):
        # memory/ is the one entry deliberately NOT delivered: it's the principal's data, and the
        # update must never touch it. Assert that intent explicitly rather than skipping silently.
        if entry == "memory":
            check("updates.md never copies memory/", "never touches `memory/`" in recipe,
                  "the freeze on the principal's data must stay stated", behavior="REL-04")
            continue
        check(f"updates.md delivers {entry}", entry in recipe,
              "shipped in the ZIP but the /update recipe never copies it — existing installs would never get it",
              behavior="REL-05")


# ---------------------------------------------------------------- 8d. published archive shapes
def test_archive_shapes() -> None:
    """The prompt boot says "unzip it into this folder", which is only true if `cos.zip` is
    FLAT. And `ChiefOfStaff.zip` must stay NESTED: installs predating 0.20.0 run an /update recipe that
    hardcodes `$tmp/ChiefOfStaff`, and that recipe lives in the brain already on their disk, so it can
    never be corrected remotely. Getting either shape wrong silently strands real users, so build both
    and look inside."""
    section("8d. Published archive shapes")

    if not shutil.which("zip"):
        check("zip available to verify archives", False, "install `zip` (the release build needs it)",
              behavior="REL-06")
        return

    with tempfile.TemporaryDirectory() as td:
        r = subprocess.run(["bash", str(ROOT / "scripts" / "build-dist.sh")], cwd=str(ROOT),
                           env={**os.environ, "DIST_OUT": td},
                           capture_output=True, text=True, check=False)
        if r.returncode != 0:
            check("build-dist.sh succeeds", False, (r.stderr or r.stdout).strip()[:200],
                  behavior="REL-06")
            return
        check("build-dist.sh succeeds", True, behavior="REL-06")

        flat = Path(td) / "cos.zip"
        nested = Path(td) / "ChiefOfStaff.zip"
        check("cos.zip built", flat.exists(), "missing", behavior="REL-06")
        check("ChiefOfStaff.zip built", nested.exists(), "missing", behavior="REL-06")
        if not (flat.exists() and nested.exists()):
            return

        def names(z: Path) -> set[str]:
            with zipfile.ZipFile(z) as zf:
                return {n for n in zf.namelist() if not n.endswith("/")}

        f, n = names(flat), names(nested)
        check("cos.zip is flat (AGENTS.md at top level)", "AGENTS.md" in f, "no top-level AGENTS.md",
              behavior="REL-07")
        check("cos.zip has no wrapper directory",
              not any(x.startswith("ChiefOfStaff/") for x in f), "found a ChiefOfStaff/ prefix",
              behavior="REL-07")
        check("ChiefOfStaff.zip is nested", all(x.startswith("ChiefOfStaff/") for x in n),
              "entries outside the ChiefOfStaff/ wrapper", behavior="REL-08")
        # Same release, two wrappings — never two different payloads.
        check("both archives carry identical contents",
              f == {x[len("ChiefOfStaff/"):] for x in n}, "file sets differ", behavior="REL-09")
        # What the prompt boot actually depends on landing.
        for must in ("AGENTS.md", "CHIEFOFSTAFF.md", "VERSION", "brain/index.md",
                     ".claude/commands/onboard.md", ".agents/skills/onboard/SKILL.md", "memory/.keep"):
            check(f"cos.zip contains {must}", must in f, "missing from the flat archive",
                  behavior="REL-10")


# ---------------------------------------------------------------- 10. onboarding lint (golden fixture)
ONBOARDED = ROOT / "tests" / "fixtures" / "onboarded" / "memory"


def md_link_targets(text: str) -> list[str]:
    """Relative `.md` link hrefs in a body, ignoring fenced/inline code and URLs."""
    body = re.sub(r"`[^`]*`", "", strip_code_fences(text))
    hrefs = []
    for raw in re.findall(r"\]\(([^)]+)\)", body):
        href = raw.split()[0].strip().split("#", 1)[0]
        if href.endswith(".md") and not href.startswith(("http://", "https://", "mailto:")):
            hrefs.append(href)
    return hrefs


def test_onboarding_lint() -> None:
    """A freshly-completed onboarding (the golden fixture) must pass the mechanically-checkable
    memory-lint checks with ZERO findings. If this fails, fix the fixture / onboarding flow — never
    weaken a check (see brain/playbooks/memory-lint.md, brain/onboarding/flow.md)."""
    section("10. Onboarding output passes memory-lint (golden fixture)")
    mem = ONBOARDED
    if not (mem / "index.md").exists():
        check("onboarded fixture exists", False, f"missing {mem}", behavior="REPO-29")
        return

    md_files = sorted(mem.rglob("*.md"))
    relp = {p: p.relative_to(mem).as_posix() for p in md_files}
    texts = {relp[p]: p.read_text(encoding="utf-8") for p in md_files}
    fms = {relp[p]: (parse_frontmatter(p) or {}) for p in md_files}
    by_rel = {relp[p]: p for p in md_files}

    # (0) schema conformance: no removed keys; every memory file carries an `updated:` date
    for p in md_files:
        r, fm = relp[p], fms[relp[p]]
        strays = {"layer", "version"} & fm.keys()
        check(f"{r} no layer/version", not strays, f"remove {sorted(strays)}" if strays else "",
              behavior="ONB-15")
        check(f"{r} has updated date", bool(re.match(r"\d{4}-\d{2}-\d{2}$", fm.get("updated", ""))),
              "missing/invalid `updated:` date", behavior="ONB-14")

    def resolve(src: Path, href: str) -> Path:
        return (src.parent / href).resolve()

    # (a) every index link resolves
    index_links = md_link_targets(texts["index.md"])
    indexed_targets = set()
    for href in index_links:
        t = resolve(by_rel["index.md"], href)
        check(f"index → {href} exists", t.exists(), "missing index target", behavior="ONB-16")
        if t.exists():
            indexed_targets.add(t.resolve())

    # (b) every created file is indexed — except index.md, meta.md, and guarded confidential/**
    for p in md_files:
        r = relp[p]
        if r in ("index.md", "meta.md") or r.startswith("confidential/"):
            continue
        check(f"{r} is indexed", p.resolve() in indexed_targets, "not linked from index.md",
              behavior="ONB-16")

    # (c) all relative links across the tree resolve
    dangling = 0
    for p in md_files:
        for href in md_link_targets(texts[relp[p]]):
            if not resolve(p, href).exists():
                dangling += 1
                check(f"{relp[p]} → {href}", False, "dangling link", behavior="ONB-17")
    check("all fixture links resolve", dangling == 0, f"{dangling} dangling", behavior="ONB-17")

    # helper: directed links from files under one prefix to files under another
    def pairs(src_prefix: str, dst_prefix: str) -> set[tuple[str, str]]:
        out: set[tuple[str, str]] = set()
        for p in md_files:
            if not relp[p].startswith(src_prefix):
                continue
            for href in md_link_targets(texts[relp[p]]):
                t = resolve(p, href)
                if t.exists() and t.is_relative_to(mem):
                    tr = t.relative_to(mem).as_posix()
                    if tr.startswith(dst_prefix):
                        out.add((relp[p], tr))
        return out

    # (d) reciprocal links between people and projects (both directions)
    ppl_prj = pairs("people/", "projects/")
    prj_ppl = pairs("projects/", "people/")
    for person, project in sorted(ppl_prj):
        check(f"reciprocal {project} → {person}", (project, person) in prj_ppl,
              "person links project but project omits the backlink", behavior="ONB-18")
    for project, person in sorted(prj_ppl):
        check(f"reciprocal {person} → {project}", (person, project) in ppl_prj,
              "project links person but person omits the backlink", behavior="ONB-18")

    # (e) provenance: material pages cite a source under log/ (or _processed/)
    def cites_source(p: Path) -> bool:
        for href in md_link_targets(texts[relp[p]]):
            t = resolve(p, href)
            if not (t.exists() and t.is_relative_to(mem)):
                continue
            tr = t.relative_to(mem).as_posix()
            if tr.startswith("log/") or "_processed/" in tr:
                return True
        return False

    material = ["profile/principal.md", "okrs.md"]
    material += [r for r in texts if r.startswith("projects/") and fms[r].get("confidential") != "true"]
    for r in material:
        if r in by_rel:
            check(f"{r} has provenance", cites_source(by_rel[r]),
                  "no source link into log/ or _processed/", behavior="ONB-19")

    # (f) no confidential real identity outside confidential/
    reg = texts.get("confidential/registry.md", "")
    tokens: set[str] = set()
    for line in reg.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower() == "codename" or set(cells[0]) <= set("-: "):
            continue  # header / separator row
        for tok in re.findall(r"\*\*([^*]+)\*\*", cells[1]):  # bold real-identity token(s)
            if len(tok.strip()) >= 4:
                tokens.add(tok.strip())
    check("registry declares a real-identity token", bool(tokens),
          "no **bold** identity in the registry's 'real identity' column", behavior="ONB-20")
    for tok in sorted(tokens):
        leaked = [r for r in texts if not r.startswith("confidential/") and tok in texts[r]]
        check(f"'{tok}' stays inside confidential/", not leaked, f"leaked in {leaked}",
              behavior="ONB-20")

    # (g) no unintended orphans — topical pages need >=1 inbound link
    inbound: dict[str, set[str]] = {}
    for p in md_files:
        for href in md_link_targets(texts[relp[p]]):
            t = resolve(p, href)
            if t.exists() and t.is_relative_to(mem):
                tr = t.relative_to(mem).as_posix()
                if tr != relp[p]:
                    inbound.setdefault(tr, set()).add(relp[p])
    for p in md_files:
        r = relp[p]
        if r.startswith(("people/", "projects/", "context/", "log/")):
            check(f"{r} has an inbound link", bool(inbound.get(r)), "orphan — no memory file links to it",
                  behavior="ONB-21")

    # (h) no duplicate name slugs
    seen: dict[str, str] = {}
    for r, fm in fms.items():
        nm = fm.get("name", "")
        if not nm:
            continue
        if nm in seen:
            check(f"name '{nm}' unique", False, f"{r} duplicates {seen[nm]}", behavior="ONB-22")
        else:
            seen[nm] = r

    # (i) mechanical stale check — no open commitment due before onboarding finished
    m = re.search(r"last_onboarded:\s*(\d{4}-\d{2}-\d{2})", texts.get("meta.md", ""))
    ref = m.group(1) if m else None
    stale = 0
    for line in texts.get("commitments.md", "").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        dm = re.match(r"(\d{4}-\d{2}-\d{2})", cells[2])
        if ref and dm and cells[3].lower() == "open" and dm.group(1) < ref:
            stale += 1
            check(f"commitment '{cells[0]}' not overdue at onboarding", False,
                  f"due {dm.group(1)} < {ref} but still open", behavior="ONB-23")
    check("no stale open commitments at onboarding", stale == 0, f"{stale} overdue",
          behavior="ONB-23")


# ---------------------------------------------------------------- 11. virtual team layout (fixture)
TEAM_FIXTURE = ROOT / "tests" / "fixtures" / "team" / "memory"


_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _section_link_targets(text: str, heading: str) -> list[str]:
    """Markdown link targets under a `## <heading>` section (until the next `##`)."""
    lines = text.splitlines()
    out, in_sec = [], False
    for line in lines:
        if line.startswith("## "):
            in_sec = line[3:].strip().lower().startswith(heading.lower())
            continue
        if in_sec:
            out += _LINK.findall(line)
    return out


def _md_section(text: str, heading: str) -> str:
    """The body of a `## <heading>` section (until the next `##`)."""
    out, in_sec = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            in_sec = line[3:].strip().lower().startswith(heading.lower())
            continue
        if in_sec:
            out.append(line)
    return "\n".join(out)


def test_team_layout() -> None:
    """A virtual-team memory tree (fixture) must satisfy the LINK-BASED team invariants: every active
    specialist is reachable by following links from `memory/index.md` → `memory/team/index.md` (roster) →
    `<slug>/charter.md`, WITHOUT directory enumeration. A specialist carries no boot files of its own
    (it is always run by Chief of Staff); the roster status agrees with the charter `status:`; no team file
    (roster/charter/specialist page) ever links the confidential registry; delegation records are
    well-formed; and no confidential identity leaks. The team is a brain trust — a specialist reads the
    whole shared brain, so there is no per-specialist clearance or cleared-slice check here; the one guard
    is the registry link check. Fix the fixture or brain if this fails — never loosen the check
    (brain/schemas/team-member.md).

    NB: this TEST globs the fixture to VALIDATE it — that is test-side. The PRODUCT must discover the
    team only via links (roster), never by scanning `memory/team/` (asserted by the link graph below)."""
    section("11. Virtual team layout — link-based roster (fixture)")
    mem = TEAM_FIXTURE
    team = mem / "team"
    member_dirs = sorted(p.parent for p in team.glob("*/charter.md")) if team.exists() else []
    if not member_dirs:
        check("team fixture exists", False, f"no specialist charters under {team}", behavior="REPO-30")
        return

    # real-identity tokens from the registry table (for the identity-leak check below)
    identity_tokens: set[str] = set()
    reg = mem / "confidential" / "registry.md"
    if reg.exists():
        for line in reg.read_text(encoding="utf-8").splitlines():
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2 or cells[0].lower() == "codename" or set(cells[0]) <= set("-: "):
                continue
            for tok in re.findall(r"\*\*([^*]+)\*\*", cells[1]):
                if len(tok.strip()) >= 4:
                    identity_tokens.add(tok.strip())

    # (a) reachability: memory/index.md → team/index.md (roster) → charters, all by link
    root_idx = mem / "index.md"
    check("root memory/index.md exists", root_idx.exists(), "no root index to reach the team from",
          behavior="TEAM-01")
    roster = team / "index.md"
    check("team/index.md roster exists", roster.exists(), "no authoritative roster file",
          behavior="TEAM-02")
    if not (root_idx.exists() and roster.exists()):
        return
    root_txt = root_idx.read_text(encoding="utf-8")
    check("root index links the roster", any("team/index.md" in t for t in _LINK.findall(root_txt)),
          "memory/index.md must link team/index.md — the team is undiscoverable otherwise",
          behavior="TEAM-01")
    roster_txt = roster.read_text(encoding="utf-8")
    check("roster is type log", (parse_frontmatter(roster) or {}).get("type") == "log",
          "roster frontmatter type must be log", behavior="TEAM-02")
    active = _section_link_targets(roster_txt, "Active")
    inactive = _section_link_targets(roster_txt, "Inactive")
    check("roster has an Active section", bool(active) or "## Active" in roster_txt,
          "roster must have an ## Active section", behavior="TEAM-02")
    for tgt in active + inactive:
        check(f"roster link {tgt} resolves", (team / tgt).resolve().exists(), "dangling roster link",
              behavior="TEAM-02")
    active_slugs = {t.split("/")[0] for t in active}
    inactive_slugs = {t.split("/")[0] for t in inactive}

    # (b) per specialist: loadable, valid, status agrees with roster, reads links, specialist-memory link
    for d in member_dirs:
        rel = d.relative_to(mem).as_posix()
        slug = d.name
        ctext = (d / "charter.md").read_text(encoding="utf-8")
        fm = parse_frontmatter(d / "charter.md") or {}
        check(f"{rel} charter type", fm.get("type") == "team-member", f"type={fm.get('type')!r}",
              behavior="TEAM-04")
        # Inverted in 0.22.0: a specialist has NO boot files of its own. One left behind is a dead
        # projection AND, now that the reachability carve-out is gone, an unreachable file
        # (brain/schemas/team-member.md -> "Why a specialist has no boot files of its own").
        check(f"{rel} has no leftover boot files",
              not (d / "AGENTS.md").exists() and not (d / "CLAUDE.md").exists(),
              "specialist AGENTS.md/CLAUDE.md are removed as of 0.22.0", behavior="TEAM-15")
        check(f"{rel} valid autonomy", fm.get("autonomy") in {"draft-and-wait", "initiative", "act-and-inform"},
              f"autonomy={fm.get('autonomy')!r}", behavior="TEAM-05")
        check(f"{rel} charter has persona block", "persona" in fm,
              "no persona: block in charter frontmatter (OPTIONAL, but expected on these fixtures)",
              behavior="TEAM-06")
        # Every charter carries a domain METHOD — the ordered checks this specialist runs and the
        # standard each is checked against. Persona changes how output sounds; the method is the only
        # part that changes what the specialist DOES, so it is required, not optional
        # (brain/schemas/team-member.md → "The charter").
        method = re.search(r"^##\s+Method\b(.*?)(?=^##\s|\Z)", ctext, re.S | re.M)
        check(f"{rel} charter has a ## Method", method is not None,
              "no ## Method section — the specialist has a persona but no procedure",
              behavior="TEAM-07")
        if method:
            steps = re.findall(r"^\s*\d+\.\s+\S", method.group(1), re.M)
            check(f"{rel} Method has >=3 ordered steps", len(steps) >= 3,
                  f"{len(steps)} numbered step(s) — a method is an ordered checklist, not a sentence",
                  behavior="TEAM-07")
        status = fm.get("status")
        check(f"{rel} has valid status", status in {"active", "inactive"}, f"status={status!r}",
              behavior="TEAM-04")
        # roster ↔ charter status agreement (no directory inference — the roster is the source of truth)
        check(f"{rel} linked from roster", slug in active_slugs or slug in inactive_slugs,
              "charter not linked from the roster — it would be an orphan, undiscoverable specialist",
              behavior="TEAM-08")
        if status == "active":
            check(f"{rel} active ⇒ under ## Active", slug in active_slugs,
                  "active charter must be linked under the roster's ## Active", behavior="TEAM-08")
        elif status == "inactive":
            check(f"{rel} inactive ⇒ under ## Inactive", slug in inactive_slugs and slug not in active_slugs,
                  "inactive charter must be under ## Inactive, not ## Active", behavior="TEAM-08")
        # specialist-memory is reached by an explicit link, never a scan
        check(f"{rel} charter links its specialist memory",
              any(t.rstrip("/").endswith("memory/index.md") or t == "memory/index.md"
                  for t in _LINK.findall(ctext)),
              "charter must link [Specialist memory](memory/index.md)", behavior="TEAM-09")
        # ## Key context (if present) is a non-binding pointer, not an access-control list — the only
        # hard requirement on it is that its links resolve.
        key_context = _section_link_targets(ctext, "Key context")
        for rp in key_context:
            check(f"{rel} Key context {rp} resolves", (d / rp).resolve().exists(),
                  "dangling ## Key context link", behavior="TEAM-10")

    # (b3) the always-loaded roster pointer stays generic — it must not name any specialist's
    # specialization. `memory/index.md` is always-loaded, so a specialization there rides into every
    # session and goes stale the moment the roster changes (brain/playbooks/team.md → build step 4,
    # memory-lint check 23). Asserts the RULE, not the literal string: the exact pointer wording
    # appears in four product files, and pinning it would make any copyedit a test break.
    idx_txt = (mem / "index.md").read_text(encoding="utf-8") if (mem / "index.md").exists() else ""
    hook = next((ln for ln in idx_txt.splitlines() if "team/index.md" in ln), "")
    for d in member_dirs:
        spec = (parse_frontmatter(d / "charter.md") or {}).get("specialization", "")
        # compare on content words, so "conveyor + robotics automation" is caught by "conveyor"
        leaked = [w for w in re.findall(r"[a-z]{5,}", spec.lower()) if w in hook.lower()]
        check(f"roster pointer omits {d.name}'s specialization", not leaked,
              f"memory/index.md's team hook names {leaked} — keep it generic",
              behavior="TEAM-11")

    # (c) no confidential identity leaks, and no team file LINKS the registry
    for p in sorted((mem / "team").rglob("*.md")):
        prel = p.relative_to(mem).as_posix()
        txt = p.read_text(encoding="utf-8")
        for tok in sorted(identity_tokens):
            check(f"{prel} hides '{tok}'", tok not in txt,
                  "confidential identity leaked into a specialist file", behavior="TEAM-12")
        check(f"{prel} never links the registry",
              not any("registry.md" in t for t in _LINK.findall(txt)),
              "the confidential registry must never be linked from a roster/charter/specialist page",
              behavior="TEAM-13")

    # (d) delegation records well-formed
    statuses = {"assigned", "in-progress", "delivered", "verified", "integrated", "rejected"}
    _DELEG_SECTIONS = ("Mandate", "Acceptance criteria", "Context provided", "Deliverable",
                       "Verification", "Integrated facts", "Lesson")
    for p in sorted((mem / "team").rglob("delegations/*.md")):
        rel = p.relative_to(mem).as_posix()
        fm = parse_frontmatter(p) or {}
        check(f"{rel} type delegation", fm.get("type") == "delegation", f"type={fm.get('type')!r}",
              behavior="TEAM-26")
        check(f"{rel} valid status", fm.get("status") in statuses, f"status={fm.get('status')!r}",
              behavior="TEAM-28")
        # The record's SHAPE, not just its frontmatter type. Measured on codex: only 1 record in 3
        # was well-formed — sections and fields the agent had nothing to put in yet were omitted
        # rather than stubbed, and `member:` (what ties a record to its specialist) went missing 2 of 3
        # times. `due:`/`source:` stay unasserted: they may legitimately be "—".
        rtext = p.read_text(encoding="utf-8")
        missing = [h for h in _DELEG_SECTIONS if f"## {h}" not in rtext]
        check(f"{rel} has all seven sections", not missing, f"missing: {missing}",
              behavior="TEAM-26")
        absent = [k for k in ("name", "description", "type", "updated", "member", "status")
                  if not fm.get(k)]
        check(f"{rel} has the required frontmatter", not absent, f"missing: {absent}",
              behavior="TEAM-26")
        check(f"{rel} name follows the deleg- convention",
              str(fm.get("name", "")).startswith("deleg-"),
              f"name={fm.get('name')!r} — expected deleg-<slug>-<task>-<date>",
              behavior="TEAM-27")

    # (d2) closed delegations teach: a terminal record carries a ## Lesson, and the specialist's own memory
    # router surfaces it under ## Casebook, linked. This is the accumulation invariant — a lesson that
    # is on disk but not on the specialist's read path is the same as not having written it
    # (brain/schemas/team-member.md → "The casebook").
    for p in sorted((mem / "team").rglob("delegations/*.md")):
        rel = p.relative_to(mem).as_posix()
        fm = parse_frontmatter(p) or {}
        if fm.get("status") not in {"integrated", "rejected"}:
            continue
        check(f"{rel} closed record has ## Lesson", "## Lesson" in p.read_text(encoding="utf-8"),
              "a closed delegation must record what the specialist's next task should inherit",
              behavior="TEAM-31")
        midx = p.parent.parent / "memory" / "index.md"
        cases = (_section_link_targets(midx.read_text(encoding="utf-8"), "Casebook")
                 if midx.exists() else [])
        check(f"{rel} is linked from the specialist's ## Casebook",
              any(p.name in t for t in cases),
              "closed delegation not linked from the specialist's memory/index.md ## Casebook",
              behavior="TEAM-31")

    # (e) starter memory is EVIDENCE ONLY: every seeded note cites a real source, and none carries an
    # `unverified` model-prior marker. A generic prior written to disk and read back teaches the model
    # nothing it already knew, and the marker dresses a guess as a finding. Where a prior is genuinely
    # load-bearing it belongs in the charter's ## Method, as reviewed instruction
    # (brain/schemas/team-member.md → "Starter memory — evidence only").
    for p in sorted((mem / "team").rglob("memory/notes/*.md")):
        rel = p.relative_to(mem).as_posix()
        txt = p.read_text(encoding="utf-8")
        check(f"{rel} cites a source", "(source:" in txt,
              "a seeded note must carry provenance", behavior="TEAM-17")
        check(f"{rel} carries no 'unverified' model prior", "unverified" not in txt.lower(),
              "seeded notes are evidence only — move the prior into the charter's ## Method",
              behavior="TEAM-17")

    # (f) a SUGGESTION is not membership. It lives outside memory/team/, is capped at one pending
    # entry, and its always-load pointer stays generic — the same rule as the roster pointer in
    # (b): a hook naming the specialization rides into every session and goes stale the moment the
    # suggestion is answered (brain/schemas/team-member.md → "A suggestion is not membership").
    check("no suggestion file inside memory/team/", not (team / "suggestions.md").exists(),
          "a suggestion is not membership — it never goes in the folder that means membership",
          behavior="TEAM-67")
    sugg = mem / "team-suggestions.md"
    check("team-suggestions.md exists in the fixture", sugg.exists(), f"missing {sugg}",
          behavior="TEAM-68")
    if sugg.exists():
        stext = sugg.read_text(encoding="utf-8")
        check("team-suggestions.md is type log",
              (parse_frontmatter(sugg) or {}).get("type") == "log",
              f"type={(parse_frontmatter(sugg) or {}).get('type')!r}", behavior="TEAM-68")
        pending = [ln for ln in _md_section(stext, "Pending").splitlines()
                   if ln.strip().startswith("- ")]
        check("at most one pending suggestion", len(pending) <= 1,
              f"{len(pending)} pending entries — the cap is one, so an unanswered ask cannot pile up",
              behavior="TEAM-68")
        for tgt in _LINK.findall(stext):
            check(f"suggestion link {tgt} resolves", (mem / tgt).resolve().exists(),
                  "a suggestion cites the pages its domain recurs across; a dangling one is ungrounded",
                  behavior="TEAM-68")
        check("team-suggestions.md carries a Declined section", "## Declined" in stext,
              "without a permanent tombstone the next exploration re-derives the same suggestion",
              behavior="TEAM-70")
        shook = next((ln for ln in idx_txt.splitlines() if "team-suggestions.md" in ln), "")
        check("memory/index.md links team-suggestions.md", bool(shook),
              "boot step 8 reads it out of the always-load tier; unlinked, it is invisible",
              behavior="TEAM-69")
        slug = pending[0].split("**")[1] if pending and "**" in pending[0] else ""
        leaked = [w for w in re.findall(r"[a-z]{5,}", slug.lower()) if w in shook.lower()]
        check("suggestion pointer omits the suggested specialization", not leaked,
              f"memory/index.md's suggestion hook names {leaked} — keep it generic",
              behavior="TEAM-69")


# ---------------------------------------------------------------- 12. memory reachability
_REACH_EXEMPT = re.compile(r"(^|/)_quarantined/|(^|/)_processed/")


def _reachable_md(root: Path) -> set[Path]:
    """BFS from `root/index.md`, following in-tree markdown links transitively (through sub-indexes)."""
    idx = (root / "index.md").resolve()
    seen: set[Path] = set()
    stack = [idx] if idx.exists() else []
    while stack:
        f = stack.pop()
        if f in seen or not f.exists():
            continue
        seen.add(f)
        for tgt in _LINK.findall(f.read_text(encoding="utf-8")):
            tgt = tgt.split("#")[0].strip()
            if not tgt.endswith(".md") or "://" in tgt:
                continue
            dest = (f.parent / tgt).resolve()
            try:
                dest.relative_to(root.resolve())
            except ValueError:
                continue
            if dest not in seen:
                stack.append(dest)
    return seen


def test_memory_reachability() -> None:
    """Every file under a memory tree must be reachable by following links from its root `index.md`
    (through sub-indexes) — memory is one connected graph, not a folder scan. The exemptions are
    `memory/_quarantined/` files and uncited archived originals under `memory/_processed/` (both
    deliberately kept out of the reachable graph). The specialist-boot-file carve-out was dropped in
    0.22.0 along with the files, which TIGHTENS this: a specialist subtree is now fully link-reachable. `meta.md` and the confidential registry ARE linked
    (registry from the root index only). Fix the fixture or brain if this fails
    (brain/schemas/memory-file.md → reachability invariant)."""
    section("12. Memory reachability (every file linked from index.md)")
    roots = [ROOT / "tests/fixtures/onboarded/memory", ROOT / "tests/fixtures/team/memory"]
    roots += sorted(p for p in (ROOT / "tests/fixtures/memory").glob("*") if p.is_dir())
    for root in roots:
        if not (root / "index.md").exists():
            continue
        rel = root.relative_to(ROOT).as_posix()
        reached = _reachable_md(root)
        unreached = sorted(
            p for p in root.rglob("*.md")
            if p.resolve() not in reached and not _REACH_EXEMPT.search(p.relative_to(root).as_posix()))
        detail = ", ".join(p.relative_to(root).as_posix() for p in unreached)
        check(f"{rel}: all memory reachable from index.md "
              f"(except _quarantined/ and _processed/, exempt wholesale)",
              not unreached, f"unreachable: {detail}", behavior="MEM-17")


# ------------------------------------------------------------ 13. no em-dashes in the shipped README
def test_no_em_dashes() -> None:
    """House style for the public marketing surfaces: no em-dash. Use commas for simple joins, a
    period to split independent clauses, a colon for a "label: detail" lead-in, parentheses for a
    true aside.

    This repo owns one of those surfaces, `src/README.md`, which ships in the ZIP and is the first
    thing a principal reads in their folder. The site owns the other three and asserts them in its
    own suite. Until the split the rule was a grep documented in four places and enforced by none,
    which is how an em-dash reaches production.

    The ROOT README.md is exempt: it is the repo landing page for developers, not marketing copy —
    the same exemption CONTRIBUTING.md has always stated.
    """
    section("13. No em-dashes in the shipped README")
    p = SRC / "README.md"
    check("src/README.md exists", p.exists(), f"{p} is missing", behavior="REPO-18")
    if not p.exists():
        return
    hits = [i for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1) if "—" in line]
    check("src/README.md is em-dash free", not hits,
          f"line(s) {hits[:8]}" + (" ..." if len(hits) > 8 else ""), behavior="REPO-18")


# -------------------------------------------------- 14. workflow jobs are pinned to this repository
THIS_REPO = "pkozanian/ChiefOfStaff"


def test_workflow_repo_guards() -> None:
    """Every workflow job must refuse to run anywhere but this repository.

    These workflows are written for one place: they cut releases, publish artifacts under names that
    are already in the wild, and spend tokens. A copy of this tree running them somewhere else --
    a fork, a mirror, a scratch clone -- would do all of that from a repository nobody is watching.

    The pin travels with the file, so a workflow added a year from now inherits the rule rather than
    inheriting someone's memory of a repository setting.
    """
    section(f"14. Workflow jobs pinned to {THIS_REPO}")
    files = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
    check("workflows present to scan", bool(files), "no .github/workflows/*.yml found",
          behavior="REPO-19")
    guard = f"github.repository == '{THIS_REPO}'"
    for p in files:
        lines = p.read_text(encoding="utf-8").splitlines()
        starts = [i for i, line in enumerate(lines) if line.rstrip() == "jobs:"]
        if not starts:
            check(f"{p.name} declares jobs", False, "no top-level `jobs:` block",
                  behavior="REPO-19")
            continue
        # Job keys are the 2-space-indented mapping keys under `jobs:`. A `runs-on:` inside the block
        # is what distinguishes a real job from a stray 2-space line in a `run: |` block scalar.
        keys = [i for i in range(starts[0] + 1, len(lines))
                if re.match(r"^  [A-Za-z0-9_-]+:\s*$", lines[i])]
        jobs = []
        for n, i in enumerate(keys):
            end = keys[n + 1] if n + 1 < len(keys) else len(lines)
            body = "\n".join(lines[i:end])
            if re.search(r"^    runs-on:", body, re.M):
                jobs.append((lines[i].strip().rstrip(":"), body))
        check(f"{p.name} has at least one job", bool(jobs), "none found under `jobs:`",
              behavior="REPO-19")
        for name, body in jobs:
            check(f"{p.name} job '{name}' pinned to {THIS_REPO}", guard in body,
                  f"add `if: ${{{{ {guard} }}}}` — it would otherwise run in any copy of this tree",
                  behavior="REPO-19")


# -------------------------------------------------- 15. the release path never writes to the site
def test_release_never_writes_to_site() -> None:
    """`release.yml` publishes to the official repo and stops there.

    The site pulls a release from `pkozanian/ChiefOfStaff` on its own dispatch. That is the whole
    reason the official repo is the source of truth and not merely a record: the site can only serve
    what that repo contains, and no public artifact traces back to this one. A mirror step added here
    "just to save a step" silently reverses it, and everything would keep working — which is exactly
    why it needs a test rather than a note.

    Asserted as the credential and the clone URL, not the repo's name: the file SHOULD discuss the
    site in comments (it explains the invariant), and banning the string would forbid saying why.
    Writing to it requires one of these two.
    """
    section("15. The release path never writes to the site")
    p = ROOT / ".github" / "workflows" / "release.yml"
    check("release.yml exists", p.exists(), f"{p} is missing", behavior="REL-11")
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    for token, why in (
        ("SITE_REPO_TOKEN", "the site credential — the release path must not hold one"),
        ("chiefofstaff-site.git", "a clone/push URL for the site repo"),
    ):
        check(f"release.yml omits '{token}'", token not in text,
              f"{why}; the site PULLS (see CONTRIBUTING.md -> The website)", behavior="REL-11")


# ------------------------------------------------ 16. no tracked file names the authoring sandbox
# Assembled from fragments on purpose: this needle must never appear as a literal anywhere in the
# tree, and a check that hard-codes it would be the first thing it catches.
SANDBOX_NEEDLE = "chiefofstaff" + "-dev"


def test_no_sandbox_references() -> None:
    """No tracked file may name the private sandbox this tree is authored in.

    Every file here is published. Work happens somewhere private first, and that arrangement is
    nobody's business: a stray mention in a comment, a doc, or a workflow puts a private repository's
    name in front of everyone who reads the project.

    Scans every tracked file with no exclusions, because there is no directory here that isn't
    published. It is a grep, and that is the point -- the rule erodes through ordinary helpfulness
    ("added a note about where this gets built"), which is exactly what a grep catches and a
    convention does not.
    """
    section("16. No tracked file names the authoring sandbox")
    try:
        tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                                 text=True, check=True).stdout.split()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        check("git ls-files available", False, str(e), behavior="REPO-20")
        return
    check("tracked files to scan", bool(tracked), "git ls-files returned nothing",
          behavior="REPO-20")
    hits = []
    for rel in tracked:
        p = ROOT / rel
        if not p.is_file():
            continue
        try:
            # errors="ignore": the tree is markdown and text, but a fixture could be anything, and a
            # binary that cannot hold the needle as UTF-8 is not worth failing the suite over.
            if SANDBOX_NEEDLE in p.read_text(encoding="utf-8", errors="ignore"):
                hits.append(rel)
        except OSError:
            continue
    check("no tracked file names the sandbox", not hits,
          f"found in {hits[:6]}" + (" ..." if len(hits) > 6 else ""), behavior="REPO-20")


# ---------------------------------------------------------------- main
# ------------------------------------ 18. the demotion claim is recomputed, never verified by hand
# The registry row this enforces. Spelled out at every check() site rather than held in a constant,
# because check #17 rule 3 reads `behavior=` statically from source and a name is invisible to it.
_MENTIONS_RE = re.compile(r"^output mentions (.+)$")


def always_load_files(persona: Path) -> list[Path]:
    """A fixture's always-load tier: `index.md` plus every file linked under its `## Always load`.

    This is what the agent has in context before it opens anything, so it is the exact set a
    "the answer came from the on-demand page" claim has to be clean against.
    """
    idx = persona / "index.md"
    if not idx.exists():
        return []
    text = idx.read_text(encoding="utf-8", errors="ignore")
    if "## Always load" not in text:
        return [idx]
    block = text.split("## Always load", 1)[1].split("\n## ", 1)[0]
    found = [idx]
    for rel in re.findall(r"\]\(([^)]+)\)", block):
        target = (idx.parent / rel).resolve()
        if target.exists():
            found.append(target)
    return found


def test_demotion_claim() -> None:
    """Every scenario MEM-54 cites must assert a token its fixture does NOT always-load.

    MEM-54 claims the demoted detail is retrieved from its on-demand page rather than read off the
    always-loaded index. An eval scenario passes when a token appears in the output -- so if that
    token also sits in a file the agent loads every turn, the pass is consistent with never opening
    the page, and the row is over-claiming.

    Recomputed rather than trusted because the hand check has failed twice on this exact property.
    `decisions.md` -> `## buried-needle-fixture-hooks` caught three chatty `## Load on demand` hook
    lines and missed three always-load PAGES carrying the same tokens (`projects/meridian.md` names
    both of `mem-saas-cto-routing`'s old assertions; `commitments.md` names `idempotency`). A second
    pass over the hooks made the same mistake before this check existed.

    Fails, deliberately, on a cited scenario with no positive output assertion at all -- otherwise
    deleting the last `out_has` would leave the row claiming something nothing checks, which is the
    defect recorded in `## file-has-date-is-vacuous`.
    """
    section("18. Demotion claims hold against the always-load tier")
    reg = ROOT / "tests" / "behaviors.md"
    parsed, _ = parse_behaviors(reg)
    rows = dict(parsed)
    if "MEM-54" not in rows:
        check("MEM-54 row exists", False, "registry has no such row", behavior="MEM-54")
        return
    pats, _marker = covered_tokens(rows["MEM-54"]["covered"])

    sys.path.insert(0, str(ROOT / "tests" / "eval"))
    try:
        from scenarios import SCENARIOS  # type: ignore
    except Exception as e:  # noqa: BLE001
        check("load eval scenarios", False, str(e), behavior="MEM-54")
        return

    cited = [s for s in SCENARIOS if any(fnmatch.fnmatch(s.key, pat) for pat in pats)]
    check("MEM-54 cites at least one scenario", bool(cited),
          "no scenario matches its Covered by cell", behavior="MEM-54")

    fixtures = ROOT / "tests" / "fixtures" / "memory"
    for s in cited:
        name = getattr(s.seed, "fixture", None)
        if name is None:
            check(f"{s.key} seeds a named fixture", False,
                  "its seed is not seed_fixture(), so its always-load tier cannot be resolved",
                  behavior="MEM-54")
            continue
        loaded = always_load_files(fixtures / name)
        check(f"{s.key} fixture {name!r} has an always-load tier", bool(loaded),
              f"no index.md under tests/fixtures/memory/{name}/", behavior="MEM-54")
        text = "\n".join(p.read_text(encoding="utf-8", errors="ignore").lower() for p in loaded)
        tokens = [ast.literal_eval(m.group(1))
                  for m in (_MENTIONS_RE.match(desc) for desc, _ in s.assertions) if m]
        check(f"{s.key} asserts a positive token", bool(tokens),
              "no `output mentions ...` assertion — nothing proves the detail was recalled at all",
              behavior="MEM-54")
        for tok in tokens:
            where = [p.name for p in loaded if tok.lower() in
                     p.read_text(encoding="utf-8", errors="ignore").lower()]
            check(f"{s.key} {tok!r} is not always-loaded", not where,
                  f"{tok!r} is in the always-load tier ({', '.join(where)}) — a pass does not show "
                  f"the on-demand page was opened", behavior="MEM-54")


# ---------------------------------------------------------------- 24. boot cost
def test_boot_cost() -> None:
    """Boot loads what the first turn needs and nothing that only a later turn needs.

    Four rules, each of which a measured install violated at ~78k tokens of boot:
    the team-member schema loading because a roster merely exists; the session-start digest
    rebuilt by walking every specialist instead of read from the commitments tracker; the capability
    inventory re-derived from `hosts.md`/`connectors.md` rather than its own cached file; and the
    read waves described in one host's vocabulary. Substring matching is deliberate — these are
    load-bearing phrasings, not prose (see the `Never` list in AGENTS.md)."""
    section("24. Boot cost (what the first turn actually needs)")

    def flat(p: Path) -> str:
        raw = re.sub(r"[*_`]", "", p.read_text(encoding="utf-8"))
        return re.sub(r"\s+", " ", raw).lower()

    def flat_keys(p: Path) -> str:
        """Like flat(), but keeps `_` — frontmatter keys (`last_lint`) are not md emphasis."""
        raw = re.sub(r"[*`]", "", p.read_text(encoding="utf-8"))
        return re.sub(r"\s+", " ", raw).lower()

    # --- decision 5: the team-member schema is not a boot file
    hook = [ln for ln in (BRAIN / "index.md").read_text(encoding="utf-8").splitlines()
            if "schemas/team-member.md" in ln]
    check("brain/index.md hooks the team-member schema", len(hook) == 1,
          f"expected exactly one hook line, found {len(hook)}", behavior="BOOT-24")
    line = re.sub(r"[*_`]", "", hook[0]).lower() if hook else ""
    check("team-member schema does not load because a roster exists",
          "links a team roster" not in line,
          "the hook fires on a property of the install, not on the conversation — so for any "
          "principal with a team it is always-load wearing an on-demand label (426 lines)",
          behavior="BOOT-24")
    check("team-member schema loads on use",
          any(w in line for w in ("creating", "delegating", "reviewing")),
          "the hook must name the acts that need the schema", behavior="BOOT-24")

    # split on the HEADINGS: steps 1 and 9 both say "see SESSION FRESHNESS", so splitting on the
    # bare phrase truncates boot to its first two steps and every later assertion passes vacuously.
    boot = flat(SRC / "CHIEFOFSTAFF.md").split("## boot protocol")[1].split("## session freshness")[0]

    # --- the batch/size interaction: a wave that can't return a big file whole must not
    # cause it to be fetched twice (measured: memory-file.md and capture-rules.md read 3x each)
    for tok in ("one pass per file", "once", "only those"):
        check(f"boot's wave rule states {tok!r}", tok in boot,
              "batching plus an oversized file is worse than either alone — the batch returns it "
              "truncated, the agent measures it and re-fetches it whole", behavior="BOOT-29")
    check("boot forbids re-reading the whole wave", "never the whole wave again" in boot,
          "a partial batch must be repaired file by file, not repeated", behavior="BOOT-29")

    # --- decision 7: the digest reads the tracker, it does not walk the team
    check("boot does not follow per-specialist charter links",
          "active charter links you actually need" not in boot,
          "walking every active specialist's charter and ledger recomputes what memory/commitments.md "
          "already holds (delegate.md step 6 mirrors every delegation into it)", behavior="BOOT-25")
    check("boot names the commitments tracker as the digest source",
          "commitments.md" in boot,
          "the session-start digest must read the tracker boot already loads", behavior="BOOT-25")
    check("boot still forbids scanning the team tree", "never scan" in boot,
          "the link-based roster invariant must survive this change", behavior="BOOT-25")
    # Decision 7 has to hold across the WHOLE file, not just the boot window this check slices.
    # It didn't: § VIRTUAL TEAM went on ordering the digest to read every specialist's
    # `delegations/` and `ledger.md` — 400 lines after boot step 4 forbade exactly that, in the same
    # always-loaded file, and outside this window so nothing objected. Measured on a real
    # 15-specialist install, the traversal that paragraph authorised was 132,442 bytes (~33,110
    # tokens) per session — more than the entire brain boot tier.
    whole = flat(SRC / "CHIEFOFSTAFF.md")
    check("no section reinstates the per-specialist traversal",
          "specialists' delegations/ and ledger.md, reached by" not in whole,
          "boot step 4 forbids opening specialist files at boot; a later section telling the agent "
          "to walk them is the regression decision 7 removed", behavior="BOOT-25")

    # --- decision 3: read waves are described host-neutrally
    check("boot describes its reads as waves", "wave" in boot,
          "boot must state which reads are independent so a host can batch them", behavior="BOOT-26")
    for tok in ("cat ", "parallel tool", "read tool", "bash tool"):
        check(f"boot does not name the mechanism {tok.strip()!r}", tok not in boot,
              "hosts differ and one has no execution surface — say 'in as few operations as your "
              "host allows', never how", behavior="BOOT-26")

    # --- decision 10: the capability inventory is read, not re-derived
    step7 = boot.split("know your tools")[1].split("session-start maintenance")[0] if \
        "know your tools" in boot else ""
    check("boot step 7 is present", bool(step7), "could not locate the capability step",
          behavior="BOOT-27")
    check("boot step 7 reads the cached inventory", "memory/integrations.md" in step7,
          "the inventory file is already in memory's always-load tier", behavior="BOOT-27")
    # Not "must not mention" — the re-derive path legitimately names them. What must hold is that
    # the cached file is reached for FIRST and the discovery files are gated behind a condition.
    for rel in ("integrations/hosts.md", "integrations/connectors.md"):
        check(f"boot step 7 reaches the cache before {rel}",
              rel not in step7 or step7.index("memory/integrations.md") < step7.index(rel),
              "the cached inventory must be the boot answer; discovery is the exception",
              behavior="BOOT-27")
    check("boot step 7 gates re-discovery", "only when" in step7,
          "re-deriving the inventory costs ~5.3k tokens to restate a file boot already holds — the "
          "re-read must be conditional, not the default", behavior="BOOT-27")
    check("boot step 7 says not to load the discovery files by default",
          "don't load" in step7 or "do not load" in step7,
          "an agent reading a mention of hosts.md/connectors.md will fetch them unless told not to",
          behavior="BOOT-27")

    # --- decision 9: the maintenance clock reads meta.md, not a scan of the ledger
    bootk = flat_keys(SRC / "CHIEFOFSTAFF.md").split("## boot protocol")[1].split(
        "## session freshness")[0]
    step8 = bootk.split("session-start maintenance")[1].split("update check —")[0] \
        if "session-start maintenance" in bootk else ""
    check("boot step 8 is present", bool(step8), "could not locate the maintenance step",
          behavior="BOOT-28")
    check("boot step 8 reads the dates from meta.md",
          "last_lint" in step8 and "last_explore" in step8,
          "the clock's other anchor (last_onboarded) already lives in meta.md, which wave 1 loads",
          behavior="BOOT-28")
    check("boot step 8 does not read the ledger first",
          "memory/ledger.md" not in step8 or
          (0 <= step8.find("last_lint") < step8.index("memory/ledger.md")),
          "Claude Code reads memory/ledger.md whole — 334 lines / ~9,814 tokens on a measured "
          "install, and it is append-only, so the cost grows forever", behavior="BOOT-28")
    meta_row = [l for l in (BRAIN / "schemas" / "memory-file.md").read_text(
        encoding="utf-8").splitlines() if "`memory/meta.md`" in l]
    check("memory-file.md documents the meta.md state keys",
          any("last_lint" in l and "last_explore" in l for l in meta_row),
          "a key boot depends on must be in the schema, or nothing writes it", behavior="BOOT-28")
    for rel, key in (("playbooks/memory-lint.md", "last_lint"),
                     ("playbooks/explore.md", "last_explore")):
        check(f"{rel} records {key}", key in flat_keys(BRAIN / rel),
              "the clock never resets unless the run that satisfies it writes the date",
              behavior="BOOT-28")

    # A pending suggestion rides step 8 rather than opening a second session-start ask. The always-
    # load tier already holds the file, so this trigger costs no extra read
    # (brain/schemas/team-member.md → "A suggestion is not membership").
    check("boot step 8 also fires on a pending team suggestion",
          "team-suggestions.md" in step8,
          "a suggestion nobody ever sees again is not persisted, it is buried",
          behavior="BOOT-30")
    check("the suggestion file is documented where boot expects it",
          "team-suggestions.md" in (BRAIN / "schemas" / "memory-file.md").read_text(
              encoding="utf-8"),
          "a file boot depends on must be in the memory map, or nothing ever creates it",
          behavior="BOOT-30")

    # --- decision 6: the tier rule names the trackers it assumes are in the tier
    tier = flat(BRAIN / "schemas" / "capture-rules.md")
    tier = tier.split("always load for", 1)[-1][:400]
    check("capture-rules' tier rule names commitments.md", "commitments.md" in tier,
          "memory-file.md assumes the commitments tracker is always-load; the rule that places "
          "files must say so, or an install puts it on demand and boot rebuilds it by walking "
          "every team member (measured: 28,655 tokens to recompute a 1,966-token file)",
          behavior="MEM-55")
    # Only `commitments.md` — all seven fixtures keep `okrs.md` and `decisions.md` on demand, and
    # that is correct: the session-start digest needs open commitments, not the OKR set.
    # --- decision 7's safety net: if the mirror is skipped, the digest silently misses work
    lint = flat(BRAIN / "playbooks" / "memory-lint.md")
    check("memory-lint reconciles delegations against the tracker",
          "delegated work missing from the tracker" in lint,
          "boot no longer walks specialists, so nothing else would notice an unmirrored delegation",
          behavior="PLAY-50")
    check("the reconciliation names the delegation statuses it applies to",
          all(s in lint for s in ("assigned", "in-progress", "delivered")),
          "an open record is one not yet integrated or rejected", behavior="PLAY-50")

    personas = sorted(d for d in (ROOT / "tests" / "fixtures" / "memory").iterdir() if d.is_dir())
    check("persona fixtures exist to check against", bool(personas), "", behavior="MEM-55")
    for d in personas:
        if not (d / "commitments.md").exists():
            continue
        check(f"{d.name} always-loads commitments.md",
              "commitments.md" in [f.name for f in always_load_files(d)],
              "the fixtures encode the convention the brain now states", behavior="MEM-55")


# --------------------------------------------- 25. team suggestions (notice → offer → persist)
def test_team_suggestions() -> None:
    """A suggested specialist is offered in the run that found it and persisted only if unanswered.

    Substring matching is deliberate, as in check #24: these are load-bearing phrasings, not prose.
    The file path is the wiring between four files (explore files it, boot step 8 raises it, team.md
    answers it, memory-lint drops a stale one) and a copyedit that drops it silently breaks the
    chain. Reword any of these and update the check in the same change (see AGENTS.md → Never)."""
    section("25. Team suggestions (notice → offer → persist)")

    def flat(p: Path) -> str:
        raw = re.sub(r"[*`]", "", p.read_text(encoding="utf-8"))
        return re.sub(r"\s+", " ", raw).lower()

    expl = flat(BRAIN / "playbooks" / "explore.md")
    check("explore names the suggestion file", "team-suggestions.md" in expl,
          "the run that notices is the run that has to file it", behavior="MEM-56")
    check("explore states the grounding threshold", "at least two" in expl,
          "the same rail as every other finding — a domain named in one file is not a pattern",
          behavior="MEM-56")
    check("explore reads the roster for coverage", "## active" in expl,
          "coverage is read from the roster's Active entries, never a scan of memory/team/",
          behavior="MEM-56")
    check("explore checks the tombstones before filing", "declined" in expl,
          "without this the same suggestion is re-derived every run and 'no' means nothing",
          behavior="MEM-57")
    check("explore honours a pending suggestion", "pending" in expl,
          "one open ask at a time — a second is piling on", behavior="MEM-57")
    check("explore honours the team-offer switch", "team-offer" in expl,
          "the principal turned the onboarding proposal off; this is the same offer, later",
          behavior="MEM-59")
    dflt = flat(BRAIN / "role" / "defaults.md")
    check("knob 13 covers both surfaces", "team-offer" in dflt and "explor" in dflt.split(
          "virtual team (13")[-1][:600],
          "one switch, or the principal turns it off and it comes back through the other door",
          behavior="MEM-59")

    team = flat(BRAIN / "playbooks" / "team.md")
    check("team.md answers a suggestion", "answer a suggestion" in team,
          "boot step 8 and explore both route here; the section has to exist to be routed to",
          behavior="TEAM-71")
    sec = team.split("answer a suggestion")[-1][:900]
    check("accepting clears the pending entry", "delete" in sec,
          "a suggestion left behind after the specialist exists is an offer for something they have",
          behavior="TEAM-71")
    check("denying tombstones the slug", "declined" in sec,
          "without a tombstone the next exploration re-derives the same suggestion",
          behavior="TEAM-71")
    lint = flat(BRAIN / "playbooks" / "memory-lint.md")
    check("memory-lint drops a covered suggestion", "team-suggestions.md" in lint,
          "a suggestion answered by another route otherwise re-fires at every session start",
          behavior="PLAY-51")


# ---------------------------------------------------------------- 26. decision role coverage
def test_decision_role_coverage() -> None:
    """The RAPID sweep spans BOTH benches — real people and the virtual roster — and the two things
    it may never do (fill A/D, contact a real person) are asserted at the producer. The offers are
    checked against the brief's deliver-in-this-turn contract because an offer that stalls the brief
    is how PLAY-13 regresses without anything else going red."""
    section("26. Decision role coverage (RAPID sweep across both benches)")

    def flat(p: Path) -> str:
        raw = re.sub(r"[*`]", "", p.read_text(encoding="utf-8"))
        return re.sub(r"\s+", " ", raw).lower()

    dec = flat(BRAIN / "playbooks" / "decisions.md")
    brief = flat(BRAIN / "playbooks" / "decision-brief.md")
    dele = flat(BRAIN / "playbooks" / "delegate.md")

    check("decisions.md states the sweep", "role coverage" in dec,
          "the sweep belongs where the log is, not only where the brief is", behavior="PLAY-52")
    check("the sweep is gated on the right-size bar", "capturing step 4" in dec,
          "an ungated sweep reads the roster for every 'let's ship it Friday' and fights right-sizing",
          behavior="PLAY-52")
    check("the sweep reads both benches",
          "memory/team/index.md" in dec and "memory/index.md" in dec,
          "a sweep that reads only people/ misses the virtual bench it exists to cover",
          behavior="PLAY-52")
    check("decisions.md blocks a virtual A or D", "never holds a or d" in dec,
          "agreement is veto authority and the decide is the principal's — neither is delegable",
          behavior="PLAY-53")
    check("delegate.md carries the same block", "never a or d" in dele,
          "the boundary must hold where delegation is defined, not only where decisions are logged",
          behavior="PLAY-53")
    check("a real role-holder gets an outreach draft offer", "draft the outreach" in dec,
          "naming who is missing without offering the message leaves the principal the whole job",
          behavior="PLAY-54")
    check("Chief of Staff never contacts them itself", "never contact anyone yourself" in dec,
          "principle #3 — Chief of Staff drafts, the principal sends", behavior="PLAY-54")
    check("neither offer stalls the brief", "neither offer holds the brief" in brief,
          "PLAY-13's deliver-in-this-turn contract outranks both offers", behavior="PLAY-55")

    # The trigger is stated in two always-on places. Asserting the phrase in BOTH is the point:
    # a copyedit to one that narrows it back to decision-shaped wording is a silent regression,
    # and nothing else in the suite reads these two lines together.
    cap = flat(BRAIN / "schemas" / "capture-rules.md")
    cos = flat(SRC / "CHIEFOFSTAFF.md")
    PHRASE = "advice, input, or an opinion"
    check("capture-rules widens the trigger past a named call", PHRASE in cap,
          "a request for advice is a decision; keying on 'help me decide' misses it",
          behavior="PLAY-56")
    check("passive capture states it identically", PHRASE in cos,
          "one clause narrower than the other is how the rule gets rationalised around",
          behavior="PLAY-56")
    check("capture-rules routes an inferred choice to the section",
          "an unnamed decision" in cap.split("## procedure", 1)[-1],
          "the clause must sit in the Procedure, which runs whatever row a fact routed to — inside "
          "the decision row it is unreachable for a bare situation statement, which is the only "
          "input it exists for (measured: eval unnamed-decision failed exactly this way)",
          behavior="PLAY-57")
    check("decisions.md carries the unnamed-decision section", "an unnamed decision" in dec,
          "capture-rules points here; the section has to exist to be routed to", behavior="PLAY-57")
    check("the log/surface test is who voiced it", "the test is who voiced it" in dec,
          "conditioning on confidence instead makes the behaviour a self-assessment",
          behavior="PLAY-57")
    check("an inferred choice is not written", "surfaced, not logged" in dec,
          "a row the principal never agreed to invents the decision with the authority",
          behavior="PLAY-57")
    check("at most one is raised per turn", "one per turn" in dec,
          "with no decline memory (a deliberate accepted cost) this cap is the only volume control",
          behavior="PLAY-57")


# ---------------------------------------------------------------- 27. specialist memory scope
def test_member_memory_scope() -> None:
    """A specialist's memory is finer-grained than the principal's, and nothing said so. The grain test
    is asserted in both directions on purpose: it decides what a specialist FILES and what it may not
    PROMOTE, and a one-directional reading would let specialist detail climb into shared memory."""
    section("27. Specialist memory scope (the grain test)")

    def flat(p: Path) -> str:
        raw = re.sub(r"[*`]", "", p.read_text(encoding="utf-8"))
        return re.sub(r"\s+", " ", raw).lower()

    schema = flat(BRAIN / "schemas" / "team-member.md")
    team = flat(BRAIN / "playbooks" / "team.md")
    dele = flat(BRAIN / "playbooks" / "delegate.md")

    check("the charter carries a memory scope",
          "## memory scope (what this specialist keeps, at what grain)" in schema,
          "without a per-specialist list the grain test has nothing domain-specific to apply",
          behavior="TEAM-72")
    check("the schema states the grain test", "would chief of staff keep this" in schema,
          "the one question that tells a specialist what is its to keep and what is the principal's",
          behavior="TEAM-73")
    check("the grain test bounds what climbs up", "stays down" in dele,
          "read one-directionally the test files detail correctly and still promotes it into shared "
          "memory — the compartment is a write boundary in both directions", behavior="TEAM-73")
    check("onboard asks what the specialist should remember", "what would a great" in team,
          "the specialist's own answer outranks a drafted scope", behavior="TEAM-74")
    check("the ask rides the existing confirm beat",
          "same confirm beat as the method and persona" in team,
          "the intake already runs long enough to cap onboarding at one specialist — this is a nod, "
          "not a turn", behavior="TEAM-74")
    check("the charter write step includes the scope",
          "the ## memory scope list confirmed above" in team,
          "confirmed in the beat and then not written is how the section goes missing",
          behavior="TEAM-74")
    check("existing specialists get a backfill path",
          "give existing specialists a memory scope" in team,
          "a charter section added with no migration is the 0.15.0 failure — the first-boot pass "
          "walks straight past specialists that predate it", behavior="TEAM-76")
    check("the backfill is idempotent and roster-driven",
          "skip any charter that already has a ## memory scope" in team,
          "a re-run must be a no-op, and discovery stays link-following", behavior="TEAM-76")
    check("delegation files at the charter's grain",
          "at the grain its charter's ## memory scope names" in dele,
          "without this the scope shapes only the seed and every later task files by whim",
          behavior="TEAM-75")


def test_capture_step0_pin() -> None:
    """AGENTS.md's boot paragraph cites capture-rules.md's document procedure by numeral ('step 0'),
    but check 3 skips inline code and nothing else asserts that procedure still starts there.
    Renumbering the Procedure list would silently point the always-loaded entry point at the wrong
    step, so pin the numeral: if AGENTS.md still cites 'step 0', the procedure must still open on a
    `0.` item."""
    section("28. Capture-rules step 0 pin (BOOT-03)")
    agents = (SRC / "AGENTS.md").read_text(encoding="utf-8")
    if "step 0" not in agents:
        return  # AGENTS.md no longer cites a numbered step of this procedure — nothing to pin
    capture = (BRAIN / "schemas" / "capture-rules.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Procedure — for each document shared:\*\*\n(\d+)\.", capture)
    check("capture-rules.md's document procedure still starts at step 0",
          bool(m) and m.group(1) == "0",
          "AGENTS.md cites 'step 0' of this procedure by numeral, but it no longer starts there",
          behavior="BOOT-03")


def test_feedback_address() -> None:
    """The upstream feedback address is published in two shipped files, and the site repo asserts the
    address it publishes against the one in the shipped brain. Two hand-kept copies drift, and the
    drift surfaces as a failing build in the *other* repo, where the cause is not visible. Pin them
    to one literal here, where the edit happens."""
    section("29. Feedback address is one string (REPO-35)")
    pat = re.compile(r"[\w.+-]+@chiefofstaff\.team")
    found: dict[str, set[str]] = {}
    for p in sorted(SRC.rglob("*.md")):
        if "memory" in p.relative_to(SRC).parts:
            continue  # the principal's own tree, not shipped text
        hits = set(pat.findall(p.read_text(encoding="utf-8")))
        if hits:
            found[p.relative_to(SRC).as_posix()] = hits
    check("the shipped tree names a feedback address", bool(found),
          "no @chiefofstaff.team address found anywhere in src/", behavior="REPO-35")
    check("src/README.md names it", "README.md" in found,
          "the principal's first read must carry the address", behavior="REPO-35")
    distinct = set().union(*found.values()) if found else set()
    check("every copy is the same address", len(distinct) <= 1,
          f"{len(distinct)} distinct addresses: " +
          ", ".join(f"{f} → {sorted(a)}" for f, a in sorted(found.items())), behavior="REPO-35")


def test_loading_tips() -> None:
    """The loading tips are spoken to the principal on a host we don't control. Boot step 2 already
    learned this the hard way with `/onboard`: naming a slash command in text that reaches every host
    hands a dead end to the ones that have none (`brain/integrations/hosts.md`). The tips carry the
    same exposure and nothing else asserts it, so pin the count the rotation divides by, and pin the
    rule."""
    section("30. Loading tips (BOOT-31, BOOT-33)")
    text = (SRC / "CHIEFOFSTAFF.md").read_text(encoding="utf-8")
    if "## LOADING TIPS" not in text:
        check("CHIEFOFSTAFF.md has a LOADING TIPS section", False, "section missing",
              behavior="BOOT-31")
        return
    block = text.split("## LOADING TIPS", 1)[1].split("\n## ", 1)[0]
    tips = [ln for ln in block.splitlines() if re.match(r"^\d+\. ", ln)]
    check("there are 8 tips", len(tips) == 8,
          f"found {len(tips)} — boot step 10 divides by 8, so the count is load-bearing",
          behavior="BOOT-31")
    named = [t for t in tips if re.search(r"(?<![\w/])/[a-z][a-z-]+\b", t)]
    check("no tip names a slash command", not named,
          "; ".join(t[:70] for t in named), behavior="BOOT-33")

    # The tip is the one thing boot prints BEFORE it has finished loading, so every gate on it has
    # to be answerable at wave 1. It shipped conditioned on steps 8 and 9 — which have not run —
    # under a "when in doubt, skip it" tiebreak, and fired in 1 of 10 benched boots. These three
    # pin the fix: the decision stays at wave 1, and nothing reintroduces a gate it can't evaluate.
    step = text.split("\n10. **Loading tip", 1)[1].split("\n\nOnly after boot", 1)[0]
    for phrase in ("no maintenance offer", "no update prompt"):
        check(f"the tip is not gated on {phrase!r}", phrase not in step,
              "steps 8 and 9 have not run when the tip must print; gating on them is what makes "
              "the agent carry the decision to the end of boot and skip it", behavior="BOOT-31")
    check("the tip has no 'when in doubt, skip it' tiebreak",
          "when in doubt, skip" not in step.lower(),
          "with an undecidable gate above it, that tiebreak is an instruction to never print",
          behavior="BOOT-31")
    preamble = text.split("## BOOT PROTOCOL", 1)[1].split("\n0. **First boot", 1)[0]
    check("the boot preamble names the loading tip",
          "loading\ntip" in preamble.lower() or "loading tip" in preamble.lower(),
          "step 10 is last in a 10-step protocol but must fire first in time; the wave rules are "
          "where the agent is reading when that moment arrives", behavior="BOOT-31")


# ---------------------------------------------------------------- 18. onboarding checklist
CHECKLIST_TEMPLATE = BRAIN / "onboarding" / "checklist.md"
STEP_FILES = {str(i): BRAIN / "onboarding" / "steps" / n for i, n in enumerate((
    "0-set-expectations.md", "1-principal.md", "2-organization-context.md", "3-key-people.md",
    "4-priorities-projects.md", "5-working-preferences.md", "6-routines-cadence.md"))}
CHECKLIST_STATUS = re.compile(r"^(done|declined|deferred|blocked|n/a)\b")


def checklist_template_rows(path: Path) -> list[tuple[str, str]]:
    """(id, step) per row of the template's `## Rows` table — that section only, so the `## Statuses`
    table's `open`/`done` cells are not mistaken for IDs."""
    text = path.read_text(encoding="utf-8")
    body = text.split("\n## Rows", 1)[1].split("\n## ", 1)[0] if "\n## Rows" in text else ""
    return [(m.group(1), m.group(2).strip())
            for m in re.finditer(r"^\|\s*`([a-z][a-z-]*)`\s*\|[^|]*\|([^|]*)\|", body, re.M)]


def checklist_memory_rows(path: Path) -> list[tuple[str, str]]:
    """(id, status) per row of a memory/onboarding-checklist.md table."""
    return [(m.group(1), m.group(2).strip())
            for m in re.finditer(r"^\|\s*`?([a-z][a-z-]*)`?\s*\|[^|]*\|[^|]*\|([^|]*)\|",
                                 path.read_text(encoding="utf-8"), re.M)
            if m.group(1) != "id"]


def test_onboarding_checklist() -> None:
    """The template is the single source of truth for what onboarding owes; a row nobody's step
    file references is a requirement nothing will ever resolve. And the golden fixture must look
    like a finished checklist: the template's rows, none open, every status one of the six."""
    section("18. Onboarding checklist — template rows owned by steps; fixture resolved")
    rows = checklist_template_rows(CHECKLIST_TEMPLATE)
    check("template has rows", len(rows) >= 15, f"parsed {len(rows)}", behavior="REPO-39")
    ids = [r for r, _ in rows]
    check("template IDs unique", len(ids) == len(set(ids)), "duplicate ID", behavior="REPO-39")
    flow = (BRAIN / "onboarding" / "flow.md").read_text(encoding="utf-8")
    for rid, step in rows:
        owners = [BRAIN / "onboarding" / "flow.md"] if "Finishing" in step else []
        owners += [STEP_FILES[d] for d in re.findall(r"\d", step) if d in STEP_FILES]
        check(f"`{rid}` referenced by its owning step ({step})",
              any(f"`{rid}`" in o.read_text(encoding="utf-8") for o in owners),
              "add the row ID (backticked) to the step file the template names — or fix the template",
              behavior="REPO-39")
    check("flow.md links the template", "checklist.md" in flow, "reach it from flow.md",
          behavior="REPO-39")

    fx = ONBOARDED / "onboarding-checklist.md"
    check("onboarded fixture has a checklist", fx.exists(), f"missing {fx}", behavior="ONB-66")
    if fx.exists():
        mem_rows = checklist_memory_rows(fx)
        check("fixture rows are the template's rows", {r for r, _ in mem_rows} == set(ids),
              f"diff: {sorted({r for r, _ in mem_rows} ^ set(ids))}", behavior="ONB-66")
        for rid, status in mem_rows:
            check(f"fixture `{rid}` is resolved",
                  status != "open" and bool(CHECKLIST_STATUS.match(status)),
                  f"status {status!r}", behavior="ONB-66")


def main() -> int:
    print("Chief of Staff — structural tests")
    for t in (test_frontmatter, test_index, test_links, test_naming, test_connectors_contract,
              test_release_metadata, test_override_targets, test_commands, test_neutral_skills,
              test_gitignore,
              test_site_not_in_src, test_dist_boundary, test_update_delivers_src, test_archive_shapes,
              test_onboarding_lint, test_onboarding_checklist, test_team_layout,
              test_memory_reachability, test_no_em_dashes, test_workflow_repo_guards,
              test_release_never_writes_to_site, test_no_sandbox_references, test_behaviors,
              test_demotion_claim, test_boot_cost, test_team_suggestions,
              test_decision_role_coverage, test_member_memory_scope, test_capture_step0_pin,
              test_feedback_address, test_loading_tips):
        t()
    print(f"\n{'=' * 48}")
    if FAILURES:
        print(f"❌ FAILED — {len(FAILURES)}/{CHECKS} checks failed:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print(f"✅ OK — all {CHECKS} checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
