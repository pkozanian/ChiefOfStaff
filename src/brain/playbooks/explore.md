---
name: playbook-explore
description: Surface non-obvious connections across the principal's people, projects, and decisions.
type: playbook
---

# Playbook: Explore (connect the dots)

Turns Chief of Staff's **Anticipate** mandate (`brain/role/charter.md`, `brain/role/principles.md`) into a
workflow: mine `memory/` for relationships the principal hasn't connected yet, and surface the ones
worth acting on. Runs on **`/explore`** or when the principal asks "what am I missing / connect the
dots". Distinct from `memory-lint.md` (which checks memory is *correct*) — explore looks for
*insight*.

**Ground everything in stored memory. Never invent a connection** — if the link isn't supported by
what's actually written, don't claim it.

## Scope
Explore all of `memory/` by default; if `$ARGUMENTS` names a person, project, or theme, center the
exploration there. Start from `memory/index.md`, then read the memory files.

## Find the connections
Scan for entities or topics that appear across **multiple files but aren't directly linked**, e.g.:
- A person who recurs in several projects but has no stated role in one of them.
- Two projects that share an owner, a dependency, a deadline, or a risk — but neither memory file mentions
  the other.
- A decision (`decisions.md`) or commitment (`commitments.md`) that bears on a project or person not
  cross-referenced.
- A stated preference or sensitivity that's relevant to an upcoming meeting or open decision.
- A risk or blocker in one place that threatens a goal recorded elsewhere.
- A **domain that recurs across several memory files with no team member covering it** — a specialist the
  principal keeps needing and doesn't have. Read coverage from the roster's `## Active` entries
  (`brain/schemas/team-member.md`); with no roster linked, nothing is covered.

## Produce
Deliver in this turn — **bottom line first** (`brain/role/voice.md`): the single most useful
connection, then a short ranked list. For each connection:
1. **The link** — the two (or more) things and how they connect, citing the memory files.
2. **The insight** — why it might matter (a risk to flag, a person to loop in, a dependency to
   sequence, a question to ask).
3. **What would confirm it** — the fact or source that would validate the hunch (and whether it's
   already in memory or a gap to fill).

Pick the few most interesting connections, not every pair — signal over volume. If nothing
non-obvious surfaces, say so honestly.

## Suggest a team member (when one is obvious)
A recurring domain with nobody on it is a connection like any other, and the run that reads the whole
tree is the one placed to notice it. **Same grounding rail as every finding above:** the domain must
be named in **at least two** memory files. Never infer one from what a principal in this role
probably needs.

Before filing anything:
- **Read `memory/team-suggestions.md`.** A slug under `## Declined` is a permanent no — never
  re-suggest **that domain**. It says nothing about any other: a declined specialist is not a
  declined feature, and a different gap still earns a suggestion. An entry under `## Pending` means
  file nothing this run; surface the existing one instead if it fits.
- **Skip entirely** if `team-offer: off` is set in `memory/preferences/briefings.md`.
- **One per run at most** — the widest-spread gap if several qualify.

**Offer it in this turn** — the principal is here. Name the domain, the memory files it recurs across, and
that nobody covers it: *"You keep running into reliability — Meridian, the on-call rotation, and the
Q3 OKR all turn on it, and nobody on your roster owns it. Want me to stand up a reliability
specialist?"*
**Write the `## Pending` entry as you make the offer** — creating the file and its generic
`## Always load` pointer in `memory/index.md` if this is the first one
(`brain/schemas/team-member.md`). Don't wait to see whether they answer: you have no moment at which
to notice that they didn't, and an offer that evaporates when the session does is not persisted.
Then resolve it the moment they answer (`brain/playbooks/team.md` → "Answer a suggestion"): **yes** —
run "Onboard a specialist" now and delete the entry; **no** — move the slug to `## Declined` with today's
date, permanently.

Unanswered, the entry stays, and the next session's maintenance offer raises it
(`CHIEFOFSTAFF.md` boot step 8).

## After
- **Offer to act** on confirmed connections: add cross-reference links between the related memory files
  (standard markdown links, per `brain/schemas/memory-file.md`), create a new memory file if a theme
  deserves one, or turn an insight into a commitment/decision to track. Apply only on the
  principal's OK, and update `memory/index.md` for anything you add.
- If a connection reveals a **gap** (something worth knowing but not recorded), flag it and suggest
  what would fill it (a note to capture, a question to answer).
- **Ledger.** Append one `explore` line to `memory/ledger.md` — the run and the connection(s)
  surfaced (`brain/schemas/capture-rules.md` → "Action ledger").
- **Clock.** Set `last_explore: <today's date>` in `memory/meta.md`. This is what resets the
  session-start maintenance offer (`CHIEFOFSTAFF.md` boot step 8); without it the offer re-fires next
  session as though the run never happened.
