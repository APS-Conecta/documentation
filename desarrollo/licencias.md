---
tipo: guia
audiencia: desarrollo
apps: [.github, gestion, repo-docs, documentation, AIO]
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
| agents, pi-sandbox, rpiv-artifacts | Ninguno | Sin archivo de licencia |

En este sitio, `REUSE.toml` asigna cada ruta: la prosa de las páginas es CC-BY-3.0; `conf.py`, el `Makefile`, `tools/` y `_templates/` son AGPL-3.0-or-later; y `_static/css/aps-brand.css`, el mapeo de la marca, está reservado.

## Requisitos

- Saber quién es dueño de cada hecho: `CONTRIBUTING.md` de `.github` fija la regla de la organización; el [ADR-0010 de gestion](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0010-agpl-across-the-org.md) registra la decisión; `docs/LICENSING.md` de gestion lleva el inventario de terceros y el análisis de agregación; y `componentes.yml` de este repositorio alimenta la tabla publicada.

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
- **Un componente es AGPL-3.0-only.** El conector `eurooffice`, el servidor de documentos Euro-Office y el instalador AIO de upstream no tienen la cláusula «o posterior». La tabla de gestion declaró `eurooffice` como «o posterior» durante dos auditorías de documentación; por eso la compuerta lee el `info.xml` dentro del paquete en vez de confiar en la tabla.
- **Redis 8 ofrece tres licencias.** APS Conecta elige la AGPL v3, la única de las tres aprobada por la OSI.

### Deuda y pendientes

- agents, pi-sandbox y rpiv-artifacts no tienen `LICENSE`, contra la regla de un `LICENSE` idéntico en cada repositorio, y no corren el workflow de documentación que lo detectaría.
- La reserva de las marcas se mantiene a mano: un SVG nuevo en `mu-plugins/assets/brand/` del repositorio aps-conecta-web queda bajo la AGPL hasta que alguien lo agregue a la lista de su `LICENSE` de marcas.
- `docs/LICENSING.md` marca puntos que requieren revisión legal: el titular de los derechos es una persona natural mientras no exista una entidad legal, la disputa pública sobre los términos de la sección 7 que afecta a Euro-Office, y los términos de uso de las coordenadas del Geoportal de Chile, que no declaran licencia.
