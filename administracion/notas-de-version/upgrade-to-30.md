---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cambios al actualizar a Nextcloud 30: requisitos del sistema, WebP, opciones de config.php, Imaginary, contraseñas de aplicación, monitorización y AppAPI."
---
# Actualización a Nextcloud 30

## Resumen

Esta página recoge los cambios que hay que conocer al actualizar a Nextcloud 30: los requisitos del sistema, cómo servir las imágenes WebP, las opciones de `config.php` que cambian, las vistas previas de PDF con Imaginary, la limpieza de contraseñas de aplicación, el recuento de usuarios activos y AppAPI como app predeterminada. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/release_notes/upgrade_to_30.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Requisitos del sistema

- PHP 8.1 queda obsoleto, aunque todavía es compatible.
- PHP 8.0 ya no es compatible.
- PostgreSQL 9.4 ya no es compatible.
- MariaDB 10.3 y 10.5 ya no son compatibles.

### Configuración del servidor web

Asegurarse de que el servidor web sirve correctamente como recursos estáticos los archivos con la extensión `webp` (imágenes WebP). Esto viene incluido en el archivo `.htaccess` que se distribuye, pero si se usa otro servidor web o una configuración personalizada, hay que comprobarlo manualmente.

### Configuración de Nextcloud

Cambios en las opciones disponibles en `config.php`.

- La opción `blacklisted_files` queda obsoleta y se sustituye por `forbidden_filenames`
- La opción `forbidden_chars` queda obsoleta y se sustituye por `forbidden_filename_characters`
- Se añadió la opción `forbidden_filename_basenames` para permitir bloquear archivos con nombres base concretos (el nombre de archivo sin extensión (lo que va antes del primer punto))
- Se añadió la opción `forbidden_filename_extensions` para permitir bloquear el uso de extensiones en los nombres de archivo

### Vistas previas de archivos PDF con Imaginary

El proveedor de vistas previas `OC\Preview\Imaginary` ya no genera vistas previas de archivos PDF. Añadir el nuevo proveedor de vistas previas `OC\Preview\ImaginaryPDF` a `enabledPreviewProviders` para activar la generación de vistas previas de archivos PDF con Imaginary.

### Limpieza automática de contraseñas de aplicación

Nextcloud 30 {nc-ref}`limpiará las contraseñas de aplicación sin usar <authentication-app-password-clean-up>`.

### Monitorización: recuento de usuarios activos

A partir de Nextcloud 30.0.12, la app de monitorización se ajustó para contar los usuarios activos del mismo modo que occ user:report y la app de soporte.

### AppAPI (app_api) es ahora una app predeterminada

A partir de Nextcloud 30.0.1, la app AppAPI viene incluida y activada de forma predeterminada. Consultar {nc-doc}`admin_manual/exapps_management/index` para más detalles.

Esta app puede desactivarse de la forma habitual desde el menú *Apps* si no se prevé usar integraciones de AppAPI en un futuro próximo.

Si AppAPI está desactivada, las demás apps que dependen de ella no serán visibles en la tienda de apps. También se desactivarán las comprobaciones de configuración relacionadas con AppAPI.
````
