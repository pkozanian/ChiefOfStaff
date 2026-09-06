---
name: integration-routines
description: How Chief of Staff's briefs are delivered on a schedule via Claude Code Routines (overridable).
type: role
---

# Scheduled briefs (routines)

Run Chief of Staff on a schedule so briefs arrive automatically instead of only on request. **The mechanism
depends on the host** (see `brain/integrations/hosts.md`):
- **Claude Code desktop** — **Routines**. Chief of Staff **creates these itself** using its routine tools
  (the principal approves each tool execution) — see "Setting them up".
- **Codex (in the ChatGPT desktop app)** — **Scheduled** tasks (the Scheduled tab). Set one per brief with the same cadence
  + prompt (below); guide the principal to add them, or add them if the host lets you.

Either way the briefs **read `memory/`, so they must run *locally against this folder*** — *not* a
cloud/remote copy (which wouldn't have this principal's `memory/`; see "Setting them up"). The
cadences below are **defaults the principal can override or turn off** (see the Briefings section of
`brain/role/defaults.md`).

## Recommended routine set (defaults)

**Briefs** — regular deliverables:

| Brief | Default cadence | Routine prompt |
|-------|-----------------|----------------|
| Daily brief | weekday mornings (~8am) | "Run the daily-brief playbook and send me today's brief." |
| Weekly retro | Friday afternoon | "Run the weekly-retro playbook and send me the close-out." |
| Weekly preview | Sunday evening / Monday early | "Run the weekly-preview playbook and send me next week's look-ahead." |

**Maintenance** — keep memory clean and connected (read-only reports that *propose* changes, they
don't edit memory on their own):

| Routine | Default cadence | Routine prompt |
|---------|-----------------|----------------|
| Memory lint | monthly (1st, morning) | "Run the memory-lint playbook and send me the findings." |
| Explore | every 2 weeks | "Run the explore playbook and send me the connections." |

Each routine runs in the Chief of Staff project, so it loads the brain, reads `memory/`, uses the connected
**calendar**, and produces the brief. The maintenance routines also append a run entry to
`memory/ledger.md` (per `brain/schemas/capture-rules.md` → "Action ledger"), which is what the
session-start maintenance offer reads to know when they last ran (see `CHIEFOFSTAFF.md` boot protocol).

## Setting them up (onboarding or later)

Run this flow at onboarding step 6, on `/routines`, or whenever a brief would help. **It applies to
any scheduled task Chief of Staff creates** — the five default routines, per-specialist routines, and any
ad-hoc one-off (e.g. "remind me every Friday to send the update").

1. **Review what's already scheduled first — don't create blind.** Before proposing or creating
   anything, take stock of the current scheduled tasks: read the registry in
   `memory/preferences/briefings.md` (step 6 keeps it current — it's the reliable source), and if the
   host exposes a way to list existing routines/scheduled tasks, use that too. Hold that picture for
   the dedup check in step 3.
2. **Propose** all five at once as a compact menu with their default cadences (the tables above) —
   the three briefs plus the two maintenance routines (memory lint monthly, explore biweekly, each
   with its one-line benefit) — and ask for **yes / adjust the times / skip**. Frame them as good
   defaults.
3. **Before creating each task, check it against what's already scheduled — suggest a dedup on
   overlap.** Overlap = the **same purpose** (same playbook/brief) **or** an **overlapping
   cadence/time**. If a task would duplicate a current one, **don't silently add a second** — surface
   it and offer a choice: **update the existing one, adjust its timing, merge them, or skip**. Let the
   principal decide. If you can't tell for sure whether it already exists (empty registry and no way
   to list the host's tasks), **ask once** rather than assume ("looks like you may already have a
   daily brief — want me to update that one instead of adding a second?").
4. **Create each one they keep — how depends on the host** (`brain/integrations/hosts.md`):
   - **Claude Code:** create it **yourself with your routine tool** — don't make them open the UI.
     Create a **persistent Local routine** (runs in this project → reads `memory/`, brain, calendar)
     with the **schedule** + **prompt = run the matching playbook**. The principal **approves the
     tool execution** — that's the confirmation. Use a persistent (not session-only) routine.
   - **Codex:** add each as a **Scheduled** task (Scheduled tab) with the same cadence +
     prompt — do it if the host lets you, otherwise hand the principal the exact cadence + prompt to
     add. It must run **locally against this folder** so it can read `memory/`.
   - **Other host with no routine tool:** walk the principal through its scheduler (or a headless
     run + system cron), Name / Schedule / prompt = the routine prompt / working folder = this
     project, running **locally**.
5. **Changing or removing one later** (different time, turn one off) — update/delete it the same way
   for the host (your routine tool on Claude Code; the Scheduled tab on Codex). When the principal
   asks for a change, **prefer updating the existing task over creating a new one.**
6. **Record every scheduled task you create** in `memory/preferences/briefings.md` — its cadence, the
   prompt/purpose, the host, and status (`created`, `declined`, or `deferred`) — plus any cadence
   change as an override (per `brain/role/defaults.md`). Recording **every** task, not just the five
   defaults (ad-hoc ones too), keeps this file a complete, enumerable **registry** so step 1's review
   can dedup reliably even on a host that can't list its own tasks. This is also what lets Chief of
   Staff stop re-asking (see `CHIEFOFSTAFF.md` → CONNECTORS & ROUTINES) and what the session-start
   maintenance offer checks.

- **Why local (not cloud/remote):** a cloud/remote run happens on a **fresh copy with NO access
  to this principal's `memory/`** — so any memory-touching brief would see empty memory and produce an
  empty brief. A **local** run (Claude Code Routine, or a Codex Scheduled task on this folder)
  reads `memory/`, the brain, and the connected calendar. This is true on **every host**.
- Let them **change the times, or disable any** — these are defaults, not requirements.

## Per-specialist routines (virtual team cadence)
If the principal runs a **virtual team** (`brain/schemas/team-member.md`), a specialist's `cadence:`
duties become **Local routines** too, set up the same way (propose → create with the host's routine
tools / a **Scheduled** task, gated by the tool-approval prompt). A specialist routine's prompt is:
*"Act as `<slug>` (load `memory/team/<slug>/charter.md` + its memory + the shared brain in code
names), run this standing duty, then hand the result to Chief of Staff to verify and integrate."* It obeys the specialist's
`autonomy` (draft-and-wait ⇒ prepare and surface only — nothing outward/irreversible), must run
**locally** (it reads the specialist's own memory), and records its run in the specialist's `ledger.md`. On
a run is a persona-swap, the same on every host.

## Honest limits
- Scheduled briefs are what make **auto-delivery** possible — without them, briefs only run when asked.
- On **Claude Code**, you create routines yourself with your routine tools (not silently): each
  create/update surfaces a **tool-approval prompt** the principal accepts (and a one-time
  working-folder **trust** prompt may appear). On **Codex**, briefs are **Scheduled** tasks.
- A scheduled brief typically **only fires while the app is open and the machine is awake** (host
  behavior varies — e.g. Claude Code runs a single catch-up for a recent missed time). Each run
  arrives as a notification / new session — it isn't emailed.
- It must run **locally against this folder** — a cloud/remote run can't see the principal's
  `memory/`, so it would produce an empty brief. **Verify** a new host's scheduler runs locally
  (`brain/integrations/hosts.md`).
- A brief with no calendar connected still runs; it just asks for / omits the schedule (see
  `brain/integrations/calendar.md`).
