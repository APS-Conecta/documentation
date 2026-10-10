---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo exponer páginas públicas de una app con PublicShareController y AuthPublicShareController: token, contraseña y funciones que implementar."
---
# Páginas públicas

## Resumen

Esta página explica el concepto de página pública, identificada por un token y opcionalmente protegida con contraseña, y cómo implementarla con los controladores `PublicShareController` y `AuthPublicShareController`. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/publicpage.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Muchas apps de Nextcloud quieren exponer páginas públicas de alguna forma. Puede ser para compartir archivos, un calendario o cualquier otra cosa. Para garantizar que todas esas páginas se beneficien de las mejoras de seguridad que se agregan, se crearon controladores simplificados para que los usen quienes desarrollan apps.

### Concepto

Una página pública sirve para mostrar un recurso que un usuario quiere exponer mediante un enlace público en una app.

Una página pública se identifica mediante un `token` y puede protegerse con una `password`.

Si una página pública está protegida con contraseña, de forma predeterminada se muestra la página de autenticación normal para introducir la contraseña.

Una página pública también puede llamar a otros endpoints. Estos endpoints funcionan de forma muy similar, con la diferencia de que, si el usuario no está autenticado correctamente, lanzarán un 404.

Es obligatorio tener un parámetro (probablemente en la URL) con el `token`. Por ejemplo, el `routes.php` podría tener este aspecto:

```php
<?php
return [
    'routes' => [
        [ 'name' => 'PublicAPI#get', 'url' => '/api/{token}', 'verb' => 'GET' ],
        [ 'name' => 'PublicDisplay#get', 'url' => '/display/{token}', 'verb' => 'GET' ],
    ]
];
```

### Implementar una API llamada desde una página pública de un recurso compartido

Como se ha dicho, el PublicShareController es un controlador muy básico. Hay que implementar 3 funciones: `isPasswordProtected`, `isValidToken` y `getPasswordHash`.

```php
<?php

namespace OCA\Share_Test\Controller;

use OCP\AppFramework\Http\Attribute\PublicPage;
use OCP\AppFramework\PublicShareController;

class PublicAPIController extends PublicShareController {
    /**
     * Return the hash of the password for this share.
     * This function is of course only called when isPasswordProtected is true
     */
    protected function getPasswordHash(): string {
        return md5('secretpassword');
    }

    /**
    * Validate the token of this share. If the token is invalid this controller
    * will return a 404.
    */
    public function isValidToken(): bool {
        return $this->getToken() === 'secretToken';
    }

    /**
     * Allows you to specify if this share is password protected
     */
    protected function isPasswordProtected(): bool {
        return true;
    }

    /**
     * Your normal controller function. The following annotation will allow guests
     * to open the page as well
     */
    #[PublicPage]
    public function get() {
        // Work your magic
    }
}
```

También se puede optar por sobrescribir la función `shareNotFound`, a la que se llama cuando el token no es válido. Ahí se puede, por ejemplo, registrar información adicional en el log.

### Implementar una página pública autenticada

En algunas páginas puede ser necesaria la autenticación con contraseña (igual que cuando se comparte un archivo mediante un enlace público con contraseña). En ese caso hay que extender un proveedor distinto.

El AuthPublicShareController requiere, además de lo que requiere el PublicShareController, que también se implementen las funciones `verifyPassword` y `showShare`.

Además, se pueden sobrescribir las funciones `showAuthenticate` y `showAuthFailed` si no se quieren usar las páginas de autenticación predeterminadas.

Las funciones `authFailed` y `authSucceeded` también pueden sobrescribirse, y se llaman según la autenticación haya tenido éxito o no. Ahí se puede, por ejemplo, registrar información adicional en el log.
````
