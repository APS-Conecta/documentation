---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API UserConfig para las preferencias de los usuarios: valores tipados, sensibles, indexados y diferidos, y los métodos para guardar, leer, gestionar y buscar."
---
# UserConfig

## Resumen

Esta página describe la API UserConfig, con la que una app almacena y lee los valores de configuración de los usuarios: valores tipados, sensibles, indexados y de carga diferida, y los métodos para guardarlos, leerlos, gestionarlos y buscarlos. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/config/userconfig.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 31
:::

Desde la v31, Nextcloud incluye una nueva API para gestionar las preferencias de los usuarios.

### Visión general de los conceptos

Nextcloud incluye una API para almacenar los valores de configuración de los usuarios y acceder a ellos.
Además de almacenar los valores de configuración y acceder a ellos, `IUserConfig` incorpora distintos conceptos:

(nc-dev-userconfig_concepts)=
:::{note}
Consultar los {nc-ref}`Conceptos del Lexicon <concept-overview>` para saber más sobre **Lexicon**, una forma de definir por completo las claves de configuración y evitar conflictos al usarlas en el código.
:::

#### Valores de configuración tipados

Para garantizar una mayor estabilidad del código, se impone el tipo de los valores de configuración.
El tipo se establece una sola vez, al crearse en la base de datos, y no se puede cambiar.

:::{note}
- Los valores almacenados antes de Nextcloud 31 se tipan automáticamente como *mixed*. Sin embargo, no es posible establecer manualmente un valor como *mixed*.
- Los valores no establecidos como *mixed* deben recuperarse con el método correspondiente.
:::

#### Sensibilidad de los valores

Al almacenar un nuevo valor de configuración, se puede establecer como *sensitive*.
Los valores de configuración establecidos como *sensitive* se ocultan de los informes del sistema y se almacenan cifrados en la base de datos.

```php
setValueString(
    'user',
    'myapp',
    'mykey',
    'myvalue',
    flags: IUserConfig::FLAG_SENSITIVE
);
```

:::{note}
Una vez establecido como *sensitive*, solo se puede revertir con `updateSensitive()`/`updateGlobalSensitive()`
:::

#### Valores indexados

Si se prevé una búsqueda por valor de configuración, este se puede establecer como *indexed*.

```php
setValueString(
    'user',
    'myapp',
    'mykey',
    'myvalue',
    flags: IUserConfig::FLAG_INDEXED
);
```

:::{note}
Los valores de configuración establecidos como *indexed* se almacenan en un campo indexado de la base de datos, con una longitud limitada a 64 caracteres.
:::

#### Carga diferida

Para aligerar la carga de la configuración de los usuarios, existe la posibilidad de establecer valores de configuración como *lazy*.
Todos los valores de configuración *lazy* se cargan desde la base de datos en cuanto se lee uno.

```php
setValueString(
    'user',
    'myapp',
    'mykey',
    'myvalue',
    lazy: true
);
```

:::{note}
- Marcar como *lazy* tantas entradas de tipo «bloque grande de texto» (json, pares de claves, ...) como sea posible,
- marcar como *lazy* las entradas que se necesitan en endpoints poco concurridos,
- **no** marcar como *lazy* partes del código que podrían llamarse durante la carga global de todas las páginas.
:::

Para recuperar el valor de configuración habrá que especificar que está almacenado como *lazy*.

```php
getValueString(
    'user',
    'myapp',
    'mykey',
    'default',
    lazy: true
);
```

### Consumir la API UserConfig

Para consumir la API, primero hay que {nc-ref}`inyectar <dependency-injection>` `\OCP\Config\IUserConfig`

#### Almacenar un valor de configuración

La API proporciona varios métodos para almacenar un valor de configuración, según su tipo.
El comportamiento general de cada uno de esos métodos es llamarlos con:

- ID de usuario (string)
- ID de app (string),
- clave de configuración (string),
- valor de configuración,
- indicador de carga diferida (booleano),
- indicadores (int)

El booleano devuelto será true si fue necesaria una actualización de la base de datos.

- `setValueString(string $userId, string $app, string $key, string $value, bool $lazy, int $flags)`
- `setValueInt(string $userId, string $app, string $key, int $value, bool $lazy, int $flags)`
- `setValueFloat(string $userId, string $app, string $key, float $value, bool $lazy, int $flags)`
- `setValueBool(string $userId, string $app, string $key, bool $value, bool $lazy, int $flags)`
- `setValueArray(string $userId, string $app, string $key, array $value, bool $lazy, int $flags)`

#### Recuperar un valor de configuración

Los valores de configuración se deben recuperar con uno de los métodos de retorno tipado de la lista:

- `getValueString(string $userId, string $app, string $key, string $default, bool $lazy)`
- `getValueInt(string $userId, string $app, string $key, int $default, bool $lazy)`
- `getValueFloat(string $userId, string $app, string $key, float $default, bool $lazy)`
- `getValueBool(string $userId, string $app, string $key, bool $default, bool $lazy)`
- `getValueArray(string $userId, string $app, string $key, array $default, bool $lazy)`

#### Gestionar las claves de configuración

- `getUserIds(string $appId)` devuelve la lista de usuarios con valores de configuración almacenados para una app
- `getApps(string $userId)` devuelve la lista de apps con valores de configuración almacenados para un usuario
- `getKeys(string $userId, string $app)` devuelve la lista de claves de configuración almacenadas para un usuario y una app
- `hasKey(string $userId, string $app, string $key, ?bool $lazy)` devuelve TRUE si se encuentra la clave
- `isSensitive(string $userId, string $app, string $key, ?bool $lazy)` devuelve TRUE si el valor está establecido como *sensitive*
- `isIndexed(string $userId, string $app, string $key, ?bool $lazy)` devuelve TRUE si el valor está establecido como *indexed*
- `isLazy(string $userId, string $app, string $key)` devuelve TRUE si el valor está establecido como *lazy*
- `updateSensitive(string $userId, string $app, string $key, bool $sensitive)` actualiza el estado *sensitive* de un valor de configuración para un usuario concreto
- `updateGlobalSensitive(string $app, string $key, bool $sensitive)` actualiza el estado *sensitive* de un valor de configuración para todos los usuarios
- `updateIndexed(string $userId, string $app, string $key, bool $sensitive)` actualiza el estado *indexed* de un valor de configuración para un usuario concreto
- `updateGlobalIndexed(string $app, string $key, bool $sensitive)` actualiza el estado *indexed* de un valor de configuración para todos los usuarios
- `updateLazy(string $userId, string $app, string $key, bool $lazy)` actualiza el estado *lazy* de un valor de configuración para un usuario concreto
- `updateGlobalLazy(string $app, string $key, bool $lazy)` actualiza el estado *lazy* de un valor de configuración para todos los usuarios
- `getValueType(string $userId, string $app, string $key, bool $lazy)` devuelve la máscara de bits que define el tipo de un valor de configuración
- `getValueFlags(string $userId, string $app, string $key, bool $lazy)` devuelve la máscara de bits que define los indicadores de un valor de configuración
- `deleteUserConfig(string $userId, string $app, string $key)` elimina una clave de configuración y su valor para un usuario
- `deleteAllUserConfig(string $userId)` elimina todos los valores de configuración de un único usuario
- `deleteKey(string $app, string $key)` elimina una clave de configuración y su valor para todos los usuarios
- `deleteKey(string $app, string $key)` elimina una clave de configuración y su valor para todos los usuarios
- `deleteApp(string $app)` elimina todas las claves de configuración de una app para todos los usuarios

:::{note}
Algunos métodos permiten que `$lazy` sea `null`, lo que significa que la búsqueda se extenderá a todos los valores de configuración, sean *lazy* o no.
:::

#### Varios

La API también proporciona herramientas adicionales para usos más amplios

- `getValues(string $userId, string $app, string $prefix, bool $filtered)` devuelve todos los valores de configuración almacenados. `$filtered` se puede establecer en TRUE para ocultar los valores *sensitive* en el array devuelto
- `getAllValues(string $userId, bool $filtered)` devuelve todos los valores de configuración almacenados. `$filtered` se puede establecer en TRUE para ocultar los valores *sensitive* en el array devuelto
- `getValuesByApps(string $userId, string $key, bool $lazy, ?ValueType $typedAs)` devuelve todos los valores de configuración almacenados por app, según una clave de configuración concreta.
- `getValuesByUsers(string $app, string $key, ?ValueType $typedAs, array $userIds)` devuelve todos los valores de configuración almacenados por usuario, según una clave de configuración concreta.
- `searchUsersByValueString(string $app, string $key, string $value, bool $caseInsensitive)` devuelve la lista de usuarios que tienen una clave de configuración establecida en un valor concreto.
- `searchUsersByValues(string $app, string $key, array $values)` devuelve la lista de usuarios que tienen una clave de configuración establecida en un valor de una lista.
- `searchUsersByValueInt(string $app, string $key, string $value)` devuelve la lista de usuarios que tienen una clave de configuración establecida en un valor concreto.
- `searchUsersByValueBool(string $app, string $key, string $value)` devuelve la lista de usuarios que tienen una clave de configuración establecida en un valor concreto.
- `getDetails(string $userId, string $app, string $key)` obtiene todos los detalles de una clave de configuración.
- `clearCache(string $userId, bool $reload)` vacía la caché interna de un usuario concreto
- `clearCacheAll()` vacía toda la caché interna
````
