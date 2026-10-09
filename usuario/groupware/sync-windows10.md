---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Sincronizar calendario y contactos con la app Calendario de Windows 10 vía CalDAV y CardDAV, y resolver problemas de 2FA y TLSv1.2."
---
# Sincronizar con Windows 10

## Resumen

Esta página explica cómo sincronizar el calendario y los contactos con la aplicación Calendario de Windows 10, a través de una cuenta de iCloud cuyas direcciones CalDAV y CardDAV se reemplazan por las del servidor, y cómo resolver los problemas de autenticación de dos factores y de TLSv1.2. Está dirigida a usuarios de Windows 10.

````{upstream} user_manual/groupware/sync_windows10.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
(nc-calendar-section)=
### Calendario

1. En su navegador, vaya a la aplicación Calendario de Nextcloud. En «Configuración del calendario», copie la dirección al portapapeles con «Copy iOS/macOS CalDAV address».

2. Abra la aplicación Calendario de Windows 10. A continuación, haga clic en el icono de ajustes (engranaje) y seleccione "Gestionar cuentas".

3. Haga clic en "Añadir cuenta" y elija "iCloud".

4. Introduzca un correo, nombre de usuario y contraseña cualesquiera. Estos datos no tienen por qué ser correctos, puesto que los modificaremos en los pasos siguientes.

5. Seleccione "Hecho". Aparecerá un mensaje confirmando el guardado de los ajustes.

6. En el menú "Gestionar cuentas", haga clic en la cuenta de iCloud que acaba de crear en los pasos anteriores, y seleccione "Cambiar ajustes". A continuación haga clic en "Cambiar ajustes de sincronización de correo".

7. Desplácese a la parte inferior del cuadro de diálogo y seleccione "Configuración avanzada de correo". Desplácese al final del cuadro de diálogo y pegue su URL CalDAV en el campo llamado "Servidor de calendario (CalDAV)".

8. Pulse "Hecho". Introduzca su nombre de usuario y contraseña en los campos correspondientes y ajuste el nombre de la cuenta (por ejemplo "Calendario Nextcloud"). Pulse "Guardar".

### Contactos

1. Repita los pasos 1–7 de las {nc-ref}`instrucciones del Calendario <calendar-section>`. Si ya configuró la sincronización del Calendario, puede usar la misma cuenta para esto.

2. Desde la pantalla «Configuración avanzada de correo», desplácese a la parte inferior del cuadro de diálogo y pegue su URL CardDAV en el campo llamado «Servidor de contactos (CardDAV)».

3. En la URL, reemplace la ruta "principals" por "addressbooks".

4. Pulse "Hecho". Introduzca su nombre de usuario y contraseña de Nextcloud en los campos correspondientes y ajuste el nombre de la cuenta (por ejemplo "Nextcloud"). Pulse "Guardar".

### Solución de problemas: 2FA

**NOTA: No le será posible sincronizar su calendario si ha habilitado el segundo factor de autenticación o autenticación en dos pasos. Siga los pasos a continuación para obtener una contraseña de aplicación que puede ser utilizada con la aplicación cliente de Calendario:**

1. Inicie sesión en Nextcloud. Pulse su icono de usuario, y a continuación en "Ajustes".

2. Haga clic en «Seguridad» y localice un botón con la etiqueta «Crear nueva contraseña de app». Junto a este botón, introduzca «Aplicación Calendario de Windows 10». A continuación, haga clic en el botón y copie y pegue la contraseña. Use esta contraseña en lugar de su contraseña de Nextcloud cuando se le soliciten credenciales durante la configuración, por ejemplo en el paso 8 del Calendario o en el paso 4 de Contactos.

### Solución de problemas: TLSv1.2

- En Windows 10, su servidor https de Nextcloud [debe admitir TLSv1.2](https://docs.microsoft.com/en-us/windows/win32/secauthn/protocols-in-tls-ssl--schannel-ssp-). Esto se pone de manifiesto cuando no se observa ningún intento de conexión en el servidor, y el Visor de eventos del cliente Windows mostrará errores TLS de Schannel en «Registros de Windows -> Sistema».

### Créditos

Un agradecimiento especial a este usuario de Reddit por su publicación: <https://www.reddit.com/r/Nextcloud/comments/5rcypb/using_the_windows_10_calendar_application_with/>
````
