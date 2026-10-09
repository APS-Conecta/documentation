---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Añadir cuentas CalDAV y CardDAV en Cuentas de Internet de macOS para sincronizar Calendario y Contactos, y qué revisar si falla."
---
# Sincronizar con macOS

## Resumen

Esta página explica cómo añadir, desde Cuentas de Internet, una cuenta CalDAV para el calendario y otra CardDAV para los contactos en las aplicaciones integradas de macOS, y qué revisar si la sincronización falla. Está dirigida a usuarios de Mac.

````{upstream} user_manual/groupware/sync_osx.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Configurar sus Cuentas

En los siguientes pasos añadirá **CalDAV** (Calendario) y **CardDAV** (Contactos) a las aplicaciones Calendario y Contactos integradas en macOS. En el momento de escribir esta guía, macOS está en la versión 26.3.1.

1. Haga clic en el menú **Apple** y seleccione **Ajustes del Sistema...** en el menú desplegable.

2. Navegue a **Cuentas de Internet**.

3. Haga clic en la pequeña opción azul **seleccionar de una lista.**

4. Haga clic en **Añadir otra cuenta...**

5. Seleccione **Cuenta CalDAV** para el calendario y **Cuenta CardDAV** para los contactos.

:::{note}
No es posible configurar Calendario y Contactos a la vez. Debe configurarlos **por separado**.
:::

6. Seleccione **Manual** como tipo de cuenta e introduzca sus credenciales correspondientes:

   **Nombre de usuario**: Su nombre de usuario de Nextcloud o correo electrónico

   **Contraseña**: su contraseña o, si usa 2FA, la contraseña/token de aplicación que haya generado ({nc-ref}`Más información <managing_devices>`).

   **Dirección del servidor**: URL de su servidor Nextcloud (p. ej., `https://nextcloud.yourdomain.com`)

7. Pulse **Iniciar sesión**.

### Resolución de problemas

- macOS **no** soporta la sincronización de CalDAV/CardDAV con conexiones `http://` no cifradas. Asegúrese de que tiene `https://` activado y configurado tanto en el cliente como en el servidor.

- Los **certificados auto-firmados** deben ser añadidos al llavero de macOS.
````
