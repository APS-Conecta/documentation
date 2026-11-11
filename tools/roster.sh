#!/usr/bin/env bash
# roster.sh — the site's build roster: every repository catalogo.yml lists.
#
#   tools/roster.sh          clone each one missing under ${APS_ORG_ROOT:-/opt/aps-conecta-org},
#                            shallow; a checkout already there is left as it is, so a second run
#                            clones nothing
#   tools/roster.sh --list   print their names, one per line
#
# Credentials stay ambient: gh reads its own session or GH_TOKEN, never argv or a URL.
set -euo pipefail

root="$(realpath -m "${APS_ORG_ROOT:-/opt/aps-conecta-org}")"
case "${1:-}" in
  "" | --list) ;;
  *) echo "usage: tools/roster.sh [--list]" >&2; exit 2 ;;
esac

cd "$(dirname "$0")/.."
names="$(python3 -c 'import yaml; print("\n".join(row["repo"] for row in yaml.safe_load(open("catalogo.yml", encoding="utf-8"))["repos"]))')"
if [[ "${1:-}" == "--list" ]]; then
  printf '%s\n' "$names"
  exit 0
fi

while IFS= read -r repo; do
  [[ -n "$repo" ]] || continue
  if [[ -d "$root/$repo/.git" ]]; then
    echo "roster: $repo is there"
  else
    gh repo clone "APS-Conecta/$repo" "$root/$repo" -- --depth 1
  fi
done <<< "$names"
