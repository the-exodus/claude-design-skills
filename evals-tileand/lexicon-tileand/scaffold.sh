#!/usr/bin/env bash
# Brings Tileand's lexicon and what it is checked against into the run's empty
# workspace, from a pinned commit, read-only. Nothing of Tileand is kept in this repo.
#
# The runner gives a scaffold script a scrubbed environment: no EVAL_* variable from
# the shell or from the case reaches it. So the checkout is named by a one-line,
# gitignored pointer file beside the cases: evals-tileand/tileand-repo.path
set -euo pipefail

PIN=3bdb64f   # the commit just before Tileand's own consolidation of its lexicon

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pointer="$here/../tileand-repo.path"
if [ ! -f "$pointer" ]; then
  echo "scaffold: no $pointer. Write the path of your Tileand checkout into it to run this case." >&2
  exit 1
fi
repo="$(head -n 1 "$pointer" | tr -d '\r')"
if ! git -C "$repo" cat-file -e "$PIN^{commit}" 2>/dev/null; then
  echo "scaffold: $repo is not a git checkout that has commit $PIN" >&2
  exit 1
fi

# git archive only reads the object store: no checkout, no index or ref is touched.
git -C "$repo" archive "$PIN" -- README.md docs src | tar -x -f - -C .
