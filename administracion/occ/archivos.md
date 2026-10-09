---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Comandos occ de archivos: caché y análisis, almacenamiento de objetos, vistas previas, papelera, versiones, comparticiones, montajes externos e integridad."
---
# Comandos de archivos

## Resumen

Esta página es la referencia de los comandos `occ` para la gestión diaria de archivos, el mantenimiento del almacenamiento y la administración de comparticiones: caché y análisis de archivos, almacenamiento de objetos, vistas previas, papelera, versiones, comparticiones, sincronización de federación, almacenamiento externo y comprobación de integridad. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/occ_files.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los comandos `occ` de esta sección abarcan la gestión diaria de archivos, el mantenimiento del almacenamiento y la administración de comparticiones. Permiten analizar y reparar la caché de archivos, mover o eliminar archivos en nombre de los usuarios, gestionar la papelera y el historial de versiones, configurar montajes de almacenamiento externo, inspeccionar el contenido del almacenamiento de objetos y verificar la integridad de las apps desde la línea de comandos.

Varias secciones requieren que estén activadas apps concretas. Todas las siguientes se distribuyen con Nextcloud y pueden activarse en el menú Apps:

- Los comandos de **papelera** requieren la app **Archivos eliminados** (`files_trashbin`), activada de forma predeterminada
- Los comandos de **versiones de archivos** requieren la app **Versiones** (`files_versions`), activada de forma predeterminada
- La **sincronización de federación** requiere la app **Federación** (`federation`), activada de forma predeterminada
- Los comandos de **almacenamiento externo** requieren la app **Soporte de almacenamiento externo** (`files_external`), no activada de forma predeterminada

### Operaciones con archivos

```
files
 files:cleanup                        remove file cache entries with no matching storage entry
 files:copy                           copy a file or folder
 files:delete                         delete a file or folder
 files:get                            get the contents of a file
 files:mount:list                     list all mounts for a user
 files:mount:refresh                  refresh the list of mounts for a user
 files:move                           move a file or folder
 files:put                            write content to a file
 files:reminders                      list file reminders
 files:repair-tree                    repair malformed filesystem tree structures
 files:sanitize-filenames             rename files that do not match the current filename constraints
 files:scan                           rescan the filesystem
 files:scan-app-data                  rescan the AppData folder
 files:transfer-ownership             transfer all files and shares from one user to another
 files:windows-compatible-filenames   toggle enforcement of Windows-compatible filenames
```

#### files:cleanup

Eliminar todas las entradas de la caché de archivos que no tienen una entrada correspondiente en la tabla de almacenamientos. Ejecutarlo después de eliminar registros de almacenamiento huérfanos o después de una migración que haya dejado la caché de archivos en un estado incoherente:

```
sudo -E -u www-data php occ files:cleanup
```

#### files:copy

Copiar un archivo o carpeta dentro de Nextcloud. El origen y el destino aceptan una ruta de Nextcloud o un ID numérico de archivo:

```
sudo -E -u www-data php occ files:copy /layla/files/Photos \
  /layla/files/Photos-backup
```

Si la ruta de destino ya existe y es una carpeta, el origen se copia dentro de ella (el comportamiento estándar de cp). Usar `--no-target-directory` / `-T` para sobrescribir en su lugar la carpeta de destino:

```
sudo -E -u www-data php occ files:copy -T /layla/files/Photos \
  /layla/files/Photos-backup
```

Si el destino existe, el comando pide confirmación. Usar `--force` / `-f` para omitir la pregunta y suprimir las advertencias de discrepancia de tipo.

#### files:delete

Eliminar un archivo o carpeta:

```
sudo -E -u www-data php occ files:delete /layla/files/Documents/old-draft.pdf
```

El comando pide confirmación antes de eliminar. Usar `--force` / `-f` para omitir la pregunta.

Si la ruta apunta a la raíz de una compartición recibida por un usuario, el comando pregunta si se quiere dejar de compartir (quitar el acceso del usuario) en lugar de eliminar el archivo subyacente:

```
sudo -E -u www-data php occ files:delete /layla/files/Shared-Folder
  /layla/files/Shared-Folder in a shared file, do you want to unshare
  the file from layla instead of deleting the source file? [Y/n]
```

Cuando el archivo es accesible para varios usuarios, el comando lista todos los usuarios afectados y pide confirmación antes de continuar.

#### files:get

Descargar un archivo de Nextcloud a una ruta local. El argumento de origen acepta una ruta de Nextcloud o un ID numérico de archivo:

```
sudo -E -u www-data php occ files:get /layla/files/Documents/report.pdf \
  /tmp/report.pdf
```

Omitir la ruta de salida (o indicar `-`) para escribir en la salida estándar:

```
sudo -E -u www-data php occ files:get /layla/files/Documents/report.pdf -
```

:::{warning}
Escribir archivos binarios en un terminal puede dañar la sesión del terminal. Nextcloud se niega a escribir contenido binario en STDOUT salvo que se indique explícitamente `-` como ruta de salida.
:::

#### files:mount:list

Listar todos los montajes registrados de un usuario, con el punto de montaje, el ID de almacenamiento, el proveedor y si el montaje sigue proporcionándose activamente:

```
sudo -E -u www-data php occ files:mount:list layla
/layla/: local::home/nextcloud/data/layla/files
        - provider: OC\Files\Mount\LocalRootMountProvider
        - storage id: 1
        - root id: 1
```

Los montajes obsoletos (registrados en la caché pero que ya no se proporcionan) se marcan con `registered but no longer provided`.

#### files:mount:refresh

Volver a registrar en la caché de montajes todos los montajes activos actualmente de un usuario. Es útil después de cambios en la configuración de montajes que no se aplicaron automáticamente:

```
sudo -E -u www-data php occ files:mount:refresh layla
  Registered 3 mounts
```

#### files:move

Mover un archivo o carpeta dentro de Nextcloud:

```
sudo -E -u www-data php occ files:move \
  /layla/files/Documents/draft.pdf \
  /layla/files/Documents/Archive/draft.pdf
```

Si el destino ya existe, el comando pide confirmación. Usar `--force` / `-f` para omitir la pregunta. Si el origen y el destino son de tipos distintos (archivo frente a carpeta), el destino se elimina antes de mover; el comando se niega si el destino es la raíz de un montaje o no puede eliminarse.

#### files:put

Subir un archivo local a Nextcloud. El argumento de destino acepta una ruta de Nextcloud o el ID numérico de un archivo existente:

```
sudo -E -u www-data php occ files:put /tmp/report.pdf \
  /layla/files/Documents/report.pdf
```

Leer de la entrada estándar indicando `-` como origen:

```
cat /tmp/report.pdf | sudo -E -u www-data php occ files:put - \
  /layla/files/Documents/report.pdf
```

#### files:reminders

Listar todos los recordatorios de archivos de todos los usuarios o de un usuario concreto:

```
sudo -E -u www-data php occ files:reminders
+-------+---------+-------------------------------------------+---------------------------+
| User  | File Id | Path                                      | Due Date (UTC)            |
+-------+---------+-------------------------------------------+---------------------------+
| layla | 42      | /layla/files/Documents/report.pdf         | 2026-05-01T09:00:00+00:00 |
+-------+---------+-------------------------------------------+---------------------------+

sudo -E -u www-data php occ files:reminders layla
```

Usar `--output=json_pretty` para obtener una salida legible por máquina.

#### files:repair-tree

Reparar las entradas de la caché de archivos cuya ruta almacenada no coincide con la ruta derivada de su carpeta superior. Esto puede hacer que los archivos aparezcan en una ubicación incorrecta: al listar una carpeta se muestra el archivo, pero el acceso a él por su ruta falla. El comando restablece cada entrada afectada a su ruta correcta:

```
sudo -E -u www-data php occ files:repair-tree
```

(nc-occ_files_sanitize_filenames)=
#### files:sanitize-filenames

Renombrar los archivos que no cumplen las restricciones actuales de nombres de archivo (por ejemplo, después de activar los {nc-ref}`nombres de archivo compatibles con Windows <windows_compatible_filenames>`). Ejecutarlo para todos los usuarios o para un usuario concreto:

```
sudo -E -u www-data php occ files:sanitize-filenames
sudo -E -u www-data php occ files:sanitize-filenames layla
```

Los caracteres no válidos se sustituyen por un espacio, un guion bajo o un guion, el que permitan las restricciones actuales. Usar `--char-replacement` para indicar el carácter de sustitución cuando ninguno de esos valores predeterminados está permitido:

```
sudo -E -u www-data php occ files:sanitize-filenames \
  --char-replacement=_ layla
```

Usar `--dry-run` para previsualizar los cambios de nombre sin hacer cambios:

```
sudo -E -u www-data php occ files:sanitize-filenames --dry-run
```

(nc-occ_files_scan_label)=
#### files:scan

Buscar archivos nuevos o modificados y actualizar la caché de archivos. Ejecutarlo para todos los usuarios, para un usuario concreto o para una ruta concreta:

```
sudo -E -u www-data php occ files:scan --all
sudo -E -u www-data php occ files:scan layla
sudo -E -u www-data php occ files:scan layla fred
```

Usar `--path` para limitar el análisis a un directorio concreto. La ruta debe incluir el ID de usuario y `files/`:

```
sudo -E -u www-data php occ files:scan --path="/layla/files/Photos"
```

Las opciones `--path`, `--all` y `[user_id]` son mutuamente excluyentes; solo puede indicarse una a la vez.

Opciones adicionales:

- `--generate-metadata`: genera metadatos (p. ej., datos EXIF) para los archivos analizados
- `--unscanned`: analiza solo los archivos marcados como aún no analizados por completo (útil para lanzar el análisis que, de otro modo, ejecutaría el trabajo en segundo plano)
- `--shallow`: no analiza las carpetas de forma recursiva
- `--home-only`: omite los almacenamientos externos y las comparticiones, y analiza solo el almacenamiento personal
- `--quiet`: suprime la salida; sin esta opción, se muestran estadísticas después del análisis
- `--output=json_pretty`: salida legible por máquina

Usar `-v` para ver cada archivo a medida que se procesa. Los niveles de verbosidad `-vv` y `-vvv` se limitan silenciosamente a `-v`.

Un trabajo en segundo plano se ejecuta cada 10 minutos para analizar los archivos de tamaño desconocido en la caché de archivos, de modo que los nuevos análisis rutinarios se gestionan automáticamente. Usar este comando cuando se necesite un nuevo análisis inmediato; por ejemplo, después de copiar archivos directamente en el directorio de datos, después de una migración o para investigar incoherencias de la caché de archivos. El análisis en segundo plano puede desactivarse estableciendo `'files_no_background_scan' => true` en `config.php`.

#### files:scan-app-data

Volver a analizar el directorio `appdata` y actualizar la caché de archivos de los archivos compartidos entre usuarios (imágenes de avatar, vistas previas de archivos, CSS en caché, etc.):

```
sudo -E -u www-data php occ files:scan-app-data
```

Limitar el análisis a un subdirectorio concreto de appdata:

```
sudo -E -u www-data php occ files:scan-app-data preview
```

A diferencia de `files:scan`, no hay ningún trabajo en segundo plano que vuelva a analizar appdata automáticamente. Ejecutar este comando manualmente cuando la caché de archivos de appdata pueda haber quedado incoherente; por ejemplo, después de restaurar appdata desde una copia de seguridad, después de mover o copiar manualmente archivos en el directorio appdata, o cuando las vistas previas o los avatares no se muestran correctamente pese a que los archivos subyacentes están en el disco.

#### files:transfer-ownership

Transferir todos los archivos y comparticiones de un usuario a otro. Es útil antes de eliminar una cuenta de usuario:

```
sudo -E -u www-data php occ files:transfer-ownership layla fred
```

Los archivos transferidos aparecen en un subdirectorio dentro de la carpeta personal del usuario de destino.

:::{note}
Salvo que el cifrado en el servidor esté activado, el comando inicializa el sistema de archivos del usuario de destino si este aún no ha iniciado sesión. Si no se puede escribir en el directorio de datos del usuario de destino, el comando informa: `unable to rename, destination directory is not writable`.
:::

Si la carpeta personal del usuario de destino está vacía, usar `--move` para mover los archivos directamente a la raíz sin crear un subdirectorio:

```
sudo -E -u www-data php occ files:transfer-ownership --move layla fred
```

Transferir solo una carpeta concreta con `--path`:

```
sudo -E -u www-data php occ files:transfer-ownership \
  --path="Documents/Project" layla fred
```

Las comparticiones entrantes (archivos compartidos con el usuario de origen) no se transfieren de forma predeterminada, porque la propiedad sigue siendo de quien compartió originalmente. Transferirlas con `--transfer-incoming-shares=1`:

```
sudo -E -u www-data php occ files:transfer-ownership \
  --transfer-incoming-shares=1 layla fred
```

Establecer `'transferIncomingShares' => true` en `config.php` para transferir siempre las comparticiones entrantes. La opción de línea de comandos tiene prioridad:

```
sudo -E -u www-data php occ files:transfer-ownership \
  --transfer-incoming-shares=0 layla fred
```

Los usuarios también pueden transferir archivos de forma selectiva desde la interfaz web. Consultar la [documentación de usuario](https://docs.nextcloud.com/server/latest/user_manual/en/files/transfer_ownership.html) para más detalles.

(nc-occ_files_windows_filenames)=
#### files:windows-compatible-filenames

Activar o desactivar la aplicación obligatoria de los {nc-ref}`nombres de archivo compatibles con Windows <windows_compatible_filenames>`:

```
sudo -E -u www-data php occ files:windows-compatible-filenames --enable
sudo -E -u www-data php occ files:windows-compatible-filenames --disable
```

Después de activarla, ejecutar `files:sanitize-filenames` para renombrar los archivos existentes que no la cumplan.

### Almacenamiento de objetos

```
files
 files:object:delete                  delete an object from the object store
 files:object:get                     get the contents of an object
 files:object:info                    get the metadata of an object
 files:object:list                    list all objects in the object store
 files:object:orphans                 list objects in the object store with no matching database entry
 files:object:put                     write a file to the object store
```

Estos comandos operan directamente sobre el almacenamiento de objetos subyacente (S3, Swift, etc.) que se usa como almacenamiento principal de Nextcloud. Omiten la caché de archivos y los controles de acceso normales.

:::{warning}
Estos comandos manipulan objetos directamente en el almacenamiento de objetos. Escribir o eliminar objetos que pertenecen a archivos existentes daña esos archivos. Usarlos solo para depuración o recuperación, nunca para la gestión rutinaria de archivos.
:::

#### files:object:list

Listar todos los objetos del almacenamiento de objetos. Requiere que el almacenamiento de objetos configurado admita el listado de metadatos:

```
sudo -E -u www-data php occ files:object:list
+------------+--------+-------------------------------+
| URN        | Size   | Last modified                 |
+------------+--------+-------------------------------+
| urn:oid:1  | 512    | 2026-01-01T00:00:00+00:00     |
| urn:oid:42 | 204800 | 2026-04-01T12:00:00+00:00     |
+------------+--------+-------------------------------+
```

Usar `--bucket` / `-b` si el bucket no puede determinarse a partir de la configuración. Usar `--output=json_pretty` para obtener una salida legible por máquina.

#### files:object:get

Descargar un objeto del almacenamiento de objetos a un archivo local. Indicar `-` como ruta de salida para escribir en la salida estándar:

```
sudo -E -u www-data php occ files:object:get urn:oid:42 /tmp/recovered.pdf
sudo -E -u www-data php occ files:object:get urn:oid:42 -
```

#### files:object:info

Mostrar los metadatos (tamaño, tipo MIME, fecha de última modificación) de un objeto:

```
sudo -E -u www-data php occ files:object:info urn:oid:42
  - size: 200 KB
  - mimetype: application/pdf
  - mtime: 2026-04-01T12:00:00+00:00
```

Usar `--output=json_pretty` para obtener una salida legible por máquina.

#### files:object:put

Subir un archivo local al almacenamiento de objetos con el nombre de objeto indicado. Leer de la entrada estándar indicando `-`:

```
sudo -E -u www-data php occ files:object:put /tmp/data.bin urn:oid:42
sudo -E -u www-data php occ files:object:put - urn:oid:42
```

Si el objeto ya corresponde a un archivo de la base de datos, el comando avisa y pide confirmación antes de sobrescribirlo. Para actualizar un archivo de forma segura, usar en su lugar `files:put` con el ID del archivo.

#### files:object:delete

Eliminar un objeto del almacenamiento de objetos:

```
sudo -E -u www-data php occ files:object:delete urn:oid:42
```

Si el objeto pertenece a un archivo de la base de datos, el comando advierte de que eliminarlo dañará el archivo y muestra el ID del archivo para que pueda usarse en su lugar `files:delete` y hacer una eliminación limpia.

#### files:object:orphans

Listar los objetos del almacenamiento de objetos que no tienen una entrada correspondiente en la base de datos de la caché de archivos. Son objetos de los que Nextcloud ya no lleva registro y que puede ser seguro eliminar después de investigarlos:

```
sudo -E -u www-data php occ files:object:orphans
```

Usar `--output=json_pretty` para obtener una salida legible por máquina. Requiere que el almacenamiento de objetos admita el listado de metadatos.

(nc-occ_cleanup_previews)=
### Vista previa

```
preview
 preview:cleanup                      remove all generated preview files
```

#### preview:cleanup

Eliminar todos los archivos de vista previa generados. Es útil después de cambiar la configuración de las vistas previas (tamaños, calidad o tipos de archivo admitidos), o en instalaciones que usan almacenamiento de objetos como almacenamiento principal, donde la carpeta de vistas previas no puede eliminarse manualmente:

```
sudo -E -u www-data php occ preview:cleanup
  Previews removed
```

Después de ejecutar este comando, Nextcloud regenera las vistas previas a demanda a medida que los usuarios acceden a los archivos.

Consultar {nc-doc}`admin_manual/configuration_files/previews_configuration` para los ajustes de las vistas previas.

### Papelera

```
trashbin
 trashbin:cleanup                     permanently delete all files in the trash for a user
 trashbin:expire                      expire trash items that exceed the configured retention period
 trashbin:size                        show or set the target trash bin size
```

#### trashbin:size

Mostrar el tamaño objetivo actual de la papelera:

```
sudo -E -u www-data php occ trashbin:size
  Default size: default (50% of available space)
```

Mostrar el tamaño efectivo para un usuario concreto:

```
sudo -E -u www-data php occ trashbin:size --user layla
  default (50% of available space)
```

Establecer el tamaño objetivo predeterminado global. Acepta tamaños legibles por personas:

```
sudo -E -u www-data php occ trashbin:size 10GB
```

:::{note}
Cambiar el valor predeterminado global desencadena inmediatamente una limpieza de las papeleras existentes. La papelera de un usuario puede superar temporalmente el tamaño configurado hasta que el usuario vuelva a mover un archivo a la papelera.
:::

Establecer un tamaño objetivo por usuario:

```
sudo -E -u www-data php occ trashbin:size --user layla 2GB
```

#### trashbin:cleanup

Eliminar de forma permanente todos los archivos de la papelera de uno o varios usuarios, o de todos los usuarios:

```
sudo -E -u www-data php occ trashbin:cleanup layla
  Remove deleted files of   layla

sudo -E -u www-data php occ trashbin:cleanup layla fred
sudo -E -u www-data php occ trashbin:cleanup --all-users
```

Usar `--verbose` para ver la cantidad de datos liberados por usuario. Hay que indicar un ID de usuario o `--all-users`; no pueden combinarse.

#### trashbin:expire

Hacer caducar los elementos de la papelera que superan el periodo de retención configurado, definido por `trashbin_retention_obligation` en `config.php`:

```
sudo -E -u www-data php occ trashbin:expire layla
sudo -E -u www-data php occ trashbin:expire
```

:::{note}
Este comando solo se ejecuta cuando hay configurado un periodo de retención personalizado. Si Nextcloud está configurado con caducidad automática (el valor predeterminado), el comando termina con un mensaje informativo y no hace nada; la caducidad automática la gestiona en su lugar el trabajo en segundo plano.
:::

Consultar {nc-doc}`admin_manual/configuration_files/file_versioning` para la configuración de la retención.

### Versiones de archivos

```
versions
 versions:cleanup                     delete stored file versions
 versions:expire                      expire file versions that exceed the configured retention period
```

#### versions:cleanup

Eliminar las versiones de archivos almacenadas de uno o varios usuarios, de todos los usuarios o de una ruta concreta:

```
sudo -E -u www-data php occ versions:cleanup layla
  Delete versions of   layla

sudo -E -u www-data php occ versions:cleanup layla fred
sudo -E -u www-data php occ versions:cleanup
```

Usar `--path` para limitar la eliminación a un directorio concreto. La ruta debe incluir el ID de usuario y `files/`:

```
sudo -E -u www-data php occ versions:cleanup \
  --path="/layla/files/Documents" layla
```

#### versions:expire

Hacer caducar las versiones de archivos que superan el periodo de retención configurado, definido por `versions_retention_obligation` en `config.php`:

```
sudo -E -u www-data php occ versions:expire layla
sudo -E -u www-data php occ versions:expire
```

:::{note}
Este comando solo se ejecuta cuando hay configurado un periodo de retención personalizado. Si Nextcloud está configurado con caducidad automática (el valor predeterminado), el comando termina y no hace nada; la caducidad automática la gestiona en su lugar el trabajo en segundo plano.
:::

Consultar {nc-doc}`admin_manual/configuration_files/file_versioning` para la configuración de la retención.

(nc-occ_sharing_label)=
### Compartición de archivos

```
sharing
 sharing:cleanup-remote-storages      clean up remote storage entries with no matching federated share
 sharing:delete-orphan-shares         delete shares where the owner no longer has file access
 sharing:expiration-notification      notify share initiators when a share expires the next day
 sharing:fix-share-owners             fix share owner after a legacy transfer-ownership operation
share
 share:list                           list available shares
```

#### share:list

Listar las comparticiones de toda la instancia. Sin opciones, lista todas las comparticiones:

```
sudo -E -u www-data php occ share:list
+----+-------+-------------------------------+------+-------+-----------+-------+
| id | file  | source-path                   | type | owner | recipient | by    |
+----+-------+-------------------------------+------+-------+-----------+-------+
| 1  | 42    | /layla/files/Documents/rep... | user | layla | fred      | layla |
+----+-------+-------------------------------+------+-------+-----------+-------+
```

Opciones de filtro:

- `--owner`: solo las comparticiones propiedad de un usuario concreto
- `--recipient`: solo las comparticiones con un destinatario concreto
- `--by`: solo las comparticiones iniciadas por un usuario concreto
- `--file`: solo las comparticiones de un archivo concreto (ruta o ID de archivo)
- `--parent`: solo las comparticiones de archivos dentro de una carpeta concreta
- `--recursive`: combinado con `--parent`, incluye las comparticiones anidadas
- `--type`: filtra por tipo de compartición: `user`, `group`, `link`, `email`, `remote`, `room`, `deck`
- `--status`: solo las comparticiones con un estado concreto

Usar `--output=json_pretty` para obtener una salida legible por máquina.

#### sharing:cleanup-remote-storages

Eliminar de la base de datos las entradas de almacenamiento `shared::` que no tienen una entrada correspondiente en la tabla `shares_external`. Estas entradas huérfanas quedan cuando se elimina una compartición federada sin la limpieza adecuada:

```
sudo -E -u www-data php occ sharing:cleanup-remote-storages
  5 remote storage(s) need(s) to be checked
  3 remote share(s) exist
  deleting shared::abc123 [14] ... deleted 1 storage
```

Usar `--dry-run` para previsualizar lo que se eliminaría sin hacer cambios:

```
sudo -E -u www-data php occ sharing:cleanup-remote-storages --dry-run
```

#### sharing:delete-orphan-shares

Eliminar las comparticiones cuyo propietario ha perdido el acceso al archivo compartido o cuyo archivo ya no existe:

```
sudo -E -u www-data php occ sharing:delete-orphan-shares
  /layla/files/Documents/report.pdf owned by layla
    file still exists but the share owner lost access to it,
    run occ info:file 42 for more information about the file
  Delete 1 orphan shares? [y/N]
```

Usar `--force` / `-f` para eliminar sin preguntar. Filtrar las comparticiones de un usuario concreto con `--owner` o las comparticiones con un usuario concreto con `--with`:

```
sudo -E -u www-data php occ sharing:delete-orphan-shares --owner layla
sudo -E -u www-data php occ sharing:delete-orphan-shares --with fred
```

#### sharing:expiration-notification

Enviar notificaciones dentro de la app a quienes iniciaron comparticiones que caducan al día siguiente. Ejecutarlo a diario mediante un trabajo cron para garantizar que las notificaciones lleguen a tiempo:

```
sudo -E -u www-data php occ sharing:expiration-notification
```

#### sharing:fix-share-owners

Corregir el propietario registrado de las comparticiones que quedaron dañadas por una operación `transfer-ownership` realizada en una versión antigua de Nextcloud. Usar `--dry-run` para previsualizar los cambios:

```
sudo -E -u www-data php occ sharing:fix-share-owners --dry-run
  Share with id 7 (target: /fred/files/report.pdf) can be
  updated to owner layla

sudo -E -u www-data php occ sharing:fix-share-owners
  Share with id 7 (target: /fred/files/report.pdf) updated to owner layla
  No broken shares detected
```

(nc-federation_sync_label)=
### Sincronización de federación

```
federation
 federation:sync-addressbooks         synchronize address books of all federated clouds
```

#### federation:sync-addressbooks

Sincronizar las libretas de direcciones compartidas de todos los servidores Nextcloud federados. Los servidores federados comparten las libretas de direcciones de usuarios para que los nombres de usuario se autocompleten en los diálogos de compartición. Ejecutar este comando para lanzar una sincronización inmediata en lugar de esperar al trabajo en segundo plano:

```
sudo -E -u www-data php occ federation:sync-addressbooks
```

(nc-files_external_label)=
### Archivos externos

```
files_external
 files_external:applicable            manage applicable users and groups for a mount
 files_external:backends              show available authentication and storage backends
 files_external:config                manage backend configuration for a mount
 files_external:create                create a new mount configuration
 files_external:delete                delete an external mount
 files_external:dependencies          check for missing dependencies needed for mounting external storages
 files_external:export                export mount configurations
 files_external:import                import mount configurations
 files_external:list                  list configured admin or personal mounts
 files_external:notify                listen for active update notifications for a configured external mount
 files_external:option                manage mount options for a mount
 files_external:scan                  scan an external storage for changed files
 files_external:verify                verify mount configuration
```

Gestionar los montajes de almacenamiento externo de Nextcloud. Los comandos que leen o escriben la configuración de los montajes operan sobre los mismos datos que la página de ajustes de administración **Almacenamiento externo**.

#### files_external:list

Listar los montajes configurados. Sin argumentos, lista los montajes de nivel de administración:

```
sudo -E -u www-data php occ files_external:list
+----+------------------+-----------+--------------+---------+--------+-------+
| ID | Mount Point      | Storage   | Auth. Type   | Config  | Status | Users |
+----+------------------+-----------+--------------+---------+--------+-------+
| 1  | /shared/data     | amazons3  | builtin      | valid   | ok     | all   |
+----+------------------+-----------+--------------+---------+--------+-------+
```

Listar los montajes personales de un usuario concreto:

```
sudo -E -u www-data php occ files_external:list layla
```

Usar `--output=json_pretty` para obtener una salida legible por máquina. Añadir `--show-password` para incluir las credenciales en la salida.

#### files_external:create

Crear una configuración de montaje nueva:

```
sudo -E -u www-data php occ files_external:create \
  /shared/photos amazons3 builtin::builtin \
  --config bucket=my-nextcloud-photos \
  --config region=eu-central-1 \
  --config key=AKIAIOSFODNN7EXAMPLE \
  --config secret=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

Argumentos:

- **mount-point**: la ruta dentro de Nextcloud (p. ej., `/shared/photos`)
- **storage-backend**: el identificador del tipo de almacenamiento (p. ej., `amazons3`, `sftp`, `smb`, `owncloud`)
- **auth-backend**: el método de autenticación (p. ej., `builtin::builtin`, `password::sessioncredentials`)

Usar `files_external:backends` para listar todos los backends de almacenamiento y de autenticación disponibles.

Para un montaje personal, indicar el usuario con `--user`:

```
sudo -E -u www-data php occ files_external:create \
  /my-s3 amazons3 builtin::builtin \
  --config bucket=layla-bucket \
  --user layla
```

#### files_external:config

Leer o escribir opciones individuales de configuración del backend de un montaje. Usar el ID de montaje que muestra `files_external:list`:

```
sudo -E -u www-data php occ files_external:config 1 get bucket
  my-nextcloud-photos

sudo -E -u www-data php occ files_external:config 1 set bucket new-bucket-name
```

#### files_external:applicable

Gestionar qué usuarios y grupos tienen acceso a un montaje:

```
sudo -E -u www-data php occ files_external:applicable 1 --add-user layla
sudo -E -u www-data php occ files_external:applicable 1 --add-group milliways
sudo -E -u www-data php occ files_external:applicable 1 --remove-user layla
sudo -E -u www-data php occ files_external:applicable 1 --remove-group milliways
```

Un montaje sin usuarios ni grupos asignados está disponible para todos los usuarios.

#### files_external:option

Leer o escribir opciones de montaje como `enable_sharing` o `filesystem_check_changes`:

```
sudo -E -u www-data php occ files_external:option 1 get enable_sharing
sudo -E -u www-data php occ files_external:option 1 set enable_sharing true
```

#### files_external:verify

Probar la configuración de un montaje e informar de si se puede establecer una conexión:

```
sudo -E -u www-data php occ files_external:verify 1
  +----------+---------+
  | Result   | Message |
  +----------+---------+
  | success  |         |
  +----------+---------+
```

Indicar pares clave-valor de configuración adicionales (p. ej., credenciales) con `--config` cuando la configuración almacenada está incompleta:

```
sudo -E -u www-data php occ files_external:verify 1 \
  --config user=layla --config password=secret
```

#### files_external:delete

Eliminar una configuración de montaje:

```
sudo -E -u www-data php occ files_external:delete 1
```

El comando pide confirmación. Usar `--yes` para omitir la pregunta.

#### files_external:scan

Analizar un almacenamiento externo en busca de archivos modificados y actualizar la caché de archivos. Es útil para los backends de almacenamiento que no admiten notificaciones de cambios activas:

```
sudo -E -u www-data php occ files_external:scan 1
```

Para los montajes que usan credenciales de sesión, indicarlas con `--user` y `--password`:

```
sudo -E -u www-data php occ files_external:scan 1 \
  --user layla --password secret
```

#### files_external:export

Exportar todos los montajes de administración a JSON:

```
sudo -E -u www-data php occ files_external:export > mounts.json
```

Exportar los montajes personales de un usuario concreto:

```
sudo -E -u www-data php occ files_external:export layla > layla-mounts.json
```

Usar el JSON exportado con `files_external:import` para replicar la configuración en otra instancia de Nextcloud.

#### files_external:import

Importar configuraciones de montaje desde un archivo JSON generado por `files_external:export`:

```
sudo -E -u www-data php occ files_external:import mounts.json
```

Importar como montajes personales de un usuario concreto:

```
sudo -E -u www-data php occ files_external:import \
  --user layla layla-mounts.json
```

#### files_external:backends

Listar todos los backends de almacenamiento y de autenticación disponibles:

```
sudo -E -u www-data php occ files_external:backends
```

Filtrar por tipo:

```
sudo -E -u www-data php occ files_external:backends storage
sudo -E -u www-data php occ files_external:backends authentication
```

Usar `--output=json_pretty` para inspeccionar el esquema completo de capacidades y de configuración de cada backend.

#### files_external:notify

Escuchar las notificaciones de cambios activas de un montaje externo que admite eventos de actualización por push (p. ej., SMB con inotify):

```
sudo -E -u www-data php occ files_external:notify 1
```

Es un proceso de larga duración; ejecutarlo bajo un supervisor de procesos o en un servicio de systemd dedicado.

#### files_external:dependencies

Comprobar si faltan extensiones de PHP o paquetes del sistema necesarios para usar los backends de almacenamiento externo configurados:

```
sudo -E -u www-data php occ files_external:dependencies
```

(nc-trashbin_label)=
### Papelera

:::{note}
Estos comandos solo están disponibles cuando la app «Archivos eliminados» (`files_trashbin`) está activada.
:::

```
trashbin
 trashbin:cleanup  remove deleted files
 trashbin:expire   expire deleted files according to the configured retention policy
 trashbin:restore  restore all deleted files according to the given filters
 trashbin:size     configure or show the target trashbin size
```

#### trashbin:cleanup

Eliminar todos los archivos eliminados de todos los usuarios o de usuarios concretos:

```
sudo -E -u www-data php occ trashbin:cleanup
sudo -E -u www-data php occ trashbin:cleanup layla fred
```

#### trashbin:expire

Aplicar la política de retención de la papelera configurada y eliminar los archivos que han superado la antigüedad máxima de retención. De forma predeterminada se ejecuta para todos los usuarios, o bien para usuarios concretos:

```
sudo -E -u www-data php occ trashbin:expire
sudo -E -u www-data php occ trashbin:expire layla
```

#### trashbin:restore

Restaurar archivos eliminados según los filtros indicados. Restaurar todos los archivos eliminados de todos los usuarios:

```
sudo -E -u www-data php occ trashbin:restore --all-users
```

Restaurar los archivos eliminados de usuarios concretos:

```
sudo -E -u www-data php occ trashbin:restore layla
```

Usar `--scope` para limitar la restauración a un ámbito concreto; uno de `user`, `groupfolders` o `all` (predeterminado: `user`):

```
sudo -E -u www-data php occ trashbin:restore --scope groupfolders layla
```

Usar `--since` y `--until` para limitar la restauración a los archivos eliminados dentro de un intervalo de tiempo. Ambas opciones aceptan cualquier formato admitido por `strtotime` de PHP:

```
sudo -E -u www-data php occ trashbin:restore --scope all \
  --since "2026-08-01 11:55:22" --until "2026-08-02 01:33:00" layla
```

Usar `--dry-run` para simular la restauración sin hacer ningún cambio:

```
sudo -E -u www-data php occ trashbin:restore --dry-run --all-users
```

:::{note}
Usar `-v` o `-vv` para ver más detalles sobre el proceso de restauración y sobre por qué pueden omitirse algunos archivos.
:::

#### trashbin:size

Mostrar o configurar el tamaño objetivo de la papelera. Si se ejecuta sin argumentos, muestra el tamaño configurado actualmente:

```
sudo -E -u www-data php occ trashbin:size
```

Establecer el tamaño predeterminado de la papelera para todos los usuarios:

```
sudo -E -u www-data php occ trashbin:size 10GB
```

Establecer el tamaño de la papelera de un usuario concreto:

```
sudo -E -u www-data php occ trashbin:size --user layla 5GB
```

(nc-versions_label)=
### Versiones

:::{note}
Estos comandos solo están disponibles cuando la app «Versiones» (`files_versions`) está activada.
:::

```
versions
 versions:cleanup  delete file versions
 versions:expire   expire file versions according to the configured retention policy
```

#### versions:cleanup

Eliminar todas las versiones de archivos de todos los usuarios o de usuarios concretos. Usar `--path` para limitar la eliminación a una ruta concreta:

```
sudo -E -u www-data php occ versions:cleanup
sudo -E -u www-data php occ versions:cleanup layla
sudo -E -u www-data php occ versions:cleanup layla --path="/files/Documents"
```

#### versions:expire

Aplicar la política de retención de versiones configurada y eliminar las versiones que han superado la antigüedad máxima de retención. De forma predeterminada se ejecuta para todos los usuarios, o bien para usuarios concretos:

```
sudo -E -u www-data php occ versions:expire
sudo -E -u www-data php occ versions:expire layla
```

(nc-integrity_check_label)=
### Comprobación de integridad

```
integrity
 integrity:check-app                  check integrity of an app using a signature
 integrity:check-core                 check core integrity using a signature
 integrity:sign-app                   sign an app using a private key
```

Las apps con la etiqueta `Featured` deben estar firmadas por {vendor}`Nextcloud`. Las apps destacadas sin firmar no pueden instalarse.

#### integrity:check-app

Comprobar la integridad de una app con su firma:

```
sudo -E -u www-data php occ integrity:check-app contacts
```

Comprobar todas las apps instaladas a la vez:

```
sudo -E -u www-data php occ integrity:check-app --all
```

Cuando la app supera la comprobación, el comando no produce ninguna salida (usar `-v` para confirmarlo). Cuando falla, se lista cada error de integridad con detalles. Usar `--path` para indicar una ubicación de la app no estándar:

```
sudo -E -u www-data php occ integrity:check-app \
  --path=/var/www/nextcloud/apps/myapp myapp
```

Las apps sin archivo `signature.json` se omiten con un mensaje informativo.

#### integrity:check-core

Comprobar la integridad del núcleo de Nextcloud con su firma:

```
sudo -E -u www-data php occ integrity:check-core
```

#### integrity:sign-app

Firmar una app con una clave privada antes de distribuirla. Requiere la clave y el certificado obtenidos mediante el proceso de firma de {vendor}`Nextcloud`:

```
sudo -E -u www-data php occ integrity:sign-app \
  --path=/path/to/app \
  --privateKey=/path/to/myapp.key \
  --certificate=/path/to/myapp.crt
```

Consultar [Firma de código](https://docs.nextcloud.com/server/latest/developer_manual/app_publishing_maintenance/code_signing.html) en el manual de desarrollo para el proceso de firma completo.
````
