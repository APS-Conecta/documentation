---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API de la app Actividad: publicar eventos; implementar proveedores, ajustes y filtros; y consumir el flujo de actividad con la API REST v2."
---
(nc-dev-activity-api)=
# API de actividad

## Resumen

Esta página describe, para quienes desarrollan apps y clientes, la API de la app Actividad: cómo registrar y publicar eventos de actividad, cómo implementar sus proveedores, ajustes y filtros, y cómo consumir el flujo de actividad mediante la API REST v2.

````{upstream} developer_manual/client_apis/activity-api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

La app Actividad ofrece una API para que otras apps de Nextcloud publiquen eventos, los muestren en el flujo de actividad y permitan a los usuarios controlar sus preferencias de notificación. También expone una API REST para que los clientes consuman el flujo de actividad.

La API de extensión consta de cuatro interfaces, todas en el espacio de nombres `OCP`:

- **IEvent** — El objeto del evento de actividad
- **IProvider** — Analiza y traduce las actividades para mostrarlas
- **ISetting** — Define los tipos de actividad y las preferencias de notificación
- **IFilter** — Añade filtros a la barra lateral del flujo de actividad

Las tres interfaces de extensión (IProvider, ISetting, IFilter) se registran en el `appinfo/info.xml` de la app.

### Registrar los componentes de actividad

Añadir una sección `<activity>` al `appinfo/info.xml` de la app para registrar proveedores, ajustes y filtros:

```xml
<?xml version="1.0"?>
<info>
    ...
    <activity>
        <settings>
            <setting>OCA\MyApp\Activity\Setting</setting>
        </settings>

        <filters>
            <filter>OCA\MyApp\Activity\Filter</filter>
        </filters>

        <providers>
            <provider>OCA\MyApp\Activity\Provider</provider>
        </providers>
    </activity>
</info>
```

Cada valor es el nombre de clase completamente cualificado de la implementación.

### Crear y publicar eventos

Para crear y publicar un evento de actividad, generar un `IEvent` desde el gestor de actividad y llamar a `publish()`:

```php
<?php
// IManager is injected via dependency injection
$event = $this->activityManager->generateEvent();
$event->setApp('myapp')
    ->setType('myapp_action')
    ->setAffectedUser('targetUser')
    ->setSubject('subject_key', ['param1' => 'value1'])
    ->setObject('myobject', 42, 'Object Name');
$this->activityManager->publish($event);
```

#### Campos obligatorios

Antes de publicar hay que establecer lo siguiente:

- `setApp()` — El ID de la app
- `setType()` — Debe coincidir con un `ISetting::getIdentifier()`
- `setAffectedUser()` — El usuario que verá esta actividad
- `setSubject()` — Una clave de asunto y parámetros opcionales
- `setObject()` — El tipo, el ID y el nombre del objeto

#### Campos opcionales

- `setAuthor()` — Si no se establece, se usa el usuario actual
- `setTimestamp()` — Si no se establece, se usa la hora actual
- `setMessage()` — Una clave de mensaje adicional y parámetros
- `setLink()` — Normalmente debería establecerse en `IProvider::parse()` en su lugar
- `setIcon()` — Normalmente debería establecerse en `IProvider::parse()` en su lugar

:::{note}
No llamar a `setParsedSubject()`, `setRichSubject()`, `setParsedMessage()`, `setRichMessage()` ni `setChildEvent()` al publicar. Estos valores no se guardan de forma persistente y deberían establecerse en el método `parse()` del proveedor.
:::

### Implementar un proveedor

Los proveedores implementan `OCP\Activity\IProvider` para analizar, traducir y embellecer las actividades a fin de mostrarlas. La interfaz tiene un único método `parse()`.

#### Comprobar la responsabilidad

Primero, comprobar si el evento pertenece a la app. Si no es así, lanzar `UnknownActivityException` para que la app Actividad lo pase al siguiente proveedor:

```php
<?php
public function parse(string $language, IEvent $event, ?IEvent $previousEvent = null): IEvent {
    if ($event->getApp() !== 'myapp') {
        throw new \OCP\Activity\Exceptions\UnknownActivityException();
    }

    // ... parse the event
}
```

:::{note}
`UnknownActivityException` se añadió en Nextcloud 30. En versiones anteriores, lanzar `\InvalidArgumentException` en su lugar.
:::

#### Establecer el asunto analizado

Como mínimo, hay que llamar a `setParsedSubject()` con una cadena traducida en texto plano:

```php
$event->setParsedSubject(
    $this->l->t('You created %1$s', [$event->getObjectName()])
);
```

Además, se debería llamar a:

- `setIcon()` — Una URL completa de un icono para la actividad
- `setRichSubject()` — Una cadena traducida con marcadores de posición y un array de parámetros para la visualización enriquecida

:::{note}
A partir de Nextcloud 26, llamar a `setRichSubject()` genera automáticamente un asunto analizado, por lo que ya no es necesaria una llamada aparte a `setParsedSubject()`.
:::

#### Cadenas de objetos enriquecidos

Los asuntos enriquecidos permiten que la interfaz represente elementos interactivos, como enlaces a archivos y avatares de usuario. El método `setRichSubject()` recibe una cadena traducida con marcadores de posición y un array de objetos tipados:

```php
$event->setRichSubject(
    $this->l->t('You added {file} to your favorites'),
    ['file' => [
        'type' => 'file',
        'id' => (string) $event->getObjectId(),
        'name' => basename($event->getObjectName()),
        'path' => $event->getObjectName(),
    ]]
);
```

Los tipos de objeto disponibles y sus claves obligatorias se definen en [OCP\RichObjectStrings\Definitions](https://github.com/nextcloud/server/blob/master/lib/public/RichObjectStrings/Definitions.php).

#### Traducciones cortas y largas

Las actividades relacionadas con archivos admiten una forma corta (p. ej., «Añadido a favoritos») para la barra lateral y una forma larga (p. ej., «Has añadido hello.jpg a tus favoritos») para el flujo. Comprobar `IManager::isFormattingFilteredObject()` para decidir qué forma usar.

#### Combinar actividades

Las actividades relacionadas pueden combinarse automáticamente con `OCP\Activity\IEventMerger` (se inyecta mediante inyección de dependencias). El combinador une los eventos cuando se cumplen todas las condiciones siguientes:

- Mismo `getApp()`
- Sin mensaje establecido (`getMessage()` está vacío)
- Mismo `getSubject()`
- Mismo `getObjectType()`
- La diferencia de tiempo es inferior a 3 horas
- Se combinan como máximo 5 eventos

No combinar eventos manualmente si no se cumplen estos requisitos.

### Implementar un ajuste

Los ajustes definen tipos de actividad y aparecen en la página personal de preferencias de notificación. Implementan `OCP\Activity\ISetting`.

:::{list-table}
:header-rows: 1
:widths: 25 75

* - Método
  - Descripción
* - `getIdentifier()`
  - ID único (solo `a-z` en minúsculas y guiones bajos). **Debe coincidir** con el valor usado en `IEvent::setType()`.
* - `getName()`
  - Descripción breve y traducida. Puede usar `<strong>` para dar énfasis.
* - `getIcon()`
  - URL absoluta de un icono de 32x32 píxeles (preferiblemente SVG).
* - `getPriority()`
  - De `0` (primero) a `100` (último). Usar `70` como valor predeterminado. Los valores inferiores a `10` están reservados.
* - `isDefaultEnabledStream()`
  - Si la visualización en el flujo está habilitada de forma predeterminada para los usuarios nuevos.
* - `isDefaultEnabledMail()`
  - Si las notificaciones por correo electrónico están habilitadas de forma predeterminada.
* - `canChangeStream()`
  - Si los usuarios pueden activar o desactivar la visualización en el flujo.
* - `canChangeMail()`
  - Si los usuarios pueden activar o desactivar las notificaciones por correo electrónico.
:::

Cuando tanto `canChangeStream()` como `canChangeMail()` devuelven `false`, el ajuste se oculta por completo de la página personal.

### Implementar un filtro

Los filtros restringen el flujo de actividad y aparecen en la navegación de la barra lateral. Implementan `OCP\Activity\IFilter`.

:::{list-table}
:header-rows: 1
:widths: 25 75

* - Método
  - Descripción
* - `getIdentifier()`
  - ID único (solo `a-z` en minúsculas y guiones bajos). Se usa en las URL.
* - `getName()`
  - Etiqueta traducida, de 1 a 3 palabras cortas.
* - `getIcon()`
  - URL absoluta de un icono de 32x32 píxeles (preferiblemente SVG).
* - `getPriority()`
  - De `0` (primero) a `100` (último). Usar `70` como valor predeterminado. Los valores inferiores a `10` están reservados.
* - `allowedApps()`
  - Devolver un array con los ID de las apps que se mostrarán, o un array vacío para todas las apps.
* - `filterTypes()`
  - Recibe una lista de identificadores de tipo (de `ISetting`); devolver un subconjunto filtrado. Devolver la entrada sin cambios para mostrar todos los tipos.
:::

Ejemplo de filtro que solo muestra las actividades de tareas del calendario:

```php
public function filterTypes(array $types): array {
    return array_intersect(['calendar_todo'], $types);
}
```

### API REST (v2)

La app Actividad expone una API REST para que los clientes consuman el flujo de actividad.

#### Capacidades

La API anuncia sus funciones mediante las capacidades:

```xml
GET /ocs/v2.php/cloud/capabilities

<activity>
 <apiv2>
  <element>filters</element>
  <element>previews</element>
  <element>rich-strings</element>
 </apiv2>
</activity>
```

#### Endpoints

```text
GET /ocs/v2.php/apps/activity/api/v2/activity
GET /ocs/v2.php/apps/activity/api/v2/activity/{filter}
GET /ocs/v2.php/apps/activity/api/v2/activity/filters
```

#### Parámetros

:::{list-table}
:header-rows: 1
:widths: 20 15 65

* - Nombre
  - Tipo
  - Descripción
* - `since`
  - int
  - ID de la última actividad vista (opcional)
* - `limit`
  - int
  - Número de actividades que se devuelven (predeterminado: `50`, opcional)
* - `object_type`
  - string
  - Filtrar por tipo de objeto. Requiere `object_id` y el filtro de tipo `filter` (opcional)
* - `object_id`
  - string
  - Filtrar por ID de objeto. Requiere `object_type` y el filtro de tipo `filter` (opcional)
* - `sort`
  - string
  - `asc` o `desc` (predeterminado: `desc`, opcional)
:::

#### Códigos de estado HTTP

:::{list-table}
:header-rows: 1
:widths: 20 80

* - Código
  - Descripción
* - `200 OK`
  - Se devuelven las actividades
* - `204 No Content`
  - El usuario no tiene actividades seleccionadas para el flujo
* - `304 Not Modified`
  - El ETag coincide o se llegó al final de la lista
* - `403 Forbidden`
  - La actividad usada como desplazamiento pertenece a otro usuario, o no se ha iniciado sesión
* - `404 Not Found`
  - Filtro desconocido
:::

#### Cabeceras de respuesta

- `Link`: URL de la página siguiente de resultados, incluidos todos los parámetros: `<https://cloud.example.com/ocs/v2.php/apps/activity/api/v2/activity/all?since=364>; rel="next"`
- `X-Activity-First-Known`: ID de la primera actividad conocida (cuando no se reconoció `since`).
- `X-Activity-Last-Given`: ID que se usa como `since` en la siguiente petición.

#### Campos del elemento de actividad

:::{list-table}
:header-rows: 1
:widths: 20 15 65

* - Campo
  - Tipo
  - Descripción
* - `activity_id`
  - int
  - ID único de la actividad
* - `datetime`
  - string
  - Marca de tiempo ISO 8601
* - `app`
  - string
  - App que creó la actividad
* - `type`
  - string
  - Identificador del tipo de actividad
* - `user`
  - string
  - ID de usuario del actor (puede estar vacío)
* - `subject`
  - string
  - Asunto traducido en texto plano
* - `subject_rich`
  - array
  - Asunto enriquecido: `[0]` es la cadena de plantilla y `[1]` es el objeto de parámetros
* - `message`
  - string
  - Mensaje traducido en texto plano (opcional)
* - `message_rich`
  - array
  - Mensaje enriquecido, con el mismo formato que `subject_rich` (opcional)
* - `icon`
  - string
  - URL completa del icono de la actividad (opcional)
* - `link`
  - string
  - URL completa de la ubicación correspondiente (opcional)
* - `object_type`
  - string
  - Tipo del objeto relacionado (opcional)
* - `object_id`
  - int
  - ID del objeto relacionado (opcional)
* - `object_name`
  - string
  - Nombre o ruta del objeto relacionado (opcional)
* - `previews`
  - array
  - Lista de elementos de vista previa para las actividades de archivos (opcional)
:::

#### Ejemplo de respuesta

```json
{
  "activity_id": 1,
  "datetime": "2015-11-20T12:49:31+00:00",
  "app": "files",
  "type": "file_created",
  "user": "test1",
  "subject": "test1 created hello.txt",
  "subject_rich": {
    "0": "{user1} created {file1}",
    "1": {
      "user1": {
        "type": "user",
        "id": "test1",
        "name": "Test User"
      },
      "file1": {
        "type": "file",
        "id": 23,
        "name": "hello.txt",
        "path": "/test/hello.txt"
      }
    }
  },
  "icon": "https://cloud.example.com/apps/files/img/add-color.svg",
  "link": "https://cloud.example.com/apps/files/?dir=/test",
  "object_type": "files",
  "object_id": 23,
  "object_name": "/test/hello.txt",
  "previews": [
    {
      "source": "https://cloud.example.com/core/preview.png?file=/hello.txt&x=150&y=150",
      "link": "https://cloud.example.com/apps/files/?dir=/test&scrollto=hello.txt",
      "mimeType": "text/plain",
      "fileId": 23,
      "view": "files",
      "isMimeTypeIcon": false,
      "filename": "hello.txt"
    }
  ]
}
```

:::{note}
Pueden aparecer en las respuestas campos adicionales no enumerados arriba, por compatibilidad con versiones anteriores, pero deberían ignorarse.
:::

### Lecturas adicionales

El repositorio de la app Actividad contiene documentación adicional con ejemplos más detallados:

- [Crear eventos](https://github.com/nextcloud/activity/blob/master/docs/create.md)
- [Implementar un proveedor](https://github.com/nextcloud/activity/blob/master/docs/provider.md)
- [Implementar un ajuste](https://github.com/nextcloud/activity/blob/master/docs/setting.md)
- [Implementar un filtro](https://github.com/nextcloud/activity/blob/master/docs/filter.md)
- [Endpoint de la API REST v2](https://github.com/nextcloud/activity/blob/master/docs/endpoint-v2.md)
````
