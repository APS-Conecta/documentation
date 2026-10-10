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

Una clave que una fuente no tiene se omite, nunca es `null`. El contrato es `openapi.json`, que `scripts/openapi.sh` genera desde el controlador y nunca se edita a mano; gestion lo registra como estable en su [índice de contratos](https://github.com/APS-Conecta/gestion/blob/main/docs/CONTRACTS.md). Las rutas anteriores ya no existen: `/apps/epidemiologia/api/v1/…` desde la versión 0.2.0, y `/ocs/…/alerts` y `…/reports` desde la 0.3.0.

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

## Deuda técnica y límites

- **Los establecimientos reciben la versión 0.9.0.** gestion instala desde un tarball la versión fijada en su [`provisioning/apps/epidemiologia/VENDOR`](https://github.com/APS-Conecta/gestion/blob/main/provisioning/apps/epidemiologia/VENDOR) (hoy, 0.9.0) siempre que `apps/epidemiologia` no sea un clon de git, que es el caso de toda instalación AIO; la sube en un hito, no en cada etiqueta. Esa versión es anterior al traslado de las fuentes de la versión 0.10.0: lee Alertas vigentes y el informe en las direcciones que la 0.10.0 abandonó porque su host respondía 403 a toda red desde octubre de 2025, y los informes de ese publicador anterior no se trasladaron a ninguna parte. Esta página describe la versión 0.11.3, la de `main`.
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
