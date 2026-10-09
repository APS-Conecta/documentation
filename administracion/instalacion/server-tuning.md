---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Ajustes que mejoran el rendimiento de Nextcloud: cron, registro, caché, base de datos, AES-NI, HTTP/2, PHP-FPM, OPcache e Imaginary."
---
# Ajuste del servidor

## Resumen

Esta página reúne cambios de configuración que mejoran el rendimiento del servidor Nextcloud: tareas en segundo plano con cron, nivel de registro y modo de depuración, caché, base de datos, bloqueo de archivos con Redis, AES-NI, HTTP/2, el ajuste de PHP-FPM y de OPcache, y la generación de vistas previas con Imaginary. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/installation/server_tuning.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

Esta página reúne cambios de configuración que pueden mejorar el rendimiento del servidor Nextcloud. La mayoría de los elementos solo requieren editar un archivo de configuración o instalar un paquete, mientras que unos pocos implican servicios adicionales. Empezar por los que se ajusten a la configuración propia y revisar el resto a medida que la instancia crezca.

### Usar cron para ejecutar las tareas en segundo plano

Consultar {nc-doc}`admin_manual/configuration_server/background_jobs_configuration` para ver una descripción y sus ventajas.

### Reducir la carga del sistema

Una carga alta del sistema ralentiza Nextcloud y también puede provocar otros efectos secundarios no deseados. Para reducir la carga, primero hay que identificar el origen del problema. Herramientas como htop, iotop, [netdata](https://my-netdata.io) o [glances](https://nicolargo.github.io/glances/) pueden ayudar a identificar el proceso o la unidad que ralentiza el sistema. Primero, asegurarse de haber instalado y asignado suficiente RAM. Reducir al mínimo posible el uso de swap, ya que un intercambio excesivo puede degradar gravemente el rendimiento. Si la base de datos se ejecuta dentro de una VM, usar un dispositivo de bloques dedicado para el almacenamiento de la base de datos en lugar de guardarla dentro del archivo de imagen de disco de la VM, para reducir la latencia que causan las múltiples capas de abstracción.

(nc-caching)=
### Niveles de registro

Verificar el `loglevel` del archivo `config.php`. En las instalaciones nuevas, el nivel de registro predeterminado es `2` (WARN). A veces este parámetro se deja por descuido en el nivel DEBUG (`0`) después de solucionar un problema. En algunas instalaciones antiguas, este parámetro también puede tener un valor distinto del predeterminado. Usar `0` (DEBUG) cuando haya un problema que diagnosticar y después devolver el nivel de registro a uno menos detallado. DEBUG genera mucha información y puede afectar al rendimiento del servidor.

### Modo de depuración

Verificar que `debug` esté establecido en `false` en el archivo `config.php`. El valor predeterminado es `false` en las instalaciones nuevas (o cuando no se especifica). Aunque es similar al nivel de registro DEBUG, esta opción también desactiva varias optimizaciones (para facilitar la depuración) y genera salida de depuración adicional tanto en el navegador como en el servidor. No debe activarse en entornos de producción, salvo durante una solución de problemas aislada.

### Caché

La caché mejora el rendimiento al almacenar datos, código y otros objetos en memoria. La caché de memoria no está activada de forma predeterminada porque requiere extensiones opcionales (como APCu) o componentes del sistema (p. ej., Redis), o ambos. Aunque estos complementos no suelen ser difíciles de instalar y activar —al menos en despliegues de un solo servidor—, hay que instalarlos antes de activar su uso en Nextcloud. Consultar {nc-doc}`admin_manual/configuration_server/caching_configuration` para obtener orientación.

### Compresión

Activar la compresión en el servidor web para los archivos JavaScript, CSS y SVG mejora el rendimiento, porque se transfieren menos datos a los clientes.

### Sustituir SQLite

SQLite es una base de datos adecuada para algunos casos de uso, pero usar MariaDB, MySQL o PostgreSQL puede ser más beneficioso con Nextcloud.

Si no se selecciona una base de datos en el momento de la instalación, se usa SQLite de forma predeterminada, porque no requiere ningún componente externo.

Sin embargo, en general se recomiendan MySQL/MariaDB o PostgreSQL para Nextcloud, debido a las [limitaciones de rendimiento de SQLite con aplicaciones de alta concurrencia](https://www.sqlite.org/whentouse.html), como Nextcloud.

Si la instalación ya funciona sobre SQLite, se puede convertir a MySQL o MariaDB con los pasos que se indican en {nc-doc}`admin_manual/configuration_database/db_conversion`.

Consultar la sección {nc-doc}`admin_manual/configuration_database/linux_database_configuration` para obtener instrucciones sobre cómo configurar Nextcloud para MySQL o MariaDB.

### Ajustar la base de datos

Las bases de datos no son plug-and-play. Se benefician no solo de una configuración básica para la compatibilidad con Nextcloud, sino también de un ajuste dentro del entorno en el que se despliegan. Este ajuste debe basarse en el hardware, el almacenamiento, los patrones de uso, el sistema operativo subyacente, las prioridades y otros factores.

Para más detalles y ayuda para ajustar la base de datos:

- [MariaDB – Optimización y ajuste](https://mariadb.com/docs/server/ha-and-performance/optimization-and-tuning/)
- [PostgreSQL – Consumo de recursos](https://www.postgresql.org/docs/17/runtime-config-resource.html)
- [PostgreSQL – Ajustar el servidor PostgreSQL](https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server)

### Usar el bloqueo transaccional de archivos basado en Redis

El bloqueo transaccional de archivos usa la base de datos como backend predeterminado. Esto añade carga a la base de datos. Consultar la sección {nc-doc}`admin_manual/configuration_files/files_locking_transactional` para obtener instrucciones sobre cómo configurar Nextcloud para usar el bloqueo transaccional de archivos basado en Redis.

### TLS / app de cifrado

TLS (HTTPS) y el cifrado/descifrado de archivos pueden delegarse en la extensión AES-NI del procesador. Esto puede acelerar estas operaciones y a la vez reducir la sobrecarga de procesamiento. Requiere un procesador con el [conjunto de instrucciones AES-NI](https://wikipedia.org/wiki/AES_instruction_set).

A continuación, algunos ejemplos de cómo comprobar si la CPU o el entorno admiten la extensión AES-NI:

- Para cada núcleo de CPU presente: `grep flags /proc/cpuinfo` o, como resumen para todos los núcleos: `grep -m 1 '^flags' /proc/cpuinfo`. Si el resultado contiene `aes`, la extensión está presente.

- En los procesadores Intel, se puede buscar en la base de datos Intel ARK para comprobar si la CPU admite AES-NI. Usar el [filtro de características de procesadores de Intel](https://ark.intel.com/MySearch.aspx?AESTech=true), filtrando por «AES New Instructions».

- En las versiones de openssl >= 1.0.1, AES-NI no funciona mediante un motor y no aparece en el comando `openssl engine`. Está activo de forma predeterminada en el hardware compatible. La versión de OpenSSL puede comprobarse con `openssl version -a`.

- Si el procesador admite AES-NI pero no aparece mediante `grep` o `coreinfo`, puede que simplemente esté desactivado en la BIOS. Revisar la configuración de la BIOS.

- Si el entorno se ejecuta virtualizado, consultar al proveedor de virtualización sobre la compatibilidad.

### Activar HTTP/2 para una carga más rápida

HTTP/2 ofrece [enormes mejoras de velocidad](https://www.troyhunt.com/i-wanna-go-fast-https-massive-speed-advantage/) frente a HTTP con múltiples solicitudes. La mayoría de los *navegadores ya admiten HTTP/2 sobre TLS (HTTPS)*.

### Ajustar PHP-FPM

PHP-FPM es necesario en las configuraciones con Nginx y también se usa mucho con Apache. Su configuración predeterminada es extremadamente conservadora: el pool predeterminado tiene `pm.max_children = 5`, lo que limita Nextcloud a cinco solicitudes de PHP simultáneas y es una causa habitual de tiempos de espera agotados de la pasarela, cargas lentas de páginas y errores del cliente de sincronización con cualquier carga real.

#### Modos del gestor de procesos

La directiva `pm` controla cómo gestiona PHP-FPM sus procesos de trabajo:

- `dynamic`: mantiene vivos entre `pm.min_spare_servers` y `pm.max_spare_servers` procesos de trabajo inactivos, hasta un máximo de `pm.max_children`. Un buen valor predeterminado para la mayoría de las instalaciones de Nextcloud: equilibra la eficiencia en el uso de RAM con la capacidad para absorber picos. Establecer `pm.min_spare_servers` lo bastante alto para que los picos de sondeo de los clientes de sincronización no se atasquen esperando a que se generen procesos nuevos.

- `static`: mantiene siempre exactamente `pm.max_children` procesos en ejecución. El mayor uso de memoria y la menor latencia. Usarlo en servidores dedicados con carga predecible. Establecer siempre `pm.max_requests` para reciclar los procesos de trabajo y evitar fugas de memoria.

- `ondemand`: genera un proceso de trabajo solo cuando llega una solicitud; termina los procesos inactivos después de `pm.process_idle_timeout` (predeterminado: `10s`). El menor uso de memoria, pero añade latencia de arranque en frío en cada pico. No se recomienda para Nextcloud: los clientes de escritorio y móviles sondean cada 30 segundos, lo que provoca arranques en frío una y otra vez.

#### Parámetros clave

- `pm.max_children`: número máximo (o fijo, con `static`) de procesos de trabajo simultáneos. Es el valor más importante que ajustar. Si todos los procesos de trabajo están ocupados, las solicitudes nuevas se ponen en cola; una cola llena produce errores 502/504.

  Estimarlo a partir de la RAM disponible:

  ```
  pm.max_children = floor(available_RAM_for_PHP / average_worker_RSS)
  ```

  Medir el RSS medio de un pool en ejecución:

  ```
  ps --no-headers -o rss -C php-fpm | awk '{sum+=$1; count++} END {if (count>0) print sum/count/1024 " MB"; else print "No php-fpm processes found"}'
  ```

  Un proceso de trabajo típico de Nextcloud usa **50–100 MB** (más si se cargan Imagick o LDAP). Hay que dejar margen para el sistema operativo, el servidor web, la base de datos y la caché. Establecer `pm.max_children` demasiado alto provoca swapping, que es peor que la espera en cola.

- `pm.start_servers` *(solo dynamic)*: procesos de trabajo que se inician al arrancar FPM. Si no se establece, el valor predeterminado es `(pm.min_spare_servers + pm.max_spare_servers) / 2`.

- `pm.min_spare_servers` / `pm.max_spare_servers` *(solo dynamic)*: rango de procesos de trabajo inactivos que se mantienen listos. En Nextcloud, mantener `pm.min_spare_servers` lo bastante alto para absorber un pico de clientes de sincronización sin generar procesos nuevos:

  ```
  pm.min_spare_servers = 4    # adjust upward for many connected clients
  pm.max_spare_servers = 16
  ```

- `pm.max_requests`: recicla un proceso de trabajo después de este número de solicitudes. `0` significa no reciclar nunca. Establecer un valor de `500`–`1000` protege contra el crecimiento lento de la memoria por extensiones con fugas (Imagick, LDAP, analizadores XML de SAML). Imprescindible en el modo `static`.

- `pm.process_idle_timeout` *(solo ondemand)*: cuánto tiempo vive un proceso de trabajo inactivo antes de que se termine. Predeterminado: `10s`.

#### Configuración de ejemplo

Un punto de partida para el modo `dynamic` en un servidor con 2 GB de RAM dedicados a PHP (ajustar `pm.max_children` según el RSS medido de los procesos de trabajo):

```ini
pm = dynamic
pm.max_children = 30
pm.start_servers = 8
pm.min_spare_servers = 4
pm.max_spare_servers = 16
pm.max_requests = 500
```

Usar la [calculadora de procesos de PHP-FPM](https://spot13.com/pmcalculator/) para contrastar los valores.

#### Registro de lentitud

Activar el registro de lentitud (slow log) para identificar los scripts PHP que tardan demasiado:

```ini
slowlog = /var/log/php-fpm-slow.log
request_slowlog_timeout = 5s
```

Cada entrada registra la traza completa de PHP de la solicitud lenta. Es la forma más rápida de encontrar la causa raíz de los tiempos de espera agotados de la pasarela y de las páginas lentas.

#### Solución de problemas

- **502 Bad Gateway**: todos los procesos de trabajo de `pm.max_children` están ocupados. Aumentar `pm.max_children` si la RAM lo permite. Activar el registro de lentitud para comprobar si una consulta lenta está acaparando procesos de trabajo. Comprobar también que un `request_terminate_timeout` no esté terminando procesos de trabajo en mitad de una solicitud.

- **504 Gateway Timeout**: un proceso de trabajo está en ejecución pero no responde dentro del tiempo de espera hacia el upstream del servidor web (nginx `fastcgi_read_timeout`, Apache `ProxyTimeout`). Causas habituales en Nextcloud: operaciones con archivos grandes, consultas lentas a la base de datos durante la sincronización o PROPFIND sobre árboles de directorios grandes. Usar el registro de lentitud para identificar el cuello de botella.

- **La memoria crece con el tiempo**: pueden producirse fugas de memoria en los procesos de trabajo. Entre los culpables habituales están las bibliotecas que gestionan recursos externos (como Imagick para el procesamiento de imágenes). Usar el registro de lentitud y la supervisión del RSS para identificar qué solicitudes causan el crecimiento. Establecer `pm.max_requests = 500` para reciclarlos antes de que crezcan demasiado.

- **Primera solicitud lenta tras un periodo de inactividad**: `pm = ondemand` o `pm.min_spare_servers` demasiado bajo. Cambiar a `pm = dynamic` y subir `pm.min_spare_servers`.

Después de cualquier cambio de configuración, recargar PHP-FPM; los cambios no surten efecto hasta hacerlo:

```bash
sudo systemctl reload php8.3-fpm   # Debian/Ubuntu — adjust version as needed
sudo systemctl reload php-fpm      # RHEL/Fedora
```

Para los detalles de configuración del pool (variables de entorno, tamaños de subida, socket Unix frente a TCP), consultar {nc-ref}`php_fpm_tips_label` en la guía de instalación.

### Activar OPcache de PHP

[OPcache](https://www.php.net/manual/en/book.opcache.php) mejora el rendimiento de las aplicaciones PHP almacenando en caché el bytecode precompilado.

#### Revalidación

La revalidación de OPcache en PHP gestiona los cambios hechos en el código de la aplicación PHP almacenado en disco. Hay cambios de código cada vez que:

- se actualiza Nextcloud o una app de Nextcloud
- se hace un cambio de configuración (p. ej., cuando se modifica `config.php`)

Nextcloud, en la medida de lo posible, gestiona internamente la revalidación de la caché cuando es necesaria. Sin embargo, esto no es infalible. En un entorno PHP predeterminado, la revalidación está activada y cada `2` segundos se comprueba si los scripts en caché cambiaron en disco. En muchos entornos, estos valores predeterminados son razonables y puede que nunca haga falta cambiarlos.

Sin embargo, la frecuencia de revalidación puede ajustarse, lo que *potencialmente* puede mejorar el rendimiento. Aquí no hacemos recomendaciones sobre valores adecuados para la revalidación (aparte de los predeterminados de PHP).

:::{danger}
Aumentar el tiempo entre revalidaciones (o desactivarla por completo) significa que los cambios en los scripts, incluido `config.php`, tardarán más en hacerse efectivos (o puede que nunca lo hagan si la revalidación está desactivada por completo). Aumentar el intervalo también eleva el riesgo de problemas transitorios en las actualizaciones del servidor y de las aplicaciones, e impide activar y desactivar correctamente el modo de mantenimiento.
:::

:::{warning}
Si se ajustan estos parámetros, es más probable que haya que reiniciar o recargar el servidor web (`mod_php`) o PHP-FPM después de hacer cambios de configuración o de realizar actualizaciones. Si se olvida hacerlo, puede producirse un comportamiento inusual por un desajuste entre lo que hay en disco y lo que hay en memoria. Puede parecer que son errores, pero desaparecerán en cuanto se reinicie o recargue `mod_php` / fpm.
:::

Para cambiar el valor predeterminado de `2` y comprobar los cambios en disco como máximo cada `60` segundos, añadir el siguiente ajuste al archivo `php.ini`:

```ini
opcache.revalidate_freq = 60
```

Cualquier actualización del servidor o de apps, o cualquier cambio en `config.php`, requerirá entonces reiniciar PHP (o vaciar la caché manualmente de otra forma o invalidar ese script en particular).

:::{warning}
Por favor, no informar de errores ni de comportamientos extraños después de actualizar Nextcloud o apps de Nextcloud hasta haber reiniciado mod_php/fpm (para confirmar que el problema no lo causa la configuración local de la revalidación).
:::

#### Tamaño

Si algún límite de tamaño de OPcache supera el 90 % de su tamaño asignado, el panel de administración mostrará una advertencia al respecto y sugerirá cambios.

Para más detalles, consultar la [documentación oficial de PHP](https://php.net/manual/en/opcache.configuration.php). Para supervisar el uso de OPcache y borrar entradas de caché individuales o todas, se puede usar [opcache-gui](https://github.com/amnuts/opcache-gui).

#### Comentarios

Nextcloud requiere estrictamente que los comentarios del código se conserven en el opcode, que es el comportamiento predeterminado. Si se cambiaron los ajustes de PHP, asegurarse de que lo siguiente esté establecido en `php.ini`:

```ini
opcache.save_comments = 1
```

#### JIT

PHP incluye un compilador JIT que puede activarse en plataformas x86 para beneficiar a cualquier app con uso intensivo de la CPU que se esté ejecutando. Para activar un JIT de trazado con todas las optimizaciones, añadir a `php.ini`:

```ini
opcache.jit = 1255
opcache.jit_buffer_size = 8M
```

:::{note}
La mayoría de las instancias de Nextcloud usan menos de 2 MiB del tamaño de búfer de JIT configurado, así que 8 MiB suelen bastar. Sin embargo, el uso total de OPcache aumenta en un margen mayor. Puede que en algunos casos haya que aumentar el parámetro de PHP `opcache.memory_consumption`. El uso del búfer de JIT también puede supervisarse con [opcache-gui](https://github.com/amnuts/opcache-gui).
:::

### Vistas previas

Es posible acelerar la generación de vistas previas con un microservicio externo: [Imaginary](https://github.com/h2non/imaginary).

:::{warning}
Actualmente Imaginary es incompatible con el cifrado del lado del servidor. Consultar <https://github.com/nextcloud/server/issues/34262>
:::

Recomendamos encarecidamente ejecutar nuestra imagen de Docker personalizada, que está más actualizada que la imagen oficial. La imagen está en <https://ghcr.io/nextcloud-releases/aio-imaginary>. Al ejecutarla, mapear un puerto añadiendo *-p \<port\>:9000* al comando *docker run* (o su equivalente en Compose), p. ej.:

```
docker run -d -p 9000:9000 --name nextcloud_imaginary --restart always ghcr.io/nextcloud-releases/aio-imaginary:latest
```

Asegurarse de que el servicio solo sea accesible desde los servidores internos. Después, configurar Nextcloud para que use Imaginary editando el archivo `config.php`:

```php
'enabledPreviewProviders' => [
    'OC\Preview\TXT',
    'OC\Preview\MarkDown',
    'OC\Preview\OpenDocument',
    'OC\Preview\Krita',
    'OC\Preview\Imaginary',
],
'preview_imaginary_url' => 'http://<url of imaginary>:<port>',
```

:::{warning}
Asegurarse de iniciar Imaginary con el parámetro de línea de comandos `-return-size`. De lo contrario, habrá un pequeño impacto en el rendimiento. El parámetro requiere una versión reciente de Imaginary (posterior a v1.2.4). Además, si se ejecuta Imaginary en Docker, hay que añadir la capacidad del contenedor de Docker `SYS_NICE` mediante `--cap-add=sys_nice` (CLI de Docker) o `cap_add: - SYS_NICE` (Docker Compose), ya que Imaginary la necesita para generar las vistas previas de HEIC. Esto no se aplica cuando Imaginary se ejecuta fuera de Docker.
:::

:::{note}
En instancias grandes, seguir la [recomendación de escalabilidad de Imaginary](https://github.com/h2non/imaginary#scalability).
:::

#### Ajustes

Para establecer el formato de las vistas previas de Imaginary (el predeterminado es jpeg), añadir a `config.php`:

```
'preview_format' => 'webp',
```

Para establecer una clave de API para Imaginary:

```
'preview_imaginary_key' => 'secret',
```

La calidad WebP predeterminada de las imágenes de vista previa es '80'. Cambiarla con:

```
occ config:app:set preview webp_quality --value="30"
```
````
