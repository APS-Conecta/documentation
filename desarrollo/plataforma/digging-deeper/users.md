---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo crear, modificar y obtener usuarios con IUserManager, iniciar y cerrar sesión con IUserSession y leer o fijar los gerentes de un usuario."
---
# Gestión de usuarios

## Resumen

Esta página muestra cómo gestionar usuarios desde una app con los servicios `IUserManager` e `IUserSession`: crearlos, modificarlos, obtener sus objetos, iniciar y cerrar sesión, y leer o actualizar los gerentes de un usuario. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/users.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los usuarios pueden gestionarse con el servicio IUserManager, que puede {nc-ref}`inyectarse <dependency-injection>`.

**Archivo {file}`lib/Service/UserService.php`**:

```php
<?php

namespace OCA\MyApp\Service;

use OCP\IUserManager;

class UserService {
    private IUserManager $userManager;

    public function __construct(IUserManager $userManager){
        $this->userManager = $userManager;
    }

    public function createUser($userId, $password) {
        return $this->userManager->create($userId, $password);
    }
}
```

### Crear usuarios

Para crear un usuario, se pasan un nombre de usuario y una contraseña al método create:

**Archivo {file}`lib/Service/UserService.php`**:

```php
<?php

namespace OCA\MyApp\Service;

class UserService {
    private IUserManager $userManager;

    public function __construct(IUserManager $userManager){
        $this->userManager = $userManager;
    }

    public function create($userId, $password) {
        return $this->userManager->create($userId, $password);
    }
}
```

### Modificar usuarios

Los usuarios pueden modificarse obteniendo un usuario por su userId o mediante un patrón de búsqueda. Los objetos de usuario devueltos pueden usarse después para:

* Eliminarlos
* Establecer una nueva contraseña
* Deshabilitarlos o habilitarlos
* Obtener su directorio personal

```php
<?php
namespace OCA\MyApp\Service;

class UserService {

    private IUserManager $userManager;

    public function __construct(IUserManager $userManager){
        $this->userManager = $userManager;
    }

    public function delete($userId) {
        return $this->userManager->get($userId)->delete();
    }

    // recoveryPassword is used for the encryption app to recover the keys
    public function setPassword($userId, $password, $recoveryPassword) {
        return $this->userManager->get($userId)->setPassword($password, $recoveryPassword);
    }

    public function disable($userId) {
        return $this->userManager->get($userId)->setEnabled(false);
    }

    public function getHome($userId) {
        return $this->userManager->get($userId)->getHome();
    }
}
```

### Información de la sesión del usuario

Para iniciar sesión, cerrar sesión u obtener el usuario que tiene la sesión iniciada, el servicio IUserSession, que puede {nc-ref}`inyectarse <dependency-injection>`.

**Archivo {file}`lib/Service/UserService.php`**:

```php
<?php

namespace OCA\MyApp\Service;

use OCP\IUserSession;

class UserService {
    private IUserSession $userSession;

    public function __construct(IUserSession $userSession){
        $this->userSession = $userSession;
    }
}
```

Después, los usuarios pueden iniciar y cerrar sesión con:

**Archivo {file}`lib/Service/UserService.php`**:

```php
<?php

namespace OCA\MyApp\Service;

use OCP\IUserSession;

class UserService {
    private IUserSession $userSession;

    public function __construct(IUserSession $userSession){
        $this->userSession = $userSession;
    }

    public function login(string $userId, string $password): void {
        return $this->userSession->login($userId, $password);
    }

    public function logout(): void {
        $this->userSession->logout();
    }
}
```

### Objetos de usuario

Los objetos de usuario pueden obtenerse con el método `IUserManager::get`.

**Archivo {file}`lib/Service/UserService.php`**:

```php
<?php

namespace OCA\MyApp\Service;

use OCP\IUser;
use OCP\IUserManager;

class UserService {
    private IUserManager $userManager;

    public function __construct(IUserManager $userManager) {
        $this->userManager = $userManager;
    }

    public function foo(string $userId): void {
        /** @var IUser|null $user */
        $user = $this->userManager->get($userId);
        if ($user !== null) {
            // User exists
        } else {
            // The user does not exist
        }
    }
}
```

#### Gerentes de usuarios

:::{versionadded} 27
:::

Los usuarios de Nextcloud pueden definirse como gerentes de otros usuarios. Se trata de una propiedad informativa y no influye en la autorización. Un gerente de usuario no debe confundirse con los administradores ni con los subadministradores.

**Archivo {file}`lib/Service/UserService.php`**:

```php
<?php

namespace OCA\MyApp\Service;

use OCP\IUser;
use OCP\IUserManager;

class UserService {
    private IUserManager $userManager;

    public function __construct(IUserManager $userManager) {
        $this->userManager = $userManager;
    }

    public function updateUserManagers(string $userId): void {
        /** @var IUser|null $user */
        $user = $this->userManager->get('user123');
        if ($user === null) {
            throw \InvalidArgumentException("User $userId does not exist");
        }

        $managerUids = $user->getManagerUids();
        // Turn UIDs into user objects
        $managers = array_map(function(string $uid) {
            return $this->userManager->get($uid);
        }, $managerUids));
        // Remove any managers that no longer exist as users
        $existingManagers = array_filter($managers);
        $user->setManagerUids(array_map(function(IUser $admin) {
            return $admin->getUID();
        }, $existingManagers));
    }
}
```
````
