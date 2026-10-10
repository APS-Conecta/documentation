---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo una app consume servicios de correo de otras apps mediante el gestor de correo, o los proporciona implementando y registrando un proveedor."
---
(nc-dev-mail-providers)=
# Interfaz de proveedores de correo

## Resumen

Esta página explica la interfaz de proveedores de correo: su terminología, cómo una app consume un servicio de correo de otra app mediante el gestor de correo y cómo proporciona uno creando y registrando las clases de proveedor y de servicio. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/groupware/mail_provider.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Las apps de Nextcloud pueden usar y registrar la interfaz de proveedores de correo para proporcionar funcionalidad de servicio de correo a otras apps o consumirla de ellas.

El acceso a los servicios de correo de otra app lo proporciona la clase Mail Manager. Con esta clase, la app puede encontrar los proveedores y servicios de correo disponibles. Para más detalles, ver la sección correspondiente más abajo.

También es posible lo contrario: registrar una app para que suministre servicios de correo a otras apps. Esto se consigue implementando una clase Mail Provider y una clase Mail Service personalizadas y registrando después el proveedor en el sistema. Para más detalles, ver la sección correspondiente más abajo.

(nc-dev-mail-provider-terminology)=
### Terminología

A modo de aclaración, esta es una referencia de la terminología utilizada.

1. *Proveedor*: es la app que proporciona servicios de correo, p. ej., «BigHostingApp»; puede ser una app para un protocolo concreto
2. *Servicio*: es una cuenta de servicio de correo configurada, p. ej., «Big Email Hosting Co». Cada proveedor de correo puede tener varios servicios de correo configurados para un usuario.

(nc-dev-mail-provider-consume)=
### Consumir un servicio de correo

Para usar el correo como un servicio que proporciona otra app, la app necesita instanciar la clase del gestor de correo y luego usar los métodos incorporados para listar o encontrar un proveedor y un servicio adecuados.

```php
<?php

use OCP\Mail\Provider\IManager as IMailManager;
use OCP\Mail\Provider\Address;
use OCP\Mail\Provider\Attachment;

class MyTestService {

    // Instance the mail manager using dependency injection
    public function __construct(IMailManager $mailManager) {
        private IMailManager $mailManager;
    }

    public function acquireMailProvider(): void {

        // determine if any providers are available
        if (!$this->mailManager->has()) {
            return;
        }

        // retrieve types of providers available (array of id's and labels)
        $types = $this->mailManager->types();

        // retrieve all providers available (array of provider objects)
        $providers = $this->mailManager->providers();

        // retrieve a single provider (provider objects)
        $provider = $this->mailManager->findProviderById('provider1');

    }

    public function acquireMailService(): void {

        // determine if any providers are available
        if (!$this->mailManager->has()) {
            return;
        }

        // retrieve services available for a user (array of service objects)
        $services = $this->mailManager->services('user1');

        // retrieve a single service with a specific mail address (service objects)
        $service = $this->mailManager->findServiceByAddress('user@testing.com');

    }

    public function sendMessage(): void {

        // determine if any providers are available
        if (!$this->mailManager->has()) {
            return;
        }

        // retrieve a single service with a specific mail address (service objects)
        $service = $this->mailManager->findServiceByAddress('user@testing.com');

        // construct mail message and set required parameters
        $message = $service->initiateMessage();
        $message->setFrom(new Address('user1@testing.com', 'User One'));
        $message->setTo(new Address('user2@testing.com', 'User Two'));
        $message->setSubject('Our Great Plan');
        $message->setBodyPlain('See the attached itinerary for our great plan');
        $message->setBodyHtml('<html>See the attached itinerary for our great plan</html>');
        $message->setAttachments(new Attachment(
            'Our great plan itinerary',
            'theplan.txt',
            'text/plain'
        ));
        // send message
        $service->sendMessage($message);

    }
}
```

Para información más detallada sobre los métodos disponibles, sus parámetros y sus valores de retorno, ver el directorio de los proveedores de correo en el repositorio del servidor. (lib/public/Mail/Provider)

(nc-dev-mail-provider-provide)=
### Proporcionar un servicio de correo

Para que la app proporcione un servicio de correo a otras apps, necesita implementar dos interfaces principales, además de las interfaces de la funcionalidad admitida.

#### Paso 1: crear una clase de proveedor de correo

La clase del proveedor de correo es la clase principal que usa el gestor de correo para obtener los servicios disponibles de la app. Cada proveedor de correo puede tener varios servicios de correo configurados para un usuario.

Esta clase necesita implementar la interfaz *IProvider* y tener definidos todos los métodos requeridos.

```php
namespace OCA\BigHostingApp\Provider;

use OCP\Mail\Provider\IProvider;
use OCP\Mail\Provider\IService;

class MailProvider implements IProvider {

    public function id(): string {
        return 'big-hosting-app';
    }

    public function label(): string {
        return 'Big Hosting App';
    }

    public function hasServices(string $userId): bool {
        // app specific code to check for available services
    }

    public function listServices(string $userId): array {
        // app specific code to list all available services
    }

    public function findServiceById(string $userId, string $serviceId): IService | null {
        // app specific code to find a specific services
    }

    public function findServiceByAddress(string $userId, string $address): IService | null {
        // app specific code to find a service with a specific email address
    }

}
```

#### Paso 2: crear una clase de servicio de correo

La clase del servicio de correo es la clase principal que usan otras apps para acceder a la funcionalidad de correo de la app. La clase del proveedor de correo también devuelve esta clase.

Esta clase necesita implementar la interfaz *IService* y tener definidos todos los métodos requeridos. Como la funcionalidad varía entre protocolos, esta clase también necesita extenderse con las interfaces de las funciones admitidas que correspondan, como 'IMessageSend', que proporciona la capacidad de enviar correo.

```php
namespace OCA\BigHostingApp\Provider;

use OCP\Mail\Provider\Address;
use OCP\Mail\Provider\IAddress;
use OCP\Mail\Provider\IMessage;
use OCP\Mail\Provider\IMessageSend;
use OCP\Mail\Provider\IService;
use OCP\Mail\Provider\Message;

class MailService implements IService, IMessageSend {

    public function id(): string {
        return '1 or service1 or anything else';
    }

    public function capable(string $value): bool {
        // app specific code to check if a service is capable of perform a specific function e.g. Sending a Message
    }

    public function capabilities(): array {
        // app specific code to retrieve a list of capabilities
    }

    public function getLabel(): string {
        // app specific code to retrieve the label/description/name of the service
    }

    public function getPrimaryAddress(): IAddress {
        // app specific code to retrieve the primary email address of the service
    }

    public function getSecondaryAddresses(): array {
        // app specific code to retrieve the secondary email addresses (aliases) of the service
    }

    public function initiateMessage(): IMessage {
        // app specific code to create a fresh message e.g message object to send a message or save a message in drafts
    }

    // this function is the extended capabilities added to this class from IMessageSend
    public function sendMessage(IMessage $message, array $option = []): void {
        // app specific code to send a message
    }

}
```

#### Paso 3: registrar el proveedor de correo

El registro se realiza en las etapas iniciales de la carga de la app por parte del sistema de Nextcloud, dentro del archivo 'AppInfo/Application.php'

```php
namespace OCA\BigHostingApp\AppInfo;

use OCA\BigHostingApp\Provider\MailProvider;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IRegistrationContext;

class Application extends App {

    public const APP_ID = 'BigHostingApp';

    public function __construct(array $urlParams = []) {
        parent::__construct(self::APP_ID, $urlParams);
    }

    public function register(IRegistrationContext $context): void {

        // Tip: If your app spans multiple version of Nextcloud, we recommend to make sure the method exists with 'method_exists()'
        $context->registerMailProvider(MailProvider::class);

    }

}
```
````
