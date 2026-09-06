---
name: playbook-draft-comms
description: Draft emails/messages/updates in the principal's voice — never send without an OK.
type: playbook
---

# Playbook: Draft Comms

Run when the principal needs a message drafted — an email, a Slack/Teams reply, a stakeholder or
board update. You **draft**; the principal sends.

## Inputs to pull
- Who it's for → their file in `memory/people/` (relationship, how they operate, sensitivities).
- What it's about → the relevant `memory/projects/` file and recent context.
- The principal's voice (`brain/role/voice.md`) and comms preferences (`memory/preferences/`).

## Produce
1. **The draft** — in the principal's voice: tight, clear, right tone for the recipient. Lead with
   the point.
2. **Subject / opener** where relevant.
3. **Options** — if tone or framing is a real choice, offer 2 (e.g. warmer vs. firmer) rather than
   guessing.
4. A one-line note on anything you assumed or left blank for them to fill.

## Sending — the hard rule
**Never send without explicit confirmation.** With a mail connector (Gmail, or Microsoft 365 /
Outlook), **create the message as a draft in the mailbox** — it lands in their Drafts ready to
review, edit, and send themselves — do **not** auto-send. (No mail connector → just give them the
text to paste.) Anything outward-facing waits for a clear go (per `brain/role/principles.md`).
Before drafting, also keep private memory out of the message itself — see
`brain/schemas/confidentiality.md` → "Principal-private material in shared outputs".

## After
- A draft the principal wants **as a file** goes to `memory/desk/`, linked from the desk index
  (`brain/schemas/memory-file.md` → "The desk") — never to the folder root.
- If the message creates a commitment or follow-up, add it to `memory/commitments.md`.
