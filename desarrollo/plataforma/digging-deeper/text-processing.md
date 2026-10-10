---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo consumir la API de Procesamiento de texto de OCP: tipos de tarea, tareas, estados y eventos, y cómo implementar y registrar un proveedor."
---
(nc-dev-text_processing)=
# Procesamiento de texto

## Resumen

Esta página explica la API de Procesamiento de texto, obsoleta desde la versión 30 en favor de la API de TaskProcessing: sus tipos de tarea, cómo ejecutar o programar tareas, sus estados y sus eventos, y cómo implementar y registrar un proveedor, con contexto de usuario y tiempo de ejecución esperado. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/text_processing.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 27.1.0
:::

:::{deprecated} 30
Usar en su lugar la API de TaskProcessing
:::

Nextcloud ofrece una API de **Procesamiento de texto**. La idea general es que existe una API central de OCP que las apps pueden usar para enviar tareas a modelos de lenguaje de gran tamaño y a herramientas similares de procesamiento de texto. Para no depender de ninguna tecnología, cualquier app puede proporcionar esta funcionalidad registrando proveedores de Procesamiento de texto.

### Consumir la API de Procesamiento de texto

Para consumir la API de modelos de lenguaje, hay que {nc-ref}`inyectar <dependency-injection>` `\OCP\TextProcessing\IManager`. Este gestor ofrece los siguientes métodos:

- `hasProviders()` Este método devuelve un booleano que indica si se ha registrado algún proveedor. Si es false, no se puede usar la función TextProcessing.
- `getAvailableTaskTypes()` Este método devuelve una lista de cadenas de clase que representan las tareas que se admiten actualmente.
- `runTask(Task $task)` Este método proporciona la funcionalidad de prompt propiamente dicha. La tarea se define con la clase Task. Este método ejecuta la tarea de forma síncrona, así que, según la implementación, no se sabe con certeza cuánto tardará (entre 3 s y 10 min).
- `scheduleTask(Task $task)` Este método proporciona la funcionalidad de prompt propiamente dicha. La tarea se define con la clase Task. Este método ejecuta la tarea de forma asíncrona, en un trabajo en segundo plano.
- `getTask(int $id)` Este método obtiene una tarea indicada por su id.

:::{versionadded} 28.0.0
- `runOrScheduleTask(Task $task)` Este método también ejecuta una tarea, pero primero comprueba el tiempo de ejecución esperado del proveedor que se va a usar. Si el tiempo de ejecución cabe en el tiempo de procesamiento disponible para la petición actual, la tarea se ejecuta de forma síncrona; si no, se programa como trabajo en segundo plano. La tarea se define con la clase Task.
:::

Si se quiere usar la funcionalidad de procesamiento de texto en un cliente, también hay endpoints de OCS disponibles para ello: {nc-ref}`API de procesamiento de texto de OCS <ocs-textprocessing-api>`

#### Tipos de tareas

Están disponibles los siguientes tipos de tareas:

- `\OCP\TextProcessing\FreePromptTaskType`: esta tarea permite pasar un prompt arbitrario al modelo de lenguaje.
- `\OCP\TextProcessing\HeadlineTaskType`: esta tarea generará un titular para el texto de entrada recibido.
- `\OCP\TextProcessing\TopicsTaskType`: esta tarea generará una lista de temas separados por comas para el texto de entrada recibido.
- `\OCP\TextProcessing\SummaryTaskType`: esta tarea resumirá el texto de entrada recibido.

#### Tareas

Para crear una tarea se usa la clase `\OCP\TextProcessing\Task`. Su constructor recibe los siguientes argumentos: `new \OCP\TextProcessing\Task(string $type, string $input, string $appId, ?string $userId, string $identifier = '')`. Por ejemplo:

```php
if (in_array(SummaryTaskType::class, $textprocessingManager->getAvailableTaskTypes()) {
    $summaryTask = new Task(SummaryTaskType::class, $emailText, "my_app", $userId, (string) $emailId);
} else {
    // cannot use summarization
}
```

Los objetos de la clase Task tienen disponibles los siguientes métodos:

- `getType()` Esto devuelve el tipo de tarea.
- `getStatus()` Este método devuelve uno de los estados indicados más abajo.
- `getId()` Este método devolverá `null` antes de que la tarea se haya pasado a `runTask` o a `scheduleTask`
- `getInput()` Esto devuelve la cadena de entrada.
- `getOutput()` Este método devolverá `null` salvo que la tarea tenga éxito
- `getAppId()` Esto devuelve el ID de la aplicación que originó la tarea.
- `getIdentifier()` Esto devuelve el identificador original de la tarea, definido por quien la programó
- `getUserId()` Esto devuelve el ID del usuario que originó la tarea.

Ahora se podría ejecutar la tarea directamente de la siguiente manera. Sin embargo, esto bloqueará el proceso PHP actual hasta que la tarea termine, lo que a veces puede tardar decenas de minutos, según el proveedor que se use.

```php
try {
    $textprocessingManager->runTask($summaryTask);
} catch (\OCP\PreConditionNotMetException|\OCP\TextProcessing\Exception\TaskFailureException $e) {
    // task failed
    // return error
}
// task was successful
```

La opción más sensata, cuando se está en el contexto de un controlador HTTP, es programar la tarea para que se ejecute en un trabajo en segundo plano, de la siguiente manera:

```php
try {
    $textprocessingManager->scheduleTask($summaryTask);
} catch (\OCP\PreConditionNotMetException|\OCP\DB\Exception $e) {
    // scheduling task failed
}
// task was scheduled successfully
```

##### Programación condicional de tareas

:::{versionadded} 28.0.0
:::

Por supuesto, puede que se quiera programar la tarea en un trabajo en segundo plano **solo** si tarda más que el tiempo de espera de la petición. Eso es lo que hace `runOrScheduleTask`.

```php
try {
    $textprocessingManager->runOrScheduleTask($summaryTask);
} catch (\OCP\PreConditionNotMetException|\OCP\DB\Exception $e) {
    // scheduling task failed
    // return error
} catch (\OCP\TextProcessing\Exception\TaskFailureException $e) {
    // task was run but failed
    // status will be STATUS_FAILED
    // return error
}

switch ($summaryTask->getStatus()) {
    case \OCP\TextProcessing\Task::STATUS_SUCCESSFUL:
        // task was run directly and was successful
    case \OCP\TextProcessing\Task::STATUS_RUNNING:
    case \OCP\TextProcessing\Task::STATUS_SCHEDULED:
        // task was deferred to background job
    default:
        // something went wrong
}
```

#### Estados de las tareas

Todas las tareas tienen siempre uno de los siguientes estados:

```php
Task::STATUS_FAILED = 4;
Task::STATUS_SUCCESSFUL = 3;
Task::STATUS_RUNNING = 2;
Task::STATUS_SCHEDULED = 1;
Task::STATUS_UNKNOWN = 0;
```

#### Escuchar los eventos de procesamiento de texto

Como `scheduleTask` no bloquea, habrá que escuchar los siguientes eventos en la app para obtener la salida o recibir aviso de cualquier fallo.

- `OCP\TextProcessing\Events\TaskSuccessfulEvent` Esta clase de evento ofrece el método `getTask()`, que devuelve el objeto de la tarea actualizado, con la salida del modelo.
- `OCP\TextProcessing\Events\TaskFailedEvent` Además del método `getTask()`, esta clase de evento proporciona el método `getErrorMessage()`, que devuelve el mensaje de error como una cadena (solo en inglés y con fines de depuración, así que no se debe mostrar al usuario)

Por ejemplo, en el archivo `lib/AppInfo/Application.php`:

```php
$context->registerEventListener(OCP\TextProcessing\Events\TaskSuccessfulEvent::class, MyPromptResultListener::class);
$context->registerEventListener(OCP\TextProcessing\Events\TaskFailedEvent::class, MyPromptResultListener::class);
```

La clase `MyPromptResultListener` correspondiente puede tener este aspecto:

```php
<?php
namespace OCA\MyApp\Listener;

use OCA\MyApp\AppInfo\Application;
use OCP\TextProcessing\Events\AbstractTextProcessingEvent;
use OCP\TextProcessing\Events\TaskSuccessfulEvent;
use OCP\TextProcessing\Events\TaskFailedEvent;
use OCP\EventDispatcher\Event;
use OCP\EventDispatcher\IEventListener;

class MyPromptResultListener implements IEventListener {
    public function handle(Event $event): void {
        if (!$event instanceof AbstractTextProcessingEvent || $event->getTask()->getAppId() !== Application::APP_ID) {
            return;
        }

        if ($event instanceof TaskSuccessfulEvent) {
            $output = $event->getTask()->getOutput()
            // store $output somewhere
        }

        if ($event instanceof TaskFailedEvent) {
            $error = $event->getErrorMessage()
            $userId = $event->getTask()->getUserId()
            // Notify relevant user about failure
        }
    }
}
```

### Implementar un proveedor de TextProcessing

Un **proveedor de procesamiento de texto** es una clase que implementa la interfaz `OCP\TextProcessing\IProvider`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\TextProcessing;

use OCA\MyApp\AppInfo\Application;
use OCP\Files\File;
use OCP\TextProcessing\IProvider;
use OCP\TextProcessing\SummaryTaskType;
use OCP\IL10N;

class Provider implements IProvider {

    public function __construct(
        private IL10N $l,
    ) {
    }

    public function getName(): string {
        return $this->l->t('My awesome text processing provider');
    }

    public function getTaskType(): string {
        return SummaryTaskType::class;
    }

    public function process(string $input): string {
        // Return the output here
    }
}
```

El método `getName` devuelve una cadena que identifica al proveedor registrado en la interfaz de usuario.

El método `process` implementa el paso de procesamiento de texto; p. ej., pasa el prompt a un modelo de lenguaje. Si la ejecución falla por algún motivo, se debe lanzar una `RuntimeException` con un mensaje de error explicativo.

La clase normalmente se guardaría en un archivo en `lib/TextProcessing` de la app, pero se puede colocar en otro lugar siempre que el {nc-ref}`contenedor de inyección de dependencias <dependency-injection>` de Nextcloud pueda cargarla.

#### Procesar tareas en el contexto de un usuario

:::{versionadded} 28.0.0
:::

A veces el procesamiento de una tarea de procesamiento de texto puede depender de qué usuario la solicitó. Ahora se puede obtener esta información en el proveedor implementando además la interfaz `OCP\TextProcessing\IProviderWithUserId`:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\TextProcessing;

use OCA\MyApp\AppInfo\Application;
use OCP\Files\File;
use OCP\TextProcessing\IProvider;
use OCP\TextProcessing\IProviderWithUserId;
use OCP\TextProcessing\SummaryTaskType;
use OCP\IL10N;

class Provider implements IProvider, IProviderWithUserId {

    private ?string $userId = null;

    public function __construct(
        private IL10N $l,
    ) {
    }

    public function getName(): string {
        return $this->l->t('My awesome text processing provider');
    }

    public function getTaskType(): string {
        return SummaryTaskType::class;
    }

    public function setUserId(?string $userId): void {
        $this->userId = $userId;
    }

    public function process(string $input): string {
        // Return the output here, making use of $this->userId
    }
}
```

#### Agilizar el procesamiento para proveedores rápidos

:::{versionadded} 28.0.0
:::

Los consumidores posteriores de la API de TextProcessing pueden optimizar la ejecución de las tareas si saben cuánto tiempo se ejecutará una tarea con el proveedor. Para permitir este tipo de optimización, se puede proporcionar una estimación de cuánto tiempo suele tardar el proveedor. Para ello, basta con implementar la interfaz adicional `OCP\TextProcessing\IProviderWithExpectedRuntime`

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\TextProcessing;

use OCA\MyApp\AppInfo\Application;
use OCP\Files\File;
use OCP\TextProcessing\IProvider;
use OCP\TextProcessing\IProviderWithExpectedRuntime;
use OCP\TextProcessing\SummaryTaskType;
use OCP\IL10N;

class Provider implements IProvider, IProviderWithExpectedRuntime {

    public function __construct(
        private IL10N $l,
    ) {
    }

    public function getName(): string {
        return $this->l->t('My awesome text processing provider');
    }

    public function getTaskType(): string {
        return SummaryTaskType::class;
    }

    public function getExpectedRuntime(): int {
        return 10; // expected runtime of a task is 10s
    }

    public function process(string $input): string {
        // Return the output here
    }
}
```

#### Proporcionar más tipos de tareas

Si se quiere implementar proveedores que gestionen tipos de tareas adicionales, se pueden crear clases TaskType propias que implementen la interfaz `OCP\TextProcessing\ITaskType`:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\TextProcessing;

use OCA\MyApp\AppInfo\Application;
use OCP\Files\File;
use OCP\TextProcessing\ITaskType;
use OCP\IL10N;

class OscarWildeTaskType implements ITaskType {

     public function __construct(
        private IL10N $l,
    ) {
    }

    public function getName(): string {
        return $this->l->t('Oscar Wilde Generator');
    }

    public function getDescription(): string {
      return $this->l->t('Turn text into Oscar Wilde prose');
    }
}
```

### Registro del proveedor

La clase del proveedor se registra mediante el {nc-ref}`mecanismo de arranque <bootstrapping>` de la clase `Application`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCA\MyApp\TextProcessing\Provider;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;

class Application extends App implements IBootstrap {

    public function register(IRegistrationContext $context): void {
        $context->registerTextProcessingProvider(Provider::class);
    }

    public function boot(IBootContext $context): void {}

}
```
````
