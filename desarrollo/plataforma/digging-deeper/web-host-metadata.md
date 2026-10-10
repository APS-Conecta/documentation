---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo escribir y registrar manejadores para las peticiones HTTP a la ruta .well-known/* (RFC6415), con un ejemplo genérico y uno de webfinger."
---
(nc-dev-web-host-metadata)=
# Metadatos del host web

## Resumen

Esta página explica cómo una app responde a las peticiones HTTP a la ruta `.well-known/*`: escribir un manejador que implementa `IHandler`, cómo se encadenan los manejadores, un ejemplo genérico y uno de webfinger, y cómo registrarlo en el arranque. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/web_host_metadata.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La [RFC6415][RFC6415] define cómo los hosts web pueden exponer sus metadatos mediante recursos. A partir de Nextcloud 21, es posible registrar manejadores para las peticiones HTTP a la ruta `.well-known/*`.

### Escribir un manejador

Un manejador well-known es una clase sencilla que implementa la interfaz `\OCP\Http\WellKnown\IHandler`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Http\WellKnown;

class Handler implements IHandler {

    public function handle(string $service, IRequestContext $context, ?IResponse $previousResponse): ?IResponse {
        // the handler-specific logic
    }

}
```

La idea básica es que cada manejador se llama de forma consecutiva. Un manejador puede reaccionar a la petición y devolver un nuevo objeto de respuesta o modificar el del manejador anterior. El primer manejador recibe un `$previousResponse` nulo. El segundo manejador recibe lo que haya devuelto el primero, es decir, `null` o una instancia de `\OCP\Http\WellKnown\IResponse`.

#### Ejemplo de manejador genérico

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Http\WellKnown;

use OCP\AppFramework\Http\JSONResponse;
use OCP\Http\WellKnown\GenericResponse;
use OCP\Http\WellKnown\IHandler;
use OCP\Http\WellKnown\IRequestContext;
use OCP\Http\WellKnown\IResponse;
use OCP\IURLGenerator;

class GenericHandler implements IHandler {

    public function handle(string $service, IRequestContext $context, ?IResponse $previousResponse): ?IResponse {
        if ($service !== 'nextcloudtest') {
            // Not relevant to this handler

            return $previousResponse;
        }

        return new GenericResponse(
            new JSONResponse(['message' => 'hello']),
        );
    }
}
```

#### Ejemplo de manejador webfinger

El ejemplo siguiente muestra cómo una app podría reaccionar a las peticiones webfinger de la [RFC6415][RFC6415]:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Http\WellKnown;

use OCP\Http\WellKnown\IHandler;
use OCP\Http\WellKnown\IRequestContext;
use OCP\Http\WellKnown\IResponse;
use OCP\Http\WellKnown\JrdResponse;
use OCP\IURLGenerator;

class WebFingerHandler implements IHandler {

    /** @var IURLGenerator */
    private $urlGenerator;

    public function __construct(IURLGenerator $urlGenerator) {
        $this->urlGenerator = $urlGenerator;
    }

    public function handle(string $service, IRequestContext $context, ?IResponse $previousResponse): ?IResponse {
        if ($service !== 'webfinger') {
            // Not relevant to this handler

            return $previousResponse;
        }

        $subject = $context->getHttpRequest()->getParam('resource', '');
        $href = $this->urlGenerator->linkToRouteAbsolute('myapp.example.test');

        // Use the previous response and amend it, if possible
        $response = $previousResponse;
        if (!($response instanceof JrdResponse)) {
            // We override null or any other types
            $response = new JrdResponse($subject);
        }

        return $response->addLink('self', 'application/activity+json', $href);
    }
}
```

### Registro del manejador

La clase del manejador se registra mediante el {nc-ref}`mecanismo de arranque <Bootstrapping>` de la clase `Application`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCA\MyApp\Http\WellKnown\Handler;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;

class Application extends App implements IBootstrap {

    public function register(IRegistrationContext $context): void {
        $context->registerWellKnownHandler(Handler::class);
    }

    public function boot(IBootContext $context): void {}

}
```

[RFC6415]: https://tools.ietf.org/html/rfc6415
[RFC7033]: https://tools.ietf.org/html/rfc7033
````
