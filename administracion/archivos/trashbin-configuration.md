---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Retención de la papelera: valores de trashbin_retention_obligation en config.php y trabajo en segundo plano que elimina definitivamente los archivos."
---
# Elementos eliminados (papelera)

## Resumen

Esta página describe la política que decide cuándo se eliminan definitivamente los archivos y carpetas de la papelera: los valores de `trashbin_retention_obligation` en `config.php` y el trabajo en segundo plano que los elimina. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/trashbin_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Si la app de papelera está activada (lo está de forma predeterminada), este ajuste define la política que determina cuándo se eliminan definitivamente los archivos y carpetas de la papelera.

:::{note}
Si se supera el límite de cuota del usuario a causa de los archivos eliminados que hay en la papelera, se ignorarán los ajustes de retención y se limpiarán archivos hasta que se cumplan los requisitos de la cuota.
:::

La app admite dos ajustes: un tiempo mínimo de retención en la papelera y un tiempo máximo de retención en la papelera.
El tiempo mínimo es el número de días que se conservará un archivo, pasados los cuales puede eliminarse. El tiempo máximo es el número de días a partir del cual se garantiza que se eliminará.
Ambos tiempos, mínimo y máximo, pueden establecerse juntos para definir de forma explícita la eliminación de archivos y carpetas. Por motivos de migración, este ajuste se instala con el valor inicial "auto", que equivale al ajuste predeterminado de Nextcloud.

El patrón predeterminado puede modificarse en `config.php`. El ajuste predeterminado es `auto`, que establece el patrón predeterminado:

```
'trashbin_retention_obligation' => 'auto',
```

Valores disponibles:

- `auto`: ajuste predeterminado. Conserva los archivos y carpetas en la papelera durante 30 días y los elimina automáticamente en cualquier momento posterior si se necesita espacio (nota: puede que los archivos no se eliminen si no se necesita espacio).
- `D, auto`: conserva los archivos y carpetas en la papelera durante D días o más y los elimina en cualquier momento si se necesita espacio (nota: puede que los archivos no se eliminen si no se necesita espacio)
- `auto, D`: elimina automáticamente todos los archivos de la papelera con más de D días de antigüedad y elimina los demás archivos en cualquier momento si se necesita espacio
- `D1, D2`: conserva los archivos y carpetas en la papelera al menos durante D1 días y los elimina cuando superan los D2 días (nota: los archivos no se eliminarán automáticamente si se necesita espacio)
- `disabled`: limpieza automática de la papelera desactivada; los archivos y carpetas se conservarán para siempre

### Trabajo en segundo plano

Para eliminar definitivamente los archivos, se ejecuta un trabajo en segundo plano cada 30 minutos.
Es posible desactivar el trabajo en segundo plano y configurar un cron (del sistema) que haga caducar las versiones mediante occ.

Desactivar el trabajo en segundo plano: `occ config:app:set --value=no files_trashbin background_job_expire_trash`

Activar el trabajo en segundo plano: `occ config:app:delete files_trashbin background_job_expire_trash`

Hacer caducar las versiones: `occ trashbin:expire` o `occ trashbin:expire --quiet` (sin la barra de progreso)
````
