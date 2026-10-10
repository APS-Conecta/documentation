---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Métodos del ciclo de vida de una ExApp (healthcheck, /heartbeat, /init, /enabled), sus tiempos de espera, el esquema del ciclo y la autenticación AppAPIAuth."
---
(nc-dev-ex_app_lifecycle)=
# Ciclo de vida de una ExApp

## Resumen

Esta página describe las reglas de comunicación entre Nextcloud y una ExApp: los manejadores healthcheck, /heartbeat, /init y /enabled con sus respuestas y tiempos de espera, el esquema del ciclo de vida, los métodos del lado de Nextcloud y la autenticación. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/development_overview/ExAppLifecycle.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El ciclo de vida de una ExApp es un conjunto de reglas de comunicación (o protocolos) entre Nextcloud y la ExApp.
Son necesarias por la arquitectura de microservicios de las ExApps.
Esta sección es una visión general; hay más detalles aquí: {nc-ref}`app_installation_flow`, {nc-ref}`app_deployment`.

(nc-dev-ex_app_lifecycle_methods)=
### Métodos del ciclo de vida de una ExApp

Cuando la ExApp se instala en Nextcloud, ocurren varios pasos del ciclo de vida.
El ciclo de vida de la ExApp requiere los siguientes manejadores de endpoints de API (en orden):

0. `healthcheck`: comprobación de estado del contenedor Docker
1. `/heartbeat`: **[obligatorio]** manejador de latido (heartbeat) de la ExApp
2. `/init`: **[opcional]** manejador de inicialización de la ExApp
3. `/enabled`: **[obligatorio]** manejador de habilitación/deshabilitación de la ExApp

#### Comprobación de estado (healthcheck)

Docker permite definir un script personalizado de comprobación de estado (healthcheck) para el contenedor (especificado en el Dockerfile).
Aquí se puede definir cualquier lógica personalizada de arranque del contenedor, si es necesario.

:::{note}
El tiempo de espera del healthcheck de AppAPI es de 15 minutos.
:::

#### Latido (heartbeat)

Nextcloud llama periódicamente al método `GET /heartbeat` para comprobar el estado de salud de la ExApp,
es decir, si su servidor web está en ejecución y recibiendo solicitudes.

URL: `GET http://localhost:2345/heartbeat`

AppAPI espera una respuesta con el estado HTTP 200.
Este paso falla si la ExApp no responde en 10 minutos.

:::{note}
Este endpoint debe estar disponible **sin autenticación AppAPIAuth**.
Hay un tiempo de espera de 10 minutos para que la ExApp arranque y responda a la solicitud `/heartbeat`.
:::

(nc-dev-ex_app_lifecycle_init)=
#### Inicialización (init)

El endpoint `POST /init` se llama después de que la ExApp se habilita en Nextcloud.
Es un disparador para que la ExApp inicie su proceso de inicialización, p. ej., descargar modelos, datos iniciales, etc.

:::{note}
El tiempo de espera de inicialización predeterminado (`init_timeout`) es de 40 minutos. Puede cambiarse en los ajustes de administración de AppAPI
o mediante el comando `occ config:app:set app_api init_timeout --value 40 --type mixed`.
:::

URL: `POST http://localhost:2345/init`

AppAPI espera una respuesta con el estado HTTP 200.

:::{note}
Aunque la ExApp no implemente el endpoint `/init` y AppAPI reciba una respuesta `HTTP 501 NOT IMPLEMENTED` o `HTTP 404 NOT FOUND`,
AppAPI puede igualmente habilitar la ExApp.
:::

La ExApp debe actualizar el progreso de la inicialización mediante la solicitud a la API `PUT /ocs/v2.php/apps/app_api/ex-app/status`
con una carga útil `{ "progress": <number> }`.

#### Habilitación (enabled)

El método `PUT /enabled?enabled=1|0` se llama cuando la ExApp se habilita o se deshabilita en Nextcloud.
El parámetro de consulta `enabled` se usa para determinar el estado de la ExApp: 1 - habilitada, 0 - deshabilitada.

- `PUT http://localhost:2345/enabled?enabled=1` - habilitar la ExApp; durante esta llamada, la ExApp debe registrar todas las API necesarias
- `PUT http://localhost:2345/enabled?enabled=0` - deshabilitar la ExApp; durante esta llamada, la ExApp debe anular el registro de todas las API

AppAPI espera una respuesta con el estado HTTP 200. Cualquier otro código de estado se considerará un error.

:::{note}
El tiempo de espera de AppAPI para el manejador `enabled` es de 30 segundos.
:::

### Esquema del ciclo de vida de una ExApp

A continuación se revisa un esquema sencillo del ciclo de vida de una ExApp:
un diagrama de secuencia con las llamadas de Nextcloud a /heartbeat, /init y /enabled (con 1 y con 0), y cómo la ExApp responde con HTTP 200, informa del progreso de la inicialización y registra o anula el registro de sus API mediante la API OCS.

### Métodos del ciclo de vida de una ExApp del lado de Nextcloud

Los métodos del ciclo de vida de la ExApp del lado de Nextcloud son las API OCS.
Las API OCS de Nextcloud disponibles en AppAPI pueden consultarse {nc-ref}`aquí <app_api_nextcloud_apis>`.

:::{note}
La ExApp debe registrar todas las API necesarias durante la llamada al método `enabled`,
como la interfaz de usuario ({nc-ref}`top-menu <top_menu_section>`, {nc-ref}`filesactionmenu <file_actions_menu_section>`), los {nc-ref}`comandos occ <occ_command>`, etc.
:::

### Autenticación de AppAPI

Las solicitudes de Nextcloud a la ExApp se protegen con {nc-doc}`AppAPIAuth <developer_manual/exapp_development/tech_details/Authentication>`.
La ExApp debe validar la autenticación con el mismo algoritmo que usa AppAPI.

:::{note}
Corresponde a quien desarrolla aplicar límites de frecuencia, protección contra ataques de fuerza bruta y otras medidas de seguridad
en los endpoints de la API de la ExApp.
:::

#### Cookies

Además de AppAPIAuth, la ExApp puede usar las cookies de Nextcloud del usuario autenticado
que hizo la solicitud a la ExApp.
````
