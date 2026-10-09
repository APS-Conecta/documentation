---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "La clase Application de una app, la interfaz IBootstrap y las etapas de registro y arranque con las que una app se engancha al inicio de cada proceso."
---
(nc-dev-bootstrapping)=
# Arranque

## Resumen

Esta página explica el arranque de una app: la clase `Application` como punto de entrada, la interfaz `IBootstrap` y el orden de las etapas de registro y arranque, con ejemplos del método `boot`. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/app_development/bootstrap.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Cada proceso de php tiene una vida relativamente corta, que dura lo mismo que la solicitud HTTP o que la invocación del programa de línea de comandos. Al comienzo de esa vida, Nextcloud inicializa sus servicios. Al mismo tiempo, cualquier app adicional también puede querer registrar sus servicios en Nextcloud. Este suceso se denomina *arranque*, y este capítulo pretende aclarar un poco cómo engancharse a él con una app.

(nc-dev-application-php)=
### La clase Application

La clase *Application* es el punto de entrada principal de una app. Esta clase es opcional, pero muy recomendable si la app necesita registrar algún servicio o ejecutar código en cada solicitud.

Nextcloud intentará cargar automáticamente la clase desde el espacio de nombres `\OCA\<App namespace>\AppInfo\Application`, como `\OCA\MyApp\AppInfo\Application`, donde *MyApp* sería el nombre de la app. Por lo tanto, el archivo estará en `myapp/lib/AppInfo/Application.php`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCP\AppFramework\App;

class Application extends App {

    public function __construct() {
        parent::__construct('myapp');
        \OCP\Util::connectHook('OC_User', 'pre_deleteUser', 'OCA\MyApp\Hooks\User', 'deleteUser');
    }

}
```

La clase **debe** extender `OCP\AppFramework\App` y, de forma opcional, puede implementar `\OCP\AppFramework\Bootstrap\IBootstrap`:

**Archivo {file}`lib/AppInfo/Application.php`**:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCA\MyApp\Listeners\UserDeletedListener;
use OCA\MyApp\Notifications\Notifier;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;
use OCP\Notification\IManager;
use OCP\User\Events;

class Application extends App implements IBootstrap {

    public function __construct() {
        parent::__construct('myapp');
    }

    public function register(IRegistrationContext $context): void {
        // ... registration logic goes here ...

        // Register the composer autoloader for packages shipped by this app, if applicable
        include_once __DIR__ . '/../../vendor/autoload.php';

        $context->registerEventListener(
            BeforeUserDeletedEvent::class,
            UserDeletedListener::class
        );
    }

    public function boot(IBootContext $context): void {
        // ... boot logic goes here ...

        /** @var IManager $manager */
        $manager = $context->getAppContainer()->query(IManager::class);
        $manager->registerNotifierService(Notifier::class);
    }

}
```

Hay que tener en cuenta que los objetos de contexto de los métodos `register` y `boot` tienen interfaces distintas y, por lo tanto, capacidades distintas, adecuadas a su etapa.

### Proceso de arranque

Para dar una mejor visión general de *cuándo* se alcanza cada una de las etapas del arranque y de cómo la app puede interactuar con ellas, esta sección explica los cambios hechos en Nextcloud 20.

#### Nextcloud 20 y posteriores

Nextcloud 20 es la primera versión con la interfaz `\OCP\AppFramework\Bootstrap\IBootstrap`. La clase `Application` de la app puede implementar esta interfaz para indicar que quiere actuar en las etapas del arranque. La principal diferencia entre esto y el proceso anterior es que el arranque no se realiza en secuencia, sino que las apps se registran y arrancan de forma intercalada. Esto debería garantizar que una app que ejecuta su `boot` pueda contar con que el registro de todas las demás apps ya ha terminado.

El proceso general es el siguiente:

1. En cada app instalada y activada que tenga una clase `Application` que además implemente `IBootstrap`, se llamará al método `register`. Este método recibe un argumento de contexto mediante el cual la app puede preparar el contenedor de inyección de dependencias y registrar otros servicios de forma diferida, p. ej., llamando a `$context->registerService(...)`. El énfasis está en la **carga diferida**. En esta etapa tan temprana de la vida del proceso, no están listas ni las demás apps ni todos los componentes del servidor. Por lo tanto, la app **no debe** intentar usar nada excepto la API que ofrece el contexto. Eso debe garantizar que todas las apps puedan ejecutar con seguridad su lógica de registro antes de que se consulte (instancie) cualquier servicio del contenedor de inyección de dependencias o se ejecute código relacionado.
2. Nextcloud cargará antes los grupos de ciertas apps, p. ej., las apps del sistema de archivos o de sesión, y las demás después.
3. Nextcloud consultará (de nuevo) la clase `Application` de la app, implemente o no `IBootstrap`.
4. Nextcloud invocará el método {nc-ref}`boot <app-bootstrap-boot>` de cada instancia de `Application` que implemente `IBootstrap`. En esta etapa se puede dar por hecho que todos los registros mediante `IBootstrap::register` han terminado.

(nc-dev-app-bootstrap-boot)=
##### Arrancar una app

Todo código que deba ejecutarse una vez en cada proceso de Nextcloud va en el método `boot` de la clase `Application` de una app. Este mecanismo debe usarse con cuidado, ya que podría tener un efecto negativo en el rendimiento general de Nextcloud.

**Archivo {file}`lib/AppInfo/Application.php`**:

```php
<?php

class Application extends App implements IBootstrap {

    public function __construct() {
        parent::__construct('myapp');
    }

    public function register(IRegistrationContext $context): void {}

    public function boot(IBootContext $context): void {
        /** @var IFooManager $manager */
        $manager = $context->getAppContainer()->query(IFooManager::class);
        $manager->registerCustomFoo(MyFooImpl::class);
    }

}
```

El código anterior obtiene un *gestor de foo* ficticio para registrar una clase de la app. El objeto de contexto de arranque incluye un asistente `injectFn` que facilita la inyección de dependencias dentro del método `boot`, inyectando los argumentos de un callable:

**Archivo {file}`lib/AppInfo/Application.php`**:

```php
<?php

class Application extends App implements IBootstrap {

    public function __construct() {
        parent::__construct('myapp');
    }

    public function register(IRegistrationContext $context): void {}

    public function boot(IBootContext $context): void {
        $context->injectFn(function(IFooManager $manager) {
            $manager->registerCustomFoo(MyFooImpl::class);
        });
    }

}
```

Con ayuda de `Closure::fromCallable` también se puede delegar en otros métodos que reciben sus argumentos inyectados:

**Archivo {file}`lib/AppInfo/Application.php`**:

```php
<?php

class Application extends App implements IBootstrap {

    public function __construct() {
        parent::__construct('myapp');
    }

    public function register(IRegistrationContext $context): void {}

    public function boot(IBootContext $context): void {
        $context->injectFn($this->registerFoo(...));
    }

    protected function registerFoo(IFooManager $manager): void {
        $manager->registerCustomFoo(MyFooImpl::class);
    }

}
```
````
