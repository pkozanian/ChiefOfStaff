<!--
Title: name the user-visible bug or behavior, not the mechanism.
  good: fix: setup instructions send ChatGPT users to a command that does not exist
  bad:  fix: add host check to greeting
A reviewer should understand what broke from the title alone, before opening the diff.
-->

## What problem this solves

<!--
One or two sentences, from the USER's side (an executive, or an agent following this repo's
AGENTS.md) — not from the code's side. "The onboarding flow asked for a role twice" beats "refactored
flow.md's step-2 branch." If there is no problem — this is a pure addition — say what capability was
missing instead.
-->

## Why this change

<!--
Why THIS fix, not an alternative. If you considered and rejected another approach, say so and why
(doctrine item 6: name the accepted tradeoff). If this is a mechanical/generated change, say that
plainly instead of inventing a rationale.
-->

## Impact

<!--
What this touches and what it doesn't. Call out explicitly:
- Does this touch `src/`? If so, it ships to every executive on next release/update.
- Does this need a `### Migration notes` block in CHANGELOG.md → ## [Unreleased] (see CONTRIBUTING.md
  → "Migration directive")? If it changes what valid memory/ looks like, yes.
- Any `tests/behaviors.md` rows added/removed for a behavior you added/removed — including a row left
  with an empty `Covered by`, which is a recorded gap, not a failure.
-->

## Evidence

<!--
Do not narrate file by file — the diff already shows what changed. State what you VERIFIED, with the
command and its result:
  - `python3 tests/run.py` → pass/fail, check count.
  - Relevant behavioral eval scenario(s) run, if the change touches brain/ behavior.
  - For a release-adjacent change: the live-endpoint checks from the `/release` skill.
A PR that only says "tests pass" for a behavior change that has no test covering it is a finding
against itself — say so rather than implying coverage that doesn't exist.
-->
