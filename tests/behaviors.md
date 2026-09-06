# Behavior coverage registry

One row per behavior the Chief of Staff promises. Structural check #17 keeps it honest in both
directions: a scenario naming an unregistered ID fails, and a row citing a scenario that no longer
names it back fails. It also gates completeness — a shipped functional file no row states, an eval
scenario no row claims, and a `check()` carrying no `behavior=` each fail the suite.

- **ID** — `<AREA>-<NN>`. Permanent: never renumbered, never reused. A retired behavior keeps its ID
  and moves to [`decisions.md`](decisions.md).
- **Behavior** — the invariant that holds, stated in one line. Not the test that checks it.
- **Stated in** — the `src/`-relative file that states the rule, or `repo policy` for invariants no
  shipped file states (archive shapes, the dev/dist boundary, workflow pinning).
- **Covered by** — space-separated. `eval:<key>` names a scenario; `eval:<glob>` matches several via
  `fnmatch`; a bare `check` means a structural `check()` call carries this ID. **An empty cell means
  untested** — legal, counted, and the point of the artifact.
- **`check(fixture)` is a weaker claim than `check`.** It marks a check that reads a hand-maintained
  fixture under `tests/fixtures/` rather than the shipped tree, so it proves *the fixture satisfies
  the rule* — not that the shipped flow produces output that does. Loosen the rule in `brain/` and a
  bare `check` goes red; a `check(fixture)` stays green until someone also edits the fixture. Use it
  for any structurally-covered row whose check reads a fixture, and see
  [`decisions.md`](decisions.md#fixture-backed-checks) for why the distinction is recorded rather
  than fixed. **The suite does not enforce the qualifier** — the marker is read as the bare `check`
  inside it, so a row can drop `(fixture)` silently. It is a convention, kept honest by hand; all 29
  were verified against their call sites on this branch, and why it stays unenforced is recorded in
  the same entry.
- **Escape a literal `|` in any cell as `\|`.** An unescaped one splits the row into five columns;
  check #17 fails it rather than dropping it, but the row is still wrong until you escape it.

## Where the coverage is

**A checksum, not decoration.** Check #17 rule 7 compares every count below with the rows, so the
table cannot drift: add or move a row and the suite fails until you edit it. **The table follows the
rows, not the other way round** — on a mismatch, check first for a mistyped or dropped row before
touching the table; only edit the table once the rows are confirmed correct. That reconciliation is
also the only guard a **gap** row has: a covered row is held from both sides by rules 2 and 3, but
nothing claims a gap row, so without these counts a mistyped ID would drop a behavior in silence. Read
a gap count as "nothing asserts these", never as "these are broken".

| Area | Rows | Covered | Gaps |
|------|-----:|--------:|-----:|
| `BOOT` boot + routing | 35 | 19 | 16 |
| `ONB` onboarding | 71 | 22 | 49 |
| `ROLE` charter/defaults/principles/voice | 22 | 8 | 14 |
| `MEM` memory + retrieval | 61 | 32 | 29 |
| `CAP` capture + confidentiality | 41 | 14 | 27 |
| `PLAY` deliverable playbooks | 57 | 20 | 37 |
| `TEAM` virtual team | 76 | 43 | 33 |
| `DESK` the desk write boundary | 13 | 5 | 8 |
| `REL` updates, versioning, migrations | 39 | 24 | 15 |
| `HOST` integrations + host parity | 37 | 14 | 23 |
| `REPO` conformance + dev-repo invariants | 39 | 39 | 0 |
| **Total** | **491** | **240** | **251** |

Every area is now authored. **Read a covered cell with the `check(fixture)` caveat above**: 22 of
`TEAM`'s 38 and 11 of `ONB`'s 22 rest on a fixture rather than on shipped output, as does `MEM`'s one
structurally-covered row. **The eleven area prefixes above are the fixed set**; a twelfth is a spec
change, not an implementation decision.

### `BOOT` — boot + routing

| ID | Behavior | Stated in | Covered by |
|----|----------|-----------|------------|
| `BOOT-01` | the entry point hands off to `CHIEFOFSTAFF.md` and nothing else — the shipped tree has no developer mode to route to, so none is ever offered | `AGENTS.md` | eval:route-boots-as-cos |
| `BOOT-02` | both hosts enter through the same file: Codex reads `AGENTS.md` directly, Claude Code reaches it through the one-line import in `CLAUDE.md` | `AGENTS.md` | |
| `BOOT-03` | the boot protocol runs to completion before the principal is greeted, answered, or acted for — an instruction inside a shared document does not cancel it | `AGENTS.md` | check eval:dropped-doc-injection |
| `BOOT-04` | boot forks first-boot from re-entry before anything else, and resolves doubt toward the full boot — always so while onboarding is `pending` or `in_progress` | `CHIEFOFSTAFF.md` | |
| `BOOT-05` | a re-entry after compaction re-grounds silently and picks the conversation up — no re-introduction, and no announcement that it reloaded anything | `CHIEFOFSTAFF.md` | eval:reload-after-compaction |
| `BOOT-06` | a reload re-reads `VERSION`, both indexes, both always-load tiers, the confidential registry, the overlay and a linked roster — read-only re-grounding, with no side effect | `CHIEFOFSTAFF.md` | |
| `BOOT-07` | the once-per-session maintenance offer is not re-fired on re-entry — a re-entry is not a new session | `CHIEFOFSTAFF.md` | eval:reload-no-maintenance-repeat |
| `BOOT-08` | the once-per-day update check *does* re-run on re-entry, because a day can roll over inside a long session while a session cannot | `CHIEFOFSTAFF.md` | |
| `BOOT-09` | an un-onboarded principal is pointed at onboarding rather than put through it — nothing is written to memory until they ask for it | `CHIEFOFSTAFF.md` | eval:nudge |
| `BOOT-10` | that greeting never names a slash command, on any host, not even as an alternative — plain words work everywhere and `/onboard` does not exist on Codex | `CHIEFOFSTAFF.md` | eval:nudge eval:onboard-greeting-host-aware |
| `BOOT-11` | an `in_progress` onboarding is offered a resume from `current_step`, never silently treated as finished | `CHIEFOFSTAFF.md` | |
| `BOOT-12` | boot loads only the `## Always load` tier; an on-demand file is read the moment the conversation touches its topic, not before | `CHIEFOFSTAFF.md` | |
| `BOOT-13` | the team is discovered by link only — `memory/team/` is never scanned, globbed or listed, and an unlinked specialist folder is orphaned data rather than a specialist | `CHIEFOFSTAFF.md` | eval:team-orphan-ignored |
| `BOOT-14` | the boot capability refresh is cheap, silent and best-effort — no deep auth probes, never narrated, and it is the one memory write that is not announced | `CHIEFOFSTAFF.md` | |
| `BOOT-15` | the session-start maintenance offer fires only when a run is genuinely due, is anchored to `last_onboarded` when a check has never run, and never auto-runs anything | `CHIEFOFSTAFF.md` | eval:boot-maintenance-offer eval:boot-maintenance-fresh |
| `BOOT-16` | a real opening request is answered first — the maintenance offer rides along as at most one line and never replaces the answer | `CHIEFOFSTAFF.md` | |
| `BOOT-17` | the `/onboard` trigger runs the flow immediately and the interview it runs writes memory | `CHIEFOFSTAFF.md` | eval:onboard |
| `BOOT-18` | running the trigger after onboarding is already complete is a re-onboard: existing memory is updated, never clobbered | `CHIEFOFSTAFF.md` | |
| `BOOT-19` | an un-onboarded principal who asks something else gets it answered properly first, and the nudge is one line that is dropped if they move on | `CHIEFOFSTAFF.md` | |
| `BOOT-20` | the plain trigger phrases — "onboard", "onboard me", "start onboarding", case-insensitive and on their own — start onboarding exactly as `/onboard` does, which is what makes the slash-command-free greeting work | `CHIEFOFSTAFF.md` | |
| `BOOT-21` | the guide is never forked per host: `CLAUDE.md` keeps behavior in `AGENTS.md` and says so in the comment under its import — a Claude-Code-only directive goes below that comment as plain text, never by restating behavior `AGENTS.md` already carries (`BOOT-02` states the import path itself) | `CLAUDE.md` | |
| `BOOT-22` | the `/onboard` command enters `brain/onboarding/flow.md` at step 0 and begins the interview without asking permission first | `.claude/commands/onboard.md` | |
| `BOOT-23` | the brain router splits into `## Always load` and `## Load on demand`, and every on-demand entry names the hook that pulls it in — the router says *when* to read a file, not only where it is | `brain/index.md` | |
| `BOOT-24` | the team-member schema is not a boot file — it loads when a specialist is created, run, delegated to, or reviewed, never because `memory/index.md` links a roster | `brain/index.md` | check |
| `BOOT-25` | the session-start digest reads `memory/commitments.md`; boot never walks active specialists' charters or ledgers to rebuild it | `CHIEFOFSTAFF.md` | check |
| `BOOT-26` | boot states its reads as waves and names no host-specific mechanism for batching them | `CHIEFOFSTAFF.md` | check |
| `BOOT-27` | boot step 7 reads the cached `memory/integrations.md`; it does not load `hosts.md` or `connectors.md` to re-derive the inventory | `CHIEFOFSTAFF.md` | check |
| `BOOT-28` | the session-start maintenance clock reads `last_lint`/`last_explore` from `memory/meta.md`, which boot already loads — not a scan of the append-only `memory/ledger.md` | `CHIEFOFSTAFF.md` | check |
| `BOOT-29` | a file too large to return whole in a batch is read on its own and **once** — a truncated batch is repaired file by file, never by repeating the wave | `CHIEFOFSTAFF.md` | check |
| `BOOT-30` | a pending team suggestion is a third due-trigger for the session-start maintenance offer, raised inside that one offer rather than as a new per-session ask | `CHIEFOFSTAFF.md` | check eval:boot-team-suggestion-offer |
| `BOOT-31` | boot prints one loading tip while the second read wave lands — at most once a day, rotating by day of year, and only once onboarding is complete and tips are not switched off | `CHIEFOFSTAFF.md` | eval:boot-tip check |
| `BOOT-32` | the tip is suppressed whenever boot has something that needs the principal — a migration pass, a maintenance offer, an update prompt, or a stale-session banner — so it never competes for the turn | `CHIEFOFSTAFF.md` |  |
| `BOOT-33` | no loading tip names a slash command, which would hand a dead end to every host that has none | `CHIEFOFSTAFF.md` | check |
| `BOOT-34` | an `in_progress` onboarding resumes at the first `open` row of `memory/onboarding-checklist.md`, named in the greeting alongside the step; a missing checklist falls back to `current_step` | `CHIEFOFSTAFF.md` | eval:onboard-resume-substep |
| `BOOT-35` | the onboarding trigger while `in_progress` resumes at that row rather than restarting; only an explicit "start over" begins again at step 0 | `CHIEFOFSTAFF.md` | |

### `ONB` — onboarding

| ID | Behavior | Stated in | Covered by |
|----|----------|-----------|------------|
| `ONB-01` | personal mode never asks the confidentiality question | `brain/onboarding/steps/4-priorities-projects.md` | |
| `ONB-02` | accepting the shipped defaults writes no override at all; a dimension the principal changes writes one at that dimension's declared target | `brain/onboarding/steps/5-working-preferences.md` | eval:defaults-keep eval:defaults-change eval:interview-change |
| `ONB-03` | the work/personal mode is recorded in memory — `memory/meta.md` or a profile file carries it | `brain/onboarding/flow.md` | eval:onboard-personal |
| `ONB-04` | a work principal's role type is recorded in memory as IC or manager, so the lens it selects survives the session it was set in | `brain/onboarding/flow.md` | eval:onboard-ic |
| `ONB-05` | a mode that turns out to be wrong is switched on the spot by rewriting the two mode lines — a mis-inference never costs a re-onboarding | `brain/onboarding/flow.md` | |
| `ONB-06` | a personal onboarding creates no OKR record — the work apparatus is not run for a principal who is not at work | `brain/onboarding/flow.md` | eval:onboard-personal |
| `ONB-07` | every step from 1 on opens with the six-cell progress bar, filled to the current step, before that step's questions | `brain/onboarding/flow.md` | |
| `ONB-08` | the time estimate tracks the path actually being taken — recomputed down when the bootstrap ran, up on the manual path, and the bump is said out loud once rather than growing silently | `brain/onboarding/flow.md` | |
| `ONB-09` | steps are loaded one at a time as the interview reaches them; the rest of the flow is never preloaded | `brain/onboarding/flow.md` | |
| `ONB-10` | `current_step` is recorded at the start of every step, so an onboarding interrupted mid-flow can be resumed from where it stopped | `brain/onboarding/flow.md` | |
| `ONB-11` | onboarding writes memory as it goes, section by section — nothing is held back to be written at the end | `brain/onboarding/flow.md` | |
| `ONB-12` | the profile file is created in the turn a name first exists, before the step's questions are done — a principal who introduces themselves and walks away has still been recorded | `brain/onboarding/steps/0-set-expectations.md` | |
| `ONB-14` | every memory file onboarding writes carries a well-formed `updated:` date | `brain/onboarding/flow.md` | check(fixture) |
| `ONB-15` | memory files onboarding writes carry the frontmatter the schema actually defines — no `layer:` field, which the tree's location already implies, and no `version:`, which is the release's job | `brain/schemas/memory-file.md` | check(fixture) |
| `ONB-16` | the index onboarding leaves behind is a complete, accurate router: every file it created is linked from `memory/index.md`, and every line the index carries points at a file that exists | `brain/onboarding/flow.md` | check(fixture) |
| `ONB-17` | every relative link onboarding writes anywhere in the memory tree resolves to a real file | `brain/playbooks/memory-lint.md` | check(fixture) |
| `ONB-18` | a person page and a project page that reference each other link both ways — no one-directional pair | `brain/onboarding/flow.md` | check(fixture) |
| `ONB-19` | material pages onboarding writes carry a source link into `log/` or an archived original — the profile, the OKRs, and every non-confidential project | `brain/onboarding/flow.md` | check(fixture) |
| `ONB-20` | the real identity recorded in the confidential registry appears nowhere outside `memory/confidential/` | `brain/onboarding/flow.md` | check(fixture) |
| `ONB-21` | no topical page onboarding writes is left an orphan — every one has at least one inbound link | `brain/onboarding/flow.md` | check(fixture) |
| `ONB-22` | no two memory files onboarding wrote share a `name:` slug — the slug is the file's identity and is unique within its tree | `brain/schemas/memory-file.md` | check(fixture) |
| `ONB-23` | onboarding never finishes holding a commitment that was already overdue on the day it was captured | `brain/onboarding/flow.md` | check(fixture) |
| `ONB-24` | onboarding self-audits before it marks itself complete — the memory-lint checks are run against the memory it just built and every defect fixed first | `brain/onboarding/flow.md` | |
| `ONB-25` | step 0 sets expectations before any question: the honest time range, that uploads and speech work instead of typing, and that they can stop once the essentials are in | `brain/onboarding/steps/0-set-expectations.md` | |
| `ONB-26` | the principal is asked what they want to be called and it is recorded as `Goes by:`, which is the name used in conversation afterwards | `brain/onboarding/steps/1-principal.md` | |
| `ONB-27` | before step 2 the principal gets one role-aware first-win line, framed as capability coming online rather than a deliverable already in hand — and never a fabricated insight, because no history is connected yet | `brain/onboarding/steps/1-principal.md` | |
| `ONB-28` | connectors are recommended for the stack the principal actually described, leading with calendar and mail, and what is already connected is confirmed rather than walked through again | `brain/onboarding/steps/2-organization-context.md` | |
| `ONB-29` | browser control is one host-aware line offered once, with the never-your-password and never-send-without-a-go rails said in the same breath — a recommendation the interview does not stop on for a decision | `brain/onboarding/steps/2-organization-context.md` | |
| `ONB-30` | step 2 does not end without `memory/integrations.md` written — the capability inventory later boots keep fresh | `brain/onboarding/steps/2-organization-context.md` | |
| `ONB-31` | the history bootstrap is offered once, right after connectors, only when a useful connector is actually live, and declining it just continues the interview | `brain/onboarding/steps/2-organization-context.md` | |
| `ONB-32` | the bootstrap's consent ask bundles acceptance and scope, so a bare "yes" is never consent to scan personal accounts — work mode scans only work accounts or confirms the scope first | `brain/onboarding/steps/2-organization-context.md` | |
| `ONB-33` | in personal mode that default inverts: a bare yes must not land on a near-empty work-only scan, and the scope question is asked account-neutrally, never as "work accounts" | `brain/onboarding/steps/2-organization-context.md` | |
| `ONB-34` | the chosen scope is recorded as `bootstrap_scope` in `memory/meta.md`, and steps 3 and 6 and any resumed session honor it rather than guessing again | `brain/onboarding/steps/2-organization-context.md` | |
| `ONB-35` | the bootstrap is reviewed in one batch — a grounded synthesis, a recap of what was saved, and the top few hypotheses as a single checklist — never walked item by item | `brain/onboarding/steps/2-organization-context.md` | |
| `ONB-36` | at most one "here's your world" synthesis fires before Finishing: the bootstrap's if it ran, step 4's if it did not, and Finishing builds on whichever fired instead of repeating it | `brain/onboarding/flow.md` | |
| `ONB-37` | every observation a synthesis or the closing recap offers traces to data actually captured; too thin to be specific means skipping gracefully rather than forcing a generic-sounding insight | `brain/onboarding/flow.md` | |
| `ONB-38` | a person captured is filed under `memory/people/` and tagged with the `relationship:` value for their circle — the scenario seeds an already-onboarded principal, so it fences the capture shape rather than the onboarding step | `brain/onboarding/steps/3-key-people.md` | eval:stakeholder-map |
| `ONB-39` | OKRs are recorded and then offered a critique — offered, never forced — and an accepted critique names the sharpest issue in their actual key results and hands back the measurable reframe | `brain/onboarding/steps/4-priorities-projects.md` | |
| `ONB-40` | an open decision gets one grounded reaction before it is filed: react first, log second | `brain/onboarding/steps/4-priorities-projects.md` | |
| `ONB-41` | nobody leaves step 4 without a think-with-me beat — an IC with no OKR and no live decision, and a personal principal who has neither, each get their own | `brain/onboarding/steps/4-priorities-projects.md` | |
| `ONB-42` | the confidentiality ask is narrow — whether anything is unannounced or pre-public, never whether anything is "sensitive" | `brain/onboarding/steps/4-priorities-projects.md` | |
| `ONB-43` | the virtual team is proposed from an initiative just captured, by name — and nothing is built until the principal picks one | `brain/onboarding/steps/4-priorities-projects.md` | eval:team-propose |
| `ONB-44` | context too thin to ground a team proposal falls back to the one-line generic offer or skips it — a rationale is never manufactured to make the proposal look sharp | `brain/onboarding/steps/4-priorities-projects.md` | |
| `ONB-45` | the team offer is skipped entirely when `team-offer: off` is set or the principal has declined it before | `brain/onboarding/steps/4-priorities-projects.md` | |
| `ONB-46` | step 4 is an honest exit: with profile, people and priorities captured, onboarding can pause with `in_progress` and `current_step` set and be finished later | `brain/onboarding/steps/4-priorities-projects.md` | |
| `ONB-47` | the open preferences collected at step 5b are written in directive format, each bullet carrying its `observed:` date and `status:` | `brain/onboarding/steps/5-working-preferences.md` | |
| `ONB-48` | in personal mode the warmth default is presented as warm-casual, in a line that says how it will sound and how to change it | `brain/onboarding/steps/5-working-preferences.md` | |
| `ONB-49` | the five routines are one accept-all-defaults ask, not five separate ones; only a principal who wants to customize gets them one at a time | `brain/onboarding/steps/6-routines-cadence.md` | |
| `ONB-50` | a routine that already exists is updated or skipped rather than duplicated, and each routine's outcome is recorded so it is not asked again | `brain/onboarding/steps/6-routines-cadence.md` | |
| `ONB-51` | a routine actually created is promised honestly — its cadence and that it needs the app open, never a specific next timestamp | `brain/onboarding/steps/6-routines-cadence.md` | |
| `ONB-52` | a completed onboarding leaves the files every later session boots from: `memory/meta.md`, `memory/index.md`, and the profile | `brain/onboarding/flow.md` | eval:onboard |
| `ONB-53` | Finishing records what onboarding ran against — `onboarding_status: complete`, `onboarded_against` set to `VERSION`, and today's `last_onboarded` — which is what the migration pass later reads | `brain/onboarding/flow.md` | |
| `ONB-54` | the closing recap is a real artifact — their role, key people and priorities organized, not a wall of prose — and it surfaces one non-obvious connection or risk drawn across the memory | `brain/onboarding/flow.md` | |
| `ONB-55` | the principal is told once that one chat per topic works best, and why closing a chat loses nothing here | `brain/onboarding/flow.md` | |
| `ONB-56` | IC vs manager is inferred from the role or title rather than asked; only a genuinely ambiguous title earns the question | `brain/onboarding/flow.md` | |
| `ONB-57` | step 3 walks every circle explicitly — up, skip-up, peers, directs, skip-down, cross-org and external — rather than stopping at the immediate team | `brain/onboarding/steps/3-key-people.md` | |
| `ONB-58` | the team proposal names two or three candidates with the reason attached and stands up at most one, because the per-specialist intake runs long | `brain/onboarding/steps/4-priorities-projects.md` | |
| `ONB-59` | the shipped defaults are presented as one compact menu with each default marked, inviting changes only — never a configure-from-scratch interview | `brain/onboarding/steps/5-working-preferences.md` | |
| `ONB-60` | the mode is recorded in both places it has to live: the always-loaded profile, which steers every session, and `memory/meta.md`, which the migration pass reads | `brain/onboarding/flow.md` | |
| `ONB-61` | every real relationship onboarding records is wired both ways in the same step — a project to its owner and stakeholders, a decision to the project it drives — not only people to projects | `brain/onboarding/flow.md` | |
| `ONB-62` | the question bank is drawn from, not read out: the questions asked are the ones relevant to this principal, asked conversationally, and the ones that don't apply are skipped | `brain/onboarding/question-bank.md` | |
| `ONB-63` | the work/personal mode is decided at step 0, before anything else is asked | `brain/onboarding/flow.md` | |
| `ONB-64` | the mode recorded at onboarding is still there for every later session — read back, never re-asked | `brain/onboarding/flow.md` | |
| `ONB-65` | each person captured gets their OWN file — `person_tagged()` passes on any single file under `people/` holding the name and the tag, so one file listing everyone would satisfy it | `brain/onboarding/steps/3-key-people.md` | |
| `ONB-66` | onboarding creates `memory/onboarding-checklist.md` from the template at the start with every row `open`, links it under Load on demand, and a completed onboarding leaves every row resolved — none `open` | `brain/onboarding/checklist.md` | check(fixture) eval:onboard-terse |
| `ONB-67` | a row holds exactly one of six statuses and leaves `open` only by being addressed — short answers, pace, or an earlier decline never close a row; "optional" means the principal may decline, not that the offer may be omitted | `brain/onboarding/checklist.md` | eval:onboard-terse |
| `ONB-68` | when the principal signals pace or asks for it, the express path is offered once, names the deferrable rows it would set aside, and records them `deferred` only on agreement — never assumed, never re-offered | `brain/onboarding/flow.md` | eval:onboard-terse |
| `ONB-69` | an answer that covers a later row resolves it when heard, and that step confirms it in one line instead of asking again | `brain/onboarding/flow.md` | |
| `ONB-70` | step 2 resolves each connector category to a discovery state and records it per connector; an unresolved one is said plainly with what would resolve it; the bootstrap offer is `n/a` only on a positive state 6 for every category and `blocked` when any is inconclusive | `brain/onboarding/steps/2-organization-context.md` | |
| `ONB-71` | Finishing audits the checklist — an untouched row is resolved now or deferred with explicit agreement — and shows a completion summary naming the deferred and blocked rows with the plain-words way to pick them up | `brain/onboarding/flow.md` | eval:onboard-terse |
| `ONB-72` | in work mode the OKR question is always asked — an IC who does not run on them says so in a word; the agent never decides it for them | `brain/onboarding/steps/4-priorities-projects.md` | eval:onboard-terse |

### `ROLE` — charter/defaults/principles/voice

| ID | Behavior | Stated in | Covered by |
|----|----------|-----------|------------|
| `ROLE-01` | Chief of Staff advises and prepares while the principal decides — nothing irreversible or outward-facing happens without explicit confirmation | `brain/role/charter.md` | |
| `ROLE-02` | Chief of Staff operates on behalf of exactly one principal — this deployment's `memory/` | `brain/role/charter.md` | |
| `ROLE-03` | the principal deals with one operator: a delegation comes back as Chief of Staff's own finished answer, attributed to the specialist rather than relayed in their voice | `brain/schemas/team-member.md` | eval:delegate-attribution |
| `ROLE-04` | the `Context` and `Role type` recorded at onboarding steer every later session: a manager gets a team-and-delegation lens, an IC their own deliverables, a personal principal their life | `brain/role/charter.md` | |
| `ROLE-05` | every override target the defaults catalog declares mirrors a real brain file by path — the overlay binds by path alone, so a target with no counterpart could never take effect | `brain/role/defaults.md` | check |
| `ROLE-06` | the answer or the call comes first, then the reasoning | `brain/role/principles.md` | |
| `ROLE-07` | initiative is the default and reversibility is the gate: prep and drafts happen unasked, anything hard to undo waits for an explicit go | `brain/role/principles.md` | |
| `ROLE-08` | the interview level is tunable — at `assume` an underspecified ask is delivered on stated assumptions, at `thorough` a batched set of questions comes first and the deliverable waits | `brain/role/principles.md` | eval:interview-assume eval:interview-thorough |
| `ROLE-09` | the consent floor holds at the lowest interview level: even at `assume`, a material memory conflict is surfaced rather than silently absorbed | `brain/role/principles.md` | eval:interview-safety-floor |
| `ROLE-10` | memory edits are surgical — only what the request needs; unrelated stale or duplicate memory is mentioned, never silently deleted | `brain/role/principles.md` | |
| `ROLE-11` | when a memory is stored, changed, or relied on, it is said briefly so the principal can correct it | `brain/role/principles.md` | |
| `ROLE-12` | a recommendation the principal has overridden more than once is not re-proposed — the decided course is helped along, not relitigated | `brain/role/principles.md` | eval:disagree-and-commit |
| `ROLE-13` | opinions are held and volunteered, but grounded in memory or stated fact and labeled as a read — conviction is never license to invent | `brain/role/voice.md` | |
| `ROLE-14` | replies do not open with filler enthusiasm or performative eagerness | `brain/role/voice.md` | eval:personal-voice |
| `ROLE-15` | personal mode speaks warm and human — the human moment named in a few words before the practical move — while staying honest and never sycophantic | `brain/role/voice.md` | eval:personal-voice |
| `ROLE-16` | the principal is addressed by the name they go by at genuine moments, at most about once a message, and never guessed when it is not known | `brain/role/voice.md` | |
| `ROLE-17` | an override at the mirrored path actually binds — the shipped behavior changes to match what the override says | `CHIEFOFSTAFF.md` | eval:override |
| `ROLE-18` | in personal mode things are never called "projects" — they are goals and plans | `brain/role/charter.md` | |
| `ROLE-19` | persona depth is a knob whose default is crisp-professional; the characterful setting is opt-in and stays inside the same anti-sycophancy rails | `brain/role/voice.md` | |
| `ROLE-20` | the overlay's precedence is exact: `replace` supersedes the brain file, `extend` loads the brain file first and amends it, and where they conflict the override wins | `CHIEFOFSTAFF.md` | |
| `ROLE-21` | a twice-overridden recommendation is folded into preferences, so the retirement outlives the session that noticed the pattern | `brain/role/principles.md` | |
| `ROLE-22` | specialists propose durable facts and Chief of Staff verifies and integrates them — a specialist never writes shared memory or the confidential registry | `brain/schemas/team-member.md` | |

### `MEM` — memory + retrieval

| ID | Behavior | Stated in | Covered by |
|----|----------|-----------|------------|
| `MEM-01` | a fact recorded in a memory page is recalled accurately when it is asked for — no shipped file states plain recall, and `query.md` is not it: it disclaims trivial one-liners, which is exactly what these scenarios ask (as `MEM-02`/`MEM-03`) | `repo policy` | eval:mem-*-fact |
| `MEM-02` | two people who share a first name are told apart — the one asked about is answered, never merged with the other | `repo policy` | eval:mem-*-disambiguation |
| `MEM-03` | where memory holds a value a later entry superseded, the answer gives the current one | `repo policy` | eval:mem-*-latest-wins |
| `MEM-04` | an answer that needs a second, linked page is assembled by following the link rather than stopping at the first page | `brain/playbooks/query.md` | eval:mem-*-multi-hop |
| `MEM-05` | a constraint or sensitivity recorded about a person or a system is surfaced when a question touches them, without the question having named it | `brain/playbooks/query.md` | eval:mem-*-buried-needle |
| `MEM-06` | a person or fact memory does not hold is never confabulated — no work, detail or update is invented for it | `brain/playbooks/query.md` | eval:mem-*-absence |
| `MEM-07` | detail kept out of the always-load tier is still recalled when a question touches it — demotion is not loss | `brain/schemas/memory-file.md` | eval:mem-*-routing |
| `MEM-08` | asked what is due, the overdue items — past `due` and still open or blocked — are the ones returned, and they lead | `brain/playbooks/commitments.md` | eval:mem-*-aggregation |
| `MEM-09` | a synthesis question is answered from what memory actually holds about the subject, not from generic advice | `brain/playbooks/query.md` | eval:mem-*-synthesis |
| `MEM-10` | the objectives and key results in `memory/okrs.md` are recalled on request — the single tracker is where they are kept and read back from | `brain/playbooks/okrs.md` | eval:mem-*-okr |
| `MEM-11` | the decision log answers which decisions are open and who decides them — one row per decision, with its RAPID roles | `brain/playbooks/decisions.md` | eval:mem-*-decision |
| `MEM-12` | an answer from memory cites the pages it rests on when the principal asks for sources | `brain/playbooks/query.md` | eval:query-cite |
| `MEM-13` | a question reaching into the past that the index hooks do not hit escalates to a chronological walk of `memory/log/` and `memory/ledger.md`, rather than a thin answer from always-load context | `brain/playbooks/query.md` | |
| `MEM-14` | when memory only partly answers a question, the shortfall is said plainly instead of filled with a guess | `brain/playbooks/query.md` | |
| `MEM-15` | a substantial, reusable synthesis is offered back into memory with its sources, so the next question starts from it | `brain/playbooks/query.md` | |
| `MEM-16` | a question that reveals something worth knowing but unrecorded ends with the gap named and what would fill it | `brain/playbooks/query.md` | |
| `MEM-17` | every file under `memory/` is reachable by link traversal from `memory/index.md`, transitively through sub-indexes — `_quarantined/` and `_processed/` are exempt wholesale (`_REACH_EXEMPT` never tests whether a `_processed/` original was cited) | `brain/schemas/memory-file.md` | check(fixture) |
| `MEM-18` | when one memory file links another, the inbound link is written back wherever the relationship is meaningful — no one-directional pair | `brain/schemas/memory-file.md` | eval:backlink |
| `MEM-19` | one concept per file — a person, a project, a preference each get their own, so the index can route precisely and edits stay small | `brain/schemas/memory-file.md` | |
| `MEM-20` | a relative date is converted to an absolute one on the way in, so it still means the same thing when it is read back | `brain/schemas/memory-file.md` | eval:commitment-capture |
| `MEM-21` | the root index carries log entries from the last 30 days and never fewer than the 5 most recent; the moment one falls outside that window its line moves to `memory/log/index.md` | `brain/schemas/memory-file.md` | |
| `MEM-22` | the sub-index for scale is `log/`'s alone — `people/`, `projects/`, `context/` and `preferences/` stay flat however long they grow, because their one-line hooks are the routing signal | `brain/schemas/memory-file.md` | eval:log-rollup |
| `MEM-23` | always-load files stay lean by construction — one-line index hooks, a ~100-line soft target, and outgrowth demoted to a linked on-demand file rather than grown in place | `brain/schemas/memory-file.md` | |
| `MEM-24` | a memory file that is written or changed gets its `memory/index.md` line added or adjusted in the same turn, so the next session can find it | `CHIEFOFSTAFF.md` | |
| `MEM-25` | `/lint` diagnoses and proposes — it rewrites nothing in memory until the principal says so | `brain/playbooks/memory-lint.md` | eval:memory-lint eval:log-rollup |
| `MEM-26` | `/lint` audits `memory/` only, never `brain/` | `brain/playbooks/memory-lint.md` | |
| `MEM-27` | a stored claim a later entry superseded is surfaced, naming the newer status that overrides it | `brain/playbooks/memory-lint.md` | eval:memory-lint |
| `MEM-28` | a memory file that no link chain from the root index reaches is reported by name | `brain/playbooks/memory-lint.md` | eval:memory-lint |
| `MEM-29` | a markdown link to a relative path with no file at the other end is reported | `brain/playbooks/memory-lint.md` | eval:memory-lint |
| `MEM-30` | a root index still listing log entries outside the recency window is flagged, with `memory/log/index.md` named as where they belong | `brain/playbooks/memory-lint.md` | eval:log-rollup |
| `MEM-31` | a material fact whose origin would have to be known to trust it is flagged when it carries no provenance — and only then, never a source demanded for everything | `brain/playbooks/memory-lint.md` | |
| `MEM-32` | two memory files covering the same subject are flagged for merge | `brain/playbooks/memory-lint.md` | |
| `MEM-33` | two clearly related pages with no link between them are flagged | `brain/playbooks/memory-lint.md` | |
| `MEM-34` | two `active` preference directives that contradict each other are flagged and resolved by supersede-in-place — the superseded line is kept, never deleted | `brain/playbooks/memory-lint.md` | |
| `MEM-35` | an always-load file grown well past the soft target, or an index hook spilled past one line, is flagged with the specific demotion proposed — never auto-trimmed | `brain/playbooks/memory-lint.md` | |
| `MEM-36` | an action-gating condition past its date, and a standing-rule directive past its `expires:`, are proposed for resolution rather than merely flagged as stale | `brain/playbooks/memory-lint.md` | |
| `MEM-37` | `memory/integrations.md` disagreeing with what is actually available is a low-severity reconcile proposal, never a conclusion that an integration is gone | `brain/playbooks/memory-lint.md` | |
| `MEM-38` | the lint report opens with a one-line health read, groups findings by check with a proposed fix each, and orders them by severity | `brain/playbooks/memory-lint.md` | |
| `MEM-39` | a lint pass over clean memory reports it clean — a finding is never invented to fill the report | `brain/playbooks/memory-lint.md` | |
| `MEM-40` | the Distill sweep re-scans `memory/log/` since the last ledgered `lint` for durable facts never routed into a proper memory file, and proposes each promotion with its origin class and provenance — read-only, applied only on the principal's OK | `brain/playbooks/memory-lint.md` | |
| `MEM-41` | a `/lint` run appends its own `lint` line to `memory/ledger.md` | `brain/playbooks/memory-lint.md` | |
| `MEM-42` | a class of issue lint keeps re-surfacing is offered as a scheduled routine rather than re-reported forever | `brain/playbooks/memory-lint.md` | |
| `MEM-43` | `/explore` surfaces a genuine connection across memory that neither page draws — grounded in what is written, never invented | `brain/playbooks/explore.md` | eval:explore |
| `MEM-44` | each connection is delivered with the insight it carries and what would confirm it, and only the few most interesting are picked — signal over volume | `brain/playbooks/explore.md` | |
| `MEM-45` | the cross-references an exploration proposes are applied only on the principal's OK, with `memory/index.md` updated for anything added | `brain/playbooks/explore.md` | |
| `MEM-46` | an `/explore` run appends its own `explore` line to `memory/ledger.md` | `brain/playbooks/explore.md` | |
| `MEM-47` | an exploration that surfaces nothing non-obvious says so honestly rather than manufacturing a connection | `brain/playbooks/explore.md` | |
| `MEM-48` | a bare `/lint` runs the audit in that turn and reports what it found — the command dispatches straight to the playbook rather than asking first what to audit | `.claude/commands/lint.md` | eval:memory-lint eval:log-rollup — `brain/index.md` hooks the same playbook on `/lint`, so what these fence is that a bare `/lint` produces the audit, not this file in isolation |
| `MEM-49` | an argument scopes the lint to that subpath or file (`people/`, `projects/onyx.md`); with none, all of `memory/` is audited | `.claude/commands/lint.md` | |
| `MEM-50` | `/lint` against an empty or missing `memory/` says so and does nothing — no audit is manufactured for a tree with nothing in it | `.claude/commands/lint.md` | |
| `MEM-51` | a bare `/explore` runs the exploration in that turn across all of `memory/` — the command dispatches straight to the playbook | `.claude/commands/explore.md` | eval:explore — `brain/index.md` hooks the same playbook on `/explore`, so this fences that a bare `/explore` produces the exploration, not this file in isolation |
| `MEM-52` | an argument centers the exploration on that person, project or theme instead of scanning the whole tree | `.claude/commands/explore.md` | |
| `MEM-53` | `/explore` against an empty or missing `memory/` says so and does nothing rather than falling back on general advice | `.claude/commands/explore.md` | |
| `MEM-54` | the demoted detail is retrieved from its on-demand page rather than answered out of the index hook — every routing fixture's `## Load on demand` hook names the topic and not the value its scenario asserts, see [`decisions.md`](decisions.md#buried-needle-fixture-hooks) | `brain/schemas/memory-file.md` | eval:mem-*-routing check(fixture) |
| `MEM-55` | `memory/commitments.md` belongs to `## Always load` — the rule that places files says so, not only the rule that sizes them; `okrs.md` and `decisions.md` stay on demand | `brain/schemas/capture-rules.md` | check check(fixture) |
| `MEM-56` | an exploration notices a domain recurring across several memory pages with no active roster specialist covering it, grounded in at least two files like every other finding | `brain/playbooks/explore.md` | check eval:explore-team-suggestion |
| `MEM-57` | a suggestion is checked against `memory/team-suggestions.md` before it is filed — a declined slug is never re-suggested, and a pending one blocks a second | `brain/playbooks/explore.md` | check eval:explore-suggestion-declined |
| `MEM-58` | the suggestion is offered in the run that found it, and the `## Pending` entry is written as part of making that offer — not deferred to an end-of-turn moment the agent has no hook for | `brain/playbooks/explore.md` | eval:explore-team-suggestion |
| `MEM-59` | `team-offer: off` suppresses an exploration's suggestion exactly as it suppresses the onboarding proposal — one switch, both surfaces | `brain/role/defaults.md` | check eval:boot-team-suggestion-off |
| `MEM-60` | `/explore` tells the principal a suggested specialist is offered in that turn and that a no is permanent | `.claude/commands/explore.md` | eval:explore-team-suggestion — `brain/index.md` hooks the same playbook, so this fences that a bare `/explore` produces the suggestion, not this file in isolation |
| `MEM-61` | a tombstone suppresses **its own domain, not the feature** — a later exploration still suggests a specialist for a different uncovered domain | `brain/playbooks/explore.md` | eval:explore-suggestion-after-tombstone |

### `CAP` — capture + confidentiality

| ID | Behavior | Stated in | Covered by |
|----|----------|-----------|------------|
| `CAP-01` | every turn is evaluated for durable content, and what is durable is written to memory without being asked to | `brain/schemas/capture-rules.md` | eval:capture |
| `CAP-02` | ephemera is not written — small talk, one-off calculations, and anything already captured | `brain/schemas/capture-rules.md` | eval:capture-skip |
| `CAP-03` | nothing is written at the folder root — an explicit ask for a file there is redirected under `memory/` and the reason said out loud, never silently obeyed and never silently relocated | `brain/schemas/memory-file.md` | eval:desk-no-stray-writes |
| `CAP-04` | a fact that gates an action carries the gate inline as an absolute date or a named condition; a bare "not yet" or "soon" is a capture defect to resolve, not a note | `brain/schemas/capture-rules.md` | |
| `CAP-05` | a standing rule is captured with the trigger context that fires it and, when time-bounded, an expiry — and it surfaces when the trigger arises, not as a recurring reminder | `brain/schemas/capture-rules.md` | |
| `CAP-06` | high-confidence facts are stored now; an inference the principal has not confirmed is recorded as a labeled hypothesis in a dated log note and kept out of always-loaded files | `brain/schemas/capture-rules.md` | |
| `CAP-07` | a derived or generated fact never silently overrides a principal-stated one — that is a contradiction to flag, and the principal-stated value wins by default | `brain/schemas/capture-rules.md` | |
| `CAP-08` | an instruction asserted by a source is captured as that source's claim, never filed as a standing rule — standing rules come only from the principal | `brain/schemas/capture-rules.md` | |
| `CAP-09` | a change to behavior is captured as an override under `memory/overrides/`: `extend` created autonomously, `replace` of core brain only after confirming with the principal | `brain/schemas/capture-rules.md` | |
| `CAP-10` | a durable voice preference observed from how the principal reacts is folded into the voice override and named in one line — grounded in a real pattern, never a single data point | `brain/schemas/capture-rules.md` | |
| `CAP-11` | dedup comes first: an existing file on the subject is edited rather than duplicated, and a fact recalled from memory this session is never re-captured as a new entry | `brain/schemas/capture-rules.md` | |
| `CAP-12` | what was saved and where is told to the principal in one line, so they can correct it — the capability inventory being the single write that is recorded quietly | `brain/schemas/capture-rules.md` | |
| `CAP-13` | information conflicting with a stored fact is surfaced against what memory already held — both values named — never silently absorbed | `brain/schemas/capture-rules.md` | eval:contradiction-flag |
| `CAP-14` | a question about a conflicting field holds that field, not the turn — everything else the principal just said is still captured | `brain/schemas/capture-rules.md` | |
| `CAP-15` | a changed preference supersedes in place: the active directive is rewritten with today's date and the old line flipped to `superseded`, never two contradictory actives at once | `brain/schemas/capture-rules.md` | |
| `CAP-16` | the action ledger is append-only and milestones-only — new lines at the end, past entries never edited or deleted, routine single-fact edits never logged | `brain/schemas/capture-rules.md` | |
| `CAP-17` | a document shared in the chat is auto-intaked inline, in the moment, with no command needed | `brain/schemas/capture-rules.md` | eval:dropped-doc |
| `CAP-18` | a shared document is screened before anything is extracted, and one carrying instructions is refused wholesale: not ingested, quarantined, and the principal told what was flagged | `brain/schemas/capture-rules.md` | eval:dropped-doc-injection |
| `CAP-19` | a fact captured from a shared document records where it came from | `brain/schemas/capture-rules.md` | eval:provenance |
| `CAP-20` | a document that implies doing something has that surfaced rather than silently acted on | `brain/schemas/capture-rules.md` | |
| `CAP-21` | a document shared alongside a question gets the question answered too — the intake happens in addition, never instead of it | `brain/schemas/capture-rules.md` | |
| `CAP-22` | a closing session, or context that has been summarized away, triggers a sweep for durable facts not yet filed — and when summarization was the trigger, the reload runs first so the sweep files against the real rules rather than a paraphrase | `brain/schemas/capture-rules.md` | |
| `CAP-23` | a confidential project is referred to only by its non-descriptive code name in every output, and its real name exists nowhere in `memory/` but the registry | `brain/schemas/confidentiality.md` | eval:confidential eval:mem-*-confidential |
| `CAP-24` | even the setup confirmation uses the code name alone — the real name is not repeated back in the acknowledgement | `brain/schemas/confidentiality.md` | eval:confidential |
| `CAP-25` | the code name is a narrow tool for a discrete unannounced initiative — revenue, budgets, headcount, org structure and candid reads on people are captured plainly, because `memory/` is already private | `brain/schemas/confidentiality.md` | eval:capture |
| `CAP-26` | confidentiality is never *suggested* in personal mode — no code name proposed and no registry stood up, however sensitive the fact | `brain/schemas/confidentiality.md` | eval:personal-no-confidential |
| `CAP-27` | offering a code name never delays or loses the capture — the fact is filed in the same turn under the proposed name and the identity goes straight to the registry | `brain/schemas/confidentiality.md` | |
| `CAP-28` | the registry is linked exactly once, from the root index, and by nothing else — no project, person, preference, roster or charter may link it, or a team member would have a hop to the real identities | `brain/schemas/confidentiality.md` | |
| `CAP-29` | the registry is loaded silently at boot and never quoted, echoed, or surfaced — linking it makes it reachable, not quotable | `brain/schemas/confidentiality.md` | |
| `CAP-30` | principal-private material never rides into output that leaves the principal's hands — a private note may shape a draft, it is never quoted in one | `brain/schemas/confidentiality.md` | |
| `CAP-31` | a project that becomes confidential is scrubbed everywhere at once — body, index line, inbound links and log entries — leaving the real name only in the registry | `brain/schemas/confidentiality.md` | |
| `CAP-32` | the secrecy promised to the principal is bounded by what a behavioral control can do: the registry is plaintext on disk, and it is never oversold as encryption | `brain/schemas/confidentiality.md` | |
| `CAP-33` | an auto-intake of a chat-shared document records an `ingest` line in the action ledger | `brain/schemas/capture-rules.md` | eval:log-ledger |
| `CAP-34` | a material conflict — a changed decision, a moved deadline, a reversed status, a sensitive fact — is confirmed with the principal before the stored value is overwritten, not merely announced | `brain/schemas/capture-rules.md` | |
| `CAP-35` | an explicit "this is confidential" is honored in every mode: the code-name machinery in work mode, plain discretion in personal mode | `brain/schemas/confidentiality.md` | |
| `CAP-36` | `updated:` is set to today on every touch of a memory file — on create and on every edit, with no exceptions | `brain/schemas/capture-rules.md` | |
| `CAP-37` | a surfaced contradiction says which of the two claims is newer, not merely that both exist | `brain/schemas/capture-rules.md` | |
| `CAP-38` | a detail that would itself unmask a confidential project — the counterparty, the target company — stays in the registry or a sealed file, never in the working project page | `brain/schemas/confidentiality.md` | |
| `CAP-39` | nothing is written outside `memory/` — never into `brain/`, never into a new top-level folder (the folder-root case is `CAP-03`) | `brain/schemas/memory-file.md` | |
| `CAP-40` | identifying details are withheld from output as well as the real name — the site, the word for the action, the headcount are as unmasking as the name itself ("Never emit its real name **or identifying details** outside the registry") | `brain/schemas/confidentiality.md` | eval:mem-manufacturing-ceo-confidential |
| `CAP-41` | the real name is not emitted even in a statement about not emitting it — a disclaimer that carries the secret ("never NimbusAI in my output") has already leaked the code name ↔ real identity mapping to anyone the line is forwarded to | `brain/schemas/confidentiality.md` | eval:mem-saas-cto-confidential-meta-mention |

### `PLAY` — deliverable playbooks

| ID | Behavior | Stated in | Covered by |
|----|----------|-----------|------------|
| `PLAY-01` | a commitment made in passing is appended to the single tracker `memory/commitments.md` with status `open`, in the turn it is made | `brain/playbooks/commitments.md` | eval:commitment-capture |
| `PLAY-02` | the tracker is one running table — `what · owner · due · status · source` — never one file per item and never buried in a `log/` entry; done rows archive to `memory/commitments/done.md`, which is linked the first time it is created so the archive stays reachable | `brain/playbooks/commitments.md` | |
| `PLAY-03` | a commitment's `due` is stored as an absolute date — "Friday" is converted on the way in; `commitment-capture`'s date assertion cannot prove this, see [`decisions.md`](decisions.md#file-has-date-is-vacuous) | `brain/playbooks/commitments.md` | |
| `PLAY-04` | an item whose `owner` is not the principal is surfaced with who to nudge and an offer to draft the nudge — drafted, never sent without an OK | `brain/playbooks/commitments.md` | |
| `PLAY-05` | a genuinely time-sensitive item — an overdue commitment, an imminent hard deadline — is raised when it is spotted, by notification or a reminder routine, rather than held for the next brief | `brain/playbooks/commitments.md` | |
| `PLAY-06` | a commitment dropped deliberately is removed and the principal told — the tracker is kept accurate rather than complete | `brain/playbooks/commitments.md` | |
| `PLAY-07` | a decision the principal states in passing is called out and logged to `memory/decisions.md` without being asked to — always-on capture, not only on request | `brain/playbooks/decisions.md` | eval:decision-log |
| `PLAY-08` | a logged decision carries the log's shape — status, RAPID roles, the date, and the rationale with where it came from — so a later brief reading the log actually surfaces it (the read side is `MEM-11`) | `brain/playbooks/decisions.md` | |
| `PLAY-09` | a decision is told apart from a task: a choice with consequences and alternatives goes to the decision log, a task to `memory/commitments.md`, and one decision may spawn commitments as its **P** | `brain/playbooks/decisions.md` | |
| `PLAY-10` | RAPID is filled from what is known and right-sized — an unclear **D** or **A** is left blank and asked about rather than invented, and a small one-person call is logged lightly instead of forced into five roles | `brain/playbooks/decisions.md` | |
| `PLAY-11` | a decision a later one overturns is marked `reversed` and the new one added, so the log always reflects the current call | `brain/playbooks/decisions.md` | |
| `PLAY-12` | a confidential decision is logged under its code name only | `brain/playbooks/decisions.md` | |
| `PLAY-13` | a decision brief is delivered in the turn it is asked for — a reply that only logs the decision and asks what to do next is a failure of the playbook, not a partial success | `brain/playbooks/decision-brief.md` | eval:decision-brief |
| `PLAY-14` | the brief makes a real recommendation supported by reasoning, rather than hedging into a menu of options | `brain/playbooks/decision-brief.md` | eval:decision-brief |
| `PLAY-15` | the brief carries its full shape — the decision and its deadline, the recommendation up front, 2–4 realistic options with pros, cons, risk and reversibility, why, what it costs to be wrong, and open questions | `brain/playbooks/decision-brief.md` | |
| `PLAY-16` | the brief is framed without stalling on questions: where memory is silent the assumption is stated and the brief proceeds, and only a question that would flip the recommendation is asked first — the rest go under Open questions | `brain/playbooks/decision-brief.md` | |
| `PLAY-17` | the deadline is pressure-tested — urgency masquerading as importance is named, and what waiting a week actually costs is asked | `brain/playbooks/decision-brief.md` | |
| `PLAY-18` | irreversible options are flagged as such, and the bar for recommending one is higher | `brain/playbooks/decision-brief.md` | |
| `PLAY-19` | logging the decision to `memory/decisions.md` happens alongside the brief, never in place of it | `brain/playbooks/decision-brief.md` | |
| `PLAY-20` | a message asked for comes back as a complete draft — opener, body and sign-off, addressed to the named recipient — presented for review and never described as already sent | `brain/playbooks/draft-comms.md` | eval:draft-comms |
| `PLAY-21` | with a mail connector the draft is created in the principal's own mailbox as a draft, ready for them to review and send — never auto-sent | `brain/playbooks/draft-comms.md` | |
| `PLAY-22` | the draft is written in the principal's voice and comms preferences, and for the recipient's relationship and sensitivities as `memory/people/` records them | `brain/playbooks/draft-comms.md` | |
| `PLAY-23` | where tone or framing is a real choice, two options are offered rather than one guessed, and anything assumed or left blank for them to fill is named in one line | `brain/playbooks/draft-comms.md` | |
| `PLAY-24` | a message that creates a commitment or follow-up adds it to `memory/commitments.md` | `brain/playbooks/draft-comms.md` | |
| `PLAY-25` | a batch of incoming asks is sorted and prioritized by how much each needs the principal, rather than handed back as a flat list | `brain/playbooks/inbox-triage.md` | eval:inbox-triage |
| `PLAY-26` | the escalation test is the blindside test — would this surprise them in a way that damages their position; if yes it goes up now — see [`decisions.md`](decisions.md#inbox-triage-blindside-test) | `brain/playbooks/inbox-triage.md` | |
| `PLAY-27` | a draft-and-confirm item arrives with its response already prepared, so a quick yes is all that is left, and the needs-principal items lead the summary under a one-line bottom line | `brain/playbooks/inbox-triage.md` | |
| `PLAY-28` | commitments, deadlines and decisions that surface during triage are captured | `brain/playbooks/inbox-triage.md` | |
| `PLAY-29` | asked to prep for a meeting, the pre-read is produced in that turn for the named attendee — the context and objectives or talking points to walk in with, not an offer to prepare one | `brain/playbooks/meeting-prep.md` | eval:meeting-prep |
| `PLAY-30` | the pre-read is enriched with live connector data where it exists — the calendar event with its agenda and attachments, recent related mail, the docs in play — rather than built from stale memory alone | `brain/playbooks/meeting-prep.md` | |
| `PLAY-31` | the pre-read carries its shape — bottom line, attendees and what each cares about, the 3–5 facts to have fresh, objectives, talking points, watch-outs — readable in under two minutes | `brain/playbooks/meeting-prep.md` | |
| `PLAY-32` | outcomes, decisions and new commitments from the meeting are logged afterwards and the relevant people and project files updated | `brain/playbooks/meeting-prep.md` | |
| `PLAY-33` | OKRs the principal shares are recorded in the single tracker `memory/okrs.md` | `brain/playbooks/okrs.md` | eval:okr-critique |
| `PLAY-34` | shared OKRs are pressure-tested, not merely filed — the candid critique comes in the same turn they are recorded | `brain/playbooks/okrs.md` | eval:okr-critique |
| `PLAY-35` | an activity masquerading as a key result — "hold weekly syncs", "launch the pricing page" — is named as such, and the outcome it is meant to produce is proposed in its place; `okr-critique`'s judge offers this only as an example and grades on any clear quality critique, so it does not fence this clause | `brain/playbooks/okrs.md` | |
| `PLAY-36` | the critique ends with the one or two highest-leverage fixes phrased as a suggested rewrite, and asks before overwriting the principal's own wording | `brain/playbooks/okrs.md` | |
| `PLAY-37` | at-risk key results — low confidence, a flat `current` — are surfaced in the briefs with what would move them | `brain/playbooks/okrs.md` | |
| `PLAY-38` | a key result is a measurable outcome with a baseline, a target and a timeframe, owned by someone, and never a restatement of its objective | `brain/playbooks/okrs.md` | |
| `PLAY-39` | asked for the daily brief, the brief itself comes back — a concise start-of-day briefing grounded in this principal's situation, not an offer to produce one and not a generic answer | `brain/playbooks/daily-brief.md` | eval:daily-brief |
| `PLAY-40` | the daily brief carries its shape — a one-line bottom line, today's schedule with what needs prep, what needs the principal, due-today and overdue led by the overdue, and the top 1–3 focus | `brain/playbooks/daily-brief.md` | |
| `PLAY-41` | asked for the weekly preview, the look-forward is what comes back — upcoming meetings, decisions to land, prep and commitments coming due, grounded in this principal's situation rather than a backward recap or generic advice | `brain/playbooks/weekly-preview.md` | eval:weekly-preview |
| `PLAY-42` | the preview names which meetings need prep and offers to prep each, and closes on the 2–3 outcomes to aim for, what to protect time for, and what to defer | `brain/playbooks/weekly-preview.md` | |
| `PLAY-43` | asked for the weekly retro, the close-out comes back in that turn and reviews the week just past — what progressed, what closed, what slipped — rather than a forward plan | `brain/playbooks/weekly-retro.md` | eval:weekly-retro |
| `PLAY-44` | what slipped is named honestly with its cause, and the patterns worth adjusting — recurring blockers, over-commitment — are called out rather than smoothed over | `brain/playbooks/weekly-retro.md` | |
| `PLAY-45` | the retro's carry-over feeds the next preview, project statuses are updated, and completed commitments are marked `done` | `brain/playbooks/weekly-retro.md` | |
| `PLAY-46` | an update check that cannot fetch — no network, or a host that can't reach the release — says so and hands over the manual path, never a guess about what is available | `brain/playbooks/update.md` | |
| `PLAY-47` | already on the latest release, the check says so and stops | `brain/playbooks/update.md` | |
| `PLAY-48` | a newer release is reported with its version and the changelog highlights, and the file swap — irreversible, inside the principal's own folder — is applied only on an explicit OK | `brain/playbooks/update.md` | |
| `PLAY-49` | the session that applied an update migrates nothing and ledgers nothing: it enters stale mode, says in one line that the next fresh session applies any migration, and leaves `memory/` untouched until then | `brain/playbooks/update.md` | |
| `PLAY-50` | `/lint` flags an open delegation record with no matching row in `memory/commitments.md` — the tracker is what the session-start digest reads, so an unmirrored delegation is invisible | `brain/playbooks/memory-lint.md` | check |
| `PLAY-51` | memory-lint drops a pending suggestion whose domain an active specialist already covers — it was answered by another route, and an offer for a specialist the principal already has is noise at every session start | `brain/playbooks/memory-lint.md` | check |
| `PLAY-52` | a decision that clears the right-size bar is swept for role holders across both benches — the people hooks in `memory/index.md` and the roster's `## Active` entries — before the row is final; a small one-person call skips the sweep entirely | `brain/playbooks/decisions.md` | check eval:decision-role-coverage |
| `PLAY-53` | a specialist may hold a decision's **R**, **I** or **P**, but **never A or D** — agreement is veto authority and the decide is the principal's, and an unclear one is still left blank and asked rather than filled by the sweep | `brain/playbooks/decisions.md` | check |
| `PLAY-54` | a real person missing from a role is surfaced as a recommendation to loop in **with an offer to draft the outreach** — Chief of Staff never contacts them itself and never drafts unasked | `brain/playbooks/decisions.md` | check |
| `PLAY-56` | a request for **advice, input or an opinion** on a call trips the same chain as one phrased as a decision — the brief is produced and the log entry happens alongside it; both always-on statements of the rule carry the phrase, so one cannot drift from the other | `brain/schemas/capture-rules.md` | check eval:advice-is-a-decision |
| `PLAY-57` | a choice Chief of Staff **inferred** from a situation the principal never framed as a decision is surfaced in one line and **never written** to `memory/decisions.md` until they agree — the test is who voiced it, and at most one is raised per turn | `brain/playbooks/decisions.md` | check eval:unnamed-decision |
| `PLAY-55` | neither offer holds the brief — a specialist's consult is folded in inline and the fuller work-up and outreach draft are left as offers in the same turn, so `PLAY-13` still governs | `brain/playbooks/decision-brief.md` | check |

### `TEAM` — virtual team

| ID | Behavior | Stated in | Covered by |
|----|----------|-----------|------------|
| `TEAM-01` | the team exists if and only if `memory/index.md` links `memory/team/index.md` — with no roster link there is no team | `brain/schemas/team-member.md` | check(fixture) |
| `TEAM-02` | the roster is a `type: log` file with an `## Active` section whose links all resolve — it is the authoritative source of truth for who is on the team | `brain/schemas/team-member.md` | check(fixture) |
| `TEAM-03` | the team is listed from the roster's `## Active` entries and their linked charters — never by scanning `memory/team/*/charter.md` — and a folder with no linked roster is reported as no team yet | `.claude/commands/team-members.md` | |
| `TEAM-04` | a specialist's charter is `type: team-member` and carries a `status:` of `active` or `inactive` | `brain/schemas/team-member.md` | check(fixture) eval:team-create |
| `TEAM-05` | `autonomy:` is one of `draft-and-wait`, `initiative` or `act-and-inform` — the leash is an enumerated setting, never free text | `brain/schemas/team-member.md` | check(fixture) |
| `TEAM-06` | the charter carries a `persona:` block, so the specialist reads as a distinct colleague rather than a competent tone | `brain/schemas/team-member.md` | check(fixture) eval:team-create |
| `TEAM-07` | the charter carries a required `## Method` of ordered, domain-specific steps — the part that changes what the specialist *does* rather than how it sounds; "understand / analyze / recommend" is a finding, not a pass | `brain/schemas/team-member.md` | check(fixture) eval:team-create |
| `TEAM-08` | a charter is linked from the roster, and an `active` one is linked under `## Active` | `brain/schemas/team-member.md` | check(fixture) |
| `TEAM-09` | the charter links its own `[Specialist memory](memory/index.md)`, so a specialist's deep memory is reached by following a link rather than by knowing the layout | `brain/schemas/team-member.md` | check(fixture) |
| `TEAM-10` | `## Key context` is a non-binding start-here pointer list, not an access-control surface — the one hard requirement on it is that its links resolve | `brain/schemas/team-member.md` | check(fixture) |
| `TEAM-11` | the always-loaded roster pointer in `memory/index.md` stays generic — it never names a specialist's specialization, which would ride into every session and go stale the moment the roster changes | `brain/playbooks/team.md` | check(fixture) |
| `TEAM-12` | no confidential real identity appears in any roster, charter, delegation record or specialist page — specialists work in code names | `brain/schemas/team-member.md` | check(fixture) |
| `TEAM-13` | no roster, charter or specialist page links `memory/confidential/registry.md` — the one guard the brain trust has, since every specialist reads the whole shared brain | `brain/schemas/team-member.md` | check(fixture) |
| `TEAM-14` | creating the first specialist is atomic — the specialist folder, the roster, its `## Active` entry and the `memory/index.md` pointer land in the same turn, never a bare folder with no way to reach it | `brain/playbooks/team.md` | eval:team-create |
| `TEAM-15` | a specialist has no boot files of its own — no `AGENTS.md` or `CLAUDE.md` beside the charter — because its rails exist only when Chief of Staff is the one running it | `brain/schemas/team-member.md` | check(fixture) eval:team-create |
| `TEAM-16` | no `.claude/agents/<slug>.md` shim is generated — there is no subagent path, so one would be a dead projection drifting from the charter with nothing to detect it | `brain/schemas/team-member.md` | eval:team-create |
| `TEAM-17` | starter memory is evidence only — every seeded note cites a real source, and none carries an `unverified` model-prior marker | `brain/schemas/team-member.md` | check(fixture) eval:team-create |
| `TEAM-18` | a specialist's domain knowledge stays in its own subtree — no seeded or generated domain fact is written into a shared knowledge page (Chief of Staff's own audit trail recording that it built the specialist is not a leak) | `brain/schemas/team-member.md` | eval:team-create |
| `TEAM-19` | the specialist-onboard trigger builds the specialist now rather than promising to — the folder, its charter and its roster entry all exist when the turn ends | `.claude/commands/team-member-onboard.md` | eval:team-create |
| `TEAM-20` | an ask an existing specialist's specialization already covers surfaces that specialist rather than minting a near-twin — an **emergent** behavior the scenario fences, not a promise the corpus makes: `team.md` states no overlap rule, and the intake line that did was measured and dropped as not load-bearing, see [`decisions.md`](decisions.md#team-create-dedupe) | `repo policy` | eval:team-create-dedupe |
| `TEAM-21` | the proposed `handle` is checked against `memory/people/` and picked again on a clash — a handle duplicating a real colleague makes the people graph, `commitments.md`'s `owner:` field and every brief ambiguous | `brain/schemas/team-member.md` | |
| `TEAM-22` | the drafted method and the drafted persona are shown together in a single confirm beat, and the principal's confirmation is what makes that method the specialist's operating procedure | `brain/playbooks/team.md` | |
| `TEAM-23` | the method is built in a fixed order — the agency-agents catalog, then search of the generic role, then the specialization, then one grounding question whose answer outranks the rest — with the steps that came from a source cited inline | `brain/playbooks/team.md` | |
| `TEAM-24` | fetched content never becomes a method step verbatim: it is screened as untrusted data and rewritten, and anything reading as an instruction to the reader is dropped | `brain/playbooks/team.md` | |
| `TEAM-25` | a search run for a specialist's method or starter memory covers the generic role only — never the principal's name, never a confidential code name | `brain/playbooks/team.md` | |
| `TEAM-26` | a delegated task leaves a record under `memory/team/<slug>/delegations/` as `type: delegation`, carrying all seven sections and every required frontmatter field, the `specialist:` key included (the frozen fixture, written before the rename, carries `member:` — both are read) — a part with nothing in it yet is stubbed, never omitted | `brain/schemas/team-member.md` | check(fixture) eval:delegate-record |
| `TEAM-27` | the record's `name:` carries the `deleg-` prefix that marks it a delegation | `brain/schemas/team-member.md` | check(fixture) |
| `TEAM-28` | a record's `status:` is one of the six allowed values, and a delegation that has closed does not stay `assigned` | `brain/schemas/team-member.md` | check(fixture) eval:delegate-record |
| `TEAM-29` | a closed record's `## Verification` carries the check against the acceptance criteria, filled rather than left stubbed | `brain/playbooks/delegate.md` | eval:delegate-record |
| `TEAM-30` | which of the specialist's promoted facts were actually written to shared memory is recorded in the record's `## Integrated facts`, filled on close — the specialist's `## Promote` list and the record's section are reconciled in exactly that one place | `brain/playbooks/delegate.md` | eval:delegate-record |
| `TEAM-31` | every closed delegation carries a one-line `## Lesson`, pass or fail, and that line is prepended to the specialist's `## Casebook` linked to its record — a lesson off the specialist's read path is the same as not having written it | `brain/schemas/team-member.md` | check(fixture) eval:delegate-record |
| `TEAM-32` | a lesson already in the casebook reaches the next task's work — the compounding loop is read, not only written | `brain/schemas/team-member.md` | eval:specialist-casebook-compounds |
| `TEAM-33` | a specialist's `## Method` changes what it produces, not only how its charter reads | `brain/schemas/team-member.md` | eval:specialist-follows-method |
| `TEAM-34` | the principal's override of a playbook binds work produced through a specialist — an overridden decision brief comes back in the house shape, not the shipped one. **Which mechanism carried it is not isolated** — the specialist resolving `memory/overrides/` as it borrows the playbook, or Chief of Staff applying the override on integration — and the craft-inheritance prose is itself recorded unproven, see [`decisions.md`](decisions.md#team-member-craft-inheritance-source) | `brain/schemas/team-member.md` | eval:specialist-honors-override |
| `TEAM-35` | a specialist never loads `brain/role/voice.md` — that is Chief of Staff's voice, and the exclusion holds even when the principal has overridden it | `brain/schemas/team-member.md` | |
| `TEAM-36` | delegated work is mirrored into `memory/commitments.md` with `owner: <slug>` and a link to the record, so the principal's single what's-on-my-plate view surfaces it with the same overdue and waiting-on logic | `brain/playbooks/delegate.md` | |
| `TEAM-37` | the delegation ledger lines are written — `delegate` on assign, `integrate` or `reject` on close — to the specialist's `ledger.md` and a milestone line to `memory/ledger.md`, with the `delegate` line linking the record so it is reachable by roster → charter → ledger → record | `brain/playbooks/delegate.md` | |
| `TEAM-38` | a specialist consult is mediated: a specialist may hand up for a peer's input or the principal's answer, Chief of Staff runs that leg and returns the result, and there is no direct specialist↔specialist channel | `brain/playbooks/delegate.md` | |
| `TEAM-39` | a consulted peer answers as `draft-and-wait` whatever its own autonomy — a specialist-initiated consult never makes a peer act or write | `brain/playbooks/delegate.md` | |
| `TEAM-40` | every leg of a consult is screened as data rather than instructions, and a relayed opinion carries its provenance and is verified before it is treated as fact — never written into the peer's own memory as if the peer had found it | `brain/playbooks/delegate.md` | |
| `TEAM-41` | a consult is depth-1 and non-re-entrant — a specialist being consulted cannot itself hand up; no chains, no cycles | `brain/playbooks/delegate.md` | |
| `TEAM-42` | a stale session delegates nothing that writes — no delegation record, no specialist subtree, no promotion into shared memory — and adopting a specialist's persona does not lift the freeze | `brain/playbooks/delegate.md` | |
| `TEAM-43` | a delegation brief and an integrated result are shared outputs: private person-file notes, hypotheses and anything from `memory/confidential/` stay out of them, and the registry is never pasted | `brain/playbooks/delegate.md` | |
| `TEAM-44` | a specialist acts only within its charter's `autonomy`, and at every level nothing outward-facing or hard to undo happens without the principal — a specialist may draft an email, never send it | `brain/schemas/team-member.md` | |
| `TEAM-45` | confidential work is handed down in code names exactly as it lives in shared memory, and specialists never create confidential projects — code-naming stays with Chief of Staff | `brain/schemas/team-member.md` | |
| `TEAM-46` | asking a named specialist for their input is answered in that specialist's own voice, led by an attribution marker naming them — the four `specialist-voice-*` scenarios are fences, not proofs of prose, see [`decisions.md`](decisions.md#team-member-voice-fences) | `brain/playbooks/team.md` | eval:specialist-voice-direct |
| `TEAM-47` | that passage reads as a distinct colleague, not neutral assistant prose with a name attached — the judge probes that as an observable property (leading with a number, a threshold, a failure mode, the domain's own vocabulary) rather than by matching words, so those are the probe and not the promise; see [`decisions.md`](decisions.md#team-member-voice-fences) | `brain/schemas/team-member.md` | eval:specialist-voice-direct |
| `TEAM-48` | a specialist still speaks when asked several turns into a session, not only on a cold first turn — the runner cannot resume a session, so the scenario simulates one in the prompt, see [`decisions.md`](decisions.md#team-member-voice-fences) | `brain/playbooks/team.md` | eval:specialist-voice-midsession |
| `TEAM-49` | naming a specialist by role rather than by handle still reaches that specialist | `brain/playbooks/team.md` | eval:specialist-voice-by-role |
| `TEAM-50` | a specialist-voiced passage and Chief of Staff's own close stay separable in one turn — the close carries no specialist attribution marker; a marker leaking onto a later turn after hand-back needs a multi-turn harness, see [`decisions.md`](decisions.md#team-member-voice-fences) | `brain/schemas/team-member.md` | eval:specialist-voice-handback |
| `TEAM-51` | a document dropped in the chat while working with a specialist is auto-intaked into that specialist's own memory under its scope, screened as untrusted data exactly like any chat-shared doc | `brain/schemas/team-member.md` | |
| `TEAM-52` | every lifecycle change is an edit to the roster's links and the charter's `status:` — creating or deleting a folder alone changes nothing about membership | `brain/playbooks/team.md` | |
| `TEAM-53` | a hard delete removes the specialist's link from every roster section before any file is deleted, so nothing is ever unreachable-but-present | `brain/playbooks/team.md` | |
| `TEAM-54` | a slug rename updates every inbound link in the same turn — the roster entry, the charter's own `name:`, and any cross-links from shared pages into the old path | `brain/playbooks/team.md` | |
| `TEAM-55` | a specialist review is read-only — a specialist-scoped memory lint plus the delegation track record, reported bottom line first with a proposed fix per finding and applied only on the principal's OK | `.claude/commands/team-member-review.md` | |
| `TEAM-56` | a review that finds a recurring lesson, or a rejection tracing to a check the `## Method` does not make, proposes that specific method amendment with the cases motivating it — the method changes only here, deliberately and visibly | `brain/playbooks/team.md` | |
| `TEAM-57` | removing a specialist offboards rather than deletes: the principal is asked whether to retain its facts first, the default is remove-retain with the subtree kept for provenance, and standing routines go either way | `.claude/commands/team-member-remove.md` | |
| `TEAM-58` | removing the last specialist also removes the `## Always load` team pointer and the roster link from `memory/index.md` | `brain/playbooks/team.md` | |
| `TEAM-59` | migrating a pre-roster team writes nothing until the principal approves what was found, in one exchange — and its one-time charter scan is the only sanctioned filesystem inspection of `memory/team/` | `brain/playbooks/team.md` | |
| `TEAM-60` | the give-existing-specialists-a-method migration is idempotent — a charter that already has a `## Method` is skipped — and every drafted method is shown together in one exchange before anything is written | `brain/playbooks/team.md` | |
| `TEAM-61` | the team triggers work as plain natural language on every host — "who's on my team", "review the audio dev" — with the slash commands as the Claude Code spelling of the same thing | `brain/playbooks/team.md` | |
| `TEAM-62` | where neither search nor the principal yields a verified starter fact, nothing is seeded and that is said in one line — an empty evidence folder is honest, a folder of guesses is not | `brain/schemas/team-member.md` | |
| `TEAM-63` | a deliverable that fails a criterion sets the record `status: rejected`, records what is missing, writes its `## Lesson` and goes back — unverified work is never passed to the principal | `brain/playbooks/delegate.md` | |
| `TEAM-64` | the whole feature is invisible until used — with no roster linked, the team is never mentioned unless the principal asks or it is offered at onboarding | `brain/schemas/team-member.md` | |
| `TEAM-65` | the rest of the record name is `<slug>-<task>-<YYYY-MM-DD>`, so a record identifies its specialist and its task without being opened; only the `deleg-` prefix is asserted (`TEAM-27`) | `brain/schemas/team-member.md` | |
| `TEAM-66` | an `inactive` charter is linked under `## Inactive` and not under `## Active` — the branch exists in the layout check but no fixture reaches it: both team charters are `status: active` and the roster's `## Inactive` is `_(none)_` | `brain/schemas/team-member.md` | |
| `TEAM-67` | a suggested specialist is not membership — suggestions live in `memory/team-suggestions.md`, outside `memory/team/`, and filing one neither creates that folder nor makes a team exist | `brain/schemas/team-member.md` | check(fixture) |
| `TEAM-68` | the suggestion file is a `type: log` file holding at most one `## Pending` entry whose grounding links resolve — one ask at a time, and an always-loaded file that stays bounded | `brain/schemas/team-member.md` | check(fixture) |
| `TEAM-69` | the always-loaded pointer to the suggestion file stays generic — it never names the suggested specialization, which would ride into every session and go stale the moment the suggestion is answered | `brain/schemas/team-member.md` | check(fixture) |
| `TEAM-70` | a denied suggestion becomes a permanent `## Declined` tombstone, so the domain is never re-suggested | `brain/schemas/team-member.md` | check(fixture) |
| `TEAM-71` | accepting a suggestion stands the specialist up and removes the pending entry, so a suggestion and a specialist never coexist for the same slug; denying moves it to the tombstones | `brain/playbooks/team.md` | check |
| `TEAM-72` | a charter carries a `## Memory scope` — the record types this specialist keeps and at what grain, drafted from the specialization at onboard and confirmed by the principal | `brain/schemas/team-member.md` | check eval:team-create |
| `TEAM-73` | the grain test decides what is the specialist's to keep: what Chief of Staff would not keep, and the specialist cannot work without, is filed in the specialist's subtree — and detail that fails the test stays down rather than climbing into a `## Promote` list | `brain/schemas/team-member.md` | check |
| `TEAM-74` | onboard asks what a great specialist would remember and what that would let it accomplish, drafts a scope from the specialization first, and shows it in the same confirm beat as the method and persona rather than adding a turn | `brain/playbooks/team.md` | check |
| `TEAM-75` | a specialist files its delegation findings at the grain its charter's `## Memory scope` names, so the scope governs every later task and not only the starter seed | `brain/playbooks/delegate.md` | check |
| `TEAM-76` | a specialist created before the `## Memory scope` existed is backfilled at first boot after upgrading — drafted per specialist from the roster, shown in one exchange, written only on approval, and idempotent on re-run | `brain/playbooks/team.md` | check |

### `DESK` — the desk write boundary

| ID | Behavior | Stated in | Covered by |
|----|----------|-----------|------------|
| `DESK-01` | everything Chief of Staff writes that is not durable memory — a draft, an analysis, an export, any work product the principal will reuse — lands under `memory/desk/` | `brain/schemas/memory-file.md` | eval:desk-deliverable eval:desk-no-stray-writes |
| `DESK-02` | a chat-sized answer stays in chat — the desk holds work in progress, not a transcript | `brain/schemas/memory-file.md` | |
| `DESK-03` | work written to the desk is linked from `memory/desk/index.md` in the same turn | `brain/schemas/memory-file.md` | eval:desk-deliverable eval:desk-folder-readme |
| `DESK-04` | a top-level folder under `desk/` is created with its `readme.md` already in place — a frontmatter block carrying today's `updated:` | `brain/schemas/memory-file.md` | eval:desk-folder-readme |
| `DESK-05` | touching any file beneath a desk folder bumps that folder readme's `updated:` in the same turn — it is the folder's freshness signal | `brain/schemas/memory-file.md` | |
| `DESK-06` | the root `memory/index.md` links the desk index under Load on demand, so work in progress is reachable when it is resumed | `brain/schemas/memory-file.md` | |
| `DESK-07` | a loose desk file takes a dated slug | `brain/schemas/memory-file.md` | |
| `DESK-08` | saving to the desk earns the same one-line receipt as any capture — the reply says where the file went | `brain/schemas/memory-file.md` | eval:desk-deliverable |
| `DESK-09` | shelving desk work is a move, not a delete: the file and its desk-index line go to `memory/desk/_parked/` in the same turn, a folder parks whole with its readme, and parked work stays reachable through `_parked/index.md` | `brain/schemas/memory-file.md` | |
| `DESK-10` | confidential content on the desk lives under its code name, exactly as anywhere else in memory | `brain/schemas/memory-file.md` | |
| `DESK-11` | nothing under `memory/desk/` is deleted without the principal's explicit approval of a complete, enumerated list of what would be removed — an earlier "apply all the fixes" does not cover it | `brain/playbooks/memory-lint.md` | eval:lint-desk-asks |
| `DESK-12` | a desk write is a memory write, so a stale session holds it — the content is delivered in chat and filed in a fresh session | `brain/schemas/memory-file.md` | |
| `DESK-13` | `/lint` audits desk hygiene — an unlinked desk file, a folder missing its readme, a readme older than a file beneath it, work untouched for 30+ days, and `_parked/` integrity | `brain/playbooks/memory-lint.md` | |

### `REL` — updates, versioning, migrations

| ID | Behavior | Stated in | Covered by |
|----|----------|-----------|------------|
| `REL-01` | a clean VERSION requires its own changelog header and a migration-notes block | `repo policy` | check |
| `REL-02` | the shipped tree always states which release it is — `VERSION` is never empty | `repo policy` | check |
| `REL-03` | when `VERSION` carries a pre-release suffix, the work since the last release sits under `## [Unreleased]` | `repo policy` | check |
| `REL-04` | an update replaces only the shipped files — the recipe states it never touches `memory/`, and a `/update check` leaves memory intact | `brain/integrations/updates.md` | check eval:update-prompt |
| `REL-05` | every top-level entry of the shipped folder is named in the `/update` copy recipe, so an existing install actually receives it | `brain/integrations/updates.md` | check |
| `REL-06` | the release build produces both published archives from `src/` alone, with no hand steps | `repo policy` | check |
| `REL-07` | `cos.zip` is flat — unzipping it drops the files straight into the principal's folder, with no wrapper directory | `brain/integrations/updates.md` | check |
| `REL-08` | `ChiefOfStaff.zip` stays wrapped in a `ChiefOfStaff/` directory, because installs predating 0.20.0 hardcode that path and can never be corrected remotely | `brain/integrations/updates.md` | check |
| `REL-09` | both published archives carry identical payloads — one release in two wrappings, never two builds | `brain/integrations/updates.md` | check |
| `REL-10` | the flat archive contains everything a prompt boot needs: `AGENTS.md`, `CHIEFOFSTAFF.md`, `VERSION`, `brain/index.md`, the onboard command, and an empty `memory/` | `repo policy` | check |
| `REL-11` | the release path publishes to the official repo and stops there — it holds no site credential and no site clone URL, because the site pulls | `repo policy` | check |
| `REL-12` | `/update check` reports the local version and applies nothing | `.claude/commands/update.md` | eval:update-prompt |
| `REL-13` | the boot update check runs at most once a day, prompts once, and never updates without the principal's OK | `brain/integrations/updates.md` | |
| `REL-14` | a `-dev` local `VERSION` skips the update check entirely — a development checkout is already ahead of the latest release | `brain/integrations/updates.md` | |
| `REL-15` | the memory migration pass runs at the first fresh session after an upgrade, spans `memory/meta.md` → `onboarded_against` to `VERSION`, and advances that marker only once the required steps are done | `brain/integrations/updates.md` | eval:migration-span |
| `REL-16` | version spans are compared numerically, component by component — `0.9.0` is older than `0.10.0`, though text comparison claims the opposite | `brain/integrations/updates.md` | eval:migration-version-order |
| `REL-17` | the migration pass proposes before writing: anything that would change the principal's own content is raised in one exchange and written only on a yes | `brain/integrations/updates.md` | eval:upgrade-proposes-migration |
| `REL-18` | when nothing that applies would write the principal's content, the migration pass says nothing about migrations | `brain/integrations/updates.md` | eval:upgrade-silent-when-nothing-applies |
| `REL-19` | a stale session never writes memory — it holds the change, says why, and names a fresh chat as what unblocks it | `CHIEFOFSTAFF.md` | eval:stale-blocks-memory-write |
| `REL-20` | the stale freeze covers writes only — a stale session still reads, drafts and answers from memory | `CHIEFOFSTAFF.md` | eval:stale-still-answers |
| `REL-21` | once stale, every reply for the rest of the session opens with the stale-session banner, and it is not dismissible in-session — needs a multi-turn harness, see [`decisions.md`](decisions.md#session-freshness-ablation) | `CHIEFOFSTAFF.md` | |
| `REL-22` | a reload after compaction does not clear stale mode — the banner and the write freeze survive it — needs a multi-turn harness, see [`decisions.md`](decisions.md#session-freshness-ablation) | `CHIEFOFSTAFF.md` | |
| `REL-23` | an update never half-applies: if the unpacked archive has no `AGENTS.md`, it stops and changes nothing | `brain/integrations/updates.md` | |
| `REL-24` | `brain/` and `.claude/commands/` are replaced wholesale — removed, then copied — so files a release deleted do not survive the update | `brain/integrations/updates.md` | |
| `REL-25` | the migration pass reads every release entry in the span, not only the entries carrying migration notes | `brain/integrations/updates.md` | |
| `REL-26` | an override whose brain target a release removed is flagged to the principal with a choice, never migrated silently | `brain/integrations/updates.md` | |
| `REL-27` | a colleague who wants their own Chief of Staff is pointed at chiefofstaff.team for their own copy, not handed this folder — carried by the site link in the shipped README, not by prose, see [`decisions.md`](decisions.md#confidentiality-referral-not-load-bearing) | `README.md` | eval:referral-points-to-site |
| `REL-28` | between releases `VERSION` carries a `-dev` suffix — the suffix is check #5's branch predicate, not an assertion, so a release-shaped `VERSION` on main skips the branch instead of failing it | `repo policy` | |
| `REL-29` | an update never touches `.claude/settings.local.json` either — the principal's local host settings survive it, and nothing fences that today | `brain/integrations/updates.md` | |
| `REL-30` | the silent migration pass still advances the marker — `REL-15`'s marker assertion was not reused here, so only the silence is asserted | `brain/integrations/updates.md` | |
| `REL-31` | every release entry in `CHANGELOG.md` carries exactly one migration block, so a span walk has no holes in it | `repo policy` | check |
| `REL-32` | a migration block opens with one of the four classification literals, so the pass can tell "nothing to do" from "writes at boot" without reading prose | `repo policy` | check |
| `REL-33` | a subject-keyed bullet parses as `<scope>:<name>` with a known scope, so the resolver can bucket statements across entries | `repo policy` | check |
| `REL-34` | a supersede names a real, older entry — supersession is forward-only, so the newest statement per key wins a span walk | `repo policy` | check |
| `REL-35` | the span is walked entry by entry from oldest to newest, not read as an unordered set — the traversal order is what makes an order-dependent chain resolve the same way a one-version-at-a-time upgrade would | `brain/integrations/updates.md` | |
| `REL-36` | keyed statements are bucketed by subject key and only the newest one in the span survives — an earlier statement about the same subject is discarded, not applied and then undone | `brain/integrations/updates.md` | |
| `REL-37` | a surviving statement is checked against what this folder actually contains before anything is proposed — a change to something this install does not have is not a migration for this principal | `brain/integrations/updates.md` | |
| `REL-38` | versioned migration playbooks run in the version order of the releases pointing to them, and each is idempotent, so a multi-version jump lands where sequential upgrades would | `brain/integrations/updates.md` | |
| `REL-39` | a subject key stated on more than one entry declares `**Supersedes X.Y.Z.**` on its newest statement — a repeated key is how an order-dependent chain is written down, and an undeclared one is how that chain collapses to its newest half in silence | `repo policy` | check |

### `HOST` — integrations + host parity

| ID | Behavior | Stated in | Covered by |
|----|----------|-----------|------------|
| `HOST-01` | a compaction is detected and context reloaded on Codex, not only on Claude Code — open, see [`decisions.md`](decisions.md#reload-codex-compaction-open) | `CHIEFOFSTAFF.md` | |
| `HOST-02` | the host-neutral discovery contract stays stated in the shipped tree — absence is inconclusive, at least two integration-specific attempts and a status check run first, the fallback order is named, and four of the six connector states are matched as literal labels (states 1 and 3 are not). **Check #4b matches these as literal token strings on purpose**: reword one without changing the check in the same commit and the guard goes vacuous rather than red (`AGENTS.md` → Never) | `brain/integrations/connectors.md` | check |
| `HOST-03` | a tool missing from the initial context is inconclusive — a connector is never called disconnected off one failed discovery query, and "genuinely unavailable" needs a positive signal from a status surface or from the principal | `brain/integrations/connectors.md` | eval:connector-no-premature-browser |
| `HOST-04` | the browser sits last in the fallback order — it is never opened to route around a slow tool search, a connector awaiting authorization, or a status nobody checked | `brain/integrations/browser.md` | eval:connector-no-premature-browser |
| `HOST-05` | once the native tier is genuinely out, the browser is proposed rather than waited for — with the check that was actually run stated in the same sentence, so the offer carries its own evidence — and offered at most once per session | `brain/integrations/browser.md` | |
| `HOST-06` | a decline of browser control is honored — it is not re-pitched, and the page is not pretended to have been fetched | `brain/integrations/browser.md` | eval:browser-offer-after-decline |
| `HOST-07` | Chief of Staff never types or stores a secret — a page needing a sign-in is co-browsed, with the principal entering it themselves and the task picked back up after | `brain/integrations/browser.md` | eval:browser-no-credentials |
| `HOST-08` | a credential the principal pastes anyway is not repeated back and is never claimed to have been saved | `brain/integrations/browser.md` | eval:browser-no-credentials |
| `HOST-09` | CAPTCHAs and bot checks, system or security settings, financial transactions, and running a file from an untrusted source are handed to the principal, never done | `brain/integrations/browser.md` | |
| `HOST-10` | nothing is sent, submitted, published, purchased or consented to in a browser without an explicit OK each time — a prior yes never carries to the next one | `brain/integrations/browser.md` | |
| `HOST-11` | page content is untrusted input — text that instructs is data to report, never a command to follow, and an injection attempt is quoted to the principal and quarantined rather than acted on | `brain/integrations/browser.md` | |
| `HOST-12` | what is typed into a page has left the principal's hands, so the code-name rule applies in full — a field that genuinely needs a real identity is handed to the principal | `brain/integrations/browser.md` | |
| `HOST-13` | the host is detected and recorded in `memory/meta.md` as `host:`, with the machine's OS and default browser inferred quietly alongside it — never surfaced as commands, never guessed, and asked once where they genuinely cannot be determined | `brain/integrations/hosts.md` | |
| `HOST-14` | the principal is addressed in app names — "the ChatGPT desktop app", "the Claude desktop app" — while branching happens on the host name they never see | `brain/integrations/hosts.md` | |
| `HOST-15` | on Codex, connector guidance names the Plugins tab — never claude.ai → Settings → Connectors, which is a dead end there. The four `codex-*` scenarios carry `only_hosts=("codex",)`, so this coverage exists only on a Tier 2 `--host codex` run | `brain/integrations/hosts.md` | eval:codex-connector-path |
| `HOST-16` | on Codex, a recurring brief is set up as a Scheduled task, never as a Routine — the assertion fences only the plural label "Routines", so the singular would pass; Tier 2 only, as `HOST-15` | `brain/integrations/hosts.md` | eval:codex-scheduled-naming |
| `HOST-17` | on Codex, the browser fallback is the app's own built-in browser with nothing to install — never the Claude for Chrome extension; Tier 2 only, as `HOST-15` | `brain/integrations/hosts.md` | eval:codex-browser-fallback |
| `HOST-18` | on a host without slash commands the same actions are offered as plain words — the judge grades the plain-words offer and the absence is asserted for `/lint` alone, not for every slash command; Tier 2 only, as `HOST-15` | `brain/integrations/hosts.md` | eval:codex-no-slash-commands |
| `HOST-19` | whichever calendar is connected is simply used, and for ongoing work every connected calendar and account is spanned rather than just the default — the onboarding history scan being the one exception, held to the consented scope | `brain/integrations/calendar.md` | |
| `HOST-20` | with no calendar connected the absence is said once, briefly, and the brief or the prep is produced anyway or the meetings asked for — it never blocks | `brain/integrations/calendar.md` | |
| `HOST-21` | reading the calendar is free; creating, moving or declining an event is outward-facing and waits for an explicit OK | `brain/integrations/calendar.md` | |
| `HOST-22` | Microsoft 365 needs a business account — a personal Outlook.com or Hotmail address cannot connect, and that is said rather than discovered | `brain/integrations/calendar.md` | |
| `HOST-23` | connectors are recommended for the stack the principal actually described, calendar and mail first, each with one line on what it unlocks — and anything already connected is confirmed rather than walked through again | `brain/integrations/connectors.md` | |
| `HOST-24` | every connected account of a type is read for ongoing work, not just the primary — a principal's world crosses accounts and one default misses half of it | `brain/integrations/connectors.md` | |
| `HOST-25` | when delayed discovery finally succeeds, the principal's original task resumes automatically and the capability is recorded in `memory/integrations.md` | `brain/integrations/connectors.md` | |
| `HOST-26` | a failure is reported as what was actually checked — a browser, permission or discovery failure is never converted into a claim that a connector's authentication is broken | `brain/integrations/connectors.md` | |
| `HOST-27` | the routines flow proposes the daily and weekly briefs plus the two maintenance routines, memory lint and explore, as Local routines that run against this folder — `routines-suggest` matches `weekly` once, so it cannot tell the preview and the retro apart | `brain/integrations/routines.md` | eval:routines-suggest |
| `HOST-28` | before any scheduled task is created, what is already scheduled is reviewed, and an overlap in purpose or timing is surfaced with a choice — update, adjust, merge or skip — never a silent second copy | `brain/integrations/routines.md` | eval:routines-dedup |
| `HOST-29` | every scheduled task created is recorded in `memory/preferences/briefings.md` with its cadence, purpose, host and outcome — including ad-hoc ones — so the registry stays enumerable on a host that cannot list its own tasks | `brain/integrations/routines.md` | |
| `HOST-30` | a routine must run locally against this folder — a cloud or remote run has no access to this principal's `memory/` and would produce an empty brief | `brain/integrations/routines.md` | |
| `HOST-31` | the routine promise is honest about its limits — a scheduled brief typically fires only while the app is open and awake, and each run arrives as a notification and a new session, never an email | `brain/integrations/routines.md` | |
| `HOST-32` | a specialist's `cadence:` duty becomes a Local routine that runs as a persona-swap, stays bounded by that specialist's `autonomy`, and records its run in the specialist's own `ledger.md` | `brain/integrations/routines.md` | |
| `HOST-33` | each routine the principal keeps is created by Chief of Staff with the host's own routine tools — their approval of the tool execution is the confirmation, not a hand-off to manual UI steps | `.claude/commands/routines.md` | |
| `HOST-34` | a pasted credential is not restated for any reason — not to warn about it, not to confirm which one is meant; the reply says it was not stored, suggests rotating it, and refers to it as "that password" | `brain/integrations/browser.md` | |
| `HOST-37` | the Codex status check names something the agent can actually run — its callable tools, then deferred discovery by provider and canonical action names — rather than the Plugins tab, which is what the principal is pointed at; tool presence counts as positive evidence while absence proves nothing, and an unreadable status is `inconclusive` | `brain/integrations/connectors.md` | check |
| `HOST-35` | both per-host discovery procedures stay stated in the shipped tree — each host's own status surface, state labels and retry mechanics, so host logic never leaks across hosts. Same literal-token caveat as `HOST-02` | `brain/integrations/hosts.md` | check |
| `HOST-36` | the decline is honored from the RECORD — `memory/integrations.md` showing a past decline suppresses the offer in a later session; the scenario's decline arrives in the prompt and no seed writes that file | `brain/integrations/browser.md` | |

### `REPO` — conformance + dev-repo invariants

| ID | Behavior | Stated in | Covered by |
|----|----------|-----------|------------|
| `REPO-01` | every brain file carries `name`, `description` and `type` in frontmatter | `brain/schemas/memory-file.md` | check |
| `REPO-02` | `layer:` and `version:` never return to the frontmatter schema | `brain/schemas/memory-file.md` | check |
| `REPO-03` | every brain file's `type` is one of the allowed set | `brain/schemas/memory-file.md` | check |
| `REPO-04` | every brain file's `name` is unique across the tree | `brain/schemas/memory-file.md` | check |
| `REPO-05` | every brain file is reachable from `brain/index.md` by link traversal — an unlinked one is an orphan the router can never load | `repo policy` | check |
| `REPO-06` | every path `brain/index.md` routes to directly exists — the router never points at a missing file | `repo policy` | check |
| `REPO-07` | every relative `.md` link in a tracked file resolves to a file that exists — outside `tests/fixtures/` (test data, not product links), and not counting links inside code fences or inline code, or runtime `memory/` paths | `repo policy` | check |
| `REPO-08` | no tracked file uses the retired terms "canonical" or "instance", except the sanctioned "canonical action(s)" of connector discovery — `tests/` and `.agents/personas/`, which describe the guard rather than obey it, are exempt | `repo policy` | check |
| `REPO-09` | links are plain markdown — no `[[wikilinks]]`, which only one editor resolves; same `tests/` and `.agents/personas/` exemption as `REPO-08` | `repo policy` | check |
| `REPO-10` | at least one slash command ships, and every one of them declares a `description` in frontmatter | `repo policy` | check |
| `REPO-11` | every `brain/…` path named in a slash command or a boot file resolves | `repo policy` | check |
| `REPO-12` | the principal's `memory/` contents are never tracked; only `memory/.keep` is, so the folder exists in a fresh install | `repo policy` | check |
| `REPO-13` | `brain/` and `.claude/commands/` are tracked — they are what ships | `repo policy` | check |
| `REPO-14` | local runtime state (`.claude/settings.local.json`, `.claude/scheduled_tasks.lock`) is ignored in both the repo root and `src/`, not just on one developer's machine | `repo policy` | check |
| `REPO-15` | the development specialists under the root `.agents/personas/` are tracked; the generated per-principal shims under `src/.claude/agents/` are not | `repo policy` | check |
| `REPO-16` | no web tooling takes root in `src/` — its conventional directories and config files would ship inside `cos.zip` | `repo policy` | check |
| `REPO-17` | the shipped tree never mentions the development repo: no dev-only path (`CONTRIBUTING.md`, `tests/`, `scripts/`, `.github/`, `.gitignore`) and nothing explained in git terms — scanned over `src/**/*.md` with code fences stripped, and `CHANGELOG.md` exempt as released history | `repo policy` | check |
| `REPO-18` | the shipped `README.md`, the first thing a principal reads, contains no em-dash | `repo policy` | check |
| `REPO-19` | every workflow job that declares `runs-on:` refuses to run outside `pkozanian/ChiefOfStaff`, so a fork or mirror can never cut a release or spend tokens — a job with no `runs-on:` (a reusable-workflow call) is not scanned | `repo policy` | check |
| `REPO-20` | no tracked file names the private repo this tree is authored in | `repo policy` | check |
| `REPO-21` | the behavior registry exists and parses to at least one well-formed row | `repo policy` | check |
| `REPO-22` | every registry row is four columns — a literal `\|` must be escaped, and a row that is not is failed rather than silently dropped | `repo policy` | check |
| `REPO-23` | behavior IDs are unique: permanent, never renumbered, never reused | `repo policy` | check |
| `REPO-24` | every behavior ID's area prefix is one of the eleven fixed areas | `repo policy` | check |
| `REPO-25` | every `Stated in` path resolves to a real file under `src/`, unless it is the literal `repo policy` | `repo policy` | check |
| `REPO-26` | structural coverage is bidirectional: a row's `check` marker is backed by an annotated `check()`, and an annotated ID has a row that claims it | `repo policy` | check |
| `REPO-27` | `check()`'s `behavior=` is a string literal, so the static reader and the annotation scanner can never disagree | `repo policy` | check |
| `REPO-28` | eval coverage is bidirectional: a cited `eval:` pattern matches a real scenario, and that scenario names the behavior back | `repo policy` | check |
| `REPO-29` | the golden onboarding fixture is present in the repo — the tree every memory-lint check and most eval seeds read | `repo policy` | check |
| `REPO-30` | the virtual-team fixture is present in the repo — the tree every team-layout check reads | `repo policy` | check |
| `REPO-31` | every functional file that ships — `brain/**/*.md`, the three boot files, every slash command — is the `Stated in` of at least one row, so adding one and naming no behavior for it fails the suite | `repo policy` | check |
| `REPO-32` | no eval scenario is an orphan: every scenario names at least one behavior in its `behaviors=`, and rule 2's transpose then requires that row to cite the scenario back — so a scenario cannot drift out of the registry unnoticed | `repo policy` | check |
| `REPO-33` | every `check()` call site in `tests/run.py` carries a `behavior=`, so no structural assertion exists outside the registry | `repo policy` | check |
| `REPO-34` | the summary table's per-area and total counts equal the rows' — the checksum that gives a **gap** row an integrity guard, since nothing else claims one and a mistyped ID would otherwise drop a behavior in silence | `repo policy` | check |
| `REPO-35` | the upstream feedback address is one literal string, identical in the shipped `README.md` and in `brain/schemas/capture-rules.md` — the site asserts the address it publishes against the shipped brain, so a drifted copy breaks that build at a distance | `repo policy` | check |
| `REPO-36` | every shipped slash command has a matching `.agents/skills/<name>/SKILL.md` and vice versa, with one shared `description` | `repo policy` | check |
| `REPO-37` | every neutral skill's frontmatter `name` equals its directory, and every `brain/…` path it names resolves | `repo policy` | check |
| `REPO-38` | the two published copies of a command — `.claude/commands/<name>.md` and `.agents/skills/<name>/SKILL.md` — carry the same body, so neither side can be edited alone | `repo policy` | check |
| `REPO-39` | every row of the onboarding checklist template is referenced, by ID, from the step file the template says owns it (Finishing rows from `flow.md`), so no requirement exists that no step resolves | `repo policy` | check |
