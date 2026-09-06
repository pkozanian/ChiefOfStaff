---
name: release
description: "Cut a Chief of Staff release end to end: pre-flight sanity on the CHANGELOG, the version bump, tag, workflow watch, the manual fallback for when GitHub Actions stalls, and live-endpoint verification. Use when asked to cut/create a release, publish a version, or ship what's on main."
---

# /release

Cut a release of Chief of Staff. Six were cut by hand in one session and **a different thing went
wrong nearly every time** — this encodes the checks that would have caught each one.

```
/release              # cut the next version from what's on main
/release 0.21.1       # cut an explicit version (e.g. a patch)
```

**Needs `gh` and `zip` on PATH** (`gh` for PR/release/deploy recovery; `zip` via
`scripts/build-dist.sh`). Confirm both resolve before starting: `command -v gh zip`.

**Runs in the repository that publishes Releases** — `release.yml` is pinned to it by name and starts
on nothing else, so a tag pushed from anywhere else produces no run and the by-hand fallback in step 4
would cut a Release in the wrong place. Confirm first: `git remote get-url origin`.

## Read First

Before touching anything, load: `src/VERSION` and the live published version
(`curl -s https://chiefofstaff.team/dist/VERSION`), the whole `## [Unreleased]` section of
`src/CHANGELOG.md`, `gh pr list --state open`, and `CONTRIBUTING.md` → **Releasing** (the source of
truth this skill encodes — if the two disagree, the doc wins and this skill is stale).

## Repo assumptions (verify before trusting this skill)

Written for this repository. It assumes:
- the product tree is **`src/`**, so the version is **`src/VERSION`** and notes are **`src/CHANGELOG.md`**
- `main` carries `X.Y.Z-dev` between releases; cutting one drops the suffix, and **reopening the next
  `-dev` is a manual edit** — no workflow does it for you
- `scripts/build-dist.sh` emits **`dist/cos.zip`** (flat, current) and **`dist/ChiefOfStaff.zip`**
  (nested, for installs predating 0.20.0). Both go on the Release, but **the site mirror pulls only
  `cos.zip`, `VERSION`, and `CHANGELOG.md`** — the published `ChiefOfStaff.zip` is frozen at whatever
  release last wrote it, still served so the URL resolves, and does not move when you cut a release
- `release.yml` fires on the `vX.Y.Z` tag and publishes the **GitHub Release here**, using the
  built-in `GITHUB_TOKEN` — no secret of its own, nothing cross-repo
- **tagging does NOT put the release in front of anyone.** The site pulls it on a separate manual
  dispatch (step 5). Until then the download and `/update` serve the previous version
- the public download and in-app `/update` resolve from **`pkozanian/chiefofstaff-site`**'s
  `public/dist/`, served at chiefofstaff.team, not from GitHub Releases

**If any of those don't hold, stop and re-read `CONTRIBUTING.md` → Releasing rather than improvising.**

## 1. Pre-flight — these are the checks that caught real bugs

Run all of it before touching anything. Report what you find; don't silently fix.

```bash
git checkout main && git pull --ff-only
cat src/VERSION                                    # must end in -dev
curl -s https://chiefofstaff.team/dist/VERSION     # what users currently resolve
gh pr list --state open                            # should be empty; if not, ask before proceeding
python3 tests/run.py                               # must be green

gh release view --json tagName --jq .tagName       # the last release CUT — the diff baseline
```

**The baseline for every diff below is the last release *cut*, not the live version.** A release cut
but never published leaves the two apart, and diffing from what users resolve then re-lists work that
already shipped. Each command below re-resolves it rather than reusing a variable, because a shell
variable does not survive from one block to the next.

Then **read the whole `## [Unreleased]` section** and check it like an editor, because these all
shipped or nearly shipped:

- **Duplicate `###` headings.** Separate PRs each append their own `### Changed`, so the section ends
  up with two or three. Consolidate into one **Added / Changed / Fixed** sequence, in that order.
- **Stale migration notes.** A note written early in the cycle can be falsified by a later PR. A note
  saying "nothing about your folder changes" shipped in a release that *changed the archive shape*.
  Re-read every note against what actually landed.
- **Stale overview.** `overview.md` in the **site repo** is the plain-language summary of the brain,
  and the site re-renders `/brain/` from the zip this release publishes. Re-read it against the
  release diff: a summary that no longer matches a renamed section or changed behavior ships as
  published misinformation. A citation naming a brain file this release *removed* is worse — it fails
  that repo's build, so the site stops deploying until someone fixes it. Check before tagging.
- **Missing migration notes.** If anything altered what valid `memory/` looks like, or added/renamed a
  shipped file, `CONTRIBUTING.md` requires a `### Migration notes` block — and the first-boot migration
  pass *reads* it. No note = a silent migration.
  The block must open with one of the four classification lines and carry a subject-keyed bullet for
  anything actionable — `tests/run.py` check #5 enforces both, on every entry. If this release
  changes something an earlier release migrated, say `**Supersedes X.Y.Z.**` on that bullet rather
  than editing the earlier entry.
- **Backfill annotations naming the wrong version.** The italic `_Backfilled in X.Y.Z …_` /
  `_Migration position corrected in X.Y.Z …_` lines hardcode the release that did the backfill, and
  nothing ties them to `VERSION`. The ones 0.30.0 wrote are history and must keep saying 0.30.0 —
  only annotations *this* release adds are at risk, and they all go false at once if it is
  renumbered. List them and check the ones inside the section you are about to name:
  `grep -n '_Backfilled in\|_Migration position corrected in' src/CHANGELOG.md`
- **`_Nothing yet._`** left behind above real entries.

Cross-check the entries against what actually merged:
```bash
git log --oneline "$(gh release view --json tagName --jq .tagName)..main" -- src/
```
An entry with no commit, or a commit with no entry, is a finding.

**Then make the migration call with the diff in front of you.** `tests/run.py` check #5 now refuses a
clean `VERSION` whose section has no `### Migration notes` block, so you cannot ship without stating a
position — but it can't tell you whether "No action required" is *true*. Look before you write it:

```bash
git diff --name-only "$(gh release view --json tagName --jq .tagName)..main" \
  -- src/brain/schemas/ src/brain/onboarding/
```

Anything listed there shapes what a valid `memory/` contains. If a field was renamed or removed, a file
moved, or a convention retired, an existing folder has the old shape and the note must say what happens
to it. **0.15.0 removed the per-member `clearance:`/`## Reads` charter fields with no note at all** —
the first-boot pass migrated straight past it, and that is the failure this step exists to prevent.

## 2. Ask for the title

The heading is user-facing. **Ask** with 2-3 concrete options (AskUserQuestion), each previewed as the
literal `## [x.y.z] — title` line. Lead with the dominant user-visible theme, not the biggest diff.

## 3. Cut it

```bash
git checkout -b release-X.Y.Z
```
- `src/VERSION`: drop `-dev`
- `src/CHANGELOG.md`: rename `## [Unreleased]` → `## [X.Y.Z] — title`, add a short intro paragraph
  saying what changed *for a user*, and open a fresh `## [Unreleased]` above it containing
  `_Nothing yet._` **and a `### Migration notes` block reading `**No action required.**`** — check #5
  is total, so an entry with no block fails the suite the moment you open it. Opening the block with
  the cycle is the point: a change that alters what a folder should look like has to state its
  position as it lands, not be remembered at release time. Update the `-dev` example in the
  boilerplate to the next version.
- `python3 tests/run.py` → green. Structural check #5 wants `[x.y.z]` for a clean VERSION.
- House style: structural check 13 refuses an em-dash in `src/README.md`; the site repo asserts its own three surfaces.

Commit, open a PR, merge it, then tag:
```bash
git checkout main && git pull --ff-only
git tag vX.Y.Z && git push origin vX.Y.Z
```
The tag must match `src/VERSION` exactly; the workflow refuses a `-dev` version.

## 4. Watch the workflow — and know its failure mode

```bash
gh run list --workflow=release.yml --limit 1
```
Poll until `completed`. **A tag push that produces no run at all is the common failure** (it happened
for three consecutive releases during a GitHub incident). Don't wait indefinitely; if no run appears
within ~1 minute, **re-check the precondition above before assuming an incident** — a tag pushed to a
repository `release.yml` is not pinned to fails exactly this way, every time. Then go to the fallback.

### Fallback: publish by hand

Build the archives and create the Release yourself. Everything the workflow would have done, minus
the checks — so run those first, by hand, rather than skipping them because Actions is down:

```bash
cat src/VERSION                      # must equal X.Y.Z, with no -dev suffix
python3 tests/run.py                 # the workflow gates on this; so should you
bash scripts/build-dist.sh

gh release create vX.Y.Z dist/cos.zip dist/ChiefOfStaff.zip src/VERSION src/CHANGELOG.md \
  --title "$(bash scripts/changelog-section.sh --title X.Y.Z)" \
  --notes-file <(bash scripts/changelog-section.sh X.Y.Z)
```

Publishing is step 5 either way — by hand or not, the site still has to be told to pull.

> **Use `changelog-section.sh` for the title and notes even by hand.** The site's publish step
> verifies the assets, but nothing verifies prose: a Release whose notes were typed from memory is
> how the published record and the CHANGELOG quietly disagree.

## 5. Publish it — the release is not live yet

**Nothing so far has changed what a user gets.** The site pulls the release on its own dispatch; until
you run this, the download and every install's `/update` still resolve to the previous version:

```bash
gh workflow run publish-release.yml --repo pkozanian/chiefofstaff-site -f version=vX.Y.Z
gh run list --repo pkozanian/chiefofstaff-site --workflow=publish-release.yml --limit 1
```

That workflow downloads three assets from the official repo — `cos.zip`, `VERSION`, `CHANGELOG.md` —
refuses to commit them if `VERSION` disagrees with the tag or `cos.zip` is not the flat shape, commits
`public/dist/` in one commit, and
**dispatches the site's `deploy.yml`** — which is the step that actually republishes. Watch the
*deploy* run, not the publish run, for the live result:

```bash
gh run list --repo pkozanian/chiefofstaff-site --workflow=deploy.yml --limit 1
```

If the site ends up stale anyway, re-dispatch either one — both are idempotent.

**Rollback is the same command with an older tag.** `-f version=v0.26.0` puts that release back on
the live URLs; nothing else needs undoing.

## 6. Verify what the user actually gets

Never end on "the workflow succeeded". Check the live surfaces, cache-busted:

```bash
curl -s "https://chiefofstaff.team/dist/VERSION?cb=$RANDOM"                 # == X.Y.Z
curl -s -o /dev/null -w "%{http_code} %{size_download}\n" -L "https://chiefofstaff.team/dist/cos.zip"
curl -s "https://chiefofstaff.team/dist/CHANGELOG.md?cb=$RANDOM" | grep -m1 "^## \[0"
curl -s "https://chiefofstaff.team/brain/chiefofstaff.html?cb=$RANDOM" | grep -o "release [0-9.]*" | head -1   # /brain/ re-rendered from the new zip
```

Then the Release itself:
```bash
gh release view vX.Y.Z --json assets --jq '.assets[].name'   # 4 assets
```

**Then reopen the next dev cycle by hand** — nothing does it for you:
```bash
# bump src/VERSION to <next-minor>-dev and add a fresh ## [Unreleased] to src/CHANGELOG.md
python3 tests/run.py     # check #5 wants [Unreleased] once VERSION carries -dev again
```
Forgetting leaves `VERSION` sitting on a clean release number, which makes the *next* release's
pre-flight look like it has nothing to do.

For a release that changes the install path, also **rehearse the install** into an empty temp dir with
the real published URL — mechanics can pass while the artifact is wrong:
```bash
d=$(mktemp -d) && cd "$d" && curl -fsSL -o cos.zip https://chiefofstaff.team/dist/cos.zip \
  && unzip -q cos.zip && ls -A && head -3 AGENTS.md && cat VERSION
```

## Output Habit

State plainly, and keep **released** and **published** separate — they are now two different facts,
and reporting only the first is how a release quietly reaches nobody:

- **released:** version, the Release URL, `VERSION` reopened at `<next>-dev`, and **whether
  `release.yml` ran or you fell back**
- **published:** live `dist/VERSION`, the `cos.zip` size, and whether the site's deploy actually ran

If you released but did not publish, say so in those words rather than calling it done. If Actions failed, say so — a silent
manual rescue hides a broken pipeline.
