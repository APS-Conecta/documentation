---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Sincronizar archivos y notificaciones con el cliente Android, y contactos y calendarios con DAVx⁵, con o sin la aplicación móvil."
---
# Sincronizar con Android

## Resumen

Esta página explica cómo configurar el cliente Android para archivos y notificaciones, y cómo sincronizar contactos y calendarios con DAVx⁵, con o sin la aplicación móvil. Está dirigida a usuarios que usan la plataforma desde un teléfono o tableta Android.

````{upstream} user_manual/groupware/sync_android.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Archivos y notificaciones

1. Instale el cliente Android de Nextcloud [desde Google Play Store](https://play.google.com/store/apps/details?id=com.nextcloud.client) o [desde F-Droid](https://f-droid.org/packages/com.nextcloud.client/).
2. Inicie la aplicación. Hay dos maneras de configurarla:

   *O bien*: introduzca la URL de su servidor, pulse continuar, introduzca su usuario y contraseña y confirme que permite el acceso a su cuenta.

   *O*: en la interfaz web de Nextcloud, vaya a las {nc-doc}`preferencias de usuario <user_manual/userpreferences>` y luego a **Seguridad**. Genere una contraseña de aplicación, pulse "Generar código QR", toque el icono del escáner QR en la aplicación de Nextcloud y apunte la cámara de su teléfono hacia la pantalla.

### Contactos y Calendario

#### Con la aplicación móvil de Nextcloud

1. Instale [DAVx⁵ (antes conocida como DAVDroid)](https://www.davx5.com/download/) en su dispositivo Android, [desde Google Play Store](https://play.google.com/store/apps/details?id=at.bitfire.davdroid) o [desde F-Droid](https://f-droid.org/packages/at.bitfire.davdroid/).
2. En la aplicación móvil de Nextcloud, vaya a **Ajustes**/**Más** y toque "**Sincronizar calendarios y contactos**".
3. Ahora DAVx⁵ abrirá la ventana de inicio de sesión Webflow de Nextcloud, donde tendrá que introducir sus credenciales y conceder el acceso.
4. DAVx⁵ se abrirá y le pedirá que cree una cuenta. Asigne a la cuenta el nombre que prefiera y establezca **Método de grupos de contactos** en **Los grupos son categorías por contacto**.
5. Después de esto, DAVx⁵ se cerrará y volverá a aparecer la aplicación de Nextcloud. Para terminar la configuración, tiene que volver a abrir DAVx⁵ manualmente.
6. Toque el icono de la cuenta que DAVx⁵ acaba de crear y, cuando se le solicite, conceda a DAVx⁵ acceso a sus calendarios y contactos.
7. Al tocar el icono de la cuenta que DAVx⁵ ha configurado, la aplicación descubrirá las libretas de direcciones y los calendarios disponibles. Elija cuáles desea sincronizar y termine.

#### Sin la aplicación móvil de Nextcloud

Si no desea instalar la aplicación móvil de Nextcloud, siga los siguientes pasos:

1. Instale [DAVx⁵ (antes conocida como DAVDroid)](https://www.davx5.com/download/) en su dispositivo Android, [desde Google Play Store](https://play.google.com/store/apps/details?id=at.bitfire.davdroid) o [desde F-Droid](https://f-droid.org/packages/at.bitfire.davdroid/).
2. Opcionalmente, instale OpenTasks ([Google Play Store](https://play.google.com/store/apps/details?id=org.dmfs.tasks) o [F-Droid](https://f-droid.org/packages/org.dmfs.tasks/)).
3. Cree una cuenta nueva (botón "+").
4. Seleccione **Conexión con URL y nombre de usuario** y complete el formulario. **URL base** es la URL de su instancia de Nextcloud (p. ej., `https://sub.example.com/remote.php/dav`), **Nombre de usuario** es su nombre de usuario de Nextcloud y, como **Contraseña**, use una {nc-ref}`contraseña de aplicación dedicada <managing_devices>` en lugar de la contraseña de su cuenta.
5. Pulse **Registrar**.
6. En **Método de grupos de contactos**, elija la opción `Groups are per-contact categories`; luego seleccione **Crear cuenta**.
7. Seleccione los datos que desea sincronizar.
8. Cuando se le solicite, conceda a DAVx⁵ permisos de acceso a sus contactos, sus calendarios y, opcionalmente, sus tareas.

:::{note}
Introduzca su dirección de correo electrónico como nombre de la cuenta de DAVx⁵ (obligatorio si desea poder enviar invitaciones de calendario). Si su dirección de correo electrónico está registrada en sus preferencias de Nextcloud y configuró su cuenta con la aplicación móvil de Nextcloud, esto ya debería ser así.
:::

:::{note}
Usar el nombre de usuario y la contraseña no funcionará si la autenticación de dos factores está habilitada, y producirá un error genérico «Unknown resource». En su lugar, use una {nc-ref}`contraseña de aplicación dedicada <managing_devices>`. Si habilitó la 2FA después de haber configurado DAVx⁵, actualice su cuenta de DAVx⁵ para reemplazar su contraseña de inicio de sesión por una contraseña de aplicación.
:::

:::{tip}
DAVx⁵ muestra las suscripciones de calendario hechas con la aplicación Calendario de Nextcloud, pero para sincronizarlas necesita instalar la aplicación [ICSx⁵ (antes conocida como ICSDroid)](https://icsx5.bitfire.at/) en su dispositivo Android, [desde Google Play Store](https://play.google.com/store/apps/details?id=at.bitfire.icsdroid) o [desde F-Droid](https://f-droid.org/packages/at.bitfire.icsdroid/).
:::
````
