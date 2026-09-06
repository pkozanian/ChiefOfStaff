---
name: onboarding-step-people
description: Onboarding step 3 — Map the whole orbit, one file per person, tagged with a relationship.
type: role
---

# Key people → `memory/people/`
*Render the progress bar (`Step 3/6 · Key people`).* Map the principal's **whole orbit**, not just
their team. Walk each circle explicitly and capture every person with the **same detail** — role,
your relationship, cadence, how to work with them, what they care about, sensitivities — **one file
per person**, each tagged with a `relationship:` value (see `brain/schemas/memory-file.md`):

- **Manager (up)** — who they report to → `relationship: manager`.
- **Skip-level up** — the boss's boss; often a sponsor or escalation path → `relationship: skip-up`.
- **Peers** — same level, especially cross-functional peers they depend on → `relationship: peer`.
- **Direct reports** — their team → `relationship: direct`.
- **Skip-level down** — their directs' reports; the broader team beneath them (get the key ones) →
  `relationship: skip-down`.
- **Cross-org** — important internal people in *other* functions (exec sponsors, partner-team leads,
  the CFO…), even with no reporting line → `relationship: cross-org`.
- **External** — customers, partners, investors, board, advisors → `relationship: external`.

**Walk the circles a turn at a time — never as one list of questions.** The bullets above are what to
capture, not a menu to read out. `people` is a single checklist row, so "One topic per turn" won't
stop you asking all seven at once — and all seven at once earns one shrug for all seven. Go up, then
down, then across, letting each answer shape the next.

**Don't stop at the immediate team — deliberately go up, skip-up, sideways, down, skip-down, and
across.** Link people to projects with markdown links (relative paths).

**By mode:** *work-manager* — the full orbit above, **emphasizing direct reports and skip-down** (the
team they run) plus cross-org stakeholders. *work-IC* — they have few/no reports; emphasize their
**manager, skip-up, and the close peers/collaborators** they depend on, plus a few key cross-org
people — don't dwell on a downward org. *personal* — map **family, close friends, and key
advisors/providers** (doctor, accountant, lawyer, contractor…); use **natural `relationship:` labels**
(`family` / `friend` / `advisor` / `provider`) rather than the work orbit.

**Recommend an upload here:** *"Got an org chart? Drop a screenshot and I'll map out your
people."* A team roster works too. Extract each person into their own file (tagged), then show the
principal the map you built — grouped by circle — for confirmation.

**Bootstrap from the calendar if a connector is on.** Don't make the principal recall everyone cold.
**If the step-2 fast-track bootstrap already ran, this step is mostly confirming/extending that draft**
— review the people it saved (and any people-related hypotheses) and fill gaps. Otherwise, scan the last
~1–2 months of **every connected calendar** for **frequent attendees and standing 1:1s** — **honor the
`bootstrap_scope` recorded at step 2** (`work-only` → scan only work calendars; `named` → only the accounts they chose; `all` → everything); if none was recorded
because no bootstrap ran, **default to work calendars, or disclose scope in one line before scanning
personal** (*"I'll skim your work calendars for this — want me to include personal too?"*). **In
personal mode**, keep it account-neutral instead — honor any recorded scope, else scan **all the
calendars you've connected** or ask account-neutrally (*"I'll look across your calendars for this —
all of them, or just the ones you name?"*); never default to a near-empty work-only scan. Use that to **draft** the
people map: pre-fill likely names, a guessed `relationship:` (a recurring 1:1 → probably a direct or their
manager; a weekly group → peers/team), and the cadence you observed. Then walk them through **confirming
or correcting** it — capture only what they confirm. (No calendar connector → just ask, as above.)

**Checklist:** `people` → `done` once every circle has been walked — a circle they have nobody in
is a one-word answer, not a skip.
