---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Advertencias que muestra el comprobador de configuración de Nextcloud en la página de administración y qué hacer con cada una."
---
# Advertencias en la página de administración

## Resumen

Esta página recoge, para quienes administran el servidor, algunas de las advertencias que el comprobador de configuración integrado de Nextcloud muestra en la página de administración y qué hacer con cada una.

````{upstream} admin_manual/configuration_server/security_setup_warnings.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El servidor Nextcloud tiene un comprobador de configuración integrado que informa de sus hallazgos en la parte superior de la página de administración. Estas son algunas de las advertencias que pueden aparecer y qué hacer con ellas.

Puede usarse el [escáner de seguridad de {vendor}`Nextcloud`](https://scan.nextcloud.com) para ver si el sistema está actualizado y bien protegido. {vendor}`Nextcloud` ha ejecutado este análisis sobre direcciones IP públicas en el pasado para intentar contactar con [sistemas extremadamente desactualizados](https://nextcloud.com/blog/nextcloud-releases-security-scanner-to-help-protect-private-clouds/) y podría volver a hacerlo en el futuro. ¡Proteger la privacidad y mantener el servidor actualizado! La privacidad significa poco sin seguridad.

### Advertencias de caché

«No memory cache has been configured. To enhance your performance please configure a memcache if available.» Nextcloud admite varias extensiones de caché de PHP:

- APCu (versión mínima requerida de la extensión PHP: 4.0.6)
- Memcached
- Redis (versión mínima requerida de la extensión PHP: 2.2.6)

Esta advertencia aparece si no hay ninguna caché instalada y activada, o si la caché no tiene instalada la versión mínima requerida; las versiones anteriores se desactivan por problemas de rendimiento.

Si aparece «*{Cache}* below version *{Version}* is installed. for stability and performance reasons we recommend to update to a newer *{Cache}* version», hay que actualizarla o, si no se usa, eliminarla.

No es obligatorio usar ninguna caché, pero las cachés mejoran el rendimiento del servidor. Consultar {nc-doc}`admin_manual/configuration_server/caching_configuration`.

### El bloqueo transaccional de archivos está desactivado

«Transactional file locking is disabled, this might lead to issues with race conditions.»

Consultar {nc-doc}`admin_manual/configuration_files/files_locking_transactional` para saber cómo configurar correctamente el entorno para el bloqueo transaccional de archivos.

### Se está accediendo a este sitio mediante HTTP

«You are accessing this site via HTTP. We strongly suggest you configure your server to require using HTTPS instead.» Esta advertencia debe tomarse en serio; usar HTTPS es una medida de seguridad fundamental. Hay que configurar el servidor web para que lo admita, y después hay algunos ajustes que activar en la sección {guilabel}`Seguridad` de la página de administración de Nextcloud. Las páginas siguientes describen cómo activar HTTPS en los servidores web Apache y Nginx.

{nc-ref}`Activar SSL <enabling_ssl_label>` (en Apache)

{nc-ref}`Usar HTTPS <use_https_label>`

{nc-doc}`admin_manual/installation/nginx`

### La prueba con getenv("PATH") solo devuelve una respuesta vacía

Algunos entornos no pasan una variable PATH válida a Nextcloud. La sección {nc-ref}`Configuración de PHP-FPM <php_fpm_tips_label>` ofrece la información sobre cómo configurar el entorno.

### La cabecera HTTP «Strict-Transport-Security» no está configurada

«The "Strict-Transport-Security" HTTP header is not configured to least "15552000" seconds. For enhanced security we recommend enabling HSTS as described in our security tips.»

La cabecera HSTS debe configurarse en el servidor web siguiendo la documentación de {nc-ref}`Activar HTTP Strict Transport Security <enable-hsts-label>`

Puede comprobarse si la cabecera aparece en las solicitudes con el inspector del navegador o con una herramienta como cURL: `curl --head https://cloud.domain.tld`.

### PHP no puede leer /dev/urandom

«/dev/urandom is not readable by PHP which is highly discouraged for security reasons. Further information can be found in our documentation.»

Este es otro mensaje que debe tomarse en serio. Consultar la documentación de {nc-ref}`Dar a PHP acceso de lectura a /dev/urandom <dev-urandom-label>`.

### El servidor web aún no está configurado correctamente para permitir la sincronización de archivos

«Your web server is not yet set up properly to allow file synchronization because the WebDAV interface seems to be broken.»

En los foros de la comunidad de ownCloud se mantiene una [FAQ](https://forum.owncloud.org/viewtopic.php?f=17&t=7536) más amplia, con información diversa y consejos de depuración.

### Versión de NSS / OpenSSL desactualizada

«cURL is using an outdated OpenSSL version (OpenSSL/$version). Please update your operating system or features such as installing and updating apps via the app store or Federated Cloud Sharing will not work reliably.»

«cURL is using an outdated NSS version (NSS/$version). Please update your operating system or features such as installing and updating apps via the app store or Federated Cloud Sharing will not work reliably.»

Hay errores conocidos en las versiones antiguas de OpenSSL y NSS que provocan un mal funcionamiento en combinación con hosts remotos que usan SNI, una tecnología que usan la mayoría de los sitios web HTTPS. Para garantizar que Nextcloud funcione correctamente, hay que actualizar OpenSSL al menos a 1.0.2b o 1.0.1d. En el caso de NSS, la versión del parche depende de la distribución, y una heurística ejecuta la prueba que efectivamente reproduce el error.

### El servidor web no está configurado correctamente para resolver /.well-known/caldav/ o /.well-known/carddav/

Ambas URL deben redirigirse correctamente al extremo DAV de Nextcloud. Consultar {nc-ref}`Descubrimiento de servicios <service-discovery-label>` para más información.

### Algunos archivos no han superado la comprobación de integridad

Consultar la documentación de {nc-ref}`Corregir los mensajes de integridad del código no válidos <code_signing_fix_warning_label>` para saber cómo depurar este problema.

### La base de datos no funciona con el nivel de aislamiento de transacciones «READ COMMITTED»

«Su base de datos no funciona con el nivel de aislamiento de transacciones "READ COMMITTED". Esto puede causar problemas cuando se ejecutan en paralelo varias acciones.»

Consultar {nc-ref}`Nivel de aislamiento de transacciones «READ COMMITTED» de la base de datos <db-transaction-label>` para saber cómo configurar la base de datos para este requisito.

### No se usa el prefijo «__Host-» en el nombre de la cookie

«The `__Host-` prefix is not used for the cookie name. It is recommended to enable this in your configuration.»

Nextcloud aplica el prefijo `__Host-` a sus cookies CSRF same-site (`__Host-nc_sameSiteCookiestrict` y `__Host-nc_sameSiteCookielax`) cuando detecta que la conexión se sirve por HTTPS. El prefijo indica a los navegadores que acepten esas cookies solo mediante una conexión segura y desde el host exacto que las estableció, lo que refuerza la protección CSRF.

Esta advertencia aparece cuando Nextcloud no puede confirmar que se ejecuta sobre HTTPS. La causa más habitual es un **proxy inverso** que termina TLS y reenvía las solicitudes a Nextcloud por HTTP sin cifrar. En ese caso, Nextcloud ve HTTP internamente y omite el prefijo.

Para corregirlo, indicar a Nextcloud que trate la conexión como HTTPS añadiendo `overwriteprotocol` a `config/config.php`:

```
'overwriteprotocol' => 'https',
```

Si no se está detrás de un proxy inverso, asegurarse de que el servidor web esté configurado para servir Nextcloud exclusivamente por HTTPS. Consultar la documentación de {nc-ref}`Usar HTTPS <use_https_label>`.

Para más contexto sobre las propias cookies, consultar {nc-ref}`Cookies <cookies>`.
````
