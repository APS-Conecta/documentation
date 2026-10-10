---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Índice de las API de Nextcloud que AppAPI ofrece a las ExApps, y aviso de que todas sus API OCS, salvo la de ExApp, requieren AppAPIAuth."
---
(nc-dev-app_api_nextcloud_apis)=
# API de Nextcloud de AppAPI

## Resumen

Esta sección reúne el índice de las API de Nextcloud que AppAPI ofrece a las ExApps: registro, configuración de la app, preferencias, menús, notificaciones, escucha de eventos, comandos OCC y otras API OCS. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
AppAPIAuth es necesario para todas las API OCS de AppAPI, excepto `ExApp`.
:::

- {nc-doc}`developer_manual/exapp_development/tech_details/api/logging`
- {nc-doc}`developer_manual/exapp_development/tech_details/api/appconfig`
- {nc-doc}`developer_manual/exapp_development/tech_details/api/preferences`
- {nc-doc}`developer_manual/exapp_development/tech_details/api/exapp`
- {nc-doc}`developer_manual/exapp_development/tech_details/api/routes`
- {nc-doc}`developer_manual/exapp_development/tech_details/api/utils`
- {nc-doc}`developer_manual/exapp_development/tech_details/api/fileactionsmenu`
- {nc-doc}`developer_manual/exapp_development/tech_details/api/topmenu`
- {nc-doc}`developer_manual/exapp_development/tech_details/api/settings`
- {nc-doc}`developer_manual/exapp_development/tech_details/api/notifications`
- {nc-doc}`developer_manual/exapp_development/tech_details/api/events_listener`
- {nc-doc}`developer_manual/exapp_development/tech_details/api/occ_command`
- {nc-doc}`developer_manual/exapp_development/tech_details/api/talkbots`
- {nc-doc}`developer_manual/exapp_development/tech_details/api/other_ocs`
````

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
