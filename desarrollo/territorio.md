---
tipo: referencia
esqueleto: contratos
audiencia: desarrollo
apps: [territorio, gestion]
resumen: "Contratos de territorio: superficies OCS e inyección, ciclo de vida de registros, pares y lotes, cursor de revisiones, errores, fallos y deuda técnica."
---
# territorio

## Propósito y diseño

Territorio es la base de conocimiento territorial que un CESFAM mantiene sobre la población que atiende: qué subdivisiones oficiales existen, cómo el establecimiento las reparte entre sus equipos y qué hay físicamente en el territorio.
Es una aplicación de Nextcloud 34 de APS Conecta, con el código en el repositorio privado `territorio`; su vocabulario está en `CONTEXT.md` y sus decisiones en `docs/adr/`.
Una instalación sirve a una comuna y al territorio de un CESFAM dentro de ella; qué comuna es, es configuración y no código.
La aplicación no guarda información de pacientes, pero sí nombres, teléfonos y correos de dirigentes de juntas de vecinos, que son datos personales según la ley chilena.

El modelo tiene un solo tipo de registro con geometría (`Feature`), y su forma decide su clase: un `Point` es un lugar, un `LineString` una ruta y un `Polygon` una zona.
Los sectores y las unidades vecinales son registros de ese mismo tipo, archivados en la categoría «División territorial»: historial, retiro, cursor de cambios, listas y reversión de importaciones se aplican a ellos sin una segunda implementación.
La geometría se guarda como texto GeoJSON con su caja envolvente al lado, porque la base de datos no tiene PostGIS ni índice espacial.

| ADR | Decisión | Consecuencia en el código |
|---|---|---|
| 0001 | Aplicación propia y no una capa de la app Maps, que modela geografía personal. | La suite no instala `maps`. |
| 0002 | Colaboración por sondeo de un cursor de cambios cada cinco segundos, no por push. | Toda mutación de un registro avanza el cursor. |
| 0003 | Una edición local de un registro catastral prevalece sobre la reimportación. | El valor oficial entrante se guarda junto a la edición. |
| 0004 | OpenStreetMap aporta solo el mapa base y fuentes de importación fuera de línea. | La aplicación no consulta Overpass ni escribe en OpenStreetMap. |
| 0005 | Toda persona usuaria edita; el historial y el retiro reemplazan a los permisos. | No existe `DELETE` físico de un registro. |
| 0006, 0012 | Exportar datos de contacto exige confirmar la contraseña y se anota en `territorio_export`. | La exportación no toma revisión. |
| 0007 | El límite de un sector se construye eligiendo líneas reales y se ajusta a mano. | Dibujar a mano sigue siendo un camino completo. |
| 0008 | El sector y la unidad vecinal de un lugar se derivan de la geometría y se guardan. | No son campos editables. |
| 0009 | No hay función de respaldo; cada importación es un lote reversible. | La pérdida catastrófica corresponde al respaldo de PostgreSQL de la suite. |
| 0011 | Los registros parecidos se encolan para una persona y nunca se fusionan solos. | Una decisión se guarda y no se recalcula. |
| 0013, 0017 | El color agrupa categorías, el pictograma las identifica y la aplicación asigna el color. | `tools/ramp-check.py`, que corre en el lint del repositorio, verifica contraste y separación. |
| 0014, 0020 | Inyección para llamadas dentro de la instancia; tres rutas OCS de lectura como superficie publicada. | `tests/unit/RoutesTest.php` fija las tres rutas. |
| 0015 | Una división territorial se dibuja como división, no como categoría. | La unidad vecinal va con línea discontinua y sin relleno. |
| 0016 | Quitar una categoría se rechaza mientras tenga registros. | «División territorial» y «Sin clasificar · Otro» no se pueden quitar. |
| 0018 | La procedencia del límite de un sector se lee del historial. | No existe una columna de procedencia. |
| 0019 | El mapa base es un archivo PMTiles autoalojado. | {doc}`/administracion/mapas-base` describe el servicio. |

### En APS Conecta Gestión

APS Conecta Gestión instala Territorio desde un paquete construido con una etiqueta de versión del repositorio, como el resto de sus aplicaciones propias, sin red ni git en la instalación.
La fase 16 del aprovisionamiento escribe `comuna_cut` y `comuna_name` desde el archivo del establecimiento, y se detiene si falta el código CUT: un `comuna_cut` vacío se lee como «sin elegir» y desarma el rechazo de archivos de otra comuna.
La misma fase escribe `tile_url` con la dirección de la instancia seguida de `/tiles/chile.pmtiles`. Si no puede leer `overwrite.cli.url`, deja el valor anterior y lo anota en el registro. En la pila de desarrollo, que no corre bajo AIO, escribe el valor vacío y la aplicación vuelve a las teselas raster de OpenStreetMap.
Las unidades vecinales y los establecimientos DEIS de la comuna se importan desde un paquete que se recorta de los maestros nacionales fijados por suma de verificación en `provisioning/data/packages.json`.
{doc}`/administracion/aprovisionamiento` describe las fases.

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/territorio>
```

## Contratos de componentes y API

Territorio publica dos superficies de lectura sobre un mismo servicio, `OCA\Territorio\Service\RegistryService`.
Las escrituras quedan en las rutas propias de la aplicación, porque un cambio es un acto de una persona hecho desde las pantallas que muestran lo que cambia.

### Inyección

Una aplicación de la misma instancia inyecta `RegistryService` en su constructor: la llamada no serializa nada, participa en la transacción del llamador y no necesita autenticación.
Es la vía preferida para las llamadas transaccionales dentro de la instancia.

| Método | Devuelve |
|---|---|
| `counts()` | `total`, `unknownSubcategory`, `categories` (por slug: `label`, `total`, `subcategories`), `bySector` y `byUnidadVecinal` (por id del límite) |
| `find(int $id)` | Un registro visible, o `null` |
| `inSubcategory(string $category, string $subcategory)` | Los registros del par; `[]` si el par existe sin registros y `null` si el par no existe |

Las claves son slugs y no ids, porque los ids cambian entre instalaciones y los slugs son los que usan la semilla y las importaciones.
Las cuentas por sector y por unidad vecinal se indexan por el id del límite, porque dos sectores pueden compartir nombre.
Todo se lee mediante `FeatureMapper::findAll()`, el único lugar que decide qué muestra el registro: los registros retirados y los conjuntos de datos de líneas de límite quedan fuera.

### OCS

`ApiController` registra por atributo tres rutas `GET`, de solo lectura, abiertas a toda persona usuaria autenticada y limitadas a 60 lecturas por usuario cada 60 segundos.

| Ruta | 200 | 404 |
|---|---|---|
| `/ocs/v2.php/apps/territorio/api/v1/counts` | La forma de `counts()` | — |
| `/ocs/v2.php/apps/territorio/api/v1/features/{id}` | `id`, `name`, `kind`, `category`, `subcategory`, `address`, `geometry` | El registro no existe o está retirado |
| `/ocs/v2.php/apps/territorio/api/v1/subcategories/{category}/{subcategory}/features` | Lista sin paginar; `[]` si el par existe sin registros | El par no existe |

Cada solicitud lleva la cabecera `OCS-APIRequest: true` y se autentica con usuario y contraseña de aplicación o con un token bearer; sin sesión, la respuesta es 401.
La forma pública de un registro no lleva teléfono, correo ni persona de contacto.
`openapi.json` se genera con `scripts/openapi.sh` a partir de los atributos y docblocks del controlador, se versiona y no se edita a mano; el job `openapi` de CI falla si el archivo versionado difiere.
Un cambio de forma regenera la especificación, y su diff versionado es el cambio de contrato.
`tests/unit/RoutesTest.php` falla si se agrega otra ruta OCS o si aparece una sección `ocs` en `appinfo/routes.php`.

### Rutas de la aplicación

Una ruta sin `#[NoAdminRequired]` queda solo para la administración: así están `GET /export/history`, `PUT /settings/basemap` y `PUT /settings/comuna`.
Las demás rutas, escrituras incluidas, están abiertas a toda persona usuaria autenticada; solo la página `GET /` omite la verificación CSRF.
La exportación tiene dos rutas para una sola operación: `POST /export/contacts` lleva `#[PasswordConfirmationRequired(strict: true)]` y es la única que puede llevar datos de contacto, mientras que `POST /export` no puede llevarlos.
Las categorías y subcategorías se direccionan por slug, que es lo que un cambio de nombre conserva; el slug de una subcategoría es único solo dentro de su categoría.
La lista completa de rutas, ajustes y comandos `occ` es la referencia generada:

```{include} ../_generated/attach/territorio.md
```

## Transiciones de estado

### Registro

El historial registra cinco acciones: `created`, `updated`, `retired`, `restored` y `merged`.

| Estado | Evento | Estado siguiente | Efecto |
|---|---|---|---|
| — | crear | visible | Revisión `created` |
| visible | guardar | visible | Revisión `updated`; si cambió la geometría, se recalcula la asignación |
| visible | retirar | retirado | Sale del mapa y de toda lista por defecto; conserva su historial |
| retirado | restaurar | visible | Revisión `restored` |
| visible | fusionar, como perdedor | fusionado | Queda retirado y apunta al registro sobreviviente |
| fusionado | restaurar | visible | El par candidato se reabre |

Redibujar un sector reasigna cada lugar que cubre, y ese cambio queda en el historial como cualquier otro.
Retirar o restaurar dentro de una reversión pasa por `FeatureService` y no por el mapper, porque el servicio también reasigna lo que el límite cubría.

### Par candidato

Un par candidato está `pending`, `merged` o `dismissed`.
Un par `merged` vuelve a `pending` cuando se restaura el registro perdedor; un par `dismissed` no se vuelve a ofrecer.
El sobreviviente de una fusión lo nombra siempre una persona.
Un par con algún registro no visible sigue `pending`, pero sale de la cola hasta que ambos registros vuelven a estar visibles.
La búsqueda de pares corre al final de cada importación y recorre todo el registro, no solo lo importado.

### Lote de importación

Una importación sigue este orden:

1. Rechaza el archivo si declara otra comuna, antes de escribir nada.
2. Colapsa las filas que el archivo repite textualmente y anota cuántas fueron.
3. Valida el archivo completo contra la taxonomía: una fila inválida rechaza el archivo entero, y una fila con un tipo de geometría no admitido se omite y se cuenta.
4. Busca o crea el conjunto de datos: es la primera escritura.
5. Escribe el lote (`ImportBatch`) antes de la primera fila.
6. Aplica las filas, cada una en su propia transacción.
7. Guarda las cuentas del lote en un `finally`, también cuando la ejecución falla.
8. Busca pares candidatos cuando el lote ya está cerrado.

Revertir un lote crea un lote nuevo que apunta al revertido y aplica la inversa de cada acción, de la más nueva a la más antigua.
Ese lote nuevo también se puede revertir.
Revertir un lote ya deshecho se rechaza con «Ese lote ya está deshecho.».
Un registro modificado después del lote queda como está y se cuenta como intacto.

## Taxonomía de errores

| Código | Significado | Reintento | Remedio del cliente |
|---|---|---|---|
| 422 `{"message": …}` | Rechazo: la solicitud se entendió y no se guarda. Lo lanzan las subclases de `RefusedException`: `InvalidFeatureException`, `InvalidGeometryException`, `InvalidImportException`, `InvalidTaxonomyException` e `InvalidComunaException`. | La misma solicitud se rechaza otra vez. | Corregir lo que nombra el mensaje, que está en español. |
| 404 `{"message": …}` | Registro inexistente (`DoesNotExistException`) en las rutas de la aplicación. | No. | Volver a leer el estado. |
| 404 con `data` vacío en el sobre OCS | En OCS: registro inexistente o retirado, o par inexistente. | No. | Volver a leer el estado. |
| 500 con una frase en español | Falla del servidor (`ServerFaultException`), como un disco lleno o un directorio temporal sin escritura. | Sí, después de que se corrige el servidor. | Avisar a la administración. |
| 401 | Solicitud OCS sin sesión. | Sí, con credenciales. | Autenticar la solicitud. |

Una importación falla entera ante un archivo inválido: lo rechaza completo antes de escribir una sola fila.
Una reversión falla registro a registro: deja como está cada registro que no puede deshacer y lo cuenta.

## Concurrencia e invariantes

- **Cursor único.** Cada revisión sale de una sola fila de `territorio_cursor`, incrementada con un `UPDATE` que toma un bloqueo de fila hasta el commit de la transacción. Las escrituras hacen cola, y el orden de commit es el orden de emisión: ningún cliente que sondea guarda un cursor por encima de un cambio aún no visible.
- **Toda mutación de un registro avanza el cursor.** La excepción está registrada: crear, renombrar o quitar categorías y subcategorías, y los ajustes, no lo avanzan, porque el contador cuelga de un id de registro.
- **Sondeo.** Cada mapa abierto consulta `GET /changes` cada cinco segundos y se detiene con la pestaña oculta. Cuando nada cambió, la respuesta sale de una lectura por clave primaria.
- **Arranque.** La página lee el cursor antes que los registros: un cambio que cae entre ambas lecturas llega otra vez en el primer sondeo, y aplicarlo dos veces en el navegador es inocuo.
- **Lotes por id.** Una reversión lee las revisiones de su lote por `import_id`, nunca por un rango, porque un rango arrastraría lo que otra persona guardó durante la importación.
- **Idempotencia.** La importación empareja por conjunto de datos e id externo; reimportar un archivo sin cambios no genera revisiones.
- **Edición local.** Una importación no sobrescribe un registro que una persona editó: el valor oficial se guarda aparte y sin tomar revisión.
- **Exportaciones.** Exportar no toma revisión ni despierta a los clientes que sondean.
- **Pares.** Si dos personas resuelven el mismo par, la segunda decisión se rechaza.
- **Historial.** No hay `DELETE` físico de un registro, y el historial solo crece: nunca se edita para corregir un error.

## Dominios de fallo

- **Mapa base.** Si el mapa base no carga, el mapa sigue usable con todos los registros y sus formas, y muestra un aviso. El archivo PMTiles se verifica una vez leyendo sus primeros siete bytes, porque `protomaps-leaflet` no informa errores de tesela.
- **`tile_url` rechazado.** Un valor que no es ni archivo PMTiles ni plantilla `{z}/{x}/{y}` se guarda pero no se sirve: el mapa vuelve a las teselas de OpenStreetMap y la página de ajustes lo indica.
- **Sin líneas de límite.** Sin el conjunto de calles, canales y vías importado, la búsqueda de calles queda vacía y no se puede generar un polígono; dibujar un sector a mano sigue funcionando.
- **Cambio de versión.** Subir la versión en `appinfo/info.xml` deja toda la instancia en «requiere actualización», con 503 en todas las páginas y no solo en esta aplicación, hasta que corre `occ upgrade`.
- **APCu.** La caché local es por proceso: un ajuste escrito con `occ config:app:set` no llega al proceso web hasta su reinicio. Un ajuste guardado desde la interfaz no tiene ese retraso.
- **Importación interrumpida.** Si una importación falla después de empezar a escribir, las filas ya escritas quedan; el lote existe desde antes y las revierte.
- **Pérdida catastrófica.** Un disco perdido o tablas borradas corresponden al respaldo de PostgreSQL de la suite, no a la aplicación.
- **Sin push.** La instancia corre `nextcloud:34-apache`, donde cada conexión abierta ocupa un worker de PHP; por eso no hay SSE ni WebSocket, y la frescura queda acotada por el intervalo de sondeo.

## Deuda técnica y límites

- **Sin paginación.** `FeatureMapper::findAll()` y `findChangedSince()` devuelven el conjunto entero: un cliente que estuvo ausente mucho tiempo recibe la comuna completa en una respuesta.
- **Índice de caja envolvente parcial.** La tabla de registros indexa solo `min_lat` (`terr_feat_bbox_idx`). La consulta del editor de límites hace cuatro comparaciones de rango y el índice sirve solo la primera; las otras tres filtran lo que el índice devuelve.
- **Escrituras serializadas.** Todas las escrituras de la aplicación hacen cola detrás de una fila; si una importación masiva lo vuelve un cuello de botella, el camino previsto es reservar un bloque de revisiones por lote.
- **Lecturas completas.** `counts()` cuenta en PHP sobre todo el conjunto visible, y `find()` recorre ese conjunto para devolver una fila.
- **Reversión.** Deshacer cuesta dos consultas por entrada, unas mil idas y vueltas para un lote de 500 filas. La verificación de «modificado después» lee fuera de la transacción que escribe, y una escritura que cae en esos milisegundos no se ve.
- **Calles.** Los nombres de calles se leen sin caché, unas once mil filas por sesión, y el editor de límites recibe un tope fijo de líneas por vista, sin paginación.
- **Taxonomía y cursor.** Agregar una subcategoría no avisa a los navegadores ya abiertos: un registro archivado en ella aparece allí como «Clasificación desconocida» hasta recargar.
- **Coordenadas.** La validación solo revisa rangos: una coordenada chilena con latitud y longitud invertidas se acepta y cae en el Atlántico Sur.
- **Geometrías.** Solo se guardan `Point`, `LineString` y `Polygon`; una importación omite y cuenta las filas con otro tipo, como `MultiPolygon`.
- **GeoJSON sin ids.** En un archivo sin ids externos, una corrección de nombre o coordenada en el origen entra como un registro nuevo.
- **Paleta.** Con la paleta actual quedan ocho colores de reserva; agotados, una categoría nueva toma el color neutro y se distingue solo por su pictograma.
- **Dos registros de actividad.** Los cambios y las exportaciones viven en tablas distintas, y un informe de «todo lo ocurrido» tiene que leer ambas. Una exportación anota cuántos registros salieron y si llevaba contactos, no cuáles.
- **Historial sin límite.** El historial crece sin tope, por diseño.
- **Tamaño de importación.** Desde el navegador, un archivo admite hasta 8 MiB; `occ territorio:import` no tiene tope.
