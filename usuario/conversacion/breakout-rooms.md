---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Dividir una llamada de Talk en salas de grupos: cómo las configura un moderador, cómo se asignan los participantes y cómo se gestionan."
---
(nc-breakout-rooms)=
# Salas de grupos

## Resumen

Esta página explica a los moderadores de Talk cómo dividir una llamada en salas de grupos, asignar a los participantes y gestionar las salas desde la barra lateral.

````{upstream} user_manual/talk/breakout_rooms.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Las salas de grupos permiten dividir una llamada de Nextcloud Talk en grupos más pequeños para conversaciones más centradas. El moderador de la llamada puede crear varias salas de grupos y asignar participantes a cada sala.

:::{note}
Por ahora, las salas de grupos no están disponibles en las conversaciones a las que pueden unirse invitados (conversaciones públicas).
:::

### Configurar salas de grupos

Para crear salas de grupos hay que ser moderador en una conversación grupal. Hacer clic en el menú de la barra superior y luego en `Setup breakout rooms`.

Se abrirá un diálogo donde se puede indicar el número de salas que se quieren crear y el método de asignación de participantes.
Hay tres opciones:

- **Asignar participantes automáticamente**: Talk asignará automáticamente los participantes a las salas.
- **Asignar participantes manualmente**: se pasa por un editor de participantes donde se pueden asignar participantes a las salas.
- **Permitir a los participantes escoger**: los participantes podrán unirse por sí mismos a las salas de grupos.

### Gestionar salas de grupos

Una vez creadas las salas de grupos, se podrán ver en la barra lateral.

Desde la cabecera de la barra lateral se puede:

- **Iniciar y detener las salas de grupos**: esto moverá a todos los usuarios de la conversación principal a sus respectivas salas de grupos.
- **Difundir un mensaje a todas las salas**: esto enviará un mensaje a todas las salas al mismo tiempo.
- **Hacer cambios en los participantes asignados**: esto abrirá el editor de participantes, donde se puede cambiar qué participantes están asignados a cada sala de grupos. Desde este diálogo también es posible eliminar las salas de grupos.

Desde el elemento de la sala de grupos en la barra lateral también es posible unirse a una sala de grupos concreta o enviar un mensaje a una sala específica.
````
