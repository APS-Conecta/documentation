---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Actualización manual de Nextcloud Server desde el archivo comprimido, paso a paso, con las versiones anteriores y la solución de problemas."
---
# Actualizar manualmente

## Resumen

Esta página explica cuándo conviene actualizar Nextcloud Server a mano y detalla, paso a paso, cómo sustituir los archivos de la instalación conservando los datos y la configuración, dónde encontrar versiones anteriores y cómo resolver los problemas habituales. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/maintenance/manual_upgrade.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Descripción general

En algunos entornos, usar el actualizador integrado en modo web no es fiable (por ejemplo, por los tiempos de espera del servidor web) y ejecutarlo en modo de línea de comandos no es una opción (como en algunos entornos de alojamiento compartido). En estos casos, una actualización manual puede ser el mejor enfoque.

Una actualización manual consiste en descargar y desempaquetar el archivo comprimido de Nextcloud en el PC o en el host. Después, eliminar los archivos y carpetas de la instalación existente de Nextcloud Server en el host, **excepto** `data/` y `config/`. Después, mover los archivos de la nueva instalación de Nextcloud Server al lugar adecuado del host, conservando de nuevo los archivos existentes de `data/` y `config/`. Y hacer algunas otras tareas de mantenimiento, como asegurarse de que las apps instaladas se transfieran a la nueva instalación y ajustar los permisos. Puede parecer mucho, pero a continuación hay instrucciones detalladas.

:::{important}
Antes de actualizar, especialmente entre versiones mayores (p. ej., v27.y.z -> v28.y.z), revisar primero los {nc-ref}`cambios críticos <critical-changes>`. Son lo más destacado de los cambios que pueden ser necesarios en el entorno para adaptarse a los cambios de Nextcloud Server. Estas notas se revisan periódicamente según sea necesario, por lo que conviene volver a consultarlas incluso al aplicar actualizaciones menores y de mantenimiento, por si acaso.
:::

:::{warning}
Al actualizar manualmente, hay que confirmar que el sistema cumple los {nc-doc}`admin_manual/installation/system_requirements` de la nueva versión y que se siguen los {nc-doc}`requisitos de actualización <admin_manual/maintenance/upgrade>` estándar (como actualizar a la última versión de mantenimiento *antes* de actualizar a una nueva versión mayor).
:::

### Actualización manual paso a paso

:::{important}
Empezar siempre haciendo una copia de seguridad nueva y desactivando todas las apps de terceros.
:::

1. Hacer una copia de seguridad de la base de datos, el directorio de datos y el archivo `config.php` existentes de Nextcloud Server. (Consultar {nc-doc}`admin_manual/maintenance/backup`; para la información sobre la restauración, consultar {nc-doc}`admin_manual/maintenance/restore`)

2. Elegir una versión de destino de Nextcloud Server en <https://nextcloud.com/changelog/> y descargar el archivo comprimido (tarball o archivo zip) en un directorio vacío fuera de la instalación actual.

   :::{warning}
   No puede avanzarse más de una versión mayor a la vez (es decir, 27->28 está bien, pero 27->29 no).
   :::

3. Desempaquetar el tarball o el archivo zip descargado; p. ej.:

   ```
   unzip nextcloud-[version].zip
   (or)
   tar -xjf nextcloud-[version].tar.bz2
   ```

4. Detener el servidor web.

5. Si se ejecuta un trabajo cron para las tareas de mantenimiento de nextcloud, desactivarlo comentando la entrada en el archivo crontab:

   ```
   crontab -u www-data -e
   ```

   (Poner un *#* al principio de la línea correspondiente).

6. Cambiar el nombre del directorio actual de Nextcloud, por ejemplo a `nextcloud-old`.

7. Al desempaquetar el nuevo archivo comprimido se crea un nuevo directorio `nextcloud` con los nuevos archivos del servidor. Mover este directorio y su contenido a la ubicación original del servidor antiguo. Por ejemplo, `/var/www/`, de modo que vuelva a existir `/var/www/nextcloud`.

8. Copiar el archivo `config/config.php` del directorio antiguo de Nextcloud al nuevo directorio de Nextcloud.

9. Si el directorio `data/` está dentro del directorio `nextcloud/`, moverlo desde la versión antigua de Nextcloud al nuevo `nextcloud/`. Si está fuera de `nextcloud/`, no hay que hacer nada con él, porque su ubicación está configurada en el `config.php` original y ninguno de los pasos de la actualización lo toca.

10. Si se usa una aplicación de terceros, puede que no siempre esté disponible en la instancia de Nextcloud actualizada/nueva. Para comprobarlo, comparar una lista de las apps de la nueva carpeta `nextcloud/apps/` con una lista de las apps de la carpeta `nextcloud/apps/` antigua o de la copia de seguridad. Si en la carpeta antigua hay apps de terceros que deben estar en la instancia nueva/actualizada, basta con copiarlas y asegurarse de que los permisos estén configurados como se muestra más abajo.

11. Si hay carpetas de apps adicionales, como por ejemplo `nextcloud/apps-extras` o `nextcloud/apps-external`, asegurarse de transferirlas o conservarlas también en la carpeta actualizada.

12. Si se usa un tema de terceros, asegurarse de copiarlo del directorio `themes/` al nuevo. Es posible que haya que hacerle algunas modificaciones después de la actualización.

13. Ajustar la propiedad y los permisos de los archivos:

    ```
    chown -R www-data:www-data nextcloud
    find nextcloud/ -type d -exec chmod 750 {} \;
    find nextcloud/ -type f -exec chmod 640 {} \;
    ```

14. Reiniciar el servidor web.

15. Ahora, lanzar la actualización desde la línea de comandos con `occ`, como en este ejemplo en Ubuntu Linux:

    ```
    sudo -E -u www-data php occ upgrade
    ```

    (!) esto DEBE ejecutarse desde dentro del directorio de instalación de nextcloud

16. La operación de actualización tarda desde unos minutos hasta unas horas, según el tamaño de la instalación. Cuando termine, se verá un mensaje de éxito o un mensaje de error que indicará dónde falló.

17. Volver a activar el trabajo cron de nextcloud. (Consultar el paso 4 más arriba).

    > crontab -u www-data -e

    (Eliminar el *#* del principio de la línea correspondiente en el archivo crontab).

Iniciar sesión y mirar la parte inferior de la página de administración para verificar el número de versión. Revisar los demás ajustes para asegurarse de que son correctos. Ir a la página de apps y revisar las apps principales para asegurarse de que estén activadas las correctas. Volver a activar las apps de terceros.

### Versiones anteriores de Nextcloud

Las versiones anteriores de Nextcloud se encuentran en el [registro de cambios de Nextcloud Server](https://nextcloud.com/changelog/).

### Solución de problemas

En ocasiones, *los archivos no aparecen tras una actualización*. Volver a escanear los archivos puede ayudar:

```
sudo -E -u www-data php console.php files:scan --all
```

Consultar [la página de soporte de nextcloud.com](https://nextcloud.com/support/) para más recursos.

A veces, Nextcloud puede quedarse *atascado en una actualización* si se usa el proceso de actualización web. Normalmente se debe a que el proceso tarda demasiado y se alcanza un tiempo de espera de PHP. Detener el proceso de actualización de esta forma:

```
sudo -E -u www-data php occ maintenance:mode --off
```

Después, iniciar el proceso manual:

```
sudo -E -u www-data php occ upgrade
```

Si esto no funciona correctamente, probar la función de reparación:

```
sudo -E -u www-data php occ maintenance:repair
```

[nextcloud.com/install/]: https://nextcloud.com/install/
````
