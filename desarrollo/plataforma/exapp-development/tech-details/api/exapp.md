---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de ExApp: listar ExApps, informar el progreso de inicialización, obtener la URL de Nextcloud, hacer solicitudes a ExApps y leer su estado."
---
# ExApp

## Resumen

Esta página describe las API OCS para acciones de las ExApps: obtener la lista de ExApps, establecer el progreso de inicialización, obtener la URL de Nextcloud, hacer solicitudes a las ExApps y obtener su estado de habilitación. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/exapp.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
API OCS para acciones de las ExApps.

### Obtener la lista de ExApps

Obtener la lista de ExApps instaladas.

Endpoint OCS: `GET /apps/app_api/api/v1/ex-app/{list}`

Hay dos opciones para `list`:

- `enabled`: lista solo las ExApps habilitadas
- `all`: lista todas las ExApps

#### Datos de la respuesta

Los datos de la respuesta son un array JSON de objetos ExApp con los siguientes atributos:

```json
{
    "id": "appid of the ExApp",
    "name": "name of the ExApp",
    "version": "version of the ExApp",
    "enabled": "true/false flag",
    "last_check_time": "timestamp of last successful Nextcloud->ExApp connection check",
}
```

### Establecer el progreso de inicialización de la ExApp

Se usa durante el {nc-ref}`paso de inicialización <ex_app_lifecycle_init>` de la ExApp.

:::{note}
Requiere AppAPIAuth.
:::

Endpoint OCS: `PUT /apps/app_api/ex-app/status`

#### Datos de la solicitud

```json
{
    "progress": "progress value",
    "error": "optional, error string message"
}
```

#### Datos de la respuesta

Devuelve HTTP 200 si tiene éxito y HTTP 404 si hay un error.

### Obtener la URL de Nextcloud

Puede que la ExApp necesite conocer (o actualizar) la URL de Nextcloud.

Endpoint OCS: `GET /apps/app_api/api/v1/info/nextcloud_url`

#### Datos de la respuesta

Devuelve la URL base de la instancia de Nextcloud:

```json
{
    "base_url": "http(s)://nextcloud.example.com"
}
```

### Hacer solicitudes a las ExApps

Hay dos endpoints para hacer solicitudes a las ExApps:

1. Solicitud síncrona: `POST /apps/app_api/api/v1/ex-app/request/{appid}`
2. Solicitud síncrona con el usuario establecido para la ExApp: `POST /apps/app_api/api/v1/ex-app/request/{appid}/{userId}`

#### Datos de la solicitud

Los parámetros de los datos de la solicitud son los mismos que en `lib/PublicFunction.php`:

```json
{
    "route": "relative route to ExApp API endpoint",
    "method": "GET/POST/PUT/DELETE",
    "params": {},
    "options": {},
}
```

:::{note}
`userId` y `appId` se toman de los parámetros de la URL
:::

#### Datos de la respuesta

La estructura de los datos de la respuesta OCS de una solicitud correcta a la ExApp es la siguiente:

```json
{
    "status_code": "HTTP status code",
    "body": "response data from ExApp",
    "headers": "response headers from ExApp",
}
```

Si hay un error, el objeto de respuesta solo tendrá un atributo `error` con el mensaje de error.

### Obtener el estado de habilitación de la ExApp

Devolver el estado de habilitación de la ExApp autenticada.

Endpoint OCS: `GET /apps/app_api/api/v1/ex-app/state`

:::{note}
La ExApp puede llamar a este endpoint aunque esté deshabilitada en el lado de Nextcloud,
y requiere {nc-doc}`AppAPIAuth <developer_manual/exapp_development/tech_details/Authentication>`.
:::

#### Datos de la respuesta

Devuelve 1 si la ExApp está habilitada y 0 si está deshabilitada.
````
