---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Servidor de calendario CalDAV: invitaciones, cumpleaños, recordatorios, FreeBusy, suscripciones, federación, papelera, salas, límites y retención de datos."
---
# Calendario / CalDAV

## Resumen

Esta página describe los ajustes y comandos `occ` del servidor de calendario CalDAV: invitaciones, calendario de cumpleaños, recordatorios, tipos de alarma, FreeBusy, suscripciones, calendarios compartidos federados, papelera, recursos y salas, límites de frecuencia, evento de ejemplo y retención de datos. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/groupware/calendar.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Ajustes del servidor de calendario

El servidor de calendario puede configurarse en la página de configuraciones de administración de Groupware. Puede desactivarse de forma global el envío de correos de invitación a eventos, la generación del calendario de cumpleaños integrado y el envío de notificaciones por correo electrónico sobre los próximos eventos.

:::{versionadded} 30.0.0 La sección se ocultará si ninguna app usa el backend de CalDAV.
:::

A partir de Nextcloud 30, la sección de ajustes del servidor de calendario se ocultará si ninguna app usa el backend de CalDAV. Para volver a mostrar la sección, instalar y activar una app adecuada, p. ej., [Calendario](https://apps.nextcloud.com/apps/calendar) o [Tareas](https://apps.nextcloud.com/apps/tasks).

### Eventos

Se puede personalizar la interfaz de usuario de los eventos.

#### Ocultar los botones de exportación

De forma predeterminada, los usuarios pueden exportar los datos de su calendario desde el editor de eventos. La administración puede desactivar esta función:

```
sudo -E -u www-data php occ config:app:set calendar hideEventExport --value=yes
```

### Invitaciones

Nextcloud puede enviar invitaciones a los asistentes de los eventos si esta opción está activada. Hay que asegurarse de haber configurado antes el servidor de correo electrónico, para que las invitaciones lleguen a su destino. Consultar {nc-doc}`admin_manual/configuration_server/email_configuration`.

También hay que asegurarse de que el ajuste «Enviar invitaciones a los asistentes» esté activado en la sección de groupware de las configuraciones de administración para que se envíen los correos.

La administración puede desactivar el envío de invitaciones a participantes externos con el siguiente comando:

```
sudo -E -u www-data php occ config:app:set dav caldav_external_attendees_disabled --value yes
```

Esto impide que se envíen invitaciones a asistentes de fuera de la instancia y oculta los contactos externos en la búsqueda de invitados.

### Calendario de cumpleaños

Los contactos que tienen rellenada la fecha de cumpleaños se añaden automáticamente como eventos a un calendario especial de cumpleaños. Si se desactiva esta opción, todos los usuarios dejarán de tener este calendario.

Al activar esta opción, los calendarios de cumpleaños de los usuarios no estarán disponibles de inmediato, porque debe generarlos una tarea en segundo plano. Consultar la sección de comandos DAV de {nc-doc}`admin_manual/occ_command`.

### Notificaciones de recordatorio

Nextcloud se encarga de enviar las notificaciones de los eventos.

Actualmente, Nextcloud gestiona dos tipos de notificaciones de recordatorio: las notificaciones integradas de Nextcloud y las notificaciones por correo electrónico. Para que se envíen los correos, hace falta un servidor de correo electrónico configurado. Consultar {nc-doc}`admin_manual/configuration_server/email_configuration`.

Hay que asegurarse de que «Enviar notificaciones de los eventos» y «Activar notificaciones push para eventos» estén activados en la sección de groupware de las configuraciones de administración para que esta función opere.

#### Trabajos en segundo plano

Ejecutar los trabajos en segundo plano puede ser una tarea costosa cuando hay un gran número de eventos, recordatorios, personas con quienes se comparten eventos y asistentes. Sin embargo, debe ocurrir con la frecuencia suficiente para que las notificaciones se envíen a tiempo. Para lograrlo, conviene usar un comando `occ` específico que se ejecute con más frecuencia que el sistema `cron` estándar:

```
# crontab -u www-data -e
*/5 * * * * php -f /var/www/nextcloud/occ dav:send-event-reminders
```

Consultar la sección de comandos DAV de {nc-doc}`admin_manual/occ_command`.

También hay que cambiar el modo de envío de `background-job` a `occ`:

```
sudo -E -u www-data php occ config:app:set dav sendEventRemindersMode --value occ
```

Si no se usa este comando específico, los recordatorios simplemente se enviarán en cuanto sea posible, cuando se ejecuten los trabajos en segundo plano.

### Tipos de alarma de los eventos

Nextcloud permite a los usuarios establecer recordatorios de los eventos por notificación y por correo electrónico. La administración puede imponer una de las dos opciones:

```
occ config:app:set calendar forceEventAlarmType --value=EMAIL
```

Los valores permitidos son `EMAIL` (correo electrónico) y `DISPLAY` (notificación).

:::{note}
Esto solo impone los tipos de alarma de los eventos creados con el Calendario de Nextcloud. Este ajuste no influye en otras aplicaciones conectadas.
:::

### FreeBusy

Con la sesión iniciada, Nextcloud puede devolver la información FreeBusy de todos los usuarios de la instancia, para saber cuándo están disponibles y así poder programar un evento en el momento adecuado. Si no se desea que los usuarios tengan esta capacidad, puede desactivarse FreeBusy para toda la instancia con el siguiente ajuste:

```
sudo -E -u www-data php occ config:app:set dav disableFreeBusy --value yes
```

### Suscripciones

#### Calendarios públicos personalizados

Además de los calendarios de días festivos, es posible definir un calendario propio. Estos calendarios funcionan igual que los de días festivos y pueden configurarse con el siguiente comando:

```
sudo -E -u www-data php occ config:app:set calendar publicCalendars --value '[{"name":"My custom calendar","source":"http://example.com/example.ics"}]'
```

El ajuste se especifica como una matriz JSON de objetos con las siguientes opciones:

- `name` - nombre del calendario en el listado
- `source` - URL del archivo ICS del calendario
- `displayName` - opcional, para sobrescribir el nombre del calendario suscrito
- `description` - opcional, descripción en el listado
- `authors` - opcional, derechos de autor y similares

#### Frecuencia de actualización

Las suscripciones de calendario se guardan en caché en el servidor y se actualizan periódicamente. Si el servidor del calendario indica un [intervalo de actualización](https://icalendar.org/New-Properties-for-iCalendar-RFC-7986/5-7-refresh-interval-property.html), se respeta. Si no, la frecuencia de actualización predeterminada es de un día.

Para establecer otra frecuencia de actualización predeterminada para los calendarios cuyo servidor no indica ninguna, cambiar la opción `calendarSubscriptionRefreshRate`:

```
sudo -E -u www-data php occ config:app:set dav calendarSubscriptionRefreshRate --value "PT6H"
```

Donde el valor es un [DateInterval](https://www.php.net/manual/dateinterval.construct.php); por ejemplo, con el comando anterior todos los calendarios de la instancia de Nextcloud se actualizarían cada 6 horas.

#### Permitir suscripciones en la red local

Por motivos de seguridad, Nextcloud prohíbe las suscripciones desde hosts de la red local. Si es necesario permitirlas, cambiar el siguiente parámetro a:

```
sudo -E -u www-data php occ config:app:set dav webcalAllowLocalAccess --value yes
```

### Calendarios compartidos federados

:::{versionadded} 32.0.0
:::

:::{versionchanged} 33.0.0 Los calendarios compartidos federados ahora son de lectura y escritura.
:::

Nextcloud admite crear calendarios compartidos federados. Un usuario puede compartir un calendario con un usuario remoto de una instancia federada. A partir de Nextcloud 33, los usuarios remotos pueden crear, editar y eliminar eventos dentro del calendario compartido. En Nextcloud 32, los calendarios compartidos eran de solo lectura.

La función puede desactivarse opcionalmente mediante una configuración de la app. Ejecutar el siguiente comando para desactivar la creación de nuevos calendarios compartidos federados para todos los usuarios:

```
sudo -E -u www-data php occ config:app:set dav enableCalendarFederation --type=bool --value=false
```

Tener en cuenta que los calendarios compartidos existentes se eliminarán al desactivar la función, ya que su sincronización fallaría.

### Papelera

Nextcloud admite una papelera para calendarios, eventos y tareas.

El plazo predeterminado antes de que los objetos se purguen de la papelera es de 30 días. Un trabajo en segundo plano se ejecuta cada 6 horas para limpiar los objetos caducados.

Para establecer otro periodo de retención, cambiar la opción `calendarRetentionObligation`:

```
sudo -E -u www-data php occ config:app:set dav calendarRetentionObligation --value=2592000
```

Donde el valor es el número de segundos del periodo. Establecer el valor en `0` desactiva la papelera.

### Recursos y salas

El backend de CalDAV de Nextcloud admite recursos y salas. Los recursos y las salas pueden reservarse para citas, y el sistema los programa de modo que no puedan usarse más de una vez al mismo tiempo. Esos recursos y salas debe proporcionarlos una app que aporte un backend para ello.

Una vez instalada una app de backend, normalmente esta permite a la administración, o incluso a los usuarios, definir los recursos, aunque eso depende de cada implementación concreta.

Nextcloud consulta periódicamente todos los backends registrados, por lo que los recursos y salas nuevos o actualizados aparecen con retraso.

#### Backends conocidos

- [Calendar Resource Management](https://github.com/nextcloud/calendar_resource_management): backend de base de datos con configuración por CLI para la administración

### Límites de frecuencia

Nextcloud limita la frecuencia de creación de calendarios y suscripciones si se crean demasiados elementos en un intervalo corto de tiempo. El valor predeterminado es de 10 calendarios o suscripciones por hora. Puede personalizarse de la siguiente manera:

```
# Set limit to 15 items per 30 minutes
sudo -E -u www-data php occ config:app:set dav rateLimitCalendarCreation --type=integer --value=15
sudo -E -u www-data php occ config:app:set dav rateLimitPeriodCalendarCreation --type=integer --value=1800
```

Además, el número máximo de calendarios y suscripciones que un usuario puede crear está limitado a 30 elementos. Esto también puede personalizarse:

```
# Allow users to create 50 calendars/subscriptions
sudo -E -u www-data php occ config:app:set dav maximumCalendarsSubscriptions --type=integer --value=50
```

o bien:

```
# Allow users to create calendars/subscriptions without restriction
sudo -E -u www-data php occ config:app:set dav maximumCalendarsSubscriptions --type=integer --value=-1
```

### Evento de ejemplo

:::{versionadded} 32.0.0
:::

Cuando un usuario inicia sesión por primera vez, se crea un evento de ejemplo en su calendario personal.

Esta función está activada de forma predeterminada y la controla la configuración de app `create_example_event`.

La administración puede desactivar la creación del evento de ejemplo. También es posible sustituir el evento predeterminado por uno personalizado.

Para desactivar la creación del evento de ejemplo para los usuarios nuevos:

1. Ir a los ajustes de Groupware en las configuraciones de administración.
2. Desplazarse hasta la sección «Contenido de ejemplo».
3. Desactivar el ajuste «Add example event ...» con la casilla de verificación

También puede activarse o desactivarse desde la línea de comandos:

```
sudo -E -u www-data php occ config:app:set dav create_example_event --value=no
```

Para sustituir el evento predeterminado integrado por uno personalizado:

1. Ir a los ajustes de Groupware en las configuraciones de administración.
2. Pulsar el botón «Importar evento del calendario».
3. Elegir un archivo ICS para importarlo.

:::{note}
Cuando se proporciona un evento personalizado, sus fechas de inicio y de fin se sobrescriben con fechas futuras para garantizar que el usuario vea el evento.
:::

También es posible volver al evento integrado predeterminado pulsando el botón «Restablecer a predeterminado», junto al botón de importación.

(nc-caldav-data-retention)=
### Retención de datos

:::{versionadded} 26.0.0
:::

Se puede configurar durante cuánto tiempo conserva Nextcloud algunos de los tokens de sincronización del calendario.

#### Tokens de sincronización

El backend de CalDAV registra cualquier modificación de los calendarios, es decir, todo lo que se añade, modifica o elimina. Estos datos se usan para la sincronización diferencial de clientes sin conexión como Thunderbird. A partir de cierto momento, los datos pueden considerarse obsoletos, suponiendo que ya no habrá ningún cliente que los necesite. Esto puede ayudar a mantener pequeña la tabla de base de datos *calendarchanges*:

```
sudo -E -u www-data php occ config:app:set totalNumberOfSyncTokensToKeep --value=30000
```

El valor predeterminado es conservar 10 000 entradas. Esta opción debe ajustarse de forma adecuada al número de usuarios. P. ej., en una instalación con 5000 calendarios sincronizados activos, el sistema solo conservaría una media de 10 cambios por calendario. Esto provocará una eliminación prematura de datos y problemas de sincronización.

:::{warning}
Este ajuste también influye en la {nc-ref}`retención de datos de CardDAV <carddav-data-retention>`.
:::
````
