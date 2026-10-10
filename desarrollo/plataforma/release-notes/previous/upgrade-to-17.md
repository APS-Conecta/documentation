---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 17 para las apps: globales de JavaScript obsoletas y sus reemplazos, API de backend retiradas y cambios en LDAP y aprovisionamiento."
---
# Actualización a Nextcloud 17

## Resumen

Esta página enumera los cambios de la versión 17 que afectan a las apps: las variables globales de JavaScript obsoletas con su reemplazo, un plugin de jQuery eliminado, las API de backend retiradas del espacio de nombres público u obsoletas y los cambios de comportamiento en LDAP y en la API de aprovisionamiento. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_17.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Los cambios críticos se recopilaron [en GitHub](https://github.com/nextcloud/server/issues/15339). Consultar el ticket original para ver los enlaces a las pull requests y a los tickets.
:::

### Cambios de frontend

#### Variables globales obsoletas

- `initCore`: no usar esta función interna.
- `oc_appconfig`: usar `OC.appConfig` en su lugar.
- `oc_appswebroots`: usar `OC.appswebroots` en su lugar.
- `oc_capabilities`: usar `OC.getCapabilities()` en su lugar.
- `oc_config`: usar `OC.config` en su lugar.
- `oc_current_user`: usar `OC.getCurrentUser().uid` en su lugar.
- `oc_debug`: usar `OC.debug` en su lugar.
- `oc_isadmin`: usar `OC.isUserAdmin()` en su lugar.
- `oc_requesttoken`: usar `OC.requestToken` en su lugar.
- `oc_webroot`: usar `OC.getRootPath()` en su lugar.
- `OCDialogs`: usar `OC.dialogs` en su lugar.
- `OC._capabilities`: usar `OC.getCapabilities()` en su lugar.
- `OC.addTranslations`: usar *OC.L10N.load* en su lugar.
- `OC.coreApps`: solo para uso interno, sin reemplazo.
- `OC.getHost`: usar directamente `window.location.host`.
- `OC.getHostName`: usar directamente `window.location.hostname`.
- `OC.getPort`: usar directamente `window.location.port`.
- `OC.getProtocol`: usar directamente `window.location.protocol.split(':')[0]`.
- `OC.fileIsBlacklisted`: usar directamente la expresión regular `OC.config.blacklist_files_regex`.
- `OC.redirect`: usar directamente `window.location`.
- `OC.reload`: usar directamente `window.location.reload()`.

#### Plugins de jQuery eliminados

- `singleselect`: incluir uno propio si realmente se necesita.

### Cambios de backend

#### Eliminado del espacio de nombres público

- `\OCP\App::checkAppEnabled`
- `\OCP\Security\StringUtils`
- `\OCP\Util::callCheck`

#### Obsolescencias

- `\OCP\AppFramework\Http\EmptyContentSecurityPolicy::allowEvalScript`: esto significa que las apps ya no deben usar eval en su JavaScript. Se pretende prohibirlo de forma general en una versión futura de Nextcloud.
- `\OCP\AppFramework\Utility\IControllerMethodReflector::reflec`: se eliminará en la 18.

### Cambios de comportamiento

- LDAP: el valor predeterminado de `ldapGroupMemberAssocAttr` cambió de `uniqueMember` a sin definir. En las instalaciones automatizadas mediante scripts, debe definirse si se quieren usar grupos LDAP dentro de Nextcloud.
- API de aprovisionamiento: al crear usuarios, se devolverá el ID de usuario asignado como conjunto de datos, como en `['id' => $userid]`.
````
