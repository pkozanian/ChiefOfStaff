---
name: context-company
description: Cardinal — the mid-size payments infrastructure company Nadia works at, and its org shape.
type: context
updated: 2026-07-12
---

# Cardinal — company context

- **What it is:** mid-size **payments infrastructure** company (~800 people, ~250 in engineering).
  Cardinal provides the money-movement rails — ledgering, settlement, payouts — that other fintechs
  build on. B2B; correctness and reliability are the product.
- **Stage:** post Series C, revenue-generating, not yet profitable. Reliability incidents are
  existential (customers move real money).

## Org shape (my corner)
- **Payments Platform** org — Director [Diane Foster](../people/diane-foster.md).
  - **Ledger squad** — EM [Marcus Bell](../people/marcus-bell.md); my squad.
  - **Payouts squad** — separate squad under Diane.
  - **Tech Lead** across the org: [Kenji Watanabe](../people/kenji-watanabe.md).
- **Data Platform** — separate org; owns the ETL/backfill pipeline
  ([Alex Novak](../people/alex-novak.md)). Cross-org dependency for Ledger v2.
- **Product:** [Priya Anand](../people/priya-anand.md) (Payments PM).

## Norms
- Written-first culture: RFCs and design docs over meetings.
- Blameless postmortems; every SEV incident gets a public writeup (e.g. INC-2043).
- Change freezes around planning cycles and end-of-quarter.
