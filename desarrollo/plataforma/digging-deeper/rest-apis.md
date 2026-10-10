---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo ofrecer una API REST desde una app: ApiController y CORS, versionado en la URL, cabeceras CORS y comparación entre controladores REST y OCS."
---
(nc-dev-rest-apis)=
# API REST

## Resumen

Esta página explica cómo ofrecer una API REST desde una app con `ApiController` y el atributo `#[CORS]`, cómo versionarla y modificar las cabeceras CORS, y compara los controladores simples con los de OCS, incluidas las opciones históricas. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/rest_apis.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Ofrecer una API RESTful no es distinto de crear una {nc-doc}`ruta <developer_manual/basics/routing>` y {nc-doc}`controladores <developer_manual/basics/controllers>` para la interfaz web.
Sin embargo, se recomienda heredar de ApiController y agregar el atributo `#[CORS]` a los métodos para que [las aplicaciones web también puedan acceder a la API](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS).

```php
<?php
namespace OCA\MyApp\Controller;

use OCP\AppFramework\ApiController;
use OCP\AppFramework\Http\Attribute\CORS;
use OCP\IRequest;

class AuthorApiController extends ApiController {

    public function __construct($appName, IRequest $request) {
        parent::__construct($appName, $request);
    }

    #[CORS]
    public function index() {

    }

}
```

CORS también necesita una URL aparte para la solicitud de verificación previa **OPTIONS**, que se puede agregar fácilmente añadiendo la siguiente ruta:

```php
<?php
// appinfo/routes.php
array(
    'name' => 'author_api#preflighted_cors',
    'url' => '/api/1.0/{path}',
    'verb' => 'OPTIONS',
    'requirements' => array('path' => '.+')
)
```

Hay que tener en cuenta que es probable que varias apps dependan de la interfaz de la API una vez publicada, y que reaccionarán a distinta velocidad a los cambios implementados en la API.
Por eso se recomienda versionar la API en la URL para no romper las apps existentes cuando se introduzcan cambios incompatibles con versiones anteriores:

```
/index.php/apps/myapp/api/1.0/resource
```

### Modificar las cabeceras CORS

De forma predeterminada, se usarán los siguientes valores para la solicitud OPTIONS de verificación previa:

- **Access-Control-Allow-Methods**: 'PUT, POST, GET, DELETE, PATCH'
- **Access-Control-Allow-Headers**: 'Authorization, Content-Type, Accept'
- **Access-Control-Max-Age**: 1728000

Para agregar un método o una cabecera adicional, o para permitir menos cabeceras, basta con pasar valores adicionales al constructor padre:

```php
<?php
namespace OCA\MyApp\Controller;

use \OCP\AppFramework\ApiController;
use \OCP\IRequest;

class AuthorApiController extends ApiController {

    public function __construct($appName, IRequest $request) {
        parent::__construct(
            $appName,
            $request,
            'PUT, POST, GET, DELETE, PATCH',
            'Authorization, Content-Type, Accept',
            1728000);
    }

}
```

(nc-dev-ocs-vs-rest)=
### Relación entre REST y OCS

Existe una relación estrecha entre las API REST y {nc-ref}`OCS <ocscontroller>`.
Ambas proporcionan una forma de transmitir datos entre el backend de la app en el servidor Nextcloud y algún frontend.
Explícitamente, esto no trata de las {nc-ref}`respuestas de plantillas HTML <controller_html_responses>`.

#### Métodos actuales y comparación

Las siguientes combinaciones de atributos pueden ser relevantes para distintos escenarios:

1. Ruta de frontend simple: clase `Controller`
2. Ruta OCS: clase `OCSController`
3. Ruta OCS con CORS activado: clase `OCSController` y atributo `#[CORS]` en el método

:::{warning}
Agregar el atributo `#[NoCSRFRequired]` supone un riesgo de seguridad.
No se debe agregar a los métodos del controlador salvo que se comprendan las implicaciones y se tenga la certeza de que el atributo es absolutamente necesario.
Normalmente, en su lugar se puede usar la cabecera `OCS-APIRequest` en las solicitudes de datos, a fin de satisfacer las comprobaciones CSRF de las solicitudes a la API.
:::

:::{warning}
Agregar solo el atributo `#[CORS]` no basta para permitir el acceso mediante CORS con rutas de frontend simples.
Sin más medidas, el comprobador de CSRF fallaría.
Por eso, activar CORS en controladores simples se desaconseja de forma general y rotunda.

Habría que desactivar las comprobaciones CSRF (un riesgo de seguridad más), o usar la cabecera `OCP-APIRequest` o enviar un token CSRF para superar las comprobaciones.
Esto último requiere código JS específico en la página que importa.
:::

Hay distintas formas en que los clientes pueden interactuar con las API.
Estas formas dependen de la configuración de la API (lo que se permite) y de la ruta a la que finalmente se haga la solicitud.

- *Acceso desde el frontend web* significa que el usuario accede al frontend web de Nextcloud con un navegador web.
- *Acceso desde fuera del navegador* se da cuando el usuario accede al recurso o a la página usando algo que no es un navegador web, como una app de Android o un comando curl.
- *Acceso desde un sitio web externo* significa que el usuario navega por algún sitio web de terceros y en él aparecen datos del servidor Nextcloud.
  Para poder hacerlo, el otro sitio web tiene que incrustar/cargar/usar imágenes, datos JSON u otros recursos desde una URL que apunta al servidor Nextcloud.

:::{hint}
Lo expuesto aquí se refiere solo a las solicitudes de datos.
Si se piensa en {nc-ref}`métodos de controlador que sirven plantillas (HTML) <controller_html_responses>`, desactivar CSRF se considera aceptable.
:::

:::{list-table} Comparación de los distintos tipos de API
:header-rows: 1
:align: center

* - Descripción
  - Clase `Controller`
  - Clase `OCSController`
  - Clase `OCSController` y `CORS` en el método
* - Prefijo de URL (relativo al servidor)
  - `/apps/<appid>/`
  - `/ocs/v2.php/apps/<appid>/`
  - `/ocs/v2.php/apps/<appid>/`
* - Acceso desde el frontend web
  - sí
  - sí
  - sí
* - Acceso desde fuera del navegador
  - parcial [^1]
  - sí
  - sí
* - Acceso desde un sitio web externo
  - no
  - no
  - sí
* - Datos encapsulados
  - no
  - sí (JSON o XML)
  - sí (JSON o XML)
:::

Los métodos de las clases `Controller` pueden devolver objetos `DataResponse`, de forma similar a los métodos de la clase `OCSController`.
En los métodos de una clase `Controller`, los datos de esta respuesta se envían, p. ej., como JSON, tal como se proporcionan.
Básicamente, la salida es muy similar a lo que haría `json_encode`.
En cambio, el `OCSController` encapsula los datos en una envoltura externa que proporciona algo más de (meta)información.
Por ejemplo, en el nivel superior se transmite un código de estado (similar al código de estado HTTP).
Los datos reales se transmiten en la propiedad `data`.

Como regla general, se puede concluir que OCS ofrece una buena forma de cubrir la mayoría de los casos de uso, incluidas comprobaciones de seguridad suficientes.
La única excepción es cuando se quiere ofrecer una API para uso externo en la que hay que cumplir un esquema de API definido externamente.
En ese caso, la encapsulación que introduce OCS y las comprobaciones CSRF pueden ser un obstáculo.

#### Opciones históricas

:::{deprecated} 30
La información de esta sección es principalmente de referencia. No usar estos enfoques en código nuevo.
:::

Antes de Nextcloud 30, los métodos de las clases `Controller` simples no respetaban la cabecera `OCS-APIRequest`.
Por eso, para dar acceso a apps externas a este tipo de métodos de controlador, era necesario usar el atributo `#[NoCSRFRequired]` (o la anotación `@NoCSRFRequired` correspondiente).

Las siguientes combinaciones de atributos eran relevantes para distintos escenarios:

1. Ruta de frontend simple: clase `Controller`
2. Frontend simple con las comprobaciones CSRF desactivadas: clase `Controller` y atributo `#[NoCSRFRequired]` en el método
3. Ruta de frontend simple con CORS activado: clase `Controller` y atributos `#[CORS]` y `#[NoCSRFRequired]` en la ruta
4. Ruta OCS: clase `OCSController`
5. Ruta OCS con CORS activado: clase `OCSController` y atributo `#[CORS]` en el método

:::{hint}
Los dos escenarios en los que interviene el `OCSController` no han cambiado y, por tanto, la documentación actual indicada más arriba sigue siendo válida.
Por eso, estas opciones no se vuelven a considerar aquí, por simplicidad y para que la visión general sea más nítida.

Las advertencias sobre no usar `NoCSRFRequired` y `CORS` mencionadas en la sección de métodos actuales también son válidas aquí.
:::

:::{list-table} Comparación de los distintos tipos de API
:header-rows: 1
:align: center

* - Descripción
  - Clase `Controller`
  - Clase `Controller` con `NoCSRFRequired` en el método
  - Clase `Controller` con `NoCSRFRequired` y `CORS` en el método
* - Prefijo de URL (relativo al servidor)
  - `/apps/<appid>/`
  - `/apps/<appid>/`
  - `/apps/<appid>/`
* - Acceso desde el frontend web
  - sí
  - sí (riesgo de CSRF)
  - sí (riesgo de CSRF)
* - Acceso desde fuera del navegador
  - no
  - sí
  - sí
* - Acceso desde un sitio web externo
  - no
  - no
  - sí
* - Datos encapsulados
  - no
  - no
  - no
:::

[^1]: La app externa tiene que satisfacer las comprobaciones CSRF.
    Es decir, la cabecera de solicitud HTTP `OCS-APIRequest` tiene que estar establecida en `true`.
    Esto solo es posible a partir de Nextcloud 30; las versiones anteriores no respetan la cabecera.
````
