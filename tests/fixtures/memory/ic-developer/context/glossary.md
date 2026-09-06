---
name: context-glossary
description: Internal service names and jargon used across the Ledger squad and Payments Platform.
type: context
updated: 2026-07-12
---

# Glossary — internal names & jargon

- **`ledger`** — the double-entry system-of-record service (Kotlin/JVM, Postgres). Owned by Nadia.
- **`ledger-db`** — the Postgres primary for `ledger`.
- **`settlement`** — the Go service that settles/reconciles batches (Kafka consumer). Owned by Nadia.
- **Recon worker** — the nightly reconciliation job (formerly Ravi Menon's); reconciles settlement
  batches against the ledger.
- **the ETL / the backfill** — Data Platform's nightly pipeline (Alex Novak); also the mechanism
  for the one-time Ledger v2 historical backfill.
- **the freeze window** — 02:00–04:00 UTC, when `ledger-db` can't take writes (ETL holds the lock).
- **cutover** — the switch of live traffic from the old ledger to **Ledger v2**.
- **double-entry** — every transaction posts balanced debit+credit; the correctness model for v2.
- **pgledger** — the open-source Postgres double-entry library `ledger` builds on (maintainer:
  Lena Vogel); **v3** adds event-sourced primitives Ledger v2 needs.
- **platform sync** — the biweekly Payments Platform technical review (where benchmarks/RFCs land).
- **RFC** — written design proposal; the platform's decision unit (Kenji owns the process).
- **DRI** — Directly Responsible Individual.
- **INC-####** — incident IDs (e.g. INC-2043, the Settlement double-charge).
- **`LD`** — LaunchDarkly (feature flags).
- **Aurora** — a confidential initiative; use the code name only (details in the registry).
