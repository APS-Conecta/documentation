---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo dirigir a los usuarios a una URL propia de restablecimiento de contraseña cuando el backend de autenticación, como LDAP, es de solo lectura."
---
# Restablecer la contraseña de un usuario

## Resumen

Esta página explica cómo indicar en `config.php` una URL personalizada para restablecer contraseñas cuando el backend de autenticación es de solo lectura, como LDAP o Active Directory. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_user/reset_user_password.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La pantalla de inicio de sesión de Nextcloud muestra el mensaje **«Wrong password. Reset it?»** cuando un usuario introduce una contraseña incorrecta, y entonces Nextcloud restablece automáticamente su contraseña. Sin embargo, esto no funciona si se usa un backend de autenticación de solo lectura como LDAP o Active Directory. En ese caso puede indicarse una URL personalizada en el archivo `config.php` para dirigir al usuario a un servidor capaz de gestionar un restablecimiento automático:

```
'lost_password_link' => 'https://example.org/link/to/password/reset',
```
````
