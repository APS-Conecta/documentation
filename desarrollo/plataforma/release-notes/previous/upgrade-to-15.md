---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 15 para las apps: unsafe-eval ya no permitido por defecto, fin de PHP 7.0 y API de frontend y backend obsoletas o eliminadas."
---
# Actualización a Nextcloud 15

## Resumen

Esta página enumera los cambios de la versión 15 que afectan a las apps: `unsafe-eval` ya no se permite por defecto, se deja de admitir PHP 7.0 y varias API de frontend y backend quedan obsoletas o se eliminan. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_15.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Los cambios críticos se recopilaron [en GitHub](https://github.com/nextcloud/server/issues/15339). Consultar el ticket original para ver los enlaces a las pull requests y a los tickets.
:::

### Cambios de frontend

- `unsafe-eval` ya no se permite de forma predeterminada.

#### API eliminadas

- `fileDownloadPath()`
- `getScrollBarWidth()`
- `OC.AppConfig.hasKey()`
- `OC.AppConfig.deleteApp()`
- `OC.Share.ShareConfigModel.areAvatarsEnabled()`
- `OC.Util.hasSVGSupport()`
- `OC.Util.replaceSVGIcon()`
- `OC.Util.replaceSVG()`
- `OC.Util.scaleFixForIE8()`
- `OC.Util.isIE8()`

### Cambios de backend

- Se eliminó la compatibilidad con PHP 7.0

#### API obsoletas

- `\OCP\Util::linkToPublic`
- `\OCP\Util::recursiveArraySearch`

#### API eliminadas

- `\OCP\Activity\IManager::publishActivity`
- `\OCP\Util::logException`
- `\OCP\Util::mb_substr_replace`
- `\OCP\Util::mb_str_replace`
````
