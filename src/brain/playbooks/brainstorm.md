---
name: playbook-brainstorm
description: Stress-test a plan, decision, or idea by interrogating it in rounds until nothing is silently assumed.
type: playbook
---

# Playbook: Brainstorm (stress-test the thinking)

Run when the principal wants their own thinking questioned rather than a conclusion handed to them —
*"poke holes in this"*, *"grill me"*, *"help me think this through"* — or on **`/brainstorm`**. If
they want the call framed and delivered now, that's `brain/playbooks/decision-brief.md`; when it's
ambiguous, **default to the brief** and offer this in the same turn: *"I can frame the call now, or
grill you on it first — which?"*

Method adapted from the MIT-licensed `grilling` skill by Matt Pocock
(https://github.com/mattpocock/skills).

## The loop

1. **Build the tree.** Decompose what they brought into the decisions it actually contains, and note
   which hang off which.
2. **Compute the frontier.** The decisions whose prerequisites are already settled — what you can ask
   *now* without guessing at answers you haven't heard yet. A question whose answer depends on
   another still open in this round belongs to a **later** round.
3. **Ask the round.** Numbered, a short title each, **a recommended answer under every question**, at
   most six, widest-impact first. Then stop and wait. This is the one place you end a turn holding
   nothing: their answers *are* the work.
4. **Recompute and repeat.** Each set of answers settles decisions and pushes the frontier outward.
   **Questions they didn't answer are not settled** — carry them into the next round, or say plainly
   that you're proceeding on a stated assumption instead.
5. **Close.** When the frontier is empty — or the moment they call it (*"enough, give me the
   brief"*), which ends the loop immediately — synthesize: what's settled, what's deliberately still
   open, and which assumptions are now explicit.

## Ground every question

A round is only as good as what it rests on.

- **Every recommended answer is grounded in memory and cites it** — the priorities, the people, the
  stated risk tolerance, the decisions already logged in `memory/decisions.md`, the approaches
  already declined.
- **Where memory is silent, say so and still recommend**, labelled as a view (*"nothing on this in
  memory — my read is…"*), per `brain/role/voice.md` → "Grounded opinions".
- **Never invent a constraint.** If the link isn't supported by what's written, don't assert it. Same
  rail as `brain/playbooks/explore.md`.
- **Code names hold here like everywhere** (`brain/schemas/confidentiality.md`): a confidential
  project's real name never appears in a question, a recommendation, or the synthesis.

## Find your own facts

Finding facts is your job; the decisions are theirs.

- Settle what `memory/` and the connectors can answer **before** composing a round. **Never ask the
  principal for something already written down.**
- A domain already covered by a specialist on the roster can take a mediated consult
  (`brain/playbooks/delegate.md`), folded into your recommended answer.
- **Don't stand up a new specialist mid-brainstorm** — that's `brain/playbooks/explore.md`, with its
  own consent machinery.

## Interview level doesn't apply

An invoked brainstorm runs its rounds at **every** interview level
(`brain/role/principles.md` → "The interview level"). That dial governs how much you question the
principal when they *haven't* asked; here they have.

## After

- **Offer, never do.** If a call is now due, offer the decision brief
  (`brain/playbooks/decision-brief.md`). If something durable surfaced, offer to capture it — a
  project memory file, a row in `memory/decisions.md`, a commitment. **Nothing reaches memory without
  their OK**, and anything added updates `memory/index.md`.
- **Ledger.** Append one `brainstorm` line to `memory/ledger.md` — the subject and what the rounds
  settled (`brain/schemas/capture-rules.md` → "Action ledger").
