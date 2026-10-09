---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Transferir la propiedad de un archivo o carpeta a otro usuario, con sus ajustes de uso compartido y permisos, desde Ajustes > Compartir."
---
# Transferir la propiedad

## Resumen

Esta página explica, paso a paso, cómo transferir la propiedad de un archivo o carpeta a otro usuario y qué ocurre cuando el destinatario acepta o rechaza la transferencia. Está dirigida a usuarios que entregan archivos y carpetas a otra persona.

````{upstream} user_manual/files/transfer_ownership.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los usuarios pueden transferir la propiedad de archivos y carpetas a otros usuarios. Los ajustes de uso compartido y los permisos de los archivos y carpetas transferidos también se transfieren al nuevo propietario.

1. Vaya a *Ajustes* > *Compartir*.
2. En la sección *Archivos*, haga clic en *Elegir archivo o carpeta para transferir*. Se abre un selector de archivos que muestra todos los archivos y carpetas de la cuenta del usuario.
3. Elija un archivo o carpeta y haga clic en *Seleccionar*. Se muestra el nombre del archivo o carpeta elegido.
4. Haga clic en *Cambiar* para cambiar la elección si es necesario.
5. Elija un nuevo propietario escribiendo su nombre en el campo de búsqueda junto a *Nuevo propietario*.
6. Haga clic en *Transferir*.

   :::{note}
   El autocompletado o la lista de nombres de usuario pueden estar limitados por la configuración de visibilidad administrativa. Consulte la [documentación de administración](https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/file_sharing_configuration.html) para más detalles.
   :::

7. El usuario destinatario recibirá una notificación que les dará la opción de aceptar o rechazar la transferencia entrante.

8. Si la acepta, el usuario destinatario encuentra los archivos y carpetas transferidos en su carpeta raíz, dentro de una carpeta *Se transfirió desde [usuario] en [fecha y hora]*.
9. El usuario de origen recibe una notificación que le informa si la transferencia se aceptó o se rechazó.
````
