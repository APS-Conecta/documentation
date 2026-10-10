---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 20 para las apps: temas, jQuery 2.2, búsqueda unificada, nueva API de arranque, PSR-3 y PSR-11 y la lista de API y eventos obsoletos."
---
# Actualización a Nextcloud 20

## Resumen

Esta página enumera los cambios de la versión 20 que afectan a las apps: las clases de tema, la actualización de jQuery, la búsqueda unificada, las variables globales eliminadas u obsoletas, la nueva API de arranque, la integración de PSR-3 y PSR-11, las API y eventos obsoletos y lo retirado del espacio de nombres público. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_20.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Los cambios críticos se recopilaron [en GitHub](https://github.com/nextcloud/server/issues/20953). Consultar el ticket original para ver los enlaces a las pull requests y a los tickets.
:::

### Cambios de frontend

#### Tema del elemento body

Las clases de tema del elemento body ahora son `theme--highcontrast`, `theme--dark` y/o `theme--light`.

#### Actualización de jQuery

jQuery se actualizó a la v2.2. El cambio más notable es que `$(document).ready(...)`, o `$(...)` en su forma abreviada, se dispara antes que hasta ahora. Usar en su lugar el [evento DOMContentLoaded](https://developer.mozilla.org/fr/docs/Web/Events/DOMContentLoaded).

#### Búsqueda

La {nc-ref}`búsqueda unificada <unified-search>` reemplaza el campo de búsqueda tradicional, por lo que `OCA.Search` pasó a no hacer nada (noop). Por compatibilidad con versiones anteriores, el código no generará errores por ahora, pero no tiene ninguna funcionalidad.

#### Variables globales eliminadas

- `escape-html`: usar [el paquete escape-html](https://www.npmjs.com/package/escape-html) o similar

#### Variables globales obsoletas

- `humanFileSize`: usar `formatfilesize` de <https://www.npmjs.com/package/@nextcloud/files>
- `OC.getCanonicalLocale`: usar `getCanonicalLocale` de <https://www.npmjs.com/package/@nextcloud/l10n>

#### Plugins de jQuery eliminados

- `$.tipsy`

### Cambios de backend

#### Lógica de arranque de la app

El código que inicializa una app, o cualquier cosa que deba ejecutarse en cada solicitud y en cada comando, se trasladó ahora a una API dedicada y tipada. Por lo tanto, `appinfo/app.php` queda en desuso y obsoleto. Ver {nc-ref}`arranque <bootstrapping>` para los detalles.

(nc-dev-upgrade-psr3)=
#### Integración de PSR-3

Nextcloud 20 es la primera versión mayor de Nextcloud que ofrece compatibilidad total con {nc-ref}`psr3`. A partir de ahora se recomienda encarecidamente usar esta interfaz, principalmente porque la antigua `\OCP\ILogger` quedó obsoleta con los últimos cambios que faltaban. La mayoría de los métodos son idénticos entre la interfaz específica de Nextcloud y la de PSR. Prestar atención a los usos de `\OCP\ILogger::logException`, ya que ese método no existe en el logger de PSR. Sin embargo, se puede indicar una clave `exception` en el argumento `$context` de cualquier método de `\Psr\Log\LoggerInterface` y Nextcloud la formateará como lo hacía con el antiguo `logException`.

(nc-dev-upgrade-psr11)=
#### Integración de PSR-11

Nextcloud 20 es la primera versión mayor de Nextcloud que ofrece compatibilidad total con {nc-ref}`psr11`. A partir de ahora se recomienda encarecidamente usar esta interfaz, principalmente porque la antigua `\OCP\IContainer` quedó obsoleta con este cambio.

Las interfaces `\OCP\AppFramework\IAppContainer` y `\OCP\IServerContainer` se mantendrán, pero dejarán de extender `IContainer` una vez que esa interfaz se elimine. Como resultado, `IAppContainer` e `IServerContainer` acabarán siendo interfaces de marcado cuyo único propósito es permitir que se inyecte explícitamente el contenedor de la app o el del servidor.

Si la app requiere Nextcloud 20 o posterior, se puede reemplazar cualquiera de las antiguas declaraciones de tipo por una de `\Psr\Container\ContainerInterface` y reemplazar las llamadas a `query` por `get`, por ejemplo en los closures que se usan al registrar servicios:

```php
// old
$container->registerService('DecryptAll', function (IAppContainer $c) {
  return new DecryptAll(
    $c->query('Util'),
    $c->query(KeyManager::class),
    $c->query('Crypt'),
    $c->query(ISession::class)
  )
})
```

se convierte en

```php
// new
$container->registerService('DecryptAll', function (ContainerInterface $c) {
  return new DecryptAll(
    $c->get('Util'),
    $c->get(KeyManager::class),
    $c->get('Crypt'),
    $c->get(ISession::class)
  )
})
```

:::{note}
Para una transición más suave, las interfaces antiguas se modificaron para que se basen en `ContainerInterface`, de modo que se pueden usar `has` y `get` en `IContainer` y sus subtipos.
:::

##### API obsoletas

- `\OCP\IContainer`: ver {nc-ref}`upgrade-psr11`
- `\OCP\ILogger`: ver {nc-ref}`upgrade-psr3`
- `\OCP\IServerContainer::getEventDispatcher`
- `\OCP\IServerContainer::getCalendarManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getCalendarResourceBackendManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getCalendarRoomBackendManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getContactsManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getEncryptionManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getEncryptionFilesHelper`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getEncryptionKeyStorage`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getRequest`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getPreviewManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getTagManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getSystemTagManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getSystemTagObjectMapper`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getAvatarManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getRootFolder`
- `\OCP\IServerContainer::getUserManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getGroupManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getUserSession`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getSession`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getTwoFactorAuthManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getNavigationManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getConfig`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getSystemConfig`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getAppConfig`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getL10NFactory`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getL10N`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getURLGenerator`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getAppFetcher`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getMemCacheFactory`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getGetRedisFactory`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getDatabaseConnection`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getActivityManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getJobList`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getLogger`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getLogFactory`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getRouter`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getSearch`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getSecureRandom`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getCrypto`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getHasher`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getCredentialsManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getCertificateManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getHTTPClientService`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::createEventSource`
- `\OCP\IServerContainer::getEventLogger`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getQueryLogger`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getTempManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getAppManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getMailer`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getWebRoot`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getOcsClient`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getDateTimeZone`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getDateTimeFormatter`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getMountProviderCollection`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getIniWrapper`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getCommandBus`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getTrustedDomainHelper`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getLockingProvider`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getMountManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getUserMountCache`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getMimeTypeDetector`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getMimeTypeLoader`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getCapabilitiesManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getNotificationManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getCommentsManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getThemingDefaults`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getIntegrityCodeChecker`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getSessionCryptoWrapper`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getCsrfTokenManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getBruteForceThrottler`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getContentSecurityPolicyManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getContentSecurityPolicyNonceManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getStoragesBackendService`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getGlobalStoragesService`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getUserGlobalStoragesService`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getUserStoragesService`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getShareManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getCollaboratorSearch`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getAutoCompleteManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getLDAPProvider`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getSettingsManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getAppDataDir`
- `\OCP\IServerContainer::getCloudIdManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getGlobalScaleConfig`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getCloudFederationProviderManager`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getRemoteApiFactory`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getCloudFederationFactory`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getRemoteInstanceFactory`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getStorageFactory`: hacer que se inyecte la interfaz en su lugar
- `\OCP\IServerContainer::getGeneratorHelper`: hacer que se inyecte la interfaz en su lugar
- `\OC_App::registerLogIn()`: usar el {nc-ref}`arranque <bootstrapping>` y `\OCP\AppFramework\Bootstrap\IRegistrationContext::registerAlternativeLogin`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::createCachedCalendarObject`: escuchar `\OCA\DAV\Events\CachedCalendarObjectCreatedEvent`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::createCalendar`: escuchar `\OCA\DAV\Events\CalendarCreatedEvent`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::createCalendarObject`: escuchar `\OCA\DAV\Events\CalendarObjectCreatedEvent`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::createSubscription`: escuchar `\OCA\DAV\Events\SubscriptionCreatedEvent`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::deleteCachedCalendarObject`: escuchar `\OCA\DAV\Events\CachedCalendarObjectDeletedEvent`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::deleteCalendar`: escuchar `\OCA\DAV\Events\CalendarDeletedEvent`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::deleteCalendarObject`: escuchar `\OCA\DAV\Events\CalendarObjectDeletedEvent`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::deleteSubscription`: escuchar `\OCA\DAV\Events\SubscriptionDeletedEvent`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::publishCalendar`: escuchar `\OCA\DAV\Events\CalendarPublishedEvent`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::publishCalendar`: escuchar `\OCA\DAV\Events\CalendarUnpublishedEvent`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::updateCachedCalendarObject`: escuchar `\OCA\DAV\Events\CachedCalendarObjectUpdatedEvent`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::updateCalendar`: escuchar `\OCA\DAV\Events\CalendarUpdatedEvent`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::updateCalendarObject`: escuchar `\OCA\DAV\Events\CalendarObjectUpdatedEvent`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::updateShares`: escuchar `\OCA\DAV\Events\CalendarShareUpdatedEvent`
- Evento `\OCA\DAV\CalDAV\CalDavBackend::updateSubscription`: escuchar `\OCA\DAV\Events\SubscriptionUpdatedEvent`
- Evento `\\OCA\DAV\CardDAV\CardDavBackend::createCard`: escuchar `\OCA\DAV\Events\CardCreatedEvent`
- Evento `\OCA\DAV\CardDAV\CardDavBackend::deleteCard`: escuchar `\OCA\DAV\Events\CardDeletedEvent`
- Evento `\OCA\DAV\CardDAV\CardDavBackend::updateCard`: escuchar `\OCA\DAV\Events\CardUpdatedEvent`
- Evento `\OCA\Files_Sharing::loadAdditionalScripts:: publicShareAuth`: escuchar `\OCA\Files_Sharing\Event\BeforeTemplateRenderedEvent`
- Evento `\OCA\Files_Sharing::loadAdditionalScripts`: escuchar `\OCA\Files_Sharing\Event\BeforeTemplateRenderedEvent`
- Evento `\OCA\User_LDAP\User\User::postLDAPBackendAdded`: escuchar `\OCA\User_LDAP\Events\UserBackendRegistered`
- Evento `\OCA\User_LDAP\User\User::postLDAPBackendAdded`: escuchar `\OCA\User_LDAP\Events\GroupBackendRegistered`
- Evento `\OCP\AppFramework\Http\StandaloneTemplateResponse::EVENT_LOAD_ADDITIONAL_SCRIPT`: escuchar `\OCP\AppFramework\Http\Events\BeforeTemplateRenderedEvent`
- Evento `\OCP\AppFramework\Http\StandaloneTemplateResponse::EVENT_LOAD_ADDITIONAL_SCRIPTS_LOGGEDIN`: escuchar `\OCP\AppFramework\Http\Events\BeforeTemplateRenderedEvent`
- Evento `\OCP\WorkflowEngine::loadAdditionalSettingScripts`: escuchar `\OCP\WorkflowEngine\Events\LoadSettingsScriptsEvent`

#### Eliminado del espacio de nombres público

- `\OCP\IServerContainer::getAppFolder`
- Hook `\OCA\DAV\Connector\Sabre::authInit`: usar en su lugar el evento `\OCA\DAV\Events\SabrePluginAuthInitEvent`
- Evento `\OC_User::post_removeFromGroup`: escuchar `\OCP\Group\Events\UserRemovedEvent`
- Evento `\OCA\DAV\Connector\Sabre::authInit`: escuchar `\OCA\DAV\Events\SabrePluginAuthInitEvent`
````
