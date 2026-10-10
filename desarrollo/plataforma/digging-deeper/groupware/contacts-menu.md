---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo una app extiende las entradas del menú de contactos: proveedores IProvider e IBulkProvider, datos del contacto, acciones y estado del usuario."
---
# Menú de contactos

## Resumen

Esta página explica cómo una app extiende las entradas del menú de contactos de la cabecera: implementar y registrar un proveedor individual o en bloque, leer la información del contacto y agregar acciones de correo electrónico y de enlace. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/groupware/contacts_menu.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud muestra un *menú de contactos* en la esquina derecha de la cabecera. Este menú lista los contactos de un usuario. Las apps pueden extender estas entradas de contacto.

Las apps que extienden el menú de contactos implementan un IProvider o un IBulkProvider. El método `process` de IProvider se llama para cada entrada que se muestra en el menú de contactos. El método `process` de IBulkProvider se llama para todas las entradas a la vez. Si resulta más barato obtener los datos en una sola operación, usar IBulkProvider.

**Archivo {file}`lib/ContactsMenu/MyProvider.php`**:

```php
<?php

namespace OCA\MyApp\ContactsMenu;

use OCP\Contacts\ContactsMenu\IEntry;
use OCP\Contacts\ContactsMenu\IProvider;

class MyProvider implements IProvider {
    public function process(IEntry $entry): void {
        // todo: something useful
    }
}
```

Alternativamente, como proveedor en bloque:

**Archivo {file}`lib/ContactsMenu/MyBulkProvider.php`**:

```php
<?php

namespace OCA\MyApp\ContactsMenu;

use OCP\Contacts\ContactsMenu\IEntry;
use OCP\Contacts\ContactsMenu\IProvider;

class MyBulkProvider implements IBulkProvider {
    public function process(array $entries): void {
        // todo: something useful in bulk
    }
}
```

**Archivo {file}`appinfo/info.xml`**:

```xml
<?xml version="1.0"?>
<info xmlns:xsi= "http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="https://apps.nextcloud.com/schema/apps/info.xsd">
    <id>my_app</id>
    <name>My App</name>
    <contactsmenu>
        <provider>OCA\MyApp\ContactsMenu\MyProvider</provider>
        <!-- or -->
        <provider>OCA\MyApp\ContactsMenu\MyBulkProvider</provider>
    </contactsmenu>
</info>
```

### Acceder a la información de contacto

Los objetos `IEntry` ofrecen getters para la información de contacto:

- `getFullName()`: obtiene el nombre completo. Si no hay un nombre completo establecido, devuelve una cadena vacía.
- `getEMailAddresses()`: obtiene todas las direcciones de correo electrónico.
- `getAvatar()`: obtiene la URI del avatar.
- `getProperty(string $name)`: lee una [propiedad vCard](https://www.rfc-editor.org/rfc/rfc6350#page-23) del contacto. Devuelve NULL si la propiedad no está establecida.

### Acciones

Los proveedores pueden agregar acciones a las entradas de contacto. Por ahora se admiten acciones de correo electrónico y de enlace. Se crean con ayuda de `IActionFactory`.

**Archivo {file}`lib/ContactsMenu/LinkProvider.php`**:

```php
<?php

namespace OCA\MyApp\ContactsMenu;

use OCP\Contacts\ContactsMenu\IEntry;
use OCP\Contacts\ContactsMenu\IProvider;

class LinkProvider implements IProvider {
    private IActionFactory $actionFactory;

    public function __construct(IActionFactory $actionFactory) {
        $this->actionFactory = $actionFactory
    }

    public function process(IEntry $entry): void {
        $emailAction = $this->actionFactory->newEMailAction(
            '/apps/myapp/img/link.png', // icon URL
            'Click me', // name
            'user@domain.tld', // email address
            'my_app', // app ID (optional)
        );
        $linkAction = $this->actionFactory->newLinkAction(
            '/apps/myapp/img/link.png', // icon URL
            'Click me', // name
            'https://.....', // href
            'my_app', // app ID (optional)
        );

        $entry->addAction($emailAction);
        $entry->addAction($linkAction);
    }
}
```

### Estado del usuario

Los proveedores pueden establecer un estado de usuario mediante `IEntry::setStatus`. Este mecanismo está reservado para el estado de usuario de Nextcloud. No debe usarse.
````
