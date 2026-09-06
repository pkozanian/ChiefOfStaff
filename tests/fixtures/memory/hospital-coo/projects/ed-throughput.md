---
name: project-ed-throughput
description: ED Throughput Improvement — cut boarding and door-to-provider time.
type: project
updated: 2026-07-27
---

# ED Throughput Improvement

- **Goal / definition of done:** cut ED **median door-to-provider from ~42 to 30 minutes** and
  materially reduce **boarding hours** for admitted patients.
- **Owner:** [David Coleman](../people/david-coleman.md), Director of Emergency Services.
  Clinical co-sign: [Priya Anand](../people/priya-anand.md).
- **Status:** active; on track on the front-end (intake redesign) but **gated on the boarding
  constraint**, which the ED cannot fix alone.

## The dependency chain (why this is upstream)
1. The binding constraint is **inpatient boarding** — admitted patients stuck in the ED for
   lack of a bed.
2. Resolving it depends on the **bed-management / capacity module** being delivered by
   [Epic Optimization — Phase 2](epic-optimization-phase-2.md).
3. That module is owned by **[Wei Chen](../people/wei-chen.md)** — so the person to move
   ED throughput is upstream in informatics, not in the ED.
- Longer-term capacity relief also comes from the
  [New Patient Tower](new-patient-tower.md).
- Bed-flow / care-progression is co-owned operationally by
  [Karen Osei](../people/karen-osei.md) (CNO).
