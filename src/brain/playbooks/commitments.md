---
name: playbook-commitments
description: Track commitments/follow-ups to completion — surface what's due, overdue, or slipping.
type: playbook
---

# Playbook: Commitments

The engine behind "nothing the principal cares about drops." Runs when the principal asks what's on
their plate, during briefs/weekly-review, or whenever a commitment is made or completed.

## The tracker — `memory/commitments.md`
A single running table (not one file per item). Append rows; check items off in place; move done
rows to `memory/commitments/done.md` when the table gets long.

```markdown
---
name: memory-commitments
description: Open commitments and follow-ups Chief of Staff tracks to completion.
type: commitment
updated: <YYYY-MM-DD>
---

# Commitments

| what | owner | due | status | source |
|------|-------|-----|--------|--------|
| Send the board deck | me | 2026-07-25 | open | staff mtg |
| Reliability review | Jane | 2026-07-30 | open | [platform migration](projects/platform-migration.md) |
```
- `owner`: `me` (the principal) or a person (link to `people/` where useful).
- `due`: an **absolute** date (convert "Friday" → the date).
- `status`: `open` · `done` · `blocked`.
- `source`: where it came from (a meeting, a note, a project).

## Capturing a commitment
When the principal (or someone) commits to something — a decision to act, a deadline, a follow-up —
**append a row** (per `brain/schemas/capture-rules.md`). Don't bury it in a `log/` entry; the
tracker is the one place open items live.

## Surfacing (the review)
When asked "what's on my plate / what's due", or inside a brief:
1. **Overdue** — past `due`, still `open`/`blocked`. Lead with these.
2. **Due soon** — today / this week.
3. **Slipping** — open, no movement, or a `blocked` item that needs unblocking.
4. **Waiting on others** — `owner` ≠ me; note who to nudge, and **offer to draft the nudge**
   (email/Slack via the connector, per `brain/playbooks/draft-comms.md`) for a one-tap send — never
   send without an OK.
Give a tight, prioritized list — bottom line first.

**Don't just list the urgent ones — surface them.** For a genuinely time-sensitive item (an
**overdue** commitment, an imminent hard deadline), raise it proactively — a **desktop
notification** if available, or a reminder **routine** (`brain/integrations/routines.md`) — rather
than waiting for the next brief.

## Closing the loop
When something's done, mark the row `done` (and date it in `source`/notes); archive to
`memory/commitments/done.md` periodically. **The first time you create `memory/commitments/done.md`,
link it from `memory/commitments.md`** (or the index) so the archive stays reachable per the
reachability invariant (`brain/schemas/memory-file.md`) — not an orphaned file off the tracker. When
a commitment is dropped deliberately, remove it and tell the principal. Accurate > complete.
