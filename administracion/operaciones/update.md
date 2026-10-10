---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "El actualizador integrado de Nextcloud: qué hace, cómo usarlo desde la web o la línea de comandos, el modo por lotes y la solución de problemas."
---
# Actualizar con el actualizador integrado

## Resumen

Esta página describe las operaciones que realiza el actualizador integrado de Nextcloud y cómo usarlo paso a paso desde la web o desde la línea de comandos, incluido el modo por lotes no interactivo y la solución de problemas. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/maintenance/update.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El actualizador integrado automatiza muchos de los pasos de la actualización de una instalación de Nextcloud. Es útil para instalaciones sin acceso root, como el alojamiento compartido, y para instalaciones con un número menor de usuarios y datos, y automatiza la actualización de las {nc-doc}`instalaciones manuales <admin_manual/installation/source_installation>`.

:::{warning}
No se admite **volver a una versión anterior** y se corre el riesgo de dañar los datos. Si se quiere volver a una versión anterior de Nextcloud, instalarla desde cero y luego restaurar los datos desde la copia de seguridad. Antes de hacerlo, abrir un ticket de soporte si se cuenta con soporte de pago o pedir ayuda en los foros de {vendor}`Nextcloud` para ver si el problema puede resolverse sin volver a una versión anterior.
:::

:::{danger}
Hay que mantener copias de seguridad periódicas (consultar {nc-doc}`admin_manual/maintenance/backup`) y hacer una copia de seguridad antes de cada actualización. El actualizador integrado no hace copia de seguridad de la base de datos ni del directorio de datos.
:::

### ¿Qué hace el actualizador?

:::{note}
El actualizador integrado en sí solo sustituye los archivos existentes por los de la versión a la que actualiza. La fase de migración, que actualiza la base de datos y las apps, debe ejecutarse después. En modo de línea de comandos, el actualizador ofrece lanzarla justo después de sustituir correctamente el código, ejecutando `occ upgrade` automáticamente. En modo web, el actualizador termina y luego ofrece volver a la URL principal de la instancia para lanzar la interfaz web de la fase de migración.
:::

El actualizador integrado realiza estas operaciones:

- **Comprobar los archivos esperados:** comprueba que solo estén presentes los archivos esperados de una instalación de Nextcloud, porque se observó que algunos archivos que quedaban en el directorio de Nextcloud causaban efectos secundarios que ponían en riesgo el procedimiento de actualización.
- **Comprobar los permisos de escritura:** comprueba si todos los archivos que deben poder escribirse durante el procedimiento de actualización realmente pueden escribirse.
- **Activar el modo de mantenimiento:** activa el modo de mantenimiento para que no se ejecute ninguna otra acción mientras se actualiza el código.
- **Crear copia de seguridad:** crea una copia de seguridad del código existente en `/updater-INSTANCEID/backups/nextcloud-CURRENTVERSION/` dentro del directorio de datos (no contiene el directorio `/data` ni la base de datos).
- **Descarga:** descarga el código de la versión a la que debe actualizar. Esto también se muestra en la interfaz web antes de iniciar la actualización. Este archivo comprimido se descarga en `/updater-INSTANCEID/downloads/`.
- **Extracción:** extrae el archivo comprimido en la misma carpeta.
- **Sustituir los puntos de entrada:** sustituye todos los puntos de entrada de Nextcloud por archivos ficticios para que, mientras se sustituyen esos archivos, todos los clientes sigan recibiendo la respuesta adecuada del modo de mantenimiento. Ejemplos de esos endpoints son `index.php`, `remote.php` o `ocs/v1.php`.
- **Eliminar los archivos antiguos:** elimina todos los archivos excepto los puntos de entrada mencionados, el directorio de datos y el de configuración, así como las apps y los temas que no vienen incluidos. (Y, por supuesto, el propio actualizador)
- **Mover los archivos nuevos a su lugar:** mueve a su lugar los archivos del archivo comprimido extraído.
- **¿Mantener activo el modo de mantenimiento?:** pregunta si el modo de mantenimiento debe mantenerse activo. Esto permite al administrador usar el actualizador web pero ejecutar los pasos de migración propiamente dichos (`occ upgrade`) en la línea de comandos. Si el modo de mantenimiento se mantiene activo, se requiere acceso a la línea de comandos. Para usar la página web de actualización, desactivar el modo de mantenimiento y hacer clic en el enlace para ir a la página de actualización. (Este paso solo está disponible en el actualizador web).
- **Listo** la actualización del código ha terminado y hay que ir a la página enlazada o a la línea de comandos para terminar la actualización ejecutando los pasos de migración.

### Usar el actualizador web

Actualizar la instalación de Nextcloud con el actualizador integrado lleva solo unos pocos pasos:

1. Debería verse una notificación en la parte superior de cualquier página de Nextcloud cuando hay una nueva actualización disponible. Ir a la página de configuraciones de administración y desplazarse hasta la sección «Versión». Esta sección tiene un botón para abrir el actualizador. Esta sección, así como la notificación de actualización, solo está disponible si la app de notificación de actualizaciones está activada en la gestión de apps.

2. Hacer clic en el botón «Abrir el actualizador».

3. Verificar la información que se muestra y hacer clic en el botón «Iniciar actualización» para iniciar la actualización.

4. Si ocurre un error o la comprobación falla, el actualizador detiene el proceso e informa de ello. Entonces puede intentarse resolver el problema y hacer clic en el botón «Retry update». Esto continuará la actualización y volverá a ejecutar el paso fallido. No volverá a ejecutar los pasos anteriores que se completaron correctamente.

5. Si se cierra el actualizador antes de que termine, basta con volver a abrir la página del actualizador para continuar en el último paso completado. Cerrar la página web seguirá ejecutando el paso en curso, pero no continuará con el siguiente, porque eso lo desencadena la página del actualizador abierta.

6. Una vez ejecutados todos los pasos, el actualizador hace una última pregunta: «Keep maintenance mode active?». Esto permite usar la página web de actualización o el procedimiento de actualización por línea de comandos (`occ upgrade`). Si el modo de mantenimiento se mantiene activo, se requiere acceso a la línea de comandos.

7. Listo. Ahora puede continuarse con la página web de actualización o ejecutarse `occ upgrade`. Los dos ejemplos «Actualización vía web» y «Actualización por línea de comandos» muestran cómo se ven entonces las pantallas.

**Actualización vía web**

Así continuaría la actualización vía web:

- El actualizador web de Nextcloud muestra la opción de desactivar el modo de mantenimiento tras la actualización.
- La página de actualización de Nextcloud se muestra cuando el actualizador web termina.

**Actualización por línea de comandos**

Así continuaría la actualización por línea de comandos:

- El actualizador de línea de comandos de Nextcloud pregunta si se mantiene activo el modo de mantenimiento.

```
$ sudo -E -u www-data php ./occ upgrade
Nextcloud or one of the apps require upgrade - only a limited number of commands are available
You may use your browser or the occ upgrade command to do the upgrade
Set log level to debug
Updating database schema
Updated database
Updating <files_pdfviewer> ...
Updated <files_pdfviewer> to 1.1.1
Updating <gallery> ...
Updated <gallery> to 17.0.0
Updating <activity> ...
Updated <activity> to 2.5.2
Updating <comments> ...
Updated <comments> to 1.2.0
Updating <theming> ...
Updated <theming> to 1.3.0
Starting code integrity check...
Finished code integrity check
Update successful
Maintenance mode is kept active
Reset log level
```

### Usar el actualizador por línea de comandos

El actualizador por línea de comandos funciona exactamente de la misma forma que el actualizador web. Los pasos y las comprobaciones son los mismos.

Los pasos son básicamente los mismos que en el actualizador web:

1. Debería verse una notificación en la parte superior de cualquier página de Nextcloud cuando hay una nueva actualización disponible. Ir a la página de configuraciones de administración y desplazarse hasta la sección «Versión». Esta sección tiene un botón para abrir el actualizador. Esta sección, así como la notificación de actualización, solo está disponible si la app de notificación de actualizaciones está activada en la gestión de apps.

2. En lugar de hacer clic en ese botón, ahora puede invocarse el actualizador por línea de comandos yendo al directorio *updater/* del directorio de Nextcloud y ejecutando *updater.phar* como el usuario del servidor web. (Es decir, `sudo -E -u www-data php /var/www/nextcloud/updater/updater.phar`)

3. Verificar la información que se muestra e introducir «Y» para iniciar la actualización.

4. Si ocurre un error o la comprobación falla, el actualizador detiene el proceso e informa de ello. Entonces puede intentarse resolver el problema y volver a ejecutar el comando del actualizador. Esto continuará la actualización y volverá a ejecutar el paso fallido. No volverá a ejecutar los pasos anteriores que se completaron correctamente.

6. Una vez ejecutados todos los pasos, el actualizador hace una última pregunta: «Should the "occ upgrade" command be executed?». Esto permite ejecutar directamente el procedimiento de actualización por línea de comandos (`occ upgrade`). Si se selecciona «No», terminará con «*Please now execute "./occ upgrade" to finish the upgrade.*».

7. Una vez terminado `occ upgrade`, se pregunta si el modo de mantenimiento debe mantenerse activo.

### Modo por lotes del actualizador por línea de comandos

Es posible ejecutar el actualizador por línea de comandos en modo no interactivo. Así, el actualizador no hace ninguna pregunta interactiva. Se supone que, si hay una actualización disponible, debe instalarse, y también se ejecuta el comando `occ upgrade`. Al terminar, el modo de mantenimiento se desactiva, salvo que haya ocurrido un error durante `occ upgrade` o durante la sustitución del código.

Para ello, ejecutar el comando con la opción `--no-interaction`. (Es decir, `sudo -E -u www-data php /var/www/nextcloud/updater/updater.phar --no-interaction`)

### Solución de problemas

- El actualizador integrado registra todas sus acciones en un archivo de registro dedicado llamado `updater.log`, ubicado en el `datadirectory` configurado (p. ej., `/var/www/html/data/updater.log`). Este archivo puede ser útil para aislar dónde fallan las cosas. También se necesitará si se pide ayuda en el foro de ayuda de la comunidad (<https://help.nextcloud.com>).

- Si hay problemas al usar el actualizador en modo web, conviene probar el modo de línea de comandos (si es una opción en el entorno). La línea de comandos evita los problemas con los tiempos de espera del servidor web, que pueden ser problemáticos porque a veces el actualizador tarda mucho en completar ciertos pasos.

- Si el problema parece estar en el paso de copia de seguridad, puede probarse a desactivar las copias de seguridad de los archivos de la instalación que el actualizador crea automáticamente. Hay que tener en cuenta que estas copias de seguridad **no** incluyen los datos (de los que, es de esperar, ya se hacen copias). El paso de copia de seguridad solo puede desactivarse en modo de línea de comandos. Añadir la opción `--no-backup` al comando `updater.phar`.

- Si por error se responde que no cuando el modo de línea de comandos del actualizador pregunta si se quiere ejecutar `occ upgrade`, puede ejecutarse `occ upgrade` manualmente sin riesgo o simplemente visitar la URL de la instancia para completar las migraciones de la base de datos y la fase de actualización de las apps.

- Pedir ayuda en el foro de ayuda de la comunidad (<https://help.nextcloud.com>)
````
