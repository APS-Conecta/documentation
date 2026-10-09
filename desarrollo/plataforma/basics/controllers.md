---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo escribir controladores: parámetros de la solicitud, sesiones, cookies, respuestas HTML, OCS y JSON, responders y opciones de seguridad."
---
# Controladores

## Resumen

Esta página explica cómo escribir controladores que conectan las rutas con la lógica de la app: cómo reciben los parámetros de la solicitud, las sesiones y las cookies, los tipos de respuesta (plantillas, OCS, JSON, redirecciones, descargas y respuestas propias) y las opciones de seguridad (autenticación, limitación de frecuencia, protección contra fuerza bruta y política de seguridad de contenido). Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/controllers.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los controladores se usan para conectar las {nc-doc}`rutas <developer_manual/basics/routing>` con la lógica de la app. Se pueden ver como callbacks que se ejecutan una vez que ha llegado una solicitud. Los controladores se definen dentro del directorio **lib/Controller/**.

Para crear un controlador, basta con extender la clase Controller y crear un método que deba ejecutarse ante una solicitud:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\Response;

class AuthorController extends Controller {

    public function index(): Response {

    }
}
```

### Conectar un controlador y una ruta

Si se usa un espacio de nombres adecuado para la app (ver {nc-ref}`appclassloader`), Nextcloud resolverá el controlador y sus dependencias automáticamente.

Un nombre de ruta de ejemplo tendría este aspecto:

```
author_api#some_method
```

Este nombre se procesa de la siguiente manera:

* Quitar el guion bajo y poner en mayúscula el carácter siguiente:

  ```
  authorApi#someMethod
  ```

* Dividir en el # y poner en mayúscula la primera letra de la parte izquierda:

  ```
  AuthorApi
  someMethod
  ```

* Agregar Controller a la primera parte:

  ```
  AuthorApiController
  someMethod
  ```

* Ahora obtener del contenedor el servicio registrado como **AuthorApiController**, buscar en la solicitud los parámetros del método **someMethod**, convertirlos si hay anotaciones de tipo en el PHPDoc y ejecutar el método **someMethod** del controlador con esos parámetros.

### Obtener los parámetros de la solicitud

Los parámetros pueden pasarse de muchas formas:

* Extraídos de la URL usando llaves, como **{key}**, dentro de la URL (ver {nc-doc}`developer_manual/basics/routing`)
* Añadidos a la URL como una solicitud GET (p. ej., ?something=true)
* application/x-www-form-urlencoded desde un formulario o jQuery
* application/json desde una solicitud POST, PATCH o PUT

Se puede acceder fácilmente a todos esos parámetros agregándolos al método del controlador:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\Response;

class PageController extends Controller {

    // this method will be executed with the id and name parameter taken
    // from the request
    public function doSomething(string $id, string $name): Response {

    }

}
```

También es posible fijar valores predeterminados para los parámetros usando los valores predeterminados de los métodos de PHP, de modo que se puedan omitir los valores habituales:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\Response;

class PageController extends Controller {

    /**
     * @param int $id
     */
    public function doSomething(int $id, string $name='john', string $job='author'): Response {
        // GET ?id=3&job=killer
        // $id = 3
        // $name = 'john'
        // $job = 'killer'
    }

}
```

#### Conversión de parámetros

URL, GET y application/x-www-form-urlencoded tienen el problema de que todos los parámetros son cadenas, lo que significa que:

```
?doMore=false
```

se pasaría como la cadena *'false'*, que no es lo que se esperaría. Para convertirlos a los tipos correctos, basta con agregar PHPDoc de la forma:

```
@param type $name
```

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\Response;

class PageController extends Controller {

    /**
     * @param int $id
     * @param bool $doMore
     * @param float $value
     */
    public function doSomething(int $id, bool $doMore, float $value): Response {
        // GET /index.php/apps/myapp?id=3&doMore=false&value=3.5
        // => $id = 3
        //    $doMore = false
        //    $value = 3.5
    }

}
```

Se convierten los tipos siguientes:

* **bool** o **boolean**
* **float**
* **int** o **integer**

#### Parámetros JSON

Es posible pasar JSON mediante una solicitud POST, PUT o PATCH. Para ello, la cabecera **Content-Type** debe establecerse en **application/json**. El JSON se analiza como un array y las claves del primer nivel se usan para pasar los argumentos, p. ej.:

```
POST /index.php/apps/myapp/authors
Content-Type: application/json
{
    "name": "test",
    "number": 3,
    "publisher": true,
    "customFields": {
        "mail": "test@example.com",
        "address": "Somewhere"
    }
}
```

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\Response;

class PageController extends Controller {

    public function create(string $name, int $number, string $publisher, array $customFields): Response {
        // $name = 'test'
        // $number = 3
        // $publisher = true
        // $customFields = array("mail" => "test@example.com", "address" => "Somewhere")
    }

}
```

#### Leer cabeceras, archivos, cookies y variables de entorno

Se puede acceder a las cabeceras, los archivos, las cookies y las variables de entorno directamente desde el objeto de la solicitud:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\Response;
use OCP\IRequest;

class PageController extends Controller {

    public function someMethod(): Response {
        $type = $this->request->getHeader('Content-Type');  // $_SERVER['HTTP_CONTENT_TYPE']
        $cookie = $this->request->getCookie('myCookie');  // $_COOKIES['myCookie']
        $file = $this->request->getUploadedFile('myfile');  // $_FILES['myfile']
        $env = $this->request->getEnv('SOME_VAR');  // $_ENV['SOME_VAR']
    }

}
```

¿Por qué se debe acceder a esos valores desde el objeto de la solicitud y no desde el array global, como $_FILES? Sencillo:
[porque es una mala práctica](http://c2.com/cgi/wiki?GlobalVariablesAreBad) y hará más difíciles las pruebas.

(nc-dev-controller-use-session)=
#### Sesiones y variables de sesión

##### Introducción

Las sesiones permiten a la aplicación almacenar datos específicos de un usuario concreto a lo largo de varias solicitudes HTTP. Las variables se guardan en el servidor y quedan ligadas a un identificador de sesión único que se gestiona mediante una cookie del navegador.

Nextcloud usa la gestión de sesiones nativa de PHP, pero agrega varias optimizaciones de rendimiento y una capa de cifrado transparente mediante la clase `CryptoSessionData`. Los datos que se escriben a través de la API `OCP\ISession` se benefician de estas optimizaciones y se cifran automáticamente en reposo.

:::{danger}
No usar nunca la superglobal de PHP `$_SESSION`. La superglobal se salta el cifrado y la gestión del ciclo de vida de Nextcloud, lo que provoca condiciones de carrera o pérdida de datos.
:::

##### Uso básico

Se inyecta el objeto {code}`OCP\ISession` mediante el constructor del controlador.

Un ejemplo más completo:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\Attribute\UseSession;
use OCP\AppFramework\Http\Response;
use OCP\ISession;
use OCP\IRequest;

class PageController extends Controller {
    public function __construct(
        $appName,
        IRequest $request,
        private ISession $session // PHP 8 property promotion
    ) {
        parent::__construct($appName, $request);
    }

    // Simple (existing) variable retrieval
    public function simpleReads(): Response {
        $this->session->get('last_visit');
        return new Response();
    }

    // Default: Implicit locking per write. Good for single operations.
    public function simpleWrite(): Response {
        $this->session->set('last_visit', time());
        return new Response();
    }

    // Optimization: Keeps session open for the entire method.
    #[UseSession]
    public function batchUpdate(): Response {
        $this->session->set('theme', 'dark');
        $this->session->set('font_size', '14px');
        $this->session->remove('fallback_theme');
        return new Response();
    }
}
```

##### Cuándo usar `#[UseSession]`

De forma predeterminada, Nextcloud usa una **estrategia de bloqueo bajo demanda**: cierra la sesión inmediatamente después de que empieza la solicitud para permitir una alta concurrencia y luego la vuelve a abrir y cerrar brevemente solo durante una llamada a `set()` o `remove()`. Este comportamiento predeterminado de «cierre temprano» funciona para escrituras poco frecuentes y aisladas, y evita que una solicitud bloquee a otra. No es necesario hacer nada especial para activar este comportamiento.

Sin embargo, en escenarios más avanzados (p. ej., llamar a `set()` cinco veces seguidas), el comportamiento predeterminado de Nextcloud implica que la sesión se abrirá y cerrará cinco veces. Esto introduce una sobrecarga de E/S considerable (aunque reduce al mínimo los bloqueos). Para estos casos, Nextcloud admite un atributo opcional a nivel de método: `#[UseSession]`. Este atributo garantiza que la sesión se abra una vez al inicio del método y se cierre al final, lo que aporta eficiencia y un bloqueo correcto en flujos de trabajo complejos.

Usar el atributo `#[UseSession]` cuando:

* **Varias escrituras**: se llama a `set()` o `remove()` varias veces en un mismo método (evita la sobrecarga de E/S de los ciclos repetidos de apertura y cierre).
* **Manipulación de referencias**: se necesita que la sesión permanezca abierta para una lógica compleja o para garantizar la coherencia de los datos a lo largo del método.
* **Regeneración de los ids de sesión**: se elevan los privilegios de un usuario (p. ej., se introduce una contraseña válida de un recurso compartido y el estado «acceso concedido» se guarda en la sesión) o el usuario realiza una modificación sensible (p. ej., un cambio de contraseña).

:::{note}
El atributo `#[UseSession]` se introdujo en Nextcloud 26. Antes, esta función usaba la anotación `@UseSession`, que ahora está obsoleta pero por lo demás es equivalente.
:::

##### Rendimiento y concurrencia

PHP bloquea de forma nativa el archivo de sesión mientras está abierto para escritura. Si un controlador mantiene una sesión abierta sin necesidad, puede bloquear otras solicitudes del mismo usuario (p. ej., pestañas paralelas del navegador o llamadas AJAX), lo que provoca retrasos o tiempos de espera agotados.

Al mantener las sesiones cerradas salvo durante el breve intervalo de una escritura real, Nextcloud garantiza una experiencia ágil, con varias pestañas y altamente concurrente. Para más información técnica, ver [PHP Session Locking and How to Prevent It](https://ma.ttias.be/php-session-locking-prevent-sessions-blocking-php-requests/).

:::{warning}
Si el método del controlador mantiene las sesiones abiertas de forma agresiva, puede bloquear otras solicitudes del mismo usuario o proceso (por ejemplo, una segunda pestaña del navegador, una solicitud AJAX o un trabajo en segundo plano), lo que provoca retrasos o bloqueos mutuos.
:::

Para la API completa de `OCP\\ISession`, ver
[ISession.php](https://github.com/nextcloud/server/blob/master/lib/public/ISession.php).

#### Establecer cookies

Las cookies pueden establecerse o modificarse directamente en la clase de respuesta:

```php
 <?php
 namespace OCA\MyApp\Controller;

 use DateTime;

 use OCP\AppFramework\Controller;
 use OCP\AppFramework\Http\TemplateResponse;
 use OCP\IRequest;

 class BakeryController extends Controller {

     /**
      * Adds a cookie "foo" with value "bar" that expires after user closes the browser
      * Adds a cookie "bar" with value "foo" that expires 2015-01-01
      */
     public function addCookie(): TemplateResponse {
         $response = new TemplateResponse(...);
         $response->addCookie('foo', 'bar');
         $response->addCookie('bar', 'foo', new DateTime('2015-01-01 00:00'));
         return $response;
     }

     /**
      * Invalidates the cookie "foo"
      * Invalidates the cookie "bar" and "bazinga"
      */
     public function invalidateCookie(): TemplateResponse {
         $response = new TemplateResponse(...);
         $response->invalidateCookie('foo');
         $response->invalidateCookies(array('bar', 'bazinga'));
         return $response;
     }
}
```

### Respuestas

Del mismo modo que cada controlador recibe un objeto de solicitud, cada método de controlador debe devolver una Response. Puede ser en forma de una subclase de Response o en forma de un valor que pueda gestionar un responder registrado.

Hay distintos tipos de respuestas disponibles, como respuestas basadas en HTML, respuestas de datos u otras. La app decide de qué tipo es la respuesta devolviendo un objeto `Response` adecuado en el método de controlador correspondiente. Las secciones siguientes dan un panorama de los distintos tipos y de cómo implementarlos.

(nc-dev-controller_html_responses)=
### Respuestas basadas en HTML

Las páginas HTML suelen servirse mediante respuestas de plantilla. Esto se usa normalmente como punto de partida para cargar el sitio web. El servidor encapsula de forma predeterminada el código enlazado por la plantilla para aplicar algunos estilos comunes (p. ej., la fila de cabecera). Luego el código usa JavaScript para cargar más componentes (ver {nc-ref}`Construcción del frontend en Vue <ApplicationJs>`) y los datos propiamente dichos. Esta sección se centra solo en el contenido HTML propiamente dicho, no en los datos con que se rellenan las páginas dinámicas.

(nc-dev-controller_template)=
#### Plantillas

Una {nc-doc}`plantilla <developer_manual/basics/front-end/templates>` puede renderizarse devolviendo una TemplateResponse. Una TemplateResponse recibe los siguientes parámetros:

* **appName**: indica al motor de plantillas en qué app debe ubicarse la plantilla
* **templateName**: el nombre de la plantilla dentro de la carpeta templates/, sin la extensión .php
* **parameters**: parámetros opcionales en forma de array que están disponibles en la plantilla mediante $_, p. ej.:

  ```
  array('key' => 'something')
  ```

  se puede acceder a ellos mediante:

  ```
  $_['key']
  ```

* **renderAs**: el valor predeterminado es *user*; indica a Nextcloud si debe incluirla en la interfaz web o, si se pasa *blank*, solo renderizar la plantilla

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\TemplateResponse;

class PageController extends Controller {

    public function index(): TemplateResponse {
        $templateName = 'main';  // will use templates/main.php
        $parameters = array('key' => 'hi');
        return new TemplateResponse($this->appName, $templateName, $parameters);
    }

}
```

Mostrar una plantilla es la única excepción a la regla de {nc-ref}`no desactivar las comprobaciones CSRF <csrf_introduction>`:
El usuario podría escribir la URL directamente (o usar un marcador del navegador o algo similar) para navegar a una plantilla HTML.
Por eso, en este contexto es aceptable usar el atributo `#[NoCSRFRequired]` (ver {nc-ref}`más abajo <controller_authentication>`).

#### Plantillas de páginas públicas

Para las páginas públicas, que se renderizan para usuarios que no han iniciado sesión en la instancia de Nextcloud, debe usarse una `OCP\\AppFramework\\Http\\Template\\PublicTemplateResponse`, para cargar la plantilla base correcta. También permite agregar un conjunto opcional de acciones que se mostrarán en la esquina superior derecha de la página pública.

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\Template\SimpleMenuAction;
use OCP\AppFramework\Http\Template\PublicTemplateResponse;

class PageController extends Controller {

    public function index(): PublicTemplateResponse {
        $template = new PublicTemplateResponse($this->appName, 'main', []);
        $template->setHeaderTitle('Public page');
        $template->setHeaderDetails('some details');
        $template->setHeaderActions([
            new SimpleMenuAction('download', 'Label 1', 'icon-css-class1', 'link-url', 0),
            new SimpleMenuAction('share', 'Label 2', 'icon-css-class2', 'link-url', 10),
        ]);
        return $template;
    }

}
```

El título y el subtítulo de la cabecera se renderizarán en la cabecera, junto al logotipo. La acción con la prioridad más alta (el número más bajo) se usará como acción principal; las demás se mostrarán bajo demanda en el menú emergente.

Una `OCP\\AppFramework\\Http\\Template\\SimpleMenuAction` será un enlace con un icono agregado al menú. Quienes desarrollan apps pueden implementar sus propios tipos de renderizado de menús agregando una clase personalizada que implemente la interfaz `OCP\\AppFramework\\Http\\Template\\IMenuAction`.

Como la plantilla pública también es una plantilla HTML, vale la misma argumentación que para las {nc-ref}`plantillas normales <controller_template>` respecto de las comprobaciones CSRF:
El uso de `#[NoCSRFRequired]` en las páginas públicas se considera aceptable para algunas páginas:
Toda página a la que el usuario deba poder acceder directamente (escribiendo o pegando la URL en el navegador o haciendo clic en un enlace de un correo) debe tener este atributo.
En los formularios de varias páginas, a partir de la segunda etapa **no** debe establecerse, ya que el usuario debe seguir la serie de páginas.

### Respuestas basadas en datos

A diferencia de las respuestas de plantillas HTML, las respuestas de datos devuelven datos de usuario en forma empaquetada.
Se pueden concebir distintas codificaciones, como JSON, XML u otros formatos.
Lo principal es que el navegador solicita los datos mediante JavaScript en nombre del sitio web que se muestra.
El usuario solo solicitó los datos de forma indirecta, al interactuar con el frontend.

(nc-dev-ocscontroller)=
#### OCS

Para simplificar el intercambio de datos entre el backend de Nextcloud y cualquier cliente (ya sea el frontend web o cualquier otro), se introdujo la API OCS.
En ella se han preparado responders de JSON y de XML, que se instalan sin esfuerzo adicional.

:::{note}
El uso de OCS está estrechamente relacionado con el uso de {nc-doc}`developer_manual/digging_deeper/rest_apis`.
Salvo que exista un caso de uso claro, se aconseja usar OCS en lugar de REST puro.
Se puede encontrar una descripción más detallada en {nc-ref}`ocs-vs-rest`.
:::

Para usar OCS en la API se puede usar la clase base **OCP\AppFramework\OCSController** y devolver los datos en forma de una **DataResponse** de la siguiente manera:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Http\DataResponse;
use OCP\AppFramework\Http\Attribute\NoAdminRequired;
use OCP\AppFramework\OCSController;

class ShareController extends OCSController {

    #[NoAdminRequired]
    public function getShares(): DataResponse {
        return new DataResponse([
            //Your data here
        ]);
    }

}
```

En las clases `OCSController` y sus métodos se pueden registrar {nc-ref}`responders <controller-responders>` como en cualquier otro método de `Controller`.
Sin embargo, la clase `OCSController` trae preinstalados automáticamente dos responders:
Tanto JSON (`application/json`) como XML (`text/xml`) se generan sobre la marcha según lo que solicite el navegador o el usuario.
Para elegir el formato de salida, el parámetro de consulta `?format=` o la cabecera `Accept` de la solicitud funcionan de inmediato, sin necesidad de intervención.
En general se aconseja preferir la cabecera, ya que es la forma más estandarizada.

Para que las rutas funcionen con OCS, la ruta debe registrarse en el núcleo.
Esto puede hacerse de dos maneras:
Se puede agregar un atributo *#[ApiRoute]* al método del controlador.
Como alternativa, se puede agregar {nc-ref}`una entrada 'ocs' aparte <routes_ocs>` a la tabla de rutas en `appinfo/routes.php` de la app.
Dentro de ellas va la misma información que en las rutas normales.

```php
<?php

return [
     'ocs' => [
         [
             'name' => 'Share#getShares',
             'url' => '/api/v1/shares',
             'verb' => 'GET',
         ],
     ],
];
```

Ahora el método será accesible mediante `<server>/ocs/v2.php/apps/<APPNAME>/api/v1/shares`

:::{versionadded} 29
Se puede usar el atributo `ApiRoute`, como se describe en {nc-doc}`Rutas <developer_manual/basics/routing>`, en lugar de la entrada en `appinfo/routes.php`, como alternativa.
:::

#### JSON

:::{warning}
El uso de un controlador estándar para acceder a contenido de datos como JSON (no HTML) se considera heredado.
Es mejor usar {nc-ref}`OCS <ocscontroller>` para este tipo de solicitudes.
:::

Devolver JSON es sencillo: basta con pasar un array a una JSONResponse:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\JSONResponse;

class PageController extends Controller {

    public function returnJSON(): JSONResponse {
        $params = array('test' => 'hi');
        return new JSONResponse($params);
    }

}
```

Como devolver JSON es una tarea tan habitual, hay incluso una forma más corta de hacerlo:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;

class PageController extends Controller {

    public function returnJSON(): array {
        return array('test' => 'hi');
    }

}
```

¿Por qué funciona? Porque el despachador ve que el controlador no devolvió una subclase de Response y le pide al controlador que convierta el valor en una Response. Ahí es donde entran los responders.

:::{deprecated} 30
Debe evitarse el uso de controladores «index.php» para la transmisión de datos. Usar OCS en su lugar.
:::

#### Gestión de errores

A veces una solicitud debe fallar, por ejemplo, si se solicita un autor con id 1 que no existe. En ese caso, usar un [código de error HTTP](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_Error) adecuado para indicar al cliente que se produjo un error.

Cada subclase de respuesta tiene acceso al método **setStatus**, que permite establecer un código de estado HTTP. Para devolver una JSONResponse que indique que no se encontró el autor con id 1, usar el siguiente código:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http;
use OCP\AppFramework\Http\JSONResponse;

class AuthorController extends Controller {

    public function show($id) {
        try {
            // try to get author with $id

        } catch (NotFoundException $ex) {
            return new JSONResponse(array(), Http::STATUS_NOT_FOUND);
        }
    }
}
```

(nc-dev-controller-responders)=
#### Responders

Los responders son funciones breves que reciben un valor y devuelven una respuesta. Se usan para devolver distintos tipos de respuesta según un parámetro **format** que proporciona el cliente. Piénsese en una API capaz de devolver tanto XML como JSON según se llame a la URL con:

```
?format=xml
```

o:

```
?format=json
```

El responder adecuado se elige según los criterios siguientes:

* Primero, el despachador comprueba si la Request tiene un parámetro **format**, p. ej.:

  ```
  ?format=xml
  ```

  o:

  ```
  /index.php/apps/myapp/authors.{format}
  ```

* Si no lo tiene, toma la cabecera **Accept**, usa el primer tipo MIME y le quita *application/*. En el siguiente ejemplo, el formato sería *xml*:

  ```
  Accept: application/xml, application/json
  ```

* Si no hay cabecera Accept o el responder no existe, el formato es **json** de forma predeterminada.

De forma predeterminada solo hay un responder para JSON, pero se pueden agregar más fácilmente:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\DataResponse;

class PageController extends Controller {

    public function returnHi(): array {

        // XMLResponse has to be implemented
        $this->registerResponder('xml', function($value) {
            if ($value instanceof DataResponse) {
                return new XMLResponse(
                    $value->getData(),
                    $value->getStatus(),
                    $value->getHeaders()
                );
            } else {
                return new XMLResponse($value);
            }
        });

        return array('test' => 'hi');
    }

}
```

:::{note}
El ejemplo anterior solo devolvería XML si el parámetro **format** fuera *xml*. Si se quiere devolver una XMLResponse independientemente del parámetro format, hay que extender la clase Response y devolver una nueva instancia de ella desde el método del controlador.
:::

Como devolver valores funciona bien en caso de éxito, pero no en caso de un fallo que requiera un código de error HTTP personalizado, siempre se puede envolver el valor en una **DataResponse**. Esto funciona tanto para las respuestas normales como para las respuestas de error.

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\DataResponse;
use OCP\AppFramework\Http\Http;

class PageController extends Controller {

    public function returnHi(): DataResponse {
        try {
            return new DataResponse(calculate_hi());
        } catch (\Exception $ex) {
            return new DataResponse(array('msg' => 'not found!'), Http::STATUS_NOT_FOUND);
        }
    }

}
```

### Respuestas diversas

También hay disponibles algunas respuestas especiales.
Se describen aquí.

#### Redirecciones

Una redirección se consigue devolviendo una RedirectResponse:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\RedirectResponse;

class PageController extends Controller {

    public function toGoogle(): RedirectResponse {
        return new RedirectResponse('https://google.com');
    }

}
```

#### Descargas

La descarga de un archivo se puede iniciar devolviendo una DownloadResponse:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\DownloadResponse;

class PageController extends Controller {

    public function downloadXMLFile(): DownloadResponse {
        $path = '/some/path/to/file.xml';
        $contentType = 'application/xml';

        return new DownloadResponse($path, $contentType);
    }

}
```

#### Crear respuestas personalizadas

Si ninguna Response prefabricada se ajusta al caso de uso necesario, es posible extender la clase base Response y crear una Response personalizada. Lo único que hay que implementar es el método **render**, que devuelve el resultado como cadena.

Crear una clase XMLResponse personalizada podría verse así:

```php
<?php
namespace OCA\MyApp\Http;

use OCP\AppFramework\Http\Response;

class XMLResponse extends Response {

    private array $xml;

    public function __construct(array $xml) {
        $this->addHeader('Content-Type', 'application/xml');
        $this->xml = $xml;
    }

    public function render(): string {
        $root = new SimpleXMLElement('<root/>');
        array_walk_recursive($this->xml, array ($root, 'addChild'));
        return $xml->asXML();
    }

}
```

#### Respuestas transmitidas y renderizadas de forma diferida

De forma predeterminada, todas las respuestas se renderizan de una vez y se envían como una cadena a través del middleware. En ciertos casos este no es un comportamiento deseable, por ejemplo, si se quiere transmitir un archivo para ahorrar memoria. Para ello, usar la clase **OCP\AppFramework\Http\StreamResponse**, ahora disponible:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\StreamResponse;

class PageController extends Controller {

    public function downloadXMLFile() {
        return new StreamResponse('/some/path/to/file.xml');
    }

}
```

Si se quiere usar una respuesta personalizada renderizada de forma diferida, basta con implementar la interfaz **OCP\AppFramework\Http\ICallbackResponse** en la respuesta:

```php
<?php
namespace OCA\MyApp\Http;

use OCP\AppFramework\Http\Response;
use OCP\AppFramework\Http\ICallbackResponse;

class LazyResponse extends Response implements ICallbackResponse {

    public function callback(IOutput $output) {
        // custom code in here
    }

}
```

:::{note}
Como este código se renderiza después de varios asistentes que normalmente vienen incorporados, hay que ocuparse por cuenta propia de los errores y del almacenamiento en caché HTTP adecuado.
:::

### Consideraciones de seguridad

Según el caso de uso, se pueden endurecer o relajar las medidas de seguridad instaladas de forma predeterminada en las rutas.
Esta sección da un panorama rápido de las opciones.

(nc-dev-controller_authentication)=
#### Autenticación

De forma predeterminada, cada método de controlador aplica la máxima seguridad, que consiste en:

* Asegurar que el usuario sea administrador
* Asegurar que el usuario haya iniciado sesión
* Asegurar que el usuario haya superado el desafío de dos factores, si corresponde
* Asegurar que la solicitud no sea un ataque CSRF, es decir, al menos una de las siguientes condiciones:

  - Asegurar que el token CSRF esté presente y sea válido
  - Asegurar que la cabecera `OCS-APIRequest` esté presente y establecida en `true` [^1]

##### Relajar las restricciones predeterminadas

Sin embargo, la mayoría de las veces tiene sentido permitir también el acceso a la página a los usuarios normales, y el método `PageController->index()` no debería comprobar el token CSRF, porque todavía no se ha enviado al cliente y, por eso, no puede funcionar.

Para desactivar comprobaciones, se pueden agregar los siguientes *atributos* antes del controlador:

* `#[NoAdminRequired]`: también los usuarios que no son administradores pueden acceder a la página
* `#[PublicPage]`: cualquiera puede acceder a la página sin tener que iniciar sesión
* `#[NoTwoFactorRequired]`: un usuario puede acceder a la página antes de haber superado el desafío de dos factores (usarlo con prudencia y solo en apps de autenticación de dos factores, p. ej., para permitir la configuración durante el inicio de sesión)
* `#[NoCSRFRequired]`: no comprobar el token CSRF (usarlo con prudencia, ya que se podría crear un agujero de seguridad; para entender qué hace, ver {nc-ref}`CSRF en la sección de seguridad <csrf_introduction>`)

:::{note}
Los atributos solo están disponibles en Nextcloud 27 o posterior. En versiones anteriores existen anotaciones con los mismos nombres:

* `@NoAdminRequired` en lugar de `#[NoAdminRequired]`
* `` @PublicPage` `` en lugar de `#[PublicPage]`
* `` @NoTwoFactorRequired` `` en lugar de `#[NoTwoFactorRequired]`
* `` @NoCSRFRequired` `` en lugar de `#[NoCSRFRequired]`
:::

A continuación se dan algunos ejemplos de configuración.

##### Mostrar una página HTML al usuario

Una app típica necesita una página `index.html` en la que mostrar todo el contenido.
Esta página debe ser visible para todos los usuarios de la instancia.
Por eso hay que relajar la restricción de solo administradores (`#[NoAdminRequired]`).
Además, como el usuario podría no tener todavía una cookie de comprobación CSRF, las comprobaciones CSRF deben desactivarse (lo que no es un problema, ya que se trata de una respuesta de plantilla).

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\TemplateResponse;
use OCP\AppFramework\Http\Attribute\NoCSRFRequired;
use OCP\AppFramework\Http\Attribute\PublicPage;

class PageController extends Controller {

    #[NoCSRFRequired]
    #[NoAdminRequired]
    public function index(): TemplateResponse {
        return new TemplateResponse($this->appName, 'main');
    }

}
```

Si la página solo debe ser visible para el administrador, se puede mantener el valor predeterminado restrictivo omitiendo el atributo `#[NoAdminRequired]`.

##### Obtener datos del backend mediante solicitudes AJAX

Los datos para el frontend deben ponerse a disposición desde el backend.
Para ello, OCS es la vía sugerida.
Este es el ejemplo de {nc-ref}`controladores OCS <ocscontroller>`:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Http\DataResponse;
use OCP\AppFramework\Http\Attribute\NoAdminRequired;
use OCP\AppFramework\OCSController;

class ShareController extends OCSController {

    #[NoAdminRequired]
    public function getShares(): DataResponse {
        return new DataResponse([
            // Your data here
        ]);
    }

}
```

Aquí se necesita `#[NoAdminRequired]`, ya que los usuarios normales deben poder acceder a los datos.
Puede omitirse si solo el usuario administrador debe poder acceder a los datos.
La comprobación CSRF sigue activa.
Por lo tanto, el cliente debe cumplir los requisitos correspondientes.

##### Autenticación completamente desactivada

:::{warning}
Esto es un problema de seguridad si no se consideran cuidadosamente los efectos secundarios.
Solo debe usarse para páginas públicas a las que cualquiera puede acceder.
:::

Un método de controlador que desactiva todas las comprobaciones tendría este aspecto:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\IRequest;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\Attribute\NoCSRFRequired;
use OCP\AppFramework\Http\Attribute\PublicPage;

class PageController extends Controller {
    #[NoCSRFRequired]
    #[PublicPage]
    public function freeForAll() {

    }
}
```

#### Limitación de frecuencia

Nextcloud admite la limitación de frecuencia por método de controlador y de forma {nc-ref}`programática <programmatic-rate-limiting>`. De forma predeterminada, los métodos de controlador no tienen limitación de frecuencia. La limitación de frecuencia debe usarse en funciones costosas o sensibles para la seguridad (p. ej., el restablecimiento de contraseñas) para aumentar la seguridad general de la aplicación.

La limitación de frecuencia nativa devolverá a los clientes un código de estado 429 cuando se alcance el límite, junto con una página de error predeterminada de Nextcloud. Al implementar la limitación de frecuencia en la aplicación, conviene por tanto contemplar el manejo de las situaciones de error en que Nextcloud devuelve un 429.

Para activar la limitación de frecuencia, se pueden agregar los siguientes *atributos* al controlador:

* `#[UserRateLimit(limit: int, period: int)]`: la limitación de frecuencia que se aplica a los usuarios que han iniciado sesión. Si no se especifica, Nextcloud recurrirá a `AnonRateLimit`, si está disponible.
* `#[AnonRateLimit(limit: int, period: int)]`: la limitación de frecuencia que se aplica a los invitados.

:::{note}
Los atributos solo están disponibles en Nextcloud 27 o posterior. En versiones anteriores se pueden usar las anotaciones `@UserRateThrottle(limit=int, period=int)` y `@AnonRateThrottle(limit=int, period=int)`. Si ambos están presentes, se considerará primero el atributo.
:::

Un método de controlador que permitiera cinco solicitudes para los usuarios que han iniciado sesión y una solicitud para los usuarios anónimos en los últimos 100 segundos tendría este aspecto:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\IRequest;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\Attribute\AnonRateLimit;
use OCP\AppFramework\Http\Attribute\UserRateLimit;

class PageController extends Controller {

    /**
     * @PublicPage
     */
    #[UserRateLimit(limit: 5, period: 100)]
    #[AnonRateLimit(limit: 1, period: 100)]
    public function rateLimitedForAll() {

    }
}
```

#### Protección contra fuerza bruta

Nextcloud admite la protección contra fuerza bruta por acción. De forma predeterminada, los métodos de controlador no están protegidos. La protección contra fuerza bruta debe usarse en funciones sensibles para la seguridad (p. ej., los intentos de inicio de sesión) para aumentar la seguridad general de la aplicación.

La protección nativa contra fuerza bruta ralentizará las solicitudes si se han detectado demasiadas infracciones. Esta ralentización se aplicará a todas las solicitudes, provenientes de la IP afectada, contra un controlador protegido contra fuerza bruta con la misma acción.

Para activar la protección contra fuerza bruta, se puede agregar el siguiente *atributo* al controlador:

* `#[BruteForceProtection(action: 'string')]`: «string» es el nombre de la acción, como «login» o «reset». Los intentos de fuerza bruta se cuentan por acción; esto significa que, si se produce una infracción en la acción «login», otras acciones como «reset» o «foobar» no se ven afectadas.

:::{note}
El atributo solo está disponible en Nextcloud 27 o posterior. En versiones anteriores se puede usar la anotación `@BruteForceProtection(action=string)`, pero esta no permite varias asignaciones a un mismo método de controlador.
:::

Luego, en caso de infracción, hay que llamar al método **throttle()** de la respuesta. Al hacerlo, aumenta el contador de limitación y las solicitudes siguientes se vuelven más lentas, hasta alcanzar una lentitud de unos 30 segundos y que el controlador devuelva un estado `429 Too Many Requests` sin seguir procesando la solicitud.

Un método de controlador que implementara la protección contra fuerza bruta con una acción «foobar» tendría este aspecto:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\IRequest;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\Attribute\BruteForceProtection;
use OCP\AppFramework\Http\TemplateResponse;

class PageController extends Controller {

    #[BruteForceProtection(action: 'foobar')]
    public function bruteforceProtected(): TemplateResponse {
        $templateResponse = new TemplateResponse(…);
        // In case of a violation increase the throttle counter
        // note that $this->auth->isSuccessful here is just an
        // example.
        if (!$this->auth->isSuccessful()) {
             $templateResponse->throttle();
        }
        return $templateResponse;
    }
}
```

Un controlador también puede tener varios factores frente a los que protegerse de la fuerza bruta. En ese caso, se pueden especificar varios atributos y luego, en throttle, indicar la acción que se infringió. Esto es especialmente útil cuando un secreto (en el ejemplo de abajo, token) podría adivinarse en varios endpoints, p. ej., un token de recurso compartido en el nivel de la API, el endpoint de vista previa, el controlador del frontend, etc., mientras que otro secreto (password) es específico de este único método de controlador.

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\IRequest;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\Attribute\BruteForceProtection;
use OCP\AppFramework\Http\TemplateResponse;

class PageController extends Controller {

    #[BruteForceProtection(action: 'token')]
    #[BruteForceProtection(action: 'password')]
    public function getPasswordProtectedShare(string $token, string $password): TemplateResponse {
        $templateResponse = new TemplateResponse(…);
        if (!$this->shareManager->getByToken($token)) {
            $templateResponse->throttle(['action' => 'token']);
        }
        // …
        if (!$share->verifyPassword($password)) {
            $templateResponse->throttle(['action' => 'password']);
        }
        return $templateResponse;
    }
}
```

#### Modificar la política de seguridad de contenido

De forma predeterminada, Nextcloud desactiva todos los recursos que no se sirven desde el mismo dominio, prohíbe las solicitudes entre dominios y desactiva el CSS y el JavaScript en línea estableciendo una [política de seguridad de contenido](https://developer.mozilla.org/en-US/docs/Web/Security/CSP/Introducing_Content_Security_Policy).
Sin embargo, si una app depende de contenido multimedia de terceros o de otras funciones que la política actual prohíbe, la política puede relajarse.

:::{note}
¡Comprobar bien el contenido y los casos límite antes de relajar la política! Leer también la [documentación que ofrece MDN](https://developer.mozilla.org/en-US/docs/Web/Security/CSP/Introducing_Content_Security_Policy)
:::

Para relajar la política, se pasa una instancia de la clase ContentSecurityPolicy a la respuesta. Los métodos de la clase pueden encadenarse.

Los siguientes métodos desactivan funciones de seguridad al pasar **true** como parámetro **$isAllowed**

* **allowInlineScript** (bool $isAllowed)
* **allowInlineStyle** (bool $isAllowed)
* **allowEvalScript** (bool $isAllowed)
* **useStrictDynamic** (bool $isAllowed)

  Confiar en todos los scripts que carga un script de confianza; ver 'script-src' y 'strict-dynamic'

* **useStrictDynamicOnScripts** (bool $isAllowed)

  Confiar en todos los scripts que carga un script de confianza que se cargó mediante una etiqueta `<script>`; ver 'script-src-elem' **(activado de forma predeterminada)**

:::{note}
`useStrictDynamicOnScripts` está activado de forma predeterminada desde Nextcloud 28, para permitir que el JavaScript de módulos cargue sus dependencias mediante `import`. Se puede desactivar pasando **false** como parámetro.
:::

Los siguientes métodos agregan dominios a la lista de permitidos al pasar un dominio, o \* para cualquier dominio:

* **addAllowedScriptDomain** (string $domain)
* **addAllowedStyleDomain** (string $domain)
* **addAllowedFontDomain** (string $domain)
* **addAllowedImageDomain** (string $domain)
* **addAllowedConnectDomain** (string $domain)
* **addAllowedMediaDomain** (string $domain)
* **addAllowedObjectDomain** (string $domain)
* **addAllowedFrameDomain** (string $domain)
* **addAllowedChildSrcDomain** (string $domain)

La siguiente política, por ejemplo, permite imágenes, audio y video de otros dominios:

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\TemplateResponse;
use OCP\AppFramework\Http\ContentSecurityPolicy;

class PageController extends Controller {

    public function index() {
        $response = new TemplateResponse('myapp', 'main');
        $csp = new ContentSecurityPolicy();
        $csp->addAllowedImageDomain('*');
            ->addAllowedMediaDomain('*');
        $response->setContentSecurityPolicy($csp);
    }

}
```

[^1]: Aunque el nombre de la cabecera `OCS-APIRequest` sugiere que se aplica solo a los controladores OCS, desde NC 30 los métodos de los controladores clásicos también respetan esta cabecera.
    Hasta NC 30, los métodos de los controladores clásicos no respetaban la cabecera.
````
