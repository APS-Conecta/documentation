---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API AppConfig: valores tipados, sensibles y diferidos, la interfaz de AppFramework y los métodos para guardar, leer y gestionar la configuración de una app."
---
(nc-dev-app config)=
# AppConfig

## Resumen

Esta página describe la API AppConfig, con la que una app almacena y lee sus valores de configuración: valores tipados, sensibles y de carga diferida, la interfaz con ámbito de app de AppFramework y los métodos para guardar, leer y gestionar claves. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/config/appconfig.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 29
:::

Nextcloud incluye una API AppConfig para gestionar los valores de configuración de las apps.

### Visión general de los conceptos

Nextcloud proporciona una API para almacenar los valores de configuración de las apps y acceder a ellos.
Además de las operaciones simples de lectura y escritura, `IAppConfig` admite:

- valores tipados,
- carga diferida,
- valores sensibles,
- utilidades para descubrir claves y valores.

(nc-dev-appconfig_concepts)=
:::{note}
Consultar los {nc-ref}`Conceptos del Lexicon <concept-overview>` para saber más sobre **Lexicon**, una forma de definir las claves de configuración y evitar conflictos en el código.
:::

### AppFramework

La API AppConfig también está disponible en AppFramework a través de
`OCP\AppFramework\Services\IAppConfig`.

Todos los métodos de esa interfaz tienen como ámbito la propia app de forma automática, por lo que no
es necesario pasar un ID de app explícitamente.

```php
<?php
namespace OCA\MyApp;

use OCP\AppFramework\Services\IAppConfig;

class MyClass {
    public function __construct(
        private IAppConfig $appConfig,
    ) {}

    public function hasConfig(): bool {
        return $this->appConfig->hasAppKey('mykey');
    }
}
```

Usar `\OCP\IAppConfig` cuando haya que leer o escribir la configuración de ID de app arbitrarios.
Usar `OCP\AppFramework\Services\IAppConfig` para las operaciones con ámbito de app dentro de la propia app.

#### Valores de configuración tipados

Para mejorar la seguridad y la estabilidad, se impone el tipo de los valores de configuración.

El tipo se establece cuando la clave se crea en la base de datos y no se puede cambiar después.

El tipo de una clave lo define el setter que se usa cuando la clave se crea por primera vez
(por ejemplo, `setValueString()` crea una clave de tipo string y `setValueInt()`, una clave de tipo int).

```php
$appConfig->setValueInt('myapp', 'retry_count', 3);       // key type: int
$appConfig->setValueString('myapp', 'display_name', 'A'); // key type: string
```

:::{note}
- Los valores almacenados antes de Nextcloud 29 se tratan como `mixed`.
- No es posible crear manualmente nuevos valores `mixed`.
- Los valores que no son `mixed` deben recuperarse con el getter tipado correspondiente.
:::

:::{note}
La urgencia de la migración difiere entre lecturas y escrituras:

- Las rutas de lectura normalmente deberían migrarse pronto a getters tipados al adoptar
  `IAppConfig`, para que el comportamiento en tiempo de ejecución sea explícito y seguro en cuanto a tipos.
- La normalización de los valores heredados en el lado de la escritura a menudo puede ser incremental y hacerse
  al modificar rutas de código relacionadas, sobre todo si:

  - se quieren garantías de tipado más estrictas,
  - ya se está refactorizando,
  - la clave está causando ambigüedad/errores

Para las claves nuevas, usar siempre setters tipados y getters tipados.

**Un patrón seguro de migración en el lado de la escritura es:**

1. Leer el valor heredado existente.
2. Validarlo/convertirlo en el código de la app.
3. Volver a escribirlo con el setter tipado adecuado (por ejemplo `setValueInt()`,
   `setValueString()`, `setValueBool()`, ...).
4. Después, usar siempre el getter tipado correspondiente.
:::

#### Valores sensibles

Al almacenar un nuevo valor de configuración, se puede marcar como sensible.

Los valores sensibles se ocultan de los listados e informes filtrados y se tratan como valores protegidos
en el almacenamiento de AppConfig.

```php
$appConfig->setValueString(
    'myapp',
    'mykey',
    'myvalue',
    sensitive: true
);
```

:::{note}
Una vez marcado como sensible, esto se puede cambiar más adelante con `updateSensitive()`.
:::

#### Carga diferida

Para reducir el uso de memoria y la sobrecarga del arranque, los valores de configuración pueden marcarse como diferidos.

Los valores no diferidos se cargan primero. Los valores diferidos se cargan solo cuando se necesitan. Cuando se
solicita un valor diferido, los valores diferidos se cargan todos juntos.

```php
$appConfig->setValueString(
    'myapp',
    'mykey',
    'myvalue',
    lazy: true
);
```

Para recuperar un valor diferido hay que usar el modo de lectura diferida:

```php
$appConfig->getValueString(
    'myapp',
    'mykey',
    'default',
    lazy: true
);
```

##### Comportamiento de lectura con el parámetro `lazy`

Al leer valores, el argumento `lazy` determina qué compartimento del almacenamiento se consulta.

| Modo de la clave almacenada | Lectura con `lazy` | Resultado |
|---|---|---|
| no diferida | `false` | valor almacenado |
| no diferida | `true` | valor almacenado |
| diferida | `false` | valor predeterminado (la clave diferida no se busca) |
| diferida | `true` | valor almacenado |

:::{warning}
Si una clave puede ser diferida, leerla con `lazy: true` para no obtener valores predeterminados sin advertirlo.
:::

:::{note}
Algunos métodos de la API ignoran explícitamente el filtrado por carga diferida y pueden cargar todos los valores.
Revisar la descripción de cada método por si incluye advertencias.
:::

##### Cómo elegir qué debe ser diferido

Buenos candidatos para `lazy: true`:

- Valores grandes (por ejemplo, blobs JSON, textos largos, mapas grandes de clave/valor).
- Valores usados solo en flujos concretos (páginas de administración, trabajos en segundo plano, herramientas de configuración inicial/migración).
- Valores que se leen con poca frecuencia o solo después de acciones explícitas del usuario.

Normalmente conviene mantener como no diferidos (`lazy: false`):

- Valores pequeños y de acceso frecuente que se usan en la mayoría de las solicitudes.
- Valores necesarios durante el arranque de la app, el registro, la conexión de capacidades u otras rutas de código tempranas del ciclo de vida.
- Valores usados en rutas de ejecución intensiva (middleware, constructores de servicios comunes, comprobaciones críticas para la solicitud).

Regla práctica:

- Si un valor se necesita en la mayoría de las solicitudes, mantenerlo no diferido.
- Si es grande y solo se necesita de forma ocasional, hacerlo diferido.

### Consumir la API AppConfig

Se puede inyectar cualquiera de las dos interfaces, según el caso de uso:

- `\OCP\IAppConfig` (API global): usarla cuando haya que acceder explícitamente a la configuración
  de uno o varios ID de app.
- `\OCP\AppFramework\Services\IAppConfig` (API de AppFramework con ámbito de app):
  usarla dentro de la app cuando se quiera que los métodos tengan automáticamente como ámbito el ID de la app.

Consultar {nc-ref}`dependency-injection` para los detalles de la inyección.

:::{important}
Salvo que se indique explícitamente lo contrario, los ejemplos de esta página usan la interfaz
global `\OCP\IAppConfig` (con el ID de app pasado explícitamente).

Si se inyecta `\OCP\AppFramework\Services\IAppConfig`, los métodos tienen ámbito de app
y no se pasa el ID de app.
:::

#### Almacenar un valor de configuración

La API proporciona métodos tipados para almacenar valores de configuración.

Los argumentos comunes son:

- ID de app (`string`),
- clave de configuración (`string`),
- valor de configuración (tipado),
- indicador de carga diferida (`bool`),
- indicador de sensible (`bool`, donde se admite).

El valor devuelto es `true` si fue necesaria una actualización de la base de datos.

- `setValueString(string $app, string $key, string $value, bool $lazy = false, bool $sensitive = false)`
- `setValueInt(string $app, string $key, int $value, bool $lazy = false, bool $sensitive = false)`
- `setValueFloat(string $app, string $key, float $value, bool $lazy = false, bool $sensitive = false)`
- `setValueBool(string $app, string $key, bool $value, bool $lazy = false)`
- `setValueArray(string $app, string $key, array $value, bool $lazy = false, bool $sensitive = false)`

Equivalentes de AppFramework (con ámbito de app, sin el argumento `$app`):

```php
$appConfig->setAppValueString('mykey', 'myvalue', lazy: true);
$appConfig->setAppValueInt('retry_count', 3);
$appConfig->setAppValueArray('options', ['a' => true], sensitive: true);
```

#### Recuperar un valor de configuración

Los valores de configuración se pueden recuperar con getters tipados:

- `getValueString(string $app, string $key, string $default = '', bool $lazy = false)`
- `getValueInt(string $app, string $key, int $default = 0, bool $lazy = false)`
- `getValueFloat(string $app, string $key, float $default = 0.0, bool $lazy = false)`
- `getValueBool(string $app, string $key, bool $default = false, bool $lazy = false)`
- `getValueArray(string $app, string $key, array $default = [], bool $lazy = false)`

Equivalentes de AppFramework (con ámbito de app, sin el argumento `$app`):

```php
$name = $appConfig->getAppValueString('display_name', 'default');
$count = $appConfig->getAppValueInt('retry_count', 0);
$enabled = $appConfig->getAppValueBool('enabled', false, lazy: true);
```

#### Gestionar las claves de configuración

- `getApps()` devuelve los ID de las apps que tienen valores de configuración almacenados.
- `getKeys(string $app)` devuelve las claves almacenadas de una app.
- `searchKeys(string $app, string $prefix = '', bool $lazy = false)` devuelve las claves de una app que coinciden con un prefijo.
- `hasKey(string $app, string $key, ?bool $lazy = false)` devuelve `true` si la clave existe.
- `isSensitive(string $app, string $key, ?bool $lazy = false)` devuelve `true` si el valor es sensible.
- `isLazy(string $app, string $key)` devuelve `true` si el valor es diferido.
- `updateSensitive(string $app, string $key, bool $sensitive)` actualiza el estado de sensible.
- `updateLazy(string $app, string $key, bool $lazy)` actualiza el estado de diferido.
- `getValueType(string $app, string $key)` devuelve la máscara de bits del tipo de un valor.
- `deleteKey(string $app, string $key)` elimina una clave y su valor.
- `deleteApp(string $app)` elimina todas las claves de una app.

Entre los equivalentes de AppFramework están:

- `getAppKeys()`
- `hasAppKey(string $key, ?bool $lazy = false)`
- `isSensitive(string $key, ?bool $lazy = false)`
- `isLazy(string $key)`

:::{note}
Los métodos con `?bool $lazy` pueden usar `null` para buscar tanto entre los valores diferidos como entre los no diferidos.
:::

#### Varios

La API también proporciona utilidades adicionales:

- `getAllValues(string $app, string $prefix = '', bool $filtered = false)`
  devuelve los valores almacenados de una app. Si `$filtered` es `true`, los valores sensibles se ocultan.
- `searchValues(string $key, bool $lazy = false)`
  busca las apps/valores que contienen la clave especificada.
- `getDetails(string $app, string $key)`
  devuelve metadatos/detalles sobre una clave.
- `convertTypeToInt(string $type)`
  convierte un tipo legible por humanos en una máscara de bits de tipo.
- `convertTypeToString(int $type)`
  convierte una máscara de bits de tipo en un tipo legible por humanos.
- `clearCache(bool $reload = false)`
  vacía la caché interna.

Utilidad equivalente de AppFramework:

- `getAllAppValues(string $key = '', bool $filtered = false)`

#### Constantes e indicadores

`\OCP\IAppConfig` expone constantes de tipo de valor e indicadores, entre ellos:

- `FLAG_SENSITIVE` (desde la 31),
- `FLAG_INTERNAL` (desde la 33; marca los valores como internos y aptos para ocultarse de los listados).
````
