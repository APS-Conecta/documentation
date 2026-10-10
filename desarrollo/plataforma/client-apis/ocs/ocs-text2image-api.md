---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de texto a imagen: comprobar la disponibilidad, programar, obtener, eliminar y listar tareas de generación de imágenes, y obtener sus imágenes."
---
(nc-dev-ocs-text2image-api)=
# API OCS de texto a imagen

## Resumen

Esta página describe, para quienes desarrollan clientes o apps, la API OCS de texto a imagen: los endpoints para comprobar su disponibilidad, programar tareas de generación de imágenes, obtenerlas, eliminarlas, listarlas por app y descargar las imágenes resultantes, con sus campos y códigos de estado.

````{upstream} developer_manual/client_apis/OCS/ocs-text2image-api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

:::{versionadded} 28
:::

La API OCS de texto a imagen permite ejecutar tareas de generación de imágenes que implementan apps mediante {nc-ref}`la API de texto a imagen del backend <text2image>`.

La URL base de todas las llamadas a esta API es: `<nextcloud_base_url>/ocs/v2.php/text2image/`

Todas las llamadas a endpoints OCS requieren que la cabecera `OCS-APIRequest` tenga el valor `true`.

### Comprobar la disponibilidad

:::{versionadded} 28
:::

- Método: `GET`
- Endpoint: `/is_available`
- Respuesta:
  - Código de estado:
    - `200 OK`
  - Datos:

| campo | tipo | Descripción |
|---|---|---|
| `isAvailable` | bool | Booleano que indica si hay instalado algún proveedor de texto a imagen |

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
| `numberOfImages` | int | El número de imágenes que se generarán (opcional; valor predeterminado: 8) |
| `appId` | string | El id de la app que hace la solicitud |
| `identifier` | string | Un identificador de la tarea definido por la app (opcional) |

Si es posible, la tarea se ejecuta mientras el servidor procesa la solicitud; de lo contrario, se programa como trabajo en segundo plano.

- Respuesta:
  - Código de estado:
    - `200 OK`
    - `412 Precondition Failed` - Cuando el tipo de tarea no está disponible en este momento
    - `429 Too Many Requests` - Cuando se superó el límite de frecuencia de solicitudes
  - Datos:
    - `id` - Solo se proporciona en caso de `200 OK`, el id asignado a la tarea, int
    - `input` - Solo se proporciona en caso de `200 OK`, la entrada de la tarea, string
    - `status` - Solo se proporciona en caso de `200 OK`, el estado actual de la tarea, int, ver {nc-ref}`la API de texto a imagen del backend <text2image_statuses>`
    - `userId` - Solo se proporciona en caso de `200 OK`, el userId de origen de la tarea, string
    - `appId` - Solo se proporciona en caso de `200 OK`, el appId de origen de la tarea, string
    - `identifier` - Solo se proporciona en caso de `200 OK`, el appId de origen de la tarea, string
    - `numberOfImages` - Solo se proporciona en caso de `200 OK`, el número de imágenes generadas, int
    - `completionExpectedAt` - Solo se proporciona en caso de `200 OK`, la fecha y hora en que se espera que el resultado esté completo, como marca de tiempo UNIX, int
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
    - `id` - Solo se proporciona en caso de `200 OK`, el id asignado a la tarea, int
    - `input` - Solo se proporciona en caso de `200 OK`, la entrada de la tarea, string
    - `status` - Solo se proporciona en caso de `200 OK`, el estado actual de la tarea, int, ver {nc-ref}`la API de texto a imagen del backend <text2image_statuses>`
    - `userId` - Solo se proporciona en caso de `200 OK`, el userId de origen de la tarea, string
    - `appId` - Solo se proporciona en caso de `200 OK`, el appId de origen de la tarea, string
    - `identifier` - Solo se proporciona en caso de `200 OK`, el appId de origen de la tarea, string
    - `numberOfImages` - Solo se proporciona en caso de `200 OK`, el número de imágenes generadas, int
    - `completionExpectedAt` - Solo se proporciona en caso de `200 OK`, la fecha y hora en que se espera que el resultado esté completo, como marca de tiempo UNIX, int
    - `message` - Solo se proporciona cuando no es `200 OK`, un mensaje de error en el idioma del usuario, listo para mostrarse

### Obtener una imagen de resultado

:::{versionadded} 28
:::

- Método: `POST`
- Endpoint: `/task/{id}/image/{index}`
  - `index`: El índice de la imagen, empezando en 0
- Respuesta:
  - Código de estado:
    - `200 OK`
    - `404 Not Found` - Cuando no se encontró la tarea, no tuvo éxito, aún no se completó o el índice está fuera de rango
  - Datos: Los datos de la imagen sin procesar

### Eliminar una tarea

:::{versionadded} 28
:::

- Método: `DELETE`
- Endpoint: `/task/{id}`
- Respuesta:
  - Código de estado:
    - `200 OK`
    - `404 Not Found` - Cuando no se encontró la tarea
  - Datos:
    - `id` - Solo se proporciona en caso de `200 OK`, el id asignado a la tarea, int
    - `input` - Solo se proporciona en caso de `200 OK`, la entrada de la tarea, string
    - `status` - Solo se proporciona en caso de `200 OK`, el estado actual de la tarea, int, ver {nc-ref}`la API de texto a imagen del backend <text2image_statuses>`
    - `userId` - Solo se proporciona en caso de `200 OK`, el userId de origen de la tarea, string
    - `appId` - Solo se proporciona en caso de `200 OK`, el appId de origen de la tarea, string
    - `identifier` - Solo se proporciona en caso de `200 OK`, el appId de origen de la tarea, string
    - `numberOfImages` - Solo se proporciona en caso de `200 OK`, el número de imágenes generadas, int
    - `completionExpectedAt` - Solo se proporciona en caso de `200 OK`, la fecha y hora en que se espera que el resultado esté completo, como marca de tiempo UNIX, int
    - `message` - Solo se proporciona cuando no es `200 OK`, un mensaje de error en el idioma del usuario, listo para mostrarse

### Listar las tareas por app

:::{versionadded} 28
:::

:::{note}
El endpoint tiene un límite de frecuencia de solicitudes, ya que puede consumir bastantes recursos. Los invitados solo pueden hacer 5 solicitudes en 2 minutos
:::

- Método: `DELETE`
- Endpoint: `/tasks/app/{appId}`
- Datos:

| campo | tipo | Descripción |
|---|---|---|
| `appId` | string | El id de la app que hace la solicitud |
| `identifier` | string | Un identificador de la tarea definido por la app (opcional) |

- Respuesta:
  - Código de estado:
    - `200 OK`
    - `404 Not Found` - Cuando no se encontró la tarea
  - Datos:
    - Solo se proporciona en caso de `200 OK`, un array de objetos:
      - `id` - el id asignado a la tarea, int
      - `input` - la entrada de la tarea, string
      - `status` - el estado actual de la tarea, int, ver {nc-ref}`la API de texto a imagen del backend <text2image_statuses>`
      - `userId` - el userId de origen de la tarea, string
      - `appId` - el appId de origen de la tarea, string
      - `identifier` - el appId de origen de la tarea, string
      - `numberOfImages` - el número de imágenes generadas, int
      - `completionExpectedAt` - la fecha y hora en que se espera que el resultado esté completo, como marca de tiempo UNIX, int
    - `message` - Solo se proporciona cuando no es `200 OK`, un mensaje de error en el idioma del usuario, listo para mostrarse
````
