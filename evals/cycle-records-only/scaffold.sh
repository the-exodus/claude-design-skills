#!/usr/bin/env bash
# Builds the ferry fixture repository: base on trunk, the case's branch on top.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$here/../review-fixtures/ferry/build.sh" records adr-refunds
