---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Utilidades de seguridad para apps: limitar la frecuencia de operaciones con ILimiter, validar hosts remotos y comprobar dominios de confianza."
---
(nc-dev-security)=
# Seguridad

## Resumen

Esta página describe tres utilidades de seguridad que una app puede inyectar: la limitación de frecuencia con `ILimiter`, la validación de hosts remotos con `IRemoteHostValidator` y la comprobación de dominios de confianza con `ITrustedDomainHelper`. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/security.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
(nc-dev-programmatic-rate-limiting)=
### Limitación de frecuencia

La limitación de frecuencia se puede usar para restringir con qué frecuencia alguien puede ejecutar una operación en un intervalo de tiempo definido. Para los controladores del framework de apps, se recomienda usar los atributos de limitación de frecuencia.

Fuera de los controladores, p. ej., en código DAV, también es posible proteger las operaciones {nc-ref}`inyectando <dependency-injection>` `\OCP\Security\RateLimiting\ILimiter` y registrando las solicitudes *antes* de la operación:

```php
<?php

use OCP\Security\RateLimiting\ILimiter;

class MyDavPlugin {
    private ILimiter $limiter;

    public function __construct(ILimiter $limiter) {
        $this->limiter = $limiter;
    }

    public function calledAnonymously(): void {
        try {
            $this->limiter->registerAnonRequest(
                'my-dav-plugin-anon',
                5, // Allow five executions …
                60 * 60, // … per hour
            );
        } catch (IRateLimitExceededException $exception) {
            // Respond with a HTTP 429 error
        }

        // No rate limiting reached. Carry on.
    }

    public function calledByUser(IUser $user): void {
        try {
            $this->limiter->registerUserRequest(
                'my-dav-plugin-user',
                5, // Allow five executions …
                60 * 60, // … per hour
                $user
            );
        } catch (IRateLimitExceededException $exception) {
            // Respond with a HTTP 429 error
        }

        // No rate limiting reached. Carry on.
    }
}
```

### Validación de hosts remotos

Nextcloud puede ayudar a validar un host remoto para que no se contacte con infraestructura interna a partir de nombres de host o IP proporcionados por usuarios. El validador `\OCP\Security\IRemoteHostValidator` puede {nc-ref}`inyectarse <dependency-injection>` en cualquier clase de la app:

```php
<?php

use OCP\Security\IRemoteHostValidator;

class MyRemoteServerIntegration {
    private IRemoteHostValidator $hostValidator;

    public function __construct(IRemoteHostValidator $hostValidator) {
        $this->hostValidator = $hostValidator;
    }

    public function contactRemoteServer(string $hostname): void {
        if (!$this->hostValidator->isValid($hostname)) {
            // ABORT
        }

        // Contact the server
    }
}
```

:::{note}
Los clientes HTTP de Nextcloud obtenidos de `\OCP\Http\Client\IClientService` tienen esta validación integrada, por lo que no hay que comprobar los hosts de las solicitudes HTTP mientras se use esta abstracción proporcionada.
:::

### Dominio de confianza

En algunos casos puede ser necesario que una app compruebe que un enlace proporcionado por un usuario pertenece a la instancia actual.
Esto es posible con `OCP\Security\ITrustedDomainHelper`:

```php
<?php

declare(strict_types=1);
use OCP\Security\ITrustedDomainHelper;

$helper = \OC::$server->get(ITrustedDomainHelper::class);

// Compare a full URL example given
$url = 'https://localhost/nextcloud/index.php/apps/files/';
$helper->isTrustedUrl($url);

// Compare a domain and port
$domain = 'example.tld:8443';
$helper->isTrustedDomain($domain);
```
````
