---
name: log-2026-05-12-inc-2043
description: Postmortem for INC-2043, the Settlement double-charge incident.
type: log
updated: 2026-05-12
---

# 2026-05-12 — INC-2043 postmortem (Settlement double-charge, SEV-1)

- **What happened:** a retried settlement batch double-posted to a subset of accounts.
- **Root cause:** the settlement retry path lacked an **idempotency key**, so a retried batch was
  processed twice.
- **Blast radius:** limited set of accounts; all reversed and reconciled within the day.
- **Fix:** idempotency keys + dedup on the settlement path (driven by
  [Alex Chen](../people/alex-chen.md)).
- **Follow-through:** spun up the [Settlement reliability](../projects/settlement-reliability.md)
  initiative; [Diane Foster](../people/diane-foster.md) reviewed the writeup personally.
