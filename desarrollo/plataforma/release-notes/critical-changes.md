---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios imprescindibles para que una app siga funcionando en la nueva versión: rango en info.xml y API de frontend y backend eliminadas."
---
(nc-dev-critical-changes)=
# Cambios críticos

## Resumen

Esta página enumera los cambios imprescindibles para que una app siga funcionando en la nueva versión: el rango de versiones en info.xml, las API y bibliotecas de frontend y las API de backend eliminadas, y tres cambios de interfaz anunciados. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/critical_changes.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Requisitos de info.xml

Actualizar info.xml para añadir Nextcloud 34 al rango de versiones compatibles:

```xml
<dependencies>
  <nextcloud min-version="34" max-version="34" />
</dependencies>
```

Para permitir también la instalación en versiones anteriores, basta con mantener el min-version anterior.

### API y bibliotecas de frontend eliminadas

- `OC.Dialogs.fileexists` estaba obsoleto y ahora se ha eliminado.
  En su lugar, usar el selector de conflictos de la biblioteca `@nextcloud/dialogs`.
- `OC.Notifications` estaba obsoleto y ahora se ha eliminado.
  En su lugar, usar la API de notificaciones de la biblioteca `@nextcloud/dialogs`.
- `OC.Apps` estaba obsoleto y ahora se ha eliminado.
  En su lugar, usar componentes Vue de `@nextcloud/vue`.
- Los métodos `OC.*menu*` estaban obsoletos y ahora se han eliminado.
  En su lugar, usar componentes Vue de `@nextcloud/vue`.
- Se eliminó la gestión mágica de `.live-relative-timestamp` (los elementos con esta clase se actualizaban automáticamente para mostrar marcas de tiempo relativas).
  En su lugar, usar el componente `NcDateTime` de la biblioteca `@nextcloud/vue`.
- El `snapper` global estaba obsoleto y ahora se ha eliminado.
  Para la navegación de la app, migrar la app a Vue
  y usar en su lugar el componente `NcAppNavigation` de la biblioteca `@nextcloud/vue`.
- Se eliminaron algunas bibliotecas compartidas globalmente que estaban obsoletas. Si todavía se depende de ellas, hay que empaquetarlas con la app:

  - `jQuery` estaba obsoleto y con su eliminación prevista desde Nextcloud 19.
  - `jQuery UI` estaba obsoleto y con su eliminación prevista desde Nextcloud 19.
  - `Backbone` estaba obsoleto y con su eliminación prevista desde Nextcloud 19.
  - `OC.Files.Client`, ya que extendía `Backbone`.
  - `Handlebars` estaba obsoleto y con su eliminación prevista desde Nextcloud 19.

### API de backend eliminadas

- Se eliminaron `\OCP\Share_Backend`, `\OCP\Share_Backend_Collection` y `\OCP\Share_Backend_File_Dependent`. Este antiguo
  backend de compartición se sustituyó en Nextcloud 9 por un nuevo sistema de backends basado en `IShareProvider`.
- Se eliminaron todos estos métodos, obsoletos desde antes de Nextcloud 20:

  - `\OCP\AppFramework\Http\EmptyContentSecurityPolicy::allowEvalScript`
  - `\OCP\AppFramework\Http\EmptyContentSecurityPolicy::addAllowedChildSrcDomain`
  - `\OCP\AppFramework\Http\EmptyContentSecurityPolicy::disallowChildSrcDomain`
  - `\OCP\Collaboration\Resources\IManager::registerResourceProvider`
  - `\OCP\Notification\IManager::registerNotifier`
  - `\OCP\Util::recursiveArraySearch`
- Se eliminaron todas estas clases, obsoletas desde antes de Nextcloud 20:

  - `\OCP\AppFramework\Http\StrictContentSecurityPolicy`
  - `\OCP\AppFramework\Http\StrictEvalContentSecurityPolicy`
  - `\OCP\AppFramework\Http\StrictInlineContentSecurityPolicy`
- Se eliminaron varios métodos de la antigua clase estática `OC_Util`:

  - En lugar de `\OC_Util::encodePath`, usar `\OCP\Util::encodePath`.
  - En lugar de `\OC_Util::sanitizeHTML`, usar `\OCP\Util::sanitizeHTML`.
  - En lugar de `\OC_Util::redirectToDefaultPage` y `\OC_Util::getDefaultPageUrl`, usar `\OCP\IUrlGenerator::linkToDefaultPageUrl`.
  - En lugar de `\OC_Util::checkAdminUser`, usar `IGroupManager::class::isAdmin`.

### Revisión del estilo de la navegación

Se revisará el estilo de los componentes de navegación. Ver [nextcloud-libraries/nextcloud-vue#7222](https://github.com/nextcloud-libraries/nextcloud-vue/issues/7222) para más detalles.

### Rediseño de las pestañas de la barra lateral

Se rediseñarán los componentes de las pestañas de la barra lateral. Ver [nextcloud-libraries/nextcloud-vue#7520](https://github.com/nextcloud-libraries/nextcloud-vue/issues/7520) para más detalles.

### Alineación a la izquierda del título de los ajustes

La alineación del título de las páginas de ajustes pasará a ser a la izquierda. Ver [nextcloud-libraries/nextcloud-vue#7641](https://github.com/nextcloud-libraries/nextcloud-vue/issues/7641) para más detalles.
````
