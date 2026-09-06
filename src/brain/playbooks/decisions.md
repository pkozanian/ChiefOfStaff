---
name: playbook-decisions
description: Log every decision (implied or explicit) as a tracked item with RAPID roles.
type: playbook
---

# Playbook: Decision Log (RAPID)

Decisions are how the org actually moves — and they get lost in chat. **Whenever a decision is made
or implied — explicitly ("we're going with X") or implicitly ("let's just ship it Friday") — call it
out and log it as its own tracked item** in `memory/decisions.md`, with roles per **RAPID**. This is
always-on capture (see `brain/schemas/capture-rules.md`), not only on request.

This playbook **logs and tracks** decisions. To *help the principal make* a hard one (options +
recommendation), use `brain/playbooks/decision-brief.md` — the two are complementary.

## The log — `memory/decisions.md`

A single file. Frontmatter `type: decision`. One row per decision:

```markdown
---
name: memory-decisions
description: Decision log — one row per decision, with RAPID roles and status.
type: decision
updated: <YYYY-MM-DD>
---

# Decisions

| decision | status | R (recommend) | A (agree) | P (perform) | I (input) | D (decide) | date | rationale / source |
|---|---|---|---|---|---|---|---|---|
| Go with vendor X over Y | decided | Jane | — | Ops | Finance, Security | me | 2026-07-20 | lower TCO; [migration](projects/migration.md) |
| Reorg the data team | open | Raj | HR | — | Raj, leads | me | due 2026-08-01 | consolidate on-call |
```

- **status**: `open` · `decided` · `reversed` (if a later decision overturns it, mark the old row
  `reversed` and add the new one — keep the log the source of truth, newest wins).
- **RAPID roles** (people from `memory/people/` where known; `me` = the principal; `—` if none):
  - **R — Recommend**: drives the proposal, gathers input.
  - **A — Agree**: must sign off / has veto — only for specialized decisions (legal, compliance).
  - **P — Perform**: executes once decided.
  - **I — Input**: consulted for information/advice (SMEs, affected stakeholders); no approval.
  - **D — Decide**: the single decision-maker.
- **date**: when decided (or `due <date>` while open). **rationale/source**: the why + where it came
  from (link the project/meeting).

## Capturing a decision
1. **Spot it.** A decision is a *choice with consequences and alternatives* (vs a mere task, which
   goes to `memory/commitments.md`). One decision can **spawn commitments** — those are the **P**.
2. **Log it** as a row; assign RAPID roles from what you know.
3. **Fill gaps, don't fabricate.** If who **Decides** (or **Agrees**) is unclear, leave it blank and
   **ask the principal** — never invent authority.
4. **Right-size RAPID.** Full roles are for **complex, high-stakes, multi-stakeholder** decisions.
   For a small/one-person call, log it lightly (decision + `D` + date) — don't force five roles.
5. **Sequence** (when helping run one): gather **Input first**, then Recommend → Agree → Perform
   stages, then **Decide**.
6. Confidential decisions use the **code name** only.
7. **Tell the principal** what you logged, in one line.

## An unnamed decision
Sometimes the principal states a situation, not a choice — *"Meridian's slipping again."* If a choice
with consequences follows from it and nobody has named one, say so.

**The test is who voiced it.** A choice the principal named is logged (Capturing, above). One *you*
inferred is **surfaced, not logged** — writing a row they never agreed to invents the decision along
with the authority (Capturing step 3).

1. **Name it in one line**, with what makes it a choice: *"That's a call, not just a slip — re-scope
   or move the date. Want me to log it and work it up?"*
2. **At most one per turn.** If several surface, take the one with the nearest consequence.
3. **On their yes** — log it `open`, settle a **due**, and continue through Capturing and Role
   coverage as normal. **On their no** — drop it, and don't argue it.

## Role coverage — sweep for who's missing
When a decision clears Capturing step 4's bar (**complex, high-stakes, multi-stakeholder**), sweep
for role holders before the row is final. A small one-person call skips this entirely — don't read
the roster for it.

1. **Sweep both benches.** The people hooks in `memory/index.md`, and the `## Active` entries in
   `memory/team/index.md` (match on routing hook + `specialization`). Per role ask: who is affected,
   who executes, who knows something you don't.
2. **A and D stay human.** An unclear **Decide** or **Agree** is still left blank and asked (Capturing
   step 3) — a sweep may not fill authority it inferred, and **a specialist never holds A or D**.
   A specialist may hold **R**, **I**, or **P**.
3. **Virtual gaps — act on them.** Where a specialist's specialization lands on a role, say which depth
   you recommend and name the other: a **full delegation** for **R** (driving a recommendation is real
   work, and the record makes it auditable), a **mediated consult** for **I** (usually a read) — both
   in `brain/playbooks/delegate.md`. The principal picks.
4. **Real gaps — recommend, then offer the draft.** Name who should be looped in and why, and **offer
   to draft the outreach** (`brain/playbooks/draft-comms.md`). Never contact anyone yourself, and
   never draft unasked — the offer is the step (principle #3).
5. Confidential decisions are handed down and drafted in **code names**
   (`brain/playbooks/delegate.md` step 1, `brain/schemas/confidentiality.md`).

Both offers ride the line that already reports what you logged (Capturing step 7). Neither replaces
work you could already do.

## Surfacing & closing the loop
- In briefs/reviews, surface **open** decisions (esp. past their `due`) and what they're waiting on.
- When a decision lands, set `decided` + the date + rationale. If it's later **reversed**, mark the
  old row and add the new one (so the log always reflects the current call).
