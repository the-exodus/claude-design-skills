#!/usr/bin/env bash
# Brings Tileand's code and records into the run's empty workspace, from a pinned commit,
# read-only, and writes the one project convention the case needs. Nothing of Tileand is
# kept in this repo: the graders and expected.md beside this script are generated locally
# from the owner's labels, which live outside it, and are gitignored.
#
# The runner gives a scaffold script a scrubbed environment, so the checkout is named by
# the one-line, gitignored pointer file beside the cases: evals-tileand/tileand-repo.path
set -euo pipefail

PIN=0e71d66   # THE-219 merged, THE-221's comment pass not yet

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pointer="$here/../tileand-repo.path"
if [ ! -f "$pointer" ]; then
  echo "scaffold: no $pointer. Write the path of your Tileand checkout into it to run this case." >&2
  exit 1
fi
if [ ! -d "$here/graders" ]; then
  echo "scaffold: no graders beside $0. Generate them with gen-graders.py from the owner's labels." >&2
  exit 1
fi
repo="$(head -n 1 "$pointer" | tr -d '\r')"
if ! git -C "$repo" cat-file -e "$PIN^{commit}" 2>/dev/null; then
  echo "scaffold: $repo is not a git checkout that has commit $PIN" >&2
  exit 1
fi

# git archive only reads the object store: no checkout, no index or ref is touched.
git -C "$repo" archive "$PIN" -- README.md docs src tests | tar -x -f - -C .

# At the pin this convention lived only in Tileand's gitignored local instructions, so the
# case states it, in its own words.
cat > CLAUDE.md <<'EOF'
# Conventions

- Comments under `tests/` cite no ADR or other document. A test comment whose only content is a pointer to a document is deleted, not re-pointed.
- Comments under `src/` may cite ADRs, by number.
EOF
