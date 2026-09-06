---
name: log-2026-07-08-ledger-v2-blocked
description: Ledger v2 migration went BLOCKED — backfill deprioritized to Q4; cutover slips. (CURRENT.)
type: log
updated: 2026-07-08
---

# 2026-07-08 — Ledger v2 status: BLOCKED, cutover slipped to Q4 (CURRENT)

- **Status change:** migration is now **BLOCKED**; the 2026-08-15 cutover **slips to Q4**.
- **Why:** [Alex Novak](../people/alex-novak.md) (Data Platform) **deprioritized the historical
  backfill to Q4** — Data Platform is under a change freeze until Q4 planning, and the backfill
  collides with the nightly reconciliation window on `ledger-db`.
- **Reminder:** the backfill can't just be scheduled around it — the ETL already holds the
  `ledger-db` write lock 02:00–04:00 UTC (see [systems](../context/systems.md)).
- **Next:** re-baseline the plan in writing for Marcus; raise a Director-to-Director escalation via
  [Diane Foster](../people/diane-foster.md).
- This is the **current** status — supersedes [2026-06-20](2026-06-20-ledger-v2-on-track.md).
