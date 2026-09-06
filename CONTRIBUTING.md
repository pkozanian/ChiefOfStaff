# Developing the Chief of Staff

Developer guide for working **on** the Chief of Staff. If you just want to *use* it, see [`README.md`](README.md).

The Chief of Staff is **pure markdown** — there's no application code to build or run. Its behavior is prose that
an agent tool (Claude Code, Codex) reads and follows. "Developing" it means editing that prose
and keeping the tests in sync.

## Mental model

**`src/` is the product. Everything else builds, tests, or publishes it.**

That split is load-bearing, so learn it first: `scripts/build-dist.sh` copies `src/` **verbatim** into
the ZIP. There is no ship-list to maintain — anything you put in `src/` ships to every executive, and
anything outside it cannot ship at all. To add a shipped file, put it in `src/` and teach
`src/brain/integrations/updates.md` to copy it (a test enforces that pairing, so an existing install
can never be left without a file the ZIP contains).

Because the trees are separate, **the shipped tree must never mention this one.** No links to
`CONTRIBUTING.md`, `tests/`, or `scripts/`; no explaining the product in git terms ("a fresh clone",
"git-ignored", "a `git pull`"). The user has a folder they unzipped, not a checkout. `tests/run.py`
enforces this (check 8b), which is why the entry-point router no longer needs to *detect* which tree
it's in — a bug that once offered "developer mode" to an executive.

Inside `src/`, two trees, never mixed:

- **`src/brain/`** — *what the Chief of Staff is*: role, principles, voice, playbooks, onboarding,
  schemas, integrations. **Shipped, versioned, and read-only at runtime.** Identical for every
  deployment. You develop here.
- **`src/memory/`** — *what it knows about one principal*: profile, people, projects, preferences,
  logs, the confidential registry. **Per-deployment and never committed** — the Chief of Staff reads
  and writes it at runtime. It exists in the source tree because `src/` is a complete, runnable
  install: **to try a change, open `src/` in your host**, not the repo root.

Boot: **`src/AGENTS.md`** is the entry point — read directly by Codex (in the ChatGPT desktop app) and
other `AGENTS.md`-aware tools, and by the Claude desktop app via a one-line `@AGENTS.md` import in
`src/CLAUDE.md`. It does one thing: hand off to **`src/CHIEFOFSTAFF.md`**, which holds the persona +
boot protocol (the single source of truth for *using* the Chief of Staff). Behavior goes in
`CHIEFOFSTAFF.md`/`brain/`, never duplicated.

Key conventions the brain relies on (see [`brain/schemas/memory-file.md`](src/brain/schemas/memory-file.md)):
- **Tiered index router** — `brain/index.md` and `memory/index.md` split `## Always load` vs
  `## Load on demand`; files load lazily by their hook.
- **Overrides overlay** — a deployment customizes brain behavior via `memory/overrides/` (mirrors
  `brain/` by path; `mode: replace|extend`) without editing `brain/`.
- **Confidentiality** — real↔code-name mapping lives only in `memory/confidential/registry.md`; code
  names everywhere else.

## Repo layout

```
src/                 # THE PRODUCT — copied verbatim into ChiefOfStaff.zip
  AGENTS.md          #   entry point: hands off to CHIEFOFSTAFF.md
  CHIEFOFSTAFF.md    #   persona + BOOT PROTOCOL (source of truth for using it)
  CLAUDE.md          #   one-line @AGENTS.md import (Claude desktop boot shim)
  VERSION            #   semver; `main` carries a `-dev` suffix between releases (see Releasing)
  CHANGELOG.md       #   release history + migration notes (read at boot)
  README.md          #   user-facing quick start + install
  brain/             #   role/ schemas/ onboarding/ playbooks/ integrations/
    index.md         #     the brain router (Always load / Load on demand)
  .claude/commands/  #   slash commands (/onboard, /lint, /explore, /routines, /update)
  .agents/skills/    #   the same commands as skills, read by Codex/Cursor/Gemini CLI/OpenCode/Copilot
  memory/            #   per-principal, never committed (only .keep is tracked)
                     # --- everything below is development scaffolding; none of it ships ---
AGENTS.md            # dev entry point: you're working ON Chief of Staff -> this file
CLAUDE.md            # one-line @AGENTS.md import
README.md            # repo landing page
CONTRIBUTING.md      # this file
.agents/personas/    # dev specialist reviewers (see "Agent capability" below) — versioned
.agents/skills/      # dev procedures (/release, /critique-loop) — versioned
.claude/agents, .claude/skills  # symlinks into .agents/ above (the repo's only tracked symlinks)
scripts/             # build-dist.sh (copies src/ into the exec release ZIP)
tests/               # structural suite + behavioral evals + behavior registry + fixtures
```

The **website** is a separate repo: **`pkozanian/chiefofstaff-site`**, serving chiefofstaff.team and
the public download at `/dist/`. It **pulls** a release from here when someone dispatches its own
`publish-release.yml`. Nothing in this repo writes to it, and check #15 keeps it that way.

That direction is the point: the site can only ever serve a release that exists here, and publishing
stays a decision someone makes rather than a side effect of tagging.

### Agent capability: `.agents/personas/` vs `.agents/skills/` vs `src/.claude/` + `src/.agents/skills/`

Two kinds of capability live at the repo root, both versioned like any other file here, under
`.agents/`; `.claude/agents` and `.claude/skills` are symlinks to them (see `AGENTS.md` → content vs
configuration):
- **`.agents/personas/`** — specialists (e.g. `brain-rigor-critic`, `brain-efficiency-critic`): a persona + lenses
  for judging or authoring one kind of thing, dispatched via the Agent tool.
- **`.agents/skills/`** — procedures (`/release`, `/critique-loop`): a repeatable multi-step workflow,
  invoked by name.

**`src/.claude/` and `src/.agents/skills/`** are unrelated — product: slash commands the executive's
agent runs (e.g. `/onboard`), shipped twice for host reach, plus, for `src/.claude/agents/`, generated
per-principal virtual-team shims. Both ship in the ZIP (`.claude/agents/` is stripped by
`build-dist.sh`); the root `.claude/` and `.agents/` never do.

## The develop loop

1. **Edit the brain.** Change behavior by editing the relevant markdown — voice in
   `brain/role/voice.md`, a workflow in `brain/playbooks/`, a rule in `brain/schemas/`, a host detail
   in `brain/integrations/`, etc. Follow the frontmatter + format in
   [`brain/schemas/memory-file.md`](src/brain/schemas/memory-file.md), and match the surrounding style.
2. **Run the structural suite** — fast, zero-dependency, and what CI enforces:
   ```
   python3 tests/run.py
   ```
   Editing a brain file needs no extra ceremony — the PR diff is the review. If you *add* or *remove* a
   functional file, name its behaviors in `tests/behaviors.md` (see **Keeping tests in sync**).
3. **(When it matters) run a behavioral eval** against the real agent — see below.
4. **Open a PR** (feature branch off `main`; structural must be green).

## Working with agents (model routing & delegation)

The Chief of Staff is developed *by* agents as much as by hand. What's worked well:

- **Route by model.** Plan and review on **Opus**; hand the actual edits to **Sonnet** subagents
  (Agent tool, `model: sonnet`); run behavioral evals on **Sonnet** too (`CHIEFOFSTAFF_EVAL_MODEL`, default
  `sonnet`). Opus decides *what*; Sonnet does the mechanical *how*.
- **Isolate parallel writers.** Subagents editing files at the same time need worktree isolation so they
  don't clobber each other; sequential subagents can share the tree. Shape a big plan so independent
  clusters run concurrently.
- **The delegation loop.** For open-ended improvement work: **summarize → critique → plan the
  medium/high items → delegate to Sonnet → verify with the tests → repeat** until nothing high-value is
  left. Keep each handoff small, verifiable, and additive.

## Authoring the brain — principles

The brain *is* behavior, so edits are prose with real stakes:

- **Additive by default.** Don't remove or weaken existing behavior; preserve the headings/anchors that
  tests and cross-references depend on. Changes accumulate under the current release (no per-feature
  version bump).
- **Target both desktop hosts.** Every behavior must work on **both** desktop apps — **Claude** (Claude
  Code / Claude Desktop) and **ChatGPT** (Codex). Never design, word, or document a feature for
  only one. Where a host's capabilities differ (connectors, scheduling, a shell), **degrade gracefully**
  and keep the host mapping in [`brain/integrations/hosts.md`](src/brain/integrations/hosts.md) accurate.
  Behavioral evals run under Claude Code, so when a change touches host-specific plumbing, sanity-check
  the Codex path against `hosts.md` / [`brain/integrations/connectors.md`](src/brain/integrations/connectors.md).
- **Honesty guardrails.** Never write a claim you can't ground; when the data or context is thin, **say
  so and skip** rather than force a generic-sounding line. This holds for the product too — every
  onboarding "moment" must trace to real data or the stated role.
- **Bump `updated:` on every memory-file touch** (create *or* edit), and hold unconfirmed inferences as
  labeled **hypotheses**, promoting them only once confirmed — see
  [`brain/schemas/capture-rules.md`](src/brain/schemas/capture-rules.md) and
  [`brain/schemas/memory-file.md`](src/brain/schemas/memory-file.md).
- **Reachability & confidentiality.** Every memory file must be reachable by link from the root
  `memory/index.md` (only a team member's generated boot files are exempt); confidential subjects use
  code names only, with the registry linked exactly once — see
  [`brain/schemas/confidentiality.md`](src/brain/schemas/confidentiality.md).
- **Migration directive for memory-affecting changes.** If a change alters what valid memory looks
  like — a schema/format convention, the folder layout, a renamed or removed brain file that
  overrides may mirror — add (or extend) a **`### Migration notes`** block at the top of
  `CHANGELOG.md` → `## [Unreleased]`, above `### Added`. Say explicitly what happens to an
  **existing** `memory/` tree, and make each note **actionable** so the migration pass can apply it,
  classified as one of: **no action required** (stays valid as-is / converges lazily — name which lint
  check; treated as non-blocking), a **required** step the pass performs, or a pointer to a
  **versioned migration** playbook — and say explicitly **whether it writes at boot**, since that is
  what decides if it belongs in the migration proposal the pass shows the principal (e.g. `brain/playbooks/team.md` → "Migrate a pre-roster team", also
  required). This block is not decoration — the **first-boot migration pass**
  (`brain/integrations/updates.md` → "Applying memory migrations", run from `CHIEFOFSTAFF.md` boot
  step 2 when `onboarded_against` < `VERSION`) reads the notes for the spanned releases and
  **applies** them, then advances `onboarded_against`. Use the `### Migration notes` heading going
  forward; the pass also tolerates the legacy `### Migration` block and inline `**Migration:**`
  statements used by older entries. A memory-affecting change without a note ships a silent migration.

  **The block's shape.** Three parts; only the first is required.

  1. **A classification line** — first, bold, one of exactly four. `tests/run.py` check #5 matches
     them literally, and the dash is an em-dash:

     | Line | Means | In the principal's proposal? |
     |---|---|---|
     | `**No action required.**` | Nothing to do; existing memory stays valid. | No |
     | `**Required — writes at boot.**` | The pass changes the principal's own content. | **Yes** — nothing written until they agree |
     | `**Required — no write.**` | The pass must act, but not on principal content: regenerating a specialist's generated boot files, deleting a dead shim, backfilling a detected `meta:` field. | No |
     | `**Optional convergence.**` | Offer a `/lint` pass; non-blocking. | Offered, not proposed |

  2. **Prose** — free-form, human-facing, unchanged in style from today.

  3. **Subject-keyed bullets**, on anything actionable. Key is `<scope>:<name>`, scope one of
     `charter` · `meta` · `frontmatter` · `path` · `preference` · `member` · `override`.

  **Bullets state an end state, not a delta.** This is what makes the ordered walk correct from any
  starting version. "Remove the `## Reads` section" is wrong; "a charter carries neither a `reads:`
  field nor a `## Reads` section — its pointers live under `## Key context`; convert or remove
  whichever is present" is right.

  **Supersession is forward-only.** When a release changes something an earlier release migrated, the
  **later** entry carries `**Supersedes X.Y.Z.**` on the relevant bullet. Never reach back and edit
  the earlier entry. Version order decides; the marker states intent and is checked.

  **A versioned migration must be idempotent** — re-running it on already-migrated memory is a no-op.
  The pass keeps no per-release record: `onboarded_against` advances only once *every* required step
  in the span is done, so a principal deferring one step re-runs the whole span next boot.
  Idempotency is what makes that safe, and nothing enforces it but this line.

  **Accepted tradeoff.** `brain/integrations/updates.md` still tells the pass to skim the release
  entries themselves, not only their blocks. That is redundant once every entry carries a block, and
  it costs context on a wide upgrade. It is kept deliberately as defence in depth, because the class
  of bug it guards against shipped twice — 0.15.0 and 0.18.0 — before anyone noticed.

## Running the tests

Full detail is in **[`tests/README.md`](tests/README.md)**. The essentials:

| Command | What it does |
|---|---|
| `python3 tests/run.py` | Structural suite — frontmatter, index, links, naming, version, behavior registry + eval integrity. Fast, no deps, runs in CI on push. |
| `python3 tests/eval/run_eval.py --dry-run` | Exercise eval plumbing **without** calling the agent (no tokens). |
| `python3 tests/eval/run_eval.py --only <key>` | Run one behavioral scenario live (needs the `claude` CLI + auth). |
| `python3 tests/eval/run_eval.py --filter mem-` | Run the memory-retrieval suite (deep fixtures; token-costly). |
| `python3 tests/eval/run_eval.py --retries 1` | Re-run a scenario to absorb non-determinism. |

- **Structural** is deterministic and gates every push (`.github/workflows/tests.yml`).
- **Behavioral evals** run the real `claude -p` in a throwaway repo copy and assert on the output —
  non-deterministic, need auth, **local/on-demand only** (`.github/workflows/eval.yml` is dispatch
  only, never on push or a schedule). Start with `--dry-run`.
- Optional: run the structural suite before every commit with `git config core.hooksPath tests/hooks`.

### Eval discipline
- Behavioral evals need the **`claude` CLI and an authenticated session — no `ANTHROPIC_API_KEY`**. The
  harness shells out to `claude -p`, so it runs under your logged-in session (works headless wherever the
  CLI is authed).
- After a brain change, run the **impacted subset** — find the file in the `Stated in` column of
  `tests/behaviors.md`; its rows name the scenarios. Rows are per behavior, so finer-grained than the
  file: `onboarding/flow.md` names `onboard`, `onboard-personal` and `onboard-ic`, while `defaults-keep`
  and `defaults-change` sit on `onboarding/steps/5-working-preferences.md` — check the steps too.
- **Sonnet is non-deterministic — re-run a red once (`--retries 1`) before calling it a regression.** A
  scenario that fails then passes was a flake; an *unrelated* scenario failing is a strong flake signal.
  Structural gates every change; run the impacted evals once **before merging** a brain change.

### Keeping tests in sync (the behavior registry)
`tests/behaviors.md` holds one row per behavior the product promises: the `src/` file that states it,
and the tests that cover it. Check #17 asserts the citations are an exact transpose both ways, that
every functional file is some row's `Stated in`, that no eval scenario is an orphan, and that the
file's own summary table still counts the rows (add a row, update the table). An **empty
`Covered by` is legal** — an untested behavior, counted and printed every run. Content *changes* are
not gated; the PR diff is the review. See `tests/README.md` → "Keeping tests in sync with the brain".

## Recipes

- **Add a playbook** → create `brain/playbooks/<name>.md` (frontmatter, `type: playbook`), list it in
  `brain/index.md`, add its `tests/behaviors.md` rows, and (optionally) an eval scenario.
- **Add a slash command** → `.claude/commands/<name>.md` (with `description`) **and** its neutral
  counterpart `.agents/skills/<name>/SKILL.md` (check 7b / `REPO-36` fails without both; `REPO-38`
  asserts the two bodies match), plus its registry rows.
- **Add an eval scenario** → add a `Scenario` to `tests/eval/scenarios.py`, set its `behaviors=`, and
  **cite its key** from those `tests/behaviors.md` rows (the orphan guard fails otherwise).
- **Add a memory-retrieval fixture persona** → a new tree under `tests/fixtures/memory/<persona>/`
  (test data — exempt from the structural checks) + `mem-<persona>-*` scenarios + their registry rows.
- **Change/add a default the principal can tune** → `brain/role/defaults.md`, with its override
  target under `memory/overrides/`.

## Releasing

The Chief of Staff ships to executives as a **GitHub Release ZIP** (`ChiefOfStaff.zip`), and the running Chief of Staff
**self-updates** from it (`brain/integrations/updates.md`).

**`main` carries a `-dev` pre-release VERSION** (e.g. `0.12.0-dev`) so it's honestly marked *ahead of the
last release* — end users only ever get clean released builds. Cutting a release drops the suffix and tags
the clean number; the release workflow then reopens the next `-dev` automatically. To cut a release:

1. **Land everything on `main`** with structural green.
2. **Turn the dev version into a release.** In one PR: drop the `-dev` suffix in `src/VERSION` (e.g.
   `0.12.0-dev` → `0.12.0`); in `src/CHANGELOG.md`, rename the top `## [Unreleased]` section to
   `## [x.y.z] — title` **and add a fresh `## [Unreleased]` above it, carrying a `### Migration notes`
   block that reads `**No action required.**`** (structural check #5 wants `[x.y.z]` for a clean
   VERSION, `## [Unreleased]` for a `-dev` VERSION, and a migration block on **every** entry —
   including the one you just opened). Brain files carry **no**
   per-file `version:`, so this is a small mechanical edit; run
   `python3 tests/run.py` → green and merge.
3. **Tag it** — the tag must match `VERSION` (the workflow verifies this, and refuses a `-dev` VERSION):
   ```bash
   git checkout main && git pull
   git tag vX.Y.Z && git push origin vX.Y.Z
   ```
4. **The `release` workflow** (`.github/workflows/release.yml`) fires on the `v*` tag: it verifies the
   tag matches a clean `VERSION`, runs the **structural suite** (a release is permanent — it should
   never be cut from a red tree), runs `scripts/build-dist.sh`, and **publishes the GitHub Release**
   with both archives + `src/VERSION` + `src/CHANGELOG.md` attached and the
   CHANGELOG section as its notes. It authenticates with the built-in `GITHUB_TOKEN`.

   Build it locally to inspect: `bash scripts/build-dist.sh` → `dist/ChiefOfStaff.zip`. (The workflow
   can also be re-run from the **Actions** tab; pick the `vX.Y.Z` tag as the ref — but only a tag from
   `v0.28.0` on, since a dispatch runs the workflow as it existed at that ref. It is re-runnable: an
   existing Release is edited in place rather than treated as an error.)

   **Then reopen the next dev cycle yourself:** bump `src/VERSION` to `<next-minor>-dev` and add a
   fresh `## [Unreleased]`. A workflow used to do this; it no longer does, and nothing will remind
   you. Leaving `VERSION` on a clean number makes the next release's pre-flight look like there is
   nothing to release.
5. **Publish it.** **The release is not live yet.** Nothing above touches the site — that step is a
   deliberate act performed in the site repo, which *pulls* the release:

   ```bash
   gh workflow run publish-release.yml --repo pkozanian/chiefofstaff-site -f version=vX.Y.Z
   ```

   It downloads three of the Release's four assets — `cos.zip`, `VERSION`, `CHANGELOG.md` — checks
   them (VERSION matches the tag, the zip opens and is the flat shape `/update` expects), commits
   `public/dist/` in one commit, and dispatches the site's deploy. Passing an **older** tag is the
   rollback.

   The exec download and in-app `/update` are **anonymous** and resolve from the site's `public/dist/`
   — public even while this repo is private. The URLs baked into the brain
   (`https://chiefofstaff.team/dist/…`) are already the public ones.

   **This is the state to watch for:** a Release published here, and users still on the previous
   version because nobody dispatched the publish. Nothing detects it. Verify with the live-endpoint
   checks in the `/release` skill, not with any workflow's exit code.

### Credentials

`release.yml` publishes a Release in this repository, so it authenticates with the built-in
`GITHUB_TOKEN` and needs no secret of its own. Two things it does NOT do, both deliberate: it does not
write to the website (check #15), and it does not carry a cross-repo credential.

The one secret worth knowing about lives in the **website** repo, not here:
`CHIEFOFSTAFF_RELEASE_READ_TOKEN`, a fine-grained PAT scoped to this repository with
**`Contents: read`** only. That is what lets the site download a release's assets to publish them.
Read-only is correct — the site never writes here, and the name says so, because the next person
deciding what to grant a replacement will read the name before they read this paragraph.

`eval.yml` needs `CLAUDE_CODE_OAUTH_TOKEN` if you dispatch it. Nothing else does.

Fine-grained PATs **expire**, and an expired one fails with a 403 that looks like nothing else. Note
the renewal date when you create one. If that becomes annoying, a GitHub App installation token does
not expire and is the intended replacement.

### The published prompt string

The one-line prompt boot — `Install https://chiefofstaff.team` — is a **published interface**. It gets
pasted into chats and shared, so copies of it survive in places neither repo can reach.

It is stated twice: in `README.md` here, and on the landing page in the site repo. **Nothing pins the
two together, deliberately.** A `prompt-boot.txt` at this repo's root used to be the single copy both
derived from, published as a release asset that the site's suite asserted its landing page against. That was removed in 2026-08 and
the reasoning is worth keeping, because the arrangement looked principled right up until its premise
expired:

- The pin was built when the prompt named a **versioned archive URL**. The failure it existed to catch
  was a stale paste installing an old archive from a URL that still resolved. Real, and worth a check.
- The prompt now names only the site, which serves whatever is current. A stale paste of an older
  wording fetches the same page as a fresh one, so that failure can no longer happen.
- The cost stayed. Because the site could only see the string through a release asset, rewording one
  sentence required cutting a product release — a version bump, and an `/update` prompt for every
  install, to ship a brain byte-identical to the one before it.

**The accepted tradeoff:** the two copies can now drift, and nothing will tell you. Both resolve to the
same page, so drift is cosmetic rather than functional. Reword the prompt and you must change both by
hand — here, and `index.astro` in the site repo.

### Two archives, and why

The build publishes the same release twice:

| | |
|---|---|
| **`cos.zip`** | **The one to use.** Flat: unzips its contents straight into the folder the principal is already in. This is what the prompt boot and `/update` fetch. |
| **`ChiefOfStaff.zip`** | **Compatibility bridge.** The same files wrapped in a `ChiefOfStaff/` directory. Installs predating 0.20.0 run an `/update` recipe that hardcodes `$tmp/ChiefOfStaff`, and that recipe lives in the brain **already on their disk**, so it cannot be corrected remotely. |

The bridge drains itself: an old install updates once through `ChiefOfStaff.zip`, receives the new
brain (whose recipe points at `cos.zip`), and is on the current path from then on.

**The site already stopped mirroring it.** `publish-release.yml` pulls only `cos.zip`, `VERSION`, and
`CHANGELOG.md`, so the published `ChiefOfStaff.zip` is frozen at whatever release last wrote it and no
longer moves when you cut one. It is still served so the URL resolves, and it is still post-0.20.0, so
the bridge still drains — but a release does not refresh it, and no live check of that URL says
anything about the release you just cut. Re-adding the pattern there would silently un-retire it.

This repo still builds and attaches both: `tests/run.py` check 8d asserts the two shapes and that
their contents are identical. **Drop `ChiefOfStaff.zip` from `build-dist.sh` and `release.yml` once
you're satisfied no install is still on a pre-0.20.0 brain.**

**The prompt is a published interface.** It appears on the landing page with a copy button and
gets pasted into chats and shared. Changing its wording, or the `cos.zip` URL, breaks instructions
already in the wild — treat both as stable.

## The website, and where the download comes from

Both live in a separate repo: **`pkozanian/chiefofstaff-site`**, which serves chiefofstaff.team from
GitHub Pages and carries the release mirror at `/dist/`. The split exists because the two projects
have nothing in common mechanically: this repo is markdown with zero dependencies, that one is an
Astro app with ~200 packages.

**It pulls from the official repo; this repo never writes to it.** Its `publish-release.yml` (manual
dispatch, a tag or `latest`) downloads a release from `pkozanian/ChiefOfStaff`, verifies it, commits
`public/dist/`, and dispatches its own deploy. So publishing is a decision someone makes over there,
separate from releasing — and dispatching an older tag is the rollback.

What still matters from this side:

- **The `/dist/` URLs are frozen.** `https://chiefofstaff.team/dist/cos.zip` and its siblings are
  baked into `brain/integrations/updates.md` inside every install already on a principal's disk, and
  cannot be corrected remotely. `cos.team/dist/cos.zip` is the same file under the older domain and
  is the URL in the prompt boot. Only that repo's publish workflow writes those files.
- **The shipped `README.md` hotlinks the site's logo** and deep-links `chiefofstaff.team/#training`.
  An asset rename over there breaks a README already in the field, so that repo treats
  `public/assets/` as a product dependency.
- **`overview.md` lives there**, and its citations resolve against the released zip. A brain file
  renamed here fails that repo's build until the citation is updated. That is deliberate: it is how a
  published summary stays honest about a corpus it does not own.
- **No em-dashes in `src/README.md`** — house style for the public marketing surfaces. Structural
  check 13 enforces it here; the site's own suite covers its three. Use commas for simple joins, a
  period to split independent clauses, a colon for a "label: detail" lead-in, parentheses for a true
  aside. The **root** `README.md` is the repo landing page, not marketing copy, so it is exempt like
  the other dev docs.

Visual verification (nine widths, both themes, overflow and contrast gates) moved with the site; see
that repo's `AGENTS.md`.

## Conventions

- **Version** — `main` carries a `-dev` semver (e.g. `0.12.0-dev`); accumulate notes under
  `## [Unreleased]`. Don't bump per feature. Cutting a **release** drops the suffix + renames
  `## [Unreleased]` → `## [x.y.z]`, then tags `vX.Y.Z` (see **Releasing**); the workflow reopens the next
  `-dev`. Brain files carry no per-file version.
- **Never write to `brain/` from a running session** — capture only ever writes to `memory/`.
  **Never commit `memory/`** (it's git-ignored).
- **Integrity — never weaken a check to make it pass.** If a test fails, fix the fixture or the brain
  and keep the test's intent; don't loosen or delete the assertion. Do not cheat.
- **Git** — keep structural green before anything lands. CI = `tests.yml` (structural, on push) +
  `eval.yml` (behavioral, dispatch only).
- **Merging** — don't merge without the principal's explicit OK; open the PR and hold it for review.
- **Stacked PRs** — base a child PR on its parent branch. Squash-merging the parent **deletes that branch
  and auto-closes the child**; rebase the child onto `main` (`git rebase --onto main <parent-tip>`),
  force-push, and open a fresh PR to `main`.
- **Don't rewrite history in `CHANGELOG.md`** — past release entries are a record; new work gets a new
  entry. **One carve-out, and only this one:** you may **add** a `### Migration notes` block to an
  entry that shipped without one, and **annotate** an existing block with a classification line and
  subject-keyed bullets. You may **not** edit a release's own account of what it did, and you may
  **not** move a block that is already there. A backfilled block closes with an italic line saying it
  was backfilled and from which diff, so the record stays honest about which sentences are
  contemporary and which are not.

## Pointers
- [`tests/README.md`](tests/README.md) — the full test guide.
- [`brain/index.md`](src/brain/index.md) — what the brain contains and when each file loads.
- [`brain/schemas/memory-file.md`](src/brain/schemas/memory-file.md) — the memory-file format + layout.
- [`brain/integrations/hosts.md`](src/brain/integrations/hosts.md) — how the Chief of Staff maps onto each host.
- `pkozanian/ChiefOfStaff` — the official release repo, release-only history (see **The official
  release repo**).
- `pkozanian/chiefofstaff-site` — the website and the release mirror (see **The website, and where
  the download comes from**).
- [`CHANGELOG.md`](src/CHANGELOG.md) — what's changed.
