---
tipo: guia
audiencia: desarrollo
apps: [.github, gestion, repo-docs, documentation, instalador]
resumen: "La licencia del código de la organización, cómo se declara en cada repositorio, la reserva de las marcas y las compuertas que verifican todo eso."
---
# Licencias

## Objetivo

Contribuir bajo la licencia de la organización y mantener coherente su declaración en cada repositorio. Todo lo que produce APS-Conecta es AGPL-3.0-or-later, y quien contribuye licencia su trabajo en los mismos términos.

La obligación se hereda, no se elige: las aplicaciones compilan `@nextcloud/vue` (AGPL-3.0-or-later) en los paquetes que sirven al personal, junto a otras bibliotecas de Nextcloud bajo GPL-3.0-or-later, como `@nextcloud/initial-state`. La cláusula de red de la AGPL, la sección 13, hace la obligación real aunque nada se publique: quien usa la intranet tiene derecho a pedir el código fuente.

La tabla de componentes de terceros que distribuye la suite, con su origen, versión, licencia y lo que APS cambia en cada uno, se genera en cada compilación de este sitio: {doc}`/_generated/componentes`.

### La licencia de cada repositorio

| Repositorio | Archivo | Licencia |
|---|---|---|
| gestion, IntraVox, farmacia, estadistica, epidemiologia, territorio, aps-common, Databases, repo-docs, `.github` | `LICENSE` | El mismo texto de la GNU AGPL v3 en todos; la organización la declara AGPL-3.0-or-later |
| documentation | `LICENSE` y `COPYING` | AGPL-3.0-or-later para las herramientas de compilación; CC BY 3.0 para el texto y las capturas del sitio |
| AIO | `LICENSE` de upstream | AGPL v3 sin la cláusula «o posterior», es decir, AGPL-3.0-only |
| rpiv-artifacts | Ninguno | Sin archivo de licencia |

En este sitio, `REUSE.toml` asigna cada ruta: la prosa de las páginas es CC-BY-3.0; `conf.py`, el `Makefile`, `tools/` y `_templates/` son AGPL-3.0-or-later; y `_static/css/aps-brand.css`, el mapeo de la marca, está reservado.

## Requisitos

- Saber quién es dueño de cada hecho: esta página fija la regla de la organización; el [ADR de AGPL en toda la organización](https://github.com/APS-Conecta/instalador/blob/main/docs/adr/0006-agpl-across-the-org.md) registra la decisión; la tabla de componentes de este sitio lleva el inventario de terceros y el análisis de agregación; y `componentes.yml` alimenta la tabla publicada.

## Pasos

1. Mantener en el repositorio un `LICENSE` idéntico al de la organización.
2. Declarar el mismo identificador, `AGPL-3.0-or-later`, en `appinfo/info.xml`, `composer.json` y `package.json`, donde existan.
3. Dejar fuera de la licencia las marcas: el logotipo, el logotipo monocromo, el logotipo con nombre y el favicon están reservados según la sección 7(e) de la AGPL. Las fichas de color siguen bajo la AGPL, como el código.
4. Al vendorizar o parchar una aplicación de terceros en gestion, dejar en `provisioning/apps/<id>/` el paquete, su archivo `VENDOR` y sus parches, y agregar la aplicación a la tabla de `docs/LICENSING.md`, que debe listar cada entrada de `APPS` y de `OWN_APPS`.
5. Declarar el componente en `componentes.yml` de este repositorio, con su licencia SPDX leída del propio componente y, si APS lo modifica, qué cambia.
6. Atribuir en `THIRD-PARTY-NOTICES.md` los paquetes de terceros que compila una aplicación.
7. En un repositorio con documentación en español, enlazar el {doc}`aviso legal </aviso>` de este sitio desde la sección «Licencia» del `README.md`.

## Verificación

El verificador de documentación de cada repositorio aplica cuatro reglas de licencia:

```bash
python3 .github/repo-docs.py check . --offline
```

| Regla | Severidad | Falla cuando |
|---|---|---|
| `license-posture` | Error | Falta `LICENSE` —una licencia no se hereda del repositorio `.github` de la organización— o la licencia no es la AGPL |
| `licence-declaration` | Error | `LICENSE`, `appinfo/info.xml`, `composer.json` y `package.json` declaran licencias distintas, o hay una declaración sin `LICENSE` |
| `licence-prose` | Error | La prosa presenta el código de la organización como cerrado, contra la licencia declarada |
| `licence-inventory` | Aviso | Una familia de licencias que usa una dependencia falta en el documento de avisos |

En gestion, el objetivo `test` del Makefile compara la tabla de `docs/LICENSING.md` con el `info.xml` de cada paquete vendorizado, sin red, y falla también si la tabla no describe ninguna aplicación. En este sitio, `make html` falla si gestion distribuye un componente que `componentes.yml` no declara, o si declara uno que ya no distribuye.

## Problemas frecuentes

- **Un `info.xml` declara `agpl`.** No es un error: el esquema de aplicaciones acepta desde siempre esa cadena como AGPL v3 o posterior, y la compuerta de gestion la normaliza.
- **Un componente es AGPL-3.0-only.** El conector `eurooffice`, el servidor de documentos Euro-Office y el instalador AIO de upstream no tienen la cláusula «o posterior».
- **Redis 8 ofrece tres licencias.** APS Conecta elige la AGPL v3, la única de las tres aprobada por la OSI.
- **Las tipografías de la marca viajan dos veces bajo la OFL-1.1.** Servidas como `.woff2` —conversión de formato del `.ttf` original: la versión original en otro contenedor, sin más requisitos— e incrustadas como subconjunto dentro de los logotipos SVG (`tools/embed-fonts.py` del instalador). Un subconjunto es una versión modificada bajo la OFL, permitido porque las fuentes no se venden solas y viajan con su licencia; los nombres reservados no se usan para las copias modificadas: los subconjuntos van incrustados, nunca distribuidos como archivos instalables bajo los nombres originales.
- **Las coordenadas del registro DEIS no declaran licencia.** El registro de establecimientos (`sites/establecimientos-deis-<fecha>.csv` del instalador) añade `latitud` y `longitud` desde el conjunto «Establecimientos de salud de Chile Junio 2026» del Geoportal de Chile: catálogo 41966, publicado por el Ministerio de Salud — DEIS con la georreferenciación de atención primaria por DIVAP, el 2026-06-12, en CRS84; el archivo fuente es la descarga GeoJSON del catálogo (5.295 puntos, sha256 `9403ba2c…`), unido por `cod_vig`: las 2.655 filas del registro emparejan. Solo se toman las dos propiedades de coordenadas, tal como se publican. Los metadatos del conjunto dejan vacías las restricciones de uso, así que donde los puntos se muestran el crédito es «Puntos: MINSAL/DEIS, Geoportal de Chile», y cualquier uso más allá del propio de los centros requiere preguntar a ideminsal@minsal.cl.

### Deuda y pendientes

- rpiv-artifacts no tiene `LICENSE`, contra la regla de un `LICENSE` idéntico en cada repositorio, y no corre el workflow de documentación que lo detectaría.
- La reserva de las marcas se mantiene a mano: un SVG nuevo en `mu-plugins/assets/brand/` del repositorio aps-conecta-web queda bajo la AGPL hasta que alguien lo agregue a la lista de su `LICENSE` de marcas.
- Esta página y la tabla de componentes marcan los puntos que requieren revisión legal: el titular de los derechos es una persona natural mientras no exista una entidad legal, la disputa pública sobre los términos de la sección 7 que afecta a Euro-Office, y los términos de uso de las coordenadas del Geoportal de Chile.
