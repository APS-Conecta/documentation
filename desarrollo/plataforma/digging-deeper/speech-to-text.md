---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo consumir la API de Voz a texto de OCP, escuchar sus eventos de transcripción e implementar y registrar un proveedor de Voz a texto."
---
(nc-dev-speech-to-text)=
# Voz a texto

## Resumen

Esta página explica la API de Voz a texto, obsoleta desde la versión 30 en favor de la API de TaskProcessing: cómo consumirla mediante `ISpeechToTextManager` y sus eventos de transcripción, cómo implementar un proveedor de Voz a texto, con contexto de usuario, y cómo registrarlo. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/speech-to-text.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 27
:::

:::{deprecated} 30
Usar en su lugar la API de TaskProcessing
:::

Nextcloud ofrece una API de **Voz a texto**. La idea general es que existe una API central de OCP que las apps pueden usar para solicitar transcripciones de archivos de audio o de video. Para no depender de ninguna tecnología, cualquier app puede proporcionar esta funcionalidad de Voz a texto registrando un proveedor de Voz a texto.

### Consumir la API de Voz a texto

Para consumir la API de Voz a texto, se necesita `\OCP\SpeechToText\ISpeechToTextManager`. Este gestor ofrece los siguientes métodos:

- `hasProviders()` Este método devuelve un booleano que indica si se ha registrado algún proveedor. Si es false, no se puede usar Voz a texto.
- `transcribeFile(File $file)` Este método recibe un objeto `OCP\Files\File` que debe apuntar a un archivo multimedia e intentará transcribirlo **en el proceso actual**. Por lo tanto, bloqueará hasta que termine la transcripción y devolverá la transcripción como una cadena. Por eso, usar este método solo se recomienda en comandos de CLI o en trabajos en segundo plano, cuando no se está limitado por los tiempos de espera de las peticiones HTTP ni por los límites de tiempo de ejecución.
- `scheduleFileTranscription(File $file, ?string $userId, string $appId)` Este método programa una transcripción del archivo multimedia recibido **en un trabajo en segundo plano** y, por lo tanto, no bloqueará.

#### Escuchar los eventos de transcripción

Como `scheduleFileTranscription` no bloquea, habrá que escuchar los siguientes eventos en la app para obtener la transcripción o recibir aviso de cualquier fallo.

- `OCP\SpeechToText\Events\TranscriptionSuccessfulEvent` Esta clase de evento ofrece el método `getTranscript()`, que devuelve la transcripción como una cadena
- `OCP\SpeechToText\Events\TranscriptionFailedEvent` Esta clase de evento ofrece el método `getErrorMessage()`, que devuelve el mensaje de error como una cadena (solo en inglés y con fines de depuración, así que no se debe mostrar al usuario)

Ambas clases proporcionan los parámetros `$appId` y `$userId` que se pasaron inicialmente a `scheduleFileTranscription`, mediante `getAppId()` y `getUserId()`, así como `getFileId()` y `getFile()` para acceder al archivo multimedia que se transcribió.

Por ejemplo, en el archivo `lib/AppInfo/Application.php`:

```php
$context->registerEventListener(OCP\SpeechToText\Events\TranscriptionSuccessfulEvent::class, MyTranscriptionListener::class);
$context->registerEventListener(OCP\SpeechToText\Events\TranscriptionFailedEvent::class, MyTranscriptionListener::class);
```

La clase `MyReferenceListener` correspondiente puede tener este aspecto:

```php
<?php
namespace OCA\MyApp\Listener;

use OCA\MyApp\AppInfo\Application;
use OCP\SpeechToText\Events\AbstractTranscriptionEvent;
use OCP\SpeechToText\Events\TranscriptionSuccessfulEvent;
use OCP\SpeechToText\Events\TranscriptionFailedEvent;
use OCP\EventDispatcher\Event;
use OCP\EventDispatcher\IEventListener;

class MyTranscriptionListener implements IEventListener {
    public function handle(Event $event): void {
        if (!$event instanceof AbstractTranscriptionEvent || $event->getAppId() !== Application::APP_ID) {
            return;
        }

        if ($event instanceof TranscriptionSuccessfulEvent) {
            $transcript = $event->getTranscript();
            // store $transcript somewhere
        }

        if ($event instanceof TranscriptionFailedEvent) {
            $error = $event->getErrorMessage();
            $userId = $event->getUserId();
            // Notify relevant user about failure
        }
    }
}
```

### Implementar un proveedor de Voz a texto

Un **proveedor de Voz a texto** es una clase que implementa la interfaz `OCP\SpeechToText\ISpeechToTextProvider`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\SpeechToText;

use OCA\MyApp\AppInfo\Application;
use OCP\Files\File;
use OCP\SpeechToText\ISpeechToTextProvider;
use OCP\IL10N;

class Provider implements ISpeechToTextProvider {

    public function __construct(
        private IL10N $l,
    ) {
    }

    public function getName(): string {
        return $this->l->t('My awesome speech to text provider');
    }

    public function transcribeFile(File $file): string {
        // transcribe file here and return transcript
    }
}
```

El método `getName` devuelve una cadena que identifica al proveedor registrado en la interfaz de usuario.

El método `transcribeFile` transcribe el archivo recibido y devuelve la transcripción. Si la transcripción falla, se debe lanzar una `RuntimeException` con un mensaje de error explicativo.

La clase normalmente se guardaría en un archivo en `lib/SpeechToText` de la app, pero se puede colocar en otro lugar siempre que el {nc-ref}`contenedor de inyección de dependencias <dependency-injection>` de Nextcloud pueda cargarla.

### Proveedor con contexto de usuario

:::{versionadded} 29.0.0
:::

A veces el procesamiento de la tarea puede depender de qué usuario la solicitó.
Ahora se puede obtener esta información en el proveedor implementando además la interfaz `OCP\SpeechToText\ISpeechToTextProviderWithUserId`:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\SpeechToText;

use OCA\MyApp\AppInfo\Application;
use OCP\Files\File;
use OCP\SpeechToText\ISpeechToTextProviderWithUserId;
use OCP\IL10N;

class Provider implements ISpeechToTextProviderWithUserId {

    private ?string $userId = null;

    public function __construct(
        private IL10N $l,
    ) {
    }

    public function getName(): string {
        return $this->l->t('My awesome speech to text provider');
    }

    public function setUserId(?string $userId): void {
        $this->userId = $userId;
    }

    public function transcribeFile(File $file): string {
        // transcribe file here with the use of $this->userId context and return transcript
    }
}
```

### Registro del proveedor

La clase del proveedor se registra mediante el {nc-ref}`mecanismo de arranque <bootstrapping>` de la clase `Application`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCA\MyApp\SpeechToText\Provider;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;

class Application extends App implements IBootstrap {

    public function register(IRegistrationContext $context): void {
        $context->registerSpeechToTextProvider(Provider::class);
    }

    public function boot(IBootContext $context): void {}

}
```
````
