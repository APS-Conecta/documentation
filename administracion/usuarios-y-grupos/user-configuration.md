---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "La página de gestión de usuarios: crear, deshabilitar y eliminar cuentas, nombres mostrados, contraseñas, grupos, administradores y cuotas."
---
# Gestión de usuarios

## Resumen

Esta página explica la página de gestión de usuarios de la interfaz web: las propiedades de una cuenta, cómo crear usuarios, restablecer contraseñas, cambiar nombres mostrados, conceder privilegios de administrador, gestionar grupos y cuotas, y deshabilitar o eliminar cuentas. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_user/user_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
En la página de gestión de usuarios de la interfaz web de Nextcloud se puede:

- Crear usuarios nuevos
- Ver todos los usuarios en una única ventana desplazable
- Filtrar los usuarios por grupo
- Ver a qué grupos pertenecen
- Editar sus nombres completos y sus contraseñas
- Ver las ubicaciones de almacenamiento de sus datos
- Ver y establecer cuotas
- Crear y editar sus direcciones de correo electrónico
- Enviar una notificación automática por correo electrónico a los usuarios nuevos
- Deshabilitar y habilitar usuarios
- Eliminarlos con un solo clic

La vista predeterminada muestra información básica sobre los usuarios.

Los filtros de grupo de la barra lateral izquierda permiten filtrar rápidamente los usuarios según su pertenencia a grupos y crear grupos nuevos.

:::{note}
Es posible que el número de usuarios de ciertos grupos, como «Todas las cuentas», no se muestre al usar ciertos backends, como LDAP/AD/SAML.
:::

Hacer clic en el icono del engranaje de la parte inferior de la barra lateral izquierda para establecer una cuota de almacenamiento predeterminada y para mostrar campos adicionales: **Mostrar ubicación del almacenamiento, Mostrar último inicio de sesión, Mostrar backend de usuario, Enviar correo electrónico a los usuarios nuevos** y **Mostrar dirección de correo electrónico**.

Las cuentas de usuario tienen las siguientes propiedades:

- *Nombre de inicio de sesión (nombre de usuario)*: El ID único de un usuario de Nextcloud, que no puede cambiarse.
- *Nombre completo*: El nombre mostrado del usuario, que aparece en los recursos compartidos, en la interfaz web de Nextcloud y en los correos electrónicos. Los administradores y los usuarios pueden cambiar el nombre completo en cualquier momento. Si el nombre completo no está establecido, se usa por defecto el nombre de inicio de sesión.
- *Contraseña*: El administrador establece la contraseña inicial del usuario nuevo. Tanto el usuario como el administrador pueden cambiar la contraseña del usuario en cualquier momento.
- *Dirección de correo electrónico*: Se puede establecer una dirección de correo electrónico para un usuario. Esta dirección puede usarse al crear la cuenta por primera vez, para que el usuario reciba un correo que le pida crear una contraseña si no se proporciona ninguna. Esta dirección también puede usarse para las solicitudes de restablecimiento de contraseña.
- *Grupos*: Se pueden crear grupos y asignar a los usuarios pertenencias a grupos. De forma predeterminada, los usuarios nuevos no se asignan a ningún grupo.
- *Administrador de grupo*: Los administradores de grupo reciben privilegios administrativos sobre grupos concretos y pueden crear usuarios en sus grupos y quitarlos de ellos. Esto significa que pueden modificar el nombre de usuario, la contraseña, el correo electrónico, la cuota, etc., de los miembros del grupo. Los administradores de grupo no pueden añadir usuarios existentes a sus grupos.
- *Cuota*: El espacio máximo en disco asignado a cada usuario. Ningún usuario que supere la cuota puede subir ni sincronizar datos. Existe la opción de incluir el almacenamiento externo en las cuotas de los usuarios.
- *Gerente*: Cada usuario puede tener un gerente en la organización. La propiedad de gerente pasa a la tarjeta del usuario en la libreta de direcciones del sistema y se usa, por ejemplo, para el organigrama de la app Contactos. Establecer un gerente **no** cambia ningún nivel de autorización del usuario ni de su gerente.

### Crear un usuario nuevo

Para crear una cuenta de usuario:

- Introducir el **Nombre de inicio de sesión** del usuario nuevo y su **Contraseña** inicial
- Opcionalmente, asignar pertenencias a **Grupos**
- Hacer clic en el botón **Crear**

Los nombres de inicio de sesión pueden contener letras (a-z, A-Z), números (0-9), guiones (-), guiones bajos (\_), puntos (.), espacios ( ) y arrobas (@). Después de crear el usuario, se puede rellenar su **Nombre completo** si es distinto del nombre de inicio de sesión, o dejar que el usuario lo complete.

Si se ha marcado **Enviar correo electrónico al usuario nuevo** en el panel de control de la parte inferior de la barra lateral izquierda, también se puede introducir la dirección de correo electrónico del usuario nuevo, y Nextcloud le enviará automáticamente una notificación con sus nuevos datos de inicio de sesión. Este correo puede editarse con el editor de plantillas de correo electrónico de la página de administración (véase {nc-doc}`admin_manual/configuration_server/email_configuration`).

Si se marca la casilla **Enviar correo electrónico al usuario nuevo**, se puede dejar vacío el campo **Contraseña**. El usuario recibirá un correo de activación para establecer su propia contraseña.

### Restablecer la contraseña de un usuario

La contraseña de un usuario no puede recuperarse, pero se puede establecer una nueva:

- Pasar el cursor sobre el campo **Contraseña** del usuario
- Hacer clic en el **icono del lápiz**
- Introducir la nueva contraseña del usuario en el campo de contraseña, y no olvidar comunicarle al usuario su contraseña

Si el cifrado está activado, hay consideraciones especiales para el restablecimiento de contraseñas de usuario. Véase {nc-doc}`admin_manual/configuration_files/encryption_configuration`.

### Cambiar el nombre de un usuario

Cada usuario de Nextcloud tiene dos nombres: un **Nombre de inicio de sesión** único, que se usa para la autenticación, y un **Nombre completo**, que es su nombre mostrado. El nombre mostrado de un usuario puede editarse, pero el nombre de inicio de sesión de ningún usuario puede cambiarse.

Para establecer o cambiar el nombre mostrado de un usuario:

- Pasar el cursor sobre el campo **Nombre completo** del usuario
- Hacer clic en el **icono del lápiz**
- Introducir el nuevo nombre mostrado del usuario

### Conceder privilegios de administrador a un usuario

Nextcloud tiene dos tipos de administradores: **Superadministradores** y **Administradores de grupo**. Los administradores de grupo tienen derecho a crear, editar y eliminar usuarios en los grupos que tienen asignados. Los administradores de grupo no pueden acceder a la configuración del sistema ni añadir o modificar usuarios en grupos de los que no son **Administradores de grupo**. Para asignar privilegios de administrador de grupo se usan los menús desplegables de la columna **Administrador de grupo**.

Los **Superadministradores** tienen todos los derechos sobre el servidor Nextcloud y pueden acceder a toda la configuración y modificarla. Para asignar a un usuario el rol de **Superadministradores**, basta con añadirlo al grupo `admin`.

### Gestionar grupos

Los usuarios nuevos pueden asignarse a grupos al crearlos, y pueden crearse grupos nuevos al crear usuarios nuevos. También puede usarse el botón **Añadir grupo** de la parte superior del panel izquierdo para crear grupos nuevos. Los nuevos miembros de un grupo tendrán acceso inmediato a los recursos compartidos que pertenecen a sus nuevos grupos.

### Establecer cuotas de almacenamiento

Hacer clic en el icono del engranaje de la parte inferior del panel izquierdo para establecer una cuota de almacenamiento predeterminada. Esta cuota se aplica automáticamente a los usuarios nuevos. A cualquier usuario se le puede asignar una cuota distinta en el desplegable **Cuota**, eligiendo un valor predefinido o introduciendo un valor personalizado. Al crear cuotas personalizadas, usar las abreviaturas habituales para los valores de almacenamiento, como 500 MB, 5 GB, 5 TB, etc.

Ahora existe una opción configurable en `config.php` que controla si el almacenamiento externo cuenta para las cuotas de los usuarios. Todavía es experimental y puede no funcionar como se espera. De forma predeterminada, el almacenamiento externo no se cuenta como parte de las cuotas de almacenamiento de los usuarios. Para incluirlo, cambiar el valor predeterminado `false` por `true`.

```
'quota_include_external_storage' => false,
```

:::{note}
Si un almacenamiento externo se define como raíz, la cuota no podrá calcularse y se **ignorará**.
:::

Los metadatos (como las miniaturas, los archivos temporales y las claves de cifrado) ocupan alrededor del 10 % del espacio en disco, pero no cuentan para las cuotas de los usuarios. Los usuarios pueden consultar su espacio usado y disponible en sus páginas personales. Solo cuentan para la cuota de un usuario los archivos que se originan en él, y no los archivos compartidos con él que se originan en otros usuarios. Por ejemplo, si se suben archivos a un recurso compartido de otro usuario, esos archivos cuentan para la cuota de quien los sube. Si se vuelve a compartir un archivo que otro usuario ha compartido, ese archivo no cuenta para la cuota de quien lo vuelve a compartir, sino para la del usuario que lo originó.

Los archivos cifrados son algo más grandes que los no cifrados; para la cuota del usuario se calcula el tamaño sin cifrar.

Los archivos eliminados que siguen en la papelera no cuentan para las cuotas. La papelera está fijada en el 50 % de la cuota. La antigüedad de los archivos eliminados está fijada en 30 días. Cuando los archivos eliminados superan el 50 % de la cuota, se eliminan los archivos más antiguos hasta que el total quede por debajo del 50 %.

Cuando el control de versiones está activado, las versiones antiguas de los archivos no cuentan para las cuotas.

Cuando un usuario crea un recurso compartido público mediante URL y permite subidas, los archivos subidos cuentan para la cuota de ese usuario.

### Deshabilitar y habilitar usuarios

A veces puede interesar deshabilitar a un usuario sin eliminar de forma permanente su configuración ni sus archivos. El usuario puede volver a activarse en cualquier momento, sin pérdida de datos.

Pasar el cursor sobre su nombre en la página **Usuarios** hasta que aparezca el icono de menú «...» en el extremo derecho. Al hacer clic en él, aparece la opción **Deshabilitar**.

El usuario ya no podrá acceder a su Nextcloud hasta que se le vuelva a habilitar. Además, ninguno de los recursos compartidos externos, por enlace público o por correo electrónico, será accesible. Los recursos compartidos internos seguirán funcionando, de modo que los demás usuarios de Nextcloud pueden seguir trabajando.

Si se quiere que los recursos compartidos internos también se desactiven cuando se deshabilita a un usuario, activar la opción de configuración files_sharing:hide_disabled_user_shares:

```
occ config:app:set files_sharing hide_disabled_user_shares --value yes
```

Todos los usuarios deshabilitados están en la sección **deshabilitados** del panel izquierdo. Habilitar usuarios es tan fácil como deshabilitarlos. Basta con hacer clic en el menú «...» y seleccionar **Habilitar**.

### Eliminar usuarios

Eliminar a un usuario es fácil: pasar el cursor sobre su nombre en la página **Usuarios** hasta que aparezca el icono de menú «...» en el extremo derecho. Al hacer clic en él, aparece la opción **Eliminar**. Al hacer clic en ella, el usuario se elimina de inmediato con todos sus datos.

En la parte superior de la página aparece un botón para deshacer, que permanece unos segundos. Cuando el botón para deshacer desaparece, el usuario eliminado ya no puede recuperarse.

También se eliminan todos los archivos de los que el usuario es propietario, incluidos todos los que ha compartido. Si hay que conservar los archivos y los recursos compartidos del usuario, primero hay que descargarlos desde la página Archivos de Nextcloud, que los comprime en un archivo zip, o usar un cliente de sincronización para copiarlos al computador local. Véase {nc-doc}`admin_manual/configuration_files/file_sharing_configuration` para saber cómo crear recursos compartidos persistentes que sobreviven a la eliminación de usuarios.

### Desactivar el correo «Su dirección de correo electrónico [...] fue cambiada»

Si un administrador cambia la dirección de correo electrónico de un usuario, se envía al usuario un correo que dice «Su dirección de correo electrónico en [URL] fue cambiada por un administrador.». En algunos casos esto no debería ocurrir, porque se trataba de un cambio de mantenimiento normal. Para desactivar este correo concreto, la opción de appconfig `disable_email.email_address_changed_by_admin` puede establecerse en `yes`:

```
occ config:app:set settings disable_activity.email_address_changed_by_admin --value yes
```

Para desactivar este comportamiento, cambiarla a cualquier otro valor o eliminar la configuración de la app:

```
occ config:app:delete settings disable_activity.email_address_changed_by_admin
```
````
