---
description: Audit the Chief of Staff's memory for staleness, contradictions, orphans, and broken links.
argument-hint: "[optional: a memory/ subpath or file to scope the lint]"
---

Run the memory-lint audit now, following `brain/playbooks/memory-lint.md`.

- If `$ARGUMENTS` (or the request) names a subpath or file (e.g. `people/`, `projects/onyx.md`), scope
  the lint to it; otherwise audit all of `memory/`.
- Read `memory/index.md` first, then the memory files; check for stale claims, contradictions, orphan files,
  broken links, uncited durable facts, duplicates, and missing cross-references.
- **Report only — don't rewrite memory.** Deliver a grouped findings list (bottom line first) with a
  proposed fix per item, then offer to apply the fixes on my OK.

If `memory/` is empty or missing, say so and do nothing.
