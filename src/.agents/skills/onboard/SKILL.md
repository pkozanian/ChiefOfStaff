---
name: onboard
description: Start (or re-run) the Chief of Staff onboarding flow.
---

Run the Chief of Staff onboarding now, following `brain/onboarding/flow.md` — from step 0, or, if
`memory/meta.md` says onboarding is `in_progress`, from the first `open` row of
`memory/onboarding-checklist.md` (restart from step 0 only if the principal asks to start over).

- Begin immediately — no need to ask permission.
- Follow the flow's conventions: render the progress bar each step, write to `memory/` as you go,
  create `memory/meta.md` and `memory/index.md` if they don't exist, and update the index.
- If onboarding was already completed before, treat this as a re-onboard: **update** existing
  memory (create-or-update), don't clobber it.
- On finish, set `memory/meta.md` → `onboarding_status: complete` and `onboarded_against` to the
  value in `VERSION`.
