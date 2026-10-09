---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Comandos occ de DAV (libretas, calendarios, suscripciones, ausencias) y de base de datos (índices, columnas, esquema y conversiones)."
---
# Comandos de DAV y de base de datos

## Resumen

Esta página es la referencia de los comandos `occ` que gestionan libretas de direcciones, calendarios, suscripciones de calendario y ausencias (`dav`, `calendar`) y de los que mantienen, inspeccionan y convierten la base de datos (`db`), con ejemplos y su salida. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/occ_database.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
(nc-dav_label)=
### Comandos de DAV

Los comandos `dav` gestionan libretas de direcciones, calendarios, suscripciones de calendario, ausencias y datos relacionados:

```
dav
 dav:absence:get                 get the out-of-office absence settings for a user
 dav:absence:set                 set the out-of-office absence settings for a user
 dav:clear-calendar-unshares     clear calendar unshares for a user
 dav:clear-contacts-photo-cache  clear cached contact photos
 dav:create-addressbook          create a dav addressbook
 dav:create-calendar             create a dav calendar
 dav:create-subscription         create a dav subscription
 dav:delete-calendar             delete a dav calendar
 dav:delete-subscription         delete a calendar subscription for a user
 dav:fix-missing-caldav-changes  insert missing calendarchanges rows for existing events
 dav:list-addressbooks           list all addressbooks of a user
 dav:list-calendar-shares        list all calendar shares for a user
 dav:list-calendars              list all calendars of a user
 dav:list-subscriptions          list all calendar subscriptions for a user
 dav:move-calendar               move a calendar from one user to another
 dav:remove-invalid-shares       remove invalid dav shares
 dav:retention:clean-up          delete CalDAV trash elements that are due for removal
 dav:send-event-reminders        send event reminder notifications
 dav:sync-birthday-calendar      synchronize the birthday calendar
 dav:sync-system-addressbook     synchronize users to the system addressbook
calendar
 calendar:export                 export a calendar of a user
 calendar:import                 import a calendar to a user
```

#### Gestión de libretas de direcciones

##### dav:list-addressbooks

Listar todas las libretas de direcciones de un usuario:

```
sudo -E -u www-data php occ dav:list-addressbooks layla
+-------------+----------+-----------------------------+-------------------+----------+
| Database ID | URI      | Owner principal             | Owner displayname | Writable |
+-------------+----------+-----------------------------+-------------------+----------+
| contacts    | Contacts | principals/users/layla      | Layla Smith       |  ✓       |
+-------------+----------+-----------------------------+-------------------+----------+
```

##### dav:create-addressbook

Crear una libreta de direcciones para un usuario:

```
sudo -E -u www-data php occ dav:create-addressbook layla work
```

#### Gestión de calendarios

##### dav:list-calendars

Listar todos los calendarios de un usuario:

```
sudo -E -u www-data php occ dav:list-calendars layla
+----------+-------------+-----------------------------+-------------------+----------+
| URI      | Displayname | Owner principal             | Owner displayname | Writable |
+----------+-------------+-----------------------------+-------------------+----------+
| personal | Personal    | principals/users/layla      | Layla Smith       |  ✓       |
+----------+-------------+-----------------------------+-------------------+----------+
```

##### dav:list-calendar-shares

Listar todas las comparticiones de calendario de un usuario:

```
sudo -E -u www-data php occ dav:list-calendar-shares layla
  User layla has no calendar shares
```

Usar `--calendar-id` para limitar los resultados a un calendario concreto.

##### dav:create-calendar

Crear un calendario para un usuario:

```
sudo -E -u www-data php occ dav:create-calendar layla holidays
```

##### dav:delete-calendar

Eliminar un calendario de un usuario indicando su nombre:

```
sudo -E -u www-data php occ dav:delete-calendar layla holidays
```

Usar `--birthday` para eliminar el calendario de cumpleaños en lugar de indicar un nombre. Usar `-f` / `--force` para eliminarlo de inmediato en lugar de moverlo a la papelera:

```
sudo -E -u www-data php occ dav:delete-calendar --force layla holidays
sudo -E -u www-data php occ dav:delete-calendar --birthday layla
```

##### dav:move-calendar

:::{note}
Mover un calendario cambia sus URL de compartición existentes.
:::

Mover un calendario de un usuario a otro:

```
sudo -E -u www-data php occ dav:move-calendar personal layla fred
```

Sin `--force`, el comando falla si el usuario de destino ya tiene un calendario con el mismo nombre o si el calendario está compartido con un grupo del que el usuario de destino no es miembro.

Usar `-f` / `--force` para continuar de todos modos: las comparticiones con grupos en conflicto se descartan y, si el nombre del calendario ya está ocupado en el destino, se prueba automáticamente un nombre nuevo (`personal-1`, `personal-2`, hasta diez intentos). El comando falla si no encuentra un nombre libre en esos intentos.

##### dav:clear-calendar-unshares

Borrar los registros obsoletos de comparticiones de calendario anuladas de un usuario. Es útil cuando el estado de compartición de los calendarios de un usuario ha quedado incoherente:

```
sudo -E -u www-data php occ dav:clear-calendar-unshares layla
  User layla has no calendar unshares
```

#### Gestión de suscripciones de calendario

##### dav:list-subscriptions

Listar todas las suscripciones de calendario de un usuario:

```
sudo -E -u www-data php occ dav:list-subscriptions layla
  User layla has no subscriptions
```

##### dav:create-subscription

Crear un calendario de suscripción para un usuario:

```
sudo -E -u www-data php occ dav:create-subscription layla "Astronomy Calendar" \
  webcal://cantonbecker.com/astronomy-calendar/astrocal.ics
```

Opcionalmente, indicar un código de color HEX para el calendario:

```
sudo -E -u www-data php occ dav:create-subscription layla "Astronomy Calendar" \
  webcal://cantonbecker.com/astronomy-calendar/astrocal.ics "#ff5733"
```

Si no se indica, se usa el color predeterminado del tema.

##### dav:delete-subscription

Eliminar una suscripción de calendario de un usuario:

```
sudo -E -u www-data php occ dav:delete-subscription layla "Astronomy Calendar"
```

#### Gestión de ausencias (fuera de la oficina)

##### dav:absence:set

Establecer la ausencia (fuera de la oficina) de un usuario. `first-day` y `last-day` son inclusivos y tienen el formato `YYYY-MM-DD`.

- **short-message**: un breve mensaje de una línea que se muestra como estado del usuario junto a su nombre en toda la interfaz mientras está ausente (p. ej., en contactos, chat y listas de usuarios).
- **message**: el texto completo de fuera de la oficina que se muestra a los usuarios que intentan contactar con el usuario ausente.
- **replacement-user-id**: opcional; un colega al que contactar en su lugar. Su nombre mostrado se guarda junto con la ausencia y se muestra a los demás.

```
sudo -E -u www-data php occ dav:absence:set layla 2026-05-01 2026-05-15 \
  "On leave" \
  "I am on leave until May 15. For urgent matters please contact my colleague."
```

Para establecer una ausencia con un usuario sustituto:

```
sudo -E -u www-data php occ dav:absence:set layla 2026-05-01 2026-05-15 \
  "On leave" \
  "I am on leave. Please contact fred for urgent matters." \
  fred
```

##### dav:absence:get

Mostrar los ajustes de ausencia actuales de un usuario:

```
sudo -E -u www-data php occ dav:absence:get layla
  Start day: 2026-05-01
  End day: 2026-05-15
  Short message: On leave
  Message: I am on leave until May 15. For urgent matters please contact my colleague.
  Replacement user: none
  Replacement display name: none
```

#### Sincronización

##### dav:sync-system-addressbook

(nc-dav-sync-system-address-book)=
Sincronizar todos los usuarios con la {nc-ref}`libreta de direcciones del sistema <system-address-book>`:

```
sudo -E -u www-data php occ dav:sync-system-addressbook
  Syncing users ...
```

##### dav:sync-birthday-calendar

Añadir al calendario de un usuario los cumpleaños de las libretas de direcciones compartidas:

```
sudo -E -u www-data php occ dav:sync-birthday-calendar layla
  Start birthday calendar sync for layla
```

#### Mantenimiento

##### dav:fix-missing-caldav-changes

Restaurar los registros de cambios de sincronización de calendario que faltan. Si la tabla `calendarchanges` ha perdido datos, puede que los clientes no sincronicen correctamente. Ejecutarlo para un solo usuario u omitir el ID de usuario para corregir todos los usuarios (puede tardar en instancias grandes):

```
sudo -E -u www-data php occ dav:fix-missing-caldav-changes layla
sudo -E -u www-data php occ dav:fix-missing-caldav-changes
```

##### dav:remove-invalid-shares

Eliminar las comparticiones DAV no válidas creadas por un error de una versión anterior:

```
sudo -E -u www-data php occ dav:remove-invalid-shares
```

##### dav:retention:clean-up

Eliminar de la papelera de CalDAV los elementos que han superado su periodo de retención:

```
sudo -E -u www-data php occ dav:retention:clean-up
```

##### dav:send-event-reminders

Enviar las notificaciones pendientes de recordatorios de eventos de calendario. De forma predeterminada, Nextcloud envía los recordatorios mediante el trabajo en segundo plano. Para usar este comando en su lugar, cambiar primero el modo:

```
sudo -E -u www-data php occ config:app:set dav sendEventRemindersMode --value occ
```

Después, ejecutar el comando con regularidad mediante un trabajo cron dedicado para garantizar que los recordatorios se envíen a tiempo:

```
sudo -E -u www-data php occ dav:send-event-reminders
```

Consultar {nc-doc}`admin_manual/groupware/calendar` para la programación de cron recomendada.

##### dav:clear-contacts-photo-cache

Borrar todas las fotos de contactos almacenadas en caché. Es útil después de una migración o si los avatares de los contactos no se muestran correctamente:

```
sudo -E -u www-data php occ dav:clear-contacts-photo-cache
  No cached contact photos found.
```

#### Exportar e importar calendarios

##### calendar:export

Exportar un calendario a un archivo o a la salida estándar:

```
sudo -E -u www-data php occ calendar:export layla personal --location /tmp/personal.ics
```

`--format` selecciona el formato de salida (predeterminado: `ical`):

- `ical`: iCalendar (RFC 5545)
- `xcal`: iCalendar en XML (RFC 6321)
- `jcal`: iCalendar en JSON (RFC 7265)

`--location` establece la ruta del archivo de salida. Si se omite, la salida se escribe en la salida estándar:

```
sudo -E -u www-data php occ calendar:export layla personal --format xcal \
  --location /tmp/personal.xcal
sudo -E -u www-data php occ calendar:export layla personal --format jcal
```

##### calendar:import

Importar entradas de calendario en el calendario de un usuario:

```
sudo -E -u www-data php occ calendar:import layla personal /tmp/personal.ics
```

`--format` selecciona el formato de entrada (predeterminado: `ical`). Admite los mismos valores que `calendar:export`. Si se omite `location`, lee de la entrada estándar:

```
sudo -E -u www-data php occ calendar:import --format xcal layla personal \
  /tmp/personal.xcal
cat /tmp/personal.ics | sudo -E -u www-data php occ calendar:import layla personal
```

`--supersede` fuerza la sustitución de los objetos existentes con el mismo UID.

El comportamiento de la validación se controla con `--validation`:

- `0`: sin validación
- `1`: validar y omitir las entradas no válidas
- `2`: validar y fallar ante entradas no válidas

El tratamiento de errores se controla con `--errors`:

- `0`: continuar ante un error (predeterminado)
- `1`: fallar ante el primer error

Usar `--show-created`, `--show-updated`, `--show-skipped` o `--show-errors` para ver los UID de los objetos afectados después de la importación.

#### Desactivar la creación de eventos de ejemplo

Desactivar la creación automática de eventos de ejemplo para los nuevos usuarios de calendario:

```
sudo -E -u www-data php occ config:app:set dav create_example_event \
  --value=false --type=boolean
```

(nc-database_conversion_label)=
### Comandos de base de datos

Los comandos `db` gestionan el esquema de la base de datos, los índices y las conversiones de datos:

```
db
 db:add-missing-columns          add missing optional columns to the database tables
 db:add-missing-indices          add missing indices to the database tables
 db:add-missing-primary-keys     add missing primary keys to the database tables
 db:convert-filecache-bigint     convert the ID columns of the filecache to BigInt
 db:convert-mysql-charset        convert charset of MySQL/MariaDB to utf8mb4
 db:convert-type                 convert the Nextcloud database to a different type
 db:schema:expected              export the expected database schema for a fresh installation
 db:schema:export                export the current database schema
```

#### Mantenimiento del esquema

##### db:add-missing-indices

Añadir a la base de datos los índices que están definidos en el esquema pero faltan en la instalación actual. Ejecutarlo después de las actualizaciones si el rendimiento ha empeorado o si lo pide la vista general de administración:

```
sudo -E -u www-data php occ db:add-missing-indices
  Done.
```

Usar `--dry-run` para previsualizar las sentencias SQL sin ejecutarlas:

```
sudo -E -u www-data php occ db:add-missing-indices --dry-run
```

##### db:add-missing-columns

Añadir las columnas opcionales que están definidas en el esquema pero faltan en la instalación actual:

```
sudo -E -u www-data php occ db:add-missing-columns
  Done.
```

Usar `--dry-run` para previsualizar las sentencias SQL sin ejecutarlas.

##### db:add-missing-primary-keys

Añadir las claves primarias que están definidas en el esquema pero faltan en la instalación actual:

```
sudo -E -u www-data php occ db:add-missing-primary-keys
  Done.
```

Usar `--dry-run` para previsualizar las sentencias SQL sin ejecutarlas.

#### Inspección del esquema

##### db:schema:export

Exportar el esquema actual de la base de datos. Es útil para depurar o para compararlo con el esquema esperado:

```
sudo -E -u www-data php occ db:schema:export
  - oc_filecache:
    - columns:
      - checksum:
        - name: checksum
        - type: string
```

Limitar la salida a una sola tabla:

```
sudo -E -u www-data php occ db:schema:export oc_filecache
```

Usar `--sql` para obtener sentencias SQL `CREATE TABLE` en lugar del formato estructurado predeterminado. Usar `--output=json_pretty` para obtener una salida legible por máquina.

##### db:schema:expected

Exportar el esquema esperado para una instalación nueva de la versión actual. Compararlo con `db:schema:export` para detectar divergencias causadas por actualizaciones incompletas o por cambios manuales:

```
sudo -E -u www-data php occ db:schema:expected
sudo -E -u www-data php occ db:schema:expected oc_filecache
```

Admite las mismas opciones `--sql` y `--output` que `db:schema:export`.

#### Conversiones de datos

##### db:convert-filecache-bigint

Convertir las columnas de ID de la tabla `filecache` de entero a BigInt. Es necesario en instalaciones grandes en las que los ID de archivo han superado el límite de los enteros. Este comando no es destructivo, pero puede tardar en bases de datos grandes:

```
sudo -E -u www-data php occ db:convert-filecache-bigint
```

##### db:convert-mysql-charset

Convertir todas las tablas de MySQL o MariaDB para que usen `utf8mb4` (Unicode completo, emojis incluidos). Es necesario para un soporte adecuado de Unicode. Ejecutarlo una vez después de cambiar a MySQL/MariaDB o de actualizarlo:

```
sudo -E -u www-data php occ db:convert-mysql-charset
```

##### db:convert-type

(nc-database_add_indices_label)=
Convertir la base de datos de Nextcloud de SQLite a MySQL, MariaDB o PostgreSQL. SQLite es adecuado para pruebas y configuraciones de un solo usuario, pero los servidores de producción con varios usuarios deben usar una de las otras bases de datos compatibles.

Requisitos:

- La base de datos de destino y su conector PHP deben estar instalados.
- Credenciales de inicio de sesión de un usuario administrador de la base de datos.
- El número de puerto de la base de datos, si no es el estándar.

Este ejemplo convierte de SQLite a MySQL/MariaDB:

```
sudo -E -u www-data php occ db:convert-type mysql oc_dbuser 127.0.0.1 oc_database
```

Para un recorrido detallado, consultar {nc-doc}`admin_manual/configuration_database/db_conversion`.
````
