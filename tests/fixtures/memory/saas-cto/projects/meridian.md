---
name: project-meridian
description: Reliability & SLA program to hit contractual 99.95% uptime.
type: project
updated: 2026-07-27
---

# Meridian — Reliability / SLA Program

> Internal program name only. Unrelated to **Meridian Ventures**, the VC where board chair
> [Eleanor Vance](../people/eleanor-vance.md) is a partner.

- **Goal / definition of done:** sustain **99.95%** monthly uptime across the core platform and
  eliminate the recurring incident classes behind recent breaches, by end of Q3.
- **Owner:** [Raj Patel](../people/raj-patel.md).
- **Status:** **AT RISK** (updated 2026-07-18). June missed SLA at 99.86% after incident
  **INC-204**; a repeat class of failover incidents is not yet closed out. This overrides the
  earlier "on track" read from the June offsite.
- **Watched by:** [Sofia Alvarez](../people/sofia-alvarez.md) (revenue at risk on renewals) and
  [Eleanor Vance](../people/eleanor-vance.md) (board reliability section). Sofia wants weekly status.

## Open items
- Redis failover fix (root cause of INC-204) rolling out; see [systems](../context/systems.md).
- Error-budget policy needs Maya's sign-off.
