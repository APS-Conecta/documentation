---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Comandos occ de sistema: delegación, trabajos en segundo plano, registro, mantenimiento, seguridad, estado, temas, instalación y actualización."
---
# Comandos de sistema y mantenimiento

## Resumen

Esta página es la referencia de los comandos `occ` de administración del servidor: delegación de administración, trabajos en segundo plano, información de archivos y almacenamientos, registro, mantenimiento, OAuth2, seguridad, comprobaciones de configuración, estado, procesamiento de tareas, temas, webhooks, flujos de trabajo, instalación, actualización y antivirus. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/occ_system.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los comandos `occ` de esta sección abarcan la administración del servidor, la gestión de los trabajos en segundo plano y las tareas operativas. Permiten configurar el registro y el tema, gestionar los trabajos en segundo plano y el procesamiento de tareas de IA, administrar clientes OAuth2, reglas de delegación y flujos de trabajo, comprobar el estado del servidor y realizar procedimientos de instalación y actualización desde la línea de comandos.

(nc-admin_delegation_label)=
### Delegación de administración

Los comandos `admin-delegation` permiten conceder a grupos que no son de administración acceso a paneles concretos de configuraciones de administración, sin darles privilegios de administrador completos:

```
admin-delegation
 admin-delegation:add     add setting delegation to a group
 admin-delegation:remove  remove settings delegation from a group
 admin-delegation:show    show delegated settings
```

#### admin-delegation:add

Delegar una clase de configuraciones de administración a un grupo:

```
sudo -E -u www-data php occ admin-delegation:add \
  'OCA\Settings\Settings\Admin\Sharing' milliways
```

El argumento `settingClass` debe ser el nombre de clase PHP completo de una clase de ajustes que implemente `IDelegatedSettings`. Ejemplos habituales:

- `OCA\Settings\Settings\Admin\Sharing`: administración de la compartición
- `OCA\Settings\Settings\Admin\Users`: gestión de usuarios
- `OCA\Settings\Settings\Admin\Mail`: configuración del correo electrónico
- `OCA\Theming\Settings\Admin`: ajustes del tema

#### admin-delegation:remove

Quitar una delegación de ajustes de un grupo:

```
sudo -E -u www-data php occ admin-delegation:remove \
  'OCA\Settings\Settings\Admin\Sharing' milliways
```

#### admin-delegation:show

Mostrar todas las delegaciones de ajustes configuradas actualmente:

```
sudo -E -u www-data php occ admin-delegation:show
```

Usar `--output=json_pretty` para obtener una salida legible por máquina.

(nc-occ_background_jobs_label)=
### Trabajos en segundo plano

Los comandos `background-job` permiten inspeccionar y ejecutar trabajos en segundo plano individuales. Los comandos independientes `background:cron`, `background:ajax` y `background:webcron` configuran cómo se activa el planificador de trabajos en segundo plano:

```
background
 background:ajax     use ajax to run background jobs
 background:cron     use cron to run background jobs
 background:webcron  use webcron to run background jobs
background-job
 background-job:delete   remove a background job from the database
 background-job:execute  execute a single background job manually
 background-job:list     list background jobs
 background-job:worker   run a background job worker
```

#### background:cron

Establecer el modo de ejecución de los trabajos en segundo plano en cron. {vendor}`Nextcloud` recomienda el modo cron del sistema para las instancias de producción:

```
sudo -E -u www-data php occ background:cron
  Set mode for background jobs to 'cron'
```

Usar `background:ajax` para cambiar al planificador AJAX en el navegador o `background:webcron` para usar en su lugar un servicio webcron externo.

Consultar {nc-doc}`admin_manual/configuration_server/background_jobs_configuration` para una guía completa de configuración del planificador de trabajos en segundo plano.

#### background-job:delete

Eliminar un trabajo en segundo plano de la base de datos. El comando muestra los detalles del trabajo y pide confirmación:

```
sudo -E -u www-data php occ background-job:delete 42
  Job class: OCA\Files\BackgroundJob\ScanFiles
  Arguments: []

  Do you really want to delete this background job? It could create some misbehaviours in Nextcloud. (y/N)
```

:::{warning}
Eliminar un trabajo en segundo plano puede hacer que funciones de Nextcloud dejen de funcionar correctamente. Eliminar solo los trabajos que se sepa que es seguro quitar, como entradas duplicadas o huérfanas.
:::

#### background-job:execute

Ejecutar un único trabajo en segundo plano por su ID en la base de datos:

```
sudo -E -u www-data php occ background-job:execute 42
```

El comando muestra la clase, el tipo, la hora de la última ejecución y la próxima ejecución programada del trabajo antes de ejecutarlo. Si el trabajo se ejecutó hace poco y aún no le toca, puede omitirse; usar `--force-execute` para ejecutarlo de todos modos:

```
sudo -E -u www-data php occ background-job:execute --force-execute 42
```

#### background-job:list

Listar todos los trabajos en segundo plano registrados en la base de datos:

```
sudo -E -u www-data php occ background-job:list
+----+------------------------------------------------------+---------------------------+------------+
| id | class                                                | last_run                  | argument   |
+----+------------------------------------------------------+---------------------------+------------+
| 1  | OCA\Files\BackgroundJob\ScanFiles                    | 2025-06-23T10:00:00+00:00 | []         |
| 2  | OCA\Activity\BackgroundJob\DigestMail                | 2025-06-23T08:00:00+00:00 | []         |
| 3  | OC\Share20\SharesReminderJob                         | 2025-06-23T07:00:00+00:00 | []         |
+----+------------------------------------------------------+---------------------------+------------+
```

Usar `-c` / `--class` para filtrar por clase de trabajo, `-l` / `--limit` para controlar cuántos trabajos se muestran (predeterminado: 500) y `-o` / `--offset` para paginar los resultados.

#### background-job:worker

Ejecutar un proceso trabajador continuo de trabajos en segundo plano. Es una alternativa al cron del sistema para entornos en los que se quieren ejecutar los trabajos en segundo plano desde un proceso persistente en lugar de una invocación periódica de cron:

```
sudo -E -u www-data php occ background-job:worker
```

De forma predeterminada, el trabajador se ejecuta indefinidamente y comprueba cada segundo si hay trabajos nuevos.

Usar `--once` para procesar como máximo un trabajo y terminar (equivale a una única ejecución de cron):

```
sudo -E -u www-data php occ background-job:worker --once
```

Usar `--stop_after` para establecer un tiempo máximo de ejecución tras el cual el trabajador termina limpiamente (se deja terminar el trabajo en curso). Acepta segundos o valores como `30s`, `10m`, `2h`:

```
sudo -E -u www-data php occ background-job:worker --stop_after 1h
```

Usar `--interval` para establecer el intervalo de comprobación en segundos (predeterminado: 1). Establecerlo en `0` para procesar los trabajos una vez y terminar si no se encuentra ninguno:

```
sudo -E -u www-data php occ background-job:worker --interval 5
```

Indicar uno o varios nombres de clase de trabajo para procesar solo los trabajos de esos tipos:

```
sudo -E -u www-data php occ background-job:worker \
  'OCA\Files\BackgroundJob\ScanFiles'
```

(nc-broadcast_label)=
### Difusión

Enviar una difusión de prueba de Server-Sent Events (SSE) para verificar que las notificaciones push en tiempo real funcionan:

```
sudo -E -u www-data php occ broadcast:test layla
```

Indicar un nombre de evento personalizado como segundo argumento (predeterminado: `test`):

```
sudo -E -u www-data php occ broadcast:test layla my-event
```

(nc-info_label)=
### Información

Los comandos `info` muestran información detallada sobre archivos y almacenamientos. Son útiles para depurar problemas de acceso a archivos, investigar la disposición del almacenamiento e identificar el uso de espacio:

```
info
 info:file        get information for a file
 info:file:space  summarize space usage of a folder
 info:storage     get information for a single storage
 info:storages    list storages ordered by file count
```

#### info:file

Mostrar información detallada de un archivo o carpeta identificado por su ID de archivo o por su ruta:

```
sudo -E -u www-data php occ info:file /layla/files/Documents/report.pdf
  FileId: 12345
  MimeType: application/pdf
  Modified: 2025-06-01T14:30:00+00:00
  Encrypted: false
  Size: 204800
  ETag: abc123
  Permissions: 27
  Users with access: layla
```

Usar `-c` / `--children` para listar el contenido inmediato de una carpeta. Usar `--storage-tree` para mostrar el árbol de envoltorios de almacenamiento y de caché.

#### info:file:space

Mostrar cuánto espacio usa una carpeta, con un desglose ordenado de los elementos más grandes:

```
sudo -E -u www-data php occ info:file:space /layla/files/Videos
  Total: 14.7 GB
  +------------------+--------+
  | Path             | Size   |
  +------------------+--------+
  | lecture-2025.mp4 | 8.2 GB |
  | demo-video.mp4   | 4.1 GB |
  +------------------+--------+
```

Usar `-c` / `--count` para cambiar el número de elementos que se muestran (predeterminado: 25), o `-a` / `--all` para mostrar todos los elementos.

#### info:storage

Mostrar información de un único almacenamiento por su ID numérico de almacenamiento:

```
sudo -E -u www-data php occ info:storage 5
```

#### info:storages

Listar todos los almacenamientos ordenados por el número de archivos que contienen:

```
sudo -E -u www-data php occ info:storages
```

Usar `-c` / `--count` para limitar el número de almacenamientos que se muestran (predeterminado: 25), o `-a` / `--all` para listar todos los almacenamientos.

(nc-logging_commands_label)=
### Comandos de registro

Estos comandos muestran y configuran las preferencias de registro de Nextcloud:

```
log
 log:file    manipulate Nextcloud logging backend
 log:manage  manage logging configuration
 log:tail    tail the Nextcloud logfile [requires app "Log Reader" to be enabled]
 log:watch   watch the Nextcloud logfile live [requires app "Log Reader" to be enabled]
```

#### log:file

Mostrar el estado actual del registro:

```
sudo -E -u www-data php occ log:file
  Log backend Nextcloud: enabled
  Log file: /opt/nextcloud/data/nextcloud.log
  Rotate at: disabled
```

Usar `--enable` para activar el backend de registro de Nextcloud, `--file` para establecer otra ruta para el archivo de registro y `--rotate-size` para rotar el registro al alcanzar un tamaño de archivo dado en bytes (`0` desactiva la rotación).

#### log:manage

Establecer el backend de registro, el nivel de registro y la zona horaria. Los valores predeterminados son `file`, `warning` y `UTC`:

```
sudo -E -u www-data php occ log:manage --backend file --level warning --timezone UTC
  Log backend: file
  Log level: Warning (2)
  Log timezone: UTC
```

Opciones:

- `--backend`: uno de `file`, `syslog`, `errorlog`, `systemd`
- `--level`: uno de `debug`, `info`, `warning`, `error`, `fatal`
- `--timezone`: un nombre de zona horaria de PHP; consultar <https://www.php.net/manual/en/timezones.php>

(nc-maintenance_commands_label)=
### Comandos de mantenimiento

Usar estos comandos al actualizar Nextcloud, al hacer copias de seguridad o al realizar otras tareas que requieren dejar temporalmente fuera a los usuarios:

```
maintenance
 maintenance:data-fingerprint    update the systems data-fingerprint after a backup is restored
 maintenance:mimetype:update-db  update database mimetypes and update filecache
 maintenance:mimetype:update-js  update mimetypelist.js
 maintenance:mode                set maintenance mode
 maintenance:repair              repair this installation
 maintenance:repair-share-owner  fix some shares owner if it fell out of sync
 maintenance:theme:update        apply custom theme changes
 maintenance:update:htaccess     update the .htaccess file
```

#### maintenance:data-fingerprint

Después de restaurar una copia de seguridad del directorio de datos o de la base de datos, ejecutar este comando una vez. Actualiza la ETag de todos los archivos, lo que permite que los clientes de sincronización detecten que los archivos se modificaron:

```
sudo -E -u www-data php occ maintenance:data-fingerprint
```

#### maintenance:mimetype:update-db y maintenance:mimetype:update-js

Actualizar la base de datos de Nextcloud y la caché de archivos con los tipos MIME modificados de `config/mimetypemapping.json`. Ejecutarlo después de modificar ese archivo. Indicar `--repair-filecache` para aplicar el cambio a los archivos existentes:

```
sudo -E -u www-data php occ maintenance:mimetype:update-db --repair-filecache
```

`maintenance:mimetype:update-js` regenera la lista de tipos MIME del lado del cliente:

```
sudo -E -u www-data php occ maintenance:mimetype:update-js
```

#### maintenance:mode

Bloquear las sesiones de todos los usuarios con sesión iniciada, administradores incluidos, y mostrar una pantalla de estado que avisa de que el servidor está en modo de mantenimiento. Los usuarios que aún no han iniciado sesión no pueden hacerlo hasta que se desactive el modo de mantenimiento. Cuando el servidor sale del modo de mantenimiento, los usuarios con sesión iniciada deben recargar el navegador para seguir trabajando:

```
sudo -E -u www-data php occ maintenance:mode --on
  Maintenance mode enabled

sudo -E -u www-data php occ maintenance:mode --off
  Maintenance mode disabled
```

#### maintenance:repair

Se ejecuta automáticamente durante las actualizaciones para limpiar la base de datos. También puede ejecutarse manualmente si es necesario:

```
sudo -E -u www-data php occ maintenance:repair
```

#### maintenance:repair-share-owner

Corregir los registros de propietario de comparticiones que han dejado de estar sincronizados con la propiedad real de los archivos:

```
sudo -E -u www-data php occ maintenance:repair-share-owner
```

#### maintenance:theme:update

Ejecutarlo cuando los iconos de un tema personalizado no se actualizan correctamente. Reconstruye la lista de tipos MIME y borra la caché de imágenes:

```
sudo -E -u www-data php occ maintenance:theme:update
```

#### maintenance:update:htaccess

Regenerar el archivo `.htaccess` a partir de la configuración actual. Ejecutarlo después de cambiar los ajustes de reescritura de URL o después de una actualización si el archivo parece desactualizado:

```
sudo -E -u www-data php occ maintenance:update:htaccess
```

(nc-oauth2_label)=
### OAuth2

:::{note}
Este comando solo está disponible cuando `'oauth2.enable_oc_clients' => true` está establecido en `config/config.php`. Está pensado solo para migraciones de ownCloud a Nextcloud.
:::

Importar el registro de un cliente OAuth2 desde una base de datos de ownCloud durante una migración. Los argumentos `client-id` y `client-secret` provienen directamente de la tabla `oc_oauth2_clients` de la base de datos de ownCloud:

```
sudo -E -u www-data php occ oauth2:import-legacy-oc-client \
  <client-id> <client-secret>
```

(nc-security_commands_label)=
### Seguridad

Usar estos comandos para gestionar parámetros de seguridad de todo el servidor, incluidos {nc-doc}`admin_manual/configuration_server/bruteforce_configuration` y los certificados SSL de confianza. Los certificados de confianza son útiles al crear conexiones de federación con servidores que usan certificados autofirmados:

```
security
 security:bruteforce:attempts  show bruteforce attempts status for a given IP address
 security:bruteforce:reset     reset bruteforce attempts for a given IP address
 security:certificates         list trusted certificates
 security:certificates:export  export the certificate bundle
 security:certificates:import  import trusted certificate
 security:certificates:remove  remove trusted certificate
```

#### security:bruteforce:attempts

Mostrar el estado actual de la limitación por fuerza bruta de una dirección IP, incluidos el número de intentos registrados y el retraso que se aplica actualmente. Opcionalmente, filtrar por nombre de acción:

```
sudo -E -u www-data php occ security:bruteforce:attempts 192.168.1.100
sudo -E -u www-data php occ security:bruteforce:attempts 192.168.1.100 login
```

Usar `--output=json_pretty` para obtener una salida legible por máquina.

#### security:bruteforce:reset

Borrar todos los intentos de fuerza bruta registrados de una dirección IP, lo que elimina de inmediato cualquier retraso de inicio de sesión:

```
sudo -E -u www-data php occ security:bruteforce:reset 192.168.1.100
```

#### security:certificates

Listar todos los certificados de confianza instalados en el servidor:

```
sudo -E -u www-data php occ security:certificates
+---------------------+-------------+-------------------+-------------+-----------+
| File Name           | Common Name | Organization      | Valid Until | Issued By |
+---------------------+-------------+-------------------+-------------+-----------+
| myserver.crt        | myserver    | My Org            | 2026-01-01  | My CA     |
+---------------------+-------------+-------------------+-------------+-----------+
```

Usar `--output=json_pretty` para obtener una salida legible por máquina.

#### security:certificates:export

Exportar el paquete completo de certificados a stdout. Es útil para copias de seguridad o para inspeccionarlo:

```
sudo -E -u www-data php occ security:certificates:export
```

#### security:certificates:import

Instalar un certificado de confianza desde un archivo. El nombre del certificado se deriva del nombre del archivo:

```
sudo -E -u www-data php occ security:certificates:import /path/to/certificate.crt
```

#### security:certificates:remove

Quitar un certificado de confianza por su nombre de archivo (tal como se muestra en `security:certificates`):

```
sudo -E -u www-data php occ security:certificates:remove my-certificate
```

(nc-setupchecks_commands_label)=
### Comprobaciones de configuración

Ejecutar las comprobaciones de configuración desde la línea de comandos para verificar la configuración de la instalación:

```
sudo -E -u www-data php occ setupchecks
```

Ejemplo de salida:

```
dav:
  ✓ DAV system address book: No outstanding DAV system address book sync.
network:
  ✓ WebDAV endpoint: Your web server is properly set up to allow file synchronization over WebDAV.
  ✓ Data directory protected
  ✓ Internet connectivity
  ...
```

Usar `--output=json_pretty` para obtener una salida legible por máquina, adecuada para la monitorización automatizada.

(nc-share_operations_label)=
### Operaciones con comparticiones

Comandos `occ` disponibles para el espacio de nombres `share`:

```
share
 share:list  list available shares
```

(nc-occ_share_list_label)=
#### share:list

Listar todas las comparticiones del sistema:

```
sudo -E -u www-data php occ share:list
```

Filtrar por propietario, por destinatario o por el usuario que creó la compartición:

```
sudo -E -u www-data php occ share:list --owner layla
sudo -E -u www-data php occ share:list --recipient fred
sudo -E -u www-data php occ share:list --by layla
```

Filtrar por la ruta de un archivo concreto:

```
sudo -E -u www-data php occ share:list --file "/layla/files/Documents/report.pdf"
```

Filtrar por una carpeta; usar `--recursive` para incluir las comparticiones anidadas en cualquier lugar dentro de ella:

```
sudo -E -u www-data php occ share:list --parent "/layla/files/Projects" --recursive
```

Filtrar por tipo de compartición (uno de `user`, `group`, `link`, `email`, `remote`, `room`, `deck`) o por estado de la compartición:

```
sudo -E -u www-data php occ share:list --type link
sudo -E -u www-data php occ share:list --status 0
```

(nc-snowflakes_commands_label)=
### ID Snowflake

Nextcloud usa ID Snowflake como identificadores únicos en varios subsistemas. Decodificar un ID Snowflake para inspeccionar su marca de tiempo y sus metadatos incrustados:

```
sudo -E -u www-data php occ snowflake:decode 6768789079123765868
```

Ejemplo de salida:

```
+--------------------+-------------------------+
| Snowflake ID       | 6768789079123765868     |
| Seconds            | 1575981518              |
| Milliseconds       | 50                      |
| Created from CLI   | no                      |
| Server ID          | 441                     |
| Sequence ID        | 2668                    |
| Creation timestamp | 1575981518.050          |
| Creation date      | 2019-12-10 11:18:38.050 |
+--------------------+-------------------------+
```

### Estado

Usar el comando `status` para obtener información sobre la instalación actual:

```
sudo -E -u www-data php occ status
  - installed: true
  - version: 30.0.0.0
  - versionstring: 30.0.0
  - edition:
  - maintenance: false
  - needsDbUpgrade: false
  - productname: Nextcloud
  - extendedSupport: false
```

Usar `--output=json_pretty` para obtener una salida legible por máquina:

```
sudo -E -u www-data php occ status --output=json_pretty
{
    "installed": true,
    "version": "30.0.0.0",
    "versionstring": "30.0.0",
    "edition": "",
    "maintenance": false,
    "needsDbUpgrade": false,
    "productname": "Nextcloud",
    "extendedSupport": false
}
```

#### Código de retorno del estado

Usar la opción `-e` para obtener un código de salida legible por máquina que refleja el estado de la instalación. De forma predeterminada no hay salida, lo que lo hace adecuado para scripts, comprobaciones de monitorización y unidades de systemd:

```
sudo -E -u www-data php occ status -e
echo $?
0
sudo -E -u www-data php occ maintenance:mode --on
Maintenance mode enabled
sudo -E -u www-data php occ status -e
echo $?
1
sudo -E -u www-data php occ maintenance:mode --off
Maintenance mode disabled
sudo -E -u www-data php occ status -e
echo $?
0
```

| Código de retorno | Descripción |
| --- | --- |
| 0 | funcionamiento normal |
| 1 | el modo de mantenimiento está activado; la instancia no está disponible para los usuarios en este momento |
| 2 | se requiere `occ upgrade` |

(nc-taskprocessing_label)=
### Procesamiento de tareas

Los comandos `taskprocessing` gestionan los trabajos de procesamiento de tareas de IA y en segundo plano. El procesamiento de tareas proporciona la infraestructura para funciones de IA como la generación de texto, la clasificación de imágenes y la conversión de voz a texto:

```
taskprocessing
 taskprocessing:task-type:set-enabled enable or disable a task type
 taskprocessing:task:cleanup          cleanup old tasks
 taskprocessing:task:get              display all information for a specific task
 taskprocessing:task:list             list tasks
 taskprocessing:task:stats            get statistics for tasks
 taskprocessing:worker                run a dedicated worker for synchronous TaskProcessing providers
```

#### taskprocessing:task-type:set-enabled

Activar o desactivar un tipo de tarea:

```
sudo -E -u www-data php occ taskprocessing:task-type:set-enabled core:text2text 1
sudo -E -u www-data php occ taskprocessing:task-type:set-enabled core:text2text 0
```

#### taskprocessing:task:cleanup

Eliminar los registros de tareas antiguos y sus archivos de salida asociados. De forma predeterminada, se eliminan las tareas de más de cuatro meses:

```
sudo -E -u www-data php occ taskprocessing:task:cleanup
```

Indicar una antigüedad máxima en segundos para cambiar el valor predeterminado:

```
sudo -E -u www-data php occ taskprocessing:task:cleanup 2592000
```

#### taskprocessing:task:get

Mostrar toda la información de una tarea concreta por su ID numérico:

```
sudo -E -u www-data php occ taskprocessing:task:get 42
```

#### taskprocessing:task:list

Listar las tareas del procesamiento de tareas:

```
sudo -E -u www-data php occ taskprocessing:task:list
```

Filtrar por usuario, tipo, app o ID personalizado:

```
sudo -E -u www-data php occ taskprocessing:task:list --userIdFilter layla
sudo -E -u www-data php occ taskprocessing:task:list --type core:text2text
```

Filtrar por estado (0=UNKNOWN, 1=SCHEDULED, 2=RUNNING, 3=SUCCESSFUL, 4=FAILED, 5=CANCELLED):

```
sudo -E -u www-data php occ taskprocessing:task:list --status 4
```

Otros filtros disponibles: `--appId`, `--customId`, `--scheduledAfter`, `--endedBefore`.

#### taskprocessing:task:stats

Mostrar estadísticas de las tareas (tiempo de ejecución máximo y medio, tiempo en cola y tamaños de entrada y salida). Acepta las mismas opciones de filtro que `taskprocessing:task:list`:

```
sudo -E -u www-data php occ taskprocessing:task:stats
```

#### taskprocessing:worker

Ejecutar un trabajador dedicado que procesa las tareas de los proveedores síncronos de TaskProcessing. Usarlo cuando se quiera descargar la ejecución de tareas de IA en un proceso aparte:

```
sudo -E -u www-data php occ taskprocessing:worker
```

Usar `--once` para procesar como máximo una tarea y terminar. Usar `--timeout` para establecer un tiempo máximo de ejecución en segundos (predeterminado: `0` = ejecutarse indefinidamente). Usar `--taskTypes` (repetible) para restringir el trabajador a ID de tipos de tarea concretos:

```
sudo -E -u www-data php occ taskprocessing:worker \
  --taskTypes core:text2text --once
```

(nc-theming_label)=
### Temas

La app de temas (`theming`) está siempre activada. El comando `theming:config` permite ver y actualizar los ajustes del tema sin iniciar sesión en la interfaz web:

```
theming
 theming:config  set theming app config values
```

#### theming:config

Sin argumentos, muestra todos los valores actuales del tema:

```
sudo -E -u www-data php occ theming:config
  Current theming config:
  name: Nextcloud
  url: https://nextcloud.com
  slogan: a safe home for all your data
  ...
```

Mostrar el valor actual de una sola clave:

```
sudo -E -u www-data php occ theming:config name
```

Establecer un valor:

```
sudo -E -u www-data php occ theming:config name "Acme Cloud"
sudo -E -u www-data php occ theming:config url "https://acme.example.com"
sudo -E -u www-data php occ theming:config slogan "Secure file sync for Acme"
sudo -E -u www-data php occ theming:config primary_color "#0082c9"
sudo -E -u www-data php occ theming:config background_color "#00679e"
sudo -E -u www-data php occ theming:config disable-user-theming true
```

Para establecer una imagen, indicar como valor la ruta del archivo de imagen:

```
sudo -E -u www-data php occ theming:config logo /path/to/logo.png
sudo -E -u www-data php occ theming:config favicon /path/to/favicon.ico
sudo -E -u www-data php occ theming:config background /path/to/background.jpg
```

Restablecer una clave a su valor predeterminado:

```
sudo -E -u www-data php occ theming:config --reset name
```

Claves de texto admitidas: `name`, `url`, `imprintUrl`, `privacyUrl`, `slogan`, `primary_color`, `background_color`, `disable-user-theming`.

Claves de imagen admitidas: `background`, `logo`, `logoheader`, `favicon`.

(nc-webhook_listeners_label)=
### Receptores de webhooks

:::{note}
La app Webhook listeners (`webhook_listeners`) se distribuye con Nextcloud, pero no está activada de forma predeterminada. Activarla en el menú Apps antes de usar estos comandos.
:::

Listar todas las configuraciones de receptores de webhooks registradas en el servidor. Cada entrada muestra el ID del receptor, el usuario o la app que lo registró, el método HTTP y el URI de destino, el evento de Nextcloud que escucha, el filtro de eventos, si lo hay, y el método de autenticación configurado (`none` o `header`):

```
sudo -E -u www-data php occ webhook_listeners:list
```

Usar `--output=json_pretty` para obtener una salida legible por máquina, que incluye además los campos completos de cabecera y de datos de autenticación:

```
sudo -E -u www-data php occ webhook_listeners:list --output=json_pretty
```

Los receptores de webhooks se configuran desde la interfaz de configuraciones de administración o con la API REST. Este comando es de solo lectura: ofrece una vista de auditoría de los receptores activos sin necesidad de acceder a la interfaz web.

(nc-workflows_label)=
### Flujos de trabajo

El motor de flujos de trabajo (`workflowengine`) está siempre activado:

```
workflows
 workflows:list  list configured workflows
```

#### workflows:list

Listar las reglas de flujo de trabajo configuradas. Usar el argumento opcional `scope` para filtrar por ámbito: `admin` (predeterminado) o `user`:

```
sudo -E -u www-data php occ workflows:list
sudo -E -u www-data php occ workflows:list user
sudo -E -u www-data php occ workflows:list user layla
```

La salida es una representación JSON de las operaciones de flujo de trabajo configuradas.

(nc-command_line_installation_label)=
### Instalación desde la línea de comandos

Estos comandos solo están disponibles antes de instalar Nextcloud, después de desempaquetar el archivo y copiar Nextcloud en los directorios adecuados.

Mostrar las opciones de instalación disponibles:

```
sudo -E -u www-data php /var/www/nextcloud/occ maintenance:install --help
Nextcloud is not installed - only a limited number of commands are available

Usage:
  maintenance:install [options]

Options:
      --database[=DATABASE]                  Supported database type [default: "sqlite"]
      --database-name[=DATABASE-NAME]        Name of the database
      --database-host[=DATABASE-HOST]        Hostname of the database [default: "localhost"]
      --database-port[=DATABASE-PORT]        Port of the database
      --database-user[=DATABASE-USER]        User name to connect to the database
      --database-pass[=DATABASE-PASS]        Password of the database user
      --database-table-prefix[=...]          Table prefix for every table in the database
      --admin-user[=ADMIN-USER]              User name of the admin account [default: "admin"]
      --admin-pass[=ADMIN-PASS]              Password of the admin account
      --data-dir[=DATA-DIR]                  Path to data directory [default: "/var/www/nextcloud/data"]
```

Este ejemplo instala Nextcloud con una base de datos MySQL:

```
sudo -E -u www-data php occ maintenance:install \
  --database mysql \
  --database-name nextcloud \
  --database-host 127.0.0.1 \
  --database-user nextcloud \
  --database-pass secret \
  --admin-user admin \
  --admin-pass password
  Nextcloud was successfully installed
```

Bases de datos compatibles:

- `sqlite`: SQLite (solo edición Community; no recomendada para producción)
- `mysql`: MySQL o MariaDB
- `pgsql`: PostgreSQL
- `oci`: Oracle (solo {vendor}`Nextcloud` Enterprise)

(nc-command_line_upgrade_label)=
### Actualización desde la línea de comandos

Estos comandos están disponibles después de descargar un paquete o tarball actualizado y antes de completar la actualización.

:::{important}
`occ upgrade` solo ejecuta la **fase de migración**: las actualizaciones del esquema de la base de datos y las actualizaciones de las apps. **No** descarga ni sustituye los archivos de código de Nextcloud.

Antes de ejecutar `occ upgrade`, primero hay que sustituir el código de una de estas formas:

- El actualizador integrado: `sudo -E -u www-data php /var/www/nextcloud/updater/updater.phar`
- Un tarball extraído manualmente (consultar {nc-doc}`admin_manual/maintenance/manual_upgrade`)

Si `occ upgrade` informa *«Nextcloud is up to date»* cuando se espera que se ejecute una actualización, es que aún no se han sustituido los archivos de código: ejecutar antes el actualizador o extraer el nuevo tarball.

Consultar {nc-doc}`admin_manual/maintenance/upgrade` para el proceso de actualización completo.
:::

Al hacer una actualización, usar `occ upgrade` en lugar del actualizador web para evitar los límites de tiempo de espera de PHP (la interfaz web impone un límite de 3600 segundos). En instalaciones grandes, ese límite puede no ser suficiente y dejar el sistema en un estado incoherente.

Después de completar todos los pasos previos (consultar {nc-doc}`admin_manual/maintenance/upgrade`), ejecutar la actualización:

```
sudo -E -u www-data php occ upgrade
  Nextcloud or one of the apps require upgrade - only a limited number of
  commands are available
  Turned on maintenance mode
  Checked database schema update
  Checked database schema update for apps
  Updated database
  Updating <gallery> ...
  Updated <gallery> to 0.6.1
  Updating <activity> ...
  Updated <activity> to 2.1.0
  Update successful
  Turned off maintenance mode
```

Usar `-v` para mostrar marcas de tiempo en cada paso:

```
sudo -E -u www-data php occ upgrade -v
  2025-06-23T09:06:15+0000 Turned on maintenance mode
  2025-06-23T09:06:15+0000 Checked database schema update
  2025-06-23T09:06:15+0000 Checked database schema update for apps
  2025-06-23T09:06:15+0000 Updated database
  2025-06-23T09:06:15+0000 Updated <files_sharing> to 0.6.6
  2025-06-23T09:06:15+0000 Update successful
  2025-06-23T09:06:15+0000 Turned off maintenance mode
```

Si se produce un error, la excepción se registra en el archivo de registro de Nextcloud:

```
Turned on maintenance mode
Checked database schema update
Checked database schema update for apps
Updated database
Updating <files_sharing> ...
Exception
ServerNotAvailableException: LDAP server is not available
Update failed
Turned off maintenance mode
```

(nc-antivirus_commands_label)=
### Antivirus

:::{note}
Estos comandos requieren que la app [files_antivirus](https://apps.nextcloud.com/apps/files_antivirus) esté instalada y activada.
:::

```
files_antivirus
 files_antivirus:background-scan  run the background scan
 files_antivirus:mark             mark a file as scanned or unscanned
 files_antivirus:scan             scan a file
 files_antivirus:status           show antivirus scanner status
```

#### files_antivirus:background-scan

Lanzar manualmente el análisis antivirus en segundo plano. De forma predeterminada se procesan todos los archivos pendientes. Usar `--max` para limitar el número de archivos analizados en una sola ejecución:

```
sudo -E -u www-data php occ files_antivirus:background-scan
sudo -E -u www-data php occ files_antivirus:background-scan --max 500
```

#### files_antivirus:mark

Marcar un archivo como analizado o no analizado. El argumento `file` es la ruta del archivo y `mode` es `scanned` o `unscanned`:

```
sudo -E -u www-data php occ files_antivirus:mark /layla/files/report.pdf scanned
sudo -E -u www-data php occ files_antivirus:mark /layla/files/report.pdf unscanned
```

Usar `--forever` (`-f`) al marcar un archivo como analizado para excluirlo de forma permanente de futuros análisis:

```
sudo -E -u www-data php occ files_antivirus:mark --forever /layla/files/report.pdf scanned
```

#### files_antivirus:scan

Analizar un único archivo de inmediato e informar del resultado:

```
sudo -E -u www-data php occ files_antivirus:scan /layla/files/report.pdf
```

Usar `--debug` para activar la salida detallada del backend, útil para diagnosticar problemas de conectividad del escáner:

```
sudo -E -u www-data php occ files_antivirus:scan --debug /layla/files/report.pdf
```

#### files_antivirus:status

Mostrar el estado actual del escáner antivirus, incluidos el backend configurado y si el escáner es accesible:

```
sudo -E -u www-data php occ files_antivirus:status
```

Usar `-v` para obtener más detalles del backend.
````
