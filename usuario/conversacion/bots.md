---
tipo: referencia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Qué hacen los bots de Talk, algunos ejemplos disponibles y dónde está la lista completa; los comandos se eliminaron en favor de los bots."
---
# Bots y comandos

## Resumen

Esta página describe qué hacen los bots en los chats de Talk, con algunos ejemplos, y los antiguos comandos, que se eliminaron en favor de los bots. Está dirigida a quienes usan los chats de Talk.

````{upstream} user_manual/talk/bots.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Bots

Los bots pueden responder a mensajes del chat, dar respuestas automáticas e integrarse con servicios externos. El administrador puede habilitar bots en la instancia de Talk.

Algunos ejemplos de bots disponibles:

- **Call summary** — Publica un mensaje de resumen al terminar una llamada, con la lista de todos los participantes y un esbozo de las tareas que se hayan mencionado.
- **Agenda bot** — Ayuda a gestionar las agendas de las reuniones con control del tiempo y control de acceso basado en permisos.
- **Roll a dice** — Escribir `/roll` en una conversación para tirar dados.

La lista completa de bots disponibles y las instrucciones de instalación están en la [documentación de administración de Talk](https://nextcloud-talk.readthedocs.io/en/latest/bot-list/).

### Comandos

:::{warning}
Los comandos se eliminaron en favor de los bots.
:::

Nextcloud permite a los usuarios ejecutar acciones mediante comandos. Un comando suele tener este aspecto:

> `/wiki airplanes`

Los administradores pueden configurar, habilitar y deshabilitar comandos. Los usuarios pueden usar el comando `help` para averiguar qué comandos están disponibles.

> `/help`
````
