---
name: log-2026-06-05-double-entry-decision
description: Design decision to build Ledger v2 as event-sourced double-entry.
type: log
updated: 2026-06-05
---

# 2026-06-05 — Ledger v2 design decision: event-sourced double-entry

- **Decision:** build **Ledger v2** as an **event-sourced double-entry** service (not a
  schema patch on the existing single-entry ledger).
- **Why:** correctness and auditability; per-currency ledgers for
  [multi-currency settlement](../projects/multi-currency-settlement.md) need the double-entry model.
- **Depends on:** **pgledger v3** primitives (upstream, [Lena Vogel](../people/lena-vogel.md)) and a
  one-time historical backfill via Data Platform's ETL.
- **RFC:** [Kenji Watanabe](../people/kenji-watanabe.md)'s double-entry schema RFC — approval owed.
