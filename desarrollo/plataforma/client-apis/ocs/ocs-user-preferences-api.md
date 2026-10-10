---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de preferencias de usuario: establecer y eliminar una o varias preferencias de una app, con sus datos y códigos de estado."
---
# API OCS de preferencias de usuario

## Resumen

Esta página describe, para quienes desarrollan clientes o apps, la API OCS de preferencias de usuario: los endpoints para establecer y eliminar una o varias preferencias de una app, con sus datos y códigos de estado.

````{upstream} developer_manual/client_apis/OCS/ocs-user-preferences-api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

La API OCS de preferencias de usuario permite establecer y eliminar preferencias desde fuera mediante llamadas OCS predefinidas.

La URL base de todas las llamadas a la API de preferencias de usuario es: `<nextcloud_base_url>/ocs/v2.php/apps/provisioning_api/api/v1/config/users/`

Todas las llamadas a endpoints OCS requieren que la cabecera `OCS-APIRequest` tenga el valor `true`.

### Establecer una preferencia

- Método: `POST`
- Endpoint: `/{appId}/{configKey}`
- Datos:

| campo | tipo | Descripción |
|---|---|---|
| configValue | string | El valor que se asignará a la preferencia |

- Respuesta:
  - Código de estado:
    - `200 OK`
    - `400 Bad Request` Si la preferencia no se puede modificar o el valor indicado no es válido
    - `401 Unauthorized` Si la solicitud no la hace un usuario

### Establecer varias preferencias

- Método: `POST`
- Endpoint: `/{appId}`
- Datos:

| campo | tipo | Descripción |
|---|---|---|
| config | array | Pares clave-valor de conjuntos de configuración con configKey (string) => configValue (string) |

- Respuesta:
  - Código de estado:
    - `200 OK`
    - `400 Bad Request` Si alguna preferencia no se puede modificar o el valor no es válido. No se modificará ninguna preferencia.
    - `401 Unauthorized` Si la solicitud no la hace un usuario

### Eliminar una preferencia

- Método: `DELETE`
- Endpoint: `/{appId}/{configKey}`
- Respuesta:
  - Código de estado:
    - `200 OK`
    - `400 Bad Request` Si la preferencia no se puede eliminar
    - `401 Unauthorized` Si la solicitud no la hace un usuario

### Eliminar varias preferencias

- Método: `DELETE`
- Endpoint: `/{appId}`
- Datos:

| campo | tipo | Descripción |
|---|---|---|
| configKeys | array | Lista de configKeys (string) que se eliminarán |

- Respuesta:
  - Código de estado:
    - `200 OK`
    - `400 Bad Request` Si alguna preferencia no se puede eliminar. No se eliminará ninguna preferencia.
    - `401 Unauthorized` Si la solicitud no la hace un usuario
````
