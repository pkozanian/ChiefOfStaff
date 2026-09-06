---
name: project-atlas-v2-platform
description: The next-gen internal developer platform that Atlas Migration moves services onto.
type: project
updated: 2026-07-27
---

# Atlas v2 Platform

> Not to be confused with [Atlas Migration](atlas-migration.md). This file is the **platform
> itself** — the new internal developer platform (Kubernetes-based, multi-region, with a
> service mesh). The migration is a separate effort that depends on this one.

- **Goal / definition of done:** GA the new platform — including multi-region service mesh,
  self-serve deploys, and golden-path templates — by **2026-10-15**.
- **Owner:** [Raj Patel](../people/raj-patel.md).
- **Status:** **at risk.** Core platform is up; the **service-mesh GA has slipped to September**.
- **Critical path — the blocker of record:** the **service-mesh GA**, technically led by staff
  engineer [Grace Liu](../people/grace-liu.md). Multi-region traffic policy and mTLS rollout are
  the hard parts; this slip is what is holding up [Atlas Migration](atlas-migration.md).

## Open items
- Grace Liu needs one more engineer pulled onto mesh work; competing with incident load.
- Golden-path templates ~70% done; self-serve deploy in beta with 4 teams.
