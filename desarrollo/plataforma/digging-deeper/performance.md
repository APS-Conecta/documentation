---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Rendimiento al desarrollar: cargador de clases, trabajos en segundo plano, consultas y transacciones en clústeres de bases de datos y datos en caché."
---
# Consideraciones de rendimiento

## Resumen

Esta página reúne consideraciones y consejos para mejorar el rendimiento: el cargador de clases y los trabajos en segundo plano en PHP, cómo reducir y supervisar las consultas a la base de datos, cómo escribir transacciones que escalen en clústeres, cómo medir el impacto de un cambio y los nombres mostrados en caché. Está dirigida a quienes desarrollan apps o el servidor.

````{upstream} developer_manual/digging_deeper/performance.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Este documento presenta algunas consideraciones y consejos habituales para mejorar el rendimiento de Nextcloud. La velocidad de Nextcloud es importante: a nadie le gusta esperar y, a menudo, lo que es *simplemente lento* con una pequeña cantidad de datos se vuelve *inutilizable* con una gran cantidad de datos. Tener presentes estos consejos al desarrollar para Nextcloud y plantearse revisar la app para hacerla más rápida.

:::{note}
Se agradecen los consejos: ¡más consejos e ideas sobre rendimiento son muy bienvenidos!
:::

### Rendimiento de PHP

- Cargador automático: plantearse usar un {nc-ref}`cargador de clases optimizado <app-custom-classloader>`. El código de la aplicación no tiene que cambiar para esta optimización.
- Trabajos en segundo plano pesados: plantearse marcar los {nc-ref}`trabajos en segundo plano <app-backgroundjobs>` como {nc-ref}`no sensibles al tiempo <app-backgroundjobs-time-sensitivity>` si pueden ejecutarse en horas de poca actividad con menor carga del sistema, p. ej., de noche.

### Rendimiento de la base de datos

La base de datos desempeña un papel importante en el rendimiento de Nextcloud. La regla general es: las consultas a la base de datos son muy malas y deben evitarse si es posible. Los motivos son:

- Viajes de ida y vuelta: en las instalaciones de Nextcloud más grandes, la base de datos no está instalada en el servidor de aplicaciones, sino en un servidor de base de datos remoto dedicado. El problema es que entonces las consultas a la base de datos pasan por la red. Estos viajes de ida y vuelta pueden acumularse de forma considerable si hay muchas consultas.
- Velocidad. Mucha gente cree que las bases de datos son rápidas. Esto no siempre es cierto si se compara con gestionar los datos internamente en PHP o en el sistema de archivos, o incluso con usar almacenamientos de clave/valor. Así que todo desarrollador debería comprobar siempre si la base de datos es realmente el mejor lugar para los datos.
- Escalabilidad. En una configuración grande de clúster de Nextcloud, normalmente hay varios servidores Nextcloud/web en paralelo, una base de datos central y un almacenamiento central. Esto significa que todo lo que ocurre en el lado de Nextcloud/PHP puede paralelizarse y escalarse. Lo que ocurre en la base de datos y en el almacenamiento es crítico, porque solo existe una vez y no puede escalarse con tanta facilidad.

Se puede reducir la carga de la base de datos:

1. Asegurándose de que cada consulta use un índice.
2. Reduciendo el número total de consultas.
3. Si se está familiarizado con la invalidación de caché, se puede intentar almacenar en caché los resultados de las consultas en PHP.

Hay varias formas de supervisar qué consultas se ejecutan realmente en la base de datos.

Con MySQL es muy fácil, con solo un poco de configuración:

1. Registro de consultas lentas.

Si se pone esto en el archivo my.cnf, toda consulta que tarde más de un segundo se registra en un archivo de registro:

```
slow_query_log = 1
slow_query_log_file = /var/log/mysql/mysql-slow.log
long_query_time=1
```

Si una consulta tarda más de un segundo, hay, por supuesto, un problema serio. Se puede observar con *tail -f /var/log/mysql/mysql-slow.log* mientras se usa Nextcloud.

2. Registrar todas las consultas.

Si se reduce long_query_time a cero, se registran todas las sentencias. Esto es muy útil para ver lo que está pasando. Basta con hacer un *tail -f* sobre el archivo de registro y hacer clic por la interfaz o acceder a la interfaz WebDAV:

```
slow_query_log = 1
slow_query_log_file = /var/log/mysql/mysql-slow.log
long_query_time=0
```

3. Registrar las consultas que no usan un índice.

Si se aumenta long_query_time a 100 y se agrega log-queries-not-using-indexes, se registran todas las consultas que no usan un índice. Toda consulta debería usar siempre un índice. Así que, idealmente, no debería haber ninguna salida:

```
log-queries-not-using-indexes
slow_query_log = 1
slow_query_log_file = /var/log/mysql/mysql-slow.log
long_query_time=100
```

#### Escribir transacciones escalables

Las consultas y transacciones de base de datos tienen que funcionar de forma eficiente sea cual sea el tamaño de las instalaciones de Nextcloud. Tienen que funcionar con un SQLite simple, con un Postgres de un solo nodo y con un clúster MariaDB Galera, por dar algunos ejemplos.

##### Clústeres de bases de datos

Las bases de datos de una sola instancia ofrecen una consistencia fuerte. Los clústeres también pueden ofrecerla, pero conlleva una penalización de rendimiento, y los administradores a veces optan por relajar estas garantías para aumentar la capacidad de procesamiento. Una de estas inconsistencias permitidas puede darse en los clústeres con división de lectura/escritura, en los que algunos nodos solo atienden operaciones de lectura (SELECT) mientras que otros pueden atender lectura y escritura (SELECT, INSERT, UPDATE y DELETE). Mantener los nodos réplica sincronizados con los nodos primarios es costoso. Permitir unos pocos milisegundos de retraso para que los datos se propaguen del primario a la réplica permite que el primario procese más consultas.

:::{versionadded} 29
Las instalaciones de Nextcloud pueden tener una conexión primaria y varias conexiones réplica. La abstracción de base de datos dividirá automáticamente las operaciones de lectura y de escritura. Las lecturas van a una réplica, salvo que ocurran dentro de una transacción. Las escrituras siempre van al primario. En cuanto se ha escrito en una tabla, las lecturas posteriores también van al primario.
:::

Otras instalaciones hacen esta división dentro del clúster o con un balanceador de carga de base de datos que envía las consultas a un nodo u otro según criterios, round robin, etc. Esto significa que Nextcloud no siempre puede influir en dónde se ejecutan las consultas.

Es importante que quienes desarrollan Nextcloud tengan esto presente al escribir consultas a la base de datos, sobre todo cuando se trata de una serie de consultas. Las siguientes secciones cubren antipatrones habituales y sus soluciones.

##### Leer datos que se acaban de escribir

Un patrón habitual que funciona bien con bases de datos pequeñas, pero que se desmorona en clústeres sobrecargados, son las lecturas causales. Ocurren cuando un proceso de Nextcloud inserta (INSERT) datos nuevos y lee esos datos de inmediato. Esto puede ser obvio de detectar en el código, pero a veces también queda oculto por listeners de eventos que reaccionan a los datos nuevos.

Hay dos patrones para evitar la lectura «sucia»:

1. **Envolver la operación de escritura+lectura en una transacción**. La división de lectura/escritura de Nextcloud, pero también otros balanceadores de carga de clústeres de bases de datos, garantizan que las consultas de una transacción vayan a un único nodo de base de datos de un clúster. Eso garantiza que los datos escritos estén disponibles al instante para volver a leerlos. Este enfoque garantiza la consistencia, pero agrega carga al nodo primario, porque también tiene que ejecutar la operación de lectura. Es mejor usarlo en bloques de código acotados. No extender las transacciones a los listeners de eventos, porque su ejecución podría provocar {nc-ref}`transacciones largas <performance-long-transactions>` y problemas de bloqueo.
2. **Evitar la operación de lectura**. Si el código lo permite, evitar por completo la operación de lectura. Se debería saber qué se acaba de escribir. Si se necesita el ID autoincremental, usar la función *last insert ID* de la base de datos. Continuar con estos datos, pasarlos a los listeners de eventos, etc. Este enfoque también garantiza la consistencia, pero además mejora el rendimiento general.

:::{tip}
Nextcloud puede ayudar a identificar lecturas tras escritura sin necesidad de montar un clúster para el entorno de desarrollo. Si se cambia el nivel de log a 0 (debug), las lecturas sucias generarán una entrada en el registro. Supervisar el registro mientras se prueba el código.

Prestar atención a mensajes como ``dirty table reads: SELECT `id` FROM `*PREFIX*jobs` WHERE (`class` = :dcValue1) AND (`argument_hash` = :dcValue2) LIMIT 1``. Usar la *traza* de la entrada del registro para localizar el código que ejecutó la consulta.

Tener en cuenta que la detección de lecturas sucias no es perfecta y podría registrar por error una lectura sucia cuando se escriben y leen datos no relacionados. Por ejemplo, se puede leer el usuario *alice*, actualizar sus datos y después leer los datos de *bob* y hacer lo mismo. Aunque la base de datos replique lentamente, no se leerán datos que todavía no existen. Como Nextcloud hace el seguimiento a nivel de tabla, igualmente emite la advertencia.
:::

(nc-dev-performance-long-transactions)=
##### Transacciones largas

Las transacciones son cruciales para los cambios que van juntos, pero pueden causar problemas bajo carga. Esto se debe a que, cuanto más tiempo permanece abierta la transacción, más otras consultas pueden tener que esperar a que se libere un bloqueo. Esto puede provocar contención, peticiones que agotan el tiempo de espera y bloqueos mutuos. Así que conviene usar las transacciones con sensatez e intentar que sean lo más cortas posible. No mezclar, por ejemplo, operaciones de base de datos con operaciones del sistema de archivos.

:::{tip}
Nextcloud puede ayudar a identificar transacciones lentas. Si se cambia el nivel de log a 0 (debug), una transacción lenta generará un mensaje de log en el commit/rollback.

Prestar atención a mensajes como `Transaction took longer than 1s: 7.1270351409912` y `Transaction rollback took longer than 1s: 1.2153599501`.
:::

#### Medir el rendimiento

Si se hacen cambios importantes en la arquitectura o en la estructura de la base de datos, siempre conviene comprobar el impacto positivo o negativo en el rendimiento.

La recomendación es hacer automáticamente 10000 PROPFIND o subidas de archivos, medir el tiempo y comparar el tiempo antes y después del cambio.

### Datos en caché

A partir de Nextcloud 26, los nombres mostrados de los usuarios y los grupos se almacenan en caché. Usar las funciones `IUserManager::getDisplayName` o `IGroupManager::getDisplayName` para evitar viajes de ida y vuelta a la base de datos.

### Obtener ayuda

Si se necesita ayuda con el rendimiento o con otros problemas, preguntar en nuestros [foros](https://help.nextcloud.com).
````
