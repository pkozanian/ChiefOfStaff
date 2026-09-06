---
name: playbook-daily-brief
description: Start-of-day brief — what's on today, what needs the principal, commitments due.
type: playbook
---

# Playbook: Daily Brief

Run at the start of the day (usually delivered by a scheduled **Routine** — see
`brain/integrations/routines.md`) or on request. Keep it tight — readable in under a minute.

## Inputs to pull
- **Calendar** (if connected — see `brain/integrations/calendar.md`): today's meetings.
- **Commitments** (`memory/commitments.md`): due today / overdue.
- Active projects and their status; the principal's top priorities (`memory/profile/`).
- Anything captured since yesterday worth surfacing.

## Produce
**Produce the brief in this turn — deliver it directly, don't just offer to.** Capture/index
housekeeping is fine, but it never replaces the deliverable.

1. **Bottom line** — one line: the single most important thing about today.
2. **Today's schedule** — meetings in order; flag any that need prep and offer to prep them.
3. **Needs you** — decisions/asks/approvals waiting on the principal.
4. **Due today / overdue** — from the commitments tracker; lead with overdue.
5. **Top 1–3 focus** — what to actually spend the day on; what to protect time for.

If no calendar is connected, say so briefly and ask for today's meetings (or proceed without them).
