---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Atender los derechos del RGPD: acceso, supresión, portabilidad, rectificación y limitación del tratamiento, con occ y lo que queda por limpiar."
---
# Responder a las solicitudes de los interesados

## Resumen

Esta página explica cómo atender con las herramientas integradas las solicitudes de acceso, supresión, portabilidad, rectificación y limitación del tratamiento que prevé el RGPD, incluidos los datos que no se eliminan automáticamente. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/gdpr/subject_rights.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El RGPD concede a las personas varios derechos sobre sus datos personales. Esta página describe cómo atender las solicitudes más habituales con las herramientas integradas de Nextcloud.

Las solicitudes de acceso de los interesados deben responderse en el plazo de **un mes**. Si una solicitud es compleja o se recibe un volumen elevado, este plazo puede ampliarse otros dos meses, pero hay que informar al solicitante dentro del primer mes de que se necesita una prórroga y explicar el motivo. No puede cobrarse ninguna tarifa por atender una solicitud, salvo que sea manifiestamente infundada o excesiva.

### Derecho de acceso (artículo 15)

Un usuario puede ver directamente en Nextcloud la mayor parte de sus propios datos personales:

- **Información del perfil y de la cuenta**: Ajustes personales → Información personal.
- **Archivos**: la app Archivos muestra todos los archivos almacenados.
- **Registro de actividad**: la app Actividad muestra los eventos de archivos y de uso compartido.
- **Historial de uso compartido**: la sección Compartir de los Ajustes personales.
- **Clientes conectados y contraseñas de aplicación**: Ajustes personales → Seguridad.

Como administrador, puede obtenerse un resumen de los metadatos de una cuenta con:

```
sudo -E -u www-data php occ user:info <uid>
```

Esto muestra el nombre mostrado, el correo electrónico, el último inicio de sesión, la cuota, los grupos y el backend.

### Derecho de supresión (artículo 17)

Para eliminar de forma permanente una cuenta de usuario y todos los datos asociados:

```bash
sudo -E -u www-data php occ user:delete <uid>
```

Esto elimina la cuenta, todos los archivos propiedad del usuario, sus datos de perfil, los tokens de autenticación y los datos de groupware (contactos, calendarios).

:::{warning}
**Los comentarios deben eliminarse manualmente antes de ejecutar** `user:delete`. Los comentarios de archivos y los mensajes de Talk se almacenan en `oc_comments` y `oc_comments_read_markers`. `user:delete` no los elimina y, si no se limpian antes, quedarán atribuidos a «unknown/anonymous user». Ejecutar estas consultas SQL antes de eliminar la cuenta:

```sql
DELETE FROM oc_comments
  WHERE actor_type = 'users' AND actor_id = '$USERID';

DELETE FROM oc_comments_read_markers
  WHERE user_id = '$USERID';
```

Sustituir `$USERID` por el nombre de usuario de la cuenta. Para encontrar todos los tipos de comentario de la instancia (comentarios de archivos, Talk, etc.), ejecutar:

```sql
SELECT DISTINCT object_type FROM oc_comments;
```
:::

:::{note}
**Qué más no se elimina automáticamente:**

- Los archivos que el usuario ha compartido con otros siguen siendo accesibles para los destinatarios hasta que el destinatario o un administrador los elimine.
- Los recursos compartidos federados que el usuario aceptó desde otras instancias se guardan en esos servidores remotos y deben eliminarse allí por separado.
- Las entradas del registro de auditoría del sistema (`admin_audit`) se conservan porque forman parte del registro administrativo. Consultar con el equipo jurídico el periodo de conservación adecuado para los registros de auditoría.
- Los mensajes de chat de las conversaciones de Talk se conservan en el historial de la conversación. Usar el panel de administración de Talk para eliminar conversaciones concretas si es necesario.
- Datos de las copias de seguridad: consultar {nc-doc}`admin_manual/gdpr/data_retention` para obtener orientación.
:::

Antes de eliminar la cuenta, puede convenir transferir la propiedad de los archivos a otro usuario para que los archivos compartidos sigan disponibles:

```
sudo -E -u www-data php occ files:transfer-ownership <uid> <destination-uid>
```

### Derecho a la portabilidad de los datos (artículo 20)

Los usuarios pueden exportar sus propios datos directamente desde Nextcloud:

- **Archivos**: se pueden descargar como ZIP desde la app Archivos, o se puede acceder a ellos en su totalidad mediante WebDAV en `https://<your-server>/remote.php/dav/files/<uid>/`.
- **Contactos**: se pueden exportar como archivo `.vcf` desde la app Contactos (seleccionar todo → Exportar).
- **Calendario**: se puede exportar como archivo `.ics` desde la app Calendario (Configuración del calendario → Exportar).
- **Exportación de datos personales**: los usuarios pueden solicitar una exportación completa de datos en Ajustes personales → Información personal → desplazarse hasta el final → **Descargar sus datos**. Esto genera un archivo ZIP con los archivos, los contactos y los datos del calendario.

Como administrador, puede exportarse el calendario de un usuario desde la línea de comandos:

```
sudo -E -u www-data php occ dav:export-calendar <uid> <calendar-name> <output-file>
```

### Derecho de rectificación (artículo 16)

Los usuarios pueden corregir sus propios datos de perfil en Ajustes personales → Información personal. Los administradores pueden actualizar el nombre mostrado, el correo electrónico y otros campos del perfil con:

```
sudo -E -u www-data php occ user:setting <uid> settings email <new-email>
sudo -E -u www-data php occ user:setting <uid> settings displayname <new-name>
```

En el caso de los campos almacenados en un directorio LDAP o SAML conectado, las correcciones deben hacerse en el directorio de origen y no en Nextcloud.

### Derecho a la limitación del tratamiento (artículo 18)

Para suspender el tratamiento sin eliminar una cuenta, desactivarla:

```
sudo -E -u www-data php occ user:disable <uid>
```

Una cuenta desactivada no puede iniciar sesión y no se ejecuta ningún trabajo en segundo plano para ella. La cuenta y todos sus datos permanecen intactos y pueden volver a activarse en cualquier momento:

```
sudo -E -u www-data php occ user:enable <uid>
```
````
