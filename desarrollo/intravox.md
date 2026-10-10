---
tipo: referencia
esqueleto: contratos
audiencia: desarrollo
apps: [IntraVox, gestion]
resumen: "Contratos del fork APS de IntraVox: páginas en una carpeta de grupo, publicación, bloqueos, muros, errores y la siembra que gestion converge por sección."
---
# IntraVox

## Propósito y diseño

IntraVox es la intranet de la suite: el fork de APS Conecta de IntraVox, la aplicación de VoxCloud (`nextcloud/IntraVox`), que la suite instala como aplicación propia. Los equipos de comunicaciones publican y el personal lee. El personal la encuentra como «Inicio», la portada del establecimiento ({doc}`/usuario/inicio`).

Decisiones de diseño:

- **Una página es una carpeta.** La página `<pageId>/` contiene `<pageId>.json` (widgets y diseño) y `_media/`, dentro de una carpeta de grupo. La página hereda de la carpeta todo lo que Nextcloud da a una carpeta —compartir, ACL, versiones, papelera— e IntraVox no reimplementa nada de eso.
- **La identidad es el `uniqueId`, nunca la carpeta.** El nombre de la carpeta se deriva del título y solo es único entre hermanas (una colisión recibe el sufijo `-2`, `-3`); renombrar o sufijar una carpeta no rompe enlaces, compartidos ni grupos de traducción.
- **Doce widgets.** Texto, título, imagen, enlaces, separador, vídeo, noticias, personas, calendario, fuente, historia fotográfica e historia de archivos (`ALLOWED_WIDGET_TYPES` en `lib/Service/Sanitize/PageShapeSanitizer.php`); el saneador descarta cualquier otro tipo y admite como máximo cinco columnas.
- **Comunicación de la organización, no productividad personal.** IntraVox publica para un público amplio; el Dashboard es la vista personal de cada cuenta. En la suite, la capa personal se queda en páginas de equipo con ACL, porque el personal usa computadores compartidos en sesiones cortas ([gestion ADR-0016](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0016-personal-layer-stays-page-level.md)).

El repositorio se mantiene como fork con funciones locales ([ADR-0001](https://github.com/APS-Conecta/IntraVox/blob/main/docs/adr/0001-fork-with-local-features.md)): el upstream es el motor y se incorpora; las diferencias del fork son pocas y quedan registradas. Una incorporación desde el upstream que toca una de ellas vuelve a leer ese ADR antes de fusionarse.

| Diferencia del fork | Qué hace | Registro |
|---|---|---|
| Idiomas | El valor por defecto de idiomas habilitados es `['es', 'en']` con `es` como principal (`lib/Service/LanguageService.php`); gestion ya no escribe la clave. | [gestion ADR-0018](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0018-language-reality-is-the-engines-es-only-default.md) |
| Raíz de almacenamiento | El nombre de la carpeta de grupo es un valor de la app, `groupfolder_name` (por defecto `IntraVox`), leído por una sola clase, `MountName`, que usan todas las resoluciones de rutas, el único recortador de rutas y los enlaces a Archivos. | [gestion ADR-0020](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0020-the-storage-root-is-named-for-staff.md) |
| Siembra gestionada | `occ intravox:import --skip-existing` (`ManagedTreeImporter`) nunca sobrescribe una página, un archivo ni una imagen existente. | [gestion ADR-0019](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0019-the-welcome-tree-is-declared-and-converged-per-section.md) |
| Muros | Una página con `"protected": true` rechaza eliminarse y moverse en el servidor; se edita, título incluido. | `CHANGELOG.md`, `[Unreleased]` |
| Datos de demostración | Sin descarga remota: la única fuente es `demo-data/<lang>/` empaquetado, y el paso de reparación posterior a la migración solo converge la carpeta de grupo, los grupos y los permisos, sin contenido. | `CHANGELOG.md`, `[Unreleased]` |
| Plegado compartido | `slugifyHeading` pliega los títulos con la regla compartida de aps-common, copiada en `src/aps/` por el objetivo `aps-sync` del `Makefile` del fork; `scripts/check-aps-parity.mjs` fija los anclajes byte a byte, porque están guardados en las páginas y en los enlaces compartidos. | `Makefile`, `src/utils/headingAnchors.js` |
| Documentación | Los enlaces `<documentation>` de `appinfo/info.xml` apuntan a la documentación del fork; el corpus en neerlandés y las comparaciones comerciales del upstream están retirados. | ADR-0001 |

gestion instala el fork así:

1. `OWN_APPS` incluye `intravox` desde `v3.1.0-aps1` (2026-09-25) (`provisioning/phases/12-apps.sh`). El tarball se construye desde la etiqueta del fork y su versión y sha256 quedan fijados en `provisioning/apps/intravox/VENDOR` (hoy 3.1.7, `v3.1.7-aps1`).
2. La fase 15 fija `defaultapp` en `intravox`: un inicio de sesión aterriza en la intranet ([gestion ADR-0014](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0014-intravox-is-the-default-landing-app.md)).
3. La política de apps fija `intravox:telemetry_enabled:false`: la telemetría del motor viene activada por defecto y la suite la apaga con el literal `'false'` (`provisioning/app-policy.sh`).
4. La fase 41 (`provisioning/phases/41-intravox.sh`) escribe `groupfolder_name` antes de `occ intravox:setup --skip-demo`, asigna los grupos del registro a los del motor, renderiza el árbol que el establecimiento declara y lo importa por sección, y escribe las ACL de las páginas de equipo. La guía del operador es [`docs/WELCOME-SCREEN.md`](https://github.com/APS-Conecta/gestion/blob/main/docs/WELCOME-SCREEN.md) de gestion.

## Contratos de componentes y API

La lista de rutas es la referencia generada, {doc}`/_generated/referencia/intravox`, y en el fork [`docs/route-table.md`](https://github.com/APS-Conecta/IntraVox/blob/main/docs/route-table.md), que `npm run route-table` genera y CI rechaza cuando queda desactualizada. Su resumen por exigencia de quien llama:

| Exigencia | Rutas | Ejemplos |
|---|---|---|
| Cualquier cuenta con sesión | 120 | Páginas, medios, navegación, comentarios |
| Administración | 12 | Datos de demostración, idiomas, datos huérfanos |
| Administración, comprobada en el cuerpo | 22 | Ajustes, licencia, operaciones masivas, liberar un bloqueo ajeno |
| Administración de la carpeta de equipo, comprobada en el cuerpo | 6 | Exportar e importar ZIP y Confluence |
| Anónima | 19 | `/feed/{token}`, `/api/share/{token}/…`, `/s/{shareToken}`, `/api/health` |

La superficie OCS externa (`/api/v1/pages` y sus medios) admite autenticación básica. `openapi.json` describe la API (OpenAPI 3.1.0, versión 3.1.7). La protección de fuerza bruta de la plataforma puede responder 429 en cualquier ruta autenticada tras credenciales erróneas repetidas, y sigue respondiendo 429 aunque las credenciales ya sean correctas, hasta que vence la ventana: un cliente trata el 401 como terminal y no reintenta.

Contrato de la página:

| Campo | Quién lo escribe | Contrato |
|---|---|---|
| `uniqueId` | El cliente al crear (`page-<uuid>`); el importador gestionado acuña uno si falta | Identidad estable; el servidor lo conserva en cada guardado. |
| `title` | El editor | Al crear, el nombre de la carpeta se deriva de él. |
| `status` | El editor | `draft` o `published`; una página nueva nace en `draft`. |
| `protected` | Solo el renderizador de gestion y `occ intravox:protect` | Un guardado conserva el valor almacenado, nunca el del cliente. |
| `layout` | El editor | Filas, columnas y widgets del conjunto permitido; el saneador vuelve a aplicarse en cada lectura. |
| `baseVersion` | El cliente, solo en el transporte | El mtime del archivo que el cliente cargó; nunca se persiste. |
| `filesFolderUrl` | El servidor, en la respuesta | El enlace a la carpeta de la página en Archivos; lo usan «Abrir en Archivos» y el enlace de ubicación de la barra lateral. |

El importador gestionado tiene su propio contrato de árbol: `home.json`, `navigation.json`, `footer.json`, `images/` y una carpeta `<page>/<page>.json` por página, en forma recursiva. Una carpeta que no contiene su propio `<folder>/<folder>.json` no se importa ni se recorre, y los medios de una página van en `<page>/images/`. La importación de los editores (ZIP o Confluence, `ImportService`) usa la convención `_media/`: dos públicos, dos convenciones, sin fusión por diseño. Con `--skip-existing`, un nodo existente se informa como `Skipped (exists)` y el recorrido sigue bajando, de modo que una nueva ejecución agrega lo que falta sin aplanar lo editado.

```{include} ../_generated/attach/intravox.md
```

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/intravox>
```

## Transiciones de estado

**Publicación.** `PublicationStateService::effectivePublishState()` combina la marca manual con los campos de fecha de MetaVox y devuelve uno de cuatro estados. Se evalúa al leer, sin cron.

| Estado | Condición | Lo ven |
|---|---|---|
| `draft` | Marca manual en borrador y sin fecha de publicación | Quienes pueden escribir en la página |
| `published` | Marca manual publicada, o fecha de publicación pasada, sin vencimiento cumplido | Todo lector con acceso |
| `scheduled` | Fecha de publicación futura | Quienes pueden escribir en la página |
| `expired` | Fecha de vencimiento pasada | Quienes pueden escribir en la página |

Sin MetaVox, o sin campos de fecha configurados, solo existen `draft` y `published`. gestion no instala MetaVox ([gestion ADR-0017](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0017-metavox-deferred-alert-expiry-is-editorial.md)): en la suite, un aviso vence cuando un editor lo devuelve a borrador.

**Bloqueo de edición.** `PageLockService` es un bloqueo pesimista por página en la tabla `intravox_page_locks`:

| Desde | Evento | Hacia |
|---|---|---|
| Libre | `acquireLock()` | Tomado por la cuenta |
| Tomado | `acquireLock()` de la misma cuenta, o latido (`refreshLock()`) | Tomado, con el plazo renovado |
| Tomado | `acquireLock()` de otra cuenta | Sin cambio; la respuesta devuelve quién lo tiene |
| Tomado | `releaseLock()` de su dueño | Libre |
| Tomado | `forceReleaseLock()` de la administración | Libre |
| Tomado | 15 minutos sin latido | Vencido; se borra en la siguiente consulta del bloqueo o el siguiente intento de tomarlo |

**Muro.** Una página pasa de normal a muro solo por el renderizador de gestion, al declarar una sección `wall`, o por el comando `intravox:protect` de la administración; retirarlo es el paso deliberado antes de eliminar o mover un muro. El cambio es idempotente: una página que ya está en el estado pedido no se reescribe; si cambia, primero se guarda una versión, de modo que el historial de la página lo revierte.

**Siembra por sección.** En cada siembra, la fase 41 compara la declaración `SITE_WELCOME` con la carpeta de grupo. El marcador de una sección es su página principal, `es/<sección>/<sección>.json`; el de una página de equipo, `es/equipos/<gid>/<gid>.json`; el de los archivos base, `es/navigation.json`.

| Situación | Resultado |
|---|---|
| Declarada y ausente | Se renderiza, se importa y se registra `created` |
| Declarada y presente | No se toca y se registra `exists`; lo que el personal borró dentro de ella sigue borrado |
| Presente y no declarada | `scripts/divergence.sh` la informa; nunca se elimina |
| Archivos base (`home.json`, `navigation.json`, `footer.json`) | Se renderizan solo en la primera siembra; después son datos del personal |

## Taxonomía de errores

| Código o excepción | HTTP | Significado | Reintento | Remedio del cliente |
|---|---|---|---|---|
| `PAGE_PROTECTED` | 400 | Eliminar o mover un muro | No | Retirar el muro primero, un paso deliberado de la administración descrito en «Walls» de [`docs/WELCOME-SCREEN.md`](https://github.com/APS-Conecta/gestion/blob/main/docs/WELCOME-SCREEN.md) de gestion, y repetir |
| `HOMEPAGE_PROTECTED` | 400 | Eliminar o mover la página de inicio configurada | No | Asignar otra página de inicio primero |
| `ForbiddenException` | 403 | Escritura sobre una página o carpeta en la que la cuenta solo lee | No | Pedir permiso de escritura en la carpeta de grupo |
| `PageNotFoundException` | 404 | Ningún idioma contiene ese `uniqueId` ni ese identificador antiguo | No | Corregir el identificador |
| `PageConflictException` | 409 | Guardado obsoleto: el `baseVersion` enviado es anterior al mtime del archivo | Sí, después de recargar | Recargar la página y rehacer el cambio |
| `CrossLanguageMoveException` | — | Mover una página a la carpeta de otro idioma | No | Ninguno: el rechazo es deliberado; en una operación masiva se informa por página y el resto continúa |
| `InvalidImportException` | — | El ZIP de un editor no valida: `INVALID_ZIP`, `MISSING_EXPORT_JSON`, `INVALID_JSON`, `UNSUPPORTED_VERSION`, `INCOMPLETE_EXPORT` | No | Corregir el archivo; el código es estable y el mensaje en inglés es solo el respaldo |
| `MOUNT_NAME_INVALID` | — | `groupfolder_name` vacío o con `/` | No | Corregir el valor; la fase 41 rechaza `IV_MOUNT` antes de escribirlo en el motor |

Un `PageNotFoundException` o un `ForbiddenException` nunca se convierte en 400: ambas excepciones extienden `\RuntimeException` para que los bloques que traducen `\InvalidArgumentException` a 400 no las absorban.

## Concurrencia e invariantes

- **Guardado entero, dos guardas.** El JSON de una página se escribe completo, así que un guardado obsoleto no se mezcla: borra todo lo escrito después. El bloqueo pesimista cubre el caso común; el `baseVersion` cubre la pestaña que vuelve tras un bloqueo vencido. El token es el mtime del archivo, que el sistema de archivos fija en cada escritura, y no el campo `modified` del JSON, que es lo que el cliente envió. Un cliente que no envía `baseVersion` no se bloquea.
- **La carrera por el bloqueo la resuelve la base de datos.** Un índice UNIQUE sobre `page_unique_id` impide dos bloqueos; quien pierde la inserción recibe el bloqueo existente.
- **Los muros viven en el servidor.** Ningún cliente puede activar la marca y ninguna refactorización retira la guarda del servidor.
- **Una sola raíz configurada.** Ningún código nombra la carpeta de almacenamiento con un literal; todo pasa por `MountName`.
- **La siembra nunca sobrescribe.** `--skip-existing` es obligatorio en la fase 41, y una sección existente no se vuelve a importar.
- **La asignación de grupos solo agrega.** `intravox_group_map` (gestion, `provisioning/lib.sh`) suma `all-staff` a `IntraVox Users` y `cat-jefaturas` y `role-oirs` a `IntraVox Editors`; nunca quita a nadie.

## Dominios de fallo

- **La carpeta de grupo.** Todo el contenido vive en una carpeta de grupo, y la app exige Team folders. Si `groupfolder_name` no coincide con la carpeta montada, cada página responde *IntraVox folder not found* hasta completar el cambio de nombre. La fase 41 se niega a sembrar mientras exista una carpeta con el nombre anterior: `occ intravox:setup` crearía una segunda carpeta, vacía, junto a la real.
- **La app desactivada.** `defaultapp` cae al valor fijo `dashboard,files` y el inicio de sesión aterriza en el Dashboard. No se pierde contenido: las páginas son archivos.
- **Herramientas bajo la API de páginas.** La app Archivos (un administrador de la carpeta de grupo puede eliminar la carpeta), una importación ZIP con sobrescritura y el reinicio limpio de la administración ignoran la marca de muro.
- **MetaVox ausente.** Las funciones que lo usan, como la importación y el filtrado de historias fotográficas, se degradan sin fallar.
- **La siembra interrumpida.** El renderizador falla cerrado antes de importar nada. Una siembra que muere entre la importación y las reglas deja una página de equipo sin sus ACL, y la siguiente siembra no las reescribe: se reponen a mano con `occ groupfolders:permissions`, o se elimina la carpeta de esa página y se vuelve a sembrar.
- **Contenido de demostración.** Si la marca `demo_data_imported` existe, la fase 41 se detiene: el contenido de demostración desplazaría a la portada sembrada.

## Deuda técnica y límites

- **Presupuesto de páginas.** gestion presupuesta 50 páginas como máximo; los borradores cuentan y la papelera no. El motor declara un límite gratuito de 50 páginas por idioma (`LicenseService.php`), que en el código actual solo se informa en las Configuraciones de administración: `checkPageLimit()` tiene un único llamador, `getStats()`.
- **Vencimiento editorial.** Sin MetaVox, ningún aviso se despublica solo. El disparador de adopción es que el piloto informe despublicaciones olvidadas o que el volumen de avisos supere lo que se cambia a mano.
- **Idioma de fuentes y pie.** Las fuentes y el pie de página consultan el idioma propio del lector; las cuentas de la planilla sin `core/lang` reciben `en` en esas dos superficies hasta que el motor consolide su fuente de idioma.
- **Evolución de plantillas.** Una sección existente nunca se vuelve a importar: un cambio en la biblioteca de gestion llega solo a las instalaciones que aún no tienen esa sección.
- **Equipos.** El informe de divergencia de gestion (`scripts/divergence.sh`) cubre secciones, no páginas de equipo; un equipo retirado de `SITE_TEAMS` conserva su página hasta que una persona la elimina. Quien deja un grupo conserva la lectura, porque la asignación solo agrega.
- **Tamaño.** El tarball pesa 46 MB y trae 1546 archivos: la forma de envío del upstream, con traducciones automáticas, datos de demostración y vitrinas.
- **Traducción y nombre.** Las pestañas del panel «Estructura de páginas» (`Pages`, `On this page`) no tienen traducción en `l10n/es.json` y se muestran en inglés. La entrada de la barra de aplicaciones dice «IntraVox», mientras que el instalador y la portada la llaman «Inicio».
- **Registro de cambios.** Todo lo posterior a 3.1.0 está bajo `[Unreleased]` en `CHANGELOG.md`, aunque `appinfo/info.xml` declara 3.1.7 y existen las etiquetas `v3.1.1-aps1` a `v3.1.7-aps1`.
- **Análisis estático.** La línea base de PHPStan (`phpstan-baseline.neon`) tiene 158 entradas; la regla del fork es que solo se reduce.
- **Espejo.** El repositorio de GitHub es un espejo que recibe `main` y las etiquetas; las ramas de trabajo se desarrollan y se validan antes del espejo.
