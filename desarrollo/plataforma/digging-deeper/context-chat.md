---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo implementar un proveedor de contenido para Context Chat: la interfaz IContentProvider, el servicio IContentManager, su registro y el envío de contenido."
---
(nc-dev-context_chat)=
# Context Chat

## Resumen

Esta página explica cómo una app envía sus datos a Context Chat mediante un proveedor de contenido: implementar `IContentProvider`, usar el servicio `IContentManager`, registrar el proveedor con el evento `ContentProviderRegisterEvent` y enviar objetos `ContentItem`. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/context_chat.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 32.0.0
:::

Nextcloud ofrece una API de **Context Chat** que permite a apps como Archivos enviar datos
al [Context Chat del Asistente de Nextcloud](https://docs.nextcloud.com/server/latest/admin_manual/ai/app_context_chat.html),
lo que permite al [Asistente de Nextcloud](https://docs.nextcloud.com/server/latest/admin_manual/ai/app_assistant.html)
responder preguntas y ofrecer análisis y resultados de búsqueda basados en los datos enviados y en consultas en lenguaje natural.

### Implementar un proveedor de contenido para Context Chat

#### La interfaz IContentProvider

Un proveedor de contenido para Context Chat debe implementar la interfaz `\OCP\ContextChat\IContentProvider`:

```php
/**
 * This interface defines methods to implement a content provider
 * @since 32.0.0
 */
interface IContentProvider {
    /**
     * The ID of the provider
     *
     * @return string
     * @since 32.0.0
     */
    public function getId(): string;

    /**
     * The ID of the app making the provider available
     *
     * @return string
     * @since 32.0.0
     */
    public function getAppId(): string;

    /**
     * The absolute URL to the content item
     *
     * @param string $id
     * @return string
     * @since 32.0.0
     */
    public function getItemUrl(string $id): string;

    /**
     * Starts the initial import of content items into context chat
     *
     * @return void
     * @since 32.0.0
     */
    public function triggerInitialImport(): void;
}
```

Se llama al método `triggerInitialImport` cuando Context Chat se configura por primera vez,
y permite que la app importe en Context Chat todo el contenido existente de una sola vez.
Los demás elementos que se creen después deberán agregarse a demanda.

#### Usar el servicio IContentManager

Para agregar contenido y registrar la implementación del proveedor hay que usar el servicio `\OCP\ContextChat\IContentManager`.

La clase `IContentManager` tiene los siguientes métodos:

- `isContextChatAvailable()`: devuelve `true` si la app Context Chat está activada; `false` en caso contrario.
- `registerContentProvider(string $providerClass)`: registra un nuevo proveedor de contenido.
- `submitContent(string $appId, array $items)`: los proveedores pueden usarlo para enviar contenido para su indexación en Context Chat.
- `updateAccess(string $appId, string $providerId, string $itemId, string $op, array $userIds)`: actualiza los derechos de acceso de un elemento de contenido. Usar las constantes de `\OCP\ContextChat\Type\UpdateAccessOp` para el valor de `$op`.
- `updateAccessProvider(string $appId, string $providerId, string $op, array $userIds)`: actualiza los derechos de acceso de todos los elementos de contenido de un proveedor. Usar las constantes de `\OCP\ContextChat\Type\UpdateAccessOp` para el valor de `$op`.
- `updateAccessDeclarative(string $appId, string $providerId, string $itemId, array $userIds)`: actualiza los derechos de acceso de un elemento de contenido. Este método es declarativo y reemplaza los derechos de acceso actuales por los proporcionados.
- `deleteProvider(string $appId, string $providerId)`: elimina todos los elementos de contenido de un proveedor de la base de conocimiento de Context Chat.
- `deleteContent(string $appId, string $providerId, array $itemIds)`: elimina elementos de contenido específicos de la base de conocimiento de Context Chat.

#### Implementar el evento ContentProviderRegisterEvent

Para registrar el proveedor de contenido,
la app debe escuchar el evento `OCP\ContextChat\Events\ContentProviderRegisterEvent`
y llamar al método `registerContentProvider` del evento por cada proveedor que se quiera registrar.

Algunas implementaciones parciales de `Application.php` y de un `ContentProvider` como referencia:

```php
use OCA\MyApp\ContextChat\ContentProvider;
use OCP\ContextChat\Events\ContentProviderRegisterEvent;
// ...
$context->registerEventListener(ContentProviderRegisterEvent::class, ContentProvider::class);
```

```php
class ContentProvider implements IContentProvider {
// ...
public function handle(Event $event): void {
    if (!$event instanceof ContentProviderRegisterEvent) {
        return;
    }
    $event->registerContentProvider('***appId***', '***providerId***', ContentProvider::class);
}
```

Cualquier interacción con el gestor de contenido mediante los métodos de ContentManager,
o el listado de los proveedores en el Asistente, debería registrar el proveedor automáticamente.

Se puede llamar al método `registerContentProvider` de forma explícita
si se quiere desencadenar una importación inicial de elementos de contenido.

#### Enviar datos de ContentItem

Antes de enviar, conviene comprobar primero que la app Context Chat esté activada
llamando al método `isContextChatAvailable()`.

Después, para enviar contenido, hay que envolverlo en una lista de objetos `\OCP\ContextChat\ContentItem`:

```php
new ContentItem(
        string $itemId,
        string $providerId,
        string $title,
        string $content,
        string $documentType,
        \DateTime $lastModified,
        array $users,
    )
```

:::{note}
1. Asegurarse de que los ID de los elementos sean únicos entre todos los usuarios para un proveedor dado.
2. Ni el ID de la app ni el ID del proveedor pueden contener guiones bajos dobles, espacios ni dos puntos.
3. `documentType` es un término en lenguaje natural, en inglés, para el tipo de documento, p. ej., `E-Mail` o `Bookmark`.
:::
````
