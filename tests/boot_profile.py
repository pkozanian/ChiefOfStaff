#!/usr/bin/env python3
"""Boot profile — what an ordinary greeting costs, before the greeting.

Deterministic, read-only, spends no tokens. Point it at any install:

    python3 tests/boot_profile.py                    # the shipped tree (src/), no memory
    python3 tests/boot_profile.py ~/projects/ChiefOfStaff
    python3 tests/boot_profile.py <path> --paths      # also list always-load paths

Reports the files an ordinary boot must read, their size, an approximate token
count, an estimated operation count, and which requirements are deferred and on
what trigger. Content is never printed.
"""
import sys, re, math, pathlib

CHUNK_LINES = 200          # observed: files >340 lines are read in chunks; <=110 are not
TOK = 4                    # bytes per token, approximate

def links(md: pathlib.Path, heading: str) -> list[str]:
    """Relative link targets under `## <heading>`, up to the next H2."""
    if not md.exists():
        return []
    out, on = [], False
    for line in md.read_text(errors="replace").splitlines():
        if line.startswith("## "):
            on = line.strip().lower() == f"## {heading}".lower()
            continue
        if on:
            out += [t for t in re.findall(r"\]\(([^)]+)\)", line)
                    if not t.startswith(("http", "#", "mailto:"))]
    return out

class Group:
    def __init__(self, name, note=""):
        self.name, self.note, self.files = name, note, []
    def add(self, p):
        if p.exists() and p.is_file() and p not in self.files:
            self.files.append(p)
    @property
    def lines(self):  return sum(f.read_text(errors="replace").count("\n") for f in self.files)
    @property
    def bytes(self):  return sum(f.stat().st_size for f in self.files)
    @property
    def chunks(self):
        """Reads this group costs if each file is fetched whole."""
        return sum(max(1, math.ceil(f.read_text(errors="replace").count("\n") / CHUNK_LINES))
                   for f in self.files)

def profile(root: pathlib.Path, show_paths: bool):
    brain, mem = root / "brain", root / "memory"
    groups = []

    g = Group("entry + kernel", "read before anything else")
    for n in ("CLAUDE.md", "AGENTS.md", "CHIEFOFSTAFF.md"):
        g.add(root / n)
    groups.append(g)

    g = Group("routers", "fixed paths, wave 1")
    for p in (root/"VERSION", brain/"index.md", mem/"index.md", mem/"meta.md",
              mem/"overrides"/"index.md", mem/"confidential"/"registry.md"):
        g.add(p)
    groups.append(g)

    g = Group("brain always-load", "brain/index.md -> ## Always load")
    for t in links(brain/"index.md", "Always load"):
        g.add(brain / t)
    groups.append(g)

    g = Group("memory always-load", "memory/index.md -> ## Always load")
    for t in links(mem/"index.md", "Always load"):
        g.add(mem / t)
    groups.append(g)

    # Team: fires whenever memory/index.md links a roster — a property of the
    # install, not of the conversation.
    g = Group("team subsystem", "fires when memory/index.md links a roster")
    roster = mem/"team"/"index.md"
    if any("team/index.md" in t for t in links(mem/"index.md", "Always load")) and roster.exists():
        g.add(brain/"schemas"/"team-member.md")
        g.add(roster)
        for t in links(roster, "Active"):
            charter = (roster.parent / t).resolve()
            g.add(charter)
            g.add(charter.parent / "ledger.md")
    groups.append(g)

    g = Group("integrations", "pulled by boot steps 7 and 9 in practice")
    for n in ("hosts.md", "connectors.md", "updates.md"):
        g.add(brain/"integrations"/n)
    groups.append(g)

    print(f"BOOT PROFILE  {root}")
    v = root/"VERSION"
    print(f"version: {v.read_text().strip() if v.exists() else '(none)'}\n")
    print(f"{'group':<22}{'files':>6}{'lines':>7}{'bytes':>9}{'~tok':>8}{'reads':>7}  note")
    print("-" * 96)
    tf = tl = tb = tc = 0
    for g in groups:
        if not g.files:
            continue
        print(f"{g.name:<22}{len(g.files):>6}{g.lines:>7}{g.bytes:>9}{g.bytes//TOK:>8}{g.chunks:>7}  {g.note}")
        tf, tl, tb, tc = tf+len(g.files), tl+g.lines, tb+g.bytes, tc+g.chunks
    print("-" * 96)
    print(f"{'TOTAL':<22}{tf:>6}{tl:>7}{tb:>9}{tb//TOK:>8}{tc:>7}")

    over = [f for g in groups for f in g.files
            if f.read_text(errors="replace").count("\n") > CHUNK_LINES]
    if over:
        print(f"\nOver the {CHUNK_LINES}-line cap — each costs an extra read:")
        for f in sorted(over, key=lambda f: -f.read_text(errors='replace').count("\n")):
            n = f.read_text(errors="replace").count("\n")
            print(f"  {n:>5} lines  {math.ceil(n/CHUNK_LINES)} reads  {f.relative_to(root)}")

    if show_paths:
        for g in groups:
            if g.files and "always-load" in g.name or g.name == "team subsystem":
                print(f"\n{g.name}:")
                for f in g.files:
                    print(f"  {f.read_text(errors='replace').count(chr(10)):>4}  {f.relative_to(root)}")

    print("\nDeferred (brain/index.md -> ## Load on demand), with trigger:")
    idx = (brain/"index.md")
    if idx.exists():
        on = False
        for line in idx.read_text().splitlines():
            if line.startswith("## "):
                on = line.strip().lower() == "## load on demand"; continue
            if on and line.strip().startswith("- ["):
                m = re.match(r"- \[([^\]]+)\]\(([^)]+)\)\s*(?:—|-)\s*(.*)", line.strip())
                if m:
                    p = brain / m.group(2)
                    n = p.read_text(errors="replace").count("\n") if p.exists() else 0
                    print(f"  {n:>4} lines  {m.group(1):<28} {m.group(3)[:56]}")

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = pathlib.Path(args[0]).expanduser() if args else pathlib.Path(__file__).resolve().parents[1]/"src"
    profile(root.resolve(), "--paths" in sys.argv)
