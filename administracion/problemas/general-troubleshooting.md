---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Soporte, informe de errores y fallos frecuentes: registros, PHP, servidor web, WebDAV, descubrimiento de servicios, directorio de datos y cuotas."
---
# Solución general de problemas

## Resumen

Esta página reúne los canales de soporte de la comunidad, cómo informar de errores y la solución de los problemas frecuentes del servidor: registros, PHP, servidor web, WebDAV, descubrimiento de servicios, uso compartido, directorio de datos, cuotas y archivos cifrados, además de la política de uso justo. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/issues/general_troubleshooting.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Si hay problemas al instalar, configurar o mantener Nextcloud, consultar nuestros canales de soporte de la comunidad:

- [Los foros de {vendor}`Nextcloud`][the Nextcloud Forums]: los foros de {vendor}`Nextcloud` tienen una [página de preguntas frecuentes][FAQ page] en la que cada tema corresponde a errores típicos o a problemas frecuentes

Conviene entender que todos estos canales están formados esencialmente por usuarios como uno mismo que se ayudan entre sí. Considerar ayudar a otros cuando sea posible, para devolver la ayuda recibida. ¡Es la única manera de mantener sana y sostenible una comunidad como la de {vendor}`Nextcloud`!

Si se usa Nextcloud en una empresa o en otro despliegue a gran escala, tener en cuenta que Nextcloud GmbH ofrece opciones de soporte comercial.

### Errores

Si se cree haber encontrado un error en Nextcloud:

- Buscar una solución (ver las opciones anteriores)
- Comprobar de nuevo la configuración

Si no se encuentra una solución, usar nuestro [centro de incidencias][bugtracker]. Puede generarse un informe de configuración con el {nc-ref}`comando occ config <config_commands_label>`, con las contraseñas ocultadas automáticamente.

### Solución general de problemas

Consultar los {nc-doc}`admin_manual/installation/system_requirements` de Nextcloud, especialmente las versiones de navegador compatibles.

Ante avisos sobre `code integrity`, consultar {nc-doc}`admin_manual/issues/code_signing`.

#### Desactivar las apps de terceros / no incluidas

Es posible que las apps de terceros / no incluidas causen problemas diversos. Desactivar siempre las apps de terceros antes de las actualizaciones y para la solución de problemas. Consultar {nc-ref}`apps_commands_label` para saber cómo desactivar una app desde la línea de comandos.

#### Errores internos del servidor

Un error interno del servidor, a veces llamado «error 500», indica que el servidor web encontró una condición inesperada que le impidió atender la solicitud.

Esta respuesta de error es una respuesta genérica «comodín». Para averiguar el origen del error hay que revisar el registro de Nextcloud (ubicado de forma predeterminada en *data/nextcloud.log*) y, posiblemente, el registro de errores del servidor web (según dónde se produzca el fallo).

:::{tip}
Siempre que sea posible, Nextcloud incluirá el «ID de la solicitud» en el error. Este ID de solicitud puede buscarse en el archivo de registro de Nextcloud para encontrar las entradas asociadas a la transacción fallida.
:::

#### Archivos de registro de Nextcloud

El archivo de registro de Nextcloud se encuentra de forma predeterminada en el directorio de datos, p. ej., `data/nextcloud.log`. Si la interfaz web sigue siendo accesible, también está disponible en *Configuraciones de administración->Registros*.

:::{tip}
Al pedir ayuda, por lo general se necesita la entrada de registro completa y sin procesar.
:::

% note: En una instalación estándar de Nextcloud el nivel de registro se establece en `2`. Esto se
% conoce como el nivel `WARN`. Es suficiente para detectar los problemas del día a día
% (avisos, errores y errores fatales).

En algunas situaciones puede ser necesario ajustar el nivel de registro en el archivo `config.php`. Consultar {nc-doc}`admin_manual/configuration_server/logging_configuration` para obtener más información sobre estos niveles de registro.

Parte del registro, por ejemplo el registro de la consola de JavaScript, necesita que la depuración esté activada. Editar {file}`config/config.php` y cambiar `'debug' => false,` por `'debug' => true,`. Asegurarse de volver a cambiarlo al terminar.

Para los problemas de JavaScript también hay que ver la consola de JavaScript. Todos los navegadores principales tienen herramientas para desarrolladores con las que ver la consola, y normalmente se accede a ellas pulsando F12.

(nc-label-phpinfo)=
#### Versión e información de PHP

Hay que conocer la versión y la configuración de PHP que se usan en el servidor Nextcloud. No tienen por qué ser la misma versión y configuración que se obtienen desde la línea de comandos. La forma más sencilla de reunir esta información es usar lo que comúnmente se conoce como `phpinfo()`.

La forma más precisa (y la más sencilla) de acceder a `phpinfo` es consultarlo desde el propio Nextcloud. Por supuesto, esto requiere que Nextcloud funcione lo suficiente como para poder iniciar sesión como administrador y acceder al menú **Configuraciones de administración -> Sistema**. Si es así, puede activarse la exposición de los datos de `phpinfo` mediante `occ`:

`./occ config:app:set --value=yes serverinfo phpinfo`

A partir de entonces, en la interfaz web se verá un nuevo botón con la etiqueta **Mostrar phpinfo** en **Configuraciones de administración -> Sistema**. Al hacer clic en él se muestra prácticamente todo lo que se pueda querer saber sobre el entorno de PHP.

Si no es posible acceder a la interfaz web de Nextcloud, puede crearse un archivo de texto plano llamado **phpinfo.php** y colocarlo en la raíz web, por ejemplo `/var/www/html/phpinfo.php`. (La raíz web puede estar en otra ubicación; la documentación de la distribución de Linux indica dónde). Este archivo contiene solo esta línea:

```
<?php phpinfo(); ?>
```

Abrir este archivo en un navegador web apuntando el navegador a `localhost/phpinfo.php`.

La versión de PHP aparece en la parte superior, y el resto de la página contiene abundante información del sistema, como los módulos activos, los archivos `.ini` activos y mucho más. Al terminar de revisar la información hay que eliminar `phpinfo.php` o moverlo fuera del directorio web, porque exponer datos tan sensibles es un riesgo de seguridad.

#### Depurar problemas de sincronización

:::{warning}
El directorio de datos del servidor es exclusivo de Nextcloud y no debe modificarse manualmente.
:::

No respetar esto puede provocar comportamientos no deseados como:

- Problemas con los clientes de sincronización
- Cambios no detectados debido a la caché en la base de datos

Si hace falta subir archivos directamente desde el mismo servidor, usar un cliente WebDAV de línea de comandos como `cadaver` para subir los archivos a la interfaz WebDAV en:

`https://example.com/nextcloud/remote.php/dav`

#### Problemas y mensajes de error comunes

Algunos problemas y mensajes de error comunes que aparecen en los archivos de registro, como se describe arriba:

- `SQLSTATE[HY000] [1040] Too many connections` -> Hay que aumentar el límite de conexiones de la base de datos; consultar el manual de la base de datos para obtener más información.
- `SQLSTATE[HY000]: General error: 5 database is locked` -> Se está usando `SQLite`, que no puede gestionar muchas solicitudes en paralelo. Considerar la conversión a otra base de datos, como se describe en {nc-doc}`admin_manual/configuration_database/db_conversion`.
- `SQLSTATE[HY000]: General error: 2006 MySQL server has gone away` -> Consultar {nc-ref}`db-troubleshooting-label` para obtener más información.
- `SQLSTATE[HY000] [2002] No such file or directory` -> Hay un problema al acceder al archivo de la base de datos SQLite en el directorio de datos (`data/nextcloud.db`). Comprobar los permisos de esta carpeta o archivo, o si existe siquiera. Si se usa MySQL, iniciar la base de datos.
- `Connection closed / Operation cancelled` -> Puede deberse a una configuración incorrecta de `KeepAlive` en la configuración de Apache. Asegurarse de que `KeepAlive` esté establecido en `On` y probar también a aumentar los límites de `KeepAliveTimeout` y `MaxKeepAliveRequests`.
- `No basic authentication headers were found` -> Este error aparece en el archivo `data/nextcloud.log`. Algunos módulos de Apache, como `mod_fastcgi`, `mod_fcgid` o `mod_proxy_fcgi`, no pasan a PHP las cabeceras de autenticación necesarias, por lo que falla el inicio de sesión en Nextcloud mediante clientes WebDAV, CalDAV y CardDAV.

### Solución de problemas del servidor web y de PHP

#### Archivos de registro

Cuando hay problemas, el primer paso es revisar los archivos de registro de PHP, del servidor web y del propio Nextcloud.

:::{note}
En lo que sigue se suponen las rutas a los archivos de registro de una instalación predeterminada de Debian que ejecuta Apache2 con mod_php. En otros servidores web, distribuciones de Linux o sistemas operativos pueden ser distintas.
:::

- El archivo de registro de Apache2 se encuentra en `/var/log/apache2/error.log`.
- El archivo de registro de PHP puede configurarse en `/etc/php/8.3/apache2/php.ini`. Hay que establecer la directiva `log_errors` en `On` y elegir en la directiva `error_log` la ruta en la que guardar el archivo de registro. Después de esos cambios hay que reiniciar el servidor web.
- El archivo de registro de Nextcloud se encuentra en el directorio de datos, en `/var/www/nextcloud/data/nextcloud.log`.

#### Servidor web y módulos de PHP

:::{note}
Lighttpd no está soportado con Nextcloud, y algunas funciones de Nextcloud pueden no funcionar en absoluto con Lighttpd.
:::

Hay algunos módulos del servidor web o de PHP que se sabe que causan diversos problemas, como subidas o descargas rotas. A continuación se muestra un resumen provisional de estos módulos:

1. Apache

- mod_pagespeed
- mod_evasive
- mod_security
- mod_reqtimeout
- mod_deflate
- mod_spdy
- mod_dav
- mod_xsendfile / X-Sendfile (causa descargas rotas si no se configura correctamente)

2. NginX

- ngx_pagespeed
- HttpDavModule
- X-Sendfile (causa descargas rotas si no se configura correctamente)

3. PHP

- Tideways
- eAccelerator

(nc-trouble-webdav-label)=
### Solución de problemas de WebDAV

Nextcloud usa SabreDAV, y la documentación de SabreDAV es completa y útil.

% note: Lighttpd no está soportado en Nextcloud, y el WebDAV de Lighttpd no
% funciona con Nextcloud.

Véase:

- [Preguntas frecuentes de SabreDAV](http://sabre.io/dav/faq/)
- [Servidores web](http://sabre.io/dav/webservers) (indica que lighttpd no es recomendable)
- [Trabajar con archivos grandes](http://sabre.io/dav/large-files/) (muestra un error de PHP en versiones antiguas de SabreDAV e información sobre problemas con mod_security)
- [Archivos de 0 bytes](http://sabre.io/dav/0bytes) (motivos de los archivos vacíos en el servidor)
- [Clientes](http://sabre.io/dav/clients/) (una lista completa de clientes WebDAV y de los posibles problemas de cada uno)
- [Finder, el cliente WebDAV integrado de OS X](http://sabre.io/dav/clients/finder/) (describe problemas de Finder con distintos servidores web)

También hay un hilo de preguntas frecuentes bien mantenido en los [foros de ownCloud](https://central.owncloud.org/t/how-to-fix-caldav-carddav-webdav-problems/852), que contiene diversa información adicional sobre problemas de WebDAV.

(nc-service-discovery-label)=
### Descubrimiento de servicios

Algunos clientes, sobre todo en iOS/macOS, tienen problemas para encontrar la URL de sincronización correcta, incluso cuando se configuran explícitamente para usarla.

Si se quieren usar junto con Nextcloud clientes CalDAV o CardDAV u otros clientes que requieren descubrimiento de servicios, es importante tener una configuración que funcione correctamente para las siguientes URL:

`https://example.com/.well-known/carddav`\
`https://example.com/.well-known/caldav`

Estas deben redirigir a los clientes a los endpoints correctos. Si Nextcloud se ejecuta en el `DocumentRoot` del servidor web, la URL correcta es `https://example.com/remote.php/dav` para CardDAV y CalDAV, y si se ejecuta en una subcarpeta como `nextcloud`, la URL correcta es `https://example.com/nextcloud/remote.php/dav`.

:::{note}
En los sistemas Debian/Ubuntu, el `DocumentRoot` de Apache es `/var/www/html` de forma predeterminada. En otras distribuciones esta ruta puede ser distinta. Ajustar las rutas de los ejemplos siguientes en consecuencia.
:::

Para el primer caso, el archivo {file}`.htaccess` que se distribuye con Nextcloud debería hacer este trabajo cuando se ejecuta Apache. Hay que asegurarse de que el servidor web use este archivo. Además, se necesita el módulo mod_rewrite de Apache instalado y `AllowOverride All` establecido en {file}`apache2.conf` o en el archivo del vHost para procesar estas redirecciones. Si se ejecuta Nginx, consultar {nc-doc}`admin_manual/installation/nginx`.

Para el segundo caso, hay que añadir lo siguiente a {file}`/etc/apache2/apache2.conf`, sustituyendo `/var/www/html` por el `DocumentRoot` real si es distinto:

```
<Directory /var/www/html>
    AllowOverride FileInfo
</Directory>
```

`AllowOverride FileInfo` basta para las directivas de reescritura que usa el descubrimiento de servicios. Si ya se tiene `AllowOverride All` establecido para este directorio, no hace falta ningún cambio. A continuación, crear o editar el archivo {file}`.htaccess` del `DocumentRoot` del servidor web y añadir las siguientes líneas:

```
<IfModule mod_rewrite.c>
  RewriteEngine on
  RewriteRule ^\.well-known/carddav /nextcloud/remote.php/dav [R=301,L]
  RewriteRule ^\.well-known/caldav /nextcloud/remote.php/dav [R=301,L]
  RewriteRule ^\.well-known/webfinger /nextcloud/index.php/.well-known/webfinger [R=301,L]
  RewriteRule ^\.well-known/nodeinfo /nextcloud/index.php/.well-known/nodeinfo [R=301,L]
</IfModule>
```

Asegurarse de cambiar /nextcloud por la subcarpeta real en la que se ejecuta la instancia de Nextcloud.

:::{note}
Si las directivas anteriores se ponen directamente en un archivo de configuración de Apache (normalmente dentro de `/etc/apache2/`) en lugar de en `.htaccess`, hay que anteponer una barra `/` al primer argumento de cada opción `RewriteRule`, por ejemplo `^/\.well-known/carddav`. Esto se debe a que Apache normaliza las rutas para su uso en los archivos `.htaccess` eliminando cualquier número de barras iniciales, pero no lo hace para su uso en sus archivos de configuración principales.
:::

Si se ejecuta NGINX, asegurarse de que `location = /.well-known/carddav {` y `location = /.well-known/caldav {` estén configurados correctamente como se describe en {nc-doc}`admin_manual/installation/nginx`, y adaptarlos para usar una subcarpeta si es necesario.

Ahora cambiar la URL en los ajustes del cliente para usar solo:

`https://example.com`

en lugar de, p. ej.,

`https://example.com/nextcloud/remote.php/dav/principals/username`.

Hay también varias técnicas para remediar esto, que se describen extensamente en el [sitio web de Sabre DAV](http://sabre.io/dav/service-discovery/).

### Solución de problemas al compartir

#### Los ID de nube federada de los usuarios no se actualizan tras un cambio de nombre de dominio

1. ejecutar la consulta a la base de datos

`DELETE FROM oc_cards_properties WHERE name = 'CLOUD' AND addressbookid = (select id from oc_addressbooks where principaluri = 'principals/system/system' AND uri = 'system');`

2. ejecutar los comandos occ

`occ dav:sync-system-addressbook`\
`occ federation:sync-addressbooks`

### Solución de problemas de contactos y calendario

:::{tip}
Consultar también el artículo de solución de problemas de la sección de groupware: {nc-ref}`troubleshooting_groupware`.
:::

(nc-troubleshooting_data_directory)=
### Solución de problemas del directorio de datos

#### Mover el directorio de datos / cambiar la ruta `datadirectory`

Para el almacenamiento local, Nextcloud identifica el almacenamiento por su ruta absoluta en el disco. Lo ideal es que la ubicación del directorio de datos no cambie después del despliegue. Si se trata de una instalación nueva, considerar reinstalar con la ubicación de directorio preferida antes de pasar a producción.

:::{danger}
Si hay que cambiar la ruta `datadirectory` (a menos que la transición se gestione con cuidado), Nextcloud tratará su contenido como «almacenamiento nuevo». Esto puede provocar archivos duplicados o huérfanos, la pérdida de metadatos de los archivos y la pérdida de los enlaces compartidos anteriormente.
:::

Para mover el directorio de datos de forma segura, las acciones recomendadas son:

1. Asegurarse de que no se esté ejecutando ningún trabajo cron y, si se usa el cron del sistema, de que la entrada de crontab de Nextcloud esté desactivada.

2. Detener los servidores web/de aplicaciones.

3. Mover `/data` a la nueva ubicación (asegurarse de mover también los archivos ocultos o que empiezan por punto, como `.ncdata`).

4. Crear un enlace simbólico desde la ubicación original a la nueva ubicación.

5. Asegurarse de que los permisos sigan siendo correctos (también en las carpetas superiores).

6. Reiniciar los servidores web/de aplicaciones.

7. Volver a activar la entrada de crontab del sistema de Nextcloud (si corresponde).

:::{note}
Puede ser necesario configurar el servidor web para que admita enlaces simbólicos.
:::

También es posible mover el directorio de datos sin usar enlaces simbólicos, pero esto requiere modificar manualmente la tabla interna `oc_storages` de la base de datos:

1. Asegurarse de que no se esté ejecutando ningún trabajo cron y, si se usa el cron del sistema, de que la entrada de crontab de Nextcloud esté desactivada.

2. Detener los servidores web/de aplicaciones.

3. Mover `/data` a la nueva ubicación (asegurarse de mover también los archivos ocultos o que empiezan por punto, como `.ncdata`).

4. Actualizar el valor de `datadirectory` en `config.php`.

5. Editar la base de datos: en la tabla `oc_storages`, actualizar la parte de la ruta del campo `id` de la entrada que empieza por `local::/old-data-dir/` (p. ej., cambiar `local::/old-data-dir/` por `local::/new-data-dir/`).

6. Asegurarse de que los permisos sigan siendo correctos (también en las carpetas superiores).

7. Reiniciar los servidores web/de aplicaciones.

8. Volver a activar la entrada de crontab del sistema de Nextcloud (si corresponde).

:::{warning}
Este método no está soportado y se corre el riesgo de dañar la base de datos. Asegurarse siempre de tener copias de seguridad actualizadas (incluida la base de datos) y un proceso de restauración que funcione (y esté probado) **antes** de intentarlo.
:::

### Solución de problemas de cuota o de tamaño

A veces puede ocurrir que el espacio usado que se muestra en la interfaz web o con `occ user:info $userId` no coincida con los datos reales almacenados en el directorio `data/$userId/files` del usuario.

:::{note}
Los metadatos, las versiones, la papelera y las claves de cifrado no se cuentan en el espacio usado anterior. Consultar la [documentación sobre la cuota](https://docs.nextcloud.com/server/latest/user_manual/en/files/quota.html) para conocer los detalles.
:::

Ejecutar el siguiente comando puede ayudar a corregir los tamaños y la cuota de un usuario concreto:

```
sudo -E -u www-data php occ files:scan -vvv <user-id>
```

Si **el cifrado se activó antes en la instancia y se desactivó después**, es probable que algunos valores de tamaño de la base de datos no se restablecieran correctamente al descifrar. Pueden restablecerse ejecutando la siguiente consulta SQL después de **hacer una copia de seguridad de la base de datos**:

```sql
UPDATE oc_filecache SET unencrypted_size=0 WHERE encrypted=0;
```

### Solución de problemas de archivos cifrados

:::{tip}
Consultar también la sección de solución de problemas del capítulo de cifrado: {nc-doc}`admin_manual/configuration_files/encryption_configuration`.
:::

### Política de uso justo

Nextcloud es de código abierto y puede alojarse gratis en un servidor propio o en un proveedor.

{vendor}`Nextcloud` recomienda usar {vendor}`Nextcloud Enterprise` para desplegar instancias de más de 500 usuarios. Con ese tamaño, problemas como un servidor averiado o una fuga de datos se vuelven muy graves.

Si hay un problema con el servidor, 500 personas no pueden trabajar. Una fuga de datos pondría en riesgo los datos de muchos usuarios. En resumen, el servidor debe considerarse crítico. Creemos que tanto quien administra como sus usuarios tendrían una mejor experiencia con {vendor}`Nextcloud Enterprise`.

{vendor}`Nextcloud Enterprise` viene preconfigurado y optimizado para las necesidades de las organizaciones profesionales, más que para los usuarios domésticos. Incluye soporte, ventajas de seguridad y de escalado, experiencia en cumplimiento normativo y acceso a nuestro conocimiento sobre cómo ejecutar con éxito un {vendor}`Nextcloud`, para lograr la mejor experiencia posible para usuarios y administradores. Esto también reduce la carga que los problemas exclusivos de los grandes despliegues suponen para nuestro foro de usuarios domésticos <http://help.nextcloud.com>.

{vendor}`Nextcloud` proporciona algunos componentes de infraestructura necesarios para que los servidores Nextcloud funcionen de forma fiable. Esto incluye las notificaciones, nuestra tienda de aplicaciones y más. Para garantizar que estos recursos no se sobrecarguen por administradores que ejecutan Nextcloud para miles de usuarios sin aportar a cambio recursos económicos a {vendor}`Nextcloud`, estos componentes están limitados y no funcionarán para más de 500 usuarios.

Creemos que todas las organizaciones que ejecutan Nextcloud para cientos de usuarios deberían contar con soporte oficial. Sabemos que puede haber restricciones económicas para las organizaciones sin ánimo de lucro y, como queremos que todo el mundo tenga la oportunidad de sacar el máximo partido de Nextcloud, tenemos ofertas especiales para ONG, escuelas pequeñas y otras organizaciones sin ánimo de lucro. Para hablar con nosotros sobre lo que es posible, usar el [formulario de contacto de nuestro sitio](https://nextcloud.com/contact/) o pedir al administrador del sistema que se ponga en contacto.

### Otros problemas

Algunos servicios como *Cloudflare* pueden causar problemas al minimizar el JavaScript y cargarlo solo cuando se necesita. Ante problemas como un botón de inicio de sesión que no funciona o al crear usuarios nuevos, asegurarse de desactivar primero esos servicios.

[the Nextcloud Forums]: https://help.nextcloud.com
[FAQ page]: https://help.nextcloud.com/t/how-to-faq-wiki
[bugtracker]: https://docs.nextcloud.com/server/latest/developer_manual/prologue/bugtracker/index.html
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
