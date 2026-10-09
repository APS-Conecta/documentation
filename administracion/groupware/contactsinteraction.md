---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo la app Interacción de contactos registra a quién contacta cada usuario y lo ofrece como libreta CardDAV de solo lectura, y cuánto conserva esos datos."
---
# Interacción de contactos

## Resumen

Esta página explica cómo la app Interacción de contactos registra las personas con las que cada usuario ha interactuado, qué guarda en la libreta de direcciones de solo lectura «Contactados recientemente», dónde es visible y cuándo se eliminan sus entradas. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/groupware/contactsinteraction.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La app Interacción de contactos registra automáticamente con qué personas ha interactuado recientemente un usuario y ofrece estos datos como una libreta de direcciones CardDAV de solo lectura llamada **Contactados recientemente**. Esto permite sugerencias de autocompletado en los diálogos de uso compartido, la redacción de correos, las invitaciones de calendario y otros lugares que consultan las libretas de direcciones del usuario, incluso para personas que no están guardadas como contactos explícitos.

La app viene incluida con Nextcloud y está activada de forma predeterminada. Puede desactivarse.

### Cómo se registran las interacciones

La app escucha los eventos `ContactInteractedWithEvent` que emiten otras apps de Nextcloud. Las siguientes apps emiten este evento:

- **Uso compartido de archivos**: cuando un usuario crea un recurso compartido con otro usuario local, con una dirección de correo electrónico o con un usuario remoto federado.
- **Calendario**: cuando un usuario comparte un calendario con otro usuario.
- **Correo**: cuando un usuario envía un correo electrónico.

Cualquier app puede integrarse emitiendo un `ContactInteractedWithEvent` con al menos un identificador: un ID de usuario de Nextcloud, una dirección de correo electrónico o un ID de nube federada.

Cuando se registra una interacción, la app comprueba primero si la persona contactada ya existe en alguna de las libretas de direcciones normales del usuario. Si encuentra una coincidencia, no se crea ninguna entrada en la libreta de direcciones de contactados recientemente, ya que la persona ya es un contacto conocido. Las interacciones consigo mismo (cuando el usuario interactúa consigo mismo) también se ignoran.

Para los contactos nuevos se genera una vCard mínima que contiene:

- `FN` (nombre mostrado): se obtiene del perfil de usuario de Nextcloud si la persona es un usuario local; si no, se recurre a la dirección de correo electrónico o al ID de nube federada.
- `EMAIL`: se incluye cuando se conoce una dirección de correo electrónico.
- `CLOUD`: se incluye cuando se conoce un ID de nube federada.
- `CATEGORIES`: se establece en {guilabel}`Contactados recientemente`, lo que permite a la app Contactos identificar las entradas de esta libreta de direcciones y ofrecer a los usuarios la opción de copiarlas a una libreta de direcciones normal.

Si se vuelve a contactar con la misma persona, se actualiza la marca de tiempo de la entrada existente en lugar de crear un duplicado.

### La libreta de direcciones de contactados recientemente

La libreta de direcciones de contactados recientemente de cada usuario es accesible por CardDAV en:

```
/remote.php/dav/addressbooks/users/{userId}/z-app-generated--contactsinteraction--recent/
```

El prefijo `z-app-generated` garantiza que la libreta de direcciones se ordene después de las libretas de direcciones creadas por los usuarios. Los usuarios no pueden crear libretas de direcciones propias con este prefijo reservado.

La libreta de direcciones es de **solo lectura** y **no se puede compartir**. Los usuarios no pueden crear, modificar ni eliminar entradas. Las entradas solo se eliminan automáticamente, mediante el trabajo de limpieza o cuando se elimina una cuenta de usuario.

La libreta de direcciones es visible en:

- **Clientes CardDAV**: cualquier cliente que se sincronice con el Nextcloud del usuario (p. ej., Thunderbird, Contactos de macOS, DAVx5) verá la libreta de direcciones.
- **Contactos de Nextcloud**: la libreta de direcciones y sus entradas aparecen en la interfaz de Contactos si la app Contactos está activada. Los contactos de esta libreta de direcciones pueden copiarse a una libreta de direcciones normal.
- **Autocompletado**: las entradas están disponibles para las sugerencias de destinatarios en los diálogos de uso compartido y en otros lugares de la interfaz web de Nextcloud.

### Retención de datos

Un trabajo en segundo plano se ejecuta cada 24 horas y elimina las entradas que no se han actualizado en los últimos 7 días. Tanto el periodo de retención como el intervalo de limpieza son fijos y no pueden configurarse.

:::{note}
El trabajo de limpieza depende del sistema de trabajos en segundo plano de Nextcloud. Hay que asegurarse de que cron esté configurado correctamente para la instancia. Consultar {nc-doc}`admin_manual/configuration_server/background_jobs_configuration`.
:::

### Eliminación de usuarios

Cuando se elimina una cuenta de usuario, todas las entradas de contactados recientemente de ese usuario se eliminan automáticamente de la base de datos.
````
