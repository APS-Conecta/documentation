---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo integrar el asistente en el frontend web de otra app: mostrar el resultado de una tarea, abrir el formulario y rellenar la entrada desde un archivo."
---
(nc-dev-assistant-integration)=
# Integrar el asistente

## Resumen

Esta página explica cómo integrar el asistente en el frontend web de otras aplicaciones: mostrar el resultado de una tarea, ejecutar una tarea con `OCA.Assistant.openAssistantForm` y sus opciones, y rellenar la entrada a partir de un archivo. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/assistant_integration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Esta sección trata la integración del asistente de Nextcloud en el frontend web de otras aplicaciones de Nextcloud. Para la integración en el backend mediante la API OCP de procesamiento de tareas, ver {nc-doc}`developer_manual/digging_deeper/task_processing`. Para la API OCS, ver {nc-doc}`developer_manual/client_apis/OCS/ocs-assistant-api`.

### Mostrar el resultado de una tarea

Hay dos formas de mostrar el resultado de una tarea con el asistente.

#### Abrir el modal del asistente

Si se tiene un objeto de tarea obtenido del endpoint OCS `/ocs/v2.php/apps/assistant/api/v1/task/TASK_ID` o `/ocs/v2.php/apps/assistant/api/v1/tasks`, pasarlo a la función auxiliar `OCA.Assistant.openAssistantTask`. Esto abre el modal del asistente con el tipo de tarea, la entrada y la salida ya cargados.

#### Ver la página del resultado de la tarea

Hay una página independiente disponible en `/apps/assistant/task/view/TASK_ID`. Renderiza el mismo contenido que el modal del asistente.

### Ejecutar una tarea

Usar `OCA.Assistant.openAssistantForm` para abrir el modal del asistente desde la aplicación. La función acepta un único objeto de configuración con las siguientes claves:

:::{list-table} Opciones de `openAssistantForm`
:header-rows: 1
:widths: 20 10 70

* - Clave
  - Obligatoria
  - Descripción
* - `appId`
  - Sí
  - ID de la aplicación que hace la llamada.
* - `customId`
  - No
  - Identificador personalizado de la tarea; útil para correlacionar el evento de backend `task finished` con la llamada que lo originó. El valor predeterminado es `''`.
* - `taskType`
  - No
  - Tipo de tarea seleccionado inicialmente (p. ej., `core:text2text`, `speech-to-text`, `OCP\TextToImage\Task`). El valor predeterminado es el último tipo de tarea usado.
* - `input`
  - No
  - Objeto que contiene los valores iniciales de entrada, específicos de cada tipo de tarea. El valor predeterminado es `{}`.
* - `isInsideViewer`
  - No
  - Establecer en `true` si la función se llama mientras el Viewer está abierto. El valor predeterminado es `false`.
* - `closeOnResult`
  - No
  - Si es `true`, el modal se cierra después de que una tarea síncrona se completa y los resultados están disponibles. El valor predeterminado es `false`.
* - `actionButtons`
  - No
  - Lista de botones adicionales que se muestran en el formulario de resultados. Solo se usa cuando `closeOnResult` es `false`. El valor predeterminado es una lista vacía.
:::

La función devuelve una Promise que se resuelve cuando se cierra el modal, ya sea porque se programó una tarea o porque una tarea síncrona se ejecutó y produjo resultados. La promesa se resuelve con un objeto de tarea:

```javascript
{
    appId: 'text',
    id: 310,
    customId: 'my custom identifier',
    input: { input: 'give me a short summary of a simple settings section about GitHub' },
    ocpTaskId: 152,
    output: { output: 'blabla' },
    status: 'STATUS_SUCCESSFUL',
    type: 'core:text2text',
    lastUpdated: 1711545305,
    scheduledAt: 1711545301,
    startedAt: 1711545302,
    endedAt: 1711545303,
    userId: 'janedoe',
}
```

Los valores posibles de `status` son: `STATUS_UNKNOWN` (0), `STATUS_SCHEDULED` (1), `STATUS_RUNNING` (2), `STATUS_SUCCESSFUL` (3), `STATUS_FAILED` (4).

Ejemplo completo:

```javascript
OCA.Assistant.openAssistantForm({
    appId: 'my_app_id',
    customId: 'my custom identifier',
    taskType: 'core:text2text',
    inputs: { input: 'count to 3' },
    actionButtons: [
        {
            label: 'Label 1',
            title: 'Title 1',
            variant: 'warning',
            iconSvg: cogSvg,
            onClick: (output) => { console.debug('first button clicked', output) },
        },
        {
            label: 'Label 2',
            title: 'Title 2',
            onClick: (output) => { console.debug('second button clicked', output) },
        },
    ],
}).then(task => {
    console.debug('assistant promise success', task)
}).catch(error => {
    console.debug('assistant promise failure', error)
})
```

### Rellenar la entrada a partir de un archivo

Se puede rellenar de antemano un campo de entrada de la tarea con el contenido de un archivo pasando un `fileId` o un `filePath` en lugar de un valor de cadena simple:

```javascript
OCA.Assistant.openAssistantForm({
    appId: 'my_app_id',
    customId: 'my custom identifier',
    taskType: 'core:text2text',
    inputs: { input: { fileId: 123 } },
})

OCA.Assistant.openAssistantForm({
    appId: 'my_app_id',
    customId: 'my custom identifier',
    taskType: 'core:text2text',
    inputs: { input: { filePath: '/path/to/file.txt' } },
})
```
````
