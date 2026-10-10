---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo cargar el JavaScript de una app, enviar el token CSRF, generar URL, extender el menú «Nuevo» de Archivos, cargar el estado inicial y respetar los atajos."
---
(nc-dev-applicationjs)=
# JavaScript

## Resumen

Esta página explica cómo inyectar los archivos JavaScript de una app y cómo enviar el token CSRF, generar URL, extender el menú «Nuevo» de la app Archivos, cargar el estado inicial y respetar el ajuste de atajos de teclado. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/front-end/js.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los archivos JavaScript se ubican en la carpeta **js/** y deben incluirse
en el controlador correspondiente. Hay dos métodos para inyectar los archivos JavaScript.

1. `Util::addScript`
2. `Util::addInitScript`

```php
/**
 * Add a javascript file
 *
 * @param string $application Your application ID, e.g. 'your_app'
 * @param string $file Your script name, e.g. 'main'
 * @param string $afterAppId Optional, the script will be loaded after this app
 * @param bool $prepend Optional, if true the script will be prepended to this app scripts list
 */
 public static function addScript(string $application, string $file = null, string $afterAppId = 'core', bool $prepend = false): void

/**
 * Add a standalone init js file that is loaded for initialization.
 * Be careful loading scripts using this method as they are loaded early
 * and block the initial page rendering. They should not have dependencies
 * on any other scripts than core-common and core-main.
 *
 * @param string $application Your application ID, e.g. 'your_app'
 * @param string $file Your script name, e.g. 'main'
 */
 public static function addInitScript(string $application, string $file): void
```

:::{note}
Si el script solo se necesita tras un evento concreto, p. ej., después de que se cargue la app Archivos,
habrá que registrar un listener en el `Appinfo/Application.php` de la app.
:::

Este es un ejemplo para la app Archivos (que emite el `LoadAdditionalScriptsEvent`).
Para más información sobre el arranque de las apps, consultar la sección {nc-ref}`application-php`.

```php
namespace OCA\YourApp\AppInfo;

use OCA\Files\Event\LoadAdditionalScriptsEvent;
use OCA\YourApp\Listener\LoadAdditionalListener;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;

/**
 * @package OCA\YourApp\AppInfo
 */
class Application extends App implements IBackendProvider, IAuthMechanismProvider, IBootstrap {
  public const APP_ID = 'your_app';

  public function __construct(array $urlParams = []) {
    parent::__construct(self::APP_ID, $urlParams);
  }

  public function register(IRegistrationContext $context): void {
    $context->registerEventListener(LoadAdditionalScriptsEvent::class, LoadAdditionalListener::class);
  }

  public function boot(IBootContext $context): void {}
```

```php
namespace OCA\YourApp\Listener;

use OCA\YourApp\AppInfo\Application;
use OCA\Files\Event\LoadAdditionalScriptsEvent;
use OCP\EventDispatcher\Event;
use OCP\EventDispatcher\IEventListener;
use OCP\Util;

class LoadAdditionalListener implements IEventListener {

    public function handle(Event $event): void {
        if (!($event instanceof LoadAdditionalScriptsEvent)) {
            return;
        }

        Util::addInitScript(Application::APP_ID, 'init');
        Util::addScript(Application::APP_ID, 'main', 'files');
    }
}
```

### Enviar el token CSRF

Si se usa una biblioteca de peticiones JavaScript distinta de jQuery, las peticiones deben enviar el token CSRF como una cabecera HTTP llamada **requesttoken**. El token está disponible en la variable global **OC.requestToken**.

Para AngularJS habría que agregar las siguientes líneas:

```js
var app = angular.module('MyApp', []).config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.common.requesttoken = OC.requestToken;
}]);
```

### Generar URL

Para enviar peticiones a Nextcloud se necesita la URL base en la que Nextcloud se está ejecutando en ese momento. Para obtener la URL base se usa:

```js
var baseUrl = OC.generateUrl('');
```

Las URL completas se pueden generar con:

```js
var authorUrl = OC.generateUrl('/apps/myapp/authors/1');
```

### Extender partes del núcleo

Es posible extender componentes de la interfaz web del núcleo. Los siguientes ejemplos
deberían mostrar cómo hacerlo.

#### Extender el menú «Nuevo» de la app Archivos

:::{versionadded} 9.0
:::

```js
var myFileMenuPlugin = {
    attach: function (menu) {
        menu.addMenuEntry({
            id: 'abc',
            displayName: 'Menu display name',
            templateName: 'templateName.ext',
            iconClass: 'icon-filetype-text',
            fileType: 'file',
            actionHandler: function () {
                console.log('do something here');
            }
        });
    }
};
OC.Plugins.register('OCA.Files.NewFileMenu', myFileMenuPlugin);
```

Esto registrará una nueva entrada de menú en el menú «Nuevo» de la app Archivos. El
método `attach()` se llama una vez que el menú está construido. Normalmente esto ocurre justo
después de hacer clic en el botón.

### Cargar el estado inicial

A menudo las apps tienen algún tipo de estado inicial. A menudo, lo primero que hace un script
es consultar un endpoint para obtener ese estado inicial. Esto hace que la experiencia
de usuario no sea óptima, ya que hay que esperar a que termine de cargarse otra petición
más.

Para proporcionar el estado inicial al JavaScript de forma rápida y estandarizada,
Nextcloud ofrece una API. La API consta de una parte en PHP (que suministra el estado)
y una parte en JS (que obtiene y analiza el estado).

#### Proporcionar el estado inicial con PHP

El estado se proporciona en PHP mediante `OCP\AppFramework\Services\IInitialState`. Este servicio
tiene dos métodos que se pueden usar para proporcionar el estado inicial. Su ámbito se limita automáticamente
a la app, así que ya no hace falta proporcionar el ID de la app.

- `provideInitialState(string $key, $data)`:
  Si se sabe con seguridad que el estado se usará. Por ejemplo, en la página de ajustes de la app.
- `provideLazyInitialState(string $key, Closure $closure)`:
  Si se quiere inyectar el estado en una página general. Por ejemplo, el estado inicial de la app de notificaciones. El callback se invocará si y solo si se renderiza una plantilla.

Ambos métodos se llaman con el nombre de la app y una clave. Esto sirve para delimitar
correctamente el ámbito de los estados. Se necesitarán ambos al recuperar el estado inicial en
JavaScript.

Los datos del estado inicial se convierten a JSON. Así que hay que asegurarse de que los
datos que se proporcionan (ya sea en $data o como valor devuelto por $closure) se puedan convertir
a JSON.

#### Obtener el estado inicial en JavaScript

Para obtener el estado inicial en JavaScript solo hay que llamar a una
función

- A la manera de Vue, con [@nextcloud/initial-state](https://github.com/nextcloud/nextcloud-initial-state):

```js
import { loadState } from '@nextcloud/initial-state'

const val = loadState('myapp', 'user_preference')

// Provide a fallback value to return when the state is not found
const valWithFallback = loadState('myapp', 'user_preference', 'no_preference')
```

- A la manera heredada:

```js
const state = OCP.InitialState.loadState('MyApp', 'MyState');
```

Ahora state contendrá el estado proporcionado, que se puede usar como cualquier variable. Así
de sencillo.

(nc-dev-basics_frontend_javascript_keyboard_shortcuts)=
### Atajos de teclado

Si se quiere mejorar la experiencia de usuario con atajos de teclado, hay que asegurarse
de no sobrescribir los atajos del navegador, del sistema operativo ni otros atajos de todo Nextcloud.
Además, existe un ajuste de accesibilidad para que los usuarios renuncien a **cualquier** atajo de teclado
en todo Nextcloud. El ajuste se puede comprobar con la siguiente función, que devuelve un booleano
(disponible en Nextcloud 25 y posteriores):

```js
OCP.Accessibility.disableKeyboardShortcuts();
```

Si es así, ninguna app debe registrar atajos adicionales. Solo `space`
para marcar o desmarcar casillas y `enter` para enviar los botones o enlaces activos en ese momento son aceptables,
ya que cualquier otro atajo podría interferir con los lectores de pantalla y otras herramientas de accesibilidad.
````
