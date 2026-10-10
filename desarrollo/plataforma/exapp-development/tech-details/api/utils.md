---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de utilidades del sistema que AppAPI ofrece para la lógica interna de las ExApps: obtener la lista de ID de usuarios de Nextcloud."
---
# API OCS varias

## Resumen

Esta página describe las API OCS de utilidades del sistema que las ExApps necesitan para su lógica interna: el endpoint que devuelve la lista de ID de usuarios y su respuesta. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/utils.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Hay algunas API de utilidades del sistema necesarias para la lógica interna de las ExApps.

### Obtener la lista de usuarios de NC

Endpoint OCS: `GET /apps/app_api/api/v1/users`

#### Datos de la respuesta

Devuelve solo una lista de ID de usuario.

```json
{"ocs": {
    "meta": {
        "status": "ok",
        "statuscode": 100,
        "message": "OK",
        "totalitems": "",
        "itemsperpage": ""
        },
    "data": ["admin", "alice", "bob", "jane", "john"]
    }
}
```
````
