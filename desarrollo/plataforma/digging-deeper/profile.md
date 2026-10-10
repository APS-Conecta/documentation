---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo una app agrega sus propias acciones al perfil de usuario: implementar ILinkAction y registrar la acción durante el arranque de la app."
---
# Perfil

## Resumen

Esta página describe el perfil de usuario y sus acciones de perfil, y cómo una app puede aportar las suyas implementando la interfaz `ILinkAction` y registrándolas durante el arranque de la app. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/profile.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El perfil de usuario presenta la información de un usuario, incluidos su nombre completo, su foto de perfil, su organización, su rol, su ubicación, su biografía y su titular, así como información accionable a la que se denomina acciones de perfil. Estas acciones pueden incluir iniciar un chat de [Nextcloud Talk](https://nextcloud.com/talk/) con el usuario, enviarle un correo electrónico, visitar su sitio web, abrir su perfil de Twitter, llamar a su número de teléfono, programar una cita y más.

Quienes desarrollan apps pueden integrarse en el perfil y proporcionar sus propias acciones.

### Registrar una acción de perfil

Una acción de perfil se representa mediante una clase que implementa la interfaz `OCP\\Profile\\ILinkAction`. Esta clase se instancia cada vez que se carga el perfil de usuario.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Profile;

use OCP\Accounts\IAccountManager;
use OCP\IURLGenerator;
use OCP\IUser;
use OCP\IL10N;
use OCP\Profile\ILinkAction;

class MyProfileAction implements ILinkAction {

    /** @var string */
    private $targetUser;

    /** @var IAccountManager */
    private $accountManager;

    /** @var IL10N */
    private $l10n;

    /** @var IUrlGenerator */
    private $urlGenerator;

    public function __construct(
        IAccountManager $accountManager,
        IL10N $l10n,
        IURLGenerator $urlGenerator
    ) {
        $this->accountManager = $accountManager;
        $this->l10n = $l10n;
        $this->urlGenerator = $urlGenerator;
    }

    /**
     * Preload the user specific value required by the action
     *
     * e.g. the email is loaded for the email action and the userId for the Talk action
     *
     * @since 23.0.0
     */
    public function preload(IUser $targetUser): void {
        $this->targetUser = $targetUser;
    }

    /**
     * Returns the app ID of the action
     *
     * e.g. 'spreed'
     *
     * @since 23.0.0
     */
    public function getAppId(): string {
        return 'my_app_id';
    }

    /**
     * Returns the unique ID of the action
     *
     * *For account properties this is the constant defined in lib/public/Accounts/IAccountManager.php*
     *
     * e.g. 'email'
     *
     * @since 23.0.0
     */
    public function getId(): string {
        return 'my_unique_action';
    }

    /**
     * Returns the translated unique display ID of the action
     *
     * Should be something short and descriptive of the action
     * as this is seen by the end-user when configuring actions
     *
     * e.g. 'Email'
     *
     * @since 23.0.0
     */
    public function getDisplayId(): string {
        return $this->l10n->t('My unique action');
    }

    /**
     * Returns the translated title
     *
     * e.g. 'Mail user@domain.com'
     *
     * Use the L10N service to translate it
     *
     * @since 23.0.0
     */
    public function getTitle(): string {
        return $this->l10n->t('Ping %s', [$this->targetUser->getDisplayName()]);
    }

    /**
     * Returns the priority
     *
     * *Actions are sorted in ascending order*
     *
     * e.g. 60
     *
     * @since 23.0.0
     */
    public function getPriority(): int {
        return 60;
    }

    /**
     * Returns the URL link to the 16*16 SVG icon
     *
     * @since 23.0.0
     */
    public function getIcon(): string {
        return $this->urlGenerator->getAbsoluteURL($this->urlGenerator->imagePath('my_app_id', 'actions/my_unique_action.svg'));
    }

    /**
     * Returns the target of the action,
     * if null is returned the action won't be registered
     *
     * e.g. 'mailto:user@domain.com'
     *
     * @since 23.0.0
     */
    public function getTarget(): ?string {
        return $this->urlGenerator->linkToRouteAbsolute('my_app_id.Page.index') . '?pingUser=' . $this->targetUser->getUID();
    }
}
```

La clase `MyProfileAction` debe registrarse durante el {nc-ref}`arranque de la app <bootstrapping>`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;
use OCA\MyApp\Profile\MyProfileAction;

class Application extends App implements IBootstrap {

    public const APP_ID = 'my_app_id';

    public function __construct(array $urlParams = []) {
        parent::__construct(self::APP_ID, $urlParams);
    }

    public function register(IRegistrationContext $context): void {
        $context->registerProfileLinkAction(MyProfileAction::class);
    }

    public function boot(IBootContext $context): void {
    }
}
```
````
