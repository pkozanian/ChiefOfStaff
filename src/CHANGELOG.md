# Changelog — Chief of Staff Brain

All notable changes to the **brain** (the shipped Chief of Staff release) are recorded here. This file
documents the `brain/` tree only; a user's `memory/` memory is never affected by a release.

The version lives in `VERSION` and follows [semantic versioning](https://semver.org). While
pre-1.0 (`0.x`), the API/schema is still stabilizing and MINOR bumps may include changes that
would be breaking after 1.0:
- **MAJOR** — breaking change to the memory schema or folder layout; may require migration.
- **MINOR** — new playbooks, onboarding steps, or capabilities.
- **PATCH** — wording, fixes, clarifications.

## Upgrading

Replace the `brain/` tree with the new release and bump `VERSION`. **Leave
`memory/` untouched.** On next boot Chief of Staff compares `memory/meta.md` → `onboarded_against`
with `VERSION` and surfaces any migration notes below.

---

## [Unreleased]

Work landed on `main` since the last release. `main`'s `VERSION` carries a `-dev` suffix (e.g.
`0.36.3-dev`) to mark it as unreleased and ahead of the latest tag; cutting a release renames this
section to `## [x.y.z]`, drops the suffix, and tags `vX.Y.Z` (see `CONTRIBUTING.md` → Releasing).

_Nothing yet._

### Migration notes

**No action required.**

---

## [0.36.2] — Lighter onboarding scan

Onboarding's opt-in history scan now looks back about a month instead of six. It is a smaller ask up
front, it finishes faster, and it still surfaces your standing meetings, frequent collaborators, and
active projects — the things a recent month of calendar and mail already show.

### Changed

- Onboarding's step-2 history bootstrap now scans **~1 month** of connected calendar/mail history
  instead of ~6 months. Step 3's no-bootstrap calendar fallback matches it (was ~1–2 months).

### Migration notes

**No action required.**

---

## [0.36.1] — MIT

Chief of Staff is now MIT-licensed. `LICENSE.md` ships in the folder, so the terms travel with the
files instead of living somewhere you'd have to go looking for. Everything in `memory/` is yours and
isn't covered by it.

### Migration notes

**No action required.**

---

## [0.36.0] — one thing at a time

Setup now asks about **one thing per turn**. Earlier versions bundled unrelated questions — which
tools you use *and* who reports to you, in the same breath — and the whole turn got one short answer.
Each topic now gets its own question, so a short answer costs you that topic and not four others.

Setup also no longer talks itself out of finishing. If several answers in a row were brief, it could
decide you had lost interest and quietly stop asking — leaving your people, projects and preferences
empty without ever saying so. Brief answers are now just brief answers: each question is recorded and
the next one gets asked. The one place setup may stop early is the checkpoint after priorities, and
only once everything before it is genuinely resolved.

### Changed

- Setup asks about one topic per turn. Several questions within a topic are fine — *"who do you report
  to, and is there a skip-level above them?"* is one question. Two unrelated topics in one turn is not.
- The key-people step walks your orbit one circle at a time — manager, then peers, then reports —
  rather than reading all seven out as a single list.
- The organization step asks what the company does and how it's shaped; your tools and the people in
  those teams are their own questions, later.

### Fixed

- Setup no longer abandons itself after a run of short answers, leaving the rest of your world
  uncaptured and saying nothing about it.
- The early-finish checkpoint now only offers once priorities, decisions and the rest of that step are
  actually resolved — not partway through, where it could skip questions it had not yet reached.
- Pausing at that checkpoint no longer marks setup **complete**. It stays in progress, so the next
  session picks up where it stopped instead of treating the unanswered rest as finished.
- The shipped-defaults review is no longer silently set aside when setup wraps up early. It is not an
  optional step, and it is now asked rather than parked.

### Migration notes

**No action required.**

---

## [0.35.0] — nothing in setup gets skipped

Setup asks you a lot in its first fifteen minutes, and it used to read your pace as an answer. Give
short replies, or turn down one offer, and it would quietly stop raising the rest — so you could
finish setup having never heard that it can recommend connectors for the tools you actually use,
pre-fill most of your world from your calendar and mail, record your OKRs, or stand up specialists
to hold the deep context you don't want to carry. You cannot decline something you were never
offered.

Setup now keeps a checklist of everything it owes you, and every row on it ends up marked: done,
declined, deferred, blocked, or not applicable, each with a reason. Optional means you can say no.
It no longer means the offer can be left out. If you would rather move fast, it offers you a shorter
path and names exactly what it would set aside, so what you are trading is in front of you. Before
it calls itself done it audits the list and shows you what is left. And if you walk away halfway
through, it picks up at the first thing still unresolved rather than at the top of the step.

### Added

- **Onboarding keeps a checklist, and nothing on it gets skipped.** Every question and offer in
  onboarding — the connector recommendations, the history pre-fill, OKRs, open decisions, the
  virtual-team proposal, your working preferences, the routines — is now a row in
  `memory/onboarding-checklist.md`, marked done, declined, deferred, blocked, or not applicable, each
  with a reason. Optional means you can say no; it no longer means the offer can be left out. If
  you want to move fast, Chief of Staff offers a shorter path and names exactly what it would set
  aside, and records what you agreed to defer. Before finishing it audits the list and shows you a
  summary with any gaps, and if you step away it resumes at the first unresolved item, not just the
  step.
- **The commands work in more than one assistant.** The nine commands that ship with Chief of Staff
  are now also published as skills in `.agents/skills/`, the shared location Codex, Cursor, Gemini
  CLI, OpenCode and Copilot read. Nothing changes on Claude Code, where they keep working exactly as
  before — the same set is simply readable from both places, and both run the same playbook.

### Fixed

- **Short answers no longer switch off the rest of setup.** Onboarding used to read a brisk pace or a
  declined offer as permission to stop offering things for the session, so a principal who answered
  in one line could finish without ever hearing about plugins, the history pre-fill, OKRs, or a
  virtual team. Those rules are gone.
- **A connector whose tools haven't surfaced yet is no longer treated as disconnected.** Step 2 now
  resolves each connector to a state and records it; an unresolved one is said plainly, with what
  would resolve it, and the history pre-fill is offered as soon as the connector is live.
- **An update now delivers whatever the release ships.** The update recipe used to copy a named list
  of files, so anything added to a later release that wasn't on that list would never reach an
  existing install. It now copies everything the release carries, leaving `memory/` and your local
  settings untouched as always.

### Migration notes

**Required — no write.**

- **`path:agents-dir`** — the shipped commands are now also published as skills at
  `.agents/skills/`, the location Codex, Cursor, Gemini CLI, OpenCode and Copilot read. An install
  updating from a release before this one runs a copy recipe that predates the directory, so it
  arrives one update later. At first boot Chief of Staff runs `brain/playbooks/update.md` →
  **"Create the neutral skills directory (existing installs)"**: it copies the existing
  `.claude/commands/` files into place, changes nothing else, and says nothing. Idempotent, so a
  re-run is a no-op. Your `memory/` is untouched, and `.claude/commands/` keeps working exactly as
  before.
- **`meta:onboarding-checklist`** — onboarding now keeps `memory/onboarding-checklist.md`. **No
  action required** for a completed onboarding: the file is created by the next onboarding or
  re-onboarding, and nothing reads it until then. An onboarding that was left `in_progress` on an
  older release has no checklist; boot resumes from `current_step` as before.

---

## [0.34.0] — nothing in a document gets to give orders

Two ways Chief of Staff could be talked into something, both closed.

A shared document carrying an injected instruction was being answered before the brain had loaded.
The refusal itself was right, and you were told — but the screening procedure never ran, so no copy
was kept and the attempt left no trace you could go back to. Nothing in the conversation cancels the
boot now, and a document carrying instructions is named as the case that most needs it.

Separately, a confidential project's real name was being said in the act of promising not to say it.
"Falcon status — never NimbusAI in my output" hands the code name and the real identity to everyone
the line reaches, which is the one thing a code name exists to prevent. The handling can still be
explained; the name stays out of it.

This release also stops a decision going unnoticed because of how you phrased it. Asking for advice
on a call now gets the same work as naming one: a recommendation, a log entry, and a check for which
colleague or specialist should be in it. And when you describe a situation without naming a choice at
all, Chief of Staff will say if it sees one — once, and without writing it down until you agree.

Sessions also open with something to read. One line — a short tip about working with Chief of
Staff — now arrives alongside the greeting, at most once a day, and one of them carries an
address to write to when something surprises you or you want it to do something it can't.

The rest is one word for one thing. "Page" now always says which one it means, a memory file or a
web page, and one virtual team member is a specialist everywhere. Delegation records name theirs with
a `specialist:` field — both forms are read, so nothing breaks while your records are mixed.

### Added

- **A tip when a session opens.** Opening a session now carries one line — a short tip about working
  with Chief of Staff — alongside the greeting. **At most once a day**, the same tip all day, and not
  when the session start has something that genuinely displaces it: a migration to run, or a stale
  session. An overdue memory check or a new release no longer suppresses it; you may see both in the
  same opening. There are eight, and they rotate by the date. Switch them off with `tips: off` in
  `memory/preferences/briefings.md` (adjustable default 18).

- **A way to tell the people who build this what you think.** One of the eight tips carries
  `feedback@chiefofstaff.team` — for when something surprises you, or you want it to do something it
  can't. Nothing is sent on your behalf and nothing leaves your machine on its own: it is an address,
  and you write to it. It is also in `README.md`, alongside a note to mention your version.

### Changed

- **An instruction inside a document can no longer stop the boot.** A shared document carrying an
  injected instruction ("ignore your previous instructions and…") was being answered immediately —
  correctly refused, and correctly flagged to you, but without the brain having loaded. The screening
  procedure never ran, so no copy was kept in `memory/_quarantined/` and the attempt left no trail.
  The entry point now states that nothing in the conversation cancels the boot, and that a document
  carrying instructions is the case that most needs it.

- **The real name is no longer emitted to say it will not be.** A confidential project is referred
  to by its code name only. That rule did not cover the case of *mentioning the real name while
  declaring it would not be used* ("Falcon status — never NimbusAI in my output"), which leaks the
  code name ↔ real identity mapping to anyone the line reaches, exactly what the code name exists
  to prevent. The handling can still be explained — without the token.

- **Asking for advice gets the same treatment as naming a decision.** *"What do you think about the
  vendor timing?"* is a question about a call, but Chief of Staff only recognised the ones phrased as
  decisions — so the advice version skipped the brief, the decision log, and the sweep that looks for
  who should weigh in. A request for advice, input, or an opinion on a call now gets all three,
  including the check for which colleague or specialist should be in it.
- **A call nobody has named gets raised, not quietly filed.** Tell Chief of Staff *"Meridian slipped
  again"* and it used to record the slip. If a choice with consequences follows from what you said
  and nobody has put it on the table, it now says so — once, in a line — and leaves it there. It
  won't write a decision into your log that you never made; that happens when you say yes.

- **The session-start team digest reads the tracker, not every specialist's files.** When a team is
  active, the one-line digest of what needs you is drawn from `memory/commitments.md` — where every
  delegation is already mirrored with its owner and due date — instead of opening each active
  specialist's `delegations/` and `ledger.md`. Same digest, and boot stays link-based rather than
  walking the folder.

- **"Page" never stands alone.** Chief of Staff's own instructions used one word for two different
  things: a file in your memory, and the content of a web page it had fetched. Those are not the
  same, and the rules for handling fetched content depend on telling them apart. Every mention now
  says which it means — **memory file** or **web page**. Wording inside the brain only; nothing in
  your folder changes.
- **A team member is a "specialist".** One word for one thing, everywhere. "Team member" still reads
  naturally and is still used; what changed is that Chief of Staff no longer calls the same thing a
  "member" in one sentence and something else in the next. The delegation records it writes name the
  specialist with a `specialist:` field, where they used to say `member:`.

### Fixed

- **On Codex, Chief of Staff can check its own connections instead of asking you.** Its instructions
  told it to look at the **Plugins** tab — a screen it cannot actually see — so when it needed to know
  whether Gmail or Microsoft 365 was connected, it had nothing to check and asked you, sometimes about
  a service that was already working. It now looks at the tools it can genuinely call, confirms with a
  harmless read-only status check (never reading your mail to find out), and asks only when it truly
  cannot tell.

### Migration notes

**Required — writes at boot.**

**Required — one exchange at your next fresh session, nothing written without your OK.** Your
`memory/` stays valid either way, and declining costs you nothing.

- **`frontmatter:specialist-key`** — every delegation record names its specialist with
  `specialist:`. Records written before this release use `member:` instead. **Both are read**, so
  nothing is broken while they are mixed; the change is for consistency, and so the older form can
  be retired at 1.0. At first boot after upgrading, Chief of Staff runs `brain/playbooks/team.md` →
  **"Rename the delegation specialist key"**: it walks the records linked from each active
  specialist, changes that one field and nothing else, reports the count in a single exchange, and
  writes only on your approval. Idempotent, so a re-run is a no-op, and if your records are already
  in that shape it checks, finds nothing to do, and says nothing.
- **No action for anything else.** The wording changes above are confined to the brain; your existing
  memory files, charters and rosters are left exactly as they are.
- **Two `brain/playbooks/team.md` sections were renamed.** Earlier notes below name them **"Give
  existing members a memory scope"** and **"Give existing members a method"**; they are now **"Give
  existing specialists a memory scope"** and **"Give existing specialists a method"** — same
  sections, same procedure.

---

## [0.33.0] — what your team knows that you don't

Two halves of the same idea: the people and specialists around you know things you don't, and
Chief of Staff was not reliably reaching for either.

A decision now gets checked for who is missing from it — the colleague who should weigh in, the
specialist whose read would change the call — before the row is final. And a specialist now knows
what to remember: the exact medication and dose, the exact vehicle and its service history, every
post and how it performed. That detail was never Chief of Staff's to hold, and until now nobody
held it.

### Added

- **`decisions:role-coverage`** — when a decision is big enough to matter (complex, high-stakes, more
  than one stakeholder), Chief of Staff now checks who is missing from it before the row is final. It
  sweeps both benches — the people in your memory and your virtual team's active roster — and asks of
  each RAPID role who is affected, who executes, and who knows something you don't. A small one-person
  call is untouched: it is still logged lightly, and no roster is read for it.

  Where a specialist fits, Chief of Staff acts: it names the depth it recommends — a full delegation
  for **Recommend**, a quicker consult for **Input** — and you pick. Where a *person* is missing, it
  recommends looping them in and offers to draft the message; it never contacts anyone itself. A
  virtual member can hold **Recommend**, **Input** or **Perform**, but never **Agree** or **Decide** —
  agreement is veto authority and the decision is yours. None of this holds up a decision brief; the
  brief still arrives in the turn you asked for it. `brain/playbooks/decisions.md`,
  `brain/playbooks/decision-brief.md`, `brain/playbooks/delegate.md`.

- **`team:memory-scope`** — a specialist now knows what to remember. Its charter carries a
  `## Memory scope` — the record types it keeps and at what grain — drafted from its specialization
  when you create it and confirmed alongside its method and persona, so creating a member still takes
  one beat rather than another question. A nutrition specialist keeps the meal, the portion, the date
  and how you felt; a vehicle specialist keeps the car, its VIN, its mileage and every service; a
  social specialist keeps every post, when it ran and how it did.

  The rule behind it is one question: *would Chief of Staff keep this?* If not, and the specialist
  can't work without it, it belongs to the specialist — filed at full detail in its own memory, and
  kept there. That same test decides what never travels up: the working record stays with the member,
  and only what your world needs reaches your shared memory. It governs every later task too, not
  just the day you create it. `brain/schemas/team-member.md`, `brain/playbooks/team.md`,
  `brain/playbooks/delegate.md`.

### Migration notes

**Required — writes at boot.**

**Required — one exchange at your next fresh session, nothing written without your OK.** Your
`memory/` stays valid and nothing is rewritten behind you.
- **Members created before this release have no `## Memory scope`.** They keep working, but file at
  whatever grain each session judged. At first boot after upgrading, Chief of Staff runs
  `brain/playbooks/team.md` → **"Give existing members a memory scope"**: it drafts one per member
  from the roster, shows them all together in a single exchange, and writes only on your approval.
  Idempotent, so a re-run is a no-op.
- **No action for anything else.** Your existing member notes are left exactly as they are — the
  scope governs what is filed from now on, and back-filling old notes would invent detail nobody
  recorded. The decision-log change needs nothing: the role sweep fills the same RAPID columns
  `memory/decisions.md` has always had.
- **`charter:memory-scope`** — every member charter carries a `## Memory scope`, the record types that
  member keeps and at what grain. Members created before this release have none;
  `brain/playbooks/team.md` → "Give existing members a memory scope" drafts one per member from the
  roster, shows them together in a single exchange, and writes on approval. Idempotent.

---

## [0.32.0] — the specialist you keep needing

Until now, the only time Chief of Staff ever offered to stand up a specialist was during onboarding —
once, on the day it knew least about your world. Everything after that was on you to ask for.

It now watches for the gap itself. When a domain keeps turning up across your projects and nobody on
your team owns it, an exploration says so and offers to build the specialist. If you don't answer, the
offer isn't lost: it comes back at the start of your next session, folded into the check-in you
already get, until you say yes or no.

### Added

- **`explore:team-suggestions`** — an exploration now notices when a domain recurs across your memory
  with nobody on your team covering it, and suggests a specialist for it. It asks in the run that
  found it and records the ask at the same moment in `memory/team-suggestions.md`; unanswered, it is
  raised again inside the session-start maintenance offer — the same once-per-session offer as
  before, not a new one — until you say yes or no. A yes stands the member
  up; a no is permanent and that domain is never suggested again. `team-offer: off` silences it, the
  same switch that silences the onboarding proposal. `brain/playbooks/explore.md`,
  `brain/playbooks/team.md`, `brain/schemas/team-member.md`, `CHIEFOFSTAFF.md` boot step 8.

### Migration notes

**No action required.** `memory/team-suggestions.md` is created the first time a suggestion is
actually filed; until then its absence is normal and nothing needs backfilling. Nothing about your
existing folder changes.

---

## [0.31.1] — each file, once

0.31.0 told Chief of Staff which files it could fetch together, and starting a session got markedly
faster. But on some setups a large file came back cut short, and the obvious next move was to go and
get it again — so it paid for that file twice, and in a couple of cases three times. The session was
quicker and still heavier than it needed to be.

It now reads each file once. A file too big to arrive whole alongside others is fetched on its own,
and when a group does come back short, only the files that were actually cut are re-read — never the
whole group again.

Nothing about your folder changes.

### Fixed

- **A file fetched together with others is no longer fetched again on its own.** Measured on one
  install, the two largest reference files were each being loaded three times at the start of every
  session. The instructions now say to read each file once, to pull an oversized file separately
  rather than in a group, and to repair a short group file by file instead of repeating it.

### Migration notes

**No action required.** This release changes only what Chief of Staff reads at the start of a
session, not what your folder contains.

---

## [0.31.0] — less to read before it says hello

Chief of Staff used to spend about 78,000 words of reading before its first sentence, and roughly
three quarters of that was work it had already done. It opened every team member's file to work out
what was outstanding, when your commitments list already said. It read a 426-line handbook on how
team members work just because you had one. It re-derived the list of apps it can reach from two
reference documents, having already written that list down. And it read your whole activity log —
a file that only grows — to recover two dates.

None of that changed what it knows or what it says. It knows the same things and greets you the
same way; it just stops fetching the same answers twice on the way there. On the folder this was
measured against, a session now starts having read less than half of what it used to, and the parts
that were getting slower every month have stopped growing.

Two things about your own folder may need adjusting, and Chief of Staff will ask before changing
either. See the migration notes below.

### Changed

- **Chief of Staff stops re-reading, at the start of every session, things it already had.** A
  greeting on a folder with a virtual team was costing about 78,000 words of reading before the
  first sentence, and roughly three quarters of that was work already done. Boot used to open every
  team member's charter and ledger to work out what was outstanding — even though every delegation
  is already recorded, with its owner and due date, in your commitments list. It now reads the list.
  On a folder with fourteen members that is ~28,000 fewer words, and the answer is the same one.
- **The team-member handbook is no longer opened just because you have a team.** A 426-line
  reference on how members are built and run was loaded at the start of every session, for anyone
  whose folder listed one. It is needed when you create, run, delegate to, or review a member —
  never to decide who a question should go to, which the roster alone answers. It now loads when
  it's used.
- **The "want me to tidy your memory?" clock stops re-reading your whole activity log.** Chief of
  Staff offers a memory check-up on a cadence, and worked out whether one was due by reading your
  action log from the top — a file that only ever grows, read in full every session, to recover two
  dates. Those two dates now sit in `memory/meta.md`, alongside the onboarding date the same clock
  already used. On a folder with a year of history that is ~10,000 fewer words per session, and it
  stops growing.
- **The capability list is read, not rebuilt.** Chief of Staff keeps a note of what this install can
  reach — connectors, terminal, browser. Boot was re-deriving that from two reference files it
  already had the answer to. It now reads its own note, and goes back to the references only when
  the note is missing or a task needs something it doesn't mention.
- **Boot says which files it can read together.** The steps were numbered, and were being followed
  one file at a time. They now state which reads don't depend on each other, so a host that can
  fetch several at once does — without the instructions assuming any particular one can.

### Fixed

- **Your commitments list belongs in the always-loaded section, and Chief of Staff now says so.**
  One file assumed it was there; the rule that decides where files go never listed it. On folders
  where it landed in the load-on-demand section, the session-start summary couldn't see it — which
  is exactly why boot was walking the team instead. The placement rule now names it.
- **`/lint` notices delegated work that never reached your commitments list.** Now that the
  session-start summary reads that list rather than each member's ledger, a delegation that was
  never mirrored across would be invisible at session start. Lint flags the gap, and the reverse —
  a row still open whose work was finished.

### Migration notes

**Required — writes at boot.**

- **`meta:lint-explore-dates`** — `memory/meta.md` carries `last_lint:` and `last_explore:` (the
  dates those runs last completed). If they're missing, Chief of Staff recovers them once from the
  last `lint`/`explore` lines in `memory/ledger.md` and writes them in; if a run has never happened,
  the key is left out and the clock keeps anchoring to `last_onboarded` exactly as before. Nothing
  is removed from the ledger, and the dates it recovers are the ones already recorded there — so if
  your folder is already right, it checks, finds nothing to do, and says nothing.
- **`path:commitments-tier`** — `memory/commitments.md` is listed under `## Always load` in
  `memory/index.md`. If it's under `## Load on demand`, Chief of Staff proposes moving the line (the
  file itself doesn't move) and explains why: the session-start summary reads the tracker, and can't
  if it isn't loaded. Skip if there is no `memory/commitments.md`, or if it is already in the
  always-load tier — in which case it checks, finds nothing to do, and says nothing.

---

## [0.30.0] — upgrades that finish what earlier ones started

When you update, Chief of Staff reads what each release since your last one means for your folder,
works through them oldest to newest, and asks you once about whatever is actually left to do. It has
always asked once; what is new is that it now knows what earlier releases already did, so
instructions that replaced each other no longer both get applied.

That mattered more than it sounds. Four changes to how your folder is meant to look shipped without
saying so, which meant nothing ever applied them — team-member charters kept a permissions field
that stopped meaning anything, kept their reading list in the old place, and missed the personality
layer added for them; and a couple of stale files lingered. This release states all four, so they
reach you even though the releases that introduced them are long behind you. If your folder is
already in good shape, it checks, finds nothing to do, and says nothing.

### Migration notes

**Required — writes at boot.** Four migrations that shipped silently or understated themselves —
0.15.0's removal of per-member access control, 0.18.0's persona rework, the host rename 0.13.0
corrected, and the `memory/.gitignore` 0.7.0 retired — never ran, because no release carried a note
the migration pass could read. This release restates them so they reach installs that have already
upgraded past those versions. If your folder is already in the shape described, Chief of Staff checks,
finds nothing to do, and says nothing.

- **`charter:clearance`** — a charter carries no `clearance:` field. Remove it if present.
  **Supersedes 0.15.0.**
- **`charter:reads`** — a charter carries no `reads:` field and no `## Reads` section; its pointers
  live under `## Key context`. Convert a `## Reads` section by renaming the heading and keeping its
  links; fold a bare `reads:` field into the same section. **Supersedes 0.15.0.**
- **`charter:persona`** — every member charter carries a `persona:` block, at default depth
  `character`. A member with no `persona:` gets one synthesized from its `specialization`; a member
  already at `depth: working-style` keeps that unless the principal asks otherwise.
  **Supersedes 0.18.0.**
- **`charter:persona.handle`** — a `character`-depth persona carries `handle:`, not `name_flavor:`.
  Rename where present, and check the value against `memory/people/` — pick again on a clash.
  **Supersedes 0.18.0.**
- **`meta:host`** — `memory/meta.md` names the host under its current identifier:
  `host: claude-code | codex | other`. A tree recording `host: chatgpt-work` is rewritten to
  `host: codex` — the same host under its real name, not a different one. A tree with no `host:` line
  gets one the next time the host is detected. **Supersedes 0.13.0.**
- **`path:memory/.gitignore`** — the `memory/` folder carries no `.gitignore` of its own. Where the
  shipped file is still there — its only rules are `*` and `!.gitignore` — it is deleted, because
  that `*` hides the whole memory tree from any repository the folder sits in. One carrying any other
  rule was written by the principal; leave it exactly as it is. **Supersedes 0.7.0.**

Two older corrections are deliberately **not** restated here. 0.10.0's reachability repair would put
a walk of every index and charter in front of every upgrader, and `/lint` already offers that same
repair on demand — run it once if you want it. 0.12.0's retired `memory/inbox/`, and the archives
that moved out of it, were stated in that release's own note when it shipped; what can still be
sitting there is inert archived copies, not live memory.

### Changed
- **Every release entry now states its migration position, and they apply in order.** Each entry in
  this file carries a migration block saying what it means for an existing folder — including the
  releases that shipped silent. When you upgrade across several versions at once, Chief of Staff
  walks them oldest to newest, keeps the most recent instruction for each thing, checks what your
  folder actually holds, and asks you once about whatever is left. You still see a single question,
  not one per version.

### Fixed
- **The memory-file schema now lists every type it asks for.** Its desk section requires a desk
  folder's `readme.md` to carry `type: desk`, but `desk` was missing from the list of allowed types
  further down the same file — so the schema contradicted itself. Nothing behaved differently and
  nothing in your folder changes; the list is simply complete now.

## [0.29.0] — a new chat costs you nothing

Everything your Chief of Staff knows lives in files in your folder, not in the conversation — so
closing a chat and opening a fresh one loses nothing, and a new one starts with a clear head. This
release says so where you'll see it, and stops renaming your conversations, which under one chat per
topic only made them all look alike.

### Added
- **One chat per topic, and Chief of Staff will say so.** Everything it knows lives in files in your
  folder, not in the conversation — so a new chat starts knowing all of it, with none of the clutter.
  That makes a fresh chat per subject the best way to work here, and it's the opposite of the habit
  most chat apps teach, so onboarding now ends by telling you, and the folder's `README.md` says it
  too. Chief of Staff won't interrupt a session to remind you: it's a habit worth having, not
  something to be prompted about.

### Removed
- **Sessions are no longer renamed.** 0.24.0 made Chief of Staff title every conversation
  `ChiefOfStaff v<version>`, and 0.26.0 made it a requirement. Under one chat per topic that backfires:
  every chat in your sidebar ends up with the *same* name, which is worse than whatever your app would
  have called them. Chief of Staff now leaves your conversation titles alone — your app's own naming,
  or your own, tells them apart far better.

### Migration notes

**No action required.** Nothing in this release changes what your `memory/` folder contains. Any
sessions already titled `ChiefOfStaff v<version>` keep those titles; nothing is renamed back. If your
capabilities table carries a `Session title (set_thread_title)` row, it now points at nothing — delete
it or leave it; neither changes anything.

## [0.28.0] — still nothing new for you

The second housekeeping release in a row. Your folder, and everything the Chief of Staff does with
it, are unchanged since 0.26.0 — only the machinery that builds and publishes releases has moved. If
you updated to 0.27.0 and wondered what changed, the answer was nothing, and it is nothing again.

### Migration notes

**No action required.**

No action required. This release changes nothing in `brain/`, and nothing about what a valid
`memory/` looks like.

## [0.27.0] — the same brain, a new home

Releases are now published from a repository of their own. Nothing about how your Chief of Staff
works changes: the folder you have is identical to 0.26.0, file for file. If you update, the only
difference you will see is the version number.

### Migration notes

**No action required.**

No action required. This release changes nothing in `brain/`, and nothing about what a valid
`memory/` looks like.

## [0.26.0] — how much it asks you

Some people want their chief of staff to just make the call. Others want to be asked first. That is
a setting now: tell it to assume, to ask only what changes the outcome, or to interview you properly
before starting anything big. Whatever you pick, the confirmations that protect you never move.

### Added
- **Tell it how much to check with you.** New **Interviewing** setting with three levels:
  `assume` (make a sensible call and say so), `targeted` (the default: ask only what changes the
  outcome), and `thorough` (on big ambiguous asks, interview you first — a short batch of
  questions, then the work). Change it anytime ("what can I change about how you work?"). Team
  members inherit your setting, or get their own per member (`interview:` in a charter, beside
  `autonomy:`), and their questions for you still arrive through Chief of Staff. Confirmations
  that protect you — sending anything, overwriting a conflicting memory, deleting desk work — are
  not a setting and hold at every level.

### Changed
- **Onboarding reads one step at a time.** The setup interview used to live in a single long file
  that was loaded whole. It is now a short spine plus one file per step, so only the step you are
  actually on is in play. The questions, their order, and what gets written are unchanged.
- **Plainer language about what stays where.** Your memory lives in your folder and Chief of Staff
  never copies it anywhere. The wording used to say it "never leaves this computer", which quietly
  implied more than it could promise: what it reads during a conversation reaches your AI app like
  anything you type there. Setup and the confidentiality rules now say so directly. No behavior
  changed, and the guarantee that matters is the same one.
- **Where updates come from, said plainly.** The update rules described the download location using
  an internal folder path that no longer exists. They now just name the address anything you install
  from already uses. Same files, same address, nothing to do.

### Migration notes

**No action required.** Nothing about your folder changes: no memory file is renamed, moved, or
reformatted, and no field is removed. The new `interview:` setting is optional everywhere it
appears. Leave it out of a team member's charter and that member follows your global level, which
is `targeted` unless you say otherwise, and `targeted` is how Chief of Staff already behaved.

To find the new setting, ask **"what can I change about how you work?"** — it is listed with the
other things you can tune.

## [0.25.0] — a desk of its own

Every file your chief of staff makes now has a home. Ask for a draft, an analysis, anything you'll
keep editing, and it lands on the desk — `memory/desk/`, inside the one folder an update never
touches — indexed, receipted, and impossible to lose to a release. It will never scatter files
anywhere else in your folder, even if you ask it to; it will tell you why instead. Sessions also
now name themselves reliably, and the folder's README points to the site's new plain-language
explanation of how all of this works.

### Added
- **The desk.** Ask for a file — a memo draft, an analysis, anything you'll keep editing — and it
  lands in `memory/desk/`, linked from the desk's own index and receipted in the reply. Chief of
  Staff now writes **only** inside `memory/`: never the folder root, never `brain/`, so nothing it
  makes can be destroyed by an update. Working folders carry a `readme.md` that says why they
  exist and when they were last touched; shelved work parks in `memory/desk/_parked/` (still
  findable via its own index); and `/lint` now sweeps the desk — proposing cleanup, and never
  deleting anything before you've seen the exact list and said yes.
### Changed
- The folder's `README.md` now points to [How it works](https://chiefofstaff.team/brain/), the
  site's plain-language explanation of what Chief of Staff does with your information, with every
  brain file rendered beside it — and its setup steps now link the Claude and ChatGPT desktop
  apps directly.
- Session naming is now a boot requirement, not a courtesy. Chief of Staff actively checks whether
  your app can rename the conversation — including tools that only appear on demand, as in the
  ChatGPT desktop app — sets the title to `ChiefOfStaff v<version>`, and confirms the rename took,
  all before it greets you. If your app genuinely has no rename control, nothing changes and nothing
  is said.

### Migration notes

**No action required.** `memory/desk/` (and `memory/desk/_parked/`) are created the first time
they're needed; nothing about an existing `memory/` folder changes shape.

## [0.24.0] — specialists with a pedigree

Your virtual team members get a stronger start and firmer edges. A new member's working method now
begins from a matching profile in an open, MIT-licensed catalog of ~300 specialist definitions —
cited step by step, so you can always see where a method came from — and a member asked for
something no playbook covers now shapes its work around the acceptance criteria you agreed up
front. Chief of Staff itself sharpens too: it still tells you when it disagrees, and once you
decide, it commits — fully, without re-arguing. Sessions also name themselves after the release
they run, so your chat history finally tells you which is which.

### Migration notes

**No action required.** Nothing in this release changes what your `memory/` folder contains — team
charters, notes, and preferences all keep their existing shape.

### Added
- On boot, where the app lets a conversation be renamed, Chief of Staff titles the session
  `ChiefOfStaff v<version>` — so you can spot your chief-of-staff sessions (and which release each
  ran) in the app's chat history. Where the app has no such control, nothing changes.

### Changed
- Chief of Staff now disagrees *and commits*. It has always been willing to tell you an idea is bad —
  but nothing said what happens after you overrule it. Now it's explicit: once you've decided, it
  executes fully, and a recommendation you've turned down more than once is treated as a settled
  preference rather than a debate to reopen — it stops re-proposing it.
- Two sharper judgment tests, where they're used: inbox triage now asks *"would this surprise you in
  a way that damages your position?"* to decide what escalates immediately, and decision briefs now
  check whether a deadline is real — urgency masquerading as importance is how a reversible decision
  steals attention from an irreversible one.
- When a team member is asked for something no shipped playbook covers, its deliverable now takes its
  shape from the delegation's acceptance criteria — the "what does done look like" written when the
  work was handed over — instead of having no stated structure at all.
- New team members start from a stronger draft. When you create one, Chief of Staff now first checks
  the open-source [agency-agents](https://github.com/msitarzewski/agency-agents) catalog (~300
  specialist definitions, MIT-licensed) for a matching profile and uses it as the foundation for the
  member's working method — then refines it with published standards, as before. Steps taken from a
  profile cite it, so you can always see where a method came from. If the catalog is unreachable or
  nothing matches, creation works exactly as it did.

### Fixed
- Member onboarding no longer asks about tool grants. That question fed a charter field that stopped
  existing in 0.22.0 (when members stopped being separate subagents), so the answer had nowhere to
  go.
- When your brain files change mid-conversation, Chief of Staff freezes anything that writes until you
  start a new chat. Delegating to a virtual team member is the one path where that was easy to lose —
  taking on a specialist's persona reads like a fresh start — so the delegation playbook now says
  plainly that the freeze travels with the persona: no delegation record, no member notes, no
  promotion into your memory. It still does the thinking and still gives you the answer.

## [0.23.0] — an upgrade that asks first

Installing a new release has always been able to change things in your folder — a renamed field, a
convention that moved on, a file that no longer means anything. Until now most of that happened
quietly: Chief of Staff worked out what to do and did it, asking only where a particular step
happened to demand it, and you often never learned your memory had been touched at all.

Now the first session after an upgrade works out the span it is bridging — the release your memory was
last aligned with, through to the one you just installed — reads what actually changed across that
whole window, checks which of those changes apply to *your* folder, and if any would alter something
you wrote, **puts the whole set to you in one exchange and waits.** Saying no just means it asks again
next time. If nothing applies, it says nothing and gets on with your morning.

Underneath that, a fix worth naming: whether your memory needed migrating at all was being decided by
comparing version numbers as text, which quietly got the answer backwards for old enough installs. The
folders with the most history to bring forward were the ones being skipped.

### Migration notes

**No action required.** This release changes how the *next* upgrade behaves, not what your memory
holds — nothing in your folder needs to change.

### Changed

- **An upgrade now tells you what it wants to change before it changes it.** The first session after
  an update already ran a migration pass, but most of it was silent: it applied what it could, asked
  only where a step happened to demand it, and you often never learned your folder had been touched.
  Now it works out the span it is bridging — the release your memory was aligned with, through to the
  one you just installed — reads what actually changed across that whole window, checks which of those
  changes apply to *your* folder, and if any of them would alter something you wrote, **puts the whole
  set to you in one exchange and waits.** Declining just means it asks again next session.

  If nothing applies, it says nothing and gets on with the morning. Its own bookkeeping — noting which
  release your memory is now aligned with — never needed your permission and still doesn't.

  It also stops trusting that every release remembered to leave a migration note. It reads the release
  entries themselves, because a change to what memory holds has shipped without a note before: 0.15.0
  removed a field from every team member's charter and said nothing, and the pass walked straight past
  it. `brain/integrations/updates.md`, `CHIEFOFSTAFF.md`.

- **Migrating a pre-roster team asks first.** That one-time migration rewrites every charter and edits
  your memory index, and it was the last one that did so without showing you anything.
  `brain/playbooks/team.md`.

### Fixed

- **An old enough install was silently skipped by the upgrade check.** Whether your memory needed
  migrating was decided by comparing two version numbers as *text*, and by that comparison `0.9.0`
  looks newer than `0.10.0`. The effect was invisible and backwards: the folders with the most history
  to bring forward were the ones the pass quietly declined to run on, and nothing said so. Versions are
  now compared numerically, component by component. `CHIEFOFSTAFF.md`,
  `brain/integrations/updates.md`.

## [0.22.0] — fewer moving parts

There were three ways to run a virtual team member and two of them earned their keep only on paper.
A member could be dispatched as a native subagent, or opened as a folder in your desktop app, or run
by Chief of Staff itself. Testing found the first made no measurable difference to the work, and the
second quietly dropped the rules that keep a specialist safe — the ones that screen a dropped
document, keep a confidential project behind its code name, and stop a pasted password being echoed
back. Both are gone. **You reach a specialist by asking Chief of Staff for it**, which is the one
route where those rules are actually loaded.

The delegation record that tracks a handed-off task also stopped losing pieces of itself: it is now
written whole when the task is opened, rather than growing section by section and dropping whichever
ones never had an obvious moment.

Updating no longer assumes anything about your shell, and the folder placeholder is honest about the
fact that you unzipped a folder rather than cloning a repository.

### Migration notes

**Required — no write.**

**No action required, but one thing stops working.** Nothing is rewritten behind you and no memory is
lost.

- **A leftover `memory/.gitkeep` is harmless.** An update never touches `memory/`, so if your install
  predates this release the old placeholder stays where it is while new installs get `memory/.keep`.
  It does nothing either way. Delete it whenever you like, or don't.

- **Opening a member's folder to talk to it no longer works.** If you had a member folder bookmarked,
  reach that specialist by asking Chief of Staff for it instead — say "let me talk to the audio dev"
  and it answers in the room. Members created on an earlier release still have `AGENTS.md` and
  `CLAUDE.md` sitting in their folder; those are dead files now, and Chief of Staff deletes them the
  next time it touches that member (at `/team-member-review`, or during the 0.21.0 method migration
  if you haven't run that yet). A `/lint` before then will offer to delete them — take the offer; it
  will never suggest linking them into your index.
- **The same pass removes a `.claude/agents/<slug>.md` shim** left by an older release and drops the
  charter's now-meaningless `tools:` field. **This supersedes 0.21.0's note about bringing `tools:` up
  to the current default** — if you have not upgraded past 0.20.0 yet, that step is now a no-op; the
  field is gone, not updated.
- **`charter:tools`** — a charter carries no `tools:` field. Remove it if present; do not update it.
  **Supersedes 0.21.0.**
- **`member:shim`** — no `.claude/agents/<slug>.md` shim exists for a member. Delete any left by an
  earlier release.
- **`member:bootfiles`** — a member's folder holds no `AGENTS.md` or `CLAUDE.md`. Those are dead
  files; delete them where present. Chief of Staff removes them the next time it touches that member,
  and `/lint` offers to before then.
- **`path:memory/.gitkeep`** — the placeholder is `memory/.keep`. A leftover `memory/.gitkeep` is
  inert; delete it or leave it, neither changes anything.

### Changed

- **Updating no longer assumes a particular shell.** The apply step used to be a bash script presented
  as *the* procedure, so on Windows it quietly depended on Git Bash being installed. It is now stated
  as a **contract** — fetch, locate the payload, replace `brain/` and `.claude/commands/` wholesale,
  overwrite the boot files, touch nothing else, clean up — with the shell script kept as one reference
  implementation and the PowerShell equivalents named. The one-prompt install always worked this way;
  the update now matches it. Nothing about what an update *does* changed, only what it assumes about
  the machine. `brain/integrations/updates.md`.

- **The folder placeholder is `memory/.keep`,** renamed from `.gitkeep`. You unzipped a folder, you
  didn't clone a repository, and nothing in it should suggest otherwise.

### Removed

- **A team member is now reached only through Chief of Staff.** Each member folder used to carry a
  generated `AGENTS.md` and `CLAUDE.md` so you could open `memory/team/<slug>/` in your desktop app
  and talk to that member standalone. Both are gone. Ask for the specialist instead — "let me talk to
  the audio dev" — and Chief of Staff speaks as it, in the same conversation, telling you who is
  speaking.

  The reason is that **a member's rails only exist when Chief of Staff is running it.** A member boots
  on its charter, its own memory, and one playbook; it never loads the capture rules, the
  confidentiality rules, or the credential rules. Opened on its own it had no prompt-injection
  screening, no code-name substitution, and nothing stopping it echoing a pasted password — while the
  docs promised a document dropped into it was screened "exactly like any chat-shared doc". That
  promise could not be kept on that path, and removing the path is what makes it true. Delegation is
  unaffected: it never used those files.

- **Team members no longer run as native subagents.** A member had a third projection of its charter
  (`.claude/agents/<slug>.md` on Claude Code) so it could be dispatched into an isolated context. It
  is gone: a member now runs by **persona-swap on every host** — Chief of Staff loads the charter and
  works as the member, then integrates — which is what every host except Claude Code already did, and
  what Claude Code itself did in the session a member was created.

  The isolated path promised parallelism and keeping a member's deep memory out of Chief of Staff's
  context. Testing found **no observable difference**: a dispatched member resolved overrides, applied
  its casebook, and had its notes filed exactly as persona-swap did — even with those instructions
  deleted from its shim. Against an unmeasurable benefit sat a certain cost: a third file to
  regenerate on every charter edit with nothing to detect drift, a per-host branch through the team
  playbooks, a tool-grant field that existed only to feed it, and a shim that wasn't usable until the
  next session. The tradeoff, and the condition for revisiting it, are recorded in
  `brain/schemas/team-member.md` → "Why there is no subagent projection".

  Nothing about how you work with a member changes: you still delegate the same way, still get one
  integrated answer, and can still open `memory/team/<slug>/` to talk to a member directly.

### Fixed

- **A delegation record could lose the sections nobody had a moment to write.** The record's template
  listed seven sections, but the procedure filled them across three separate steps — so whichever
  section had nothing to put in it yet was simply never written. Measured across real runs, only one
  record in three came out whole: the verification, the context handed down, and even the `member:`
  field that ties a record to its member went missing. The record is now written in full when it is
  opened, with anything not known yet marked `(not filled yet)` and filled in later, and the tests
  check the whole shape instead of two of its sections.
  `brain/playbooks/delegate.md`, `brain/schemas/team-member.md`.
- **Two different things were both called "promote".** A member ends its deliverable with a
  `## Promote` list of facts worth keeping; the delegation record had a `## Promoted facts` section
  recording which of them were actually filed. One word, two meanings, one step apart — and the
  record's section was never named in the procedure at all, only in the template, so it was routinely
  written as `## Promote` instead. It is now **`## Integrated facts`**, matching the step that fills
  it, and the procedure names it explicitly. Records written before this keep their old heading; the
  name only matters for new ones, so nothing needs migrating.
  `brain/schemas/team-member.md`, `brain/playbooks/delegate.md`.
- **The virtual-team pointer in your index could name a specialist's domain.** The line in
  `memory/index.md` that points at your team is meant to stay generic, but it was written as an
  example rather than a fixed string — so Chief of Staff sometimes described the member it had just
  built ("your real-time audio specialist") instead. That detail then rides into every session,
  because the index is always loaded, and goes stale the moment the roster changes. The line is now
  copied verbatim, and a memory-lint check flags one that already names a specialization, so an
  existing install repairs itself. `brain/playbooks/team.md`, `brain/playbooks/memory-lint.md`.

## [0.21.0] — specialists that earn their keep

A virtual team member used to be a persona and a one-line specialization pointed at the same memory
Chief of Staff already reads — the same model with a narrower brief, which is why handing work to one
rarely beat just asking. Now each member carries a **method**: the ordered checks it runs and the
standard each is checked against, looked up from how that work is actually reviewed rather than
recalled. It **learns** — every closed delegation leaves a one-line lesson its next task inherits. It
borrows the same craft Chief of Staff uses when it writes something, and it respects the
customizations you've made.

Alongside that: code names are now reserved for genuinely unannounced work instead of anything that
looks sensitive, a pasted password can no longer be echoed back at you, and a question Chief of Staff
asks can no longer swallow a whole turn's worth of things it should have written down.

### Migration notes

**Required — writes at boot.**

**Required — one exchange at your next fresh session, nothing written without your OK.** Your
`memory/` stays valid and nothing is rewritten behind you.
- **Members created before 0.21.0 have no `## Method`.** They keep working, but stay weaker until they
  have one. At first boot after upgrading, Chief of Staff runs
  `brain/playbooks/team.md` → **"Give existing members a method"**: it drafts one per member from the
  roster, shows them all together in a single exchange, and writes only on your approval — then
  regenerates each member's boot files. Idempotent, so a re-run is a no-op.
- **The same step brings each charter's `tools:` up to the current default**, unless you deliberately
  narrowed it. A member is required to write its own subtree, and the old read-only grant left it
  silently unable to.
- **No action for anything else.** The `## Casebook` appears on its own at the next closed delegation,
  and older seeded notes are left exactly as they are — the rule about model priors governs what gets
  written from now on, and rewriting history would destroy the provenance trail.
- **`charter:method`** — every member charter carries a `## Method`. Members created before this
  release have none; `brain/playbooks/team.md` → "Give existing members a method" drafts one per
  member from the roster, shows them together in a single exchange, writes only on approval, then
  regenerates each member's boot files. Idempotent.
- **`charter:tools`** — a charter's `tools:` grant matches the current default, unless the
  principal deliberately narrowed it. Bring it up where it does not.

### Added
- **Team members now get better with use.** Closing a delegation writes a one-line `## Lesson` into
  its record — what the *next* task in that domain should inherit — and mirrors it into a
  `## Casebook` in the member's own memory router, which the member already reads on boot. A lesson
  learned on the third delegation is in front of it on the fortieth, for the cost of one line.
  Rejections are written too; they usually teach more than clean passes. The casebook stays at ten
  lines: a lesson that recurs has become domain knowledge and graduates into a note, and a recurring
  gap becomes a proposed `## Method` amendment at `/team-member-review`. Nothing accumulated before
  this, which is why a member was no better at its fiftieth task than its first.
  `brain/playbooks/delegate.md`, `brain/schemas/team-member.md`, `brain/playbooks/team.md`.
- **Members borrow the craft when they produce.** Before writing a deliverable a member now reads
  `brain/role/principles.md` and the playbook matching what it was asked for — a decision brief, a
  message, a meeting pre-read — so specialist work comes out in the same shape as Chief of Staff's.
  The playbook gives the deliverable its shape; the charter's `## Method` gives it the domain depth.
  It deliberately does **not** load Chief of Staff's voice: the answer is re-voiced on integration
  anyway. `brain/schemas/team-member.md`.
- **Members honour your overrides.** Anything a member borrows from `brain/` is resolved through
  `memory/overrides/` first, exactly as Chief of Staff does it — including a playbook you wrote that
  has no shipped counterpart, which a member may now use. Without this, borrowing a playbook would
  have produced work in the shape you had explicitly overridden.
  `brain/schemas/team-member.md`.
- **A long session no longer drifts onto a summary of its own instructions.** When a conversation runs
  long enough to be compacted, the always-load brain stops being the text Chief of Staff booted with and
  becomes a paraphrase of it — including the rules that govern what gets written into your memory and
  what may be said out loud, where a paraphrase produces malformed files or a disclosure that shouldn't
  have happened, silently. Boot now forks at **step 0**: a genuinely new session boots as before, while a
  re-entry after compaction runs a new **RELOAD** — re-read `VERSION`, both indexes, both `## Always
  load` tiers, the confidential registry, the overlay and a linked roster, then the once-per-day update
  check, without re-greeting you, repeating the once-per-session maintenance offer, or narrating any of
  it. Previously the entry-point router simply said "run the BOOT PROTOCOL from the top", so a compaction
  could re-introduce Chief of Staff mid-conversation and re-offer maintenance it had already offered.
  A reload deliberately does **not** clear stale mode after an update — that still needs a new chat.
  `CHIEFOFSTAFF.md`, `brain/schemas/capture-rules.md`.

### Changed
- **A virtual team member now carries a method, not just a persona.** A member was a persona and a
  one-line specialization pointed at the same memory Chief of Staff already reads — the same model
  with a narrower brief, which is why one rarely beat just asking. Every charter now carries a
  required **`## Method`**: the ordered checks that specialist runs and the standard each is checked
  against. A persona changes how a draft *sounds*; the method is the only part that changes what the
  member *does*. Where the host offers search the method is **looked up rather than recalled** — how
  that role's work is actually reviewed, with the source cited on the steps that came from one, so a
  threshold can be checked instead of taken on faith. Steps written from the specialization alone stay
  uncited; Chief of Staff won't imply a source it doesn't have. Because a method is instruction the
  member executes, fetched content is screened as data and rewritten in Chief of Staff's own words —
  never pasted in as a step. `brain/schemas/team-member.md`, `brain/playbooks/team.md`.
- **A member's starter memory is evidence only.** It was seeded partly from the model's own priors,
  tagged `unverified` — writing to disk what the model already knew and reading it back, which
  teaches it nothing and dresses a guess as a finding. Seeding is now web-cited facts and the
  principal's confirmed specifics; where a prior is genuinely load-bearing it belongs in the
  `## Method`, as instruction the principal reviewed. If neither source yields anything, Chief of
  Staff seeds nothing and says so — an empty evidence folder is honest, a folder of guesses is not.
  `brain/schemas/team-member.md`, `brain/integrations/connectors.md`, `brain/role/defaults.md`.
- **Code names are now for genuinely secret initiatives, not for anything that feels sensitive.**
  The trigger listed "personnel" and "financials" as bare topics, which covers most of what an
  executive says in a day — Chief of Staff would offer to code-name a customer's revenue share
  instead of simply writing it down, and the ceremony made memory harder to read for no gain in
  protection. It now suggests confidentiality only for a **discrete unannounced initiative**: an
  acquisition, a reduction in force or reorg, an unannounced launch, active litigation, or a
  personnel action about a named individual who hasn't been told. Revenue, budgets, headcount,
  pipeline, org structure, and candid reads on people are captured **plainly** — `memory/` never
  leaves the computer, so ordinary discretion already covers them. The test is whether naming it in
  something Chief of Staff writes would cause the harm. Substitution is unchanged: once something
  *is* code-named, the code name is used everywhere, always.
- **Personal mode no longer stands up code-name machinery.** It already never suggested
  confidentiality; now an explicit "keep this confidential" is honored as **discretion** — filed
  plainly, never raised unprompted — rather than creating a code name and a registry. A household
  doesn't need one, and it made the principal's own memory harder to read. Ask for a code name in
  those words and you still get one. `brain/schemas/confidentiality.md`,
  `brain/schemas/capture-rules.md`, `brain/onboarding/flow.md`, `CHIEFOFSTAFF.md`.

### Fixed
- **The reason given for "start a new chat after an update" was mechanically false.** Both
  `CHIEFOFSTAFF.md` and `brain/integrations/updates.md` justified stale mode by saying the swap "doesn't
  hot-reload" — but the new files on disk *can* be re-read at any time, as the new RELOAD now
  demonstrates. Stating a reason that doesn't survive inspection invites working around it, and the
  workaround is unsafe. Both now give the reason that actually holds: the old brain is still in context,
  so a re-read layers a conflicting copy on top of it and refreshes only the always-load tier, leaving
  every on-demand playbook already pulled at the old version — a partial upgrade that looks complete.
  `CHIEFOFSTAFF.md`, `brain/integrations/updates.md`.
- **A team member had no tool to write its own memory.** Its charter required it to file deep
  findings in its own subtree and to accept documents fed to it, but the default tool grant was
  read-only — so on the isolated-subagent path the write simply never happened, silently, and the
  member returned findings it had been told to keep. The default grant now includes write access; the
  boundary keeping a member out of shared memory is the rail in its boot protocol, as it always
  actually was. `brain/schemas/team-member.md`.
- **Two files still said a delegated result comes back unattributed.** Since 0.18.0 an integrated
  delegation names the specialist it came from, but `brain/playbooks/team.md` and `CHIEFOFSTAFF.md`
  carried the old wording, so which rule applied depended on which file was read first. Both now say
  what the delegation playbook says: the voice stays Chief of Staff's, the credit goes to the
  specialist. Also corrected the team offer's onboarding step number in `CHIEFOFSTAFF.md` (step 4,
  not 3).
- **A pasted password could be echoed back into the chat.** If the principal pasted a credential,
  Chief of Staff correctly refused to use it, but could then quote it back while explaining why, or
  while advising them to rotate it. That writes a live secret into the transcript a second time, which
  is the one part they can't undo. It now never echoes a pasted credential, refers to it as "that
  password", and offers the co-browse path so the task still gets done. `brain/integrations/browser.md`.
- **A question could swallow a whole turn's captures.** When something looked sensitive, or when new
  information contradicted a stored fact, Chief of Staff could ask how to proceed and file *nothing*
  while it waited — so a turn's facts were lost to a single unanswered question, and the principal
  believed they'd been saved. A question now holds only the field it's about: everything else is
  captured in the same turn, and an offer never replaces a capture.
  `brain/schemas/capture-rules.md`.
- **Offering a code name could drop the identity entirely.** Suggesting confidentiality for a
  sensitive fact could result in the fact being written down *without* who it was about — the one
  outcome that silently destroys the thing worth remembering. The real identity is now always
  recorded, in `memory/confidential/registry.md` when a code name is in play.
  `brain/schemas/confidentiality.md`.
- **A material conflict could be overwritten silently.** "Default to the newer value" and "confirm
  before overwriting a material conflict" sat as sibling rules, so a moved deadline or reversed
  status could be applied either way depending on which was read first. The material-conflict rule
  now explicitly governs. `brain/schemas/capture-rules.md`.
- **A prompt-injected document might not be kept.** Quarantining a copy of a document that carried an
  injection read as optional, so the evidence could be discarded along with the instruction. It is now
  the default whenever files can be written. `brain/schemas/capture-rules.md`.
- **Introducing yourself and then stopping left no trace.** Onboarding deferred writing
  `memory/profile/principal.md` until its first step's questions were answered, so a principal who
  gave their name and then walked away had nothing recorded — onboarding can be paused or abandoned,
  and a profile that only appears at the end is one they can lose. It's now written in the turn a
  name first appears, and enriched as later answers arrive. `brain/onboarding/flow.md`.
- **A not-yet-onboarded principal got no nudge.** Asking a question before onboarding got a plain
  answer with no mention that onboarding would make it better — the brain described the situation but
  never said to raise it. It now closes with a one-line, plain-words offer. `CHIEFOFSTAFF.md` boot
  step 2.
- **The first thing a ChatGPT user was told to do didn't exist.** The greeting for a not-yet-onboarded
  principal said *"Run `/onboard`"* on every host, but Codex (the ChatGPT desktop app) has no slash
  commands, so a brand-new principal's very first instruction was a dead end. The greeting now says
  **"onboard me"** and never names a slash command, on any host. (`/onboard` still works for anyone who
  types it; the greeting just stops advertising it.) `CHIEFOFSTAFF.md` boot step 2.

## [0.20.0] — install in one paste

Getting started used to mean downloading a ZIP, finding it, unzipping it, hunting for the folder, then
opening it in the right app. Now you make an empty folder, open it, and paste one line: it fetches
itself, unpacks, and starts onboarding. The folder it leaves behind also stops explaining itself in
terms of the repo that built it, and the entry point it boots from is a router again rather than a
page of self-interrogation.

### Migration notes

**No action required.** Your folder keeps its shape and `/update` keeps working: this release publishes
a new archive (`cos.zip`, which unzips flat) *alongside* the existing `ChiefOfStaff.zip`, precisely so
installs from before 0.20.0 — whose updater looks for the old wrapped layout — update exactly as they
did. Doing so hands you a brain that fetches `cos.zip` from then on, so the move happens by itself.

### Added
- **Installing is now one paste.** Make an empty folder, open it in the Claude or ChatGPT desktop app,
  and paste:

  > Run Chief of Staff: download https://chiefofstaff.team/dist/cos.zip and unzip it into this folder.
  > Then read AGENTS.md and start the onboarding.

  It fetches itself, unpacks, and starts onboarding. No downloading, finding, unzipping, or hunting for
  the folder afterwards. The landing page carries the prompt with a copy button, and the manual path
  still works for anyone who prefers it.

### Changed
- **The release publishes `cos.zip`, which unzips flat.** "Unzip it into this folder" is only honest if
  the archive has no wrapper directory, so `cos.zip` contains the files themselves rather than a
  `ChiefOfStaff/` folder. `ChiefOfStaff.zip` is still published, unchanged, because an install's
  `/update` is run by the brain **already on its disk** and older recipes look for that wrapper. Your
  next update moves you onto `cos.zip` automatically; nothing to do.
- **The entry point is a router again, not an interrogation.** `AGENTS.md` used to open every session
  by proving to itself which kind of folder it was in, with a filesystem probe and a five-row decision
  table, because a development checkout and an installed folder were the same shape. They no longer
  are: the product is now built from its own tree, so an installation contains no developer surface to
  route to. `AGENTS.md` drops from 61 lines to 9 and simply hands off to `CHIEFOFSTAFF.md`. The failure
  it was defending against (an executive being offered "developer mode") is now structurally
  impossible rather than argued away.
- **The product stops describing itself as a source repo.** Shipped files referred to things you don't
  have: a developer guide, a test suite, `.gitignore`, "a fresh clone", "a `git pull`". They now
  describe the folder you actually unzipped. Affects `CHIEFOFSTAFF.md`, `README.md`, and six files
  under `brain/`. Behavior is unchanged; only the explanations are now true of an install.
- **The README in your folder is an orientation card, not a second website.** It was a full 111-line
  guide duplicating chiefofstaff.team, including install instructions for software you had already
  installed by the time you could read it, and an app-details table that had drifted out of date. It's
  now ~30 lines: what this folder is, how to start it, what `memory/` and `brain/` are, how updates
  work, and a link to the site for everything else.

### Fixed
- **A source tree could edit its own memory with a brain it no longer had.** The stale-session write
  freeze was skipped entirely for a `-dev` version, on the reasoning that development trees update by
  other means. But a `-dev` version **doesn't move when the files move** — it stays `0.x.y-dev` across
  any number of changes — so the freeze was disabled in exactly the sessions where the brain is most
  likely to shift underfoot, which is the corruption the freeze exists to prevent. `-dev` now means
  "`VERSION` can't answer this", not "you're current": staleness falls back to **direct evidence** (the
  brain demonstrably changed under this session), and when it does, writes are held like any stale
  session. Released builds are unaffected — their versions do move, so the existing comparison already
  worked. `CHIEFOFSTAFF.md` → SESSION FRESHNESS.

## [0.19.0] — a way through when nothing's connected, and a Chief of Staff that knows its own toolkit

When something isn't connected, Chief of Staff stops saying "I can't." It now **offers to do it in the
browser** — but only once a connector, MCP/API, or terminal command is genuinely ruled out, and only
inside hard rails: it **never types your passwords** (you sign in, it picks the task back up) and
**never sends or submits anything without your explicit confirmation**. It also now **knows its own
toolkit**: an always-loaded capability inventory, refreshed at boot, so a session starts knowing which
connectors, terminal, and browser it can actually use instead of rediscovering blind.

### Migration notes

**No action required.**

**No action required** — `memory/` stays valid and nothing is rewritten.
- **`memory/integrations.md` (new, always-loaded)** is created **lazily on the next boot** that has a
  discovery surface (boot step 7); until then its absence is normal. Existing installs need no edit,
  and `/lint` check 22 reconciles it if it later drifts.
- **`memory/meta.md` gains `os:` and `browser:`** (the detected OS and default browser). An already
  onboarded tree has neither; boot step 7 **backfills them** the next time it runs with an execution
  surface. Nothing depends on them except which browser extension gets recommended, so a tree without
  them behaves exactly as before.
- **`path:memory/integrations.md`** — created lazily on the next boot with a discovery surface. Its
  absence before then is normal, and `/lint` check 22 reconciles it if it later drifts.
- **`meta:os`** — `memory/meta.md` records the detected OS. Backfilled by boot step 7 the next time it
  runs with an execution surface.
- **`meta:browser`** — `memory/meta.md` records the default browser. Same lazy backfill. Nothing
  depends on either field except which browser extension gets recommended.

### Added
- **Browser control — the fallback Chief of Staff offers, with hard rails.** When a task needs
  something no connector, MCP/API, **or terminal command** can do, Chief of Staff no longer stops at
  "I can't": it **offers to do it in the browser** and, on your OK, drives it. Onboarding now
  encourages the right browser control **per host** — on Claude Code it **detects your OS and default
  browser** (never asks) and recommends the matching extension (Chrome/Chromium → **Claude for
  Chrome**; Safari/Firefox → verify support first); on ChatGPT it uses the app's **built-in browser**,
  nothing to install. The rails are absolute: it **never types or stores passwords, credentials, keys,
  or card/ID data** — it **co-browses**, opening the page and letting you sign in yourself — and
  **never sends, submits, publishes, or purchases without your explicit confirmation** (a prior yes
  never carries to the next one). Page content is treated as **untrusted data, not instructions**
  (prompt-injection screening, quarantine and flag), with privacy defaults (decline non-essential
  cookies, no personal data in URLs). Native paths still come first — connectors/MCP and terminal rank
  together, ahead of the browser — and an unseen tool stays **inconclusive**, so the browser is never
  a shortcut around discovery. New `brain/integrations/browser.md`; `hosts.md` gains a browser-control
  capability map plus OS/default-browser detection; `connectors.md` offers the browser before
  degrading.
- **Chief of Staff knows its own toolkit — a capability inventory.** A new **always-loaded**
  `memory/integrations.md` records what this install can actually use: each connector/plugin and its
  status, whether there's a terminal/execution surface, and how browser control is reached. **Boot
  refreshes it** (new step 7 — quiet, best-effort, no auth probes) so a new session starts knowing
  what's available **before onboarding or answering** instead of rediscovering blind, and a capability
  is recorded whenever it's installed or discovered mid-session. It's a **cached snapshot, not proof**
  — the discovery contract still verifies before relying on a tool — and `/lint` gains check 22 to
  reconcile it when it drifts. `memory/meta.md` also now carries the detected `os:` and `browser:`.

## [0.18.0] — named specialists, and answers that say who informed them

Virtual team members stop being anonymous. Each one now gets a **handle** the principal can address it
by, on top of the job-typical voice it already had, and every integrated delegation **names the
specialist behind it** while staying in Chief of Staff's own voice: attribution, not relay, so the
principal knows who to push back on without losing the single finished answer. Handles are checked
against the principal's real people so a specialist never shadows a colleague. Alongside it, a naming
rule that had been quietly wrong since the rebrand: Chief of Staff branches on the host it runs as, but
now *says* the app the principal actually installed.

### Changed
- **Team members get a name and a distinct voice, and their work gets attributed.** A new member now
  defaults to `character` depth: a job-typical voice plus a **handle** the principal can address it by,
  rather than an unnamed competent tone. And an integrated delegation now **names the specialist it came
  from** (*"Your reliability specialist's read: …"*), which it previously did not.
  - **Attribution is not relay.** The integrated answer stays in Chief of Staff's own voice, because it
    verified the work and stands behind the claim; naming the source tells the principal who to push back
    on. A member's exact words may be quoted where they matter (a dissent, a caveat), a sentence or two,
    never the whole answer. This narrows a rule that previously forbade attribution on integrated results
    outright, and leaves "one finished answer, never raw output" true.
  - **Handles are checked against `memory/people/`.** A handle duplicating a real colleague's name would
    make the people graph, `commitments.md`'s `owner:` field and every brief ambiguous, so onboarding
    picks again on a clash. A handle names the archetype, never claims to be a person.
- **Chief of Staff now says the app name and branches on the host name.** It runs as *Claude Code* or
  *Codex*, but a principal installed the **Claude** or **ChatGPT** desktop app. Those are two different
  facts and the brain was using one word for both, so the product could tell someone to "open the folder
  in Codex" when they had never seen that word.
  - `brain/integrations/hosts.md` now maps each host to the app it runs inside, and states the rule
    once: **branch on the host name, say the app name to the principal.** UI paths name the app first,
    then the path, since the wording belongs to the app.
  - The onboarding recap and the site copy follow the rule; the per-host forks do not change. The host
    identity still drives Connectors vs Plugins, Routines vs Scheduled, and the boot-file difference, so
    renaming those would have removed the trigger the branching depends on.
  - `README.md` keeps the agent names in one place, the note about which tools read `AGENTS.md`, because
    there the agent is genuinely what is being described.

### Migration notes

**Required — writes at boot.** Existing members keep working; their charters carry the previous
`persona:` shape until migrated.

- **`charter:persona`** — every member charter carries a `persona:` block; it was optional before.
  Its default depth is `character`. A member with no `persona:` gets one synthesized from its
  `specialization`; a member already at `depth: working-style` keeps that unless the principal asks
  otherwise.
- **`charter:persona.handle`** — a `character`-depth persona carries `handle:` (a short name for the
  archetype), not `name_flavor:`. Rename the field where present. Check the value against
  `memory/people/`: a handle that duplicates a real colleague's name is ambiguous in the people
  graph, in `memory/commitments.md`'s `owner:` field, and in every brief that draws on them — pick
  again on a clash.

_Backfilled in 0.30.0 from the release diff; 0.18.0 itself shipped no migration note._

## [0.17.0] — a session that knows when it's out of date, and migrations that apply themselves

Three guardrails that make upgrading safe, plus a router fix. After an in-session update a live session
now **knows it's out of date**: it shows a persistent banner and **freezes memory writes** — so a
session still running the old brain can't corrupt memory the new brain expects in a different shape —
and any needed **memory migration applies itself** at the first fresh session, instead of leaving you a
manual `/lint` to remember. No memory-schema migration is required to adopt 0.17.0 itself.

### Changed
- **New primary logo, adopted across the site, the README and the icon set.** The mark is a plated form
  (navy `#1c3d5a` rounded square, cream figures) showing one orchestrator coordinating a team. It
  replaces the "CoS" monogram everywhere in the icon set.
  - **It ships in two forms, and the split is deliberate.** Plated for every icon, the site header and
    the README; **unplated** (figures in `currentColor`) for the one in-page placement, in the "Build a
    team" section. Rendered in place, the plated form at 120px is the heaviest object on a page that has
    nothing darker than an h2, and its 22% corner is the app-icon idiom, so it reads as an icon that
    wandered onto the page. At icon sizes the opposite holds: the plate is what makes the mark legible,
    since unplated at 16px does not cohere on light chrome and disappears on dark at 1.61:1.
  - **The in-page mark is inlined, not linked.** `currentColor` does not resolve through
    `<img src="*.svg">`, and a `prefers-color-scheme` `<picture>` cannot see the site's `?theme=`
    override. Inlined under `color: var(--accent)` it inherits `#1c3d5a` light and `#8fb4d6` dark.
  - **Optical lift.** The figure group is raised 35 units (4.5%): the ink centroid sat at 59.5% of plate
    height with 2.22x more mass below the midline than above. Measured across a ladder, 35 was the point
    that improved centring (to 55.0%, 1.68) while also *increasing* minimum corner clearance
    (4.08% to 5.84%); lifting further reversed that and crowded the top corners.
  - **`apple-touch-icon.png` had transparent corners** (sampled: all four `RGBA(0,0,0,0)`). iOS does not
    honor alpha on touch icons, so it composited them onto black. The replacement is a flat 180x180
    square with no radius and no alpha. Pre-existing bug, fixed here.
  - Added a dedicated **16x16 favicon** rather than letting browsers downsample 32 to 16, which costs
    real clarity on a mark this dense. The manifest deliberately does **not** declare
    `"purpose": "maskable"`: that requires content inside a 66%-diameter safe circle and this mark is at
    86%, so it would be shredded.
  - `og.png` keeps its existing card; only the 104x104 tile was swapped, verified by pixel diff.
  - Every prior version is kept under `docs/assets/logo-archive/` with provenance headers.

### Migration notes

**No action required.**

**No action required** — `memory/` is untouched and every existing file stays valid. The new
stale-session guardrails and the migration pass are brain behavior; they take effect on your **next
fresh session** after updating (the session that installs 0.17.0 predates them, by design). From 0.17.0
on, `memory/meta.md` `onboarded_against` advances automatically as the first-boot migration pass runs —
previously it was set only at onboarding.

### Added
- **A stale session is frozen from writing memory.** Before creating or updating any `memory/` file,
  Chief of Staff re-reads `VERSION` and writes **only** if it still matches the session's boot
  baseline. If an update has landed (on-disk `VERSION` is newer), it **won't write** — writing with the
  old brain's directives could corrupt memory the new brain expects in a different shape — and instead
  holds the change and tells the principal to start a new chat, where it lands correctly. The freeze
  covers passive capture, preference/fact updates, and the update ledger; reads, drafts, and answering
  are unaffected. This also makes the `/update` session no longer write its own ledger line (the
  first-boot migration pass records the upgrade instead). New **Memory-write freeze** rule under
  `## SESSION FRESHNESS` (`CHIEFOFSTAFF.md`).
- **Memory migrations apply automatically on upgrade.** A needed memory migration is no longer just
  *surfaced* as a to-do — it now **runs as part of upgrading**, at the **first fresh session** after
  the update (the new brain drives its own migration). Boot step 2 was the detection point already
  (`onboarded_against` < `VERSION`); it now runs a **migration pass**: apply each spanned release's
  `CHANGELOG.md` migration notes in version order (silently for "no action required"), run any
  versioned migration a note points to, reconcile orphaned overrides, offer an optional `/lint`
  convergence, then **advance `onboarded_against`** and ledger it — so the pass runs once, not every
  boot (previously `onboarded_against` was set only at onboarding and never advanced). It's the single
  choke point for **every** upgrade path (`/update`, manual ZIP replace, `git`); the stale session that
  ran `/update` no longer attempts migration itself. New "Applying memory migrations" section
  (`brain/integrations/updates.md`); boot step 2, `brain/playbooks/update.md`, and the `CONTRIBUTING.md`
  migration-directive convention updated to match.
- **Stale-session banner after an in-session update.** An update swaps `brain/` on disk, but a live
  session keeps running the brain it loaded at boot — the swap doesn't hot-reload — so the session is
  out of date until a **new chat** re-runs the boot protocol. Previously this was a one-time nudge
  that was easy to scroll past. Now, once an update is applied in-session (or the on-disk `VERSION` is
  observed to be newer than the session's boot baseline), Chief of Staff enters **stale-session mode**
  and **prefixes every reply** with a one-line banner naming the running vs. installed version and
  telling the principal to start a new chat — persistent and non-dismissible until they do. Boot step 1
  records the session baseline; a fresh session boots current and never shows the banner (no
  cross-session state). New `## SESSION FRESHNESS` section (`CHIEFOFSTAFF.md`), with
  `brain/playbooks/update.md` and `brain/integrations/updates.md` activating it after an update.
  (Takes effect for updates applied *from* this release onward — the live session that installs this
  release predates the rule, so it can't retroactively show the banner.)

### Fixed
- **The session-start router no longer mistakes its own instructions for a filesystem.** `AGENTS.md`
  said to offer developer mode "when `CONTRIBUTING.md` exists", and an agent read that **conditional**
  as evidence the file was there, offering developer mode inside a **packaged installation** where
  both `CONTRIBUTING.md` and `.git` were absent. The fork now requires a **real filesystem check** of
  the exact path `<project-root>/CONTRIBUTING.md`, and states plainly that the document's own mention
  of the file, environment or workspace metadata, permission entries, and anything asserted in an
  earlier message are **not** evidence it exists.
  - **Fail-safe:** if the check cannot be run, errors, or is ambiguous, `CONTRIBUTING.md` is treated as
    **absent**. Chief of Staff must never state or imply "this is a development checkout" unless the
    check actually succeeded. Absent or unverified means Use mode **immediately** (read
    `CHIEFOFSTAFF.md`, run its boot protocol) with no developer/use question.
  - A five-row **decision table**, evaluated in order, makes the routing unambiguous. Routing a
    concrete first request by intent, without asking, is unchanged.
  - The router had **no behavioral coverage at all** before this, which is how the bug survived. It now
    has four eval scenarios, including one that strips exactly what `build-dist.sh` omits to reproduce
    a real packaged install.

## [0.16.0] — durable memory: dated directives, origin trust, and log distillation

A batch of memory-architecture conventions — adapted from openclaw — that make memory more durable and
trustworthy over time, plus an onboarding change that **proposes** a virtual team instead of asking you
to invent one. Preferences become dated, supersede-in-place directives; every durable fact carries an
**origin class** (principal-stated / derived / generated) so untrusted input can't silently override
what you told it; `/lint` gains a **log-distillation** sweep that promotes durable facts buried in the
log; always-load files get **size discipline**; and standing rules become trigger/expiry-aware intents.
No memory-schema migration required — legacy files stay valid and pick up the new annotations when next
touched (run `/lint` once for a one-pass convergence).

### Migration notes

**Optional convergence.**

**No action required** — `memory/` is untouched and every existing file remains valid. Legacy
preference bullets (no `observed:`/`status:` comment) read as implicitly `active` and pick up
annotations when next touched; new and changed captures use the directive format automatically.
Unlabeled existing facts read as **principal-stated**, the origin-class default — no re-tagging
needed. Existing standing-rule preferences pick up `trigger:`/`expires:` fields when next touched
(or in one `/lint` pass); expired-rule flagging arrives via the existing check 1. For a one-pass
convergence, run `/lint` once after updating: it offers to annotate legacy preference bullets
(check 20, low severity), flags oversized always-load files (check 21), expired action-gates and
expired standing-rule directives (check 1), and — with no prior `lint` ledger line for it — runs its
first log-distillation sweep over the accumulated log, catching durable facts that predate this
release. `/update` itself checks for overrides orphaned by removed brain files and walks through
re-home / convert-to-addition / retire.

- **`preference:directives`** — preference bullets carry `observed:` / `status:` annotations. Legacy
  bullets without them read as implicitly `active` and are annotated when next touched. For a
  one-pass convergence, run `/lint` once after updating (check 20, low severity). Non-blocking.

### Added
- **Onboarding proposes virtual team members instead of asking you to invent them.** The virtual-team
  offer used to be an open question at step 3 (*"want me to stand up any virtual team members, e.g. a
  software developer?"*), which put the design work on the principal at the exact moment Chief of Staff
  knew more about their world than they'd had to articulate. It is now a **grounded proposal**, and it
  has **moved to step 4**, after priorities and OKRs are captured, so it can cite the principal's actual
  initiatives rather than a role stereotype: *"a reliability engineer, since Meridian is your top
  priority and it's at risk."* Chief of Staff names 2-3 candidates with the reason attached and asks the
  principal to pick **at most one** to stand up now (the per-member intake runs long); the rest stay a
  `/team-member-onboard` away. Accepting runs the existing `brain/playbooks/team.md` intake unchanged.
  - **Grounded or skipped** — every proposed member must trace to something captured that session. Too
    thin to ground, and it falls back to a one-line generic offer or skips entirely, per the honesty rail.
  - **No new ask.** This moves an existing opt-in rather than adding one, so the flow still has four.
    Step 4 now carries two of them, so the flow explicitly paces it: never propose a team straight off a
    declined OKR critique.
  - `team-offer: off` still skips it, and a prior decline is still remembered.
- **Directive-format preferences.** A preference bullet is now a dated, imperative directive —
  `<!-- observed: YYYY-MM-DD | status: active|superseded -->` above the line. A changed preference
  is **superseded in place**: the active directive is rewritten with the new instruction, the prior
  line flips to `superseded` and stays (a trail, not a version log) — never two contradictory
  `active` directives at once. Onboarding step 5b now writes captures this way; a legacy
  un-annotated bullet reads as implicitly active. New `### Memory — preference` template and
  `### Preference directives` convention (`brain/schemas/memory-file.md`), new
  `### Preference changes — supersede in place` (`brain/schemas/capture-rules.md`), and a new
  memory-lint check 20 (contradictory actives, un-retained superseded entries, un-annotated
  legacy bullets — low severity).
- **Size discipline for always-load files.** `memory/profile/` and the single trackers now carry an
  explicit soft target (~100 lines) and a rule for outgrowth: **demote** the overflow into a linked
  on-demand file (a project's own context page, `commitments/done.md`) rather than growing the
  always-loaded file in place; index hooks stay one line. New `## Size discipline (always-load
  files)` (`brain/schemas/memory-file.md`) and memory-lint check 21 (oversized file / multi-line
  index hook — propose the specific demotion, never auto-trim).
- **Action-sensitive capture.** A fact that gates action (cleared to announce, requires sign-off) is
  now captured with an **absolute date or named condition** inline — a bare "not yet"/"soon" is a
  capture defect. An expired date or a met condition is a staleness signal. New
  `### Facts that gate action` (`brain/schemas/capture-rules.md`); memory-lint check 1 (stale
  claims) now also flags expired action-gating conditions.
- **Log distillation.** `/lint` gains a read-only sweep of `memory/log/` for durable facts never
  routed into people/projects/preferences/context/trackers — scanning since the last `lint` line in
  `memory/ledger.md` (or ~90 days if none) and proposing promotions with provenance back to the log
  entry, applied on the principal's OK via the existing `## After`. New `## Distill (log → durable
  memory)` section in `brain/playbooks/memory-lint.md`.
- **Shared-context privacy.** Memory is the principal's private counsel: person-file notes, private
  reads, preferences, hypotheses, and anything under `memory/confidential/` now never ride into a
  draft sent externally, a delegation brief, or an exported brief — private context may **shape**
  output without being **quoted**. New `## Principal-private material in shared outputs`
  (`brain/schemas/confidentiality.md`), cross-referenced from `draft-comms.md` → "Sending — the hard
  rule" and `delegate.md` → "Boundaries".
- **Orphaned-override migration.** `/update`'s delete-then-copy previously could silently degrade a
  `replace`/`extend` override into a de-facto addition if its brain counterpart was removed by the
  release. `## After updating` now checks every `## Replace`/`## Extend` entry in
  `memory/overrides/index.md` against the new brain, flags any orphan (with the removing release),
  and offers **re-home** / **convert to a pure addition** / **retire** — never a silent migration.
  `brain/playbooks/update.md` → `## After` gets a matching interaction step.
- **Origin classes & taint gating.** Every durable fact now carries a trust class —
  **principal-stated** (the default, unlabeled), **derived** (from a shared document, connector, or
  web page), or **generated** (inferred by Chief of Staff or a team member). A derived or generated
  fact never silently overrides a principal-stated one — that's a contradiction, flagged as before.
  Instructions asserted by a fetched page or an intaken document ("always do X") are captured as a
  claim by that source, never as a standing rule. New `### Origin classes`
  (`brain/schemas/capture-rules.md`), a cross-ref in `## Provenance`
  (`brain/schemas/memory-file.md`), and Distill promotions in `/lint` now name each candidate's
  origin class, calling out derived/generated ones (`brain/playbooks/memory-lint.md`).
- **Recall-loop prevention.** A fact loaded from memory this session — recalled, not newly stated —
  is never re-captured as a new entry; re-confirmation by the principal may bump `updated:`, but it
  stays one entry. `brain/schemas/capture-rules.md` → `## Procedure` dedup step.
- **Standing rules as intents.** A standing-rule directive (a preference that fires only when a
  trigger condition arises, not a general style) now accepts optional `expires:` and `trigger:`
  fields on its comment, so it's handled as prospective memory instead of a flat fact. Capture
  records the trigger context and, if time-bounded, an expiry date; surfacing follows an
  anti-nagging rule — on trigger, not as a recurring reminder every session. New fields in
  `### Preference directives` (`brain/schemas/memory-file.md`), new `### Standing rules — trigger
  and expiry` (`brain/schemas/capture-rules.md`), and memory-lint check 1 now also flags an expired
  `expires:` date on a standing-rule directive.
- **Session-wrap sweep.** When a long session is wrapping up, or earlier conversation has been
  summarized away, sweep for durable facts passive capture hasn't filed yet and write them before
  they're lost. New `### Session-wrap sweep` (`brain/schemas/capture-rules.md`).
- **Temporal/multi-hop query escalation.** When a question reaches into the past and the index hooks
  give no strong hit, the query workflow now walks `memory/log/` (bounded by the timeframe) and
  `memory/ledger.md` chronologically instead of answering thinly from always-load context.
  `brain/playbooks/query.md` → `## Workflow` step 1.

## [0.15.0] — the virtual team is a brain trust

The virtual team stops being a set of siloed specialists and becomes a **brain trust**: members share
the full context and can consult each other through the Chief of Staff. No memory-schema migration
required, and the confidentiality model (code names everywhere; real identities Chief of Staff-only) is
unchanged.

### Changed
- **The virtual team is now a brain trust.** Members share the **full shared context** instead of a
  curated, cleared slice — they read the whole shared brain (people, projects, context, decisions),
  with confidential work seen **as code names**, and they can **see their peers** via the roster. The
  per-member `clearance:`/`## Reads` access barrier is gone; the charter's optional start-here
  pointers become a non-binding `## Key context` list. The **real-identity registry**
  (`memory/confidential/registry.md`) stays **Chief of Staff-only** and is never reachable by any
  member — the code name is the protection, applied to everyone.
- **Members can consult each other — through the Chief of Staff.** A member working a delegated task
  can **hand up** that it needs another member's input (and may name the peer); the Chief of Staff
  mediates the consult (**input-only, screened as data on every leg, depth-1 and non-re-entrant, with
  provenance and no fact-laundering**) and returns **one integrated answer** in its own voice. There
  is no direct member↔member channel. **Sole-writer** (members propose, the Chief of Staff verifies
  and integrates) and **ask-before-outward** (nothing outward or irreversible without the principal)
  are unchanged.

### Migration notes

**Required — writes at boot.** Team-member charters lose per-member access control. Nothing outside
`memory/team/` changes.

- **`charter:clearance`** — a charter carries no `clearance:` field. Remove it if present.
- **`charter:reads`** — a charter carries no `reads:` frontmatter field and no `## Reads — cleared
  shared context` section. Its pointers live under `## Key context (start here — not a limit)`, which
  is a set of optional starting points rather than a boundary the member may not read past. Convert a
  `## Reads` section by renaming the heading and keeping its links; fold a bare `reads:` field into
  the same section. **Supersedes 0.9.0.**

_Backfilled in 0.30.0 from the release diff; 0.15.0 itself shipped no migration note. This entry's
summary line "No memory-schema migration required" predates that finding and is left as it shipped._

## [0.14.0] — attributed team-member voice, clearer update reload

A small, polish-focused release: when the Chief of Staff speaks in a team member's voice it now says
which member, and the post-update flow makes the "reload on a fresh session" step explicit. No
memory-schema migration required.

### Added
- **Attributed team-member voice.** When you talk to a virtual team member directly and the Chief of
  Staff **persona-swaps into that member**, it now leads each member-voiced turn with a marker naming
  the member (e.g. `**Audio dev —** …`) and **hands back to its own voice explicitly** — so you always
  know whether you're hearing the Chief of Staff or a specific specialist. This applies only to
  speaking *in the member's voice*; an **integrated delegation result stays the Chief of Staff's own
  voice, unattributed** ("one finished answer"). Presentation only, no capability change.

### Changed
- **Clearer post-update reload guidance.** After `/update`, the Chief of Staff now explains that the
  swap happens **on disk** while the current session keeps running the brain it loaded at boot — so the
  update only takes effect on a **fresh session** — and prompts you to start one now (reassuring that
  the current session is safe to keep using until you do). No change to what `/update` does.

### Migration notes

**No action required.** This release changes how a member's voice is attributed in conversation.
That is brain behavior — nothing about what your `memory/` folder contains changes.

_Backfilled in 0.30.0 from the release diff; 0.14.0 itself shipped no migration note._

## [0.13.0] — a voice with character, scheduled-task dedup, consented scan scope

A personality pass and a batch of consistency work: the Chief of Staff gets a real character layer for
its own voice, scheduled-task creation reviews for duplicates first, the onboarding history scan makes
its account scope a consented choice, and a full-brain architecture review fixes several
rule-didn't-propagate defects. No memory-schema migration required.

### Added
- **Scheduled-task dedup — review before creating.** Before creating any scheduled task (a routine,
  a per-member routine, or an ad-hoc one), Chief of Staff now **reviews what's already scheduled** and,
  on overlap (same purpose, or an overlapping cadence/time), **suggests a dedup** — update the existing
  one, adjust its timing, merge, or skip — instead of silently adding a duplicate. It applies in
  general and during onboarding (folded into step 6's single accept-all-defaults ask). Because hosts
  don't reliably expose their scheduled-task list, `memory/preferences/briefings.md` becomes a
  complete **registry** — every created task is recorded there (cadence, prompt/purpose, host, status)
  so the review can enumerate reliably; when it still can't be sure, it asks rather than duplicate.
- **A character layer for the Chief of Staff's own voice.** `brain/role/voice.md` gains a `## Character`
  (Core Truths) block — who CoS is, not just how it speaks: earn trust through competence, treat access
  to your working life as a privilege, be the steady hand under pressure, and **hold a point of view and
  say it** (lead with a recommendation, disagree plainly, don't hedge to sound safe). It's explicitly
  **subordinate to the honesty and principal-owns-the-decision rails** — opinions must be grounded in
  memory/facts and labelled as a view, never invented conviction or fabricated warmth. A new **persona
  depth** knob (`brain/role/defaults.md`) keeps the default **crisp-professional** and lets you opt into
  a more **characterful** voice, mirroring the depth setting CoS already offers for virtual team
  members. And the voice **learns**: durable style preferences you show are folded into your voice
  override and acknowledged in a line ("Noticed you'd rather I skip the preamble — saved."). (Inspired
  by the SOUL pattern; designed via the brain-experience-critic, authored by the brain-experience-author,
  and coherence-checked by the brain-rigor-critic.)

### Changed
- **Onboarding history-scan scope is now a consented, up-front choice.** The ~6-month bootstrap scan
  spans all connected accounts (work and personal), but the consent ask now **discloses that scope
  before you agree** and lets you **narrow to work-only** (or, in personal mode, name specific
  accounts). The choice is recorded as `bootstrap_scope` and honored everywhere the scan decides
  account scope — the step-3/step-6 fallback calendar scans, the `connectors.md`/`calendar.md`
  guidance, and on resume — with a privacy-safe default (never scan personal accounts on a bare "yes",
  and account-neutral wording in personal mode). Span-all remains the default for ongoing briefs and
  triage; only the onboarding scan is scoped to consent. (Found via a multi-round AI-interaction-design
  review of onboarding.)

### Fixed
- **The virtual-team slash commands now use the link-based roster** (found via a full-brain
  architecture review). The four `.claude/commands/team-*.md` still encoded the retired "team = a set
  of folders, scan them" model: `/team-member-onboard` never created `memory/team/index.md`, so on
  Claude Code a created team was invisible and unroutable at every later boot. They now create/read the
  roster and route via its `## Active` section (never a folder scan), and `/team-member-remove` sets
  `status: inactive` (not an invalid `retired`) and maintains the roster links.
- **Quarantined content can't be pulled into memory.** The reachability invariant now exempts
  `memory/_quarantined/` (and uncited `memory/_processed/` originals) consistently across the schema,
  `/lint`, the boot persona, and onboarding — so a prompt-injection file set aside during intake is
  never reported as "unreachable" and linked back into the live memory graph.
- **Decision briefs log to the tracker.** `decision-brief` now records a made decision in
  `memory/decisions.md` (with RAPID roles), not only a `log/` note, so it surfaces in the daily/weekly
  briefs that read the decision log. Plus smaller consistency fixes (the commitments archive is linked
  when created; `host:` is documented in the `meta.md` schema).

### Migration notes

**Required — no write.** One `memory/meta.md` field is documented here and carries a retired value
that must be corrected, one is genuinely new and filled in lazily, and one reachability rule relaxes.

- **`meta:host`** — `memory/meta.md` names the host under its current identifier:
  `host: claude-code | codex | other`. A tree recording `host: chatgpt-work` is rewritten to
  `host: codex` — the same host under its real name, not a different one. A tree with no `host:` line
  gets one the next time the host is detected, and nothing depends on the gap in the meantime.
  **Supersedes 0.11.0.**
- **`meta:bootstrap_scope`** — `memory/meta.md` records `bootstrap_scope: all | work-only | named`,
  the consented onboarding-scan scope. Trees onboarded earlier have none; it is written at the next
  onboarding or resume, and nothing reads it in between.
- **`path:memory/_quarantined/`** — quarantined files live at `memory/_quarantined/`, not
  `memory/inbox/_quarantined/`; move any that are still nested. Files under that folder, and uncited
  archived originals under `memory/_processed/`, are exempt from the reachability invariant. A
  quarantined file is flagged, untrusted material, not a fact to route to. If an earlier `/lint`
  linked one into the graph to satisfy reachability, that link is no longer required; nothing breaks
  if it stays. **Supersedes 0.12.0.**

_Backfilled in 0.30.0 from the release diff; 0.13.0 itself shipped no migration note. This entry's
summary line "No memory-schema migration required." predates that finding and is left as it
shipped._

## [0.12.0] — chat-drop file intake, onboarding polish, log rollup

Files are now handed over by dropping them in the chat (the inbox drop-folder and `/intake` are
retired), the onboarding flow gets a golden-moment UX pass, and the root memory index gains a log
recency window. No memory-schema migration required.

### Added
- **Log rollup — a recency window for `memory/log/` in the root index.** `memory/log/` is the only
  folder that grows without bound, and its dated one-line hooks route far more weakly than a
  person's or project's, so an unbounded log section crowds the signal out of the index. The root
  `memory/index.md` now keeps only log entries from the **last 30 days** (never fewer than the **5
  most recent**) plus one link to a new **`memory/log/index.md`**, which lists every entry newest
  first. The sub-index is created the moment an entry falls outside the window — no separate size
  threshold. Older entries stay findable by date through the sub-index and by topic through the
  provenance backlinks that already cite them.
  - This is **`log/` only.** `people/`, `projects/`, `context/`, and `preferences/` stay flat in the
    root index however long they get: their per-file hooks *are* the routing signal, and hiding them
    behind a sub-index would trade a real recall regression for no meaningful token saving.
  - Enforced on the write side by `brain/schemas/capture-rules.md` (Procedure step 3) and defined in
    `brain/schemas/memory-file.md` ("Log rollup"); `brain/playbooks/memory-lint.md` gains **check #9**
    to audit the window after the fact (team-integrity checks renumber 9–18 → 10–19).
  - **No migration needed** — an existing memory keeps working unchanged; the window applies the next
    time a log entry is captured or `/lint` runs.

### Changed
- **Give the Chief of Staff files by dropping them in the chat.** Sharing a document in the host chat
  (drag-drop / attach / paste, on Claude Code or Codex) is now the single way to hand it a file: it's
  **auto-intaked inline** — screened for prompt injection, facts extracted, routed/deduped into
  `memory/` with provenance, and logged to the action ledger — with no command and no folder to
  manage.
- **Onboarding golden-moment polish.** A UX pass on `brain/onboarding/flow.md` so every path lands its
  moments of value, not just the connector-bootstrap one: a **manual-path (and personal-mode)
  mid-flow synthesis** for users who skip the scan; a **work-IC sounding-board beat** so an IC with no
  OKRs/decisions still gets a "think-with-you" moment; the **connector-reconnect checkpoint** now
  survives a fresh-session restart and re-offers the history bootstrap on resume; the step-6 routine
  payoff and the bootstrap synthesis are **hedged/tentative and invite correction** (no falsifiable
  "brief at 8am tomorrow", no presumptuous first impression); **honest time estimates and progress
  bar** on the manual path; **Codex routine parity**; a **cumulative offer budget** to avoid opt-in
  fatigue; cheap **mid-flow mode correction**; and dedup rails so the synthesis and closing recap
  never repeat a beat.
- **History bootstrap scans all connected accounts.** The optional ~6-month onboarding scan (and the
  everyday connector use behind briefs and triage) now enumerates **every** connected calendar and
  mailbox — work and personal — instead of only the default account.

### Removed
- **The `/intake` command and the `memory/inbox/` drop-folder are gone** (both the top-level inbox and
  the per-member `memory/team/<slug>/inbox/`). The chat-drop auto-intake above replaces them; feeding
  a team member is now done by dropping a document in the chat while working with that member
  (persona-swap or its folder open). The surviving auto-intake **archive relocates to
  `memory/_processed/`** and **quarantine to `memory/_quarantined/`**.
  - **Migration:** if you have leftover files in a `memory/inbox/`, share them in the chat to fold
    them in; the old folder is otherwise inert and can be deleted. Existing memory is untouched.

### Migration notes

**Required — no write.** Chat-dropped files are ingested inline; the standing inbox folder retires.

- **`path:memory/inbox/`** — no `memory/inbox/` folder is required. Leftover files in one are not
  ingested automatically: share them in the chat to fold them in, then delete the folder. It is inert
  until you do.
- **`path:memory/_processed/`** — archived originals live at `memory/_processed/`, not
  `memory/inbox/_processed/`. Move any that are still nested.
- **`path:memory/_quarantined/`** — quarantined files live at `memory/_quarantined/`, not
  `memory/inbox/_quarantined/`. Move any that are still nested.

_Backfilled in 0.30.0 from the release diff; 0.12.0 stated its migration inline rather than as a
block. That inline statement, and this entry's summary line "No memory-schema migration required.",
are both left exactly as they shipped._

## [0.11.0] — Chief of Staff (rebrand) + the Codex host

A big batch: the product is renamed, the OpenAI host is corrected to Codex, the boot entry is
restructured, and onboarding + the website get a substantial upgrade. No change to the memory model.

### Renamed — Chief of Staff (formerly cOS)
- The product is now **Chief of Staff** (compact mark **CoS**); the old "cOS" name and its "Chief
  Operating System" double entendre are retired. Brand, website, docs, tests, the repo, and the domain
  (**chiefofstaff.team**) are renamed; the download/update artifact is now **`ChiefOfStaff.zip`**.

### Codex host (formerly labeled "ChatGPT Work")
- The OpenAI host is **Codex** (a view in the **ChatGPT desktop app**); its Local mode opens a project
  folder and reads `AGENTS.md`. Open a folder via **New chat → Choose Project → Add folders ChatGPT can
  read → your folder → Create Project**. Connectors stay **Plugins**; Claude Code is unchanged.

### Boot: a thin entry-point router
- **`AGENTS.md`** is now a small **dev-vs-use router**. In a dev checkout it offers to load the developer
  guide; otherwise it loads **`CHIEFOFSTAFF.md`** (the persona + boot protocol). The developer guide is
  now **`CONTRIBUTING.md`**.

### Onboarding
- Optional **history bootstrap** (opt-in): once connectors are on, Chief of Staff can review ~6 months of
  activity to pre-fill people/projects/rhythms — high-confidence facts stored now, inferences held as
  labeled **hypotheses** you confirm.
- **Golden moments** (synthesis reveal, an early first-value beat, a sounding-board take on decisions, a
  closing "here's your world" recap), **resume** support (`current_step`) + a minimum-viable checkpoint,
  and a one-line **mode-inference confirm**.

### Memory rules
- `updated:` MUST be set on every memory-file touch; new **fact-vs-hypothesis** capture convention.

### Website
- Landing-page overhaul: hero example carousel, a "your memory is just files" trust section (incl. opening
  `memory/` as an **Obsidian** vault), accessibility + SEO (`SoftwareApplication` JSON-LD) +
  WCAG-AA contrast, a custom 404, and share-reliable OG/favicons.

### Migration

**Required — no write.** The OpenAI host's identifier changed with the rebrand, so a tree onboarded
against it records a host name the product no longer knows. Correcting it touches `memory/meta.md`
only, not the principal's own content.

- **New installs** unzip to a **`ChiefOfStaff/`** folder (was `cOS/`).
- **Existing users:** run **`/update`** (or say "update"). It refreshes `brain/` and the boot files — now
  including the new **`CHIEFOFSTAFF.md`** and the **`AGENTS.md`** router — **in place**, and **never
  touches `memory/`**. Your existing folder keeps its current name (e.g. `cOS/`); that's cosmetic and
  everything keeps working. Rename the folder yourself if you want it to match.
- The download/update URL is now **`https://chiefofstaff.team/dist/ChiefOfStaff.zip`** (the old
  `cos.team` / `cOS.zip` URLs are superseded).
- **`meta:host`** — `memory/meta.md` names the host under its current identifier; the OpenAI host is
  `codex`. A tree recording `host: chatgpt-work` is rewritten to `host: codex` — the same host under
  its real name, not a different one. A tree with no `host:` line needs nothing here.

_Migration position corrected in 0.30.0 from the release diff; the original note understated what
this release changed. This entry's summary line "No change to the memory model." predates that
finding and is left as it shipped._

## [0.10.2] — custom domain (cos.team)

Distribution polish, no brain-behavior change. The public Pages site now lives at **cos.team**, so the
download and auto-update URLs point there instead of the `github.io` project path.

- Updater (`brain/integrations/updates.md`), README, and the landing-page download buttons now use
  `https://cos.team/dist/…`. (The old `pkozanian.github.io/cOS/…` URLs redirect there, so pre-0.10.2
  installs keep working.)

### Migration
**No action required.**
- None.

---

## [0.10.1] — public downloads while the repo stays private

Distribution fix, no brain-behavior change. A private repo's **GitHub Release assets aren't publicly
downloadable**, but its **GitHub Pages site is** — so the download and auto-update now go through the
public Pages mirror instead of the Release API.

- The release workflow mirrors `cOS.zip` + `VERSION` + `CHANGELOG.md` into `docs/dist/` on every
  release; GitHub Pages serves them publicly at `https://pkozanian.github.io/cOS/dist/…`.
- `/update` and the boot update-check now fetch from that Pages URL
  (`brain/integrations/updates.md`); the README and landing-page download buttons point there too.
- Net: anyone can download and auto-update while the source repo stays private. (The `cOS.zip`
  contains the shipped `brain/`, so publishing it does make the brain content public; `memory/` is
  never in the zip.)

### Migration
**No action required.**
- None.

---

## [0.10.0] — memory is one connected graph

Generalizing the roster fix to all of `memory/`: **every memory file must be reachable by following
links from the root `memory/index.md`** (through sub-indexes — `overrides/index.md`, `team/index.md`,
member `memory/index.md`, a member's charter → ledger → delegation records, …). Memory is one
connected graph, not a folder scan. Write nothing you don't link in.

### The reachability invariant
- Documented in `brain/schemas/memory-file.md`; enforced two ways: **`/lint`** gains a first-class,
  high-severity **Reachability** check that lists every unreachable file and offers to link it in
  (`brain/playbooks/memory-lint.md`), and structural check #12 asserts it on the shipped fixtures.
- **The only exemption** is a member's generated boot files (`team/*/AGENTS.md` / `CLAUDE.md`) — pure
  bootstraps for independently-running subagents.
- `meta.md` is now linked from the root index; delegation records and member ledgers are reachable via
  the charter → `ledger.md` → record chain.

### Confidential registry — reachable, still guarded
- The registry is now **linked once, from the root `memory/index.md`** (reachable/auditable) instead of
  being unlinked. Its **contents are still never quoted or echoed**, `memory/` stays git-ignored, and
  it is **never linked from the team subgraph or any member-readable page** — so members still reach it
  via no path. Only its existence is linked, never its identities.

### Migration

**Required — writes at boot.** Memory became one connected graph, and a tree written before this
release has files nothing links to — including two the release linked for the first time. Repairing it
edits `memory/index.md` and member charters, which is principal content.

- None required. Behavior/convention only. Existing installs can run **`/lint`** once after updating to
  surface (and link in) any file the new reachability check flags.
- **`path:memory/index.md`** — every file under `memory/` is reachable by following links from
  `memory/index.md`, transitively through sub-indexes; sitting in the right folder is not enough. A
  file nothing links to is linked from the index, or from the page that owns it, in whichever tier
  fits. Later releases exempt specific paths; those exemptions are stated on their own entries.
- **`path:memory/meta.md`** — `memory/meta.md` is reachable from the root `memory/index.md`, under a
  Load-on-demand heading (the conventional one is `### Metadata`). Add the link where an index does
  not carry it.
- **`path:memory/confidential/registry.md`** — the registry is linked **once**, from the root
  `memory/index.md`, so it is reachable and auditable; linking it does not relax the handling rule —
  its contents are still never quoted or echoed. That one root link is the only link it ever gets: it
  is never linked from `memory/team/index.md`, a charter, a member's own memory index, or a project
  page a member is cleared to read. Where the registry exists, add that root link if the index lacks
  it; a principal who has never had a confidential project has no registry and needs no link. Remove
  any link to it that exists anywhere in the team subgraph.
- **`charter:records`** — a member that has a `ledger.md` carries a `- **Records:** [Ledger](ledger.md)`
  line in its charter, and each `delegate` entry in that ledger links the record it logs
  (`→ [record](delegations/<file>.md).`), so roster → charter → ledger → delegation record resolves by
  link alone. Add the line, and the record links, where a ledger exists without them. A member with no
  ledger — nothing has been delegated to it yet — carries no such line and needs none; the ledger and
  its charter line arrive together when the first entry is appended.

_Migration position corrected in 0.30.0 from the release diff; the original note understated what
this release changed. Its own first bullet, "None required. Behavior/convention only", predates
that finding and is left as it shipped._

---

## [0.9.0] — the virtual team is a roster, not a folder scan

Team membership is now **explicit and link-based**. cOS discovers and routes to members only by
following links from `memory/index.md` — it never scans, globs, lists, or infers members from
directories under `memory/`.

### An authoritative roster
- **`memory/team/index.md`** is the source of truth: `## Active` / `## Inactive` sections linking each
  member's charter with a routing hook. A member is discoverable and routable **only** when its active
  charter is linked there. An unlinked `memory/team/<slug>/` folder is **orphaned data, not a member**.
- **Reachability:** `memory/index.md` → `memory/team/index.md` → `<slug>/charter.md` →
  `[Member memory](memory/index.md)` + the charter's `## Reads` links. Boot, routing, querying, and
  delegation are link-only; only a deliberate lint/audit or the migration may touch the filesystem.

### Charter changes
- Charters gain **`status: active | inactive`** (must agree with the roster section they're linked
  under) and move their cleared-reads list out of a `reads:` frontmatter field into an explicit
  **`## Reads`** body section of markdown links — the single, human-readable, machine-routable source
  of what shared pages the member may load. The confidential registry is never linked anywhere.

### Lifecycle & lint
- Create / activate / deactivate / remove / rename all maintain the link graph atomically; creating or
  deleting a folder never changes membership on its own. `memory-lint` gains team-integrity checks
  (roster↔charter link + status agreement, missing member-memory link, undeclared reads, registry
  links, and orphan directories — the last reported only in an explicit filesystem audit).

### Migration

**Required — writes at boot.**

- **Existing installs with a directory-inferred team:** on the first boot after updating (when
  `onboarded_against` < `VERSION`), cOS surfaces a one-time migration. It builds `memory/team/index.md`
  from your existing member folders (the one sanctioned filesystem scan), links every active charter
  under `## Active` (retired → `## Inactive`), links the roster from `memory/index.md`, converts each
  charter's old `reads:` into a `## Reads` link section and adds `status:`, validates reachability, and
  records the migration in `memory/ledger.md`. No member data is lost. Installs with no team are
  unaffected.
- **`path:memory/team/index.md`** — a team exists as an authoritative roster: active charters linked
  under `## Active`, retired ones under `## Inactive`, and the roster linked from `memory/index.md`.
  An install whose team was inferred from member folders is migrated by
  `brain/playbooks/team.md` → "Migrate a pre-roster team", which is idempotent. Installs with no team
  are unaffected.
- **`charter:reads`** — a charter carries a `## Reads` link section rather than a `reads:`
  frontmatter field. Convert the field into the section where one is present.
- **`charter:status`** — each charter carries `status:`.

---

## [0.8.0] — connectors that don't give up too early

cOS used to conclude an installed, authorized integration was *unavailable* when its tools weren't in
the initial context — tools can be exposed lazily — and would jump to a browser and misreport the
integration as disconnected. This release makes connector/plugin discovery reliable across hosts.

### A host-neutral discovery contract (`brain/integrations/connectors.md`)
- **Initial tool absence is inconclusive.** Tools can surface lazily/deferred; a missing tool is not a
  missing integration.
- **At least two integration-specific discovery attempts** before concluding anything — provider +
  capability (`Gmail search and read email`) *and* provider + canonical actions
  (`Gmail search_emails read_email_thread`) — not one generic query.
- **Six distinguishable states** (installed & guided · tools not yet surfaced · permission required ·
  authentication required · host-reported connection failure · genuinely unavailable), checked before
  declaring anything unavailable. **Never** call an integration disconnected on a single empty query.
- **Fallback order:** purpose-built connector/plugin → API / MCP / CLI → browser or computer-use →
  graceful degradation. Browser/computer-use is a **last resort**, only after discovery + status checks
  are exhausted. When delayed discovery succeeds, the original task **resumes** automatically, and a
  verified failure is reported precisely (no browser/permission/discovery failure dressed up as a
  connector-auth problem).

### Per-host procedures (`brain/integrations/hosts.md`)
- **Claude Code/Desktop** — `/mcp` (or connector status) when tools seem missing; `connected` /
  `needs-auth` / `failed` / `pending`; retry with connector name + expected MCP action names; tools may
  need a fresh session; don't say "reconnect" unless status shows it; prefer the connector over a
  browser.
- **ChatGPT Desktop/Work** — deferred tool discovery; search by exact plugin name + canonical action
  names; inspect plugin permissions/connection; an installed plugin skill ≠ tools already surfaced;
  avoid the browser until discovery + checks are done; a blocked Google login never implies the Gmail/
  Calendar plugin is disconnected. Host logic does not leak across hosts.

### Tests
- New structural check (run.py #4b) asserts the discovery contract's anchors in both files; a graded
  eval (`connector-no-premature-browser`) guards the core anti-pattern. (The headless eval sandbox
  can't load real connectors, so behavior is locked deterministically by the contract check.)

### Migration
**No action required.**
- None. Behavior-only; memory untouched.

---

## [0.7.0] — a team that starts sharp, and a personal cOS that feels personal

Two themes: virtual team members now begin useful instead of blank, and **personal mode** grows a
character of its own — the right words, the right discretion, and a warmer voice.

### Virtual team — members onboard with a persona and a seeded memory
- Creating a member now **synthesizes a job-typical persona** from its specialization (offered at two
  depths — a working-style voice, or a fuller character) and **seeds its memory** so it starts with
  real domain grounding instead of empty: web-grounded facts (cited) where the host has search, model
  priors marked *unverified*, and your confirmed specifics — draft-then-confirm. Seeded knowledge is
  member-scoped and never auto-promoted; the cOS stays the sole writer of shared memory.

### Personal mode feels personal
- **No work framing.** A personal cOS says **"goals & plans," not "projects,"** and drops OKRs / org
  charts / RAPID.
- **No code-name prompts.** The proactive confidentiality suggestion is now **work-mode only**;
  personal mode relies on general discretion (an explicit "keep this private" is still honored).
- **A warmer voice.** The personal cOS speaks like a trusted friend who's brilliant at running your
  life — plain language, genuine warmth, a light touch of wit, still honest and never sycophantic.
  Surfaced and adjustable at onboarding (Warmth defaults to warm-casual).

### Onboarding & repo
- **Onboarding stops pushing the `memory/inbox/` folder.** It still invites you to **upload files/
  images or use voice** in the conversation — the folder + `/intake` remain for anyone who wants them,
  just not front-and-center.
- **The memory ignore rule moved to the top-level `.gitignore`** (with a tracked `memory/.gitkeep`),
  so you can version your `memory/` in a separate git repo if you like.

### Migration

**Required — no write.** Moving the ignore rule retired a file inside `memory/`, and an in-place
upgrade leaves the retired one behind. Nothing the principal wrote is touched.

- None. Existing memory is untouched. New members gain a `persona` block and seeded notes; already
  onboarded principals are unaffected (a re-onboard picks up the personal-mode voice/vocabulary).
- **`path:memory/.gitignore`** — the `memory/` folder carries no `.gitignore` of its own; an ignore
  rule, where one is wanted, belongs to the folder the install sits in, not inside `memory/`. A folder
  still holding the shipped file — the one whose only rules are `*` and `!.gitignore` — has it
  deleted: that `*` rule hides the whole memory tree from any repository the principal keeps the
  folder in, which is exactly what moving the rule was meant to stop. A `memory/.gitignore` carrying
  any other rule was written by the principal, not shipped — leave it exactly as it is. A folder that
  has none needs nothing.

_Migration position corrected in 0.30.0 from the release diff; the original note understated what
this release changed. Its own first bullet, "None. Existing memory is untouched.", predates that
finding and is left as it shipped._

---

## [0.6.0] — onboarding that fits you

Onboarding is no longer one-size-fits-all. It now tailors the whole interview — and the cOS's ongoing
behavior — to who you are.

### Onboarding modes (work / personal, and IC / manager)
- **Work vs personal fork** at the top of onboarding. A **personal** cOS runs a genuine
  life-management flow (household, family, personal goals) — no org, manager, OKRs, or RAPID
  decisions. A **work** cOS keeps the org/priorities/decisions flow.
- **Within work — IC vs manager.** Inferred from your role/title; asked only when ambiguous. The two
  tracks differ mainly in emphasis (people orbit, priorities, routines, and how the virtual team is
  framed).
- **Infer, don't interrogate.** If your opening already implies the mode ("VP of Product at Northwind"
  → work + manager; "help me run my household" → personal), the cOS infers it and proceeds, asking the
  one-line fork only when it can't be derived.
- **Recorded in your profile.** The chosen mode is written to the Always-loaded profile
  (`Context: work|personal`, `Role type: IC|manager`) and `memory/meta.md`, so every session's briefs,
  prep, and language adapt — not just onboarding.

### Docs
- README and website now lead with the chief of staff and present the team as the upgrade; the
  marketing copy no longer uses "operating system." The generic team example is a software developer.

### Under the hood
- Behavioral evals now run on **Sonnet** by default (`COS_EVAL_MODEL`, override to `opus` etc.) —
  exercising the product on the model users typically run and keeping eval volume cheap.

### Migration

**No action required.**

- None. Existing memory is untouched. Newly onboarded principals get `Context`/`Role type`; already
  onboarded principals keep working unchanged (a re-onboard would add the fields).
- **`meta:context`** — `memory/meta.md` records `context: work | personal`, mirrored as `Context:` in
  the Always-loaded profile. A tree onboarded before this release records neither, and needs neither:
  the personal fork did not exist yet, so such a tree is a work install and its silence reads that
  way. The field is written at the next onboarding, or when the principal corrects the mode.
- **`meta:role_type`** — in work mode, `memory/meta.md` records `role_type: ic | manager`, mirrored as
  `Role type:` in the profile. A tree onboarded earlier has neither. It steers emphasis only — the
  people orbit, how priorities and the team are framed — so its absence costs tailoring, not
  correctness, and it is filled in at the same points.

---

## [0.5.0] — the virtual team, and a new name: **cOS**

The biggest release yet: the product grows from a single chief of staff into one that **builds and
runs a team** — and gets the name to match.

### New name — cOS (Chief of Staff · Chief Operating System)
- Rebranded from "Chief of Staff / CoS" to **cOS** (pronounced "Koss") — a double entendre: it's your
  **chief of staff**, and, now that it runs a team of specialist agents, the **operating system for
  how you work**. The agent still presents as your chief of staff; "Chief Operating System" is the
  brand wink. README, website, and the release asset are rebranded; the download is now **`cOS.zip`**.

### Virtual team (Phases 1–3)
- **Create specialist team members** — each a `memory/team/<slug>/` with its own charter, deep
  memory, generated `AGENTS.md`/`CLAUDE.md` (open the folder to load the member standalone on any
  host), and access-scoped `reads:`/`clearance:`. Offered at onboarding or via `/team-member-onboard`.
- **Delegate → verify → integrate.** cOS hands a task to a member, verifies the deliverable against
  acceptance criteria, and integrates promoted facts into shared memory — **cOS stays the sole writer
  of shared memory**; members hold compartmentalized deep context and propose facts upward.
- **Routing** — inbound facts and questions go to the right owner (specialist member vs shared memory).
- **Native-subagent acceleration** — on Claude Code, a member also projects to `.claude/agents/<slug>.md`
  for isolated/parallel dispatch; persona-swap is the portable floor everywhere else.
- **Cadence, autonomy, digest, per-member inbox** — members can hold standing routines, run under a
  bounded `autonomy` (nothing outward/irreversible without you), surface a once-a-session team digest,
  and be fed directly via a per-member inbox.
- Commands: `/team-member-onboard`, `/team-members`, `/team-member-review`, `/team-member-remove`.

### Migration

**No action required.**

None. Existing memory is untouched; the team is opt-in and invisible until you create a member.

---

## [0.4.0] — slimmer frontmatter schema

Trims the memory-file frontmatter to what actually earns its place. **Schema change** (pre-1.0
MINOR), but backward-compatible in practice.

### Changed
- **Dropped `layer:`** from every file. A file's tree is implied by its location (`brain/` vs
  `memory/`) — the field was pure redundancy that nothing branched on.
- **Dropped `version:` from brain files.** The release now lives solely in the top-level `VERSION`
  file (+ this changelog); brain files no longer repeat it. Cutting a release no longer hand-bumps
  every brain file.
- **Renamed memory `version:` → `updated:`** — an honest name for what it always was: the date the
  file was last edited (`YYYY-MM-DD`). Capture rules bump `updated` on every edit.
- New required frontmatter: **brain** = `name`, `description`, `type`; **memory** = those plus
  `updated` (situational `relationship` / `confidential`+`codename` / `mode`+`base_version` unchanged).

### Migration

**No action required.**

None required. Existing memory files that still carry `layer:`/`version:` keep parsing — the extra
keys are simply ignored — and the cOS drops them / switches to `updated:` the next time it edits a
file. No action needed on upgrade.

- **`frontmatter:layer`** — a memory file carries no `layer:` key. A file that still has one parses
  fine; the key is ignored and dropped the next time that file is edited.
- **`frontmatter:version`** — a memory file carries no `version:` key; freshness is tracked by
  `updated:`. Same lazy convergence — ignored where present, dropped on next edit.

---

## [0.3.0] — sharper onboarding & always-on capture

Refines the day-one experience and makes capture effortless. Brain changes since 0.2.0:

### Onboarding
- **Lint-clean by construction.** A freshly-completed onboarding now produces a `memory/` tree that
  passes memory-lint immediately: it creates `memory/overrides/index.md` up front (no dangling index
  link), keeps a dated **onboarding source note** and cites it as provenance from
  profile/projects/OKRs, wires **reciprocal** backlinks, and confines confidential identities to
  `memory/confidential/`. A closing **self-audit** runs the lint checks and fixes any
  onboarding-generated structural defect *before* marking onboarding complete.
- **Voice input encouraged** alongside document uploads — the principal can dictate answers instead
  of typing.

### Capture
- **Auto-intake of attached documents.** A document shared in the conversation is folded into memory
  immediately — screened as untrusted data, facts filed, provenance kept — the same result as
  `/intake`, with no inbox round-trip. Files dropped in `memory/inbox/` stay manual (`/intake`).

### Fixes
- **No maintenance nag right after onboarding.** The session-start explore/lint offer anchors its
  "never-run" clock to the onboarding date, so the first offer comes one cadence later, not the
  moment onboarding ends.

### Also in this release (non-brain)
- Editorial **GitHub Pages landing page** under `docs/`; the README now links the stable
  latest-release ZIP.

### Migration notes

**No action required.** One `memory/meta.md` field is new and is filled in lazily.

- **`meta:last_onboarded`** — `memory/meta.md` records the onboarding date, which anchors the
  session-start maintenance-offer clock. A tree onboarded before this release has none; it is written
  at the next onboarding, and until then the maintenance offer simply does not fire.

_Backfilled in 0.30.0 from the release diff; 0.3.0 itself shipped no migration note._

---

## [0.2.0] — first distributed release

The first release intended for **deployment to executives**. Rolls up all the 0.1.0 development work
(below) and adds packaging, distribution, and **prompted self-update**:

### Packaging & distribution
- **GitHub Releases ZIP** — each tagged release publishes an exec-ready ZIP (brain + `AGENTS.md` +
  `CLAUDE.md` + `.claude/commands/` + `VERSION` + `CHANGELOG.md` + README + empty `memory/`), built
  by `.github/workflows/release.yml`. No build step, no dev files (`tests/`, `.github/`,
  `DEVELOPING.md` excluded).
- **Three-step install** (Mac & Windows, no terminal/git): install the host (Claude Code desktop or
  ChatGPT Work) → download + unzip the release → open the folder and say "onboard me". See `README.md`.

### Prompted self-update
- **Boot update check** (`AGENTS.md`) — gated (≤ once/day, off-able), compares the local `VERSION`
  to the latest published one; when newer, **prompts** with the changelog highlights. Degrades
  silently with no network / no execution surface.
- **`/update`** (`.claude/commands/update.md` + `brain/playbooks/update.md`,
  `brain/integrations/updates.md`) — on the principal's OK, downloads the latest release and swaps in
  the new `brain/` + top-level files, **leaving `memory/` untouched**, bumps `VERSION`, and reports
  what changed + any migration notes. **Host-agnostic** (any host that can fetch + write files).
- New adjustable default (**Update check**: on/when-due · off) in `brain/role/defaults.md`.

### Migration notes

**No action required.** Three top-level memory files are new; each is created the first time it is
needed, and nothing about an existing tree changes shape.

- **`path:memory/commitments.md`** — exists once there is a commitment to track. Its absence is valid.
- **`path:memory/okrs.md`** — exists once the principal shares objectives. Its absence is valid.
- **`path:memory/decisions.md`** — exists once a decision is logged. Its absence is valid.
- **`frontmatter:relationship`** — a `memory/people/` file carries `relationship:` (one of
  `manager`, `skip-up`, `peer`, `direct`, `skip-down`, `cross-org`, `external`). Person files written
  before this release stay valid without it and pick it up the next time they are edited.

_Backfilled in 0.30.0 from the release diff; 0.2.0 itself shipped no migration note._

---

## [0.1.0] — initial development release

Pre-1.0 and not yet deployed anywhere; the schema and behavior may still change before 1.0.0.
This is the accumulated state of the cOS as first assembled.

### Core memory system
- Boot protocol and two-tree memory model (`brain/` + `memory/`).
- Tiered index router pattern (`## Always load` / `## Load on demand`).
- Role definition: charter, principles, voice.
- Memory-file schema and passive-capture routing rules; memory links related files with
  standard markdown links (relative paths).
- First-run onboarding flow and question bank.
- Playbooks: weekly review, meeting prep, decision brief, inbox triage.

### Memory override / overlay layer
- **Overlay tree `memory/overrides/`** mirroring `brain/` by path, letting a deployment
  extend or overwrite brain behavior without editing the shipped `brain/` tree.
- Whole-file override modes: `mode: replace` (stand in for the brain file) and `mode: extend`
  (amend it; override wins on conflict). Overrides at a path with no brain counterpart are
  pure additions.
- Global precedence rule (**memory overrides brain**) and an overlay step in the boot
  protocol (`CLAUDE.md`).
- Override frontmatter fields `mode` and `base_version`, plus boot-time staleness surfacing when
  an override's `base_version` predates a brain change.
- Capture policy for overrides: `extend` created autonomously; `replace` of core brain
  (`role/*`, `schemas/*`) requires explicit principal confirmation. Capture still never writes
  into `brain/`.

### Onboarding experience
- **Progress bar** at the start of every onboarding step (compact bar: step count + 6-cell fill
  + `~N min left`), driven by a steps-manifest table in `brain/onboarding/flow.md`.
- **Time estimate** — onboarding announces "about 10–15 minutes" up front, with per-step estimates.
- **Upload recommendations** — mentions uploading screenshots/documents up front and reminds at
  high-value steps (org-chart screenshot at People, planning doc at Projects); the cOS extracts
  structured info from uploads, writes the memory, and confirms it with the principal.

### Empty memory tree + clean git split
- **`memory/.gitignore`** (`*` + `!.gitignore`): the `memory/` folder is tracked but all its
  contents are git-ignored, so `git pull` updates the brain without clobbering memory.
- Root `.gitignore` for OS/editor hygiene.
- The `memory/` tree is **empty by default** — its subfolders, `meta.md`, `index.md`, and
  `overrides/index.md` are created during onboarding and by capture, not pre-shipped.
- Boot tolerates a missing `memory/index.md` (treat memory as empty) and a missing
  `memory/overrides/index.md` (treat as "no overrides").
- "Memory layout (created on demand)" reference in `brain/schemas/memory-file.md`, and a
  "Version control" section in `README.md`.

### Confidential projects (code names)
- **Confidentiality system** (`brain/schemas/confidentiality.md`, Always-loaded): confidential
  projects are referred to **only by a non-descriptive code name** in all output.
- **Guarded registry** `memory/confidential/registry.md` — the single place the code name ↔ real
  identity mapping lives; loaded silently at boot, never surfaced. Working memory is de-identified.
- Always-on **substitution rule** in `CLAUDE.md`; **suggest + explicit flagging** for
  sensitive-looking topics (M&A, layoffs, legal, unannounced launches, personnel, financials).
- Behavioral control, not encryption — the registry is plaintext but lives in the git-ignored
  `memory/` tree, so it is never committed or pushed.

### Inbox ingestion (file-based capture)
- **`memory/inbox/`** drop zone: the principal adds memory without prompting by saving raw notes
  (meeting notes, docs) there — via any editor.
- Ingestion is **manual, via the `/intake` slash command** (`.claude/commands/intake.md`) or on
  request — the cOS **does not ingest automatically**; when files are waiting it **reminds the
  principal to run `/intake`** (at boot and when it notices them). `/intake` extracts durable facts,
  routes/dedups them into structured memory, updates the index, applies confidentiality, archives
  each raw file to `memory/inbox/_processed/`, and summarizes what it captured.
- Reuses the passive-capture rules (one source of truth in `brain/schemas/capture-rules.md`).
- **Any file type, not just Markdown** — `/intake` processes whatever is dropped (text, PDFs,
  Office docs, spreadsheets, images, …) best-effort, skipping only hidden/system files;
  archives/quarantines preserve the original extension. A format that genuinely can't be read is
  left in place (never deleted or guessed). Onboarding also **creates `memory/inbox/` at the start**
  so there's a drop-zone from turn one. Covered by the `intake-nonmd` eval.
- **Prompt-injection screening** — every `/intake` screens each file first; untrusted docs that try
  to override rules, exfiltrate memory, or trigger actions are **quarantined to
  `memory/inbox/_quarantined/`** and flagged, not obeyed (files are treated as data, not instructions).

### Adjustable defaults (called out at onboarding)
- Onboarding now **calls out the cOS's behavioral defaults** and leaves the principal only the
  option to change them (no configuring from scratch). Catalog in `brain/role/defaults.md`: length,
  directness/sternness, warmth/formality, pleasantries, and proactivity — each with its shipped
  default marked and an override target. (Inbox ingestion isn't a knob — it's always manual via
  `/intake`.)
- A **changed** default becomes an `extend` override in `memory/overrides/`; **accepting** the
  defaults creates nothing.

### Explicit onboarding
- Onboarding starts **explicitly**, not automatically: `/onboard` slash command
  (`.claude/commands/onboard.md`), or the one-line shell start `claude "/onboard"` /
  `claude "onboard me"` (an opening-message trigger in `CLAUDE.md`, since the CLI can't invoke a
  slash command directly). Works first-run and as a re-onboard (create-or-update).
- On an un-onboarded start the cOS greets and points to `/onboard` rather than forcing the flow.

### Operating principles
- Operating principles incorporate four behavioral guidelines (adapted from coding-agent guidance
  to the cOS's markdown/executive-work domain), de-duplicated into one set: **think before acting**,
  **do the least that solves it**, **define success criteria and close the loop**, and **edit
  memory surgically**.

### Tests
- **Structural suite** (`tests/run.py`, Python stdlib): frontmatter validity, index completeness,
  link resolution, naming guards, version consistency, override mirror-paths, slash-command
  validity, and gitignore behavior. Runs in CI (`.github/workflows/tests.yml`) on push/PR.
- **Behavioral eval** (`tests/eval/`): a headless `claude -p` harness that drives onboarding,
  `/intake`, capture, overrides, and confidentiality in a throwaway repo copy and asserts on the
  results. Local/on-demand (non-deterministic, needs auth/tokens) — not run in CI.
- **Memory-retrieval suite** (`mem-*`, run with `run_eval.py --filter mem-`): the cOS's hardest
  behavior under test. **7 deep static fixture principals** (`tests/fixtures/memory/<persona>/`)
  spanning leadership level (C-suite → first-line manager → individual contributor), industry, and
  technicality — each a full onboarded memory tree with planted traps (same-name people, stale-vs-
  current facts, multi-hop chains, buried needles, absent look-alikes, aggregation, confidential
  code names). A 54-scenario battery asserts retrieval across fact / disambiguation / latest-wins /
  multi-hop / buried-needle / confidential / absence / routing / aggregation / synthesis —
  deterministic-first (`out_has` a verbatim fact, `out_lacks` a confidential real name), with an LLM
  judge only for `synthesis` and `absence`. Fixtures are test data — exempt from the structural
  frontmatter/naming/link/coverage checks. Largest/most token-costly suite; on-demand only.

### Test-coverage drift detection
- **Coverage manifest** (`tests/coverage.md`) maps every functional file (`brain/**/*.md`,
  `CLAUDE.md`, `.claude/commands/*.md`) → its tests + a blessed content hash. Structural check #9
  fails on **add** (unregistered file), **remove** (dangling row), or **modify** (hash mismatch),
  and on broken/orphan eval-scenario references — so tests can't drift out of sync with the brain.
- `tests/bless.py` acknowledges a reviewed change in one command; opt-in pre-commit hook
  (`tests/hooks/pre-commit`, install via `git config core.hooksPath tests/hooks`).

### Evals in CI
- `.github/workflows/eval.yml` runs the behavioral evals in GitHub Actions — **manually** (Run
  workflow, optional single scenario) and **weekly, but only if** the functional surface changed in
  the last ~8 days (a `gate` job; skips otherwise). Never on push; non-blocking.
- Authenticates via a `CLAUDE_CODE_OAUTH_TOKEN` secret (your subscription, not API billing;
  generated with `claude setup-token`, 1-year expiry). See `tests/README.md`.

### Stakeholder map
- Onboarding now maps the principal's **whole orbit** by circle — manager, skip-up, peers, directs,
  skip-down, cross-org, and external — instead of one lumped "key people" prompt. Person files carry
  a `relationship:` tag (`manager | skip-up | peer | direct | skip-down | cross-org | external`) so
  the cOS can group the map. Covered by the deterministic `stakeholder-map` eval.

### Follow-through, briefings, comms & connectors (Claude Code desktop)
- **Commitment tracking** — a single `memory/commitments.md` tracker (what/owner/due/status) +
  a `commitments` playbook (surface due/overdue/slipping) + capture routing, so nothing drops.
- **Briefing suite** — `daily-brief`, `weekly-retro` (close-out), `weekly-preview` (look-forward)
  playbooks, delivered by scheduled **Routines** (`integrations/routines.md`) as **overridable
  defaults** — configured **Local** (cloud routines run on a fresh clone and can't read the
  git-ignored `memory/`). Retires the combined `weekly-review`.
- **Routine setup is now proactive and self-service** — instead of only mentioning routines (or
  making the principal set them up by hand), the cOS **proposes the three briefs and then creates
  them itself using its routine tools** — each create/update surfaces a tool-approval prompt the
  principal accepts (that acceptance is the confirmation; no manual UI steps). Persistent **Local**
  routines. Runs at onboarding step 6, via the **`/routines`** command anytime, and via a gated
  one-time offer when any brief has no recorded decision. Outcomes (`created` / `declined` /
  `deferred`) are tracked in `memory/preferences/briefings.md` so the cOS doesn't re-nag. Honest
  limits documented (approve-on-execution + one-time working-folder trust prompt; Local routines
  only fire while the desktop app is open/awake). Covered by the deterministic `routines-suggest`
  eval.
- **Comms drafting** — `draft-comms` playbook (draft in the principal's voice; never send without
  an OK; prepare a draft via the connected mail).
- **Connectors** — `integrations/calendar.md` (native **Google Calendar** + **Microsoft 365**;
  M365 needs a business account) and `integrations/connectors.md` (a map of calendar/mail/docs/
  PM/dev/chat connectors → what each unlocks). Onboarding recommends the right ones for the
  principal's stack.
- **README quick start** recommending Claude Code desktop; `CLAUDE.md` connectors/routines note.
- **Fuller use of the desktop environment** — `meeting-prep` now pulls the **live calendar event +
  related mail/docs** via connectors (not memory alone); onboarding **bootstraps from the calendar**
  (drafts the people map from frequent attendees/standing 1:1s in step 3, and infers cadence in
  step 6, for the principal to confirm); `commitments` offers to **draft nudges** for waiting-on
  items and **surfaces overdue/urgent proactively** (desktop notification / reminder routine); and
  `draft-comms` now **creates the draft in the mailbox** (ready to send) rather than just text. All
  outward actions stay confirmation-gated.

### Multiple hosts (Claude Code + ChatGPT Work) via open standards
- The cOS is now **host-aware** — the same local folder (`brain/` + `memory/`) runs on **Claude Code
  desktop** and **ChatGPT Work** (folder-backed Project → *Use an existing folder*), with identical
  local file-based memory + the confidential registry on both.
- **`AGENTS.md`** (new, repo root) — the **primary** guide and single source of truth, read directly
  by ChatGPT Work and other `AGENTS.md`-aware tools. **Claude Code** loads it via a one-line
  `@AGENTS.md` import in `CLAUDE.md` (the Anthropic-recommended pattern), so there's no duplication.
- **`brain/integrations/hosts.md`** — maps each host's plumbing: boot (`CLAUDE.md`/`AGENTS.md`),
  connectors (Claude **Connectors** vs ChatGPT **Plugins**), scheduled briefs (Claude **Routines** vs
  ChatGPT **Scheduled**), commands (slash vs plain requests). Onboarding records `host:` in
  `memory/meta.md` and branches guidance; connectors/routines/calendar docs and the README are
  host-aware. **Run locally** (a cloud clone drops the git-ignored `memory/`).

### OKRs & decision tracking (RAPID)
- **OKRs** — a `memory/okrs.md` tracker (`type: okr`) + `brain/playbooks/okrs.md`. Beyond recording,
  the cOS **critiques OKRs when shared** — flagging activities-masquerading-as-KRs, missing
  baselines/targets, unowned or misaligned or sandbagged KRs — and offers outcome-based rewrites.
- **Decision log (RAPID)** — a `memory/decisions.md` log (`type: decision`) + `brain/playbooks/decisions.md`.
  The cOS **calls out every decision, implied or explicit, as a separate tracked item** with **RAPID**
  roles (Recommend / Agree / Perform / Input / Decide), infers roles from memory and flags gaps
  (never fabricates who decides), right-sizes RAPID to the stakes, and tracks decisions to resolution.
  Complements `decision-brief` (which helps *make* a decision).
- Wired as **always-on passive capture** (`AGENTS.md`, `capture-rules.md`) and into **onboarding**
  (step 4 captures OKRs + offers a critique, and captures open decisions). New `okr`/`decision` memory
  types; covered by the `okr-critique` and `decision-log` evals.

### Playbook & capture refinements (from behavioral-eval findings)
- **Playbooks produce, don't defer** — `meeting-prep`, `daily-brief`, `weekly-retro`, and
  `decision-brief` now state explicitly to **produce the artifact in the same turn** rather than
  offering to; capture/index housekeeping happens alongside, never in place of the deliverable.
- **`decision-brief` reached when asked to decide** — `capture-rules.md` and `AGENTS.md` now route an
  explicit "help me decide" request to **run `decision-brief.md` and produce the brief** (the decision
  is still logged to `memory/decisions.md` alongside), instead of only logging it and deferring.
- Behavioral-eval harness hardened: format-flexible date assertions, corrected over-strict decoys,
  de-flaked LLM-judge wording, and consistent (fully-indexed) onboarded seed fixtures.

### Second-brain capabilities (memory hygiene & discovery)
- **Memory Lint** (`/lint` → `brain/playbooks/memory-lint.md`) — a read-only self-audit of the
  principal's `memory/`: stale claims, contradictions, orphan files, broken links, uncited durable
  facts, duplicates, missing cross-references. Reports findings (never silently rewrites) and offers
  to apply fixes.
- **Explore** (`/explore` → `brain/playbooks/explore.md`) — surfaces non-obvious connections across
  people/projects/decisions (shared owners, cross-project dependencies/risks), grounded strictly in
  stored memory, and offers to add cross-references. Turns the "anticipate" mandate into a workflow.
- **Contradiction-flagging** — when new durable info conflicts with a stored fact, `capture-rules.md`
  now flags both claims (with dates/sources) and confirms material conflicts before overwriting,
  rather than silently replacing (latest-wins preserved).
- **Source-provenance** — `memory-file.md` adds a lightweight convention to cite where a durable fact
  came from (a link to the `log/` event or the retained `inbox/_processed/` original); `/intake`
  records provenance on ingest, and lint flags uncited facts.
- Adapted from a "second brain" wiki pattern; deliberately skips wiki-style double-bracket links
  (conflicts with the naming guard; cOS uses standard markdown links), parallel `raw/`/`wiki/`/
  `outputs/` trees (memory/ already fills that role), and an append-only action log.

### Answer citations, reciprocal backlinks, action ledger
- **Query with citations** — new `brain/playbooks/query.md` (answer-from-memory workflow: read
  index → pages → synthesize bottom-line-first → cite sources → offer to file back → flag gaps) plus
  a `voice.md` convention: cite the memory page(s) an answer draws on **when it matters or when
  asked** (inline `(per [page](path))` or a trailing `**Sources:**` line, reusing the provenance
  style). Traceable-on-request rather than citation-on-every-line (fits the concise cOS voice).
- **Reciprocal backlinking** — `memory-file.md` + `capture-rules.md` now require links to be
  **reciprocal** (link A→B, add B→A; wire inbound links when creating a file), the write-side
  complement to `memory-lint`'s orphan/missing-cross-ref checks.
- **Action ledger** — a top-level append-only `memory/ledger.md` recording what the cOS *did*
  (`## [YYYY-MM-DD] <action> | <desc>`, grep-parseable; actions: ingest/lint/explore/contradiction/
  create/delete). **Milestones only** (intake runs, lint/explore runs, contradiction resolutions,
  notable create/delete) — not routine single-fact captures. Append-only; distinct from the `log/`
  folder of dated session notes.

### Periodic memory maintenance (lint + explore)
- **Maintenance routines** — `/lint` (monthly) and `/explore` (biweekly) join the daily/weekly briefs
  as schedulable **Local Routines** (`routines.md`), with matching adjustable-default knobs
  (`defaults.md` 9–10) proposed and set up at onboarding step 6 / via `/routines`; cadence overridable.
- **Session-start maintenance offer** — a new boot-protocol step offers to run an **explore, then a
  lint** at session start, **only when due** (reads the last run from `memory/ledger.md` vs the
  cadence) and only on a bare opener — a real task always gets answered first, never hijacked. Names
  each one's benefit, asks permission, never auto-runs, and is toggleable (`boot-offer: off`,
  defaults.md knob 11).

### Migration
**No action required.**
- None — initial development release.
