---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Conectar un servidor FTP o FTPS como almacenamiento externo: datos necesarios, restricción de acceso, FTPS y el ajuste de PHP allow_url_fopen."
---
# FTP/FTPS

## Resumen

Esta página explica cómo conectar un servidor FTP o FTPS como almacenamiento externo: los datos necesarios, cómo restringir el acceso, cómo activar FTPS y el ajuste de PHP que requiere. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/external_storage/ftp.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Para conectarse a un servidor FTP, se necesita:

- Un nombre de carpeta para el punto de montaje local; la carpeta se creará si no existe
- La URL del servidor FTP
- El número de puerto (predeterminado: 21)
- El nombre de usuario y la contraseña del servidor FTP
- Subcarpeta remota, el directorio FTP que se montará en Nextcloud. Nextcloud usa de forma predeterminada el directorio raíz. Si se especifica una subcarpeta, hay que omitir la barra inicial. Por ejemplo, `public_html/images`

El nuevo punto de montaje está disponible para todos los usuarios de forma predeterminada, y se puede restringir el acceso introduciendo usuarios o grupos concretos en el campo **Disponible para**.

Opcionalmente, Nextcloud puede usar FTPS (FTP sobre SSL) marcando **ftps:// Seguro**. Esto requiere configuración adicional con el certificado raíz si el servidor FTP usa un certificado autofirmado.

:::{note}
El almacenamiento externo `FTP/FTPS` necesita que el ajuste de PHP `allow_url_fopen` esté establecido en `1`. Si hay problemas de conexión, comprobar que no esté establecido en `0` en el archivo `php.ini`. Consultar {nc-ref}`label-phpinfo` para saber cómo encontrar el archivo `php.ini` correcto que hay que editar.
:::

Consultar {nc-doc}`admin_manual/configuration_files/external_storage_configuration_gui` para ver más opciones de montaje e información.

FTP usa el esquema de autenticación por contraseña; consultar {nc-doc}`admin_manual/configuration_files/external_storage/auth_mechanisms` para obtener más información sobre los esquemas de autenticación.
````
