#!/usr/bin/env bash
# fetch-brand.sh — repopulate _generated/brand/ with the APS-Conecta brand assets.
#
# Source resolution (first hit wins):
#   1. $GESTION_SRC                  — explicit path (CI points it at the clone)
#   2. /opt/aps-conecta-org/gestion  — the org checkout, when present
#   3. shallow clone of APS-Conecta/gestion at main — gh if GH_TOKEN is set,
#      else git. Credentials arrive ambient (gh reads GH_TOKEN itself, git its
#      own configuration); never on the URL, never on argv.
#
# The 11-asset set (4 woff2 under fonts/, 3 logo SVG under img/logo/, 4 favicon
# files under img/) is copied from <src>/themes/apsconecta/core/ preserving
# structure. Idempotent: the destination is wiped and repopulated, so repeated
# runs produce identical bytes. No partial brand is ever left behind: every
# source asset is verified BEFORE the wipe, and the result is re-asserted as
# exactly 11 non-empty files.

set -euo pipefail

BRAND_OUT="${BRAND_OUT:-_generated/brand}"
SRC_SUBDIR="themes/apsconecta/core"

ASSETS=(
  fonts/Fraunces.woff2
  fonts/Fraunces-Italic.woff2
  fonts/NunitoSans.woff2
  fonts/NunitoSans-Italic.woff2
  img/logo/logo.svg
  img/logo/logo-header.svg
  img/logo/logo-mark.svg
  img/favicon.svg
  img/favicon.ico
  img/favicon-mask.svg
  img/favicon-touch.png
)

CLONE_TMP=""
cleanup() {
  if [[ -n "$CLONE_TMP" ]]; then
    rm -rf "$CLONE_TMP" || true
  fi
}
trap cleanup EXIT

resolve_src() {
  if [[ -n "${GESTION_SRC:-}" ]]; then
    printf '%s\n' "$GESTION_SRC"
    return
  fi
  if [[ -d /opt/aps-conecta-org/gestion ]]; then
    printf '%s\n' /opt/aps-conecta-org/gestion
    return
  fi
  local tmp clone
  tmp="$(mktemp -d)"
  CLONE_TMP="$tmp"
  clone="$tmp/gestion"
  if [[ -n "${GH_TOKEN:-}" ]]; then
    gh repo clone APS-Conecta/gestion "$clone" -- --depth 1 --branch main 1>&2
  else
    git clone --depth 1 --branch main https://github.com/APS-Conecta/gestion.git "$clone" 1>&2
  fi
  printf '%s\n' "$clone"
}

src="$(resolve_src)"
src_assets="$src/$SRC_SUBDIR"

if [[ ! -d "$src_assets" ]]; then
  echo "fetch-brand.sh: no theme assets at $src_assets" >&2
  exit 1
fi

# Verify the full set in the source BEFORE wiping: a missing asset fails the
# run and leaves any previous good copy in place.
for rel in "${ASSETS[@]}"; do
  if [[ ! -s "$src_assets/$rel" ]]; then
    echo "fetch-brand.sh: missing or empty source asset: $src_assets/$rel" >&2
    exit 1
  fi
done

rm -rf "$BRAND_OUT"
for rel in "${ASSETS[@]}"; do
  mkdir -p "$BRAND_OUT/$(dirname "$rel")"
  cp "$src_assets/$rel" "$BRAND_OUT/$rel"
done

# No partial brand: exactly 11 non-empty files, or fail.
count="$(find "$BRAND_OUT" -type f -size +0c | wc -l)"
if [[ "$count" -ne 11 ]]; then
  echo "fetch-brand.sh: expected 11 non-empty files under $BRAND_OUT, found $count" >&2
  exit 1
fi

echo "fetch-brand.sh: 11 brand assets in $BRAND_OUT (source: $src)"
