#!/usr/bin/env bash
# Copies the invented project into the run's empty workspace, which is the
# working directory. Only fixture/ is copied: expected.md and graders/ stay out
# of the agent's reach.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ ! -d "$here/fixture" ]; then
  echo "scaffold: no fixture/ beside ${BASH_SOURCE[0]}" >&2
  exit 1
fi
cp -R "$here/fixture/." .
