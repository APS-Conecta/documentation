---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 18 para las apps: tamaño de fuente, globales obsoletas, espacio WorkflowEngine y cambios en compartición, barra lateral y Viewer."
---
# Actualización a Nextcloud 18

## Resumen

Esta página enumera los cambios de la versión 18 que afectan a las apps: el aumento del tamaño de fuente, las variables globales de JavaScript obsoletas, el nuevo espacio de nombres `\OCP\WorkflowEngine`, una API obsoleta y los cambios de comportamiento en las comparticiones, la barra lateral y Viewer. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_18.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Los cambios críticos se recopilaron [en GitHub](https://github.com/nextcloud/server/issues/17131). Consultar el ticket original para ver los enlaces a las pull requests y a los tickets.
:::

### Cambios de frontend

#### CSS

- Se aumentó el tamaño de fuente general. Asegurarse de usar unidades relativas como *rem* en lugar de píxeles.

#### Variables globales obsoletas

- `Backbone`: incluir una propia.
- `Clipboard`: incluir una propia.
- `ClipboardJs`: incluir una propia.
- `DOMPurify`: incluir una propia.
- `Handlebars`: incluir una propia.
- `jstimezonedetect`: incluir una propia.
- `jstz`: incluir una propia.
- `md5`: incluir una propia.
- `moment`: incluir una propia.
- `OC.basename`: usar `basename` de <https://www.npmjs.com/package/@nextcloud/paths>
- `OC.dirname`: usar `dirname` de <https://www.npmjs.com/package/@nextcloud/paths>
- `OC.encodePath`: usar `encodePath` de <https://www.npmjs.com/package/@nextcloud/paths>
- `OC.isSamePath`: usar `isSamePath` de <https://www.npmjs.com/package/@nextcloud/paths>
- `OC.joinPaths`: usar `joinPaths` de <https://www.npmjs.com/package/@nextcloud/paths>

### Cambios de backend

#### Nuevas API

- Espacio de nombres `\OCP\WorkflowEngine`

#### Obsolescencias

- `\OCP\Collaboration\Resources\IManager::registerResourceProvider`: usar `\OCP\Collaboration\Resources\IProviderManager::registerResourceProvider` en su lugar.

### Cambios de comportamiento

- Las comparticiones por correo electrónico y las comparticiones por enlace ahora comparten la misma configuración.
  No se pueden crear comparticiones por correo electrónico si la administración ha deshabilitado los enlaces de compartición
- Registrar los scripts de las nuevas pestañas de la barra lateral con el script `OCA\Files\Event\LoadSidebar\Event`
- Viewer ahora vincula el objeto de archivo completo a las vistas. ¡Los nombres de las variables cambiaron!
````
