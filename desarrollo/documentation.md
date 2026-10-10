---
tipo: explicacion
audiencia: desarrollo
apps: [documentation]
resumen: "Cómo se construye este sitio: Sphinx y MyST, los archivos fuente únicos, el tejido de los manuales de la plataforma base, los generadores y las compuertas."
---
# documentation

## Contexto

[documentation](https://github.com/APS-Conecta/documentation) es el repositorio de este sitio: la fuente única, en español, de las guías para el personal de salud, la administración de las instalaciones y el desarrollo de la organización. No contiene código de producto: las aplicaciones, la distribución, las bibliotecas y los datos viven en sus propios repositorios, y el sitio solo los documenta y enlaza. La instalación y la operación de la plataforma se describen aquí, pero se ejecutan desde el repositorio de cada componente.

El sitio se compila con Sphinx y MyST, con el tema Furo y el idioma `es`, y se publica en GitHub Pages solo desde `main`. Las licencias del texto, del código de compilación y de las fuentes tipográficas, y la reserva de marcas, están en {doc}`/aviso`.

## Diseño

### Estructura del sitio

| Directorio | Audiencia | Contenido |
| --- | --- | --- |
| `usuario/` | Personal del centro de salud | Las guías de uso diario de la plataforma, de las aplicaciones propias y del inicio IntraVox |
| `administracion/` | Administración de una instalación | Instalación, arquitectura, aprovisionamiento, usuarios y grupos, oficina, mapas base, seguridad y operaciones |
| `desarrollo/` | Desarrollo | Entorno, desarrollo de aplicaciones, tema, calidad y licencias, con una página de referencia por repositorio de la organización |
| `proyecto/` | Seguimiento público | El catálogo de repositorios, las novedades, el glosario, los errores conocidos, los pendientes y la hoja de ruta |
| `_generated/` | — | Lo que escriben los generadores y los scripts de obtención en cada compilación; nunca se versiona (`.gitignore`) |

Cada página declara en su encabezado `tipo`, `audiencia`, `apps` y `resumen`, y lleva el esqueleto de secciones H2 de su `tipo`; la regla `site-structure` del canon repo-docs lo exige con nivel de error. La extensión `_ext/pagefind_meta.py` convierte `audiencia` y `apps` en filtros de la búsqueda Pagefind, y `resumen` en la descripción de la página.

### Archivos fuente únicos

| Archivo | Dueño de | Lo consumen |
| --- | --- | --- |
| `catalogo.yml` | Los repositorios de la organización: tipo, rol, manuales, dependencias y estado | `tools/gen-catalogo.py`, que escribe {doc}`/_generated/catalogo`; `tools/about-sync.py`, que replica cada rol en la descripción del repositorio en GitHub |
| `upstream.yml` | De dónde sale el texto de la plataforma base y en qué rama, cómo se nombra el producto y en qué página se teje cada documento | `tools/upstreamlib.py`, su único lector, del que dependen la extensión `_ext/upstream.py`, `tools/upstream-fidelity.py` y el tejido por lotes |
| `glosario.yml` | Los términos de la interfaz y los términos técnicos aprobados, con sus variantes que se evitan | `tools/gen-glosario.py`, que escribe {doc}`/_generated/glosario`, y `tools/term-check.py` |
| `componentes.yml` | Origen, licencia SPDX y modificaciones de cada componente | `tools/gen-componentes.py`, que escribe la tabla de componentes del aviso legal y falla si un componente distribuido no tiene fila |
| `ia.yml` | Las herramientas y los modelos de inteligencia artificial declarados | `tools/gen-ia.py`, que escribe la tabla del aviso legal, y `tools/ia-check.py` |

### El tejido de la plataforma base

Las páginas de la plataforma base tejen los manuales oficiales que publica {vendor}`Nextcloud` (`nextcloud/documentation`). La rama sigue a la suite: `stable<mayor>`, con el mayor leído de la imagen del servidor en `compose.yaml` de gestion. `tools/fetch-upstream.sh` hace un clon parcial en `_generated/upstream`, con el historial completo para que el SHA de cada bloque resuelva y solo los archivos de texto, sin descargar imágenes.

Un bloque tejido es la directiva `{upstream}`, que actúa a la vez como marcador, atribución y contexto de lectura: muestra una línea «Fuente» y, con `:difiere:`, un aviso de que APS Conecta Gestión se aparta del original. Sus referencias cruzadas conservan los destinos originales y resuelven a la página de APS donde ese documento está tejido o, mientras no lo está, al sitio de documentación del fabricante, así que un sitio a medio tejer nunca tiene un enlace muerto.

`tools/weave.py` decide qué se teje y dónde, a partir de `upstream.yml`; el traductor con inteligencia artificial nunca lo decide. El contrato de traducción es [`tools/weave-contract.md`](https://github.com/APS-Conecta/documentation/blob/main/tools/weave-contract.md): solo se traduce la prosa, y el código, los comandos, las claves de configuración, las rutas y las URL quedan byte a byte. Los catálogos oficiales en español del manual de usuario cubren cerca del 20 % del texto vigente y se usan textuales donde el original todavía coincide.

`tools/upstream-fidelity.py` contrasta cada bloque con la sección original en el SHA del propio bloque: estructura de títulos, literales, enlaces, etiquetas, redacción oficial donde existe, idioma y marcador. La traducción puede cambiar las palabras, nunca los hechos sobre los que actúa quien lee.

### El nombre del producto

`_ext/rebrand.py` reemplaza `Nextcloud` por «APS Conecta Gestión» en cada página al leerla, antes de que Sphinx reúna los títulos, así que el texto, los encabezados, la navegación y el índice de búsqueda llevan el nombre del producto. No reemplaza el código, el HTML crudo, el texto de las URL, las líneas de atribución, el rol `{vendor}`, el texto de los enlaces al sitio del fabricante, los nombres legales y de producto de `rename.keep` ni las páginas de `rename.exempt_pages`, que hoy son solo el aviso legal. Los clientes de escritorio, Android e iOS conservan su nombre de tienda mediante `{vendor}`. `tools/rebrand-check.py` prueba la regla desde fuera sobre `_build/html`, de modo que también detecta una plantilla o un generador que se salte la transformación.

### Generadores

El objetivo `generate` del `Makefile` corre los generadores antes de cada compilación; todos escriben en `_generated/`.

| Generador | Escribe |
| --- | --- |
| `tools/gen-catalogo.py` | El catálogo de repositorios, con la tabla de dependencias y la semilla de URL privadas que `linkcheck` omite. Valida la nómina, la paridad con las aplicaciones propias que instala el aprovisionamiento de gestion y que cada manual declarado exista. |
| `tools/gen-referencia.py` | La referencia de cada aplicación (comandos `occ`, ajustes y rutas) desde `appinfo/info.xml` y `appinfo/routes.php`. Degrada, nunca omite: una superficie vacía se declara con una frase «Sin …», y una entrada que no se puede interpretar corta la compilación. |
| `tools/gen-mapa.py` | El mapa de módulos de cada repositorio, extraído con graphify, salvo el almacén de artefactos, los valores por defecto de la organización y este sitio. |
| `tools/gen-inicio-rapido.py` | La sección «Inicio rápido de desarrollo» del README de cada repositorio, incluida en {doc}`/_generated/inicio-rapido/index`. |
| `tools/gen-glosario.py` | El glosario. |
| `tools/gen-componentes.py` | La tabla de componentes del aviso legal y la compuerta de deriva que la respalda. |
| `tools/gen-ia.py` | La tabla de uso de inteligencia artificial del aviso legal. |

### Compuertas

El flujo `build` corre en cada pull request, en cada push a `main` y a diario después de 📚 Scribe, para que las páginas generadas sigan la rama `main` de cada repositorio. Clona los repositorios de `catalogo.yml` con un token de GitHub App de solo lectura y envuelve cada compuerta en un objetivo de `make`, así que `-W --keep-going` vive en un solo lugar, el `Makefile`:

| Compuerta | Qué prueba |
| --- | --- |
| `make html` | Obtiene la marca y el texto original, corre los generadores, compila con advertencias como errores y construye el índice de Pagefind. |
| `make test` | Las pruebas unitarias de `tools/tests` y las autopruebas de `gen-componentes` e `ia-check`. |
| `make fidelity` | La fidelidad de cada bloque tejido y la cobertura de todos los documentos mapeados. |
| `make term-check` | Las formas aprobadas de `glosario.yml` y el registro formal, «usted» o impersonal, sin tuteo. |
| `make rebrand-check` | Ninguna mención del nombre de la plataforma base fuera de los lugares que la regla de nombre deja intactos. |
| `make linkcheck` | Los enlaces de la prosa de APS. |
| `make check-site` | El sitio servido bajo `/documentation/`, con Playwright: idioma, marca, fuentes, tema claro, diseño angosto, búsqueda y ausencia de solicitudes a terceros. |

El flujo `docs` corre además la revisión del canon repo-docs, con `gitleaks` sobre los commits de la pull request y la exigencia de un título de pull request en inglés:

```console
python3 .github/repo-docs.py check . --offline
```

Tres flujos más completan el repositorio: `about-sync` replica los roles de `catalogo.yml` en las descripciones de los repositorios cuando cambia el catálogo, `capturas` toma cada lunes las capturas de las cinco aplicaciones y abre un borrador de pull request solo si cambian, e `ia-check` comprueba cada lunes que ningún modelo ni bot escriba en los repositorios sin estar declarado en `ia.yml`. La rutina 📚 Scribe mantiene la prosa fiel al código, por carriles ({doc}`/desarrollo/agents`).

## Compromisos y límites

- **Enlaces que `linkcheck` omite.** Las URL que solo aparecen dentro de bloques tejidos no se comprueban: mantenerlas vivas es tarea del original. Tampoco se comprueban las URL de repositorios privados, las anclas de GitHub, que se arman con JavaScript, ni dos hosts que fallan de forma intermitente desde los runners de GitHub (deis.minsal.cl y gitnet.fr).
- **Traducción mayoritariamente automática.** Los catálogos oficiales en español cubren cerca del 20 % del texto vigente; el resto lo traduce un flujo con inteligencia artificial, acotado por `upstream-fidelity`.
- **Capturas comparadas por tamaño.** Dos ejecuciones locales sobre una pila nueva produjeron PNG distintos byte a byte en las cinco aplicaciones por el ruido de tiempo de gráficos y mapas en canvas, así que la compuerta semanal compara por clase de tamaño con un 5 % de tolerancia en lugar de exigir igualdad de bytes.
- **Solo modo claro.** El tema fija el modo claro; las variables oscuras repiten las claras.
- **Sin URL canónica.** `html_baseurl` falta a propósito: emitiría etiquetas canónicas con un host externo, que la regla de aislamiento del sitio prohíbe.
- **La hoja de ruta fuera de CI.** `tools/hoja-de-ruta.sh` usa la sesión de GitHub del responsable, porque el token de CI no alcanza para crear ni actualizar el proyecto de la organización; por eso no es un objetivo de `make` ni corre en CI.
- **Uso de IA sin trailer.** `ia-check` solo ve los commits que llevan un trailer `Co-Authored-By` o un autor bot; el uso de inteligencia artificial que no deja trailer es invisible para la compuerta, y `ia.yml`, declarado por una persona, sigue siendo la fuente.
