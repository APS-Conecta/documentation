---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 31 para las apps: diseño de plantillas sin main, CSS lógico, comparticiones públicas en Vue, PHP 8.4 y alias de DI eliminados."
---
# Actualización a Nextcloud 31

## Resumen

Esta página enumera los cambios de la versión 31 que afectan a las apps: el nuevo diseño de las plantillas de usuario, de invitado y pública, las reglas CSS de posición lógica, las comparticiones públicas en el frontend de Vue, la compatibilidad con PHP 8.4 y las API añadidas, modificadas, obsoletas o eliminadas, incluidos los alias de inyección de dependencias retirados. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_31.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Cambios de frontend

#### Diseño de las plantillas de usuario, de invitado y pública

Se cambió el diseño principal de todas las apps (las plantillas de usuario, de invitado y pública):
el contenido principal ya no se representa dentro de un elemento `<main>` con la clase `content`, sino en un elemento `div` con la clase `content`.
El motivo es permitir escribir apps basadas en Vue 3, que de lo contrario representarían incorrectamente dos elementos `main` apilados.

Para las apps Vue 2 esto **no cambia nada**.
Pero si solo se usan plantillas simples (vanilla) u otros frameworks, esto cambia el diseño de la página y podría requerir ajustes.
Se recomienda envolver el contenido en un elemento `main` propio si no se usa ningún framework o si no se usa Vue como framework.

#### Reglas CSS de posición lógica

Con Nextcloud 31, todos los estilos que aporta el servidor se migraron para usar [posicionamiento lógico](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values)
en lugar de físico, lo que permite que el diseño del frontend se adapte a distintas direcciones de idioma (de derecha a izquierda).
Se anima encarecidamente a quienes desarrollan apps a migrar también sus apps al posicionamiento lógico.

Ejemplos de posicionamiento lógico frente a físico:

- `margin-inline-start: 4px;` en lugar de `margin-left: 4px;`
- `inset-inline-end: 8px;` en lugar de `right: 8px`

#### Archivos y compartición de archivos

Con Nextcloud 28, el frontend de la app Archivos se migró a Vue y se eliminó la API privada ( `OCA.Files` ),
pero para las comparticiones públicas se seguía usando el frontend heredado. Con Nextcloud 31, las comparticiones públicas también usan el nuevo frontend de Vue.
Esto significa que ya no es posible acceder a la API privada heredada de `OCA.Files`; todas las apps existentes deben migrar a la {nc-ref}`API pública <js-library_nextcloud-files>`.

Para facilitar la migración, el {nc-ref}`paquete <js-library_nextcloud-sharing>` `@nextcloud/sharing` ofrece funciones de utilidad
para comprobar si la instancia actual de la app Archivos es una compartición pública y, en tal caso, obtener el token de la compartición.

```JavaScript
import { isPublicShare, getSharingToken } from '@nextcloud/sharing/public'

if (isPublicShare()) {
    console.info('This is a public share with the sharing token: ', getSharingToken())
}
```

#### API eliminadas

- `OCA.FilesSharingDrop` se eliminó como parte de la migración a Vue. Usar la API de la app Archivos que proporciona el {nc-ref}`paquete <js-library_nextcloud-files>` .
- Se eliminó de la app Notificaciones el evento jQuery `$.Event('OCA.Notification.Action')` como parte de la migración a Vue. Usar en su lugar el {nc-ref}`paquete <js-library_nextcloud-event-bus>` `@nextcloud/event-bus`.

```JavaScript
import { subscribe, unsubscribe } from '@nextcloud/event-bus'

subscribe('notifications:action:execute', (event) => {
    console.info('Notification action has been executed:', event.notification, event.action)
})
```

### Cambios de backend

#### Se añadió la compatibilidad con PHP 8.4

En esta versión se añadió la compatibilidad con PHP 8.4. Seguir los pasos siguientes para que la app sea compatible.

1. Si `appinfo/info.xml` tiene una especificación de dependencia para PHP, aumentar `max-version` a 8.4.
Sin embargo, se recomienda admitir siempre todas las versiones de PHP que son compatibles con la versión de Nextcloud admitida.
En ese caso, las entradas de dependencias de `php` pueden omitirse.

```xml
<dependencies>
  <php min-version="8.1" max-version="8.4" />
  <nextcloud min-version="29" max-version="31" />
</dependencies>
```

2. Si la app tiene un `composer.json` y el archivo contiene las restricciones de PHP de `info.xml`, ajustarlo también.

```json
{
  "require": {
    "php": ">=8.1 <=8.4"
  }
}
```

3. Si se tiene configurada la {nc-ref}`integración continua <app-ci>`, ampliar la matriz de pruebas con pruebas y linters de PHP 8.4.
Esto ocurre automáticamente al reutilizar nuestras [plantillas de GitHub Workflow](https://github.com/nextcloud/.github),
pero también se puede usar directamente la [Action icewind1991/nextcloud-version-matrix](https://github.com/icewind1991/nextcloud-version-matrix) subyacente.

La información sobre los cambios de código se encuentra en [php.net](https://www.php.net/migration84) y [stitcher.io](https://stitcher.io/blog/new-in-php-84).

#### API añadidas

- Ahora es posible descargar carpetas como archivos zip o tar mediante el backend WebDAV, con solicitudes {code}`GET`.
  Ver la {nc-ref}`documentación del endpoint <webdav-download-folders>` correspondiente.
- Se añadió `OCP\SetupCheck\CheckServerResponseTrait` para facilitar la implementación de {nc-ref}`comprobaciones de configuración <setup-checks>` personalizadas
  que necesitan comprobar llamadas HTTP al propio servidor.
- Cualquier implementación de `OCP\Files\Mount\IMountPoint` puede implementar además `OCP\Files\Mount\IShareOwnerlessMount`, lo que permite que cualquiera con permiso de compartir edite y elimine cualquier compartición de los archivos y directorios situados bajo el punto de montaje.
- `OCP\Navigation\Events\LoadAdditionalEntriesEvent` se despacha cuando el gestor de navegación necesita conocer sus entradas, aparte de las entradas estándar de las apps, que se cargan automáticamente. Solo es relevante para las apps que aportan entradas adicionales.
- Se añadió `OCP\User\Backend\ILimitAwareCountUsersBackend` como reemplazo de `ICountUsersBackend`. Permite indicar un límite para el recuento de usuarios, para no contar todos los usuarios cuando quien llama no lo necesita. Se puede ignorar el límite sin problema si no tiene sentido para el caso de uso.
- Si una app admite la conversión de archivos, ahora puede registrar un `OCP\Files\Conversion\ConversionProvider`, al que se
  llamará automáticamente según los tipos MIME admitidos. Una app puede registrar tantos como necesite.
- Se añadieron los nuevos eventos `OCP\User\Events\BeforeUserIdUnassignedEvent`, `OCP\User\Events\UserIdUnassignedEvent` y `OCP\User\Events\UserIdAssignedEvent` para reemplazar los hooks `\OC\User::preUnassignedUserId`, `\OC\User::postUnassignedUserId` y `\OC\User::assignedUserId`.
- Nueva interfaz `OCP\Files\Storage\IConstructableStorage` para los almacenamientos que pueden construirse pasando solo un array al constructor.
- Nuevo servicio `OCP\RichObjectStrings\IRichTextFormatter` para convertir texto enriquecido en texto plano analizado mediante su método `richToParsed`.
- Nuevo parámetro de consulta mágico `forceLanguage` para forzar un idioma concreto en una solicitud web (API o frontend). Ver {nc-ref}`Forzar el idioma de una llamada <api-force-language>`.
- Se añadió la nueva propiedad WebDAV `nc:hide-download` para indicar si las acciones de descarga deben ocultarse para un archivo o una carpeta compartidos.
- Se añadió `OCP\Security\PasswordContext`, que permite definir el contexto en el que se usará una contraseña.
  Lo usan `GenerateSecurePasswordEvent` y `ValidatePasswordPolicyEvent`, lo que permite aplicar reglas distintas para contextos distintos.

#### API modificadas

- Se aclara que `OCP\Files\Storage\IStorage::getOwner()` devuelve `string|false`.
- Se añadieron tipos de parámetros y de retorno de los métodos a todas las clases que heredan de `OCP\Files\Storage\IStorage`. Para migrar de forma compatible con versiones anteriores:

  1. Añadir ahora todos los tipos de retorno a la implementación.
  2. Añadir todos los tipos de parámetros a la implementación cuando Nextcloud 31 sea la versión mínima admitida.

- La implementación de Nextcloud del método `log` de `Psr\Log\LoggerInterface` admite ahora `Psr\Log\LogLevel` como parámetro de nivel de registro.
- `OCP\DB\QueryBuilder\IQueryBuilder` admite ahora más tipos de parámetros relacionados con la fecha y la hora:

  - `PARAM_DATE_MUTABLE` y `PARAM_DATE_IMMUTABLE` para pasar una instancia de `\DateTime` (o de `\DateTimeImmutable`, respectivamente) cuando solo interesa la parte de la fecha.
  - `PARAM_TIME_MUTABLE` y `PARAM_TIME_IMMUTABLE` para pasar una instancia de `\DateTime` (o de `\DateTimeImmutable`, respectivamente) cuando solo interesa la parte de la hora.
  - `PARAM_DATETIME_MUTABLE` y `PARAM_DATETIME_IMMUTABLE` para pasar una instancia de `\DateTime` (o de `\DateTimeImmutable`, respectivamente) sin gestión de la zona horaria.
  - `PARAM_DATETIME_TZ_MUTABLE` y `PARAM_DATETIME_TZ_IMMUTABLE` para pasar una instancia de `\DateTime` (o de `\DateTimeImmutable`, respectivamente) con gestión de la zona horaria.

- `OCP\\DB\\Types` admite ahora más tipos relacionados con la fecha y la hora para usarlos con la `Entity`:

  - `DATE_IMMUTABLE` para los campos que se (de)serializarán como instancias de `\DateTimeImmutable` con solo la parte de la fecha establecida.
  - `TIME_IMMUTABLE` para los campos que se (de)serializarán como instancias de `\DateTimeImmutable` con solo la parte de la hora establecida.
  - `DATETIME_IMMUTABLE` para los campos que se (de)serializarán como instancias de `\DateTimeImmutable` con también la parte de la hora establecida, pero sin información de zona horaria.
  - `DATETIME_TZ` para los campos que se (de)serializarán como instancias de `\DateTime` con también la parte de la hora establecida y con información de zona horaria.
  - `DATETIME_TZ_IMMUTABLE` para los campos que se (de)serializarán como instancias de `\DateTimeImmutable` con también la parte de la hora establecida y con información de zona horaria.

- Ahora es posible paginar las solicitudes DAV con nuevas cabeceras.

  - La primera solicitud debe contener las siguientes cabeceras:

    - `X-NC-Paginate: true` activa la funcionalidad
    - `X-NC-Paginate-Count: X` establece el número de resultados por página (100 por defecto)

  - El servidor responderá con nuevas cabeceras:

    - `X-NC-Paginate-Total` indica el número total de resultados.
    - `X-NC-Paginate-Token` proporciona un token para acceder a otras páginas del mismo resultado.

  - Emitir nuevas solicitudes con el token:

    - `X-NC-Paginate-Token: xxx` contiene el token tal como lo envió el servidor
    - `X-NC-Paginate-Count: X` establece el número de resultados por página (100 por defecto)
    - `X-NC-Paginate-Offset: Y` establece el desplazamiento (número de resultados ignorados) para la página solicitada (normalmente «page_number × page_size»)

- La clase heredada `OC_Image` se trasladó a `OC\Image`. Nunca debe usarse directamente; en su lugar, usar `new \OCP\Image()` para construir el objeto y la interfaz `OCP\IImage` para llamar a los métodos.
- El constructor de `OCP\Preview\BeforePreviewFetchedEvent` tiene un nuevo parámetro, `$mimeType`, que debe ser una cadena o null.
- Tiene un nuevo método, `getMimeType()`, para obtener la nueva propiedad.
- El método `OCP\Files\Storage::needsPartFile` se trasladó a la interfaz `OCP\Files\Storage\IStorage`.
- Se eliminó el constructor de la interfaz `OCP\Files\Storage\IStorage` para que los wrappers puedan usar DI en su constructor. Si la implementación del almacenamiento debe construirse llamando al constructor, implementar la nueva interfaz `OCP\Files\Storage\IConstructableStorage`.
- Se añadió el método `OCP\IUser::getFirstLogin` para obtener el primer inicio de sesión conocido de un usuario. Devolverá una marca de tiempo unix, o 0 si el usuario nunca inició sesión, o -1 si no se conoce este dato (lo que significa que el primer inicio de sesión de este usuario fue anterior a la actualización a la 31).
- `OCP\Security\GenerateSecurePasswordEvent` y `OCP\Security\ValidatePasswordPolicyEvent` tienen ahora un método `getContext` que devuelve el contexto de la contraseña,
  lo que permite aplicar reglas distintas para contextos distintos.

#### API obsoletas

- El endpoint `/s/{token}/download` para descargar comparticiones públicas está obsoleto.
  En su lugar, usar el {nc-ref}`endpoint WebDAV <webdav-download-folders>` que proporciona Nextcloud.
- `OCP\DB\QueryBuilder\IQueryBuilder::PARAM_DATE` está obsoleto en favor de `PARAM_DATETIME_MUTABLE`,
  para dejar claro que este tipo también incluye la parte de la hora de una instancia de fecha y hora.
- `OCP\User\Backend\ICountUsersBackend` quedó obsoleto. Implementar y usar en su lugar `OCP\User\Backend\ILimitAwareCountUsersBackend`.
- Los hooks `\OC\User::preUnassignedUserId`, `\OC\User::postUnassignedUserId` y `\OC\User::assignedUserId` están obsoletos; usar en su lugar los nuevos eventos de OCP.

#### API eliminadas

- Se eliminó `OC_App::getForms`, heredado y no funcional.
- Se eliminó la clase privada y heredada `OC_Files`.
  En su lugar, usar `OCP\AppFramework\Http\StreamResponse` o `OCP\AppFramework\Http\ZipResponse`.
- Se eliminó el endpoint Ajax privado y heredado para descargar archivos comprimidos (`/apps/files/ajax/download.php`).
  En su lugar, usar el {nc-ref}`endpoint WebDAV <webdav-download-folders>` que proporciona Nextcloud.
- Se eliminaron todos los métodos de registro de `OCP\ILogger`, obsoletos desde Nextcloud 20.
  - La interfaz ahora solo contiene las constantes de nivel de registro internas de Nextcloud.
    Para todo el registro debe usarse `Psr\Log\LoggerInterface`.
  - La interfaz `OCP\ILogger` ya no puede inyectarse como dependencia, ya que ahora solo contiene constantes.
  - Se eliminó `OCP\IServerContainer::getLogger`; usar en su lugar la inyección de dependencias con `Psr\Log\LoggerInterface`.
- Se eliminó la clase interna `OC\AppFramework\Logger`; nunca debería haberla usado ninguna app.
  Todas las apps que la usan deben migrar a `Psr\Log\LoggerInterface`.
- Se eliminó el endpoint heredado para probar el endpoint de compartición remota (`/testremote`).
- La clase heredada `OC_API` se trasladó a un espacio de nombres privado. Las aplicaciones no deberían necesitarla.
- Se eliminó la interfaz obsoleta `OCP\Files\Storage`. Usar `OCP\Files\Storage\IStorage` en su lugar.
- Se eliminaron los alias obsoletos de la inyección de dependencias; usar en su lugar las interfaces o los nombres de clase:

:::{list-table} Alias obsoletos eliminados
:header-rows: 1

* - Alias eliminado
  - Reemplazar por
* - CalendarManager
  - `OCP\Calendar\IManager::class`
* - CalendarResourceBackendManager
  - `OCP\Calendar\Resource\IManager::class`
* - CalendarRoomBackendManager
  - `OCP\Calendar\Room\IManager::class`
* - ContactsManager
  - `OCP\Contacts\IManager::class`
* - PreviewManager
  - `OCP\IPreview::class`
* - EncryptionManager
  - `OCP\Encryption\IManager::class`
* - EncryptionFileHelper
  - `OCP\Encryption\IFile::class`
* - EncryptionKeyStorage
  - `OCP\Encryption\Keys\IStorage::class`
* - TagMapper
  - `OC\Tagging\TagMapper::class`
* - TagManager
  - `OCP\ITagManager::class`
* - SystemTagObjectMapper
  - `OCP\SystemTag\ISystemTagObjectMapper::class`
* - LazyRootFolder
  - `OCP\Files\IRootFolder::class`
* - UserManager
  - `OCP\IUserManager::class`
* - GroupManager
  - `OCP\IGroupManager::class`
* - UserSession
  - `OCP\IUserSession::class::class`
* - NavigationManager
  - `OCP\INavigationManager::class`
* - AllConfig
  - `OCP\IConfig::class`
* - SystemConfig
  - `OC\SystemConfig::class`
* - AppConfig
  - `OCP\IAppConfig::class`
* - L10NFactory
  - `OCP\L10N\IFactory::class`
* - URLGenerator
  - `OCP\IURLGenerator::class`
* - AppFetcher
  - `OC\App\AppStore\Fetcher\AppFetcher::class`
* - CategoryFetcher
  - `OC\App\AppStore\Fetcher\CategoryFetcher::class`
* - UserCache
  - `OCP\ICache::class`
* - MemCacheFactory
  - `OCP\ICacheFactory::class`
* - ActivityManager
  - `OCP\Activity\IManager::class`
* - AvatarManager
  - `OCP\IAvatarManager::class`
* - Logger
  - `OCP\ILogger::class` (pero usar LoggerInterface en su lugar)
* - JobList
  - `OCP\BackgroundJob\IJobList::class`
* - Router
  - `OCP\Route\IRouter::class`
* - SecureRandom
  - `OCP\Security\ISecureRandom::class`
* - Crypto
  - `OCP\Security\ICrypto::class`
* - Hasher
  - `OCP\Security\IHasher::class`
* - CredentialsManager
  - `OCP\Security\ICredentialsManager::class`
* - DatabaseConnection
  - `OCP\IDBConnection::class`
* - EventLogger
  - `OCP\Diagnostics\IEventLogger::class`
* - QueryLogger
  - `OCP\Diagnostics\IQueryLogger::class`
* - TempManager
  - `OCP\ITempManager::class`
* - AppManager
  - `OCP\App\IAppManager::class`
* - DateTimeZone
  - `OCP\IDateTimeZone::class`
* - DateTimeFormatter
  - `OCP\IDateTimeFormatter::class`
* - UserMountCache
  - `OCP\Files\Config\IUserMountCache::class`
* - MountConfigManager
  - `OCP\Files\Config\IMountProviderCollection::class`
* - IniWrapper
  - `bantu\IniGetWrapper\IniGetWrapper::class`
* - AsyncCommandBus
  - `OCP\Command\IBus::class`
* - TrustedDomainHelper
  - `OCP\Security\ITrustedDomainHelper::class`
* - Throttler
  - `OCP\Security\Bruteforce\IThrottler::class`
* - Request
  - `OCP\IRequest::class`
* - Mailer
  - `OCP\Mail\IMailer::class`
* - LDAPProvider
  - `OCP\LDAP\ILDAPProvider::class`
* - LockingProvider
  - `OCP\Lock\ILockingProvider::class`
* - MountManager
  - `OCP\Files\Mount\IMountManager::class`
* - MimeTypeDetector
  - `IMimeTypeDetector::class`
* - MimeTypeLoader
  - `OCP\Files\IMimeTypeLoader::class`
* - NotificationManager
  - `OCP\Notification\IManager::class`
* - CapabilitiesManager
  - `OC\CapabilitiesManager::class`
* - CommentsManager
  - `OCP\Comments\ICommentsManager::class`
* - CsrfTokenManager
  - `OC\Security\CSRF\CsrfTokenManager::class`
* - ContentSecurityPolicyManager
  - `OCP\Security\IContentSecurityPolicyManager::class`
* - ShareManager
  - `OCP\Share\IManager::class`
* - CollaboratorSearch
  - `OCP\Collaboration\Collaborators\ISearch::class`
* - ControllerMethodReflector
  - `OCP\AppFramework\Utility\IControllerMethodReflector::class`
* - TimeFactory
  - `OCP\AppFramework\Utility\ITimeFactory::class`
* - Defaults
  - `OCP\Defaults::class`
:::
````
