---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Tipos de conversación de Talk, panel de Talk, crear, filtrar, archivar y gestionar conversaciones, vetar participantes, caducidad y notificaciones."
---
# Tipos y gestión de conversaciones

## Resumen

Esta página explica a las personas usuarias de Talk los tipos de conversación, el Panel de Talk y cómo crear, filtrar, archivar y gestionar conversaciones; a los moderadores, cómo vetar participantes y hacer caducar los mensajes; y a todos, cómo ajustar las notificaciones y la privacidad.

````{upstream} user_manual/talk/conversations.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los chats y las llamadas tienen lugar en conversaciones. Se puede crear cualquier número de conversaciones. Hay distintos tipos de conversaciones:

### 1. Conversaciones privadas (uno a uno)

Aquí se mantiene un chat o una llamada privados con otro usuario de Talk.

En la barra lateral de contenido se encuentra información adicional sobre la persona con la que se chatea, como su dirección de correo electrónico, su número de teléfono u otros datos que haya compartido en su perfil.

Nadie, excepto uno mismo y la otra persona, puede ver esta conversación ni unirse a una llamada en ella. Una llamada en curso se puede ampliar a una nueva conversación de grupo añadiendo a más personas. La llamada continúa allí sin interrupción.

Si un usuario deja de estar disponible y ha establecido un estado de **fuera de la oficina** en `Personal settings > Availability`, en esta conversación se encuentra información adicional, como la descripción proporcionada, la fecha de ausencia o la persona que lo sustituye.

### 2. Conversaciones de grupo

Una conversación de grupo puede tener cualquier número de personas. Se pueden añadir usuarios internos, invitados por correo electrónico, grupos o equipos a una conversación de grupo al crearla o, cuando ya existe, mediante la pestaña {guilabel}`Participantes`.

Una conversación de grupo se puede compartir con un enlace público para que los invitados puedan unirse a un chat y a una llamada. También se puede abrir a los usuarios registrados (o a los usuarios de la aplicación 'Guests'), para que puedan descubrir esta conversación y unirse a ella.

### 3. Nota personal

Es una conversación especial con uno mismo. Los mensajes de esta conversación no tienen límite para su edición o eliminación. Se puede usar para:

- **Tomar notas**: anotar ideas, recordatorios o información importante que se quiere tener a mano.
- **Crear listas de tareas**: usar la sintaxis Markdown para crear listas de comprobación de las tareas que hay que completar.
- **Reenviar mensajes de otro chat**: usar el menú del mensaje para reenviar mensajes importantes de otras conversaciones a la Nota personal.

### 4. Conversaciones temporales

Estas conversaciones cubren algunos casos especiales y existen durante un periodo de tiempo limitado. La administración de la instancia puede configurar el periodo de conservación:

- **Reuniones instantáneas**: estas conversaciones se pueden crear para reuniones rápidas e improvisadas. Se pueden iniciar al instante desde el Panel de Talk.
- **Conversaciones de eventos**: se crean cuando la aplicación Calendario las establece como lugar de un evento.
- **Conversaciones telefónicas**: están dedicadas a las llamadas telefónicas SIP de marcación entrante y saliente (requiere una pasarela SIP).
- **Verificación por video**: se crean cuando alguien intenta acceder a un enlace público protegido por contraseña con verificación por video (se eliminan inmediatamente cuando termina la llamada).

#### Panel de Talk

El Panel de Talk es el centro desde el que gestionar las conversaciones y acceder a ellas. Ofrece una vista general de:

- Las menciones y los mensajes sin leer en chats privados;
- Los recordatorios de mensajes, programados para atenderlos más tarde;
- Las reuniones programadas, con los detalles del evento y botones de acceso directo para unirse a ellas;
- Acciones de acceso directo para crear conversaciones nuevas, unirse a conversaciones abiertas o comprobar rápidamente los dispositivos multimedia.

#### Crear una conversación

Se puede crear un chat privado (uno a uno) buscando el nombre de un usuario, un grupo o un equipo y haciendo clic en él. Con un solo usuario, la conversación se crea de inmediato y se puede empezar a chatear. Con un grupo o un círculo, se eligen un nombre y unos ajustes antes de crear la conversación y añadir a los participantes.

Para crear una conversación de grupo personalizada, hacer clic en el botón situado junto al campo de búsqueda y al botón de filtros y, luego, en {guilabel}`Crear una conversación nueva`.

Después se puede elegir un nombre para la conversación, escribir una descripción y establecer un avatar para ella (con una foto subida o un emoji), y seleccionar si la conversación debe estar abierta a usuarios externos y si los demás usuarios del servidor pueden verla y unirse a ella.

En el segundo paso se añaden los participantes y se termina de crear la conversación.

Tras confirmar, se redirige a la nueva conversación y se puede empezar a comunicarse de inmediato.

#### Filtrar las conversaciones

Las conversaciones se pueden filtrar con el botón de filtro situado junto al campo de búsqueda. Hay varias opciones de filtrado:

1. **Menciones sin leer**: ver las conversaciones privadas sin leer, o las conversaciones de grupo en las que se ha mencionado a uno.
2. **Mensajes sin leer**: ver los mensajes sin leer de todas las conversaciones en las que se participa.
3. **Conversaciones de eventos**: ver todas las conversaciones creadas para eventos próximos o pasados.

Después se puede quitar el filtro desde el menú de filtros.

#### Archivar conversaciones

Se pueden archivar las conversaciones que ya no se necesita ver en la lista principal de conversaciones. Cuando una conversación se archiva, pasa a la sección {guilabel}`Conversaciones archivadas`. Una conversación archivada no aparece en la lista principal de conversaciones, pero sigue respetando el nivel de notificación establecido en sus ajustes.

La lista es accesible desde el botón situado en la parte inferior de la barra de navegación.

#### Gestionar una conversación

En una conversación nueva propia siempre se es moderador. En la lista de participantes se puede ascender a otros participantes a moderadores con el menú `...` situado a la derecha de su nombre de usuario, asignarles permisos personalizados o eliminarlos de la conversación.

Cambiar los permisos de un usuario que se unió a una conversación pública también lo añade de forma permanente a la conversación.

Los moderadores pueden configurar la conversación. Para acceder a los ajustes, seleccionar {guilabel}`Ajustes de la conversación` en el menú `...` de la conversación, en la parte superior.

Aquí se puede configurar la descripción, el acceso de invitados, si la conversación es visible para los demás usuarios del servidor y más.

#### Vetar participantes

Para ayudar a mantener las discusiones seguras y bajo control, los moderadores pueden vetar a participantes de las conversaciones. Esto se aplica por igual a usuarios internos e invitados; en el caso de los invitados, también se veta su dirección IP.

En la lista de participantes, seleccionar al usuario o invitado y hacer clic en {guilabel}`Eliminar participante`.

Ahí, marcar la casilla {guilabel}`También bloquear de esta conversación` e indicar un motivo para el veto. El usuario vetado se elimina de la conversación y no puede volver a unirse.

Más adelante, la lista de usuarios vetados se encuentra en la sección {guilabel}`Moderación` de los ajustes de la conversación. Ahí se puede ver el motivo del veto y revertirlo si es necesario.

#### Caducidad de los mensajes

Un moderador puede configurar la caducidad de los mensajes en {guilabel}`Ajustes de la conversación`, dentro de la sección {guilabel}`Moderación`. Cuando un mensaje alcanza su momento de caducidad, se elimina automáticamente de la conversación. Las duraciones de caducidad disponibles son 1 hora, 8 horas, 1 día, 1 semana, 4 semanas o nunca (que es el valor predeterminado).

#### Notificaciones y privacidad

De forma predeterminada, Nextcloud Talk avisa de:

- Los mensajes nuevos en conversaciones privadas;
- Las respuestas a los mensajes que se han enviado;
- Los mensajes que mencionan a uno o a un grupo o equipo del que se es miembro;
- Las llamadas iniciadas en las conversaciones en las que se participa.

Este comportamiento se puede cambiar en los ajustes de la conversación. Además, se puede configurar:

- **Conversaciones importantes**: siempre se recibe aviso de los mensajes nuevos, incluso en el modo «No molestar»;
- **Conversaciones sensibles**: el contenido de los mensajes no se muestra en la lista de conversaciones y se oculta en las notificaciones.

Para tener más control sobre la privacidad, también se puede configurar la visibilidad de los indicadores propios de escritura y de lectura en `Talk settings`.
````
