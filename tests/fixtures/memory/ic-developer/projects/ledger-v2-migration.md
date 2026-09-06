---
name: project-ledger-v2-migration
description: Migrate the ledger to an event-sourced double-entry service (Ledger v2). Currently blocked/slipped.
type: project
updated: 2026-07-18
---

# Ledger v2 migration

> Not to be confused with the [Ledger read-path rework](ledger-read-path-rework.md) — that's a
> latency effort on the existing ledger; **this** is the full re-platform to double-entry v2.

- **Goal / definition of done:** replace the single-entry monolith ledger with the event-sourced,
  double-entry **Ledger v2** service; all money movement written through v2; historical balances
  backfilled and reconciled to the cent; old path decommissioned.
- **DRI:** [Nadia Rao](../profile/principal.md) (technical). **EM:** [Marcus Bell](../people/marcus-bell.md).
- **Original target cutover:** 2026-08-15.
- **Status (CURRENT, 2026-07-18): BLOCKED — cutover SLIPPED to Q4.**
  Earlier in the quarter this was on track (see [log 2026-06-20](../log/2026-06-20-ledger-v2-on-track.md));
  it went blocked on 2026-07-08 (see [log 2026-07-08](../log/2026-07-08-ledger-v2-blocked.md)).

## What's blocking it (the dependency chain)
- Cutover requires a **one-time historical double-entry backfill** of all prior ledger entries.
- That backfill runs on **Data Platform's ETL pipeline**, which is **owned by
  [Alex Novak](../people/alex-novak.md)** (Data Platform — *not* Alex Chen on my squad).
- Alex Novak has **deprioritized the ledger backfill to Q4**: Data Platform is under a change
  freeze until Q4 planning, and the backfill collides with the nightly reconciliation window.
- Net: no backfill until Q4 → **no cutover until Q4.** Escalation path is Director-to-Director via
  [Diane Foster](../people/diane-foster.md).

## Constraints
- Any backfill/migration must run **outside 02:00–04:00 UTC** — the `ledger-db` write freeze window
  (see [systems](../context/systems.md)).
- Blocked on **pgledger v3** (upstream, [Lena Vogel](../people/lena-vogel.md)) for the
  event-sourced primitives.

## Next actions
- Re-baselined plan in writing for Marcus + the skip-level pre-read for Diane.
- RFC approval owed to [Kenji Watanabe](../people/kenji-watanabe.md) on the double-entry schema.
