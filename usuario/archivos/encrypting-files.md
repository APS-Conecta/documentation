---
tipo: explicacion
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Qué hace el cifrado del lado del servidor, sus preguntas frecuentes, cómo afecta a los recursos compartidos y qué archivos no se cifran."
---
# Usar el cifrado del lado del servidor

## Resumen

Esta página explica qué protege el cifrado del lado del servidor y qué no, responde preguntas frecuentes sobre cómo deshabilitarlo y describe qué debe hacer el usuario cuando se activa, cómo afecta a los archivos compartidos y qué archivos quedan sin cifrar. Está dirigida a usuarios de un servidor con el cifrado habilitado.

````{upstream} user_manual/files/encrypting_files.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud incluye una aplicación de cifrado del lado del servidor y, cuando su administrador de Nextcloud la habilita, todos sus archivos de datos de Nextcloud se cifran automáticamente en el servidor. El cifrado abarca todo el servidor, así que, cuando está habilitado, no puede elegir mantener sus archivos sin cifrar. No tiene que hacer nada especial, ya que el cifrado usa su inicio de sesión de Nextcloud como contraseña de su clave privada de cifrado única. Simplemente cierre sesión y vuelva a iniciarla, y gestione y comparta sus archivos como lo hace normalmente; además, puede seguir cambiando su contraseña cuando quiera.

Su función principal es cifrar archivos en servicios de almacenamiento remoto que están conectados a su servidor Nextcloud. Esto es una manera sencilla y transparente de proteger sus archivos en almacenamiento remoto. Puede compartir sus archivos remotos a través de Nextcloud del mismo modo, pero no puede compartir sus archivos cifrados directamente desde el servicio remoto que está usando, porque las claves de cifrado están almacenadas en su servidor Nextcloud, y nunca se exponen a proveedores de servicio externos.

Si su servidor Nextcloud no está conectado a ningún servicio de almacenamiento remoto, es mejor usar otra forma de cifrado, como el cifrado a nivel de archivo o de disco completo. Como las claves se guardan en su servidor Nextcloud, es posible que su administrador de Nextcloud acceda a sus archivos sin cifrar y, si el servidor se ve comprometido, el intruso podría obtener acceso a sus archivos. (Lea [El cifrado en Nextcloud](https://nextcloud.com/blog/encryption-in-nextcloud/) para obtener más información.)

### Preguntas más frecuentes de cifrado

#### ¿Cómo se puede deshabilitar el cifrado?

La única forma de deshabilitar el cifrado es ejecutar el script [«decrypt all»](https://docs.nextcloud.com/server/latest/admin_manual/occ_command.html#encryption-label), que descifra todos los archivos y deshabilita el cifrado.

#### ¿Es posible deshabilitar el cifrado con la clave de recuperación?

Sí, *si* todos los usuarios usan la [clave de recuperación de archivos](https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/encryption_configuration.html#enabling-users-file-recovery-keys), [«decrypt all»](https://docs.nextcloud.com/server/latest/admin_manual/occ_command.html#encryption-label) la usará para descifrar todos los archivos.

#### ¿Puede deshabilitarse el cifrado sin la contraseña del usuario?

Si no tiene la contraseña del usuario o [el archivo con la clave de recuperación](https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/encryption_configuration.html#enabling-users-file-recovery-keys) del usuario, resultará imposible desencriptar todos los archivos. Además, ejecutarlo al iniciar sesión podría ser peligroso, ya que probablemente se agotaría el tiempo máximo de la petición.

#### ¿Hay planes para mover esto al siguiente inicio de sesión del usuario o una tarea en segundo plano?

Si hiciéramos eso, entonces tendríamos que guardar su contraseña de inicio de sesión en la base de datos. Esto puede ser visto como un problema de seguridad, así que no hay ningún plan similar.

#### ¿Es posible compartir con grupos con la clave de recuperación?

Si se refiere añadir usuarios a grupos y que funcione mágicamente, no. Esto solo funciona con la clave maestra.

### Usar el cifrado

El cifrado de Nextcloud es del tipo "actívalo y olvídate", pero tiene unas cuantas opciones que puede usar.

Cuando su administrador de Nextcloud activa el cifrado por primera vez, debe cerrar sesión y reabrirla para crear sus claves de cifrado y cifrar sus archivos. Cuando el cifrado ha sido habilitado en su servidor Nextcloud, verá un cartel amarillo en su página de Archivos, indicándole que cierre sesión y la abra de nuevo.

Cuando inicie sesión de nuevo, puede que tarde unos minutos en conseguirlo, en función del número de archivos que tenga. A continuación volverá a su página por defecto de Nextcloud.

:::{note}
Nunca debe perder su contraseña de Nextcloud, porque perdería el acceso a sus archivos. No obstante, existe una opción de recuperación opcional que su administrador de Nextcloud puede habilitar; consulte la sección Contraseña de la Clave de Recuperación (más abajo) para obtener más información.
:::

### Compartir archivos cifrados

Solo aquellos usuarios que tengan claves de cifrado privadas tienen acceso a archivos y carpetas cifrados compartidos. Los usuarios que aún no han creado su clave de cifrado privada no tendrán acceso a archivos compartidos cifrados; verán carpetas y nombres de archivo, pero no podrán abrir ni descargar los archivos. Verán un cartel amarillo de aviso indicando «La app de cifrado está habilitada pero sus claves no se han inicializado, por favor, cierre la sesión y vuelva a iniciarla de nuevo.»

Los propietarios de archivos o carpetas compartidas deberán re-compartir archivos tras la activación del cifrado; los usuarios que intenten acceder al recurso compartido verán un mensaje indicando que soliciten al propietario del recurso compartido que re-comparta el archivo con ellos. Para archivos compartidos a un solo usuario, deje de compartir y vuelva a compartirlo. Para archivos compartidos a un grupo, compártalos con los individuos que no puedan acceder. Esta acción actualiza el cifrado, y a continuación el propietario del recurso compartido puede borrar los usuarios añadidos de forma individual.

#### Contraseña de la Clave de Recuperación

Si su administrador de Nextcloud ha habilitado la herramienta de la clave de recuperación, usted puede utilizarla para su cuenta. Si habilita "Recuperación por contraseña", el administrador puede leer sus datos con una contraseña especial. Esta característica permite al administrador recuperar sus archivos si usted pierde su contraseña de Nextcloud. Si la clave de recuperación no está habilitada, no hay manera de restaurar sus archivos si pierde su contraseña de inicio de sesión.

### Archivos no cifrados

Solo se cifran los datos de sus archivos, no los nombres de archivo ni las estructuras de carpetas. Estos archivos nunca se cifran:

- Los archivos antiguos de la papelera.
- Las miniaturas de imágenes de la aplicación Galería.
- Las vistas previas de la aplicación Archivos.
- El índice de búsqueda de la aplicación de búsqueda de texto completo.
- Los datos de aplicaciones de terceros

#### Cambiar la contraseña de la clave privada

Esta opción solo está disponible si la contraseña de cifrado no ha sido cambiada por el administrador, sino que solo se ha modificado la contraseña de inicio de sesión. Esto puede ocurrir si su proveedor de Nextcloud utiliza un soporte de usuarios externo (por ejemplo, LDAP) y ha cambiado su contraseña de inicio de sesión usando la configuración del soporte externo. En ese caso, usted puede cambiar su contraseña de cifrado a su nueva contraseña de inicio de sesión al proporcionar su antigua y nueva contraseña de inicio de sesión. La aplicación Cifrado solo funciona si su contraseña de inicio de sesión y su contraseña de cifrado son idénticas.
````
