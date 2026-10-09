---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Montar un directorio de un servidor WebDAV u otro servidor Nextcloud como almacenamiento externo: datos necesarios, HTTPS y subcarpeta remota."
---
# WebDAV

## Resumen

Esta página explica cómo montar un directorio de cualquier servidor WebDAV, o de otro servidor Nextcloud, como almacenamiento externo: los datos necesarios, la opción HTTPS y la subcarpeta remota. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/external_storage/webdav.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Usar este backend para montar un directorio de cualquier servidor WebDAV o de otro servidor Nextcloud.

Se necesita la siguiente información:

- Nombre de la carpeta: el nombre del punto de montaje local.
- La URL del servidor WebDAV o Nextcloud.
- El nombre de usuario y la contraseña del servidor remoto
- `https://` Seguro: siempre se recomienda `https://` por seguridad, aunque se puede dejar sin marcar para usar `http://`.

Opcionalmente, se puede especificar una `Remote Subfolder` para cambiar el directorio de destino. El valor predeterminado es usar toda la raíz.

:::{note}
Los usuarios de CPanel deberían instalar [Web Disk](https://documentation.cpanel.net/display/ALD/Web+Disk) para activar la funcionalidad WebDAV.
:::

Consultar {nc-doc}`admin_manual/configuration_files/external_storage_configuration_gui` para ver más opciones de montaje e información.

Consultar {nc-doc}`admin_manual/configuration_files/external_storage/auth_mechanisms` para obtener más información sobre los esquemas de autenticación.
````
