---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo consumir la API de Procesamiento de tareas de OCP: tipos de tarea y sus formas, tareas, estados y eventos, y cómo implementar y registrar proveedores."
---
(nc-dev-task_processing)=
# Procesamiento de tareas

## Resumen

Esta página explica la API de Procesamiento de tareas, que desde la versión 30 sustituye a las API de Procesamiento de texto, Texto a imagen y Voz a texto: los tipos de tarea integrados y sus formas de entrada y de salida, cómo crear y programar tareas, sus estados y sus eventos, y cómo implementar y registrar proveedores y tipos de tarea propios. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/task_processing.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 30.0.0
:::

Nextcloud ofrece una API de **Procesamiento de tareas** que sustituye a las API de {nc-ref}`Procesamiento de texto <text_processing>`, {nc-ref}`Texto a imagen <text2image>` y {nc-ref}`Voz a texto <speech-to-text>` introducidas anteriormente. La idea general es que existe una API central de OCP que las apps pueden usar para programar todo tipo de tareas (pensada principalmente para tareas de IA). Para no depender de ninguna tecnología, cualquier otra app puede proporcionar esta funcionalidad de tareas registrando proveedores de Procesamiento de tareas para tipos de tarea específicos.

### Consumir la API de Procesamiento de tareas

Para consumir la API de Procesamiento de tareas, hay que {nc-ref}`inyectar <dependency-injection>` `\OCP\TaskProcessing\IManager`. Este gestor ofrece los siguientes métodos:

- `hasProviders()` Este método devuelve un booleano que indica si se ha registrado algún proveedor. Si es false, no se puede usar la función TextProcessing.
- `getAvailableTaskTypes(bool $showDisabled = false)` Este método devuelve un array de los tipos de tarea habilitados, indexado por su ID, con sus nombres y metadatos adicionales. Si se establece `$showdisabled` en `true` (disponible desde NC31), incluirá los tipos de tarea deshabilitados. Desde NC33 también incluirá el campo `isInternal`, que indica si el tipo de tarea está orientado al usuario o es solo para uso interno.
- `getAvailableTaskTypeIds()` Este método (disponible desde NC32) devuelve una lista de los ID de los tipos de tarea disponibles. Usa la misma lógica que `getAvailableTaskTypes()`, pero es más rápido porque no calcula los metadatos de los tipos de tarea (lo que puede ser lento al obtener los valores predeterminados de los campos o las listas de valores de selección múltiple). Si solo se quiere comprobar si una función está disponible, es preferible usar este método en lugar de `getAvailableTaskTypes()`.
- `scheduleTask(Task $task)` Este método proporciona la funcionalidad de programación propiamente dicha. La tarea se define con la clase Task. Este método ejecuta la tarea de forma asíncrona, en un trabajo en segundo plano.
- `getTask(int $id)` Este método obtiene una tarea indicada por su id.
- `deleteTask(Task $task)` Este método elimina una tarea
- `cancelTask(int $id)` Este método cancela una tarea indicada por su id.

Si se quiere usar la funcionalidad de procesamiento de tareas en un cliente, también hay endpoints de OCS disponibles para ello: {nc-ref}`API de procesamiento de tareas de OCS <ocs-taskprocessing-api>`

#### Tipos de tareas

Están disponibles los siguientes tipos de tareas integrados:

- `'core:text2text'`: esta tarea permite pasar un prompt arbitrario al modelo de lenguaje. La implementa `\OCP\TaskProcessing\TaskTypes\TextToText`
  - Forma de entrada:
    - `input`: `Text`
  - Forma de salida:
    - `output`: `Text`
- `'core:text2text:chat'`: esta tarea permite chatear con el modelo de lenguaje. La implementa `\OCP\TaskProcessing\TaskTypes\TextToTextChat`
  - Forma de entrada:
    - `system_prompt`: `Text`
    - `input`: `Text`
    - `history`: `ListOfTexts`
  - Forma de salida:
    - `output`: `Text`
- `'core:text2text:chatwithtools'`: esta tarea permite chatear con el modelo de lenguaje con soporte para llamadas a herramientas. La implementa `\OCP\TaskProcessing\TaskTypes\TextToTextChatWithTools`
  - Forma de entrada:
    - `system_prompt`: `Text`
    - `input`: `Text`
    - `tool_message`: `Text` Una cadena que contiene un array JSON de `{"name": string, "content": string, "tool_call_id": string}`
    - `history`: `ListOfTexts` Cada elemento de la lista es una cadena JSON con `{"role": "human", "content": string}` o `{"role": "assistant", "content": string, (optional: "tool_calls": array<{"name": string, "type": "tool_call", "id": string, "args": object}>)}` o `{"role": "tool", "content": string, "name": string, "tool_call_id": string}`
    - `tools`: `Text` El parámetro tools debe ser un array JSON con el formato de las especificaciones de la API de OpenAI: <https://platform.openai.com/docs/api-reference/chat/create#chat-create-tools>
  - Forma de salida:
    - `output`: `Text`
    - `tool_calls`: `Text` Una cadena que contiene un array JSON con `{"name": string, "type": "tool_call", "id": string, "args": object}`
- `'core:contextagent:interaction'`: esta tarea permite chatear con un agente. La implementa `\OCP\TaskProcessing\TaskTypes\ContextAgentInteraction`
  - Forma de entrada:
    - `input`: `Text`
    - `confirmation`: `Number` Entero booleano que indica si se confirman las acciones solicitadas anteriormente: 0 para rechazar o 1 para confirmar.
    - `conversation_token`: `Text` Token que representa la conversación
  - Forma de salida:
    - `output`: `Text`
    - `conversation_token`: `Text`
    - `actions`: `Text`
- `'core:text2text:formalization'`: esta tarea reformulará el texto de entrada recibido para que tenga un tono más formal. La implementa `\OCP\TaskProcessing\TaskTypes\TextToTextFormalization`
  - Forma de entrada:
    - `input`: `Text`
  - Forma de salida:
    - `output`: `Text`
- `'core:text2text:headline'`: esta tarea generará un titular para el texto de entrada recibido. La implementa `\OCP\TaskProcessing\TaskTypes\TextToTextHeadline`
  - Forma de entrada:
    - `input`: `Text`
  - Forma de salida:
    - `output`: `Text`
- `'core:text2text:reformulation'`: esta tarea reformulará el texto de entrada recibido de forma arbitraria. La implementa `\OCP\TaskProcessing\TaskTypes\TextToTextReformulation`
  - Forma de entrada:
    - `input`: `Text`
  - Forma de salida:
    - `output`: `Text`
- `'core:text2text:simplification'`: esta tarea reformulará el texto de entrada recibido para que sea muy fácil de entender, p. ej., por niños. La implementa `\OCP\TaskProcessing\TaskTypes\TextToTextSimplification`
  - Forma de entrada:
    - `input`: `Text`
  - Forma de salida:
    - `output`: `Text`
- `'core:text2text:summary'`: esta tarea resumirá el texto de entrada recibido. La implementa `\OCP\TaskProcessing\TaskTypes\TextToTextSummary`
  - Forma de entrada:
    - `input`: `Text`
  - Forma de salida:
    - `output`: `Text`
- `'core:text2text:topics'`: esta tarea generará una lista de temas separados por comas para el texto de entrada recibido. La implementa `\OCP\TaskProcessing\TaskTypes\TextToTextTopics`
  - Forma de entrada:
    - `input`: `Text`
  - Forma de salida:
    - `output`: `Text`
- `'core:text2text:translate'`: esta tarea traducirá texto de un idioma a otro. La implementa `\OCP\TaskProcessing\TaskTypes\TextToTextTranslate`
  - Forma de entrada:
    - `input`: `Text`
    - `origin_language`: `Enum`
    - `target_language`: `Enum`
  - Forma de salida:
    - `output`: `Text`
- `'core:audio2text'`: este tipo de tarea sirve para transcribir audio a texto. La implementa `\OCP\TaskProcessing\TaskTypes\AudioToText`
  - Forma de entrada:
    - `input`: `Audio`
  - Forma de salida:
    - `output`: `Text`
- `'core:text2image'`: este tipo de tarea sirve para generar imágenes a partir de prompts de texto. La implementa `\OCP\TaskProcessing\TaskTypes\TextToImage`
  - Forma de entrada:
    - `input`: `Text`
    - `numberOfImages`: `Number`
  - Forma de salida:
    - `output`: `ListOfImages`
- `'core:text2text:changetone'`: este tipo de tarea sirve para reformular un texto cambiando su tono. La implementa `\OCP\TaskProcessing\TaskTypes\TextToTextChangeTone`
  - Forma de entrada:
    - `input`: `Text`
    - `tone`: `Enum`
  - Forma de salida:
    - `output`: `Text`
- `'core:text2text:proofread'`: este tipo de tarea sirve para revisar un texto, comprobando si tiene errores gramaticales y ortográficos. La implementa `\OCP\TaskProcessing\TaskTypes\TextToTextProofread`
  - Forma de entrada:
    - `input`: `Text`
  - Forma de salida:
    - `output`: `Text`
- `'core:text2speech'`: este tipo de tarea sirve para generar voz a partir de prompts de texto. La implementa `\OCP\TaskProcessing\TaskTypes\TextToSpeech`
  - Forma de entrada:
    - `input`: `Text`
  - Forma de salida:
    - `speech`: `Audio`
- `'core:analyze-images'`: este tipo de tarea sirve para analizar imágenes. La implementa `\OCP\TaskProcessing\TaskTypes\AnalyzeImages`
  - Forma de entrada:
    - `input`: `Text`
    - `images`: `ListOfImages`
  - Forma de salida:
    - `output`: `Text`
- `'core:image2text:ocr'`: este tipo de tarea sirve para extraer texto de archivos mediante OCR. La implementa `\OCP\TaskProcessing\TaskTypes\ImageToTextOpticalCharacterRecognition`
  - Forma de entrada:
    - `input`: `ListOfFiles`
  - Forma de salida:
    - `output`: `ListOfTexts`

Los tipos de tarea pueden deshabilitarse en los ajustes de administración de IA para que no estén disponibles para el Asistente ni para otras apps, aunque estén implementados. Todos los tipos de tarea implementados están habilitados de forma predeterminada.

##### Prompts de LLM y E/S multilingüe

Al escribir prompts para el tipo de tarea TextToText en las apps, se recomienda probarlos al menos con

- OpenAI GPT-3.5
- Llama 3.1

Además, hay que asegurarse de indicar al modelo que use el idioma correcto en su salida. De forma predeterminada, la mayoría de los modelos responderán en inglés si el prompt principal está en inglés, aunque los datos de origen estén en otro idioma.
Un ajuste para asegurarse de ello es dar al modelo la siguiente instrucción:

```php
"Detect the language used in the text and make sure to answer in the same language without mentioning the language explicitly."
```

###### Formas de entrada y de salida

Cada tipo de tarea define cómo deben ser su entrada y su salida. Esto se llama forma de entrada y forma de salida.

Por ejemplo, el tipo TextToImage define su forma de entrada de la siguiente manera:

```php
/**
 * @return ShapeDescriptor[]
 * @since 30.0.0
 */
public function getInputShape(): array {
    return [
        'input' => new ShapeDescriptor(
            $this->l->t('Prompt'),
            $this->l->t('Describe the image you want to generate'),
            EShapeType::Text
        ),
        'numberOfImages' => new ShapeDescriptor(
            $this->l->t('Number of images'),
            $this->l->t('How many images to generate'),
            EShapeType::Number
        ),
    ];
}
```

La entrada y la salida de una tarea siempre se representan con un array asociativo. En este caso, la entrada de una tarea TextToImage debe tener una clave de array llamada `'input'`, que debe contener un texto, y una clave de array llamada `'numberOfImages'`, que debe contener un número.

Si simplemente se quiere usar un tipo de tarea, se pueden consultar sus formas de entrada y de salida más arriba o, si no es un tipo integrado, en la documentación o en la implementación de la app que introduce el tipo de tarea. Si se quiere usar tipos de tarea de forma dinámica sin conocer sus formas de antemano, se puede obtener la información de sus formas del método `IManager#getAvailableTaskTypes()`. La clase ShapeDescriptor permite acceder a los datos del tipo, así como a un nombre y una descripción legibles por personas, mediante los métodos `getName()`, `getDescription()` y `getShapeType()`.

###### Tipos de forma

Las claves de las formas de entrada y de salida pueden tener uno de un conjunto predefinido de tipos, que se enumeran en el Enum `\OCP\TaskProcessing\EShapeType`:

```php
enum EShapeType: int {
    case Number = 0;
    case Text = 1;
    case Image = 2;
    case Audio = 3;
    case Video = 4;
    case File = 5;
    case Enum = 6;
    case ListOfNumbers = 10;
    case ListOfTexts = 11;
    case ListOfImages = 12;
    case ListOfAudio = 13;
    case ListOfVideo = 14;
    case ListOfFiles = 15;
}
```

Al consumir la API de procesamiento de tareas, las ranuras `Image`, `Audio`, `Video` y `File` se rellenan con ID de archivo de Nextcloud; así, en lugar de proporcionar los datos de la imagen directamente como una cadena a la tarea, se crea un archivo para ella y se pasa su id. Del mismo modo, si la tarea produce una imagen, se recibirá un ID de archivo en esa ranura.

#### Tareas

Para crear una tarea se usa la clase `\OCP\TaskProcessing\Task`. Su constructor recibe los siguientes argumentos: `new \OCP\TaskProcessing\Task(string $taskTypeId, array $input, string $appId, ?string $userId, string $customId = '')`. Por ejemplo:

```php
// getAvailableTaskTypeIds is faster than getAvailableTaskTypes
// if (isset($textprocessingManager->getAvailableTaskTypes()[TextToTextSummary::ID]) {
// if you don't need the task type metadata, prefer this:
if (in_array(TextToTextSummary::ID, $textprocessingManager->getAvailableTaskTypeIds(), true) {
    $summaryTask = new Task(TextToTextSummary::ID, $emailText, "my_app", $userId, (string) $emailId);
} else {
    // cannot use summarization
}
```

Los objetos de la clase Task tienen disponibles los siguientes métodos:

- `getTaskTypeId()` Esto devuelve el tipo de tarea.
- `getStatus()` Este método devuelve uno de los estados indicados más abajo.
- `getId()` Este método devolverá `null` antes de que la tarea se haya pasado a `scheduleTask`; en caso contrario, devolverá el ID único de la tarea.
- `getInput()` Esto devuelve el array de entrada.
- `getOutput()` Este método devolverá `null` salvo que la tarea se haya ejecutado con éxito; en ese caso, devolverá el array de salida
- `getAppId()` Esto devuelve el ID de la aplicación que originó la tarea.
- `getCustomId()` Esto devuelve el identificador original de la tarea, definido por quien la programó
- `getUserId()` Esto devuelve el ID del usuario que originó la tarea.
- `getCompletionExpectedAt()` Está disponible después de programar la tarea y devuelve el DateTime en que se espera que la tarea se complete
- `getLastUpdated()` Esto devuelve el momento de la última actualización de la tarea, como marca de tiempo unix
- `getScheduledAt()` Esto devuelve el momento en que se programó la tarea, como marca de tiempo unix
- `getStartedAt()` Esto devuelve el momento en que empezó la ejecución de la tarea, como marca de tiempo unix
- `getEndedAt()` Esto devuelve el momento en que terminó la ejecución de la tarea, como marca de tiempo unix
- `getErrorMessage()` Esto devuelve el mensaje de error si la ejecución de la tarea falló
- `getProgress()` Esto devuelve el progreso actual de la tarea, entre 0 y 1 mientras la tarea se ejecuta. Será 1 cuando la tarea se haya completado
- `setWebhookUri()` Esto establece la URI de un webhook que se notificará cuando haya terminado la ejecución de la tarea
- `setWebhookMethod()` Esto establece el método HTTP que se usará para el webhook cuando haya terminado la ejecución de la tarea
- `getWebhookUri()` Esto devuelve la URI del webhook que se notificará cuando haya terminado la ejecución de la tarea
- `getWebhookMethod()` Esto devuelve el método HTTP que se usará para el webhook cuando haya terminado la ejecución de la tarea

:::{versionadded} 33.0.0
- `getUserFacingErrorMessage()` Esto devuelve cualquier mensaje de error destinado a mostrarse al usuario; incluso si una tarea ha fallado, no se garantiza que esté establecido.
:::

Ahora se podría programar la tarea de la siguiente manera:

```php
try {
    $taskprocessingManager->scheduleTask($summaryTask);
} catch (OCP\TaskProcessing\Exception\Exception|OCP\TaskProcessing\Exception\PreConditionNotMetException|OCP\TaskProcessing\Exception\UnauthorizedException|OCP\TaskProcessing\Exception\ValidationException $e) {
    // scheduling task failed
}
```

#### Estados de las tareas

Todas las tareas tienen siempre uno de los siguientes estados:

```php
Task::STATUS_CANCELLED = 5;
Task::STATUS_FAILED = 4;
Task::STATUS_SUCCESSFUL = 3;
Task::STATUS_RUNNING = 2;
Task::STATUS_SCHEDULED = 1;
Task::STATUS_UNKNOWN = 0;
```

#### Escuchar los eventos de procesamiento de tareas

Como `scheduleTask` no bloquea, habrá que escuchar los siguientes eventos en la app para obtener la salida o recibir aviso de cualquier fallo.

- `OCP\TaskProcessing\Events\TaskSuccessfulEvent` Esta clase de evento ofrece el método `getTask()`, que devuelve el objeto de la tarea actualizado, con la salida de la tarea.
- `OCP\TaskProcessing\Events\TaskFailedEvent` Además del método `getTask()`, esta clase de evento proporciona el método `getErrorMessage()`, que devuelve el mensaje de error como una cadena (solo en inglés y con fines de depuración, así que no se debe mostrar al usuario)

Por ejemplo, en el archivo `lib/AppInfo/Application.php`:

```php
$context->registerEventListener(OCP\TaskProcessing\Events\TaskSuccessfulEvent::class, MyPromptResultListener::class);
$context->registerEventListener(OCP\TaskProcessing\Events\TaskFailedEvent::class, MyPromptResultListener::class);
```

La clase `MyPromptResultListener` correspondiente puede tener este aspecto:

```php
<?php
namespace OCA\MyApp\Listener;

use OCA\MyApp\AppInfo\Application;
use OCP\TaskProcessing\Events\AbstractTaskProcessingEvent;
use OCP\TaskProcessing\Events\TaskSuccessfulEvent;
use OCP\TaskProcessing\Events\TaskFailedEvent;
use OCP\EventDispatcher\Event;
use OCP\EventDispatcher\IEventListener;

class MyPromptResultListener implements IEventListener {
    public function handle(Event $event): void {
        if (!$event instanceof AbstractTaskProcessingEvent || $event->getTask()->getAppId() !== Application::APP_ID) {
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

### Implementar un proveedor de TaskProcessing

Un **proveedor de procesamiento de tareas** normalmente será una clase que implemente la interfaz `OCP\TaskProcessing\ISynchronousProvider`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\TaskProcessing;

use OCA\MyApp\AppInfo\Application;
use OCP\Files\File;
use OCP\TaskProcessing\IProvider;
use OCP\TaskProcessing\TaskTypes\TextToTextSummary;
use OCP\TaskProcessing\SummaryTaskType;
use OCP\IL10N;

class Provider implements ISynchrounousProvider {

    public function __construct(
        private IL10N $l,
    ) {
    }

    public function getId(): string {
      return 'myapp:summary';
    }

    public function getName(): string {
        return $this->l->t('My awesome summary provider');
    }

    public function getTaskTypeId(): string {
        return TextToTextSummary::ID;
    }

    public function process(?string $userId, array $input, callable $reportProgress): array {
        // Return the output here
    }

    public function getExpectedRuntime(): int {
        // usually takes 1min on average
        return 60;
    }

    public function getInputShapeDefaults(): array {
        return [];
    }

    public function getOptionalInputShape(): array {
        return [];
    }

    public function getOptionalInputShapeDefaults(): array {
        return [];
    }

    public function getOptionalOutputShape(): array {
        return [];
    }

    public function getInputShapeEnumValues(): array {
        return [];
    }

    public function getOptionalInputShapeEnumValues(): array {
        return [];
    }

    public function getOutputShapeEnumValues(): array {
        return [];
    }

    public function getOptionalOutputShapeEnumValues(): array {
        return [];
    }
}
```

El método `getName` devuelve una cadena que identifica al proveedor registrado en la interfaz de usuario.

El método `process` implementa el paso de procesamiento de la tarea. Si la ejecución falla por algún motivo, se debe lanzar una `\OCP\TaskProcessing\Exception\ProcessingException` con un mensaje de error explicativo.
Desde la v33.0.0 también se puede lanzar una `OCP\TaskProcessing\Exception\UserFacingProcessingException`, que incluye un parámetro de cadena para establecer mensajes de error que se propagarán al usuario final; hay que asegurarse de traducirlos siempre al idioma del usuario que solicitó la tarea. La regla general para saber cuándo usar un mensaje de error orientado al usuario es la siguiente: cuando el error se produjo por una equivocación del usuario o el usuario puede hacer algo para corregirlo, lanzar un error orientado al usuario. Sin embargo, hay que asegurarse de no incluir detalles de la implementación ni del servidor en el mensaje de error orientado al usuario; para eso está el mensaje de error normal, que solo será visible para los administradores.

Es importante señalar aquí que las ranuras `Image`, `Audio`, `Video` y `File` del array de entrada se rellenarán con objetos `\OCP\Files\File` por comodidad. Al producir uno de estos como salida, basta con devolver una cadena; la API convertirá los datos en un archivo adecuado por comodidad. El parámetro `$reportProgress` es un callback que se puede usar libremente para informar del progreso de la tarea como un único valor float entre 0 y 1. Su valor de retorno indicará si la tarea sigue en ejecución (`true`) o si se canceló (`false`) y debe terminarse el procesamiento.

Esta clase normalmente se guardaría en un archivo en `lib/TaskProcessing` de la app, pero se puede colocar en otro lugar siempre que el {nc-ref}`contenedor de inyección de dependencias <dependency-injection>` de Nextcloud pueda cargarla.

#### Proporcionar entradas y salidas adicionales

Los tipos de tarea integrados a menudo solo especifican las ranuras de entrada y de salida más básicas. Si se quiere ofrecer más opciones de entrada
con el proveedor, se pueden especificar entradas y salidas opcionales con los métodos `getOptionalInputShape` y `getOptionalOutputShape`.
Hay que devolver un array asociativo de objetos `\OCP\TaskProcessing\ShapeDescriptor`.

```php
public function getOptionalInputShape(): array {
    return [
        'tone' => new ShapeDescriptor($this->l->t('Tone of voice'), $this->l->t('Set the tone of voice to be used for the output'), EShapeType::Text)
    ];
}
```

En la misma línea, también se pueden proporcionar ranuras de forma de salida opcionales además de las ranuras de salida predefinidas.

```php
public function getOptionalOutputShape(): array {
    return [
        'co2_emissions' => new ShapeDescriptor($this->l->t('CO2 Emissions'), $this->l->t('The CO2 emissions produced by running this task in metric tons'), EShapeType::Number)
    ];
}
```

#### Proporcionar valores predeterminados de entrada

Con el método `getInputShapeDefaults` se pueden especificar valores predeterminados para las ranuras de entrada (que define el tipo de tarea). Por ejemplo:

```php
public function getInputShapeDefaults(): array {
    return [
        'input' => 'There was once a man with many cows who wanted to have even more cows.'
    ];
}
```

Tener en cuenta que solo se pueden especificar valores predeterminados para las ranuras 'Text' y 'Number'.

Lo mismo funciona para las formas de entrada opcionales que se hayan definido en `getOptionalInputShape`:

```php
public function getOptionalInputShapeDefaults(): array {
    return [
        'tone' => 'Formal'
    ];
}
```

#### Trabajar con tipos de forma Enum

Tanto las formas de entrada y de salida como las formas de entrada y de salida opcionales permiten declarar ranuras de tipo `'Enum'`. Un Enum
es un tipo que solo admite valores de un conjunto predefinido. En el caso de la API de TaskProcessing, este conjunto no lo define el tipo de tarea, sino
el proveedor que implementa el tipo de tarea, mediante `getInputShapeEnumValues`, `getOutputShapeEnumValues`, `getOptionalInputShapeEnumValues` y `getOptionalOutputShapeEnumValues`.

Por ejemplo, se podría implementar la ranura de tono de voz anterior con un Enum:

```php
public function getOptionalInputShape(): array {
    return [
        'tone' => new ShapeDescriptor($this->l->t('Tone of voice'), $this->l->t('Set the tone of voice to be used for the output'), EShapeType::Enum)
    ];
}
```

```php
public function getOptionalInputShapeEnumValues(): array {
    return [
        'tone' => [
            new ShapeEnumValue($this->l->t('Simple'), 'So that a kid could understand'),
            new ShapeEnumValue($this->l->t('Funny'), 'Funny'),
            new ShapeEnumValue($this->l->t('Formal'), 'Formal'),
        ]
    ];
}
```

#### Proporcionar más tipos de tareas

Si se quiere implementar proveedores que gestionen tipos de tareas adicionales, se pueden crear clases de tipo de tarea propias que implementen la interfaz `OCP\TaskProcessing\ITaskType`:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\TaskProcessing;

use OCA\MyApp\AppInfo\Application;
use OCP\Files\File;
use OCP\TaskProcessing\ITaskType;
use OCP\IL10N;

class AudioToImage implements ITaskType {
    public const ID = 'myapp:audiotoimage';

    public function getId(): string {
        return self::ID;
    }

    public function getName(): string {
        return 'Get Spectrogram';
    }

    public function getDescription(): string {
        return 'Turns audio into an image';
    }

    public function getInputShape(): array {
        return [
            'audio' => new ShapeDescriptor('Audio', 'The audio', EShapeType::Audio),
        ];
    }

    public function getOutputShape(): array {
        return [
            'spectrogram' => new ShapeDescriptor('Spectrogram', 'The audio spectrogram', EShapeType::Image),
        ];
    }
}
```

##### Tipos de tarea internos

:::{versionadded} 33.0.0
:::

Las demás apps y clientes darán por hecho que los tipos de tarea están orientados al usuario y los mostrarán en el frontend. Si los tipos de tarea personalizados
no están pensados para mostrarse a los usuarios, se debe implementar en su lugar la interfaz `IInternalTaskType`. Así
las demás apps y clientes sabrán que no deben mostrar el tipo de tarea personalizado a los usuarios finales.

#### Proveedores activables

:::{versionadded} 33.0.0
:::

Los proveedores síncronos se ejecutan automáticamente mediante un trabajo en segundo plano al que normalmente apuntará un worker para garantizar
que se ejecute casi al instante. Las ExApps, en cambio, antes tenían que consultar periódicamente al servidor si había tareas nuevas. Desde la introducción de los
proveedores activables, las ExApps reciben aviso de inmediato de las tareas nuevas cuando se programan. Esto se implementa mediante la interfaz `ITriggerableProvider`,
que agrega a la interfaz del proveedor un método adicional `trigger(): void`, al que se llama cuando se programa una tarea nueva para este proveedor y
no hay tareas en ejecución para él en ese momento. Normalmente, si se implementa un proveedor en PHP no habrá que ocuparse de esta interfaz, pero se documenta
aquí para que la información esté completa.

### Registro de proveedores y tipos de tarea

Los proveedores y los tipos de tarea se registran mediante el {nc-ref}`mecanismo de arranque <bootstrapping>` de la clase `Application`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCA\MyApp\TaskProcessing\Provider;
use OCA\MyApp\TaskProcessing\AudioToImage;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;

class Application extends App implements IBootstrap {

    public function register(IRegistrationContext $context): void {
        $context->registerTaskProcessingProvider(Provider::class);
        $context->registerTaskProcessingTaskType(AudioToImage::class);
    }

    public function boot(IBootContext $context): void {}

}
```
````
