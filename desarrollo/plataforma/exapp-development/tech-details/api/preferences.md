---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de preferencias de las ExApps: establecer, obtener y eliminar valores de configuración del usuario autenticado, con solicitud y respuesta."
---
# Preferencias

## Resumen

Esta página describe la API de preferencias de las ExApps, un ajuste específico de cada usuario: los endpoints OCS para establecer o actualizar, obtener y eliminar valores de configuración del usuario autenticado actual. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/preferences.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La API de preferencias de las ExApps es similar a la API de preferencias estándar.
Se trata de un ajuste específico de cada usuario.

:::{note}
Desde Nextcloud 32, los valores de configuración sensibles se cifran en la base de datos.
:::

### Establecer un valor de configuración del usuario

Establecer o actualizar un valor de configuración para el **usuario autenticado actual**.

Endpoint OCS: `POST /apps/app_api/api/v1/ex-app/preference`

#### Datos de la solicitud

```json
{
    "configKey": "key",
    "configValue": "value",
    "sensitive": "store value encrypted in the database (0/1, default: 0)"
}
```

#### Datos de la respuesta

Si tiene éxito, se devuelve el objeto ExAppPreference.
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
            "id":983,
            "appid":"app_id",
            "configkey":"test key",
            "configvalue":"123",
            "sensitive":0
        }
    }
}
```

### Obtener valores de configuración del usuario

Obtener los valores de configuración del **usuario autenticado actual**.

Endpoint OCS: `POST /apps/app_api/api/v1/ex-app/preference/get-values`

#### Datos de la solicitud

```json
{
    "configKeys": ["key1", "key2", "key3"]
}
```

#### Datos de la respuesta

Se devuelve la lista de valores de preferencias de la ExApp.

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
            "configkey":"test key",
            "configvalue":"123"
            },
            {
            "configkey":"test key2",
            "configvalue":"321"
            }
        ]
    }
}
```

### Eliminar valores de configuración del usuario

Eliminar los valores de configuración del **usuario autenticado actual**.

Endpoint OCS: `DELETE /apps/app_api/api/v1/ex-app/preference`

#### Datos de la solicitud

```json
{
    "configKeys": ["key1", "key2", "key3"]
}
```

#### Respuesta

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
        "data":2
    }
}
```
````
