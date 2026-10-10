---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo una app aporta resultados a la búsqueda unificada: proveedores simples, avanzados y externos, su registro, la paginación y la privacidad."
---
(nc-dev-unified-search)=
# Búsqueda

## Resumen

Esta página explica la búsqueda unificada: cómo se obtienen los proveedores y sus resultados, cómo implementar y registrar un proveedor de búsqueda simple, avanzado o externo, cómo paginar los resultados y qué exige la privacidad. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/search.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud 20 ofrece una nueva **búsqueda unificada**. La idea general es tener una vista combinada para la búsqueda, pero mostrar en ella resultados de cualquier fuente de datos. Por eso, esta lógica se basa en una arquitectura de complementos en la que las apps registran sus proveedores de búsqueda.

### Visión general del concepto

La búsqueda unificada combina un número variable de proveedores de búsqueda en un resultado de búsqueda unificado para el usuario. Para mejorar la experiencia de usuario de la búsqueda, los resultados deben mostrarse rápidamente. Por eso se usa el paralelismo para dividir el proceso en varias solicitudes que pueden procesarse de forma concurrente, a fin de dar al cliente (p. ej., JavaScript en el navegador) la posibilidad de mostrar resultados de búsqueda parciales a medida que llegan.

Por eso, el proceso de búsqueda consta de dos pasos.

1. Obtener el conjunto actual de ID de proveedores de búsqueda
2. Obtener los resultados de búsqueda de cada proveedor

Estos dos pasos tienen que ejecutarse de forma consecutiva, pero las solicitudes individuales del segundo paso pueden despacharse y procesarse de forma concurrente.

#### Obtener los ID de los proveedores

`GET https://cloud.domain/ocs/v2.php/search/providers`

Esto devolverá una estructura como

```json
{
    "ocs": {
        "meta": {
            "…": "…"
        },
        "data": [
            {
                "id": "talk-message",
                "appId": "spreed",
                "name": "Messages",
                "icon": "/apps/spreed/img/app.svg",
                "order": -2,
                "triggers": ["talk-message"],
                "filters": {
                    "term": "string",
                    "since": "datetime",
                    "until": "datetime",
                    "person": "person"
                },
                "inAppSearch": false
            },
            {
                "id": "files",
                "appId": "files",
                "name": "Fichiers",
                "icon": "/apps/files/img/app.svg",
                "order": 5,
                "triggers": ["files"],
                "filters": {
                    "term": "string",
                    "since": "datetime",
                    "until": "datetime",
                    "person": "person",
                    "min-size": "int",
                    "max-size": "int",
                    "mime": "string",
                    "type": "string"
                },
                "inAppSearch": false
            }
        ]
    }
}
```

`filters` enumera los filtros que admite el proveedor, con su tipo esperado

#### Obtener los resultados de búsqueda individuales

`GET https://cloud.domain/ocs/v2.php/search/providers/files/search?term=cat`

```json
{
    "ocs": {
        "meta": {
            "…": "…"
        },
        "data": {
            "name": "Files",
            "isPaginated": false,
            "entries": [
                {
                    "thumbnailUrl": "/core/preview?x=32&y=32&fileId=9261",
                    "title": "my cute cats.jpg",
                    "subline": "/my cute cats.jpg",
                    "resourceUrl": "/apps/files/?dir=/&scrollto=my%20cute%20cats.jpg"
                },
                {
                    "thumbnailUrl": "/core/preview?x=32&y=32&fileId=1553",
                    "title": "cat (2).png",
                    "subline": "/cat (2).png",
                    "resourceUrl": "/apps/files/?dir=/&scrollto=cat%20%282%29.png"
                }
            ],
            "cursor": null
        }
    }
}
```

### Proveedores de búsqueda simples

Un **proveedor de búsqueda** es una clase que implementa la interfaz `\OCP\Search\IProvider`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Search;

use OCA\MyApp\AppInfo\Application;
use OCP\IUser;
use OCP\Search\IProvider;

class Provider implements IProvider {

    public function getId(): string {
        return 'mysearchprovider';
    }

    public function getName(): string {
        return $this->l->t('My custom group');
    }

    public function getOrder(string $route, array $routeParameters): int {
        if (str_contains($route, Application::APP_ID)) {
            // Active app, prefer my results
            return -1;
        }

        return 55;
    }

    public function search(IUser $user, ISearchQuery $query): SearchResult {
        return SearchResult::complete(
            'My custom group', // TODO: this should be translated
            [
                ...
            ]
        );
    }
}
```

El método `getId` devuelve un identificador de tipo cadena del proveedor registrado. Tiene que ser único globalmente, por lo que no debe entrar en conflicto con ninguna otra app. Por eso se aconseja usar simplemente el ID de la app (p. ej., `mail`) como ID, o un ID que lleve como prefijo el ID de la app, como `mail_recipients`. `getName` es un nombre traducido para los resultados de búsqueda.

El método `getOrder` devuelve el orden del proveedor para la página actual. Con el parámetro de ruta se puede comprobar si la ruta es de la app y, en ese caso, usar un valor negativo. En caso contrario, la app debería usar un valor en torno a 50.

El método `search` transforma una solicitud de búsqueda en un resultado de búsqueda.

La clase normalmente se guardaría en un archivo en `lib/Search` de la app, pero se puede colocar en otro lugar siempre que el {nc-ref}`contenedor de inyección de dependencias <dependency-injection>` de Nextcloud pueda cargarla.

### Proveedor de búsqueda avanzado

Desde Nextcloud 28.0 es posible usar proveedores de búsqueda avanzados implementando `\OCP\Search\IFilteringProvider`.
Esta interfaz permite admitir otros tipos de filtrado.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Search;

use OCA\MyApp\AppInfo\Application;
use OCP\IUser;
use OCP\Search\FilterDefinition;
use OCP\Search\IFilteringProvider;

class Provider implements IFilteringProvider {

    // TODO Implement functions from simple search provider

public function getSupportedFilters(): array {
        return [
            'term',
            'since',
            'until',
            'person',
            'custom_int',
            'custom_user',
            'custom_bool',
        ];
    }

public function getAlternateIds(): array {
        return [];
    }

public function getCustomFilters(): array {
        return [
            new FilterDefinition('custom_int', FilterDefinition::TYPE_INT),
            new FilterDefinition('custom_user', FilterDefinition::TYPE_USER),
            new FilterDefinition('custom_bool', FilterDefinition::TYPE_BOOL),
        ];
    }

    public function search(IUser $user, ISearchQuery $query): SearchResult {
        // Retrieve filters
        /** @var $since ?DateTimeImmutable */
        $since = $query->getFilter('since')?->get();
        /** @var $user ?IUser */
        $user = $query->getFilter('custom_user')?->get();

        // TODO Do actual search

        return new SearchResult(/* … */);
    }
}
```

`getSupportedFilters` enumera los filtros que admite el proveedor. Si los filtros que envía el cliente no son compatibles, el proveedor no recibirá la solicitud.

`getCustomFilters` permite declarar filtros específicos. En el estado actual, los filtros específicos solo estarán disponibles en la API.

### Proveedor de búsqueda externo

Desde Nextcloud 32, para mejorar la privacidad, se puede extender el proveedor con la interfaz `\OCP\Search\IExternalProvider` e implementar el método `isExternalProvider()` para indicar que la búsqueda se realiza sobre recursos externos (de terceros).
En la interfaz de la búsqueda unificada, la búsqueda en estos proveedores está desactivada de forma predeterminada (mediante un interruptor).

### Registro del proveedor

La clase del proveedor se registra mediante el {nc-ref}`mecanismo de arranque <bootstrapping>` de la clase `Application`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCA\MyApp\Search\Provider;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;

class Application extends App implements IBootstrap {

    public function register(IRegistrationContext $context): void {
        $context->registerSearchProvider(Provider::class);
    }

    public function boot(IBootContext $context): void {}

}
```

### Gestión de las solicitudes de búsqueda

Las solicitudes de búsqueda se procesan en el método `search`. El objeto `$user` es el usuario para el que debe generarse el resultado. `$query` aporta información de contexto, como el **término de búsqueda**, el **orden de clasificación**, la **información de la ruta**, el **límite de tamaño** de una solicitud y el **cursor** para la solicitud siguiente de resultados paginados.

El resultado se encapsula en la clase `SearchResult`, que ofrece dos métodos de fábrica estáticos, `complete` y `paginated`. Ambos métodos reciben un array de objetos `SearchResultEntry`.

A continuación se muestra un proveedor ficticio que devuelve un conjunto estático de resultados.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Search;

use OCA\MyApp\AppInfo\Application;
use OCP\IL10N;
use OCP\IURLGenerator;
use OCP\IUser;
use OCP\Search\IProvider;
use OCP\Search\SearchResult;
use OCP\Search\SearchResultEntry;
use OCP\Search\ISearchQuery;

class Provider implements IProvider {

    /** @var IL10N */
    private $l10n;

    /** @var IURLGenerator */
    private $urlGenerator;

    public function __construct(IL10N $l10n,
                                IURLGenerator $urlGenerator) {
        $this->l10n = $l10n;
        $this->urlGenerator = $urlGenerator;
    }

    public function getId(): string {
        return 'mysearchprovider';
    }

    public function getName(): string {
        return $this->l->t('My app');
    }

    public function getOrder(string $route, array $routeParameters): int {
        if (strpos($route, Application::APP_ID . '.') === 0) {
            // Active app, prefer my results
            return -1;
        }

        return 25;
    }

    public function search(IUser $user, ISearchQuery $query): SearchResult {
        return SearchResult::complete(
            $this->l10n->t('My app'),
            [
                new SearchResultEntry(
                    $this->urlGenerator->linkToRoute(
                        'myapp.Preview.getPreviewByFileId',
                        [
                            'id' => 1
                        ]
                    ),
                    'Search result 1',
                    'This goes into the subline',
                    $this->urlGenerator->linkToRoute(
                        'myapp.view.index',
                        [
                            'id' => 1,
                        ]
                    )
                )
            ]
        );
    }
}
```

Cada entrada de resultado tiene

- Una miniatura o un icono, que es una URL (relativa)
- Un título, p. ej., el nombre de un archivo
- Una línea secundaria, p. ej., la ruta de un archivo
- Una URL del recurso que permite navegar a los detalles de este resultado
- Una clase CSS de icono opcional, que se aplica cuando no se estableció la URL de la miniatura
- Un booleano rounded, que indica si la miniatura debe redondearse, p. ej., cuando es un avatar

Las apps **pueden** devolver el resultado completo en `search`, pero en la mayoría de los casos el tamaño del conjunto de resultados puede volverse demasiado grande para caber en una sola solicitud HTTP y es complicado de mostrar al usuario, por lo que el conjunto debería dividirse en fragmentos: debería estar **paginado**.

#### Paginación

Los resultados paginados funcionan casi igual que los resultados completos. Las diferencias son que para construir el conjunto se usa el método de fábrica `SearchResult::paginated` y que para ello se necesita un **cursor**.

Hay dos formas de usar el **cursor**: la paginación basada en desplazamiento y la paginación basada en cursor.

Para la **paginación basada en desplazamiento**, se devuelven `$query->getLimit()` resultados y se especifica ese número como **cursor**. En cualquier llamada posterior en la que `$query->getCursor()` no devuelva `null`, se toma el valor como **desplazamiento** para la página siguiente. El siguiente ejemplo pretende demostrar este caso de uso.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Search;

use OCA\MyApp\AppInfo\Application;
use OCP\IL10N;
use OCP\IURLGenerator;
use OCP\IUser;
use OCP\Search\IProvider;
use OCP\Search\SearchResult;
use OCP\Search\ISearchQuery;

class Provider implements IProvider {

    /** @var IL10N */
    private $l10n;

    /** @var IURLGenerator */
    private $urlGenerator;

    public function __construct(IL10N $l10n,
                                IURLGenerator $urlGenerator) {
        $this->l10n = $l10n;
        $this->urlGenerator = $urlGenerator;
    }

    public function getId(): string {
        return 'mysearchprovider';
    }

    public function getName(): string {
        return $this->l->t('My app');
    }

    public function getOrder(string $route, array $routeParameters): int {
        if (strpos($route, Application::APP_ID . '.') === 0) {
            // Active app, prefer my results
            return -1;
        }

        return 25;
    }

    public function search(IUser $user, ISearchQuery $query): SearchResult {
        $offset = ($query->getCursor() ?? 0);
        $limit = $query->getLimit();

        $data = []; // Fill this with $limit entries, where the first entry is row $offset

        return SearchResult::paginated(
            $this->l10n->t('My app'),
            $data,
            $offset + $limit
        );
    }
}
```

Así, la primera llamada recibirá un cursor `null` y un límite de, por ejemplo, 20. Así que se obtienen las primeras 20 filas. La siguiente llamada tendrá un cursor de 20, así que se obtienen las filas de la 20.ª a la 39.ª.

La desventaja de la paginación basada en desplazamiento es que, cuando los datos subyacentes cambian (se insertan entradas en la base de datos o se eliminan de ella, cambian archivos), el desplazamiento puede desincronizarse de una solicitud a la siguiente. Por eso, si es posible, es preferible una verdadera paginación basada en cursor.

Para una **paginación basada en cursor** se usa una propiedad específica de la app para conocer una referencia al último elemento de la solicitud de búsqueda anterior. La premisa de este algoritmo es que el conjunto de resultados está ordenado por un atributo y que este atributo es un `int` o un `string`. El valor del atributo del último elemento de la página de resultados determina el cursor para la siguiente solicitud de búsqueda. De nuevo, un pequeño ejemplo pretende demostrar cómo funciona.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\Search;

use OCA\MyApp\AppInfo\Application;
use OCP\IL10N;
use OCP\IURLGenerator;
use OCP\IUser;
use OCP\Search\IProvider;
use OCP\Search\SearchResult;
use OCP\Search\ISearchQuery;

class Provider implements IProvider {

    /** @var IL10N */
    private $l10n;

    /** @var IURLGenerator */
    private $urlGenerator;

    public function __construct(IL10N $l10n,
                                IURLGenerator $urlGenerator) {
        $this->l10n = $l10n;
        $this->urlGenerator = $urlGenerator;
    }

    public function getId(): string {
        return 'mysearchprovider';
    }

    public function getName(): string {
        return $this->l->t('My app');
    }

    public function getOrder(string $route, array $routeParameters): int {
        if (strpos($route, Application::APP_ID . '.') === 0) {
            // Active app, prefer my results
            return -1;
        }

        return 25;
    }

    public function search(IUser $user, ISearchQuery $query): SearchResult {
        $cursor = $query->getCursor();
        $limit = $query->getLimit();

        if ($cursor === null) {
            $data = []; // Fill this with $limit entries sorted ascending by created_at
        } else {
            $data = []; // Fill this with $limit entries sorted ascending by created_at that have a created_at > $cursor
        }
        $last = end($data);

        return SearchResult::paginated(
            $this->l10n->t('My app'),
            $data,
            $last->getCreatedAt()
        );
    }
}
```

#### Atributos opcionales

La búsqueda unificada está disponible mediante OCS, lo que significa que las aplicaciones cliente, como las apps móviles, pueden usarla para acceder al mecanismo de búsqueda del servidor. Las propiedades predeterminadas de una entrada de resultado de búsqueda pueden ser difíciles de analizar e interpretar en esos clientes, por lo que es posible agregar atributos opcionales de tipo cadena a cada entrada.

```php
<?php

$entry = new SearchResultEntry(/* same arguments as above */);
$entry->addAttribute("type", "deckCard");
$entry->addAttribute("cardId", "1234");
$entry->addAttribute("boardId", "567");
```

:::{note}
Este método se agregó en Nextcloud 21. Si la app también está destinada a Nextcloud 20, no se debe usar, o se debe agregar una comprobación de versión para invocar el método solo de forma condicional.
:::

### Declarar una búsqueda dentro de la app

Si la aplicación también tiene búsqueda dentro de la app (como `mail` o `talk`), el proveedor también puede implementar la interfaz `\OCP\Search\IInAppSearch`.

Esto agregará un enlace a ella después de los resultados de búsqueda.

### Privacidad

Todos los proveedores de búsqueda tienen que valorar la privacidad y evitar de forma predeterminada la filtración de datos sensibles. Por eso, de forma predeterminada, los términos de búsqueda no deben enviarse a terceros. Si un proveedor de búsqueda usa servicios de terceros, hay que obtener el consentimiento del usuario, p. ej., mediante un interruptor de aceptación explícita en los ajustes personales del usuario.
````
