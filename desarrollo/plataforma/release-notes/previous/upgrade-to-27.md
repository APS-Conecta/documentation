---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 27 para las apps: módulos .mjs, API Files Router, fin del cargador PSR-0, ITimeFactory con PSR-20 y cambios de las API."
---
# Actualización a Nextcloud 27

## Resumen

Esta página enumera los cambios de la versión 27 que afectan a las apps: el rango de `appinfo/info.xml`, los módulos JavaScript `.mjs`, la API Files Router, el cargador de clases optimizado, el fin del cargador de clases PSR-0, las API de backend añadidas, modificadas, obsoletas o eliminadas, los cambios de comportamiento y los de las API de cliente. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_27.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Los cambios críticos se recopilaron [en GitHub](https://github.com/nextcloud/server/issues/37039).
Consultar el ticket original para ver los enlaces a las pull requests y a los tickets.
:::

### General

#### info.xml

Asegurarse de que el `appinfo/info.xml` de la app admita Nextcloud 27.

```xml
<dependencies>
    <nextcloud min-version="25" max-version="27" />
</dependencies>
```

### Cambios de frontend

#### General

- Con Nextcloud 27 también se pueden aportar archivos JavaScript de módulo con la extensión de archivo `.mjs`. Por compatibilidad con versiones anteriores, se pueden aportar archivos con el mismo nombre pero con la extensión de archivo `.js`, que se cargarán en las versiones de Nextcloud anteriores a la 27.

#### API añadidas

- Una nueva API Files Router permite controlar el servicio de enrutamiento de archivos y actualizar vistas, consultas o parámetros sin recargar la página. Ver {nc-ref}`FilesAPI`

### Cambios de backend

#### Cargador de clases optimizado

Esta documentación recomendaba antes usar cualquier optimización del cargador de clases de composer en {nc-ref}`app-custom-classloader`. Lamentablemente, los mapas de clases autoritativos no funcionan con el proceso de actualización de las apps de Nextcloud. Cuando el código de una app se reemplaza durante su actualización, el autocargador también tiene que cargar clases *nuevas*. Los cargadores de clases autoritativos no lo hacen, por diseño. Usar solo la optimización simple del mapa de clases.

#### Eliminación del cargador de clases PSR-0

Nextcloud 27 ya no carga clases que siguen el {nc-ref}`estándar de nombres PSR-0 <psr0>`, obsoleto. {nc-ref}`Actualizar la estructura a PSR-4 <app-psr4-autoloader>` o {nc-ref}`incluir un autocargador personalizado <app-custom-classloader>`.

#### API añadidas

- `\OCP\AppFramework\Utility\ITimeFactory` ahora es un `\PSR\Clock\ClockInterface` que sigue el [estándar PSR-20](https://www.php-fig.org/psr/psr-20/#21-clockinterface). ([nextcloud/server#35872](https://github.com/nextcloud/server/pull/35872))
- Se añadió `\OCP\Accounts\IAccountManager::PROPERTY_DISPLAYNAME_LEGACY` para mantener la compatibilidad de la API de aprovisionamiento. ([nextcloud/server#36665](https://github.com/nextcloud/server/pull/36665))
- Se añadió una nueva configuración del sistema, `ratelimit.protection.enabled` (booleana, true por defecto), para que quienes desarrollan puedan **desactivar** la limitación de tasa. **No** se recomienda desactivarla en un sistema de producción o en vivo. ([nextcloud/server#37542](https://github.com/nextcloud/server/pull/37542))
- Se introdujo una nueva API OCP en `\OCP\SpeechToText` para permitir la transcripción automática de contenido multimedia ([nextcloud/server#37674](https://github.com/nextcloud/server/pull/37674))
- Se añadió una nueva interfaz, `\OCP\BackgroundJob\IParallelAwareJob`, que ahora implementa `\OCP\BackgroundJob\Job`. Puede usarse para indicar que no deben ejecutarse varias instancias de un trabajo al mismo tiempo. También se añadió el método `\OCP\BackgroundJob\IJobList#hasReservedJob(?string $className = null)` para comprobar la condición ([nextcloud/server#37835](https://github.com/nextcloud/server/pull/37835))
- Se añadió la nueva propiedad `$actionLabel` a la clase `\OCP\Files\Template\TemplateFileCreator`, con su setter `TemplateFileCreator::setActionLabel` y su getter `TemplateFileCreator::getActionLabel`. ([nextcloud/server#37929](https://github.com/nextcloud/server/pull/37929) + [nextcloud/server#37955](https://github.com/nextcloud/server/pull/37955))
- Se añadió una nueva interfaz, `\OCP\Group\Backend\ISearchableGroupBackend`, para los backends de grupos que admiten el nuevo método `searchInGroup`, que busca entre los usuarios de un grupo de forma eficiente. ([nextcloud/server#32866](https://github.com/nextcloud/server/pull/32866))
- `\OCP\App\IAppManager` tiene los siguientes métodos nuevos ([nextcloud/server#36591](https://github.com/nextcloud/server/pull/36591)):
  - `loadApp(string $app): void` Cargar una app, si aún no está cargada
  - `isAppLoaded(string $app): bool` Comprobar si una app está cargada
  - `loadApps(array $types = []): bool` Carga todas las apps. Si $types es un array no vacío, solo se cargarán las apps de esos tipos.
  - `isType(string $app, array $types): bool` Comprobar si una app es de un tipo concreto
- Se añadió el nuevo método `atomicRetry()` al trait `\OCP\AppFramework\Db\TTransactional`, como envoltorio de atomic(), para reintentar operaciones de base de datos después de que se produzca una excepción reintentable, como un interbloqueo de la base de datos ([nextcloud/server#38030](https://github.com/nextcloud/server/pull/38030))

#### API modificadas

- `\OCP\UserMigration\ISizeEstimationMigrator::getEstimatedExportSize()` ahora devuelve `int|float` para admitir sistemas de 32 bits. ([nextcloud/server#38104](https://github.com/nextcloud/server/pull/38104))
- El tipo de retorno documentado de `\OCP\Files\FileInfo::getOwner` ahora es anulable, para coincidir con lo que la implementación ya devolvía ([nextcloud/server#36836](https://github.com/nextcloud/server/pull/36836))
- Los tipos de retorno documentados de `\OCP\Files\File::fopen` y `\OCP\Files\SimpleFS\ISimpleFile::read` ahora son anulables, para coincidir con lo que las implementaciones ya devolvían ([nextcloud/server#36836](https://github.com/nextcloud/server/pull/36836))
- `\OCP\Files\File::getContent` ahora también puede lanzar una `GenericFileException` en los casos en que antes devolvía false (aunque estaba documentado que siempre devolvía una cadena, lo que ahora debería cumplirse - [nextcloud/server#37943](https://github.com/nextcloud/server/pull/37943)).

#### API obsoletas

- `\OCP\AppFramework\Utility\ITimeFactory::getTime()` y `\OCP\AppFramework\Utility\ITimeFactory::getDateTime()` quedaron obsoletos porque la interfaz ahora es un `\PSR\Clock\ClockInterface` que sigue el [estándar PSR-20](https://www.php-fig.org/psr/psr-20/#21-clockinterface). ([nextcloud/server#35872](https://github.com/nextcloud/server/pull/35872))
- `\OCP\GroupInterface::usersInGroup()` está obsoleto en favor de la nueva interfaz `\OCP\Group\Backend\ISearchableGroupBackend`. ([nextcloud/server#32866](https://github.com/nextcloud/server/pull/32866))
- En `\OC_App`, los siguientes métodos están obsoletos: `isAppLoaded`, `loadApp`, `isType`. Usar en su lugar los nuevos métodos de `\OCP\App\IAppManager` ([nextcloud/server#36591](https://github.com/nextcloud/server/pull/36591)).

#### API eliminadas

- Se eliminaron las clases de eventos de transición intermedia `\OCP\WorkflowEngine\IEntityCompat` y `\OCP\WorkflowEngine\IOperationCompat`, como se había anunciado para 2023 ([nextcloud/server#37040](https://github.com/nextcloud/server/pull/37040))

#### Cambios de comportamiento

- `\OCP\Files\Cache\CacheEntryRemovedEvent` ahora se despachará para todos los archivos y carpetas dentro del nodo eliminado. ([nextcloud/server#34773](https://github.com/nextcloud/server/pull/34773))
- `\OCP\AppFramework\Db\IMapperException` ahora implementa `\Throwable`; antes había que capturar explícitamente `\OCP\AppFramework\Db\DoesNotExistException` o `\OCP\AppFramework\Db\MultipleObjectsReturnedException`. ([nextcloud/server#37324](https://github.com/nextcloud/server/pull/37324))

### API de cliente

#### API modificadas

- Las solicitudes HTTP que no superan la *comprobación de cookies lax y strict* ahora devuelven siempre un estado HTTP 412. Antes era HTTP 412 o 503, según el endpoint. ([nextcloud/server#37316](https://github.com/nextcloud/server/pull/37316))
- La API de traducción de OCS se amplió para devolver el atributo de idioma `from`, de modo que, si no se indicó ningún idioma de origen, los clientes puedan mostrar después en la interfaz qué idioma se detectó y se usó para traducir. ([nextcloud/server#38003](https://github.com/nextcloud/server/pull/38003))
````
