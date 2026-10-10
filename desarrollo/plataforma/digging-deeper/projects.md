---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo integrar una app en los proyectos: registrar un proveedor de recursos, su interfaz de selección y el selector de proyectos en Vue."
---
# Proyectos

## Resumen

Esta página explica cómo una app se integra en los proyectos, que vinculan elementos de distintas apps: registrar un proveedor de recursos, proporcionar la interfaz para elegir un recurso y mostrar el selector de proyectos. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/projects.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los proyectos son una forma de vincular elementos de distintas apps mediante una interfaz común.

Quienes desarrollan apps pueden integrarse en los proyectos y proporcionar sus propios tipos de entidad con los que vincular.

### Registrar un proveedor de recursos

Elementos como los archivos, las tarjetas de Deck y las salas de Talk se denominan recursos en los proyectos. Para agregar un tipo de recurso propio, hay que crear una clase que implemente la interfaz `OCP\Collaboration\Resources\IProvider`.

```php
<?php

namespace OCA\MyApp\Collaboration\Resources;


use OCP\Collaboration\Resources\IProvider;
use OCP\Collaboration\Resources\IResource;
use OCP\IURLGenerator;
use OCP\IUser;

class MyResourceProvider implements IProvider {
    public const RESOURCE_TYPE = 'my-app-item';

    /**
     * @var IURLGenerator
     */
    private $url;

    public function __construct(IURLGenerator $url) {
        $this->url = $url;
    }

    /**
     * @inheritDoc
     */
    public function getType(): string {
        return self::RESOURCE_TYPE;
    }

    /**
     * @inheritDoc
     */
    public function getResourceRichObject(IResource $resource): array {
        $item = $this->getItem($resource);
        $icon = $this->url->linkToRouteAbsolute('myapp.images.get_icon', ['id' => $item->getId()]);
        $resourceUrl = $this->url->linkToRouteAbsolute('bookmarks.page.index', ['item' => $bookmark->getId()]);

        return [
            'type' => self::RESOURCE_TYPE,
            'id' => $resource->getId(),
            'name' => $item->getTitle(),
            'link' => $resourceUrl,
            'iconUrl' => $icon,
        ];
    }

    /**
     * @inheritDoc
     */
    public function canAccessResource(IResource $resource, ?IUser $user): bool {
        if ($resource->getType() !== self::RESOURCE_TYPE || !($user instanceof IUser)) {
            return false;
        }
        $bookmark = $this->getItem($resource);
        if ($bookmark === null) {
            return false;
        }
        return $bookmark->getUserId() === $user->getUID()
    }

    private function getItem(IResource $resource) : ?Item {
        // implement me
    }
}
```

La clase `MyResourceProvider` debe registrarse durante el {nc-ref}`arranque de la app <bootstrapping>`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;
use OCA\MyApp\Dashboard\MyAppWidget;

class Application extends App implements IBootstrap {

    public const APP_ID = 'myapp';

    public function __construct(array $urlParams = []) {
        parent::__construct(self::APP_ID, $urlParams);
    }

    public function register(IRegistrationContext $context): void {
    }

    public function boot(IBootContext $context): void {
        $context->injectFn(Closure::fromCallable([$this, 'registerCollaborationResources']));
    }

    protected function registerCollaborationResources(IProviderManager $resourceManager, IEventDispatcher $eventDispatcher): void {
        $resourceManager->registerResourceProvider(ResourceProvider::class);

        $eventDispatcher->addListener(\OCP\Collaboration\Resources\LoadAdditionalScriptsEvent::class, static function () {
            Util::addScript(self::APP_ID, 'collections');
        });
    }
}
```

Como se puede ver, también se registra ya un script de frontend, que se creará a continuación.

### Proporcionar una interfaz de usuario

La interfaz de usuario puede registrarse mediante el método público de JavaScript `OCP.Collaboration.registerType`. El primer parámetro representa el tipo de recurso que ya se especificó en la implementación de `IResourceProvider`. El segundo parámetro es un objeto con tres propiedades:

- `typeString` Una cadena traducida que se mostrará en el desplegable al elegir a qué tipo de recurso vincular
- `typeIconClass` Una clase CSS del icono que debe usarse para esta entrada
- `action` Una función asíncrona que generará una interfaz para elegir un recurso y se resolverá con el id del recurso

El siguiente ejemplo muestra cómo podría usarse un componente de Vue.js para renderizar la interfaz de usuario del widget; sin embargo, este enfoque funciona igualmente con cualquier otro framework, así como con JavaScript puro:

```javascript
    import Vue from 'vue'
    import ItemPickerDialog from './components/ItemPickerDialog'

    OCP.Collaboration.registerType('myapp', {
    action: () => {
        return new Promise((resolve, reject) => {
            const container = document.createElement('div')
            container.id = 'myapp-item-select'
            const body = document.getElementById('body-user')
            body.appendChild(container)
            const ComponentVM = new Vue({
                render: h => h(ItemPickerDialog),
            })
            ComponentVM.$mount(container)
            ComponentVM.$root.$on('close', () => {
                ComponentVM.$el.remove()
                ComponentVM.$destroy()
                reject(new Error('User cancelled resource selection'))
            })
            ComponentVM.$root.$on('select', (id) => {
                resolve(id)
                ComponentVM.$el.remove()
                ComponentVM.$destroy()
            })
        })
    },
    typeString: t('myapp', 'Link to an item'),
    typeIconClass: 'icon-file',
})
```

Esto permitirá que otras apps vinculen a los elementos de la app. También se quiere vincular a elementos de otras apps. Como todas las apps compatibles con los proyectos escuchan el LoadAdditionalScriptsEvent anterior, basta con despacharlo al renderizar la plantilla de la página principal.

```php
<?php

class MyController extends Controller {
    private IEventDispatcher $eventDispatcher;

    public function __construct(string $appName, IRequest $request, IEventDispatcher $eventDispatcher) {
        parent::__construct($appName, $request);
        $this->eventDispatcher = $eventDispatcher;
    }

    public function index() {
        $this->eventDispatcher->dispatchTyped(new \OCP\Collaboration\Resources\LoadAdditionalScriptsEvent());
        return new TemplateResponse('my_app', 'main');
    }
}
```

En la app de Vue se puede renderizar entonces el selector de proyectos ya preparado que está disponible en el paquete npm `nextcloud-vue-collections`.

```
<template>
    <div>
        <CollectionList v-if="itemId"
            :id="itemId"
            :name="itemTitle"
            type="myapp" />
    </div>
</template>

<script>
import { CollectionList } from 'nextcloud-vue-collections'
export default {
    name: 'CollaborationView',
    components: {
        CollectionList,
    },
    props: {
        id: {
            type: String,
            default: '',
        },
        name: {
            type: String,
            default: '',
        }
    }
}
</script>
```
````
