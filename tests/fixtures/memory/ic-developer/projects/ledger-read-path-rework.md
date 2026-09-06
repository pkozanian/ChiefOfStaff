---
name: project-ledger-read-path-rework
description: Latency effort to cut p99 on ledger balance reads via read replicas + query rework. On track.
type: project
updated: 2026-07-19
---

# Ledger read-path rework

> Distinct from the [Ledger v2 migration](ledger-v2-migration.md). This is a **latency/perf**
> effort on the **existing** ledger read path — no re-platforming.

- **Goal / definition of done:** cut **p99 on ledger balance queries from ~800ms to <150ms**;
  move heavy reads off the primary onto read replicas; kill the worst N+1 query in the balance
  endpoint.
- **DRI:** [Nadia Rao](../profile/principal.md), with [Sofia Reyes](../people/sofia-reyes.md) on
  the read APIs.
- **Status (CURRENT): on track.** Benchmarks to be presented at platform sync **2026-08-05**
  (see [commitments](../commitments.md)).

## Key decision (reversed)
- Originally planned a **Redis read-through cache**. **Reversed on 2026-07-18** — went with
  **Postgres read replicas** instead, because cache invalidation couldn't guarantee read-your-writes
  consistency on money balances. See [log 2026-07-18](../log/2026-07-18-readpath-reversal.md).

## Open items
- Confirm replica lag budget stays under the balance-freshness SLO.
- Hand the benchmark presentation to Sofia if I want to give her platform-sync visibility.
