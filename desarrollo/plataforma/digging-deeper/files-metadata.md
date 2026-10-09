---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API de metadatos de archivos: IFilesMetadataManager, eventos en vivo y en segundo plano, occ, PROPPATCH, PROPFIND y SEARCH de WebDAV, y consultas."
---
# Metadatos de archivos

## Resumen

Esta página describe la API de metadatos de archivos: los métodos de `IFilesMetadataManager`, los eventos en vivo y en segundo plano que generan metadatos, su lectura con `occ`, su creación, eliminación, lectura y búsqueda mediante WebDAV y el auxiliar de consultas SQL. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/files-metadata.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 28
:::

Nextcloud incluye una API para gestionar los metadatos de los archivos, con una integración profunda en WebDAV.

### Visión general del concepto

Cuando se crea o modifica un archivo en Nextcloud, se inicia una actualización de sus metadatos. Entonces se puede escuchar el evento *MetadataLiveEvent* para crear, actualizar o eliminar metadatos. Si se sospecha que el proceso consume mucho tiempo o recursos, se puede solicitar un evento en segundo plano llamado *MetadataBackgroundEvent* y hacer allí el trabajo.

### Consumir la API de metadatos de archivos

Para consumir la API de metadatos de archivos hay que {nc-ref}`inyectar <dependency-injection>` `IFilesMetadataManager`.
Este gestor ofrece los siguientes métodos:

- `refreshMetadata(Node $node, int $process)` Este método inicia el proceso de actualización de los metadatos relacionados con un archivo.
- `getMetadata(int $fileId, bool $generate)` Este método devuelve un `IFilesMetadata` que contiene los metadatos relacionados con un archivo.
- `saveMetadata(IFilesMetadata $filesMetadata)` Guarda un `IFilesMetadata` y genera los índices.
- `deleteMetadata(int $fileId)` Elimina todos los metadatos relacionados con un archivo.
- `getMetadataQuery(IQueryBuilder $qb, string $fileTableAlias, string $fileIdField)` Este método devuelve un `IMetadataQuery` para ayudar a construir consultas Sql.
- `getKnownMetadata()` Devuelve una lista de las claves de metadatos conocidas, disponibles globalmente en la instancia, y el tipo esperado de cada valor.
- `initMetadata(string $key, string $type, bool $indexed, bool $remotelyEditable)` Este método permite iniciar un metadato antes de que se examine ninguno de los archivos

### Eventos en vivo y en segundo plano

La app puede capturar dos (2) eventos para generar metadatos. El primero se llama en el proceso principal, justo después de la subida o modificación del archivo.
El segundo se llama en un proceso en segundo plano, iniciado por el cronjob.

- `OCP\FilesMetadata\Event\MetadataLiveEvent`
- `OCP\FilesMetadata\Event\MetadataBackgroundEvent`

Ambos eventos contienen estos métodos:

- `getNode()` Devuelve el `Node` relacionado.
- `getMetadata()` Devuelve `IFilesMetadata`. Cualquier cambio hecho en este objeto se guardará al final del evento.

Generar metadatos a partir de un archivo puede requerir muchos recursos; en ese caso se recomienda ejecutar esta generación
en un trabajo en segundo plano, solicitando una nueva ejecución mediante una llamada al método `MetadataLiveEvent::requestBackgroundJob()`

```php
<?php
/** lib/AppInfo/Application.php */
declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCA\MyApp\Listeners\UpdateFilesMetadata;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;
use OCP\FilesMetadata\Event\MetadataBackgroundEvent;
use OCP\FilesMetadata\Event\MetadataLiveEvent;
use OCP\FilesMetadata\IFilesMetadataManager;
use OCP\FilesMetadata\Model\IMetadataValueWrapper;

class Application extends App implements IBootstrap {
    public function __construct(array $params = []) {
        parent::__construct('my_app', $params);
    }

    public function register(IRegistrationContext $context): void {
        $context->registerEventListener(MetadataLiveEvent::class, UpdateFilesMetadata::class);
        $context->registerEventListener(MetadataBackgroundEvent::class, UpdateFilesMetadata::class);
    }

    public function boot(IBootContext $context): void {
    }
}
```

:::{note}
Si la generación de metadatos requiere pocos recursos, la app solo necesita escuchar `MetadataLiveEvent`
:::

```php
<?php
/** lib/Listeners/UpdateFilesMetadata.php */
declare(strict_types=1);

namespace OCA\MyApp\Listeners;

use OCP\EventDispatcher\Event;
use OCP\EventDispatcher\IEventListener;
use OCP\FilesMetadata\Event\MetadataBackgroundEvent;
use OCP\FilesMetadata\Event\MetadataLiveEvent;

class UpdateFilesMetadata implements IEventListener {
    public function __construct() {
    }

    public function handle(Event $event): void {
        if (!($event instanceof MetadataLiveEvent) &&
            !($event instanceof MetadataBackgroundEvent)) {
            return;
        }

        $node = $event->getNode();

        // my-first-meta is light enough
        $metadata = $event->getMetadata();
        $metadata->setString('my-first-meta', 'yes');

        if ($event instanceof MetadataLiveEvent) {
            $event->requestBackgroundJob();
            return;
        }

        // my-second-meta is too heavy and should be run on a background job
        $metadata->setInt('my-second-meta', 1234, true);
    }
}
```

### Leer metadatos con el comando occ

Los metadatos almacenados relacionados con un archivo pueden obtenerse desde una consola, con el comando `occ`:

```console
$ ./occ metadata:get 1742
{
    "my-first-meta": {
        "value": "yes",
        "type": "string",
        "indexed": false
    },
    "my-second-meta": {
        "value": 1234,
        "type": "int",
        "indexed": true
    }
}
```

:::{note}
El proceso de generación también puede iniciarse con la opción `--refresh`. Tener en cuenta que hay que especificar en el comando el propietario del archivo.
Al actualizar los metadatos desde la consola se disparan tanto `MetadataLiveEvent` como `MetadataBackgroundEvent`, sin esperar al siguiente ciclo de crontab
:::

### Actualizar metadatos con PROPPATCH

Mediante una solicitud WebDAV, un cliente puede crear o actualizar metadatos de un archivo:

```console
curl 'https://cloud.example.net/remote.php/dav/files/test/document.txt' \
    --user test:test \
    --request PROPPATCH \
    --data '<?xml version="1.0" encoding="UTF-8"?>
        <d:propertyupdate xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
            <d:set>
                <d:prop>
                    <nc:metadata-myapp-test>123</nc:metadata-myapp-test>
                </d:prop>
            </d:set>
        </d:propertyupdate>'
```

Esto devolverá un resultado como el siguiente

```xml
<?xml version="1.0"?>
<d:multistatus xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
    <d:response>
        <d:href>/remote.php/dav/files/test/document.txt</d:href>
        <d:propstat>
            <d:prop>
                <nc:metadata-myapp-test/>
            </d:prop>
            <d:status>HTTP/1.1 200 OK</d:status>
        </d:propstat>
    </d:response>
</d:multistatus>
```

:::{note}
WebDAV antepone a los metadatos el prefijo `<nc:metadata-`, lo que significa que el nombre del metadato disponible para el backend en nuestro ejemplo es `myapp-test`.
:::

:::{note}
De forma predeterminada, los metadatos no se pueden editar ni crear con una solicitud PROPPATCH de WebDAV.
Hay que iniciarlos primero con `IFilesMetadataManager::initMetadata()`
:::

```php
/** lib/AppInfo/Application.php */
public function boot(IBootContext $context): void {
    /** @var IFilesMetadataManager $metadataManager */
    $metadataManager = $context->getServerContainer()->get(IFilesMetadataManager::class);
    $metadataManager->initMetadata('myapp-test', IMetadataValueWrapper::TYPE_INT, true, IMetadataValueWrapper::EDIT_REQ_OWNERSHIP);
}
```

### Eliminar metadatos con PROPPATCH

Mediante una solicitud WebDAV, un cliente puede eliminar metadatos de un archivo:

```console
curl 'https://cloud.example.net/remote.php/dav/files/test/document.txt' \
    --user test:test \
    --request PROPPATCH \
    --data '<?xml version="1.0" encoding="UTF-8"?>
        <d:propertyupdate xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
            <d:remove>
                <d:prop>
                    <nc:metadata-myapp-test></nc:metadata-myapp-test>
                </d:prop>
            </d:remove>
        </d:propertyupdate>'
```

### Obtener metadatos con PROPFIND

Los metadatos están disponibles para las solicitudes PROPFIND de WebDAV:

```console
curl 'https://cloud.example.net/remote.php/dav/files/test/document.txt' \
    --user test:test \
    --request PROPFIND \
    --data '<?xml version="1.0" encoding="UTF-8"?>
        <d:propfind xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
            <d:prop>
                <nc:metadata-myapp-test>
            </d:prop>
        </d:propfind>'
```

Esto devolverá un resultado como el siguiente

```xml
<?xml version="1.0"?>
<d:multistatus xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
    <d:response>
        <d:href>/remote.php/dav/files/test/document.txt</d:href>
        <d:propstat>
            <d:prop>
                <nc:metadata-myapp-test>123</nc:metadata-myapp-test>
            </d:prop>
            <d:status>HTTP/1.1 200 OK</d:status>
        </d:propstat>
    </d:response>
</d:multistatus>
```

### SEARCH de WebDAV basado en metadatos

```console
curl 'https://cloud.example.net/remote.php/dav/' \
    --user test:test \
    --request SEARCH \
    --data '<?xml version="1.0" encoding="UTF-8"?>
        <d:searchrequest xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
            <d:basicsearch>
                <d:select>
                    <d:prop>
                        <nc:metadata-myapp-test />
                    </d:prop>
                </d:select>
                <d:from>
                    <d:scope>
                        <d:href>/files/test/</d:href>
                        <d:depth>infinity</d:depth>
                    </d:scope>
                </d:from>
                <d:where>
                    <d:and>
                        <d:gt>
                            <d:prop>
                                <nc:metadata-myapp-test/>
                            </d:prop>
                            <d:literal>10</d:literal>
                        </d:gt>
                        <d:lt>
                            <d:prop>
                                <nc:metadata-myapp-test/>
                            </d:prop>
                            <d:literal>1000</d:literal>
                        </d:lt>
                    </d:and>
                </d:where>
                <d:orderby>
                    <d:order>
                        <d:prop>
                            <nc:metadata-myapp-test/>
                        </d:prop>
                        <d:descending/>
                    </d:order>
                </d:orderby>
                <d:limit>
                    <d:nresults>200</d:nresults>
                    <ns:firstresult>0</ns:firstresult>
                </d:limit>
            </d:basicsearch>
        </d:searchrequest>'
```

Esto devolverá un resultado como el siguiente:

```xml
<?xml version="1.0"?>
<d:multistatus xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
    <d:response>
        <d:href>/remote.php/dav/files/test/</d:href>
        <d:propstat>
            <d:prop>
                <nc:metadata-myapp-test/>
            </d:prop>
            <d:status>HTTP/1.1 404 Not Found</d:status>
        </d:propstat>
    </d:response>
    <d:response>
        <d:href>/remote.php/dav/files/test/document.txt</d:href>
        <d:propstat>
            <d:prop>
                <nc:metadata-myapp-test>123</nc:metadata-myapp-test>
            </d:prop>
            <d:status>HTTP/1.1 200 OK</d:status>
        </d:propstat>
    </d:response>
    <d:response>
        <d:href>/remote.php/dav/files/test/another-one.txt</d:href>
        <d:propstat>
            <d:prop>
                <nc:metadata-myapp-test>369</nc:metadata-myapp-test>
            </d:prop>
            <d:status>HTTP/1.1 200 OK</d:status>
        </d:propstat>
    </d:response>
</d:multistatus>
```

:::{warning}
Los metadatos usados en las sentencias ORDER y WHERE requieren que el metadato se haya iniciado y configurado como indexado.
Hay que llamar a `IFilesMetadataManager::initMetadata()` antes de ejecutar la solicitud WebDAV; de lo contrario, devolverá una excepción por propiedad desconocida.
:::

```php
/** lib/AppInfo/Application.php */
public function boot(IBootContext $context): void {
    /** @var IFilesMetadataManager $metadataManager */
    $metadataManager = $context->getServerContainer()->get(IFilesMetadataManager::class);
    $metadataManager->initMetadata('my-second-meta', IMetadataValueWrapper::TYPE_INT, true);
}
```

### Auxiliar de consultas de metadatos

`IFilesMetadataManager::getMetadataQuery(IQueryBuilder $qb, string $fileTableAlias, string $fileIdField)` devuelve un `IMetadataQuery` para ayudar a construir consultas Sql con los siguientes métodos.
Los parámetros al llamar al método son el alias de la tabla y el nombre del campo que contiene los ids de los archivos.

- `retrieveMetadata()` añade un select sobre los metadatos almacenados
- `extractMetadata(array $row)` convierte una fila obtenida del resultado en un `IFilesMetadata`
- `joinIndex(string $metadataKey, bool $enforce)` une los índices a la consulta
- `getMetadataKeyField(string $metadataKey)` devuelve el campo y la tabla con alias de la clave de un índice
- `getMetadataValueField(string $metadataKey)` devuelve el campo y la tabla con alias del valor de un índice

```php
// generate your normal query builder
$qb = new QueryBuilder();
$qb->select('file_id')
   ->from('my_table', 'my_alias');

/** @var IFilesMetadataManager $metadataManager */
$metadataManager = $context->getServerContainer()->get(IFilesMetadataManager::class);

// get a configured query helper and add a select on the metadata
$metadataQuery = $metadataManager->getMetadataQuery($qb, 'my_alias', 'file_id');
$metadataQuery->retrieveMetadata();

// right join the index table and get only value lower than 8910 for metadata 'my-second-meta'
$metadataQuery->joinIndex('my-second-meta', true);
$qb->where($qb->expr()->lt($metadataQuery->getMetadataValueField('my-second-meta'), $qb->createNamedParameter(8910)));

// get result
$result = $qb->execute();
$items = $result->fetchAll();

// extract metadata from each row
$entries = array_map(function (array $data) use ($metadataQuery): array {
    $data['metadata'] = $metadataQuery->extractMetadata($data)->asArray();
}, $items);
```
````
