#!/usr/bin/env bash
# Builds the ferry fixture repository: base on trunk with a protected-paths
# list, the midnight fix plus a lens edit and a new ADR on the branch.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$here/../review-fixtures/ferry/build.sh" fix,protected-fix fix-midnight-departures protected
