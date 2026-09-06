---
name: playbook-weekly-retro
description: Weekly close-out — look back at the week: what moved, what closed, what slipped, lessons.
type: playbook
---

# Playbook: Weekly Retro (close-out)

Run at the end of the week (usually delivered by a scheduled **Routine** — see
`brain/integrations/routines.md`) or on request. Backward-looking; pairs with `weekly-preview`.

## Inputs to pull
- Active projects (`memory/projects/`) and status changes over the week.
- The **commitments tracker** — what closed, what's still open, what slipped past its date.
- Calendar (if connected): the week's meetings and outcomes; the `log/` for decisions captured.

## Produce
**Produce the retro in this turn — deliver it directly, don't just offer to.** Capture/index
housekeeping is fine, but it never replaces the deliverable.

1. **Bottom line** — one line: how the week went and the headline.
2. **What moved / closed** — progress and wins, tied to projects and commitments completed.
3. **What slipped** — commitments past due, stalled projects; be honest, name the cause.
4. **Lessons / patterns** — anything worth adjusting (recurring blockers, over-commitment).
5. **Carry-over** — open items that roll into next week (feeds `weekly-preview`).

## After
- Update project statuses and mark completed commitments `done` (per
  `brain/playbooks/commitments.md`).
