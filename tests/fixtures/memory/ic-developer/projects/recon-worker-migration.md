---
name: project-recon-worker-migration
description: Tech-debt paydown — move the legacy nightly reconciliation cron onto the new worker framework.
type: project
updated: 2026-07-14
---

# Recon worker migration (tech-debt paydown)

- **Goal / definition of done:** retire the **legacy nightly reconciliation cron** and move the
  **Recon worker** onto the standard worker framework (observability, retries, no bespoke cron);
  delete the old cron entirely.
- **DRI:** [Nadia Rao](../profile/principal.md) and [Alex Chen](../people/alex-chen.md) — we
  **inherited this** when [Ravi Menon](../people/ravi-menon.md) transferred off the squad on
  2026-05-30 and his ownership was reassigned.
- **Status (CURRENT): in progress**, low priority behind Ledger v2 re-planning.

## Why it matters
- The legacy cron is undocumented bus-factor debt; it's also what runs against `ledger-db` and
  must respect the **02:00–04:00 UTC** write-freeze window (see [systems](../context/systems.md)).

## Open items
- Reverse-engineer the reconciliation edge cases from Ravi's old code (he's available as a last
  resort on Data Platform, but shouldn't be treated as a squad resource).
