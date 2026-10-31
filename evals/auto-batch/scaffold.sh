#!/usr/bin/env bash
# Builds the autonomous-mode fixture (gaugefeed plus its overlay, committed as a
# repository) in the run's empty workspace. See design-fixtures/gaugefeed-autonomous/.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$here/../design-fixtures/gaugefeed-autonomous/build.sh"
