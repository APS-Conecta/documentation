---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo una app registra y define comprobaciones de configuración: nombre, categoría, niveles de gravedad del resultado y peticiones HTTP contra el servidor."
---
(nc-dev-setup-checks)=
# Comprobaciones de configuración

## Resumen

Esta página explica cómo una app registra una comprobación de configuración en su arranque y cómo la define: su nombre, su categoría, el resultado con su nivel de gravedad y las peticiones HTTP contra el propio servidor con `CheckServerResponseTrait`. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/setup_checks.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Las comprobaciones de configuración permiten probar funcionalidades específicas del servidor e informar pronto a los administradores de problemas
de configuración, para prevenir problemas en tiempo de ejecución.

Un ejemplo de comprobación de configuración es la prueba de módulos JavaScript, que garantiza que el servidor puede
servir correctamente los archivos `.mjs`, algo necesario para las apps que usan JavaScript moderno en su interfaz de usuario.
Cualquier problema con la configuración se informaría al administrador, ya sea en la interfaz web (ajuste de administración)
o al ejecutar el comando `occ setupchecks`, antes de que un usuario sufra el problema.

### Registrar una comprobación de configuración

Las comprobaciones de configuración se registran dentro del contexto de registro del arranque de la app:

```php
<?php
declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

class Application extends App implements IBootstrap {

    public function register(IRegistrationContext $context): void {
        // Other registration
        $context->registerSetupCheck(JavaScriptModules::class);
    }

    // ...

}
```

### Definir una comprobación de configuración

Definir una comprobación de configuración personalizada se hace simplemente implementando `OCP\SetupCheck\SetupResult`;
en este ejemplo se crea una comprobación que garantiza que la instancia de Nextcloud no se está ejecutando en modo de depuración.

```php
<?php
declare(strict_types=1);

namespace OCA\MyApp\SetupChecks;

use OCP\IConfig;
use OCP\IL10N;
use OCP\SetupCheck\ISetupCheck;
use OCP\SetupCheck\SetupResult;

class DebugModeSetupCheck implements ISetupCheck {
    public function __construct(
        private IL10N $l10n,
        private IConfig $config,
    ) {
    }

    public function getName(): string {
        return $this->l10n->t('Debug mode');
    }

    public function getCategory(): string {
        return 'system';
    }

    public function run(): SetupResult {
        if ($this->config->getSystemValueBool('debug', false)) {
            return SetupResult::warning($this->l10n->t('This instance is running in debug mode. Only enable this for local development and not in production environments.'));
        } else {
            return SetupResult::success($this->l10n->t('Debug mode is disabled.'));
        }
    }
}
```

Primero es necesario proporcionar un nombre, que debe resumir la comprobación y debe proporcionarse como una cadena visible para el usuario y, por lo tanto, traducida.

```php
public function getName(): string {
    // This is user visible and thus should be translated
    return $this->l10n->t('Debug mode');
}
```

Las comprobaciones de configuración se agrupan por categoría; la categoría debe ser una de

- `security`: relacionada con la seguridad de la instancia
- `accounts`: relacionada con las cuentas de usuario
- `system`: relacionada con el estado del sistema
- Categoría personalizada: se fusionará en system. Ejemplos de categorías personalizadas existentes son `network` y `database`.

```php
public function getCategory(): string {
    return 'system';
}
```

La parte más importante es la función `run`.
Esta función debe realizar la prueba e informar del resultado como un `OCP\SetupCheck\SetupResult`.
Los niveles de gravedad disponibles son:

- `SetupResult::success`: la prueba tuvo éxito; no se necesita ninguna acción.
- `SetupResult::info`: no se requiere ninguna acción, pero no se puede garantizar que la comprobación haya pasado (p. ej., falta una condición previa para ejecutar la prueba).
- `SetupResult::warning`: la prueba falló, pero el resultado no es fatal; aun así, se debe advertir de ello al administrador.
- `SetupResult::error`: la prueba falló y alguna funcionalidad no está disponible o podría estar rota.

También es posible agregar un enlace a la documentación para facilitar que los administradores resuelvan el problema.
El enlace simplemente se pasa como segundo parámetro a `SetupResult`.

Además, también es posible usar objetos enriquecidos (`OCP\RichObjectStrings`) para dar formato al mensaje;
en este caso, el tercer parámetro debe contener los parámetros de los objetos enriquecidos.

:::{note}
Tener en cuenta que las comprobaciones de configuración pueden ejecutarse tanto
desde el frontend web como desde la CLI. Es decir, podrían usar archivos `php.ini` distintos.
:::

```php
public function run(): SetupResult {
    if ($this->config->getSystemValueBool('debug', false)) {
        return SetupResult::warning($this->l10n->t('This instance is running in debug mode. Only enable this for local development and not in production environments.'));
    } else {
        return SetupResult::success($this->l10n->t('Debug mode is disabled.'));
    }
}
```

#### Ejecutar peticiones HTTP contra el servidor

Como se mencionó en el ejemplo inicial, a veces es necesario ejecutar peticiones HTTP
en una comprobación de configuración para garantizar que la configuración funciona correctamente.
Para facilitar la escritura de pruebas como esa, se proporciona el trait `CheckServerResponseTrait`.

La función `run` de la comprobación de configuración de módulos JavaScript podría tener este aspecto:

```php
public function run(): SetupResult {
    // This is a real existing file
    $testFile = $this->urlGenerator->linkTo('settings', 'js/esm-test.mjs');

    $noResponse = true;
    foreach ($this->runRequest('HEAD', $testFile) as $response) {
        $noResponse = false;
        if (preg_match('/(text|application)\/javascript/i', $response->getHeader('Content-Type'))) {
            return SetupResult::success();
        }
    }

    if ($noResponse) {
        return SetupResult::warning($this->l10n->t('Unable to run check for JavaScript support.') . "\n" . $this->serverConfigHelp());
    }
    return SetupResult::error($this->l10n->t('Your webserver does not serve `.mjs` files using the JavaScript MIME type. This will break some apps by preventing browsers from executing the JavaScript files.'));
}
```

`runRequest` lo proporciona `CheckServerResponseTrait`; acepta un método de petición HTTP
como primer parámetro (en este ejemplo, `HEAD`) y una URL con una ruta absoluta, es decir,
la ruta completa pero sin host, tal como la proporciona el generador de URL. Una cadena de ejemplo sería `nextcloud/apps/settings/js/esm-test.mjs`.
Internamente, la función solicita esa URL en todas las URL posibles (usando el host actual, los dominios de confianza y la URL de sobrescritura de la CLI)
y luego produce un resultado por cada petición.

`CheckServerResponseTrait::serverConfigHelp` proporciona información sobre
problemas comunes que impiden las peticiones HTTP contra el servidor actual.
Si el método `runRequest` no produce ninguna respuesta, se debe incluir esta información.
````
