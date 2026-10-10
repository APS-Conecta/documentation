---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de AppAPI para que las ExApps envíen mensajes al registro de Nextcloud: endpoint, datos de la solicitud, niveles de registro y respuestas."
---
# Registro

## Resumen

Esta página describe la API de registro con la que las ExApps envían mensajes al registro de Nextcloud: el endpoint OCS, los datos de la solicitud y las respuestas posibles. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/logging.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Hay una API de registro que puede usarse para registrar en Nextcloud mensajes de las ExApps.

:::{note}
El *loglevel* de Nextcloud para uso interno de la ExApp puede obtenerse
de las capacidades privadas de *app_api* (tras la autenticación).
:::

### Enviar un mensaje de registro (OCS)

Endpoint OCS: `POST /apps/app_api/api/v1/log`

#### Datos de la solicitud

```json
{
    "level": "log_lvl(integer)",
    "message": "message",
}
```

Los valores posibles de `log_lvl` se describen aquí: [Nivel de registro de Nextcloud](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/logging_configuration.html#log-level)

#### Datos de la respuesta

Si no se produce ningún error, se devuelve una respuesta vacía con el código de estado 200.
Si la ExApp no se encuentra o está deshabilitada, o el *loglevel* no es válido, se devuelve un OCS Bad Request.
````
