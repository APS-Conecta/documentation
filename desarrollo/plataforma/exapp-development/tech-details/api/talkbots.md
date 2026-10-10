---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de AppAPI para registrar y anular bots de Talk de una ExApp: endpoints y datos de la solicitud."
---
# Bots de Talk

## Resumen

Esta página describe la API OCS de AppAPI con la que una ExApp registra un bot de Talk y anula su registro, con los datos de cada solicitud. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/talkbots.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
AppAPI ofrece una API para registrar bots de Talk de ExApps.
Esto significa que las ExApps podrían funcionar solo como un bot de Talk o como una de las opciones de la app.
Más información sobre los bots de Talk [aquí](https://nextcloud-talk.readthedocs.io/en/latest/bots/).

### Registrar un bot de Talk de una ExApp (OCS)

Endpoint OCS: `POST /apps/app_api/api/v1/talk_bot`

#### Datos de la solicitud

```json
{
    "name": "Talk bot display name",
    "route": "/talk_bot_webhook_route_on_ex_app",
    "description": "Talk bot description",
}
```

### Anular el registro de un bot de Talk de una ExApp (OCS)

Para anular el registro del bot de Talk de la ExApp, se indica la ruta en la que está registrado el bot de Talk.

Endpoint OCS: `DELETE /apps/app_api/api/v1/talk_bot`

#### Datos de la solicitud

```json
{
    "route": "/route_of_talk_bot"
}
```
````
