---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Comandos occ taskprocessing para inspeccionar y depurar tareas de IA: obtener una tarea por su ID, sus campos y listar y filtrar tareas."
---
# Inspección y depuración

## Resumen

Esta página reúne, para quienes administran el servidor, los comandos occ del espacio de nombres taskprocessing que sirven para inspeccionar y depurar las tareas de IA: obtener una tarea por su ID, los campos de cada tarea y cómo listar y filtrar tareas. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/insight_and_debugging.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

(nc-ai-insight-and-debugging)=
Para obtener información sobre las tareas de IA y depurarlas, hay varios comandos occ
disponibles en el espacio de nombres *taskprocessing*.

Todos los comandos que se enumeran aquí aceptan un parámetro *--output* que puede fijarse en *plain*, *json* o *json_pretty*.

Las tareas se conservan en la base de datos durante 6 meses. Sin embargo, hay que tener en cuenta que no existe una garantía estricta de solo escritura para estos registros.
Esto significa que Nextcloud no modificará los registros de tareas en la base de datos una vez terminada la tarea, pero cualquier administrador con acceso a la base de datos tiene la capacidad de modificarlos.

### Obtener una tarea por su ID

```
$ occ taskprocessing:task:get <task-id>
```

Por ejemplo

```
$ occ taskprocessing:task:get --output=json_pretty 42
{
  "id": 1,
  "type": "core:text2text:chat",
  "lastUpdated": 1759739466,
  "status": "STATUS_SUCCESSFUL",
  "userId": "admin",
  "appId": "assistant:chatty-llm",
  "input": {
    "system_prompt": "This is a conversation in a specific language between the user and you, Nextcloud Assistant. You are a kind, polite and helpful AI that helps the user to the best of its abilities. If you do not understand something, you will ask for clarification. Detect the language that the user is using. Make sure to use the same language in your response. Do not mention the language explicitly.",
    "input": "What's the weather in Berlin today?",
    "history": []
  },
  "output": {
    "output": "I'm happy to help, but I'm a large language model, I don't have real-time access to current weather conditions. However, I can suggest checking a reliable weather website or app, such as AccuWeather or OpenWeatherMap, for the most up-to-date information on the weather in Karlsruhe today. Would you like me to help with anything else?"
  },
  "customId": "chatty-llm:1",
  "completionExpectedAt": 1759739513,
  "progress": 1,
  "scheduledAt": 1759739453,
  "startedAt": 1759739455,
  "endedAt": 1759739466,
  "allowCleanup": true,
  "error_message": null
}
```

Cada tarea tiene los siguientes campos:

- *id* El ID interno de la tarea, al que también se hace referencia en los mensajes de error que ve el usuario cuando algo sale mal
- *type* El tipo de la tarea
- *status* El estado actual de la tarea (puede ser *"STATUS_CANCELLED"*, *"STATUS_FAILED"*, *"STATUS_SUCCESSFUL"*, *"STATUS_SCHEDULED"*, *"STATUS_RUNNING"* o *"STATUS_UNKNOWN"*)
- *userId* El ID del usuario que solicitó la tarea
- *lastUpdated* Cuándo se actualizó la tarea por última vez
- *scheduledAt* Cuándo se programó o creó la tarea
- *startedAt* Cuándo el proveedor de procesamiento de tareas configurado empezó a procesar la tarea
- *completionExpectedAt* Cuándo espera o esperaba el sistema que la tarea terminara
- *endedAt* Cuándo terminó la tarea, con éxito o sin él
- *appid* El ID de la app que programó la tarea
- *input* Los valores que formaban parte de la entrada de la tarea
- *output* Los valores que formaban parte de la salida de la tarea
- *error_message* El mensaje de error en caso de que la tarea haya fallado

### Listar y filtrar tareas

```
$ occ taskprocessing:task:list [options]

-u, --userIdFilter[=USERIDFILTER]        only get the tasks for one user ID
-t, --type[=TYPE]                        only get the tasks for one task type
    --appId[=APPID]                      only get the tasks for one app ID
    --customID[=CUSTOMID]                only get the tasks for one custom ID
-s, --status[=STATUS]                    only get the tests that have a specific status
    --scheduledAfter[=SCHEDULEDAFTER]    only get the tasks that were scheduled after a specific date (Unix timestamp)
    --endedBefore[=ENDEDBEFORE]          only get the tasks that ended before a specific date (Unix timestamp)
```

Por ejemplo

```
$ occ taskprocessing:task:list --output=json_pretty --status=3 --scheduledAfter=1759740266 --endedBefore=1759743900
[
  {
     ...
  }
]
```
````
