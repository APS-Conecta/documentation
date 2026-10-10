---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Lexicon: definir en un solo lugar las claves de configuración de una app, registrarlo, los argumentos de cada entrada, los preajustes y su comando occ."
---
# Lexicon

## Resumen

Esta página describe el Lexicon, que centraliza la definición de las claves de configuración de una app: cómo registrarlo, los argumentos de cada entrada, los valores predeterminados según el preajuste de la instancia y el comando `occ` que muestra sus detalles. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/config/lexicon.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 32
:::

Desde la v32, Nextcloud ofrece una forma de centralizar en un único lugar la definición de las claves y los valores de configuración de una app.

(nc-dev-concept-overview)=
### Visión general de los conceptos

Nextcloud incluye la API `ILexicon` para crear un **Lexicon** de las claves de configuración.
Este Lexicon permite a quienes desarrollan definir las claves de configuración de sus apps, el tipo de su valor y detalles adicionales.

(nc-dev-lexicon_concepts)=
Imponer una configuración única para cada una de las claves de configuración en un único lugar ayuda a evitar que se usen indebidamente.

Los detalles de cada clave de configuración son:

- tipo esperado del valor de configuración,
- un valor predeterminado,
- una descripción de su uso,
- ajuste de carga diferida,
- indicadores que marcan la clave de configuración como sensible o indexable

#### Registrar el Lexicon

El Lexicon se define en una clase local que implementa *\OCP\Config\Lexicon\ILexicon* y se registra desde el `Application.php`:

```php
public function register(IRegistrationContext $context): void {
    $context->registerConfigLexicon(\OCA\MyApp\ConfigLexicon::class);
}
```

Ejemplo del `ConfigLexicon.php` registrado:

```php
use OCP\Config\Lexicon\Entry;
use OCP\Config\Lexicon\ILexicon;
use OCP\Config\Lexicon\Strictness;
use OCP\Config\ValueType;

class Lexicon implements ILexicon {
    public function getStrictness(): Strictness {
        return Strictness::WARNING;
    }

    public function getAppConfigs(): array {
        return [
            new Entry('key1', ValueType::STRING, 'abcde', 'test key', true, IAppConfig::FLAG_SENSITIVE),
            new Entry('key2', ValueType::INT, 12345, 'test key', false)
        ];
    }

    public function getUserConfigs(): array {
        return [
            new Entry('key1', ValueType::STRING, 'abcde', 'test key', true, IUserConfig::FLAG_SENSITIVE),
            new Entry('key2', ValueType::INT, 12345, 'test key', false)
        ];
    }
}
```

Cada uno de los métodos `getUserConfigs()` y `getAppConfigs()` devuelve una lista de `\OCP\Config\Lexicon\Entry`.

`getStrictness()` sirve para definir el comportamiento esperado del proceso cuando encuentra una clave de configuración que no figura en el Lexicon de configuración de la app.
Debe devolver un valor del enum `\OCP\Config\Lexicon\Strictness`.

Valores disponibles:

- `::IGNORE` - no limita el set/get de una clave de configuración desconocida.
- `::NOTICE` - no limita el set/get de una clave de configuración desconocida, pero genera un aviso en los registros.
- `::WARNING` - la clave de configuración desconocida no se establecerá, y get devolverá el valor predeterminado. Se emitirá una advertencia en los registros.
- `::EXCEPTION` - el set/get de una clave de configuración desconocida generará una excepción.

#### Entrada del Lexicon de configuración

Cada clave de configuración se define en un objeto mediante estos argumentos:

```php
new Entry(
    key: 'my_config_key',        // config key
    type: ValueType::STRING,     // expected value type when the code set/get value
    defaultRaw: 'default value', // value to returns if a config value is not available in the database
    definition: 'this is a description of the use for this config key',
    lazy: true,                  // config value is stored as lazy
    flags: FLAG_SENSITIVE,       // value is sensitive and/or indexable, using IAppConfig::FLAG_*, IUserConfig::FLAG_*
    deprecated: false,           // if set to ``true`` will generate a notice entry in the nextcloud logs when called
);
```

:::{note}
Salvo que se establezca en `null`, el valor predeterminado definido en el Lexicon de configuración sobrescribe el valor predeterminado que se usa como argumento al llamar a `getValueString('my_config_key', 'another default value');`
:::

#### Preajuste

Con la 32, Nextcloud incluye una lista de *preajustes* para facilitar la experiencia predeterminada del usuario, según el contexto de la instancia.
La selección de un preajuste es opcional y puede hacerse justo después de la instalación de Nextcloud, y en cualquier momento posterior, con este comando occ:

```bash
$ ./occ config:preset
current preset: NONE
$ ./occ config:preset PRIVATE
current preset: PRIVATE
```

Si se quiere que la app tenga un valor predeterminado distinto según el preajuste seleccionado, hay que generar un Closure como `$defaultRaw` al generar la entrada del Lexicon.
El primer parámetro del Closure es un enum `'\OCP\Config\Lexicon\Preset'` que define el preajuste actual:

```php
new Entry('key3', ValueType::STRING, fn (Preset $p): string => match ($p) {
            Preset::FAMILY => 'family',
            Preset::CLUB, Preset::MEDIUM => 'club+medium',
            default => 'none',
        }),
```

Valores disponibles:

- `::LARGE` - Organización de gran tamaño (> 50k cuentas)
- `::MEDIUM` - Organización de tamaño mediano (> 100 cuentas)
- `::SMALL` - Organización de tamaño pequeño (< 100 cuentas)
- `::SHARED` - Alojamiento compartido
- `::EDUCATION` - Escuela/Universidad
- `::CLUB` - Club/Asociación
- `::FAMILY` - Familia
- `::PRIVATE` - Privado

#### ./occ config:app:get --details

Los detalles del Lexicon se pueden extraer con el comando `occ`

```bash
$ ./occ config:app:get myapp my_config_key --details
  - app: myapp
  - key: my_config_key
  - value: 'a_value'
  - type: string
  - lazy: true
  - description:
  - sensitive: false
```
````
