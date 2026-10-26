---
tipo: referencia
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo se construye y se prueba gestion, el tronco de la suite: rama y versiones, la pila de desarrollo y cada compuerta de integración continua."
---
# gestion

## Resumen

gestion es el tronco de desarrollo de APS Conecta Gestión: configuración como código sobre la imagen oficial publicada por {vendor}`Nextcloud`, sin bifurcar el servidor.
Conserva la pila de desarrollo de Compose y las compuertas que la prueban.
La definición de la suite —manifiesto de aplicaciones, registro DEIS de establecimientos, datos y tema del servidor— y la mitad de instalación —paquete del host, ejecutor de aprovisionamiento y Provisionador— viven hoy en el repositorio {doc}`instalador </desarrollo/instalador>`; las copias que quedan aquí están congeladas —no se mantienen— y su retiro definitivo es decisión de la organización.
`main` es el tronco; el ritual de etiquetas se retiró: la etiqueta que instala un centro es la etiqueta de versión de instalador, que arma el paquete firmado y publica las veinte imágenes.
No hay archivo `VERSION`: su mitad congelada imprime `git describe --tags --always --dirty` en la primera línea de cada siembra, y la versión de una instalación de centro la fija el `VERSION` de instalador.

El repositorio no compila la imagen del servidor: las imágenes de la suite se construyen desde el árbol de instalador, y ninguna lleva una aplicación —las propias y los forks llegan de la publicación firmada de su propio repositorio y las de tienda, de la tienda con la puerta acotada ({doc}`AIO </administracion/aio>`).
Lo que sí es de gestion es el régimen de laboratorio: un clon en `apps/<id>` declarado en `dev/lab-apps.sh`, que nunca entra en una versión; la fase congelada de su copia solo actúa sobre una entrada cuando existe `apps/<id>/.git`, y ese mismo contrato es el que respeta la fase viva de instalador.

El código es AGPL-3.0-or-later desde el 2026-08-07.
El código, los comentarios y la documentación del repositorio están en inglés; el texto de la interfaz, en español.

## Tabla

| Compuerta | Comando | Cuándo corre | Qué prueba |
|---|---|---|---|
| Búsqueda de secretos | `gitleaks detect --redact --source "$GITHUB_WORKSPACE" --exit-code 1 --verbose` | Cada pull request y cada push a `main` (`ci.yml`) | Ningún secreto en todo el historial, no solo en la punta; el registro nunca imprime el hallazgo. |
| Compuerta estática | `make test` | Cada pull request y cada push a `main`, después de `make setup` (`ci.yml`); también en local | Que Compose resuelva `compose.yaml` y `compose.dev.yaml`; `bash -n` sobre cada script, y que ningún `*.sh` versionado quede fuera de ese barrido; que ninguna fase redirija la salida de un ayudante, que es lo que lee la compuerta de idempotencia; las autopruebas herméticas de las herramientas congeladas del repositorio; y las fijaciones de `desktop_workspace`. La prueba de humo y la de la oficina corren solo si hay una pila AIO en marcha. |
| Deriva entre aplicaciones | `scripts/check-org-drift.sh apps` | Cada pull request y cada push a `main` (`ci.yml`) | Que territorio, farmacia y estadistica compartan byte a byte `phpunit.xml` y `phpunit.integration.xml`, conserven los objetivos comunes de su `Makefile` y las reglas fijas de ESLint, y que sus copias de aps-common sean iguales entre sí y al paquete. |
| Instalación limpia | `cleanboot.yml` de instalador | En instalador: pull requests y programación; la copia de gestion quedó congelada con su mitad de instalación | Instala un centro desde cero por el bootstrap firmado, con la misma instalación silenciosa que usa un establecimiento, por dominio y por la IP del ejecutor, y termina con `make test` de instalador. |
| Idempotencia | `scripts/seed-idempotent.sh` | La instalación limpia, en instalador | Que una segunda siembra no escriba nada. |
| Divergencia | `bash scripts/divergence.sh --gate` | La instalación limpia, en instalador | Que la instancia coincida con su declaración, cuentas incluidas; sale con código 1 ante cualquier nota. |
| Fijaciones | `bash scripts/image-digests.sh --validate`, `make images-check`, `make apps-check` | Los lunes a las 05:00 UTC, y en pull requests que tocan una fijación (`image-digests.yml`) | Que cada imagen esté fijada por resumen, e informa si una etiqueta o una aplicación de terceros tiene una versión más nueva. |
| Manifiesto de versión | `bash scripts/release-manifest.sh --validate` | A demanda, sobre la copia congelada | El manifiesto de la versión que esa copia armaba. La publicación es hoy la de instalador, que arma el paquete firmado desde su propio árbol y firma su propio manifiesto. |

## Notas

### El ciclo de desarrollo

1. Generar `.env` con `make setup`, que escribe los cuatro secretos con modo 600 y se niega si el archivo ya existe.
2. Elegir el establecimiento: `scripts/deis.py` escribe `sites/<slug>/site.sh` desde el registro DEIS, y `SITE` en `.env` lo nombra.
3. Levantar la pila con `make up`; `make up-dev` agrega la imagen derivada con Xdebug en el puerto 9003, y `bash scripts/install.sh` (el envoltorio `make install` se retiró con el ciclo de etiquetas) siembra y termina con el informe de divergencia.
4. Ejecutar `make test` antes de abrir un pull request: es el mismo script que corre la integración continua.

`make help` lista todos los objetivos, leídos del `Makefile`.
El {doc}`entorno de desarrollo </desarrollo/entorno>` y las {doc}`compuertas de calidad </desarrollo/calidad>` de la organización tienen sus propias páginas.

### Por qué la prueba de humo pide AIO

`scripts/smoke.sh` responde solo por una instancia AIO: una pila Compose de desarrollo aparece como detenida, a propósito.
Sin una pila AIO, `make test` en local corre solo la parte estática y lo dice con una línea `skipped`.
`bash scripts/aio-testbed.sh up` levanta la instancia AIO desechable (la copia viva está en instalador, que la usa su instalación limpia): las imágenes publicadas por el fork, el asistente en el puerto 8080 y apache solo en la interfaz local, sin tomar los puertos 80 ni 443 del host.
La comprobación 15 de la prueba de humo, que inicia sesión como administrador, es solo para desarrollo: en AIO la contraseña de administración es la del instalador y no la de `.env`.

### Disciplina de las compuertas

Una compuerta que no puede ponerse en rojo no es una compuerta: el barrido de `bash -n` se compara con `git ls-files` y no con un conteo, y la compuerta de las bibliotecas de mapa incorporadas muta un byte de una copia para demostrar que falla.
Un paso que no corrió se nombra en el pull request y nunca se informa como aprobado.
Un cambio de endurecimiento llega con una prueba o una aserción de configuración que `make test` ejecuta.
La instalación limpia de instalador elige un establecimiento del registro de forma determinista sobre su contenido, y no un código fijo: cualquier centro del registro es una instalación válida, y un código fijo nombraría un centro real en un registro público.

### Deuda técnica y límites

- La compuerta de deriva todavía no compara epidemiologia, y omite la paridad con aps-common cuando no encuentra esa copia; los repositorios que compara son privados y necesitan el token `APS_BOT_PAT`.
- La instalación limpia de instalador tarda unos 15 minutos con la descarga de imágenes y tiene un límite de 60 minutos.
- La prueba de la oficina se omite en la pila Compose de desarrollo: responde solo por el servidor de documentos de AIO.

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/gestion>
```
