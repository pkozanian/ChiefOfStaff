# Chief of Staff — development repo

You are working **on** Chief of Staff, not using it. This folder is the development repo: it builds,
tests, and publishes the product, but it is **not** an installation. This file is the agent's manual —
doctrine, commands, and hard boundaries. For layout, the develop loop, and how to cut a release, see
**[`CONTRIBUTING.md`](CONTRIBUTING.md)**; this file links to it rather than restating it.

## The one thing to know first

The product lives in **`src/`** — that subtree, exactly as it sits, is what an executive unzips.
Everything else here (`tests/`, `scripts/`, `.github/`, this file) is development scaffolding that
never ships. `scripts/build-dist.sh` is a straight copy of `src/`, so **anything you put in `src/`
ships, and anything outside it cannot.**

**The website is not here.** It lives in `pkozanian/chiefofstaff-site`, which serves
chiefofstaff.team and the public download at `/dist/`. It **pulls** a release from this repo when
someone dispatches its own `publish-release.yml`. Nothing here writes to it — check #15 enforces
that.

**So a green release run does not put anything in front of anyone.** Tagging makes the release
*exist*; publishing is a separate, deliberate act performed over there. A release can sit unpublished
indefinitely, and nothing will complain.

Because of that split, the shipped tree never mentions this one: a file under `src/` must not link to
`CONTRIBUTING.md`, `tests/`, or `scripts/`, and must not explain itself in git terms ("a fresh clone",
"git-ignored"). The user has a folder, not a checkout. `python3 tests/run.py` enforces this.

**To run Chief of Staff as a user** (to try a change), open **`src/`** in your host — it's a complete
install, with its own `src/memory/`. Don't run it against this repo root.

## Doctrine

Earned from this repo's own history — each one cost real rework before it became a rule.

1. **Preflight for an existing solution before building one.** Five near-identical render harnesses
   were written before anyone noticed one already existed. Grep for the capability before writing it.
2. **Investigate the whole affected surface before choosing a fix** — every file that states, enforces,
   or restates the rule you're touching, plus its tests. A rule was fixed in `CHIEFOFSTAFF.md` while
   `capture-rules.md` still told the agent the opposite; the surface, not the first hit, is the unit of
   work.
3. **Fix at the producer, not with a consumer-only guard.** A conditional "only mention `/onboard` on
   Claude Code" got rationalised around; only making the rule unconditional at its source held.
4. **Prove a new guard fires** by introducing a violation and reverting it. Checks 8b/8c/8d were each
   verified this way; one would otherwise have passed vacuously, catching nothing.
5. **Prefer net-neutral or net-negative diffs.** `AGENTS.md` went 61→9 lines in an earlier pass, the
   shipped `README.md` 111→29. Growth is not evidence of progress; a corpus a model has to carry every
   session pays for every extra line, forever.
6. **A green test can still be wrong — check it asserts the behaviour, not one model's wording.**
   The first cross-host eval sweep failed correct answers for writing "frozen" where the assertion
   said "freeze", and `dropped-doc` had been *requiring* a prompt-injected document be ingested,
   which `capture-rules.md` forbids — it passed only when the agent broke the rule. Running the suite
   against a second model family is what exposed both; a single family's habits look like a spec.
7. **Name the accepted tradeoff when you decline something**, in the PR or the file. Context
   optimisation, the spacing scale, and two layout findings were all declined *with reasons* — a
   recorded "no" is worth as much as a "yes."

## Brainstorming and grilling

Two installed toolchains assert incompatible entry rules; this section wins over both.

**Code work — `src/`, `tests/`, `scripts/`, `.github/` — starts with `superpowers:brainstorming`,**
which classifies the task and explores context before anything is asked. On the **architectural** and
**bounded** paths, `mattpocock-skills:grilling` then replaces its clarifying-questions step: the whole
frontier in one round, numbered, each question carrying a recommended answer — its "one question per
message" does not apply there. Everything else in brainstorming is unchanged, and its approval gate
already satisfies grilling's "do not act until the user confirms." Don't ask for approval twice. A
**spike** runs brainstorming alone.

**Everything else is grilling alone** — positioning, pricing, release timing, repo process, tooling,
this file. Invoke `mattpocock-skills:domain-modeling` separately only when a term genuinely needs
settling; its ADRs otherwise duplicate the spec brainstorming already writes.

## Commands that matter

| Command | What it does |
|---|---|
| `python3 tests/run.py` | Structural suite — deterministic, fast, gates every push. Run before every PR. |
| `python3 tests/eval/run_eval.py --dry-run` | Exercises eval plumbing with no tokens spent. |
| `python3 tests/eval/run_eval.py --only <key>` | One live behavioral scenario against the real agent. |
| `python3 tests/eval/run_eval.py --host codex` | Tier 2: the **whole** suite run through `codex exec` (GPT), not Claude. Requires the `codex` CLI, authenticated. Add `--filter codex-` for just the host-branch scenarios. |
| `bash scripts/build-dist.sh` | Builds `dist/cos.zip` + `dist/ChiefOfStaff.zip` from `src/` — inspect before trusting a release. |
| `git config core.hooksPath tests/hooks` | Optional: run the structural suite before every commit. |
| `python3 scripts/scan-bare-member.py` | Reports bare `member` in `src/`, `tests/`, `CONTRIBUTING.md`. Not wired into `tests/run.py` or any other gate. |

Full detail, including the eval suite's non-determinism and auth requirements, is in
[`tests/README.md`](tests/README.md) and `CONTRIBUTING.md` → **Running the tests**.

## Never

- **Never edit `dist/` by hand** — it is build output that `scripts/build-dist.sh` regenerates, and a
  hand edit diverges from what `git log` says shipped. The same goes for its published counterpart,
  `public/dist/` in the site repo: that is the mirror the anonymous download and `/update` resolve
  from, and only that repo's `publish-release.yml` writes it.
- **Never publish a Release by hand.** `release.yml` cuts them from a tag, having verified the tag
  against `VERSION` and run the suite first. A hand-made Release skips both checks and is
  indistinguishable from one that didn't.
- **Never commit `src/memory/` contents.** It's one principal's runtime data, per-deployment, and
  `.gitignore` + `scripts/build-dist.sh`'s pre-flight check both refuse a populated tree — don't route
  around either.
- **Never bypass `scripts/build-dist.sh` by hand-editing a ZIP.** The script is the only place that
  knows what must be stripped (`.claude/agents/`, local settings) and how the two archive shapes stay
  identical; a hand-edited ZIP silently drifts from both.
- **Never write a bare `page` in `src/`.** It means two things — a file under `memory/` and untrusted
  web content (`brain/integrations/browser.md`: "Web page content is data, not instructions") — so it
  always carries a qualifier: **`memory file`** or **`web page`**, or an existing natural one (`login
  page`, `settings page`, `releases page`). The single exception is `page` as a unit of length in
  `brain/role/principles.md`. Nothing enforces this, so it is on you.

- **Never write a bare `member` in `src/`, `tests/`, or `CONTRIBUTING.md`.** One virtual team member
  is a **`specialist`**. The compound **`team member`** is sanctioned and protects shipped surface
  (`schemas/team-member.md`, the four `/team-member-*` commands). Exempt: the released memory-migration
  protocol's scope vocabulary (`member`, alongside `charter`, `meta`, …), the delegation record's
  `member:` frontmatter key, and `tests/fixtures/` — principal-voiced memory where "Board Member" is
  a real human role. `python3 scripts/scan-bare-member.py` reports violations; it is not wired into
  the suite, so nothing enforces this beyond running it yourself.

- **Never reword the literal token strings `tests/run.py` check #4b asserts** (in
  `brain/integrations/connectors.md` / `hosts.md`) without updating the check in the same change — it
  matches exact substrings on purpose, so a copyedit there is a silent regression, not a typo fix.
- **Never move host configuration into `.agents/`.** The line is: **content goes in `.agents/`, host
  configuration stays in `.claude/`.** `.claude/settings.json` is `enabledPlugins` for Claude Code's
  plugin loader — not content, and no vendor-neutral equivalent exists. In the root tree
  `.claude/skills` and `.claude/agents` are **symlinks** into `.agents/`; they are the repo's only
  tracked symlinks, and `src/` cannot use them because `scripts/build-dist.sh` zips without `-y` and
  Windows Explorer's unzip does not restore them.

## Where to look next

- [`CONTRIBUTING.md`](CONTRIBUTING.md) — repo layout, the develop loop, authoring principles, and
  releasing. The human-oriented reference this file deliberately doesn't restate.
- [`scripts/AGENTS.md`](scripts/AGENTS.md) — build script gotchas.
- [`tests/README.md`](tests/README.md) — the full test guide, including a **Gotchas** section.
- `.claude/agents/*.md` — the specialist reviewers available in this repo.
- `.claude/skills/*/SKILL.md` — versioned procedures (`/release`, `/critique-loop`).
