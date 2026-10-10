---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API de AppAPI para que una ExApp registre y anule escuchas de eventos de Nextcloud: parámetros, carga útil del evento y subtipos de eventos de nodo."
---
(nc-dev-events_listener)=
# Escucha de eventos

## Resumen

Esta página describe la API con la que una ExApp escucha eventos de Nextcloud: cómo registrar y anular el registro de una escucha, la carga útil que llega de forma asíncrona y los subtipos de eventos de nodo admitidos. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/events_listener.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Esta API permite escuchar los {nc-ref}`eventos de Nextcloud <Events>`.

Actualmente solo se admite un número **limitado** de eventos.

Si hay algún evento específico al que convenga añadir soporte, se ruega comunicarlo a {vendor}`Nextcloud`.

:::{note}
A diferencia de los eventos de PHP, toda la información de los eventos llega a la ExApp de forma **asíncrona**, más bien como un sistema de notificaciones,
para no ralentizar el servidor.
:::

### Registrar

Endpoint OCS: `POST /apps/app_api/api/v1/events_listener`

#### Parámetros

```json
{
    "eventType": "node_event",
    "actionHandler": "/action_handler_route"
    "eventSubtypes": [],
}
```

:::{note}
`eventSubtypes` es un parámetro opcional; cuando no se especifica, todos los subtipos de evento se propagan a la ExApp.

La URL de `actionHandler` es relativa a la raíz de la ExApp; no se requiere la barra inicial.
:::

### Anular el registro

Endpoint OCS: `DELETE /apps/app_api/api/v1/events_listener`

#### Parámetros

Para anular el registro de un EventsListener, basta con indicar el *eventType* del EventsListener registrado:

```json
{
    "eventType": "node_event"
}
```

### Carga útil del evento

```json
{
    "event_type": "node_event",
    "event_subtype": "NodeCreatedEvent",
    "event_data": "associative array depending on `event_subtype`"
}
```

### Tipos de eventos

#### Eventos de nodo

`node_event` - eventos sobre los *Nodes* de archivos

Subtipos de evento admitidos:

- `NodeCreatedEvent`
- `NodeTouchedEvent`
- `NodeWrittenEvent`
- `NodeDeletedEvent`
- `NodeRenamedEvent`
- `NodeCopiedEvent`

En todos los eventos de nodo, `event_data` contiene una clave `target` con el mismo formato que en la {nc-ref}`carga útil de FileActionsMenu <node_info>`.

En `NodeCopiedEvent` y `NodeRenamedEvent` también hay una clave `source` con el mismo formato.
````
