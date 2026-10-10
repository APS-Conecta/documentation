---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo consumir la API de Texto a imagen de OCP: tareas, estados y eventos, y cómo implementar y registrar un proveedor de Texto a imagen."
---
(nc-dev-text2image)=
# Texto a imagen

## Resumen

Esta página explica la API de Texto a imagen, obsoleta desde la versión 30 en favor de la API de TaskProcessing: cómo consumirla con tareas síncronas o programadas, sus estados y sus eventos, y cómo implementar y registrar un proveedor de Texto a imagen. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/text2image.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 28
:::

:::{deprecated} 30
Usar en su lugar la API de TaskProcessing
:::

Nextcloud ofrece una API de **Texto a imagen**. La idea general es que existe una API central de OCP que las apps pueden usar para enviar tareas a modelos de IA de difusión latente y a herramientas similares de generación de imágenes. Para no depender de ninguna tecnología, cualquier app puede proporcionar esta funcionalidad registrando un proveedor de Texto a imagen.

### Consumir la API de Texto a imagen

Para consumir la API de Texto a imagen, hay que {nc-ref}`inyectar <dependency-injection>` `\OCP\TextToImage\IManager`. Este gestor ofrece los siguientes métodos:

- `hasProviders()` Este método devuelve un booleano que indica si se ha registrado algún proveedor. Si es false, no se puede usar la función de generación de imágenes.
- `runTask(Task $task)` Este método proporciona la funcionalidad propiamente dicha. La tarea se define con la clase Task. Este método ejecuta la tarea de forma síncrona, así que, según la implementación, no se sabe con certeza cuánto tardará (entre 3 s y varias horas).
- `scheduleTask(Task $task)` Este método también ejecuta una tarea, pero de forma asíncrona, en un trabajo en segundo plano. La tarea se define con la clase Task.
- `runOrScheduleTask(Task $task)` Este método también ejecuta una tarea, pero primero comprueba el tiempo de ejecución esperado del proveedor que se va a usar. Si el tiempo de ejecución cabe en el tiempo de procesamiento disponible para la petición actual, la tarea se ejecuta de forma síncrona; si no, se programa como trabajo en segundo plano. La tarea se define con la clase Task.
- `getTask(int $id)` Este método obtiene una tarea indicada por su id.
- `getUserTask(int $id, ?string $userId)` Este método obtiene una tarea indicada por su id y por el usuario asociado a ella.
- `getUserTasksByApp(?string $userId, string $appId, ?string $identifier = null)` Este método obtiene las tareas de un usuario creadas por una app concreta (opcionalmente, también se puede indicar el identificador de la tarea como filtro adicional)

Si se quiere usar la funcionalidad de generación de imágenes en un cliente, también hay endpoints de OCS disponibles para ello: {nc-ref}`API de texto a imagen de OCS <ocs-text2image-api>`

#### Tareas

Para crear una tarea se usa la clase `\OCP\TextToImage\Task`. Su constructor recibe los siguientes argumentos: `new \OCP\TextToImage\Task(string $input, string $appId, int $numberOfImages, ?string $userId, string $identifier = '')`. Por ejemplo:

```php
$text2imageTask = new Task($documentTitle, "my_app", 8, $userId, (string) $documentId);
```

Los objetos de la clase Task tienen disponibles los siguientes métodos:

- `getStatus()` Este método devuelve uno de los estados indicados más abajo.
- `getId()` Este método devolverá `null` antes de que la tarea se haya pasado a `runTask` o a `scheduleTask`; en caso contrario, devolverá un entero
- `getInput()` Esto devuelve la cadena de entrada.
- `getAppId()` Esto devuelve el ID de la aplicación que originó la tarea.
- `getNumberOfImages()` Esto devuelve el número de imágenes generadas para la tarea.
- `getIdentifier()` Esto devuelve el identificador original de la tarea, definido por quien la programó
- `getUserId()` Esto devuelve el ID del usuario que originó la tarea.
- `getOutputImages()` Este método devolverá `null` salvo que la tarea tenga éxito; si lo tiene, devolverá una lista de objetos `IImage`

Se podría ejecutar la tarea directamente de la siguiente manera. Sin embargo, esto bloqueará el proceso PHP actual hasta que la tarea termine, lo que a veces puede tardar decenas de minutos, según el proveedor que se use.

```php
try {
    $text2imageManager->runTask($text2imageTask);
} catch (\OCP\PreConditionNotMetException|\OCP\TextToImage\Exception\TaskFailureException $e) {
    // task failed
    // return error
}
// task was successful
```

La opción más sensata, cuando se está en el contexto de un controlador HTTP, es programar la tarea para que se ejecute en un trabajo en segundo plano, de la siguiente manera:

```php
try {
    $text2imageManager->scheduleTask($text2imageTask);
} catch (\OCP\PreConditionNotMetException|\OCP\DB\Exception $e) {
    // scheduling task failed
}
// task was scheduled successfully
```

Por supuesto, puede que se quiera programar la tarea en un trabajo en segundo plano **solo** si tarda más que el tiempo de espera de la petición. Eso es lo que hace runOrScheduleTask.

```php
try {
    $text2imageManager->runOrScheduleTask($text2imageTask);
} catch (\OCP\PreConditionNotMetException|\OCP\DB\Exception $e) {
    // scheduling task failed
    // return error
} catch (\OCP\TextToImage\Exception\TaskFailureException $e) {
    // task was run but failed
    // status will be STATUS_FAILED
    // return error
}

switch ($text2imageTask->getStatus()) {
case \OCP\TextToImage\Task::STATUS_SUCCESSFUL:
    // task was run directly and was successful
case \OCP\TextToImage\Task::STATUS_RUNNING:
case \OCP\TextToImage\Task::STATUS_SCHEDULED:
    // task was deferred to background job
default:
    // something went wrong
}
```

#### Estados de las tareas

(nc-dev-text2image_statuses)=

Todas las tareas tienen siempre uno de los siguientes estados:

```php
Task::STATUS_FAILED = 4;
Task::STATUS_SUCCESSFUL = 3;
Task::STATUS_RUNNING = 2;
Task::STATUS_SCHEDULED = 1;
Task::STATUS_UNKNOWN = 0;
```

#### Escuchar los eventos de generación de imágenes

Como `scheduleTask` no bloquea, habrá que escuchar los siguientes eventos en la app para obtener las imágenes resultantes o recibir aviso de cualquier fallo.

- `OCP\TextToImage\Events\TaskSuccessfulEvent` Esta clase de evento ofrece el método `getTask()`, que devuelve el objeto de la tarea actualizado, con la salida del modelo.
- `OCP\TextToImage\Events\TaskFailedEvent` Además del método `getTask()`, esta clase de evento proporciona el método `getErrorMessage()`, que devuelve el mensaje de error como una cadena (solo en inglés y con fines de depuración, así que no se debe mostrar al usuario)

Por ejemplo, en el archivo `lib/AppInfo/Application.php`:

```php
$context->registerEventListener(OCP\TextToImage\Events\TaskSuccessfulEvent::class, ImageGenerationResultListener::class);
$context->registerEventListener(OCP\TextToImage\Events\TaskFailedEvent::class, ImageGenerationResultListener::class);
```

La clase `ImageGenerationResultListener` correspondiente podría tener el siguiente aspecto:

```php
<?php
declare(strict_types=1);

namespace OCA\MyApp\Listener;

use OCA\MyApp\AppInfo\Application;
use OCP\TextToImage\Events\AbstractTextToImageEvent;
use OCP\TextToImage\Events\TaskSuccessfulEvent;
use OCP\TextToImage\Events\TaskFailedEvent;
use OCP\EventDispatcher\Event;
use OCP\EventDispatcher\IEventListener;

class ImageGenerationResultListener implements IEventListener {
    public function handle(Event $event): void {
        if (!$event instanceof AbstractTextProcessingEvent || $event->getTask()->getAppId() !== Application::APP_ID) {
            return;
        }

        if ($event instanceof TaskSuccessfulEvent) {
            $images = $event->getTask()->getOutputImages()
            // store $images somewhere
        }

        if ($event instanceof TaskFailedEvent) {
            $error = $event->getErrorMessage()
            $userId = $event->getTask()->getUserId()
            // Notify relevant user about failure
        }
    }
}
```

### Implementar un proveedor de Texto a imagen

Un **proveedor de Texto a imagen** es una clase que implementa la interfaz `OCP\TextToImage\IProvider`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\TextToImage;

use OCA\MyApp\AppInfo\Application;
use OCP\Files\File;
use OCP\TextToImage\IProvider;
use OCP\IL10N;

class ImageGenerationProvider implements IProvider {

    public function __construct(
        private IL10N $l,
    ) {
    }

    public function getId(): string {
        return self::class;
    }

    public function getName(): string {
        return $this->l->t('My awesome text to image provider');
    }

    public function generate(string $input, array $resources): void {
        // write the resulting images to the file resources in $resources
    }
}
```

El método `getId` devuelve una cadena que identifica de forma única al proveedor registrado. Para ello se puede usar, por ejemplo, el nombre de la clase.

El método `getName` devuelve una cadena que identifica al proveedor registrado en la interfaz de usuario y debe estar localizada.

El método `generate` implementa el paso de generación de imágenes. Recibe un array de valores `resource`. La longitud del array indica cuántas imágenes deben generarse. Cada imagen debe escribirse en uno de los recursos, p. ej., con `fwrite()`. Si la ejecución falla por algún motivo, se debe lanzar una `RuntimeException` con un mensaje de error explicativo.

La clase normalmente se guardaría en un archivo en `lib/TextToImage` de la app, pero se puede colocar en otro lugar siempre que el {nc-ref}`contenedor de inyección de dependencias <dependency-injection>` de Nextcloud pueda cargarla.

### Registro del proveedor

La clase del proveedor se registra mediante el {nc-ref}`mecanismo de arranque <bootstrapping>` de la clase `Application`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCA\MyApp\TextToImage\ImageGenerationProvider;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;

class Application extends App implements IBootstrap {

    public function register(IRegistrationContext $context): void {
        $context->registerTextToImageProvider(ImageGenerationProvider::class);
    }

    public function boot(IBootContext $context): void {}

}
```
````
