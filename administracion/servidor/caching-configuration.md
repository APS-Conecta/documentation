---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Caché de memoria en Nextcloud: opcache, APCu, Redis y Memcached, recomendaciones por tipo de despliegue y su configuración en config.php."
---
# Caché de memoria

## Resumen

Esta página explica los tipos de caché de memoria que admite Nextcloud, qué combinación conviene según el tipo de despliegue y cómo instalar y configurar APCu, Redis y Memcached en `config.php`, además del directorio de caché y el prefijo de las claves. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_server/caching_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El rendimiento del servidor Nextcloud puede mejorarse notablemente con la caché de memoria, que almacena en memoria los objetos solicitados con frecuencia para recuperarlos más rápido. Hay dos tipos de caché que usar: una caché de opcode de PHP, que suele llamarse *opcache*, y una caché de datos para el servidor web, que suele llamarse «memcache».

:::{note}
Si no se instala y activa una memcache local, aparecerá una advertencia en la página de administración de Nextcloud. **Una memcache no es obligatoria. Si se prefiere, la advertencia puede ignorarse sin problema.** Si en `config.php` se activa solo una caché distribuida (`memcache.distributed`) y no una caché local (`memcache.local`), la advertencia de caché seguirá apareciendo.
:::

Una **opcache de PHP** almacena los scripts PHP compilados, para que no haya que volver a compilarlos cada vez que se llaman. PHP incluye Zend OPcache en su núcleo desde la versión 5.5, así que no hace falta instalar una opcache manualmente.

La **caché de datos** la aporta el usuario. Nextcloud admite varios backends de caché de memoria, así que puede elegirse el tipo de memcache que mejor se ajuste a las necesidades. Los backends de caché admitidos son:

- [APCu](https://pecl.php.net/package/APCu) (se requiere APCu 4.0.6 o superior).

  Una caché local para sistemas.

- [Redis](https://redis.io/open-source/) (se requiere 4.0.0 o superior); se espera que [Valkey](https://valkey.io/) y [KeyDB](https://docs.keydb.dev/) funcionen como backends compatibles con Redis.

  :::{note}
  Actualmente, las pruebas automatizadas o formales solo se hacen con Redis Open Source.
  :::

  Para caché local y distribuida, así como para el bloqueo transaccional de archivos.

- [Memcached](https://www.memcached.org/)

  Para caché distribuida.

Las cachés de datos, o memcaches, deben configurarse explícitamente en Nextcloud: instalar y activar la caché deseada y después añadir la entrada correspondiente a `config.php` (en {nc-doc}`Parámetros de configuración <admin_manual/configuration_server/config_sample_php_parameters>` hay una descripción general de todos los parámetros de configuración posibles).

### Recomendaciones según el tipo de despliegue

Pueden usarse a la vez una caché local y una distribuida. Las cachés recomendadas son APCu y Redis. Después de instalar y activar la memcache (caché de datos) elegida, verificar que esté activa ejecutando {nc-ref}`Versión e información de PHP <label-phpinfo>`.

:::{note}
Las opciones de configuración específicas de cada caché están en la sección correspondiente, más abajo.
:::

#### Servidor doméstico pequeño o privado

Usar solo APCu:

```
'memcache.local' => '\OC\Memcache\APCu',
```

#### Organizaciones con un solo servidor

Usar Redis para todo excepto la memcache local:

```
'memcache.local' => '\OC\Memcache\APCu',
'memcache.distributed' => '\OC\Memcache\Redis',
'memcache.locking' => '\OC\Memcache\Redis',
'redis' => [
     'host' => 'localhost',
     'port' => 6379,
],
```

#### Organizaciones con configuraciones en clúster

Usar APCu para la caché local y bien un clúster de Redis ...:

```
'memcache.local' => '\OC\Memcache\APCu',
'memcache.distributed' => '\OC\Memcache\Redis',
'memcache.locking' => '\OC\Memcache\Redis',
'redis.cluster' => [
    'seeds' => [ // provide some/all of the cluster servers to bootstrap discovery, port required
       'cache-cluster:7000',
       'cache-cluster:7001',
    ],
 ],
```

... o bien un clúster de Memcached ...:

```
'memcache.local' => '\OC\Memcache\APCu',
'memcache.distributed' => '\OC\Memcache\Memcached',
'memcache.locking' => '\OC\Memcache\Memcached',
'memcached_servers' => [
    [ 'server1.example.com', 11211 ],
    [ 'server2.example.com', 11211 ],
 ],
```

... para las cachés distribuida y de bloqueo.

:::{note}
Si se ejecutan varios servidores web y se activa en `config.php` una caché distribuida (`memcache.distributed`) o un proveedor de bloqueo de archivos (`memcache.locking`), hay que asegurarse de que apunten exactamente al mismo servidor o clúster de memcache y no a `localhost` ni a un socket unix.
:::

#### Notas adicionales sobre Redis frente a APCu para la caché de memoria

APCu es más rápido que Redis para la caché local. Si hay memoria suficiente, usar APCu para la caché de memoria y Redis para el bloqueo de archivos. Si hay poca memoria, usar Redis para ambos.

### APCu

APCu es una caché de datos y está disponible en la mayoría de las distribuciones Linux. En sistemas Red Hat/CentOS/Fedora, instalar `php-pecl-apcu`. En sistemas Debian/Ubuntu/Mint, instalar `php-apcu`.

Después de reiniciar el servidor web, añadir esta línea al archivo `config.php`:

```
'memcache.local' => '\OC\Memcache\APCu',
```

Al actualizar la página de administración de Nextcloud, la advertencia de caché debería desaparecer.

Según el tamaño de la instalación y el número de usuarios e interacciones con el sistema, puede convenir adaptar el ajuste `apc.shm_size` en `php.ini`. El valor predeterminado es 32M, que suele ser demasiado bajo para Nextcloud. Un buen punto de partida es 128M. Si hay muchos usuarios y/o muchas apps instaladas, puede convenir aumentar más este valor. Hay que tener en cuenta que esta memoria debe estar disponible en la memoria del sistema y considerarse al dimensionar la cantidad de workers del servidor.

Una caché que se reinicia con frecuencia puede provocar ralentizaciones inesperadas mientras se vacía y se vuelve a llenar.

Hay una comprobación de administración que intenta detectar un dimensionamiento de memoria demasiado bajo, pero conviene supervisar el estado de la caché APCu para ver si está llena y si hay que aumentar su tamaño. [APCu proporciona un script](https://github.com/krakjoe/apcu/blob/master/apc.php) que puede ayudar con esto; si no, la [app serverinfo](https://github.com/nextcloud/serverinfo) de Nextcloud también puede mostrar el estado de la caché APCu.

### Redis

Redis es una memcache moderna excelente para usarla como caché distribuida y como almacén clave-valor para el {nc-doc}`bloqueo transaccional de archivos <admin_manual/configuration_files/files_locking_transactional>`, porque garantiza que los objetos en caché estén disponibles durante todo el tiempo que se necesiten.

Nextcloud usa la extensión PHP PhpRedis. Esta extensión proporciona una API para comunicarse con almacenes clave-valor compatibles con Redis. Redis Open Source es el backend probado formalmente; se espera que Valkey y KeyDB funcionen también como backends compatibles.

El módulo PHP de Redis debe ser de la versión 2.2.6 o superior. Si se usa una distribución Linux que no empaqueta las versiones compatibles de este módulo, o que no empaqueta Redis en absoluto, consultar {nc-ref}`Memcached <install_redis_label>`.

En Debian/Ubuntu/Mint, instalar `redis-server` (o equivalente) y `php-redis`. Los nombres de los paquetes varían según la distribución y el backend.

En CentOS y Fedora, instalar `redis` (o equivalente) y `php-pecl-redis`. No se inicia automáticamente, así que hay que usar el gestor de servicios para iniciar el servidor `redis` y para lanzarlo como demonio en el arranque.

Puede verificarse que el demonio de Redis está en ejecución con `ps ax`:

```
ps ax | grep redis
22203 ? Ssl    0:00 /usr/bin/redis-server 127.0.0.1:6379
```

Reiniciar el servidor web, añadir las entradas correspondientes a `config.php` y actualizar la página de administración de Nextcloud.

#### Configuración de Redis en Nextcloud (config.php)

Para obtener el mejor rendimiento, usar Redis para el bloqueo de archivos añadiendo esto:

```
'memcache.locking' => '\OC\Memcache\Redis',
```

Además, conviene usar Redis para la caché distribuida del servidor:

```
'memcache.distributed' => '\OC\Memcache\Redis',
```

Asimismo, podría usarse Redis para la caché local de esta manera, pero no se recomienda (ver la advertencia más abajo):

```
'memcache.local' => '\OC\Memcache\Redis',
```

:::{warning}
Usar Redis para la caché local en una configuración con varios servidores puede causar problemas. Además, incluso en una configuración de un solo servidor, APCu (ver la sección anterior) debería ser más rápido.
:::

Al usar Redis para cualquiera de los ajustes de caché anteriores, también hay que especificar la configuración `redis` o `redis.cluster` en `config.php`.

Las siguientes opciones pueden configurarse al usar un único servidor redis (todas son opcionales salvo `host` y `port`; para estas dos, ver las secciones siguientes):

```
'memcache.locking' => '\OC\Memcache\Redis',
'memcache.distributed' => '\OC\Memcache\Redis',
'memcache.local' =>'\OC\Memcache\Redis' ,
'memcache_customprefix' => 'mynextcloudprefix',
'redis' => [
   // 'host'      => see connection parameters below
   // 'port'      => see connection parameters below
  'user'          => 'nextcloud',
  'password'      => 'password',
  'dbindex'       => 0,
  'timeout'       => 1.5,
  'read_timeout'  => 1.5,
],
```

Las siguientes opciones pueden configurarse al usar un clúster de redis (todas son opcionales salvo `seeds`):

```
'memcache.locking' => '\OC\Memcache\Redis',
'memcache.distributed' => '\OC\Memcache\Redis',
'memcache.local' =>'\OC\Memcache\Redis' ,
'memcache_customprefix' => 'mynextcloudprefix',
'redis.cluster' => [
   'seeds' => [ // provide some/all of the cluster servers to bootstrap discovery, port required
      'cache-cluster:7000',
      'cache-cluster:7001',
      'cache-cluster:7002',
      'cache-cluster:7003',
      'cache-cluster:7004',
      'cache-cluster:7005'
   ],
   'failover_mode'   => \RedisCluster::FAILOVER_ERROR,
   'timeout'         => 0.0,
   'read_timeout'    => 0.0,
   'user'            => 'nextcloud',
   'password'        => 'password',
   'dbindex'         => 0,
],
```

:::{note}
El puerto es obligatorio como parte de la URL del servidor. Sin embargo, no es necesario enumerar todos los servidores: por ejemplo, si todos los servidores se balancean a través del mismo nombre DNS, solo hace falta ese nombre de servidor.
:::

#### Conectarse a un único servidor Redis por TCP

Para conectarse por TCP a un servidor Redis remoto o local, usar:

```
'redis' => [
   'host' => 'redis-host.example.com',
   'port' => 6379,
],
```

#### Conectarse a un único servidor Redis por TLS

Para conectarse por TCP sobre TLS, añadir la siguiente configuración:

```
'redis' => [
   'host' => 'tls://127.0.0.1',
   'port' => 6379,
   'ssl_context' => [
      'local_cert' => '/certs/redis.crt',
      'local_pk' => '/certs/redis.key',
      'cafile' => '/certs/ca.crt',
      'verify_peer_name' => false,
   ],
],
```

#### Conectarse a un clúster de Redis por TLS

Para conectarse por TCP sobre TLS, añadir la siguiente configuración:

```
'redis.cluster' => [
   'seeds' => [ // provide some/all of the cluster servers to bootstrap discovery, port required
      'cache-cluster:7000',
      'cache-cluster:7001',
   ],
   'ssl_context' => [
      'local_cert' => '/certs/redis.crt',
      'local_pk' => '/certs/redis.key',
      'cafile' => '/certs/ca.crt',
      'verify_peer_name' => false,
   ],
],
```

#### Conectarse a un único servidor Redis por socket UNIX

Para conectarse a un Redis configurado para escuchar en un socket Unix (lo que se recomienda si Redis se ejecuta en el mismo sistema que Nextcloud), usar esta configuración de ejemplo de `config.php`:

```
'redis' => [
   'host'     => '/run/redis/redis-server.sock',
   'port'     => 0,
],
```

Solo las variables «host» y «port» son obligatorias; las demás son opcionales.

Actualizar en consecuencia la configuración de redis en `/etc/redis/redis.conf`: descomentar las opciones del socket Unix y asegurarse de que los ajustes «socket» y «port» coincidan con la configuración de Nextcloud.

Hay que asegurarse de establecer los permisos correctos en redis.sock para que el servidor web pueda leer y escribir en él. Para ello, normalmente hay que añadir el usuario del servidor web al grupo redis:

```
usermod -a -G redis www-data
```

Y modificar en consecuencia `unixsocketperm` en `redis.conf`:

```
unixsocketperm 770
```

Puede ser necesario reiniciar apache y redis para que los cambios surtan efecto:

```
systemctl restart apache2
systemctl restart redis-server
```

Redis es muy configurable; para saber más, consultar [la documentación de Redis](http://redis.io/documentation).

#### Usar el gestor de sesiones de Redis

Si se usa Redis para el bloqueo y/o la caché, puede convenir usar también Redis para la gestión de sesiones. A diferencia del gestor estándar *files*, Redis puede usarse para gestionar las sesiones de forma centralizada en varios servidores de aplicación de Nextcloud. Sin embargo, si se usa el gestor de Redis, *HAY QUE* asegurarse de que el bloqueo de sesiones esté activado. En el momento de escribir esto, el gestor de sesiones de Redis *NO* activa el bloqueo de sesiones de forma predeterminada, lo que puede corromper las sesiones en algunas apps de Nextcloud que escriben mucho en la sesión, como Talk. Además, incluso con el bloqueo de sesiones activado, si la aplicación no consigue obtener un bloqueo, el gestor de sesiones de Redis actualmente no devuelve ningún error. Añadir los siguientes ajustes al archivo `php.ini` evita que se corrompan las sesiones al usar Redis como gestor de sesiones:

```
redis.session.locking_enabled=1
redis.session.lock_retries=-1
redis.session.lock_wait_time=10000
```

Hay más información sobre la configuración del gestor de sesiones de phpredis en la [página de PhpRedis en GitHub](https://github.com/phpredis/phpredis)

(nc-install_redis_label)=
### Memcached

Memcached es un veterano fiable para la caché compartida en servidores distribuidos y funciona bien con Nextcloud, con una excepción: no es adecuado para el {nc-doc}`bloqueo transaccional de archivos <admin_manual/configuration_files/files_locking_transactional>`, porque no almacena bloqueos y los datos pueden desaparecer de la caché en cualquier momento (Redis es la mejor memcache para esto).

:::{note}
Hay que asegurarse de instalar el módulo PHP **memcached**, y no memcache, como en los ejemplos siguientes. Nextcloud solo admite el módulo PHP **memcached**.
:::

Configurar Memcached es fácil. En Debian/Ubuntu/Mint, instalar `memcached` y `php-memcached`. El instalador inicia automáticamente `memcached` y lo configura para que se lance al arrancar.

En Red Hat/CentOS/Fedora, instalar `memcached` y `php-pecl-memcached`. No se inicia automáticamente, así que hay que usar el gestor de servicios para iniciar `memcached` y para lanzarlo como demonio en el arranque.

Puede verificarse que el demonio de Memcached está en ejecución con `ps ax`:

```
ps ax | grep memcached
19563 ? Sl 0:02 /usr/bin/memcached -m 64 -p 11211 -u memcache -l
127.0.0.1
```

Reiniciar el servidor web, añadir las entradas correspondientes a `config.php` y actualizar la página de administración de Nextcloud.

#### Configuración de Memcached en Nextcloud (config.php)

Este ejemplo usa APCu para la caché local y Memcached como memcache distribuida, y enumera todos los servidores del grupo de caché compartida con sus números de puerto:

```
'memcache.local' => '\OC\Memcache\APCu',
'memcache.distributed' => '\OC\Memcache\Memcached',
'memcache.locking' => '\OC\Memcache\Memcached',
'memcached_servers' => [
     [ 'server0.example.com', 11211 ],
     [ 'server1.example.com', 11211 ],
     [ 'server2.example.com', 11211 ],
 ],
```

### Ubicación del directorio de caché

El directorio de caché es, de forma predeterminada, `data/$user/cache`, donde `$user` es el usuario actual. Puede usarse la directiva `'cache_path'` en `config.php` (ver {nc-doc}`Parámetros de configuración <admin_manual/configuration_server/config_sample_php_parameters>`) para elegir otra ubicación.

### Prefijo de las claves de caché para Redis o Memcached

De forma predeterminada, Nextcloud genera un prefijo semiúnico para las claves de caché a partir de información como el ID de instancia, la versión, etc., para mitigar el problema de las colisiones al usar la misma caché para varias instancias de Nextcloud. Para evitar por completo las colisiones, puede usarse el siguiente ajuste para definir un prefijo personalizado:

```
'memcache_customprefix' => 'mynextcloudprefix',
```

Esto también permite crear ACL en Redis y limitar las claves a las que pueden acceder determinados usuarios (p. ej., para aislar instancias concretas de Nextcloud que usan la misma caché). Esto puede ser relevante para la seguridad.
````
