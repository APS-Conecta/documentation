---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de estado del usuario: consultar y cambiar el estado propio y sus mensajes, estados predefinidos, estados de otros usuarios y respaldo."
---
# API OCS de estado

## Resumen

Esta página describe, para quienes desarrollan clientes o apps, la API OCS de estado del usuario: los endpoints para consultar y modificar el estado propio y sus mensajes, listar los estados predefinidos, obtener los estados de otros usuarios y restaurar un estado de respaldo.

````{upstream} developer_manual/client_apis/OCS/ocs-status-api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

La API OCS de estado permite acceder a la API de estado y modificarla desde fuera mediante llamadas OCS predefinidas.

La URL base de todas las llamadas a la API de estado es: `<nextcloud_base_url>/ocs/v2.php/apps/user_status/api/v1/user_status`

Todas las llamadas a endpoints OCS requieren que la cabecera `OCS-APIRequest` tenga el valor `true`.

### Estado del usuario: manipulación del estado

#### Obtener el estado propio

- Capacidad requerida: `user_status`
- Método: `GET`
- Endpoint: `/`
- Respuesta:
  - Código de estado:
    - `200 OK`
    - `404 Not Found` si el usuario no tiene un estado establecido

#### Establecer el estado propio

- Capacidad requerida: `user_status`
- Método: `PUT`
- Endpoint: `/status`
- Datos:

| campo | tipo | Descripción | Valores permitidos |
|---|---|---|---|
| `statusType` | string | Nuevo estado del usuario autenticado | `online`, `away`, `dnd`, `invisible`, `offline` |

- Respuesta:
  - Código de estado:
    - `200 OK`
    - `400 Bad Request` si el tipo de estado enviado no es válido

#### Establecer un mensaje personalizado (predefinido)

- Capacidad requerida: `user_status`
- Método: `PUT`
- Endpoint: `/message/predefined`
- Datos:

| campo | tipo | Descripción |
|---|---|---|
| `messageId` | string | Message-Id del mensaje predefinido |
| `clearAt` | int | Marca de tiempo Unix que representa el momento en que se borra el estado |

- Respuesta:
  - Código de estado:
    - `200 OK`
    - `400 Bad Request` si el messageId enviado no existe
    - `400 Bad Request` si la marca de tiempo Unix está en el pasado

#### Establecer un mensaje personalizado (definido por el usuario)

- Capacidad requerida: `user_status`, `supports_emoji` para admitir `statusIcon`
- Método: `PUT`
- Endpoint: `/message/custom`
- Datos:

| campo | tipo | Descripción |
|---|---|---|
| `statusIcon` | string/null | El icono elegido por el usuario (debe ser un emoji, como máximo uno) |
| `message` | string | El mensaje personalizado elegido por el usuario |
| `clearAt` | int | Marca de tiempo Unix que representa el momento en que se borra el estado |

- Respuesta:
  - Código de estado:
    - `200 OK`
    - `400 Bad Request` si *statusIcon* no es un emoji o es más de un emoji
    - `400 Bad Request` si *message* es demasiado largo
    - `400 Bad Request` si la marca de tiempo Unix está en el pasado

#### Borrar el mensaje

- Capacidad requerida: `user_status`
- Método: `DELETE`
- Endpoint: `/message`
- Respuesta:
  - Código de estado:
    - `200 OK`

### Estado del usuario: estados predefinidos

Endpoint base: `/ocs/v2.php/apps/user_status/api/v1/predefined_statuses`

#### Obtener la lista de estados predefinidos

- Capacidad requerida: `user_status`
- Método: `GET`
- Endpoint: `/`
- Respuesta:
  - Código de estado:
    - `200 OK`

### Estado del usuario: obtener estados

Endpoint base: `/ocs/v2.php/apps/user_status/api/v1/statuses`

#### Obtener una lista de todos los estados de usuario establecidos

- Capacidad requerida: `user_status`
- Método: `GET`
- Endpoint: `/`
- Datos:

| campo | tipo | Descripción |
|---|---|---|
| `limit` | int | Límite para la paginación |
| `offset` | int | Desplazamiento para la paginación |

- Respuesta:
  - Código de estado:
    - `200 OK`

#### Obtener el estado de un usuario concreto

- Capacidad requerida: `user_status`
- Método: `GET`
- Endpoint: `/{userId}`
- Respuesta:
  - Código de estado:
    - `200 OK`
    - `404 Not Found` si el usuario no tiene un estado establecido

#### Obtener el estado de respaldo de un usuario

En algunos escenarios el estado del usuario puede sobrescribirse automáticamente, p. ej., al unirse a una llamada en Nextcloud Talk
o cuando la automatización de disponibilidad está activada. En ese caso el userId puede llevar como prefijo un guion bajo *_*
para obtener el estado original del usuario. Cuando se devuelve un estado de usuario y la capacidad `user_status` > `restore`
está disponible, el estado de respaldo debe añadirse como un elemento de la lista de estados predefinidos. Al hacer clic en él,
debería hacerse una llamada a la API [Estado del usuario: restaurar el respaldo](#ocs-status-api-user-status-restore-backup).

- Capacidad requerida: `user_status`
- Método: `GET`
- Endpoint: `/_{userId}`
- Respuesta:
  - Código de estado:
    - `200 OK`
    - `404 Not Found` si el usuario no tiene un estado de respaldo establecido

#### Uso compartido de archivos

El estado del usuario también se expone mediante las siguientes API de uso compartido de archivos:

- `GET /ocs/v2.php/apps/files_sharing/api/v1/sharees`
- `GET /ocs/v2.php/apps/files_sharing/api/v1/sharees_recommended`
- `GET /ocs/v2.php/apps/files_sharing/api/v1/shares`
- `GET /ocs/v2.php/apps/files_sharing/api/v1/shares/inherited`
- `GET /ocs/v2.php/apps/files_sharing/api/v1/shares/pending`
- `GET /ocs/v2.php/apps/files_sharing/api/v1/shares/{id}`
- `POST /ocs/v2.php/apps/files_sharing//api/v1/shares`
- `PUT /ocs/v2.php/apps/files_sharing/api/v1/shares/{id}`

(ocs-status-api-user-status-restore-backup)=
### Estado del usuario: restaurar el respaldo

- Capacidad requerida: `user_status` > `restore`
- Método: `DELETE`
- Endpoint: `/revert/{messageId}`
- Respuesta:
  - Código de estado:
    - `200 OK`
````
