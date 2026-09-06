# Tests

The Chief of Staff is pure markdown, so "tests" come in two layers.

## 1. Structural tests — deterministic, fast, run anywhere

```
python3 tests/run.py
```

Zero dependencies (Python 3 stdlib). Checks the files and conventions, exits non-zero on any
failure. Listed in the order they run, under the labels they print:

1. **Frontmatter validity** — every `brain/**/*.md` carries `name`, `description` and a valid
   `type`, with a unique `name`. Also a stray-key guard: `layer:` and `version:` were removed from
   the schema (the tree is implied by the path, the release lives in `VERSION`) and must not return.
2. **Index completeness** — every brain file is **reachable** from `brain/index.md` by following
   links, not necessarily listed in it. Transitive on purpose: `onboarding/steps/*` are reached only
   from `onboarding/flow.md`, and listing them in an always-loaded file would cost tokens and imply
   a load trigger they do not have.
3. **Link resolution** — every relative markdown link in tracked files resolves (skipping fixtures,
   code fences, inline code, and runtime `memory/…` paths).
4. **Naming guards** — no bare `canonical`/`instance` terminology (the phrase "canonical action(s)"
   is the one allowed form), no `[[wikilinks]]`.
   **4b. Connector-discovery contract** — asserts the literal token strings in
   `brain/integrations/connectors.md` and `hosts.md`. It matches exact substrings deliberately, so a
   copyedit there is a silent regression rather than a typo fix: reword one and update this in the
   same change.
5. **Release metadata** — a `-dev` VERSION requires a `## [Unreleased]` section; a clean one requires
   its own `## [x.y.z]` header **and** a `### Migration notes` block. Silence is not an answer —
   0.15.0 removed the per-specialist `clearance:`/`## Reads` charter fields with no note at all and the
   first-boot pass migrated straight past it. "No action required." is a fine answer; not saying
   anything is not.
6. **Override-target mirror paths** — each override target in `brain/role/defaults.md` mirrors a real
   `brain/` file.
7. **Slash-command validity** — `.claude/commands/*.md` have a description and valid `brain/` refs.
8. **Gitignore behavior** — `memory/` contents ignored, `memory/.keep` tracked, `brain/` tracked,
   `.claude/settings.local.json` ignored.
   **9b. No web tooling in `src/`** — no `pages/`, `layouts/`, `components/`, `content/`, `styles/`,
   no `package.json` or `*.config.*`. `src/` is the manifest, so any tool claiming those conventional
   names would ship its scaffolding to every principal.
   **8b. Dev/dist boundary** — `src/` is self-contained: nothing in it links out to `CONTRIBUTING.md`,
   `tests/`, or `scripts/`, or explains itself in git terms. The user has a folder, not a checkout.
   **8c. `/update` delivers everything in `src/`** — an install updates by running the recipe in the
   brain it already has, so a newly added file has to be one the recipe actually copies.
   **8d. Published archive shapes** — `cos.zip` is flat (the prompt boot says "unzip it into this
   folder", which is only true if it is), `ChiefOfStaff.zip` is nested for pre-0.20.0 installs, and
   their contents are identical.
10. **Onboarding output passes memory-lint** — the golden fixture of a freshly-completed onboarding
    satisfies the mechanically-checkable lint rules.
11. **Virtual team layout** — a fixture team tree satisfies the link-based roster invariants.
12. **Memory reachability** — every file in a memory fixture is reachable from its `index.md`
    (except `_quarantined/` and uncited `_processed/` originals).
13. **No em-dashes in `src/README.md`** — house style for the public marketing surfaces. The site
    repo asserts the same rule over its own three.
17. **Behavior coverage registry** — every behavior in [`behaviors.md`](behaviors.md) is well-formed
    and states a real file; every eval scenario and every `check()` names what it covers, and the
    registry cites it back. The link is written twice and asserted an exact transpose, so a citation
    that stopped being true fails instead of reading green. Its summary table is reconciled with the
    rows as a checksum — the only guard an *untested* row has, since nothing else claims one. Prints
    the untested count.

> The numbering is historical and not sorted: `9b` runs before `8b`, and the `8x` family grew around
> the original check 8. It runs to **17**, with **9 retired** — the coverage manifest it gated is gone
> and its number never reused; 14–16 run but are documented where they bind (the workflows,
> `CONTRIBUTING.md`). The labels are cited by name there and in `AGENTS.md`, so they stay stable.

**CI** (`.github/workflows/tests.yml`) runs this suite on every push / PR.

## 2. Behavioral eval — runs the real agent (`claude -p`, or `codex exec`)

```
python3 tests/eval/run_eval.py            # all scenarios (live)
python3 tests/eval/run_eval.py --only dropped-doc
python3 tests/eval/run_eval.py --filter mem-   # all scenarios whose key contains a substring
python3 tests/eval/run_eval.py --dry-run  # exercise plumbing WITHOUT calling claude / spending tokens
python3 tests/eval/run_eval.py --retries 1
python3 tests/eval/run_eval.py --host codex --filter codex-   # Tier 2 (see below)
```

For each scenario the harness **copies the repo to a throwaway temp dir**, seeds preconditions,
runs the agent there, and asserts on the resulting files / output. Scenarios cover: explicit
onboarding, the un-onboarded nudge, defaults accept-vs-change, passive capture, auto-intake of
chat-shared documents, confidentiality (real name never surfaced), override precedence, and
host-specific branches (Codex's Plugins tab, Scheduled tasks, built-in browser, no slash commands).

A scenario may carry `turns` — follow-up principal messages sent one at a time into the **same**
agent session (`claude -p --resume <session_id>`; `codex exec resume <id>`). The graded output is
every reply concatenated, each under a `── turn N · principal: …` marker, so a judge sees both sides.
This is how a conversation-shaped failure is tested at all: `onboard-terse` feeds twenty-six one-line
answers and asserts every required offer was still made. It costs one agent call per turn, so keep
such scenarios few.

A failing scenario prints only the first 700 characters of the agent's output. Set
`CHIEFOFSTAFF_EVAL_DUMP=<dir>` to keep the whole transcript and the `memory/` tree the run left behind
under `<dir>/<scenario-key>/` — the temp copy is otherwise gone on return, which makes a multi-turn
failure impossible to diagnose from the summary alone.

### Two tiers, and what each proves

Chief of Staff ships to **two hosts** — the Claude desktop app (Claude Code) and the ChatGPT desktop
app (Codex) — and several brain files branch on which one it is (`hosts.md`, `connectors.md`,
`routines.md`, `updates.md`, `onboarding/flow.md`, and others). The eval suite runs at two tiers:

- **Tier 1 — host-independent behaviour, executed by Claude.** Runs by default, no new dependency.
  Scenarios here must be ones whose correct answer **does not depend on the host**, e.g.
  `onboard-greeting-host-aware`: the greeting must never name a slash command *on any host*, so it is
  observable everywhere.

  **You cannot test a host BRANCH this way, and it is worth knowing why.** Seeding `host: codex` and
  running under `claude -p` does not work: the brain detects the real host and *corrects* the seeded
  value, exactly as `hosts.md` tells it to. Measured — a connector scenario opened with *"your memory
  had you flagged as running on Codex, but you're actually talking to me through Claude Code, I fixed
  that in `memory/meta.md`"*, and then correctly gave Claude Code guidance. The scenario failed while
  the product was behaving perfectly.

  The corollary is a design lesson, not just a testing one: **a rule written to be host-independent is
  both more robust and cheaper to verify than a conditional one.** The un-onboarded greeting was
  originally conditional ("only mention `/onboard` on Claude Code"), and the model rationalised around
  it; making it unconditional fixed the behaviour *and* made it testable on any host.

  Scenarios that genuinely need a host declare it with `only_hosts=("codex",)`; the runner **skips**
  them elsewhere rather than reporting a meaningless failure.
- **Tier 2 — the same scenarios executed by `codex exec`.** Pass `--host codex` (or set
  `CHIEFOFSTAFF_EVAL_HOST=codex`). This proves **GPT actually follows our prose**, which is a
  different question from Tier 1 and the only tier that answers it. Requires the `codex` CLI on PATH
  and authenticated (`npm i -g @openai/codex`, then `codex login`). **Grading always runs on
  `claude`** regardless of `--host` — a fixed grader across model families is the point, so swapping
  the grader with the subject would make results incomparable; `claude` must still be present and
  authenticated even under `--host codex`. Running `tests/eval/run_eval.py --host codex` without the
  `codex` CLI installed exits with an actionable message (install command + `--host claude` fallback),
  not a stack trace.

**If we ever revisit native subagents.** The projection was removed in 0.22.0 (no measurable
behavioural difference — see `src/CHANGELOG.md`). Keeping the one hard-won fact here so it doesn't
have to be re-derived: a dispatch is invisible in normal output, because the prose reads the same
whether a specialist ran in its own context or Chief of Staff persona-swapped inline. To observe one, run
`claude -p` with `--output-format stream-json --verbose` and look for `"subagent_type":"<slug>"` in
the trace; the final answer then comes from the terminal `{"type":"result"}` event, not stdout. A
shim must be **seeded** before the run — one generated mid-session isn't live until the next session,
so it would only ever persona-swap. And ablate before believing any of it: every non-dispatch
assertion we built on that path still passed with the behaviour's own instructions deleted.

**Run the whole suite on both hosts, not just the `codex-` ones.** Every scenario without an
`only_hosts` restriction is executable under `--host codex`, and the first full cross-host sweep is
what surfaced the findings below — none of which the `codex-` subset could have caught:

```bash
python3 tests/eval/run_eval.py --host codex     # the FULL suite under GPT, not just --filter codex-
```

**What a second model family is actually for.** A scenario that passes on one host and fails on the
other is, more often than not, evidence about **the test or the brain** rather than about the model:

- **String assertions drift into testing one model's vocabulary.** `out_has` is a plain substring, so
  a correct answer failed for writing "frozen" where the assertion said `"freeze"`, "Sept 15" where
  the matcher only knew "Sep", and "Footwear count" for `"Footwear cycle-count"`. Each passed on
  Claude purely by phrasing habit. **Assert the concept** — a stem, a set of forms, or the number that
  proves the fact was recalled — not the wording one model happens to use.
- **A scenario can enshrine a rule violation.** `dropped-doc` required a prompt-injected document's
  facts to be ingested, which `brain/schemas/capture-rules.md` step 0 forbids outright. It passed only
  on runs where the agent *broke* the rule; the compliant answer scored as a failure. It is now split
  into `dropped-doc` (clean intake) and `dropped-doc-injection` (refuse, quarantine, don't ingest).
- **Divergence usually means the prose is ambiguous, not that one model is wrong.** Where two families
  read the same passage differently, that passage is underspecified — the fix belongs in the shared
  brain, at the producer. Three brain rules were clarified this way, each because GPT followed the
  text *more* literally than Claude did.

**Tuning discipline.** When a Codex-branch scenario fails, patch **one thing at a time** in the brain
and rerun the same subset (e.g. `--filter codex-` or `--only codex-scheduled-naming`) before touching
anything else. If a fix only regresses one model family — Tier 1 (Claude) stays green but Tier 2
(Codex) breaks, or vice versa — fix the **host overlay** (`brain/integrations/hosts.md` and the other
host-branching files), not the shared brain that both models read identically. Conflating the two
tiers muddies which layer actually needs the fix.

### Frozen eval date (why time-relative scenarios don't rot)
The agent otherwise reasons off the **real system clock**, but the fixtures are authored as-of a
fixed moment (their `commitments.md` files anchor on **2026-07-27**). So the harness **pins today**:
every scenario prompt is prefixed with "Today's date is `EVAL_TODAY`…" (see `pin()` in
`run_eval.py`), which keeps time-relative scenarios (overdue / due / this-week / current)
deterministic no matter when the suite runs. `EVAL_TODAY` defaults to `2026-07-27`; override it to
run the suite at a different clock position:

```
CHIEFOFSTAFF_EVAL_TODAY=2026-10-01 python3 tests/eval/run_eval.py --only mem-saas-cto-aggregation
```

When you add a time-relative fixture/scenario, author its dates relative to `2026-07-27`.

### Memory-retrieval suite (`mem-*`, run with `--filter mem-`)
The `mem-*` scenarios stress the Chief of Staff's hardest behavior — **retrieving from a deep memory tree**.
They seed **static fixture principals** from `tests/fixtures/memory/<persona>/` (fictitious leaders
across levels/industries — e.g. `saas-cto`, `retail-store-manager`, `ic-developer`), each with
planted traps (same-name people, stale-vs-current facts, multi-hop chains, buried needles, absent
look-alikes, aggregation, confidential code names). Each fixture header records its **answer key**;
assertions are **deterministic-first** (`out_has` exact fact / `out_lacks` a confidential real name),
with an LLM judge only for `synthesis` and `absence`. Fixtures are **test data** — exempt from the
frontmatter/naming/link checks in `run.py`. Adding a persona = a new fixture dir + scenarios, each
declaring its `behaviors=` and cited back from `behaviors.md`. This suite is the **largest and most
token-costly** — run it on demand (`--filter mem-`), not in push CI.

### What a scenario can prove — shape vs interpretation

The files this product ships **are** its behaviour, so there are two very different things a scenario
can establish, and it is easy to mistake one for the other:

- **Shape** — the file exists, has the right sections, contains the right string. Cheap, exact, and the
  right default (see the non-determinism caveat below). It proves a file was **written correctly**. It
  proves nothing about whether that file *does* anything.
- **Interpretation** — the agent's behaviour changed *because* of what a file contains. Plant something
  distinctive, then assert it surfaces downstream where it could only have come from that plant. The
  `mem-*` suite is the exemplar: `seed_fixture` is used ~60 times to bury traps (same-name people,
  stale-vs-current facts, buried needles) and assert an answer only the fixture could produce.

**Prefer interpretation for any claim that a file matters.** Shape assertions are rot-prevention —
keep them, and label them as that. The team-subsystem checks added in 0.22.0 (all seven record
sections, `member:` present, the `deleg-` naming) are exactly that: they stop silent structural rot,
they are not evidence the record is useful.

**Soundness rule: the asserted property must have exactly one causal path.** If anything other than
the thing under test could produce it, the test isolates nothing. Measured examples from this repo:

- `specialist-follows-method` plants an arbitrary house convention (`Budget-check: <n> min remaining`) in a
  specialist's charter `## Method`. Nothing in `brain/` mandates a closing marker line, so the charter is
  the only possible source. Ablated — `## Method` stripped — it fails on both hosts. **Sound.**
- `specialist-honors-override` plants a marker in an override file, but Chief of Staff's own boot step 5
  overlay pass delivers it too. Two paths. It still passes with the specialist-side rule deleted. **A
  regression fence, not a proof** — and it is labelled that way in-scenario.

**Ablate before claiming a file or section is load-bearing.** Delete it and re-run; if the behaviour
survives, the text was not doing the work. Three claims were falsified this way in one session (the
subagent shim's craft step, its casebook reference, and its tool grant), each of which read as
obviously load-bearing.

**Why there is no "judge the file" tier.** It was proposed and rejected: pointing an LLM judge at a
file grades whether the file *reads* well, which is still its surface. A well-written charter that
changes nothing would pass. Judge the transcript for conduct (voice, attribution, refusals), assert
files deterministically for shape, and use a planted fingerprint for effect.

### Honest caveats
- **Non-deterministic.** Assertions target structure (files, frontmatter, substrings), not exact
  wording. Use `--retries` to absorb variance.
- **Costs tokens & needs auth.** Requires the `claude` CLI on PATH and an authenticated session
  (Tier 1, and always for grading). `--host codex` (Tier 2) additionally requires the `codex` CLI on
  PATH, authenticated on its own (separate) account — it spends a second account's tokens.
- **Local / on-demand only — never CI.** No API-key secret is wired into CI by design. Tier 2 is
  opt-in and run deliberately; `.github/workflows/eval.yml` stays Claude-only.
- **Sandboxed.** Everything happens in a temp copy; your real `memory/` is never touched.
  `--dangerously-skip-permissions` is used *only* because the working dir is a throwaway copy.
- A couple of scenarios are **LLM-graded** (soft output checks) and marked as such.

Start with `--dry-run` to confirm the plumbing, then run live.

### Running the evals in CI

`.github/workflows/eval.yml` runs the behavioral eval in GitHub Actions:

**Dispatch-only** — Actions → **evals** → *Run workflow* (optionally set `scenario` to one key, e.g.
`nudge`, to keep a run cheap; default `all`).

It used to also run weekly, behind a `gate` job that skipped the run when the functional surface
hadn't changed. Both are gone: the evals are normally run locally, where their output can be read as
they go, and a scheduled job that spends real quota in a repo nobody is watching is a bill waiting to
be discovered. Dispatch it when you want a clean-room run.

Two guards on that run, both about cost:

- **Only the repo owner can dispatch it** (`github.actor` pin). Dispatching already needs write
  access, so this changes nothing on a private repo — it matters the day the repo is public or gains
  a collaborator, when "who can spend a full sweep" stops being the same question as "who can push".
- **The model is pinned to `sonnet`** in the workflow env, not merely defaulted. Both the scenario
  agent and the judge take `--model $CHIEFOFSTAFF_EVAL_MODEL`, so that one variable governs every
  Claude call a run makes. The run header prints the model actually used — read it rather than
  trusting the pin.

It never runs on `push`/PR and can't block merges (evals are non-deterministic; `--retries 1`
absorbs the occasional judge miss — a red run may be a flake, not a regression).

**One-time auth setup** (uses your Claude subscription, not API billing):

1. Generate a long-lived token locally: `claude setup-token` (opens a browser; prints a 1-year token).
2. Add it as a repo secret named **`CLAUDE_CODE_OAUTH_TOKEN`**:
   `gh secret set CLAUDE_CODE_OAUTH_TOKEN` (paste the token), or Settings → Secrets → Actions.
3. The token **expires in 1 year** — regenerate and update the secret before then.

## Keeping tests in sync with the brain

[`behaviors.md`](behaviors.md) is the registry: one row per behavior the product promises, naming the
`src/` file that states it and the tests that cover it. Check #17 keeps it honest in both directions;
the registry's own header documents the columns.

- **Add** a functional file → name what it promises as rows (rule 4 fails until one is its `Stated in`).
- **Add** an eval scenario → set `behaviors=` and cite it back from those rows (rule 5 fails on an
  orphan, rule 2 if only one side of the link is written).
- **Add** a `check()` → pass `behavior="<ID>"` and mark the row `check` — or `check(fixture)` if it
  reads a fixture rather than the shipped tree, which is the weaker claim.
- **Add or remove any row** → update the "Where the coverage is" table in the same change; rule 7
  reconciles it with the rows, and a row that vanished (a typo'd ID) is caught nowhere else.
- **Remove** a file or scenario → drop its citation in the same change. **Modify** one → no ceremony,
  unless what covers it changed; the PR diff is the review.
- **Leave `Covered by` empty** when nothing asserts the behavior: a recorded gap, not a failure, and
  the suite prints the count every run.

Why a rule was cut, what was measured, what is still open: [`decisions.md`](decisions.md).

### Optional pre-commit hook

Run the structural suite before every commit:

```
git config core.hooksPath tests/hooks
```

Per-clone (git hooks aren't cloned). A failing commit is blocked with a message telling you what to
fix.

## Gotchas

Scope: this file covers the test suite specifically. Global policy is in the root
[`AGENTS.md`](../AGENTS.md) — see its **Doctrine** section, which this list puts into practice.

- **Check #4b asserts literal token strings.** It matches exact substrings inside
  `brain/integrations/connectors.md` and `brain/integrations/hosts.md` — so a copyedit that reworks
  those anchors (not just a deliberate behavior change) breaks the check silently until you run it.
  If you need to reword one, update the check's string in the same change.
- **A new functional file needs a `tests/behaviors.md` row, or check #17 rule 4 fails on add.** Same
  in reverse: a new eval scenario with no `behaviors=` is an orphan and fails rule 5.
- **Check #18 constrains the `mem-*-routing` fixtures.** For every scenario `MEM-54` cites, no
  `out_has` token may appear in that persona's always-load tier — `index.md` plus every file it links
  under `## Always load`. So adding a detail to an always-load page can fail the suite from the other
  side of the tree, and the fix is usually to assert a token that only the on-demand page carries.
- **Prove a new check fires before trusting it** — introduce the violation it's meant to catch, confirm
  it fails, then fix/revert and confirm it passes. A check that has never seen a real failure may be
  passing vacuously (this is doctrine item 4; checks 8b/8c/8d were each verified this way).
- **A green run here does not mean the site is green.** The website has its own repo and its own
  `tests/run.py`, covering the `/brain/` render, its three marketing surfaces, and the landing page's
  copy of the prompt boot. One rule spans both and is asserted separately on each side: no em-dashes
  in marketing copy. The prompt string used to as well; see `CONTRIBUTING.md` → The published prompt
  string for why it no longer does.
- **Prove the step, not the neighbour.** Verifying a workflow change in isolation proves only the step
  you changed. v0.26.0 published correctly and then died reopening the dev cycle: that step had never
  set a git identity, inheriting one for eleven releases from a neighbouring step that the site split
  moved into another repo. A dry run of the changed step passed; the broken one was downstream.
- **Several checks iterate git-tracked files, not the working tree.** Running `python3 tests/run.py`
  before `git add` leaves it blind to new or renamed files that aren't staged yet — it reports green
  while the thing you just added is invisible to it. Stage first, then verify.
