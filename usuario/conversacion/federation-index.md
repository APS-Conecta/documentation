---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Conversaciones de Talk entre servidores federados: dónde está el CloudID, cómo se envía una invitación y cómo se acepta."
---
# Federación

## Resumen

Esta página explica a las personas usuarias de Talk cómo funcionan las conversaciones entre servidores federados: cómo invita un moderador a un participante de otro servidor y cómo se acepta la invitación.

````{upstream} user_manual/talk/federation_index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Con la función de federación, los usuarios pueden crear conversaciones entre distintas instancias de Talk federadas y usar las funciones de Talk como si estuvieran en el mismo servidor.

Esta función debe activarla un administrador del sistema.

### Enviar una invitación

Para recibir una invitación, la otra parte necesita el CloudID de quien la recibe, que es su identidad federada en las instancias de Nextcloud. El CloudID se encuentra en **Ajustes personales**, en **Compartir**, y tiene la forma `user@cloud.example.com`.

El moderador de la conversación puede enviar una invitación a un participante de otro servidor.

### Aceptar una invitación

Al recibir una notificación, el usuario ve un contador de invitaciones pendientes encima de la lista de conversaciones.

Al hacer clic en él, se muestra más información sobre quien invita, y el usuario puede aceptar o rechazar la invitación.

Al aceptar la invitación, la conversación aparece en la lista como cualquier otra.

Se puede usar para chatear con participantes de otros servidores federados, unirse a llamadas y usar otras funciones de Talk disponibles.
````
