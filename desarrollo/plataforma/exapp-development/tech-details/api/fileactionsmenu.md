---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API de AppAPI para registrar entradas de ExApps en el menú de acciones de archivos: parámetros, carga útil enviada, redirección a la interfaz y flujo."
---
(nc-dev-file_actions_menu_section)=
# Menú de acciones de archivos

## Resumen

Esta página describe la API FileActionsMenu, con la que una ExApp registra entradas en el menú de acciones de archivos: el registro y su anulación, la carga útil que AppAPI envía a la ExApp, la redirección a una página de su interfaz, el flujo de solicitudes y ejemplos. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/fileactionsmenu.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
FileActionsMenu es una API sencilla para registrar una entrada en el menú de acciones de archivos para las ExApps.
AppAPI se encarga de registrar el FileActionsMenu; las ExApps solo necesitan registrarlo en AppAPI.

:::{note}
El FileActionsMenu solo se muestra para las ExApps habilitadas.
:::

### Registrar

Endpoint OCS: `POST /apps/app_api/api/v2/ui/files-actions-menu`

#### Parámetros

Lista completa de parámetros (incluidos los opcionales):

```json
{
    "name": "unique_name_of_file_actions_menu",
    "displayName": "Display name (for UI listing)",
    "actionHandler": "/action_handler_route"
    "mime": "mime of files where to display action menu",
    "icon": "img/icon.svg",
    "permissions": "permissions",
    "order": "order_in_file_actions_menu",
}
```

:::{note}
Las URL `icon` y `actionHandler` son relativas a la raíz de la ExApp; no se requiere la barra inicial.
:::

#### Parámetros opcionales

- *permissions* - Permisos de archivo necesarios para mostrar el menú de acciones, valor predeterminado: **31** (todos los permisos)
- *order* - Orden en el menú de acciones de archivos, valor predeterminado: **0**
- *icon* - URL del icono, valor predeterminado: **null**
- *mime* - Un tipo MIME o varios separados por comas, valor predeterminado: **file**

### Anular el registro

Endpoint OCS: `DELETE /apps/app_api/api/v1/ui/files-actions-menu`

#### Parámetros

Para anular el registro de un FileActionsMenu, basta con indicar el nombre del FileActionsMenu registrado:

```json
{
    "name": "unique_name_of_file_action_menu"
}
```

(nc-dev-node_info)=
### Carga útil de la acción enviada a la ExApp

Cuando se invoca el FileActionsMenu, AppAPI reenvía el manejo de la acción a la ExApp.
Se envían los siguientes datos, tomados del contexto de la acción, al manejador del FileActionsMenu de la ExApp:

```json
{
    "fileId": "123",
    "name": "filename",
    "directory": "relative/to/user/path/to/directory",
    "etag": "file_etag",
    "mime": "file_full_mime",
    "fileType": "dir/file",
    "mtime": "last modify time(integer)",
    "size": "integer",
    "favorite": "nc_favorite_flag",
    "permissions": "file_permissions_for_owner",
    "shareOwner": "optional, str",
    "shareOwnerId": "optional, str",
    "shareTypes": "optional, int",
    "shareAttributes": "optional, int",
    "sharePermissions": "optional, int",
    "userId": "string",
    "instanceId": "string",
}
```

### Redirigir a una página de la interfaz de la ExApp (menú superior)

:::{note}
Solo compatible con Nextcloud 28+.
:::

Para abrir algunos archivos en la interfaz de la ExApp, el FileActionsMenu debe registrarse con la versión v2 de OCS (`/apps/app_api/api/v2/ui/files-actions-menu`).

Después, AppAPI esperará en la respuesta JSON del `action_handler` de la ExApp
el `redirect_handler`: una ruta relativa en la página del menú superior de la ExApp,
a la que AppAPI añadirá un parámetro de consulta `fileIds` con los ID de los archivos seleccionados, por ejemplo:

`/index.php/apps/app_api/embedded/ui_example/first_menu/second_page?fileIds=123,124,125`,

donde `first_menu` es el nombre de la página de la interfaz de la ExApp del menú superior,
y `second_page`, la ruta relativa gestionada por el enrutamiento del frontend de la ExApp.
El parámetro de consulta `fileIds` contiene los ID de los archivos seleccionados, separados por comas.
Después, se puede obtener la información de los archivos mediante una solicitud de búsqueda WebDAV; ver [ui_example](https://github.com/nextcloud/ui_example).

### Flujo de solicitudes

Flujo de trabajo general de una ExApp basada en FileActionsMenu.

#### Acción del usuario

El diagrama de secuencia muestra que el usuario pulsa la acción registrada de la ExApp, el menú de acciones de archivos envía a AppAPI la carga útil con el contexto de la acción, AppAPI reenvía la solicitud al manejador de la ExApp, la ExApp devuelve a AppAPI el estado de aceptación de la acción y AppAPI muestra al usuario una alerta (acción enviada o error).

#### Resultados de la acción

Los resultados del procesamiento de archivos pueden guardarse junto al archivo inicial o en cualquier otro lugar,
p. ej., en una ubicación configurada en los ajustes de la ExApp (`appconfig_ex`) o en los ajustes de usuario de la ExApp (`preferences_ex`).

El diagrama de secuencia muestra que la ExApp sube el archivo de resultado a Nextcloud y envía a AppAPI una notificación sobre los resultados de la acción.

### Ejemplos

Esta es una lista de ExApps de ejemplo sencillas basadas en FileActionsMenu:

- [to_gif](https://github.com/cloud-py-api/nc_py_api/tree/main/examples/as_app/to_gif) - ExApp basada en FileActionsMenu que convierte vídeos a GIF en el mismo lugar
- [upscaler_example](https://github.com/cloud-py-api/upscaler_example.git) - ExApp basada en FileActionsMenu que aumenta la resolución de una imagen en el mismo lugar
````
