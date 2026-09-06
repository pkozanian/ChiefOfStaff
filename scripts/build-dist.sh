#!/usr/bin/env bash
# Assemble the executive distributable ZIP — the folder an executive unzips and opens in their host
# (the Claude or ChatGPT desktop app).
#
# There is no ship-list here, on purpose. `src/` IS the product: this script copies that subtree
# verbatim, so the only way to change what ships is to change what's in `src/`. Nothing outside it
# can leak in, and nothing inside it can be forgotten. `tests/run.py` enforces the other half of the
# contract — that `brain/integrations/updates.md`'s copy recipe delivers exactly these entries, so an
# existing install receives every shipped file on `/update`.
set -euo pipefail
cd "$(dirname "$0")/.."

# Stable names (the version lives inside VERSION), so the published URLs never move:
#   https://chiefofstaff.team/dist/cos.zip           <- what the prompt boot and /update fetch
#   https://chiefofstaff.team/dist/ChiefOfStaff.zip  <- legacy shape, for pre-0.20.0 installs
VERSION="$(cat src/VERSION)"
# Output dir. Overridable so the structural suite can build into a throwaway dir and assert the
# archive shapes without clobbering a developer's dist/.
OUT="${DIST_OUT:-dist}"
NAME="ChiefOfStaff"
STAGE="${OUT}/${NAME}"

# A populated src/memory/ means someone ran Chief of Staff against the source tree. Refuse rather than
# risk shipping a developer's own memory to every executive.
stray="$(find src/memory -mindepth 1 ! -name '.keep' -print -quit)"
if [ -n "$stray" ]; then
  echo "error: src/memory/ must contain only .keep before building (found: $stray)" >&2
  exit 1
fi

rm -rf "$OUT"
mkdir -p "$STAGE"

cp -R src/. "$STAGE/"

# Local-only artifacts that live inside src/ at runtime but must never ship.
rm -f  "$STAGE/.claude/settings.local.json" "$STAGE/.claude/scheduled_tasks.lock"
rm -rf "$STAGE/.claude/agents"
find "$STAGE" -name '.DS_Store' -delete

# Two archives, one stage.
#
#   cos.zip          FLAT — the canonical artifact. Unzips its contents straight into the folder the
#                    principal is already sitting in, which is what makes the prompt boot read
#                    honestly ("unzip it into this folder"). A nested archive would land them in
#                    ChiefOfStaff/ChiefOfStaff/.
#   ChiefOfStaff.zip NESTED — a compatibility bridge, unchanged in shape. Installs from before 0.20.0
#                    run an /update recipe that hardcodes `$tmp/ChiefOfStaff`, and that recipe lives in
#                    the brain ALREADY ON DISK, so it cannot be fixed remotely. Keep publishing this
#                    until those installs have updated through it once (which hands them a recipe
#                    pointing at cos.zip), then retire it. See CONTRIBUTING.md → Releasing.
#
# The flat archive is written to $OUT, not $STAGE, so it can never contain itself.
( cd "$STAGE" && zip -r -q "../cos.zip" . )
( cd "$OUT" && zip -r -q "${NAME}.zip" "$NAME" )
echo "Built ${OUT}/cos.zip (flat) + ${OUT}/${NAME}.zip (nested, legacy) — version ${VERSION}"
