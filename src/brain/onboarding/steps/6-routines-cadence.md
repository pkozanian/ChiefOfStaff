---
name: onboarding-step-routines
description: Onboarding step 6 — Rhythms, and the five routines as one accept-all-defaults ask.
type: role
---

# Routines & cadence
*Render the progress bar (`Step 6/6 · Routines & cadence`).* Recurring commitments and rhythms
(weekly review day, 1:1 schedule, reporting cadence). Note which playbooks matter most. Capture
into the relevant files (preferences/projects/people). A calendar screenshot can quickly show the
recurring rhythms if they'd rather upload than describe.

**By mode:** *work* — work rhythms (staff meeting, 1:1s, reporting/review days). *personal* — life
rhythms (a weekly review, bills/renewals, standing family or household commitments). The brief
routines below apply either way — a daily brief for a **personal** Chief of Staff surfaces the day's appointments and
commitments, not work.

**Infer the cadence from the calendar if a connector is on.** If the step-2 fast-track bootstrap already
ran, **confirm the rhythms it captured** and fill gaps. Otherwise read the recurring events **across
every connected calendar** — **honor the `bootstrap_scope` recorded at step 2** (`work-only` → work
calendars only; `named` → only the accounts they chose; `all` → everything); if none was recorded because no bootstrap ran, **default to work calendars, or
disclose scope in one line before including personal** (**in personal mode**, stay account-neutral —
honor any recorded scope, else read **the calendars you've connected** or ask account-neutrally, never
defaulting to a near-empty work-only scan) — to
**propose** the principal's actual rhythms (weekly staff meeting, 1:1 schedule, review/reporting
days) instead of asking them to list it from memory — then confirm and capture. (No connector → ask,
or take the screenshot upload.)

**Then set up the routines — don't make them do it by hand.** Proactively **propose** all five with
their default cadences (`brain/integrations/routines.md` → "Setting them up"):
- the three **briefs** — daily brief, weekly retro, weekly preview; and
- the two **maintenance** routines, each with its one-line benefit: **memory lint** (monthly —
  *"keeps your memory accurate: catches stale statuses, contradictions, and broken links"*) and
  **explore** (biweekly — *"surfaces connections and risks across your people/projects/decisions you
  might've missed"*).

**Present this as one accept-all-defaults ask, not five separate ones** — *"Want me to set up all five
with these defaults? Say the word to adjust any of the times, or skip whichever you don't want."* Only
break it into individual questions if the principal wants to customize.

**Before creating any of them, check what's already scheduled and dedup** (`brain/integrations/routines.md`
→ "Setting them up"): read `memory/preferences/briefings.md` for routines already set up — likely on a
re-run of `/onboard` or a partial prior setup — and for any that already exist, **update or skip rather
than create a duplicate**. Keep this inside the single accept-all-defaults ask above; it's not a new
separate question.

For each one they keep, **set it up per the host**: on **Claude Code**, create it yourself with your
routine tools (they approve the tool execution — that's the confirmation); on **Codex**, add a
**Scheduled** task — if the host lets you add it directly, do so, otherwise hand the principal the
exact cadence + prompt to paste in (Scheduled tab). All run **locally** so they read `memory/`. Record
the outcome per routine (`created` / `declined` / `deferred`) in `memory/preferences/briefings.md` so
Chief of Staff doesn't re-ask later. **When a brief routine is actually created, land the payoff — make it
real, not just configured — but keep the promise honest.** A routine only fires while the app is open
and the machine's awake (`brain/integrations/routines.md` → "Honest limits"), so don't promise a
specific next timestamp — name the **cadence** and be upfront that it needs the app open. For each one
you create (skip anything declined or deferred), close with ~1 line:
- **Claude Code (auto-created):** *"Done — your daily brief is set for weekday mornings around 8am. It
  runs whenever the app's open, so you'll see it next time you're around."*
- **Codex (principal adds the Scheduled task):** frame it as handing over the setup, not "I handled
  it" — *"Here's the exact schedule and prompt to paste into a Scheduled task: weekday mornings ~8am,
  'Run the daily-brief playbook and send me today's brief.' Once it's in, your brief runs whenever
  ChatGPT's open around that time."*

If they'd rather not decide now, mark them `deferred` and note they can ask anytime (**`/routines`** on
Claude Code; the Scheduled tab on Codex). Also mention that between scheduled runs, Chief of Staff will
**offer at session start** (only when a lint/explore is due) to run them — and that's toggleable.

**Checklist:** `rhythms`; `routines` → `done` once every routine has a recorded outcome in
`briefings.md` (a routine marked `deferred` there is still a `done` ask), or `deferred` on the
express path.
