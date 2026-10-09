# Documentación APS-Conecta — configuración de Sphinx.
#
# La marca se transplanta, no se vuelve a dibujar: paleta y tipografía provienen
# del tema de gestión (APS-Conecta/gestion, themes/apsconecta) y se citan en
# _static/css/aps-brand.css. Los activos binarios (fuentes, logotipos, favicons)
# nunca se versionan: los obtiene `make brand` en _generated/brand/ (ignorado).
#
# html_baseurl está ausente A PROPÓSITO: emitiría etiquetas
# <link rel="canonical" href="https://…"> con host externo, que la regla de
# aislamiento del sitio (sin terceros) prohíbe. Las URLs relativas de los
# activos ya cubren el subdirectorio de GitHub Pages.

project = 'Documentación APS-Conecta'
language = 'es'

import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(__file__), '_ext'))

# upstream: los bloques tejidos de la documentación oficial de Nextcloud y sus referencias;
# rebrand: el nombre del producto en todo el sitio (iniciativa scribe; regla en upstream.yml).
extensions = ['myst_parser', 'upstream', 'rebrand']

html_theme = 'sphinx_rtd_theme'

# La segunda entrada existe solo tras `make brand`; sin ella, sphinx-build -W
# falla en la ruta estática ausente — obtener la marca antes de compilar es
# estructural, no advisory.
html_static_path = ['_static', '_generated/brand']
html_css_files = ['css/aps-brand.css']
html_logo = '_generated/brand/img/logo/logo-header.svg'
html_favicon = '_generated/brand/img/favicon.svg'
html_theme_options = {
    # Gradiente de cabecera del tema de gestión (core/css/server.css, #header).
    'style_nav_header_background': 'linear-gradient(90deg, #5315a8, #7f21fe)',
    'logo_only': True,
}

templates_path = ['_templates']

# En esta fase _generated se excluye al completo (solo activos de marca); las
# fases de generadores lo estrechan a las hojas que no son documentos.
exclude_patterns = [
    'README.md',
    'CHANGELOG.md',
    '.git',
    '.github',
    '.rpiv',
    '_generated/brand',
    '_generated/upstream',   # el clon de nextcloud/documentation: fuente, no páginas
    '_generated/attach',
    '_build',
    '_static',
    '_templates',
    'tools',
]

# linkcheck: URLs de repos privados, sembradas por tools/gen-catalogo.py en cada
# `make generate` (una URL raíz por fila privada de catalogo.yml; 9 líneas a la
# fecha). La lista queda vacía cuando la semilla aún no existe.
from pathlib import Path as _Path

_seed = _Path(__file__).with_name('_generated') / 'linkcheck-private.txt'
linkcheck_ignore = (
    [line.strip() for line in _seed.read_text(encoding='utf-8').splitlines() if line.strip()]
    if _seed.exists() else []
)

# linkcheck: anclas blob de GitHub (respaldo anclado del riesgo r2), sembradas
# por tools/gen-mapa.py en cada `make generate`. Las páginas blob de GitHub no
# exponen anclas #L<n> a un GET simple y el volumen de anclas por mapa vive
# bajo limitación de tasa de GitHub; las rutas ya se verifican localmente al
# generarse desde los checkouts de la organización. La semilla privada de
# gen-catalogo (9 URL raíz) queda intacta.
_blob_seed = _Path(__file__).with_name('_generated') / 'linkcheck-blob.txt'
linkcheck_ignore += (
    [line.strip() for line in _blob_seed.read_text(encoding='utf-8').splitlines() if line.strip()]
    if _blob_seed.exists() else []
)
