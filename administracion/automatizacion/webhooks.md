---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Receptores de webhooks: activar la app, registrar y filtrar webhooks, acelerar su envío con workers y carga útil de los eventos habituales."
---
# Receptores de webhooks

## Resumen

Esta página describe, para quienes administran el servidor, la app Webhook Listeners, que notifica a servicios externos los eventos de la instancia: cómo activarla, registrar y filtrar webhooks, acelerar su envío con workers de trabajos en segundo plano y qué carga útil envían los eventos disponibles habitualmente.

````{upstream} admin_manual/webhook_listeners/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

(nc-webhook_listeners)=
### Introducción

Nextcloud admite el envío de notificaciones a servicios externos cada vez que ocurre algo importante, por ejemplo, cuando se cambian o actualizan archivos.

### Descripción general

La app Webhook Listeners permite que el servidor de Nextcloud notifique automáticamente a servicios externos cada vez que ocurren eventos importantes en la instancia, como cambios, subidas o eliminaciones de archivos. Al configurar receptores de webhooks, los administradores pueden establecer notificaciones HTTP personalizadas (webhooks) que se disparan con eventos internos específicos, lo que permite una integración fluida con otras plataformas y la automatización de flujos de trabajo sin intervención manual.

La app funciona supervisando el sistema de eventos de Nextcloud y enviando solicitudes HTTP a los puntos de conexión definidos cada vez que se produce un evento coincidente. La gestión y la configuración de los receptores de webhooks se realizan mediante la API OCS de Nextcloud y herramientas de línea de comandos. La app es ideal para los casos en que se quiere conectar Nextcloud con sistemas de notificaciones, plataformas de automatización externas o integraciones personalizadas, sin necesidad de sondeo manual.

### Instalación

Activar la app `webhook_listeners` que viene incluida con Nextcloud; por ejemplo:

```bash
occ app:enable webhook_listeners
```

### Escuchar eventos

Puede usarse la API OCS para añadir webhooks para eventos específicos. Consultar: [Registrar un nuevo webhook](https://docs.nextcloud.com/server/latest/developer_manual/_static/openapi.html#/operations/webhook_listeners-webhooks-index).

Nota: al autenticarse con la API OCS para registrar webhooks, la cuenta que se use debe tener derechos de administrador o derechos de administración delegada.

#### Listar los webhooks registrados

Todos los receptores de webhooks registrados actualmente pueden listarse desde la línea de comandos:

```bash
occ webhook_listeners:list
```

De forma predeterminada, esto imprime una tabla. Usar la opción `--output` para cambiar el formato. Cada fila contiene la configuración completa de un webhook registrado

#### Filtros

Al registrar un receptor de webhooks, puede especificarse un parámetro de filtro (`eventFilter`). El filtro se evalúa contra el **sobre completo de la carga útil del webhook**, que tiene esta estructura:

```json
{
  "event": { "class": "…", "…event-specific fields…" },
  "user": { "uid": "…", "displayName": "…" },
  "time": 1700100000
}
```

Las claves de filtro usan **notación de puntos** para recorrer objetos anidados. Por ejemplo:

- `time` — coincide con la marca de tiempo Unix de nivel superior
- `user.uid` — coincide con el campo `uid` dentro del objeto `user`
- `event.class` — coincide con el nombre de clase completamente cualificado del evento dentro de `event`
- `event.node.path` — coincide con el campo `path` dentro de `event` → `node`
  (para eventos de nodo)
- `event.calendarId` — coincide con el campo `calendarId` dentro de `event`
  (para eventos de calendario)

El valor del parámetro de filtro debe ser un objeto JSON cuyas propiedades representen condiciones de filtro. El objeto `{}` es una consulta vacía, es decir, no se establece ningún criterio específico, por lo que coinciden todos los eventos.

Para que coincidan los eventos disparados por un usuario específico, puede pasarse `{ "user.uid": "bob" }`, que coincide con todos los eventos asociados al usuario `bob`.

Para exigir varios criterios, basta con pasar varias propiedades: `{ "event.tableId": 42, "event.rowId": 3 }`.

Para que los valores coincidan parcialmente, pueden usarse expresiones regulares: `{ "user.uid": "/admin_.*/" }` coincide con cualquier usuario cuyo ID de usuario empiece por `admin_`. Esto puede ser especialmente útil para los eventos del sistema de archivos al filtrar por ruta: `{ "event.node.path": "/^\\/.*\\/files\\/Special folder\\//" }` coincide con los archivos que están dentro de la carpeta `Special folder` de cualquier usuario. Tener en cuenta que las barras de la ruta deben escaparse con dos barras invertidas: una vez porque se está dentro de una cadena JSON y otra porque se está dentro de una expresión regular.

También pueden usarse operadores de comparación (`$e`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`, `$all`, `$exists`, `$mod`), así como operadores lógicos (`$and`, `$or`, `$not`, `$nor`).

Por ejemplo, usar `{ "time": { "$lt": 1711971024 } }` para aceptar solo los eventos anteriores al 1 de abril de 2024, y `{ "time": { "$not": { "$lt": 1711971024 } } }` para aceptar los eventos posteriores al 1 de abril de 2024.

Usar `{ "event.node.id": { "$exists": true } }` para que coincidan solo los eventos en los que el nodo todavía tiene un ID (es decir, no es un `NonExistingFile`/`NonExistingFolder`).

Usar `{ "event.class": "OCP\\Files\\Events\\Node\\NodeCreatedEvent" }` para que coincidan solo los eventos `NodeCreatedEvent` (las barras invertidas deben escaparse en las cadenas JSON).

(nc-webhook_dispatch)=
#### Acelerar el envío de webhooks

Esta app usa trabajos en segundo plano para disparar los webhooks registrados. De forma predeterminada, los webhooks se disparan cada 5 minutos, ya que el intervalo predeterminado de cron es de 5 minutos. Para disparar los webhooks antes, puede configurarse un worker de trabajos en segundo plano.

El siguiente comando inicia un worker para el trabajo en segundo plano que llama a los webhooks:

##### Sesión de screen o tmux

Ejecutar el siguiente comando `occ` dentro de una sesión de screen o tmux, preferiblemente cuatro o más veces, para permitir el procesamiento en paralelo de varias solicitudes de distintos usuarios o del mismo usuario. Lo mejor es ejecutar un comando por sesión de screen o por ventana o panel de tmux, para mantener visibles los registros y que cada worker sea fácil de reiniciar.

```
set -e; while true; do sudo -E -u www-data php occ background-job:worker -v -t 60 "OCA\WebhookListeners\BackgroundJobs\WebhookCall"; done
```

Para Nextcloud-AIO, debe usarse este comando en el servidor anfitrión.

```
set -e; while true; do sudo docker exec -it nextcloud-aio-nextcloud docker exec -it nextcloud-aio-nextcloud sudo -E -u www-data php occ background-job:worker -v -t 60 "OCA\WebhookListeners\BackgroundJobs\WebhookCall"; done
```

Puede convenir ajustar el número de workers y el tiempo de espera (en segundos) según las necesidades. Los registros del worker pueden consultarse conectándose a la sesión de screen o tmux.

##### Servicio de systemd

1. Crear un archivo de servicio de systemd en `/etc/systemd/system/nextcloud-webhook-worker@.service` con el siguiente contenido:

```
[Unit]
Description=Nextcloud Webhook worker %i
After=network.target

[Service]
ExecStart=/opt/nextcloud-webhook-worker/taskprocessing.sh %i
Restart=always
StartLimitInterval=60
StartLimitBurst=10

[Install]
WantedBy=multi-user.target
```

2. Crear un script de shell en `/opt/nextcloud-webhook-worker/taskprocessing.sh` con el siguiente contenido y asegurarse de hacerlo ejecutable:

```
#!/bin/sh
echo "Starting Nextcloud Webhook Worker $1"
cd /path/to/nextcloud
sudo -E -u www-data php occ background-job:worker -t 60 'OCA\WebhookListeners\BackgroundJobs\WebhookCall'
```

Puede convenir ajustar el tiempo de espera según las necesidades (en segundos).

3. Activar e iniciar el servicio 4 o más veces:

```
for i in {1..4}; do systemctl enable --now nextcloud-webhook-worker@$i.service; done
```

El estado de los workers puede comprobarse con (sustituir 1 por el número del worker):

```
systemctl status nextcloud-webhook-worker@1.service
```

La lista de workers puede comprobarse con:

```
systemctl list-units --type=service | grep nextcloud-webhook-worker
```

Los registros completos de los workers pueden consultarse con (sustituir 1 por el número del worker):

```
sudo journalctl -xeu nextcloud-webhook-worker@1.service -f
```

Se recomienda reiniciar este worker al menos una vez al día para asegurarse de que los cambios de código surtan efecto y evitar fugas de memoria; en este ejemplo, el servicio se reinicia cada 60 segundos.

### Eventos de webhook de Nextcloud

Esta es una lista de los eventos disponibles habitualmente. Incluye el ID del evento y las variables disponibles para filtrar.

:::{note}
Además de los eventos que se enumeran a continuación (que proporcionan el servidor de Nextcloud y las apps incluidas), las apps opcionales pueden registrar sus propios eventos compatibles con webhooks. El conjunto exacto de eventos disponibles en el servidor dependerá de la versión de Nextcloud y de las apps instaladas. Si se necesita descubrir los eventos disponibles, consultar la documentación de la app, o recurrir a su código fuente o a la documentación para desarrolladores de {vendor}`Nextcloud`.
:::

#### Sobre de la carga útil

Todo cuerpo HTTP POST de un webhook comparte la misma estructura de nivel superior:

```json
{
  "event": {},
  "user": { "uid": "alice", "displayName": "Alice" },
  "time": 1700100000
}
```

Donde:

- `"event"` es un objeto que contiene los datos específicos del evento **más** un campo `"class"`
  que contiene el nombre de clase PHP completamente cualificado (p. ej.,
  `"OCP\\Files\\Events\\Node\\NodeCreatedEvent"`).
- `"user"` es el usuario que disparó el evento (`null` cuando no existe ninguna sesión de usuario).
  Contiene `"uid"` (cadena) y `"displayName"` (cadena).
- `"time"` es una marca de tiempo Unix entera del momento en que se capturó el evento.

**Nota:** las cargas útiles de ejemplo que siguen se basan en cargas útiles HTTP POST reales de webhooks, con JSON y tipos de datos reales. El tipo de cada campo lo indica el tipo de su valor: por ejemplo, `"id": 123` es un entero, no una cadena.

#### Eventos de nodo (archivos/carpetas)

Los eventos de nodo incluyen los que actúan sobre un único nodo y los que actúan sobre dos nodos (como copiar, renombrar y restaurar). En los eventos de un solo nodo, el objeto `event` incluye un objeto `node`. En los eventos de dos nodos, incluye un objeto `source` y un objeto `target`. Los ejemplos siguientes muestran las cargas útiles **completas**.

**1. Eventos de un solo nodo**

Se aplica a:

- `OCP\Files\Events\Node\BeforeNodeCreatedEvent`
- `OCP\Files\Events\Node\BeforeNodeTouchedEvent`
- `OCP\Files\Events\Node\BeforeNodeWrittenEvent`
- `OCP\Files\Events\Node\BeforeNodeReadEvent`
- `OCP\Files\Events\Node\BeforeNodeDeletedEvent`
- `OCP\Files\Events\Node\NodeCreatedEvent`
- `OCP\Files\Events\Node\NodeTouchedEvent`
- `OCP\Files\Events\Node\NodeWrittenEvent`
- `OCP\Files\Events\Node\NodeDeletedEvent`

```json
{
  "event": {
    "class": "OCP\\Files\\Events\\Node\\NodeCreatedEvent",
    "node": {
      "id": 437,
      "path": "/admin/files/test-webhook.txt"
    }
  },
  "user": {
    "uid": "admin",
    "displayName": "Admin"
  },
  "time": 1700100000
}
```

Donde:

- `"event.class"` es el nombre de clase completamente cualificado del evento (cadena)
- `"event.node.id"` es un entero (ID único del nodo); puede faltar, consultar la nota siguiente
- `"event.node.path"` es una cadena (ruta del archivo o carpeta)

:::{note}
En algunos eventos (como `NodeDeletedEvent` o cuando el nodo se refiere a un archivo o carpeta inexistente), el objeto `node` puede no tener un campo `id`. Esto ocurre cuando el nodo ya no existe en el sistema de archivos o en la base de datos, y Nextcloud lo representa con un `NonExistingFile` o un `NonExistingFolder` internos. En esos casos, solo estará presente el campo `path`. Comprobar siempre la presencia del campo `id` en estas cargas útiles. Normalmente, puede usarse el evento `Before*` correspondiente (como `BeforeNodeDeletedEvent`) si se necesita el `id` del nodo antes de su eliminación.
:::

Ejemplo de carga útil de webhook de un nodo eliminado:

```json
{
  "event": {
    "class": "OCP\\Files\\Events\\Node\\NodeDeletedEvent",
    "node": {
      "path": "/user/files/oldfile.txt"
    }
  },
  "user": {
    "uid": "user",
    "displayName": "User"
  },
  "time": 1700100500
}
```

**2. Eventos de dos nodos**

Se aplica a:

- `OCP\Files\Events\Node\NodeCopiedEvent`
- `OCP\Files\Events\Node\NodeRenamedEvent`
- `OCP\Files\Events\Node\NodeRestoredEvent`
- `OCP\Files\Events\Node\BeforeNodeCopiedEvent`
- `OCP\Files\Events\Node\BeforeNodeRestoredEvent`
- `OCP\Files\Events\Node\BeforeNodeRenamedEvent`

```json
{
  "event": {
    "class": "OCP\\Files\\Events\\Node\\NodeRestoredEvent",
    "source": {
      "id": 399,
      "path": "/admin/files_trashbin/files/myfile.txt"
    },
    "target": {
      "id": 437,
      "path": "/admin/files/myfile.txt"
    }
  },
  "user": {
    "uid": "admin",
    "displayName": "Admin"
  },
  "time": 1700100000
}
```

Donde:

- `"source"` es un objeto que representa el nodo original, con `"id"` (entero) y `"path"` (cadena)
- `"target"` es un objeto que representa el nodo resultante/copiado/restaurado/renombrado, con `"id"` (entero) y `"path"` (cadena)

:::{note}
En algunos eventos de dos nodos, el nodo `source` o el `target` puede no tener un campo `id`, por ejemplo si el nodo se eliminó o falta por otro motivo en el sistema de archivos. Comprobar siempre la presencia del campo `id` en estos objetos. Normalmente, si se necesita el `id` de un nodo justo antes de su eliminación o cambio, el evento `Before*` respectivo (como `BeforeNodeRenamedEvent`) lo incluirá.
:::

Ejemplo de un evento de dos nodos (NodeRenamedEvent) en el que falta el nodo de origen:

```json
{
  "event": {
     "class": "OCP\\Files\\Events\\Node\\NodeRenamedEvent",
     "source": {
         "path": "/user/files/previousname.txt"
     },
     "target": {
         "id": 599,
         "path": "/user/files/newname.txt"
      }
    },
    "user": {
         "uid": "user",
         "displayName": "Joe User"
     },
     "time": 1700100000
 }
```

:::{note}
Solo estos campos están garantizados por el núcleo de Nextcloud. Pueden aparecer campos adicionales si los añaden plugins personalizados o versiones futuras.
:::

#### Eventos de etiquetas del sistema

- `OCP\SystemTag\TagAssignedEvent`
- `OCP\SystemTag\TagUnassignedEvent`

```json
{
    "event": {
        "class": "OCP\\SystemTag\\TagAssignedEvent",
        "objectType": "files",
        "objectIds": ["437", "438"],
        "tagIds": [3, 17]
    },
    "user": {
        "uid": "admin",
        "displayName": "Admin"
    },
    "time": 1700100000
}
```

#### Eventos de objetos de calendario

Los eventos de objetos de calendario usan dos formatos de carga útil distintos, según el evento.

**Carga útil estándar**

Se aplica a:

- `OCP\Calendar\Events\CalendarObjectCreatedEvent`
- `OCP\Calendar\Events\CalendarObjectDeletedEvent`
- `OCP\Calendar\Events\CalendarObjectMovedToTrashEvent`
- `OCP\Calendar\Events\CalendarObjectRestoredEvent`
- `OCP\Calendar\Events\CalendarObjectUpdatedEvent`

```json
{
  "event": {
    "class": "OCP\\Calendar\\Events\\CalendarObjectCreatedEvent",
    "calendarId": 9,
    "calendarData": {
      "id": 9,
      "uri": "work",
      "{http://calendarserver.org/ns/}getctag": "1736283",
      "{http://sabredav.org/ns}sync-token": 9651,
      "{urn:ietf:params:xml:ns:caldav}supported-calendar-component-set": "VEVENT,VTODO",
      "{urn:ietf:params:xml:ns:caldav}schedule-calendar-transp": "opaque"
    },
    "shares": [
      {
        "href": "mailto:alice@example.com",
        "commonName": "Alice",
        "status": 2,
        "readOnly": false,
        "{http://owncloud.org/ns}principal": "principal:users/alice",
        "{http://owncloud.org/ns}group-share": false
      }
    ],
    "objectData": {
      "id": 22,
      "uri": "event-20251111T100000Z.ics",
      "lastmodified": 1700099500,
      "etag": "19fa45b394",
      "calendarid": 9,
      "size": 4096,
      "component": "VEVENT",
      "classification": 0
    }
  },
  "user": {
    "uid": "david",
    "displayName": "David"
  },
  "time": 1700100000
}
```

**Carga útil distinta para los eventos de dos calendarios**

Se aplica a:

- `OCP\Calendar\Events\CalendarObjectMovedEvent`

```json
{
  "event": {
    "class": "OCP\\Calendar\\Events\\CalendarObjectMovedEvent",
    "sourceCalendarId": 9,
    "sourceCalendarData": {
      "id": 9,
      "uri": "work",
    },
    "targetCalendarId": 11,
    "targetCalendarData": {
      "id": 11,
      "uri": "meetings",
    },
    "sourceShares": [
      {
        "href": "mailto:alice@example.com",
        "commonName": "Alice"
      }
    ],
    "targetShares": [
      {
       "href": "mailto:bob@example.com",
       "commonName": "Bob"
      }
    ],
    "objectData": {
      "id": 22,
      "uri": "event-20251111T100000Z.ics"
    },
  },
  "user": {
    "uid": "david",
    "displayName": "David"
  },
  "time": 1700100000
}
```

#### Eventos de la app Formularios

Cuando está instalada la app opcional `forms`:

- `OCA\Forms\Events\FormSubmittedEvent`

```json
{
  "event": {
    "class": "OCA\\Forms\\Events\\FormSubmittedEvent",
    "form": {
      "id": 51,
      "hash": "abc123def456",
      "title": "Employee Feedback",
      "description": "Annual employee feedback form.",
      "ownerId": "alice",
      "fileId": 1002,
      "fileFormat": "pdf",
      "created": 1700001000,
      "access": 0,
      "expires": 1702606600,
      "isAnonymous": false,
      "submitMultiple": false,
      "showExpiration": true,
      "lastUpdated": 1700001200,
      "submissionMessage": null,
      "state": 1
    },
    "submission": {
      "id": 220,
      "formId": 51,
      "userId": "bob",
      "timestamp": 1700001234
    }
  },
  "user": {
    "uid": "bob",
    "displayName": "Bob"
  },
  "time": 1700001234,
}
```

#### Eventos de la app Tablas

Cuando está instalada la app opcional `tables`:

- `OCA\Tables\Event\RowAddedEvent`
- `OCA\Tables\Event\RowDeletedEvent`
- `OCA\Tables\Event\RowUpdatedEvent`

```json
{
  "event": {
    "class": "OCA\\Tables\\Event\\RowAddedEvent",
    "tableId": 34,
    "rowId": 7,
    "previousValues": null,
    "values": {
      "0": "Project X",
      "1": 2025,
      "2": "active"
    }
  },
  "user": {
    "uid": "carol",
    "displayName": "Carol"
  },
  "time": 1700054321,
}
```

:::{note}
Para filtrar o automatizar, comprobar siempre la carga útil que se recibe realmente, ya que coincide con los ejemplos JSON anteriores, no con el estilo de tipos de PHPDoc ni de los arrays internos de PHP.
:::
````
