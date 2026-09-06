---
name: playbook-memory-lint
description: Audit the principal's memory/ for staleness, contradictions, orphans, broken links, uncited facts, and undistilled log entries.
type: playbook
---

# Playbook: Memory Lint

Keeps the principal's `memory/` accurate as it grows. Runs on **`/lint`**, when the principal asks
you to "clean up / check my memory", or as an opt-in periodic routine
(`brain/integrations/routines.md`). This audits **memory only** — never `brain/` (that's what the
test suite is for).

Read-only by default: **you diagnose and propose; you don't rewrite memory until the principal
says so.** This mirrors `brain/role/principles.md` — edit memory surgically, and mention stale or
duplicate memory rather than silently deleting it.

## Scope
Lint all of `memory/` by default. If `$ARGUMENTS` (or the request) names a subpath
(`memory/people/`, a single file, a project), scope to that. Always start from `memory/index.md`,
then read the memory files it lists.

## What to check
1. **Stale claims** — dates/deadlines now in the past, or a status a newer entry has superseded
   (e.g. a project still "on track" while a later `log/` note says "at risk"; a commitment past its
   `due` still `open`). Reason against today (see `brain/schemas/memory-file.md` on absolute dates).
   Also flag an **action-gating condition** past its date or with its condition already met (see
   `brain/schemas/capture-rules.md` → "Facts that gate action") — propose **resolving** the line
   (confirm the gate lifted, or extend it), not just flagging it as stale. Also flag a **standing-rule
   directive** whose `expires:` date is now past (see `brain/schemas/memory-file.md` → "Preference
   directives") — propose flipping it to `superseded` (principal's OK) or renewing the date.
2. **Contradictions** — two files (or two rows) that assert conflicting facts. Follow
   `brain/schemas/capture-rules.md` → "Contradictions": name both claims, both dates/sources, and
   which is newer. Never silently pick one.
3. **Reachability (high severity)** — from `memory/index.md`, follow links **transitively** (through
   sub-indexes — `overrides/index.md`, `team/index.md`, a specialist's own `memory/index.md`, its
   charter, its `ledger.md`, etc.) and **report every `memory/**/*.md` file not reached** this way.
   The exemptions are `memory/_quarantined/` files (plus uncited archived originals under
   `memory/_processed/`) — these are deliberately out-of-graph, so **do not** report them as
   unreachable or offer to link them in. **Legacy exception:** a specialist subtree may still contain
   `AGENTS.md`/`CLAUDE.md` from a release before 0.22.0. Those are dead boot files, not memory —
   **propose deleting them; never offer to link them into the index** (`brain/schemas/team-member.md`
   → "Why a specialist has no boot files of its own"). This **subsumes check #4 (orphan files)** below — an
   unindexed file is just one way to be unreachable; a file that's *listed* somewhere but reachable
   through no unbroken link chain (a dead sub-index link, an orphaned specialist directory) is equally a
   finding here. `/lint` is the standing enforcement of the memory-reachability invariant
   (`brain/schemas/memory-file.md` → "Reachability invariant"). For each unreachable file outside the
   exemptions, offer to link it in — the root index, a sub-index, or a parent memory file.
4. **Orphan files** — a file **not listed in `memory/index.md`**, or an indexed file with **no
   inbound links** from any other memory file. Also flag the reverse: an index entry pointing at a
   file that doesn't exist. (The narrower, most common case of #3.)
5. **Broken links** — a markdown link to a relative path with no file at the other end (a dangling
   `[text](../path.md)`).
6. **Uncited durable facts** — a material fact with no provenance where one would help (see
   `brain/schemas/memory-file.md` → "Provenance"). Don't demand a source for everything — flag only
   where not knowing the origin would undermine trust (a surprising claim, a number, a sensitivity).
7. **Duplicates** — two files covering the same subject that should be merged (dedup, per capture
   rules).
8. **Missing cross-references** — two clearly related memory files (a person who owns a project; a decision
   that drives a commitment) with no link between them. (Deep connection-finding is `explore.md`;
   here, only the obvious missing link.)
9. **Log window / index rollup** — the root `memory/index.md` lists log entries **outside the recency
   window** (older than 30 days, beyond the 5-most-recent floor) while `memory/log/index.md` is
   missing or doesn't carry them. The root index is a router, and an unbounded dated list crowds out
   the hooks that do the routing. Propose rolling the out-of-window lines into `memory/log/index.md`
   (every entry, newest first), leaving the root with the window plus one link to it. Flag the reverse
   too: a `log/index.md` that exists but is missing entries, or isn't linked from the root index (that
   second case is also a reachability finding, #3). **`log/` only** — never propose a sub-index for
   `people/`, `projects/`, `context/`, or `preferences/`, whose per-file hooks *are* the routing
   signal and belong in the root index however long the list gets (see
   `brain/schemas/memory-file.md` → "Log rollup").

9b. **Desk hygiene** (`memory/desk/` — see `brain/schemas/memory-file.md` → "The desk"):
    (a) a desk file not linked from `memory/desk/index.md`, or a desk-index entry pointing
    nowhere; (b) a top-level desk folder missing its `readme.md`; (c) a folder `readme.md` whose
    `updated:` is older than the newest file beneath it (the bump rule was missed — propose
    bumping, and ask what state the work is in); (d) **abandoned work** — untouched for 30+ days
    by its `updated:` — propose **parking** it (move to `memory/desk/_parked/`, move its index
    line into `_parked/index.md` with a one-line why, same turn) or deleting it; (e) `_parked/`
    integrity — a parked file missing from `_parked/index.md`, a parked-index entry pointing
    nowhere, or a parked item the principal referenced recently (offer to un-park it).

**Team integrity (10–19) — only when a roster is linked** (`memory/index.md` → `memory/team/index.md`,
`brain/schemas/team-member.md`). **Normal Chief of Staff operation is link-only** — the filesystem checks below
(especially #19) are exactly the sanctioned exception, alongside the versioned migration
(`brain/playbooks/team.md` → "Migrate a pre-roster team"); never promote a filesystem finding into
the active graph without the principal's OK.
10. **Roster unlinked or missing** — `memory/index.md` claims a team (links `memory/team/index.md`)
    but the roster file doesn't exist, or the roster exists with no link from `memory/index.md`
    (see `brain/schemas/team-member.md` → "The roster").
11. **Dead roster link** — an `## Active` (or `## Inactive`) entry in `memory/team/index.md` whose
    charter link doesn't resolve.
12. **Unlinked active charter** — a charter with `status: active` that the roster's `## Active`
    doesn't link — found only via the sanctioned filesystem check in #19, never assumed reachable
    otherwise.
13. **Status/roster mismatch** — a charter's `status:` disagrees with the roster section it's linked
    under (e.g. linked under `## Active` but `status: inactive`).
14. **Missing specialist-memory link** — a charter with no link to `memory/index.md` (normally on
    its `**Deep context:**` line), leaving its own notes unreachable. The target is what matters,
    not the label text — a charter written before the rename still says `[Member
    memory](memory/index.md)` and satisfies this.
15. **Unreachable specialist notes** — a note under a specialist's `memory/notes/` that its own `index.md`
    doesn't link.
16. **Real identity in a specialist file** — a confidential project's **real name** (rather than its code
    name) appears in a charter, a specialist's memory, or a deliverable. Specialists work in code names; flag
    as a leak (`brain/schemas/team-member.md` → "Access control").
17. **Registry reachable from any shared memory file** — `memory/confidential/registry.md` linked from **any**
    memory file under `memory/` other than the single root-index link — a project, person, preference, or
    context memory file, a roster, a charter, any specialist memory file. Since every specialist reads the whole shared brain,
    each such link opens a memory file → registry hop straight to the real identities; the registry must be
    reachable by no specialist path (`brain/schemas/confidentiality.md` → "Reachability"). Flag as
    severity-one. (This is the broad net; #18 is the narrower team-subgraph case within it — a registry
    link from the roster/charter/specialist subgraph trips both, so report it once as the team leak.)
18. **Registry linked from the team subgraph** — `memory/confidential/registry.md` linked from any roster,
    charter, or specialist memory file (the team subgraph specifically). This must **never** happen — flag as
    severity-one.
19. **Orphan specialist directory** — a `memory/team/<slug>/` on disk but linked from **neither**
    `## Active` nor `## Inactive` in the roster. Report this **only** inside an explicitly requested
    filesystem audit (or the versioned migration) — never surface it as a routable specialist, and never
    auto-link it without the principal's OK.

**Always on (20–21).**
20. **Contradictory active directives** — two `active`-status preference bullets (in one file, or
    across `memory/preferences/`) that assert conflicting instructions. Flag both and propose
    resolving per `brain/schemas/capture-rules.md` → "Preference changes — supersede in place"
    (rewrite the current one, flip the other to `superseded`, keep both — never delete). Also note
    the reverse defects: a `superseded` entry that's been **deleted** instead of retained (breaks
    the trail — propose restoring it if recoverable), and an **un-annotated legacy bullet** (no
    `observed:`/`status:` comment), which is **low-severity** — propose annotating it as `active`
    (legacy bullets read as implicitly active) the next time the file is touched, not an urgent fix.
21. **Oversized always-load file / multi-line index hook** — a file under `## Always load` (or
    `profile/`, or a tracker) that's grown well past the ~100-line soft target, or a
    `memory/index.md` entry that's spilled past one line. Propose the **specific demotion** — which
    section moves to which linked on-demand file (per `brain/schemas/memory-file.md` → "Size
    discipline (always-load files)") — never auto-trim or silently shorten the file.
22. **Stale capability inventory** — `memory/integrations.md` disagrees with what's actually
    available: a connector listed as live that discovery no longer finds, one that's live but
    unlisted, or a browser/terminal line that no longer holds. **Low severity** — the inventory is a
    cached snapshot, so propose reconciling the row and note when it was last verified; never
    conclude an integration is gone from this file alone (`brain/integrations/connectors.md` —
    absence is inconclusive).
23. **Roster pointer names a specialization** — the `memory/team/index.md` hook under
    `## Always load` in `memory/index.md` mentions any specialist's `specialization` (or the domain of
    one) instead of the fixed generic line. `memory/index.md` is always-loaded, so it carries that
    detail into every session and goes stale as soon as the roster changes. **Low severity** —
    propose restoring the verbatim pointer (`brain/playbooks/team.md` → "Onboard a specialist", build
    step 4); the roster's own entries are where a specialist's domain belongs.
24. **Delegated work missing from the tracker** — an open delegation record under
    `memory/team/<slug>/delegations/` (`status:` `assigned`, `in-progress`, or `delivered`) with no
    matching row in `memory/commitments.md`. The session-start digest reads the tracker, **not** the
    specialists' ledgers (`CHIEFOFSTAFF.md` boot step 4), so an unmirrored delegation is invisible at
    session start — the principal is never told it's outstanding. Propose the missing row (owner
    `<slug>`, the record's own due date, a link to the record — `brain/playbooks/delegate.md` step 6)
    and **never invent a due date the record doesn't carry**; if it has none, propose the row without
    one and say so. Also flag the reverse: a tracker row whose linked delegation record is
    `integrated` or `rejected` but whose `status` is still `open`.
25. **Suggestion an active specialist already covers** — `memory/team-suggestions.md` → `## Pending`
    names a domain a roster `## Active` specialist's `specialization:` already covers. Drop the entry: it
    was answered by another route, and an offer for a specialist the principal already has is noise at
    every session start (`CHIEFOFSTAFF.md` boot step 8).

## Distill (log → durable memory)
A `/lint` pass also looks for durable facts still sitting in `memory/log/` that were never routed
into people/projects/preferences/context/trackers — the "dreaming" sweep that keeps the log from
becoming a second, un-indexed memory.

- **Find the starting point.** Read `memory/ledger.md` for the last `lint` line; distill everything
  in `memory/log/` **since** that date. If there's no prior `lint` line, cover the whole log, or the
  last ~90 days if the log is long.
- **Re-scan those entries** for durable facts that never made it into a proper memory file — a
  decision only mentioned in passing, a person or project detail buried in a dated note, a
  preference stated once and never filed.
- **Propose promotions, don't apply them.** For each candidate, name the fact, its **origin class**
  (principal-stated, derived, or generated — `brain/schemas/capture-rules.md` → "Origin classes"),
  where it currently lives (the `log/` entry), and where it should be promoted to — with
  **provenance back to the log entry**, per `brain/schemas/memory-file.md` → "Provenance". Call out
  a derived or generated promotion explicitly, so the principal's OK is an informed one. This check
  is **read-only**, same as the rest of lint; promotions apply only on the principal's OK, via the
  existing `## After`.

## Produce
Deliver the report in this turn — a grouped findings list, **bottom line first**
(`brain/role/voice.md`):
- Open with a one-line health read ("12 files; 3 issues — 1 contradiction, 2 stale").
- Group by check; for each finding give the **file(s)** (and row/line), what's wrong, and a
  **proposed fix** (one line).
- Order by severity: contradictions and stale-and-acted-on facts first; cosmetic (missing link,
  uncited) last.
- Report **Distill** candidates as their own group — each a fact, its `log/` source, and the
  proposed promotion target — since a promotion is a different shape of finding than a fix.
- If memory is clean, say so plainly — don't invent findings.

## After
- **Desk deletions require an explicit, informed OK.** Before deleting anything under
  `memory/desk/` — one file, a batch, or an entire folder — show the principal the **complete
  list** of every file and folder that would be removed, and delete only on their explicit
  approval of that list. A batch or whole-folder delete is fine once approved; deleting desk work
  the principal hasn't seen enumerated never is — desk files are their unfinished work, and lint
  can't know what a draft is worth. A general "apply all the fixes" from earlier does **not**
  cover a deletion list they haven't seen. (Parking is reversible and applies on an ordinary OK.)
- **Offer to apply** the fixes — as a batch or one by one. Apply only on the principal's OK, edit
  **surgically**, update `memory/index.md` for any file/link you change, and confirm what you
  changed (`brain/role/principles.md` → "Be transparent about memory").
- For a confirmed contradiction, resolve per capture rules (default to the newer fact, keep the
  principal informed); for a genuine duplicate, merge then dedup the index.
- **Distill promotions** apply the same way, on OK — write the fact into its proposed target file
  with provenance back to the `log/` entry and today's `updated:`, then update `memory/index.md`
  (`brain/schemas/capture-rules.md` → Procedure).
- If lint keeps surfacing the same class of issue, **offer to schedule it** as a periodic (e.g.
  monthly) routine via `/routines`.
- **Ledger.** Append one `lint` line to `memory/ledger.md` — the run and its headline findings
  (`brain/schemas/capture-rules.md` → "Action ledger").
- **Clock.** Set `last_lint: <today's date>` in `memory/meta.md`. This is what resets the
  session-start maintenance offer (`CHIEFOFSTAFF.md` boot step 8); without it the offer re-fires next
  session as though the run never happened.
