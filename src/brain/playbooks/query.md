---
name: playbook-query
description: Answer a substantial question from memory — synthesize, cite the memory files, and compound.
type: playbook
---

# Playbook: Query (answer from memory)

Runs whenever the principal asks a **substantial question that memory can answer** — recall, status,
"what do we know about X", "who owns Y", cross-file synthesis. (The briefs — daily/weekly/meeting/
decision — are specialized versions of this; they follow the same cite-your-sources discipline.)
Trivial one-liners don't need this playbook.

## Workflow
0. **Route first, if there's a team.** When `memory/index.md` links a team roster
   (`memory/team/index.md`, see `brain/schemas/team-member.md`), decide who answers: handle it
   yourself from shared memory (the default for anything general or trivial), or — if a roster
   `## Active` **specialist** would answer it materially better — consult/delegate to **the
   right** specialist (matched via its routing hook + `specialization`,
   `brain/playbooks/delegate.md`) and **integrate** their answer into one reply. Consider only
   `## Active` specialists; never filesystem-discover a specialist. Route only when depth beats breadth; the
   principal still gets a single coherent answer (unless they asked to talk to the specialist directly,
   `brain/playbooks/team.md`).
1. **Find the memory files.** Read `memory/index.md`, then open the memory files relevant to the question —
   **follow their links** (and backlinks) for connected context. Don't answer from the index alone.
   - **Temporal or multi-hop questions escalate to the log.** When the question reaches into the
     past ("what did we decide about X?", "last month…") and the index hooks give no strong hit,
     don't answer thinly from always-load context — walk `memory/log/` (newest-first, bounded by
     the timeframe in the question) and `memory/ledger.md` chronologically, then synthesize with
     cites per the existing `## After`.
2. **Synthesize** — a clear answer, **bottom line first** (`brain/role/voice.md`). Pull the facts
   together; don't just dump memory files.
3. **Cite the sources — when it matters or on request.** If the principal asks for sources, or a
   claim is material/surprising/verification-sensitive, cite the memory file(s) it rests on — an
   inline `(per [memory file](path))` on the claim, or a trailing `**Sources:**` line listing the memory files as
   markdown links (reuse the provenance style, `brain/schemas/memory-file.md` → "Provenance"). Keep
   every answer **traceable on request**; you needn't cite trivia or every routine reply.
4. **Say what you don't know.** If memory only partly answers it, say so plainly rather than
   filling the gap with a guess (`brain/role/principles.md` — a wrong memory is worse than a missing
   one).

## After
- **Compound it.** If the answer is substantial and reusable (a synthesis worth keeping, not a
  one-off), **offer to file it back** into memory — usually a `context/` memory file or an update to the
  relevant `projects/`/`people/` file — with its sources, so future queries start from it. Capture
  facts, not throwaway prose (`brain/role/principles.md` → do the least that solves it).
- **Flag gaps.** If the question revealed something worth knowing but not recorded, name the gap and
  suggest what would fill it (a note to capture, a question to answer).
