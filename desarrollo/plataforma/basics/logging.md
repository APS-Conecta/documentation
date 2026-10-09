---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo registrar mensajes desde una app con el logger PSR-3: niveles, interpolación, contexto, excepciones, archivos propios, eventos y registro de auditoría."
---
# Registro

## Resumen

Esta página explica cómo una app escribe en el registro con el logger PSR-3: su uso básico, los métodos y su equivalencia con los niveles de Nextcloud, la interpolación de mensajes, el array de contexto, el registro de excepciones, los archivos de registro propios, los datos estructurados, los eventos de registro y el registro de auditoría. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/logging.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud usa un logger {nc-ref}`PSR-3 <psr3>` (`Psr\Log\LoggerInterface`).
La forma recomendada de usarlo es mediante {nc-ref}`inyección de dependencias <dependency-injection>`.

### Uso básico

Se inyecta `Psr\Log\LoggerInterface` en la clase. Cuando el logger se resuelve desde el contenedor de una app, Nextcloud lo envuelve automáticamente para que cada mensaje de registro se atribuya a esa app: **no** hace falta pasar el nombre de la app:

```php
<?php
namespace OCA\MyApp\Service;

use Psr\Log\LoggerInterface;

class AuthorService {
    public function __construct(
        private LoggerInterface $logger,
    ) {
    }

    public function doSomething(): void {
        $this->logger->error('Something went wrong');
    }
}
```

:::{note}
Internamente, el contenedor de DI de cada app registra un `ScopedPsrLogger` que antepone `['app' => '<your-app-id>']` al contexto de cada llamada. No hace falta establecerlo manualmente.
:::

En los casos en que no se puede {nc-ref}`inyectar <dependency-injection>` un logger en una clase, se puede usar la función `\OCP\Log\logger` para obtener una instancia de logger. Como primer argumento hay que pasar el ID de la app.

```php
<?php

use function OCP\Log\logger;

logger('my_app')->warning('look, no dependency injection');
```

### Métodos de registro disponibles

El logger ofrece el conjunto completo de métodos PSR-3:

- `emergency()`: el sistema no se puede usar
- `alert()`: hay que actuar de inmediato
- `critical()`: condiciones críticas
- `error()`: errores en tiempo de ejecución
- `warning()`: sucesos excepcionales que no son errores
- `notice()`: eventos normales pero significativos
- `info()`: eventos de interés (p. ej., un usuario inicia sesión)
- `debug()`: información de depuración detallada

Cada método tiene la firma `(string|\Stringable $message, array $context = []): void`.

### Equivalencia de niveles de registro

PSR-3 define ocho niveles de gravedad, pero internamente Nextcloud usa cinco niveles numéricos (que se fijan con el ajuste `loglevel` en `config.php`). La equivalencia es:

| Nivel PSR-3 | Nivel de Nextcloud | Valor numérico |
|---|---|---|
| `emergency` | FATAL | 4 |
| `alert`, `critical`, `error` | ERROR | 3 |
| `warning` | WARN | 2 |
| `notice`, `info` | INFO | 1 |
| `debug` | DEBUG | 0 |

Un mensaje se escribe en el registro solo cuando su nivel numérico es **≥** el `loglevel` configurado (predeterminado: `2` / WARN).

### Interpolación de mensajes

Nextcloud admite la interpolación de mensajes de PSR-3. Los valores del contexto cuyas claves aparecen como marcadores `{placeholder}` en la cadena del mensaje se sustituyen automáticamente:

```php
$this->logger->warning('User {user} failed to log in', [
    'user' => $userId,
]);
```

Esto produce un mensaje de registro como `User jane failed to log in`. La clave `user` la consume la interpolación y no aparecerá por separado en la entrada de registro almacenada.

### Array de contexto

El segundo argumento de todos los métodos de registro es un array de contexto. Nextcloud reconoce varias claves especiales:

- `exception`: si el contexto contiene una clave `exception` cuyo valor es un `\Throwable`, Nextcloud serializará la excepción completa (nombre de la clase, mensaje, código, archivo, línea, traza de la pila y cualquier excepción previa). **Esta es la forma recomendada de registrar excepciones:**

  ```php
  try {
      $this->doRiskyThing();
  } catch (\Exception $e) {
      $this->logger->error('Operation failed', ['exception' => $e]);
  }
  ```

  Se puede proporcionar un mensaje personalizado como primer argumento; si se omite, se usa el propio mensaje de la excepción.

- `app`: identifica la app que produjo el mensaje. Se **establece automáticamente** cuando el logger se obtiene mediante inyección de dependencias o con el asistente `logger()`. Si hace falta, se puede reemplazar explícitamente:

  ```php
  $this->logger->info('Cross-app note', ['app' => 'other_app']);
  ```

Cualquier otra clave que se agregue al array de contexto se incluye en la entrada de registro como dato adicional:

```php
$this->logger->info('Cron job finished', [
    'duration' => $seconds,
    'items_processed' => $count,
]);
```

### Registrar excepciones

Como se mostró arriba, pasar una clave `exception` en el contexto activa la serialización detallada de la excepción. Es preferible a llamar manualmente a `$e->getMessage()`, porque Nextcloud capturará la traza de la pila completa y la cadena de excepciones previas.

```php
try {
    $this->service->process($data);
} catch (\OCP\DB\Exception $e) {
    $this->logger->error('Database operation failed for item {id}', [
        'id' => $itemId,
        'exception' => $e,
    ]);
}
```

Se puede combinar la interpolación de mensajes con el registro de excepciones: Nextcloud gestiona ambas cosas.

### Archivo de registro personalizado

Si la app necesita escribir en un **archivo de registro aparte** (por ejemplo, para mantener la salida de depuración detallada fuera del registro principal), se puede usar `OCP\Log\ILogFactory::getCustomPsrLogger()`:

```php
<?php
namespace OCA\MyApp\Service;

use OCP\Log\ILogFactory;
use Psr\Log\LoggerInterface;

class ImportService {
    private LoggerInterface $importLogger;

    public function __construct(ILogFactory $logFactory) {
        $this->importLogger = $logFactory->getCustomPsrLogger(
            '/var/log/nextcloud/import.log'
        );
    }

    public function run(): void {
        $this->importLogger->info('Import started');
    }
}
```

La firma del método es:

```php
public function getCustomPsrLogger(
    string $path,
    string $type = 'file',
    string $tag = 'Nextcloud'
): LoggerInterface;
```

`$type` puede ser `file` (predeterminado), `errorlog`, `syslog` o `systemd`.

:::{note}
`getCustomPsrLogger` está disponible desde Nextcloud 22. Los parámetros `$type` y `$tag` se agregaron en Nextcloud 24.
:::

### Registro de datos estructurados

Para casos de uso avanzados, el logger también implementa `OCP\Log\IDataLogger` (desde Nextcloud 18.0.1), que ofrece un método `logData()` para registrar datos estructurados arbitrarios:

```php
use OCP\Log\IDataLogger;

/** @var IDataLogger $logger */
$logger = \OCP\Server::get(\Psr\Log\LoggerInterface::class);
$logger->logData('Sync completed', [
    'provider' => 'caldav',
    'items' => 42,
], [
    'app' => 'my_app',
    'level' => \OCP\ILogger::INFO,
]);
```

El primer argumento es una cadena con el mensaje, el segundo es el array de datos estructurados y el tercero es un array de contexto opcional (que acepta las claves `app` y `level` descritas arriba).

### Escuchar los eventos de registro

Si la app necesita reaccionar cuando se escriben mensajes de registro (p. ej., para reenviarlos a un servicio de monitorización externo), puede escuchar el evento `OCP\Log\BeforeMessageLoggedEvent` (desde Nextcloud 28):

```php
<?php
namespace OCA\MyApp\Listener;

use OCP\EventDispatcher\Event;
use OCP\EventDispatcher\IEventListener;
use OCP\Log\BeforeMessageLoggedEvent;

/** @template-implements IEventListener<BeforeMessageLoggedEvent> */
class LogEventListener implements IEventListener {
    public function handle(Event $event): void {
        if (!$event instanceof BeforeMessageLoggedEvent) {
            return;
        }

        $app = $event->getApp();
        $level = $event->getLevel();
        $message = $event->getMessage(); // array with the log entry
        // ... forward to external service
    }
}
```

El listener se registra en el método `Application::register()`:

```php
$context->registerEventListener(
    BeforeMessageLoggedEvent::class,
    LogEventListener::class
);
```

### Registro de auditoría de administración

Si se quiere registrar cosas no tanto para la administración del sistema sino por motivos de cumplimiento normativo (p. ej., quién accedió a qué archivo, quién cambió la contraseña de un elemento o lo hizo público), el [registro de auditoría de administración](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/logging_configuration.html#admin-audit-log) es el lugar adecuado.

Se puede agregar fácilmente una entrada de registro con solo emitir un evento `OCP\Log\Audit\CriticalActionPerformedEvent`:

```php
<?php

$dispatcher = \OCP\Server::get(\OCP\EventDispatcher\IEventDispatcher::class);

$event = new \OCP\Log\Audit\CriticalActionPerformedEvent(
    'My critical action for app %s',
    ['name' => 'My App ID']
);
$dispatcher->dispatchTyped($event);
```

El constructor también acepta un tercer parámetro opcional, `bool $obfuscateParameters = false`. Se establece en `true` cuando los parámetros pueden contener información sensible (contraseñas, tokens, etc.) que no debe escribirse en texto claro en el registro de auditoría:

```php
$event = new \OCP\Log\Audit\CriticalActionPerformedEvent(
    'Password changed for user %s',
    ['name' => $userId],
    true  // obfuscate parameters in the audit log
);
```
````
