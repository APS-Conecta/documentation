---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Conectar otro servidor Nextcloud como almacenamiento externo: qué URL usar en el campo URL y dónde está el resto de la configuración."
---
# Nextcloud

## Resumen

Esta página explica cómo conectar otro servidor Nextcloud como almacenamiento externo, una variante especializada de WebDAV, y qué ruta poner en el campo URL. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/external_storage/nextcloud.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Un almacenamiento Nextcloud es un almacenamiento {nc-doc}`admin_manual/configuration_files/external_storage/webdav` especializado, con optimizaciones para la comunicación entre Nextcloud y Nextcloud. Consultar la documentación de {nc-doc}`admin_manual/configuration_files/external_storage/webdav` para saber cómo configurar un almacenamiento externo de Nextcloud.

Al rellenar el campo **URL**, usar la ruta a la raíz de la instalación de Nextcloud, en lugar de la ruta al endpoint de WebDAV. Así, para un servidor en `https://example.com/nextcloud`, usar `https://example.com/nextcloud` y no `https://example.com/nextcloud/remote.php/dav`.

Consultar {nc-doc}`admin_manual/configuration_files/external_storage_configuration_gui` para ver más opciones de montaje e información.

Consultar {nc-doc}`admin_manual/configuration_files/external_storage/auth_mechanisms` para obtener más información sobre los esquemas de autenticación.
````
