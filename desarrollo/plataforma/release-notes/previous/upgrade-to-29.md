---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 29 para las apps: Circles pasa a Teams, notas de cambios de apps, IAppConfig rehecho, atributos de ruta y API eliminadas."
---
# Actualización a Nextcloud 29

## Resumen

Esta página enumera los cambios de la versión 29 que afectan a las apps: el cambio de nombre de Circles a Teams, las notificaciones de registros de cambios de las apps, el rango de `appinfo/info.xml`, el `IAppConfig` rehecho, los atributos de ruta y las API, variables globales y eventos modificados, obsoletos o eliminados. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_29.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### General

- La app Circles pasará a llamarse Teams. Las apps que usan los términos Circle/Circles deben ajustarse para usar Team/Teams en su lugar. Por ejemplo, `share to circle` pasaría a ser `share to team`.
- La app `updatenotification` ahora también admite notificaciones para las apps que se actualizaron.
  Si la app actualizada aporta un archivo `CHANGELOG.language.md` o `CHANGELOG.en.md`, creará notificaciones para los usuarios sobre estos cambios. Ver también la sección {nc-ref}`registro de cambios de la app <app changelog>`.

#### info.xml

Asegurarse de que el `appinfo/info.xml` de la app admita Nextcloud 29.

```xml
<dependencies>
    <nextcloud min-version="27" max-version="29" />
</dependencies>
```

### Cambios de frontend

#### API modificadas

- *IAppConfig* se rehízo por completo y la mayoría de sus métodos anteriores están ahora obsoletos. La nueva versión de la API implementa varios ajustes para los valores de configuración de la app que definen su carga diferida y su sensibilidad. Ver también la sección {nc-ref}`app config`.

#### Variables globales eliminadas

- Se eliminó la variable global `autosize`: estaba obsoleta desde hacía más de 4 años y su eliminación estaba prevista para Nextcloud 20. Si todavía se necesita, hay que incluir una versión propia.

#### API obsoletas

- `OC.dialogs.fileexists` está obsoleto. Usar en su lugar `openConflictPicker` de [@nextcloud/upload](https://nextcloud-libraries.github.io/nextcloud-upload/functions/openConflictPicker.html).

### Cambios de backend

#### API añadidas

- Los atributos `OCP\AppFramework\Http\Attribute\ApiRoute` y `OCP\AppFramework\Http\Attribute\FrontpageRoute` pueden usarse para el enrutamiento, registrando rutas. Ver {nc-doc}`developer_manual/basics/routing` para la documentación.

#### API modificadas

- `OCP\IURLGenerator::URL_REGEX_NO_MODIFIERS`: se cambió para que coincida con localhost y con nombres de host con puerto.
- `OCP\Files\IMimeTypeLoader`: ahora todos los métodos de esta interfaz tienen declaraciones de tipo. Asegurarse de actualizar la implementación, si se tiene una.
- `OCP\IRequest::getParam('_route')` y `OCP\IRequest::getParams()['_route']`: el nombre de la ruta (formado por el ID de la app, el nombre del controlador y el método del controlador) ahora está todo en minúsculas

#### API eliminadas

- `OCP\Log\ILogFactory::getCustomLogger`: usar `\OCP\Log\ILogFactory::getCustomPsrLogger` para obtener un logger {nc-ref}`PSR3 <psr3>` personalizado
- Tabla `oc_share`: debido al enorme impacto en el rendimiento de las consultas al seleccionar además por `item_type`,
  ya no se permite usar la tabla `oc_share` para ningún tipo que no sea `file` y `folder`.
- `OC\BackgroundJob\Job`, `OC\BackgroundJob\QueuedJob` y `OC\BackgroundJob\TimedJob`: usar las versiones de `OCP`.

#### Eventos eliminados

- `OCP\Dashboard\RegisterWidgetEvent` quedó obsoleto en Nextcloud 20 y ahora se ha eliminado. Usar `OCP\AppFramework\Bootstrap\IRegistrationContext::registerDashboardWidget` desde el arranque de la app.

#### Cambios de comportamiento

El panel ya no carga los scripts de la barra lateral ni de Viewer; si el widget del panel depende de ello, debe emitir él mismo los eventos necesarios.
````
