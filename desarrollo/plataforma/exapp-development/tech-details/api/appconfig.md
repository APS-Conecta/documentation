---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de AppConfig de las ExApps: establecer, obtener y eliminar valores de configuración de la app, con los datos de solicitud y respuesta."
---
# AppConfig

## Resumen

Esta página describe la API AppConfig de las ExApps: los endpoints OCS para establecer o actualizar, obtener y eliminar valores de configuración de la app, con los datos de la solicitud y de la respuesta. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/appconfig.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La API AppConfig de las ExApps es similar a la API **appconfig** estándar de Nextcloud.

:::{note}
Desde Nextcloud 32, los valores de configuración sensibles se cifran en la base de datos.
:::

### Establecer un valor de configuración de la app

Establecer o actualizar un valor de configuración de la ExApp.

:::{note}
Si no se especifica `sensitive` al actualizar el valor, no se cambiará al valor predeterminado.
:::

Endpoint OCS: `POST /apps/app_api/api/v1/ex-app/config`

#### Datos de la solicitud

```json
{
    "configKey": "key",
    "configValue": "value"
    "sensitive": "store value encrypted in the database (0/1, default: 0)"
}
```

#### Datos de la respuesta

Si tiene éxito, se devuelve el objeto ExAppConfig.
Si hay un error, se devuelve OCS Bad Request.

```json
{
    "ocs":
    {
        "meta":
        {
            "status":"ok",
            "statuscode":100,
            "message":"OK",
            "totalitems":"",
            "itemsperpage":""
        },
        "data":
        {
            "id":1084,
            "appid":"app_id",
            "configkey":"key",
            "configvalue":"value",
            "sensitive":1
        }
    }
}
```

### Obtener valores de configuración de la app

Obtener los valores de configuración de la ExApp

Endpoint OCS: `POST /apps/app_api/api/v1/ex-app/config/get-values`

#### Datos de la solicitud

```json
{
    "configKeys": ["key1", "key2", "key3"]
}
```

#### Datos de la respuesta

Se devuelve la lista de valores de configuración de la ExApp.

```json
{
    "ocs":
    {
        "meta":
        {
            "status":"ok",
            "statuscode":100,
            "message":"OK",
            "totalitems":"",
            "itemsperpage":""
        },
        "data":[
            {
            "configkey":"test_key",
            "configvalue":"123"
            }
        ]
    }
}
```

### Eliminar valores de configuración de la app

Eliminar valores de configuración de la ExApp.

Endpoint OCS: `DELETE /apps/app_api/api/v1/ex-app/config`

#### Datos de la solicitud

```json
{
    "configKeys": ["key1", "key2", "key3"]
}
```

#### Respuesta

Devuelve el número de valores de configuración eliminados.

```json
{
    "ocs":
    {
        "meta":
        {
            "status":"ok",
            "statuscode":100,
            "message":"OK",
            "totalitems":"",
            "itemsperpage":""
        },
    "data":1
    }
}
```
````
