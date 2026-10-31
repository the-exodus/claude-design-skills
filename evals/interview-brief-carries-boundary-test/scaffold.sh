#!/usr/bin/env bash
# Copies the gaugefeed fixture, shared with other design cases, into the run's
# empty workspace, which is the working directory. Runs as the user, outside
# the sandbox, so it can read beside the case.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fixture="$here/../design-fixtures/gaugefeed"
if [ ! -d "$fixture" ]; then
  echo "scaffold: no gaugefeed fixture at $fixture" >&2
  exit 1
fi
cp -R "$fixture/." .
