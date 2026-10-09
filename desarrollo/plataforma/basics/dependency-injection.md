---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "La inyección de dependencias en el App Framework: el patrón, el contenedor, el ensamblado automático, los servicios del núcleo y los servicios opcionales."
---
# Contenedores / Inyección de dependencias

## Resumen

Esta página explica el patrón de inyección de dependencias y cómo lo aplica el contenedor del App Framework: la inyección en constructores y en métodos de controlador, el registro manual de servicios, el ensamblado automático (auto-wiring), los servicios predefinidos del núcleo y los servicios opcionales. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/dependency_injection.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Introducción

Las aplicaciones de software modernas se componen de varios componentes que necesitan interactuar entre sí. Tradicionalmente, los objetos crean internamente sus propias dependencias, lo que genera un acoplamiento fuerte y hace que el código sea más difícil de probar, mantener y extender. La [inyección de dependencias (DI)](https://en.wikipedia.org/wiki/Dependency_injection) es un patrón de diseño de software que ayuda a resolver este problema haciendo que las dependencias se proporcionen desde fuera, en lugar de construirse dentro del propio objeto.

La inyección de dependencias puede sonar a un gran concepto, pero en realidad se trata solo de hacer que el código sea más fácil de manejar y más flexible. En lugar de que cada parte de la app cree por sí misma lo que necesita, esas «dependencias» se le entregan, normalmente mediante un asistente especial llamado contenedor. Esto significa que las clases no necesitan saber cómo crear a sus colaboradores; solo necesitan saber cómo usarlos.

El App Framework de Nextcloud ensambla las aplicaciones mediante un contenedor basado en este patrón de diseño. Este enfoque da lugar a un código más modular, fácil de probar y de mantener.

Usar la inyección de dependencias es algo más que un código elegante. Cuando todas las apps siguen este patrón:

- Es más fácil probar y actualizar tanto las apps como el servidor, ya que las dependencias pueden sustituirse o simularse.
- Las apps se mantienen desacopladas de los detalles internos del servidor, lo que hace más seguro que Nextcloud evolucione sin romper la app.
- Funciones del núcleo como el ensamblado automático (autowiring), el descubrimiento de servicios y las nuevas API quedan disponibles para todas las apps sin código repetitivo adicional.
- Se puede reducir el uso de memoria y de recursos.
- Los nuevos servicios o API se vuelven más fáciles de adoptar a medida que Nextcloud evoluciona.

Al compartir un enfoque coherente para construir y conectar las dependencias, todos (tanto quienes desarrollan el núcleo como quienes desarrollan apps) se benefician de una plataforma más robusta, segura y preparada para el futuro.

Si no se conoce el patrón de diseño DI, no hay de qué preocuparse: se usa ampliamente en los frameworks modernos y pronto resultará familiar. También se puede ver la siguiente introducción en video:

* [Google Clean Code Talks](https://www.youtube.com/watch?v=RlfLCWKxHJ0)

(nc-dev-dependency-injection)=
### Patrón básico de la inyección de dependencias

La esencia de la inyección de dependencias es: **no instanciar las dependencias directamente dentro de las clases o los métodos, sino pasarlas como parámetros**. Esto permite sustituir las dependencias (por ejemplo, por simulaciones en las pruebas unitarias), hace explícitas las dependencias y centraliza la lógica de creación de objetos.

Por ejemplo, considérese el siguiente patrón:

```php
/**
 * Without dependency injection:
 */

use OCP\IDBConnection;

class AuthorMapper {

  // Define a property to store the dependency
  private IDBConnection $db;

  public function __construct() {
    // The dependency is instantiated within the class
    $this->db = new Db();
  }
}
```

Con la inyección de dependencias, en cambio, la dependencia se solicitaría como parte de los parámetros del constructor:

```php
/**
 * Using dependency injection:
 */

use OCP\IDBConnection;

class AuthorMapper {

  // Define a property to store the dependency
  private IDBConnection $db;

  // The dependency is passed in from outside (typically by the container)
  public function __construct(IDBConnection $db) {
    // Assigned to the property
    $this->db = $db;
  }
}
```

O, de forma más concisa, usando la promoción de propiedades en el constructor (disponible en las versiones actuales de PHP). Lo siguiente es exactamente equivalente:

```php
/**
 * Using dependency injection with constructor property promotion:
 */

use OCP\IDBConnection;

class AuthorMapper {

  /**
   * Constructor property promotion with DI reduces boilerplate code by
   * handling everything within the constructor parameters. The example below
   * does exactly the same thing as the prior example, but in less code:
   *
   * - The dependency is passed in from outside (by the container)
   * - The private property is established to store the dependency
   * - The dependency is assigned directly to that property
   */
  public function __construct(private IDBConnection $db) {
  }
}
```

### Ventajas

- **Facilidad de prueba:** se pueden inyectar objetos simulados para las pruebas unitarias.
- **Mantenibilidad:** cambiar cómo se construye una dependencia (en el contenedor) la actualiza en todos los lugares de la aplicación donde se inyecta.
- **Explicitud:** las dependencias quedan listadas claramente en los constructores o en las firmas de los métodos, lo que mejora la legibilidad y la mantenibilidad.

### Inyección en controladores

En los controladores, Nextcloud permite inyectar las dependencias también directamente en métodos individuales, no solo en los constructores. Esto se denomina *inyección en métodos* y permite especificar las dependencias solo donde se necesitan, lo que puede reducir el uso de recursos de servicios que se requieren rara vez.

**Archivo {file}`lib/Controller/ApiController.php`**:

```php
<?php

namespace OCA\MyApp\Controller;

use OCA\MyApp\Service\BarService;
use OCA\MyApp\Service\FooService;
use OCP\AppFramework\Controller;
use OCP\IRequest;

class ApiController extends Controller {
    public function __construct(string $appName, IRequest $request) {
        parent::__construct($appName, $request);
    }

    public function foo(FooService $service) {
        $service->foo();
    }

    public function bar(BarService $service) {
        $service->bar();
    }
}
```

### Usar un contenedor

:::{note}
Usar la inyección de dependencias automática (ver más abajo). En la mayoría de las apps no es necesario registrar servicios manualmente.
:::

Pasar las dependencias al constructor en lugar de instanciarlas en él tiene el siguiente inconveniente: cada línea del código fuente donde se use **new AuthorMapper** debe cambiarse en cuanto se le agrega un nuevo argumento al constructor.

La solución a este problema concreto es limitar el **new AuthorMapper** a un solo archivo: el contenedor. El contenedor contiene todas las fábricas para crear estos objetos y se configura en {file}`lib/AppInfo/Application.php`.

Nextcloud 20 y posteriores usan el {nc-ref}`estándar PSR-11 <psr11>` para la interfaz del contenedor, así que trabajar con el contenedor puede resultar familiar a quien haya trabajado antes con otras aplicaciones PHP que también siguen esa convención.

Para agregar las clases de la app, basta con abrir {file}`lib/AppInfo/Application.php` y usar el método **IRegistrationContext::registerService**:

```php
<?php

namespace OCA\MyApp\AppInfo;

use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IRegistrationContext;
use OCP\IDBConnection;
use OCP\IRequest;
use OCA\MyApp\Controller\AuthorController;
use OCA\MyApp\Service\AuthorService;
use OCA\MyApp\Db\AuthorMapper;
use Psr\Container\ContainerInterface;

class Application extends App implements IBootstrap {

  public function __construct(array $urlParams = []){
    parent::__construct('myapp', $urlParams);
  }

  public boot(IBootContext $context): void {
    // ...
  }

  /**
   * Define your dependencies in here
   */
  public function register(IRegistrationContext $context): void {
    /**
     * Controllers
     */
    $context->registerService(AuthorController::class, function(ContainerInterface $c): AuthorController {
      return new AuthorController(
        $c->get('appName'),
        $c->get(IRequest::class),
        $c->get(AuthorService::class)
      );
    });

    /**
     * Services
     */
    $context->registerService(AuthorService::class, function(ContainerInterface $c): AuthorService {
      return new AuthorService(
        $c->get(AuthorMapper::class)
      );
    });

    /**
     * Mappers
     */
    $context->registerService(AuthorMapper::class, function(ContainerInterface $c): AuthorMapper {
      return new AuthorMapper(
        $c->get(IDBConnection::class)
      );
    });
  }
}
```

### Cómo funciona el contenedor

El contenedor funciona de la siguiente manera:

* {nc-doc}`Llega una solicitud y se compara con una ruta <developer_manual/basics/routing>` (en este caso, la de AuthorController)
* La ruta coincidente consulta al contenedor el servicio **AuthorController**:

  ```
  return new AuthorController(
    $c->get('appName'),
    $c->get(IRequest::class),
    $c->get(AuthorService::class)
  );
  ```

* El **appName** se consulta y lo devuelve la clase base
* El **Request** se consulta y lo devuelve el contenedor del servidor
* Se consulta **AuthorService**. Esto activa el Callable registrado:

  ```
  $container->registerService(AuthorService::class, function(ContainerInterface $c): AuthorService {
    return new AuthorService(
      $c->get(AuthorMapper::class)
    );
  });
  ```

* Se consulta **AuthorMapper**:

  ```
  $container->registerService(AuthorMapper::class, function(ContainerInterface $c): AuthorMapper {
    return new AuthorMapper(
      $c->get(IDBConnection::class)
    );
  });
  ```

* La **conexión a la base de datos** la devuelve el contenedor del servidor
* Ahora **AuthorMapper** tiene todas sus dependencias y el código de DI puede construirlo. Se devuelve el objeto.
* **AuthorService** recibe el **AuthorMapper**, se construye y devuelve el objeto
* **AuthorController** recibe el **AuthorService** y, por fin, el controlador puede instanciarse y se devuelve el objeto

Así que, básicamente, el contenedor se usa como una fábrica gigante para construir todas las clases que la aplicación necesita. Como centraliza toda la creación de objetos (las líneas **new Class()**), es muy fácil agregar nuevos parámetros al constructor sin romper el código existente: solo hay que cambiar el método **__construct** y la línea del contenedor donde se llama a **new**.

### Usar el ensamblado automático de dependencias (recomendado)

En Nextcloud es posible construir clases y sus dependencias sin tener que registrarlas explícitamente en el contenedor, siempre que el contenedor pueda [inspeccionar por reflexión](https://www.php.net/manual/en/book.reflection.php) el constructor y buscar los parámetros por su tipo. Este concepto se conoce ampliamente como *auto-wiring*.

#### Cómo funciona el auto-wiring

El ensamblado automático crea nuevas instancias de clases con solo mirar el nombre de la clase y los parámetros de su constructor. Para cada parámetro del constructor se usa el tipo o el nombre del argumento para consultar el contenedor, p. ej.:

* **SomeType $type** usará **$container->get(SomeType::class)**
* **$variable** usará **$container->get('variable')**

Si se resuelven todos los parámetros del constructor, la clase se crea, se guarda como servicio y se devuelve.

Así que, básicamente, ahora es posible lo siguiente:

```php
<?php
namespace OCA\MyApp;

class MyTestClass {}

class MyTestClass2 {
    public MyTestClass $class;
    public string $appName;

    public function __construct(MyTestClass $class, string $appName) {
        $this->class = $class;
        $this->appName = $appName;
    }
}

$app = new \OCP\AppFramework\App('myapp');

$class2 = $app->getContainer()->get(MyTestClass2::class);

$class2 instanceof MyTestClass2;  // true
$class2->class instanceof MyTestClass;  // true
$class2->appName === 'myname';  // true
$class2 === $app->getContainer()->get(MyTestClass2::class);  // true
```

:::{note}
$appName se resuelve porque el contenedor registró un parámetro con la clave 'appName', que devuelve el id de la app.
:::

#### Cómo afecta al ciclo de vida de la solicitud

* Llega una solicitud
* Se cargan los archivos **routes.php** de todas las apps

  * Si un archivo **routes.php** devuelve un array y existe un **appname/lib/AppInfo/Application.php**, se incluye, se crea una nueva instancia de **\OCA\AppName\AppInfo\Application.php** y se registran las rutas en ella. Así se puede usar un contenedor y, a la vez, aprovechar el nuevo comportamiento de las rutas
  * Si un archivo **routes.php** devuelve un array, pero no hay un **appname/lib/AppInfo/Application.php**, se crea una nueva instancia de \OCP\AppFramework\App con el id de la app y se registran las rutas en ella

* Se compara la solicitud con la ruta, p. ej., con el nombre **page#index**
* Se consulta al contenedor correspondiente la entrada PageController (para mantener la compatibilidad con versiones anteriores)
* Si la entrada no existe, se consulta al contenedor por OCA\AppName\Controller\PageController y, si no existe ninguna entrada, el contenedor intenta crear la clase usando [reflexión][reflection] sobre los parámetros de su constructor

#### Cómo afecta a los controladores

Lo único que ahora hay que hacer para agregar una ruta y un método de controlador es:

**myapp/appinfo/routes.php**

```php
<?php
return ['routes' => [
    ['name' => 'page#index', 'url' => '/', 'verb' => 'GET'],
]];
```

**myapp/appinfo/lib/Controller/PageController.php**

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\IRequest;

class PageController {
    public function __construct($appName, IRequest $request) {
        parent::__construct($appName, $request);
    }

    public function index() {
        // your code here
    }
}
```

No hace falta conectar nada en **lib/AppInfo/Application.php**. Todo se hará automáticamente.

#### Cómo tratar los parámetros de tipo interfaz y de tipo primitivo

Las interfaces y los tipos primitivos no se pueden instanciar, así que el contenedor no puede ensamblarlos automáticamente. La implementación real debe conectarse en el contenedor:

```php
<?php

namespace OCA\MyApp\AppInfo;

use OCA\MyApp\Db\AuthorMapper;
use OCA\MyApp\Db\IAuthorMapper;

use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IRegistrationContext;
use Psr\Container\ContainerInterface;

class Application extends App implements IBootstrap {

    public function __construct(array $urlParams = []){
        parent::__construct('myapp', $urlParams);
    }

    public boot(IBootContext $context): void {
        // ...
    }

    /**
     * Define your dependencies in here
     */
    public function register(IRegistrationContext $context): void {
        // AuthorMapper requires a location as string called $TableName
        $context->registerParameter('TableName', 'my_app_table');

        // the interface is called IAuthorMapper and AuthorMapper implements it
        $context->registerService(IAuthorMapper::class, function (ContainerInterface $c): AuthorMapper {
            return $c->get(AuthorMapper::class);
        });

        // Less verbose alternative
        $context->registerServiceAlias(IAuthorMapper::class, AuthorMapper::class);
    }

}
```

#### Servicios predefinidos del núcleo

Los siguientes nombres de parámetros e indicaciones de tipo pueden usarse para inyectar servicios del núcleo en lugar de usar **$container->getServer()->getServiceX()**

Parámetros:

* **appName**: el id de la app
* **userId**: el id del usuario actual
* **webRoot**: la ruta de la instalación de Nextcloud

Alias:

* **AppName**: se resuelve como `appName` (obsoleto)
* **Request**: se resuelve como `\OCP\IRequest`
* **ServerContainer**: se resuelve como `\OCP\IServerContainer` (obsoleto)
* **UserId**: se resuelve como `userId` (obsoleto)
* **WebRoot**: se resuelve como `webRoot` (obsoleto)

Tipos:

* `\OCP\IAppConfig`
* `\OCP\IAppManager`
* `\OCP\IAvatarManager`
* `\OCP\Activity\IManager`
* `\OCP\ICache`
* `\OCP\ICacheFactory`
* `\OCP\IConfig`
* `\OCP\AppFramework\Utility\IControllerMethodReflector`
* `\OCP\Contacts\IManager`
* `\OCP\IDateTimeZone`
* `\OCP\IDBConnection`
* `\OCP\Diagnostics\IEventLogger`
* `\OCP\Diagnostics\IQueryLogger`
* `\OCP\Files\Config\IMountProviderCollection`
* `\OCP\Files\IRootFolder`
* `\OCP\IGroupManager`
* `\OCP\IL10N`
* `\OCP\BackgroundJob\IJobList`
* `\OCP\INavigationManager`
* `\OCP\IPreview`
* `\OCP\IRequest`
* `\OCP\AppFramework\Utility\ITimeFactory`
* `\OCP\ITagManager`
* `\OCP\ITempManager`
* `\OCP\Route\IRouter`
* `\OCP\ISearch`
* `\OCP\Security\ICrypto`
* `\OCP\Security\IHasher`
* `\OCP\Security\ISecureRandom`
* `\OCP\IURLGenerator`
* `\OCP\IUserManager`
* `\OCP\IUserSession`
* `\Psr\Container\ContainerInterface`
* `\Psr\Log\LoggerInterface`

#### Cómo activarlo

Para aprovechar esta nueva función hay que hacer lo siguiente:

* **appinfo/info.xml** debe proporcionar otro campo llamado **namespace**, donde se define el espacio de nombres de la app. El espacio de nombres requerido es el que va después del espacio de nombres de nivel superior **OCA\\**; p. ej., para **OCA\MyBeautifulApp\Some\OtherClass** el espacio de nombres necesario sería **MyBeautifulApp** y se agregaría al info.xml de la siguiente manera:

  ```xml
  <?xml version="1.0"?>
  <info>
     <namespace>MyBeautifulApp</namespace>
     <!-- other options here ... -->
  </info>
  ```

* **appinfo/routes.php**: en lugar de crear una nueva instancia de la clase Application, basta con devolver el array de rutas así:

  ```php
  <?php
  return ['routes' => [
      ['name' => 'page#index', 'url' => '/', 'verb' => 'GET'],
  ]];
  ```

:::{note}
Se requiere una etiqueta namespace porque el espacio de nombres no se puede deducir a partir del id de la app
:::

### Qué clases deberían agregarse

En general, todos los controladores de la app deben registrarse dentro del contenedor. Entonces surge la siguiente pregunta: ¿qué va en el constructor del controlador? Se pasa al constructor del controlador todo lo que cumpla uno de los siguientes criterios:

* Hace E/S (base de datos, escritura o lectura de archivos)
* Es una variable global (p. ej., $_POST, etc. Esto, por cierto, está en la clase de la solicitud)
* La salida no depende de las variables de entrada (lo que también se llama [función impura](https://en.wikipedia.org/wiki/Pure_function)), p. ej., la hora o un generador de números aleatorios
* Es un servicio; básicamente, tendría sentido sustituirlo por otro objeto

Qué no inyectar:

* Es un dato puro y tiene métodos que solo actúan sobre él (arrays, objetos de datos)
* Es una [función pura](https://en.wikipedia.org/wiki/Pure_function)

### Servicios opcionales

:::{versionadded} 28
:::

Si una dependencia inyectada no se puede encontrar o construir, se lanza una excepción. Esto puede evitarse usando la notación de tipo anulable para la dependencia:

```php
namespace OCA\MyApp\MyService;

use Some\Service;

class MyService {
  public function __construct(private ?Service $service) {
  }
}
```

Si `\Some\Service` existe y puede construirse, se inyectará. Si no, `MyService` recibirá `null`.

### Acceder al contenedor desde cualquier lugar

A veces puede ser difícil inyectar algún servicio dentro de código heredado; en esos casos se puede usar {code}`OCP\Server::get(MyService::class)`. Esto solo debe usarse como último recurso, ya que hace que el código sea más complicado de probar con pruebas unitarias y se considera un antipatrón.

[reflection]: https://www.php.net/manual/en/book.reflection.php
````
