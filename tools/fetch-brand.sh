#!/usr/bin/env bash
# fetch-brand.sh — repopulate _generated/brand/ with the APS-Conecta brand assets.
#
# Source resolution (first hit wins):
#   1. $SUITE_SRC                       — explicit path (CI points it at the clone)
#   2. /opt/aps-conecta-org/gestion-aio — the org checkout, when present
#   3. shallow clone of APS-Conecta/gestion-aio at main — gh if GH_TOKEN is set,
#      else git. Credentials arrive ambient (gh reads GH_TOKEN itself, git its
#      own configuration); never on the URL, never on argv.
#
# The 5-asset set comes from the suite's theme: the 2 woff2 fonts and the
# favicon of aps/brand/, the 2 logo SVGs of aps/theme/apsconecta/core/img/,
# each copied under the name the site serves (fonts/, img/logo/, img/). The SVGs
# name brand tokens as var(--aps-…); gestion-aio's own renderer
# (aps/provisionador/brand.py) writes each token's value in, as the suite does
# for art a browser draws without stylesheets. Idempotent: the destination is
# wiped and repopulated, so repeated runs produce identical bytes. No partial
# brand is ever left behind: the set is built and rendered in a staging
# directory that replaces the destination only once complete, and the result
# is re-asserted as exactly 5 non-empty files.

set -euo pipefail

BRAND_OUT="${BRAND_OUT:-_generated/brand}"
STAGE="$BRAND_OUT.new"

# <source path in gestion-aio>:<served path under $BRAND_OUT>
ASSETS=(
  aps/brand/fraunces.woff2:fonts/Fraunces.woff2
  aps/brand/nunito-sans.woff2:fonts/NunitoSans.woff2
  aps/theme/apsconecta/core/img/logo.svg:img/logo/logo.svg
  aps/theme/apsconecta/core/img/logoheader.svg:img/logo/logo-header.svg
  aps/brand/favicon.svg:img/favicon.svg
)

CLONE_TMP=""
cleanup() {
  rm -rf "$STAGE" || true
  if [[ -n "$CLONE_TMP" ]]; then
    rm -rf "$CLONE_TMP" || true
  fi
}
trap cleanup EXIT

resolve_src() {
  if [[ -n "${SUITE_SRC:-}" ]]; then
    printf '%s\n' "$SUITE_SRC"
    return
  fi
  if [[ -d /opt/aps-conecta-org/gestion-aio ]]; then
    printf '%s\n' /opt/aps-conecta-org/gestion-aio
    return
  fi
  local tmp clone
  tmp="$(mktemp -d)"
  CLONE_TMP="$tmp"
  clone="$tmp/gestion-aio"
  if [[ -n "${GH_TOKEN:-}" ]]; then
    gh repo clone APS-Conecta/gestion-aio "$clone" -- --depth 1 --branch main 1>&2
  else
    git clone --depth 1 --branch main https://github.com/APS-Conecta/gestion-aio.git "$clone" 1>&2
  fi
  printf '%s\n' "$clone"
}

src="$(resolve_src)"

rm -rf "$STAGE"
for pair in "${ASSETS[@]}"; do
  from="$src/${pair%%:*}" to="$STAGE/${pair#*:}"
  if [[ ! -s "$from" ]]; then
    echo "fetch-brand.sh: missing or empty source asset: $from" >&2
    exit 1
  fi
  mkdir -p "$(dirname "$to")"
  cp "$from" "$to"
done
# Another repository's code: it runs without the token.
env -u GH_TOKEN python3 -I "$src/aps/provisionador/brand.py" "$STAGE"/img/favicon.svg "$STAGE"/img/logo/*.svg

# No partial brand: exactly 5 non-empty files, or fail.
count="$(find "$STAGE" -type f -size +0c | wc -l)"
if [[ "$count" -ne 5 ]]; then
  echo "fetch-brand.sh: expected 5 non-empty files under $STAGE, found $count" >&2
  exit 1
fi
rm -rf "$BRAND_OUT"
mv "$STAGE" "$BRAND_OUT"

echo "fetch-brand.sh: 5 brand assets in $BRAND_OUT (source: $src)"
