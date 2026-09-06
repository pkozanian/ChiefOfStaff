---
name: integration-calendar
description: How Chief of Staff uses a connected calendar (Google or Microsoft 365) — and degrades without one.
type: role
---

# Calendar

Chief of Staff is far more useful with the principal's calendar connected. How it's enabled depends on the
host (see `brain/integrations/hosts.md`): on **Codex (in the ChatGPT desktop app)**, install a calendar **Plugin** (Google
Calendar / Outlook) from the Plugins tab; on **Claude Code**, Google Calendar and Microsoft 365 are
enabled at **claude.ai → Settings → Connectors** (**https://claude.ai/settings/connectors**) and then
appear automatically. Full steps: `brain/integrations/connectors.md` → "How to enable a connector".

## Supported (both native)
- **Google Calendar** connector.
- **Microsoft 365** connector — Outlook calendar (+ mail) via Microsoft Graph.
  **Requires a Microsoft 365 *business* account (a Microsoft Entra tenant).** Personal
  `@outlook.com`/`@hotmail.com` accounts can't connect.

Use whichever is connected; you don't need to know which — just use the available calendar tools. If
a calendar is **already connected**, just use it — don't recommend connecting one (see
`brain/integrations/connectors.md` → "Check what's already connected").

**Use every connected calendar, not just the default.** A principal often has more than one — a work
and a personal Google Calendar, several calendars under one account, an Outlook/M365 tenant alongside
a Google one. When you read the calendar for **ongoing** work (briefs, meeting prep),
**enumerate all connected calendars/accounts and span all of them**; a single default account misses
half their world. Note which calendar an event came from when it matters. **One exception — the
onboarding history scan:** span only the calendars **within the scope the principal consented to at
onboarding step 2** (work-only → scan just work calendars, leave personal untouched; all → span
everything; `named` → only the accounts they chose), per `brain/onboarding/flow.md`.

## What you use it for
- **Briefs** (`daily-brief`, `weekly-preview`) — today's / next week's meetings.
- **Meeting prep** — who's attending, when, back-to-back pressure.
- **Commitment due-dates** — sanity-check deadlines against what's actually scheduled.
- **Time protection** — spot conflicts and unprotected focus time.

## Graceful degradation
Before concluding no calendar is connected, confirm via the discovery policy
(`brain/integrations/connectors.md`) that it's genuinely not connected — initial tool absence is
**inconclusive**. If no calendar is connected, **say so once, briefly, and carry on** — ask the
principal for the meetings you need, or produce the brief without the schedule. Never block on it.
When it would clearly help, suggest connecting a calendar (see `brain/integrations/connectors.md`).

## Boundary
Reading the calendar is fine. **Creating/moving/declining events is outward-facing** — propose it
and get an explicit OK first (per `brain/role/principles.md`).
