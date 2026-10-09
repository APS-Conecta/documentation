---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cambios al actualizar a Nextcloud 32: PHP, cabecera X-XSS-Protection, libreta de direcciones del sistema, vistas previas MP3, AppAPI e integridad de S3."
---
# Actualización a Nextcloud 32

## Resumen

Esta página recoge los cambios que hay que conocer al actualizar a Nextcloud 32: las versiones de PHP, la cabecera `X-XSS-Protection`, el recuento de usuarios activos, la posible desactivación de la libreta de direcciones del sistema, las vistas previas de MP3, las comprobaciones de AppAPI y las protecciones de integridad de datos de S3. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/release_notes/upgrade_to_32.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Requisitos del sistema

- PHP 8.1 queda obsoleto, aunque todavía es compatible.
- PHP 8.4 ya es compatible, pero se recomienda 8.3.

### Configuración del servidor web

- Las comprobaciones de configuración ya no verifican la cabecera de respuesta `X-XSS-Protection`. Se ha eliminado del `.htaccess` de Nextcloud, y puede convenir ajustar la configuración del servidor web para que deje de enviarla.
  El filtrado XSS solo se admitió hasta Chromium 78 y navegadores igual de antiguos, pero se comprobó que causaba más problemas de los que resolvía, incluidos vectores de ataque.
  Hoy en día, aparte de no enviar la cabecera en absoluto, el único valor recomendado en general es `0`. Hay más contexto en la [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#x-xss-protection).

### Monitorización: recuento de usuarios activos

La app de monitorización se ajustó para contar los usuarios activos del mismo modo que occ user:report y la app de soporte.

### Libreta de direcciones del sistema

Durante la actualización a Nextcloud 32, la libreta de direcciones del sistema podría quedar desactivada si el número de usuarios del sistema supera el límite predeterminado de 5000 usuarios. Esto sirve para evitar problemas de rendimiento. La libreta de direcciones del sistema puede volver a activarse desde la línea de comandos o desde la interfaz de administración.

Para más información sobre la libreta de direcciones del sistema, consultar la documentación. {nc-ref}`Libreta de direcciones del sistema <system-address-book>`

### Vistas previas

A partir de Nextcloud 32.0.1, el proveedor de vistas previas de archivos MP3, que lee las imágenes de portada incrustadas en los archivos, está desactivado de forma predeterminada por motivos de rendimiento y estabilidad. Consultar {nc-doc}`admin_manual/configuration_files/previews_configuration` para ver cómo activar o desactivar el proveedor de vistas previas.

### Comprobaciones de configuración de AppAPI (app_api) ampliadas

A partir de Nextcloud 30.0.1, la app AppAPI viene incluida y activada de forma predeterminada. Consultar {nc-doc}`admin_manual/exapps_management/index` para más detalles. Además, a partir de la versión 32.0.0, AppAPI ha ampliado sus comprobaciones de configuración.

Esta app puede desactivarse de la forma habitual desde el menú *Apps* si no se prevé usar integraciones de AppAPI en un futuro próximo.

Si AppAPI está desactivada, las demás apps que dependen de ella no serán visibles en la tienda de apps. También se desactivarán las comprobaciones de configuración relacionadas con AppAPI.

### Protecciones de integridad de S3 activadas; puede ser necesario actualizar la configuración

El AWS SDK for PHP se actualizó y ahora admite las protecciones de integridad de datos de S3.

\>= Nextcloud 32.0.2: si el backend S3 no admite la protección de integridad de datos, puede desactivarse añadiendo `'request_checksum_calculation' => 'when_required',` y `'response_checksum_validation' => 'when_required',` a la configuración del almacenamiento de objetos.

\>= Nextcloud 32.0.3: las protecciones de integridad de datos de S3 están desactivadas de forma predeterminada y ahora hay que activarlas expresamente.

Si el backend S3 no lo admite, al subir archivos puede aparecer en los registros un error como `Checksum Type mismatch occurred, expected checksum Type: null, actual checksum Type: crc32`.

Hay más detalles sobre las protecciones de integridad de datos de S3 en <https://docs.aws.amazon.com/sdkref/latest/guide/feature-dataintegrity.html> y <https://github.com/aws/aws-sdk-php/discussions/3100>.
````
