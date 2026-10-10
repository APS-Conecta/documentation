---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "El despachador de eventos de OCP, cómo escribir eventos y listeners, los eventos públicos de la plataforma (OCP) y de las apps (OCA), y los hooks obsoletos."
---
(nc-dev-events)=
# Eventos

## Resumen

Esta página describe los mecanismos de eventos de la plataforma: el despachador de eventos de OCP con su esquema de nombres, cómo escribir eventos y listeners, la lista de eventos públicos disponibles, tanto los de la plataforma (OCP) como los de las apps (OCA), y los hooks y el emisor público, ambos obsoletos. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/events.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los eventos se usan para la comunicación entre distintos aspectos del ecosistema de Nextcloud. Se usan internamente en el servidor de Nextcloud, para la comunicación del servidor con las apps y para la comunicación entre apps.

### Descripción general

El término «eventos» es algo amplio en Nextcloud y hay varias formas de emitirlos.

* [Despachador de eventos de OCP](#events-ocp-event-dispatcher)
* [Hooks](#events-hooks)
* [Emisor público](#events-public-emitter)

(events-ocp-event-dispatcher)=
### Despachador de eventos de OCP

Este mecanismo es un enfoque versátil y tipado de los eventos en el código PHP de Nextcloud. Usa objetos en lugar de pasar solo primitivas o arrays sin tipo. Esto debería ayudar a ofrecer una mejor experiencia de desarrollo y, a la vez, reducir el riesgo de cambios inesperados en la API que son difíciles de detectar después de la implementación inicial.

#### Esquema de nombres

El nombre debe reflejar el sujeto y las acciones. Agregar el sufijo *Event* a las clases de eventos facilita reconocer su propósito.

Por ejemplo, si se crea un usuario, se emitirá un *UserCreatedEvent*.

Los eventos suelen emitirse *después* de que el suceso haya ocurrido. Si se emite antes, debe llevar el prefijo *Before*.

Así, *BeforeUserCreatedEvent* se emite *antes* de que los datos del usuario se escriban en la base de datos.

:::{note}
Aunque se puede optar por nombrar las clases de eventos de otra manera, ceñirse a la convención permitirá que los desarrolladores de Nextcloud entiendan más fácilmente las apps de los demás.
:::

:::{note}
Por retrocompatibilidad con la clase [GenericEvent](https://symfony.com/doc/current/components/event_dispatcher/generic_event.html) de Symfony, Nextcloud también ofrece una clase `\OCP\EventDispatcher\Event`. Con la publicación de Nextcloud 22, esta clase quedó obsoleta. En su lugar deben usarse clases de eventos con nombre y con tipo.
:::

#### Escribir eventos

Por regla general, los eventos son clases dedicadas que extienden `\OCP\EventDispatcher\Event`.

```php
<?php

use OCP\EventDispatcher\Event;

namespace OCA\MyApp\Event;

class AddEvent extends Event {}
```

El evento anterior permite señalar que *algo ocurrió*. Pero en muchos casos se quiere transportar datos con el evento, como el recurso afectado. Entonces los eventos actúan como simples [objetos de transferencia de datos](https://en.wikipedia.org/wiki/Data_transfer_object). Por eso necesitan un constructor que reciba los argumentos, miembros privados para almacenarlos y métodos de acceso para leer los valores en los listeners.

```php
<?php

use OCP\EventDispatcher\Event;
use OCP\IUser;

class UserCreatedEvent extends Event {
    private IUser $user;

    public function __construct(IUser $user) {
        parent::__construct();
        $this->user = $user;
    }

    public function getUser(): IUser {
        return $this->user;
    }

}
```

#### Escribir un listener

Un listener puede ser una simple función callback (o cualquier otra cosa que sea [callable](https://www.php.net/manual/en/language.types.callable.php), o una clase dedicada.

##### Callbacks como listeners

Se pueden usar simples callbacks para reaccionar a los eventos. Reciben el objeto del evento como primer y único parámetro. Se puede indicar como tipo la clase base *Event* o la subclase que se espera y para la que se registra.

```php
<?php

use OCA\MyApp\Event\AddEvent;
use OCP\AppFramework\App;
use OCP\EventDispatcher\IEventDispatcher;

namespace OCA\MyApp\AppInfo;

class Application extends App {
    public function __construct() {
        parent::__construct('myapp');
            /* @var IEventDispatcher $dispatcher */
            $dispatcher = $this->getContainer()->query(IEventDispatcher::class);
            $dispatcher->addListener(AddEvent::class, function(AddEvent $event) {
                // ...
            });
    }
}
```

:::{note}
Indicar como tipo la clase real del evento dará un mejor soporte del IDE y de los analizadores estáticos. En general, se puede dar por hecho que el despachador no entregará ningún otro objeto.
:::

##### Clases listener

Una clase que puede gestionar un evento implementará la interfaz `\OCP\EventDispatcher\IEventListener`. Los nombres de las clases deben terminar en *Listener*.

```php
<?php

use OCA\MyApp\Event\AddEvent;
use OCP\EventDispatcher\Event;
use OCP\EventDispatcher\IEventListener;

namespace OCA\MyApp\Event;

class AddTwoListener implements IEventListener {

    public function handle(Event $event): void {
        if (!($event instanceOf AddEvent)) {
            return;
        }

        $event->addToCounter(2);
    }
}
```

:::{note}
En PHP, las indicaciones de tipo de los parámetros no pueden ser más específicas que las de la interfaz; por eso no se puede usar *AddEvent* en la firma del método, sino que hay que usar un *instanceOf*.
:::

En `Application.php` se conectan el evento y la clase listener. La clase solo se instancia cuando se dispara realmente el evento.

```php
<?php

use OCA\MyApp\Event\AddEvent;
use OCA\MyApp\Listener\AddTwoListener;
use OCP\AppFramework\App;
use OCP\EventDispatcher\IEventDispatcher;

namespace OCA\MyApp\AppInfo;

class Application extends App {
    public function __construct() {
        parent::__construct('myapp');
        /* @var IEventDispatcher $eventDispatcher */
        $dispatcher = $this->getContainer()->get(IEventDispatcher::class);
        $dispatcher->addServiceListener(AddEvent::class, AddTwoListener::class);
    }
}
```

:::{note}
El listener se resuelve mediante el contenedor de DI; por eso se le puede agregar un constructor e indicar como tipos los servicios que se necesitan para procesar el evento.
:::

#### Eventos disponibles

Aquí se encuentra un resumen de los eventos públicos que pueden consumirse en las apps. Para más detalles, ver sus archivos fuente.

##### `\OCA\DAV\Events\AddressBookCreatedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario crea una nueva libreta de direcciones.

##### `\OCA\DAV\Events\AddressBookDeletedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario elimina una libreta de direcciones.

##### `\OCA\DAV\Events\AddressBookShareUpdatedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario comparte o deja de compartir una libreta de direcciones.

##### `\OCA\DAV\Events\AddressBookUpdatedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario actualiza una libreta de direcciones.

##### `\OCA\DAV\Events\CachedCalendarObjectCreatedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando se está creando un objeto de calendario en caché al obtener una suscripción de calendario.

##### `\OCA\DAV\Events\CachedCalendarObjectDeletedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando se está eliminando un objeto de calendario en caché al obtener una suscripción de calendario.

##### `\OCA\DAV\Events\CachedCalendarObjectUpdatedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando se está actualizando un objeto de calendario en caché al obtener una suscripción de calendario.

##### `\OCA\DAV\Events\CalendarCreatedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario crea un nuevo calendario.

##### `\OCA\DAV\Events\CalendarDeletedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario elimina un calendario.

##### `\OCA\DAV\Events\CalendarObjectCreatedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario crea un objeto de calendario.

##### `\OCA\DAV\Events\CalendarObjectDeletedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario elimina un objeto de calendario.

##### `\OCA\DAV\Events\CalendarObjectUpdatedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario actualiza un objeto de calendario.

##### `\OCA\DAV\Events\CalendarPublishedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario publica un calendario.

##### `\OCA\DAV\Events\CalendarShareUpdatedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario comparte o deja de compartir un calendario.

##### `\OCA\DAV\Events\CalendarUnpublishedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario deja de publicar un calendario.

##### `\OCA\DAV\Events\CalendarUpdatedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario actualiza un calendario.

##### `\OCA\DAV\Events\CardCreatedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario crea una nueva tarjeta en una libreta de direcciones.

##### `\OCA\DAV\Events\CardDeletedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario elimina una tarjeta de una libreta de direcciones.

##### `\OCA\DAV\Events\CardUpdatedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario actualiza una tarjeta de una libreta de direcciones.

##### `OCA\DAV\Events\SabrePluginAddEvent`

:::{versionadded} 28
:::

Este evento se activa durante la configuración del servidor SabreDAV para permitir el registro de plugins adicionales.

##### `\OCA\DAV\Events\SabrePluginAuthInitEvent`

:::{versionadded} 20
:::

Este evento se activa durante la configuración del servidor SabreDAV para permitir el registro de backends de autenticación adicionales.

##### `\OCA\DAV\Events\SubscriptionCreatedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario crea una nueva suscripción de calendario.

##### `\OCA\DAV\Events\SubscriptionDeletedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario elimina una suscripción de calendario.

##### `\OCA\DAV\Events\SubscriptionUpdatedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando un usuario actualiza una suscripción de calendario.

##### `\OCA\FederatedFileSharing\Events\FederatedShareAddedEvent`

:::{versionadded} 20
:::

Este evento se activa cuando se agrega correctamente un recurso compartido federado.

##### `\OCA\Files\Event\LoadAdditionalScriptsEvent`

:::{versionadded} 17
:::

Este evento se activa cuando se renderiza la app de archivos. Puede usarse para agregar scripts adicionales a la app de archivos.

##### `\OCA\Files_Sharing\Event\BeforeTemplateRenderedEvent`

:::{versionadded} 20
:::

Se emite antes de que ocurra el paso de renderizado de la página del recurso compartido público. El evento contiene un indicador que especifica si se trata de la página de autenticación de un recurso compartido público.

##### `\OCA\Files_Trashbin\Events\MoveToTrashEvent`

:::{versionadded} 28
:::

Se emite después de que un archivo o una carpeta se mueve a la papelera.

##### `\OCA\Settings\Events\BeforeTemplateRenderedEvent`

:::{versionadded} 20
:::

Este evento se activa justo antes de que se renderice la plantilla de gestión de usuarios.

##### `\OCA\User_LDAP\Events\GroupBackendRegistered`

:::{versionadded} 20
:::

Este evento se activa justo después de que se registra el backend de grupos de LDAP.

##### `\OCA\User_LDAP\Events\UserBackendRegistered`

:::{versionadded} 20
:::

Este evento se activa justo después de que se registra el backend de usuarios de LDAP.

##### `\OCA\Viewer\Event\LoadViewer`

:::{versionadded} 17
:::

Este evento se activa cada vez que se carga el visor y deben cargarse las extensiones.

##### `OCP\Accounts\UserUpdatedEvent`

:::{versionadded} 28
:::

Este evento se activa cuando se actualizaron los datos de la cuenta de un usuario.

##### `OCP\App\Events\AppDisableEvent`

:::{versionadded} 27
:::

Este evento se activa cuando se deshabilita una app.

##### `OCP\App\Events\AppEnableEvent`

:::{versionadded} 27
:::

Este evento se activa cuando se habilita una app.

##### `OCP\App\Events\AppUpdateEvent`

:::{versionadded} 27
:::

Este evento se activa cuando se actualiza una app.

##### `OCP\App\ManagerEvent`

:::{versionadded} 9
:::

Clase ManagerEvent

##### `OCP\AppFramework\Http\Events\BeforeLoginTemplateRenderedEvent`

:::{versionadded} 28
:::

Se emite antes del paso de renderizado del TemplateResponse del inicio de sesión.

##### `OCP\AppFramework\Http\Events\BeforeTemplateRenderedEvent`

:::{versionadded} 20
:::

Se emite antes del paso de renderizado de cada TemplateResponse. El evento contiene un indicador que especifica si un usuario ha iniciado sesión.

##### `OCP\Authentication\Events\AnyLoginFailedEvent`

:::{versionadded} 26
:::

Se emite cuando falla la autenticación

##### `OCP\Authentication\Events\LoginFailedEvent`

:::{versionadded} 19
:::

Se emite cuando falla la autenticación, pero solo si el nombre de inicio de sesión puede asociarse a un usuario existente.

##### `OCP\Authentication\Events\TokenInvalidatedEvent`

:::{versionadded} 32
:::

Se emite cuando se invalida un token de autenticación.

##### `OCP\Authentication\TwoFactorAuth\RegistryEvent`

:::{versionadded} 15
:::

##### `OCP\Authentication\TwoFactorAuth\TwoFactorProviderChallengeFailed`

:::{versionadded} 28
:::

##### `OCP\Authentication\TwoFactorAuth\TwoFactorProviderChallengePassed`

:::{versionadded} 28
:::

##### `OCP\Authentication\TwoFactorAuth\TwoFactorProviderDisabled`

:::{versionadded} 20
:::

##### `OCP\Authentication\TwoFactorAuth\TwoFactorProviderForUserDisabled`

:::{versionadded} 22
:::

##### `OCP\Authentication\TwoFactorAuth\TwoFactorProviderForUserEnabled`

:::{versionadded} 22
:::

##### `OCP\Authentication\TwoFactorAuth\TwoFactorProviderForUserRegistered`

:::{versionadded} 28
:::

##### `OCP\Authentication\TwoFactorAuth\TwoFactorProviderForUserUnregistered`

:::{versionadded} 28
:::

##### `OCP\Authentication\TwoFactorAuth\TwoFactorProviderUserDeleted`

:::{versionadded} 28
:::

##### `OCP\BeforeSabrePubliclyLoadedEvent`

:::{versionadded} 26
:::

Se despacha antes de que se cargue Sabre al acceder a los endpoints públicos de webdav. Puede usarse, por ejemplo, para inyectar un plugin de Sabre

##### `OCP\Calendar\Events\CalendarObjectCreatedEvent`

:::{versionadded} 32
:::

##### `OCP\Calendar\Events\CalendarObjectDeletedEvent`

:::{versionadded} 32
:::

##### `OCP\Calendar\Events\CalendarObjectMovedEvent`

:::{versionadded} 32
:::

##### `OCP\Calendar\Events\CalendarObjectMovedToTrashEvent`

:::{versionadded} 32
:::

##### `OCP\Calendar\Events\CalendarObjectRestoredEvent`

:::{versionadded} 32
:::

##### `OCP\Calendar\Events\CalendarObjectUpdatedEvent`

:::{versionadded} 32
:::

##### `OCP\Collaboration\AutoComplete\AutoCompleteEvent`

:::{versionadded} 16
:::

##### `OCP\Collaboration\AutoComplete\AutoCompleteFilterEvent`

:::{versionadded} 28
:::

##### `OCP\Collaboration\Reference\RenderReferenceEvent`

:::{versionadded} 25
:::

Evento que se emite cuando las apps podrían renderizar referencias, como vistas previas de enlaces o widgets del selector inteligente. Puede usarse para inyectar scripts que lo extiendan. Hay más detalles en el análisis en profundidad {nc-ref}`Reference providers`.

##### `OCP\Collaboration\Resources\LoadAdditionalScriptsEvent`

:::{versionadded} 25
:::

Las apps usan este evento para registrar sus propios scripts de frontend con el fin de integrar proyectos en su app. Las apps también deben despachar el evento para cargar los scripts durante la carga de la página

##### `OCP\Comments\CommentsEntityEvent`

:::{versionadded} 9.1
:::

:::{versionchanged} 28.0.0
Se despacha como evento tipado
:::

Clase CommentsEntityEvent

##### `OCP\Comments\CommentsEvent`

:::{versionadded} 9
:::

Clase CommentsEvent

##### `OCP\Config\BeforePreferenceDeletedEvent`

:::{versionadded} 25
:::

##### `OCP\Config\BeforePreferenceSetEvent`

:::{versionadded} 25
:::

##### `OCP\Console\ConsoleEvent`

:::{versionadded} 9
:::

Clase ConsoleEvent

##### `OCP\Contacts\Events\ContactInteractedWithEvent`

:::{versionadded} 19
:::

Un evento que permite a las apps notificar a otros componentes sobre una interacción entre dos usuarios. Puede usarse para construir mejores recomendaciones y sugerencias en las interfaces de usuario. Quienes lo emitan deberían agregar al menos un identificador (uid, correo electrónico, ID de nube federada) del destinatario de la interacción.

##### `OCP\DB\Events\AddMissingColumnsEvent`

:::{versionadded} 28
:::

Evento que permite a las apps registrar información sobre columnas faltantes de la base de datos. Este evento se despachará para la comprobación en las configuraciones de administración y al ejecutar occ db:add-missing-columns, que entonces creará esas columnas

##### `OCP\DB\Events\AddMissingIndicesEvent`

:::{versionadded} 28
:::

Evento que permite a las apps registrar información sobre índices faltantes de la base de datos. Este evento se despachará para la comprobación en las configuraciones de administración y al ejecutar occ db:add-missing-indices, que entonces creará esos índices

##### `OCP\DB\Events\AddMissingPrimaryKeyEvent`

:::{versionadded} 28
:::

Evento que permite a las apps registrar información sobre claves primarias faltantes de la base de datos. Este evento se despachará para la comprobación en las configuraciones de administración y al ejecutar occ db:add-missing-primary-keys, que entonces creará esas claves

##### `OCP\DirectEditing\RegisterDirectEditorEvent`

:::{versionadded} 18
:::

Evento que permite registrar el editor directo.

##### `OCP\EventDispatcher\GenericEvent`

:::{versionadded} 18
:::

Clase GenericEvent. Reimplementación de conveniencia de \Symfony\Component\GenericEvent sobre \OCP\EventDispatcher\Event

##### `OCP\Federation\Events\TrustedServerRemovedEvent`

:::{versionadded} 25
:::

##### `OCP\Files\Cache\AbstractCacheEvent`

:::{versionadded} 22
:::

##### `OCP\Files\Cache\CacheEntryInsertedEvent`

:::{versionadded} 21
:::

Evento para cuando se inserta una entrada existente en la caché

##### `OCP\Files\Cache\CacheEntryRemovedEvent`

:::{versionadded} 21
:::

Evento para cuando se elimina una entrada existente de la caché

##### `OCP\Files\Cache\CacheEntryUpdatedEvent`

:::{versionadded} 21
:::

Evento para cuando se actualiza una entrada existente en la caché

##### `OCP\Files\Cache\CacheInsertEvent`

:::{versionadded} 16
:::

Evento para cuando se agrega una entrada nueva a la caché

##### `OCP\Files\Cache\CacheUpdateEvent`

:::{versionadded} 16
:::

Evento para cuando se actualiza una entrada existente en la caché

##### `OCP\Files\Config\Event\UserMountAddedEvent`

:::{versionadded} 31
:::

Evento que se emite cuando se agregó un punto de montaje de usuario.

##### `OCP\Files\Config\Event\UserMountRemovedEvent`

:::{versionadded} 31
:::

Evento que se emite cuando se eliminó un punto de montaje de usuario.

##### `OCP\Files\Config\Event\UserMountUpdatedEvent`

:::{versionadded} 31
:::

Evento que se emite cuando se movió un punto de montaje de usuario.

##### `OCP\Files\Events\BeforeDirectFileDownloadEvent`

:::{versionadded} 25
:::

Este evento se activa cuando un usuario intenta descargar un archivo directamente.

##### `OCP\Files\Events\BeforeFileScannedEvent`

:::{versionadded} 18
:::

##### `OCP\Files\Events\BeforeFileSystemSetupEvent`

:::{versionadded} 31
:::

Evento que se activa antes de que se configure el sistema de archivos

##### `OCP\Files\Events\BeforeFolderScannedEvent`

:::{versionadded} 18
:::

##### `OCP\Files\Events\BeforeZipCreatedEvent`

:::{versionadded} 25
:::

Este evento se activa antes de que se cree un archivo comprimido cuando un usuario solicitó descargar una carpeta o varios archivos. Estableciendo *successful* en false se puede abortar la creación del tar y denegar la descarga.

##### `OCP\Files\Events\FileCacheUpdated`

:::{versionadded} 18
:::

##### `OCP\Files\Events\FileScannedEvent`

:::{versionadded} 18
:::

##### `OCP\Files\Events\FolderScannedEvent`

:::{versionadded} 18
:::

##### `OCP\Files\Events\InvalidateMountCacheEvent`

:::{versionadded} 24
:::

Se usa para notificar al gestor de configuración del sistema de archivos que cambiaron los puntos de montaje disponibles para un usuario

##### `OCP\Files\Events\Node\BeforeNodeCopiedEvent`

:::{versionadded} 20
:::

##### `OCP\Files\Events\Node\BeforeNodeCreatedEvent`

:::{versionadded} 20
:::

##### `OCP\Files\Events\Node\BeforeNodeDeletedEvent`

:::{versionadded} 20
:::

##### `OCP\Files\Events\Node\BeforeNodeReadEvent`

:::{versionadded} 20
:::

##### `OCP\Files\Events\Node\BeforeNodeRenamedEvent`

:::{versionadded} 20
:::

##### `OCP\Files\Events\Node\BeforeNodeTouchedEvent`

:::{versionadded} 20
:::

##### `OCP\Files\Events\Node\BeforeNodeWrittenEvent`

:::{versionadded} 20
:::

##### `OCP\Files\Events\Node\FilesystemTornDownEvent`

:::{versionadded} 24
:::

Evento que se dispara después de que se haya desmantelado el sistema de archivos

##### `OCP\Files\Events\Node\NodeCopiedEvent`

:::{versionadded} 20
:::

##### `OCP\Files\Events\Node\NodeCreatedEvent`

:::{versionadded} 20
:::

##### `OCP\Files\Events\Node\NodeDeletedEvent`

:::{versionadded} 20
:::

##### `OCP\Files\Events\Node\NodeRenamedEvent`

:::{versionadded} 20
:::

##### `OCP\Files\Events\Node\NodeTouchedEvent`

:::{versionadded} 20
:::

##### `OCP\Files\Events\Node\NodeWrittenEvent`

:::{versionadded} 20
:::

##### `OCP\Files\Events\NodeAddedToCache`

:::{versionadded} 18
:::

##### `OCP\Files\Events\NodeAddedToFavorite`

:::{versionadded} 28
:::

##### `OCP\Files\Events\NodeRemovedFromCache`

:::{versionadded} 18
:::

##### `OCP\Files\Events\NodeRemovedFromFavorite`

:::{versionadded} 28
:::

##### `OCP\Files\ObjectStore\Events\BucketCreatedEvent`

:::{versionadded} 33
:::

##### `OCP\Files\Template\BeforeGetTemplatesEvent`

:::{versionadded} 30
:::

##### `OCP\Files\Template\FileCreatedFromTemplateEvent`

:::{versionadded} 21
:::

##### `OCP\Files\Template\RegisterTemplateCreatorEvent`

:::{versionadded} 30
:::

##### `OCP\FilesMetadata\Event\MetadataBackgroundEvent`

:::{versionadded} 28
:::

MetadataBackgroundEvent es un evento similar a MetadataLiveEvent, pero se despacha en un hilo en segundo plano en lugar del hilo en vivo. Esto significa que no hay límite para el tiempo necesario para generar los metadatos propios.

##### `OCP\FilesMetadata\Event\MetadataLiveEvent`

:::{versionadded} 28
:::

MetadataLiveEvent es un evento que se inicia cuando se crea o actualiza un archivo. La app contiene el Node relacionado con el archivo creado/actualizado y un FilesMetadata que ya contiene los metadatos conocidos en ese momento.

Establecer metadatos nuevos, o modificar metadatos ya existentes con un valor distinto, activará el guardado de los metadatos en la base de datos.

##### `OCP\FilesMetadata\Event\MetadataNamedEvent`

:::{versionadded} 28
:::

MetadataNamedEvent es un evento similar a MetadataBackgroundEvent, completado con un nombre de destino, que se usa para limitar la actualización de metadatos solo a los listeners capaces de excluirse a sí mismos mediante un filtro. Esto significa que, al usar este evento, la app debe implementar un filtro sobre el nombre registrado del evento que devuelve getName()

- Este evento se activa principalmente cuando se agrega un nombre registrado al escaneo de archivos: es decir, ./occ files:scan --generate-metadata [name]

##### `OCP\Group\Events\BeforeGroupChangedEvent`

:::{versionadded} 26
:::

##### `OCP\Group\Events\BeforeGroupCreatedEvent`

:::{versionadded} 18
:::

##### `OCP\Group\Events\BeforeGroupDeletedEvent`

:::{versionadded} 18
:::

##### `OCP\Group\Events\BeforeUserAddedEvent`

:::{versionadded} 18
:::

##### `OCP\Group\Events\BeforeUserRemovedEvent`

:::{versionadded} 18
:::

##### `OCP\Group\Events\GroupChangedEvent`

:::{versionadded} 26
:::

##### `OCP\Group\Events\GroupCreatedEvent`

:::{versionadded} 18
:::

##### `OCP\Group\Events\GroupDeletedEvent`

:::{versionadded} 18
:::

##### `OCP\Group\Events\SubAdminAddedEvent`

:::{versionadded} 21
:::

##### `OCP\Group\Events\SubAdminRemovedEvent`

:::{versionadded} 21
:::

##### `OCP\Group\Events\UserAddedEvent`

:::{versionadded} 18
:::

##### `OCP\Group\Events\UserRemovedEvent`

:::{versionadded} 18
:::

##### `OCP\Log\Audit\CriticalActionPerformedEvent`

:::{versionadded} 22
:::

Se emite cuando la app admin_audit debe registrar una entrada

##### `OCP\Log\BeforeMessageLoggedEvent`

:::{versionadded} 28
:::

Evento para cuando se está registrando un elemento de registro

##### `OCP\Mail\Events\BeforeMessageSent`

:::{versionadded} 19
:::

Se emite antes de que se envíe un correo del sistema. Puede usarse para alterar el mensaje.

##### `OCP\Navigation\Events\LoadAdditionalEntriesEvent`

:::{versionadded} 31
:::

##### `OCP\OCM\Events\ResourceTypeRegisterEvent`

:::{versionadded} 28
:::

Este evento sirve para registrar recursos de OCM adicionales antes de que la API los devuelva en la lista de proveedores de OCM y en la capability

##### `OCP\Preview\BeforePreviewFetchedEvent`

:::{versionadded} 25.0.1
:::

:::{versionchanged} 28.0.0
los argumentos del constructor `$width`, `$height`, `$crop` y `$mode` ya no admiten null.
:::

:::{versionchanged} 31.0.0
se agregó el argumento del constructor `$mimeType`
:::

Se emite antes de que se obtenga la vista previa de un archivo. Puede usarse para bloquear el renderizado de la vista previa lanzando una `OCP\Files\NotFoundException`

##### `OCP\Profile\BeforeTemplateRenderedEvent`

:::{versionadded} 25
:::

Se emite antes de que ocurra el paso de renderizado de la página del perfil público.

##### `OCP\SabrePluginEvent`

:::{versionadded} 8.2
:::

##### `OCP\Security\CSP\AddContentSecurityPolicyEvent`

:::{versionadded} 17
:::

Permite inyectar algo en la política de contenido predeterminada. Esto es útil, por ejemplo, cuando se inyecta código Javascript en una vista que pertenece a otro controlador y no se puede modificar su propio Content-Security-Policy. Cabe señalar que el ajuste solo se aplica a las aplicaciones que usan controladores de AppFramework.

ADVERTENCIA: usar esta API de forma incorrecta puede hacer que la instancia sea más insegura. Hay que pensarlo dos veces antes de agregar recursos a la lista de permitidos. Cabe señalar también que no es posible usar las funciones *disallowXYZ*.

##### `OCP\Security\Events\GenerateSecurePasswordEvent`

:::{versionadded} 18
:::

Evento para solicitar que se genere una contraseña segura.

Desde Nextcloud 31, este evento también ofrece un método `getContext` que permite aplicar reglas distintas para distintos contextos de contraseña, como las contraseñas de cuenta o las contraseñas de recursos compartidos.

##### `OCP\Security\Events\ValidatePasswordPolicyEvent`

:::{versionadded} 18
:::

Este evento puede emitirse para solicitar la validación de una contraseña. Si hay instalada una app de política de contraseñas y la contraseña no es válida, se lanzará una *\OCP\HintException*.

Desde Nextcloud 31, este evento también ofrece un método `getContext` que permite aplicar reglas distintas para distintos contextos de contraseña, como las contraseñas de cuenta o las contraseñas de recursos compartidos.

##### `OCP\Security\FeaturePolicy\AddFeaturePolicyEvent`

:::{versionadded} 17
:::

Evento que permite registrar una cabecera de política de funciones en una solicitud.

##### `OCP\Settings\Events\DeclarativeSettingsGetValueEvent`

:::{versionadded} 29
:::

##### `OCP\Settings\Events\DeclarativeSettingsRegisterFormEvent`

:::{versionadded} 29
:::

##### `OCP\Settings\Events\DeclarativeSettingsSetValueEvent`

:::{versionadded} 29
:::

##### `OCP\Share\Events\BeforeShareCreatedEvent`

:::{versionadded} 28
:::

##### `OCP\Share\Events\BeforeShareDeletedEvent`

:::{versionadded} 28
:::

##### `OCP\Share\Events\ShareAcceptedEvent`

:::{versionadded} 28
:::

##### `OCP\Share\Events\ShareCreatedEvent`

:::{versionadded} 18
:::

##### `OCP\Share\Events\ShareDeletedEvent`

:::{versionadded} 21
:::

##### `OCP\Share\Events\ShareDeletedFromSelfEvent`

:::{versionadded} 28
:::

##### `OCP\Share\Events\VerifyMountPointEvent`

:::{versionadded} 19
:::

##### `OCP\Share\ShareReview\Events\ShareReviewAccessCheckEvent`

:::{versionadded} 34.0.2
:::

Control de autorización para eliminar un recurso compartido gestionado por una app a través de una app de revisión de recursos compartidos. Lo despacha la app propietaria del recurso compartido (su implementación de `OCP\Share\ShareReview\IShareReviewSource`) al comienzo de `deleteShare()`, antes de eliminar nada. La app de revisión de recursos compartidos escucha este evento y responde con `grantAccess()` o `denyAccess()` según si el usuario actual es un operador autorizado de revisión de recursos compartidos; las apps que solo exponen recursos compartidos no deben escucharlo. El evento deniega por defecto: si ningún listener responde, el recurso compartido no debe eliminarse. Una vez denegado, se ignoran las concesiones posteriores y se detiene la propagación del evento.

##### `OCP\Share\ShareReview\RegisterShareReviewSourceEvent`

:::{versionadded} 34.0.2
:::

Evento que despacha una app de revisión de recursos compartidos para recopilar fuentes de recursos compartidos de otras apps. Los listeners registran el nombre de clase de su implementación de `OCP\Share\ShareReview\IShareReviewSource`, cuyo método `getShares()` devuelve una lista de objetos `OCP\Share\ShareReview\ShareReviewEntry`.

##### `OCP\SpeechToText\Events\TranscriptionFailedEvent`

:::{versionadded} 27
:::

Este evento se emite si falló la transcripción de un archivo multimedia mediante un proveedor de voz a texto

##### `OCP\SpeechToText\Events\TranscriptionSuccessfulEvent`

:::{versionadded} 27
:::

Este evento se emite cuando la transcripción de un archivo multimedia se completó correctamente

##### `OCP\SystemTag\ManagerEvent`

:::{versionadded} 9
:::

Clase ManagerEvent

##### `OCP\SystemTag\MapperEvent`

:::{versionadded} 9
:::

Clase MapperEvent

##### `OCP\SystemTag\SystemTagsEntityEvent`

:::{versionadded} 9.1
:::

:::{versionchanged} 28.0.0
Se despacha como evento tipado
:::

Clase SystemTagsEntityEvent

##### `OCP\TaskProcessing\Events\GetTaskProcessingProvidersEvent`

:::{versionadded} 32
:::

Evento que despacha el servidor para recopilar proveedores de procesamiento de tareas y tipos de tarea personalizados desde los listeners (como AppAPI). Los listeners deberían agregar sus proveedores y tipos de tarea con los métodos addProvider() y addTaskType().

##### `OCP\TaskProcessing\Events\TaskFailedEvent`

:::{versionadded} 30
:::

##### `OCP\TaskProcessing\Events\TaskSuccessfulEvent`

:::{versionadded} 30
:::

##### `OCP\TextProcessing\Events\TaskFailedEvent`

:::{versionadded} 27.1
:::

##### `OCP\TextProcessing\Events\TaskSuccessfulEvent`

:::{versionadded} 27.1
:::

##### `OCP\TextToImage\Events\TaskFailedEvent`

:::{versionadded} 28
:::

##### `OCP\TextToImage\Events\TaskSuccessfulEvent`

:::{versionadded} 28
:::

##### `OCP\User\Events\BeforePasswordUpdatedEvent`

:::{versionadded} 18
:::

Se emite antes de que se actualice la contraseña del usuario.

##### `OCP\User\Events\BeforeUserCreatedEvent`

:::{versionadded} 18
:::

Se emite antes de que se cree un usuario nuevo en el backend.

##### `OCP\User\Events\BeforeUserDeletedEvent`

:::{versionadded} 18
:::

##### `OCP\User\Events\BeforeUserIdUnassignedEvent`

:::{versionadded} 31
:::

Se emite antes de eliminar el mapeo entre un usuario externo y un userid interno

##### `OCP\User\Events\BeforeUserLoggedInEvent`

:::{versionadded} 18
:::

##### `OCP\User\Events\BeforeUserLoggedInWithCookieEvent`

:::{versionadded} 18
:::

Se emite antes de que un usuario inicie sesión mediante las cookies de remember-me.

##### `OCP\User\Events\BeforeUserLoggedOutEvent`

:::{versionadded} 18
:::

Se emite antes de que un usuario cierre sesión.

##### `OCP\User\Events\OutOfOfficeChangedEvent`

:::{versionadded} 28
:::

Se emite cuando cambió el período de ausencia de un usuario

##### `OCP\User\Events\OutOfOfficeClearedEvent`

:::{versionadded} 28
:::

Se emite cuando se borra el período de ausencia de un usuario

##### `OCP\User\Events\OutOfOfficeEndedEvent`

:::{versionadded} 28
:::

Se emite cuando terminó el período de ausencia de un usuario

##### `OCP\User\Events\OutOfOfficeScheduledEvent`

:::{versionadded} 28
:::

Se emite cuando se programa el período de ausencia de un usuario

##### `OCP\User\Events\OutOfOfficeStartedEvent`

:::{versionadded} 28
:::

Se emite cuando comenzó el período de ausencia de un usuario

##### `OCP\User\Events\PasswordUpdatedEvent`

:::{versionadded} 18
:::

Se emite cuando se actualizó la contraseña del usuario.

##### `OCP\User\Events\PostLoginEvent`

:::{versionadded} 18
:::

##### `OCP\User\Events\UserChangedEvent`

:::{versionadded} 18
:::

##### `OCP\User\Events\UserCreatedEvent`

:::{versionadded} 18
:::

Se emite cuando se creó un usuario nuevo en el backend.

##### `OCP\User\Events\UserDeletedEvent`

:::{versionadded} 18
:::

##### `OCP\User\Events\UserFirstTimeLoggedInEvent`

:::{versionadded} 28
:::

##### `OCP\User\Events\UserIdAssignedEvent`

:::{versionadded} 31
:::

Lo emiten los backends (como user_ldap) cuando un usuario creado externamente se mapea por primera vez y se le asigna un userid

##### `OCP\User\Events\UserIdUnassignedEvent`

:::{versionadded} 31
:::

Se emite después de eliminar el mapeo entre un usuario externo y un userid interno

##### `OCP\User\Events\UserLiveStatusEvent`

:::{versionadded} 20
:::

##### `OCP\User\Events\UserLoggedInEvent`

:::{versionadded} 18
:::

##### `OCP\User\Events\UserLoggedInWithCookieEvent`

:::{versionadded} 18
:::

Se emite cuando un usuario inició sesión correctamente mediante las cookies de remember-me.

##### `OCP\User\Events\UserLoggedOutEvent`

:::{versionadded} 18
:::

Se emite cuando un usuario cerró sesión correctamente.

##### `OCP\User\GetQuotaEvent`

:::{versionadded} 20
:::

Evento que permite a las apps

##### `OCP\WorkflowEngine\Events\LoadSettingsScriptsEvent`

:::{versionadded} 20
:::

Se emite cuando se carga la página de ajustes del motor de flujos de trabajo.

##### `OCP\WorkflowEngine\Events\RegisterChecksEvent`

:::{versionadded} 18
:::

##### `OCP\WorkflowEngine\Events\RegisterEntitiesEvent`

:::{versionadded} 18
:::

##### `OCP\WorkflowEngine\Events\RegisterOperationsEvent`

:::{versionadded} 18
:::

(events-hooks)=
### Hooks

:::{deprecated} 18
Usar en su lugar el [despachador de eventos de OCP](#events-ocp-event-dispatcher).
:::

Los hooks se usan para ejecutar código antes o después de que haya ocurrido un suceso. Esto es útil, por ejemplo, para ejecutar código de limpieza después de que se hayan eliminado usuarios, grupos o archivos. Los hooks deben registrarse en el {nc-doc}`proceso de arranque <developer_manual/app_development/bootstrap>`.

#### Hooks disponibles

El ámbito es el primer parámetro que se pasa al método **listen**; el segundo parámetro es el método y el tercero, el callback que debe ejecutarse una vez que se llama al hook, p. ej.:

```php
<?php

// listen on user predelete
$callback = function($user) {
    // your code that executes before $user is deleted
};
$userManager->listen('\OC\User', 'preDelete', $callback);
```

Los hooks también pueden quitarse con el método **removeListener** del objeto:

```php
<?php

// delete previous callback
$userManager->removeListener(null, null, $callback);
```

Están disponibles los siguientes hooks:

#### Sesión

Se puede inyectar desde el ServerContainer con el servicio `\OCP\IUserSession`.

Hooks disponibles en el ámbito **\OC\User**:

* **preSetPassword** (\OC\User\User $user, string $password, string $recoverPassword)
* **postSetPassword** (\OC\User\User $user, string $password, string $recoverPassword)
* **changeUser** (\OC\User\User $user, string $feature, string $value)
* **preDelete** (\OC\User\User $user)
* **postDelete** (\OC\User\User $user)
* **preCreateUser** (string $uid, string $password)
* **postCreateUser** (\OC\User\User $user)
* **preLogin** (string $user, string $password)
* **postLogin** (\OC\User\User $user, string $password)
* **logout** ()

#### UserManager

Se puede inyectar desde el ServerContainer con el servicio `\OCP\IUserManager`.

Hooks disponibles en el ámbito **\OC\User**:

* **preSetPassword** (\OC\User\User $user, string $password, string $recoverPassword)
* **postSetPassword** (\OC\User\User $user, string $password, string $recoverPassword)
* **preDelete** (\OC\User\User $user)
* **postDelete** (\OC\User\User $user)
* **preCreateUser** (string $uid, string $password)
* **postCreateUser** (\OC\User\User $user, string $password)

#### GroupManager

Hooks disponibles en el ámbito **\OC\Group**:

* **preAddUser** (\OC\Group\Group $group, \OC\User\User $user)
* **postAddUser** (\OC\Group\Group $group, \OC\User\User $user)
* **preRemoveUser** (\OC\Group\Group $group, \OC\User\User $user)
* **postRemoveUser** (\OC\Group\Group $group, \OC\User\User $user)
* **preDelete** (\OC\Group\Group $group)
* **postDelete** (\OC\Group\Group $group)
* **preCreate** (string $groupId)
* **postCreate** (\OC\Group\Group $group)

#### Raíz del sistema de archivos

Se puede inyectar desde el ServerContainer llamando al método **getRootFolder()**, **getUserFolder()** o **getAppFolder()**.

Para activar estos eventos en la app, hay que agregar lo siguiente al archivo *info.xml*:

```xml
<types>
    <filesystem/>
</types>
```

Hooks del sistema de archivos disponibles en el ámbito **\OC\Files**:

* **preWrite** (\OCP\Files\Node $node)
* **postWrite** (\OCP\Files\Node $node)
* **preCreate** (\OCP\Files\Node $node)
* **postCreate** (\OCP\Files\Node $node)
* **preDelete** (\OCP\Files\Node $node)
* **postDelete** (\OCP\Files\Node $node)
* **preTouch** (\OCP\Files\Node $node, int $mtime)
* **postTouch** (\OCP\Files\Node $node)
* **preCopy** (\OCP\Files\Node $source, \OCP\Files\Node $target)
* **postCopy** (\OCP\Files\Node $source, \OCP\Files\Node $target)
* **preRename** (\OCP\Files\Node $source, \OCP\Files\Node $target)
* **postRename** (\OCP\Files\Node $source, \OCP\Files\Node $target)

#### Escáner del sistema de archivos

Hooks del escáner del sistema de archivos disponibles en el ámbito **\OC\Files\Utils\Scanner**:

* **scanFile** (string $absolutePath)
* **scanFolder** (string $absolutePath)
* **postScanFile** (string $absolutePath)
* **postScanFolder** (string $absolutePath)

(events-public-emitter)=
### Emisor público

:::{deprecated} 18
Usar en su lugar el [despachador de eventos de OCP](#events-ocp-event-dispatcher).
:::

Por definir
````
