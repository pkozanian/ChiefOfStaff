---
name: team-member-review
description: Performance-review a virtual team member — memory health plus delegation track record.
argument-hint: "<specialist slug>"
---

Review the virtual team member named in `$ARGUMENTS` (or the request), following `brain/playbooks/team.md`.

- Run `brain/playbooks/memory-lint.md` scoped to `memory/team/<slug>/` (stale, orphans, broken
  links, uncited facts) **and** read `memory/team/<slug>/delegations/` for a track record (delivered
  vs rejected, overdue, revise-loops).
- **Report only — don't rewrite.** Give a health read + track record, bottom line first, with a
  proposed fix per finding; offer to apply on my OK.
- If no slug is given, list the team via the roster's `## Active` section in `memory/team/index.md`
  — **not** by scanning `memory/team/*/charter.md` — and ask which to review.
