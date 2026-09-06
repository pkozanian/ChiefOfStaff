---
description: Retire a virtual team member, retaining its facts first if wanted.
argument-hint: "<specialist slug>"
---

Remove the virtual team member named in `$ARGUMENTS` (or the request), following `brain/playbooks/team.md`.

- **Offboard, don't just delete.** First review the specialist's `memory/` + `delegations/` and **ask me
  whether to retain its facts**. If yes, promote the still-relevant principal-world facts up into
  shared memory (verify + dedup + reciprocal links + provenance, per `brain/schemas/capture-rules.md`).
- **Default to Remove-retain:** drop the specialist's link from `memory/team/index.md`'s `## Active`
  section, set the charter `status: inactive` (never `retired` — that's the confidential-registry
  convention), and keep an `## Inactive` archival link plus the subtree for provenance. Remove any
  standing routines either way (and any `.claude/agents/<slug>.md` left by an older release).
- Only on an explicit ask for a hard **Delete**: remove the specialist's link from **every** roster
  section (`## Active` and `## Inactive`) first, then delete the `memory/team/<slug>/` subtree.
- If it was the **last** specialist, also remove the `## Always load` team pointer and the roster link
  from `memory/index.md` (delete `memory/team/index.md` itself only if I want the feature fully torn
  down — otherwise leave the empty roster in place).
- If no slug is given, list the team (roster's `## Active` entries) and ask which to remove.
