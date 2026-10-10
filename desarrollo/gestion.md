---
tipo: referencia
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo se construye y se prueba gestion, el tronco de la suite: rama y versiones, la pila de desarrollo y cada compuerta de integración continua."
---
# gestion

## Resumen

gestion es el tronco de desarrollo de APS Conecta Gestión: configuración como código sobre la imagen oficial publicada por {vendor}`Nextcloud`, sin bifurcar el servidor.
Contiene el {doc}`aprovisionamiento </administracion/aprovisionamiento>`, el tema del servidor, el paquete de host que instala un centro, el registro DEIS de establecimientos y las compuertas que prueban todo eso.
`main` es el tronco; una versión es una etiqueta más una publicación en GitHub, y esa etiqueta es lo que instala un centro.
No hay archivo `VERSION`: el aprovisionamiento imprime `git describe --tags --always --dirty` en su primera línea, así que cada ejecución dice qué gestion la produjo.

El repositorio no compila la imagen del servidor: el fork del instalador {doc}`AIO </desarrollo/aio>` la construye incorporando los tarballs verificados y el tema de gestion.
Tres clases de aplicación salen de ese modelo:

- **De terceros**: el tarball oficial, sin cambios, va en `provisioning/apps/<id>/`, junto a un archivo `VENDOR` con versión, URL y sha256.
- **Propias**: el tarball se construye desde una etiqueta del repositorio de la aplicación y se fija en un hito, no en cada etiqueta.
- **De laboratorio**: un clon en `apps/<id>` declarado en `dev/lab-apps.sh`, que nunca entra en una versión; la fase `12-apps` solo actúa sobre una entrada cuando existe `apps/<id>/.git`.

El código es AGPL-3.0-or-later desde el 2026-08-07.
El código, los comentarios y la documentación del repositorio están en inglés; el texto de la interfaz, en español.

## Tabla

| Compuerta | Comando | Cuándo corre | Qué prueba |
|---|---|---|---|
| Búsqueda de secretos | `gitleaks detect --redact --source "$GITHUB_WORKSPACE" --exit-code 1 --verbose` | Cada pull request y cada push a `main` (`ci.yml`) | Ningún secreto en todo el historial, no solo en la punta; el registro nunca imprime el hallazgo. |
| Compuerta estática | `make test` | Cada pull request y cada push a `main`, después de `make setup` (`ci.yml`); también en local | Que Compose resuelva `compose.yaml` y `compose.dev.yaml`; `bash -n` sobre cada script, y que ningún `*.sh` versionado quede fuera de ese barrido; un tarball por aplicación, con el nombre y el sha256 de su `VENDOR`; que ninguna fase redirija la salida de un ayudante, que es lo que lee la compuerta de idempotencia; las autopruebas herméticas de `scripts/env.sh`, de `provisioning/usuarios.sh`, del Provisionador, del paquete de host, de `host/tiles.sh` y de la migración a AIO; la construcción del mapa base contra un `pmtiles` simulado; y las fijaciones de `desktop_workspace`. La prueba de humo y la de la oficina corren solo si hay una pila AIO en marcha. |
| Deriva entre aplicaciones | `scripts/check-org-drift.sh apps` | Cada pull request y cada push a `main` (`ci.yml`) | Que territorio, farmacia y estadistica compartan byte a byte `phpunit.xml` y `phpunit.integration.xml`, conserven los objetivos comunes de su `Makefile` y las reglas fijas de ESLint, y que sus copias de aps-common sean iguales entre sí y al paquete. |
| Instalación limpia | `cleanboot.yml` | Pull requests que tocan `provisioning/**`, `compose*.yaml`, `Makefile`, `scripts/**`, `sites/**`, `host/**`, `dev/**`, `.env.example` o el propio flujo; los lunes a las 06:00 UTC | Instala un centro desde cero, por dominio y por IP, con la orden silenciosa que usa un centro, y termina con `make seed-idempotent`, `bash scripts/divergence.sh --gate`, un reinicio con la tienda cerrada seguido de otra siembra, y `make test`. |
| Idempotencia | `make seed-idempotent` | Instalación limpia; también en local, justo después de `make seed` | Que una segunda siembra no escriba nada. |
| Divergencia | `bash scripts/divergence.sh --gate` | Instalación limpia | Que la instancia coincida con su declaración, cuentas incluidas; sale con código 1 ante cualquier nota. |
| Fijaciones | `bash scripts/image-digests.sh --validate`, `make images-check`, `make apps-check` | Los lunes a las 05:00 UTC, y en pull requests que tocan una fijación (`image-digests.yml`) | Que cada imagen esté fijada por resumen, e informa si una etiqueta o una aplicación de terceros tiene una versión más nueva. |
| Documentación | `python3 .github/repo-docs.py check . --offline` | Pull requests y pushes a `main` que tocan `**/*.md`, `.github/**` o `.githooks/**` (`docs.yml`) | Las reglas de documentación de la organización. |
| Versión | `bash scripts/release-manifest.sh --emit > "apsconecta-$RELEASE_TAG.manifest.json"` | Cada etiqueta `v*` (`release.yml`) | Emite el manifiesto de la versión, le agrega el sha256 del archivo de la etiqueta del que se corta el paquete de host, y lo adjunta a la publicación. |

## Notas

### El ciclo de desarrollo

1. Generar `.env` con `make setup`, que escribe los cuatro secretos con modo 600 y se niega si el archivo ya existe.
2. Elegir el establecimiento: `scripts/deis.py` escribe `sites/<slug>/site.sh` desde el registro DEIS, y `SITE` en `.env` lo nombra.
3. Converger con `make install`; `make up-dev` agrega la imagen derivada con Xdebug en el puerto 9003.
4. Ejecutar `make test` antes de abrir un pull request: es el mismo script que corre la integración continua.

`make help` lista todos los objetivos, leídos del `Makefile`.
El {doc}`entorno de desarrollo </desarrollo/entorno>` y las {doc}`compuertas de calidad </desarrollo/calidad>` de la organización tienen sus propias páginas.

### Por qué la prueba de humo pide AIO

`scripts/smoke.sh` responde solo por una instancia AIO: una pila Compose de desarrollo aparece como detenida, a propósito.
Sin una pila AIO, `make test` en local corre solo la parte estática y lo dice con una línea `skipped`.
`bash scripts/aio-testbed.sh up` levanta la instancia AIO desechable que usa la instalación limpia: las imágenes publicadas por el fork, el asistente en el puerto 8080 y apache solo en la interfaz local, sin tomar los puertos 80 ni 443 del host.
La comprobación 15 de la prueba de humo, que inicia sesión como administrador, es solo para desarrollo: en AIO la contraseña de administración es la del instalador y no la de `.env`.

### Disciplina de las compuertas

Una compuerta que no puede ponerse en rojo no es una compuerta: el barrido de `bash -n` se compara con `git ls-files` y no con un conteo, y la compuerta de las bibliotecas de mapa incorporadas muta un byte de una copia para demostrar que falla.
Un paso que no corrió se nombra en el pull request y nunca se informa como aprobado.
Un cambio de endurecimiento llega con una prueba o una aserción de configuración que `make test` ejecuta.
La instalación limpia elige un establecimiento del registro de forma determinista sobre su contenido, y no un código fijo: cualquier centro del registro es una instalación válida, y un código fijo nombraría un centro real en un registro público.

### Deuda técnica y límites

- Los tarballs de las aplicaciones viven en git, que guarda una copia completa por cada actualización; Talk ocupa 52 MB, más que todas las demás juntas.
- La compuerta de deriva todavía no compara epidemiologia, y omite la paridad con aps-common cuando no encuentra esa copia; los repositorios que compara son privados y necesitan el token `APS_BOT_PAT`.
- La instalación limpia tarda unos 15 minutos con la descarga de imágenes y tiene un límite de 60 minutos.
- La prueba de la oficina se omite en la pila Compose de desarrollo: responde solo por el servidor de documentos de AIO.

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/gestion>
```
