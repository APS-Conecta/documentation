---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Comandos occ para gestionar cuentas de usuario, grupos, la autenticación de dos factores y las etiquetas del sistema, con ejemplos y su salida."
---
# Comandos de usuarios y grupos

## Resumen

Esta página es la referencia de los comandos `occ` que crean y gestionan las cuentas de usuario y sus tokens de autenticación (`user`), los grupos y sus miembros (`group`), la autenticación de dos factores (`twofactorauth`) y las etiquetas del sistema (`tag`), con ejemplos y su salida. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/occ_users.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
(nc-user_commands_label)=
### Comandos de usuario

Los comandos `user` crean y gestionan cuentas de usuario, restablecen contraseñas, gestionan los tokens de autenticación e informan sobre la actividad de los usuarios:

```
user
 user:add                            adds a user
 user:add-app-password               (deprecated) alias for user:auth-tokens:add
 user:auth-tokens:add                add an app password for an account
 user:auth-tokens:delete             delete an authentication token
 user:auth-tokens:list               list authentication tokens for an account
 user:clear-avatar-cache             clear avatar cache
 user:delete                         deletes the specified user
 user:disable                        disables the specified user
 user:enable                         enables the specified user
 user:info                           show information about a user
 user:keys:verify                    verify the stored public key matches the stored private key
 user:lastseen                       show when a user was last logged in
 user:list                           list all registered users
 user:profile                        read and modify user profile data
 user:report                         show how many users have access
 user:resetpassword                  reset the password for a user
 user:setting                        read and modify user settings
 user:sync-account-data              sync user backend data to the accounts table
 user:welcome                        send the welcome email to a user
```

#### user:add

Crear un usuario nuevo con un nombre mostrado, un nombre de inicio de sesión y, opcionalmente, su pertenencia a grupos:

```
user:add [--password-from-env] [--generate-password] [--display-name[="..."]] [-g|--group[="..."]] [--email EMAIL] uid
```

`display-name` corresponde al **Nombre completo** de la página Usuarios de la interfaz web de Nextcloud, y `uid` es su **Nombre de usuario** (nombre de inicio de sesión). Los grupos que no existen se crean automáticamente:

```
sudo -E -u www-data php occ user:add --display-name="Layla Smith" \
  --group="users" --group="db-admins" layla
  Enter password:
  Confirm password:
  The user "layla" was created successfully
  Display name set to "Layla Smith"
  User "layla" added to group "users"
  User "layla" added to group "db-admins"
```

`--password-from-env` lee la contraseña de la variable de entorno `OC_PASS`. Así la contraseña no aparece en la lista de procesos y se puede automatizar con scripts la creación de varios usuarios. Hay que tener en cuenta que `sudo` elimina las variables de entorno de forma predeterminada; la opción `-E` las conserva, como se muestra en el ejemplo siguiente:

```
export OC_PASS=newpassword
sudo -E -u www-data php occ user:add --password-from-env \
  --display-name="Layla Smith" --group="users" layla
The user "layla" was created successfully
Display name set to "Layla Smith"
User "layla" added to group "users"
```

`--generate-password` establece una contraseña generada de forma segura que nunca se muestra en la salida. Combinada con `--email`, crea un usuario con una contraseña temporal y le envía un correo electrónico de bienvenida:

```
sudo -E -u www-data php occ user:add layla --generate-password --email layla@example.tld
  The account "layla" was created successfully
  Welcome email sent to layla@example.tld
```

`--email` establece la dirección de correo electrónico del usuario y envía un correo electrónico de bienvenida si `newUser.sendEmail` está establecido en `yes` en la configuración de la app `core`, o si no está establecido en absoluto (`yes` es el valor predeterminado):

```
sudo -E -u www-data php occ user:add layla --email layla@example.tld
  Enter password:
  Confirm password:
  The account "layla" was created successfully
  Welcome email sent to layla@example.tld
```

#### user:resetpassword

Restablecer la contraseña de cualquier usuario, incluidos los administradores (ver {nc-doc}`admin_manual/configuration_user/reset_admin_password`):

```
sudo -E -u www-data php occ user:resetpassword layla
  Enter a new password:
  Confirm the new password:
  Successfully reset password for layla
```

Borrar la contraseña de un usuario con `--no-password`:

```
sudo -E -u www-data php occ user:resetpassword --no-password layla
  Are you sure you want to clear the password for layla?
  Successfully reset password for layla
```

También se puede usar `--password-from-env` para restablecer contraseñas de forma no interactiva:

```
export OC_PASS=newpassword
sudo -E -u www-data php occ user:resetpassword --password-from-env layla
  Successfully reset password for layla
```

#### user:delete

Eliminar un usuario:

```
sudo -E -u www-data php occ user:delete layla
```

#### user:disable y user:enable

(nc-disable_user_label)=
Desactivar un usuario. Sus sesiones activas se invalidarán en un plazo de 5 minutos. Para invalidar las sesiones de inmediato, usar `user:auth-tokens:delete` antes o después de desactivar la cuenta:

```
sudo -E -u www-data php occ user:disable <username>
```

Volver a activar un usuario desactivado:

```
sudo -E -u www-data php occ user:enable <username>
```

#### user:lastseen

Mostrar el inicio de sesión más reciente de un usuario concreto:

```
sudo -E -u www-data php occ user:lastseen layla
  layla's last login: 2024-03-20 17:18
```

Mostrar el inicio de sesión más reciente de todos los usuarios:

```
sudo -E -u www-data php occ user:lastseen --all
  albert's last login: 2024-03-18 10:30
  bob has never logged in.
  layla's last login: 2024-03-20 17:18
  stephanie's last login: 2024-01-11 13:26
```

#### user:list

Listar todos los usuarios registrados. De forma predeterminada, la salida se limita a 500 usuarios; usar `--limit` y `--offset` para recorrer por páginas conjuntos más grandes:

```
sudo -E -u www-data php occ user:list
  - admin: admin
  - layla: Layla Smith
  - fred: Fred Jones
```

Usar `--disabled` para listar solo los usuarios desactivados, y `--info` para incluir detalles adicionales del backend.

#### user:info

Mostrar los detalles de la cuenta de un usuario, incluidos el nombre mostrado, el correo electrónico, los grupos, la cuota y el uso de almacenamiento:

```
sudo -E -u www-data php occ user:info layla
  - user_id: layla
  - display_name: Layla Smith
  - email: layla@example.tld
  - cloud_id: layla@cloud.example.tld
  - enabled: true
  - groups:
    - users
    - db-admins
  - quota: none
  - storage:
    - free: 162409623552
    - used: 1110
    - total: 162409624662
    - relative: 0
    - quota: -3
  - first_seen: 2024-03-01T08:44:46+00:00
  - last_seen: 2024-03-20T17:18:00+00:00
  - user_directory: /var/www/nextcloud/data/layla
  - backend: Database
```

#### user:profile

Leer las propiedades del perfil de un usuario:

```
sudo -E -u www-data php occ user:profile layla
  - displayname: Layla Smith
  - address: Berlin
  - email: layla@example.tld
  - profile_enabled: 1
  - pronouns: they/them
```

Obtener una sola propiedad del perfil:

```
sudo -E -u www-data php occ user:profile layla address
  Berlin
```

Establecer una propiedad del perfil:

```
sudo -E -u www-data php occ user:profile layla address Stuttgart
```

Eliminar una propiedad del perfil:

```
sudo -E -u www-data php occ user:profile layla address --delete
```

#### user:setting

Leer los ajustes de un usuario:

```
sudo -E -u www-data php occ user:setting layla
  - core:
    - lang: en
  - login:
    - lastLogin: 1465910968
  - settings:
    - email: layla@example.tld
```

Filtrar por app:

```
sudo -E -u www-data php occ user:setting layla core
  - core:
    - lang: en
```

Obtener un solo ajuste:

```
sudo -E -u www-data php occ user:setting layla core lang
en
```

Establecer un ajuste:

```
sudo -E -u www-data php occ user:setting layla settings email "new-layla@example.tld"
```

Eliminar un ajuste:

```
sudo -E -u www-data php occ user:setting layla settings email --delete
```

#### user:report

Mostrar el recuento de todos los usuarios, incluidos los usuarios de backends de autenticación externos, como LDAP:

```
sudo -E -u www-data php occ user:report
+------------------+----+
| User Report      |    |
+------------------+----+
| Database         | 12 |
| LDAP             | 86 |
|                  |    |
| total users      | 98 |
|                  |    |
| user directories | 2  |
| active users     | 15 |
| disabled users   | 0  |
+------------------+----+
```

Los usuarios activos son los que han iniciado sesión al menos una vez. Los usuarios que nunca han iniciado sesión no se cuentan como activos ni como desactivados. Algunos backends no admiten el recuento de usuarios y pueden aparecer con cero.

#### user:auth-tokens:list

Listar todos los tokens de autenticación activos (sesiones y contraseñas de aplicación) de un usuario:

```
sudo -E -u www-data php occ user:auth-tokens:list layla
+----+------------------+---------------------------+-----------+------------+
| id | name             | lastActivity              | type      | scope      |
+----+------------------+---------------------------+-----------+------------+
| 42 | Firefox on Linux | 2024-03-20T17:18:00+00:00 | temporary | filesystem |
| 47 | Backup script    | 2024-03-19T08:00:00+00:00 | permanent | filesystem |
+----+------------------+---------------------------+-----------+------------+
```

Usar `--output=json` o `--output=json_pretty` para obtener una salida legible por máquina.

#### user:auth-tokens:add

Crear una contraseña de aplicación para un usuario. Si no se proporciona la contraseña de inicio de sesión, el token generado tendrá capacidades limitadas (las operaciones que requieren la contraseña de inicio de sesión fallarán):

```
sudo -E -u www-data php occ user:auth-tokens:add --name="Backup script" layla
  Enter password:
  app password: kFrH9-TXk4s-gUoOQ-KOVH8
```

Usar `--password-from-env` para leer la contraseña de inicio de sesión de `NC_PASS` de forma no interactiva:

```
export NC_PASS=userpassword
sudo -E -u www-data php occ user:auth-tokens:add --name="CI runner" \
  --password-from-env layla
```

#### user:auth-tokens:delete

Eliminar un token concreto por su ID (obtenido con `user:auth-tokens:list`):

```
sudo -E -u www-data php occ user:auth-tokens:delete layla 47
```

Eliminar todos los tokens de un usuario que no se han usado desde una fecha dada:

```
sudo -E -u www-data php occ user:auth-tokens:delete layla \
  --last-used-before="2024-01-01"
```

#### user:clear-avatar-cache

Borrar las imágenes de avatar en caché de todos los usuarios. Es útil después de cambiar los ajustes de almacenamiento de avatares o después de migrar datos de usuario:

```
sudo -E -u www-data php occ user:clear-avatar-cache
```

#### user:keys:verify

Verificar que la clave pública almacenada de un usuario coincide con su clave privada almacenada. Devuelve una confirmación o un aviso de discrepancia. Es útil para diagnosticar problemas del cifrado de extremo a extremo:

```
sudo -E -u www-data php occ user:keys:verify layla
  Stored public key matches stored private key
```

#### user:sync-account-data

Sincronizar los datos de usuario de los backends de usuario configurados (LDAP, SAML, etc.) con la tabla de cuentas de Nextcloud. Es útil después de cambios en el backend, para asegurar que los datos del perfil, las direcciones de correo electrónico y los nombres mostrados estén al día:

```
sudo -E -u www-data php occ user:sync-account-data
  layla - updated
```

Usar `--limit` y `--offset` para procesar los usuarios por lotes.

#### user:welcome

Enviar el correo electrónico de bienvenida a un usuario. La instancia debe tener una configuración de correo electrónico que funcione:

```
sudo -E -u www-data php occ user:welcome layla
```

Añadir `--reset-password` para incluir en el correo electrónico un enlace para restablecer la contraseña:

```
sudo -E -u www-data php occ user:welcome --reset-password layla
```

(nc-group_commands_label)=
### Comandos de grupo

Los comandos `group` crean y gestionan los grupos y sus miembros:

```
group
 group:add                           add a group
 group:adduser                       add a user to a group
 group:delete                        remove a group
 group:info                          show information about a group
 group:list                          list configured groups
 group:removeuser                    remove a user from a group
```

#### group:add

Crear un grupo nuevo:

```
sudo -E -u www-data php occ group:add milliways
```

#### group:adduser y group:removeuser

Añadir uno o varios usuarios existentes al grupo indicado con el comando `group:adduser`. La sintaxis es:

```
group:adduser <gid> <uid1> [uid2 ... uidN]
```

Este ejemplo añade los usuarios «denis», «dora» y «daisy» al grupo existente «milliways»:

```
sudo -E -u www-data php occ group:adduser milliways denis dora daisy
```

Se pueden quitar uno o varios usuarios del grupo con el comando `group:removeuser`. Este ejemplo quita los usuarios existentes «denis», «dora» y «daisy» del grupo existente «milliways»:

```
sudo -E -u www-data php occ group:removeuser milliways denis dora daisy
```

#### group:delete

Eliminar un grupo. Esto no elimina a los usuarios del grupo. El grupo `admin` no se puede eliminar:

```
sudo -E -u www-data php occ group:delete milliways
```

#### group:list

Listar los grupos configurados. Opcionalmente, filtrar por una cadena de búsqueda:

```
sudo -E -u www-data php occ group:list
  - admin:
    - admin
  - milliways:
    - layla
  - users:
    - layla

sudo -E -u www-data php occ group:list milli
  - milliways:
    - layla
```

Usar `--limit` y `--offset` para recorrer por páginas un gran número de grupos.
Usar `--info` para incluir el backend de cada grupo.
Usar `--output=json` o `--output=json_pretty` para obtener una salida legible por máquina.

#### group:info

Mostrar los detalles de un grupo, incluidos sus miembros y su backend:

```
sudo -E -u www-data php occ group:info admin
  - groupID: admin
  - displayName: admin
  - backends:
    - Database
```

Usar `--output=json_pretty` para obtener una salida legible por máquina.

(nc-two_factor_auth_label)=
### Autenticación de dos factores

Los comandos `twofactorauth` gestionan la imposición obligatoria de la autenticación de dos factores (2FA) y el estado de los proveedores:

```
twofactorauth
 twofactorauth:cleanup               clean up provider associations for a removed provider
 twofactorauth:disable               disable 2FA for a user (provider-specific)
 twofactorauth:enable                enable 2FA for a user (provider-specific)
 twofactorauth:enforce               enforce or disable mandatory 2FA globally or per group
 twofactorauth:state                 show the 2FA state for a user
```

#### twofactorauth:disable y twofactorauth:enable

Si un usuario pierde el acceso a su segundo factor (por ejemplo, por la pérdida del teléfono), un administrador puede desactivar la 2FA de ese usuario para un proveedor concreto:

```
sudo -E -u www-data php occ twofactorauth:disable <uid> <provider_id>
```

Volver a activar la 2FA del usuario:

```
sudo -E -u www-data php occ twofactorauth:enable <uid> <provider_id>
```

:::{note}
No todos los proveedores de 2FA permiten activarla o desactivarla por usuario mediante occ.
:::

#### twofactorauth:enforce

Imponer la 2FA a todos los usuarios:

```
sudo -E -u www-data php occ twofactorauth:enforce --on
  Two-factor authentication is enforced for all users
```

Imponer la 2FA solo a grupos concretos, excluyendo opcionalmente otros:

```
sudo -E -u www-data php occ twofactorauth:enforce --on \
  --group=admin --group=finance --exclude=service-accounts
  Two-factor authentication is enforced for members of the group(s) admin, finance
```

Desactivar la imposición:

```
sudo -E -u www-data php occ twofactorauth:enforce --off
  Two-factor authentication is not enforced
```

#### twofactorauth:state

Mostrar si la 2FA está activada e impuesta, y qué proveedores están activos para un usuario:

```
sudo -E -u www-data php occ twofactorauth:state layla
  Two-factor authentication is not enabled for user layla

  Disabled providers:
  - backup_codes
  - totp
```

#### twofactorauth:cleanup

Eliminar las asociaciones de proveedor de 2FA almacenadas de un proveedor que se ha desinstalado. Esto limpia los datos obsoletos después de quitar una app de 2FA:

```
sudo -E -u www-data php occ twofactorauth:cleanup <provider_id>
```

(nc-system_tags_commands_label)=
### Etiquetas del sistema

Las etiquetas del sistema son etiquetas gestionadas por el administrador que se pueden asignar a archivos para usarlas en flujos de trabajo y acciones automatizadas.

Las etiquetas tienen tres niveles de acceso:

| Nivel | Visible¹ | Asignable² |
|---|---|---|
| público | Sí | Sí |
| restringido | Sí | No |
| invisible | No | No |

¹ El usuario puede ver la etiqueta\
² El usuario puede asignar la etiqueta a un archivo

Ver {nc-doc}`admin_manual/file_workflows/automated_tagging` para los casos de uso típicos de las etiquetas restringidas e invisibles, como la retención y el control de acceso.

#### tag:list

Listar todas las etiquetas del sistema:

```
sudo -E -u www-data php occ tag:list
  - 1:
    - name: confidential
    - access: restricted
  - 2:
    - name: needs-review
    - access: public
```

#### tag:add

Crear una etiqueta del sistema nueva:

```
sudo -E -u www-data php occ tag:add confidential restricted
  - id: 1
  - name: confidential
  - access: restricted
```

#### tag:edit

Renombrar una etiqueta o cambiar su nivel de acceso. Usar el ID de la etiqueta que muestra `tag:list`:

```
sudo -E -u www-data php occ tag:edit --name "reviewed" --color="" 2
  Tag updated ("reviewed", true, true, "")
```

`--name` y `--access` son opcionales. `--color=""` debe pasarse explícitamente debido a un problema conocido del comando.

#### tag:delete

Eliminar una etiqueta por su ID:

```
sudo -E -u www-data php occ tag:delete 1
  The specified tag was deleted
```

#### Asignación de etiquetas a archivos

Añadir una o varias etiquetas a un archivo o directorio (indicado por su ID de archivo o por su ruta). El argumento `access` identifica qué etiqueta aplicar: como dos etiquetas pueden compartir el mismo nombre pero tener niveles de acceso distintos, se necesitan tanto el nombre como el nivel de acceso para identificar una etiqueta de forma única. Si no existe ninguna etiqueta que coincida, se crea automáticamente:

```
sudo -E -u www-data php occ tag:files:add /layla/files/report.pdf confidential restricted
  restricted tag named confidential added.
```

Se pueden indicar varias etiquetas como una lista separada por comas. Todas las etiquetas de una misma llamada deben compartir el mismo nivel de acceso.

Quitar etiquetas concretas de un archivo:

```
sudo -E -u www-data php occ tag:files:delete /layla/files/report.pdf confidential restricted
```

Quitar todas las etiquetas de un archivo:

```
sudo -E -u www-data php occ tag:files:delete-all /layla/files/report.pdf
```
````
