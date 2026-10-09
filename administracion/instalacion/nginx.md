---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Servir la instancia con NGINX y PHP-FPM: ajustes de la configuración, webroot o subdirectorio, y soluciones a errores frecuentes."
---
# Configuración de NGINX

## Resumen

Esta página explica cómo servir la instancia con NGINX respaldado por PHP-FPM: qué ajustar en la configuración, en qué se diferencian la instalación en el webroot y en un subdirectorio, y cómo resolver errores frecuentes como el «502 Bad Gateway». Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/installation/nginx.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

Esta página explica cómo ejecutar un servidor Nextcloud con NGINX respaldado por PHP-FPM, que también es una configuración con soporte oficial.

- Hay que insertar el siguiente código en **el archivo de configuración de Nginx**. Elegir el ejemplo adecuado según se despliegue {nc-ref}`nginx_webroot_example` (es decir, {code}`https://cloud.example.com/`) o {nc-ref}`nginx_subdir_example` (es decir, {code}`https://cloud.example.com/nextcloud`).
- Ajustar la directiva server de {code}`upstream php-handler` para que coincida con el listener de FPM configurado en la instalación de PHP (una configuración incorrecta aquí provocará un {code}`502 Bad Gateway`; ver {nc-ref}`nginx_php_handler_tips` para más detalles)
- Ajustar las directivas {code}`server_name` existentes en *ambas* secciones {code}`server` al nombre de host real
- Ajustar {code}`root` al webroot de la instalación de Nextcloud
- Ajustar las directivas {code}`ssl_certificate` y {code}`ssl_certificate_key` a las rutas reales del certificado firmado y de la clave privada. Asegurarse de que el proceso del servidor nginx puede leer los certificados SSL (ver la [documentación del módulo HTTPS SSL de nginx](https://wiki.nginx.org/HttpSslModule)).
- Si se usa Let's Encrypt como certificado TLS y nginx como servidor web, establecer *ssl_stapling* y *ssl_stapling_verify* en *off* en la configuración principal de nginx (ver [entrada del blog de Let's Encrypt](https://letsencrypt.org/2024/12/05/ending-ocsp)).
- Tener cuidado con los saltos de línea al copiar los ejemplos, ya que las líneas largas pueden cortarse para mostrarlas en la página y dar lugar a archivos de configuración no válidos.
- Algunos entornos pueden necesitar `cgi.fix_pathinfo` con el valor `1` en su `php.ini`.

(nc-nginx_webroot_example)=
### Nextcloud en el webroot de NGINX

La siguiente configuración debe usarse cuando Nextcloud está en el webroot de la instalación de nginx. En este ejemplo es `/var/www/nextcloud` y se accede mediante `http(s)://cloud.example.com/`

La configuración completa está en el archivo {file}`nginx-root.conf.sample` de la documentación original.

(nc-nginx_subdir_example)=
### Nextcloud en un subdirectorio del webroot de NGINX

La siguiente configuración debe usarse cuando Nextcloud está dentro de un subdirectorio del webroot de la instalación de nginx. En este ejemplo, los archivos de Nextcloud están en `/var/www/nextcloud` y se accede a la instancia de Nextcloud mediante `http(s)://cloud.example.com/nextcloud/`. La configuración se diferencia de la configuración «Nextcloud en el webroot» anterior en lo siguiente:

- Todas las peticiones a `/nextcloud` se encapsulan en un único bloque `location`, concretamente `location ^~ /nextcloud`.
- La cadena `/nextcloud` se antepone a todas las rutas de prefijo.
- La raíz del dominio se asigna a `/var/www` en lugar de a `/var/www/nextcloud`, de modo que la URI `/nextcloud` se asigna al directorio del servidor `/var/www/nextcloud`.
- Los bloques que gestionan las peticiones a rutas fuera de `/nextcloud` (es decir, `/robots.txt` y `/.well-known`) se sacan del bloque `location ^~ /nextcloud`.
- El bloque que gestiona */.well-known* no necesita una excepción de expresión regular, ya que la regla que impide a los usuarios acceder a carpetas ocultas en la raíz de la instalación de Nextcloud ya no coincide con esa ruta.

La configuración completa está en el archivo {file}`nginx-subdir.conf.sample` de la documentación original.

### Trucos y consejos

(nc-nginx_php_handler_tips)=
#### Configuración de PHP-Handler / Cómo evitar «502 Bad Gateway»

La línea {code}`server` dentro del {code}`upstream php-handler` anterior debe ajustarse para reflejar la configuración local de PHP FPM. Debe coincidir con lo que esté configurado en la directiva {code}`listen` del pool de PHP FPM que se vaya a usar para NC.

Muchas distribuciones Linux definen un listener para un pool de PHP-FPM predeterminado llamado {code}`www` en un archivo llamado {code}`www.conf`, ubicado en algún lugar como {code}`/etc/php/8.1/pool.d`.

Buscar la línea que tenga un valor parecido a:

{code}`listen = /var/run/php/php-fpm.sock`
o
{code}`listen = 127.0.0.1:9000`

Si PHP FPM se va a ejecutar en el mismo host que NGINX (si hay dudas, probablemente sea una suposición segura), se recomienda usar el socket UNIX (es decir, {code}`/var/run/php/php-fpm.sock`) en lugar de TCP ({code}`127.0.0.1:9000`) para obtener el máximo rendimiento (aunque cualquiera de los dos funciona siempre que las configuraciones de NGINX y de PHP FPM coincidan).

Después de decidir cómo se prefiere conectar NGINX con PHP FPM (y, si es necesario, de actualizar la configuración local de PHP FPM y reiniciar FPM), configurar el {code}`server` del {code}`upstream php-handler` de la configuración de NGINX según esa preferencia (Nota: si se usan sockets UNIX, anteponer {code}`unix:` en la configuración de NGINX, pero *no* en el {code}`www.conf` de PHP FPM).

#### Suprimir mensajes del registro

Si en el archivo de registro aparecen mensajes sin sentido, por ejemplo `client denied by server configuration: /var/www/data/htaccesstest.txt`, añadir esta sección a la configuración de nginx para suprimirlos:

```nginx
location = /data/htaccesstest.txt {
  allow all;
  log_not_found off;
  access_log off;
}
```

#### Archivos JavaScript (.js) o CSS (.css) que no se sirven correctamente

Un problema habitual de las configuraciones personalizadas de nginx es que los archivos JavaScript (.js) o CSS (.css) no se sirven correctamente, lo que provoca un error 404 (archivo no encontrado) en esos archivos y una interfaz web rota.

Puede deberse a que el bloque:

```nginx
location ~* \.(?:css|js)$ {
```

mostrado arriba no esté ubicado **debajo** del bloque:

```nginx
location ~ \.php(?:$|\/) {
```

Otras configuraciones personalizadas, como almacenar en caché los archivos JavaScript (.js) o CSS (.css) mediante gzip, también podrían causar este tipo de problemas.

Otra causa de este problema podría ser no incluir correctamente los mimetypes en el bloque http, como se muestra [aquí.](https://www.nginx.com/resources/wiki/start/topics/examples/full/)

#### Falla la subida de archivos de más de 10 MiB

Si se configura nginx (de forma global) para bloquear todas las peticiones a archivos que empiezan por punto (ocultos), puede que no sea posible subir archivos de más de 10 MiB desde la página web, debido a que Nextcloud exige subir el archivo a una URL que termina en `/.file`.

Puede ser necesario cambiar:

```nginx
location ~ /\. {
```

por lo siguiente para volver a permitir la subida de archivos:

```nginx
location ~ /\.(?!file).* {
```

Ver [issue #8802 en nextcloud/server](https://github.com/nextcloud/server/issues/8802) para más información.

Además de los anteriores, hay otros parámetros relevantes para subir archivos grandes (ver {nc-ref}`uploading_big_files`).

#### Bucle de inicio de sesión sin ninguna pista en access.log, error.log ni nextcloud.log

Si después de una instalación nueva (Centos 7 con nginx) hay problemas con el primer inicio de sesión, lo primero es revisar estos archivos:

```bash
tail /var/www/nextcloud/data/nextcloud.log
tail /var/log/nginx/access.log
tail /var/log/nginx/error.log
```

Si en el registro de acceso solo se ven algunas peticiones correctas, pero no se produce el inicio de sesión, revisar los permisos de acceso de los directorios de sesión de php y de wsdlcache. Comprobar los permisos y cambiarlos si es necesario:

```bash
chown nginx:nginx /var/lib/php/session/
chown root:nginx /var/lib/php/wsdlcache/
chown root:nginx /var/lib/php/opcache/
```
````
