---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Integrar el motor de flujos de trabajo Windmill: instalación, conexión del espacio de trabajo, disparadores, scripts, autenticación y pasos de aprobación."
---
# Flujos de trabajo de Windmill

## Resumen

Esta página explica, para quienes administran el servidor, cómo integrar el motor de flujos de trabajo Windmill con la plataforma base: instalarlo, conectar un espacio de trabajo, crear flujos que reaccionan a eventos de webhook y escribir scripts contra la API OCS. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/windmill_workflows/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/automatizacion/windmill
Nextcloud integra el [motor de flujos de trabajo Windmill](https://www.windmill.dev/) para permitir flujos de trabajo personalizados avanzados que interactúan con la instancia de Nextcloud.

### Instalación

- Configurar una instancia de Windmill

  - Debería ser una instancia independiente. La app externa «Flow» (consultar {nc-ref}`Apps externas <ai-app_api>`) hacía posible tener una instancia empaquetada instalada en Nextcloud, pero esto está obsoleto desde Nextcloud 33. Para más información, consultar el manual de administración de Nextcloud 32.

- Activar la app `webhook_listeners` que viene con Nextcloud

```bash
occ app:enable webhook_listeners
```

- Instalar la [integración de Windmill](https://apps.nextcloud.com/apps/integration_windmill)

- Activar {nc-ref}`pretty_urls_label` en la instancia de Nextcloud

- *Recomendado pero opcional:* iniciar {nc-ref}`workers de trabajos en segundo plano para los receptores de webhooks <webhook_dispatch>`

### Configurar la conexión del espacio de trabajo

En Windmill hay disponibles espacios de trabajo separados. Para que Windmill pueda reaccionar a los eventos que ocurren en la instancia de Nextcloud, hay que conectar un espacio de trabajo a la conexión de Nextcloud. Esto solo pueden hacerlo los administradores del espacio de trabajo.

- En Windmill, abrir los ajustes del espacio de trabajo que se quiere conectar a Nextcloud mediante Settings -> Workspace
- Ir a la pestaña Native Triggers y elegir Nextcloud -> Configure OAuth
- Seguir las instrucciones para configurar la conexión OAuth
- Hacer clic en «Connect» y aceptar la conexión OAuth **con una cuenta de administrador de Nextcloud** o con una cuenta que tenga privilegios de administración de webhooks
- Si muestra «Connected», la conexión del espacio de trabajo se ha configurado correctamente.

Todo flujo configurado en este espacio de trabajo puede ahora añadir disparadores y scripts de Nextcloud basados en las credenciales de la cuenta con la que se aceptó la conexión OAuth.

### Crear un flujo de trabajo

Para que un flujo de trabajo reaccione a un evento de webhook de Nextcloud, hay que añadirle un disparador. Para ello, hacer clic en el signo más del recuadro Triggers del flujo y seleccionar «Nextcloud».

Ahora puede elegirse, en una lista desplegable de eventos, el evento al que debe reaccionar el flujo. Además, pueden rellenarse algunos parámetros:

- *Event filters* permite un filtrado más fino de los eventos que deben usarse. La condición de filtro, así como los eventos disponibles con sus cargas útiles, se documentan en la {nc-ref}`documentación de webhook_listeners <webhook_listeners>`.
- El *User ID filter* permite definir el usuario que puede disparar un flujo con sus acciones en Nextcloud. El webhook solo se llamará con solicitudes de este usuario. Vacío o null significa que no se filtra.
- El campo *Headers* permite definir un array de cabeceras que se envían en una llamada al webhook, algo que la mayoría de las veces no será necesario.

Se puede añadir más de un disparador a un flujo.

### Scripts de Nextcloud

{vendor}`Nextcloud` pone a disposición diversos scripts para usar en Windmill e interactuar con las apps de Nextcloud. Se encuentran
en <https://hub.windmill.dev/integrations/nextcloud> y <https://hub.windmill.dev/integrations/nextcloud/approvals>
o en la propia instancia de Windmill, al seleccionar scripts existentes para crear un nuevo flujo de trabajo.

Si se quiere usar una función que aún no esté representada allí, es fácil escribir scripts propios a partir de un script esqueleto y de la API OCS de {vendor}`Nextcloud`, que ofrece muchos endpoints. Los endpoints disponibles pueden consultarse en la [documentación de la API OCS de Nextcloud](https://docs.nextcloud.com/server/latest/developer_manual/_static/openapi.html), o bien puede instalarse la [app OCS API Viewer](https://apps.nextcloud.com/apps/ocs_api_viewer) de {vendor}`Nextcloud` para consultarlos directamente en la instancia de Nextcloud.

Este es un esqueleto de script escrito en TypeScript (Bun). Para usarlo, hay que añadir una acción en Windmill y elegir el lenguaje de script correcto. Incluye todo lo necesario para usar la API OCS de Nextcloud; las partes marcadas como {code}`$THIS` deben rellenarse con los datos propios.

```javascript
import createClient, { type Middleware } from "openapi-fetch";

export async function main(
   nextcloud: RT.Nextcloud,
   $PARAMETER: $TYPE,
   // add any input parameters you need here
) {

   // this part is the same for any script and should  not be changed

   const client = createClient<paths>({ baseUrl: nextcloud.baseUrl });
   const authMiddleware: Middleware = {
      async onRequest({ request, options }) {
         // fetch token, if it doesn’t exist
         // add Authorization header to every request
         request.headers.set("Authorization", `Basic ${btoa(nextcloud.userId + ':' + nextcloud.token)}`);
         return request;
      },
   };
   client.use(authMiddleware);

   //starting here you can adapt the script

   data = await client.GET("/ocs/v2.php/apps/$APP/$PATH/{$PATHPARAMETER}", {
      params: {
         header: {
            "OCS-APIRequest": true,
         },
         query: {
            format: "json",
         },
         path: {
            $PATHPARAMETER: "$VALUE",
         },

      },
      body: {
         $BODYPARAMETER: $VALUE,
      },
   });

return data;
}
```

La ruta del endpoint que hay que rellenar figura en la documentación de la API.

OCS usa dos tipos de parámetros: los parámetros de ruta, que forman parte de la URL del endpoint, y los parámetros de cuerpo, que se transmiten en el cuerpo de la solicitud. En el script de ejemplo, ambos tipos pueden indicarse en los parámetros de la función.

Recordar adaptar también el método HTTP (GET, POST, PUT, etc.) si hace falta.

La variable {code}`data` recibe la respuesta de la solicitud HTTP, así que ahí está disponible cualquier dato o mensaje de error que llegue de la instancia de Nextcloud.

#### Autenticación

Todos los scripts que ofrece {vendor}`Nextcloud` tienen un parámetro de entrada en común: *nextcloud* debe ser un objeto del tipo «Nextcloud» y contener lo necesario para autenticarse contra Nextcloud:

- baseUrl: la URL en la que se accede a la instancia, p. ej. {code}`https://example.cloud`
- userId: el ID del usuario con el que el script debe autenticarse
- token: una contraseña o un token de ese usuario

Se aconseja añadir estas credenciales como recurso del tipo Nextcloud al espacio de trabajo y hacer referencia a ese recurso en el script, o bien usar las credenciales de autenticación que se proporcionan en la llamada de retorno del webhook.
En cada flujo que se dispara por un evento de Nextcloud se incluyen 2 conjuntos de credenciales temporales:

- las credenciales de la cuenta de usuario guardada en la conexión OAuth inicial, disponibles como {code}`flow_input.authentication.owner`
- las credenciales de la cuenta de usuario que disparó el evento con su acción, disponibles como {code}`flow_input.authentication.trigger`

Estas credenciales de autenticación temporales son válidas durante una hora después de dispararse el evento.

#### Pasar valores entre bloques

Al especificar las entradas de un script, los parámetros pueden rellenarse con valores estáticos o con referencias a la entrada del flujo de trabajo y a los pasos anteriores del flujo.

Para hacer referencia a la entrada del flujo de trabajo (los detalles del evento que disparó el webhook), usar la variable `flow_input`.
Por ejemplo, `flow_input.event.form.hash` hace referencia al hash de un formulario de un evento de nextcloud Forms. Como se trata de una expresión de JavaScript y no de un valor estático, hay que cambiar la entrada del parámetro con el botón que hay junto a él.

Los campos disponibles para cada evento se enumeran en la {nc-ref}`documentación de webhook_listeners <webhook_listeners>`.

A cada paso de un flujo de trabajo se le asigna automáticamente una letra como identificador.
Para hacer referencia en los parámetros a resultados de pasos anteriores, usar la variable `results` con el ID del paso
al que se hace referencia como subpropiedad. Por ejemplo, usar `results.e.submission.answers` para usar las respuestas de un envío de formulario
obtenido mediante el script «Get form submission from Nextcloud Forms» identificado con la letra «e». Las letras pueden identificarse en el diagrama de vista general del flujo.

#### Pasos de aprobación/suspensión

Windmill permite usar los llamados pasos de aprobación, que son esencialmente scripts asíncronos que esperan la llamada a una URL de webhook adicional.
El caso de uso más destacado son los flujos de trabajo de aprobación, en los que llega una entrada automatizada de algún sitio que una persona debe aprobar.
Cuando la persona aprueba o rechaza activando la URL del webhook, el flujo de trabajo se reanuda.

Para convertir un paso recién añadido en un paso de aprobación, en la pantalla de edición del flujo de trabajo,
seleccionar el script y, en el panel del paso, ir a la pestaña «Advanced», subpestaña «Suspend», y marcar «Suspend/Approval/Prompt».

Con los scripts que se ofrecen para Nextcloud, pueden enviarse enlaces de aprobación a las personas encargadas de aprobar
mediante Nextcloud Talk o una simple notificación en Nextcloud.
Por supuesto, también puede usarse cualquiera de los demás scripts para enviar mensajes disponibles en el hub de Windmill.

Windmill tiene una interfaz de usuario de aprobación predeterminada en una URL específica, pero tiene un aspecto muy técnico.
Se recomienda usar la app [approve_links](https://apps.nextcloud.com/apps/approve_links),
que permite crear una atractiva página de aprobación temporal con un mensaje personalizado y botones para aprobar y rechazar.

#### Flujos de trabajo de ejemplo

{vendor}`Nextcloud` ofrece algunos flujos de trabajo de ejemplo en <https://hub.windmill.dev/integrations/nextcloud/flows> que muestran las posibilidades de combinar los flujos de trabajo de Windmill con la IA de Nextcloud.

### Preguntas frecuentes

#### ¿Se puede crear un script?

Si el hub de Windmill no contiene ningún script que realice la acción que se tiene en mente,
puede tomarse como ejemplo un script de Nextcloud existente y crear uno propio.
Los scripts personalizados pueden hacer solicitudes a cualquier endpoint de la
[API OCS de Nextcloud](https://docs.nextcloud.com/server/latest/developer_manual/_static/openapi.html).
````

## En APS Conecta Gestión

APS Conecta Gestión no instala Windmill. Windmill corre como aplicación externa (ExApp) de AppAPI, y una ExApp necesita un daemon de despliegue: la provisión no registra ninguno y el contenedor opcional HaRP de AIO viene desactivado. AppAPI queda instalada sin cambios porque la hoja de ruta la usa; la postura de producción del daemon sigue abierta en [gestion#75](https://github.com/APS-Conecta/gestion/issues/75).
