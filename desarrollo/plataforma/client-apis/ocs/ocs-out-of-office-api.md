---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de ausencias (fuera de la oficina): consultar el período en curso o el próximo, modificar los datos y borrarlos, con campos y códigos."
---
(nc-dev-ocs-out-of-office-api)=
# API OCS de fuera de la oficina

## Resumen

Esta página describe, para quienes desarrollan clientes o apps, la API OCS de fuera de la oficina: los endpoints para consultar el período de ausencia en curso o el próximo, modificar esos datos y borrarlos, con sus campos y códigos de estado.

````{upstream} developer_manual/client_apis/OCS/ocs-out-of-office-api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

:::{versionadded} 28.0
:::

La API OCS de fuera de la oficina permite acceder a los datos de ausencia (fuera de la oficina) de los usuarios y modificarlos.

La URL base de todas las llamadas a la API de fuera de la oficina es: `<nextcloud_base_url>/ocs/v2.php/apps/dav/api/v1/outOfOffice`

Todas las llamadas a endpoints OCS requieren que la cabecera `OCS-APIRequest` tenga el valor `true`.

### Obtener los datos en curso

Obtener los datos del período de ausencia en curso de un usuario.

- Método: `GET`
- Endpoint: `/{userId}/now`
- Respuesta:
  - Código de estado:
    - `200 OK` Datos de ausencia
    - `404 Not Found` si el usuario no tiene un período de ausencia en curso
  - Datos (solo se envían si el código de estado es `200 OK`):

| campo | tipo | Descripción |
|---|---|---|
| `id` | string | ID en la base de datos de la entidad de datos de ausencia |
| `userId` | string | ID del usuario al que pertenecen los datos |
| `startDate` | int | Marca de tiempo de la fecha de inicio (según la zona horaria del userId) |
| `endDate` | int | Marca de tiempo de la fecha de término (según la zona horaria del userId) |
| `shortMessage` | string | Texto breve que se establece como estado del usuario durante la ausencia |
| `message` | string | Mensaje más largo, de varias líneas, que se muestra a otros durante la ausencia |
| `replacementUserId` | string/null | ID del usuario de reemplazo |
| `replacementUserDisplayName` | string/null | Nombre visible del usuario de reemplazo |

### Obtener los datos próximos o en curso

Puede que el período de ausencia devuelto aún no haya comenzado. Este endpoint devuelve los datos del período de
ausencia en curso o del próximo período de ausencia de un usuario.

- Método: `GET`
- Endpoint: `/{userId}`
- Respuesta:
  - Código de estado:
    - `200 OK` Datos de ausencia
    - `404 Not Found` si el usuario no programó un período de ausencia
  - Datos (solo se envían si el código de estado es `200 OK`):

| campo | tipo | Descripción |
|---|---|---|
| `id` | int | ID en la base de datos de la entidad de datos de ausencia |
| `userId` | string | ID del usuario al que pertenecen los datos |
| `firstDay` | string | Primer día de la ausencia, en formato `YYYY-MM-DD` |
| `lastDay` | string | Último día de la ausencia, en formato `YYYY-MM-DD` |
| `status` | string | Texto breve que se establece como estado del usuario durante la ausencia |
| `message` | string | Mensaje más largo, de varias líneas, que se muestra a otros durante la ausencia |
| `replacementUserId` | string/null | ID del usuario de reemplazo |
| `replacementUserDisplayName` | string/null | Nombre visible del usuario de reemplazo |

### Modificar los datos de ausencia

Solo es posible modificar los datos de ausencia del usuario que ha iniciado sesión.

- Método: `POST`
- Endpoint: `/{userId}`
- Datos:

| campo | tipo | Descripción |
|---|---|---|
| `firstDay` | string | Primer día de la ausencia, en formato `YYYY-MM-DD` |
| `lastDay` | string | Último día de la ausencia, en formato `YYYY-MM-DD` |
| `status` | string | Texto breve que se establece como estado del usuario durante la ausencia |
| `message` | string | Mensaje más largo, de varias líneas, que se muestra a otros durante la ausencia |
| `replacementUserId` | string/null | ID del usuario de reemplazo |
| `replacementUserDisplayName` | string/null | Nombre visible del usuario de reemplazo |

- Respuesta:
  - Código de estado:
    - `200 OK` Datos de ausencia actualizados
    - `400 Bad Request` si el primer día no es anterior al último día
    - `404 Not Found` si se proporciona un ID de usuario de reemplazo pero no se encuentra el usuario correspondiente
    - `401 Unauthorized` si el usuario no ha iniciado sesión
  - Datos (solo se envían si el código de estado es `200 OK`):

| campo | tipo | Descripción |
|---|---|---|
| `id` | int | ID en la base de datos de la entidad de datos de ausencia |
| `userId` | string | ID del usuario al que pertenecen los datos |
| `firstDay` | string | Primer día de la ausencia, en formato `YYYY-MM-DD` |
| `lastDay` | string | Último día de la ausencia, en formato `YYYY-MM-DD` |
| `status` | string | Texto breve que se establece como estado del usuario durante la ausencia |
| `message` | string | Mensaje más largo, de varias líneas, que se muestra a otros durante la ausencia |
| `replacementUserId` | string/null | ID del usuario de reemplazo |
| `replacementUserDisplayName` | string/null | Nombre visible del usuario de reemplazo |

### Borrar los datos y desactivar la ausencia

Solo es posible borrar los datos de ausencia del usuario que ha iniciado sesión.

- Método: `DELETE`
- Endpoint: `/{userId}`
- Respuesta:
  - Código de estado:
    - `200 OK` Se borraron los datos de ausencia
    - `401 Unauthorized` si el usuario no ha iniciado sesión
````
