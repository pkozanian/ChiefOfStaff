---
name: memory-file-schema
description: The frontmatter schema and body conventions every memory file must follow.
type: role
---

# Memory File Schema

Every file in `brain/` and `memory/` (except `VERSION`, indexes, and this repo's
top-level docs) is a **memory file**: YAML frontmatter followed by a markdown body.

## Memory layout (created on demand)

The `memory/` tree is **not pre-shipped** — a fresh install has only `memory/.keep`.
Onboarding and passive capture create these folders and files as needed (the Write tool makes
parent dirs automatically):

| Path | Holds |
|------|-------|
| `memory/meta.md` | onboarding status + `onboarded_against` version (the release your memory is aligned with — set at onboarding, then **advanced by the boot migration pass** after an upgrade, `brain/integrations/updates.md` → "Applying memory migrations") + `last_onboarded` (the onboarding date — anchors the session-start maintenance-offer clock; see `CHIEFOFSTAFF.md` boot step 8) + `last_lint` and `last_explore` (the dates those runs last completed — the same clock's other two anchors, kept here so boot never scans the append-only `memory/ledger.md` for them; written by `brain/playbooks/memory-lint.md` and `brain/playbooks/explore.md` when a run finishes) + `host: claude-code \| codex \| other` (which agentic host this install runs on) + `os: macos \| windows \| linux` and `browser: chrome \| edge \| brave \| arc \| safari \| firefox \| other` (the machine's OS and default browser — **inferred, not asked**; they pick which browser extension to recommend) — all three recorded per `brain/integrations/hosts.md` → "Detect + record the host" + the onboarding **mode**: `context: work \| personal` and (work) `role_type: ic \| manager` + `bootstrap_scope: all \| work-only \| named` (records the consented onboarding-scan scope; read by onboarding steps 3/6 and on resume — `all` = every connected account; `work-only` = work mode excluding personal; `named` = only the specific accounts the principal chose). While onboarding is `in_progress`, also `current_step: <1–6>` — the step half of the resume anchor read by `CHIEFOFSTAFF.md` boot step 2; the row half is `memory/onboarding-checklist.md` |
| `memory/onboarding-checklist.md` | every onboarding requirement (the rows of `brain/onboarding/checklist.md`) with its status — `open` · `done` · `declined` · `deferred` · `blocked` · `n/a` (reason in the Note column) — created at the start of onboarding, resolved row by row, the resume anchor (`CHIEFOFSTAFF.md` boot step 2 resumes at the first `open` row) and, after completion, the record of what was deferred. Load on demand |
| `memory/index.md` | router for memory (Always load / Load on demand) |
| `memory/profile/` | the principal: identity (incl. the name they **go by**), role, org, mandate, and the onboarding mode (`Context: work \| personal`, `Role type: ic \| manager`) — Always-loaded, so it steers ongoing behavior |
| `memory/people/` | one file per person (relationship, cadence, prefs) |
| `memory/projects/` | one file per initiative (goal, owner, status, dates) |
| `memory/preferences/` | working & communication preferences, standing rules |
| `memory/context/` | company/domain/system knowledge, glossary |
| `memory/log/` | dated session notes, decisions, captured events (one file per event). Once entries age out of the root index's recency window, `log/index.md` lists them all — see "Log rollup" below |
| `memory/integrations.md` | **capability inventory** — which connectors/plugins, terminal/shell, browser control, and session-title control this install can use (+ status and when each was last verified). **Always-loaded**, refreshed by boot step 7 and by mid-task discovery; a cached snapshot to plan with, never proof a tool exists (verify per `brain/integrations/connectors.md`) |
| `memory/ledger.md` | append-only action ledger — what Chief of Staff *did* (ingest/lint/explore/…); see `brain/schemas/capture-rules.md` → "Action ledger". Distinct from the `log/` folder |
| `memory/commitments.md` | single tracker of open commitments/follow-ups (+ `commitments/done.md` archive) |
| `memory/okrs.md` | single tracker of objectives + key results (progress/confidence); see `brain/playbooks/okrs.md` |
| `memory/decisions.md` | single decision log — one row per decision, with RAPID roles; see `brain/playbooks/decisions.md` |
| `memory/overrides/` | overlay tree (mirrors `brain/`) + its `index.md` |
| `memory/desk/` | **working files** — drafts, scratch, work products the principal will reuse or iterate on; the only home for non-memory writes, indexed by its own `desk/index.md` — see "The desk" below |
| `memory/desk/_parked/` | shelved desk work, still in-graph via its own `index.md` (underscore NAME only — not the reachability exemption) — see "The desk" |
| `memory/confidential/` | **guarded** code-name↔real-identity registry (+ any sealed files); never surfaced |
| `memory/team/` | optional **virtual team** — `index.md` is the **authoritative roster** (`type: log`, the source of truth for membership); specialists are found by **following its links**, never by scanning the folder — one `<slug>/` per specialist (charter + own memory + delegation records); see `brain/schemas/team-member.md` |
| `memory/team-suggestions.md` | optional — specialists Chief of Staff has **suggested** and the principal hasn't answered: `## Pending` (at most one) + `## Declined` (permanent tombstones). Deliberately outside `memory/team/`, because a suggestion is **not** membership; always-loaded once it exists, so the session-start offer sees it without a second read — see `brain/schemas/team-member.md` |
| `memory/_processed/` | archived originals of documents auto-intaked from the chat (for citeability); created only when the host can write files |
| `memory/_quarantined/` | files flagged by prompt-injection screening during auto-intake |

Create a folder simply by writing the first file into it, then add its entry to
`memory/index.md`.

## The desk (memory/desk/)

**The write boundary: everything Chief of Staff writes lives under `memory/`.** Durable facts go
to their schema-defined homes above; **everything else — drafts, scratch, analyses, any file that
isn't durable memory — goes under `memory/desk/`.** Never the folder root, never `brain/`, never
a new top-level folder: an update only preserves `memory/`, so a file anywhere else can be
destroyed by the next release. If the principal asks for a file outside `memory/`, say that one
sentence and save it to the desk instead — never silently obey, never silently relocate.

- **What belongs there:** files the principal will reuse or iterate on (a memo draft, an
  analysis, an export). A chat-sized answer stays in chat — the desk is not a transcript.
- **`memory/desk/index.md`** (`type: log`) lists every work-in-progress, linked **in the same
  turn** the file is written; the root `memory/index.md` links the desk index under Load on
  demand ("load when resuming work in progress"). Created on first use, like any memory folder.
- **Folders carry a readme.** A top-level folder under `desk/` gets a `readme.md` at creation —
  standard frontmatter (`name`, `description`, `type: desk`, `updated:`) plus one line on why the
  folder exists. **Touching any file beneath the folder bumps that readme's `updated:` in the
  same turn** — that date is the folder's freshness signal, and `/lint` reads it.
- **`memory/desk/_parked/`** is where shelved work goes — a move, not a delete. It keeps its own
  `index.md` (`type: log`, one line per item: what it is, why parked, when); parking a file means
  moving it and moving its desk-index line into `_parked/index.md`, same turn. A folder parks
  whole, readme included. Parked work stays reachable: root index → desk index → parked index.
- Loose files take dated slugs (`2026-08-13-board-memo.md`). Saving to the desk gets the same
  one-line receipt as any capture (`brain/role/voice.md`). Confidential content lives under its
  code name here like anywhere in memory. Desk writes are memory writes, so a **stale session
  holds them** (deliver the content in chat; file it in a fresh session).

**Reachability invariant.** Every file under `memory/` must be **reachable by link traversal from
`memory/index.md`** — transitively, through sub-indexes (`overrides/index.md`, `team/index.md`, a
specialist's own `memory/index.md`, its charter, its `ledger.md`, etc.). Memory is **one connected
graph**, not a folder scan — indexing a file is necessary but not sufficient; the link chain from
the root must actually resolve. `meta.md` is linked from the root index (Load on demand), and the
confidential registry is linked **once**, from the root index (see
`brain/schemas/confidentiality.md`) — reachable and auditable, even though its contents stay
unquoted. **The only exemption:** `memory/_quarantined/` files (plus uncited archived originals
under `memory/_processed/`), which are deliberately kept out of the reachable graph: a quarantined
file is flagged, untrusted material, not a fact to route to, and an archived original earns its link
only when a live memory file actually cites it as provenance. (`memory/desk/_parked/` shares the
underscore *naming* convention but **not** the exemption — parked work stays reachable through
`desk/_parked/index.md`.) `brain/playbooks/memory-lint.md` runs this as
its **Reachability** check (which subsumes the plain orphan check).

**Log rollup — the one sub-index for scale.** `memory/log/` is the only folder that grows without
bound (one file per event, forever), and its per-entry hooks ("2026-07-08 — Security review")
discriminate far less than a person's or project's. So the root index carries a **recency window**
of log entries rather than all of them:

- **Window:** entries from the **last 30 days**, and never fewer than the **5 most recent** (the
  floor keeps a dormant memory from showing an empty Log section).
- **The moment an entry falls outside the window**, create (or extend) **`memory/log/index.md`** and
  move its line there. That sub-index lists **every** log entry, newest first, one line each, and is
  an ordinary memory file (`type: log`, `updated:` bumped on every touch).
- **The root index keeps the window plus one link** to `log/index.md` — so recent notes stay
  one hop away and the older tail stays reachable.
- Older entries remain findable **two** ways: by date through `log/index.md`, and by topic through
  the provenance backlinks on the `people/`/`projects/` memory files that cite them (see "Provenance").

**Do this for `log/` only — never for `people/`, `projects/`, `context/`, or `preferences/`.** Their
one-line hooks in the root index *are* the routing signal, the thing that lets a session decide **not**
to open a file. Behind a sub-index those hooks are invisible until fetched, which forces either
loading every sub-index speculatively (no saving) or guessing from a folder label (worse recall).
Flat is correct there, however long the list gets. `brain/playbooks/memory-lint.md` check #9 audits
the window after the fact; `brain/schemas/capture-rules.md` → Procedure keeps it on the write side.

**Confidential projects** carry `confidential: true` and `codename: <slug>` in frontmatter, use
the **code name** as their `name:`/identity, and contain **no real name** — the real identity
lives only in `memory/confidential/registry.md`. See `brain/schemas/confidentiality.md`.

## Frontmatter

```yaml
---
name: <kebab-case-slug>          # unique within its tree; the file's identity
description: <one line>          # what this file holds — the index/recall uses it to judge relevance
type: role | playbook | profile | person | project | preference | context | log | commitment | okr | decision | team-member | delegation | desk
updated: <YYYY-MM-DD>            # memory files only: the date this file was last edited
---
```

The file's **tree is implied by its location** — anything under `brain/` is brain, anything under
`memory/` is memory — so there's no `layer` field. **Brain** files carry no version or date: the
release is the single top-level `VERSION` file (+ `CHANGELOG.md`). **Memory** files carry
`updated:` — the date the file was last edited (`YYYY-MM-DD`). **You MUST set `updated:` to today
every time you touch a memory file — on create *and* on every edit, no exceptions** (see
`brain/schemas/capture-rules.md` → Procedure). A stale `updated:` after an edit is a defect the
memory-lint catches.

**Facts vs. hypotheses.** Only write things you're confident are true as facts. An inference the
principal hasn't confirmed is held as a **labeled hypothesis** — not written into a fact-bearing
(especially Always-loaded) file — until confirmed, then promoted. See
`brain/schemas/capture-rules.md` → "High-confidence facts vs. inferred hypotheses".

**`type: person` files** add a `relationship:` tag placing the person in the principal's orbit, so
Chief of Staff can group the stakeholder map (up / across / down / external):

```
relationship: manager | skip-up | peer | direct | skip-down | cross-org | external
```
- `manager` — the principal's boss · `skip-up` — the boss's boss.
- `peer` — same level · `cross-org` — another internal function (no reporting line).
- `direct` — the principal's report · `skip-down` — a direct's report.
- `external` — customers, partners, investors, board.

For a **personal** Chief of Staff (`context: personal`), use natural labels instead — e.g. `family`, `friend`,
`advisor`, `provider`. The tag is free-form (only `type` is validated), so pick what fits the orbit.

## Body conventions

- **One concept per file.** A person, a project, a preference — keep them separate so the index
  can route precisely and so edits stay small.
- Keep it scannable: short sections, bullets over paragraphs.
- **Files in `memory/` link related files** with standard markdown links to relative paths — e.g.
  `[Jane Doe](../people/jane-doe.md)`. Link liberally; a link to a not-yet-created file (pointing
  at its intended path) is a fine to-do marker — create the file when you have content.
- **Link reciprocally (backlink).** When you link A→B, add the inbound link B→A wherever the
  relationship is meaningful — a person ↔ their projects, a project ↔ its owner/stakeholders, a
  decision ↔ the project it affects. When you create a file, wire the inbound links from the related
  memory files that should now point to it. Reciprocal links keep the graph navigable and prevent orphans;
  `brain/playbooks/memory-lint.md` flags one-directional links and orphan files after the fact — this
  is the write-side discipline that avoids them.
- Convert relative dates to absolute (`next Friday` → `2026-07-24`) so they stay meaningful later.
- **Preference bullets are directive-format** — dated and imperative, one active version at a time.
  See `### Preference directives` below.
- **Keep always-loaded files lean** — see `## Size discipline (always-load files)` below.

## Provenance (where a fact came from)

Record the **origin** of a durable fact where knowing it adds trust — a surprising claim, a number,
a sensitivity, or anything captured from a note or meeting. Provenance is a **standard markdown
link** to the source: a `log/` event, a `projects/`/`people/` file, or the retained original in
`memory/_processed/<file>` (kept when a chat-shared doc is auto-intaked and the host can write files,
so it *is* citeable). Two lightweight forms:

- **Inline**, on the specific fact: `- Prefers written pre-reads (source: [1:1 note](../log/2026-07-08-1on1.md)).`
- **A `**Sources:**` line** at the foot of a file that draws on several: `**Sources:** [ops huddle](../log/2026-07-22-ops-huddle.md), [Q3 planning doc](../_processed/2026-07-15-q3-planning.md).`

This is **not** a citation on every line — most memory is fine without it. Cite where provenance
matters; the `source` column on `commitments.md`/`decisions.md` is the same idea, already required
there. `brain/playbooks/memory-lint.md` flags **uncited durable facts** that ought to carry a source.

Provenance also conveys the fact's **origin class** — principal-stated, derived, or generated.
Absence of a source defaults to principal-stated; a derived or generated fact's source line is what
carries that label. See `brain/schemas/capture-rules.md` → "Origin classes" for the full rule set.

A `type: team-member` charter (`memory/team/<slug>/charter.md`) may also carry an OPTIONAL
`persona:` frontmatter block (see `brain/schemas/team-member.md` → "Persona"), and a required
`## Method`. Its seeded starter notes (`memory/team/<slug>/memory/notes/`) are **evidence only** and
carry a `(source: …)` naming a URL or the principal — never a model-prior fill
(`brain/schemas/team-member.md` → "Starter memory — evidence only").

## Templates

### Memory — person
```markdown
---
name: person-jane-doe
description: VP Eng, key stakeholder on the platform migration.
type: person
relationship: cross-org
updated: 2026-07-21
---

# Jane Doe — VP Engineering
- **Relationship:** cross-functional partner; owns [Platform Migration](../projects/platform-migration.md).
- **Cadence:** weekly 1:1, Mondays.
- **Notes:** prefers written pre-reads. Cares about reliability metrics (source: [1:1 note](../log/2026-07-08-1on1.md)).
```

### Memory — project
```markdown
---
name: project-platform-migration
description: Migrate core services to the new platform by Q4.
type: project
updated: 2026-07-21
---

# Platform Migration
- **Goal / definition of done:** all core services on new platform by 2026-12-01.
- **Owner:** [Jane Doe](../people/jane-doe.md).
- **Status:** on track.
- **Open items / decisions:** …
```

### Memory — preference
```markdown
---
name: pref-communication
description: How the principal likes to be addressed and communicated with.
type: preference
updated: 2026-07-21
---

# Communication Preferences
<!-- observed: 2026-07-21 | status: active -->
- **Format:** bullets over prose; lead with the bottom line.
<!-- observed: 2026-05-02 | status: superseded -->
- **Format:** a fuller written narrative before the meeting (superseded — now prefers bullets).
```

### Memory — capability inventory
One file, `memory/integrations.md`. Every row carries its **status** and the date it was last
**verified**, and the body opens with the caveat — so its non-authority travels with it into context
instead of living only in the boot instruction.
```markdown
---
name: integrations
description: What this install can use — connectors, terminal, browser control — and how current that is.
type: context
updated: 2026-08-08
---

# Capabilities
Cached snapshot, refreshed at boot — **verify before relying on any row**; never conclude a connector
is missing from this file alone (`brain/integrations/connectors.md`).

| Capability | Kind | Status | Verified |
|---|---|---|---|
| Google Calendar | connector | connected | 2026-08-08 |
| Gmail | connector | needs-auth | 2026-08-08 |
| Terminal / shell | execution | available | 2026-08-08 |
| Browser control (Claude for Chrome) | browser | declined by principal | 2026-08-08 |
```

### Preference directives

Preferences are captured as **dated, imperative directives**, not descriptive notes. Precede each
bullet with `<!-- observed: YYYY-MM-DD | status: active|superseded -->`. When a new statement
contradicts a stored preference, don't delete the old line — rewrite the **active** directive in
place with the new instruction and today's `observed:` date, then flip the prior line's status to
`superseded` and leave it in the file (a trail, not a version log). Never hold two contradictory
`active` directives at once. A legacy bullet with no annotation reads as **implicitly active** —
annotate it the next time you touch the file (see `brain/playbooks/memory-lint.md` check 20). See
`brain/schemas/capture-rules.md` → "Preference changes — supersede in place" for the capture-time
procedure.

For a **standing rule** — one that fires only when a condition arises ("always CC legal on M&A
threads"), rather than a general style preference — the directive comment accepts two optional
fields: `<!-- observed: YYYY-MM-DD | status: active | expires: YYYY-MM-DD | trigger: <when this
applies> -->`. `expires:` (or a review-by date) marks the rule for the lint's expiry check;
`trigger:` names the short context that fires it. Status values stay `active|superseded`; an expired
standing rule is flipped to `superseded` with a note, not deleted. See
`brain/schemas/capture-rules.md` → "Standing rules — trigger and expiry" for the capture-time
guidance.

## Size discipline (always-load files)

`memory/profile/`, the single trackers (`commitments.md`, `okrs.md`, `decisions.md`), and every
file listed under `## Always load` in `memory/index.md` cost context on **every** turn, not just
when a session happens to need them — keep them lean by construction, not by cleanup later.

- **Index hooks stay one line.** A `memory/index.md` entry is a scannable hook, not a summary. If a
  hook needs more than a line to be useful, the file it points to needs restructuring, not the hook.
- **Target ~100 lines (soft) for `profile/` and the trackers.** Not a hard cap — a genuinely dense
  file can run longer — but treat three digits as the point to ask whether the file is still doing
  one job.
- **Outgrowth is demoted, never grown in place.** When an always-load file swells — a project's
  notes crowd out its one-line status, a tracker accretes closed items — move the overflow into a
  linked on-demand file (a project's own `memory/context/<slug>.md` memory file, `commitments/done.md` for
  closed commitments) and leave the live summary plus a link behind. The always-load file keeps
  routing; the detail moves one hop away. `brain/playbooks/memory-lint.md` check 21 flags the
  oversized case and proposes the specific demotion — never an auto-trim.

## When to update vs. create

Before creating a file, check the relevant `index.md` for an existing file on the same subject.
If one exists, **edit it and bump `updated`** rather than creating a duplicate. Delete files
whose content is proven wrong. See `brain/schemas/capture-rules.md`. Edit **surgically** —
touch only what the change requires and don't disturb the rest of the file (see
`brain/role/principles.md` → "Edit memory surgically").

## Override files (memory overrides brain)

The principal can extend or overwrite brain behavior without editing `brain/`, by placing
a file in the overlay tree `memory/overrides/`, which **mirrors `brain/` by path**. The
override's location binds it to its brain target — there is no pointer field.

Override files add two frontmatter fields:

```yaml
---
name: override-role-voice
description: Terser, more informal voice than the shipped default.
type: role            # mirror the type of the file being overridden
mode: replace | extend
base_version: 0.1.0   # the brain VERSION this override was written against
updated: 2026-07-21   # the date this override was last edited (memory convention)
---
```

- **`mode: replace`** — this file stands in for the brain file at the mirrored path; the
  brain version is ignored entirely.
- **`mode: extend`** — the brain file loads first, then this file layers on top as
  amendments; **where they conflict, this override wins.**
- An override at a path with **no brain counterpart** is a **pure addition** (e.g. a brand
  new playbook `memory/overrides/playbooks/board-prep.md`).
- **An addition is intentional; an orphan is not.** A pure addition was written at a path that
  never had a brain counterpart. A `replace`/`extend` override whose brain counterpart was later
  **removed** by an update is an **orphaned override** — the delete-then-copy update mechanics
  silently leave it looking like an addition, which is a defect to resolve, not a feature. See
  `brain/integrations/updates.md` → "Applying memory migrations" (the first-boot pass that reconciles
  these) for the check.
- `base_version` lets boot detect staleness: if it's older than `VERSION` and the targeted
  brain file changed since (per `CHANGELOG.md`), Chief of Staff surfaces the override for review.

### Example — extend the shipped voice

Path: `memory/overrides/role/voice.md` (mirrors `brain/role/voice.md`)
```markdown
---
name: override-role-voice
description: Principal wants ultra-terse, bullet-only replies.
type: role
mode: extend
base_version: 0.1.0
updated: 2026-07-21
---

# Voice override
- Bullets only; no prose paragraphs.
- Max ~5 bullets unless asked for more.
- Drop pleasantries; lead with the answer.
```
Every rule in `brain/role/voice.md` still applies except where the above conflicts.

Whenever you create, change, or remove an override, update `memory/overrides/index.md` in the
same turn.

> **Future option (not built):** section-level patching — targeting a named section within a
> brain file instead of the whole file. Today, overrides are whole-file (`replace`/`extend`).
