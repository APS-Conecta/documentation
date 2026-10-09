#!/usr/bin/env bash
# fetch-upstream — the nextcloud/documentation text the site weaves (iniciativa scribe).
#
# A partial clone: full commit history (so a block's SHA always resolves) but blobs only on
# demand and a sparse checkout of text files, so images never download. The branch follows the
# suite: stable<major>, with the major read from gestion compose.yaml (upstreamlib).
# Idempotent: an existing clone is fetched and moved to the branch tip.
set -euo pipefail
cd "$(dirname "$0")/.."
dir="${UPSTREAM_DIR:-_generated/upstream}"
read -r repo branch < <(python3 -c 'import sys; sys.path.insert(0, "tools"); import upstreamlib as u; print(u.config()["source"]["repo"], u.branch())')
if [ ! -d "$dir/.git" ]; then
  mkdir -p "$(dirname "$dir")"
  git clone --quiet --filter=blob:none --no-checkout --branch "$branch" "https://github.com/$repo.git" "$dir"
  git -C "$dir" sparse-checkout set --no-cone '/*.py' '*.rst' '*.pot' '*.txt'
fi
git -C "$dir" fetch --quiet origin "$branch"
git -C "$dir" checkout --quiet --detach "origin/$branch"
echo "[fetch-upstream] $repo $branch @ $(git -C "$dir" rev-parse --short HEAD)"
