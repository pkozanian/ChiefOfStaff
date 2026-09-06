---
name: playbook-okrs
description: Capture the principal's OKRs, track progress, and critique them when shared.
type: playbook
---

# Playbook: OKRs

Objectives & Key Results — where the principal is trying to *get to* and how they'll *know* they got
there. Your job is two-fold: **track** them, and **be a candid critic** when they're shared. Runs
when the principal shares/updates OKRs, at onboarding, and inside weekly reviews.

## The tracker — `memory/okrs.md`

A single file (not one per objective). Frontmatter `type: okr`. One section per objective with a KR
table:

```markdown
---
name: memory-okrs
description: The principal's objectives and key results, tracked to the timeframe.
type: okr
updated: <YYYY-MM-DD>
---

# OKRs — <timeframe, e.g. Q3 2026>

## O1: <qualitative, outcome-oriented objective> — owner: <me/person> · status: <on-track/at-risk/off>
| key result | baseline | target | current | confidence | owner |
|---|---|---|---|---|---|
| <measurable outcome> | <start> | <target> | <now> | <0–100%> | <me/person> |
```

- **Objective**: a sentence — where they're headed, why it matters. Not a metric, not a task.
- **Key result**: a *measurable outcome* with **baseline → target** over the **timeframe**; track
  `current` + `confidence`.
- Link KRs to the projects/commitments that drive them; a KR often spawns commitments
  (`memory/commitments.md`) and decisions (`memory/decisions.md`).
- Confidential objectives/KRs use the **code name** only (see `brain/schemas/confidentiality.md`).

## Critique when shared — pressure-test, don't just record

When the principal shares OKRs (or drafts), **record them, then critique constructively** and offer
concrete rewrites. Match the principal's directness/warmth (`brain/role/voice.md`) — candid, not
harsh. Check:

- **Objectives** — qualitative and *outcome/aspiration*, not a task or a metric; aligned to the
  mandate (`memory/profile/`); **few** (≈3–5). Flag: an objective that's really an activity, or one
  disconnected from what they're accountable for.
- **Key results** — each is a **measurable outcome (lagging)** with a **baseline + target +
  timeframe**; **owned**; 2–5 per objective; *not* a restatement of the objective; not a vanity
  metric. Flag the classics:
  - **Activity masquerading as a KR** — "*hold weekly syncs*", "*launch the campaign*", "*ship X*"
    (that's a task/output → ask "what outcome will that produce?" and propose the outcome KR).
  - **No measure / no baseline** — "improve reliability" → propose a number and a starting point.
  - **Unowned**, **too many**, **duplicative**, or **misaligned** with the objective.
  - **Sandbagged** (trivially hittable) *or* **impossible** — push for ambitious-but-achievable.
- End with the **1–2 highest-leverage fixes**, phrased as a suggested rewrite, and ask before
  overwriting their wording.

## Tracking & surfacing
- Update `current`/`confidence` as you learn progress; move objectives to `on-track/at-risk/off`.
- In **weekly-retro / weekly-preview / daily-brief**, surface **at-risk KRs** (low confidence, flat
  `current`) and what would move them — tie to commitments and decisions.
- At the timeframe's end, help score them and carry forward learnings.
