---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 30 para las apps: dependencia de backend caldav, diseño más compacto, nonce de CSP, fin de PHP 8.0 y TaskProcessing."
---
# Actualización a Nextcloud 30

## Resumen

Esta página enumera los cambios de la versión 30 que afectan a las apps: el nuevo tipo de dependencia `backend`, las capacidades de `files`, el diseño más compacto y sus variables CSS, el nonce de CSP, el fin de PHP 8.0 y las API añadidas, modificadas, obsoletas o eliminadas, entre ellas el paso a `OCP\TaskProcessing`. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_30.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### General

Se añadió a info.xml un nuevo tipo de dependencia, `backend`.
Si la app requiere o usa el backend CalDAV del servidor, añadir el backend
`caldav` a las dependencias de la app.

```xml
<dependencies>
    <backend>caldav</backend>
</dependencies>
```

Si ninguna app requiere el backend CalDAV, la sección CalDAV de las configuraciones de administración se ocultará.
Por ahora no hay ningún otro efecto, pero eso podría cambiar en el futuro.

### Capacidades

#### `files`

- `blacklist_files_regex` está ahora obsoleto; usar `forbidden_filenames` en su lugar
- Se añadió `forbidden_filename_characters` para proporcionar una lista de caracteres no permitidos en los nombres de archivo
- Se añadió `forbidden_filename_extensions` para proporcionar una lista de extensiones (sufijos) no permitidas en los nombres de archivo

### Cambios de frontend

El diseño general se cambió para que sea menos redondeado y más compacto;
como parte de ello, con Nextcloud 30 se añadieron algunas variables CSS y otras quedaron obsoletas, ver {nc-ref}`cssvars`.

#### Área clicable

El tamaño de la variable CSS `--default-clickable-area` se redujo de `44px` a `34px`.
Esto provocará varias regresiones y pequeños fallos en la app que habrá que corregir manualmente.
Se recomienda:

1. Enlazar a la app la rama master actual de `@nextcloud/vue` (hacer pull a menudo, porque también se van incorporando correcciones);
2. Buscar en todo el código *44px* y reemplazarlo por la variable *--default-clickable-area* cuando corresponda;
3. Comprobar si hay regresiones y fallos visuales;
4. Informar de la regresión de la app en esta issue (se puede crear un encabezado con el nombre de la propia app);
5. Informar también de las regresiones de la biblioteca `@nextlcoud/vue` si aún no están informadas en su lista;
6. Corregir las regresiones de la app (solo las que no tienen relación con los componentes de `@nextcloud/vue`);

Además, para distintos casos de uso, se añadieron también dos nuevas variables:

- `--clickable-area-large` para los elementos principales de la interfaz.
- `--clickable-area-small`, que representa el tamaño más pequeño posible de los elementos interactivos, usado por acciones terciarias como los chips de filtro.

#### Altura de línea

La variable `--default-line-height` cambió de `` 24px` `` a `1.5` para el `--default-font-size`, lo que
significa que el valor real en píxeles pasará de 24 a 22.5. Aunque es un cambio pequeño, se recomienda
comprobar si hay regresiones visuales en la app.

#### Tamaños de fuente

Nextcloud ahora proporciona estilos predeterminados con sentido para los elementos de encabezado.
Esto puede causar regresiones visuales si el código no establece explícitamente el tamaño y el peso de la fuente.
Si se necesitan elementos de encabezado fuera del contenido de texto, puede que haya que ajustar sus estilos.

#### Radio del borde

Las variables CSS del radio del borde se refactorizaron:

- Añadidas

  - Se añadió `--border-radius-small` para elementos más pequeños, como los chips.
  - Se añadió `--border-radius-container` para contenedores más pequeños, como los menús de acciones.
  - Se añadió `--border-radius-container-large` para contenedores más grandes, como el body o los modales.
  - Se añadió `--border-radius-element` para elementos interactivos como botones, campos de entrada, navegación y elementos de lista.

- Obsoletas

  - `--border-radius` está ahora obsoleta en favor de `--border-radius-small`.
  - `--border-radius-large` está ahora obsoleta en favor de `--border-radius-element`.
  - `--border-radius-pill` está ahora obsoleta en favor de `--border-radius-element`.
  - `--border-radius-rounded` está ahora obsoleta en favor de `--border-radius-container`.

#### Nonce de CSP

Se corrigió un error que impedía a Nextcloud usar la variable de entorno `CSP_NONCE`;
esto significa ahora que el nonce de CSP para los recursos JavaScript ya no se basa (o no está garantizado que se base) en el token CSRF.
En su lugar, quienes administran pueden optar por usar un token generado de otra manera.
Al usar módulos JavaScript esto no supone ninguna diferencia, ya que se importan y el nonce solo tiene que establecerse en el módulo raíz (lo hace Nextcloud),
pero si se usa Webpack o se cargan scripts dinámicamente de otra forma, ahora hay que ajustar la gestión del nonce de CSP.

Obtener el nonce de CSP:

- O bien usar `getCSPNonce` del {nc-ref}`paquete <js-library_nextcloud-auth>` `@nextcloud/auth`, que también es compatible con versiones anteriores.
- O bien leer directamente el nonce de la etiqueta `<meta name="csp-nonce" />`.

Al usar Webpack:

```diff
- import { getRequestToken } from '@nextcloud/auth'
- __webpack_nonce__ = btoa(getRequestToken())
+ import { getCSPNonce } from '@nextcloud/auth'
+ __webpack_nonce__ = getCSPNonce()
```

#### API obsoletas

- `OC.config.blacklist_files_regex` está ahora obsoleto; usar en su lugar las capacidades de `files`
- `OC.config.forbidden_filename_characters` está ahora obsoleto; usar en su lugar las capacidades de `files`
- `OC.dialogs.fileexists` ya estaba obsoleto en Nextcloud 29, pero ahora también está marcado como tal.
  Usar en su lugar `openConflictPicker` de [@nextcloud/upload](https://nextcloud-libraries.github.io/nextcloud-upload/functions/openConflictPicker.html).
- La mayor parte de la API `OC.dialogs` está ahora obsoleta y se eliminará en el futuro. Para diálogos genéricos, usar el `DialogBuilder` de {nc-ref}`js-library_nextcloud-dialogs`.
  Lista de los métodos que ahora están obsoletos:

  - `OC.dialogs.alert`
  - `OC.dialogs.info`
  - `OC.dialogs.confirm`
  - `OC.dialogs.confirmDestructive`
  - `OC.dialogs.confirmHtml`
  - `OC.dialogs.prompt`
  - `OC.dialogs.message`

### Cambios de backend

#### Se eliminó la compatibilidad con PHP 8.0

En esta versión se eliminó la compatibilidad con PHP 8.0. Seguir los pasos siguientes para que la app sea compatible.

1. Si `appinfo/info.xml` tiene una especificación de dependencia para PHP, aumentar `min-version` a 8.1.

```xml
<dependencies>
  <php min-version="8.1" max-version="8.3" />
  <nextcloud min-version="27" max-version="30" />
</dependencies>
```

2. Si la app tiene un `composer.json` y el archivo contiene las restricciones de PHP de `info.xml`, ajustarlo también.

```json
{
  "require": {
    "php": ">=8.1 <=8.3"
  }
}
```

3. Si se tiene configurada la {nc-ref}`integración continua <app-ci>`, quitar PHP 8.0 de las matrices de pruebas y de linters.

#### API añadidas

- `OCP\Activity\Exceptions\FilterNotFoundException` la lanza `OCP\Activity\IManager::getFilterById()` cuando no hay ningún filtro registrado con el identificador dado
- `OCP\Activity\Exceptions\IncompleteActivityException` la lanza `OCP\Activity\IManager::publish()` cuando no se han establecido todos los campos obligatorios en el objeto `OCP\Activity\IEvent`
- `OCP\Activity\Exceptions\InvalidValueException` la lanza `OCP\Activity\IEvent::set*()` cuando el valor no cumple los criterios requeridos
- `OCP\Activity\Exceptions\SettingNotFoundException` la lanza `OCP\Activity\IManager::getSettingById()` cuando no hay ningún ajuste registrado con el identificador dado
- `OCP\Activity\Exceptions\UnknownActivityException` debe lanzarla `OCP\Activity\IProvider::parse()` cuando no haya gestionado el evento
- Se añadió `OCP\AppFramework\Db\QbMapper::yieldEntities()` para permitir iterar sobre entidades devolviendo un `Generator`, sin cargarlas todas en memoria.
- Se introdujeron las constantes `OCP\Authentication\Token\IToken::SCOPE_FILESYSTEM` y `OCP\Authentication\Token\IToken::SCOPE_SKIP_PASSWORD_VALIDATION` como constantes para los ámbitos de los tokens. Antes, el valor de `SCOPE_FILESYSTEM` estaba fijado en el código.
- `OCP\Notification\IncompleteNotificationException` la lanza `OCP\Notification\IManager::notify()` cuando no se han establecido todos los campos obligatorios en el objeto `OCP\Notification\INotification`
- `OCP\Notification\IncompleteParsedNotificationException` la lanza `OCP\Notification\IManager::prepare()` cuando ningún `OCP\Notification\INotifier` gestionó el objeto `OCP\Notification\INotification`
- `OCP\Notification\InvalidValueException` la lanzan `OCP\Notification\IAction::set*()` y `OCP\Notification\INotification::set*()` cuando el valor no cumple los criterios requeridos
- `OCP\Notification\UnknownNotificationException` debe lanzarla `OCP\Notification\INotifier::prepare()` cuando no haya gestionado la notificación
- `OCA\Files_Trashbin\Trash\ITrashItem::getDeletedBy()` debe devolver el usuario que eliminó el elemento, o null si se desconoce
- `OCP\IUser::getPasswordHash()` debe devolver el hash de la contraseña del usuario
- `OCP\IUser::setPasswordHash()` debe establecer el hash de la contraseña del usuario
- Atributo `OCP\AppFramework\Http\Attribute\OpenAPI::SCOPE_EX_APP` para limitar el ámbito de las API a que solo las usen las ExApps.
- Atributo `OCP\AppFramework\Http\Attribute\ExAppRequired` para restringir los métodos de controlador para que solo sean accesibles por las ExApps.
- Se añadió `OCP\Collaboration\Reference\IPublicReferenceProvider` para los proveedores de referencias que admiten búsquedas de referencias desde comparticiones públicas.
- Se añadió `OCP\Files\IFilenameValidator` para permitir validar nombres de archivo independientemente del almacenamiento.
- Se añadió `OCP\Files\Storage\IStorage::setOwner()` para permitir establecer el propietario de un almacenamiento, de modo que pueda gestionarse independientemente del usuario de la sesión actual. Esto es especialmente útil para los almacenamientos con propiedad compartida, como las carpetas de grupo o los almacenamientos externos, en los que el propietario del almacenamiento debe establecerse en el usuario que inicializa el almacenamiento a través de su punto de montaje personal.
- Se añadió `ShareAPIController::sendShareEmail()`, accesible mediante ocs en `/api/v1/shares/{shareId}/send-email`. Ver la documentación de {nc-ref}`send-email <Send email>`.
- Se añadió `OCP\Calendar\Room\IManager::update()` para actualizar en el momento todas las salas de todos los backends.
- Se añadió `OCP\Calendar\Resource\IManager::update()` para actualizar en el momento todos los recursos de todos los backends.
- Se añadió `OCP\App\IAppManager::BACKEND_CALDAV` para representar la dependencia del backend caldav en `isBackendRequired()`.
- Se añadió `OCP\App\IAppManager::isBackendRequired()` para comprobar si al menos una app requiere un backend concreto (actualmente solo `caldav`).
- Se añadió `OCP\Accounts\IAccountManager::PROPERTY_BIRTHDATE` para permitir que los usuarios configuren su fecha de nacimiento en sus perfiles.
- Se añadió `` OCP\TaskProcessing` `` para unificar el procesamiento de tareas de IA y de otros tipos de tareas. Ver {nc-ref}`Procesamiento de tareas <task_processing>`
- Se añadió `OCP\AppFramework\Bootstrap\IRegistrationContext::registerTaskProcessingProvider()` para permitir registrar proveedores de procesamiento de tareas
- Se añadió `OCP\AppFramework\Bootstrap\IRegistrationContext::registerTaskProcessingTaskType()` para permitir registrar tipos de tarea de procesamiento de tareas
- Se añadió `OCP\Files\IRootFolder::getAppDataDirectoryName()` para permitir obtener el nombre del directorio de datos de la app
- Se añadió `OCP\Console\ReservedOptions`, que contiene constantes para las opciones reservadas para funciones del núcleo de occ. `--debug-log` y `--debug-log-level` quedan ahora reservadas por occ, ya que permiten mostrar información de depuración en la salida de cualquier comando occ.
- `OCP\Security\IHasher::validate()` debe devolver true si la cadena pasada es un hash válido generado por `OCP\Security\IHasher::hash()`
- El constructor `OCP\AppFramework\Http\JSONResponse()` ahora admite pasar flags adicionales de `json_encode`; ver <https://www.php.net/manual/en/function.json-encode.php> para más detalles
- `OCP\EventDispatcher\IWebhookCompatibleEvent` es una nueva interfaz para los eventos compatibles con webhooks ([ver la documentación de webhook_listeners](https://docs.nextcloud.com/server/latest/admin_manual/webhook_listeners/index.html)).
- `OCP\EventDispatcher\JsonSerializer` es un nuevo ayudante público para serializar usuarios y fileinfos a json (es decir, para los eventos de webhooks)

#### API modificadas

- `OCP\Activity\IEvent::set*()` (todos los setters) lanzan `OCP\Activity\Exceptions\InvalidValueException` en lugar de `\InvalidArgumentException` cuando el valor no cumple los criterios requeridos.
- Llamar a `OCP\Activity\IEvent::setIcon()` con una URL relativa está obsoleto y lanzará `OCP\Activity\Exceptions\InvalidValueException` en una versión futura.
- Llamar a `OCP\Activity\IEvent::setLink()` con una URL relativa está obsoleto y lanzará `OCP\Activity\Exceptions\InvalidValueException` en una versión futura.
- `OCP\Activity\IManager::publish()` lanza `OCP\Activity\Exceptions\IncompleteActivityException` en lugar de `\InvalidArgumentException` cuando no se establece un campo obligatorio antes de publicar.
- `OCP\Activity\IProvider::parse()` ya no debe lanzar `\InvalidArgumentException`. Debe lanzarse `OCP\Activity\Exceptions\UnknownActivityException` cuando el proveedor no quiera gestionar el evento. Las `\InvalidArgumentException` se registran por ahora como depuración y en el futuro se registrarán como error, para ayudar a quienes desarrollan a encontrar problemas en código que lanzó `\InvalidArgumentException` sin querer
- Aclaración sobre `OCP\Dashboard\IIconWidget::getIconUrl()`: la URL debe ser absoluta. El icono servido debe ser oscuro. El icono se invertirá automáticamente en los clientes móviles y al usar el modo oscuro.
- Aclaración sobre `OCP\Dashboard\IWidget::getId()`: las implementaciones solo deben devolver cadenas basadas en `a-z`, `0-9`, `-` y `_` que empiecen por una letra, ya que el identificador se usa en clases CSS y, de lo contrario, no sería válido
- Aclaración sobre `OCP\Dashboard\IWidget::getIconClass()`: la clase CSS devuelta debe mostrar un icono oscuro. El icono se invertirá automáticamente en los clientes móviles y al usar el modo oscuro. Por lo tanto, NO se recomienda usar una clase css que establezca el fondo con `` var(--icon-…)` ``, ya que esas variables se adaptan al modo oscuro o claro en la web y aun así se invertirían, lo que daría como resultado un icono oscuro sobre fondo oscuro.
- Se añadió `OCP\Files\Lock\ILockManager::registerLazyLockProvider()` para reemplazar `registerLockProvider`; permite registrar un proveedor de bloqueos que solo se carga cuando se necesita.
- `OCP\Notification\IAction::set*()` (todos los setters) lanzan `OCP\Notification\InvalidValueException` en lugar de `\InvalidArgumentException` cuando el valor no cumple los criterios requeridos.
- Llamar a `OCP\Notification\IAction::setLink()` con una URL relativa está obsoleto y lanzará `OCP\Notification\InvalidValueException` en una versión futura.
- `OCP\Notification\IApp::notify()` lanza `OCP\Notification\IncompleteNotificationException` en lugar de `\InvalidArgumentException` cuando no se establece un campo obligatorio antes de notificar.
- `OCP\Notification\IManager::prepare()` lanza `OCP\Notification\IncompleteParsedNotificationException` en lugar de `\InvalidArgumentException` cuando un campo obligatorio no está establecido después de preparar una notificación.
- `OCP\Notification\INotification::set*()` (todos los setters) lanzan `OCP\Notification\InvalidValueException` en lugar de `\InvalidArgumentException` cuando el valor no cumple los criterios requeridos.
- Llamar a `OCP\Notification\INotification::setLink()` con una URL relativa está obsoleto y lanzará `OCP\Notification\InvalidValueException` en una versión futura.
- Llamar a `OCP\Notification\INotification::setIcon()` con una URL relativa está obsoleto y lanzará `OCP\Notification\InvalidValueException` en una versión futura.
- `OCP\Notification\INotifier::prepare()` ya no debe lanzar `\InvalidArgumentException`. Debe lanzarse `OCP\Notification\UnknownNotificationException` cuando el notificador no quiera gestionar la notificación. Las `\InvalidArgumentException` se registran por ahora como depuración y en el futuro se registrarán como error, para ayudar a quienes desarrollan a encontrar problemas en código que lanzó `\InvalidArgumentException` sin querer
- Debe usarse `OCP\IGroupManager::isAdmin()` en lugar de comprobar manualmente si el usuario actual forma parte del grupo admin.
- La clave `enabled` de `IAttributes` se renombró a `value` y admite más que valores booleanos.
- `OCP\DB\Exception` usa ahora el código de motivo `REASON_LOCK_WAIT_TIMEOUT`, en lugar de `REASON_SERVER`, para una LockWaitTimeoutException.
- `OCP\Share\IShare::setNoExpirationDate()` establece ahora un indicador de sobrescritura para los valores falsy de la fecha de caducidad; este indicador se usa para determinar si el sistema debe sobrescribir los valores falsy de la fecha de caducidad antes de crear una compartición.
- `OCP\Share\IShare::getNoExpirationDate()` recupera el valor del indicador `noExpirationDate`.
- `OCP\IUserManager::getDisabledUsers` tiene ahora un tercer parámetro para una cadena de búsqueda.
- `OCP\User\Backend\IProvideEnabledStateBackend::getDisabledUserList` tiene ahora un tercer parámetro para una cadena de búsqueda.
- La clase heredada `OC_EventSource` se trasladó al espacio de nombres `OC` con el prefijo `OC_`. No debería cambiar nada si ya se usa correctamente `OCP\IEventSourceFactory` para crear estos objetos.
- `OCP\Files\Events\Node\AbstractNodeEvent` y `OCP\Files\Events\Node\AbstractNodesEvent` implementan ahora `OCP\EventDispatcher\IWebhookCompatibleEvent`, de modo que todos los eventos relacionados con archivos o carpetas están disponibles para los webhooks ([ver la documentación de webhook_listeners](https://docs.nextcloud.com/server/latest/admin_manual/webhook_listeners/index.html)).

#### API obsoletas

- Usar la anotación `@PasswordConfirmationRequired` está obsoleto; en su lugar debe usarse el atributo `#[OCP\AppFramework\Http\Attribute\PasswordConfirmationRequired]`.
- Usar la anotación `@CORS` está obsoleto; en su lugar debe usarse el atributo `#[OCP\AppFramework\Http\Attribute\CORS]`.
- Usar la anotación `@PublicPage` está obsoleto; en su lugar debe usarse el atributo `#[OCP\AppFramework\Http\Attribute\PublicPage]`.
- Usar la anotación `@ExAppRequired` está obsoleto; en su lugar debe usarse el atributo `#[OCP\AppFramework\Http\Attribute\ExAppRequired]`.
- Usar la anotación `@AuthorizedAdminSetting` está obsoleto; en su lugar debe usarse el atributo `#[OCP\AppFramework\Http\Attribute\AuthorizedAdminSetting]`.
- Usar la anotación `@SubAdminRequired` está obsoleto; en su lugar debe usarse el atributo `#[OCP\AppFramework\Http\Attribute\SubAdminRequired]`.
- Usar la anotación `@NoAdminRequired` está obsoleto; en su lugar debe usarse el atributo `#[OCP\AppFramework\Http\Attribute\NoAdminRequired]`.
- Usar la anotación `@StrictCookieRequired` está obsoleto; en su lugar debe usarse el atributo `#[OCP\AppFramework\Http\Attribute\StrictCookiesRequired]`.
- Usar la anotación `@NoCSRFRequired` está obsoleto; en su lugar debe usarse el atributo `#[OCP\AppFramework\Http\Attribute\NoCSRFRequired]`.
- Usar la interfaz `OCP\Group\Backend\ICreateGroupBackend` está ahora obsoleto; en su lugar debe usarse la interfaz `OCP\Group\Backend\ICreateNamedGroupBackend`.
- Llamar a `OCP\DB\QueryBuilder\IExpressionBuilder::andX()` sin argumentos está obsoleto y lanzará una excepción en una versión futura, ya que la biblioteca subyacente está eliminando esa funcionalidad.
- Llamar a `OCP\DB\QueryBuilder\IExpressionBuilder::orX()` sin argumentos está obsoleto y lanzará una excepción en una versión futura, ya que la biblioteca subyacente está eliminando esa funcionalidad.
- Llamar a `OCP\DB\QueryBuilder\IQueryBuilder::delete()` con `$alias` está obsoleto y lanzará una excepción en una versión futura, ya que la biblioteca subyacente está eliminando esa funcionalidad.
- Llamar a `OCP\DB\QueryBuilder\IQueryBuilder::getQueryPart()` está obsoleto y lanzará una excepción en una versión futura, ya que la biblioteca subyacente está eliminando esa funcionalidad.
- Llamar a `OCP\DB\QueryBuilder\IQueryBuilder::getQueryParts()` está obsoleto y lanzará una excepción en una versión futura, ya que la biblioteca subyacente está eliminando esa funcionalidad.
- Llamar a `OCP\DB\QueryBuilder\IQueryBuilder::getState()` está obsoleto y lanzará una excepción en una versión futura, ya que la biblioteca subyacente está eliminando esa funcionalidad.
- Llamar a `OCP\DB\QueryBuilder\IQueryBuilder::resetQueryPart()` está obsoleto y lanzará una excepción en una versión futura, ya que la biblioteca subyacente está eliminando esa funcionalidad. En su lugar, crear un nuevo objeto de constructor de consultas.
- Llamar a `OCP\DB\QueryBuilder\IQueryBuilder::resetQueryParts()` está obsoleto y lanzará una excepción en una versión futura, ya que la biblioteca subyacente está eliminando esa funcionalidad. En su lugar, crear un nuevo objeto de constructor de consultas.
- Llamar a `OCP\DB\QueryBuilder\IQueryBuilder::update()` con `$alias` está obsoleto y lanzará una excepción en una versión futura, ya que la biblioteca subyacente está eliminando esa funcionalidad.
- Llamar a `OCP\IDBConnection::getDatabasePlatform()` está obsoleto y lanzará una excepción en una versión futura, ya que la biblioteca subyacente está renombrando y eliminando plataformas, lo que rompe la compatibilidad con versiones anteriores. Usar `getDatabaseProvider()` en su lugar.
- Llamar a `OCP\Files\Lock\ILockManager::registerLockProvider()` está obsoleto y se eliminará en el futuro. Usar `registerLazyLockProvider()` en su lugar.
- Usar `OCP\Translation` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`).
- Usar `OCP\Translation\CouldNotTranslateException` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`).
- Usar `OCP\Translation\IDetectLanguageProvider` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`).
- Usar `OCP\Translation\ITranslationManager` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`).
- Usar `OCP\Translation\ITranslationProvider` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`).
- Usar `OCP\Translation\ITranslationProviderWithId` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`).
- Usar `OCP\Translation\ITranslationProviderWithUserId` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`).
- Usar `OCP\Translation\LanguageTuple` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`).
- Usar `OCP\SpeechToText` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `SpeechToText` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\SpeechToText\Events\AbstractTranscriptionEvent` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `SpeechToText` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\SpeechToText\Events\TranscriptionFailedEvent` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `SpeechToText` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\SpeechToText\Events\TranscriptionSuccessfulEvent` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `SpeechToText` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\SpeechToText\ISpeechToTextManager` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `SpeechToText` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\SpeechToText\ISpeechToTextProvider` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `SpeechToText` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\SpeechToText\ISpeechToTextProviderWithId` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `SpeechToText` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\SpeechToText\ISpeechToTextProviderWithUserId` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `SpeechToText` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextToImage` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextToImage` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextToImage\Task` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextToImage` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextToImage\IProviderWithUserId` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextToImage` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextToImage\IProvider` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextToImage` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextToImage\IManager` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextToImage` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextToImage\Exception\TextToImageException` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextToImage` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextToImage\Exception\TaskNotFoundException` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextToImage` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextToImage\Exception\TaskFailureException` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextToImage` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextToImage\Events\TaskSuccessfulEvent` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextToImage` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextToImage\Events\TaskFailedEvent` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextToImage` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextToImage\Events\AbstractTextToImageEvent` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextToImage` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\Events\AbstractTextProcessingEvent` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\Events\TaskFailedEvent` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\Events\TaskSuccessfulEvent` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\Exception\TaskFailureException` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\FreePromptTaskType` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\HeadlineTaskType` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\IManager` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\IProvider` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\IProviderWithExpectedRuntime` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\IProviderWithId` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\IProviderWithUserId` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\ITaskType` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\SummaryTaskType` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\Task` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar `OCP\TextProcessing\TopicsTaskType` está obsoleto y se eliminará en el futuro. Usar en su lugar `OCP\TaskProcessing` (ver {nc-ref}`Procesamiento de tareas <task_processing>`). Los proveedores de `TextProcessing` existentes seguirán funcionando con la API TaskProcessing hasta entonces.
- Usar la interfaz `OCP\Group\Backend\ICreateGroupBackend` está obsoleto y se eliminará en el futuro. Usar `OCP\Group\Backend\ICreateNamedGroupBackend` en su lugar.

#### API eliminadas

- `OCP\Util::isValidFileName` estaba obsoleto desde la 8.1.0 y ahora se ha eliminado; usar `OCP\Files\Storage\IStorage::verifyPath` o el nuevo `OCP\Files\IFilenameValidator`.
- Se eliminó `OCP\Util::getForbiddenFileNameChars`; para validar nombres de archivo, usar `OCP\Files\Storage\IStorage::verifyPath` o el nuevo `OCP\Files\IFilenameValidator`.
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
