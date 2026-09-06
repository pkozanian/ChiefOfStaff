#!/usr/bin/env python3
"""Report bare `member` in the trees the vocabulary rule governs.

`team member` (any casing/hyphenation) is sanctioned and not reported. By
default the delegation record's `member:` frontmatter key is also tolerated
(it has a tolerant read and a migration — see AGENTS.md) — pass `--strict`
to report it too. tests/fixtures/, docs/ and src/CHANGELOG.md are out of
scope by design.

Not wired into tests/run.py or any other gate. Nothing runs this
automatically — see AGENTS.md's vocabulary-rule bullet.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

TEAM = re.compile(r"\bteam[- ]members?\b", re.IGNORECASE)
BARE = re.compile(r"\bmembers?\b", re.IGNORECASE)
# The `member:` frontmatter key: tolerated by default (both `member:` and
# `specialist:` are read — see AGENTS.md), reported only under --strict.
# Matches the key in delimiter position: an indented frontmatter line, a
# quote/backtick/regex-caret immediately before it (a Python string literal
# writing or matching the key), or a literal `\n` escape inside one.
# NOTE: this must stay aligned with the identical KEY regex in the sweep
# script (Task 2's report/scratchpad) — same blind spot, same fix, on both
# sides or the scan and the sweep disagree about what counts as the key.
KEY = re.compile(r'(?m)(^[ \t]*|["\'`^]|\\n)member:', re.IGNORECASE)

# Permanent carve-outs: the released migration-protocol scope vocabulary.
# tests/run.py check #5 validates released src/CHANGELOG.md entries
# (member:bootfiles, member:shim) against this exact set; src/CHANGELOG.md
# is out of scope for the sweep, so this set cannot be renamed. Tolerated
# unconditionally, regardless of --allow-key.
CARVE_OUTS = [
    ("tests/run.py",
     'SCOPES = {"charter", "meta", "frontmatter", "path", "preference", "member", "override"}'),
    ("CONTRIBUTING.md",
     "`charter` · `meta` · `frontmatter` · `path` · `preference` · `member` · `override`."),
    # Human-sense "board member" in an eval prompt — a real person, not the
    # virtual-team term. See final-review I3.
    ("tests/eval/scenarios.py",
     "A board member wants a metrics update by Friday."),
    # Set-membership sense ("member of the glob") in dev-only prose, not the
    # virtual-team term. See final-review M2.
    ("tests/decisions.md",
     "The defect is one weak member of the"),
    ("tests/decisions.md",
     "the weak glob member it warned about is the member that changed."),
    # Names the pre-rename charter link label `[Member memory]`, which is
    # persisted on existing installs and still valid — not a live mention
    # of the virtual-team term. See final-review I2.
    ("src/brain/playbooks/memory-lint.md",
     "not the label text — a charter written before the rename still says `[Member"),
]

# Key-shaped carve-out, tolerated unless --strict: this asserts the shape
# of a frozen fixture record under tests/fixtures/team/memory/ (a
# delegation's frontmatter `member:` key), spelled as a Python string
# literal the KEY regex can't see. tests/fixtures/ is never-touch, so this
# assertion must keep naming `member` for as long as that fixture does.
KEY_SHAPED_CARVE_OUTS = [
    ("tests/run.py",
     'absent = [k for k in ("name", "description", "type", "updated", "member", "status")'),
]


def in_scope(rel: str) -> bool:
    if rel.startswith("tests/fixtures/") or rel.startswith("docs/"):
        return False
    if rel == "src/CHANGELOG.md":
        return False
    if not rel.endswith((".md", ".py")):
        return False
    return rel.startswith("src/") or rel.startswith("tests/") or rel == "CONTRIBUTING.md"


def main(strict: bool) -> int:
    allow_key = not strict
    # Anchor to repo root to ensure git ls-files paths are repo-relative
    try:
        root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        sys.stderr.write("Error: not a git repository\n")
        return 1

    os.chdir(root)

    files = subprocess.run(
        ["git", "ls-files", "*.md", "*.py"], capture_output=True, text=True, check=True
    ).stdout.split()
    hits, counts, total_occurrences = [], {}, 0
    for rel in files:
        if not in_scope(rel):
            continue
        for i, line in enumerate(Path(rel).read_text(encoding="utf-8").split("\n"), 1):
            scrubbed = TEAM.sub("", line)
            if allow_key:
                scrubbed = KEY.sub("", scrubbed)
            for path, substr in CARVE_OUTS:
                if rel == path:
                    scrubbed = scrubbed.replace(substr, "")
            if allow_key:
                for path, substr in KEY_SHAPED_CARVE_OUTS:
                    if rel == path:
                        scrubbed = scrubbed.replace(substr, "")
            if BARE.search(scrubbed):
                hits.append(f"{rel}:{i}  {line.strip()[:90]}")
                bucket = "src/" if rel.startswith("src/") else (
                    "tests/" if rel.startswith("tests/") else "CONTRIBUTING.md")
                counts[bucket] = counts.get(bucket, 0) + 1
                total_occurrences += len(BARE.findall(scrubbed))
    for bucket, n in sorted(counts.items()):
        print(f"  {bucket:<18} {n}")
    print(f"  {'TOTAL':<18} {len(hits)} lines / {total_occurrences} occurrences")
    for h in hits[:40]:
        print("   ", h)
    if len(hits) > 40:
        print(f"    … {len(hits) - 40} more")
    return 1 if hits else 0


if __name__ == "__main__":
    # --strict: also report the `member:` frontmatter key (tolerated by default)
    sys.exit(main("--strict" in sys.argv))
