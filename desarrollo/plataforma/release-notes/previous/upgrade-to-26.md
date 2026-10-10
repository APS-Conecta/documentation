---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 26 para las apps: sección Groupware, Bootstrap eliminado, fin de PHP 7.4, PHP 8.2, atributos de PHP, PSR-0 y cambios de API."
---
# Actualización a Nextcloud 26

## Resumen

Esta página enumera los cambios de la versión 26 que afectan a las apps: el rango de `appinfo/info.xml`, el traslado de la sección de ajustes *Groupware* a *Disponibilidad*, la eliminación de Bootstrap, el fin de PHP 7.4 y la llegada de PHP 8.2, la migración a atributos nativos de PHP, el fin previsto de PSR-0 y las API añadidas, modificadas, obsoletas o eliminadas. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_26.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Los cambios críticos se recopilaron [en GitHub](https://github.com/nextcloud/server/issues/34692).
Consultar el ticket original para ver los enlaces a las pull requests y a los tickets.
:::

### General

#### info.xml

Asegurarse de que el `appinfo/info.xml` de la app admita Nextcloud 26.

```xml
<dependencies>
    <nextcloud min-version="23" max-version="26" />
</dependencies>
```

### La sección de ajustes personales *Groupware* pasa a *Disponibilidad*

Hasta Nextcloud 25 existía una {nc-ref}`sección de ajustes <settings-section>` *Groupware* con el ID `groupware`. A partir de Nextcloud 26, esta sección ya no existe. Los ajustes del servidor existentes se trasladaron a una nueva sección *Disponibilidad*/`availability`.

Si la app ofrece ajustes relacionados con groupware, comprobar si pueden mostrarse en la página *Disponibilidad* o si necesitan una nueva sección propia de la app.

### Cambios de frontend

#### API eliminadas

- {code}`OC.addTranslations` estaba obsoleto desde Nextcloud 17 y ahora se ha eliminado.
- El fondo de «iconos de apps» (<https://github.com/nextcloud/server/blob/stable25/core/img/background.png> y <https://github.com/nextcloud/server/blob/stable25/core/img/background.svg>) ya no se usa y se eliminará (solo se usaba en la página de inicio de sesión, donde ahora se usa el fondo de «nubes»).
- **Bootstrap eliminado**: el bootstrap incluido solo se usaba desde hacía mucho tiempo para los tooltips, pero se incluía y, por lo tanto, estaba disponible globalmente. Como la versión incluida ha llegado al final de su vida útil (EOL), se decidió eliminarlo en lugar de introducir una actualización incompatible. Para cualquier tooltip se recomienda simplemente pasar al atributo HTML nativo {code}`title=`. ([PR#36434](https://github.com/nextcloud/server/pull/36434)

### Cambios de backend

#### PHP 7.4

En esta versión se dejó de admitir PHP 7.4. Asegurarse de que la app sea compatible con PHP 8.0 o superior.

#### PHP 8.2

En esta versión se añadió la compatibilidad con PHP 8.2. Consultar las notas de versión de PHP sobre las nuevas obsolescencias.

#### Migración de las anotaciones PHPDoc a atributos nativos de PHP

Nextcloud 26 es compatible con PHP 8.0 y posteriores. Esto permite migrar de las anotaciones PHPDoc a los atributos nativos.

- `@UseSession` debe reemplazarse por `#[UseSession]`. `@UseSession` se eliminará en una versión futura. Ver {nc-ref}`controller-use-session`.

#### Eliminación prevista de la carga de clases PSR-0

Nextcloud todavía carga clases que siguen el {nc-ref}`estándar PSR-0 <psr0>`, obsoleto y reemplazado desde hace tiempo. Nextcloud 26 es la última versión que registra un cargador de clases PSR-0 genérico. A partir de Nextcloud 27, las apps tienen que cambiar los nombres de los archivos de clase para que se ajusten a PSR-4 o incluir su propio cargador de clases (de composer) para los archivos PSR-0, o. ([PR#36114](https://github.com/nextcloud/server/pull/36114)

#### Parámetros de inyección de dependencias

Los parámetros del contenedor de la app con nombres en PascalCase `AppName`, `UserId` y `WebRoot` están obsoletos. Usar en su lugar las variantes en camelCase `appName`, `userId` y `webRoot` si se inyectan en alguna de las clases de la app.

#### API modificadas

- `OCP\Files\SimpleFS\ISimpleFile::getSize()` ahora puede devolver un float (para admitir tamaños >2G en sistemas de 32 bits)
- `OCP\Files\SimpleFS\InMemoryFile::getSize()` ahora puede devolver un float (para admitir tamaños >2G en sistemas de 32 bits)
- Ya no es necesario llamar a `setParsedSubject` y `setParsedMessage` en las notificaciones y los eventos de actividad cuando se usan setRichSubject y setRichMessage: se calcula automáticamente una versión analizada. ([PR#34807](https://github.com/nextcloud/server/pull/34807)
- Se trasladó `ICreateFromString::handleIMipMessage(string $name, string $calendarData): void;` a su propia interfaz, `IHandleImipMessage` ([PR#34893](https://github.com/nextcloud/server/pull/34893)
- Las firmas de los métodos de `OCP\AppFramework\Db\Entity` cambiaron de la siguiente manera ([ref](https://github.com/nextcloud/server/commit/e91457d9cd68182591038636155d415b5dee0ec4)):
  - `public static function fromParams(array $params) -> public static function fromParams(array $params): static`
  - `public static function fromRow(array $row) -> public static function fromRow(array $row): static`
  - `protected function setter($name, $args) -> protected function setter(string $name, array $args): void`
  - `protected function getter($name) -> protected function getter(string $name): mixed`
  - `protected function markFieldUpdated($attribute) -> protected function markFieldUpdated(string $attribute): void`
- Los middlewares pueden registrarse globalmente (ver {nc-ref}`global_middlewares`, [PR#36310](https://github.com/nextcloud/server/pull/36310)

#### API eliminadas

- Se eliminó el método `OCP\BackgroundJob\IJobList::getAll` ([PR#36073](https://github.com/nextcloud/server/pull/36073)
- Se eliminó la dependencia de terceros `php-ds/php-ds` ([PR#36198](https://github.com/nextcloud/server/pull/36198)
- Se eliminó el método `OCP\Contacts\IManager::getAddressBooks` ([PR#34329](https://github.com/nextcloud/server/pull/34329)
- Se eliminaron las constantes de nivel de registro de `OCP\Util` ([PR#34329](https://github.com/nextcloud/server/pull/34329)
- Se eliminó la dependencia de terceros `nikic/php-parser` ([PR#36393](https://github.com/nextcloud/server/pull/36393)
- Se eliminó `OCP\AppFramework\Db\Mapper`, que estaba obsoleto. Se puede migrar fácilmente a `OCP\AppFramework\Db\QBMapper`, que hace lo mismo usando el constructor de consultas en lugar de consultas basadas en cadenas. ([PR#34490](https://github.com/nextcloud/server/pull/34490)
- Se eliminaron las clases obsoletas de `OCP\Dashboard` ([PR#35966](https://github.com/nextcloud/server/pull/35966)

#### API añadidas

- Nuevo `OCP\Authentication\Token\IProvider` para los proveedores de autenticación: se creó una nueva interfaz pública, `OCP\Authentication\Token\IProvider`, con un método invalidateTokensOfUser para invalidar todos los tokens de un usuario concreto. `OC\Authentication\Token\Manager` implementa `OCP\Authentication\Token\IProvider`. ([PR#36033](https://github.com/nextcloud/server/pull/36033)
- Cabecera `Auto-Submitted` para los correos electrónicos: ahora hay un nuevo método en la interfaz `OCP\Mail\IMessage`, `IMessage::setAutoSubmitted()`. Con este método se puede indicar que un correo electrónico era un correo o una respuesta automáticos, para que los servidores de correo puedan detectar mejor si debe enviarse una respuesta de fuera de la oficina, almacenar o filtrar mejor los correos, etc. Los valores posibles están documentados en la interfaz `OCP\Mail\Headers\AutoSubmitted`. ([PR#36033](https://github.com/nextcloud/server/pull/36033)
- Se añadió el método `OCP\BackgroundJob\IJobList::getJobsIterator` ([PR#36073](https://github.com/nextcloud/server/pull/36073))
- Nuevo evento `OCP\BeforeSabrePubliclyLoadedEvent`, que se despacha en los endpoints WebDAV públicos (puede usarse igual que `OCP\SabrePluginEvent`, por ejemplo para inyectar plugins de Sabre adicionales en las apps) ([PR#35789](https://github.com/nextcloud/server/pull/35789))

### Obsolescencias

- Se declaró obsoleto el método `OCP\BackgroundJob\IJobList::getJobs` ([PR#36073](https://github.com/nextcloud/server/pull/36073))
- La anotación de acción de controlador `@UseSession` está obsoleta. Usar en su lugar el nuevo atributo `UseSession` ([PR#36363](https://github.com/nextcloud/server/pull/36363)
- **Evento jQuery de notificaciones obsoleto**: el evento `OCA.Notification.Action` de la app de notificaciones está obsoleto en favor de un evento del bus de eventos `notifications:action:executed` con ([PR#728](https://github.com/nextcloud/notifications/pull/728)
````
