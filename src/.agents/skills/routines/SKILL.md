---
name: routines
description: Propose and set up the Chief of Staff's routines (daily / weekly retro / weekly preview briefs, plus memory-lint and explore maintenance), or change their cadence.
argument-hint: "[optional: e.g. 'move the daily brief to 7am' or 'turn off explore']"
---

Set up or adjust the **Routines**, following `brain/integrations/routines.md` → "Setting them up".

- **First, review what's already scheduled** — read `memory/preferences/briefings.md` (and list the
  host's routines/Scheduled tasks if you can). **Before creating any task, dedup:** if it overlaps a
  current one (same purpose, or overlapping cadence/time), surface it and offer to **update the
  existing one / adjust its timing / merge / skip** rather than adding a duplicate.
- If `$ARGUMENTS` (or the request) asks for a change (a new time/cadence, or turning one off), apply
  just that: **update or delete the affected routine yourself with your routine tools** (update the existing one,
  don't add a new one), and record it in `memory/preferences/briefings.md` (and as an override per
  `brain/role/defaults.md`).
- Otherwise, **propose** all five with their default cadences as one compact menu — the three briefs
  (daily brief · weekly retro · weekly preview) plus the two **maintenance** routines (memory lint,
  monthly · explore, biweekly), each with its one-line benefit — and ask for
  **yes / adjust the times / skip**.
- **For each one they keep, create it yourself with your routine tools** — a **persistent Local**
  routine (working folder = this Chief of Staff project; prompt = run the matching playbook). The principal
  **approves the tool execution** when prompted; that's the confirmation — don't hand them manual
  setup steps (UI walk-through only if no routine tool is available).
- **Record the outcome** per brief in `memory/preferences/briefings.md` (`created` / `declined` /
  `deferred`) so the Chief of Staff doesn't re-ask.
- Note the honest limits from `routines.md`: Local routines only fire while the desktop app is open
  and awake, and each run arrives as a notification + a sidebar session.

Finish with a short summary: which routines are now set (and when), and anything deferred.
