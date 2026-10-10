---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo implementar y registrar un proveedor de autenticación de dos factores: estado por usuario, icono, ajustes personales y activación por el administrador."
---
# Proveedores de dos factores

## Resumen

Esta página explica cómo implementar un proveedor de autenticación de dos factores con `IProvider`, propagar su estado al registro de proveedores, registrarlo en `info.xml` y, de forma opcional, darle iconos, ajustes personales y activación o desactivación por el administrador. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/two-factor-provider.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Las apps de proveedores de autenticación de dos factores sirven para conectar segundos factores personalizados al núcleo de Nextcloud.

### Implementar un proveedor sencillo de autenticación de dos factores

Los proveedores de autenticación de dos factores deben implementar la interfaz [OCP\Authentication\TwoFactorAuth\IProvider](https://github.com/nextcloud/server/blob/master/lib/public/Authentication/TwoFactorAuth/IProvider.php). El
ejemplo siguiente muestra un ejemplo minimalista de un proveedor así.

```php
<?php

namespace OCA\TwoFactor_Test\Provider;

use OCP\Authentication\TwoFactorAuth\IProvider;
use OCP\IUser;
use OCP\Template;

class TwoFactorTestProvider implements IProvider {

    /**
     * Get unique identifier of this 2FA provider
     *
     * @return string
     */
    public function getId() {
        return 'test';
    }

    /**
     * Get the display name for selecting the 2FA provider
     *
     * @return string
     */
    public function getDisplayName() {
        return 'Test';
    }

    /**
     * Get the description for selecting the 2FA provider
     *
     * @return string
     */
    public function getDescription() {
        return 'Use a test provider';
    }

    /**
     * Get the template for rending the 2FA provider view
     *
     * @param IUser $user
     * @return Template
     */
    public function getTemplate(IUser $user) {
        // If necessary, this is also the place where you might want
        // to send out a code via e-mail or SMS.

        // 'challenge' is the name of the template
        return new Template('twofactor_test', 'challenge');
    }

    /**
     * Verify the given challenge
     *
     * @param IUser $user
     * @param string $challenge
     */
    public function verifyChallenge(IUser $user, $challenge) {
        if ($challenge === 'passme') {
            return true;
        }
        return false;
    }

    /**
     * Decides whether 2FA is enabled for the given user
     *
     * @param IUser $user
     * @return boolean
     */
    public function isTwoFactorAuthEnabledForUser(IUser $user) {
        // 2FA is enforced for all users
        return true;
    }

}
```

### Registrar el estado del proveedor

Para saber siempre si un proveedor está habilitado para un usuario, el servidor guarda de forma persistente el estado habilitado/deshabilitado
de cada par proveedor-usuario. Por eso, una app de proveedor tiene que propagar estos cambios de estado. De esto se encarga
el [registro de proveedores](https://github.com/nextcloud/server/blob/master/lib/public/Authentication/TwoFactorAuth/IRegistry.php).

El registro puede inyectarse mediante inyección de dependencias en el constructor. Cada vez que cambia el estado del proveedor
(el usuario habilita o deshabilita el proveedor), hay que llamar al método `enableProviderFor` o `disableProviderFor`.

:::{note}
Este registro de proveedores se añadió en Nextcloud 14. Por compatibilidad con versiones anteriores, el servidor
todavía usa en ocasiones el método `IProvider::isTwoFactorAuthEnabledForUser` si el estado del proveedor
aún no se ha establecido. Este método se eliminará en versiones futuras.
:::

### Registrar un proveedor de autenticación de dos factores

Hay que informar al núcleo de Nextcloud de que la app ofrece funcionalidad de autenticación de dos factores. Los proveedores
de dos factores se registran mediante `info.xml`.

```XML
<two-factor-providers>
    <provider>OCA\TwoFactor_Test\Provider\TwoFactorTestProvider</provider>
</two-factor-providers>
```

### Proporcionar un icono (opcional)

Para mejorar cómo se muestra un proveedor en la lista de proveedores seleccionables de la página de inicio de sesión, se puede
especificar un icono. Para ello, la clase del proveedor debe implementar la interfaz [IProvidesIcons](https://github.com/nextcloud/server/blob/master/lib/public/Authentication/TwoFactorAuth/IProvidesIcons.php).
El icono claro se usa en la página de inicio de sesión, mientras que el oscuro se coloca junto
al encabezado de los ajustes personales opcionales (ver más abajo).

### Proporcionar ajustes personales (opcional)

Como otras apps de Nextcloud, los proveedores de dos factores suelen requerir configuración del usuario para funcionar. En Nextcloud
15 se añadió una nueva sección unificada de ajustes de dos factores. Para añadir ahí ajustes personales del proveedor,
un proveedor debe implementar la interfaz [IProvidesPersonalSettings](https://github.com/nextcloud/server/blob/master/lib/public/Authentication/TwoFactorAuth/IProvidesPersonalSettings.php).

### Hacer que el administrador pueda activar un proveedor (opcional)

Para que un administrador pueda habilitar el proveedor para un usuario concreto mediante la herramienta de línea
de comandos occ, es necesario implementar la interfaz [OCP\Authentication\TwoFactorAuth\IActivatableByAdmin](https://github.com/nextcloud/server/blob/master/lib/public/Authentication/TwoFactorAuth/IActivatableByAdmin.php).
Como se describe en la documentación de la interfaz enlazada, esto solo debe implementarse
en proveedores que no necesitan interacción del usuario al activarse.

### Hacer que el administrador pueda desactivar un proveedor (opcional)

Para que un administrador pueda deshabilitar el proveedor para un usuario concreto mediante la herramienta de línea
de comandos occ, es necesario implementar la interfaz [OCP\Authentication\TwoFactorAuth\IDeactivatableByAdmin](https://github.com/nextcloud/server/blob/master/lib/public/Authentication/TwoFactorAuth/IDeactivatableByAdmin.php).
Como se describe en la documentación de la interfaz enlazada, esto solo debe implementarse
en proveedores que no necesitan interacción del usuario al desactivarse.
````
