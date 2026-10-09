---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Extender el servidor DAV desde una app: registrar un plugin de SabreDAV, manejar eventos como propFind y evitar consultas repetidas por cada archivo."
---
(nc-dev-dav_extensions)=
# Extender el servidor DAV

## Resumen

Esta página explica cómo una app extiende el servidor DAV: registrar un plugin de SabreDAV mediante el evento `SabrePluginAddEvent`, manejar un evento DAV para añadir una propiedad propia y qué tener en cuenta sobre el rendimiento. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/app_development/dav_extension.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Las apps de Nextcloud pueden extender el servidor DAV registrando plugins de SabreDAV que se enganchan a distintas fases de una solicitud DAV. Los plugins pueden añadir manejadores para métodos y propiedades personalizados, ajustar el comportamiento de la respuesta y más. Consultar [Escribir plugins - sabre/dav](https://sabre.io/dav/writing-plugins/) para conocer otras posibilidades.

### Registrar un plugin DAV

Para registrar un plugin de servidor en la app, registrar un listener de eventos para `OCA\DAV\Events\SabrePluginAddEvent` (introducido en Nextcloud 28). En el manejador del listener, añadir el plugin DAV al servidor.

Por ejemplo:

**Archivo {file}`MyApplication.php`**:

```php
class MyApplication extends App implements IBootstrap {
    public function register(IRegistrationContext $context): void {
        $context->registerEventListener(SabrePluginAddEvent::class, MyListener::class);
    }
}
```

**Archivo {file}`MyListener.php`**:

```php
use OCP\EventDispatcher\Event;
use OCP\EventDispatcher\IEventListener;
use OCA\DAV\Events\SabrePluginAddEvent;

class MyListener implements IEventListener {
    public function handle(Event $event): void {
        if (!$event instanceof SabrePluginAddEvent) {
            return;
        }
        $server = $event->getServer();
        $server->addPlugin(new MyDavPlugin());
    }
}
```

### Manejar eventos DAV

En este ejemplo se registra un manejador para el evento `propFind` y se añade una propiedad personalizada que se devuelve en las solicitudes PROPFIND.

**Archivo {file}`MyDavPlugin.php`**:

```php
use Sabre\DAV\ServerPlugin;
use Sabre\DAV\PropFind;

class MyDavPlugin extends ServerPlugin {

    public function initialize(\Sabre\DAV\Server $server): void {
        // Register your property handler
        $server->on('propFind', $this->handleGetProperties(...));
    }

    private function handleGetProperties(PropFind $propFind, \Sabre\DAV\INode $node): void {
        // Add a property called "my-property" with the value "custom"
        $propFind->handle('{myapplication.example}my-property', fn() => 'custom');
    }
}
```

### Consideraciones de rendimiento

En el ejemplo anterior, si se reemplaza el valor «custom» por una consulta a la base de datos, se introduce un problema de rendimiento: se ejecuta una consulta cada vez que se carga la propiedad. Puede que al principio no sea evidente, pero rápidamente se convierte en un problema, porque se emite un evento `propFind` por cada archivo de una colección para descubrir sus propiedades. Si una colección contiene 1000 hijos, el código lanza 1000 consultas que probablemente son muy parecidas y solo se diferencian en el identificador del archivo.

Para mitigarlo, Nextcloud 32 introduce un nuevo evento que indica a la app que precargue los datos de una colección y de sus hijos inmediatos. Hay más información en {nc-ref}`collection_preload`.
````
