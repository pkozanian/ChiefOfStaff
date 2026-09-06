---
name: profile-principal
description: Who the principal is — Staff Software Engineer on the Ledger squad at Cardinal.
type: profile
updated: 2026-07-20
---

# Nadia Rao — Staff Software Engineer

- **Goes by:** Nadia (never "Nads"; full name on formal docs is Nadia S. Rao).
- **Role:** Staff Software Engineer, Payments Platform org, **Ledger squad** at **Cardinal**
  (mid-size payments infrastructure company). Individual contributor — **no direct reports.**
- **Manager (EM):** [Marcus Bell](../people/marcus-bell.md).
- **Skip-level:** [Diane Foster](../people/diane-foster.md), Director of Engineering.
- **Tenure:** joined Cardinal 2021; promoted to Staff in early 2025.

## What I own
- **Ledger service** (`ledger`) — the double-entry system of record for all money movement.
  Kotlin/JVM on Postgres (`ledger-db`). See [systems](../context/systems.md).
- **Settlement service** (`settlement`) — Go service that settles and reconciles batches; consumes
  Kafka. See [systems](../context/systems.md).
- Technical DRI for the [Ledger v2 migration](../projects/ledger-v2-migration.md) and DRI for
  [Multi-currency settlement](../projects/multi-currency-settlement.md).
- I inherited the nightly **Recon worker** (reconciliation) after [Ravi Menon](../people/ravi-menon.md)
  transferred off the squad — see [Recon worker migration](../projects/recon-worker-migration.md).

## Current focus (2026-Q3)
- Unblocking and re-planning the [Ledger v2 migration](../projects/ledger-v2-migration.md)
  (now slipped — the historical backfill dependency stalled).
- Shipping the [Ledger read-path rework](../projects/ledger-read-path-rework.md) latency work.
- Hardening Settlement reliability after INC-2043 — see
  [Settlement reliability](../projects/settlement-reliability.md).

## Growth goals
- Targeting **Principal Engineer** in the next review cycle; needs org-level impact and a
  written scope/promo packet (in progress — see [commitments](../commitments.md)).
- Wants to be seen as the go-to for money-movement correctness across the org, not just one squad.
- Working on delegation / mentoring — mentors [Jordan Kim](../people/jordan-kim.md).

## Working style (see [preferences](../preferences/index.md))
- Deep-work mornings; async-first; terse and technical.
