---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo obtener un cliente HTTP con IClientService, enviar solicitudes HEAD, GET, POST, PUT, DELETE y OPTIONS y manejar sus errores."
---
# Cliente HTTP

## Resumen

Esta página explica cómo usar el cliente HTTP integrado para enviar solicitudes a otros servidores web: cómo obtenerlo con la factoría `IClientService`, un ejemplo de cada tipo de solicitud y cómo manejar los errores. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/http_client.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud incluye un cliente HTTP sencillo que puede usarse para enviar solicitudes a otros servidores web. Este cliente respeta la configuración, las restricciones de seguridad y los ajustes de proxy de Nextcloud.

### Obtener un cliente HTTP

Las instancias del cliente HTTP se construyen con la [factoría](https://en.wikipedia.org/wiki/Factory_(object-oriented_programming)) del servicio de cliente, `IClientService`. La factoría puede {nc-ref}`inyectarse <dependency-injection>` en cualquier clase de la app:

```php
<?php

use OCP\Http\Client\IClientService;

class MyRemoteServerIntegration {
    private IClientService $clientService;
    public function __construct(IClientService $clientService) {
        $this->clientService = $clientService;
    }

    public function downloadNextcloudWebsite(): void {
        $client = $this->clientService->newClient();
        $response = $client->get('https://nextcloud.com');
        $body = $response->getBody();
    }
}
```

### Solicitud HEAD

```php
<?php

$client = $this->clientService->newClient();
$response = $client->head('https://nextcloud.com');
$body = $response->getBody();
```

### Solicitud GET

```php
<?php

$client = $this->clientService->newClient();
$response = $client->get('https://nextcloud.com');
$body = $response->getBody();
```

### Solicitud POST

```php
<?php

$client = $this->clientService->newClient();
$response = $client->post('https://api.domain.tld/pizza', [
    'headers' => [
        'Accept' => 'application/json',
        'Content-Type' => 'application/json',
    ],
    'body' => json_encode([
        'toppings' => [
            'cheese',
            'pineapple',
        ],
    ])
]);
$pizza = json_decode($response->getBody(), true);
```

### Solicitud PUT

```php
<?php

$client = $this->clientService->newClient();
$response = $client->put('https://api.domain.tld/pizza/42', [
    'headers' => [
        'Accept' => 'application/json',
        'Content-Type' => 'application/json',
    ],
    'body' => json_encode([
        'toppings' => [
            'cheese',
            'pineapple',
        ],
    ])
]);
$pizza = json_decode($response->getBody(), true);
```

### Solicitud DELETE

```php
<?php

$client = $this->clientService->newClient();
$response = $client->delete('https://api.domain.tld/pizza/42');
```

### Solicitud OPTIONS

```php
<?php

$client = $this->clientService->newClient();
$response = $client->options('https://nextcloud.com');
$status = $response->getStatusCode();
$allHeaders = $response->getHeaders();
$contentType = $response->getHeader('content-type');
```

### Manejo de errores

Los errores se señalan con excepciones. Capturar la `Exception` base de PHP.

```php
<?php

use Exception;

$client = $this->clientService->newClient();
try {
    $response = $client->options('https://nextcloud.com');
} catch (\Exception $e) {
    // Handle the error
}
```
````
