---
name: playbook-inbox-triage
description: Triage incoming messages/requests and decide what actually needs the principal.
type: playbook
---

# Playbook: Inbox Triage

Run when triaging a batch of messages, requests, or asks and deciding what reaches the principal.

## Inputs to pull
- Standing rules and preferences (`memory/preferences/`) — escalation bar, what to auto-handle.
- People context (`memory/people/`) — who's asking and how much weight they carry.
- Active priorities (`memory/projects/`, `memory/profile/`) — what's relevant right now.

## Sort each item into
1. **Needs the principal** — requires their decision, voice, or attention. Summarize crisply and
   say what's being asked and by when. The sharpest test for this tier: **would this surprise them
   in a way that damages their position?** If yes, it goes up now — being blindsided by something
   you knew is the one failure triage exists to prevent.
2. **Draft-and-confirm** — you can handle it; prepare a response/action for a quick yes.
3. **FYI** — worth awareness, no action. Batch these.
4. **Noise** — no action, no need to surface.

## Produce
- A short triage summary: the **needs-principal** items first (most urgent first), then the
  draft-and-confirm items with drafts ready, then a batched FYI list.
- Lead with a one-line bottom line: how many items, and the single most time-sensitive one.

## Principles
- Protect the principal's focus — escalate only what genuinely needs them.
- Never send or commit anything outward without explicit confirmation.

## After
- Capture any commitments, deadlines, or decisions that emerge
  (per `brain/schemas/capture-rules.md`).
