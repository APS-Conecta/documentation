---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 32 para las apps: tests/autoload.php, colores de estado, iconos con contorno, OCP consumible e implementable y cambios de API."
---
# Actualización a Nextcloud 32

## Resumen

Esta página enumera los cambios de la versión 32 que afectan a las apps: el nuevo `tests/autoload.php`, los colores de estado basados en el estilo secundario, los iconos con contorno, la división de OCP en API consumibles e implementables y los eventos y API añadidos, modificados, obsoletos o eliminados. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_32.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### General

- Se añadió al repositorio del servidor un nuevo archivo `tests/autoload.php`, que se puede incluir en el archivo `bootstrap.php` de la app para las pruebas, a fin de poder cargar la clase `\Test\TestCase` del núcleo.
  Se debe eliminar cualquier llamada a `\OC::$loader` en el código, ya que este cargador heredado se está eliminando.
  Este nuevo archivo se ha incorporado a las ramas stable31, stable30 y stable29, por lo que, si la aplicación admite varias versiones mayores de Nextcloud, debería seguir funcionando.

### Cambios de frontend

#### Los colores de estado se basan ahora en el estilo secundario

Los colores de estado como `error`, `success` o `warning` se basan ahora en el estilo secundario en lugar del primario.
Esto significa que ahora son mucho más claros y, por lo tanto, no pueden usarse para usos como los colores de texto o de borde.
Para mitigarlo, se introducen las siguientes variables CSS nuevas:

- `--color-text-error` para el texto que necesita un resaltado de error sobre colores de fondo **normales**.
- `--color-text-success` para el texto que necesita un resaltado de éxito sobre colores de fondo **normales**.
- `--color-border-error` para usarse como color de borde de los elementos con un estado de error, como los elementos de entrada cuya validación falla.
- `--color-border-success` para usarse como color de borde de los elementos con un estado de éxito, como una entrada que se guardó o similar.

Tener en cuenta que no hay variantes de texto ni de borde para `warning` e `info`, ya que, desde el punto de vista del diseño, se desaconseja usarlas en textos y bordes.

Además, como a veces los elementos necesitan un color de estado con el contraste adecuado, ahora se ofrecen las siguientes variables para elementos de estado como los iconos:

- `--color-element-error`
- `--color-element-info`
- `--color-element-success`
- `--color-element-warning`

Estas variables existentes cambiaron a un estilo secundario:

- `--color-error` para usarse como color de fondo de los elementos con estilo de error (como un botón en estado de error o una note-card).
- `--color-error-hover` para usarse como color de fondo de dichos elementos al pasar el cursor.
- `--color-error-text` para usarse como color de primer plano de dichos elementos.
- Lo mismo se aplica a `--color-info`, `--color-success`, `--color-warning` y sus variantes.

#### Los iconos deben ser con contorno

Al usar Material Icons, usar la variante con contorno (outlined) siempre que sea posible. Las excepciones son los propios iconos de las apps, los iconos de tipos de archivo y los iconos que ya eran de una sola línea, como los de más o de marca de verificación. El razonamiento y más detalles están en [la issue](https://github.com/nextcloud/server/issues/53701).

#### API obsoletas

- `--color-error-rgb`, `--color-info-rgb`, `--color-success-rgb`, `--color-warning-rgb` están obsoletas.
  En su lugar, usar las utilidades de color nativas de CSS con las variables existentes, como `--color-error` y similares.
- La api `OC.SystemTags` está obsoleta. Si se necesita obtener la lista de etiquetas del sistema, consultar [esta merge request](https://github.com/nextcloud/files_retention/pull/855) para ver cómo obtener las etiquetas directamente.

### Cambios de backend

- División de la API OCP en consumible e implementable:
  Para conocer mejor el contexto, ver [RFC: dividir OCP en Consumable e Implementable](https://github.com/nextcloud/standards/issues/15) para más información.
  Resumen breve:

  - **Consumable:** las interfaces, enums y clases que tienen el atributo `OCP\AppFramework\Attribute\Consumable` solo deben ser consumidas por las apps y no pueden ser implementadas por las propias apps.
    Esto significa que el lado del servidor puede ampliar la interfaz con nuevos métodos o reducir los tipos devueltos por los métodos existentes sin que se considere una ruptura de la API.
    Sin embargo, los tipos de los argumentos de los métodos existentes **no** pueden reducirse.
    Las mismas reglas se aplican a los `OCP\EventsDispatcher\Event` que tienen el atributo `OCP\AppFramework\Attribute\Listenable` y a las `Exception` con el atributo `OCP\AppFramework\Attribute\Catchable`.
  - **Implementable:** las interfaces, enums y clases que tienen el atributo `OCP\AppFramework\Attribute\Implementable` pueden ser implementadas por las apps.
    Esto significa que el lado del servidor **no** puede ampliar la interfaz con nuevos métodos ni reducir los tipos devueltos por los métodos existentes sin que se considere una ruptura de la API.
    Sin embargo, los tipos de los argumentos de los métodos existentes sí pueden reducirse.
    Las mismas reglas se aplican a los `OCP\EventsDispatcher\Event` que tienen el atributo `OCP\AppFramework\Attribute\Dispatchable` y a las `Exception` con el atributo `OCP\AppFramework\Attribute\Throwable`.
  - **ExceptionalImplementable:** aunque no sean implementables por todas las apps, algunas interfaces pueden tener el atributo `OCP\AppFramework\Attribute\ExceptionalImplementable`, que indica que una sola app (o varias) puede implementarlas.
    En esos casos se aplican las reglas generales de `OCP\AppFramework\Attribute\Consumable`, pero hay que informar a quienes mantienen las apps o al repositorio de las excepciones nombradas durante el proceso de una pull request, dejándoles tiempo suficiente para adaptarse al cambio que se avecina.

- Estos nuevos atributos se aplicarán según un criterio de «estándar de facto», según nuestro leal saber y entender.
  Si una API se marcó de forma inesperada, dejar un comentario en la pull request correspondiente del repositorio del servidor pidiendo una aclaración.

#### Eventos añadidos

- Nuevo evento `preloadCollection`, emitido por el servidor DAV durante las solicitudes PROPFIND. Ver {nc-ref}`collection_preload` para más detalles.
- Nuevo `OCP\SystemTag\TagAssignedEvent`, emitido por el mapeador de objetos de etiquetas del sistema
- Nuevo `OCP\SystemTag\TagUnassignedEvent`, emitido por el mapeador de objetos de etiquetas del sistema

#### API añadidas

- Nueva API `OCP\ContextChat`. Ver {nc-ref}`context_chat` para más detalles.
- Nueva interfaz `\OCP\OCM\ICapabilityAwareOCMProvider` para ampliar el proveedor OCM con las extensiones 1.1 y 1.2 de la API de descubrimiento de Open Cloud Mesh
- Nueva interfaz `\OCP\Search\IExternalProvider`, que permite ampliar el proveedor de búsqueda con un indicador explícito
  para señalar que la búsqueda se realiza sobre recursos externos (de terceros).
  Se usa en la búsqueda unificada para desactivar por defecto las búsquedas en ellos (mediante un interruptor).
- Nueva interfaz `\OCP\Share\IShareProviderSupportsAllSharesInFolder`, que extiende `\OCP\Share\IShareProvider`
  para añadir el método `\OCP\Share\IShareProviderSupportsAllSharesInFolder::getAllSharesInFolder`, usado para consultar todas las comparticiones de una carpeta sin filtrar por usuario.
- Nueva interfaz `\OCP\Notification\IPreloadableNotifier` para permitir que las implementaciones de notificadores precarguen
  y almacenen en caché los datos de muchas notificaciones a la vez para mejorar el rendimiento, por ejemplo agrupando consultas SQL.
- Nueva interfaz `\OCP\Template\ITemplateManager` para acceder a las funciones relacionadas con las plantillas
  y obtener instancias de la nueva interfaz `\OCP\Template\ITemplate` en lugar de construir manualmente `\OCP\Template`.
- Nuevo atributo `\OCP\AppFramework\Http\Attribute\RequestHeader`, usado para documentar las cabeceras de solicitud en las especificaciones OpenAPI generadas con openapi-extractor.
- Nuevo evento `\OCP\Files\Config\Event\UserMountAddedEvent`, que se emite cuando se añade un nuevo montaje a la tabla `oc_mounts`.
- Nuevo evento `\OCP\Files\Config\Event\UserMountRemovedEvent`, que se emite cuando se elimina un montaje existente de la tabla `oc_mounts`.
- Nuevo evento `\OCP\Files\Config\Event\UserMountUpdatedEvent`, que se emite cuando se actualiza un montaje existente en la tabla `oc_mounts`.
- Nuevo método `\OCA\Files\Controller\TemplateController::listTemplateFields` para listar los campos de una plantilla,
  accesible en `/ocs/v2.php/apps/files/api/v1/templates/fields/{fileId}`.
- Nuevo método `\OCP\Files\IFilenameValidator::sanitizeFilename`, que permite sanear un nombre de archivo dado para que cumpla las restricciones configuradas.
- Nuevo método `\OCP\Files\Template\ITemplateManager::listTemplateFields` para permitir listar los campos de una plantilla.
- Nuevo método `\OCP\Files\Template\BeforeGetTemplatesEvent::shouldGetFields` para obtener la propiedad `withFields` del evento, que debe determinar si se extraen o no los campos de plantilla de las plantillas devueltas.
- Nuevo método `\OCP\IUser::canChangeEmail`, que permite comprobar si el backend de usuarios permite al usuario cambiar su dirección de correo electrónico.
- Nuevo método `\OCP\IDateTimeZone::getDefaultTimezone`, que permite obtener la zona horaria predeterminada configurada para Nextcloud.
- Nuevo método `\OCA\Files_Versions\Versions\IVersionBackend::getRevision` para obtener la revisión de la versión a partir de un nodo.
- Nuevo `OCP\SystemTag\TagAssignedEvent`, emitido por el mapeador de objetos de etiquetas del sistema
- Nuevo `OCP\SystemTag\TagUnassignedEvent`, emitido por el mapeador de objetos de etiquetas del sistema
- API de procesamiento de tareas:

  - Nuevo tipo de tarea de procesamiento de tareas `OCP\TaskProcessing\TextToSpeech` para convertir texto en voz.
  - Nuevo tipo de tarea de procesamiento de tareas `OCP\TaskProcessing\AnalyzeImages` para hacer preguntas sobre imágenes.
  - Nuevo método `OCP\TaskProcessing\Manager::getAvailableTaskTypeIds` para listar solo los ID de los tipos de tarea, sin metadatos (más rápido que `OCP\TaskProcessing\Manager::getAvailableTaskTypes`)

- Nuevo `OCP\Mail\IEmailValidator` para validar una dirección de correo electrónico.
- Nuevo método `OCP\App\IAppManager::getAppInstalledVersions` para obtener las versiones instaladas de todas las aplicaciones
- Nuevo método `OCP\IAppConfig::getAppInstalledVersions` para hacer lo mismo

#### API modificadas

- El tipo de retorno de `\OCP\Authentication\TwoFactorAuth\ILoginSetupProvider::getBody`, `\OCP\Authentication\TwoFactorAuth\IPersonalProviderSettings::getBody` y `\OCP\Authentication\TwoFactorAuth\IProvider::getBody` se amplió de la clase `\OCP\Template` a la interfaz `\OCP\Template\ITemplate`. No debería cambiar nada para las aplicaciones.
- `\OCP\Files\Template\BeforeGetTemplatesEvent` acepta ahora un valor booleano opcional en el constructor, `withFields`, que permite controlar explícitamente si deben extraerse los campos de plantilla. El valor predeterminado es `false`.
- `\OCP\IDateTimeZone::getTimezone` tiene ahora un nuevo parámetro opcional de tipo cadena, `userId`, que permite solicitar la zona horaria de un usuario distinto del actual.
- `\OCP\IDBConnection::getDatabaseProvider` tiene ahora un nuevo parámetro booleano opcional, `strict`. Cuando se indica, la salida diferenciará entre MySQL y MariaDB. De lo contrario, MariaDB se devolverá como MySQL
- `\OCP\Notification\INotification::setIcon`, `\OCP\Notification\INotification::setLink` y `\OCP\Notification\IAction::setLink` lanzan ahora `\OCP\Notification\InvalidValueException` cuando el enlace proporcionado no es absoluto, como se anunció previamente en {nc-doc}`developer_manual/release_notes/previous/upgrade_to_30`

#### API obsoletas

- El endpoint de la API de archivos `/apps/files/api/v1/thumbnail/` para generar vistas previas está obsoleto.
  En su lugar, usar el endpoint de vistas previas que proporciona el núcleo de Nextcloud (`/core/preview`).
- El método heredado `\OC_Helper::canExecute` está obsoleto; usar en su lugar `OCP\IBinaryFinder`.
- Las clases `\OC_Template` y `\OCP\Template` están obsoletas; usar en su lugar el nuevo `\OCP\Template\ITemplateManager`.
- `\OC_User::useBackend` está obsoleto; usar `\OCP\IUserManager::registerBackend`, disponible desde la 8.0.0
- `\OC_User::clearBackends` está obsoleto; usar `\OCP\IUserManager::clearBackends`, disponible desde la 8.0.0
- `\OC_Helper::isReadOnlyConfigEnabled` está obsoleto; usar directamente la configuración del sistema `config_is_read_only`.
- `\OCP\OCM\IOCMProvider` está obsoleto; usar `\OCP\OCM\ICapabilityAwareOCMProvider`, disponible desde la 32.0.0
- `\OCP\Mail\IMailer::validateMailAddress` está obsoleto; usar `\OCP\Mail\IEmailValidator`, disponible desde la 32.0.0
- `\OC_App::getSupportedApps` está obsoleto; usar en su lugar `\OCP\Support\Subscription\IRegistry::delegateGetSupportedApps`
- `\OC_App::getAppVersions` está obsoleto; usar en su lugar `OCP\App\IAppManager::getAppInstalledVersions`
- `\OCP\Route\IRoute::actionInclude` y `\OCP\Route\IRoute::action` están obsoletos; usar en su lugar un controlador adecuado.

#### API eliminadas

- El paquete `scssphp` ya no se incluye con Nextcloud. Este paquete no se usaba y estaba obsoleto desde Nextcloud 22.
  Si la app necesita el paquete, hay que incluirlo en ella.
- Los métodos `\OCP\Files::getStorage` y el heredado `OC_App_::getStorage` estaban obsoletos desde Nextcloud 14 y Nextcloud 5, respectivamente, y ahora se eliminaron.
  En su lugar, usar `\OCP\Files\IAppData`.
- Se eliminó `\OCP\AppFramework\App::registerRoutes` (obsoleto en Nextcloud 20). En su lugar, devolver las rutas como un array desde routes.php o usar atributos de ruta.
- Las constantes de visibilidad heredadas de `OCP\Accounts\IAccountManager`,
  `VISIBILITY_PRIVATE`, `VISIBILITY_CONTACTS_ONLY`, `VISIBILITY_PUBLIC`, estaban obsoletas desde Nextcloud 21 y ahora se eliminaron.
  En su lugar, solo pueden usarse las constantes de visibilidad v2.
- Se eliminaron métodos obsoletos de la clase heredada `\OC_Helper`:

  - `humanFileSize` estaba obsoleto desde la versión 4.0.0 y se reemplazó por `\OCP\Util::humanFileSize`
  - `computerFileSize` estaba obsoleto desde la versión 4.0.0 y se reemplazó por `\OCP\Util::computerFileSize`
  - `mb_array_change_key_case` estaba obsoleto desde la versión 4.5.0 y se reemplazó por `\OCP\Util::mb_array_change_key_case`
  - `recursiveArraySearch` estaba obsoleto desde la versión 4.5.0 y se reemplazó por `\OCP\Util::recursiveArraySearch`
  - `rmdirr` estaba obsoleto desde la versión 5.0.0 y se reemplazó por `\OCP\Files::rmdirr`
  - `maxUploadFilesize` estaba obsoleto desde la versión 5.0.0 y se reemplazó por `\OCP\Util::maxUploadFilesize`
  - `freeSpace` estaba obsoleto desde la versión 7.0.0 y se reemplazó por `\OCP\Util::freeSpace`
  - `uploadLimit` estaba obsoleto desde la versión 7.0.0 y se reemplazó por `\OCP\Util::uploadLimit`

- Se eliminaron métodos obsoletos de la clase heredada `\OC_Util`:

  - `addScript` se reemplazó por `\OCP\Util::addScript` en la 24
  - `addVendorScript` no se usaba y se eliminó
  - `addTranslations` se reemplazó por `\OCP\Util::addTranslations` en la 24

- La función de plantilla `vendor_script` no se usaba y se eliminó
- Se eliminó la compatibilidad con los archivos `app.php`, obsoletos desde Nextcloud 19. Todavía se comprueba si el archivo existe para mostrar un error si está presente, pero eso se eliminará en una versión posterior. Pasar en su lugar a `OCP\AppFramework\Bootstrap\IBoostrap`.
- Se eliminaron los siguientes getters, obsoletos desde la 20. Usar en su lugar la inyección de dependencias o `\OCP\Server::get`:

  - `IServerContainer::getAppConfig()`
  - `IServerContainer::getAvatarManager()`
  - `IServerContainer::getCalendarManager()`
  - `IServerContainer::getCalendarResourceBackendManager()`
  - `IServerContainer::getCalendarRoomBackendManager()`
  - `IServerContainer::getCloudFederationFactory()`
  - `IServerContainer::getCloudFederationProviderManager()`
  - `IServerContainer::getCommandBus()`
  - `IServerContainer::getCommentsManager()`
  - `IServerContainer::getContentSecurityPolicyManager()`
  - `IServerContainer::getCredentialsManager()`
  - `IServerContainer::getDateTimeFormatter()`
  - `IServerContainer::getDateTimeZone()`
  - `IServerContainer::getEncryptionKeyStorage()`
  - `IServerContainer::getEventLogger()`
  - `IServerContainer::getGlobalScaleConfig()`
  - `IServerContainer::getHTTPClientService()`
  - `IServerContainer::getIniWrapper()`
  - `IServerContainer::getLogFactory()`
  - `IServerContainer::getMountManager()`
  - `IServerContainer::getMountProviderCollection()`
  - `IServerContainer::getNavigationManager()`
  - `IServerContainer::getPreviewManager()`
  - `IServerContainer::getQueryLogger()`
  - `IServerContainer::getRemoteApiFactory()`
  - `IServerContainer::getRemoteInstanceFactory()`
  - `IServerContainer::getRouter()`
  - `IServerContainer::getShareManager()`
  - `IServerContainer::getStorageFactory()`
  - `IServerContainer::getSystemTagManager()`
  - `IServerContainer::getSystemTagObjectMapper()`
  - `IServerContainer::getTagManager()`

- Se eliminó el autocargador heredado `\OC::$loader`. No debería afectar a la aplicación. Puede afectar a las pruebas si lo usaban. Considerar incluir en su lugar `tests/autoload.php` del servidor.
````
