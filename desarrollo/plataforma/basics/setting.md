---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo crear secciones y configuraciones de administración de una app, delegar su administración y autorizar claves de configuración y controladores."
---
# Ajustes

## Resumen

Esta página explica cómo una app crea una sección y un formulario de configuraciones de administración y los registra en `info.xml`, cómo permitir la administración delegada de esos ajustes autorizando claves de configuración de la app, y cómo autorizar controladores reservados a la administración. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/setting.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Crear una sección de administración

Cada aplicación de Nextcloud puede ofrecer ajustes personales y de administración. Para ello
hay que crear una sección que implemente *IIconSection*. Esta sección se usará
en la barra lateral de ajustes para crear una entrada nueva.

En este caso, se creará una clase de sección de administración en **\<myapp>/lib/Sections/NotesAdmin.php**:

```php
<?php
namespace OCA\NotesTutorial\Sections;

use OCP\IL10N;
use OCP\IURLGenerator;
use OCP\Settings\IIconSection;

class NotesAdmin implements IIconSection {
    private IL10N $l;
    private IURLGenerator $urlGenerator;

    public function __construct(IL10N $l, IURLGenerator $urlGenerator) {
        $this->l = $l;
        $this->urlGenerator = $urlGenerator;
    }

    public function getIcon(): string {
        return $this->urlGenerator->imagePath('core', 'actions/settings-dark.svg');
    }

    public function getID(): string {
        return 'notes';
    }

    public function getName(): string {
        return $this->l->t('Notes tutorial');
    }

    public function getPriority(): int {
        return 98;
    }
}
```

El paso siguiente es llenar la nueva sección de administración con un ajuste de administración. Para ello,
se crea una clase nueva en `<myapp>/lib/Settings/NotesAdmin.php`.

```php
<?php
namespace OCA\NotesTutorial\Settings;

use OCP\AppFramework\Http\TemplateResponse;
use OCP\IConfig;
use OCP\IL10N;
use OCP\Settings\ISettings;

class NotesAdmin implements ISettings {
    private IL10N $l;
    private IConfig $config;

    public function __construct(IConfig $config, IL10N $l) {
        $this->config = $config;
        $this->l = $l;
    }

    /**
     * @return TemplateResponse
     */
    public function getForm() {
        $parameters = [
            'mySetting' => $this->config->getSystemValue('my_notes_setting', true),
        ];

        return new TemplateResponse('settings', 'settings/admin', $parameters, '');
    }

    public function getSection() {
        return 'notes'; // Name of the previously created section.
    }

    /**
     * @return int whether the form should be rather on the top or bottom of
     * the admin section. The forms are arranged in ascending order of the
     * priority values. It is required to return a value between 0 and 100.
     *
     * E.g.: 70
     */
    public function getPriority() {
        return 10;
    }
}
```

La última parte que falta es registrar ambas clases dentro de **\<myapp>/appinfo/info.xml**.

```xml
<settings>
    <admin>OCA\NotesTutorial\Settings\NotesAdmin</admin>
    <admin-section>OCA\NotesTutorial\Sections\NotesAdmin</admin-section>
</settings>
```

:::{note}
Para registrar secciones y clases de ajustes personales, se usan *\<personal-section>* y
*\<personal>* en su lugar.
:::

### Administración delegada

:::{versionadded} 23
:::

Nextcloud tiene una funcionalidad integrada que permite [a los administradores delegar autoridad](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/admin_delegation_configuration.html)
en otras personas sin otorgarles privilegios completos de administración (y sin hacerlas
miembros del grupo `admin`).

A grupos concretos se les puede conceder autorización para acceder a configuraciones de administración individuales. Esta es una
funcionalidad que hay que habilitar en cada clase de ajuste de administración. Para ello, la clase del ajuste
debe implementar `IDelegatedSettings` en lugar de `ISettings` e implementar dos métodos
adicionales.

#### Autorizar claves de configuración de la app

Los valores que devuelve `getAuthorizedAppConfig()` definen qué claves de configuración de la app pueden
modificar los administradores delegados. Siempre que sea posible, se deben usar nombres de clave exactos. Se admiten
expresiones regulares para nombres de clave dinámicos, pero deben abarcar la clave completa usando `^` y `$`.
Hay que evitar expresiones sin anclar como `/notes_.*/`, que pueden coincidir con una clave que solo
contiene el prefijo deseado.

```php
<?php
namespace OCA\NotesTutorial\Settings;

use OCP\AppFramework\Http\TemplateResponse;
use OCP\IConfig;
use OCP\IL10N;
use OCP\Settings\IDelegatedSettings;

class NotesAdmin implements IDelegatedSettings {

    ...

    public function getName(): ?string {
        // This can also return an empty string in case there is only one setting
        // in the section.
        return $this->l->t('Notes Admin Settings');
    }

    public function getAuthorizedAppConfig(): array {
        return [
            // Simplest: authorize one exact key from this app.
            'notes' => [
                'my_notes_setting',
            ],
        ];
    }
}
```

#### Usar el ID de la aplicación

El nombre de la app se puede referenciar mediante `Application::APP_ID`. Así se evita duplicar
el ID de la app como cadena:

```php
use OCA\NotesTutorial\AppInfo\Application;

public function getAuthorizedAppConfig(): array {
    return [
        // Multiple keys: authorize several exact keys in this app.
        Application::APP_ID => [
            'my_notes_setting',
            'another_notes_setting',
        ],
    ];
}
```

#### Autorizar nombres de clave dinámicos

Para una familia de claves con nombres dinámicos, se usa una expresión regular anclada que sea lo más
restrictiva posible:

```php
public function getAuthorizedAppConfig(): array {
    return [
        // Authorize keys such as "notes_feature_a" and "notes_feature_b",
        // but not "custom_notes_feature_a".
        Application::APP_ID => [
            '/^notes_[a-z0-9_]+$/',
        ],
    ];
}
```

#### Escapar expresiones regulares dinámicas

Cuando una expresión regular se construye a partir de una variable o una constante, hay que escapar el valor
insertado con `preg_quote()`:

```php
$prefix = preg_quote('notes_', '/');

return [
    Application::APP_ID => [
        "/^{$prefix}[a-z0-9_]+$/",
    ],
];
```

#### Usar constantes de configuración

Para claves de configuración estables y declaradas, conviene usar constantes dedicadas o constantes de la
clase `ConfigLexicon` de la app. Así la lista de autorizaciones delegadas se mantiene sincronizada
con las definiciones de configuración de la app.

Por ejemplo, `<myapp>/lib/ConfigLexicon.php` podría contener:

```php
<?php
namespace OCA\NotesTutorial;

class ConfigLexicon {
     // For PHP versions before 8.3, omit the "string" type.
    public const string MY_SETTING = 'my_notes_setting';
    public const string ANOTHER_SETTING = 'another_notes_setting';
}
```

A lo que luego se puede hacer referencia:

```php
use OCA\NotesTutorial\AppInfo\Application;
use OCA\NotesTutorial\ConfigLexicon;

public function getAuthorizedAppConfig(): array {
    return [
        // Constants: Preferred for stable, declared configuration keys.
        Application::APP_ID => [
            ConfigLexicon::MY_SETTING,
            ConfigLexicon::ANOTHER_SETTING,
        ],
    ];
}
```

#### Autorizar claves de varias apps

Si un ajuste autoriza intencionadamente claves de configuración de más de una app, hay que devolver
una entrada por cada app. Conviene usar la constante `Application::APP_ID` de la app correspondiente
cuando esté disponible:

```php
use OCA\AnotherApp\AppInfo\Application as AnotherAppApplication;

public function getAuthorizedAppConfig(): array {
    return [
        Application::APP_ID => [
            ConfigLexicon::MY_SETTING,
        ],
        AnotherAppApplication::APP_ID => [
            // Prefer AnotherApp's ConfigLexicon constant when available.
            'another_setting',
        ],
    ];
}
```

No se debe usar `/.*/` salvo que el ajuste conceda intencionadamente a los administradores delegados
acceso a todas las claves de la app. No se debe usar una expresión regular para una clave fija:
en su lugar, hay que devolver la clave literal.

### Autorizar controladores reservados a la administración

El método `getAuthorizedAppConfig()` controla las escrituras en la configuración de la app. No concede
acceso a endpoints de controlador arbitrarios. Si la clase del ajuste necesita llamar a métodos de
controlador reservados a la administración, hay que marcar esos métodos con el atributo `AuthorizedAdminSetting`.

```php
<?php
use OCP\AppFramework\Http\Attribute\AuthorizedAdminSetting;
class NotesSettingsController extends Controller {
    /**
     * Save settings
     */
    #[PasswordConfirmationRequired]
    #[AuthorizedAdminSetting(settings: 'OCA\NotesTutorial\Settings\NotesAdmin')]
    public function saveSettings($mySetting) {
        ....
    }
    ...
}
```

:::{note}
El atributo solo está disponible en Nextcloud 27 o posterior. En versiones anteriores, se debe usar
en su lugar la anotación `@AuthorizedAdminSetting(settings=OCA\NotesTutorial\Settings\NotesAdmin)`.
:::

#### Autorizar varios ajustes delegados

Si se tienen varias clases `IDelegatedSettings` que hacen falta para una función, se agregan varios
atributos:

```php
<?php
use OCP\AppFramework\Http\Attribute\AuthorizedAdminSetting;
class NotesSettingsController extends Controller {
    /**
     * Save settings
     */
    #[PasswordConfirmationRequired]
    #[AuthorizedAdminSetting(settings: 'OCA\NotesTutorial\Settings\NotesAdmin')]
    #[AuthorizedAdminSetting(settings: 'OCA\NotesTutorial\Settings\NotesSubAdmin')]
     public function saveSettings($mySetting) {
         ....
     }
     ...
}
```

:::{note}
Si hay que usar la anotación obsoleta, se especifican las clases separadas por punto y coma:

`@AuthorizedAdminSetting(settings=OCA\NotesTutorial\Settings\NotesAdmin;OCA\NotesTutorial\Settings\NotesSubAdmin)`
:::
````
