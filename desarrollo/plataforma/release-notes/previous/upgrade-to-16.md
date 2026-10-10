---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 16 para las apps: CSP, bibliotecas JavaScript obsoletas, PHP 7.1 y PostgreSQL 9.5 requeridos y API de backend eliminadas."
---
# Actualización a Nextcloud 16

## Resumen

Esta página enumera los cambios de la versión 16 que afectan a las apps: el valor predeterminado de la CSP, las bibliotecas JavaScript incluidas que quedan obsoletas, los nuevos requisitos de PHP y PostgreSQL, el fin de `appinfo/classpath.php` y las API de backend eliminadas. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_16.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Los cambios críticos se recopilaron [en GitHub](https://github.com/nextcloud/server/issues/12915). Consultar el ticket original para ver los enlaces a las pull requests y a los tickets.
:::

### Cambios de frontend

- CSP: `frame-anchestor` se establece en `self` de forma predeterminada.

#### Obsolescencia de las bibliotecas JavaScript incluidas

Las siguientes bibliotecas se consideran obsoletas a partir de Nextcloud 16. Si se usa alguna de ellas en una app, hay que asegurarse de incluir una versión propia, debidamente empaquetada con la app.

- `marked`
- `Clipboard` -> ahora se exporta como `ClipboardJS` para resolver conflictos de nombres en Chrome.
- Las apps deben incluir sus propias dependencias de javascript y no depender de lo que incluye el servidor, por ejemplo jquery, etc. Depender del paquete dist del servidor está obsoleto a partir de NC16.
- `escapeHTML`
- `formatDate`
- `getURLParameter`
- `humanFileSize`
- `relative_modified_date`
- `select2`

### Cambios de backend

- Se eliminó la compatibilidad con PHP 7.0. Se requiere PHP 7.1 o superior.
- Se requiere PostgreSQL 9.5+.
- Carga automática: antes también era posible cargar automáticamente clases PHP en las apps especificando una lista de clases y nombres de archivo en *appinfo/classpath.php*. Esto ya no debe usarse y tampoco lo usa ninguna app disponible públicamente.

#### API eliminadas

- `\OCP\Activity\IManager::getNotificationTypes`
- `\OCP\Activity\IManager::getDefaultTypes`
- `\OCP\Activity\IManager::getTypeIcon`
- `\OCP\Activity\IManager::translate`
- `\OCP\Activity\IManager::getSpecialParameterList`
- `\OCP\Activity\IManager::getGroupParameter`
- `\OCP\Activity\IManager::getNavigation`
- `\OCP\Activity\IManager::isFilterValid`
- `\OCP\Activity\IManager::filterNotificationTypes`
- `\OCP\Activity\IManager::getQueryForFilter`
- `\OCP\Security\ISecureRandom::getLowStrengthGenerator`
- `\OCP\Security\ISecureRandom::getMediumStrengthGenerator`
````
