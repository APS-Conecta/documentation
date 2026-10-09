# APS-Conecta — sitio de documentación (Sphinx + MyST).
#
# `html` y `linkcheck` siempre obtienen la marca y ejecutan los generadores
# antes de compilar: un `sphinx-build -W` sin `make brand` falla en la ruta
# estática ausente (_generated/brand). Obtener-antes-de-compilar es estructural.
#
# `generate` es el gancho que las fases de generadores van poblando
# (catálogo, referencia, mapas, inicio rápido); hoy es un no-op.

.PHONY: html linkcheck brand upstream generate fidelity rebrand-check test clean

html: brand upstream generate
	sphinx-build -W --keep-going -b html . _build/html

linkcheck: brand upstream generate
	sphinx-build -W --keep-going -b linkcheck . _build/linkcheck

brand:
	tools/fetch-brand.sh

# La plataforma base: clon parcial de nextcloud/documentation en la rama de la suite.
upstream:
	tools/fetch-upstream.sh

generate:
	python3 tools/gen-catalogo.py
	python3 tools/gen-referencia.py
	python3 tools/gen-mapa.py
	python3 tools/gen-inicio-rapido.py
	python3 tools/gen-glosario.py
	python3 tools/gen-componentes.py

# Cada bloque tejido dice lo que dice su fuente upstream (estructura, código, enlaces, texto oficial).
fidelity: upstream
	python3 tools/upstream-fidelity.py

# El sitio compilado nombra el producto «APS Conecta Gestión» (lee _build/html; correr tras html).
rebrand-check:
	python3 tools/rebrand-check.py

test:
	python3 -m unittest discover -s tools/tests
	python3 tools/gen-componentes.py --selftest

clean:
	rm -rf _build _generated

# Served-site gate: depends on the html build, serves _build/html at a
# /documentation/ subpath, and asserts the c10 families (docs/brand/fonts/
# theme/isolation) via Playwright — see tools/check-site.py.
# Separate .PHONY declaration: the Makefile chain is append-only, so this
# stanza never edits any line an earlier phase wrote.
check-site: html
	python3 tools/check-site.py

.PHONY: check-site

# Phase 11 — weekly screenshots pipeline. Single entry point shared by CI and
# local runs; tools/capturas/compose.yaml + captura.py own everything else.
# --compare sizeclass is the r8 outcome (risk r8, OQ7): two fresh-stack local
# runs (2026-10-08) produced byte-different PNGs on all five apps (−5.8%…+2.9%)
# — canvas chart/map timing noise — so the weekly gate is the pre-built 5%
# size-class fallback, per the plan's recorded r8 branch. Byte equality stays
# the driver default; flip back by dropping the flag.
.PHONY: capturas
capturas:
	python3 tools/capturas/captura.py capture --compare sizeclass
