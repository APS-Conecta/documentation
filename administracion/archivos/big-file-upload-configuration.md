---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Subir archivos de más de 512 MB: límites del sistema, ajustes de PHP, Apache y nginx, directorio temporal, tamaño de fragmento y almacenamiento de objetos."
---
# Subida de archivos grandes > 512 MB

## Resumen

Esta página explica cómo ampliar el tamaño máximo de subida de archivos: los límites del sistema, los ajustes de PHP y del servidor web (Apache y nginx), la configuración del servidor, el tamaño de fragmento de subida y las particularidades del almacenamiento de objetos y de la compartición federada. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/big_file_upload_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El tamaño máximo de archivo predeterminado para las subidas es de 512 MB. Este límite puede aumentarse hasta lo que permitan el sistema de archivos y el sistema operativo. Hay ciertos límites estrictos que no pueden superarse:

- < 2 GB en arquitecturas de sistema operativo de 32 bits
- < 2 GB con IE6 - IE8
- < 4 GB con IE9 - IE11

Los sistemas de archivos de 64 bits tienen límites mucho más altos; consultar la documentación del sistema de archivos.

:::{note}
El cliente de sincronización de Nextcloud no se ve afectado por estos límites de subida, ya que sube los archivos en fragmentos más pequeños. Consultar la [documentación del cliente](https://docs.nextcloud.com/desktop/latest/advancedusage.html) para obtener más información sobre las opciones de configuración.
:::

### Configuración del sistema

- Asegurarse de que está instalada la versión más reciente de PHP
- Desactivar las cuotas de usuario, lo que las deja ilimitadas
- El archivo o la partición temporal debe ser lo bastante grande para alojar varias subidas en paralelo de varios usuarios; p. ej., si el tamaño máximo de subida es de 10 GB y el número medio de usuarios que suben a la vez es de 100, el espacio temporal debe poder alojar al menos 10x100 GB

### Configurar el servidor web

:::{note}
Nextcloud incluye su propio archivo `nextcloud/.htaccess`. Como `php-fpm` no puede leer los ajustes de PHP de `.htaccess`, estos ajustes deben establecerse en el archivo `nextcloud/.user.ini`.
:::

Establecer los dos parámetros siguientes en el archivo php.ini correspondiente (consultar la sección **Loaded Configuration File** de {nc-ref}`Versión e información de PHP <label-phpinfo>` para encontrar los archivos php.ini pertinentes):

```
php_value upload_max_filesize 16G
php_value post_max_size 16G
```

Es posible que los ajustes `upload_max_filesize` y `post_max_size` no se apliquen a las subidas de archivos mediante peticiones PUT de WebDAV de un solo archivo ni a las [subidas de archivos por fragmentos](https://docs.nextcloud.com/server/latest/developer_manual/client_apis/WebDAV/chunking.html). En esos casos, los tiempos de espera de PHP y del servidor web son el factor que limita el tamaño de la subida.

Ajustar estos valores según las necesidades. Si aparecen tiempos de espera de PHP agotados en los archivos de registro, aumentar los valores de tiempo de espera, que se expresan en segundos:

```
php_value max_input_time 3600
php_value max_execution_time 3600
```

El módulo de Apache [mod_reqtimeout](https://httpd.apache.org/docs/current/mod/mod_reqtimeout.html) también podría impedir que se completen las subidas grandes. Si se usa este módulo y fallan las subidas de archivos grandes, desactivarlo en la configuración de Apache o aumentar los tiempos de espera `RequestReadTimeout` configurados.

Hay también otras opciones de configuración del servidor web que podrían impedir la subida de archivos más grandes. Consultar el manual del servidor web para saber cómo configurar correctamente esos valores:

#### Apache

- [LimitRequestBody](https://httpd.apache.org/docs/current/en/mod/core.html#limitrequestbody) (en Apache HTTP Server <=2.4.53 su valor predeterminado era ilimitado, pero ahora es de 1 GiB. El nuevo valor predeterminado limita a 1 GiB las subidas de los clientes que no fragmentan. Si esto es un problema en el entorno, anular el nuevo valor predeterminado estableciéndolo manualmente en `0` o en un valor similar al usado para los parámetros de PHP `upload_max_filesize / post_max_size / memory_limit` del entorno local).
- [SSLRenegBufferSize](https://httpd.apache.org/docs/current/mod/mod_ssl.html#sslrenegbuffersize)
- [Timeout](https://httpd.apache.org/docs/current/mod/core.html#timeout)

#### Apache con mod_fcgid

- [FcgidMaxRequestInMem](https://httpd.apache.org/mod_fcgid/mod/mod_fcgid.html#fcgidmaxrequestinmem)
- [FcgidMaxRequestLen](https://httpd.apache.org/mod_fcgid/mod/mod_fcgid.html#fcgidmaxrequestlen)

:::{note}
Si se usa Apache/2.4 con mod_fcgid, a fecha de febrero/marzo de 2016, `FcgidMaxRequestInMem` todavía debe aumentarse considerablemente respecto de su valor predeterminado para evitar fallos de segmentación al subir archivos grandes. No es un ajuste habitual, sino una solución provisional para el [error n.º 51747 de Apache con mod_fcgid](https://bz.apache.org/bugzilla/show_bug.cgi?id=51747).

Puede que deje de ser necesario establecer `FcgidMaxRequestInMem` muy por encima de lo normal una vez que se corrija el error n.º 51747.
:::

#### Apache con mod_proxy_fcgi

- [ProxyTimeout](https://httpd.apache.org/docs/current/mod/mod_proxy.html#proxytimeout)

#### nginx

- [client_max_body_size](https://nginx.org/en/docs/http/ngx_http_core_module.html#client_max_body_size)
- [fastcgi_read_timeout](https://nginx.org/en/docs/http/ngx_http_fastcgi_module.html#fastcgi_read_timeout) \[a menudo es la solución a los tiempos de espera 504 durante las transacciones `MOVE` que se producen incluso al usar fragmentación\]
- [client_body_temp_path](https://nginx.org/en/docs/http/ngx_http_core_module.html#client_body_temp_path)

:::{note}
Asegurarse de que `client_body_temp_path` apunta a una partición con espacio suficiente para el tamaño de los archivos subidos, y en la misma partición que `upload_tmp_dir` o `tempdirectory` (ver más abajo). Para un rendimiento óptimo, situarlos en un disco duro aparte dedicado al intercambio (swap) y al almacenamiento temporal.
:::

Si el sitio está detrás de un frontend nginx (por ejemplo, un balanceador de carga):

De forma predeterminada, las descargas se limitarán a 1 GB debido a `proxy_buffering` y `proxy_max_temp_file_size` en el frontend.

- Si se tiene acceso a la configuración del frontend, desactivar [proxy_buffering](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_buffering) o aumentar [proxy_max_temp_file_size](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_max_temp_file_size) desde su valor predeterminado de 1 GB.
- Si no se tiene acceso al frontend, establecer el encabezado [X-Accel-Buffering](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_buffering) con `add_header X-Accel-Buffering no;` en el servidor de backend.

### Configurar PHP

Si no se quiere usar el archivo `.htaccess` o `.user.ini` de Nextcloud, puede configurarse PHP en su lugar. Asegurarse de comentar en `.htaccess` todas las líneas relativas al tamaño de subida, si se añadió alguna.

Si Nextcloud se ejecuta en un sistema de 32 bits, debe comentarse cualquier directiva `open_basedir` del archivo `php.ini`.

Establecer los dos parámetros siguientes en `php.ini`, con los valores de tamaño de archivo deseados:

```
upload_max_filesize = 16G
post_max_size = 16G
```

Indicar a PHP qué directorio temporal debe usar:

```
upload_tmp_dir = /var/big_temp_file/
```

El **almacenamiento en búfer de la salida** debe estar desactivado en `.htaccess`, `.user.ini` o `php.ini`; de lo contrario, PHP devolverá errores relacionados con la memoria:

- `output_buffering = 0`

### Configurar Nextcloud

Como alternativa al `upload_tmp_dir` de PHP (p. ej., si no se tiene acceso al `php.ini`), también puede configurarse una ubicación temporal para los archivos subidos mediante el ajuste `tempdirectory` del `config.php` (consultar {nc-doc}`admin_manual/configuration_server/config_sample_php_parameters`).

Si se ha configurado el ajuste `session_lifetime` en el archivo `config.php` (consultar {nc-doc}`admin_manual/configuration_server/config_sample_php_parameters`), asegurarse de que no es demasiado bajo. Este ajuste debe configurarse al menos con el tiempo (en segundos) que tardará la subida más larga. En caso de duda, eliminarlo por completo de la configuración para restablecer el valor predeterminado que figura en `config.sample.php`.

(nc-files_configure_max_chunk_size)=
### Ajustar el tamaño de fragmento en el lado de Nextcloud

Para mejorar el rendimiento de las subidas en entornos con un ancho de banda de subida alto, puede ajustarse el tamaño de fragmento de subida del servidor:

```
sudo -E -u www-data php occ config:system:set --type int --value 20971520 files.chunked_upload.max_size
```

Indicar un valor en bytes (en este ejemplo, 20 MB). Establecer `--value 0` para no usar fragmentación en absoluto.

El valor predeterminado es `104857600` (100 MiB).

### Subida de archivos grandes en almacenamiento de objetos

Las [subidas de archivos por fragmentos](https://docs.nextcloud.com/server/latest/developer_manual/client_apis/WebDAV/chunking.html) consumen más espacio en la carpeta temporal al procesar esas subidas en almacenamiento de objetos, ya que los fragmentos individuales se descargan del almacenamiento y se ensamblan en el archivo real en el directorio temporal de los servidores Nextcloud. Se recomienda aumentar en consecuencia el tamaño del directorio temporal y asegurarse también de que los tiempos de espera de las peticiones sean lo bastante altos para PHP, los servidores web y cualquier balanceador de carga implicado.

:::{tip}
En las versiones más recientes de Nextcloud Server, al subir a S3 en modo de *almacenamiento principal*, se usa *MultipartUpload* de S3. Esto permite transmitir los fragmentos de la subida directamente a S3, de modo que la petición MOVE final ya no necesita ensamblar el archivo final en el servidor Nextcloud. Para ello, `memcache.distributed` debe estar configurado para usar Redis (o Memcached); de lo contrario, se recurre al comportamiento anterior, que consume espacio en el servidor Nextcloud para ensamblar el archivo (como se describe más arriba).
:::

### Compartición federada en la nube

Si se usa la {nc-doc}`compartición federada en la nube <admin_manual/configuration_files/federated_cloud_sharing_configuration>` y se quieren compartir archivos grandes, pueden aumentarse los valores de tiempo de espera de las peticiones a los servidores federados. Para ello, puede establecerse `davstorage.request_timeout` en el `config.php`. El valor predeterminado es de 30 segundos.
````
