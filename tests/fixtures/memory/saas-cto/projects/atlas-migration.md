---
name: project-atlas-migration
description: Migrate legacy monolith services off the old stack onto the new platform.
type: project
updated: 2026-07-27
---

# Atlas Migration

> Not to be confused with [Atlas v2 Platform](atlas-v2-platform.md). **Atlas Migration** is the
> *effort to move existing services* onto the new platform. **Atlas v2 Platform** is the *new
> platform itself*. The migration consumes the platform.

- **Goal / definition of done:** decommission the legacy "Monolith" and run all 40 core services
  on the new platform by **2026-11-30**.
- **Owner:** [Raj Patel](../people/raj-patel.md) (platform), with app-side work from
  [Sam Okafor](../people/sam-okafor.md)'s teams.
- **Status:** **blocked.** 12 of 40 services migrated; the remaining wave cannot proceed.
- **Blocked by:** [Atlas v2 Platform](atlas-v2-platform.md) — specifically its **service-mesh
  GA**, which is not ready. Until the mesh GAs, multi-region services can't cut over safely.
  (Trace the mesh owner via the Atlas v2 Platform file.)

## Open items
- Cutover plan for waves 2–4 owed to [Daniel Reyes](../people/daniel-reyes.md) — see
  [commitments](../commitments.md) (currently **overdue**).
- Payments services in wave 3 are riskier since [Tom Becker](../people/tom-becker.md) left.
