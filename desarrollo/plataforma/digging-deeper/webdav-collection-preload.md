---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo usar el evento preloadCollection de un PROPFIND WebDAV para precargar en bloque los datos de los hijos de una colección y evitar consultas N+1."
---
(nc-dev-collection_preload)=
# Eventos de precarga de colecciones WebDAV

## Resumen

Esta página explica el evento de precarga que se emite durante un PROPFIND de WebDAV sobre una colección: cuándo se emite, cómo suscribirse a él desde un plugin de Sabre, los plugins que ya lo usan y las buenas prácticas para precargar datos sin trabajo duplicado. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/webdav_collection_preload.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Descripción general

Durante un PROPFIND de WebDAV sobre una colección de SabreDAV con `Depth > 0`,
Nextcloud emite un evento de precarga para que los plugins DAV puedan obtener de una sola vez
los datos de los hijos de la colección. El objetivo es evitar N+1 consultas a la base de datos
precargando lo que necesitan los manejadores de propiedades antes de que empiece el tratamiento
de propiedades por nodo. En la práctica, esto significa que el plugin puede llenar una caché por adelantado
y luego leer de ella en los manejadores `propFind` habituales, para obtener una respuesta más rápida y
eficiente.

### Cuándo se emite el evento

El evento se emite durante las peticiones PROPFIND, antes del evento `propFind`,
para los nodos que implementan `Sabre\DAV\ICollection` con `Depth > 0`.

El evento puede emitirse varias veces para una misma ruta de petición; los plugins deben
comprobar sus cachés para evitar trabajo duplicado.

### Suscribirse al evento en un plugin

Registrar un listener en la implementación propia del método `ServerPlugin::initialize()` de Sabre:

```php
use Sabre\DAV\ICollection;
use Sabre\DAV\PropFind;
use Sabre\DAV\ServerPlugin;

class MyDavPlugin extends ServerPlugin {

    public function initialize(\Sabre\DAV\Server $server): void {
        // Called before per-node property handlers
        $server->on('preloadCollection', $this->preloadCollection(...));

        // Your usual property handlers
        $server->on('propFind', $this->handleGetProperties(...));
    }

    private function preloadCollection(PropFind $propFind, ICollection $collection): void {
        // Only preload when your properties were actually requested
        $requested = [
            '{http://appdomain.example/ns}your-prop',
            '{http://appdomain.example/ns}another-prop',
        ];
        $anyRequested = array_reduce(
            $requested,
            fn($result, $property) => $result || $propFind->getStatus($property) !== null,
            false
        );
        if (!$anyRequested) {
            return;
        }

        // Fetch data for the collection and its children in bulk
        // and cache results for use in your propFind handler
        $this->cache = $this->bulkLoadDataForCollection($collection); // implement your own caching
    }

    private function handleGetProperties(PropFind $propFind, \Sabre\DAV\INode $node): void {
        // Read and return values from $this->cache to avoid per-node queries

        // Handle per-node property loading here to support Depth = 0
        // and cases where the 'preloadCollection' event is not emitted.
    }

}
```

### Ejemplos integrados

- Etiquetas: `OCA\DAV\Connector\Sabre\TagsPlugin` precarga las etiquetas y la información
  de favoritos de una carpeta y de sus hijos.
- Compartidos: `OCA\DAV\Connector\Sabre\SharesPlugin` precarga los tipos de compartición y
  los destinatarios de los elementos de una carpeta.
- Comentarios: `OCA\DAV\Connector\Sabre\CommentPropertiesPlugin` precarga el número de
  comentarios no leídos de los elementos de una carpeta.

### Buenas prácticas

- Comprobar las propiedades solicitadas: usar `$propFind->getStatus('{ns}property')` para
  confirmar que las propiedades se solicitaron realmente antes de hacer consultas.
- Guardar los resultados en caché: el evento puede dispararse varias veces; guardar en caché por ID de archivo o por ruta
  para evitar trabajo redundante durante una misma petición.
- Acotar la precarga: obtener solo los datos de la colección actual y (como mucho)
  de sus hijos directos; evitar obtener datos de todo el árbol.
````
