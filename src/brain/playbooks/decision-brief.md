---
name: playbook-decision-brief
description: Turn a pending decision into options and a clear recommendation.
type: playbook
---

# Playbook: Decision Brief

Run when the principal faces a decision and needs it framed for a call.

## Frame it (don't stall on questions)
Settle these from memory — and where memory is silent, **state your assumption and proceed**. Only
ask a question if the answer would flip the recommendation and you genuinely can't infer it; put the
rest under **Open questions** in the brief rather than holding the brief back. (At interview level
**`thorough`** — `brain/role/principles.md` → "The interview level" — ambiguity that would flip the
recommendation may be asked **first**, one batch, before the brief; at every other level this
playbook's deliver-in-this-turn contract holds.) Settle:
- What exactly is being decided, and by when?
- What's the objective / what does a good outcome protect or achieve?
- What constraints apply (time, budget, people, reversibility)?

## Produce
**Produce the full brief in this turn — lead with the recommendation and deliver it directly, don't
just offer to.** If a decision is stated or implied, you also log it to `memory/decisions.md` with
RAPID roles (per `brain/playbooks/decisions.md`) — but that logging is a **side-effect that happens
alongside the brief, never in place of it**. A reply that only logs the decision and asks what to do
next is a failure of this playbook.

**Role coverage.** If the decision clears the right-size bar, sweep for role holders as part of that
logging step (`brain/playbooks/decisions.md` → "Role coverage"): run a specialist's mediated consult
inline and fold the read into the brief, and leave the fuller work-up and any outreach draft as
offers in this same turn. **Neither offer holds the brief** — the deliver-in-this-turn contract above
governs.

1. **Decision** — state it in one sentence, with the deadline.
2. **Recommendation** — your recommended option, up front, in one line.
3. **Options** — 2–4 realistic options. For each: what it is, key pros, key cons, and the main
   risk. Note which are reversible.
4. **Why the recommendation** — the reasoning, tied to the objective and constraints.
5. **What it costs to be wrong** — the downside of the recommended path and how to mitigate.
6. **Open questions** — what's still unknown and how to resolve it, if that changes the call.

## Principles
- Make a real recommendation; don't hedge into a menu.
- Flag irreversible options clearly — the bar for those is higher.
- Check the deadline is real: **urgency masquerading as importance** is how a reversible decision
  steals an irreversible one's attention. Ask what waiting a week actually costs.
- Keep the principal's stated risk tolerance and priorities in view.

## After
- Log the decision and rationale as a row in `memory/decisions.md` with RAPID roles once made — the
  same logging step as "Produce" above, confirmed done (per `brain/schemas/capture-rules.md` routing
  table; `brain/playbooks/decisions.md` is the single source of truth for the log's shape). A dated
  `memory/log/` note may additionally record the event, but the decision + RAPID themselves live in
  `memory/decisions.md` so later briefs that read it actually surface it; update affected projects.
