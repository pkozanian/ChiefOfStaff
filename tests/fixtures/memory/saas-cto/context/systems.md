---
name: context-systems
description: Technical stack, deploy/release process, on-call, and incident history.
type: context
updated: 2026-07-27
---

# Novaflow — Systems & Engineering Context

## Stack
- **Cloud:** AWS. Primary region **us-east-1**; disaster-recovery in **eu-west-1**.
- **Compute:** Kubernetes (EKS); services being consolidated onto
  [Atlas v2 Platform](../projects/atlas-v2-platform.md).
- **Datastores:** **CockroachDB** for OLTP; **Snowflake** for analytics; **Redis** for caching
  and session/failover state.
- **Data pipelines:** owned by Data; being re-architected under [Cascade](../projects/cascade.md).
- **Languages:** Go (platform/services), TypeScript (product), Python (data/ML).

## Deploy / release process
- **CI/CD:** GitHub Actions → **Spinnaker** for deploys.
- **Strategy:** blue-green with a **4-eyes approval gate** (two approvers) on production.
- **Freeze:** **no production deploys on Fridays** or during incidents.

## On-call
- **Paging:** PagerDuty. A **6-engineer rotation** with **handoff every Wednesday**.
- **Severity:** P0 (customer-wide outage) → P3. P0/P1 page Raj and Maya automatically.

## Incident history (recent)
- **INC-204 — 2026-02-14:** the **biggest outage in company history, 3h 11m of downtime**, caused
  by a **Redis failover bug** (split-brain on a failover cascade). Root-cause fix is rolling out
  under [Meridian](../projects/meridian.md); the same failure class caused the June SLA miss.
- **INC-188 — 2025-11-03:** 47-minute partial outage from a bad Spinnaker deploy that bypassed
  the approval gate — the reason the **4-eyes gate** was made mandatory.
- **INC-221 — 2026-06-09:** brief pipeline backlog after a Datalytix connector change; drove the
  push to coordinate breaking API changes with [Helena Braun](../people/helena-braun.md).
