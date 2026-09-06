---
name: log-2026-07-18-readpath-reversal
description: Reversed the read-path caching decision — Redis cache dropped in favor of Postgres read replicas.
type: log
updated: 2026-07-18
---

# 2026-07-18 — Read-path decision REVERSED: Redis cache → Postgres read replicas

- **Reversal:** dropped the planned **Redis read-through cache** for the
  [read-path rework](../projects/ledger-read-path-rework.md); going with **Postgres read replicas**.
- **Why the reversal:** cache invalidation couldn't guarantee **read-your-writes consistency** on
  money balances — unacceptable for a ledger. Replicas with a bounded lag budget are safer.
- **Impact:** slightly less latency headroom, but correctness wins. Benchmarks to validate the
  replica-lag budget before platform sync 2026-08-05.
