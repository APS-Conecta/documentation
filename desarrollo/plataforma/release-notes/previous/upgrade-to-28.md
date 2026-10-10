---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 28 para las apps: nueva app Archivos, PHP 8.3, doctrine/dbal 3.7, symfony/event-dispatcher y eventos tipados."
---
# Actualización a Nextcloud 28

## Resumen

Esta página enumera los cambios de la versión 28 que afectan a las apps: el rango de `appinfo/info.xml`, las nuevas API de frontend de la app Archivos, la compatibilidad con PHP 8.3, las bibliotecas del núcleo actualizadas (`doctrine/dbal` y `symfony/event-dispatcher`), las API añadidas, modificadas, obsoletas o eliminadas, los eventos tipados que reemplazan a los antiguos y las propiedades WebDAV eliminadas. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_28.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### General

#### info.xml

Asegurarse de que el `appinfo/info.xml` de la app admita Nextcloud 28.

```xml
<dependencies>
    <nextcloud min-version="26" max-version="28" />
</dependencies>
```

### Cambios de frontend

#### API añadidas

- Como la nueva app Archivos se inicializa mucho más rápido que la antigua, se producirán algunas
  condiciones de carrera si se registran propiedades personalizadas cargando los scripts
  mediante el método `Util::addScript`.
  Se recomienda usar en su lugar el nuevo método `Util::addInitScript`: el script
  se cargará justo después de los scripts comunes del núcleo y justo antes de la app Archivos.
  Ver {nc-ref}`ApplicationJs` para más información.

- Acciones de archivo: para registrar acciones de archivo, usar la API dedicada de <https://npmjs.org/@nextcloud/files> o
  <https://nextcloud-libraries.github.io/nextcloud-files/functions/registerFileAction.html>
- Menú de nuevo archivo: para registrar entradas en el menú de nuevo archivo, usar la API dedicada de <https://npmjs.org/@nextcloud/files> o
  <https://nextcloud-libraries.github.io/nextcloud-files/functions/addNewFileMenuEntry.html>
- Recordatorio de la 27: para interactuar con el enrutador de la app Archivos, usar `OCP.Files.Router`. Ver {nc-ref}`FilesAPI`
- Para interactuar con los datos de la app Archivos, usar los siguientes eventos. Todos tienen un [objeto Node](https://nextcloud-libraries.github.io/nextcloud-files/classes/Node.html) como parámetro principal.

  - `files:node:created`: se creó el nodo
  - `files:node:deleted`: se eliminó el nodo
  - `files:node:moved`: se movió el nodo (y sus datos ya están actualizados)
  - `files:node:updated`: se actualizaron los datos del nodo

#### API obsoletas

- Las variables CSS `--color-text-light` y `--color-text-lighter` se convirtieron en alias de `--color-main-text` y `--color-text-maxcontrast`
  en [Nextcloud 20](https://github.com/nextcloud/server/pull/21117); ahora están oficialmente obsoletas y se eliminarán en un futuro próximo.

#### API eliminadas

- `OC.loadScript` y `OC.loadStyle`: usar `OCP.Loader` en su lugar.
- `OC.appSettings`: no hay reemplazo.
- `OCA.Files`: se eliminó todo salvo Sidebar y Settings. Ver la sección de API añadidas para los reemplazos.

### Cambios de backend

#### PHP 8.3

En esta versión se añadió la compatibilidad con PHP 8.3. Seguir los pasos siguientes para que la app sea compatible.

1. Si `appinfo/info.xml` tiene una especificación de dependencia para PHP, aumentar `max-version` a 8.3.

```xml
<dependencies>
  <php min-version="8.0" max-version="8.3" />
  <nextcloud min-version="26" max-version="28" />
</dependencies>
```

2. Si la app tiene un `composer.json` y el archivo contiene las restricciones de PHP de `info.xml`, ajustarlo también.

```json
{
  "require": {
    "php": ">=8.0 <=8.3"
  }
}
```

3. Si se tiene configurada la {nc-ref}`integración continua <app-ci>`, ampliar la matriz de pruebas con pruebas y linters de PHP 8.3.

La información sobre los cambios de código se encuentra en [php.net](https://www.php.net/migration83) y [stitcher.io](https://stitcher.io/blog/new-in-php-83).

#### El infierno de las dependencias de desarrollo

Debido a la popularidad de las herramientas CLI para el desarrollo de apps de Nextcloud, ha aumentado la probabilidad de conflictos entre paquetes. Se recomienda encarecidamente consultar {nc-ref}`app-composer-bin-tools` y migrar a directorios bin de composer.

#### Bibliotecas del núcleo actualizadas

Si las apps usan solo API públicas oficiales de Nextcloud, la actualización de las bibliotecas del núcleo debería tener poco o ningún efecto en ellas. Sin embargo, hay algunos casos límite en los que una app todavía tiene una dependencia de código con una biblioteca incluida en Nextcloud, por ejemplo cuando se usan esas clases o funciones de terceros, por lo que se recomienda a quienes desarrollan apps revisar su código en busca de cualquier incompatibilidad. Además, se recomienda comprobar la compatibilidad con herramientas sofisticadas, como se documenta en la sección de {nc-ref}`análisis estático <app-static-analysis>`.

##### `doctrine/dbal`

La capa de abstracción de bases de datos de Doctrine (Doctrine Database Abstraction Layer) impulsa la conexión a la base de datos y el constructor de consultas de Nextcloud. En Nextcloud 28, esta dependencia se actualizó de 3.3 a 3.7.

Siendo optimistas, la conexión a la base de datos y el constructor de consultas deberían funcionar en su mayor parte como en Nextcloud 27 o anteriores.
Algunos cambios incompatibles (menores) fueron inevitables. Este es el resumen:

- Cuando una instancia del constructor de consultas usa parámetros posicionales `->setValue('name', '?')` `setParameter(0, $name)`, hay que volver a establecer todos los parámetros al ejecutar la consulta varias veces, por ejemplo en un bucle. Se recomienda pasar en su lugar a parámetros con nombre usando `createParameter()`.

Los detalles de este cambio también pueden verse en la [pull request en GitHub](https://github.com/nextcloud/server/pull/38556) y en la documentación original, en el [documento de actualización de dbal 3.7.x](https://github.com/doctrine/dbal/blob/3.7.x/UPGRADE.md).

##### `symfony/event-dispatcher`

En las últimas 2 versiones mayores, el paquete `symfony/event-dispatcher` primero declaró obsoleta y luego eliminó la forma en que el servidor de Nextcloud
despachaba los eventos antiguos. Esto significa que la forma en que se encapsulaba la `\Symfony\Component\EventDispatcher\EventDispatcherInterface` de symfony,
así como el uso del `\Symfony\Component\EventDispatcher\GenericEvent`, no pudieron mantenerse de forma compatible con versiones anteriores.

Por lo tanto, para ser compatible con Nextcloud 28 es necesario migrar de `\Symfony\Component\EventDispatcher\EventDispatcherInterface`
a `\OCP\EventDispatcher\IEventDispatcher` (existe desde Nextcloud 17).
Todos los puntos del código que despachaban un `\Symfony\Component\EventDispatcher\GenericEvent` se ajustaron
y ahora tienen un evento dedicado basado en `\OCP\EventDispatcher\Event` que se despacha como evento tipado, de modo que todos los parámetros disponibles están documentados.

Los detalles de este cambio también pueden verse en las tareas pendientes enlazadas desde la [pull request en GitHub](https://github.com/nextcloud/server/pull/38546).

#### API añadidas

- `\OCP\AppFramework\Http\EmptyContentSecurityPolicy::useStrictDynamicOnScripts` para establecer 'strict-dynamic' en la CSP 'script-src-elem'; está establecido en true por defecto para permitir que las apps que usan JS de módulo importen dependencias.
- `\OCP\Mail\IMessage::setSubject` para establecer el asunto de un correo electrónico. Ver {nc-ref}`email` para un ejemplo.
- `\OCP\Mail\IMessage::setHtmlBody` y `\OCP\Mail\IMessage::setPlainBody` para establecer el cuerpo de un correo electrónico. Ver {nc-ref}`email` para un ejemplo.
- `\OCP\IEventSourceFactory` para crear una instancia de `OCP\IEventSource`.
- `\OCP\Preview\BeforePreviewFetchedEvent::getCrop`
- `\OCP\Preview\BeforePreviewFetchedEvent::getHeight`
- `\OCP\Preview\BeforePreviewFetchedEvent::getMode`
- `\OCP\Preview\BeforePreviewFetchedEvent::getWidth`
- `\OCP\IPhoneNumberUtil::convertToStandardFormat` para convertir una entrada en un número de teléfono con formato E164. Ver {nc-ref}`phonenumberutil` para un ejemplo.
- `\OCP\IPhoneNumberUtil::getCountryCodeForRegion` para obtener el código de país E164 de una región dada. Ver {nc-ref}`phonenumberutil` para un ejemplo.
- `\OCP\AppFramework\Http\EmptyContentSecurityPolicy::allowEvalWasm(bool)`: establece `wasm-unsafe-eval` en `script-src` de la Content Security Policy [para permitir la compilación y ejecución de WebAssembly en la página](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src#unsafe_webassembly_execution)
- `\OCP\FilesMetadata\IMetadataBackgroundEvent::getNode`
- `\OCP\FilesMetadata\IMetadataBackgroundEvent::getMetadata`
- `\OCP\FilesMetadata\IMetadataLiveEvent::getNode`
- `\OCP\FilesMetadata\IMetadataLiveEvent::getMetadata`
- `\OCP\FilesMetadata\IMetadataLiveEvent::requestBackgroundJob`
- `\OCP\FilesMetadata\IFilesMetadataManager::refreshMetadata`
- `\OCP\FilesMetadata\IFilesMetadataManager::getMetadata`
- `\OCP\FilesMetadata\IFilesMetadataManager::saveMetadata`
- `\OCP\FilesMetadata\IFilesMetadataManager::deleteMetadata`
- `\OCP\FilesMetadata\IFilesMetadataManager::getMetadataQuery`
- `\OCP\FilesMetadata\IFilesMetadataManager::getKnownMetadata`
- `\OCP\FilesMetadata\IFilesMetadataManager::initMetadata`
- `\OCP\FilesMetadata\IMetadataQuery::retrieveMetadata`
- `\OCP\FilesMetadata\IMetadataQuery::extractMetadata`
- `\OCP\FilesMetadata\IMetadataQuery::joinIndex`
- `\OCP\FilesMetadata\IMetadataQuery::getMetadataKeyField`
- `\OCP\FilesMetadata\IMetadataQuery::getMetadataValueField`

  - `wasm-unsafe-eval` es [compatible con la mayoría de los navegadores](https://caniuse.com/mdn-http_headers_content-security-policy_script-src_wasm-unsafe-eval)
  - La compilación y la ejecución de WebAssembly en hilos de trabajo (worker threads) no se ven afectadas por esta directiva (los navegadores permiten por defecto la compilación y la ejecución de WebAssembly en hilos de trabajo)
  - `OCP\Authentication\Token\IProvider::getToken` para obtener un token por su id de cadena de token
  - `OCP\Authentication\Token\IToken`: interfaz pública para los tokens que devuelve la función anterior. Usar estos en lugar de lo que hay en el espacio de nombres `OC`.
  - `OCP\User\Backend\IProvideEnabledStateBackend` para los backends de usuarios que quieran alterar el estado deshabilitado de los usuarios (lo usa user_ldap para marcar los restos como deshabilitados si la opción está activada).

#### API modificadas

- `\OCP\Preview\BeforePreviewFetchedEvent` ahora acepta `width, height, crop and mode` como argumentos opcionales del constructor.
- La interfaz `\OCP\Files\Folder` recibió un nuevo método: `searchBySystemTag(string $tagName, string $userId, int $limit = 0, int $offset = 0)`.
- `OCP\SystemTag\ISystemTagManager::getTagsByIds()` ahora acepta opcionalmente *IUser* como segundo parámetro, para recuperar solo las etiquetas del sistema visibles para ese usuario.

#### API obsoletas

- `\OCP\DB\IResult::fetch`: usar en su lugar los nuevos `fetchAssociative`, `fetchNumeric` y `fetchOne`. Si se llamaba a `fetch` sin argumentos, `fetchAssociative` es el reemplazo directo. Tener en cuenta que los nuevos métodos lanzan una excepción diferente.
- `\OCP\DB\IResult::fetchAll`: usar en su lugar los nuevos `fetchAllAssociative`, `fetchAllNumeric` y `fetchOne`. Si se llamaba a `fetchAll` sin argumentos, `fetchAllAssociative` es el reemplazo directo. Tener en cuenta que los nuevos métodos lanzan una excepción diferente.
- En `\OCP\Preview\BeforePreviewFetchedEvent`, pasar `null` para `width, height, crop or mode` está obsoleto. A partir de Nextcloud 31 son obligatorios.

#### API eliminadas

- `\OC_App::getAppVersion`: inyectar `\OCP\App\IAppManager` y llamar a `\OCP\App\IAppManager::getAppVersion`.
- `\OC_App::getAppInfo`: inyectar `\OCP\App\IAppManager` y llamar a `\OCP\App\IAppManager::getAppInfo`.
- `\OC_App::getNavigation`: inyectar `\OCP\App\IAppManager` y llamar a `\OCP\App\IAppManager::getAll`.
- `\OC_App::getSettingsNavigation`: inyectar `\OCP\App\IAppManager` y llamar a `\OCP\App\IAppManager::getAll('settings')`.
- `\OC_App::isEnabled`: inyectar `\OCP\App\IAppManager` y llamar a `\OCP\App\IAppManager::isEnabledForUser`.
- `\OC_Defaults::getLogoClaim`: no hay reemplazo.
- `\OCP\Util::linkToPublic`: no hay reemplazo.
- `\OC_Defaults::getLogoClaim`: no hay reemplazo.
- Se eliminó `\OC::$server->createEventSource()`; usar en su lugar `\OCP\Server::get(\OCP\IEventSourceFactory::class)->create()`.
- Se eliminó `\OCP\Util::writeLog`; usar en su lugar `\OCP\Server::get(LoggerInterface::class)->…`.

La fábrica `\OCP\IEventSourceFactory` solo funciona a partir de Nextcloud 28.
Para versiones anteriores, usar `\OC::$server->createEventSource()`.

Para admitir Nextcloud 27 y Nextcloud 28:

```php
// @TODO: Remove method_exists when min-version="28"
if (method_exists(\OC::$server, 'createEventSource')) {
    $eventSource = \OC::$server->createEventSource();
} else {
    $eventSource = \OCP\Server::get(IEventSourceFactory::class)->create();
}
```

#### Eventos añadidos

- Se añadió el evento tipado `OCA\DAV\Events\SabrePluginAddEvent`
- Se añadió el evento tipado `OCP\Accounts\UserUpdatedEvent`
- Se añadió el evento tipado `OCP\Authentication\TwoFactorAuth\TwoFactorProviderChallengeFailed`
- Se añadió el evento tipado `OCP\Authentication\TwoFactorAuth\TwoFactorProviderChallengePassed`
- Se añadió el evento tipado `OCP\Authentication\TwoFactorAuth\TwoFactorProviderForUserRegistered`
- Se añadió el evento tipado `OCP\Authentication\TwoFactorAuth\TwoFactorProviderForUserUnregistered`
- Se añadió el evento tipado `OCP\Authentication\TwoFactorAuth\TwoFactorProviderUserDeleted`
- Se añadió el evento tipado `OCP\Comments\CommentsEntityEvent`
- Evento tipado `OCP\DB\Events\AddMissingColumnsEvent` para añadir al esquema de la base de datos los índices que faltan.
- Evento tipado `OCP\DB\Events\AddMissingIndicesEvent` para añadir al esquema de la base de datos los índices que faltan.
- Evento tipado `OCP\DB\Events\AddMissingPrimaryKeyEvent` para añadir al esquema de la base de datos los índices que faltan.
- Se añadió el evento tipado `OCP\Files\Events\NodeAddedToFavorite`
- Se añadió el evento tipado `OCP\Files\Events\NodeRemovedFromFavorite`
- Se añadió el evento tipado `OCP\FilesMetadata\Event\MetadataBackgroundEvent`
- Se añadió el evento tipado `OCP\FilesMetadata\Event\MetadataLiveEvent`
- Se añadió el evento tipado `OCP\Share\Events\BeforeShareCreatedEvent`
- Se añadió el evento tipado `OCP\Share\Events\BeforeShareDeletedEvent`
- Se añadió el evento tipado `OCP\Share\Events\ShareAcceptedEvent`
- Se añadió el evento tipado `OCP\Share\Events\ShareDeletedFromSelfEvent`
- Se añadió el evento tipado `OCP\SystemTag\SystemTagsEntityEvent`
- Se añadió el evento tipado `OCP\User\Events\UserFirstTimeLoggedInEvent`

#### Eventos obsoletos

- `OC\Console\Application::run` quedó obsoleto. Escuchar en su lugar el evento tipado `OCP\Console\ConsoleEvent`
- `OCA\DAV\Connector\Sabre::addPlugin` quedó obsoleto. Escuchar en su lugar el evento tipado `OCA\DAV\Events\SabrePluginAddEvent`
- `OCA\Files_Trashbin::moveToTrash` quedó obsoleto. Escuchar en su lugar el evento tipado `OCA\Files_Trashbin\Events\MoveToTrashEvent`
- `OCA\Files_Trashbin::moveToTrash` quedó obsoleto. Escuchar en su lugar el evento tipado `OCA\Files_Trashbin\Events\MoveToTrashEvent`
- `OCP\Console\ConsoleEvent::EVENT_RUN` quedó obsoleto. Escuchar en su lugar el evento tipado `OCP\Console\ConsoleEvent`
- `OCP\Authentication\TwoFactorAuth\RegistryEvent` quedó obsoleto. Escuchar en su lugar los eventos tipados `OCP\Authentication\TwoFactorAuth\TwoFactorProviderForUserRegistered` y `OCP\Authentication\TwoFactorAuth\TwoFactorProviderForUserUnregistered`
- `OCP\Authentication\TwoFactorAuth\IRegistry::enable` quedó obsoleto. Escuchar en su lugar el evento tipado `OCP\Authentication\TwoFactorAuth\TwoFactorProviderForUserRegistered`
- `OCP\Authentication\TwoFactorAuth\IRegistry::disable` quedó obsoleto. Escuchar en su lugar el evento tipado `OCP\Authentication\TwoFactorAuth\TwoFactorProviderForUserUnregistered`
- `OCP\Authentication\TwoFactorAuth\TwoFactorProviderDisabled` quedó obsoleto. Escuchar en su lugar el evento tipado `OCP\Authentication\TwoFactorAuth\TwoFactorProviderUserDeleted`
- `OCP\Authentication\TwoFactorAuth\TwoFactorProviderForUserDisabled` quedó obsoleto. Escuchar en su lugar el evento tipado `OCP\Authentication\TwoFactorAuth\TwoFactorProviderChallengeFailed`
- `OCP\Authentication\TwoFactorAuth\TwoFactorProviderForUserEnabled` quedó obsoleto. Escuchar en su lugar el evento tipado `OCP\Authentication\TwoFactorAuth\TwoFactorProviderChallengePassed`
- `OCP\Comments\CommentsEntityEvent::EVENT_ENTITY` quedó obsoleto. Escuchar en su lugar el evento tipado `OCP\Comments\CommentsEntityEvent`
- `OCP\Comments\ICommentsManager::registerEntity` quedó obsoleto. Escuchar en su lugar el evento tipado `OCP\Comments\CommentsEntityEvent`
- `OCP\SystemTag\ISystemTagManager::registerEntity` quedó obsoleto. Escuchar en su lugar el evento tipado `OCP\SystemTag\SystemTagsEntityEvent`
- `OCP\SystemTag\SystemTagsEntityEvent::EVENT_ENTITY` quedó obsoleto. Escuchar en su lugar el evento tipado `OCP\SystemTag\SystemTagsEntityEvent`
- `OCP\IUser::firstLogin` quedó obsoleto. Escuchar en su lugar el evento tipado `OCP\User\Events\UserFirstTimeLoggedInEvent`

#### Eventos eliminados

- Se eliminó `OC\AccountManager::userUpdated`. Escuchar en su lugar el evento tipado `OCP\Accounts\UserUpdatedEvent`
- Se eliminó `OCA\Files::loadAdditionalScripts`. Escuchar en su lugar el evento tipado `OCA\Files\Event\LoadAdditionalScriptsEvent`
- Se eliminó `OCA\Files\Service\TagService::addFavorite`. Escuchar en su lugar el evento tipado `OCP\Files\Events\NodeAddedToFavorite`
- Se eliminó `OCA\Files\Service\TagService::removeFavorite`. Escuchar en su lugar el evento tipado `OCP\Files\Events\NodeRemovedFromFavorite`
- Se eliminó `OCA\Files_Sharing::loadAdditionalScripts`. Escuchar en su lugar el evento tipado `OCA\Files_Sharing\Event\BeforeTemplateRenderedEvent`
- Se eliminó `OCP\AppFramework\Http\TemplateResponse::EVENT_LOAD_ADDITIONAL_SCRIPTS` (obsoleto desde la 20). Escuchar en su lugar el evento tipado `OCP\AppFramework\Http\Events\BeforeTemplateRenderedEvent`
- Se eliminó `OCP\AppFramework\Http\TemplateResponse::EVENT_LOAD_ADDITIONAL_SCRIPTS_LOGGEDIN` (obsoleto desde la 20). Escuchar en su lugar el evento tipado `OCP\AppFramework\Http\Events\BeforeTemplateRenderedEvent`
- Se eliminó `OCP\AppFramework\Http\TemplateResponse::loadAdditionalScripts` (obsoleto desde la 20). Escuchar en su lugar el evento tipado `OCP\AppFramework\Http\Events\BeforeTemplateRenderedEvent`
- Se eliminó `OCP\AppFramework\Http\TemplateResponse::loadAdditionalScriptsLoggedIn` (obsoleto desde la 20). Escuchar en su lugar el evento tipado `OCP\AppFramework\Http\Events\BeforeTemplateRenderedEvent`
- Se eliminó `OCP\Authentication\TwoFactorAuth\IProvider::EVENT_SUCCESS` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\Authentication\TwoFactorAuth\TwoFactorProviderChallengePassed`
- Se eliminó `OCP\Authentication\TwoFactorAuth\IProvider::EVENT_FAILED` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\Authentication\TwoFactorAuth\TwoFactorProviderChallengeFailed`
- Se eliminó `OCP\Authentication\TwoFactorAuth\IProvider::failed` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\Authentication\TwoFactorAuth\TwoFactorProviderChallengeFailed`
- Se eliminó `OCP\Authentication\TwoFactorAuth\IProvider::success` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\Authentication\TwoFactorAuth\TwoFactorProviderChallengePassed`
- Se eliminó `OCP\IDBConnection::ADD_MISSING_COLUMNS` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\DB\Events\AddMissingColumnsEvent`
- Se eliminó `OCP\IDBConnection::ADD_MISSING_INDEXES` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\DB\Events\AddMissingIndicesEvent`
- Se eliminó `OCP\IDBConnection::ADD_MISSING_PRIMARY_KEYS` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\DB\Events\AddMissingPrimaryKeyEvent`
- Se eliminó `OCP\IDBConnection::CHECK_MISSING_COLUMNS` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\DB\Events\AddMissingColumnsEvent`
- Se eliminó `OCP\IDBConnection::CHECK_MISSING_COLUMNS_EVENT` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\DB\Events\AddMissingColumnsEvent`
- Se eliminó `OCP\IDBConnection::CHECK_MISSING_INDEXES` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\DB\Events\AddMissingIndicesEvent`
- Se eliminó `OCP\IDBConnection::CHECK_MISSING_INDEXES_EVENT` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\DB\Events\AddMissingIndicesEvent`
- Se eliminó `OCP\IDBConnection::CHECK_MISSING_PRIMARY_KEYS` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\DB\Events\AddMissingPrimaryKeyEvent`
- Se eliminó `OCP\IDBConnection::CHECK_MISSING_PRIMARY_KEYS_EVENT` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\DB\Events\AddMissingPrimaryKeyEvent`
- Se eliminó `OCP\IGroup::postAddUser`. Escuchar en su lugar el evento tipado `OCP\Group\Events\UserAddedEvent`
- Se eliminó `OCP\IGroup::postDelete`. Escuchar en su lugar el evento tipado `OCP\Group\Events\GroupDeletedEvent`
- Se eliminó `OCP\IGroup::postRemoveUser`. Escuchar en su lugar el evento tipado `OCP\Group\Events\UserRemovedEvent`
- Se eliminó `OCP\IGroup::preAddUser`. Escuchar en su lugar el evento tipado `OCP\Group\Events\BeforeUserAddedEvent`
- Se eliminó `OCP\IGroup::preDelete`. Escuchar en su lugar el evento tipado `OCP\Group\Events\BeforeGroupDeletedEvent`
- Se eliminó `OCP\IGroup::preRemoveUser`. Escuchar en su lugar el evento tipado `OCP\Group\Events\BeforeUserRemovedEvent`
- Se eliminó `OCP\IPreview::EVENT` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\Preview\BeforePreviewFetchedEvent`
- Se eliminó `OCP\IPreview:PreviewRequested` (obsoleto desde la 22). Escuchar en su lugar el evento tipado `OCP\Preview\BeforePreviewFetchedEvent`
- Se eliminó `OCP\IUser::changeUser`. Escuchar en su lugar el evento tipado `OCP\User\Events\UserChangedEvent`
- Se eliminó `OCP\IUser::postDelete` (obsoleto desde la 17). Escuchar en su lugar el evento tipado `OCP\User\Events\UserDeletedEvent`
- Se eliminó `OCP\IUser::postSetPassword`. Escuchar en su lugar el evento tipado `OCP\User\Events\PasswordUpdatedEvent`
- Se eliminó `OCP\IUser::preDelete` (obsoleto desde la 17). Escuchar en su lugar el evento tipado `OCP\User\Events\BeforeUserDeletedEvent`
- Se eliminó `OCP\IUser::preSetPassword`. Escuchar en su lugar el evento tipado `OCP\User\Events\BeforePasswordUpdatedEvent`
- Se eliminó `OCP\Share::preShare`. Escuchar en su lugar el evento tipado `OCP\Share\Events\BeforeShareCreatedEvent`
- Se eliminó `OCP\Share::preUnshare`. Escuchar en su lugar el evento tipado `OCP\Share\Events\BeforeShareDeletedEvent`
- Se eliminó `OCP\Share::postAcceptShare`. Escuchar en su lugar el evento tipado `OCP\Share\Events\ShareAcceptedEvent`
- Se eliminó `OCP\Share::postShare`. Escuchar en su lugar el evento tipado `OCP\Share\Events\ShareCreatedEvent`
- Se eliminó `OCP\Share::postUnshare`. Escuchar en su lugar el evento tipado `OCP\Share\Events\ShareDeletedEvent`
- Se eliminó `OCP\Share::postUnshareFromSelf`. Escuchar en su lugar el evento tipado `OCP\Share\Events\ShareDeletedFromSelfEvent`
- Se eliminó `OCP\WorkflowEngine::registerChecks` (obsoleto desde la 17). Escuchar en su lugar el evento tipado `OCP\WorkflowEngine\Events\RegisterChecksEvent`
- Se eliminó `OCP\WorkflowEngine::registerEntities` (obsoleto desde la 17). Escuchar en su lugar el evento tipado `OCP\WorkflowEngine\Events\RegisterEntitiesEvent`
- Se eliminó `OCP\WorkflowEngine::registerOperations` (obsoleto desde la 17). Escuchar en su lugar el evento tipado `OCP\WorkflowEngine\Events\RegisterOperationsEvent`
- Se eliminó `\OCP\Collaboration\Resources::loadAdditionalScripts`. Escuchar en su lugar el evento tipado `OCP\Collaboration\Resources\LoadAdditionalScriptsEvent`

#### Propiedades WebDAV eliminadas

- \<nc:file-metadata-size>
- \<nc:file-metadata-gps>
````
