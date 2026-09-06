---
name: memory-okrs
description: Nadia's 2026 H2 (Q3) personal/team objectives and key results, with owners and confidence.
type: okr
updated: 2026-07-20
---

# OKRs — 2026 H2 (Q3)

> Outcome-oriented objectives for Nadia (Staff SWE, Ledger squad). These are personal/team goals,
> not org-wide targets — she's an IC with no reports, so most KRs are owned by `me`, with a couple
> of teammates on shared work. Confidence is self-assessed as of the last review. Confidential
> initiatives appear by code name only.

## Objective 1 — Harden Settlement so it stops paging the on-call

| key result | baseline | target | current | confidence | owner |
|------------|----------|--------|---------|------------|-------|
| Cut Settlement pages per month by 50% | 40/mo (Q2 avg) | 20/mo | 28/mo | 55% | me |
| Hold settlement success at the 99.95% SLO | 99.70% | 99.95% | 99.91% | 45% | me |
| Close every INC-2043 postmortem action item | 0 of 6 | 6 of 6 | 4 of 6 | 70% | Alex Chen |

## Objective 2 — Make ledger balance reads fast enough to stop being the bottleneck

| key result | baseline | target | current | confidence | owner |
|------------|----------|--------|---------|------------|-------|
| Cut p99 ledger balance-query latency to under 150ms | 800ms | 150ms | 260ms | 60% | me |
| Move heavy balance reads off the primary onto read replicas | 0% (primary-only) | 100% | 60% | 65% | Sofia Reyes |
| Review open read-path PRs weekly to keep reviews unblocked | — | weekly | started | 85% | me |

## Objective 3 — Build the org-level track record for the Principal case

| key result | baseline | target | current | confidence | owner |
|------------|----------|--------|---------|------------|-------|
| Land the Ledger v2 re-baseline signed off by Marcus and Kenji | not approved | approved by 2026-08-15 | in review | 45% | me |
| Cut inherited Recon worker on-call toil to under 4 hrs/week | 12 hrs/wk | 4 hrs/wk | 8 hrs/wk | 50% | me |
