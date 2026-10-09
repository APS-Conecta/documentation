---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo consumir la API de Traducción de OCP e implementar y registrar un proveedor de Traducción, con contexto de usuario y detección de idioma."
---
(nc-dev-machinetranslation)=
# Traducción automática

## Resumen

Esta página explica la API de Traducción, obsoleta desde la versión 30 en favor de la API de TaskProcessing: cómo consumirla mediante `ITranslationManager`, cómo implementar un proveedor de Traducción, con contexto de usuario y con detección de idioma, y cómo registrarlo. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/machinetranslation.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 26
:::

:::{deprecated} 30
Usar en su lugar la API de TaskProcessing
:::

Nextcloud ofrece una API de **Traducción**. La idea general es que existe una API central de OCP que las apps pueden usar para solicitar traducciones automáticas de texto. Para no depender de ninguna tecnología, cualquier app puede proporcionar esta funcionalidad de Traducción registrando un proveedor de Traducción.

### Consumir la API de Traducción

Para consumir la API de Traducción, hay que {nc-ref}`inyectar <dependency-injection>` `\OCP\Translation\ITranslationManager`. Este gestor ofrece los siguientes métodos:

- `hasProviders()` Este método devuelve un booleano que indica si se ha registrado algún proveedor. Si es false, no se puede usar la función de Traducción.
- `getLanguages()` Este método devuelve una lista de objetos `OCP\Translation\LanguageTuple` que indican qué pares de idiomas se admiten actualmente para traducir.
- `translate(string $text, ?string $fromLanguage, string $toLanguage)` Este método proporciona la funcionalidad de traducción propiamente dicha. Tener en cuenta que, según la longitud del texto que se quiera traducir, esto puede tardar más que el tiempo de espera de la petición HTTP o que el límite de tiempo de ejecución de PHP.
- `canDetectLanguage()` Este método devuelve un booleano que indica si es posible la detección automática del idioma. Si es true, se puede pasar `null` como parámetro `$fromLanguage` a `translate` y averiguará automáticamente el idioma de origen.

Si se quiere usar la funcionalidad de traducción en un cliente, también hay endpoints de OCS disponibles para ello: {nc-ref}`API de traducción de OCS <ocs-translation-api>`

### Implementar un proveedor de Traducción

Un **proveedor de Traducción** es una clase que implementa la interfaz `OCP\Translation\ITranslationProvider`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Translation;

use OCA\MyApp\AppInfo\Application;
use OCP\Files\File;
use OCP\Translation\ITranslationProvider;
use OCP\IL10N;

class Provider implements ITranslationProvider {

    public function __construct(
        private IL10N $l,
    ) {
    }

    public function getName(): string {
        return $this->l->t('My awesome translation provider');
    }

    public function getAvailableLanguages(): array {
        // Return an array of OCP\Translation\LanguageTuple objects here
    }

    public function translate(?string $fromLanguage, string $toLanguage, string $text): string {
        // Do some fancy machine translation and return translated string
    }
}
```

El método `getName` devuelve una cadena que identifica al proveedor registrado en la interfaz de usuario.

El método `translate` traduce la cadena recibida y devuelve la traducción. Los dos parámetros de idioma serán códigos de idioma devueltos por `getAvailableLanguages` del proveedor. Si la traducción falla, se debe lanzar una `RuntimeException` con un mensaje de error explicativo.

La clase normalmente se guardaría en un archivo en `lib/Translation` de la app, pero se puede colocar en otro lugar siempre que el {nc-ref}`contenedor de inyección de dependencias <dependency-injection>` de Nextcloud pueda cargarla.

#### Proveedor con contexto de usuario

:::{versionadded} 29.0.0
:::

A veces el procesamiento de la tarea puede depender de qué usuario la solicitó.
Ahora se puede obtener esta información en el proveedor implementando además la interfaz `OCP\Translation\ITranslationProviderWithUserId`:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Translation;

use OCA\MyApp\AppInfo\Application;
use OCP\Files\File;
use OCP\Translation\ITranslationProviderWithUserId;
use OCP\IL10N;

class Provider implements ITranslationProviderWithUserId {

    private ?string $userId = null;

    public function __construct(
        private IL10N $l,
    ) {
    }

    public function getName(): string {
        return $this->l->t('My awesome translation provider');
    }

    public function getAvailableLanguages(): array {
        // Return an array of OCP\Translation\LanguageTuple objects here
    }

    public function setUserId(?string $userId): void {
        $this->userId = $userId;
    }

    public function translate(?string $fromLanguage, string $toLanguage, string $text): string {
        // Do some fancy machine translation and return translated string
    }
}
```

#### Proporcionar detección de idioma

También existe una interfaz `IDetectLanguageProvider` que permite indicar que el proveedor puede detectar automáticamente los idiomas a partir de un texto de entrada. Se puede usar de la siguiente manera:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Translation;

use OCA\MyApp\AppInfo\Application;
use OCP\Files\File;
use OCP\Translation\ITranslationProvider;
use OCP\Translation\IDetectLanguageProvider;
use OCP\IL10N;

class Provider implements ITranslationProvider, IDetectLanguageProvider {

    public function __construct(
        private IL10N $l,
    ) {
    }

    public function getName(): string {
        return $this->l->t('My awesome translation provider');
    }

    public function getAvailableLanguages(): array {
        // Return an array of OCP\Translation\LanguageTuple objects here
    }

    public function translate(?string $fromLanguage, string $toLanguage, string $text): string {
        // Do some fancy machine translation and return translated string
    }

    public function detectLanguage(string $text): ?string {
        // Detect the language of $text
    }
}
```

El método `detectLanguage` recibe un texto en algún idioma y devuelve el código de ese idioma, o `null` si la detección no tuvo éxito. El código de idioma que devuelve este método debería ser uno de los idiomas devueltos en `getAvailableLanguages`.

### Registro del proveedor

La clase del proveedor se registra mediante el {nc-ref}`mecanismo de arranque <bootstrapping>` de la clase `Application`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCA\MyApp\Translation\Provider;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;

class Application extends App implements IBootstrap {

    public function register(IRegistrationContext $context): void {
        $context->registerTranslationProvider(Provider::class);
    }

    public function boot(IBootContext $context): void {}

}
```
````
