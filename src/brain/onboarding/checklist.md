---
name: onboarding-checklist-template
description: Every onboarding requirement with a stable ID, the step that owns it, and the six statuses a row can hold — the template memory/onboarding-checklist.md is created from.
type: role
---

# Onboarding checklist

Onboarding owes the principal every row below. At the very start of `flow.md`, copy the `## Rows`
table into **`memory/onboarding-checklist.md`** (`type: log`, `updated:` today, shape at the end of
this file) with every status `open`, and link it from `memory/index.md` under `## Load on demand`.
Each step resolves the rows it owns and writes the status **in the turn the row is resolved**. On
resume, work continues at the first `open` row (`CHIEFOFSTAFF.md` boot step 2). After Finishing the
memory file stays — it is the record of what was deferred.

## Statuses — exactly six

| Status | Means |
|---|---|
| `open` | not yet addressed — every row starts here |
| `done` | asked or offered, and resolved; content captured where the step says |
| `declined` | offered, and the principal said no |
| `deferred` | set aside **with the principal's explicit agreement** — the express path, or a named "later" |
| `blocked` | could not be completed — the reason goes in the Note (a connector whose tools need a fresh session) |
| `n/a` | does not apply — the reason goes in the Note (`personal mode`, `team-offer: off`, `no OKRs captured`) |

A row leaves `open` only by being addressed. Short answers, a fast pace, or an earlier decline never
change a row. **Optional means the principal may decline, not that the offer may be omitted.** Three
places may record `deferred` — the **express path** (`flow.md` → "The express path"), the **step-4
minimum-viable checkpoint**, and the **Finishing audit** (`flow.md` → "Finishing") — and all three are
bound by the same two conditions: the principal's explicit agreement, and **only on rows marked
deferrable below**. A non-deferrable row is asked, or it stays `open`.

## Rows

| ID | Item | Step | Modes | Deferrable |
|---|---|---|---|---|
| `mode` | work/personal set and confirmed; IC/manager (work) | 0–1 | all | no |
| `profile` | `memory/profile/principal.md` holds name, `Goes by:`, role, mandate | 1 | all | no |
| `context` | org / life context captured to `memory/context/` | 2 | all | no |
| `connector-check` | every connector category for their stack resolved to one of the six discovery states, or recorded inconclusive with what would resolve it | 2 | all | no |
| `connector-recommend` | connectors for their stack recommended, with enable steps for the missing ones | 2 | all | no |
| `browser-line` | browser control said once, host-aware, with the rails | 2 | all | no |
| `integrations-inventory` | `memory/integrations.md` written, one row per capability with its state | 2 | all | no |
| `bootstrap-offer` | the history scan offered, with scope; `n/a` only when every category is positively state 6; `blocked` when any is inconclusive | 2 | all | no |
| `people` | the orbit walked circle by circle, one file per person | 3 | all | no |
| `projects` | top priorities / initiatives captured, one file each | 4 | all | no |
| `okrs` | asked whether they run on OKRs; recorded to `memory/okrs.md` if so | 4 | work | no |
| `okr-critique` | the critique offered (`n/a` — no OKRs captured — otherwise) | 4 | work | yes |
| `decisions` | open decisions asked and logged | 4 | all | no |
| `confidentiality` | the narrow unannounced / pre-public ask | 4 | work | no |
| `team-offer` | a grounded proposal, or the one-line generic offer when context is thin (`n/a` only on `team-offer: off` or a prior decline) | 4 | all | yes |
| `defaults-menu` | the shipped defaults shown change-only | 5 | all | no |
| `open-preferences` | cadence, standing rules, hard nos | 5 | all | yes |
| `rhythms` | recurring commitments captured or confirmed | 6 | all | yes |
| `routines` | the five routines offered as one ask; outcome per routine in `memory/preferences/briefings.md` | 6 | all | yes |
| `audit` | the memory-lint self-audit, then the checklist audit: no row `open` | Finishing | all | no |
| `summary` | the completion summary shown, deferred and blocked rows named | Finishing | all | no |

**Personal mode** marks `okrs`, `okr-critique` and `confidentiality` `n/a` (note: personal mode) at
step 0. **Modes** otherwise only changes framing, never whether a row exists.

## The memory file

```markdown
---
name: onboarding-checklist
description: Every onboarding requirement and how it was resolved — the resume anchor and the completion record.
type: log
updated: 2026-09-05
---

# Onboarding checklist

| ID | Item | Step | Status | Note |
|---|---|---|---|---|
| mode | work/personal set and confirmed; IC/manager | 1 | done | work · manager |
| connector-check | every connector category resolved to a state | 2 | blocked | Outlook tools not surfaced — retry in a fresh session, then re-offer the bootstrap |
| okr-critique | the critique offered | 4 | deferred | express path, 2026-09-05 |
```

The `Note` column is where a `blocked` or `n/a` row keeps its reason (required), a `declined` row keeps
what they said, a `deferred` row keeps how it was agreed, and a `done` row keeps a gap they left. Keep
notes to a phrase.
