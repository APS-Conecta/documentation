---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de procesamiento de texto, obsoleta desde la versión 30: obtener los tipos de tarea, programar tareas y obtenerlas por ID."
---
(nc-dev-ocs-textprocessing-api)=
# API OCS de procesamiento de texto

## Resumen

Esta página describe, para quienes desarrollan clientes o apps, la API OCS de procesamiento de texto, obsoleta desde la versión 30 en favor de la API TaskProcessing: los endpoints para obtener los tipos de tarea disponibles, programar una tarea y obtenerla por ID, con sus campos y códigos de estado.

````{upstream} developer_manual/client_apis/OCS/ocs-textprocessing-api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

:::{versionadded} 27.1.0
:::

:::{deprecated} 30
Usar en su lugar la API TaskProcessing
:::

La API OCS de procesamiento de texto permite ejecutar tareas de procesamiento de texto, como enviar instrucciones a modelos de lenguaje grandes, que implementan apps mediante {nc-ref}`la API de procesamiento de texto del backend <text_processing>`.

La URL base de todas las llamadas a esta API es: `<nextcloud_base_url>/ocs/v2.php/textprocessing/`

Todas las llamadas a endpoints OCS requieren que la cabecera `OCS-APIRequest` tenga el valor `true`.

### Obtener los tipos de tarea disponibles

:::{versionadded} 27.1.0
:::

- Método: `GET`
- Endpoint: `/tasktypes`
- Respuesta:
  - Código de estado:
    - `200 OK`
  - Datos:

| campo | tipo | Descripción |
|---|---|---|
| `types` | array | Una lista de los tipos de tarea admitidos. Ver más abajo. |

Campos de un tipo de tarea:

| campo | tipo | Descripción |
|---|---|---|
| `name` | string | El nombre del tipo de tarea en el idioma del usuario |
| `description` | string | Una descripción del tipo de tarea en el idioma del usuario |
| `id` | string | El id de este tipo de tarea |

### Programar una tarea

:::{versionadded} 28
:::

:::{note}
El endpoint tiene un límite de frecuencia de solicitudes, ya que puede consumir bastantes recursos. Los usuarios pueden hacer 20 solicitudes en 2 minutos; los invitados, solo 5
:::

- Método: `POST`
- Endpoint: `/schedule`
- Datos:

| campo | tipo | Descripción |
|---|---|---|
| `input` | string | El texto de entrada de la tarea |
| `type` | string | Id del tipo de esta tarea. |
| `appId` | string | El id de la app que hace la solicitud |
| `identifier` | string | Un identificador de la tarea definido por la app |

- Respuesta:
  - Código de estado:
    - `200 OK`
    - `400 Bad Request` - Cuando el tipo de tarea no es válido
    - `412 Precondition Failed` - Cuando el tipo de tarea no está disponible en este momento
    - `429 Too Many Requests` - Cuando se superó el límite de frecuencia de solicitudes
  - Datos:
    - `input` - Solo se proporciona en caso de `200 OK`, la entrada de la tarea, string
    - `type` - Solo se proporciona en caso de `200 OK`, el tipo de la tarea, string
    - `id` - Solo se proporciona en caso de `200 OK`, el id asignado a la tarea, int
    - `status` - Solo se proporciona en caso de `200 OK`, el estado actual de la tarea, int, ver la API del backend
    - `userId` - Solo se proporciona en caso de `200 OK`, el userId de origen de la tarea, string
    - `appId` - Solo se proporciona en caso de `200 OK`, el appId de origen de la tarea, string
    - `identifier` - Solo se proporciona en caso de `200 OK`, el appId de origen de la tarea, string
    - `output` - Solo se proporciona en caso de `200 OK`, la salida del modelo, string o null
    - `message` - Solo se proporciona cuando no es `200 OK`, un mensaje de error en el idioma del usuario, listo para mostrarse

### Obtener una tarea por ID

:::{versionadded} 28
:::

:::{note}
El endpoint tiene un límite de frecuencia de solicitudes, ya que puede consumir bastantes recursos. Los usuarios pueden hacer 20 solicitudes en 2 minutos; los invitados, solo 5
:::

- Método: `POST`
- Endpoint: `/task/{id}`
- Respuesta:
  - Código de estado:
    - `200 OK`
    - `404 Not Found` - Cuando no se encontró la tarea
  - Datos:
    - `input` - Solo se proporciona en caso de `200 OK`, la entrada de la tarea, string
    - `type` - Solo se proporciona en caso de `200 OK`, el tipo de la tarea, string
    - `id` - Solo se proporciona en caso de `200 OK`, el id asignado a la tarea, int
    - `status` - Solo se proporciona en caso de `200 OK`, el estado actual de la tarea, int, ver la API del backend
    - `userId` - Solo se proporciona en caso de `200 OK`, el userId de origen de la tarea, string
    - `appId` - Solo se proporciona en caso de `200 OK`, el appId de origen de la tarea, string
    - `identifier` - Solo se proporciona en caso de `200 OK`, el appId de origen de la tarea, string
    - `output` - Solo se proporciona en caso de `200 OK`, la salida del modelo, string o null
    - `message` - Solo se proporciona cuando no es `200 OK`, un mensaje de error en el idioma del usuario, listo para mostrarse
````
