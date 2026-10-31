#!/usr/bin/env bash
# Builds the ferry fixture repository in the current (empty) directory:
#   build.sh <branch-overlay>[,<more>...] <branch-name> [<base-extra-overlay>[,<more>...]]
# base/ (plus the optional base-extra overlays) is committed on `trunk`, which a
# fake origin names as its default branch; the branch overlays are then
# committed on the branch, in the order given. Overlays hold only the files
# they add or change.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IFS=, read -r -a overlays <<< "$1"; branch="$2"
extras=(); [ -n "${3:-}" ] && IFS=, read -r -a extras <<< "$3"
for d in base "${overlays[@]}" ${extras[@]+"${extras[@]}"}; do
  [ -d "$here/$d" ] || { echo "build.sh: no $here/$d" >&2; exit 1; }
done

cp -R "$here/base/." .
for d in ${extras[@]+"${extras[@]}"}; do cp -R "$here/$d/." .; done
git init -q -b trunk .
git config user.email dev@ferrybook.example
git config user.name "Ferrybook Dev"
git add -A
git commit -q -m "Ferrybook: bookings, fares and the timetable"

# No real remote: origin/trunk and origin/HEAD are set as a fetch would leave them.
git remote add origin https://git.ferrybook.example/ferrybook.git
git update-ref refs/remotes/origin/trunk HEAD
git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/trunk

git checkout -q -b "$branch"
for d in "${overlays[@]}"; do cp -R "$here/$d/." .; done
git add -A
git commit -q -m "$branch"
