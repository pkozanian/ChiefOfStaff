# `scripts/` — build & verify tooling

Scope: this directory only. Global policy (the `src/` boundary, doctrine, the never list) is in the
root [`AGENTS.md`](../AGENTS.md) — this file defers to it and doesn't restate it.

## `build-dist.sh` — no ship-list, on purpose

`src/` **is** the manifest. This script copies that subtree verbatim into `dist/`; there is nothing
here that decides *what* ships, only what gets stripped (`.claude/agents/`, local settings) and how
the two archives get zipped. **Never add a ship-list here** — if a file belongs in the release, it
belongs in `src/`, full stop. Adding an explicit include/exclude list would create a second place that
must agree with `src/`'s actual contents, and the two would drift.

Two archives come out of one build: `cos.zip` (flat — the one to use) and `ChiefOfStaff.zip`
(nested — a compatibility bridge for installs predating 0.20.0 whose on-disk `/update` recipe
hardcodes the nested path and can't be corrected remotely). Keep publishing both until no install is
still on a pre-0.20.0 brain; see `CONTRIBUTING.md` → **Releasing** → "Two archives, and why" for the
retirement plan.

## `changelog-section.sh` — one release's notes

Prints one `## [x.y.z]` section of `src/CHANGELOG.md`, body or `--title`. `release.yml` uses it for the
GitHub Release it publishes on the official repo, which has one squashed commit per release and no PRs
— so GitHub's own generated notes would say nothing there. It **exits non-zero on a missing section**
rather than printing nothing: empty release notes are worse than a failed release, because they look
finished.

The heading format it parses (`## [x.y.z] — title`) is the same one structural check #5 asserts. If
you change one, change both.

## This directory is two scripts

`build-dist.sh` and `changelog-section.sh` are all that live here. `build_docs.py` (which rendered the
site's `/brain/` docs) and `verify-site.mjs` (which drove headless Chrome over the built site) both
moved to `pkozanian/chiefofstaff-site` when the site split out — they read and wrote only site files,
so neither had any business in the product tree.

**This repo has no Node and no dependencies.** Keep it that way: `build-dist.sh` is POSIX shell plus
`zip`, and `tests/run.py` is stdlib Python. If a task seems to need a package, it probably belongs to
the site repo.
