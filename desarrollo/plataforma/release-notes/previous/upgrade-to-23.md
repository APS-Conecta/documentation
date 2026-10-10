---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 23 para las apps: getPassword anulable, API de calendario obsoletas, doctrine/dbal 3.1 y ExternalLinkActions obsoleta."
---
# Actualización a Nextcloud 23

## Resumen

Esta página enumera los cambios de la versión 23 que afectan a las apps: `getPassword` de `UserLoggedInEvent` pasa a ser anulable, varios métodos de `\OCP\Calendar\IManager` quedan obsoletos, `doctrine/dbal` se actualiza a 3.1 y la API de frontend `OCA.Sharing.ExternalLinkActions` queda obsoleta. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_23.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Los cambios críticos se recopilaron [en GitHub](https://github.com/nextcloud/server/issues/27846). Consultar el ticket original para ver los enlaces a las pull requests y a los tickets.
:::

### Cambios de backend

#### API modificadas

- `\OCP\User\Events\UserLoggedInEvent::getPassword` ahora es anulable porque, en configuraciones SSO, es posible iniciar sesión sin contraseña

#### API obsoletas

- `\OCP\Calendar\IManager::search`: usar {nc-ref}`la nueva API de búsqueda de calendarios <calendar-search>`
- `\OCP\Calendar\IManager::isEnabled`: no hay reemplazo
- `\OCP\Calendar\IManager::registerCalendar`: usar {nc-ref}`proveedores de calendarios <calendar-providers>`
- `\OCP\Calendar\IManager::unregisterCalendar` no hay reemplazo
- `\OCP\Calendar\IManager::register`: usar {nc-ref}`proveedores de calendarios <calendar-providers>`
- `\OCP\Calendar\IManager::getCalendars`: usar {nc-ref}`la nueva API de calendarios <calendar-access>`
- `\OCP\Calendar\IManager::clear`: no hay reemplazo

#### Bibliotecas del núcleo actualizadas

##### `doctrine/dbal`

La capa de abstracción de bases de datos de Doctrine (dbal) impulsa la conexión a la base de datos y el constructor de consultas de Nextcloud. En Nextcloud 23, esta dependencia se actualizó de 3.0 a 3.1. En consecuencia, el método `\OC\DB\QueryBuilder\QueryBuilder::getFirstResult` ahora devuelve `0` en lugar de `null` si no se llamó a `\OC\DB\QueryBuilder\QueryBuilder::setFirstResult`.

### Cambios de frontend

#### API obsoletas

- La API *OCA.Sharing.ExternalLinkActions* quedó obsoleta en favor de *OCA.Sharing.ExternalShareAction*.
````
