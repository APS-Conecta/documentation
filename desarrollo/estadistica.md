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

Un CESFAM recibe Estadística como aplicación opcional del asistente, desactivada por omisión: quien la elige recibe la publicación firmada más nueva compatible con su Nextcloud, del repositorio propio de la aplicación, sin contactar la tienda de aplicaciones, y el asistente escribe el establecimiento.
El paquete contiene solo código: las cifras REM no viajan en él y, después de instalar, `RemJob` descarga la ventana del DEIS.
La versión instalada queda registrada en el candado del servidor ({doc}`/administracion/aplicaciones`).

**Invariante: ningún identificador de persona entra en la aplicación.**
Todo lo que guarda es un conteo agregado que publican el DEIS, FONASA o el MINSAL.
La tabla REM guarda la serie, el año, el mes, el establecimiento de seis dígitos, el código de prestación y las columnas `col01`…`col50`; el servicio, la región y la comuna no se guardan.
El lector de la PIV de FONASA (`lib/Piv/PivReader.php`) tiene el encabezado bloqueado: el archivo trae exactamente las once columnas de FONASA, en cualquier orden, y cualquier otro conjunto se rechaza entero, sin guardar nada.
Ese bloqueo rechaza sobre todo un archivo que agrega un RUT o un nombre.
Las personas sin tramo de edad se cuentan y se informan al importar, pero no se guardan.

**Invariante: el establecimiento es configuración de la instancia** ([ADR-0009](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0009-the-establishment-is-instance-configuration.md)).
La aplicación lee tres claves de configuración y no tiene un método que las escriba.
En una instalación con el {doc}`asistente </administracion/instalar-gestion-aio>`, las escribe su paso «Establecimiento en Estadística» desde el centro elegido, aunque no se haya marcado Estadística, para que la encuentre quien la active después; si Nextcloud ya no las tiene, la comparación del final de la instalación vuelve a poner el paso en rojo y «Reintentar» las escribe de nuevo.
En una instalación de gestion, las escribe la [fase 16 de la provisión](https://github.com/APS-Conecta/gestion/blob/main/provisioning/phases/16-app-policy.sh), y `scripts/divergence.sh` de gestion las compara con el archivo del sitio.
Un `deis_code` que no tenga seis dígitos se lee como ausencia de establecimiento, y tanto el paso como la fase 16 se detienen antes de escribir un valor así.
Ninguna pantalla de la aplicación elige otro establecimiento como propio.

| Clave | Quién la escribe | Efecto |
|---|---|---|
| `deis_code` | El asistente, desde el código DEIS del centro; en gestion, la fase 16, desde `SITE_DEIS` | El establecimiento de la serie local. Sin ella, la aplicación muestra el país y los pares, sin serie local |
| `establishment_type` | El asistente, desde el tipo del centro en el registro DEIS; en gestion, la fase 16, desde `SITE_TIPO` | Su tipo, que muestra la sección de administración |
| `comuna_cut` | El asistente, desde la comuna del centro; en gestion, la fase 16, desde `SITE_COMUNA_CUT` | El CUT de cinco dígitos de su comuna |
| `first_year` | La sección de administración, «Años de historia nacional» | El primer año de historia nacional que se guarda; por defecto, el año en curso menos 3. Subirlo estrecha la ventana y borra los años que quedan fuera |
| `planilla_owner`, `planilla_folder` | La sección de administración, «Planillas del establecimiento» | Quién eligió la carpeta de planillas, y el id de esa carpeta. El trabajo la lee como esa persona |

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
| 0007 | La Población Inscrita Validada (PIV) de FONASA se sube a mano, se guarda por corte y da el denominador solo a rangos de tramos de edad enteros |
| 0008 | Las Metas Sanitarias son un archivo semilla por año, leído mes a mes |

## Contratos de componentes y API

La API es OCS, bajo `/ocs/v2.php/apps/estadistica/api/v1/`, y cada llamada envía la cabecera `OCS-APIRequest: true`, que también es la protección CSRF ({doc}`/desarrollo/plataforma/client-apis/ocs/ocs-api-overview`).
Todas las rutas son `#[NoAdminRequired]`: cualquier cuenta lee todo lo publicado y cualquier cuenta guarda preguntas y tableros.
Cada ruta lleva un `#[UserRateLimit]` por persona: 120 lecturas y 20 escrituras por cada 60 s.
El contrato es `openapi.json`, que un script del repositorio genera desde el controlador y que nunca se edita a mano; la prueba de humo que corre CI falla si el archivo generado difiere del guardado, y su estabilidad es de diseño ([ADR-0006 del repositorio](https://github.com/APS-Conecta/estadistica/blob/main/docs/adr/0006-one-consulta-spec-compiled-to-bound-sql.md): la respuesta solo se extiende, nunca se reformula).

| Recurso | Verbos | Respuestas |
|---|---|---|
| `fuentes` | GET | 200: REM Serie A, REM Serie P, la Base de Establecimientos y la PIV, cada una con su origen, su fecha de corte, sus filas y su estado |
| `fuentes/{id}` | GET, con `anio` opcional | 200: la fuente y su catálogo · 400: un año fuera de 2009 al año en curso · 404 |
| `consultas` | POST | 200: las series, sus etiquetas y su fuente · 422 |
| `preguntas` | GET, POST | 200 · 201: la pregunta guardada · 422 |
| `preguntas/{id}` | GET, PUT, DELETE | 200 · 403 · 404 · 422 |
| `tableros` | GET, POST | 200 · 201: el tablero guardado · 422 |
| `tableros/{id}` | GET, PUT, DELETE | 200 · 403 · 404 · 422 |
| `indicadores` | GET, con `anio` y `pares` opcionales | 200: las metas del año, mes a mes, y en `fecha_corte_local` el último mes que el establecimiento informó en cada serie · 400 · 404: no hay metas para ese año · 422 |
| `resumen` | GET, con `establecimiento` opcional | 200: una tarjeta por meta de las metas más nuevas · 400: un código DEIS que no tiene seis dígitos · 404: no hay metas cargadas · 422 |

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

**Resumen.** `GET resumen` responde `{anio, nombre, referencia, establecimiento, metas}` con las metas de la semilla más nueva, para el establecimiento configurado o para el que nombra `establecimiento`; `referencia` es la de la semilla.
Cada tarjeta de `metas` trae `codigo`, `nombre`, `indicador`, `meta_nacional`, `meta_comprometida`, `manual`, `estado`, `mes`, `datos_al`, `numerador`, `denominador`, `porcentaje`, `cumple`, `historico`, `origen` y `fecha_corte`.
El año de la tarjeta es el más reciente con cifras REM, y nunca uno posterior al de las metas: las metas del año siguiente, cargadas en octubre, se cuentan sobre las cifras del año en curso.
`Resumen` (`lib/Goals/Resumen.php`) toma de `GoalEvaluator::history()` la respuesta para el establecimiento solo, sin serie nacional ni de pares, así que en el año de las metas `numerador`, `denominador` y `porcentaje` son los de la serie local de `GET indicadores` en el mismo `mes`: el último mes con porcentaje.
`datos_al` es el último mes que el establecimiento informó en la serie de la meta, el de su fuente en `fecha_corte_local` de `GET indicadores`; en una meta de Serie P puede ser anterior a `mes`, y es `null` en una meta manual o sin establecimiento.
`cumple` compara el porcentaje con la meta comprometida, o con la meta nacional si no hay una; en una meta manual, el porcentaje es su cumplimiento informado.
`estado` es `esperando ruta oficial` cuando una ruta de la meta tiene `oficial: false`, y entonces la tarjeta no trae cifra; es `falta el denominador oficial de <año>` cuando `poblacion.falta_oficial` lo marca; si no, es `null`.
`origen` y `fecha_corte` dicen de dónde sale el `mes` de la tarjeta: hoy `datos públicos DEIS` y el último mes (`AAAA-MM`) de la carga de ese año en la fuente del numerador; sin `mes` son `null`.
`historico` es una lista `{anio, estado, cierre, meses, ruta}` por año de la ventana, del más antiguo al de la tarjeta.
Cada año cuenta las metas más nuevas con todos sus periodos corridos en años enteros (`GoalSeed::shift()`), la ventana de octubre a septiembre de la Meta I incluida, en una sola instantánea de solo lectura para todos los años.
Cada mes de `meses` trae `mes`, `numerador`, `denominador`, `porcentaje`, `origen` y `fecha_corte`: en REM Serie A, la suma desde el inicio del periodo; en REM Serie P, solo los cortes de junio y diciembre, cada uno con su propio corte: cuando el establecimiento no informó ese corte, `numerador` (y `denominador`, si también es de Serie P) y `porcentaje` son `null`, nunca los del corte anterior.
`cierre` es el `porcentaje` de diciembre de un año ya terminado, y `null` en otro caso.
`estado` es `sin datos comparables`, sin meses, cuando el diccionario propio de ese año etiqueta algún código × columna de la ruta distinto que el del año de la tarjeta (se comparan hoja, sección, prestación y columna, sin distinguir mayúsculas, tildes ni plurales), cuando el año toma prestado el diccionario de otro, o cuando un periodo corrido empieza antes del primer año de la ventana.
Si no, es `falta el denominador oficial de <año>` cuando falta el denominador comprometido de ese año, o `null`.
`ruta` trae `numerador` y `denominador` de ese año, cada uno con `fuente`, `desde` y `hasta` (`AAAA-MM`, corridos a ese año), `sumar` y `restar`: una lista por consulta de la ruta, con cada código etiquetado para sus columnas por el diccionario de ese año, como lo etiqueta `POST consultas`.
Un denominador de la población inscrita de FONASA tiene `fuente` `piv`, `desde` y `hasta` en `null` y ningún código; el que solo da el compromiso es `null`.
Una meta manual, o una que espera su ruta oficial, trae `historico` vacío.
Para el establecimiento configurado, `GET resumen` sirve el Resumen guardado en `estadistica_resumen`, así que todos leen las mismas cifras hasta el siguiente cálculo; mientras no hay uno guardado, lo arma en la solicitud.
Para cualquier otro `establecimiento` lo arma en cada solicitud y no lo guarda.
La pestaña **Resumen** es la primera y lee solo esta ruta, y dibuja `historico` con el envoltorio de Chart.js de la app.
Cada cifra de una tarjeta y de su tabla abre el panel de su origen en `NcAppSidebar` (`src/components/ResumenFuente.vue`), un fragmento que se carga en el primer clic.

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
Cada ejecución lee primero la carpeta de planillas, y después hace a lo más una unidad de trabajo, la primera que aplica:

1. Olvidar un año que la ventana ya no guarda, el más antiguo primero.
2. Cargar una (año, serie) en cola, el año más nuevo primero: desde el archivo que dejó un administrador, si lo hay, y si no, desde el DEIS por rangos.
3. Revisar el DEIS, una vez al día.

Fuera de eso, la ejecución no toca la red.

`ResumenJob` es un `QueuedJob` que vuelve a calcular y guarda el Resumen del establecimiento configurado, con `Resumen::build`, el mismo cálculo de la solicitud.
Lo ponen en cola, en la misma transacción que su escritura, una carga REM (`RemImporter`), los compromisos de la sección de administración (`Goals::commit`: meta comprometida, denominador comprometido y cumplimiento informado), la población que la sección escribe para el establecimiento (`PivImporter::enter`), que gana a la de FONASA en su serie propia, y una semilla de metas, incluida o cargada a mano (`Goals::store`); nada más lo pone en cola.
Nextcloud guarda una sola copia en cola, así que los cambios que llegan antes de que corra se calculan una vez, y un cambio durante el cálculo pone en cola el siguiente.
La población que trae el archivo de FONASA entra en el Resumen en su siguiente cálculo.

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

**La carpeta de planillas** (ADR-0010). `PUT /admin/planillas` recibe la ruta de una carpeta dentro de los archivos propios de quien llama; es una escritura delegada, como las demás.
Cada ejecución de `RemJob` lista los archivos que están directamente en la carpeta, como quien la eligió.
Lee los nuevos y los cambiados, y todos otra vez cuando cambia el establecimiento configurado o un diccionario; olvida, con sus filas, los que ya no están.
El formulario REM es su diccionario sin la columna A del código: cada cifra se lee una columna a la izquierda de su marcador `COLnn`, en la misma fila, según la ubicación que `estadistica_code` guarda al leer el diccionario de ese año.
La hoja NOMBRE da el código del establecimiento (un dígito por celda, de C3 a H3), el mes (B6), el año (B7), la versión del formulario (A9) y la serie (B17).
Una planilla se rechaza entera, con su motivo, si su código no es el configurado, si su versión no es la del diccionario de ese año, o si no es un formulario REM del DEIS.
Una fila se guarda solo si alguna de sus cifras no es 0, como las publica el DEIS: los totales del formulario son fórmulas y una fila sin llenar trae ceros.
Las cifras leídas se guardan en `estadistica_planilla_rem`, aparte de las del DEIS y con su archivo, y todavía no entran en ninguna consulta.
Por cada serie y mes cuenta la planilla más reciente, por fecha de modificación y luego por id de archivo; las demás se muestran como reemplazadas.

**La semilla de metas.** `EnsureSeedData` corre como paso de reparación en la instalación y después de cada migración.
Carga un archivo de `seeds/` cuando su año no tiene metas o tiene una versión anterior; un archivo que cargó un administrador con una versión igual o mayor se queda.
Un archivo reemplaza su año entero y los compromisos se mantienen, porque nombran su meta por código.
El año de un archivo va de 2009 al año siguiente al actual, para que las metas de un año se carguen en octubre del anterior, cuando el MINSAL publica sus Orientaciones Técnicas.
Cada ruta REM, un `numerador` o un `denominador` con `fuente`, admite la clave `oficial`, `true` o `false`; sin ella, la ruta es oficial, así que una semilla anterior se lee igual.
Una ruta preparada antes de que las Orientaciones Técnicas del año la confirmen va con `oficial: false`.

**El corte de la PIV.** Un año de metas *t* lee el corte del 31-12-(*t* − 1); si no existe, el último corte anterior × 1,03; si tampoco, ninguno.
La PIV da el denominador de una meta solo cuando su rango de edad es una suma de tramos enteros; `80 a más años` cuenta como 80–89.
Un rango que corta un tramo no tiene denominador, ni local, ni nacional, ni de pares, hasta que se escribe el denominador comprometido del año, que vale solo para la serie local.
En `indicadores`, `poblacion.falta_oficial` marca esa meta.
Las cifras que un administrador escribe para el propio establecimiento ganan sobre las de FONASA celda por celda, solo en la serie local.

## Taxonomía de errores

Los 400 y 422, y el 403 de una pregunta o un tablero, llevan en `message` la frase en español que lee una persona; un 404 de la API OCS responde un cuerpo vacío.

| Código | Significado | Reintento | Remedio del cliente |
|---|---|---|---|
| 400 | La solicitud no se entiende: un `anio` fuera de rango en `fuentes/{id}` o en `indicadores`; en `indicadores`, un rasgo de `pares` que no existe, o, en `resumen`, un `establecimiento` que no tiene seis dígitos | No | Corregir el parámetro |
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
- **El Resumen, reemplazado entero.** `estadistica_resumen` guarda solo el Resumen del establecimiento configurado: cada cálculo borra antes cualquier otra fila, y sin establecimiento configurado las borra todas. La fila tiene el documento JSON y, a su lado, la huella (`sha256` del documento), la hora del cálculo y la frase del último cálculo fallido. Las mismas entradas dan el mismo documento, byte a byte. `ResumenJob` no admite ejecuciones paralelas, así que un cálculo más antiguo no se guarda después de uno más nuevo.
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
| La carpeta de planillas no se encuentra | Las planillas, que se olvidan, y la sección de administración lo dice | Las cifras del DEIS |
| Nextcloud no entrega un archivo de la carpeta de planillas (su almacenamiento no responde, o falla su cifrado) | Ese archivo, que dice «No se pudo leer el archivo de Nextcloud» y se vuelve a intentar cada hora; el detalle queda en el registro del servidor | Los demás archivos de la carpeta |
| Falla la lectura de la carpeta de planillas | Las planillas de esa ejecución de `RemJob`; el detalle queda en el registro del servidor | La unidad de trabajo del DEIS de esa misma ejecución |
| Falla el cálculo del Resumen | Su actualización: la sección de administración, en «Metas Sanitarias», dice por qué en español, o que hubo un error interno cuyo detalle queda en el registro del servidor | El Resumen guardado anterior, hasta el siguiente cálculo que termina bien |
| Falla una semilla de metas incluida | Las metas de ese año | Las demás semillas, y la activación de la aplicación |
| La consulta de una tarjeta se rechaza | Esa tarjeta, que muestra su propio mensaje | Las demás tarjetas del tablero |
| No hay establecimiento configurado | La serie local, los pares «como el propio», la población escrita a mano y los compromisos | El país y los pares elegidos por valor |

Las cifras, el estado de carga, las etiquetas, el registro de establecimientos, las preguntas, los tableros, la población, las metas y el Resumen guardado viven en la base de datos PostgreSQL de la instancia, y las filas REM viajan en el respaldo completo de esa base; un zip REM dejado espera su carga en el almacenamiento de la aplicación (`IAppData`).

## Deuda técnica y límites

- **Validación pendiente.** La persona responsable compara las Metas I a VII de junio de 2026 con el cálculo de la unidad de Estadística-REM antes de anunciar la aplicación al personal.
- **Preguntas abiertas de la semilla 2026.** Los pesos son los de 2025, porque las Orientaciones Técnicas 2026 no repiten ninguno; el denominador de la Meta II cuenta solo mujeres, mientras su numerador también cuenta a las personas transmasculinas de col02; el numerador de la Meta VI se cuenta en 2026, donde el texto dice 2025.
- **Fecha de corte (B-030).** La serie local de una meta de Serie A termina en el último mes con una cifra escrita del propio establecimiento. La fecha de corte de la fuente, que acota las columnas Nacional y Pares, es el mes más alto de cualquier fila: en el extracto 2026, un solo establecimiento informó septiembre.
- **Etiquetas prestadas (B-031).** Un año toma etiquetas solo de un diccionario posterior; el diccionario 2026 dejó fuera dos códigos que 2023–2025 sí etiquetan, y quedan «sin descripción».
- **Consultas nacionales pesadas (B-032).** Una consulta nacional sobre toda la ventana que suma una hoja entera se cancela a los 10 s con sus 50 columnas. Los únicos índices son la clave primaria y `(estab, anio)`, sobre 27,3 millones de filas.
- **Incompleto a comienzo de año (B-020).** El año en curso puede marcarse «incompleto» temprano en el año, porque `Completeness` compara cada servicio con el año completo más cercano, entero.
- **Deuda de la plantilla (B-015 a B-019).** Pasar `@nextcloud/webpack-vue-config` a su versión 7, los 404 de `.htaccess`, un `composer.phar` sin versión fija ni verificación, la prueba de navegador fuera de CI y el valor por defecto de `APS` en un worktree se corrigen primero en farmacia y luego aquí: el clon no sigue a la plantilla por sí solo.
- **Pruebas fuera de CI.** Ningún trabajo de CI corre la suite de integración contra PostgreSQL ni la prueba de navegador.
- **Interfaz (B-012, B-013).** En un teléfono, la grilla de población escrita a mano es más ancha que su sección. Cada pestaña carga su código la primera vez que se abre, así que el paquete principal pesa 329.277 bytes frente a un presupuesto de 720.000; cada bloque `<style>` todavía lleva su archivo `.vue` entero, en base64, dentro de su paquete.
- **Techo de carga.** La carga corre a unos 32.000 filas por segundo dentro de OCP; `COPY` por una segunda conexión lo subiría, y fue rechazado.
- **Tamaño.** La ventana por defecto de cuatro años ocupa unos 4,9 GB de base de datos, y lo mismo en cada respaldo. Un respaldo de gestion que omita las filas REM, que la aplicación puede volver a descargar, queda pendiente de medir el tiempo del volcado.
- **Filtro por hoja.** Un filtro por hoja es la unión de sus códigos en los diccionarios del periodo, no año por año.
- **Costo por solicitud.** A lo más tres sentencias de 10 s cada una, y a lo más 5.000 grupos por serie.
- **Relectura diaria.** Un miembro que falla por su contenido se vuelve a descargar cada día hasta que el DEIS lo corrija.
- **PIV.** Cada corte nuevo es un paso manual, una vez al año. Los filtros por sexo ven solo Mujeres y Hombres. Los códigos administrativos de comuna del archivo de FONASA cuentan en el total nacional y en ningún grupo de pares.
- **Riesgos de entrada.** El tope de 256 MiB del lector XLSX se suma de los tamaños que el zip declara de sí mismo, así que un zip que declara de menos es el borde que falta probar; en el CSV de FONASA quedan los prefijos de fórmula y la codificación.
- **Navegación.** Un tablero no se puede enlazar, porque recargar la página vuelve al **Resumen**; una pregunta no se puede reabrir en los cuatro pasos para cambiar lo que consulta.
- **No previsto.** Un selector de establecimiento, COMGES, llenar o validar la planilla REM, y las series BS, BM y D.
