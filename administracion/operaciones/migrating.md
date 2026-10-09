---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo trasladar una instancia de Nextcloud a otro servidor sin cambiar el sistema original: preparación, copia de base de datos y archivos, y cambio de DNS."
---
# Migrar a otro servidor

## Resumen

Esta página describe, paso a paso, cómo trasladar una instancia de Nextcloud a una máquina nueva con Nextcloud fuera de línea: preparar el servidor nuevo, copiar la base de datos, los archivos y la configuración, revisar los valores propios del servidor y redirigir el DNS. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/maintenance/migrating.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Si surge la necesidad, Nextcloud puede migrarse a otro servidor. Un caso de uso típico sería un cambio de hardware o una migración desde el Appliance virtual a un servidor físico. Todas las migraciones deben realizarse con Nextcloud fuera de línea y sin que se produzcan accesos. Nextcloud solo admite la migración en línea cuando se implementan soluciones de clúster y HA estándar del sector antes de instalar Nextcloud por primera vez.

Para empezar, concretemos el caso de uso. Una instancia de Nextcloud configurada funciona de forma fiable en una máquina. Por algún motivo (p. ej., hay disponible una máquina más potente, pero aún no se necesita pasar a un entorno en clúster), la instancia debe trasladarse a una máquina nueva. Según el tamaño de la instancia de Nextcloud, la migración puede tardar varias horas. Como requisito previo, se supone que los usuarios finales acceden a la instancia de Nextcloud mediante un nombre de host virtual (un registro `CNAME` en el DNS) que puede apuntarse a la nueva ubicación. También se supone que el método de autenticación (p. ej., LDAP) sigue siendo el mismo tras la migración.

:::{warning}
En NINGÚN MOMENTO hace falta ningún cambio en el sistema **ORIGINAL**, **EXCEPTO** poner Nextcloud en modo de mantenimiento.

Así se garantiza que, si ocurre algo imprevisto, pueda volverse a la instalación existente y ofrecer a los usuarios un Nextcloud en funcionamiento mientras se depura el problema.
:::

1. Preparar la máquina nueva con el sistema operativo deseado, instalar y configurar el servidor web y PHP para Nextcloud (p. ej., permisos o límites de tamaño de subida de archivos) y asegurarse de que la versión de PHP coincida con la configuración compatible de Nextcloud y de que estén instaladas todas las extensiones de PHP pertinentes. Configurar también la base de datos y asegurarse de que sea una configuración compatible con Nextcloud. Si la máquina original se instaló hace poco, copiar sin más esa configuración base es una buena práctica segura.

   :::{important}
   Antes de empezar la migración, **revisar el archivo `config/config.php` del sistema ORIGINAL** para identificar los servicios opcionales que estén configurados, como:

   - Redis o Memcached (para caché/sesiones)
   - Almacenamiento de objetos externo (S3, etc.)
   - LDAP
   - Ajustes del servidor de correo
   - Backends de búsqueda de texto completo (Elasticsearch, etc.)

   **También hay que instalar y configurar estos mismos servicios en la máquina NUEVA antes de copiar los archivos de Nextcloud.** No hacerlo puede provocar errores como «Redis server went away» o fallos de conexión durante el arranque de Nextcloud.
   :::

2. En la máquina original, detener Nextcloud. Primero, activar el modo de mantenimiento. Tras esperar 6-7 minutos para que todos los clientes de sincronización registren que el servidor está en modo de mantenimiento, detener la aplicación y/o el servidor web que sirve Nextcloud.

3. Crear un volcado de la base de datos y copiarlo a la máquina nueva. Allí, importarlo en la base de datos (consultar {nc-doc}`admin_manual/maintenance/backup` y {nc-doc}`admin_manual/maintenance/restore`).

4. Copiar todos los archivos de la instancia de Nextcloud, los archivos del programa Nextcloud, los archivos de datos, los archivos de registro y los archivos de configuración, a la máquina nueva (consultar {nc-doc}`admin_manual/maintenance/backup` y {nc-doc}`admin_manual/maintenance/restore`). Los archivos de datos deben conservar su marca de tiempo original (puede hacerse usando `rsync` con la opción `-t`); de lo contrario, los clientes volverán a descargar todos los archivos tras la migración. Según el método de instalación original y el sistema operativo, los archivos se encuentran en ubicaciones distintas. En el sistema nuevo, asegurarse de elegir las ubicaciones adecuadas. Si se cambia alguna ruta, asegurarse de adaptar las rutas en el archivo config.php de Nextcloud.

   :::{note}
   Este paso puede tardar varias horas, según la instalación.
   :::

   :::{warning}
   Cambiar la ubicación del directorio de datos puede corromper las relaciones en la base de datos y no está admitido.
   :::

   :::{important}
   Tras copiar `config/config.php` a la máquina nueva, **revisar y actualizar todos los valores específicos del servidor** antes de iniciar Nextcloud. Como mínimo, comprobar:

   - `datadirectory` — mantener esta ruta idéntica a la del servidor original siempre que sea posible. Cambiar la ruta del directorio de datos requiere actualizar la base de datos y se desaconseja enérgicamente; consultar {nc-ref}`Solución de problemas del directorio de datos <troubleshooting_data_directory>` si no queda otra opción.
   - `dbhost`, `dbname`, `dbuser`, `dbpassword` — actualizar si el servidor nuevo usa otro host de base de datos u otras credenciales.
   - `trusted_domains` — añadir o sustituir el nombre de host o la dirección IP del servidor nuevo.
   - `overwrite.cli.url`, `overwritehost`, `overwriteprotocol`, `overwritewebroot` — actualizar para reflejar la URL del servidor nuevo y cualquier configuración de proxy inverso.
   - `memcache.local`, `memcache.distributed`, `memcache.locking` y los parámetros de conexión asociados — actualizar si la dirección del backend de caché/sesiones cambió en la máquina nueva. Según el backend en uso, revisar `redis` o `redis.cluster` (para Redis / Redis Cluster) o `memcached_servers` (para Memcached).
   - `objectstore` — si hay configurado un almacenamiento de objetos externo (S3, Swift, etc.), verificar que el endpoint, el bucket y las credenciales sigan siendo válidos y accesibles desde el servidor nuevo.
   - `mail_smtphost`, `mail_smtpport` — actualizar si el relé SMTP es distinto en el servidor nuevo.
   - `logfile` — actualizar si la ruta del registro es distinta en el servidor nuevo.
   - `tempdirectory` — si está configurado con una ruta personalizada, asegurarse de que esa ruta exista y se pueda escribir en el servidor nuevo.
   - `serverid` — si está configurado, mantener el mismo valor. Identifica el servidor en configuraciones con varios servidores PHP y no debe cambiar. Si se sustituye por servidor mediante la variable de entorno `NC_serverid`, configurar la misma sustitución en el servidor nuevo.

   Los valores `secret` e `instanceid` se generan una sola vez en el momento de la instalación y están ligados a todos los datos cifrados y a las sesiones de usuario. **No cambiarlos ni regenerarlos.** Deben copiarse tal cual del `config.php` original.

   Dejar valores obsoletos (especialmente las credenciales de la base de datos o `datadirectory`) provocará errores de arranque o corrupción de datos.
   :::

5. Revisar el archivo config.php del sistema **ORIGINAL** para ver si tiene `data-fingerprint` configurado con un valor no vacío. En ese caso, asegurarse de ejecutar también el comando `maintenance:data-fingerprint` en el sistema **NUEVO**, de forma similar a como se requiere al restaurar una copia de seguridad (consultar {nc-doc}`admin_manual/maintenance/restore` para los detalles).

6. Con Nextcloud todavía en modo de mantenimiento (¡confirmarlo!) y **ANTES** de cambiar el registro `CNAME` en el DNS, iniciar la base de datos y el servidor web / servidor de aplicaciones en la máquina nueva y abrir en el navegador web la instancia de Nextcloud migrada. Confirmar que se ve el aviso del modo de mantenimiento, que tanto el servidor web como Nextcloud escriben una entrada en el registro y que no aparecen mensajes de error. Después, sacar Nextcloud del modo de mantenimiento y repetir. Iniciar sesión como administrador y confirmar el funcionamiento normal de Nextcloud.

7. Cambiar la entrada `CNAME` en el DNS para dirigir a los usuarios a la nueva ubicación.
````
