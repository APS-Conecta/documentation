---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Conectar un servidor SMB/CIFS como almacenamiento externo: requisitos, datos, mayúsculas y minúsculas, y notificaciones de actualización con occ."
---
# SMB/CIFS

## Resumen

Esta página explica cómo conectar un servidor de archivos Windows u otro servidor compatible con SMB como almacenamiento externo: los requisitos, los datos necesarios, la opción de sistema de archivos sensible a mayúsculas y las notificaciones de actualización. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/external_storage/smb.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud puede conectarse a servidores de archivos Windows u otros servidores compatibles con SMB mediante el backend SMB/CIFS.

:::{note}
El backend SMB/CIFS requiere que `smbclient` o el módulo smbclient de PHP (`php-smbclient` / `libsmbclient-php`) estén instalados en el servidor Nextcloud. El módulo smbclient de PHP es **muy preferible**: sin él, el backend recurre a lanzar el binario `smbclient`, que tiene limitaciones conocidas (en particular, las descargas de archivos de más de ~512 MB desde recursos compartidos SMB externos pueden fallar; consultar [nextcloud/server#31308](https://github.com/nextcloud/server/issues/31308)). Deberían estar incluidos en cualquier distribución de Linux. (Consultar [PECL smbclient](https://pecl.php.net/package/smbclient) si la distribución no los incluye).
:::

Se necesita la siguiente información:

- Nombre de la carpeta del punto de montaje local.
- Servidor: la URL del servidor Samba.
- Nombre de usuario: el nombre de usuario o `domain\username` (ver más abajo) que se usa para iniciar sesión en el servidor Samba.
- Contraseña: la contraseña para iniciar sesión en el servidor Samba.
- Compartir: el recurso compartido del servidor Samba que se va a montar.
- Subcarpeta remota: la subcarpeta remota dentro del recurso compartido de Samba que se va a montar (opcional; de forma predeterminada, /). Para asignar automáticamente a la subcarpeta el nombre de usuario de inicio de sesión de Nextcloud, usar `$user` en lugar de un nombre de subcarpeta concreto.
- Y, por último, los usuarios y grupos de Nextcloud que obtienen acceso al recurso compartido.

Opcionalmente, se puede especificar un {guilabel}`Dominio`. Es útil en los casos en que el servidor SMB requiere un dominio y un nombre de usuario, y se usa un mecanismo de autenticación avanzado, como las credenciales de sesión, de modo que el nombre de usuario no puede modificarse. Se concatena con el nombre de usuario, de modo que el backend recibe `domain\username`

:::{note}
Para mejorar la fiabilidad y el rendimiento, se recomienda instalar `libsmbclient-php`, un módulo nativo de PHP para conectarse a servidores SMB.
:::

Consultar {nc-doc}`admin_manual/configuration_files/external_storage_configuration_gui` para ver más opciones de montaje e información.

Consultar {nc-doc}`admin_manual/configuration_files/external_storage/auth_mechanisms` para obtener más información sobre los esquemas de autenticación.

### Sistema de archivos sensible a mayúsculas

Esta opción indica a Nextcloud si el recurso compartido SMB está respaldado por un sistema de archivos que distingue entre mayúsculas y minúsculas. No cambia cómo el servidor SMB almacena los archivos; solo afecta a cómo Nextcloud realiza las búsquedas y valida las rutas.

- **Activada (predeterminado)**: Nextcloud asume que el recurso compartido distingue entre mayúsculas y minúsculas. Las comprobaciones de existencia de archivos usan las mayúsculas y minúsculas exactas, y se permiten los cambios de nombre que solo cambian mayúsculas o minúsculas.
- **Desactivada**: Nextcloud asume que el recurso compartido no distingue entre mayúsculas y minúsculas, y lo compensa analizando las entradas del directorio para encontrar el nombre exacto que se usa en el servidor. También bloquea los cambios de nombre que solo cambian mayúsculas o minúsculas. Esto puede ser más lento en directorios grandes.

Si el ajuste no coincide con el sistema de archivos del servidor SMB, puede producirse un comportamiento confuso:

- Un SMB que no distingue entre mayúsculas y minúsculas (por ejemplo, NTFS o FAT) con la opción activada puede provocar incoherencias o conflictos en la caché, porque Nextcloud puede tratar `File.txt` y `file.txt` como archivos distintos mientras que el servidor los trata como el mismo archivo.
- Un SMB que distingue entre mayúsculas y minúsculas (por ejemplo, ext4) con la opción desactivada puede provocar análisis de directorios innecesarios y el rechazo de cambios de nombre que solo cambian mayúsculas o minúsculas, aunque el propio servidor los permitiría.

### Notificaciones de actualización de SMB

Nextcloud puede usar las notificaciones de actualización de smb para escuchar los cambios hechos en un almacenamiento SMB/CIFS configurado y detectar casi en tiempo real los cambios externos hechos en el almacenamiento.

:::{note}
Debido a limitaciones de los servidores SMB basados en Linux, esta función solo funciona de forma fiable en servidores SMB de Windows.
:::

:::{note}
Usar las notificaciones de actualización requiere `smbclient` 4.x o posterior. Debido a limitaciones del módulo smbclient de PHP, el binario `smbclient` es necesario incluso cuando se usa el módulo de PHP.
:::

Para empezar a escuchar las notificaciones de actualización, iniciar el comando `occ` así:

```
occ files_external:notify <mount_id>
```

El ID de montaje de un almacenamiento concreto puede encontrarse con `occ files_external:list`

De forma predeterminada, este comando no muestra ninguna salida; se puede ver la lista de cambios detectados pasando la opción `-v` al comando.

#### Autenticación SMB

Las notificaciones de actualización no se admiten cuando se usa la autenticación «Credenciales de login, guardar en la sesión». Usar las notificaciones de actualización solo se admite con «Credenciales de inicio de sesión, salvar en la base de datos».

Incluso cuando se usa la autenticación «Credenciales de inicio de sesión, salvar en la base de datos» o «Introducido por el usuario, almacenado en la base de datos», el proceso de notificación no puede usar las credenciales guardadas para conectarse a los recursos compartidos smb, porque el proceso de notificación no se ejecuta en el contexto de un usuario concreto; en esos casos, se pueden proporcionar el nombre de usuario y la contraseña con los argumentos `--username` y `--password`.

#### Reducir el retraso de sincronización

Los cambios que detecte el comando de notificación solo se sincronizarán con el cliente después de que se haya ejecutado el trabajo cron de Nextcloud (normalmente cada 15 minutos). Si este intervalo es demasiado largo para el caso de uso, se puede reducir ejecutando `occ files:scan --unscanned --all` con el intervalo deseado. Hay que tener en cuenta que esto puede aumentar la carga del servidor y que hay que asegurarse de que las ejecuciones no se solapen.

#### Fallo al subir archivos ocultos o archivos ocultos que no se muestran

Si se tiene la configuración `hide dot files = Yes`, no se podrá subir un archivo oculto (un archivo cuyo nombre empieza por punto) ni se podrán mostrar los archivos ocultos en la lista de archivos (aunque la opción «Mostrar archivos ocultos» esté marcada en los ajustes de nextcloud.
Asegurarse de tener la siguiente opción en la configuración: `hide dot files = No`
````
