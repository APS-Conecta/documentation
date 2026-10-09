---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Función de ausencia: la zona horaria que usa (default_timezone) y cómo desactivarla o reactivarla para todos los usuarios con hide_absence_settings."
---
# Función de ausencia

## Resumen

Esta página describe la función de ausencia (fuera de la oficina): la zona horaria de la que depende, con `default_timezone` como respaldo, y cómo desactivarla y volver a activarla para todos los usuarios con `hide_absence_settings`. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/groupware/out_of_office.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 28.0.0
:::

La función de ausencia permite a los usuarios programar un periodo de ausencia, con un estado y un mensaje, que se integra con otras apps como Nextcloud Mail. Para más información sobre la función en sí, consultar la documentación de usuario. La administración puede desactivarla de forma global.

La función depende de que los usuarios configuren correctamente la zona horaria preferida de su calendario. Sin embargo, si un usuario no configura su zona horaria, se usa la zona horaria predeterminada del servidor. Esta puede configurarse estableciendo `default_timezone` en el archivo *config.php* del servidor Nextcloud. El valor de configuración acepta identificadores IANA como `Europe/Berlin` y su valor predeterminado es `UTC`. Para más información sobre el valor, consultar la sección *Configuración de Nextcloud*.

Para desactivar la función de ausencia para todos los usuarios, el valor de configuración de app `hide_absence_settings` de la app *dav* debe establecerse en *yes*. Esto puede hacerse ejecutando el siguiente comando en el servidor:

```
occ config:app:set --value=yes dav hide_absence_settings
```

:::{note}
Los periodos de ausencia programados antes de desactivar la función no se eliminarán. Desactivarla solo oculta la función de la interfaz de usuario. Si la función se vuelve a activar, los periodos volverán a ser visibles.
:::

Establecer el valor de *hide_absence_settings* en *no*, o eliminar por completo la opción de configuración, para volver a activar la función. Para ello puede usarse el siguiente comando:

```
occ config:app:set --value=no dav hide_absence_settings
```
````
