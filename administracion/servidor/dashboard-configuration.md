---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Activar la app Dashboard y fijar con occ la disposición de widgets de un usuario, la predeterminada para todos y la app que se abre por defecto."
---
# App Dashboard

## Resumen

Esta página explica cómo activar la app Dashboard y cómo leer y establecer con `occ` la disposición de sus widgets, por usuario o para todos, además de cómo sustituir la app predeterminada. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_server/dashboard_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El Dashboard de Nextcloud es el punto de partida del día: ofrece a los usuarios una vista general de sus próximas citas, correos urgentes, mensajes de chat, tickets entrantes, últimos tweets ¡y mucho más! Los usuarios pueden agregar los widgets que prefieran y cambiar el fondo a su gusto.

### Activar la app Dashboard

La app Dashboard viene incluida y está activada de forma predeterminada. Si no está activada, basta con ir a la página Apps de Nextcloud para activarla.

### Configurar Nextcloud para la app Dashboard

Los widgets del Dashboard los proporcionan las apps y cada uno tiene un identificador único. Un administrador puede usarlo para personalizar la disposición predeterminada del Dashboard. La disposición se almacena como una lista de identificadores de widgets separados por comas.

La disposición de un usuario existente puede leerse con el siguiente comando:

```
occ user:setting admin dashboard layout
```

La disposición del Dashboard de un usuario concreto puede establecerse con el siguiente comando:

```
occ user:setting admin dashboard layout "calendar,files,activity"
```

La disposición predeterminada del Dashboard para todos los usuarios puede establecerse con el siguiente comando:

```
occ config:app:set dashboard layout --value="files,activity,calendar"
```

Cambiar la disposición predeterminada no afecta a los usuarios existentes que ya tienen almacenada una disposición personalizada.

Es posible sustituir la app predeterminada, que es la app Dashboard, por una app personalizada con el siguiente comando:

> occ config:app:set core defaultpage --value "/apps/files/extstoragemounts"
````
