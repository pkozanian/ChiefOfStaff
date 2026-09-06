---
name: project-multi-currency-settlement
description: New feature Nadia is DRI on — multi-currency settlement with FX conversion at settlement time.
type: project
updated: 2026-07-17
---

# Multi-currency settlement (new feature)

- **Goal / definition of done:** support settling in multiple currencies with **FX conversion at
  settlement time**, correct rounding, and per-currency ledgers in Ledger v2.
- **DRI:** [Nadia Rao](../profile/principal.md). **Product:** [Priya Anand](../people/priya-anand.md).
  **Design:** [Tomás Herrera](../people/tomas-herrera.md) on the API surface.
- **Status: design / early. Target Q4** (depends on Ledger v2 landing first — per-currency ledgers
  need the v2 double-entry model).

## Watch-outs
- **Do not give [Priya Anand](../people/priya-anand.md) rough dates** — she has turned ballpark
  estimates into public roadmap commitments before (she did exactly this with multi-currency).
  Only committed, buffered, Marcus-signed dates.
- Rounding / FX correctness is a money-path landmine; needs airtight tests and Tomás on the
  display/formatting semantics.

## Open items
- Currency rounding spec + test matrix.
- Dependency note: gated on [Ledger v2 migration](ledger-v2-migration.md) (currently slipped to Q4).
