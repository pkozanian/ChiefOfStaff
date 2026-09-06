---
name: playbook-update
description: Check for a newer Chief of Staff release and, on the principal's OK, update the brain in place.
type: playbook
---

# Playbook: Update

Runs on **`/update`**, when the boot check finds a newer version, or when the principal asks to
update. The mechanics live in `brain/integrations/updates.md`; this playbook is the interaction.

## Check
1. Read the local `VERSION`; fetch the latest published `VERSION`
   (`brain/integrations/updates.md`). If the host can't fetch / there's no network, say so and give
   the manual path (README) — don't guess.
2. **Already current** → say so and stop.
3. **Newer available** → report the new version and the `CHANGELOG.md` highlights, and confirm before
   applying. (For `/update check`, stop here — report only.)

## Apply (only on an explicit OK)
Follow `brain/integrations/updates.md` → "Applying an update": download the latest release, replace
everything it ships (`brain/`, the boot files, `.claude/`'s shipped contents) **in this folder**.
**Never touch `memory/`** or `.claude/settings.local.json` — the principal's data and local settings
carry over untouched. This is an irreversible file operation on the install folder, so **confirm
first**.

## After
1. Confirm `VERSION` bumped; report the what's-new highlights.
2. **Don't migrate memory in this session** — it's now stale (still on the pre-upgrade brain). Any
   memory migration (the `CHANGELOG.md` migration notes, orphaned-override reconciliation, an optional
   `/lint` convergence) runs **automatically at the first fresh session**, driven by the new brain —
   see `brain/integrations/updates.md` → "Applying memory migrations". If the span has migration notes,
   tell the principal a one-liner that their next fresh session will apply them; their memory is
   untouched until then.
3. **Enter stale-session mode** (see `CHIEFOFSTAFF.md` → **SESSION FRESHNESS**): the swap changed the
   files on disk, but this session is still running the brain it loaded at boot, so from now on
   **prefix every reply with the stale-session banner** until the principal opens a new chat, and this
   session is now **frozen from writing memory**. Tell them plainly that the new version — and the
   migration — take effect only in a **fresh session**; this one keeps working, on the old version.
4. **Don't write the ledger here** — the freeze forbids it, and this session's brain is the old one.
   The first fresh session's migration pass records the upgrade (and any migration) in
   `memory/ledger.md` when it advances `onboarded_against`
   (`brain/integrations/updates.md` → "Applying memory migrations").

## Create the neutral skills directory (existing installs)
Run at boot by the migration pass (`brain/integrations/updates.md` → "Applying memory migrations")
when `onboarded_against` < `VERSION` and the changelog carries `path:agents-dir` — or on explicit
ask. **Idempotent:** an install where every `.claude/commands/<name>.md` already has a matching
`.agents/skills/<name>/SKILL.md` is skipped, so a re-run is a no-op.

1. Check whether every `.claude/commands/<name>.md` already has a matching
   `.agents/skills/<name>/SKILL.md`. **Yes → do nothing and say nothing.**
2. **Copy, don't compose.** For each `.claude/commands/<name>.md` **lacking a matching
   `.agents/skills/<name>/SKILL.md`**, create it with the same body, and frontmatter carrying
   `name: <name>` plus that file's existing `description:` (and `argument-hint:` where it has one).
   Use the host's file operations; writing them out as generated text is the expensive way to do
   this.
3. **No execution surface, or `.claude/commands/` is missing → skip silently.** The next update
   delivers the directory anyway.
4. Report nothing to the principal. This changes none of their content.
