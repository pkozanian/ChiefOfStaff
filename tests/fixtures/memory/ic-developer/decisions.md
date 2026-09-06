---
name: memory-decisions
description: Decision log for Nadia's technical work — status plus RAPID roles (Recommend/Agree/Perform/Input/Decide).
type: decision
updated: 2026-07-20
---

# Decision Log

> RAPID roles: **R** recommend · **A** agree · **P** perform · **I** input · **D** decide.
> Nadia is an IC — she's usually **R** (recommend) or **I** (input); the EM (Marcus Bell) or the
> Tech Lead (Kenji Watanabe) is usually **D** (decide). Confidential decisions appear by code name only.

| decision | status | R | A | P | I | D | date | rationale/source |
|----------|--------|---|---|---|---|---|------|------------------|
| Re-baseline the Ledger v2 cutover to Q4 and pause the historical backfill until Data Platform's freeze lifts | open | me | Kenji Watanabe | me | Alex Novak | Marcus Bell | 2026-07-18 | Data Platform change freeze deprioritized the backfill to Q4; escalation is Director-to-Director via Diane Foster (log 2026-07-08) |
| Use Postgres read replicas instead of a Redis read-through cache for ledger balance reads | decided | me | Sofia Reyes | me | Kenji Watanabe | Marcus Bell | 2026-07-18 | Cache invalidation couldn't guarantee read-your-writes consistency on money balances (log 2026-07-18) |
| Fix the INC-2043 double-charge with idempotency keys plus dedup on settlement retries | decided | me | Alex Chen | Alex Chen | Sofia Reyes | Marcus Bell | 2026-05-14 | INC-2043 postmortem root cause: missing idempotency key on a retried batch (log 2026-05-12) |
| Adopt Kenji's double-entry schema RFC as the Ledger v2 write model | open | Kenji Watanabe | Marcus Bell | me | me | Kenji Watanabe | 2026-07-20 | Double-entry decision; RFC approval owed 2026-08-01 (commitments) |
