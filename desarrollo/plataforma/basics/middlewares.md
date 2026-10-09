---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Qué es un middleware, sus ganchos, cómo escribirlo y registrarlo (también como global), y cómo leer anotaciones de los métodos del controlador."
---
# Middlewares

## Resumen

Esta página explica los middlewares: la lógica que se ejecuta antes y después de cada solicitud, sus ganchos, cómo escribir uno y registrarlo en la clase `Application` o como middleware global, y cómo leer anotaciones personalizadas. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/middlewares.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Un middleware es lógica que se ejecuta antes y después de cada solicitud, y está modelado a partir del [sistema de middleware de Django](https://docs.djangoproject.com/en/dev/topics/http/middleware/). Ofrece los siguientes ganchos:

* `beforeController`: se ejecuta antes de que se ejecute un método del controlador. Permite conectar comprobaciones o lógica adicionales antes de ese método, como, por ejemplo, comprobaciones de seguridad
* `afterException`: se ejecuta cuando el método beforeController o el propio método del controlador lanza una excepción. Se pide a los middlewares, en orden inverso, que gestionen la excepción y devuelvan una respuesta. Si el middleware no puede gestionar la excepción, la vuelve a lanzar
* `afterController`: se ejecuta después de una llamada correcta a un método del controlador y permite manipular un objeto Response. Los middlewares se ejecutan en orden inverso
* `beforeOutput`: se ejecuta después de que el objeto de respuesta se haya renderizado y permite manipular el texto de salida. Los middlewares se ejecutan en orden inverso

Para generar un middleware propio, basta con heredar de la clase Middleware y sobrescribir los métodos que se quieran usar.

```php
<?php

namespace OCA\MyApp\Middleware;

use \OCP\AppFramework\Middleware;


class CensorMiddleware extends Middleware {

    /**
     * this replaces "bad words" with "********" in the output
     */
    public function beforeOutput($controller, $methodName, $output): string {
        return str_replace('bad words', '********', $output);
    }

}
```

El middleware puede registrarse en la clase `Application` de la app:

**Archivo {file}`lib/AppInfo/Application.php`**:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCA\MyApp\Middleware\CensorMiddleware;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;

class Application extends App implements IBootstrap {

    public function __construct() {
        parent::__construct('myapp');
    }

    public function register(IRegistrationContext $context): void {
        $context->registerMiddleware(CensorMiddleware::class);
    }

    public function boot(IBootContext $context): void {}

}
```

(nc-dev-global_middlewares)=
### Middlewares globales

:::{versionadded} 26
:::

De forma predeterminada, un middleware registrado solo intercepta las solicitudes de su propia app. Para que un middleware sea *global* y se active también para el middleware de otras apps, se agrega *true* como segundo argumento de la llamada a `registerMiddleware`:

**Archivo {file}`lib/AppInfo/Application.php`**:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCA\MyApp\Middleware\MonitoringMiddleware;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;

class Application extends App implements IBootstrap {

    public function __construct() {
        parent::__construct('myapp');
    }

    public function register(IRegistrationContext $context): void {
        $context->registerMiddleware(MonitoringMiddleware::class, true);
    }

    public function boot(IBootContext $context): void {}

}
```

### Registro en el contenedor de inyección de dependencias

:::{deprecated} 20
:::

El middleware también puede agregarse con el método **registerMiddleware** del contenedor:

**Archivo {file}`lib/AppInfo/Application.php`**:

```php
<?php

namespace OCA\MyApp\AppInfo;

use OCP\AppFramework\App;
use OCP\IServerContainer;
use OCA\MyApp\Middleware\CensorMiddleware;

class MyApp extends App {

    public function __construct(array $urlParams = []) {
        parent::__construct('myapp', $urlParams);

        $container = $this->getContainer();

        // executed in the order that it is registered
        $container->registerMiddleware(CensorMiddleware::class);
    }
}
```

:::{note}
¡El orden es importante! El middleware que se registra primero se ejecuta primero en el método **beforeController**. Para todos los demás ganchos, el orden se invierte; es decir, si un middleware se registra primero, se ejecuta último.
:::

### Analizar anotaciones

A veces es útil ejecutar código de forma condicional antes o después de un método del controlador. Esto puede hacerse definiendo anotaciones personalizadas. Un ejemplo sería agregar un método de autenticación personalizado o simplemente agregar una cabecera adicional a la respuesta. Para acceder a las anotaciones analizadas, se inyecta la clase **ControllerMethodReflector**:

```php
<?php

namespace OCA\MyApp\Middleware;

use OCP\AppFramework\Middleware;
use OCP\AppFramework\Utility\IControllerMethodReflector;
use OCP\AppFramework\Http\Response;

class HeaderMiddleware extends Middleware {

  private $reflector;

  public function __construct(IControllerMethodReflector $reflector) {
      $this->reflector = $reflector;
  }

  /**
   * Add custom header if @MyHeader is used
   */
  public function afterController($controller, $methodName, Response $response): Response {
      if($this->reflector->hasAnnotation('MyHeader')) {
          $response->addHeader('My-Header', 3);
      }
      return $response;
  }
}
```

:::{note}
Una anotación siempre empieza con una letra mayúscula
:::
````
