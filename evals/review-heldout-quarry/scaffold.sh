#!/usr/bin/env bash
# Builds the fixture repository in the current (empty) directory:
# main = base/, feature-postpone-blast = branch/.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
branch_name="feature-postpone-blast"

if [ -n "$(ls -A .)" ]; then
  echo "scaffold.sh: run me in an empty directory" >&2
  exit 1
fi

cp -R "$here/base/." .
git init -q -b main
git config user.name "Mira Okafor"
git config user.email "mira.okafor@example.invalid"
git add -A
git commit -q -m "blastplan: schedule, window, vibration and notices"

git checkout -q -b "$branch_name"
find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -R "$here/branch/." .
git add -A
git commit -q -m "Postpone a planned blast"
