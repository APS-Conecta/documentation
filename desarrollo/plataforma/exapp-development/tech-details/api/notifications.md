---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de AppAPI para que las ExApps envíen notificaciones a los usuarios con cadenas de objetos enriquecidos: endpoint, carga útil y parámetros."
---
# Notificaciones

## Resumen

Esta página describe la API con la que las ExApps envían notificaciones limitadas a los usuarios mediante cadenas de objetos enriquecidos: el endpoint OCS, un ejemplo de carga útil y sus parámetros. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/notifications.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
AppAPI permite a las ExApps enviar notificaciones limitadas a los usuarios.
La ExApp puede enviar notificaciones sencillas usando las [cadenas de objetos enriquecidos](https://github.com/nextcloud/server/blob/master/lib/public/RichObjectStrings/Definitions.php#L42) disponibles.
Hay más información sobre las cadenas de objetos enriquecidos [aquí](https://github.com/nextcloud/server/issues/1706).

### Enviar una notificación (OCS)

Endpoint OCS: `POST /apps/app_api/api/v1/notification`

#### Carga útil de la solicitud

Ejemplo de carga útil.

```json
{
    "params": {
        "object": "app_api",
        "object_id": "app_api_id",
        "subject_type": "app_api_ex_app",
        "subject_params": {
            "rich_subject": "Image {file} successfully upscaled!",
            "rich_subject_params": {
                "file": {
                    "type": "file",
                    "id": 123,
                    "name": "upscaled_image_name",
                    "path": "path/to/upscaled_image_name"
                }
            },
            "rich_message": "{user} checkout results!",
            "rich_message_params": {
                "user": {
                    "type": "user",
                    "id": "admin",
                    "name": "admin"
                }
            },
            "link": "http(s)://nextcloud.local/index.php/apps/files/?fileid=123"
        }
    }
}
```

### Parámetros

Parámetros obligatorios de la carga útil:

- `object` - `[required]` debe establecerse en el valor predeterminado; aún no se usa
- `object_id` - `[required]` debe establecerse en el valor predeterminado; aún no se usa
- `subject_type` - `[required]` el tipo de asunto debe establecerse en el valor predeterminado; aún no se usa
- `subject_params` - `[required]`
  - `rich_subject` - `[optional]` cadena del asunto (título) enriquecido
  - `rich_subject_params` - `[optional]` parámetros del asunto (título) enriquecido para reemplazar los objetos enriquecidos en la cadena
  - `rich_message` - `[optional]` cadena del mensaje enriquecido
  - `rich_message_params` - `[optional` parámetros del mensaje enriquecido para reemplazar los objetos en la cadena
  - `link` - URL absoluta que se establece como enlace de la notificación
````
