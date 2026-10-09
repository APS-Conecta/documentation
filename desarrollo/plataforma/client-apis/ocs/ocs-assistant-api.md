---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS del Asistente: programar y gestionar tareas de IA, su historial y resultados; cómo consultar su especificación OpenAPI."
---
(nc-dev-ocs-assistant-api)=
# API OCS del Asistente

## Resumen

Esta página presenta, para quienes desarrollan clientes o apps, la API OCS del Asistente: qué permite hacer con las tareas de IA, cómo consultar su especificación OpenAPI y dónde está la documentación relacionada.

````{upstream} developer_manual/client_apis/OCS/ocs-assistant-api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

La API OCS del asistente permite programar y gestionar tareas de IA, obtener el historial de tareas y consultar los resultados de las tareas desde cualquier cliente o aplicación.

La API está documentada con OpenAPI. Para consultar la especificación completa:

1. Instalar la [app OCS API viewer](https://apps.nextcloud.com/apps/ocs_api_viewer).
2. Instalar la app *assistant*.
3. Abrir **OCS API viewer** desde el menú de apps.
4. Seleccionar **assistant** en la barra lateral izquierda.

:::{note}
Actualmente, la API del asistente tiene endpoints separados para el procesamiento de texto, la conversión de voz a texto y la generación de imágenes. Se unificarán en una versión futura, lo que puede introducir cambios incompatibles.
:::

### Documentación relacionada

- Integración del lado del servidor: {nc-doc}`developer_manual/digging_deeper/task_processing`
- Integración en el frontend: {nc-doc}`developer_manual/digging_deeper/assistant_integration`
````
