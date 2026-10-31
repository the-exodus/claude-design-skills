#!/usr/bin/env bash
# Builds the autonomous-mode fixture in the current (empty) directory: the
# shared gaugefeed fixture, this directory's overlay on top (the guard's files,
# the archive area and ADR-0004), committed as one git repository so that a
# run can make a scratch branch. Runs as the user, outside the sandbox.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
base="$here/../gaugefeed"
for d in "$base" "$here/overlay"; do
  [ -d "$d" ] || { echo "build.sh: no $d" >&2; exit 1; }
done
cp -R "$base/." .
cp -R "$here/overlay/." .
git init -q -b main .
git config user.email dev@gaugefeed.example
git config user.name "Gaugefeed Dev"
git add -A
git commit -q -m "Gaugefeed: fetch, report and the monthly archive"
