---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Proveedores de referencias: mostrar vistas previas de enlaces y el selector inteligente en una app o un cliente, y ampliarlos desde una app."
---
(nc-dev-reference providers)=
# Proveedores de referencias

## Resumen

Esta página explica las vistas previas de enlaces y el selector inteligente: cómo mostrarlos en una app o en un cliente, cómo registrar un proveedor de referencias que resuelva y renderice enlaces y cómo ampliar el selector inteligente. Está dirigida a quienes desarrollan apps y clientes.

````{upstream} developer_manual/digging_deeper/reference.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los proveedores de referencias están relacionados con dos funcionalidades de Nextcloud:

- Las vistas previas de enlaces
- El selector inteligente

Las vistas previas de enlaces se introdujeron en Nextcloud 25.
Las apps pueden registrar un proveedor de referencias para agregar compatibilidad con vistas previas a algunos enlaces HTTP.
Para proporcionar vistas previas de enlaces, un proveedor de referencias necesita:

- Resolver los enlaces (obtener información sobre los enlaces)
- Renderizar los enlaces (mostrar esta información en la interfaz de usuario)

El selector inteligente se introdujo en Nextcloud 26. Es un componente de la interfaz de usuario
que permite a los usuarios buscar o generar enlaces desde varios lugares de Nextcloud, como Texto,
Talk, Colectivos, Notas, Correo...
Los proveedores de referencias pueden implementarse para que aparezcan en la lista de proveedores del selector inteligente.
El selector inteligente puede usar 2 tipos de proveedores:

- los de búsqueda (que usan proveedores existentes de la búsqueda unificada)
- los que implementan su propio componente de selector personalizado

En resumen, las apps pueden registrar proveedores de referencias para

- agregar compatibilidad con nuevos tipos de enlaces HTTP
  - resolver los enlaces, obtener información sobre los destinos de los enlaces
  - opcionalmente, proporcionar sus propios widgets de referencia para tener una renderización personalizada de la vista previa
- ampliar el selector inteligente
  - usar proveedores existentes de la búsqueda unificada
  - u, opcionalmente, registrar componentes de selector personalizados para tener una interfaz de usuario específica

Esta documentación explica cómo

- Mostrar vistas previas de enlaces en la app
- Usar el selector inteligente en la app
- Ampliar el sistema de referencias para agregar compatibilidad con vistas previas a más enlaces
- Ampliar el selector inteligente con las capacidades de la app

### Mostrar vistas previas de enlaces

Si solo se quieren mostrar vistas previas de enlaces en la app sin ampliar el sistema de referencias,
hay que asegurarse de que se despache el `OCP\Collaboration\Reference\RenderReferenceEvent`
antes de cargar la página en la que se quieren mostrar las vistas previas de enlaces.

Por ejemplo, se puede colocar esto antes de devolver la TemplateResponse en el controlador:

```php
$this->eventDispatcher->dispatchTyped(new OCP\Collaboration\Reference\RenderReferenceEvent());
```

Esto se hace en
[Texto](https://github.com/nextcloud/text/blob/8a17046aa440df841fe9182205d80ce937068c1a/lib/Listeners/LoadViewerListener.php#L52)
y en
[Talk](https://github.com/nextcloud/spreed/blob/1f1acbd95943e6184e29de8044cd9d8e775ac7c5/lib/Controller/PageController.php#L280)
por si se necesitan más ejemplos.

En el frontend hay 3 formas de mostrar las vistas previas de enlaces (también llamadas widgets de referencia):

- usar el componente de Vue NcRichText
- usar el componente de Vue NcReferenceWidget
- acceder directamente a la API de referencias y renderizar manualmente las vistas previas

#### NcRichText

Las vistas previas de enlaces se renderizarán automáticamente para los enlaces del contenido del componente de Vue `<NcRichText>`.
Este componente se encarga de resolver los enlaces por sí mismo.

```html
<NcRichText :text="message"
    :arguments="richParameters"
    :autolink="true"
    :reference-limit="0" />
```

NcRichText puede importarse así:

```javascript
import NcRichText from '@nextcloud/vue/dist/Components/NcRichText.js'
```

[Documentación del componente NcRichText](https://nextcloud-vue-components.netlify.app/#/Components/NcRichText?id=ncrichtext-1)

#### NcReferenceWidget

Se puede mostrar una vista previa de un enlace concreto usando el componente `<NcReferenceWidget>`.
Hay que pedir al servidor que resuelva el enlace para obtener un objeto de referencia que luego se puede pasar como propiedad
a NcReferenceWidget.

Para resolver un enlace:

```javascript
const myLink = 'https://github.com'
const requestOptions = {
    params: {
        reference: myLink,
    },
}
axios.get(generateOcsUrl('references/resolve', 2), requestOptions)
    .then((response) => {
        reference = response.data.ocs.data.references[myLink]
    })
```

Luego se puede usar el objeto de referencia obtenido:

```html
<NcReferenceWidget :reference="reference" />
```

#### API para resolver enlaces

Acceder directamente a la API puede ser útil si se quiere:

- resolver enlaces desde fuera de Nextcloud, por ejemplo en un cliente
- resolver y renderizar enlaces manualmente en lugar de usar los componentes de Vue

Endpoints para resolver enlaces:

- GET /ocs/v2.php/references/resolve (autenticado)
  - parámetro `reference` con el enlace que se va a resolver
- GET /ocs/v2.php/references/resolvePublic
  - parámetro `reference` con el enlace que se va a resolver
  - parámetro `sharingToken` con el token del recurso compartido público
- POST /ocs/v2.php/references/resolve
  - parámetro `references` con un array de enlaces que se van a resolver
  - parámetro `limit` con el número máximo de enlaces que se van a resolver
- POST /ocs/v2.php/references/resolve
  - parámetro `references` con un array de enlaces que se van a resolver
  - parámetro `sharingToken` con el token del recurso compartido público
  - parámetro `limit` con el número máximo de enlaces que se van a resolver

##### Ejemplos de solicitudes

```bash
curl -u USER:PASSWD -H "Accept: application/json" -H "ocs-apirequest: true" \
    "https://my.nextcloud.org/ocs/v2.php/references/resolve?reference=https://github.com"
```

devolverá una respuesta OCS con estos datos:

```json
{
  "ocs": {
    "meta": {
    "status": "ok",
    "statuscode": 200,
    "message": "OK"
  },
  "data": {
    "references": {
      "https://github.com": {
        "richObjectType": "open-graph",
        "richObject": {
          "id": "https://github.com",
          "name": "GitHub: Let’s build from here",
          "description": "GitHub is where over 100 million developers shape the future of software, together. Contribute to the open source community, manage your Git repositories, review code like a pro, track bugs and fea...",
          "thumb": "https://my.nextcloud.org/core/references/preview/3097fca9b1ec8942c4305e550ef1b50a",
          "link": "https://github.com"
        },
        "openGraphObject": {
          "id": "https://github.com",
          "name": "GitHub: Let’s build from here",
          "description": "GitHub is where over 100 million developers shape the future of software, together. Contribute to the open source community, manage your Git repositories, review code like a pro, track bugs and fea...",
          "thumb": "https://my.nextcloud.org/core/references/preview/3097fca9b1ec8942c4305e550ef1b50a",
          "link": "https://github.com"
        },
        "accessible": true
      }
    }
  }
}
```

El enlace puede estar admitido por un proveedor de referencias que además proporcione más información en un objeto enriquecido.
El openGraphObject genérico se sigue devolviendo. Contiene un título, una descripción y una URL de imagen si el proveedor de referencias
correspondiente los definió correctamente.
Por ejemplo, resolver `https://www.themoviedb.org/movie/70981` si la app `integration_tmdb` está instalada devolverá:

```json
"data": {
  "references": {
    "https://www.themoviedb.org/movie/70981": {
      "richObjectType": "integration_tmdb_movie",
      "richObject": {
        "adult": false,
        "budget": 130000000,
        "genres": [
          {
            "id": 878,
            "name": "Science Fiction"
          },
          {
            "id": 12,
            "name": "Adventure"
          },
          {
            "id": 9648,
            "name": "Mystery"
          }
        ],
        "homepage": "https://www.20thcenturystudios.com/movies/prometheus",
        "id": 70981,
        "imdb_id": "tt1446714",
        "original_language": "en",
        "original_title": "Prometheus",
        "overview": "A team of explorers discover a clue to the origins of mankind on Earth, leading them on a journey to the darkest corners of the universe. There, they must fight a terrifying battle to save the future of the human race.",
        "popularity": 68.389,
        "release_date": "2012-05-30",
        "revenue": 403354469,
        "runtime": 124,
      },
      "openGraphObject": {
        "id": "https://www.themoviedb.org/movie/70981",
        "name": "Prometheus",
        "description": "30 mai 2012 - A team of explorers discover a clue to the origins of mankind on Earth, leading them on a journey to the darkest corners of the universe. There, they must fight a terrifying battle to save the future of the human race.",
        "thumb": "https://my.nextcloud.org/apps/integration_tmdb/t/p/w500/qsYQflQhOuhDpQ0W2aOcwqgDAeI.jpg?fallbackName=???",
        "link": "https://www.themoviedb.org/movie/70981"
      },
      "accessible": true
    }
  }
}
```

#### Renderizar vistas previas de enlaces en clientes

Los clientes pueden optar por admitir algunos tipos de objetos enriquecidos.
Quienes desarrollan pueden seguir las recomendaciones de formato de objetos enriquecidos para proporcionar información genérica en algunos casos.
El tipo de objeto enriquecido no se usa para predecir la estructura de datos.
Más bien, se recomienda establecer los atributos del objeto enriquecido respetando un formato estricto para algunos casos de uso comunes.

Hay más detalles en {nc-ref}`data-for-clients`

### Usar el selector inteligente en la app

Hay 3 formas de hacer que el selector inteligente aparezca en la app:

- usar el componente `NcRichContenteditable`
- usar el componente `NcReferencePickerModal`
- usar la función auxiliar `getLinkWithPicker`

Igual que para las vistas previas de enlaces, hay que despachar el evento `OCP\Collaboration\Reference\RenderReferenceEvent`
antes de cargar la página en la que se quiere mostrar el selector inteligente.

#### NcRichContenteditable

El selector inteligente está integrado en el componente de Vue NcRichContenteditable. Está activado de forma predeterminada,
pero puede desactivarse estableciendo la prop `linkAutocomplete` en `false`.

La lista de proveedores del selector se abre cuando el usuario escribe el carácter «/».
El resultado del selector se inserta luego directamente en el contenido.

[Documentación del componente NcRichContenteditable](https://nextcloud-vue-components.netlify.app/#/Components/NcRichContenteditable)

#### NcReferencePickerModal

El selector inteligente se muestra usando el componente de Vue NcReferencePickerModal. Está disponible en la biblioteca de Vue de Nextcloud.

```javascript
import { NcReferencePickerModal } from '@nextcloud/vue/dist/Components/NcRichText.js'
```

Props disponibles:

- initialProvider (opcional): si se pasa un objeto de proveedor de referencias, se omite la selección del proveedor y se muestra directamente este proveedor
- focusOnCreate (opcional, valor predeterminado: true): pone el foco en el elemento de entrada principal al crearse
- isInsideViewer (opcional, valor predeterminado: false): establecerlo en true si NcReferencePickerModal se usa dentro del Viewer. Esto indica al Viewer que se ocupe de la trampa de foco.

#### getLinkWithPicker

Para mostrar el selector inteligente fuera de Vue, se puede usar la función auxiliar getLinkWithPicker.
Recibe 2 parámetros:

- providerId (opcional, valor predeterminado: null): el proveedor que se seleccionará en el selector. Si es null, primero se muestra la selección de proveedor.
- isInsideViewer (opcional): se pasará internamente a NcReferencePickerModal como la prop isInsideViewer.

Esta función devuelve una promesa que se resuelve con el resultado del selector. Esta promesa se rechaza si el usuario cierra
el selector inteligente.

```javascript
import { getLinkWithPicker } from '@nextcloud/vue/dist/Components/NcRichText.js'

getLinkWithPicker(null, true)
    .then(result => {
        console.debug('Smart Picker result', result)
    })
    .catch(error => {
        console.error('Smart Picker promise rejected', error)
    })
```

### Usar el selector inteligente en clientes

Los clientes pueden admitir parcialmente las funcionalidades del selector inteligente.

Hay 2 tipos de proveedores del selector inteligente:

- Los que tienen un componente de selector personalizado
- Los que admiten uno o varios proveedores de la búsqueda unificada

Como los componentes de selector personalizados son componentes web, puede que los clientes no puedan (o no quieran) renderizarlos.
Así que aquí interesa sobre todo el segundo tipo: los que usan proveedores de la búsqueda unificada.

En la interfaz web de Nextcloud, esos proveedores se renderizan con un
[componente de Vue de búsqueda genérico](https://github.com/nextcloud/nextcloud-vue/blob/master/src/components/NcRichText/NcReferencePicker/NcSearch.vue),
que muestra un campo de búsqueda, lista el resultado de la búsqueda en un menú desplegable y envía directamente la URL del resultado seleccionado.
La búsqueda se hace consultando directamente la API OCS de la búsqueda unificada. Esto se describe más adelante.

Para implementar algo similar al selector inteligente en un cliente, hay que saber cómo:

- Obtener la lista de proveedores
- Usar la API OCS de la búsqueda unificada
- Actualizar la fecha de último uso de los proveedores

#### Obtener la lista de proveedores

La lista de proveedores del selector inteligente puede obtenerse mediante un endpoint de OCS.
Cada objeto de proveedor contiene la lista de los proveedores de la búsqueda unificada que admite.

Este es el endpoint del servidor para listar los proveedores del selector inteligente:

```bash
curl -u USER:PASSWD -H "Accept: application/json" -H "ocs-apirequest: true" \
    "https://my.nextcloud.org/ocs/v2.php/references/providers"
```

y un ejemplo de respuesta:

```json
{
  "ocs": {
    "meta": {
      "status": "ok",
      "statuscode": 200,
      "message": "OK"
    },
    "data": [
      {
        "id": "github-issue-pr",
        "title": "GitHub issues, pull requests and comments",
        "icon_url": "https://my.nextcloud.org/apps/integration_github/img/app-dark.svg",
        "order": 10,
        "search_providers_ids": [
          "github-search-issues",
          "github-search-repos"
        ]
      },
      {
        "id": "openstreetmap-point",
        "title": "Map location (by OpenStreetMap)",
        "icon_url": "https://my.nextcloud.org/apps/integration_openstreetmap/img/app-dark.svg",
        "order": 10,
        "search_providers_ids": [
          "openstreetmap-search-location"
        ]
      },
      {
        "id": "files",
        "title": "Files",
        "icon_url": "https://my.nextcloud.org/apps/files/img/folder.svg",
        "order": 0
      }
    ]
  }
}
```

En este ejemplo, el proveedor del selector inteligente «files» no admite ningún proveedor de la búsqueda unificada,
pero «github-issue-pr» admite 2 de ellos y «openstreetmap-point» admite uno.

#### Usar la API de la búsqueda unificada

Hay más detalles en la documentación de la {nc-ref}`búsqueda unificada <unified-search>`.

Así se busca usando la API OCS de la búsqueda unificada:

```bash
curl -u USER:PASSWD -H "Accept: application/json" -H "ocs-apirequest: true" \
    "https://my.nextcloud.org/ocs/v2.php/search/providers/PROVIDER_ID/search?term=QUERY&limit=LIMIT"

# with a cursor (paginated search)
curl -u USER:PASSWD -H "Accept: application/json" -H "ocs-apirequest: true" \
    "https://my.nextcloud.org/ocs/v2.php/search/providers/PROVIDER_ID/search?term=QUERY&limit=LIMIT&cursor=CURSOR"

# search a github issue with the query "bug"
curl -u USER:PASSWD -H "Accept: application/json" -H "ocs-apirequest: true" \
    "https://my.nextcloud.org/ocs/v2.php/search/providers/github-search-issues/search?term=bug&limit=2"
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
      "name": "GitHub issues and pull requests",
      "isPaginated": true,
      "entries": [
        {
          "thumbnailUrl": "https://my.nextcloud.org/apps/integration_github/avatar/Daily-DAYO",
          "title": " [bug] Change Trim bugs",
          "subline": "⑁ DAYO_Android#409",
          "resourceUrl": "https://github.com/Daily-DAYO/DAYO_Android/pull/409",
          "icon": "",
          "rounded": true,
          "attributes": []
        },
        {
          "thumbnailUrl": "https://my.nextcloud.org/apps/integration_github/avatar/walinejs",
          "title": " [Bug]:  || [Bug]:",
          "subline": "⦿ waline#2014",
          "resourceUrl": "https://github.com/walinejs/waline/issues/2014",
          "icon": "",
          "rounded": true,
          "attributes": []
        }
      ],
      "cursor": 2
    }
  }
}
```

#### Actualizar la fecha de último uso de un proveedor

En la interfaz web de Nextcloud, el orden en que se listan los proveedores a los usuarios depende de la última
fecha en que se usaron. Los proveedores usados más recientemente se muestran primero.

En un cliente, una vez usado un proveedor, debe hacerse una solicitud a este endpoint:

```bash
curl -u USER:PASSWD -H "Accept: application/json" -H "ocs-apirequest: true" -X PUT \
    "https://my.nextcloud.org/ocs/v2.php/search/provider/PROVIDER_ID"
```

Se puede pasar un parámetro de solicitud opcional `timestamp`. De forma predeterminada, la fecha de último uso se establecerá en «ahora».

### Registrar un proveedor de referencias

Un proveedor de referencias es una clase que implementa la interfaz `OCP\Collaboration\Reference\IReferenceProvider`.
Si solo se quieren resolver enlaces, basta con implementar la interfaz `IReferenceProvider`.
Esto se describe en la sección «Resolver enlaces».

Para admitir la resolución de enlaces desde recursos compartidos públicos, también hay que implementar la interfaz
`OCP\Collaboration\Reference\IPublicReferenceProvider`.

Si se quiere que el selector inteligente use el proveedor de referencias, hay que extender la clase
`OCP\Collaboration\Reference\ADiscoverableReferenceProvider` para declarar toda la información necesaria.

Hay 2 formas de hacer que el proveedor aparezca en el selector inteligente; dicho de otro modo, 2 tipos de proveedores:

- O bien el proveedor de referencias implementa la interfaz `OCP\Collaboration\Reference\ISearchableReferenceProvider` y se declara una lista de proveedores de la búsqueda unificada que usará el selector inteligente
- O bien no se implementa esta interfaz `ISearchableReferenceProvider` y hay que asegurarse de registrar un componente de selector personalizado en el frontend. Esto se describe más adelante en esta documentación.

### Ampliar la compatibilidad con vistas previas de enlaces

Esta sección se centra en los métodos de la interfaz `IReferenceProvider`.

Los enlaces que no coincidan con ningún proveedor de referencias siempre los gestionará, como alternativa, el proveedor OpenGraph del servidor.
Este proveedor intentará obtener la información declarada en las metaetiquetas de la página de destino. La vista previa del enlace se renderizará con el
widget predeterminado.

Para que el proveedor gestione correctamente algunos enlaces, hay que implementar los métodos `matchReference` y `resolve`
de `IReferenceProvider`.

Para resolver enlaces desde un recurso compartido público, hay que implementar además `resolvePublic` de `IPublicReferenceProvider`.

#### Hacer coincidir los enlaces

El método `matchReference` de `IReferenceProvider` indica al gestor de referencias si un proveedor admite un enlace o no.

```php
public function matchReference(string $referenceText): bool {
    // support all URLs starting with https://my.website.org/
    return str_starts_with($referenceText, 'https://my.website.org/');
}
```

#### Resolver enlaces

El método `resolve` de `IReferenceProvider` se usa para obtener información sobre un enlace y devolverla como un objeto
`OCP\Collaboration\Reference\Reference`.

Respectivamente, el método `resolvePublic` de `IPublicReferenceProvider` se usa para obtener información sobre un
enlace de un recurso compartido público (disponible desde Nextcloud 30).

##### Usar el widget predeterminado

Si la renderización del widget predeterminado (imagen a la izquierda, texto y subtexto a la derecha) es suficiente,
basta con proporcionar un título, una descripción y, opcionalmente, una imagen.

```php
public function resolveReference(string $referenceText): ?IReference {
    if ($this->matchReference($referenceText)) {
        $title = $this->myAwesomeService->getLinkTitle($referenceText);
        $description = $this->myAwesomeService->getLinkDescription($referenceText);
        $imageUrl = $this->myAwesomeService->getImageUrl($referenceText);

        $reference = new Reference($referenceText);
        $reference->setTitle($title);
        $reference->setDescription($description);
        $reference->setImageUrl($imageUrl);
        return $reference;
    }
    return null;
}

public function resolveReferencePublic(string $referenceText, string $shareToken): ?IReference {
    if ($this->checkShareToken() === $shareToken) {
        return $this->resolveReference($referenceText);
    }
    return null;
}
```

##### Usar widgets de referencia personalizados

Se puede personalizar la renderización de los enlaces que admite el proveedor.

En el lado del proveedor, hay que pasar toda la información que necesita el componente
de widget de referencia personalizado estableciendo el «objeto enriquecido» del objeto `Reference`
devuelto por el método `resolve`.

Se recomienda establecer de todos modos el título, la descripción y la URL de la imagen en el objeto de referencia,
por si lo usa un cliente o se usa en un contexto en el que no pueden usarse los widgets de referencia personalizados.
Así se garantiza que cualquier renderización genérica de las vistas previas de enlaces siga mostrando algo de información.

```php
public function resolveReference(string $referenceText): ?IReference {
    if ($this->matchReference($referenceText)) {
        $title = $this->myAwesomeService->getLinkTitle($referenceText);
        $description = $this->myAwesomeService->getLinkDescription($referenceText);
        $imageUrl = $this->myAwesomeService->getImageUrl($referenceText);
        $extraInformation = $this->myAwesomeService->getExtraInformation($referenceText);

        $reference = new Reference($referenceText);
        $reference->setTitle($title);
        $reference->setDescription($description);
        $reference->setImageUrl($imageUrl);
        $reference->setRichObject(
            'my_rich_object_type',
            [
                'title' => $title,
                'description' => $description,
                'image_url' => $imageUrl,
                'extra_info' => $extraInformation,
            ]
        );

        return $reference;
    }
    return null;
}

public function resolveReferencePublic(string $referenceText, string $shareToken): ?IReference {
    if ($this->checkShareToken() === $shareToken) {
        return $this->resolveReference($referenceText);
    }
    return null;
}
```

En el frontend hay que implementar y registrar el componente personalizado. Este es un ejemplo de componente:

Hay que reaccionar al evento `OCP\Collaboration\Reference\RenderReferenceEvent`
para inyectar un script que registre realmente el componente del widget cuando sea necesario.
Por ejemplo, en el archivo `lib/AppInfo/Application.php`:

```php
$context->registerEventListener(OCP\Collaboration\Reference\RenderReferenceEvent::class, MyReferenceListener::class);
```

La clase `MyReferenceListener` correspondiente puede tener este aspecto:

```php
<?php
namespace OCA\MyApp\Listener;

use OCA\MyApp\AppInfo\Application;
use OCP\Collaboration\Reference\RenderReferenceEvent;
use OCP\EventDispatcher\Event;
use OCP\EventDispatcher\IEventListener;
use OCP\Util;

class MyReferenceListener implements IEventListener {
    public function handle(Event $event): void {
        if (!$event instanceof RenderReferenceEvent) {
            return;
        }

        Util::addScript(Application::APP_ID, 'myapp-reference');
    }
}
```

El archivo `myapp-reference.js` contiene el registro del widget:

```javascript
import { registerWidget } from '@nextcloud/vue/dist/Components/NcRichText.js'
import Vue from 'vue'
import MyCustomWidgetComponent from './MyCustomWidgetComponent.vue'

Vue.mixin({ methods: { t, n } })

// here we register the MyCustomWidgetComponent to handle rich objects which type is 'my_rich_object_type'
registerWidget('my_rich_object_type', (el, { richObjectType, richObject, accessible }) => {
    const Widget = Vue.extend(MyCustomWidgetComponent)
    new Widget({
        propsData: {
            richObjectType,
            richObject,
            accessible,
        },
    }).$mount(el)
})
```

Y, por último, pero no por ello menos importante, el componente de Vue MyCustomWidgetComponent, en el que se puede renderizar la vista previa del enlace
de forma personalizada:

```html
<template>
    <div v-if="richObject">
        <div>
            <label>
                {{ t('myapp', 'Title') }}
            </label>
            <span>
                {{ richObject.title }}
            </span>
        <div>
        <div>
            <label>
                {{ t('myapp', 'Extra info') }}
            </label>
            <span>
                {{ richObject.extra_info }}
            </span>
        <div>
    </div>
</template>

<script>
export default {
    name: 'MyCustomWidgetComponent',
    props: {
        richObjectType: {
            type: String,
            default: '',
        },
        richObject: {
            type: Object,
            default: null,
        },
        accessible: {
            type: Boolean,
            default: true,
        },
    },
}
</script>
```

(nc-dev-data-for-clients)=
#### Widgets interactivos

Si se quiere proporcionar un widget personalizado que sea interactivo, se puede usar el atributo `interactive`, que se pasa junto con la función `registerWidget`.

Las apps determinarán si pueden renderizar o no el widget interactivo.

Al escribir un widget personalizado, hay que asegurarse de gestionar correctamente las distintas restricciones para garantizar que el widget se pueda usar en cualquier app que lo integre.

- El ancho del widget debe ser flexible y no superar el ancho del elemento padre.
- La altura puede ser flexible, pero puede estar limitada por el elemento padre, así que hay que asegurarse de que el widget pueda desplazarse si es necesario
- El script se cargará en cada página que use la renderización de widgets, así que hay que mantener el tamaño del script lo más pequeño posible y usar carga diferida para cualquier recurso adicional

```javascript
import { registerCustomPickerElement, registerWidget, NcCustomPickerRenderResult } from '@nextcloud/vue/dist/Functions/registerReference.js'

registerWidget('my_rich_object_type', async (el, { richObjectType, richObject, accessible, interactive }) => {
    const { default: Vue } = await import('vue')
    const { default: MyWidget } = await import('./views/MyWidget.vue')

    const Widget = Vue.extend(MyWidget)
    const vueElement = new Widget({
        propsData: {
            richObjectType,
            richObject,
            accessible,
            interactive,
        },
    }).$mount(el)

    return new NcCustomPickerRenderResult(vueElement.$el, vueElement)
}, (el, renderResult) => {
    renderResult.object.$destroy()
}, true)
```

#### Proporcionar datos genéricos para clientes

En la interfaz web, los enlaces que resuelve la app se renderizan con el widget de OpenGraph
o con el widget de referencia personalizado que se haya implementado. Así que hay total libertad sobre el formato de datos que se pone en los objetos enriquecidos,
porque también se controla la implementación de la renderización web.

Pero como los clientes de escritorio o móviles no pueden usar los componentes de la interfaz web, tienen que admitir específicamente algunos objetos enriquecidos
que tengan el formato adecuado.

Estas son algunas sugerencias de formato para algunos casos de uso. Usarlas si se quiere que los enlaces resueltos se rendericen en los clientes.
La idea es agregar un atributo genérico en los objetos enriquecidos, independientemente del tipo de objeto enriquecido.

##### Incidencia de control de versiones

Establecer el atributo `vcs_issue` del objeto enriquecido en un objeto que contenga estos atributos:

- `id`: el ID de la incidencia (número)
- `url`: la URL de la página de la incidencia
- `title`: el título de la incidencia
- `comment_count`: el número de comentarios de la incidencia
- `state`: el estado de la incidencia ('open' o 'closed')
- `labels`: un array de etiquetas. Una etiqueta es un objeto con estos atributos:
  - `color`: código de color hexadecimal
  - `name`: el nombre de la etiqueta
- `created_at`: la marca de tiempo de creación
- `author`: el ID de usuario o el nombre de quien creó la incidencia

Ejemplo de implementación: [vista previa de enlaces de incidencias de la integración con GitHub](https://github.com/nextcloud/integration_github/blob/e6792ea0aadef4f5b8faaaaa163a0cf473d86157/lib/Reference/GithubIssuePrReferenceProvider.php#L135)

##### Pull request de control de versiones

Establecer el atributo `vcs_pull_request` del objeto enriquecido en un objeto que contenga los mismos atributos que en `vcs_issue` más estos:

- `merged`: ¿se fusionó? (booleano)
- `draft`: ¿es un borrador? (booleano)

Ejemplo de implementación: [vista previa de enlaces de pull requests de la integración con GitHub](https://github.com/nextcloud/integration_github/blob/e6792ea0aadef4f5b8faaaaa163a0cf473d86157/lib/Reference/GithubIssuePrReferenceProvider.php#L162)

##### Comentario de una incidencia o de un pull request de control de versiones

Establecer el atributo `vcs_comment` del objeto enriquecido en un objeto que contenga estos atributos:

- `url`: un enlace directo/enlace permanente al comentario
- `body`: el contenido del comentario en texto plano o markdown
- `author`: el ID de usuario o el nombre de quien escribió el comentario
- `created_at`: la marca de tiempo de creación
- `updated_at`: la marca de tiempo de la última edición

`vcs_comment` puede establecerse además de `vcs_issue` o `vcs_pull_request`.

##### Imágenes

Establecer el atributo `image_TYPE` del objeto enriquecido en `true`. Así los clientes sabrán que pueden renderizarlo como una imagen
usando el título, la descripción y la URL de imagen de la referencia que se hayan establecido.

El tipo puede ser `gif`, `jpeg`, `png`, etc...

Ejemplo de implementación: [integración con Giphy](https://github.com/nextcloud/integration_giphy/blob/6c07af9c99014599bd3582a26e4fd99678b275ef/lib/Reference/GiphyReferenceProvider.php#L114-L124)

### Ampliar el selector inteligente

Si se quiere que el proveedor de referencias aparezca en el selector inteligente para buscar/obtener enlaces,
tiene que ser descubrible
(extender la clase abstracta `OCP\Collaboration\Reference\ADiscoverableReferenceProvider`)
y, o bien

- admitir uno o varios proveedores de la búsqueda unificada
- o registrar un componente de selector personalizado

Esta es una elección excluyente. No se pueden admitir proveedores de búsqueda Y registrar un componente de selector personalizado.
Si aun así se quieren combinar ambos enfoques, se puede registrar un componente de selector personalizado que incluya una funcionalidad de búsqueda personalizada.

Extender `ADiscoverableReferenceProvider` implica definir estos métodos:

- `getId`: devuelve un ID que el selector inteligente usará para identificar este proveedor
- `getTitle`: devuelve un título del proveedor (idealmente traducido), visible en la lista de proveedores del selector inteligente
- `getOrder`: devuelve un entero que ayuda a ordenar los proveedores. Después, este orden queda reemplazado por la marca de tiempo del último uso
- `getIconUrl`: devuelve la URL del icono del proveedor; igual que el título, el icono será visible en la lista de proveedores

#### Declarar los proveedores de la búsqueda unificada admitidos

Si se quiere que el proveedor de referencias permita a los usuarios elegir enlaces de los resultados de la búsqueda unificada, el proveedor de referencias debe
implementar `OCP\Collaboration\Reference\ISearchableReferenceProvider` y definir el método `getSupportedSearchProviderIds`,
que devuelve una lista de ID de proveedores de búsqueda admitidos.

Una vez seleccionado este proveedor en el selector inteligente, los usuarios verán una interfaz de búsqueda genérica con resultados de
todos los proveedores de búsqueda que se hayan declarado como admitidos. Una vez seleccionado un resultado, el selector inteligente devolverá
la URL del recurso asociado.

#### Registrar un componente de selector personalizado

En el backend, en `lib/AppInfo/Application.php`, hay que escuchar el
`OCP\Collaboration\Reference\RenderReferenceEvent`. En el listener correspondiente hay que cargar
los scripts que registrarán los componentes de selector personalizados.

Dicho de otro modo, cuando se despacha el evento `RenderReferenceEvent`,
es posible que se use el selector inteligente en el frontend, así que hay que cargar los scripts relacionados de la app.

Se puede definir una interfaz de usuario de selector propia para el proveedor registrando un componente de selector personalizado.
Esto se puede hacer con la
función `registerCustomPickerElement` de `@nextcloud/vue/dist/Components/NcRichText.js`.
Esta función recibe 3 parámetros:

- El ID del proveedor de referencias para el que se registra el componente de selector personalizado
- La función de callback para crear y montar el componente
- La función de callback para eliminar/destruir el componente

El callback de creación debe devolver un objeto `NcCustomPickerRenderResult`, al que hay que pasar el elemento DOM
recién creado y, opcionalmente, un objeto (la instancia de Vue, por ejemplo).
Este resultado de renderización se pasará luego al callback de destrucción para poder limpiar y eliminar correctamente el componente personalizado.

Para registrar un componente de Vue como componente de selector personalizado:

```javascript
import { registerCustomPickerElement, NcCustomPickerRenderResult } from '@nextcloud/vue/dist/Components/NcRichText.js'
import Vue from 'vue'
import MyCustomPickerElement from './MyCustomPickerElement.vue'

registerCustomPickerElement('REFERENCE_PROVIDER_ID', (el, { providerId, accessible }) => {
    const Element = Vue.extend(MyCustomPickerElement)
    const vueElement = new Element({
        propsData: {
            providerId,
            accessible,
        },
    }).$mount(el)
    return new NcCustomPickerRenderResult(vueElement.$el, vueElement)
}, (el, renderResult) => {
    // call the $destroy method on your custom element's Vue instance
    renderResult.object.$destroy()
})
```

Para registrar cualquier otra cosa:

```javascript
import {
    registerCustomPickerElement,
    NcCustomPickerRenderResult,
} from '@nextcloud/vue/dist/Components/NcRichText.js'

registerCustomPickerElement('REFERENCE_PROVIDER_ID', (el, { providerId, accessible }) => {
    const paragraph = document.createElement('p')
    paragraph.textContent = 'click this button to return a link'
    el.append(paragraph)
    const button = document.createElement('button')
    button.textContent = 'I am a button'
    button.addEventListener('click', () => {
        const event = new CustomEvent(
            'submit',
            {
                bubbles: true,
                detail: 'https://nextcloud.com'
            }
        )
        el.dispatchEvent(event)
    })
    el.append(button)
    return new NcCustomPickerRenderResult(el)
}, (el, renderResult) => {
    renderResult.element.remove()
})
```

En el componente personalizado, basta con emitir el evento `submit` con el resultado como datos del evento para devolverlo al selector inteligente.
También se puede emitir el evento `cancel` para cancelar y volver atrás.
````
