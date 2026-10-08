#!/usr/bin/env bash
# tools/hoja-de-ruta.sh — proyecto «Hoja de ruta» de la organización: crear si falta,
# publicar si no está público y verificar (URL anónima 200 + página enlazada).
#
# Idempotente y sin argumentos. Usa la sesión gh del propietario (ddespinoza): el token
# de CI (organization projects: R) no alcanza para crear ni actualizar, por lo que este
# script deliberadamente NO es un target de make ni corre en CI. Credenciales siempre
# ambientales, nunca en argv ni en URL (gh las toma de su propia configuración).
set -euo pipefail

ORG="APS-Conecta"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PAGE="$ROOT/proyecto/hoja-de-ruta.md"

die() { echo "hoja-de-ruta.sh: $1" >&2; exit 1; }

# Resuelve el proyecto por título; campos id/number/url/public verificados en
# `gh project list --format json`. Proyección @tsv: una línea, cuatro columnas.
resolve() {
  gh project list --owner "$ORG" --format json \
    --jq ".projects[] | select(.title == \"Hoja de ruta\") | [.id, (.number|tostring), .url, (.public|tostring)] | @tsv"
}

row="$(resolve)" || die "no se pudo listar los proyectos de $ORG"

if [ -z "$row" ]; then
  # gh no tiene flag público en project create: se crea y se publica después por GraphQL.
  gh project create --owner "$ORG" --title "Hoja de ruta" >/dev/null \
    || die "no se pudo crear el proyecto «Hoja de ruta» en $ORG"
  # Nunca se parsea la salida de create: se vuelve a resolver por la lista.
  row="$(resolve)" || die "no se pudo volver a listar tras crear"
  [ -n "$row" ] || die "el proyecto quedó creado pero no resuelve en gh project list"
fi

[ "$(printf '%s\n' "$row" | wc -l)" -eq 1 ] \
  || die "«Hoja de ruta» resuelve a más de un proyecto; estado de la organización ambiguo"

PROJECT_ID="$(printf '%s\n' "$row" | cut -f1)"
URL="$(printf '%s\n' "$row" | cut -f3)"
PUBLIC="$(printf '%s\n' "$row" | cut -f4)"

if [ "$PUBLIC" != "true" ]; then
  gh api graphql \
    -f query='mutation($id: ID!){ updateProjectV2(input: {projectId: $id, public: true}) { projectV2 { public } } }' \
    -f id="$PROJECT_ID" \
    --jq '.data.updateProjectV2.projectV2.public' | grep -qx true \
    || die "no se pudo publicar el proyecto (updateProjectV2)"
fi

# Compuerta A: la URL responde 200 para una visita anónima (curl sin credenciales).
code="$(curl -s -o /dev/null -w '%{http_code}' "$URL")"
[ "$code" = "200" ] || die "compuerta A (HTTP anónimo): $URL respondió $code, se esperaba 200"

# Compuerta B: la página enlaza exactamente esa URL, una sola vez.
[ -f "$PAGE" ] || die "compuerta B: falta $PAGE"
count="$(grep -cF "$URL" "$PAGE" || true)"
[ "$count" = "1" ] || die "compuerta B (enlace en la página): $PAGE menciona «$URL» ${count} veces, se esperaba 1; URL viva: $URL"

echo "$URL"
