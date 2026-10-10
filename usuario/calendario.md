---
tipo: guia
esqueleto: borrador
audiencia: usuario
apps: [gestion]
resumen: "Coordinar turnos, programas y comités del establecimiento con la aplicación Calendario."
---
(nc-calendar-app)=
# Calendario

## Resumen

La aplicación Calendar coordina turnos, programas y comités del establecimiento: eventos con asistentes, salas de video y vistas de día, semana, mes y agenda. Los sectores mantienen calendarios compartidos para visitas domiciliarias, talleres y turnos, con toda la agenda en la zona horaria de Chile continental.

## Secciones previstas

- Crear eventos
- Calendarios de sector
- Turnos y programas
- Huddles de sector

````{upstream} user_manual/groupware/calendar.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
La aplicación Calendario viene instalada de forma predeterminada con Nextcloud Hub, pero se puede deshabilitar. Consulte a su administrador.
:::

La aplicación Calendario de Nextcloud funciona con otras aplicaciones de calendarios con la que puede sincronizar sus calendarios y eventos de Nextcloud.

Cuando acceda por primera vez a la aplicación Calendario, un calendario inicial por defecto será creado para usted.

### Administrar sus calendarios

#### Crear un nuevo calendario

Si planea crear un nuevo calendario sin transferir previamente datos de su antiguo calendario, debería crear un nuevo calendario.

1. Pulse `+ Nuevo calendario` en la barra lateral izquierda.

2. Escriba el nombre para su nuevo calendario, por ejemplo "Trabajo", "Casa" o "Planificación de marketing".

3. Tras de pulsar el botón, su nuevo calendario se crea y se puede sincronizar entre sus dispositivos, añadir nuevos eventos y compartir con sus amigos y colegas.

#### Importar un calendario

Si quiere transferir su calendario y sus respectivos eventos a su instancia de Nextcloud, importarlo es la mejor manera de hacerlo.

1. Haga clic en el icono de **Configuración del calendario**.

2. Después de hacer clic en `Import Calendar`, que se encuentra en la sección `General`, puede seleccionar uno o más archivos de calendario de su dispositivo local para subirlos.

3. Seleccione un {guilabel}`Calendario en el cual importar`.

4. La subida puede tardar un tiempo y depende del tamaño del calendario que importe. Aparecerá una barra de progreso azul debajo de "Configuración del calendario".

:::{note}
La aplicación Calendario de Nextcloud solo admite archivos `.ics` compatibles con iCalendar, definidos en el RFC 5545.
:::

#### Importar un evento/añadir un evento .ics

Los eventos individuales suelen distribuirse como archivos `.ics` (a veces mediante un botón con la etiqueta "iCal", "Apple Calendar" u "Outlook"). Puede importarlos en el Calendario de Nextcloud con el mismo flujo de importación que un calendario completo.

1. Haga clic en el icono de **Configuración del calendario**.

2. Después de hacer clic en `Import calendar`, puede seleccionar uno o más archivos `.ics` de su dispositivo local para subirlos. Los archivos de un solo evento se añaden al calendario que seleccione.

3. Seleccione un {guilabel}`Calendario en el cual importar`.

4. La subida puede tardar un tiempo y depende del tamaño del calendario o evento que importe. Aparecerá una barra de progreso azul debajo de "Configuración del calendario".

:::{note}
La aplicación Calendario de Nextcloud solo admite archivos `.ics` compatibles con iCalendar, definidos en el RFC 5545.
:::

#### Editar, Exportar o Eliminar un Calendario

En ocasiones puede que quiera cambiar el color o el nombre de un calendario importado o creado previamente. También puede que quiera exportarlo a su disco duro local o borrarlo para siempre.

:::{note}
Tenga en cuenta que eliminar un calendario es una acción irreversible. Después de eliminarlo, no hay forma de restaurar el calendario a menos que tenga una copia de seguridad local.
:::

Haga clic en el icono del "lápiz" del calendario correspondiente. Verá una nueva ventana emergente que le permitirá cambiar el nombre y el color del calendario, y botones para eliminar o exportar el calendario.

#### Transparencia del calendario

Puede marcar o desmarcar la casilla "Nunca mostrarme como ocupado (establecer este calendario como transparente)" para determinar si los eventos de este calendario se tienen en cuenta en los cálculos de disponibilidad libre/ocupado. Si está marcada, no se tendrá en cuenta ningún evento de este calendario: su agenda aparecerá siempre libre, independientemente de la configuración de los eventos.

#### Compartir calendarios

Puede compartir su calendario con usuarios locales, grupos o usuarios remotos de servidores federados.

Los calendarios se pueden compartir con acceso de escritura o de solo lectura. Al compartir un calendario con acceso de escritura, los usuarios con quienes se comparte podrán crear eventos nuevos en el calendario, así como editar y eliminar los existentes.

:::{note}
Actualmente, los calendarios compartidos no se pueden aceptar ni rechazar. Si ya no quiere tener un calendario que alguien compartió con usted, puede hacer clic en el menú de tres puntos junto al calendario en la lista de calendarios y pulsar "Dejar de compartir conmigo". Para restaurar un recurso compartido, el calendario puede volver a compartirse, ya sea con todo el grupo, lo que restablece todas las acciones de dejar de compartir, o con un solo usuario.
:::

#### Delegación de calendarios

En los ajustes de la aplicación, puede delegar sus calendarios en otros usuarios para que los gestionen por usted. Puede conceder acceso de lectura si solo deben ver el calendario, o acceso de escritura si deben crear, editar y eliminar eventos.

La delegación de calendarios también funciona con otros clientes que admiten la delegación de calendarios.

#### Compartir calendarios federados

:::{versionadded} 32.0.0
:::

:::{versionchanged} 33.0.0 Los calendarios compartidos federados admiten acceso de lectura y escritura.
:::

Compartir un calendario con un usuario de otra instancia de Nextcloud funciona igual que compartirlo con un usuario local. La diferencia es que debe usar como destinatario el identificador de usuario federado, que tiene el formato `<username>@<instance>` (p. ej., `alice@cloud.example.com`).

A partir de Nextcloud 33, los calendarios compartidos federados admiten acceso completo de lectura y escritura, lo que permite a los usuarios remotos crear, editar y eliminar eventos en el calendario compartido. En Nextcloud 32, los calendarios compartidos federados eran de solo lectura.

#### Publicar un calendario

Los calendarios pueden ser publicados mediante un enlace público para hacerlos visibles (en modo solo lectura) a usuarios externos. Puede crear un enlace público a través del menú de compartir para un calendario y pulsando « + » al lado de « Compartir enlace ». Cuando lo haya creado, puede copiar el enlace público a su portapapeles o enviarlo por correo.

También hay un « código de inserción » que genera un iframe HTML para insertar su calendario en páginas públicas.

Se pueden compartir múltiples calendarios juntos, añadiendo su identificador único al final de un enlace de incrustación. Los identificadores individuales se pueden encontrar al final de cada enlace público a un calendario. La dirección completa se parecerá a `https://cloud.example.com/index.php/apps/calendar/embed/<token1>-<token2>-<token3>`

Para cambiar la vista o la fecha predeterminadas de un calendario insertado, debe proporcionar una URL con el formato `https://cloud.example.com/index.php/apps/calendar/embed/<token>/<view>/<date>`. En esta URL debe reemplazar las siguientes variables:

- `<token>` por el token del calendario,
- `<view>` por una de `dayGridMonth`, `timeGridWeek`, `timeGridDay`, `listMonth`, `listWeek`, `listDay`. La vista predeterminada es `dayGridMonth` y la lista que se usa normalmente es `listMonth`,
- `<date>` por `now` o por cualquier fecha con el formato `<year>-<month>-<day>` (p. ej., `2019-12-28`).

En la página pública, los usuarios pueden obtener el enlace para subscribirse al calendario y exportar el calendario completo directamente.

#### Widget de calendario

Puede insertar sus calendarios en aplicaciones compatibles como `Talk`, {guilabel}`Notas`, etc., ya sea compartiendo el enlace público para que el contenido insertado sea visible (en solo lectura) para todos los usuarios, o usando el enlace interno para que sea privado.

#### Suscribirse a un calendario

Usted puede suscribirse a calendarios iCal directamente desde su Nextcloud. Al soportar el estándar interoperable (RFC 5545) hemos hecho el calendario de Nextcloud compatible con Google Calendar, Apple iCloud y muchos otros servidores de calendario con los que puede intercambiar calendarios, incluyendo enlaces de suscripción a calendarios publicados en otras instancias Nextcloud, como se describe anteriormente.

1. Pulse {guilabel}`Nuevo calendario` en la barra lateral izquierda
2. Pulse {guilabel}`Nueva suscripción desde enlace (sólo lectura)`
3. Escriba o pegue el enlace del calendario compartido al que desea suscribirse.

Completado. Los calendarios a los que se suscriba se actualizarán regularmente.

:::{note}
De forma predeterminada, las suscripciones se actualizan cada semana. Es posible que su administrador haya cambiado este ajuste.
:::

#### Suscribirse a un calendario de días feriados

:::{versionadded} 4.4 Nextcloud 25 o posterior
:::

Puede suscribirse a un calendario de días feriados de sólo lectura provisto por [Thunderbird](https://www.thunderbird.net/calendar/holidays/).

1. Pulse {guilabel}`Nuevo calendario` en la barra lateral izquierda
2. Pulse `+ Add holiday calendar`
3. Busque su país o región y pulse {guilabel}`Suscribirse`

### Administrar eventos

#### Crear un nuevo evento

Los eventos pueden ser creados con un clic en el área donde está programado. En la vista de día y semana del calendario puede clicar y arrastrar sobre el área temporal en la que se realizará el evento.

Al pulsar el botón del globo terráqueo se abre el selector de zona horaria. Puede elegir zonas horarias distintas para el inicio y el fin de su evento. Esto es útil cuando viaja.

La vista mensual requiere solo un clic en el área del día correspondiente.

Después de eso, puede escribir el nombre del evento (p. ej., **Reunión con Linus**), elegir el calendario en el que desea guardar el evento (p. ej., **Personal**, **Eventos de la comunidad**), revisar y concretar el intervalo de tiempo o marcar el evento como evento de todo el día. Opcionalmente, puede especificar una ubicación y una descripción.

Si desea editar detalles avanzados como los **Asistentes** o los **Recordatorios**, o si desea marcar el evento como evento recurrente, pulse el botón {guilabel}`Más` para abrir el editor avanzado.

#### Añadir una conversación de Talk

Puede incluir una conversación de Talk existente en su evento pulsando "Añadir una conversación de Talk". Para ver la lista de conversaciones de Talk existentes, asegúrese de que la aplicación Talk esté habilitada. Si desea crear una nueva conversación de Talk, puede hacerlo directamente desde la misma ventana modal.

:::{note}
Si siempre quiere abrir el editor avanzado en lugar de la ventana emergente del editor de eventos simple, desmarque la opción `Enable simplified editor` en la sección {guilabel}`Ajustes` de la aplicación.
:::

Al hacer clic en el botón azul de `Guardar`, se creará el evento.

#### Editar, duplicar o eliminar un evento

Si quiere editar, duplicar o eliminar un evento específico, primero debe hacer clic en el evento.

Después de eso, podrá volver a establecer todos los detalles del evento y abrir el editor avanzado pulsando {guilabel}`Más`.

Al pulsar el botón {guilabel}`Actualizar` se actualizará el evento. Para cancelar los cambios, pulse el botón **Cerrar** de la ventana emergente o del editor avanzado.

Si abre la vista avanzada y pulsa el menú de tres puntos junto al nombre del evento, tiene la opción de exportar el evento como archivo `.ics` o de eliminarlo de su calendario.

:::{tip}
Si elimina eventos, irán a su {nc-ref}`papelera <calendar-trash-bin>`. Allí puede restaurar los eventos eliminados por accidente.
:::

Puede también exportar, duplicar o eliminar un evento desde el editor básico.

(nc-calendar-attendees)=
#### Invitar a asistentes a un evento

Es posible añadir asistentes a un evento y notificarles directamente. Recibirán una invitación por correo electrónico en la que podrán confirmar o cancelar su invitación al evento. Los asistentes pueden ser otros usuarios en su instancia de Nextcloud, contactos de su agenda y direcciones de correo electrónico. También es posible ajustar manualmente el nivel de participación de cada asistente, o deshabilitar la confirmación por correo para asistentes concretos.

:::{versionchanged} 25.0.0
Los enlaces de respuesta de correo electrónico de los asistentes ya no ofrecen entradas para agregar un comentario o invitar a más invitados al evento.
:::

:::{tip}
Al añadir a otros usuarios de Nextcloud como asistentes a un evento, puede acceder a su información de libre/ocupado, si está disponible, lo que le ayuda a determinar cuál es el mejor intervalo de tiempo para su evento. Configure su {nc-ref}`horario laboral <calendar-working-hours>` para que otras personas sepan cuándo está disponible. La información de libre/ocupado solo está disponible para otros usuarios de la misma instancia de Nextcloud.
:::

:::{attention}
La administración del servidor debe configurar el servidor de correo electrónico en la pestaña {guilabel}`Ajustes básicos`, ya que este correo se usará para enviar las invitaciones.
:::

Leyenda del estado de la invitación (como asistente):

- **Evento relleno**: aceptó
- **Tachado**: rechazó
- **Rayas**: tentativo
- **Evento vacío**: aún no ha respondido

Si usted es el organizador y todos sus asistentes rechazaron la invitación, el evento aparecerá vacío con un símbolo de advertencia.

#### Comprobar los horarios ocupados de los asistentes

Después de añadir asistentes a un evento, puede pulsar {guilabel}`Buscar una hora` para abrir la ventana modal "Libre / Ocupado". Esta le permite ver cuándo tiene otros eventos cada asistente y puede ayudarle a decidir una hora en la que todos estén libres.

Sus propios bloques ocupados se mostrarán del mismo color que su calendario personal, sus periodos de ausencia se mostrarán en gris y los horarios ocupados de los demás asistentes tendrán el mismo color que su avatar mostrado en el editor avanzado.

Puede seleccionar un intervalo de tiempo para el evento directamente en el calendario.

#### Asignar salas y recursos a un evento

De forma similar a los asistentes, usted puede añadir salas y recursos a sus eventos. El sistema se encargará de que cada sala y recurso quede reservada sin conflicto. La primera vez que un usuario añada una sala o recurso a un evento, se mostrará como aceptada. Cualquier otro evento que se solape mostrará la sala o el evento como rechazado.

:::{note}
Las salas y los recursos no los gestiona Nextcloud en sí, y la aplicación Calendario no le permitirá añadir ni cambiar un recurso. Su administrador debe instalar y, posiblemente, configurar los backends de recursos antes de que pueda usarlos como usuario.
:::

#### Disponibilidad de salas

:::{versionadded} 5.0 Nextcloud 30 o posterior
:::

Si la aplicación "Calendar Rooms and Resources" está instalada en su instancia, ahora puede encontrar `Room availability` en la sección {guilabel}`Recursos`. Allí se listan todas las salas existentes. Puede comprobar la disponibilidad de cada sala de forma similar a como comprueba el estado libre/ocupado de los asistentes a un evento.

#### Añadir adjuntos a los eventos

Puede importar adjuntos a sus eventos bien sea cargándolos o añadiéndolos desde archivos

:::{note}
Los adjuntos se pueden añadir al crear eventos nuevos o al editar eventos existentes. De forma predeterminada, los archivos recién subidos se guardarán en Archivos, en la carpeta del calendario del directorio raíz.
:::

Puede cambiar la carpeta de adjuntos en **Configuración del calendario**, cambiando `default attachments location`.

#### Configurar recordatorios

Puede configurar recordatorios para recibir una notificación antes de que empiece un evento. Actualmente están disponibles los siguientes métodos de notificación:

- Notificaciones por correo electrónico
- Notificaciones de Nextcloud

Puede establecer recordatorios en un momento relativo al evento o en una fecha concreta. Si desea que todos los eventos de un calendario tengan un recordatorio predeterminado, puede configurarlo en los ajustes de ese calendario.

:::{note}
Solo el propietario del calendario y las personas o grupos con quienes se comparte el calendario con acceso de escritura recibirán notificaciones. Si no recibe ninguna notificación pero cree que debería recibirlas, es posible que su administrador también las haya deshabilitado en su servidor.
:::

:::{note}
Si sincroniza su calendario con dispositivos móviles u otros clientes de terceros, es posible que las notificaciones también aparezcan allí.
:::

#### Añadir eventos recurrentes

Un evento se puede marcar como "recurrente", de manera que puede repetirse cada día, semana, mes o año. Existen reglas configurables para marcar el día de la semana en el que sucede el evento y reglas más complejas, como "el cuarto miércoles de cada mes".

También puede marcar una fecha límite para las repeticiones de evento.

(nc-calendar-trash-bin)=
#### Papelera

Si elimina eventos, tareas o un calendario en Calendario, sus datos no están perdidos para siempre. Estos elementos son acumulados en una *papelera*. Esto le ofrece una oportunidad de deshacer la eliminación. Después de un período de tiempo que por defecto dura 30 días (su administrador puede haber cambiado este ajuste), estos elementos serán eliminados permanentemente. También puede eliminar elementos permanentemente en cualquier momento, si así lo desea.

El botón `Vaciar papelera` eliminará todos los contenidos de la papelera en un solo paso.

:::{tip}
Solo se puede acceder a la papelera desde la aplicación Calendario. Ninguna aplicación o app conectada podrá mostrar su contenido. Sin embargo, los eventos, tareas y calendarios eliminados en aplicaciones o apps conectadas también terminarán en la papelera.
:::

(nc-calendar-working-hours)=
#### Estado de usuario automático

Cuando tenga programado un evento de calendario con el estado "BUSY", su estado de usuario se establecerá automáticamente en "En una reunión", a menos que se haya establecido como "No molestar" o "Invisible". Puede sobrescribir el estado con un mensaje personalizado en cualquier momento, o establecer sus eventos de calendario como "FREE". Los calendarios transparentes se ignorarán.

### Responder a invitaciones

Puede responder directamente a invitaciones desde la aplicación. Pulse en un evento y seleccione su estado de participación. Puede responder a una invitación aceptándola, rechazándola o aceptándola tentativamente.

También puede responder a una invitación desde el editor avanzado.

### Disponibilidad (Horario Laboral)

Su disponibilidad general, independientemente de los eventos que tenga programados, puede ser configurada en los ajustes de groupware de Nextcloud. Estos ajustes se verán reflejados en la vista disponible-ocupado cuando {nc-ref}`programe una reunión con otras personas <calendar-attendees>` en Calendario. Algunos clientes conectados como Thunderbird también mostrarán estos datos.

Puede configurar ausencias puntuales, además de su disponibilidad habitual, en la {nc-ref}`sección de ajustes de Ausencia <groupware-absence>`.

### Calendario de cumpleaños

El calendario de cumpleaños es un calendario generado automáticamente, que compila los cumpleaños de los contactos en su agenda. La única manera de editar este calendario es indicar la fecha de cumpleaños de sus contactos. No es posible realizar cambios a este calendario desde la aplicación calendario.

:::{note}
Si no ve el calendario de cumpleaños, es posible que su administrador lo haya deshabilitado en su servidor.
:::

### Citas

A partir de la versión 3 de Calendario, la aplicación puede generar huecos para citas, que otros usuarios pueden reservar, incluso aunque no tengan cuenta de Nextcloud. Las citas ofrecen un control granular sobre cuándo estará disponible para reunirse. Esto puede eliminar la necesidad de intercambiar correos para acordar un día y hora.

En esta sección usaremos el término *organizador* para la persona propietaria del calendario que configura los huecos de citas. El *asistente* es la persona que reserva uno de estos huecos.

#### Crear una configuración de citas

Como organizador de citas, acceda a través de la interfaz web de Calendario. En la barra lateral izquierda encontrará una sección de citas, donde puede abrir un diálogo para crear una nueva.

Una de las informaciones básicas de cualquier cita es un título describiendo de que se trata la misma (p.ej. "Llamada personal con...", cuando un organizador quiere ofrecer a sus colegas una llamada personal), dónde tendrá lugar la cita y una descripción más detallada de lo que se tratará la misma.

La duración de una cita puede escojerse de una lista predefinida. A continuación, puede seleccionar el incremento deseado. El incremento es la tasa a la que diferentes espacios estarán disponibles. Por ejemplo, puede tener espacios de una hora, pero ud. las facilita en incrementos de 30 minutos para que un asistente pueda agendar a las 9:00am pero también a las 9:30am. La información opcional sobre ubicación y descripción le dan a los asistentes un poco más de contexto. Cada cita agendada será escrita en uno de sus calendarios, así que puede escoger a cual de ellos debería ser. Las citas pueden ser "públicas" o "privadas". Las citas públicas pueden ser descubiertas mediante la página del perfil público de un usuario de Nextcloud. Las citas privadas solo serán accesibles por las personas que reciban el URL secreto de la misma.

:::{note}
Solo se mostrarán a los asistentes los huecos que no entren en conflicto con eventos existentes en sus calendarios.
:::

El organizador de una cita puede especificar los días y horas de la semana en los que es posible reservar un hueco. Se puede marcar como disponible las horas de trabajo, pero también cualquier otro horario personalizado.

Algunas citas requieren tiempo para su preparación. p. ej. cuando debe encontrarse en un evento y necesita hacer el tiempo para manejar hasta el mismo. El organizador puede decidir si seleccionar una duración de tiempo que debe estar libre. Solo estarán disponibles los espacios que no hagan conflicto con otros eventos durante el tiempo de preparación. Asimismo, existe la opción de seleccionar un tiempo después de cada cita que debe estar libre. Para evitar que un asistente agende en una ventana de tiempo muy corta antes de la cita es posible configurar que tan pronto la próxima cita puede ser agendada. Configurar un número máximo de espacios por día puede limitar cuantas citas les es posible agendar a los asistentes.

La cita configurada será entonces listada en la barra lateral izquierda. Usando el menú de tres puntos, puede ver una vista previa de la cita. Puede copiar el enlace a la cita y compartirlo con sus asistentes objetivo, o permitirles que descubran su cita pública navegando a la página del perfil. Puede también editar o eliminar la configuración de la cita.

#### Reservar una cita

La página de reserva muestra a los asistentes el título, ubicación, descripción y duración de una cita. Al seleccionar un día concreto se mostrará una lista con las posibles horas de inicio. Si se seleccionan días donde no haya huecos disponibles o en los que se haya alcanzado el límite de reservas, la lista puede estar vacía.

Para agendar una cita, Los usuarios deben introducir un nombre y dirección de correo electrónico. También pueden introducir un comentario de manera opcional.

Cuando se agenda de manera exitosa, un diálogo de confirmación se mostrará al asistente.

Para verificar que la dirección de correo electrónico de un asistente es válida, se le enviará un correo electrónico de confirmación.

La agenda de la cita sólo se aceptará después de que el asistente haga clic en el enlace de confirmación recibido a través del correo electrónico y esta confirmación será reenviada al organizador.

El asistente recibirá entonces otro correo electrónico confirmando los detalles de su cita.

:::{note}
Si un hueco no se ha confirmado, seguirá apareciendo como reservable. Hasta entonces, otro usuario que confirme su reserva antes también podría reservar ese hueco. El sistema detectará el conflicto y ofrecerá elegir un hueco nuevo.
:::

#### Gestionar la cita reservada

Una vez que se termina de agendar, el organizador encontrará un evento en su calendario con los detalles de la cita y la {nc-ref}`asistente <calendar-attendees>`.

Si la cita tiene la configuración "Añadir tiempo antes del evento" ó "Añadir tiempo después del evento" habilitada, se mostrarán como eventos separados en el calendario para el organizador.

Como en cualquier otro evento con asistentes, los cambios y cancelaciones estas causarán que se envíe un correo electrónico de notificación a los mismos.

Si los asistentes desean cancelar la cita, tienen que ponerse en contacto con el organizador, para que el organizador cancele o incluso elimine el evento.

#### Crear sala de Talk para las citas agendadas

Puede crear una sala de Talk directamente desde la app de Calendario para una cita agendada. La opción puede ubicarse en el modal de 'Crear cita'. Un enlace único se generará para cada cita agendada y se enviará a través del correo de confirmación cuando marque esta opción.

### Propuestas

:::{versionadded} 6.0 Nextcloud 32 o posterior
:::

Encontrar una hora de reunión para un grupo de participantes puede ser complicado. A partir de Calendario v6 se introdujo una nueva función que permite a los usuarios crear propuestas de horarios de reunión. Esto significa que, en lugar de solo reservar una hora o buscar una hora disponible en la vista libre/ocupado, los participantes pueden votar entre un conjunto de horas propuestas para una reunión. Luego, el organizador puede revisar las preferencias de los participantes y elegir la hora más adecuada para la reunión.

#### Gestionar propuestas

La lista de propuestas de la barra lateral izquierda muestra todas las propuestas que ha creado el usuario. La lista muestra el título de la propuesta, el número de participantes que han respondido y un estado que indica si todos los participantes han respondido.

El usuario puede pulsar el menú de tres puntos junto a un elemento de propuesta para editar, eliminar o ver una propuesta existente.

#### Crear una propuesta

Para crear una propuesta nueva, el usuario puede pulsar el icono de suma junto al encabezado "Propuestas de reunión", en la parte superior de la lista de propuestas. Esto abrirá una ventana modal en la que el usuario puede introducir todos los detalles relevantes de la reunión propuesta.

El editor de propuestas tiene algunos campos básicos similares a los del editor de eventos, como el título, la descripción, la ubicación, la duración y la selección de participantes, que el usuario puede rellenar. Estos detalles se usan luego para informar a los participantes sobre la reunión propuesta y sus horas.

La diferencia clave es la selección "Horas propuestas", en la que el usuario puede seleccionar varios intervalos de tiempo para una reunión. El usuario puede añadir tantos intervalos de tiempo como quiera, y cada uno se puede editar o eliminar según sea necesario.

Una vez que el usuario ha rellenado todos los detalles obligatorios (título, duración y participantes) y ha seleccionado las horas propuestas, puede pulsar el botón "Crear" para crear la propuesta. Esto guardará la propuesta y enviará notificaciones a todos los participantes seleccionados.

#### Editar una propuesta

Un usuario puede editar una propuesta existente pulsando el menú de tres puntos junto a un elemento de propuesta en la lista de propuestas y seleccionando "Editar". Esto abrirá la misma ventana modal que al crear una propuesta nueva, pero con todos los detalles existentes ya rellenados.

Después de hacer los cambios necesarios, el usuario puede pulsar el botón "Actualizar" para guardar los cambios. Esto también enviará notificaciones a todos los participantes sobre la propuesta actualizada.

#### Ver el progreso de una propuesta

Los usuarios pueden ver el progreso de una propuesta pulsando el elemento de propuesta en la lista de propuestas o pulsando "Vista" en el menú de tres puntos. Esto abrirá una vista detallada de la propuesta, con todos los detalles y una matriz de horas y participantes que muestra todas las horas propuestas y las respuestas de los participantes.

En esta vista, el usuario puede ver qué participantes han respondido a la propuesta y sus preferencias para cada hora propuesta. El usuario también puede ver el número total de votos de cada hora propuesta, lo que puede ayudarle a decidir la mejor hora para la reunión.

Una vez revisadas las respuestas de los participantes, el usuario puede seleccionar la hora más popular para la reunión pulsando el botón "Crear" al final de la matriz de fechas y participantes. Esto creará un nuevo evento en el calendario del usuario y enviará notificaciones a todos los participantes sobre la hora de reunión confirmada.

#### Notificaciones de una reunión propuesta

Los usuarios recibirán notificaciones por correo electrónico de varios sucesos relacionados con una reunión propuesta, entre ellos:

- Cuando se crea una propuesta nueva
- Cuando se actualiza una propuesta
- Cuando se elimina una propuesta
- Cuando se confirma la hora definitiva de la reunión

Estas notificaciones ayudan a que todos los participantes se mantengan informados e involucrados durante todo el proceso de propuesta.

Los correos de notificación contienen los detalles básicos de la reunión propuesta, como el título, la descripción, la ubicación, la duración y las horas propuestas. También incluyen un enlace a la página de respuesta, donde los participantes pueden ver todos los detalles y responder a las horas propuestas.

#### Responder a una reunión propuesta

Los participantes pueden responder a una reunión propuesta pulsando el enlace del correo de notificación. Esto abrirá la vista detallada de la reunión propuesta, donde pueden ver todas las horas propuestas y a los demás participantes con sus respuestas, y seleccionar su disponibilidad o sus preferencias para cada hora propuesta.

Los participantes pueden seleccionar su disponibilidad para cada hora propuesta eligiendo su preferencia en la línea correspondiente de la matriz de horas y participantes. Pueden elegir entre tres opciones: "Sí", "No" o "Quizás". Una vez hechas sus selecciones, pueden pulsar el botón "Enviar" para guardar sus respuestas.
````
