---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cambios al actualizar a Nextcloud 31: PHP, formato de fila MySQL/MariaDB, memoria de APCu, tamaño de fragmento, monitorización, vistas previas MP3 y AppAPI."
---
# Actualización a Nextcloud 31

## Resumen

Esta página recoge los cambios que hay que conocer al actualizar a Nextcloud 31: las versiones de PHP, la advertencia por el formato de fila en MySQL y MariaDB, la memoria reservada para APCu, el nuevo tamaño máximo de fragmento, el recuento de usuarios activos, las vistas previas de MP3 y AppAPI como app predeterminada. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/release_notes/upgrade_to_31.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Requisitos del sistema

- PHP 8.1 queda obsoleto, aunque todavía es compatible.
- PHP 8.4 ya es compatible, pero se recomienda 8.3.

### Configuración de la base de datos

Los formatos de fila distintos de `DYNAMIC` en las bases de datos MySQL y MariaDB [generan una advertencia desde Nextcloud 24](https://github.com/nextcloud/server/issues/34497), ya que suelen causar problemas de rendimiento. Con Nextcloud 31 se añadió para ello una [nueva advertencia de configuración más visible](https://github.com/nextcloud/server/pull/48547).

El formato de fila puede cambiarse mediante comandos DDL `ALTER TABLE` durante una ventana de mantenimiento. Cambiar el formato de fila de `COMPRESSED` a `DYNAMIC` requiere aproximadamente el doble de espacio en disco y puede tardar mucho según el tamaño de la base de datos. Consultar la [documentación de MySQL](https://dev.mysql.com/doc/refman/en/innodb-row-format.html) para más información. Si no se sabe con certeza cómo hacerlo, pueden [encontrarse algunos consejos y trucos de la comunidad](https://help.nextcloud.com/t/upgrade-to-nextcloud-hub-10-31-0-0-incorrect-row-format-found-in-your-database/218366/).

### Configuración de PHP

Hay una nueva advertencia de configuración que comprueba si la memoria reservada para APCu es suficiente. Si aparece esta advertencia, debe aumentarse la memoria reservada para APCu. Para ello, aumentar el valor de la directiva `apc.shm_size` en el archivo `php.ini`. En general se aconseja revisar este valor y aumentarlo si es necesario, según el tamaño de la instancia.

### Configuración de Nextcloud

#### Tamaño máximo de fragmento

Se ha ajustado el tamaño máximo predeterminado de fragmento para la subida de archivos grandes. Antes era de 10MiB; ahora se ha aumentado a 100MiB.

Además, la configuración se trasladó de una configuración de app a la configuración del sistema (`config.php`). Si antes se estableció un valor personalizado, ese valor se migrará automáticamente a la configuración del sistema durante la actualización. Pero si hay que establecer un nuevo valor personalizado, ahora debe usarse la configuración del sistema; consultar también {nc-ref}`files_configure_max_chunk_size`.

### Monitorización: recuento de usuarios activos

A partir de Nextcloud 31.0.6, la app de monitorización se ajustó para contar los usuarios activos del mismo modo que occ user:report y la app de soporte.

### Vistas previas

A partir de Nextcloud 31.0.10, el proveedor de vistas previas de archivos MP3, que lee las imágenes de portada incrustadas en los archivos, está desactivado de forma predeterminada por motivos de rendimiento y estabilidad. Consultar {nc-doc}`admin_manual/configuration_files/previews_configuration` para ver cómo activar o desactivar el proveedor de vistas previas.

### AppAPI (app_api) es ahora una app predeterminada

A partir de Nextcloud 30.0.1, la app AppAPI viene incluida y activada de forma predeterminada. Consultar {nc-doc}`admin_manual/exapps_management/index` para más detalles.

Esta app puede desactivarse de la forma habitual desde el menú *Apps* si no se prevé usar integraciones de AppAPI en un futuro próximo.

Si AppAPI está desactivada, las demás apps que dependen de ella no serán visibles en la tienda de apps. También se desactivarán las comprobaciones de configuración relacionadas con AppAPI.
````
