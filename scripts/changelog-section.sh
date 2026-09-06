#!/usr/bin/env bash
# Print one release's section of src/CHANGELOG.md.
#
# The release notes on the official repo come from here rather than from GitHub's own
# `generate_release_notes`: that repo receives one squashed commit per release and has no PRs, so
# generated notes there would say nothing. The CHANGELOG is the hand-written record anyway.
#
#   changelog-section.sh 0.26.0            # the section body, for --notes-file
#   changelog-section.sh --title 0.26.0    # `0.26.0 — how much it asks you`, for --title
#
# Exits non-zero if the section is missing, so a release fails loudly rather than publishing
# empty notes.
set -euo pipefail
cd "$(dirname "$0")/.."

CHANGELOG="src/CHANGELOG.md"

want_title=0
if [ "${1:-}" = "--title" ]; then
  want_title=1
  shift
fi
ver="${1:-}"
if [ -z "$ver" ]; then
  echo "usage: $0 [--title] <version>" >&2
  exit 2
fi

# Headings are `## [x.y.z] — title`. A section runs to the next level-2 heading, whichever it is —
# the previous release, or `## [Unreleased]` when reading the top section of a dev tree.
# The version is escaped before it becomes a regex: an unescaped `.` would let 0.26.0 match 0126.0.
section="$(awk -v ver="$ver" '
  BEGIN { gsub(/\./, "\\.", ver) }
  $0 ~ "^## \\[" ver "\\]" { inside = 1; print; next }
  inside && /^## / { exit }
  inside { print }
' "$CHANGELOG")"

if [ -z "$section" ]; then
  echo "error: no '## [$ver]' section in $CHANGELOG" >&2
  exit 1
fi

if [ "$want_title" = 1 ]; then
  # `## [0.26.0] — how much it asks you` -> `0.26.0 — how much it asks you`
  printf '%s\n' "$section" | sed -n '1s/^## \[\([^]]*\)\]/\1/p'
else
  # Drop the heading, then trim the blank lines bracketing the body while keeping the ones inside
  # it: blanks before the first real line never start the output, interior blanks are held and
  # flushed by the next real line, trailing blanks are simply never flushed.
  printf '%s\n' "$section" | tail -n +2 | awk '
    NF   { while (pending-- > 0) print ""; pending = 0; seen = 1; print; next }
    seen { pending++ }
  '
fi
