---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Activar y configurar el almacenamiento externo: montajes, autenticación, variables de ruta, permisos, opciones de montaje, backends y codificación de nombres."
---
# Configuración del almacenamiento externo

## Resumen

Esta página explica cómo activar la app de almacenamiento externo y configurar montajes desde la interfaz: backends y autenticación, nombre de carpeta, variables en la ruta de montaje, permisos por usuario y grupo, opciones de montaje, montajes de usuario, detección de archivos nuevos y problemas de codificación de nombres. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/external_storage_configuration_gui.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La aplicación Soporte de almacenamiento externo permite montar servicios y dispositivos de almacenamiento externo como dispositivos de almacenamiento secundarios de Nextcloud. También puede permitirse que los usuarios monten sus propios servicios de almacenamiento externo.

### Activación

El soporte de almacenamiento externo lo proporciona una app incluida (instalada automáticamente). Está desactivada de forma predeterminada, así que para usar esta función basta con activarla en **Apps**.

### Configuración

Para acceder a los ajustes de configuración de los montajes de almacenamiento externo, hacer clic en el icono del **perfil** y seleccionar **Ajustes** en el desplegable. En el lado izquierdo, bajo **Administración**, seleccionar **Almacenamiento externo**.

:::{note}
El almacenamiento externo también puede configurarse con el comando occ. Consultar la {nc-ref}`documentación de occ <files_external_label>`.
:::

Para crear un nuevo montaje de almacenamiento externo, seleccionar un backend disponible en el desplegable **Añadir almacenamiento**. Cada backend tiene distintas opciones obligatorias, que se configuran en los campos de configuración.

Cada backend también puede aceptar varios métodos de autenticación. Se seleccionan con el desplegable bajo **Autentificación**. Los distintos backends admiten distintos mecanismos de autenticación; algunos son propios del backend, mientras que otros son más genéricos. Consultar {nc-doc}`admin_manual/configuration_files/external_storage/auth_mechanisms` para obtener información más detallada.

Al seleccionar un mecanismo de autenticación, los campos de configuración cambian según corresponda al mecanismo elegido. Por ejemplo, el backend SFTP admite **Nombre de usuario y contraseña**, **Credenciales de login, guardar en la sesión** y **Clave pública RSA**.

Los campos obligatorios se marcan con un borde rojo. Cuando todos los campos obligatorios están rellenos, el almacenamiento se guarda automáticamente. Un punto verde junto a la fila del almacenamiento indica que el almacenamiento está listo para usarse. Un icono rojo o amarillo indica que Nextcloud no pudo conectarse al almacenamiento externo, por lo que hay que volver a comprobar la configuración y la disponibilidad de la red.

Si hay un error en el almacenamiento, se marcará como no disponible durante diez minutos. Para volver a comprobarlo, hacer clic en el icono de color o volver a cargar la página de administración.

### Nombre de la carpeta

{guilabel}`Nombre de la carpeta` es el nombre que tendrá la carpeta dentro de Nextcloud, es decir, el nombre que verán los usuarios de Nextcloud.

Hay que tener en cuenta que el nombre de la carpeta no puede incluir una ruta ni un subdirectorio: no incluir barras en {guilabel}`Nombre de la carpeta`.

### Uso de variables en las rutas de montaje

El mecanismo de montaje de almacenamiento externo acepta variables en la ruta de montaje.

Usar `$user` para que se sustituya automáticamente por el nombre de usuario del usuario que ha iniciado sesión.

Usar `$home` para que se sustituya automáticamente por una variable configurable de directorio personal (requiere LDAP; consultar {nc-ref}`Atributos especiales <ldap_special_attributes>` en la documentación de configuración de LDAP para los detalles).

En el siguiente ejemplo, el punto de montaje de un usuario «alice» que ha iniciado sesión se resolvería en `/opt/userDirectories/alice/myPictures`. La pantalla muestra la sustitución de la variable de usuario en un almacenamiento externo.

### Permisos de usuarios y grupos

Un almacenamiento configurado en los ajustes personales de un usuario solo está disponible para el usuario que lo creó. Un almacenamiento configurado en las configuraciones de administración está disponible de forma predeterminada para todos los usuarios, pero puede restringirse a usuarios y grupos concretos en el campo **Disponible para**.

(nc-external_storage_mount_options_label)=
### Opciones de montaje

El menú adicional (tres puntos) muestra los iconos de ajustes y de papelera. Hacer clic en la papelera para eliminar el punto de montaje. El botón de ajustes permite configurar cada montaje de almacenamiento por separado con las siguientes opciones:

- Cifrado
- Vistas previas
- Habilitar el uso compartido
- Frecuencia de comprobación del sistema de archivos (Nunca, Una vez en cada acceso)
- Compatibilidad NFD de Mac
- Solo lectura

La casilla **Cifrado** solo es visible cuando la app de cifrado está activada. Hay que tener en cuenta que el cifrado en el servidor no está disponible para otros servidores Nextcloud usados como almacenamiento externo.

**Habilitar el uso compartido** permite al administrador de Nextcloud activar o desactivar la compartición en puntos de montaje individuales. Cuando la compartición está desactivada, los recursos compartidos se conservan internamente, de modo que puede volver a activarse la compartición y los recursos compartidos anteriores vuelven a estar disponibles. La compartición está desactivada de forma predeterminada.

### Uso de certificados autofirmados

Cuando se usan certificados autofirmados para montajes de almacenamiento externo, el certificado debe importarse en los ajustes personales del usuario. Consultar [Montaje externo HTTPS en Nextcloud](https://ownclouden.blogspot.de/2014/11/owncloud-https-external-mount.html) para obtener más información.

### Backends de almacenamiento disponibles

La app de almacenamientos externos proporciona los siguientes backends.

- {nc-doc}`admin_manual/configuration_files/external_storage/amazons3`
- {nc-doc}`admin_manual/configuration_files/external_storage/ftp`
- {nc-doc}`admin_manual/configuration_files/external_storage/local`
- {nc-doc}`admin_manual/configuration_files/external_storage/nextcloud`
- {nc-doc}`admin_manual/configuration_files/external_storage/openstack`
- {nc-doc}`admin_manual/configuration_files/external_storage/sftp`
- {nc-doc}`admin_manual/configuration_files/external_storage/smb`
- {nc-doc}`admin_manual/configuration_files/external_storage/webdav`

:::{note}
Para que estos backends funcionen, se necesita una configuración de SELinux que no bloquee o que esté configurada correctamente. Consultar {nc-ref}`Configuración de SELinux <selinux-config-label>`.
:::

### Permitir que los usuarios monten almacenamiento externo

Marcar **Habilitar el almacenamiento externo de usuario** para permitir que los usuarios monten sus propios servicios de almacenamiento externo, y marcar los backends que se quieren permitir. Atención: ¡esto permite que un usuario establezca conexiones potencialmente arbitrarias con otros servicios de la red!

### Añadir archivos al almacenamiento externo

Se recomienda configurar el trabajo en segundo plano **Webcron** o **Cron** (consultar {nc-doc}`admin_manual/configuration_server/background_jobs_configuration`) para que Nextcloud detecte automáticamente los archivos añadidos a los almacenamientos externos.

Es posible que Nextcloud no siempre pueda detectar los cambios hechos de forma remota (archivos modificados sin pasar por Nextcloud), sobre todo cuando los archivos están en lo profundo de la jerarquía de carpetas del almacenamiento externo.

Puede ser necesario configurar un trabajo cron que ejecute `sudo -E -u www-data php occ files:scan --all` (o sustituir `--all` por el nombre de usuario; consultar también {nc-doc}`admin_manual/occ_command`) para lanzar periódicamente (por ejemplo, cada 15 minutos) un nuevo análisis de los archivos del usuario, que incluye el almacenamiento externo montado.

Si se usa Nextcloud AIO, el comando equivalente en ese entorno es `sudo docker exec --user www-data -it nextcloud-aio-nextcloud php occ files:scan --all`.

(nc-trouble-file-encoding-ext-storages)=
### Solución de problemas de codificación de nombres de archivo

Al usar almacenamiento externo, puede ocurrir que algunos archivos con caracteres especiales no aparezcan en la lista de archivos, o que aparezcan pero no sean accesibles.

Cuando ocurra, ejecutar el {nc-ref}`analizador de archivos <occ_files_scan_label>`, por ejemplo:

```
sudo -E -u www-data php occ files:scan --all
```

Si el analizador informa de un problema de codificación en el archivo afectado, activar la compatibilidad con la codificación de Mac en las {nc-ref}`opciones de montaje <external_storage_mount_options_label>` y después {nc-ref}`volver a analizar el almacenamiento externo <occ_files_scan_label>`.

:::{note}
Este modo afecta al rendimiento, porque Nextcloud siempre probará ambas codificaciones al detectar archivos en los almacenamientos externos.

Los computadores Mac usan la normalización Unicode NFD para los nombres de archivo, que es distinta de NFC, la que usan otros sistemas operativos. Los usuarios de Mac podrían subir archivos directamente al almacenamiento externo con nombres de archivo normalizados en NFD. Al subir a través de Nextcloud, los nombres de archivo siempre se normalizan al estándar NFC por coherencia.

Se recomienda que los almacenamientos externos se usen exclusivamente a través de Nextcloud para evitar estos problemas.

Consultar también la [explicación técnica sobre las normalizaciones NFC y NFD](https://www.win.tue.nl/~aeb/linux/uc/nfc_vs_nfd.html).
:::
````
