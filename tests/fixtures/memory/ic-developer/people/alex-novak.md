---
name: person-alex-novak
description: Senior SWE on the Data Platform team — owns the ETL/backfill (NOT Alex Chen on Ledger).
type: person
relationship: cross-org
updated: 2026-07-20
---

# Alex Novak — Senior Software Engineer, Data Platform team

- **Relationship:** cross-org partner-team engineer. **Different person from
  [Alex Chen](alex-chen.md)** on my squad — Novak is on **Data Platform**, no reporting line to me.
- **Cadence:** ad hoc; reach him in `#data-platform`. Slow to respond during data freezes.

## Why he matters
- He **owns the nightly ETL / historical backfill pipeline** — the piece the
  [Ledger v2 migration](../projects/ledger-v2-migration.md) depends on for the double-entry
  historical backfill.
- **This is the current blocker on Ledger v2:** Alex has **deprioritized the ledger backfill to
  Q4**. Reason he gave: the backfill job collides with the nightly reconciliation window and Data
  Platform is under a **change freeze until the Q4 planning cycle**, so he can't take the rework
  now. He's also the only person who knows that pipeline well — it's a bus-factor of one.
- The ETL job is what holds the `ledger-db` write lock **02:00–04:00 UTC** each night (see
  [systems](../context/systems.md)).

## Notes
- Not obstructive — genuinely under-resourced. Escalation should go Director-to-Director
  ([Diane Foster](diane-foster.md)), not engineer-to-engineer.
