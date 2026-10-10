---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo definir rutas de una app: routes.php y atributos, rutas OCS, valores de la URL, recursos, URLGenerator y los comandos occ router."
---
# Rutas

## Resumen

Esta página explica cómo asociar una URL y un método HTTP a un método de controlador: el archivo `appinfo/routes.php` y los atributos de ruta, las rutas OCS, la extracción de valores de la URL, las sub-URL con requisitos y valores predeterminados, los recursos, el generador de URL y los comandos de consola para inspeccionar las rutas. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/routing.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Las rutas asocian una URL y un método a un método de controlador. Las rutas se definen dentro de {file}`appinfo/routes.php`, devolviéndolas como un array:

```php
<?php
return [
    'routes' => [
        ['name' => 'page#index', 'url' => '/', 'verb' => 'GET'],
    ],
];
```

:::{versionadded} 29
También se pueden usar atributos en el método del controlador para definir rutas.
Admiten todos los mismos parámetros (salvo `name`, que no hace falta).
Se debe usar `FrontpageRoute` para las rutas que estaban en la sección `routes` y `ApiRoute` para las rutas que estaban en la sección `ocs`.
:::

```php
#[FrontpageRoute(verb: 'GET', url: '/')]
```

El array de la ruta contiene las siguientes partes:

* **url**: la URL que se compara después de */index.php/apps/myapp*
* **name**: el controlador y el método que se llaman; *page#index* se asocia a *PageController->index()*, *articles_api#drop_latest* se asociaría a *ArticlesApiController->dropLatest()*. El controlador del ejemplo anterior se guardaría en {file}`lib/Controller/PageController.php`. Este parámetro no hace falta con los atributos.
* **verb** (opcional, GET de forma predeterminada): el método HTTP que debe coincidir (p. ej., GET, POST, PUT, DELETE, HEAD, OPTIONS, PATCH)
* **requirements** (opcional): permite que coincidan y se extraigan URL que contienen barras (ver {nc-ref}`matching-suburls`)
* **postfix** (opcional): permite definir un sufijo para el id de la ruta. Como cada nombre de ruta se transforma en un id de ruta (**page#method** -> **myapp.page.method**) y cada id de ruta solo puede existir una vez, se puede usar la opción postfix para alterar la creación del id de la ruta agregándole una cadena; p. ej., **'name' => 'page#method', 'postfix' => 'test'** producirá el id de ruta **myapp.page.methodtest**. Esto permite agregar más de una ruta o URL para un mismo método de controlador
* **defaults** (opcional): si se indica este ajuste, se asumirá un valor predeterminado para cada parámetro de la URL que no esté presente. Los valores predeterminados se pasan como un array de pares clave => valor

(nc-dev-routes_ocs)=
### Rutas OCS

Registrar rutas OCS exige usar un {nc-ref}`controlador correspondiente <ocscontroller>`.
Además, la ruta debe configurarse como ruta OCS en el enrutador.
Para ello, se usa la clave `ocs` en el archivo `routes.php` en lugar de la clave `routes`.
El resto de la estructura es el mismo.

Por supuesto, se pueden tener a la vez rutas de index.php y rutas OCS.

```php
<?php
return [
    'routes' => [
        ['name' => 'page#index', 'url' => '/', 'verb' => 'GET'],
    ],
    'ocs' => [
        ['name' => 'api#data', 'url' => '/v1/data', 'verb' => 'GET'],
    ],
];
```

El prefijo de las rutas OCS es `/ocs/v2.php/apps/<APPNAME>/`.
Así, la URL configurada para el endpoint OCS del ejemplo sería `<server>/ocs/v2.php/apps/<APPNAME>/v1/data`.

:::{versionadded} 29
De forma similar a `FrontpageRoute`, se puede usar `ApiRoute` como atributo para marcar una ruta directamente en el controlador.

Esto equivale a la configuración del `routes.php` anterior.

```php
// In class ApiController that is a OCSController
#[ApiRoute(verb: 'GET', url: '/v1/data')]
function data() { /* ... */ }
```
:::

### Extraer valores de la URL

Es posible extraer valores de la URL para permitir un diseño de URL RESTful. Para extraer un valor, hay que envolverlo entre llaves:

```php
<?php

// Request: GET /index.php/apps/myapp/authors/3

// appinfo/routes.php
['name' => 'author#show', 'url' => '/authors/{id}', 'verb' => 'GET'],

// controller/authorcontroller.php
class AuthorController {
    public function show(string $id): Response {
        // $id is '3'
    }
}
```

El identificador usado dentro de la ruta se pasa al método del controlador reflejando los parámetros del método. En resumen, si se quiere obtener el valor **{id}** en el método, hay que agregar **$id** a los parámetros del método.

(nc-dev-matching-suburls)=
### Coincidencia de sub-URL

A veces hace falta que coincida más de un fragmento de URL. Un ejemplo sería hacer coincidir una solicitud para todas las URL que empiezan por **OPTIONS /index.php/apps/myapp/api**. Para ello, se usa en la ruta el parámetro **requirements**, que es un array con pares **'key' => 'regex'**:

```php
<?php

// Request: OPTIONS /index.php/apps/myapp/api/my/route

// appinfo/routes.php
array('name' => 'author_api#cors', 'url' => '/api/{path}', 'verb' => 'OPTIONS',
      'requirements' => array('path' => '.+')),

// controller/authorapicontroller.php
class AuthorApiController {
    public function cors(string $path): Response {
        // $path will be 'my/route'
    }
}
```

### Valores predeterminados de una sub-URL

Además de los requisitos de coincidencia, una sub-URL también puede tener un valor predeterminado. Supongamos que se quiere admitir la paginación (un parámetro 'page') en la sub-URL **/posts**, que muestra la lista de publicaciones. Se puede fijar un valor predeterminado para el parámetro 'page', que se usará si la URL no lo indica ya. Se usa en la ruta el parámetro **defaults**, que es un array con pares **'urlparameter' => 'defaultvalue'**:

```php
<?php

// Request: GET /index.php/app/myapp/post

// appinfo/routes.php
array(
    'name'     => 'post#index',
    'url'      => '/post/{page}',
    'verb'     => 'GET',
    'defaults' => array('page' => 1) // this allows same URL as /index.php/myapp/post/1
),

// controller/postcontroller.php
class PostController {
    public function index(int $page = 1): Response {
        // $page will be 1
    }
}
```

### Registrar recursos

Al trabajar con recursos, escribir las rutas puede volverse bastante repetitivo, ya que la mayoría de las veces se necesitan rutas para las siguientes tareas:

* Obtener todas las entradas
* Obtener una entrada por id
* Crear una entrada
* Actualizar una entrada
* Eliminar una entrada

Para evitar la repetición, es posible definir recursos. Las siguientes rutas:

```php
<?php
return [
    'routes' => [
        ['name' => 'author#index', 'url' => '/authors', 'verb' => 'GET'],
        ['name' => 'author#show', 'url' => '/authors/{id}', 'verb' => 'GET'],
        ['name' => 'author#create', 'url' => '/authors', 'verb' => 'POST'],
        ['name' => 'author#update', 'url' => '/authors/{id}', 'verb' => 'PUT'],
        ['name' => 'author#destroy', 'url' => '/authors/{id}', 'verb' => 'DELETE'],
        // your other routes here
    ],
];
```

se pueden abreviar usando la clave **resources**:

```php
<?php
return [
    'resources' => [
        'author' => ['url' => '/authors'],
    ],
    'routes' => [
        // your other routes here
    ],
];
```

### Usar el URLGenerator

A veces es útil convertir una ruta en una URL para que el código no dependa del diseño de las URL, o para generar la URL de una imagen en **img/**. Dentro del PageController, el generador de URL se puede inyectar agregándolo al constructor, lo que permitirá usarlo para generar una URL para una redirección. Para más detalles al respecto, consultar la referencia de {nc-ref}`dependency-injection`.

```php
<?php
namespace OCA\MyApp\Controller;

use \OCP\IRequest;
use \OCP\IURLGenerator;
use \OCP\AppFramework\Controller;
use \OCP\AppFramework\Http\RedirectResponse;

class PageController extends Controller {

    private $urlGenerator;

    public function __construct(string $appName, IRequest $request,
                                IURLGenerator $urlGenerator) {
        parent::__construct($appName, $request);
        $this->urlGenerator = $urlGenerator;
    }

    /**
     * Redirects to /apps/news/myapp/authors/3
     */
    public function redirect(): RedirectResponse {
        // route name: author_api#do_something
        // route url: /apps/news/myapp/authors/{id}

        // # needs to be replaced with a . due to limitations and prefixed
        // with your app id
        $route = 'myapp.author_api.do_something';
        $parameters = ['id' => 3];

        $url = $this->urlGenerator->linkToRoute($route, $parameters);

        return new RedirectResponse($url);
    }
}
```

URLGenerator distingue mayúsculas de minúsculas, así que **appName** debe coincidir **exactamente** con el nombre que se usa en la {nc-doc}`configuración <developer_manual/basics/storage/configuration>`.
Si se usa un nombre en CamelCase, como *myCamelCaseApp*,

```php
<?php
$route = 'myCamelCaseApp.author_api.do_something';
```

### Comandos de consola

Dos comandos `occ` ayudan a inspeccionar y depurar la tabla de rutas:

```
router
 router:list   list routes, optionally filtered by app
 router:match  match a URL path to a route
```

#### router:list

Lista todas las rutas registradas. Opcionalmente, se puede filtrar por una o varias apps:

```
sudo -E -u www-data php occ router:list
sudo -E -u www-data php occ router:list myapp
```

Usar `--ocs` para mostrar solo las rutas de la API OCS, o `--index` para mostrar solo las
rutas de `index.php`:

```
sudo -E -u www-data php occ router:list --ocs
sudo -E -u www-data php occ router:list myapp --index
```

#### router:match

Compara una ruta de URL con la tabla de rutas y muestra a qué ruta y a qué controlador
corresponde. Es útil para depurar por qué una solicitud llega al lugar equivocado:

```
sudo -E -u www-data php occ router:match /apps/myapp/authors/3
```

Usar `--method` para comparar con un verbo HTTP concreto (de forma predeterminada: `GET`):

```
sudo -E -u www-data php occ router:match /apps/myapp/authors/3 --method=POST
```
````
