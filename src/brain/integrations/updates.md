---
name: integration-updates
description: How Chief of Staff checks for a newer release and updates itself (brain only) on the principal's OK.
type: role
---

# Updates (prompted self-update)

Chief of Staff ships as a folder the principal downloads and opens in their host. An update
**replaces everything the release ships** — the brain, the boot files, and the agent directories —
and **never touches `memory/`** (the principal's data) or `.claude/settings.local.json`. So updating
is safe and their context carries over untouched.

Everything below is **host-agnostic**: it needs only the ability to **fetch a file and write into
this folder** — which every supported host with an execution surface has (Claude Code's shell, or
code execution in Codex, in the ChatGPT desktop app). If the host can't fetch or has no network, **skip silently** and fall
back to the manual path (README → download the latest ZIP and replace `brain/`).

## Where things live
**What a release ships:** the `brain/` directory; the boot files `AGENTS.md`, `CHIEFOFSTAFF.md`,
`CLAUDE.md`, `VERSION`, `CHANGELOG.md`, `README.md`, `LICENSE.md`; `.claude/` (its shipped contents, such as
`commands/` — not the principal's own `settings.local.json`, which lives alongside them and is never
touched); and `.agents/` (its shipped contents, such as `skills/` — the same commands, read by other
tools). A later release may add further top-level directories the same way; see "Applying an
update" below for how the recipe picks those up without naming them.

All three are published on **chiefofstaff.team**, refreshed on every release, so the check and the
apply need no account and no permission of any kind:
- **Latest version pointer:** `https://chiefofstaff.team/dist/VERSION`
  (the version of the latest published release).
- **Latest release archive (stable URL):** `https://chiefofstaff.team/dist/cos.zip` — **flat**: it
  unzips its contents straight into the folder, with no wrapper directory.
  (`https://chiefofstaff.team/dist/ChiefOfStaff.zip` is the same release wrapped in a
  `ChiefOfStaff/` directory. It exists only so installs predating 0.20.0 — whose copy of this recipe
  hardcodes that path — keep updating. Don't use it here; it will be retired.)
- **What's-new:** the `## [x.y.z]` section of `CHANGELOG.md` —
  `https://chiefofstaff.team/dist/CHANGELOG.md` (or the local copy).

## The check (gated — don't nag)
Run at boot (see `CHIEFOFSTAFF.md` boot protocol), **at most once per day** and only if the principal
hasn't turned it off (`update-check: off` in `memory/preferences/updates.md`; default on):
0. **If the local `VERSION` ends in `-dev`, skip the check.** A `-dev` build is a **development checkout
   of `main`**, already ahead of the latest release; refresh it however it was obtained, not with
   `/update`. Released
   builds always carry a clean version, so end users are unaffected.
1. Read the local `VERSION`.
2. Fetch **the latest release's** `VERSION` (the release-asset URL above). No network / no execution
   surface (or the release can't be reached) → **skip silently**.
3. Record the check date (`last_update_check: <YYYY-MM-DD>` in `memory/preferences/updates.md`) so
   you don't re-check the same day.
4. If the latest is **newer** than local → **prompt once**: name the new version and the CHANGELOG
   highlights, and ask if they'd like to update now (their memory is untouched). Don't auto-update.
   If they decline, don't re-ask until a still-newer version appears.

## Applying an update (`/update`, on the principal's OK)

Operate in **this Chief of Staff folder**. What follows is a **contract, not a script** — carry it out
with whatever this host actually has (a POSIX shell, PowerShell, Python, or the host's own file-write
API), the same way a prompt boot is a sentence rather than a command. Each step is a property
that must hold when you're done; the commands below are one way to get there, not the definition.

1. **Fetch** `https://chiefofstaff.team/dist/cos.zip` into a scratch directory **outside** this folder.
   Send an ordinary `User-Agent` — the CDN answers **403** to default library agents (a bare
   `Python-urllib/3.x` is refused; `curl` is fine), and a 403 body saved as `cos.zip` fails at step 2.
2. **Unpack it into a subdirectory of the scratch directory, then find the payload.** Unpack into a
   fresh directory nested inside the scratch directory, never the scratch directory itself — that
   also holds the archive file, and a scratch directory that contains both the archive and the payload
   makes the archive one more top-level entry the next step would copy in. The payload is the
   directory that directly contains `AGENTS.md`: the archive unpacks flat today, but check for a
   single wrapper directory too. **If you can't find `AGENTS.md`, stop and change nothing** — an
   unrecognized layout must never half-update a folder.
3. **Replace every entry the payload carries, except `memory/`.** For each top-level entry in the
   payload, remove the existing one in this folder and copy the new one in. Remove-then-copy, never
   overwrite in place — overwriting leaves behind files the new release deleted, and a stale playbook
   the index no longer lists is worse than a missing one.
4. **`.claude/` is the one entry you descend into rather than replace.** The principal's own
   `.claude/settings.local.json` and `.claude/scheduled_tasks.lock` live alongside the shipped
   `.claude/commands/`, so replace only the entries the payload actually carries inside `.claude/`
   and leave everything else there untouched.
5. **Copy nothing else** — an update **never touches `memory/`**, so the principal's files stay
   exactly as they are.
6. **Delete the scratch directory.**

Reference implementation, POSIX shell:

```bash
tmp="$(mktemp -d)"
curl -fsSL -o "$tmp/cos.zip" https://chiefofstaff.team/dist/cos.zip
# Unpack into its own subdirectory, not $tmp itself: $tmp already holds cos.zip, and a directory
# that holds both the archive and the payload makes the archive one more top-level entry the
# copy loop below would pick up.
mkdir -p "$tmp/unpacked"
unzip -q "$tmp/cos.zip" -d "$tmp/unpacked"
# Locate the payload rather than assuming its shape: cos.zip unpacks flat, but detect a wrapper
# directory too, so a future change to the archive can never strand an install on this recipe.
# `for d in $(find ...)` runs the assignment to `new` in this shell, not a subshell — a
# `find | while read` pipeline here would set `new` in a subshell and lose it silently.
new="$tmp/unpacked"
# The unquoted `$(find ...)` below word-splits on whitespace, so a wrapper directory name containing
# a space would not resolve to a single `$d` — it falls through to the "unrecognized archive layout"
# abort on the next line rather than silently mis-copying, but it is a known limitation of this form.
[ -f "$new/AGENTS.md" ] || { for d in $(find "$tmp/unpacked" -mindepth 1 -maxdepth 1 -type d); do [ -f "$d/AGENTS.md" ] && new="$d" && break; done; }
[ -f "$new/AGENTS.md" ] || { echo "update: unrecognized archive layout, aborting" >&2; exit 1; }
# Copy every entry the payload carries, except memory/. Enumerating them is how a new directory
# silently fails to reach existing installs, so don't: let the payload say what ships. Enumerate
# with find, not a glob: a glob that matches nothing (e.g. .claude/'s dotfiles — there are none) is
# a fatal error under zsh's default `nomatch`, aborting the whole update partway through. (`-mindepth`/
# `-maxdepth` are GNU/BSD/busybox extensions, not POSIX `find` — but every shell here ships one that
# supports them.)
find "$new" -mindepth 1 -maxdepth 1 | while IFS= read -r entry; do
  name="$(basename "$entry")"
  [ "$name" = "memory" ] && continue
  if [ "$name" = ".claude" ]; then
    # Descend: the principal's own settings.local.json and scheduled_tasks.lock live in here too,
    # and replacing the whole directory would delete them.
    mkdir -p .claude
    find "$entry" -mindepth 1 -maxdepth 1 | while IFS= read -r inner; do
      rm -rf ".claude/$(basename "$inner")" && cp -R "$inner" .claude/
    done
  else
    rm -rf "./$name" && cp -R "$entry" ./
  fi
done
rm -rf "$tmp"
```

On Windows without a bash shell, PowerShell does the same job — `Invoke-WebRequest` (step 1),
`Expand-Archive` into a subdirectory (2), then `Remove-Item -Recurse` followed by `Copy-Item
-Recurse` per top-level entry (3) — except `.claude/`, where only the entries the payload carries
inside it are replaced the same way, leaving the principal's own `settings.local.json` and
`scheduled_tasks.lock` untouched (4). Same contract.

- On a host with no execution surface at all, use its file-write capability, or hand the principal the
  one-line manual path (README).

## After updating
1. Read the new `VERSION` and confirm it bumped.
2. Report the **what's-new** highlights from `CHANGELOG.md`. **Don't apply any memory migration here** —
   this session is stale (still on the pre-upgrade brain), so migrations run automatically at the
   **first new session**, driven by the new brain (see "Applying memory migrations" below). If the new
   `CHANGELOG.md` shows migration notes for the span, tell the principal a one-liner — that their next
   fresh session will apply them (their memory is untouched until then).
3. **Enter stale-session mode.** The update changed the files **on disk**, but **this session is still
   running the brain it loaded at boot** — and re-reading the new files wouldn't fix that: the old brain
   is still in context, so a re-read layers a conflicting copy on top of it and refreshes only the
   always-load tier, leaving the on-demand playbooks you already pulled at the old version. (This is why
   `CHIEFOFSTAFF.md` → **RELOAD**, which re-grounds after a compaction, explicitly does **not** clear
   stale mode.) The update **takes effect on a fresh session**: a new session re-runs the boot protocol,
   loads the new brain,
   and applies any pending migration. So from now on, **prefix every reply with the stale-session
   banner** — that banner *is* the ongoing prompt to **start a fresh session**, not a second nag on top
   of it. The rule and the exact banner text live in `CHIEFOFSTAFF.md` → **SESSION FRESHNESS** (single
   source; don't restate the banner here). Reassure them this session is safe to keep using — it just
   won't have the new behavior (or the migration) until it's reloaded. "Start a fresh session" is the
   concept on both hosts; don't hardcode one host's UI.

## Applying memory migrations (after an upgrade)
A memory migration runs at the **first new session after an upgrade** — never in the session that ran
`/update` (that one is stale: still on the pre-upgrade brain, so it can't reliably migrate against the
new schema, and a stale session is **frozen from writing memory** anyway; see `CHIEFOFSTAFF.md` →
SESSION FRESHNESS). The new session's **boot** (step 2) is the single choke point for **every** upgrade
path — `/update` or a manual ZIP replace.

**Trigger:** at boot, `memory/meta.md` `onboarded_against` is older than `VERSION`. **Compare
numerically, component by component — never as text.** `0.9.0` is older than `0.10.0` and older than
`0.22.0`, though a text comparison claims the opposite; getting it backwards skips this pass in
silence, on exactly the installs with the most to migrate. This session is
current (baseline == `VERSION`), so it may write memory. Run the pass as the first order of business,
in version order:

1. **Establish the span, and say it.** **From** = `memory/meta.md` → `onboarded_against`; **to** =
   `VERSION`. If `onboarded_against` is missing, the span starts at the **earliest** release in
   `CHANGELOG.md`. That window — *"0.20.0 → 0.22.0"* — is what you assess, and it goes in the proposal
   (step 5) so the principal can see what was considered rather than taking it on trust.
2. **Collect, oldest → newest.** Read the `### Migration notes` block (older entries head it
   `### Migration`) of every release entry in the span. Each block opens with one of four
   classification lines — **No action required.**, **Required — writes at boot.**,
   **Required — no write.**, **Optional convergence.** — and carries
   subject-keyed bullets for anything actionable, each stating **the end state** a conforming folder
   is in after that release. Also **skim the entries themselves**, not only their blocks: the blocks
   are authoritative, but the skim is what catches a release that stated its position wrongly, and
   that has happened. (0.15.0 removed the per-specialist `clearance:` field and renamed `## Reads` to
   `## Key context`, changing it from a boundary to a set of optional pointers — and said nothing;
   0.18.0 made `persona:` required and renamed `name_flavor:` to `handle:`, also saying nothing. Both
   are backfilled now.)
3. **Resolve.** Bucket the keyed bullets by subject key. **Per key, keep the newest statement in the
   span and discard the earlier ones** — that is what makes an order-dependent chain come out right.
   Where 0.9.0 says a charter's pointers live in a `## Reads` section and 0.15.0 says they live under
   `## Key context`, the 0.15.0 statement wins and the intermediate section is never built. A bullet may say
   `**Supersedes X.Y.Z.**`, which states the intent; version order is what decides.
   Because each surviving bullet describes an end state rather than a change, it is correct however
   old the install is.
4. **Resolve the overlay.** Read `memory/overrides/index.md`; any brain playbook this pass invokes
   (a versioned migration, `/lint`) is resolved against `memory/overrides/` like any other brain file,
   so a principal's override still applies during migration. Reconciling orphaned overrides (step 7) is
   what lets you rely on the overlay safely — it runs before a possibly-dead override could mislead you.
5. **Assess each surviving statement against the actual folder, then propose once.** A change to
   something this install doesn't have is **not a migration for this principal** — check before you
   raise it: is there a roster? do charters carry a `## Method`, or a stale `clearance:` / `tools:`?
   are there leftover `AGENTS.md`/`CLAUDE.md` in a specialist folder, a `memory/.gitkeep`, an orphaned
   override?

   **If anything that applies would write the principal's content** — greet in one line, then put the
   whole thing in a **single** exchange: the span, what you would change and why, and what you checked
   and found nothing for. Write nothing until they say yes. Say plainly that declining a required step
   just means you'll raise it again next session, so a "no" is visibly not permanent.

   **If nothing that applies would write** — say nothing. Advance the marker and ledger it (step 9)
   and get on with the session; don't turn a no-op into noise.

   Your own bookkeeping is **not** a content write: advancing `onboarded_against` and appending the
   `update` ledger line happen either way and need no permission. Neither is a surviving statement
   that doesn't touch the principal's own content — a value corrected in `memory/meta.md`, a stale
   placeholder — so apply those the same way, without asking. That shortcut never covers deleting an
   existing file: deletion is hard to undo, so it goes through the proposal in step 5 like any other
   content change, whoever authored the file. What needs proposing is anything that changes what the
   principal wrote or owns — charters, notes, the index, overrides — or deletes a file.
6. **Run any versioned migration a note points to** *(required)*, **in the version order of the
   releases that point to them** — 0.9.0's roster build has to happen before 0.21.0's method pass,
   which has to happen before 0.22.0's specialist-file cleanup. Each is idempotent, so a re-run is a
   no-op; the ordering is what makes a multi-version jump land in the same place as upgrading one
   version at a time. Each may append its own ledger line in addition to the span line in step 9.
7. **Reconcile orphaned overrides** *(required)*. For each `## Replace`/`## Extend` entry in
   `memory/overrides/index.md`, verify its mirrored `brain/` path still exists in the new brain. For
   any that don't (the brain file the override targeted was removed), **flag it** — name the override,
   the vanished target, and the release that removed it (per `CHANGELOG.md`) — and offer the principal
   a choice: **re-home** it to a still-live target, **convert it to a pure addition** (move the entry
   to `## Additions`, drop `mode:`/`base_version:` from its frontmatter), or **retire** it. Never
   migrate an orphan silently — the delete-then-copy update mechanics above would otherwise leave it
   looking like an intentional addition (see `brain/schemas/memory-file.md` → "Override files").
8. **Offer any recommended convergence** *(optional)* — if a note suggests a `/lint` pass (e.g. to
   annotate legacy preference bullets), offer to run it now. It doesn't block.
9. **Advance the marker.** Once the **required** steps (6 and 7) are done, set
   `onboarded_against: <VERSION>` in `memory/meta.md` and append an `update` line to `memory/ledger.md`
   (`brain/schemas/capture-rules.md` → "Action ledger") recording the upgrade and the version span
   migrated. This is what makes the pass run **once**, not every boot. If the principal **defers a
   required** step, leave `onboarded_against` unchanged so the pass re-offers next boot; deferring the
   **optional** convergence (step 8) does **not** block advancing.

If `onboarded_against` is **missing** (legacy memory), treat memory as spanning from the **earliest**
release: run the full pass across the whole `CHANGELOG.md` — in particular **detect and run the
pre-roster team migration** (`brain/playbooks/team.md`) — before setting `onboarded_against: <VERSION>`.
Don't shortcut to just offering `/lint`.
