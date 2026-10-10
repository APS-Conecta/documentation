---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Ajustes de compartición de archivos, ajustes avanzados con occ, caducidad de recursos compartidos, transferencia de archivos y enlaces de entrega."
---
(nc-file-sharing-configuration)=
# Compartición de archivos

## Resumen

Esta página describe los ajustes de la sección de compartición de la página de administración, los ajustes avanzados que solo se cambian con `occ`, la caducidad de los recursos compartidos y su aviso, la transferencia de archivos entre usuarios, los recursos compartidos persistentes y los enlaces de entrega de archivos. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/file_sharing_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los usuarios de Nextcloud pueden compartir archivos con sus grupos de Nextcloud y con otros usuarios del mismo servidor Nextcloud, con usuarios de Nextcloud de {nc-doc}`otros servidores Nextcloud <admin_manual/configuration_files/federated_cloud_sharing_configuration>`, y crear recursos compartidos públicos para personas que no son usuarios de Nextcloud. Es posible controlar varios permisos de usuario sobre los recursos compartidos de archivos.

La política de compartición se configura en la sección Compartir de la página de administración.

- Marcar {guilabel}`Permitir a las aplicaciones utilizar la API de Compartir` para permitir que los usuarios compartan archivos. Si no está marcado, ningún usuario puede crear recursos compartidos de archivos.

  - Marcar {guilabel}`Permitir que se vuelva a compartir` para permitir que los usuarios vuelvan a compartir los archivos que se han compartido con ellos.
  - Marcar {guilabel}`Permitir compartir con grupos` para permitir que los usuarios compartan con grupos.
  - Marcar {guilabel}`Limitar a los usuarios a compartir solo con los usuarios de sus grupos` para limitar la compartición a la pertenencia a grupos. Al marcarlo, aparece una lista desplegable opcional de grupos que se ignoran al comprobar la pertenencia a grupos. Escribir cualquier nombre de grupo para buscarlo.

    - Los grupos añadidos a {guilabel}`Ignorar los siguientes grupos cuando se verifique la pertenencia a grupos` no se tendrán en cuenta para determinar si los usuarios están en los mismos grupos y pueden compartir entre sí.

    :::{note}
    Este ajuste no se aplica a la función de compartición federada en la nube. Si la {nc-doc}`compartición federada en la nube <admin_manual/configuration_files/federated_cloud_sharing_configuration>` está activada, los usuarios pueden seguir compartiendo elementos con cualquier usuario de cualquier instancia (incluida aquella en la que están) mediante un recurso compartido remoto.
    :::

- Marcar `Allow users to share via link and email` para permitir crear recursos compartidos públicos, mediante un hipervínculo, para personas que no son usuarios de Nextcloud.

  - Marcar {guilabel}`Permitir subidas públicas` para permitir que cualquier persona suba archivos a los recursos compartidos públicos.
  - Marcar {guilabel}`Pedir siempre la contraseña` para pedir de forma proactiva al usuario que establezca una contraseña para un enlace compartido.
  - Marcar {guilabel}`Forzar la protección por contraseña` para obligar a los usuarios a establecer una contraseña en todos los enlaces compartidos públicos. No se aplica a los recursos compartidos con usuarios y grupos locales.
  - Añadir grupos a {guilabel}`Excluir grupos de la creación de enlaces de recursos compartidos` para no aplicar los ajustes a esos grupos.

- Marcar `Exclude groups from sharing` para impedir que los miembros de grupos concretos creen recursos compartidos de archivos en esos grupos. Al marcarlo, aparece una lista desplegable con todos los grupos para elegir. Escribir cualquier nombre de grupo para buscarlo. Los miembros de los grupos excluidos pueden seguir recibiendo recursos compartidos, pero no crear ninguno.
- Marcar `Set default expiration date for shares` para establecer una fecha de caducidad predeterminada en los recursos compartidos con usuarios y grupos locales.

  - Marcar {guilabel}`Forzar expiración` para imponer siempre la fecha de caducidad configurada en los recursos compartidos con usuarios y grupos locales.

    :::{note}
    Los usuarios no podrán establecer una fecha de caducidad más lejana en el futuro que la fecha de caducidad impuesta, aunque sí podrán establecer una fecha más próxima. Hay que tener en cuenta también que los usuarios podrán volver a actualizar la fecha de caducidad más adelante. La fecha de caducidad se basa en la fecha actual y no en la fecha de creación del recurso compartido. El usuario podrá volver a ampliar la fecha de caducidad siempre que una fecha de caducidad anterior esté a punto de alcanzarse.
    :::

- Marcar `Set default expiration date for shares via link or email` para establecer una fecha de caducidad predeterminada en los recursos compartidos públicos.

  - Marcar {guilabel}`Forzar expiración` para imponer siempre la fecha de caducidad configurada en los recursos compartidos públicos.

    :::{note}
    Los usuarios no podrán establecer una fecha de caducidad más lejana en el futuro que la fecha de caducidad impuesta, aunque sí podrán establecer una fecha más próxima. Hay que tener en cuenta también que los usuarios podrán volver a actualizar la fecha de caducidad más adelante. La fecha de caducidad se basa en la fecha actual y no en la fecha de creación del recurso compartido. El usuario podrá volver a ampliar la fecha de caducidad siempre que una fecha de caducidad anterior esté a punto de alcanzarse.
    :::

- Marcar `Allow username autocompletion in share dialog and allow access to the system address book` para activar el autocompletado de los nombres de usuario de Nextcloud y mostrar la libreta de direcciones del sistema como recurso al sincronizar los contactos mediante CardDAV.

  - Marcar `Allow username autocompletion to users within the same groups and limit system address books to users in the same groups` para limitar el autocompletado de nombres de usuario a los usuarios que pertenecen a los mismos grupos que el propietario del recurso compartido.
  - Marcar `Allow username autocompletion to users based on phone number integration` para limitar el autocompletado de nombres de usuario a los usuarios cuando el propietario del recurso compartido ha sincronizado su libreta de direcciones del teléfono mediante los clientes móviles de Nextcloud Talk y esta contenía el número de teléfono que el usuario configuró en su perfil.

- Marcar `Allow autocompletion when entering the full name or email address (ignoring missing phonebook match and being in the same group)` para mostrar, a pesar de las restricciones anteriores, una sugerencia de usuario cuando se ha escrito el nombre mostrado o el ID de usuario completos.
- Marcar `Show disclaimer text on the public link upload page` para establecer y mostrar un texto de aviso legal en los enlaces públicos con listas de archivos ocultas. Al activar esta función, aparece un campo de texto para introducir el texto de aviso legal.

Con {guilabel}`Permisos por defecto para recurso compartido` es posible establecer los permisos predeterminados de los recursos compartidos con usuarios ({guilabel}`Crear`, {guilabel}`Cambiar`, {guilabel}`Eliminar` y {guilabel}`Volver a compartir`) sin imponerlos.

:::{note}
Nextcloud no conserva el mtime (fecha de modificación) de los directorios, aunque sí actualiza el mtime de los archivos. Consultar [Fecha de carpeta incorrecta al sincronizar](https://github.com/owncloud/core/issues/7009) para ver la discusión al respecto.
:::

:::{note}
Hay más opciones de compartición disponibles en el nivel de config.php: [Parámetros de configuración](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/config_sample_php_parameters.html#sharing)
:::

(nc-transfer_userfiles_label)=
### Ajustes avanzados

Estos son algunos ajustes para casos límite que no pueden editarse desde la interfaz web, porque solo son útiles para un pequeño subconjunto de administradores.

Pueden actualizarse con el comando `occ`, por ejemplo:

```bash
occ config:app:set core shareapi_restrict_user_enumeration_full_match_email --value yes
```

- `core.shareapi_restrict_user_enumeration_full_match_ignore_second_display_name`
  - Cuando la coincidencia completa está activada, ignorar el segundo nombre mostrado añadido.
  - Valor predeterminado: `no`
  - Ejemplos:

    | Valor del ajuste | Consulta de búsqueda | Nombre de usuario | Coincidirá |
    |---|---|---|---|
    | `yes` | User 1 | User 1 (segundo nombre mostrado) | sí |
    | `no` | User 1 | User 1 (segundo nombre mostrado) | no |

- `core.shareapi_restrict_user_enumeration_full_match_userid`
  - Cuando la coincidencia completa está activada, no hacer coincidir con el ID de usuario
  - Valor predeterminado: `yes`

- `core.shareapi_restrict_user_enumeration_full_match_email`
  - Cuando la coincidencia completa está activada, no hacer coincidir con el correo electrónico del usuario
  - Valor predeterminado: `yes`

### Distinguir entre la fecha de caducidad máxima y la fecha de caducidad predeterminada

La fecha de caducidad que puede establecerse e imponerse en los ajustes anteriores es a la vez el límite estricto y el valor predeterminado. A veces los administradores quieren tener una fecha de caducidad predeterminada moderada, por ejemplo 7 días, pero asegurarse de que el usuario no pueda ampliarla a más de 14 días.

Para ello, establecer una fecha de caducidad impuesta en los ajustes, como se ha descrito más arriba, y establecer el valor predeterminado en algo por debajo de la fecha de caducidad máxima posible con los siguientes comandos OCC:

```
occ config:app:set --value <DAYS> core internal_defaultExpDays
occ config:app:set --value <DAYS> core link_defaultExpDays
```

### Recibir una notificación antes de que caduque un recurso compartido

Los usuarios pueden recibir una notificación antes de que caduque un recurso compartido. Para ello, debe configurarse un trabajo cron que llame una vez al día al siguiente comando OCC:

```
occ sharing:expiration-notification
```

Se enviará una notificación por cada recurso compartido que caduque en las próximas 24 horas.

### Transferir archivos a otro usuario

Es posible transferir archivos de un usuario a otro con `occ`. Es útil cuando hay que eliminar un usuario. ¡Asegurarse de transferir los archivos antes de eliminar el usuario! Esto transfiere todos los archivos de user1 a user2, junto con los recursos compartidos y la información de metadatos asociados a esos archivos (recursos compartidos, etiquetas, comentarios, etc.). El contenido de la papelera no se transfiere:

```
occ files:transfer-ownership user1 user2
```

(Consultar {nc-doc}`admin_manual/occ_command` para una referencia completa de `occ`).

Los usuarios también pueden transferir por sí mismos archivos o carpetas de forma selectiva. Consultar la [documentación de usuario](https://docs.nextcloud.com/server/latest/user_manual/en/files/transfer_ownership.html) para los detalles.

### Crear recursos compartidos de archivos persistentes

Cuando se elimina un usuario, también se eliminan sus archivos. Como puede imaginarse, esto es un problema si creó recursos compartidos de archivos que deben conservarse, porque también desaparecen. En Nextcloud los archivos están ligados a sus propietarios, así que lo que le ocurra al propietario del archivo también les ocurre a los archivos.

Una solución es crear recursos compartidos persistentes para los usuarios. Es posible conservar su propiedad o crear un usuario especial con el fin de establecer recursos compartidos de archivos permanentes. Basta con crear una carpeta compartida de la forma habitual y compartirla con los usuarios o grupos que necesiten usarla. Establecer los permisos adecuados en ella y, así, sin importar qué usuarios lleguen y se vayan, los recursos compartidos de archivos se mantendrán. Porque todos los archivos que se añaden al recurso compartido, o que se editan en él, pasan automáticamente a ser propiedad del propietario del recurso compartido, independientemente de quién los añada o los edite.

### Usar enlaces de recurso compartido de entrega de archivos

Un recurso compartido de entrega de archivos permite a los usuarios subir archivos a Nextcloud mediante una sesión no autenticada. Los enlaces de recurso compartido de entrega de archivos solo funcionan cuando {guilabel}`Permitir subidas públicas` está marcado en la sección Compartir de la página Configuraciones de administración.

:::{note}
Los recursos compartidos de entrega de archivos tienen actualmente una limitación: los archivos subidos mediante una sesión no autenticada no se fragmentan. Por tanto, el tamaño máximo de archivo que puede subirse mediante recursos compartidos de entrega de archivos depende por completo de los ajustes establecidos en el entorno.
:::
````
