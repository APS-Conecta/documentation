---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Comandos occ del cifrado en el servidor: estado, cifrar y descifrar todo, módulos, almacenamiento de claves, clave maestra y reparación."
---
(nc-encryption_label)=
# Comandos de cifrado

## Resumen

Esta página es la referencia de los comandos `occ` que gestionan el cifrado en el servidor: activarlo y desactivarlo, cifrar y descifrar todos los datos, elegir el módulo, mover el almacenamiento de claves, cambiar el modo de clave maestra, reparar claves y migrar el formato heredado. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/occ_encryption.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los comandos `encryption` gestionan el cifrado en el servidor, las claves de cifrado y los módulos de cifrado. Los comandos principales están siempre disponibles. Los comandos que operan sobre el propio módulo de cifrado (clave maestra, reparación de claves, migración del formato heredado) requieren que la app **Cifrado** (`encryption`) esté activada.

:::{note}
Para una guía completa de la configuración del cifrado en el servidor, consultar {nc-doc}`admin_manual/configuration_files/encryption_configuration`.
:::

```
encryption
 encryption:change-key-storage-root      change key storage root
 encryption:clean-orphaned-keys          scan the keys storage for orphaned keys and remove them
 encryption:decrypt-all                  disable server-side encryption and decrypt all files
 encryption:disable                      disable encryption
 encryption:disable-master-key           disable the master key and use per-user keys instead
 encryption:drop-legacy-filekey          scan the files for the legacy filekey format using RC4 and get rid of it
 encryption:enable                       enable encryption
 encryption:enable-master-key            enable the master key
 encryption:encrypt-all                  encrypt all files for all users
 encryption:fix-encrypted-version        fix the encrypted version if the encrypted file(s) are not downloadable
 encryption:fix-key-location             fix the location of encryption keys for external storage
 encryption:list-modules                 list all available encryption modules
 encryption:migrate-key-storage-format   migrate the format of the key storage to a newer format
 encryption:recover-user                 recover user data in case of password loss
 encryption:scan:legacy-format           scan the files for the legacy format
 encryption:set-default-module           set the encryption default module
 encryption:show-key-storage-root        show current key storage root
 encryption:status                       lists the current status of encryption
```

### Estado y control

#### encryption:status

Mostrar si el cifrado está activado y qué módulo está activo:

```
sudo -E -u www-data php occ encryption:status
  - enabled: false
  - defaultModule: OC_DEFAULT_MODULE
```

Usar `--output=json_pretty` para obtener una salida legible por máquina.

#### encryption:enable

Activar el cifrado en el servidor. Antes hay que activar la app **Cifrado** y configurar un módulo predeterminado:

```
sudo -E -u www-data php occ app:enable encryption
sudo -E -u www-data php occ encryption:enable
  Encryption enabled

  Default module: OC_DEFAULT_MODULE
```

#### encryption:disable

Desactivar el cifrado en el servidor. Esto solo desactiva el indicador de cifrado: no descifra ningún archivo:

```
sudo -E -u www-data php occ encryption:disable
  Encryption disabled
```

Para descifrar también todos los archivos existentes, ejecutar después `encryption:decrypt-all`.

### Cifrar y descifrar todos los datos

#### encryption:encrypt-all

Cifrar todos los archivos de todos los usuarios. El cifrado debe estar activado antes de ejecutar este comando. El comando gestiona internamente el modo de mantenimiento: **no** activar antes el modo de mantenimiento, ya que el comando falla si ya está activo:

```
sudo -E -u www-data php occ encryption:encrypt-all
  You are about to encrypt all files stored in your Nextcloud installation.
  Depending on the number of available files, and their size, this may take quite some time.
  Please ensure that no user accesses their files during this time!
  Note: The encryption module you use determines which files get encrypted.

  Do you really want to continue? (y/n)
```

El comando requiere un terminal interactivo (TTY). Si se ejecuta dentro de un contenedor Docker, usar `docker exec -it`.

#### encryption:decrypt-all

Descifrar todos los archivos de todos los usuarios o de un solo usuario. El comando gestiona internamente el modo de mantenimiento: **no** activar antes el modo de mantenimiento:

```
sudo -E -u www-data php occ encryption:decrypt-all
sudo -E -u www-data php occ encryption:decrypt-all layla
```

Al descifrar los archivos de todos los usuarios, el cifrado en el servidor se desactiva automáticamente. Al descifrar los de un solo usuario, el cifrado sigue activado para los demás.

Según el módulo de cifrado que se use, el descifrado puede requerir:

- **Modo de clave maestra**: no se necesitan credenciales adicionales.
- **Modo de claves por usuario**: el usuario debe haber activado la clave de recuperación en su página de ajustes personales.

El comando requiere un terminal interactivo (TTY). Si se ejecuta dentro de un contenedor Docker, usar `docker exec -it`.

### Módulos de cifrado

#### encryption:list-modules

Listar todos los módulos de cifrado disponibles. El módulo predeterminado activo se marca con `[default*]`:

```
sudo -E -u www-data php occ encryption:list-modules
  - OC_DEFAULT_MODULE: Default encryption module [default*]
```

#### encryption:set-default-module

Establecer el módulo de cifrado predeterminado. El modo de mantenimiento debe estar desactivado:

```
sudo -E -u www-data php occ encryption:set-default-module OC_DEFAULT_MODULE
  Set default module to "OC_DEFAULT_MODULE"
```

### Almacenamiento de claves

#### encryption:show-key-storage-root

Mostrar dónde se almacenan las claves de cifrado:

```
sudo -E -u www-data php occ encryption:show-key-storage-root
  Current key storage root:  default storage location (data/)
```

#### encryption:change-key-storage-root

Mover las claves de cifrado a otro directorio. Antes de ejecutar el comando, el directorio de destino debe existir y el usuario del servidor web debe poder escribir en él:

```
sudo -E -u www-data php occ encryption:change-key-storage-root /etc/nextcloud/keys
  Change key storage root from default storage location to /etc/nextcloud/keys
  Start to move keys:
  [============================]
  Key storage root successfully changed to /etc/nextcloud/keys
```

Omitir el argumento para restablecer la raíz del almacenamiento de claves a la ubicación predeterminada (`data/`). El comando pide confirmación:

```
sudo -E -u www-data php occ encryption:change-key-storage-root
  No storage root given, do you want to reset the key storage root to the default location? (y/n)
```

#### encryption:migrate-key-storage-format

Migrar el almacenamiento de claves al formato actual (envuelto en JSON y vuelto a cifrar con el secreto del servidor). Ejecutarlo una vez después de actualizar desde una instalación que usaba el formato de claves heredado:

```
sudo -E -u www-data php occ encryption:migrate-key-storage-format
  Updating key storage format
  Start to update the keys:
  [============================]
  Key storage format successfully updated
```

### Clave maestra

La clave maestra cifra todos los datos de los usuarios con una única clave gestionada por el servidor. Es la configuración recomendada para instalaciones nuevas, porque simplifica la gestión de claves y permite que la administración descifre sin las contraseñas de cada usuario. La clave maestra se activa de forma predeterminada cuando se activa por primera vez la app Cifrado.

Ambos comandos solo están disponibles cuando la app **Cifrado** está activada.

:::{warning}
Cambiar entre el modo de clave maestra y el de claves por usuario solo es seguro en una **instalación nueva sin datos cifrados existentes**. Si se cambia de modo en una instancia que ya tiene archivos cifrados, esos archivos quedarán inaccesibles de forma permanente: el nuevo modo busca claves que nunca se crearon para los datos existentes. **No hay forma de recuperarlos.** Ejecutar siempre primero `encryption:decrypt-all` si hay que cambiar de modo en una instalación existente.
:::

:::{note}
A pesar de la advertencia que muestran ambos comandos («no way to enable/disable it again»), el cambio es técnicamente reversible mientras no existan datos cifrados. La advertencia pretende transmitir que no se puede cambiar de modo de forma segura una vez que los usuarios tienen datos.
:::

#### encryption:enable-master-key

Activar la clave maestra. Usarlo solo en una **instalación nueva sin datos cifrados existentes**. El comando pide confirmación:

```
sudo -E -u www-data php occ encryption:enable-master-key
  Master key successfully enabled.
```

#### encryption:disable-master-key

Desactivar la clave maestra y volver a las claves por usuario. Usarlo solo en una **instalación nueva sin datos cifrados existentes**. El comando pide confirmación:

```
sudo -E -u www-data php occ encryption:disable-master-key
  Master key successfully disabled.
```

Cambiar a claves por usuario tiene las siguientes consecuencias:

- **Rendimiento**: las operaciones con claves por usuario son más lentas. La clave de cada usuario debe derivarse individualmente en cada acceso a un archivo.
- **Perder la contraseña significa perder los datos**: sin la clave maestra no hay forma de descifrar desde la administración. Cada usuario debe activar la clave de recuperación en su página de ajustes personales *antes* de perder su contraseña. Sin ella, `encryption:recover-user` no sirve de nada y los archivos no pueden recuperarse.
- **La administración ya no puede descifrar**: los administradores no pueden descifrar ni acceder a los archivos de un usuario sin la contraseña de ese usuario o una clave de recuperación configurada previamente.

### Mantenimiento y reparación

#### encryption:clean-orphaned-keys

Buscar en el almacenamiento de claves las claves que ya no tienen un archivo correspondiente y eliminarlas. Opcionalmente, limitar la búsqueda a un solo usuario:

```
sudo -E -u www-data php occ encryption:clean-orphaned-keys
sudo -E -u www-data php occ encryption:clean-orphaned-keys layla
```

Cuando encuentra claves huérfanas, el comando las lista y pregunta de forma interactiva si se eliminan todas, algunas concretas o ninguna:

```
sudo -E -u www-data php occ encryption:clean-orphaned-keys layla
  Key storage scan for layla
  ==========================

  Orphaned key found: /layla/files_encryption/keys/files/old-doc.pdf/OC_DEFAULT_MODULE/fileKey
  Do you want to delete all orphaned keys? (y/n)
```

Si no encuentra claves huérfanas, el comando termina sin mostrar nada.

#### encryption:fix-encrypted-version

Corregir el contador de versión cifrada en la caché de archivos cuando los archivos cifrados no pueden descargarse. Requiere cifrado con **clave maestra**.

Ejecutarlo para un solo usuario:

```
sudo -E -u www-data php occ encryption:fix-encrypted-version layla
  Verifying the content of file "/layla/files/Documents/report.pdf"
  The file "/layla/files/Documents/report.pdf" is: OK
```

Ejecutarlo para todos los usuarios:

```
sudo -E -u www-data php occ encryption:fix-encrypted-version --all
  Processing files for layla
  Verifying the content of file "/layla/files/Documents/report.pdf"
  The file "/layla/files/Documents/report.pdf" is: OK
```

Cuando encuentra un archivo dañado, el comando prueba a disminuir y luego a aumentar el contador de versión cifrada hasta que el archivo puede leerse:

```
Attempting to fix the path: "/layla/files/Documents/broken.pdf"
Decrement the encrypted version to 2
Fixed the file: "/layla/files/Documents/broken.pdf" with version 2
```

Usar `-p` / `--path` para limitar la búsqueda a un directorio concreto:

```
sudo -E -u www-data php occ encryption:fix-encrypted-version layla --path="/Documents"
```

#### encryption:fix-key-location

Corregir la ubicación de las claves de cifrado de los archivos en montajes de almacenamiento externo. Ejecutarlo cuando los usuarios no puedan acceder a archivos del almacenamiento externo después de una migración:

```
sudo -E -u www-data php occ encryption:fix-key-location layla
  Migrating key for /layla/files/ExternalDrive/report.pdf ✓
```

Usar `--dry-run` para listar los archivos que necesitan migración sin hacer ningún cambio:

```
sudo -E -u www-data php occ encryption:fix-key-location --dry-run layla
  /layla/files/ExternalDrive/report.pdf needs migration
```

#### encryption:recover-user

Recuperar los archivos de un usuario después de que haya perdido la contraseña. Solo está disponible en el modo de **claves por usuario** (no se aplica cuando la clave maestra está activada). El usuario debe haber activado la clave de recuperación en sus ajustes personales antes de perder la contraseña.

El comando pide la contraseña de la clave de recuperación y la nueva contraseña de inicio de sesión:

```
sudo -E -u www-data php occ encryption:recover-user layla
  Please enter the recovery key password:
  Please enter the new login password for the user:
  Start to recover users files... This can take some time...Done.
```

### Migración del formato heredado

#### encryption:drop-legacy-filekey

Buscar en todos los archivos el formato heredado de clave de archivo RC4 y migrarlos al formato actual. Requiere cifrado con **clave maestra**. Los archivos que este comando no migre se migrarán automáticamente en su próxima escritura. Ejecutar este comando de antemano también convierte los archivos antiguos codificados en base64 a formato binario, lo que ahorra aproximadamente un 33 % de espacio en disco:

```
sudo -E -u www-data php occ encryption:drop-legacy-filekey
  Scanning all files for legacy filekey
  Scanning all files for layla
  All scanned files are properly encrypted.
```

#### encryption:scan:legacy-format

Buscar en todos los archivos el formato de cifrado heredado. Usarlo para determinar si algún archivo necesita todavía migración antes de desactivar la compatibilidad con el formato heredado:

```
sudo -E -u www-data php occ encryption:scan:legacy-format
  Scanning all files for legacy encryption
  Scanning all files for layla
  All scanned files are properly encrypted. You can disable the legacy compatibility mode.
```

Si se encuentran archivos con el formato heredado, se listan sus rutas. Ejecutar `encryption:drop-legacy-filekey` para migrarlos.
````
