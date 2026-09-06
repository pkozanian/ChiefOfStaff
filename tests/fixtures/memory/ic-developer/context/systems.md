---
name: context-systems
description: The services Nadia owns, the stack, deploy/CI, on-call rotation, and a notable past incident.
type: context
updated: 2026-07-16
---

# Systems Nadia owns

## Services
- **`ledger`** — the double-entry system of record for all money movement. **Kotlin/JVM** on
  **Postgres** (primary DB nicknamed **`ledger-db`**, plus read replicas being added). Builds on the
  open-source **pgledger** library ([Lena Vogel](../people/lena-vogel.md)).
- **`settlement`** — **Go** service that settles and reconciles batches; **consumes Kafka**
  (`settlement-events` topic). Reconciliation is handled by the nightly **Recon worker**.

## Stack / deploy / CI
- **CI:** GitHub Actions (unit + contract tests, then integration on a preview env).
- **Deploy:** container images → **ArgoCD** → Kubernetes. `settlement` deploys via ArgoCD;
  `ledger` behind the same pipeline.
- **Feature flags:** LaunchDarkly (`LD`).
- **Observability:** metrics + traces; SLO dashboards per service.
- **Deploy freeze:** no production deploys after 16:00 Friday or during quarter-end freezes.

## On-call
- **1-week PagerDuty rotation** across the Ledger squad. Primary carries both `ledger` and
  `settlement`. **Secondary/escalation goes to the EM, [Marcus Bell](../people/marcus-bell.md).**
- Week of 2026-07-21 primary: [Alex Chen](../people/alex-chen.md); hands off to Nadia 2026-07-28.

## Operational constraints (read before scheduling any batch/migration)
- The nightly **ETL / historical backfill** (owned by Data Platform,
  [Alex Novak](../people/alex-novak.md)) holds a write lock on `ledger-db` **02:00–04:00 UTC**.
  **The `ledger-db` primary must NOT take writes between 02:00 and 04:00 UTC** — writes in that
  window deadlock against the ETL lock. Schedule all migrations, backfills, and the Recon worker
  **outside 02:00–04:00 UTC**. (This constraint is exactly why the Ledger v2 backfill can't just be
  slotted in — it collides with this window.)

## Notable past incident
- **INC-2043 — Settlement double-charge (2026-05-12, SEV-1).** A retried settlement batch lacked an
  idempotency key and double-posted to some accounts. Root cause: missing idempotency key on retry.
  Fix: idempotency keys + dedup on the settlement path (shipped). Drove the
  [Settlement reliability](../projects/settlement-reliability.md) initiative. Postmortem:
  [log 2026-05-12](../log/2026-05-12-inc-2043-postmortem.md).
