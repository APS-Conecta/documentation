#!/usr/bin/env bash
# fetch-upstream — the nextcloud/documentation text the site weaves (iniciativa scribe).
#
# A partial clone: full commit history (so a block's SHA always resolves) but blobs only on
# demand and a sparse checkout of text files, so images never download. The branch follows the
# suite: stable<major>, with the major read from instalador's server container (upstreamlib).
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

# The server's own Spanish UI strings (core and every bundled app: settings, user_ldap, dav…), for
# the UI-label checks: a shallow, blob-less clone holding only l10n/es.json files (~2 MB).
srv="${SERVER_DIR:-_generated/server}"
if [ ! -d "$srv/.git" ]; then
  git clone --quiet --filter=blob:none --no-checkout --depth 1 --branch "$branch" https://github.com/nextcloud/server.git "$srv"
  git -C "$srv" sparse-checkout set --no-cone 'apps/*/l10n/es.json' 'core/l10n/es.json'
fi
git -C "$srv" fetch --quiet --depth 1 origin "$branch"
git -C "$srv" checkout --quiet --detach FETCH_HEAD
echo "[fetch-upstream] nextcloud/server $branch l10n @ $(git -C "$srv" rev-parse --short HEAD)"

# The store apps the suite installs (calendar, spreed…) are not organization repositories: their
# Spanish UI strings come from their own upstream repositories, same shape as the server's. The
# branch is the suite's stable<major> when the app maintains one, else its default branch.
apps="${APPS_DIR:-_generated/apps}"
while read -r id url; do
  dst="$apps/$id"
  url="$url.git"
  if git ls-remote --heads --quiet "$url" "refs/heads/$branch" | grep -q .; then
    app_branch="$branch"
  else
    app_branch="$(git ls-remote --symref --quiet "$url" HEAD | awk 'NR==1 {sub("refs/heads/", "", $2); print $2}')"
  fi
  if [ ! -d "$dst/.git" ]; then
    mkdir -p "$apps"
    git clone --quiet --filter=blob:none --no-checkout --depth 1 --branch "$app_branch" "$url" "$dst"
    git -C "$dst" sparse-checkout set --no-cone 'l10n/es.json'
  fi
  git -C "$dst" fetch --quiet --depth 1 origin "$app_branch"
  git -C "$dst" checkout --quiet --detach FETCH_HEAD
  echo "[fetch-upstream] $id $app_branch l10n @ $(git -C "$dst" rev-parse --short HEAD)"
done < <(python3 -c 'import sys; sys.path.insert(0, "tools"); import upstreamlib as u; [print(f"{i} {s}") for i, s in u.store_apps()]')
