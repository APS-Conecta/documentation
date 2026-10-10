---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 19 para las apps: fin del polyfill de Babel, jQuery obsoleto, reemplazos de globales, Symfony 4.4 y servicios por nombre obsoletos."
---
# Actualización a Nextcloud 19

## Resumen

Esta página enumera los cambios de la versión 19 que afectan a las apps: el fin del polyfill global de Babel, la obsolescencia de jQuery, las variables globales obsoletas o eliminadas con sus reemplazos, la actualización a Symfony 4.4, la obsolescencia de la inyección de servicios por nombre y las API nuevas y modificadas. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_19.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Los cambios críticos se recopilaron [en GitHub](https://github.com/nextcloud/server/issues/18479). Consultar el ticket original para ver los enlaces a las pull requests y a los tickets.
:::

### Cambios de frontend

#### Eliminación del polyfill de Babel

Nextcloud 19 ya no incluye un polyfill global de Babel, sino que usa core-js en su lugar. Asegurarse de que los scripts de frontend no dependan de API del navegador cubiertas por polyfills.

#### Obsolescencia de jQuery

A partir de Nextcloud 19, los globales *jquery* y *$* quedan obsoletos para las apps. Aunque la biblioteca no se eliminará de inmediato, para dar tiempo a que quienes desarrollan se adapten, se recomienda reemplazarla por otra biblioteca o simplemente usar una herramienta de empaquetado como webpack para acotarla al código propio. La biblioteca se actualizará en Nextcloud en futuras versiones de Nextcloud, y las versiones más recientes de jQuery traen cambios incompatibles.

#### Variables globales obsoletas

- `OC.currentUser`: usar `getCurrentUser` de <https://www.npmjs.com/package/@nextcloud/auth>
- `OC.filePath`: usar `generateFilePath` de <https://www.npmjs.com/package/@nextcloud/router>
- `OC.generateUrl`: usar `generateUrl` de <https://www.npmjs.com/package/@nextcloud/router>
- `OC.get`: usar <https://lodash.com/docs#get>
- `OC.getCurrentUser`: usar `getCurrentUser` de <https://www.npmjs.com/package/@nextcloud/auth>
- `OC.getRootPath`: usar `getRootUrl` de <https://www.npmjs.com/package/@nextcloud/router>
- `OC.imagePath`: usar `imagePath` de <https://www.npmjs.com/package/@nextcloud/router>
- `OC.linkTo`: usar `linkTo` de <https://www.npmjs.com/package/@nextcloud/router>
- `OC.linkToOCS`: usar `generateOcsUrl` de <https://www.npmjs.com/package/@nextcloud/router>
- `OC.linkToRemote`: usar `generateRemoteUrl` de <https://www.npmjs.com/package/@nextcloud/router>
- `OC.set`: usar <https://lodash.com/docs#set>
- `OC.webroot`: usar `getRootUrl` de <https://www.npmjs.com/package/@nextcloud/router>
- `OCP.Toast.*`: usar <https://www.npmjs.com/package/@nextcloud/dialogs>

#### Variables globales eliminadas

- `getURLParameter`
- `formatDate`
- `humanFileSize`
- `relative_modified_date`

#### Bibliotecas eliminadas

- `marked`

### Cambios de backend

#### Actualización de Symfony

Symfony se actualizó a la [v4.4](https://github.com/symfony/symfony/blob/4.4/CHANGELOG-4.4.md). El cambio más importante para las apps es que los comandos de CLI deben devolver un valor int. Devolver null (de forma explícita o implícita) no se permitirá en futuras versiones de Symfony.

#### Obsolescencia de la inyección de servicios con nombre

Las apps podían consultar servicios del núcleo, como la implementación de la interfaz `\OCP\ITagManager`, con el nombre `TagManager`. Para unificar la resolución de servicios con las declaraciones de tipo de la inyección por constructor, la resolución por nombre queda obsoleta, registra advertencias y se eliminará en el futuro. Usar en su lugar el nombre de clase completamente calificado (con la constante *::class*):

Si se tenía

```php
$tagManager = \OC::$server->query('TagManager');
```

cambiar el código por

```php
$tagManager = \OC::$server->query(\OCP\ITagManager::class);
```

En los argumentos del constructor, siempre debe declararse el tipo del servicio con su interfaz. Si ya se hace así, nada cambia.

#### Nuevas API

- Se añadió la clase `\OCP\Authentication\Events\LoginFailedEvent`
- Se añadió el método `\OCP\Comments\IComment::getReferenceId`
- Se añadió el método `\OCP\Comments\IComment::setReferenceId`
- Se añadió la clase `\OCP\Contacts\Events\ContactInteractedWithEvent`
- Se añadió el método `\OCP\EventDispatcher\IEventDispatcher::removeListener`
- Se añadió la constante `\OCP\ITags::TAG_FAVORITE`
- Se añadió la clase `\OCP\Mail\Events\BeforeMessageSent`
- Se añadió el método `\OCP\Lock\LockedException::getExistingLock`
- Se añadió la clase `\OCP\Share\Events\VerifyMountPointEvent`
- Se añadió el método `\OCP\Share\IManager::allowEnumeration`
- Se añadió el método `\OCP\Share\IManager::limitEnumerationToGroups`

#### API modificadas

- `\OCP\User\Events\BeforeUserLoggedInEvent::getUsername` ahora devuelve correctamente una cadena y no un `\OCP\IUser`
````
