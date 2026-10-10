---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 33 para las apps: API de archivos, barra lateral y perfil, API JavaScript eliminadas, PHP 8.2 a 8.5, ID Snowflake y API de backend."
---
# Actualización a Nextcloud 33

## Resumen

Esta página enumera los cambios de la versión 33 que afectan a las apps: la versión 4 de la biblioteca `nextcloud/files` y la nueva API de barra lateral, la API de secciones del perfil, las API de JavaScript eliminadas, la compatibilidad con PHP 8.2 a 8.5, el nuevo agente de usuario, los ID Snowflake y las API de backend añadidas, modificadas, obsoletas o eliminadas. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_33.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Cambios de frontend

#### API de archivos

##### Cambios incompatibles en el paquete de la API de archivos

La biblioteca `nextcloud/files` se actualizó a la versión v4.0.0 en Server.
Esta versión incluye cambios incompatibles en la API, por lo que habrá que actualizar el código a tiempo para Server 33.

Para mejorar la experiencia de desarrollo, se amplió el objeto de contexto que se pasa a las acciones de archivo.
Ahora incluye campos adicionales, como la carpeta actual y la lista de archivos actual.
También cambiaron las firmas de las funciones: los manejadores de acciones ahora usan parámetros desestructurados en lugar de argumentos posicionales en un array.

El registro de cambios completo y los detalles de la migración se encuentran en el repositorio: [nextcloud-files (4.0.0 beta)](https://github.com/nextcloud-libraries/nextcloud-files).

##### Barra lateral

En esta versión, la API de archivos se cambió para usar la API Node (disponible desde Nextcloud 27) en lugar de la API heredada `FileInfo`.
Por eso cambió la forma de registrar pestañas y acciones de la barra lateral.
La API `OCA.Files.Sidebar` se eliminó y se reemplazó por una nueva API de barra lateral disponible en el paquete [@nextcloud/files](https://www.npmjs.com/package/@nextcloud/files).

Para registrar pestañas de la barra lateral ahora hay que usar la nueva API, que se basa en componentes web;
para más detalles, consultar el registro de cambios del paquete `@nextcloud/files`.

Si la app usaba la barra lateral de Archivos, ahora tiene que usar una barra lateral propia mediante el componente `NcAppSidebar` del paquete [@nextcloud/vue](https://www.npmjs.com/package/@nextcloud/vue).

En cambio, si la app ya usa su propia implementación de barra lateral pero depende de la app Viewer para abrir la barra lateral mediante la API `OCA.Files.Sidebar`,
ahora hay que escuchar el evento `viewer:sidebar:open` del bus de eventos de la app Viewer para abrir la barra lateral propia.
Para habilitar la acción **Abrir barra lateral** dentro del visor, hay que establecer `enabledSidebar`
al abrir el visor, de modo que se permita abrir la barra lateral desde dentro del visor, y escuchar el evento mencionado.

#### App de perfil

Para que la API de secciones del perfil sea independiente del framework, lo que permite migrar la app de perfil a Vue 3
sin dejar de permitir que las apps externas usen secciones de perfil basadas en Vue 2,
la API `OCA.Core.ProfileSections` se reemplazó por `OCA.Profile.ProfileSections`,
que usa componentes web personalizados en lugar de basarse en componentes de Vue.

A partir de Nextcloud 33, el método `OCA.Profile.ProfileSections.registerSection` acepta
un objeto de sección con el siguiente formato:

```typescript
interface ProfileSection {
  /**
   * Unique identifier for the section
   */
  id: string
  /**
   * The order in which the section should appear (lower numbers appear first)
   */
  order: number
  /**
   * The custom element tag name to be used for this section
   *
   * The custom element must have been registered beforehand,
   * and must have the a `user` property of type `string | undefined`.
   *
   * @see https://developer.mozilla.org/en-US/docs/Web/API/Web_components
   */
  tagName: string
  /**
   * Static parameters to be passed to the custom web component
   */
  params?: Record<string, unknown>
}
```

#### API añadidas

- `OCA.Profile.ProfileSections` se añadió como reemplazo independiente del framework de `OCA.Core.ProfileSections`.
  Ver la sección sobre la app de perfil, más arriba.

#### API modificadas

- Por definir

#### API obsoletas

- Por definir

#### API eliminadas

- Se eliminó la implementación global de `md5`. Estaba obsoleta desde Nextcloud 20 y Nextcloud ya no la usaba.
  Si todavía se necesita una implementación de `md5`, basta con usar algún paquete externo como [crypto-browserify](https://www.npmjs.com/package/crypto-browserify).
- Se eliminó `OCP.WhatsNew`.
- `OC.AppConfig` estaba obsoleto desde Nextcloud 16 y ahora se eliminó. Usar `OCP.AppConfig` en su lugar.
- Se eliminó la API `OC.Settings.UserSettings`.
- Se eliminó la API `OC.SystemTags`. Si se necesita obtener la lista de etiquetas del sistema,
  consultar [esta solicitud de fusión](https://github.com/nextcloud/files_retention/pull/855) para ver cómo obtener las etiquetas directamente.
- Se eliminaron `OC.set` y `OC.get`. Ambos están obsoletos desde Nextcloud 19.
  Para `get`, si de verdad hace falta, usar [lodash get](https://lodash.com/docs#get).
  Y para `set`, usar [lodash set](https://lodash.com/docs#set).
- Se eliminaron `OC.redirect` y `OC.reload`. Ambos estaban obsoletos desde Nextcloud 17.
  Para reemplazar `OC.redirect`, usar directamente `window.location`.
  Para reemplazar `OC.reload`, usar directamente `window.location.reload`.
- Se eliminó `OC.fileIsBlacklisted`. Estaba obsoleto desde Nextcloud 18.
  El reemplazo es usar `validateFilename` del paquete [@nextcloud/files](https://www.npmjs.com/package/@nextcloud/files).
- Los métodos de host obsoletos de *OC* estaban obsoletos desde Nextcloud 17 y ahora se eliminaron

  - Para reemplazar `OC.getHost`, usar `window.location.host`.
  - Para reemplazar `OC.getHostName`, usar `window.location.hostname`.
  - Para reemplazar `OC.getPort`, usar `window.location.port`.
  - Para reemplazar `OC.getProtocol`, usar `window.location.protocol`.

- La API `OCA.Core.ProfileSections` se eliminó y se reemplazó por la API `OCA.Profile.ProfileSections`, independiente del framework.
  Ver la sección sobre la app de perfil, más arriba.

- Se eliminó la API `OCA.Files.Sidebar`.
  Era la última API que usaba la API heredada `FileInfo`.
  Ahora se reemplaza por la nueva API de barra lateral basada en Node, disponible en el paquete [@nextcloud/files](https://www.npmjs.com/package/@nextcloud/files).

- La API `OCA.Sharing.ExternalLinkActions` quedó obsoleta en Nextcloud 23 y ahora se eliminó.
  Se reemplazó por `OCA.Sharing.ExternalShareAction`, que ahora tiene una API propiamente dicha, usando en su lugar `registerSidebarAction` de [@nextcloud/sharing](https://www.npmjs.com/package/@nextcloud/sharing).

### Cambios de backend

#### Compatibilidad con PHP 8.5 añadida

Ver la sección siguiente para los cambios de código opcionales en la app y en la gestión de dependencias

#### Compatibilidad con PHP 8.1 eliminada

En esta versión se eliminó la compatibilidad con PHP 8.1. Seguir los pasos siguientes para que la app sea compatible.

1. Si `appinfo/info.xml` tiene una especificación de dependencia para PHP, aumentar `min-version` a 8.2.

```xml
<dependencies>
  <php min-version="8.2" max-version="8.5" />
  <nextcloud min-version="31" max-version="33" />
</dependencies>
```

2. Si la app tiene un `composer.json` y el archivo contiene las restricciones de PHP de `info.xml`, ajustarlo también.

```json
{
  "require": {
    "php": ">=8.2 <=8.5"
  }
}
```

3. Si se tiene configurada la {nc-ref}`integración continua <app-ci>`, quitar PHP 8.1 y añadir PHP 8.5 en las matrices de pruebas y de linters.

#### Cambio del agente de usuario predeterminado de las solicitudes salientes

A partir de esta versión, el agente de usuario predeterminado de las solicitudes que hace la instancia cambió de `Nextcloud Server Crawler` a `Nextcloud-Server-Crawler/X.Y.Z`, donde `X.Y.Z` es la versión actual del servidor.

#### ID Snowflake

Las siguientes tablas ahora usan ID Snowflake:

- `oc_previews`
- `oc_jobs`
- `oc_share_external`

Las API relacionadas con estas tablas ahora usan una cadena en lugar de un int. Ver la sección de API modificadas y {nc-doc}`developer_manual/digging_deeper/snowflake_ids`.

#### Eventos añadidos

- Por definir

#### API añadidas

- Ahora se exponen `\OCP\DB\IResult::iterateAssociative` y `\OCP\DB\IResult::iterateNumeric` de doctrine/dbal.
  Estos dos métodos devuelven iteradores que pueden usarse directamente en un *foreach* para recorrer el resultado de una consulta SQL.
  Por ejemplo:

```php
$result = $qb->executeQuery();
foreach ($result->iterateAssociative() as $row) {
    $id = $row['id'];
}
$result->closeCursor();
```

- Esta versión permite exponer algunas métricas relacionadas con Nextcloud en formato OpenMetrics.
  Se pueden añadir exportadores propios implementando la interfaz `\OCP\OpenMetrics\IMetricFamily`.
  Ver {nc-doc}`developer_manual/digging_deeper/openmetrics` para más información.

- Se añadió el tipo de tarea de TaskProcessing `ImageToTextOpticalCharacterRecognition`

- Se añadió la interfaz de proveedor de TaskProcessing `ISynchronousWatermarkingProvider` para permitir que los proveedores de procesamiento síncrono reaccionen al indicador booleano includeWatermark

- Se añadió al esquema de info.xml de las aplicaciones la compatibilidad con secciones y ajustes solo de delegación. Solo es útil si la aplicación necesita habilitar la delegación de derechos que no están relacionados con una página de ajustes. Ejemplos conocidos de ello son la gestión de usuarios y el registro de webhooks. Ver {nc-ref}`metadatos de la app <app metadata>` para más detalles.

#### API modificadas

- Los métodos `setId` y `getId` de `\OCP\BackgroundJob\IJob` se cambiaron para devolver/aceptar una cadena en lugar de un int. Lo mismo ocurre con `\OCP\BackgroundJob\IJobList`, donde algunos métodos (`removedById`, `getById` y `getDetailsById`) ahora reciben una cadena en lugar de un int. Se supone que la cadena es un ID Snowflake.
- Los métodos `setObjectId` y `getObjectId` de `\OCP\Activity\IEvent` se cambiaron para devolver/aceptar una cadena además de un int. Se supone que la cadena es un ID Snowflake.
- La clase `\OCP\TaskProcessing\Task` ahora tiene los métodos `getIncludeWatermark` y `setIncludeWatermark` para indicar si el proveedor debe añadir una marca de agua a la salida generada.
- La API OCS de TaskProcessing ahora también acepta el indicador `includeWatermark` al programar tareas
- `\OCP\Notification\INotification::setIcon`, `\OCP\Notification\INotification::setLink` y `\OCP\Notification\IAction::setLink` ahora lanzan `\OCP\Notification\InvalidValueException` cuando el enlace proporcionado no es absoluto, como se anunció anteriormente en {nc-doc}`developer_manual/release_notes/previous/upgrade_to_30`

#### API obsoletas

- `\OCP\DB\IResult::fetch` y `\OCP\DB\IResult::fetchAll` quedan obsoletos de forma suave (*soft-deprecated*). En su lugar se pueden usar
  `\OCP\DB\IResult::fetchAssociative`, `\OCP\DB\IResult::fetchNumeric` y `\OCP\DB\IResult::fetchOne`
  como reemplazo de `\OCP\DB\IResult::fetch`; y `\OCP\DB\IResult::fetchAllAssociative`,
  `\OCP\DB\IResult::fetchAllNumeric` y `\OCP\DB\IResult::fetchFirstColumn` como reemplazo de
  `\OCP\DB\IResult::fetchAll`. Si se usa rector, se puede usar el conjunto Nextcloud33 para portar automáticamente
  la mayor parte del código a los nuevos métodos.

#### API eliminadas

- El método `\OCP\BackgroundJob\IJob::execute` estaba obsoleto desde Nextcloud 25 y ahora se eliminó.
  Usar en su lugar el método `IJob::start`, disponible desde Nextcloud 25.
- Las clases `\OCP\Search\PagedProvider`, `\OCP\Search\Provider` y `\OCP\Search\Result`
  estaban obsoletas desde Nextcloud 20 y ahora se eliminaron. Usar en su lugar `\OCP\Search\SearchResult` y
  `\OCP\Search\IProvider`, disponibles desde Nextcloud 20.
- Se eliminó el método `\OC_Util::runningOnMac()`. En su lugar basta con comprobar `PHP_OS_FAMILY === 'Darwin'`.
- El método `\OCP\DB\IQueryBuilder::execute` estaba obsoleto desde Nextcloud 22 y ahora se eliminó.
  Usar en su lugar `\OCP\DB\IQueryBuilder::executeQuery` al ejecutar una consulta `SELECT`, y el método `\OCP\DB\IQueryBuilder::executeStatement`
  al ejecutar una sentencia `UPDATE`, `INSERT` y `DELETE`, disponibles desde Nextcloud 20.

  En lugar de capturar excepciones del paquete Doctrine DBAL, ahora hay que capturar `OCP\DB\Exception`
  y comprobar `getReason`. Por ejemplo, el siguiente código antiguo:

```php
try {
    $qb->insert(...);
    $qb->execute();
} catch (\Doctrine\DBAL\Exception\UniqueConstraintViolationException) {
    // Do stuff
}
```

Debe reemplazarse por el siguiente código:

```php
try {
    $qb->insert(...);
    $qb->executeStatement();
} catch (\OCP\DB\Exception $e) {
    if ($e->getReason() !== \OCP\DB\Exception::REASON_UNIQUE_CONSTRAINT_VIOLATION) {
        throw $e;
    }

    // Do stuff
}
```

- `\OCP\Files::buildNotExistingFileName` y el helper privado relacionado `\OC_Helper::buildNotExistingFileName` estaban obsoletos desde Nextcloud 14 y ahora se eliminaron. Usar `\OCP\Files\Folder::getNonExistingName` en su lugar.

- Se eliminó la función `WhatsNew` y, con ella, la clase `OC\Updater\ChangesCheck` y las API relacionadas.
  Esto incluye también la tabla de base de datos `whats_new` y la clase `WhatsNewController`, que servía el endpoint `/core/whatsnew`, ahora eliminado.

- Se eliminó la clase heredada `\OC_Response`.
````
