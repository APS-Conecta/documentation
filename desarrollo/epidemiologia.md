---
tipo: referencia
esqueleto: contratos
audiencia: desarrollo
apps: [epidemiologia]
resumen: "Contratos de epidemiologia: la ruta OCS de las fuentes, el ciclo de vida de cada fuente y su freno, los trabajos en segundo plano, las invariantes y la deuda."
---
# epidemiologia

## Propósito y diseño

`epidemiologia` es la aplicación de Nextcloud 34 que muestra dentro de la intranet lo que publican el MINSAL, el ISP y la OPS/OMS, y enlaza lo que no se puede mostrar. Persiste solo lo que publican sus fuentes —los metadatos de cada fuente y una copia del documento de cada informe— y no toca datos de pacientes. Es un proxy de lectura sobre una caché y dos tablas propias: la caché es el camino rápido y las tablas, la copia durable. La guía de uso es {doc}`/usuario/epidemiologia`.

La unidad del diseño es la **fuente** (`CONTEXT.md`): lo que la aplicación lee, interpreta y persiste, con su propia frescura y su propio estado degradado. Son siete, en el orden de `Sources::ALL`:

| id | Sector en la interfaz | Grano del host | Regla de almacenamiento | Intérprete |
|---|---|---|---|---|
| `alerts` | Alertas vigentes | `alerts` (degreyd.minsal.cl) | vigente: el conjunto se reemplaza entero | `PageParser` |
| `epi_alerts` | Departamento de Epidemiología | `epi` (epi.minsal.cl) | vigente | `PageParser` |
| `reports` | Circulación de Virus Respiratorios | `isp` (www.ispch.gob.cl) | serie por (año, semana), con el documento guardado | `IspReportRepository::parse()` |
| `isp_anamed` | Medicamentos (ANAMED) | `isp` | flujo: se conserva todo lo leído | `FeedParser` |
| `isp_pharmacovigilance` | Farmacovigilancia | `isp` | flujo | `FeedParser` |
| `isp_cosmetics` | Vigilancia de cosméticos | `isp` | flujo | `FeedParser` |
| `paho_alerts` | Alertas y actualizaciones | `paho` (www.paho.org) | flujo | `PahoParser` |

Las decisiones que sostienen esa forma están en los ADR del repositorio (`docs/adr/`):

- **Un solo pipeline para las seis fuentes de alertas** (`docs/adr/0017-six-alert-sectors-one-pipeline.md`, D1–D3). Cada fuente de alertas es una instancia de `AlertRepository` configurada por un `Fuente` de solo lectura y construida por la fábrica `AlertRepositories`: el contenedor de Nextcloud registra un servicio por nombre de clase, así que seis instancias configuradas de una clase son una fábrica, no seis registros. El informe conserva su propia clase, `IspReportRepository`, porque una serie de documentos semanales guardados es una regla que el pipeline no tiene.
- **Las fuentes persisten y el cliente se identifica** (`docs/adr/0015-the-fuentes-persist-and-the-fetcher-introduces-itself.md`). Cada solicitud lleva el User-Agent `APS-Conecta-Epidemiologia/1.0`, respeta el freno del host y acepta una negativa como respuesta.
- **Un contrato OCS de una sola ruta, con clave por fuente** (`docs/adr/0006-one-ocs-route-keyed-by-source.md`). El tablero y EPIVIGILA no son fuentes: son enlaces, sin nada que leer, guardar en caché ni degradar, y quedan fuera de la carga útil.
- **Sin catálogo `l10n/es.json`** (`docs/adr/0011-no-l10n-file-and-no-seam-without-an-adapter.md`). Las cadenas de la interfaz ya están en español en el código fuente, y el catálogo sería un mapa de identidad.
- **Sin rasterizar PDF** (`docs/adr/0002-no-pdf-rasterisation.md`). La imagen oficial del servidor trae la extensión `imagick` pero no Ghostscript, así que el informe se muestra como una tarjeta por semana epidemiológica.

La aplicación se integra con la plataforma por tres registros de `Application`: un proveedor de {doc}`búsqueda unificada </desarrollo/plataforma/digging-deeper/search>`, un {doc}`notificador </desarrollo/plataforma/digging-deeper/notifications>` y una {doc}`comprobación de configuración </desarrollo/plataforma/digging-deeper/setup-checks>`. Su licencia es AGPL-3.0-or-later, heredada de `@nextcloud/vue`, que el bundle compila.

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/epidemiologia>
```

## Contratos de componentes y API

### La ruta OCS `sources`

La aplicación publica una sola ruta OCS de lectura, sobre el mecanismo {doc}`OCS </desarrollo/plataforma/client-apis/ocs/index>` de la plataforma:

```text
GET /ocs/v2.php/apps/epidemiologia/api/v1/sources?format=json
OCS-APIRequest: true
```

La cabecera `OCS-APIRequest: true` es obligatoria: sin ella, Nextcloud responde 412 antes de llegar al controlador. La ruta exige sesión (`#[NoAdminRequired]`), limita a 120 solicitudes por minuto y por usuario (`#[UserRateLimit]`) y no declara `#[CORS]`, que necesita un origen concreto.

| Parámetro | Valor | Respuesta |
|---|---|---|
| ninguno | — | 200 con todas las fuentes, enteras |
| `source` | un id de `Sources::ALL` | 200 con esa fuente sola |
| `source` | un id desconocido | 404 |
| `source` vacío | `''` | igual que omitido |
| `category`, `olderThan` | `category` no vacío; `olderThan` con cualquier valor, también vacío | 400: se retiraron con la única fuente que tenía filtro |
| cualquiera, como arreglo | `?source[]=x` | 400 |

Esquema de `ocs.data` (generado de `ApiController::sources()`):

```text
<id>: {
  fetched_at: int | null    época de la última lectura; null cuando la copia sale de la tabla o cuando no hay nada guardado
  degraded:   bool          true: se sirve la última copia buena, o nada
  items: [ {
    title, url, year, month      todas las fuentes; month = 'YYYY-MM'
    se?                          reports: la semana epidemiológica
    date?                        epi_alerts, las tres del ISP y paho_alerts: el día del publicador, 'YYYY-MM-DD'
    tipo?                        paho_alerts: alerta | actualizacion | otro
  } ]                            todos los valores son string
  total:      int           = cantidad de items
  has_more:   bool          siempre false: cada respuesta es la fuente entera
}
```

Una clave que una fuente no tiene se omite, nunca es `null`. El contrato es `openapi.json`, que `scripts/openapi.sh` genera desde el controlador y nunca se edita a mano; su estabilidad es de diseño ([ADR-0006 del repositorio](https://github.com/APS-Conecta/epidemiologia/blob/main/docs/adr/0006-one-ocs-route-keyed-by-source.md)). Las rutas anteriores ya no existen: `/apps/epidemiologia/api/v1/…` desde la versión 0.2.0, y `/ocs/…/alerts` y `…/reports` desde la 0.3.0.

### La página y el estado inicial

`PageController::index()` entrega la misma carga útil que la ruta OCS en una sola clave de estado inicial, `sources`, y la dirección del tablero en otra, `tablero`; la página no hace una solicitud a sí misma al montarse. Su política de seguridad de contenido permite el marco de `https://app.powerbi.com`, sin el cual el tablero queda en blanco. En el navegador, una fuente ausente del estado inicial se lee como `{items: [], fetched_at: null, degraded: true}`: un panel vacío con aviso, nunca una aplicación en blanco.

### La ruta del informe

`GET /informe/{year}/{semana}` es una ruta simple, no OCS, fuera del contrato generado: es el enlace del panel, no un contrato publicado. Exige sesión, como el resto de la aplicación.

| Respuesta | Cuándo |
|---|---|
| 200, `application/pdf`, `inline` | la semana existe, su documento está guardado y el sha256 del archivo coincide con el de la fila |
| 303 a `https://www.ispch.gob.cl/documento/semana-{se}-{year}/` | la semana existe, pero el documento no está guardado, falta en los datos de la aplicación o no coincide con su hash (este último caso deja una advertencia en el registro) |
| 404 | la semana no existe |

El destino del 303 se construye con el año y la semana de la propia fila, siempre en https, nunca con una dirección del feed.

### Referencia generada

La lista de rutas, ajustes y trabajos declarados es la referencia generada:

```{include} ../_generated/attach/epidemiologia.md
```

### Configuración

Un solo ajuste está pensado para cambiarse, y tiene un valor por omisión que funciona; el resto de la configuración de la aplicación lo escribe la propia aplicación.

| Ajuste | Qué hace | Valor por omisión | Dónde vive |
|---|---|---|---|
| `notify_groups` | Qué grupos reciben el aviso cuando una fuente lleva 2, 7 o 30 días sin poder leerse | `["admin"]`, compilado en el código: una instalación nueva no tiene fila | Configuración de la aplicación: `occ config:app:set epidemiologia notify_groups --value='["admin","epi"]' --type=array` |
| `probe_failures_<fuente>`, `probe_failing_since_<fuente>` | Los contadores de fallas consecutivas que leen la notificación y Administración → Visión general | ausentes hasta el primer sondeo | Configuración de la aplicación, escrita solo por `ProbeRecord`: no fijar a mano |
| `backfilled_<fuente>` | Que un flujo ya recorrió sus dos páginas anteriores; borrarlo hace que la siguiente pasada profunda las recorra otra vez | ausente hasta ese recorrido | Configuración de la aplicación, escrita solo por `AlertRepository::converge()`: no fijar a mano |
| `EPI_CONTAINER`, `EPI_USER`, `EPI_BASE` | Con qué contenedor, usuario y dirección base conversan los scripts de desarrollo | `apsconecta-gestion-nextcloud-1`, `admin`, `http://localhost:8180` | Entorno, leído por `scripts/*.sh` |

Los tiempos de caché son constantes, no ajustes: una hora de frescura, treinta días como última copia buena y, detrás de cada fuente, una tabla que sobrevive a la caché (`AlertRepository`, `IspReportRepository`). Un ajuste ahí permitiría que una instancia se configurara hasta mostrar como vigente una alerta que el MINSAL ya retiró.

### Instalación y actualización

El primer arranque de un entorno de desarrollo está en el inicio rápido del README del repositorio. En una instalación real lo que cambia es la actualización: subir `<version>` en `appinfo/info.xml` es el mecanismo de entrega, porque deja la instancia en «requiere actualización» hasta que corre `occ upgrade`, y esa actualización hace llegar las migraciones, el paso de reparación y los trabajos en segundo plano.

1. Hacer `git pull` en el clon.
2. Ejecutar `docker exec -u www-data apsconecta-gestion-nextcloud-1 php occ upgrade`.
3. Reiniciar el contenedor web: los procesos web guardan las rutas y el estado de la aplicación en APCu, que `occ` no limpia (ver {ref}`epidemiologia-trampas`).

Antes de actualizar desde una versión anterior a la 0.11.0, respaldar la base de datos: su migración reescribe la clave primaria de `epidemiologia_alert` y Nextcloud no tiene migraciones de retroceso.

`js/` y `css/` están versionados, así que desplegar no requiere Node en el servidor; quien modifique `src/` ejecuta `npm run build` y confirma el resultado, y `scripts/smoke.sh` avisa si el bundle quedó atrás. `node_modules` no debe vivir en la raíz web de una instalación de producción: `.htaccess` lo cierra, pero depende de Apache y se aplica a cualquier persona, autenticada o no. Lo correcto es compilar en otro lugar y desplegar solo lo necesario.

### Añadir una fuente

El catálogo es una sola lista (`lib/Service/Sources.php`) y todo lo demás la consulta, pero consultarla sigue significando tocar cada consumidor que muestra, sondea, sirve o nombra la fuente nueva. Esta es la lista de verificación, escrita cuando seis sectores de alertas pasaron a un solo pipeline (`docs/adr/0017-six-alert-sectors-one-pipeline.md`). Con siete fuentes se conservaron a propósito los brazos `match` por método (D4 de ese ADR): un brazo omitido es un `UnhandledMatchError` con el que tropieza la batería de pruebas, nunca una respuesta equivocada.

La mayoría de las fuentes nuevas son **fuentes de alertas** —una página o un feed de alertas— y se suman al pipeline como configuración. Una fuente con reglas que el pipeline no tiene, como los documentos semanales guardados del informe, recibe un repositorio propio; en ese caso, en el servidor solo aplica lo de `Sources`.

Servidor:

1. `Sources`: la constante del id —nunca `sanitary_alerts`, que `RetireSanitaryAlerts` borra en cada actualización— y su fila en `ALL` (orden de presentación).
2. Para una fuente de alertas, su `Fuente` en `AlertRepositories::fuente()`: el id; la dirección que lee; su `host` (un host que ya existe comparte su freno y su enfriamiento, como `ISP_HOST` para www.ispch.gob.cl); el publicador y los dos nombres que usa el registro; su intérprete (`PageParser` para una página de enlaces a PDF, `FeedParser` para un feed de WordPress, `PahoParser` para la lista de la OPS/OMS, o un `Parser` nuevo con una captura real como fixture); `backfill`, las dos páginas anteriores, para un flujo y nada para una página vigente; y `bundle` solo para un host que sirve únicamente su certificado hoja.
3. El brazo de `Sources::get()`, sin `default` a propósito: un id de `ALL` sin brazo lanza `UnhandledMatchError`, y `SourcesTest` recorre `ALL` para que la falla caiga en la batería de pruebas y no frente a una persona del equipo clínico.
4. Los brazos de `Sources::probe()`, `revalidate()`, `name()`, `kind()` y `host()`, con la misma regla. `name()` es español a mitad de frase, con la institución dentro; `host()` pregunta a `AlertRepositories::host()` en una fuente de alertas, de modo que un host se escribe una sola vez, en su `Fuente`.
5. `SEARCHABLE`, solo si la fuente trae alertas que alguien buscaría por tema, y entonces también el brazo de `search()`.
6. `ACCUMULATING` y el brazo de `converge()`, solo para una fuente que conserva lo que lee y tiene páginas anteriores: todo flujo. Un conjunto vigente se reemplaza a sí mismo y no tiene nada que converger.
7. `ProbeJob` y `WarmJob`: nada, ambos recorren `Sources::ALL`. `RefreshJob`: nada más allá de `ACCUMULATING`, que recorre.
8. El contrato OCS: una clave nueva de elemento entra en el `@return` de `ApiController::sources()` y en `ApiContractTest::NOMBRES`; regenerar `openapi.json` con `scripts/openapi.sh`, nunca a mano.
9. `PageController`: nada, porque una sola clave de estado inicial, `sources`, ya lleva todas las fuentes.

Interfaz:

1. `src/panes.js`: una fuente de alertas es un sector, una entrada del registro con su `source` (el id del servidor), su grupo y el nombre de un ícono, más su entrada en `PANE_NAMES`. De esa entrada se derivan el panel (un `AlertsPane` más), la fila de navegación, la tarjeta de Inicio, las verificaciones de sectores de `scripts/layout.mjs` y la clavija de `panes.test.js` contra `Sources.php`.
2. `src/App.vue`: el componente del nombre de ícono en `ICONS`.
3. `src/pure.js`: su entrada en `SITIOS`, la página del propio publicador para esa lista, adonde el aviso de degradación envía a quien lee.
4. Un publicador nuevo: su entrada en `FUENTES` —`name` (a mitad de frase, con su artículo), `caption` (por sí solo: el rótulo de la navegación y de las tarjetas) y `count` (su sustantivo para lo que contienen sus listas)—, un bloque con rótulo en `App.vue` escrito como los tres que hay (los grupos no se pliegan, `docs/adr/0008-nav-groups-do-not-collapse.md`) y su nombre en el crédito del pie.
5. `src/state.js`: nada, porque `source(id)` lee cualquier id y una clave ausente se lee como degradada, nunca como cero.
6. `SURFACES` de `tests/unit/attribution.test.js`, si un archivo nuevo muestra nombres de publicadores.

Compuertas que deben seguir en verde:

1. `scripts/test.sh`: `SourcesTest` recorre `ALL` por todos los métodos y `AlertRepositoryTest` la recorre por `AlertRepositories`.
2. `npm test` y luego `npm run build`, con el `js/` y el `css/` reconstruidos confirmados.
3. `scripts/smoke.sh`: su línea `for source in …` nombra cada id a mano; agregar el nuevo.
4. `scripts/layout.sh`: las verificaciones de sectores derivan del registro, y la verificación 7 vuelve a medir la navegación contra el ADR 0008.

## Transiciones de estado

### Lectura de una fuente

`get()` decide en este orden, igual en `AlertRepository` y en `IspReportRepository`. La «copia guardada» es la entrada de caché o, si la caché está vacía, el conjunto que devuelve la tabla.

| Estado | Condición | Efecto | Respuesta |
|---|---|---|---|
| Fresca | copia guardada con `fetched_at` de hace menos de 3600 s | ninguno | la copia, `degraded: false` |
| En enfriamiento | `cooldown-{host}` presente | ninguno | la copia guardada, `degraded: true` |
| Frenada | `freno-{host}` vigente | ninguno | la copia guardada, `degraded: true` |
| Vencida | copia guardada, sin enfriamiento ni freno | encola `RevalidateJob`, con el marcador `revalidating-{id}` (300 s) | la copia vencida, `degraded: false` |
| Fría, primera vez | nada guardado, sin `cold-{id}` | fija `cold-{id}` (30 días) y lee en línea | la lectura nueva, o degradada |
| Fría, otra vez | nada guardado, con `cold-{id}` | encola `RevalidateJob` | `{items: [], fetched_at: null, degraded: true}` |

Una lectura (`refresh()`) termina de una de tres formas:

- **Elementos leídos.** Una fuente vigente escribe la caché y luego reemplaza su conjunto en la tabla; un flujo inserta o actualiza cada elemento en la tabla y guarda en caché lo que la tabla devuelve, así que un elemento que el publicador dejó de listar se sigue sirviendo. El informe inserta o actualiza cada semana y guarda en caché la serie completa.
- **Cero elementos**, porque no hubo lectura o porque lo leído no dio ninguno: advertencia en el registro, `cooldown-{host}` por 300 s y la última copia servida con `degraded: true`. No se escribe nada, ni en la caché ni en la tabla.
- **Falla de almacenamiento:** advertencia en el registro, nunca degradado. La lectura se sirve igual y la tabla se reintenta en la siguiente escritura.

### Freno

Una respuesta 4xx o 5xx activa el freno del host, `freno-{host}`: la espera empieza en 2 horas, se duplica con cada negativa y llega como máximo a 24 horas. Cualquier respuesta posterior que no sea una negativa lo levanta de una vez, aunque lo leído no dé elementos. Los hosts son `alerts`, `epi`, `isp` y `paho`; las cuatro fuentes de www.ispch.gob.cl comparten `isp`. La negativa de una página antigua o de un documento nunca activa el freno: la lectura barata de la primera página no paga los problemas de la solicitud profunda.

### Trabajos en segundo plano

| Trabajo | Clase base | Intervalo | Sensibilidad | Qué hace |
|---|---|---|---|---|
| `ProbeJob` | `TimedJob` | 24 h | `TIME_INSENSITIVE` | El sondeo: `probe()` de cada fuente, a través del freno. Único escritor de los contadores de fallas. |
| `WarmJob` | `TimedJob` | 1 h | `TIME_SENSITIVE` | `get()` de cada fuente: mantiene al día una instalación que nadie abre. |
| `RefreshJob` | `TimedJob` | 24 h | `TIME_INSENSITIVE` | `converge()` de cada fuente de `Sources::ACCUMULATING`: el relleno histórico y el archivo de documentos. |
| `RevalidateJob` | `QueuedJob` | a demanda | — | `revalidate()` de la fuente que lo encoló. No se declara en `appinfo/info.xml`, por eso la referencia generada no lo lista. |

Un trabajo `TIME_INSENSITIVE` corre solo dentro de la ventana de mantenimiento, que en Gestión va de 05:00 a 09:59 UTC (ver {doc}`/administracion/servidor/background-jobs-configuration` y {doc}`/desarrollo/plataforma/basics/backgroundjobs`). La sensibilidad vive en la fila del trabajo, no en su clase: la primera ejecución de un trabajo insensible escribe `time_sensitive = 0` y nada la vuelve a 1. Por eso el pase horario es una clase nueva y no `RefreshJob` con otra constante.

### Sondeo y notificaciones

`probe()` responde uno de tres veredictos (`Probe`):

| Veredicto | Significado | Efecto en el pase |
|---|---|---|
| `Healthy` | el host respondió y la fuente se leyó | el contador vuelve a 0 y la notificación se retira |
| `Unreadable` | el host respondió (una negativa, una página de WAF, un documento reestructurado) y la fuente no se lee | cuenta como falla; las demás fuentes del host se consultan igual |
| `Unreachable` | no hubo respuesta: tiempo agotado, conexión rechazada, DNS o TLS | cuenta como falla; las demás fuentes de ese host se registran como fallidas sin consultarlas |

`ProbeRecord` guarda en la configuración de la aplicación los días consecutivos de falla (`probe_failures_<id>`) y la fecha de la primera (`probe_failing_since_<id>`). Una lectura sana borra la racha. `ProbeJob` notifica en los días 2, 7 y 30 de falla consecutiva, con una sola notificación por host y pase, que nombra las demás fuentes caídas del mismo host. La reciben los usuarios de los grupos de `notify_groups` (por omisión, `["admin"]`). La comprobación de configuración «Epidemiología: conexión con las fuentes» lee los mismos contadores en Administración → Visión general: informa mientras el sondeo no ha corrido, marca éxito sin fallas y advierte con cada fuente caída y su fecha de inicio.

### Relleno histórico

- **Un flujo** recorre una vez sus dos páginas anteriores (`?paged=2` y `?paged=3` en WordPress, `?page=1` y `?page=2` en Drupal), solo con una copia guardada y con su host sin freno ni enfriamiento. Un 404 es el fin de la historia; otra falla detiene el recorrido hasta la noche siguiente. Al terminar fija `backfilled_<id>` en la configuración de la aplicación.
- **El informe** recorre el feed con un cursor (`backfill_page`, que empieza en 2 y vale 0 al agotarse), hasta 63 páginas por ejecución. Una página ilegible tres veces seguidas (`backfill_stalls`) se salta, con una advertencia en el registro.
- **El archivo de documentos** guarda hasta 10 documentos por ejecución, del más nuevo al más antiguo, en la carpeta `informes` de los datos de la aplicación. Rechaza un cuerpo de más de 8 MiB o que no empiece con `%PDF`; una fila sin documento conserva el enlace a la página del ISP y se reintenta la noche siguiente.

Las filas que agrega el relleno llegan al panel en la siguiente escritura de la fuente, que es la única salida de la tabla.

## Taxonomía de errores

En la ruta OCS:

| Código | Significado | Reintento | Remediación del cliente |
|---|---|---|---|
| 200 con `degraded: true` | la fuente no se pudo leer y se sirve la última copia buena, o nada | automático, en el servidor | mostrar el aviso; nunca leer `items: []` degradado como «sin alertas» |
| 400 | un parámetro llegó como arreglo, se envió `category` no vacío o se envió `olderThan` | no | quitar el parámetro |
| 401 | sin sesión | no | autenticarse |
| 404 | `source` no está en `Sources::ALL` | no | usar uno de los siete ids |
| 412 | falta `OCS-APIRequest: true` | no | enviar la cabecera |

Al leer una fuente, en el servidor:

| Clase de falla | Detección | Efecto | Recuperación |
|---|---|---|---|
| Negativa del host | respuesta 4xx o 5xx | freno del host, de 2 a 24 horas | la primera respuesta posterior que no sea una negativa; el sondeo diario consulta a través del freno |
| Sin respuesta | tiempo agotado (15 s), TLS, DNS | advertencia en el registro; enfriamiento del host, 300 s | automática |
| Lectura sin elementos | un 200 que no da elementos: reestructuración o página de WAF | enfriamiento del host, 300 s; nada escrito | automática; el sondeo cuenta el día |
| Cuerpo demasiado grande | más de 512 KiB | se trata como una lectura fallida | automática |
| Falla de almacenamiento | excepción del mapper | advertencia en el registro; se sirve la lectura, sin degradar | la siguiente escritura |
| Documento del informe no guardable | fetch fallido, más de 8 MiB o sin firma `%PDF` | la fila conserva el enlace a la página del ISP; sin freno ni enfriamiento | la noche siguiente |
| Documento guardado alterado | el sha256 no coincide con la fila | advertencia en el registro; 303 a la página del ISP | la administración revisa el archivo; la ruta sirve la página del ISP mientras tanto |

## Concurrencia e invariantes

- **Cero elementos es una falla, nunca un resultado.** Guardar una lista vacía reemplazaría todas las alertas reales por «no hay alertas vigentes», lo más peligroso que la aplicación podría mostrar.
- **Una fuente nunca leída está degradada y sin nada que servir**: el panel muestra el aviso solo, nunca «Sin alertas», que es lo que dice una fuente que respondió sin elementos.
- **Reemplazo atómico de una fuente vigente.** `AlertMapper::replaceSet()` borra y vuelve a insertar el conjunto de una sola fuente en una transacción; un conjunto a medio escribir nunca es visible.
- **Los flujos no usan bloqueo.** `upsert()` busca y luego escribe; dos lecturas que compiten por un elemento nuevo pierden una inserción contra la clave primaria `(fuente, url)`, y la perdedora lo registra y sirve su lectura.
- **El informe se lee de a uno.** `refreshLocked()` toma un bloqueo atómico (`add()`) de 1440 s en la caché de bloqueos; la solicitud que pierde sirve la copia que ya tiene. Lo que vuelve inofensiva una inserción concurrente es la clave primaria `(year, se)`.
- **Una revalidación por fuente.** El marcador `revalidating-{id}` (300 s) deduplica el encolado y se borra en un `finally`; antes de leer, `revalidate()` vuelve a consultar el enfriamiento y el freno del host, porque otra fuente del mismo host pudo encontrar la caída después de encolarse el trabajo.
- **Un solo escritor de los contadores de fallas.** Solo `ProbeJob`, a través de `ProbeRecord`, escribe los contadores; `WarmJob` y `RefreshJob` no los tocan. Por eso la notificación y la comprobación de configuración pueden quedar incompletas, pero nunca contradecirse.
- **Lo que sobrevive a la caché vive en la configuración de la aplicación.** Los contadores, el cursor del informe y las marcas `backfilled_<id>` están en `IAppConfig`, no en la caché: un vaciado de la caché no debe dar por sana una fuente caída ni pedir que se recorra otra vez una tabla que conserva la historia.
- **La caché cambia de espacio de nombres con cualquier actualización de aplicaciones de la instancia** (`docs/adr/0012-the-archive-is-a-cache-and-any-app-update-empties-it.md`), así que la tabla es el respaldo durable de `get()`, `probe()` y `search()`.
- **La búsqueda nunca consulta la red.** El proveedor de búsqueda lee la caché y, si está vacía, la tabla; un proveedor que consultara a un publicador haría esperar a toda la búsqueda de Nextcloud. La comprobación de configuración tampoco consulta la red.
- **Los PDF se leen de los enlaces, nunca se construyen.** Los nombres de archivo de ningún publicador se pueden derivar de lo que identifica al documento: el ISP agrega un sufijo de versión cuando reemite una semana (`…SE35-08-09-2026-V3`) y el MINSAL rellena dos de sus `href` con un espacio final dentro de las comillas. Cada intérprete lee lo que el publicador sirve y no lo que una regla predeciría; una reedición reemplaza su propia semana y nunca agrega una tercera fila.
- **Identidad.** Una alerta es `(fuente, url)`: el mismo PDF en dos sectores son dos filas. Un informe es `(year, se)`: una reedición reemplaza su propia semana y nunca crea otra fila.
- **El día pertenece a quien publica.** La fecha de un elemento se calcula en la zona horaria del publicador (`America/Santiago` para el ISP), no en la del servidor ni en la del lector, y el año de una semana epidemiológica sale de esa fecha.
- **El archivo se escribe antes de que la fila lo reclame**, así que una fila que dice «guardado» siempre nombra bytes que existen.

## Dominios de fallo

- **El host es el dominio de falla.** Una negativa o un tiempo agotado de www.ispch.gob.cl detiene a la vez el informe y las tres fuentes de alertas del ISP; degreyd.minsal.cl, epi.minsal.cl y www.paho.org fallan cada uno por su cuenta.
- **El punto de vista importa.** Desde un centro de datos, epi.minsal.cl responde con el 403 de Cloudflare y el ISP no responde (medido el 27 de septiembre de 2026): cuatro sectores muestran solo su aviso, y la notificación los nombra, junto con el informe, en los días 2, 7 y 30. Una instalación con conexión residencial lee los seis.
- **El certificado del ISP.** www.ispch.gob.cl envía solo su certificado hoja. La aplicación trae el intermedio que falta (`certs/gsgccr6alphasslca2025.crt`) y `CertificateBundle` lo une a las anclas de la instancia solo para las solicitudes al ISP, sin desactivar la verificación. Si la instancia no tiene un directorio temporal con escritura, la unión se omite y las cuatro fuentes del ISP se degradan.
- **El WAF del ISP responde vacío a un User-Agent literal `curl/*`**, igual que una falla de TLS; la aplicación se identifica en cada solicitud, así que una reproducción con `curl` sin User-Agent no prueba que el host esté caído.
- **Una lectura fría ocurre durante la carga de la página.** La primera lectura de una fuente sin nada guardado se hace en línea, acotada a 15 s por fuente; las siguientes se encolan.
- **En la interfaz, un panel que falla no arrastra a los demás**: cada panel tiene su propio límite de errores.
- **La búsqueda unificada no depende de los publicadores.** Además, `appinfo/info.xml` declara la extensión `intl`, que `fold()` necesita, para que un host sin ella no pueda activar la aplicación y romper la búsqueda global.

### Rotar el certificado del ISP

Si el ISP deja de responder, leer la cadena antes de suponer una caída. Esto muestra con qué firma hoy y dónde vive su intermedio:

```text
openssl s_client -connect www.ispch.gob.cl:443 -servername www.ispch.gob.cl </dev/null 2>/dev/null \
  | openssl x509 -noout -issuer -ext authorityInfoAccess
```

Si cambió, hay dos arreglos. El de una instancia es importar el certificado de «CA Issuers» que muestra esa salida, con `occ security:certificates:import`. El durable es reemplazar `certs/gsgccr6alphasslca2025.crt` del repositorio por ese mismo certificado, conversión de DER incluida, como detalla `certs/README.md`. El 15 de septiembre de 2026 la hoja del ISP se reemitió bajo `GlobalSign GCC R6 AlphaSSL CA 2025` mientras el almacén de confianza seguía con el de `GlobalSign RSA OV SSL CA 2018`: toda solicitud falló con `cURL error 60` y la fuente quedó muerta sin que nada dijera por qué. Se midió en un host sin importación, el 16 de septiembre: `cURL error 60` con solo las anclas del sistema y `200` con esas mismas anclas más ese único archivo. La verificación sigue activa en todo momento, porque un certificado en un CAfile es un ancla adicional, no una forma de evitar la verificación: nunca se usa `verify=False`.

Nada oculta la falla: la advertencia lleva el error de transporte, así que el código de cURL queda en `nextcloud.log` sin bajar el nivel de registro a `debug`.

## Deuda técnica y límites

- **Los establecimientos reciben la versión que resuelve el instalador.** La suite instala epidemiologia desde la release más nueva compatible con su Nextcloud, publicada y firmada en el repositorio propio de la aplicación ([ADR-0017 de la suite](https://github.com/APS-Conecta/instalador/blob/main/docs/adr/0017-apps-install-from-their-own-releases.md)); la versión queda registrada en el archivo de bloqueo del servidor. Esta página describe la versión de `main`.
- **Una actualización de `<version>` deja la instancia en «requiere actualización»** hasta que corre `occ upgrade`; `occ app:enable` sobre una aplicación ya activa no registra los trabajos.
- **La migración de la versión 0.11.0 reescribe la clave primaria** de `epidemiologia_alert` a `(fuente, url)`, y Nextcloud no tiene migraciones de retroceso: el único retroceso es restaurar un respaldo de la base de datos tomado antes y reinstalar la versión 0.10.0.
- **El certificado del ISP fija un emisor.** El certificado hoja vence el 23 de noviembre de 2026 y nada detecta un cambio de emisor; si cambia, las cuatro fuentes del ISP fallan con `cURL error 60` hasta reemplazar el archivo de `certs/`.
- **Superficie de SSRF.** La dirección del PDF de cada informe sale del feed y puede apuntar a cualquier host https; la protegen el cliente HTTP de la plataforma, que rechaza direcciones locales, el tiempo máximo, el tope de 8 MiB y la firma `%PDF`. El modelo de amenazas no registra riesgos aceptados.
- **Sin `#[CORS]`** en la ruta OCS, a la espera de un origen concreto.
- **Nada propaga el establecimiento a la aplicación**: lee `notify_groups` y sus propios contadores, y nada más.
- **`scripts/smoke.sh` y `scripts/layout.sh` se ejecutan a mano**, contra una instancia aprovisionada.
- **Orden dentro del mes.** La tabla no conserva el orden de las alertas de degreyd.minsal.cl dentro de un mes (no hay columna de secuencia y esa página no publica días); la caché sí lo conserva.
- **Topes sin medir o parciales.** El tope de 8 MiB por documento nunca se midió contra el ISP; el tope de 512 KiB del feed acota la interpretación, no la descarga; la espera base del freno supone una cadencia horaria.
- **Drupal responde 200 vacío después de su última página**, y el relleno lo lee como ilegible, no como agotado; hoy no ocurre porque la lista de la OPS/OMS tenía 38 páginas el 28 de septiembre de 2026 y el relleno recorre dos.
- **No construido:** notificaciones al personal por alertas nuevas, facetas por enfermedad o por subtipo del ISP, deduplicación entre sectores, niveles de gravedad, las otras 21 categorías del ISP y cualquier forma de evadir un bloqueo.
- **Límites del dominio.** El contexto no tiene palabra para una tasa local de enfermedad, porque ninguna fuente la produce, ni organiza nada por enfermedad: ninguna fuente publica a ese grano.

(epidemiologia-trampas)=
### Trampas de la plataforma

- **`occ app:enable` sobre una aplicación ya activa no registra los trabajos en segundo plano.** Si `smoke.sh` informa que falta uno, ejecutar `occ app:disable` y luego `occ app:enable`. `occ upgrade` registra todos: así la versión 0.11.0 agregó `WarmJob`. Después de habilitar, `occ background-job:list` debe mostrar exactamente tres filas: `ProbeJob`, `RefreshJob` y `WarmJob`.
- **La sensibilidad de un trabajo no se cambia en el lugar.** `oc_jobs.time_sensitive` parte en 1, la primera ejecución de un trabajo `TIME_INSENSITIVE` escribe 0, nada vuelve a escribir 1 y una actualización no lo restablece. `occ background-job:list` tampoco imprime el intervalo: leer `oc_jobs` o el campo «Next execution» de `occ background-job:execute <id>` (Nextcloud 34, 28 de septiembre de 2026).
- **El bundle debe emitir una sola hoja de estilos.** La configuración por omisión de Vite la divide en un archivo mínimo que importa con `@import` un fragmento con hash en el nombre; el parámetro `?v=` de Nextcloud no alcanza ese `@import`, de modo que un archivo mínimo en caché sigue importando un fragmento que la compilación siguiente borró: estilos viejos o ninguno, sin aviso. `build.cssCodeSplit: false` lo evita.
- **El tema no se puede cambiar, y la plataforma no lo dice.** Con `enforce_theme=light`, `occ user:setting <usuario> theming enabled-themes '["dark"]'` termina bien y se lee de vuelta, pero no cambia nada: `ThemesService::getEnabledThemes()` antepone el tema forzado. Forzar `data-theme-dark` en el DOM cambia el área de contenido y no la navegación, lo que parece un tema oscuro roto.
- **`opcache.revalidate_freq` es de 60 s**, así que un cambio de PHP puede tardar un minuto en verse.
- **Agregar o cambiar rutas por atributos exige reiniciar el contenedor.** `CachingRouter` guarda las rutas compiladas durante una hora en APCu, que es propio de cada SAPI: limpiarlo desde `occ` no hace nada, porque la CLI y la web no lo comparten. El síntoma es `998 Invalid query` desde OCS mientras `occ` lista la ruta.
- **No encadenar `docker exec … | grep -q`.** `grep` cierra la tubería en la primera coincidencia, el que escribe muere por SIGPIPE y, con `pipefail`, una verificación que pasa se informa como falla.
- **Subir `<version>` en `appinfo/info.xml` deja toda la instancia en «requiere actualización»:** `occ` pasa a modo limitado y las rutas web dejan de responder hasta que corre `occ upgrade`.

### Pruebas y verificación manual

- `scripts/test.sh` ejecuta la batería unitaria dentro del contenedor (PHPUnit 11); `npm test`, la lógica del frontend (Vitest); `scripts/smoke.sh`, el cableado contra la instancia en marcha; `scripts/layout.sh`, la disposición en un navegador real a tres anchos; `scripts/openapi.sh`, la regeneración de `openapi.json`.
- La integración continua (`.github/workflows/ci.yml`) corre sobre `main` y los pull requests, no en cada push: la batería unitaria en la misma imagen `nextcloud:34` que usa la instancia, más un trabajo de bundle que ejecuta `npm test`, recompila `src/` y exige que `js/` y `css/` no cambien.
- `scripts/layout.sh` maneja un Chromium sin interfaz a **360, 768 y 1366 px**, tras ejecutar una vez `npm install && npx playwright install chromium`. Los 360 px solo se alcanzan así: la ventana de un navegador real en una máquina de desarrollo no se estrecha tanto.
- **Sin una instancia**, `scripts/layout.mjs` aún ejecuta las verificaciones 6, 10, 11 y 12 contra el bundle compilado: servir, en 127.0.0.1, una página en `/apps/epidemiologia/` con un `#initial-state-epidemiologia-sources` sintético (JSON en base64 que incluya una fuente ausente, una degradada sin nada, una que respondió sin nada y una degradada con última copia) y un `#epidemiologia` de montaje junto a los `js/` y `css/` compilados, y ejecutar `EPI_TOKEN=x node scripts/layout.mjs http://127.0.0.1:<puerto> admin`. La verificación 7 y el ancho del informe a 360 px necesitan el CSS propio de Nextcloud, así que se juzgan solo en una instancia.
- **`smoke.sh` y `layout.sh` quedan manuales a propósito:** sus aserciones necesitan una instancia aprovisionada con la aplicación habilitada, y su valor es justamente correr contra una real. Ejecutar ambos antes de cada versión.
- Los fixtures son **respuestas reales capturadas** del MINSAL, el ISP y la OPS/OMS, de modo que los intérpretes se prueban contra lo que esos sitios publican de verdad, rarezas incluidas.
