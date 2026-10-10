---
tipo: referencia
esqueleto: contratos
audiencia: desarrollo
apps: [estadistica]
resumen: "Contratos de estadistica: API OCS y especificación de consulta, carga REM por año y serie, invariantes, dominios de fallo y deuda técnica."
---
# estadistica

## Propósito y diseño

Estadística es una aplicación propia de APS Conecta Gestión, para la versión 34 de la plataforma.
Guarda las cifras REM que el DEIS publica para todos los establecimientos del país, etiquetadas con el diccionario de cada año, para que un centro ponga sus cifras al lado de las nacionales y de las de establecimientos parecidos.
También sigue mes a mes las Metas Sanitarias de Atención Primaria.
La versión 0.1.0 cierra el hito M1, el pilar REM.
La guía de uso está en {doc}`/usuario/estadistica`.

Un CESFAM recibe Estadística por gestion, no por la tienda de aplicaciones: la fase 12 desempaqueta el paquete fijado en `provisioning/apps/estadistica/`, construido desde una etiqueta del repositorio, y la fase 16 escribe el establecimiento.
El paquete fijado es la versión 0.1.0 y contiene solo código: las cifras REM no viajan en él, y después de instalar, `RemJob` descarga la ventana del DEIS.
gestion la instala en el conjunto `OWN_APPS` ({doc}`/administracion/aplicaciones`).

**Invariante: ningún identificador de persona entra en la aplicación.**
Todo lo que guarda es un conteo agregado que publican el DEIS, FONASA o el MINSAL.
La tabla REM guarda la serie, el año, el mes, el establecimiento de seis dígitos, el código de prestación y las columnas `col01`…`col50`; el servicio, la región y la comuna no se guardan.
El lector de la PIV de FONASA (`lib/Piv/PivReader.php`) tiene el encabezado bloqueado: el archivo trae exactamente las once columnas de FONASA, en cualquier orden, y cualquier otro conjunto se rechaza entero, sin guardar nada.
Ese bloqueo rechaza sobre todo un archivo que agrega un RUT o un nombre.
Las personas sin tramo de edad se cuentan y se informan al importar, pero no se guardan.

**Invariante: el establecimiento es configuración de la instancia** ([gestion ADR-0013](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0013-the-establishment-is-instance-configuration.md)).
La aplicación lee tres claves de configuración y no tiene un método que las escriba: el único escritor es la [fase 16 de gestion](https://github.com/APS-Conecta/gestion/blob/main/provisioning/phases/16-app-policy.sh), y `scripts/divergence.sh` de gestion las compara con el archivo del sitio.
Un `deis_code` que no tenga seis dígitos se lee como ausencia de establecimiento, y la fase 16 se detiene antes de escribir un valor así.
Ninguna pantalla de la aplicación elige otro establecimiento como propio.

| Clave | Quién la escribe | Efecto |
|---|---|---|
| `deis_code` | Fase 16, desde `SITE_DEIS` | El establecimiento de la serie local. Sin ella, la aplicación muestra el país y los pares, sin serie local |
| `establishment_type` | Fase 16, desde `SITE_TIPO` | Su tipo, que muestra la sección de administración |
| `comuna_cut` | Fase 16, desde `SITE_COMUNA_CUT` | El CUT de cinco dígitos de su comuna |
| `first_year` | La sección de administración, «Años de historia nacional» | El primer año de historia nacional que se guarda; por defecto, el año en curso menos 3. Subirlo estrecha la ventana y borra los años que quedan fuera |

Las claves `deis_checked_at`, `deis_etags`, `deis_check_errors` y `deis_register` son estado del trabajo en segundo plano, no ajustes.

La sección **Estadística** de las configuraciones de administración implementa `IDelegatedSettings`: un administrador la delega a cualquier grupo ({doc}`/administracion/servidor/admin-delegation-configuration`).
El aprovisionamiento de gestion crea el grupo «Encargado/a de Estadística (REM)»; la delegación de la sección la otorga un administrador.

Las decisiones están en los ADR del repositorio, en `docs/adr/`:

| ADR | Decisión |
|---|---|
| 0001 | La aplicación se clona de la plantilla farmacia: se copia su arnés y se reescriben el esquema, los controladores y la aplicación Vue |
| 0002 | Solo PostgreSQL, declarado en `appinfo/info.xml` con `<database min-version="18">pgsql</database>`: una instalación sobre otro motor se rechaza al activar la aplicación |
| 0003 | Cada escritura de administración declara su delegación con `#[AuthorizedAdminSetting(settings: AdminSettings::class)]`, y nada más decide quién la llama |
| 0004 | REM es una tabla tipada sobre una ventana de años, cargada entera por (año, serie) |
| 0005 | La aplicación consulta al DEIS en tiempo de ejecución, por rangos HTTP, una vez al día |
| 0006 | Una sola especificación de consulta, compilada a SQL con parámetros y ejecutada en solo lectura |
| 0007 | La Población Inscrita Validada (PIV) de FONASA se sube a mano, se guarda por corte y se prorratea |
| 0008 | Las Metas Sanitarias son un archivo semilla por año, leído mes a mes |

## Contratos de componentes y API

La API es OCS, bajo `/ocs/v2.php/apps/estadistica/api/v1/`, y cada llamada envía la cabecera `OCS-APIRequest: true`, que también es la protección CSRF ({doc}`/desarrollo/plataforma/client-apis/ocs/ocs-api-overview`).
Todas las rutas son `#[NoAdminRequired]`: cualquier cuenta lee todo lo publicado y cualquier cuenta guarda preguntas y tableros.
Cada ruta lleva un `#[UserRateLimit]` por persona: 120 lecturas y 20 escrituras por cada 60 s.
El contrato es `openapi.json`, que un script del repositorio genera desde el controlador y que nunca se edita a mano; la prueba de humo que corre CI falla si el archivo generado difiere del guardado.
El [`docs/CONTRACTS.md` de gestion](https://github.com/APS-Conecta/gestion/blob/main/docs/CONTRACTS.md) lo registra junto a los contratos de las demás aplicaciones.

| Recurso | Verbos | Respuestas |
|---|---|---|
| `fuentes` | GET | 200: REM Serie A, REM Serie P, la Base de Establecimientos y la PIV, cada una con su origen, su fecha de corte, sus filas y su estado |
| `fuentes/{id}` | GET, con `anio` opcional | 200: la fuente y su catálogo · 400: un año fuera de 2009 al año en curso · 404 |
| `consultas` | POST | 200: las series, sus etiquetas y su fuente · 422 |
| `preguntas` | GET, POST | 200 · 201: la pregunta guardada · 422 |
| `preguntas/{id}` | GET, PUT, DELETE | 200 · 403 · 404 · 422 |
| `tableros` | GET, POST | 200 · 201: el tablero guardado · 422 |
| `tableros/{id}` | GET, PUT, DELETE | 200 · 403 · 404 · 422 |
| `indicadores` | GET, con `anio` y `pares` opcionales | 200: las metas del año, mes a mes · 400 · 404: no hay metas para ese año · 422 |

**La especificación de consulta.** `POST consultas` recibe `{consulta, establecimiento?}`.
Una consulta es un documento JSON con claves en español, y `QuerySpec::from()` es su único lector.
Rechaza en español, con un 422 y antes de que exista SQL, toda clave, columna, dimensión o métrica que no conoce.

| Clave | Contenido |
|---|---|
| `fuente` | `rem-a` o `rem-p` |
| `periodo` | `{desde, hasta}`, cada uno como `AAAA-MM`. Obligatorio; puede cruzar un año, y el año va de 2009 al año en curso |
| `filtros` | `hoja`, `seccion`, `codigos` y `columnas`. Nombran lo que se suma (una hoja o códigos) y las columnas, de `col01` a `col50`; hasta 1000 códigos |
| `agrupar` | Hasta dos de `anio`, `mes`, `codigo`, `columna`, `tipo`, `dependencia`, `nivel`, `servicio`, `region` y `comuna` |
| `metrica` | `suma` o `promedio_establecimiento`, que es la suma dividida por los establecimientos que informaron. Una consulta sin `metrica` se lee como `suma` |
| `comparar` | `{nacional, pares}`: agrega la serie nacional y la de un grupo de pares. Cada rasgo de `pares` es un valor de la Base de Establecimientos, o `true` para el valor del propio establecimiento |

`establecimiento` es el código DEIS de seis dígitos de la serie local; sin él, la serie local es el `deis_code` configurado.
Las páginas de la aplicación nunca lo envían.

La respuesta es `{series: {local, nacional, pares}, etiquetas: {local, pares, codigos}, fuente}`.
Cada serie es una lista de `{grupo, valor, informantes}`, y `grupo` trae los valores del grupo en el orden de `agrupar`.
Este contrato solo se extiende y nunca cambia de forma: una clave solo se agrega, nunca se renombra, y una clave desconocida sigue siendo un 422.
Así, una especificación válida nunca cambia de significado.

**Preguntas y tableros.**
`POST preguntas` guarda la consulta solo si `QuerySpec::from()` la acepta, y la guarda tal como llegó, no en su forma normalizada.
Cada vez que una tarjeta o una pregunta abierta se consulta, la consulta guardada se juzga de nuevo en `POST consultas`.
El tipo de gráfico (`tipo`: `barra`, `linea` o `tabla`) se guarda al lado de la consulta, no dentro de ella.
Un título tiene hasta 200 caracteres; un tablero, hasta 24 tarjetas, cada una de 1 a 3 columnas de ancho.

**Indicadores.** Cada término de la ruta de una meta es una consulta que `QuerySpec::from()` juzga al leer la semilla.
`GoalEvaluator` consulta todos los términos del año en el servidor, con las mismas sentencias que compila una consulta, en una sola instantánea de solo lectura.
La vista de metas lee `GET indicadores` y no envía consultas propias.

**Rutas internas.** Las acciones de la sección de administración están en la {doc}`referencia generada </_generated/referencia/estadistica>`.
Cada una lleva `#[AuthorizedAdminSetting(settings: AdminSettings::class)]` y responde un rechazo como un 422 con `{message}`.
La protección CSRF sigue activa en ellas: la sección envía el token, y un cliente de API envía `OCS-APIRequest: true` en su lugar.

```{include} ../_generated/attach/estadistica.md
```

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/estadistica>
```

## Transiciones de estado

El único trabajo programado es `RemJob`, un `TimedJob` declarado en `appinfo/info.xml`: nada corre en el planificador del host ({doc}`/desarrollo/plataforma/basics/backgroundjobs`).
Corre cada hora, como `TIME_SENSITIVE`, sin ejecuciones paralelas.
Cada ejecución hace a lo más una unidad de trabajo, la primera que aplica:

1. Olvidar un año que la ventana ya no guarda, el más antiguo primero.
2. Cargar una (año, serie) en cola, el año más nuevo primero: desde el archivo que dejó un administrador, si lo hay, y si no, desde el DEIS por rangos.
3. Revisar el DEIS, una vez al día.

Fuera de eso, la ejecución no toca la red.

Cada (año, serie) tiene una fila de estado (`IngestState`) con dos mitades: la carga cambia solo cuando se cargan filas, en la misma transacción, y el intento se escribe en cada prueba.

| Estado | Cómo se reconoce en la fila | Evento | Efecto |
|---|---|---|---|
| En cola | `pending` verdadero | Un archivo aceptado, o la revisión diaria que encuentra un CRC-32 o un tamaño distintos | Las ejecuciones siguientes lo cargan, el año más nuevo primero |
| En curso | `lastError` con la frase «La carga empezó y no ha terminado…» | El intento empieza y consume `pending` | Si sigue así pasados 15 minutos, el proceso se interrumpió |
| Cargado | `detail` y `lastError` nulos | El miembro se lee sin faltas | Las filas y el estado se confirman en una transacción |
| Incompleto | `detail` con las frases de lo que falta | `Completeness` encuentra faltas y no hay una copia completa guardada | Se carga y se muestra con su motivo |
| Carga anterior mantenida | `lastError` con «Se mantiene la carga anterior, que estaba completa…» | Llega un miembro incompleto sobre una carga completa | Se revierte; el CRC y el tamaño quedan registrados, así que los mismos bytes no se vuelven a leer |
| Fallido | `lastError` con la frase del rechazo, o con la de error interno | Un rechazo del archivo, o un error propio | Se revierte, y la carga anterior sigue sirviendo |
| Olvidado | La fila ya no existe | El año quedó fuera de la ventana | La ETag y el archivo dejado se borran primero; las filas, el estado y las etiquetas, al final y en una transacción |

`Completeness` marca un miembro como incompleto por cuatro causas: una última fila cortada, filas ilegibles, filas de otro año, o un servicio de salud cuyos establecimientos informantes cayeron bajo el 75 % del año completo más cercano.

**La revisión diaria.** Cuando no hay nada en cola y pasó un día, envía un HEAD condicional por cada año de la ventana.
Por cada año que cambió, lee el directorio central del zip y pone en cola cada miembro de Serie A o P cuyo CRC-32 o tamaño difiere del último juzgado.
La ETag de un año se guarda solo cuando no queda nada de ese año en cola.
Un 404 es silencioso solo para el año en curso, que el DEIS puede no haber publicado todavía.
La misma pasada revisa con un HEAD condicional la Base de Establecimientos más nueva y, si el archivo cambió, lo lee entero y reemplaza el registro en una transacción.

**La puerta de archivos.** `POST /admin/drop` recibe una ruta dentro de los archivos propios de quien llama y decide el tipo por los primeros bytes:

| El archivo | Se trata como | Cuándo se carga |
|---|---|---|
| Abre con «{» | Un archivo de Metas Sanitarias | En la misma solicitud |
| No es un zip | El CSV «Inscritos APS» de FONASA | En la misma solicitud |
| Zip sin Serie A ni P | La Base de Establecimientos del DEIS | En la misma solicitud |
| Zip con Serie A o P | Un zip REM del DEIS, guardado como `drops/<año>.zip` | En segundo plano, una serie por hora |

El año de un zip REM sale de sus filas, no del nombre del archivo, y tiene que estar dentro de la ventana.
Sus series se ponen en cola solo después de guardar el archivo, todas en una sentencia.
El archivo se conserva mientras una serie de su año falló por un error propio, para que el siguiente intento lo use en lugar de la copia del DEIS.

**La semilla de metas.** `EnsureSeedData` corre como paso de reparación en la instalación y después de cada migración.
Carga un archivo de `seeds/` cuando su año no tiene metas o tiene una versión anterior; un archivo que cargó un administrador con una versión igual o mayor se queda.
Un archivo reemplaza su año entero y los compromisos se mantienen, porque nombran su meta por código.
El año de un archivo va de 2009 al año siguiente al actual, para que las metas de un año se carguen en octubre del anterior, cuando el MINSAL publica sus Orientaciones Técnicas.

**El corte de la PIV.** Un año de metas *t* lee el corte del 31-12-(*t* − 1); si no existe, el último corte anterior × 1,03; si tampoco, ninguno.
Un tramo de edad cuenta su población por los años que comparte con el rango de la meta, dividida por 10, y `80 a más años` cuenta como 80–89.
Las cifras que un administrador escribe para el propio establecimiento ganan sobre las de FONASA celda por celda, solo en la serie local.

## Taxonomía de errores

Los 400 y 422, y el 403 de una pregunta o un tablero, llevan en `message` la frase en español que lee una persona; un 404 de la API OCS responde un cuerpo vacío.

| Código | Significado | Reintento | Remedio del cliente |
|---|---|---|---|
| 400 | La solicitud no se entiende: un `anio` fuera de rango en `fuentes/{id}` o en `indicadores`, o, en `indicadores`, un rasgo de `pares` que no existe | No | Corregir el parámetro |
| 403 | Cambiar una pregunta o un tablero ajenos sin administrar Estadística, o guardar sin sesión; en las rutas internas, quien no es administrador ni miembro de un grupo delegado | No | Pedir el cambio a quien la creó o a quien administra Estadística; iniciar sesión |
| 404 | No existe ese id, o no hay metas cargadas para ese año | No | Ninguno |
| 422 | Entendido y rechazado (`RefusedException`): una especificación inválida, un título o tarjetas fuera de regla, una semilla o un compromiso inválidos, o una consulta cancelada al pasar los 10 s | Solo después de acotar la consulta | Mostrar el mensaje; acotar el periodo, las prestaciones o la comparación |

Los resultados de una carga no son códigos HTTP: quedan en la fila de su (año, serie).
Un error interno deja en la fila la frase «La carga falló por un error interno; el detalle quedó en el registro del servidor».
Una revisión del DEIS que falla aparece en la sección de administración bajo «Cifras REM cargadas», con su frase en español.

## Concurrencia e invariantes

- **Un trabajo, una unidad por ejecución.** `RemJob` no admite ejecuciones paralelas: dos a la vez cargarían la misma (año, serie) dos veces.
- **Una transacción por (año, serie).** Un `DELETE` y luego `INSERT … SELECT FROM unnest(CAST(? AS …[]))` en lotes de 5.000 filas, con la fila de estado en la misma transacción. Mientras tanto, quien consulta sigue viendo las filas anteriores, hasta que la transacción se confirma.
- **El intento se anota antes del trabajo.** El inicio del intento consume `pending` en su propia sentencia, así que un archivo que vuelve a poner en cola la misma (año, serie) durante la carga sobrevive a ella.
- **Olvidar un año, las filas al final.** La ETag y el archivo dejado se borran antes que las filas, porque las filas son lo que hace que el año esté «fuera»: una ejecución que muere a medias lo encuentra otra vez y lo olvida entero.
- **Una instantánea por consulta.** Todas las series, las etiquetas y la fuente de una respuesta se leen en una transacción `REPEATABLE READ, READ ONLY`, con `statement_timeout` de 10 s fijado localmente por `set_config(…, true)`. Una escritura que llegara al ejecutor falla en PostgreSQL.
- **SQL solo con parámetros.** `QueryCompiler` escribe SQL desde su propio texto fijo y desde nombres de conjuntos cerrados (columnas, dimensiones, rasgos y las dos métricas); todo valor va como parámetro. Dos consultas que difieren solo en valores compilan a la misma sentencia.
- **Solo cuentan las celdas informadas.** Una celda vacía es NULL, nunca 0, así que un informante es un establecimiento con al menos una celda informada entre las columnas elegidas.
- **Moderación en un solo lugar.** `SavedContent` es el único lugar que cambia contenido guardado. Pregunta al núcleo si la persona es administradora o si tiene la sección delegada, y lo pregunta a lo más una vez por solicitud.
- **La delegación, probada.** `MetadataTest` falla un método de `AdminController` sin el atributo, y falla todo controlador que llame a `isAdmin(`.

## Dominios de fallo

| Falla | Qué deja de funcionar | Qué sigue funcionando |
|---|---|---|
| El DEIS no responde o un cortafuegos lo bloquea | La revisión diaria falla cada día, y lo dice la sección de administración | Las cifras cargadas, y la carga desde archivos dejados a mano |
| `'has_internet_connection' => false` | No se consulta el DEIS, y la sección de administración lo dice | La carga desde archivos dejados a mano |
| Falla la carga de un miembro | Esa (año, serie) no se actualiza | La última carga buena sigue sirviendo |
| Un diccionario o la Base de Establecimientos no se pueden leer | Las etiquetas o los pares de esa carga | Las cifras se cargan igual, y el diccionario o el registro anteriores siguen sirviendo |
| Falla una semilla de metas incluida | Las metas de ese año | Las demás semillas, y la activación de la aplicación |
| La consulta de una tarjeta se rechaza | Esa tarjeta, que muestra su propio mensaje | Las demás tarjetas del tablero |
| No hay establecimiento configurado | La serie local, los pares «como el propio», la población escrita a mano y los compromisos | El país y los pares elegidos por valor |

Las cifras, el estado de carga, las etiquetas, el registro de establecimientos, las preguntas, los tableros, la población y las metas viven en la base de datos PostgreSQL de la instancia, y las filas REM viajan en el respaldo completo de esa base; un zip REM dejado espera su carga en el almacenamiento de la aplicación (`IAppData`).

## Deuda técnica y límites

- **Validación pendiente.** La persona responsable compara las Metas I a VII de junio de 2026 con el cálculo de la unidad de Estadística-REM antes de anunciar la aplicación al personal.
- **Preguntas abiertas de la semilla 2026.** Los pesos son los de 2025, porque las Orientaciones Técnicas 2026 no repiten ninguno; el denominador de la Meta II cuenta solo mujeres, mientras su numerador también cuenta a las personas transmasculinas de col02; el numerador de la Meta VI se cuenta en 2026, donde el texto dice 2025.
- **Fecha de corte (B-030).** La fecha de corte es el mes más alto de cualquier fila: en el extracto 2026, un solo establecimiento informó septiembre, y cada meta de Serie A repite agosto en septiembre.
- **Etiquetas prestadas (B-031).** Un año toma etiquetas solo de un diccionario posterior; el diccionario 2026 dejó fuera dos códigos que 2023–2025 sí etiquetan, y quedan «sin descripción».
- **Consultas nacionales pesadas (B-032).** Una consulta nacional sobre toda la ventana que suma una hoja entera se cancela a los 10 s con sus 50 columnas. Los únicos índices son la clave primaria y `(estab, anio)`, sobre 27,3 millones de filas.
- **Incompleto a comienzo de año (B-020).** El año en curso puede marcarse «incompleto» temprano en el año, porque `Completeness` compara cada servicio con el año completo más cercano, entero.
- **Deuda de la plantilla (B-015 a B-019).** Pasar `@nextcloud/webpack-vue-config` a su versión 7, los 404 de `.htaccess`, un `composer.phar` sin versión fija ni verificación, la prueba de navegador fuera de CI y el valor por defecto de `APS` en un worktree se corrigen primero en farmacia y luego aquí: el clon no sigue a la plantilla por sí solo.
- **Pruebas fuera de CI.** Ningún trabajo de CI corre la suite de integración contra PostgreSQL ni la prueba de navegador.
- **Interfaz (B-012, B-013).** En un teléfono, la grilla de población escrita a mano es más ancha que su sección; el paquete principal pesa 711.997 bytes frente a un presupuesto de 720.000.
- **Techo de carga.** La carga corre a unos 32.000 filas por segundo dentro de OCP; `COPY` por una segunda conexión lo subiría, y fue rechazado.
- **Tamaño.** La ventana por defecto de cuatro años ocupa unos 4,9 GB de base de datos, y lo mismo en cada respaldo. Un respaldo de gestion que omita las filas REM, que la aplicación puede volver a descargar, queda pendiente de medir el tiempo del volcado.
- **Filtro por hoja.** Un filtro por hoja es la unión de sus códigos en los diccionarios del periodo, no año por año.
- **Costo por solicitud.** A lo más tres sentencias de 10 s cada una, y a lo más 5.000 grupos por serie.
- **Relectura diaria.** Un miembro que falla por su contenido se vuelve a descargar cada día hasta que el DEIS lo corrija.
- **PIV.** Cada corte nuevo es un paso manual, una vez al año. Los filtros por sexo ven solo Mujeres y Hombres. Los códigos administrativos de comuna del archivo de FONASA cuentan en el total nacional y en ningún grupo de pares.
- **Riesgos de entrada.** El tope de 256 MiB del lector XLSX se suma de los tamaños que el zip declara de sí mismo, así que un zip que declara de menos es el borde que falta probar; en el CSV de FONASA quedan los prefijos de fórmula y la codificación.
- **Navegación.** Un tablero no se puede enlazar, porque recargar la página vuelve a **Consultar**; una pregunta no se puede reabrir en los cuatro pasos para cambiar lo que consulta.
- **No previsto.** Un selector de establecimiento, COMGES, llenar o validar la planilla REM, y las series BS, BM y D.
