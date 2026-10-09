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
extensions = ['myst_parser', 'upstream', 'rebrand', 'pagefind_meta']

# colon_fence: dentro de un bloque {upstream}, las directivas (avisos, tablas) usan «:::» y las
# vallas de acentos graves quedan solo para código (tools/weave-contract.md).
myst_enable_extensions = ['colon_fence']

# Furo (iniciativa scribe, Q22): diseño pensado primero para pantallas angostas, índice
# «En esta página» a la derecha y tipografía legible en capítulos largos. La marca entra por
# las variables CSS del tema; solo modo claro (las variables oscuras repiten las claras y
# _templates/base.html fija data-theme="light"); sin solicitudes a terceros.
html_theme = 'furo'

# La segunda entrada existe solo tras `make brand`; sin ella, sphinx-build -W
# falla en la ruta estática ausente — obtener la marca antes de compilar es
# estructural, no advisory.
html_static_path = ['_static', '_generated/brand']
html_css_files = ['css/aps-brand.css']
html_logo = '_generated/brand/img/logo/logo-header.svg'
html_favicon = '_generated/brand/img/favicon.svg'
html_title = 'Documentación APS Conecta'
html_show_sphinx = False
html_show_copyright = False
# Textos de la interfaz de Furo en español: locales/es/LC_MESSAGES/sphinx.po.
locale_dirs = ['locales']

_APS = {
    # Paleta del tema de gestión (themes/apsconecta/MAPEO.md §1, libro mayor de contraste).
    'color-brand-primary': '#5315a8',
    'color-brand-content': '#9a4c00',          # enlaces: oro oscuro, AA sobre blanco
    'color-brand-visited': '#7f21fe',
    'color-sidebar-background': '#5315a8',
    'color-sidebar-background-border': '#5315a8',
    'color-sidebar-brand-text': '#ffffff',
    'color-sidebar-caption-text': '#ffffff',
    'color-sidebar-link-text': '#ffffff',
    'color-sidebar-link-text--top-level': '#ffffff',
    'color-sidebar-item-background--current': '#e06f00',
    'color-sidebar-item-background--hover': 'rgba(255, 255, 255, 0.26)',
    'color-sidebar-item-expander-background--hover': 'rgba(255, 255, 255, 0.26)',
    'color-sidebar-search-background': '#ffffff',
    'color-sidebar-search-text': '#101828',
    'color-foreground-primary': '#101828',     # tinta
    'color-foreground-secondary': '#485363',   # apagado
    'color-background-primary': '#ffffff',
    'color-background-secondary': '#f7f5fb',
    'font-stack': '"Nunito Sans", system-ui, -apple-system, sans-serif',
    'font-stack--headings': '"Fraunces", Georgia, serif',
}
html_theme_options = {
    'light_css_variables': _APS,
    'dark_css_variables': _APS,
    'sidebar_hide_name': True,
    'navigation_with_keys': True,
    'top_of_page_buttons': [],
}
pygments_style = 'friendly'
pygments_dark_style = 'friendly'

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


# linkcheck: enlaces que upstream cita y que ya no responden (upstream.yml, dead_links). El texto
# tejido conserva la URL tal cual; aquí solo se omite su comprobación.
_sys.path.insert(0, _os.path.join(_os.path.dirname(__file__), 'tools'))
import re as _re
import upstreamlib as _upstreamlib

linkcheck_ignore += [_re.escape(_url) + '$' for _url in _upstreamlib.dead_links()]
# …y las anclas que ya no existen en páginas que sí responden (upstream.yml, dead_anchors).
_dead_anchors = [_re.escape(_url) + '$' for _url in _upstreamlib.dead_anchors()]

# linkcheck: GitHub arma las anclas de un README o un archivo con JavaScript, así que una URL
# github.com/...#seccion nunca muestra su ancla a un GET (falso «Anchor not found»). La URL sí
# se comprueba; solo se omite el ancla. Los textos tejidos de Nextcloud citan anclas de README
# (p. ej. github.com/42wim/matterbridge#features) y deben conservar la URL byte a byte.
linkcheck_anchors_ignore_for_url = [r'https://github\.com/.+'] + _dead_anchors

# Sin comillas tipográficas automáticas: con language='es' docutils cambia "…" por «…» también en
# texto técnico que no es código (QT_LOGGING_RULES="qt.*=true" en un texto tejido de Nextcloud),
# y un valor de configuración debe leerse tal cual. La prosa de APS escribe «…» a mano.
smartquotes = False

# Un toctree con glob en una carpeta que el tejido aún no llena no es un error: la carpeta
# existe para recibir páginas (iniciativa scribe). Sphinx 9 emite ese aviso sin `type`
# (sphinx/directives/other.py, subtype='empty_glob'), así que suppress_warnings no lo alcanza;
# un filtro de logging descarta exactamente ese mensaje y deja intactos todos los demás.
def setup(app):
    import logging as _logging

    class _EmptyGlob(_logging.Filter):
        def filter(self, record):
            return "didn't match any documents" not in str(record.msg)

    _logging.getLogger('sphinx.sphinx.directives.other').addFilter(_EmptyGlob())
