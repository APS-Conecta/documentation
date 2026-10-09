---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cambios al actualizar a Nextcloud 26: versiones de PHP, nueva biblioteca de correo del sistema, retención de tokens de DAV y configuración de nginx."
---
# Actualización a Nextcloud 26

## Resumen

Esta página recoge los cambios que hay que conocer al actualizar a Nextcloud 26: las versiones de PHP admitidas, la nueva biblioteca para el correo electrónico del sistema, la limpieza de los tokens de sincronización de CalDAV y CardDAV, y la configuración recomendada de nginx. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/release_notes/upgrade_to_26.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Requisitos del sistema

- PHP 8.2 ya es compatible, pero se recomienda 8.1.
- PHP 7.4 ya no es compatible.

### Correo electrónico del sistema

Hubo que sustituir el componente de software que envía los correos electrónicos del sistema (notificaciones, invitaciones, restablecimiento de contraseña, etc.). La nueva biblioteca debería funcionar sin ningún cambio en la mayoría de las configuraciones.

Un breve resumen de los cambios:

- No se puede forzar STARTTLS. Se usará automáticamente si el servidor de correo lo admite. En ese caso, el tipo de cifrado debe establecerse en «Ninguno/STARTTLS».
- Los certificados autofirmados ahora deben activarse explícitamente; consultar {nc-ref}`esta guía <TLSPeerVerification>` para ver un ejemplo de cómo configurarlo.
- La nueva biblioteca de correo no admite la autenticación NTLM para Microsoft Exchange. Probar a usar en su lugar la [autenticación básica](https://learn.microsoft.com/en-us/exchange/client-developer/exchange-web-services/authentication-and-ews-in-exchange#basic-authentication).

Para más información, consultar: {nc-ref}`email-smtp-config`.

### Retención de los tokens de sincronización de DAV

Se ha añadido un mecanismo para limpiar los tokens de sincronización antiguos de CalDAV y CardDAV. Consultar {nc-ref}`Retención de CalDAV <caldav-data-retention>` y {nc-ref}`Retención de CardDAV <carddav-data-retention>`, y asegurarse de que se ajusta al tamaño de la instalación.

### Configuración del servidor web

- Ha cambiado la {nc-ref}`configuración de nginx <nginx-config>` recomendada.
````
