---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo registrar widgets del Dashboard, darles interfaz de usuario y exponerlos por la API del Dashboard: botones, icono, opciones, elementos y recarga."
---
# Dashboard

## Resumen

Esta página explica cómo una app registra sus propios widgets en el Dashboard, cómo les da una interfaz de usuario en JavaScript y cómo los expone por la API del Dashboard, con las interfaces de botones, icono, opciones, elementos y recarga periódica y ejemplos de consulta a la API. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/dashboard.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La app Dashboard pretende ofrecer al usuario una vista general de su
Nextcloud y muestra la información que es importante en ese momento.

Quienes desarrollan apps pueden integrarse en la app Dashboard y proporcionar sus propios widgets.

### Registrar un widget del Dashboard

Un widget del Dashboard se representa mediante una clase que implementa la interfaz *OCP\\Dashboard\\IWidget*.
Esta clase se instancia cada vez que se carga el Dashboard.
Cualquier código de arranque que necesite el widget puede implementarse dentro
del método *load*, que se llamará cuando se cargue el Dashboard.

```php
<?php

namespace OCA\MyApp\Dashboard;

use OCP\Dashboard\IWidget;
use OCP\IInitialStateService;
use OCP\IL10N;
use OCP\IURLGenerator;
use OCP\IUserSession;

class MyAppWidget implements IWidget {
    private IInitialStateService $initialStateService;
    private IL10N $l10n;
    private IURLGenerator $urlGenerator;

    public function __construct(
        IInitialStateService $initialStateService,
        IL10N $l10n,
        IURLGenerator $urlGenerator
    ) {
        $this->initialStateService = $initialStateService;
        $this->l10n = $l10n;
        $this->urlGenerator = $urlGenerator;
    }

    /**
     * @return string Unique id that identifies the widget, e.g. the app id
     */
    public function getId(): string {
        return 'myappwidgetid';
    }

    /**
     * @return string User facing title of the widget
     */
    public function getTitle(): string {
        return $this->l10n->t('My app');
    }

    /**
     * @return int Initial order for widget sorting
     *   in the range of 10-100, 0-9 are reserved for shipped apps
     */
    public function getOrder(): int {
        return 0;
    }

    /**
     * @return string css class that displays an icon next to the widget title
     */
    public function getIconClass(): string {
        return 'icon-class';
    }

    /**
     * @return string|null The absolute url to the apps own view
     */
    public function getUrl(): ?string {
        return $this->urlGenerator->linkToRouteAbsolute('myapp.view.index');
    }

    /**
     * Execute widget bootstrap code like loading scripts and providing initial state
     */
    public function load(): void {
        $this->initialStateService->provideInitialState('myapp', 'myData', []);
        \OCP\Util::addScript('myapp', 'dashboard');
    }
}
```

La clase *MyAppWidget* debe registrarse durante el {nc-ref}`arranque de la app <bootstrapping>`.

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
        $context->registerDashboardWidget(MyAppWidget::class);
    }

    public function boot(IBootContext $context): void {
    }
}
```

#### La interfaz IConditionalWidget

La interfaz IConditionalWidget agrega el método **isEnabled** para ofrecer a un widget la opción de excluirse más adelante.
Al registrar el widget, puede que la información de si un widget debe mostrarse o no a un usuario concreto
no esté disponible o sea demasiado compleja de calcular de antemano. En ese caso, IConditionalWidget permite comprobar las
condiciones solo cuando realmente hace falta.

```php
public function isEnabled(): bool {
    return false;
}
```

### Proporcionar una interfaz de usuario

La interfaz de usuario puede registrarse mediante el método público de JavaScript *OCA.Dashboard.register*.
El primer parámetro representa el ID del widget, que ya se especificó
en la implementación de *IWidget*. El parámetro de callback se llamará para
renderizar el widget en el frontend. La interfaz de usuario puede agregarse
al elemento DOM proporcionado, *el*.

El siguiente ejemplo muestra cómo podría usarse un componente de Vue.js para renderizar la
interfaz de usuario del widget; sin embargo, este enfoque funciona igual con cualquier otro framework
y con JavaScript puro:

```javascript
import Dashboard from './components/Dashboard.vue'

document.addEventListener('DOMContentLoaded', () => {
    OCA.Dashboard.register('myappwidgetid', (el) => {
        const View = Vue.extend(Dashboard)
        const vm = new View({
            propsData: {},
            store,
        }).$mount(el)
    })
})
```

### API del Dashboard

#### Renderizar widgets del Dashboard mediante la API

:::{versionadded} 27.1
:::

Los widgets del Dashboard pueden renderizarse en el navegador mediante la API del Dashboard. Esto permite renderizar
widgets sin código JavaScript ni de frontend. Este nuevo método favorece el rendimiento, ya que
los widgets se renderizan a partir de los datos de la API mediante un componente genérico de vue.js que proporciona la app
Dashboard.

Para renderizar un widget mediante la nueva API, hay que implementar la interfaz
{nc-ref}`OCP\Dashboard\IAPIWidgetV2 <IAPIWidgetV2>`. Opcionalmente, se puede implementar la interfaz
{nc-ref}`OCP\Dashboard\IReloadableWidget <IReloadableWidget>` para que el widget se recargue
periódicamente.

#### Proporcionar widgets a los clientes

Para proporcionar más información sobre el widget a los clientes mediante la API del Dashboard, se pueden implementar
estas interfaces adicionales:

- IButtonWidget para agregar botones que el cliente renderiza en el widget
- IIconWidget para establecer la URL del icono del widget
- IOptionWidget para establecer opciones adicionales
- IAPIWidget para proporcionar propiamente el contenido del widget (la lista de elementos)

#### La interfaz IButtonWidget

La interfaz IButtonWidget agrega el método **getWidgetButtons** para proporcionar una lista de botones
que los clientes muestran en el widget.
Estos botones permiten definir acciones que pueden desencadenarse desde el widget en los clientes.

Hay 3 tipos de botones:

- WidgetButton::TYPE_NEW para que los usuarios creen nuevos elementos en la app
- WidgetButton::TYPE_MORE para que los usuarios vean más información
- WidgetButton::TYPE_SETUP si el widget requiere alguna configuración

```php
public function getWidgetButtons(string $userId): array {
    return [
        new WidgetButton(
            WidgetButton::TYPE_NEW,
            'https://somewhere.org',
            $this->l10n->t('Create new element')
        ),
        new WidgetButton(
            WidgetButton::TYPE_MORE,
            'https://my.nextcloud.org/apps/your-app/',
            $this->l10n->t('More notifications')
        ),
        new WidgetButton(
            WidgetButton::TYPE_SETUP,
            'https://my.nextcloud.org/apps/settings/user',
            $this->l10n->t('Configure')
        ),
    ];
}
```

#### La interfaz IIconWidget

La interfaz IIconWidget agrega el método **getIconUrl** para proporcionar la URL del icono del widget. En el siguiente ejemplo,
devuelve la URL del archivo img/app.svg de la app.

```php
public function getIconUrl(): string {
    return $this->urlGenerator->getAbsoluteURL(
        $this->urlGenerator->imagePath(Application::APP_ID, 'app.svg')
    );
}
```

#### La interfaz IOptionWidget

La interfaz IOptionWidget agrega el método **getWidgetOptions** para proporcionar opciones adicionales del widget. Devuelve
un objeto WidgetOptions que, por ahora, solo contiene el valor booleano **roundItemIcons**. Este indica a los clientes si
los iconos de los elementos del widget deben ser redondos o mantenerse cuadrados.

```php
public function getWidgetOptions(): WidgetOptions {
    return new WidgetOptions(true);
}
```

#### La interfaz IAPIWidget

Si se quiere que el contenido del widget sea accesible mediante la API del Dashboard para los clientes de {vendor}`Nextcloud`,
el widget debe implementar la interfaz *OCP\\Dashboard\\IAPIWidget* en lugar de *OCP\\Dashboard\\IWidget*.
Esta interfaz contiene un método adicional, *getItems*, que devuelve un array de objetos *OCP\\Dashboard\Model\\WidgetItem*.

```php
/**
* @inheritDoc
*/
public function getItems(string $userId, ?string $since = null, int $limit = 7): array {
    return $this->myService->getWidgetItems($userId, $since, $limit);
}
```

(nc-dev-widgetitem)=
*OCP\\Dashboard\Model\\WidgetItem* contiene la información del elemento. Su constructor es:

```php
public function __construct(string $title = '',
                            string $subtitle = '',
                            string $link = '',
                            string $iconUrl = '',
                            string $sinceId = '');
```

- title: el contenido de texto principal del widget
- subtitle: el contenido de texto secundario
- link: un enlace al recurso de destino
- iconUrl: URL de un icono cuadrado (svg, o jpg/png de al menos 44x44px)
- sinceId: ID o marca de tiempo del elemento. El cliente enviará entonces el último sinceId conocido en la siguiente solicitud a la API del Dashboard.

:::{versionadded} 27.1
:::

- overlayIconUrl: pequeño icono superpuesto que se muestra en la esquina inferior derecha de *iconUrl*. Lo usa
  el widget de actividad para mostrar el icono del tipo de actividad.

(nc-dev-iapiwidgetv2)=
#### La interfaz IAPIWidgetV2

Si se quiere renderizar un widget en el navegador mediante esta API, hay que implementar la interfaz
*OCP\\Dashboard\\IAPIWidgetV2*. El registro del widget no cambia respecto del
método anterior. El tipo de un widget se detecta automáticamente durante el registro. Al
migrar widgets antiguos basados en JavaScript, el método **load** debe dejarse vacío.

Esta interfaz agrega un único método, **getItemsV2**, que devuelve
*OCP\\Dashboard\\Model\\WidgetItems*.

```php
/**
 * @inheritDoc
 */
public function getItemsV2(string $userId, ?string $since = null, int $limit = 7): WidgetItems {
    return $this->myService->getWidgetItemsV2($userId, $since, $limit);
}
```

*OCP\\Dashboard\Model\\WidgetItems* contiene todos los elementos e información meta adicional para
renderizar el widget. Su constructor es:

```php
public function __construct(
    private array $items = [],
    private string $emptyContentMessage = '',
    private string $halfEmptyContentMessage = '',
)
```

- items: un array de {nc-ref}`OCP\Dashboard\Model\WidgetItem <WidgetItem>`.
- emptyContentMessage: el mensaje que se muestra si no hay elementos disponibles.
- halfEmptyContentMessage: un mensaje opcional que se muestra encima de la lista de elementos. Es útil si no
  hay elementos importantes pero aun así se quieren mostrar algunos elementos al usuario. Ver el
  siguiente ejemplo de la app Talk.

La pantalla muestra el widget de Talk en el Dashboard en el estado de contenido medio vacío, con un mensaje encima de una lista breve de elementos.

Este es un ejemplo completo de un widget que implementa la interfaz *OCP\\Dashboard\\IAPIWidgetV2*:

```php
<?php

class MyWidget implements IButtonWidget, IIconWidget, IReloadableWidget {
    public function __construct(
        private IL10N $l10n,
        private IURLGenerator $urlGenerator,
    ) {
    }

    /**
     * @inheritDoc
     */
    public function getId(): string {
        return 'blazinglyfast';
    }

    /**
     * @inheritDoc
     */
    public function getTitle(): string {
        return $this->l10n->t('My blazingly fast widget');
    }

    /**
     * @inheritDoc
     */
    public function getOrder(): int {
        return 0;
    }

    /**
     * @inheritDoc
     */
    public function getIconClass(): string {
        return 'icon-class';
    }

    /**
     * @inheritDoc
     */
    public function getIconUrl(): string {
        return $this->urlGenerator->getAbsoluteURL(
            $this->urlGenerator->imagePath('blazinglyfast', 'icon.svg')
        );
    }

    /**
     * @inheritDoc
     */
    public function getUrl(): ?string {
        return $this->urlGenerator->linkToRouteAbsolute('blazinglyfast.view.index');
    }

    /**
     * @inheritDoc
     */
    public function load(): void {
        // No need to provide initial state or inject javascript code anymore
    }

    /**
     * @inheritDoc
     */
    public function getItemsV2(string $userId, ?string $since = null, int $limit = 7): WidgetItems {
        // TODO
        $items = [/* fancy items */];
        return new WidgetItems(
            $items,
            empty($items) ? $this->l10n->t('No items') : '',
        );
    }

    /**
     * @inheritDoc
     */
    public function getWidgetButtons(string $userId): array {
        return [
            new WidgetButton(
                WidgetButton::TYPE_MORE,
                $this->urlGenerator->linkToRouteAbsolute('blazinglyfast.view.index'),
                $this->l10n->t('More items'),
            ),
        ];
    }

    /**
     * @inheritDoc
     */
    public function getReloadInterval(): int {
        return 60;
    }
}
```

(nc-dev-ireloadablewidget)=
#### La interfaz IReloadableWidget

La interfaz IReloadableWidget agrega el método **getReloadInterval** para proporcionar un intervalo de recarga
periódica en segundos. Transcurrido este intervalo, se solicitan nuevos elementos a la API OCS para actualizar
el widget. Internamente, se llama al método **getItemsV2** para obtener los nuevos elementos.

```php
public function getReloadInterval(): int {
    // Reload data every minute
    return 60;
}
```

:::{note}
Esta interfaz requiere que el widget implemente la interfaz *OCP\\Dashboard\\IAPIWidgetV2* y no funciona con widgets antiguos.
:::

#### Usar la API

La lista de widgets activados puede solicitarse así:

```bash
curl -u user:passwd https://my.nextcloud.org/ocs/v2.php/apps/dashboard/api/v1/widgets \
    -H "Accept: application/json" \
    -X GET
```

Ejemplo de respuesta:

```json
{
  "ocs": {
    "meta": {
      "status": "ok",
      "statuscode": 200,
      "message": "OK"
    },
    "data": {
      "spreed": {
        "id": "spreed",
        "title": "Talk mentions",
        "order": 10,
        "icon_class": "dashboard-talk-icon",
        "icon_url": "https://my.nextcloud.org/apps/spreed/img/app-dark.svg",
        "widget_url": "https://my.nextcloud.org/index.php/apps/spreed/",
        "item_icons_round": true,
        "buttons": [
          {
            "type": "more",
            "text": "More unread mentions",
            "link": "https://my.nextcloud.org/index.php/apps/spreed/"
          }
        ]
      },
      "github_notifications": {
        "id": "github_notifications",
        "title": "GitHub notifications",
        "order": 10,
        "icon_class": "icon-github",
        "icon_url": "https://my.nextcloud.org/apps/integration_github/img/app-dark.svg",
        "widget_url": "https://my.nextcloud.org/index.php/settings/user/connected-accounts",
        "item_icons_round": true,
        "buttons": [
          {
            "type": "more",
            "text": "More notifications",
            "link": "https://github.com/notifications"
          }
        ]
      },
    }
  }
}
```

La lista de elementos de cada widget activado puede solicitarse así:

```bash
curl -u user:passwd http://my.nc/ocs/v2.php/apps/dashboard/api/v1/widget-items \
    -H Content-Type:application/json \
    -X GET \
    -d '{"sinceIds":{"myappwidgetid":"2021-03-22T15:01:10Z","my_other_appwidgetid":"333"}}'
```

Si el cliente obtiene periódicamente el contenido de los elementos de los widgets con esta API,
incluir el último *sinceId* de cada widget para no recibir los elementos que ya se tienen.

Ejemplo de respuesta:

```json
{
  "ocs": {
    "meta": {
      "status": "ok",
      "statuscode": 200,
      "message": "OK"
    },
    "data": {
      "github_notifications": [
        {
          "subtitle": "nextcloud-docker-dev#87",
          "title": "Improve getting started",
          "link": "https://github.com/juliushaertl/nextcloud-docker-dev/pull/87",
          "iconUrl": "https://my.nextcloud.org/index.php/apps/integration_github/avatar/juliushaertl",
          "sinceId": "2022-10-13T12:34:19Z"
        },
        {
          "subtitle": "integration_github",
          "title": "v1.0.11",
          "link": "https://github.com/nextcloud/integration_github/releases",
          "iconUrl": "https://my.nextcloud.org/index.php/apps/integration_github/avatar/nextcloud",
          "sinceId": "2022-10-13T12:32:04Z"
        },
        {
          "subtitle": "text#3209",
          "title": "Rich workspaces: If there is no Readme.md, don’t show editor placeholder but move into \"+\" menu",
          "link": "https://github.com/nextcloud/text/issues/3209",
          "iconUrl": "https://my.nextcloud.org/index.php/apps/integration_github/avatar/nextcloud",
          "sinceId": "2022-10-13T12:14:39Z"
        }
      ],
      "spreed": [
        {
          "subtitle": "- Send chat messages without notifying the recipients in case it is not urgent",
          "title": "Talk updates ✅",
          "link": "https://my.nextcloud.org/index.php/call/hw39yxkp",
          "iconUrl": "https://my.nextcloud.org/core/img/actions/group.svg",
          "sinceId": ""
        },
        {
          "subtitle": "@roberto What's up?",
          "title": "Jane",
          "link": "https://my.nextcloud.org/index.php/call/z87agy2o",
          "iconUrl": "https://my.nextcloud.org/index.php/avatar/toto/64",
          "sinceId": ""
        }
      ]
    }
  }
}
```
````
