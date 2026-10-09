---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API de la app Archivos reescrita en Nextcloud 27: bibliotecas externas de referencia, eventos de nodos del bus de eventos y el enrutador expuesto."
---
(nc-dev-filesapi)=
# Archivos

## Resumen

Esta página describe, para quienes desarrollan apps, las API de la app Archivos reescrita en Nextcloud 27: las bibliotecas externas con documentación técnica, los eventos de nodos que se escuchan con el bus de eventos y el enrutador que permite cambiar de vista.

````{upstream} developer_manual/client_apis/files.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

:::{versionadded} 27
:::

Desde Nextcloud 27, la app Archivos se ha reescrito para usar nuevos estándares y frameworks. Esto significa que la documentación anterior ya no es válida. Aquí se actualizarán y documentarán las API y los métodos de la nueva app Archivos.

:::{note}
Algunas bibliotecas externas ofrecen documentación técnica detallada. Consultar las siguientes:

- <https://github.com/nextcloud-libraries/nextcloud-event-bus> ([documentación](https://nextcloud-libraries.github.io/nextcloud-event-bus))
- <https://github.com/nextcloud-libraries/nextcloud-files> ([documentación](https://nextcloud-libraries.github.io/nextcloud-files))
- <https://github.com/nextcloud-libraries/nextcloud-upload> ([documentación](https://nextcloud-libraries.github.io/nextcloud-upload))
:::

### Eventos

Para escuchar los cambios en archivos o carpetas, o para desencadenar cambios, hay que usar el `event-bus` y los siguientes eventos:

- `files:node:created`: se ha creado el nodo
- `files:node:deleted`: se ha eliminado el nodo
- `files:node:moved`: se ha movido el nodo (y sus datos ya están actualizados)
- `files:node:updated`: se han actualizado los datos del nodo

Todos estos eventos reciben un Node como argumento. Se puede usar un cliente WebDAV (por ejemplo, mediante la función davGetClient de [@nextcloud/files](https://nextcloud-libraries.github.io/nextcloud-files/)) para obtener un nodo a partir del nombre de un archivo.

#### Ejemplos

```ts
import type { Node } from '@nextcloud/files'
import { subscribe } from '@nextcloud/event-bus'

subscribe('files:node:created', (node: Node) => {
  console.log('Node created', node)
})
```

### Enrutador

Para cambiar las vistas y los parámetros de la app Archivos actual, se expone el enrutador. Este se corresponde directamente con el enrutador de Vue. Se puede consultar su propia [documentación](https://router.vuejs.org/guide/essentials/navigation.html#navigate-to-a-different-location) para entender mejor los métodos.

```ts
/**
 * Trigger a route change on the files app
 *
 * @param path the url path, eg: '/trashbin?dir=/Deleted'
 * @param replace replace the current history
 * @see https://router.vuejs.org/guide/essentials/navigation.html#navigate-to-a-different-location
 */
goTo(path: string, replace: boolean = false): Promise<Route>

/**
 * Trigger a route change on the files App
 *
 * @param name the route name
 * @param params the route parameters
 * @param query the url query parameters
 * @param replace replace the current history
 * @see https://router.vuejs.org/guide/essentials/navigation.html#navigate-to-a-different-location
 */
goToRoute(
  name?: string,
  params?: Dictionary<string>,
  query?: Dictionary<string | (string | null)[] | null | undefined>,
  replace?: boolean,
): Promise<Route>
```

#### Ejemplos

```js
OCP.Files.Router.goTo('/trashbin?dir=/Unsplash.d1680193199')
OCP.Files.Router.goToRoute('fileslist', { view: 'files' }, { dir: '/Folders/Group folder' })
```
````
