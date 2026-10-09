---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Bloqueo transaccional de archivos: qué protege, qué no impide y cómo configurar Redis como memcache.locking para aliviar la base de datos."
---
# Bloqueo transaccional de archivos

## Resumen

Esta página explica qué hace el bloqueo transaccional de archivos y qué no hace, y cómo configurar Redis como memcache de bloqueo para aliviar la carga de la base de datos. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/files_locking_transactional.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El mecanismo de bloqueo transaccional de archivos de Nextcloud bloquea los archivos para evitar que se corrompan durante el funcionamiento normal. Cumple estas funciones:

- Opera a un nivel superior al del sistema de archivos, por lo que no es necesario usar un sistema de archivos que admita bloqueos
- Bloquea los directorios superiores para que no puedan renombrarse mientras haya cualquier actividad sobre los archivos que contienen
- Libera los bloqueos cuando se interrumpen las transacciones de archivos, por ejemplo, cuando un cliente de sincronización pierde la conexión durante una subida
- Gestiona correctamente el bloqueo y la liberación de bloqueos en los archivos compartidos durante los cambios de varios usuarios
- Gestiona correctamente los bloqueos en los montajes de almacenamiento externo
- Gestiona correctamente los archivos cifrados

Para qué no sirve el bloqueo transaccional de archivos: no impedirá que varios usuarios editen el mismo documento ni avisará de que otros usuarios están trabajando en el mismo documento. Varios usuarios pueden abrir y editar un archivo al mismo tiempo, y el bloqueo transaccional de archivos no lo impide. Lo que impide es que el archivo se guarde de forma simultánea.

De forma predeterminada, el bloqueo transaccional de archivos usa el backend de bloqueo de la base de datos. Esto supone una carga considerable para la base de datos. Establecer `memcache.locking` alivia la carga de la base de datos y mejora el rendimiento. Quienes administran servidores Nextcloud con cargas de trabajo elevadas deberían instalar una memcache. (Consultar {nc-doc}`admin_manual/configuration_server/caching_configuration`.)

Para usar una memcache con el bloqueo transaccional de archivos, deben instalarse el servidor Redis y el módulo de PHP correspondiente. Después de instalar Redis, debe introducirse en el archivo `config.php` una configuración como la de este ejemplo:

```
'memcache.locking' => '\OC\Memcache\Redis',
'redis' => array(
     'host' => 'localhost',
     'port' => 6379,
     'timeout' => 0.0,
     'password' => '', // Optional, if not defined no password will be used.
      ),
```

:::{note}
Para una mayor seguridad, se recomienda configurar Redis para que exija una contraseña. Consultar <http://redis.io/topics/security> para obtener más información.
:::

Si se quiere configurar Redis para que escuche en un socket Unix (lo que se recomienda si Redis se ejecuta en el mismo sistema que Nextcloud), usar esta configuración de ejemplo de `config.php`:

```
'memcache.locking' => '\OC\Memcache\Redis',
'redis' => array(
     'host' => '/run/redis/redis-server.sock',
     'port' => 0,
     'timeout' => 0.0,
      ),
```

Consultar `config.sample.php` para ver ejemplos de configuración de Redis y de todas las memcaches compatibles.

Puede obtenerse más información sobre Redis en [Redis](http://redis.io/). Memcached, el popular sistema distribuido de caché en memoria, no es adecuado para el nuevo bloqueo de archivos porque no está diseñado para almacenar bloqueos, y los datos pueden desaparecer de la caché en cualquier momento. Redis es un almacén de clave-valor y garantiza que los objetos en caché estén disponibles durante todo el tiempo que se necesiten.
````
