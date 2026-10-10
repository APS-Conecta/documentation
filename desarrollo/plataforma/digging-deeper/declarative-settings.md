---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo registrar el esquema de ajustes declarativos de una app, por clase o por evento, dónde se guardan sus valores y qué tipos de campo admite."
---
(nc-dev-declarative_settings_section)=
# Ajustes declarativos

## Resumen

Esta página explica cómo definir los ajustes de una app de forma declarativa: cómo registrar el esquema con una clase o con un listener de eventos, cómo se almacenan los valores de forma interna o externa y qué tipos de campo admite el esquema, con un ejemplo de cada uno. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/declarative_settings.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 29.0.0
:::

Con Nextcloud 29 hay una nueva forma de definir los ajustes de una app de manera declarativa.
Esto significa que basta con registrar el esquema de ajustes,
sin escribir código personalizado de frontend ni de backend para gestionar los ajustes
(salvo cuando se requiere una lógica o un diseño de ajustes más complejos).

### Registrar el esquema de ajustes

Hay dos formas de registrar un esquema de ajustes declarativos:

1. Basada en clases, usando la interfaz `OCP\Settings\IDeclarativeSettingsForm`
2. Usando un listener de eventos para `OCP\Settings\Events\DeclarativeSettingsRegisterFormEvent`

Además, se pueden registrar varios esquemas de parámetros declarativos por aplicación.

:::{note}
Los ids de los campos del formulario (configkeys) deben ser únicos dentro de una app.
:::

### Registro del esquema basado en clases

Para registrar un esquema de ajustes declarativos mediante una clase, hay que crear una clase que implemente la interfaz `OCP\Settings\IDeclarativeSettingsForm`:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\DeclarativeSettings;

use OCP\Settings\DeclarativeSettingsTypes;
use OCP\Settings\IDeclarativeSettingsForm;

class MyDeclarativeSettingsForm implements IDeclarativeSettingsForm {
    public function getSchema(): array {
        return [
            'id' => 'my_declarative_settings_form', // unique form id
            'priority' => 10, // declarative section priority (ordering)
            'section_type' => DeclarativeSettingsTypes::SECTION_TYPE_ADMIN, // admin, personal
            'section_id' => 'my_section_id', // existing section id or your custom section id
            'storage_type' => DeclarativeSettingsTypes::STORAGE_TYPE_INTERNAL, // external, internal (handled by core to store in appconfig and preferences)
            'title' => 'MyApp settings title', // NcSettingsSection name
            'description' => 'My app settings section description', // NcSettingsSection description
            'doc_url' => '', // NcSettingsSection doc_url for documentation or help page, empty string if not needed
            'fields' => [
                [
                    'id' => 'my_field_key', // configkey
                    'title' => 'Field title', // name or label
                    'description' => 'Additional setting hint or description', // hint
                    'type' => DeclarativeSettingsTypes::MULTI_SELECT,
                    'options' => ['foo', 'bar', 'baz'],
                    'placeholder' => 'Select some multiple options', // input placeholder
                    'default' => ['foo', 'bar'],
                ],
            ]
        ];
    }
}
```

La interfaz `OCP\Settings\IDeclarativeSettingsForm` tiene un solo método, `getSchema`, que debe devolver un array con el esquema de ajustes.

Después se puede registrar la clase del esquema con el método `IRegistrationContext->registerDeclarativeSettings`:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IRegistrationContext;
use OCA\MyApp\DeclarativeSettings\MyDeclarativeSettingsForm;

class Application extends App {
    public function __construct(array $urlParams = []) {
        parent::__construct('my_app', $urlParams);
    }

    public function register(IRegistrationContext $context): void {
        $context->registerDeclarativeSettings(MyDeclarativeSettingsForm::class);
    }
}
```

### Registro del esquema basado en eventos

Para registrar un esquema de ajustes declarativos mediante el sistema de eventos, hay que implementar un listener de eventos para `OCP\Settings\Events\DeclarativeSettingsRegisterFormEvent`:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Listener;

use OCP\EventDispatcher\Event;
use OCP\EventDispatcher\IEventListener;
use OCP\Settings\DeclarativeSettingsTypes;
use OCP\Settings\Events\DeclarativeSettingsRegisterFormEvent;

class RegisterDeclarativeSettingsListener implements IEventListener {

    public function __construct() {
    }

    public function handle(Event $event): void {
        if (!($event instanceof DeclarativeSettingsRegisterFormEvent)) {
            return;
        }

        $event->registerSchema('my_app', [
            // your declarative settings schema here
        ]);
    }
}
```

Y registrar el listener de eventos como de costumbre en el contexto de registro de `AppInfo/Application.php`:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IRegistrationContext;
use OCP\Settings\Events\DeclarativeSettingsRegisterFormEvent;
use OCA\MyApp\Listener\RegisterDeclarativeSettingsListener;

class Application extends App {
    public function __construct(array $urlParams = []) {
        parent::__construct('my_app', $urlParams);
    }

    public function register(IRegistrationContext $context): void {
        $context->registerEventListener(DeclarativeSettingsRegisterFormEvent::class, RegisterDeclarativeSettingsListener::class);
    }
}
```

### Gestionar el almacenamiento de los ajustes

Se admiten dos tipos de `storage_type` del esquema:

1. interno `OCP\Settings\DeclarativeSettingsTypes::STORAGE_TYPE_INTERNAL` - los cambios de los valores de los ajustes los gestiona el núcleo
1. externo `OCP\Settings\DeclarativeSettingsTypes::STORAGE_TYPE_EXTERNAL` - los cambios de los valores de los ajustes los gestionan los manejadores de la app (listeners de eventos).

#### Tipo de almacenamiento interno

El tipo de almacenamiento interno (`storage_type='internal'`) lo gestiona el núcleo; no hace falta implementar manejadores adicionales para él.

##### Tipo de sección admin

Para un esquema de ajustes declarativos con `section_type` establecido en `DeclarativeSettingsTypes::SECTION_TYPE_ADMIN`, los valores de los ajustes
se almacenan en la tabla `appconfig`.

Accesibles mediante la interfaz `OCP\IConfig->getAppValue`.

##### Tipo de sección personal

Para un esquema de ajustes declarativos con `section_type` establecido en `DeclarativeSettingsTypes::SECTION_TYPE_PERSONAL`, los valores de los ajustes
son específicos de cada usuario y se almacenan en la tabla `preferences`.

Accesibles mediante la interfaz `OCP\IConfig->getUserValue`.

#### Tipo de almacenamiento externo

La gestión de un tipo de almacenamiento externo (`storage_type='external'`) se hace siempre escuchando los siguientes eventos:

1. `OCP\Settings\Events\DeclarativeSettingsGetValueEvent` - para devolver el valor del ajuste declarativo desde el almacenamiento propio
2. `OCP\Settings\Events\DeclarativeSettingsSetValueEvent` - para guardar el valor del ajuste declarativo donde se quiera

Ejemplo de listener del evento DeclarativeSettingsGetValueEvent:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Listener;

use OCP\EventDispatcher\Event;
use OCP\EventDispatcher\IEventListener;
use OCP\IConfig;
use OCP\Settings\Events\DeclarativeSettingsGetValueEvent;

class GetDeclarativeSettingsValueListener implements IEventListener {

    public function __construct(private IConfig $config) {
    }

    public function handle(Event $event): void {
        if (!$event instanceof DeclarativeSettingsGetValueEvent) {
            return;
        }

        // Always check if the event is related to your app declarative settings
        if ($event->getApp() !== 'my_app') {
            return;
        }

        $value = $this->config->getUserValue($event->getUser()->getUID(), $event->getApp(), $event->getFieldId());
        $event->setValue($value);
    }
}
```

Ejemplo de listener del evento DeclarativeSettingsSetValueEvent:

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Listener;

use OCP\EventDispatcher\Event;
use OCP\EventDispatcher\IEventListener;
use OCP\IConfig;
use OCP\Settings\Events\DeclarativeSettingsSetValueEvent;

class SetDeclarativeSettingsValueListener implements IEventListener {

    public function __construct(private IConfig $config) {
    }

    public function handle(Event $event): void {
        if (!$event instanceof DeclarativeSettingsSetValueEvent) {
            return;
        }

        // Always check if the event is related to your app declarative settings
        if ($event->getApp() !== 'my_app') {
            return;
        }

        $this->config->setUserValue($event->getUser()->getUID(), $event->getApp(), $event->getFieldId(), $event->getValue());
    }
}
```

#### Registrar los listeners get/set

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IRegistrationContext;
use OCP\Settings\Events\DeclarativeSettingsGetValueEvent;
use OCP\Settings\Events\DeclarativeSettingsSetValueEvent;
use OCA\MyApp\Listener\GetDeclarativeSettingsValueListener;
use OCA\MyApp\Listener\SetDeclarativeSettingsValueListener;

class Application extends App {
    public function __construct(array $urlParams = []) {
        parent::__construct('my_app', $urlParams);
    }

    public function register(IRegistrationContext $context): void {
        $context->registerEventListener(DeclarativeSettingsGetValueEvent::class, GetDeclarativeSettingsValueListener::class);
        $context->registerEventListener(DeclarativeSettingsSetValueEvent::class, SetDeclarativeSettingsValueListener::class);
    }
}
```

### Tipos de campo del esquema

Los tipos de campo admitidos se declaran en la clase `OCP\Settings\DeclarativeSettingsTypes`:

- `DeclarativeSettingsTypes::TEXT` - input de tipo text
- `DeclarativeSettingsTypes::PASSWORD` - input de tipo password
- `DeclarativeSettingsTypes::EMAIL` - input de tipo email
- `DeclarativeSettingsTypes::TEL` - input de tipo tel
- `DeclarativeSettingsTypes::URL` - input de tipo url
- `DeclarativeSettingsTypes::NUMBER` - input de tipo number
- `DeclarativeSettingsTypes::CHECKBOX` - input de tipo checkbox
- `DeclarativeSettingsTypes::MULTI_CHECKBOX` - varias casillas de verificación que representan un ajuste con varias opciones
- `DeclarativeSettingsTypes::RADIO` - input de tipo radio para un ajuste con una sola opción
- `DeclarativeSettingsTypes::SELECT` - input de tipo select para un ajuste con una sola opción
- `DeclarativeSettingsTypes::MULTI_SELECT` - input de tipo select para un ajuste con varias opciones

A continuación se listan los ejemplos de cada tipo de campo.

:::{note}
El orden de los campos es el mismo que en el array del esquema.
:::

#### Tipos de input básicos

Para text, password, email, tel, url y number, el esquema es similar:

```php
[
    'id' => 'my_field_unique_id', // configkey
    'title' => 'Default text field', // label
    'description' => 'Set some simple text setting', // hint
    'type' => DeclarativeSettingsTypes::TEXT, // text, password, email, tel, url, number
    'placeholder' => 'Enter text setting', // placeholder
    'default' => 'foo',
],
```

#### Casilla de verificación y casillas de verificación múltiples

```php
[
    'id' => 'my_checkbox_field',
    'title' => 'Toggle something',
    'description' => 'Select checkbox option setting',
    'type' => DeclarativeSettingsTypes::CHECKBOX, // checkbox, multiple-checkbox
    'label' => 'Verify something if enabled',
    'default' => false,
],
[
    'id' => 'my_multicheckbox_field',
    'title' => 'Multiple checkbox toggles, describing one setting, checked options are saved as an JSON object {foo: true, bar: false}',
    'description' => 'Select checkbox option setting',
    'type' => DeclarativeSettingsTypes::MULTI_CHECKBOX, // checkbox, multi-checkbox
    'default' => ['foo' => true, 'bar' => true, 'baz' => true],
    'options' => [
        [
            'name' => 'Foo',
            'value' => 'foo', // multiple-checkbox configkey
        ],
        [
            'name' => 'Bar',
            'value' => 'bar',
        ],
        [
            'name' => 'Baz',
            'value' => 'baz',
        ],
        [
            'name' => 'Qux',
            'value' => 'qux',
        ],
    ],
],
```

#### Radio

```php
[
    'id' => 'my_radio_field',
    'title' => 'Radio toggles, describing one setting like single select',
    'description' => 'Select radio option setting',
    'type' => DeclarativeSettingsTypes::RADIO, // radio (NcCheckboxRadioSwitch type radio)
    'label' => 'Select single toggle',
    'default' => 'foo',
    'options' => [
        [
            'name' => 'First radio', // NcCheckboxRadioSwitch display name
            'value' => 'foo' // NcCheckboxRadioSwitch value
        ],
        [
            'name' => 'Second radio',
            'value' => 'bar'
        ],
        [
            'name' => 'Third radio',
            'value' => 'baz'
        ],
    ],
],
```

#### Selección y selección múltiple

```php
[
    'id' => 'my_select_field',
    'title' => 'Selection',
    'description' => 'Select some option setting',
    'type' => DeclarativeSettingsTypes::SELECT, // select, radio, multi-select
    'options' => ['foo', 'bar', 'baz'],
    'placeholder' => 'Select some option setting',
    'default' => 'foo',
],
```

```php
[
    'id' => 'my_multi_select_field', // configkey
    'title' => 'Multi-selection', // name or label
    'description' => 'Select some option setting', // hint
    'type' => DeclarativeSettingsTypes::MULTI_SELECT, // select, radio, multi-select
    'options' => ['foo', 'bar', 'baz'], // simple options for select, radio, multi-select
    'placeholder' => 'Select some multiple options', // input placeholder
    'default' => ['foo', 'bar'],
],
```

#### Tipo de campo sensible

Desde Nextcloud 32 hay un nuevo atributo de campo, `sensitive: true/false`, disponible para los tipos `DeclarativeSettingsTypes::TEXT` y `DeclarativeSettingsTypes::PASSWORD`.
Los valores de estos campos se almacenan cifrados en la base de datos y no se exponen en la interfaz de usuario.

```php
[
    'id' => 'test_sensitive_field',
    'title' => 'Sensitive text field',
    'description' => 'Set some secure value setting that is stored encrypted',
    'type' => DeclarativeSettingsTypes::TEXT,
    'label' => 'Sensitive field',
    'placeholder' => 'Set secure value',
    'default' => '',
    'sensitive' => true, // only for TEXT, PASSWORD types
],
[
    'id' => 'test_sensitive_field_2',
    'title' => 'Sensitive password field',
    'description' => 'Set some password setting that is stored encrypted',
    'type' => DeclarativeSettingsTypes::PASSWORD,
    'label' => 'Sensitive field',
    'placeholder' => 'Set secure value',
    'default' => '',
    'sensitive' => true, // only for TEXT, PASSWORD types
],
```
````
