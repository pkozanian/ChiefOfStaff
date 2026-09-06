---
name: project-settlement-reliability
description: On-call/reliability initiative to cut Settlement pages and hit 99.95% after INC-2043.
type: project
updated: 2026-07-16
---

# Settlement reliability hardening

- **Goal / definition of done:** cut Settlement pages by **50%**, hit a **99.95%** settlement
  success SLO, and close every action item from the **INC-2043** postmortem.
- **DRI:** [Nadia Rao](../profile/principal.md), with [Alex Chen](../people/alex-chen.md) on the
  Settlement internals.
- **Status (CURRENT): on track.** Idempotency keys + dedup shipped (the INC-2043 root-cause fix);
  now working down alerting noise and flaky retries.

## Background
- Kicked off after **INC-2043** (2026-05-12), the Settlement double-charge incident — root cause was
  a missing idempotency key on a retried batch. See [systems](../context/systems.md) and
  [log 2026-05-12](../log/2026-05-12-inc-2043-postmortem.md).

## Open items
- Tune PagerDuty alert thresholds (too many low-signal pages on the current rotation).
- Add a settlement replay tool so a bad batch can be safely re-run.
- On-call handoff notes to Alex Chen due 2026-07-31 (see [commitments](../commitments.md)).
