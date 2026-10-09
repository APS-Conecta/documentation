---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo recuperar una contraseña de administrador perdida: el enlace de restablecimiento, otro administrador o el comando occ user:resetpassword."
---
# Restablecer una contraseña de administrador perdida

## Resumen

Esta página describe las formas de recuperar la contraseña perdida de una cuenta de administración, incluido el restablecimiento con el comando `occ`. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_user/reset_admin_password.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Las formas habituales de recuperar una contraseña perdida son:

1. Hacer clic en el enlace de restablecimiento de contraseña de la pantalla de inicio de sesión; aparece después de un intento de inicio de sesión fallido. Solo funciona si la dirección de correo electrónico se registró en la página personal de la interfaz web de Nextcloud, para que el servidor Nextcloud pueda enviar por correo un enlace de restablecimiento.

2. Pedir a otro administrador del servidor Nextcloud que la restablezca.

Si ninguna de estas es posible, queda una tercera opción: usar el comando `occ`. Consultar {nc-doc}`admin_manual/occ_command` para saber más sobre el uso del comando `occ`.

```
$ sudo -E -u www-data php /var/www/nextcloud/occ user:resetpassword admin
Enter a new password:
Confirm the new password:
Successfully reset password for admin
```

Si el nombre de usuario de Nextcloud no es `admin`, sustituirlo por el nombre de usuario de Nextcloud correspondiente.
````
