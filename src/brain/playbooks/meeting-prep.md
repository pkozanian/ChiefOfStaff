---
name: playbook-meeting-prep
description: Prepare the principal for a specific meeting — context, goals, and a tight pre-read.
type: playbook
---

# Playbook: Meeting Prep

Run when preparing the principal for an upcoming meeting.

## Inputs to pull
Always deliver the pre-read below; **enrich it with live connector data** where available — don't
prep from stale memory alone, and don't turn prep into an interrogation.
- **Memory (always):** attendees → `memory/people/` (relationship, preferences, sensitivities);
  topic → the relevant `memory/projects/` file(s) and recent `memory/log/`; the principal's goals
  and standing preferences.
- **The calendar event** (calendar connector, if connected — `brain/integrations/calendar.md`):
  time, duration, attendees, location/link, and the invite's **agenda/description + any
  attachments**. Note back-to-back pressure around it.
- **Recent related mail** (mail connector, if connected): the latest threads with the attendees or
  on the topic, so the pre-read reflects what's actually happening now.
- **Related docs** (Drive / Confluence / Notion, if connected): the agenda doc, spec, or deck in
  play.

If a connector isn't available, build the pre-read from memory and whatever the principal has told
you, and just **note any gaps** — never block on a connector.

## Produce a pre-read
**Produce the pre-read in this turn — deliver it directly, don't just offer to.** Capture/index
housekeeping is fine, but it never replaces the deliverable.

1. **Bottom line** — what this meeting is for and the outcome the principal wants.
2. **Attendees** — who's in the room and what each cares about / their current stance.
3. **Context** — the 3–5 facts the principal needs fresh in mind (status, history, open items).
4. **Objectives** — what "success" is for this meeting; the decision(s) to land.
5. **Talking points / questions** — what the principal should say or ask.
6. **Watch-outs** — sensitivities, likely objections, anything to avoid.

Keep it to something readable in under two minutes.

## After
- Log outcomes, decisions, and new commitments (per `brain/schemas/capture-rules.md`), and
  update the relevant people/project files.
