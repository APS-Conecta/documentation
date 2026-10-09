---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Usar montajes de almacenamiento externo en Archivos: estado de la conexión, compartir, añadir montajes propios y backends compatibles."
---
(nc-external_storage_user_label)=
# Usar almacenamiento externo

## Resumen

Esta página explica cómo se ven y se usan los montajes de almacenamiento externo en la vista Archivos, cómo compartir desde ellos, cómo añadir montajes propios cuando el administrador lo permite y qué backends puede haber. Está dirigida a usuarios que trabajan con archivos alojados en sistemas de archivos remotos.

````{upstream} user_manual/files/external_storage.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La aplicación Almacenamiento externo permite que el servidor Nextcloud se conecte a sistemas de archivos remotos —como Amazon S3, servidores SFTP, recursos compartidos SMB/CIFS o servidores WebDAV— y los presente como carpetas dentro de la vista Archivos. El equipo de administración configura qué backends están disponibles y qué montajes se comparten con el usuario.

Si el administrador ha habilitado el almacenamiento externo gestionado por los usuarios, también se pueden añadir conexiones propias en los Ajustes personales.

### Acceder al almacenamiento externo

Los montajes de almacenamiento externo aparecen como carpetas normales en la vista Archivos. En ellos se pueden explorar, subir, descargar y eliminar archivos igual que en cualquier otra carpeta. Que se pueda compartir depende de si el administrador lo ha habilitado en cada montaje individual.

Un indicador de color junto al nombre de la carpeta muestra el estado de la conexión:

- Verde: el almacenamiento está conectado y listo para usarse.
- Amarillo: no se pudo acceder al almacenamiento; Nextcloud volverá a intentarlo automáticamente.
- Rojo: el almacenamiento no está disponible. Si esto persiste, contactar con el administrador.

Cuando un montaje no está disponible, Nextcloud lo marca como sin conexión durante diez minutos antes de volver a intentarlo. Se puede forzar una nueva comprobación manual haciendo clic en el indicador de estado.

:::{note}
Algunos montajes de almacenamiento externo pueden ser de solo lectura. En un montaje de solo lectura no se pueden subir ni eliminar archivos.
:::

### Compartir archivos desde el almacenamiento externo

Compartir desde un montaje de almacenamiento externo funciona igual que compartir cualquier otro archivo o carpeta: se usa el icono de compartir de la vista Archivos. El administrador debe habilitar explícitamente la compartición en cada montaje, por lo que es posible que el icono de compartir no esté disponible en todos los montajes.

:::{note}
El cifrado del lado del servidor no está disponible para los montajes externos que apuntan a otras instancias de Nextcloud.
:::

### Añadir almacenamiento externo propio

Si el administrador ha habilitado el almacenamiento externo gestionado por los usuarios, se pueden conectar servicios de almacenamiento propios en **Ajustes personales → Almacenamiento externo**.

Para añadir un montaje nuevo:

1. Hacer clic en el icono de perfil y seleccionar **Ajustes personales**.
2. Seleccionar **Almacenamiento externo** en la barra lateral izquierda.
3. Elegir un backend en el desplegable **Añadir almacenamiento**.
4. Completar los campos obligatorios del backend (dirección del servidor, ruta, credenciales, etc.).
5. Seleccionar un método de autenticación en el desplegable **Autentificación**.

Los campos obligatorios se marcan con un borde rojo. Una vez completados todos los campos obligatorios, el montaje se guarda automáticamente.

Un punto verde junto al montaje confirma que la conexión se estableció correctamente. Un icono rojo o amarillo significa que Nextcloud no pudo conectarse: revisar las credenciales y la configuración de red.

Para quitar un montaje, abrir el menú adicional de tres puntos que hay junto a él y seleccionar **Eliminar**.

:::{note}
Los montajes añadidos en los Ajustes personales solo son visibles para la propia cuenta.
:::

### Backends compatibles

Según lo que haya habilitado el administrador, pueden estar disponibles los siguientes backends:

- **Amazon S3**: buckets de Amazon Simple Storage Service y almacenamiento compatible con S3.
- **FTP**: servidores FTP y FTPS.
- **Nextcloud / ownCloud**: otra instancia de Nextcloud u ownCloud a través de WebDAV.
- **OpenStack Object Storage**: buckets de OpenStack Swift.
- **SFTP**: servidores SSH File Transfer Protocol.
- **SMB / CIFS**: recursos compartidos de archivos de Windows y servidores Samba.
- **WebDAV**: cualquier servidor compatible con WebDAV.

Para obtener detalles de configuración específicos de cada backend, consultar [Configurar el almacenamiento externo (GUI)](https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/external_storage_configuration_gui.html) en el manual de administración.

### Detección de cambios en los archivos

Los archivos que se añaden o modifican a través de Nextcloud se reflejan de inmediato. Los archivos añadidos o modificados directamente en el almacenamiento externo, sin pasar por Nextcloud, pueden no aparecer hasta el siguiente escaneo en segundo plano.

Si los archivos añadidos externamente no aparecen, pedir al administrador que ejecute `occ files:scan` o que configure un escaneo periódico en segundo plano para el montaje.
````
