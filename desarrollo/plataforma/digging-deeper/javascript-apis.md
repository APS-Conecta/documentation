---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Las API de JavaScript para apps: los paquetes npm de @nextcloud, los eventos de cambio del estado de la red y las variables globales OC, OCA y OCP."
---
# API de JavaScript

## Resumen

Esta página describe las API de JavaScript que pueden usar las apps: los paquetes npm de `@nextcloud`, su uso, compatibilidad y desarrollo, y qué ofrece cada paquete; los eventos de cambio del estado de la red; y las variables globales `OC`, `OCA` y `OCP`, cuyo uso se desaconseja. Está dirigida a quienes desarrollan el frontend de apps.

````{upstream} developer_manual/digging_deeper/javascript-apis.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Las apps de Nextcloud pueden usar las API de JavaScript existentes para facilitar el desarrollo de componentes de frontend y de scripts sencillos.

Antes, las API se proporcionaban mediante variables globales, disponibles en la mayoría de las páginas de Nextcloud. Para suavizar la experiencia de desarrollo con las herramientas de desarrollo modernas, este método está en proceso de declararse obsoleto y de eliminarse. Las API existentes se están migrando a paquetes npm y las nuevas API solo estarán disponibles de esa forma. La parte final de la página cubre los fundamentos del método de las variables globales, por si se quiere desarrollar una app para versiones antiguas de Nextcloud.

(javascript-apis-npm-packages)=
### Paquetes npm

Los [paquetes npm de @nextcloud](https://www.npmjs.com/org/nextcloud) proporcionan las API de frontend actuales para las apps de Nextcloud.

#### Uso

La idea es que las apps instalen estos paquetes mediante *npm* y empaqueten el código con herramientas como [Babel](https://babeljs.io/), [Webpack](https://webpack.js.org/) o [Parcel](https://parceljs.org/). Así se garantiza que una app ejecute exactamente el mismo código independientemente de la versión de Nextcloud y, además, se reducen las probabilidades de entrar en conflicto con otras apps.

Para más detalles sobre las consideraciones de diseño, ver [la discusión en GitHub](https://github.com/nextcloud/server/issues/15932).

:::{note}
Se recomienda encarecidamente mantener los paquetes actualizados, ya que aportan correcciones y parches de seguridad. Para las apps cuyo código está alojado en GitHub, se recomienda usar [Dependabot](https://dependabot.com/).
:::

#### Compatibilidad

Los paquetes proporcionados pretenden ser compatibles con todas las [versiones de Nextcloud con soporte](https://github.com/nextcloud/server/wiki/Maintenance-and-Release-Schedule). Sin embargo, puede que en el futuro haya que cambiar una API de forma no retrocompatible. Por eso conviene estar atento a los saltos de versión mayor de los paquetes y leer los registros de cambios.

#### Desarrollo

La mayoría de los paquetes están escritos en TypeScript para generar automáticamente una mejor documentación de la API, pero también para garantizar de forma programática la compatibilidad con el servidor de Nextcloud. El servidor está tipado en [un paquete npm dedicado](https://www.npmjs.com/package/@nextcloud/typings) que se usa para comprobar la solidez de los tipos.

#### Paquetes en detalle

El resto de esta sección ofrece una visión general aproximada de qué paquetes se proporcionan y para qué se usan.

(nc-dev-js-library_nextcloud-auth)=
#### `@nextcloud/auth`

Este paquete proporciona información sobre el usuario y la sesión actuales. Documentación: <https://nextcloud-libraries.github.io/nextcloud-auth/>

#### `@nextcloud/axios`

Este paquete proporciona una instancia del cliente HTTP [Axios](https://www.npmjs.com/package/axios), lista para enviar peticiones al servidor de Nextcloud. Si se usa esta instancia, no hay que preocuparse por la autenticación ni por las cabeceras especiales. Documentación: <https://nextcloud-libraries.github.io/nextcloud-axios/>

(nc-dev-js-library_nextcloud-event-bus)=
#### `@nextcloud/event-bus`

Este paquete proporciona una implementación sencilla de un bus de eventos que se integra con el servidor y con otras apps. Por ello es una de las formas recomendadas de comunicación entre apps. Documentación: <https://nextcloud-libraries.github.io/nextcloud-event-bus/>

(nc-dev-js-library_nextcloud-dialogs)=
#### `@nextcloud/dialogs`

Este paquete proporciona acceso a los diálogos de la interfaz de usuario de Nextcloud. Documentación: <https://nextcloud-libraries.github.io/nextcloud-dialogs/>

(nc-dev-js-library_nextcloud-files)=
#### `@nextcloud/files`

Este paquete proporciona métodos para acceder a la API pública de la app Archivos, funciones auxiliares para acceder a los archivos de Nextcloud mediante WebDAV
y funciones de utilidad para trabajar con archivos y carpetas. Documentación: <https://nextcloud-libraries.github.io/nextcloud-files/>

#### `@nextcloud/initial-state`

Este paquete proporciona la contraparte de *\\OCP\\IInitialStateService* del backend. Usarlo para recuperar los datos almacenados al cargar la página. Documentación: <https://nextcloud-libraries.github.io/nextcloud-initial-state/>

#### `@nextcloud/l10n`

Este paquete proporciona todo lo relacionado con la localización, como el acceso a la configuración regional del usuario actual y funciones auxiliares de traducción. Documentación: <https://nextcloud-libraries.github.io/nextcloud-l10n/>

#### `@nextcloud/logger`

Este paquete proporciona una función auxiliar de registro unificada que agrega nombres de app, gravedad y otro contexto a los mensajes de registro. Usarlo para mejorar la salida de los registros de la app, algo útil para el desarrollo y para clasificar los informes de errores. Documentación: <https://nextcloud-libraries.github.io/nextcloud-logger/>

#### `@nextcloud/moment`

Este paquete proporciona una versión modificada de [moment.js](https://momentjs.com/) con la configuración regional del usuario actual ya establecida. Documentación: <https://nextcloud-libraries.github.io/nextcloud-moment/>

#### `@nextcloud/password-confirmation`

Este paquete permite pedir a un usuario que confirme las acciones que tienen el atributo `#[PasswordConfirmationRequired]` o la anotación `@PasswordConfirmationRequired` en el método del controlador. Usarlo para acciones críticas. Documentación: <https://nextcloud-libraries.github.io/nextcloud-password-confirmation/>

#### `@nextcloud/paths`

Este paquete proporciona varias funciones auxiliares para rutas de archivos y carpetas. Documentación: <https://nextcloud-libraries.github.io/nextcloud-paths/>

#### `@nextcloud/router`

Este paquete proporciona funciones auxiliares para generar URL, p. ej., para acceder a los recursos y a las API REST de la app o del servidor de Nextcloud. Documentación: <https://nextcloud-libraries.github.io/nextcloud-router/>

(nc-dev-js-library_nextcloud-sharing)=
#### `@nextcloud/sharing`

Este paquete proporciona funciones auxiliares para interactuar con la app de compartición de archivos, p. ej., para detectar si la página actual es un recurso compartido público y recuperar el token de compartición.
Documentación: <https://nextcloud-libraries.github.io/nextcloud-sharing/>

(nc-dev-js-library_nextcloud-vue)=
#### `@nextcloud/vue`

Este paquete proporciona muchos componentes de Vue que permiten construir rápidamente interfaces de usuario con el diseño de Nextcloud.

- Documentación: <https://nextcloud-vue-components.netlify.app/>
- Código fuente: <https://github.com/nextcloud-libraries/nextcloud-vue>

### Eventos

#### Cambios del estado de la red

La app puede reaccionar a la pérdida de conectividad de red, p. ej., para gestionar con elegancia ese estado, en el que no es posible ninguna interacción con el servidor. Como la comunicación con el servidor requiere casi siempre un token CSRF válido, puede que no se quiera enviar ninguna petición antes de que el token se haya actualizado. Nextcloud puede avisar cuando esto haya ocurrido. Usar `@nextcloud/event-bus` para escuchar los eventos `networkOnline` y `networkOffline`:

```js
import { subscribe } from '@nextcloud/event-bus'

subscribe('networkOffline', () => console.info("we're offline"))
subscribe('networkOnline', (event) => {
    if (event.successful) {
        console.info("we're back online, the token was updated")
    } else {
        console.info("we're back online, but the token might not be up to date")
    }
})
```

### Variables globales

También existen variables globales que en el pasado actuaban como API. Se desaconseja usar estas variables, ya que provocan problemas de orden de carga de los scripts y el infierno de dependencias, lo que dificulta que el componente del servidor actualice las bibliotecas.

:::{note}
Hay que tener cuidado al acceder a variables globales, ya que su disponibilidad depende del orden en que se cargan los scripts. Por tanto, puede que aún no se hayan asignado cuando se ejecute el script. Usar el evento `load` del documento para esperar a que todos los scripts se hayan cargado y ejecutado.
:::

#### OC – API internas

La variable `OC` da acceso a muchos aspectos internos del servidor de Nextcloud. No está pensada para que la usen las apps, ya que las API pueden cambiar en cualquier momento.

#### OCA – API de las apps

Algunas apps usan la variable `OCA` como lugar donde registrar sus tipos. Salvo en casos límite de comunicación entre apps, no se debería asignar nada a esta variable.

#### OCP – API públicas

Algunas API más estables se exponen en el «espacio de nombres» `OCP`. Desde la publicación de los [paquetes npm](#javascript-apis-npm-packages), quedaron desfasadas y, por tanto, se declararán obsoletas.
````
