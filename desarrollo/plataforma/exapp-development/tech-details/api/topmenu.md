---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API TopMenu de AppAPI: registrar y anular entradas de ExApps en el menú superior, estado inicial, scripts y estilos, con sus endpoints OCS."
---
(nc-dev-top_menu_section)=
# Entrada del menú superior

## Resumen

Esta página describe la API TopMenu, con la que una ExApp registra una entrada en el menú superior y anula su registro, y los endpoints OCS para establecer o eliminar su estado inicial y para añadir o quitar scripts y estilos. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/topmenu.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
TopMenu es una API para registrar una entrada en el menú superior de Nextcloud para las ExApps.
AppAPI se encarga de registrar el TopMenu y de redirigir mediante proxy todas las solicitudes a la ExApp.

:::{note}
El TopMenu solo se muestra para las ExApps habilitadas.
:::

### Registrar una entrada de menú

Endpoint OCS: `POST /apps/app_api/api/v1/ui/top-menu`

#### Parámetros

Lista completa de parámetros (incluidos los opcionales):

```json
{
    "name": "unique_name_of_top_menu",
    "displayName": "Display name",
    "icon": "img/icon.svg",
    "adminRequired": "0 or 1",
}
```

:::{note}
`icon` es relativo a la raíz de la ExApp; no se requiere la barra inicial.
:::

#### Parámetros opcionales

- *icon* - URL del icono, valor predeterminado: **null**
- *adminRequired* - Valor que indica si la entrada debe ser visible para todos o solo para los administradores

### Anular el registro de una entrada de menú

Endpoint OCS: `DELETE /apps/app_api/api/v1/ui/top-menu`

#### Parámetros

Para anular el registro de un TopMenu, basta con indicar el nombre del TopMenu registrado:

```json
{
    "name": "unique_name_of_top_menu"
}
```

### Establecer el estado inicial

Endpoint OCS: `POST /apps/app_api/api/v1/ui/initial-state`

#### Parámetros

```json
{
    "type": "top_menu",
    "name": "unique_name_of_top_menu",
    "key": "key_name",
    "value": "array with value(s)",
}
```

### Eliminar el estado inicial

Endpoint OCS: `DELETE /apps/app_api/api/v1/ui/initial-state`

#### Parámetros

```json
{
    "type": "top_menu",
    "name": "unique_name_of_top_menu",
    "key": "key_name",
}
```

### Añadir un script

Endpoint OCS: `POST /apps/app_api/api/v1/ui/script`

#### Parámetros

```json
{
    "type": "top_menu",
    "name": "unique_name_of_script",
    "path": "Url to script, e.g.: js/ui_example-main",
    "afterAppId": "optional value",
}
```

:::{note}
La URL del script es relativa a la raíz de la ExApp; no se requiere la barra inicial,
y la extensión ".js" no es necesaria: el servidor la añadirá automáticamente.
:::

### Eliminar un script

Endpoint OCS: `DELETE /apps/app_api/api/v1/ui/script`

#### Parámetros

```json
{
    "type": "top_menu",
    "name": "unique_name_of_script",
    "path": "Url to script",
}
```

### Añadir un estilo

Endpoint OCS: `POST /apps/app_api/api/v1/ui/style`

#### Parámetros

```json
{
    "type": "top_menu",
    "name": "unique_name_of_style",
    "path": "Url to style, e.g.: css/my-style",
}
```

:::{note}
La URL del estilo es relativa a la raíz de la ExApp; no se requiere la barra inicial,
y la extensión ".css" no es necesaria: el servidor la añadirá automáticamente.
:::

### Eliminar un estilo

Endpoint OCS: `DELETE /apps/app_api/api/v1/ui/style`

#### Parámetros

```json
{
    "type": "top_menu",
    "name": "unique_name_of_style",
    "path": "Url to style",
}
```
````
