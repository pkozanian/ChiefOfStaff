---
name: person-lena-vogel
description: Open-source maintainer of pgledger, a library Cardinal's Ledger service depends on.
type: person
relationship: external
updated: 2026-07-10
---

# Lena Vogel — OSS maintainer (pgledger)

- **Relationship:** external. Lead maintainer of **pgledger**, the open-source Postgres
  double-entry library the `ledger` service builds on.
- **Cadence:** none scheduled — GitHub issues / occasional email.

## Why she matters
- The [Ledger v2 migration](../projects/ledger-v2-migration.md) tracks pgledger's `v3` release,
  which adds the event-sourced primitives v2 needs.
- I filed the upstream issue about the write-lock behavior during batch backfills — she confirmed
  it's expected and pointed to the advisory-lock workaround.

## Notes
- Responsive but volunteer-time only; don't build the plan around a fixed upstream date.
- Worth a small sponsorship / upstream contribution to keep goodwill — potential Principal-scope
  "external impact" story.
