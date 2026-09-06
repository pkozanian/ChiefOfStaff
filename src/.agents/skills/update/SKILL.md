---
name: update
description: Update the Chief of Staff to the latest release (refreshes the brain; your memory is untouched).
argument-hint: "[optional: 'check' to only check for a newer version without applying]"
---

Update the Chief of Staff now, following `brain/playbooks/update.md`.

- If `$ARGUMENTS` (or the request) is `check`, only **check** whether a newer version is available and
  report it — don't apply anything.
- Otherwise, **check** the latest published `VERSION` against the local one; if newer, **confirm**
  with me, then **apply** the update per `brain/integrations/updates.md` — download the latest
  release and replace everything it ships, **never touching `memory/`**. If already current, say so
  and do nothing.
- After applying: report the version bump and what's new (`CHANGELOG.md`), surface any migration
  notes, and suggest starting a fresh session so the new brain loads.

If the host can't fetch the release (no network / no execution surface), tell me the manual path:
download the latest ZIP from the releases page and replace the `brain/` folder.
