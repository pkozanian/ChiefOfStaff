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
2. **Today's schedule** — meetings in order; flag any that need prep.
3. **Needs you** — decisions/asks/approvals waiting on the principal.
4. **Due today / overdue** — from the commitments tracker; lead with overdue.
5. **Top 1–3 focus** — what to actually spend the day on; what to protect time for.
6. **Want me to…** — up to three offers, numbered, verb-first, each naming the work and where it came
   from: *"1. Prep you for the 2pm with Dana — you haven't met since the pricing call
   (`memory/people/dana.md`)."* One word answers it; "1 and 3" is a complete reply. This is where the
   brief's offers live — the sections above inform, they don't solicit.

**Where the offers come from** — today's inputs, never what a principal in this role probably needs:
- a meeting today with no pre-read on file → offer the prep (`brain/playbooks/meeting-prep.md`)
- an overdue commitment whose `owner` isn't the principal → offer the nudge (`brain/playbooks/commitments.md`)
- a decision in play with no options recorded → offer the decision brief (`brain/playbooks/decision-brief.md`)
- a project gone quiet → offer to draft the status ask (`brain/playbooks/draft-comms.md`)

Each offer cites the memory file, calendar entry, or commitment row behind it, and is work you can
start this turn. **No qualifying offer, no section** — never print an empty one.

If no calendar is connected, say so briefly and ask for today's meetings (or proceed without them).
