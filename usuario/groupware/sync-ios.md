---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Añadir cuentas CalDAV y CardDAV en iOS para sincronizar el calendario y los contactos, y qué revisar si la conexión falla."
---
# Sincronizar con iOS

## Resumen

Esta página explica cómo añadir en los ajustes de iOS una cuenta CalDAV para el calendario y una cuenta CardDAV para los contactos, con notas sobre SSL y enlaces para resolver problemas. Está dirigida a usuarios de iPhone o iPad.

````{upstream} user_manual/groupware/sync_ios.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Calendario

1. Abrir la aplicación Ajustes.
2. Seleccionar Apps.
3. Seleccionar Calendario.
4. Seleccionar Cuentas de calendario.
5. Seleccionar Añadir cuenta.
6. Seleccionar Otra como tipo de cuenta.
7. Seleccionar Añadir cuenta **CalDAV**.
8. En servidor, escribir el nombre de dominio del servidor, es decir, `example.com`.
9. Introducir el nombre de usuario y la contraseña.
10. Seleccionar Siguiente.
11. Abrir Ajustes avanzados.
12. En servidor, escribir el nombre de dominio del servidor y la ruta, es decir, `example.com/remote.php/dav/principals/users/username/` (reemplazar **example.com** y **username**).
13. Cerrar Ajustes avanzados.

El calendario ahora estará visible en la aplicación Calendario.

:::{note}
Si aparece un mensaje de error relacionado con SSL, se puede intentar lo siguiente: asegurarse de especificar en el campo `Server` o bien tanto el protocolo (`https://`) como el puerto (normalmente `443`), es decir, `https://example.com:443/remote.php/dav/principals/users/username/`, o bien ninguno de los dos, como en la guía paso a paso anterior. En ambos casos, la aplicación intenta usar SSL automáticamente, lo que se puede confirmar en “Ajustes avanzados” de la cuenta después de guardarla.
:::

:::{note}
A partir de iOS 12 es necesario el cifrado SSL. Por lo tanto, **no** desactivar **SSL** (por este motivo se requiere un certificado en el dominio; https://letsencrypt.org/ sirve).
:::

:::{note}
Si se selecciona **CardDAV**, solo quedará disponible la sincronización de contactos.
:::

### Contactos

1. Abrir la aplicación Ajustes.
2. Seleccionar Apps.
3. Seleccionar Contactos.
4. Seleccionar Cuentas de contactos.
5. Seleccionar Añadir cuenta.
6. Seleccionar Otra como tipo de cuenta.
7. Seleccionar Añadir cuenta **CardDAV**.
8. En servidor, escribir el nombre de dominio del servidor y la ruta, es decir, `example.com/remote.php/dav/principals/users/username/` (reemplazar **example.com** y **username**).
9. Introducir el nombre de usuario y la contraseña.
10. Seleccionar Siguiente.

Los contactos ahora deberían aparecer en la libreta de direcciones del iPhone.

:::{note}
A partir de iOS 12 es necesario el cifrado SSL. Por lo tanto, **no** desactivar **SSL** (por este motivo se requiere un certificado en el dominio; https://letsencrypt.org/ sirve).
:::

:::{note}
Si se selecciona **CalDAV**, solo quedará disponible la sincronización de calendarios.
:::

Si aún no funciona, consultar [Solución de problemas de Contactos y Calendario][Troubleshooting Contacts & Calendar] o [Solución de problemas del descubrimiento de servicios][Troubleshooting Service Discovery].

[Troubleshooting Contacts & Calendar]: https://docs.nextcloud.com/server/latest/admin_manual/issues/general_troubleshooting.html#troubleshooting-contacts-calendar
[Troubleshooting Service Discovery]: https://docs.nextcloud.com/server/latest/admin_manual/issues/general_troubleshooting.html#service-discovery
````
