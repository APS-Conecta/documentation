---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo caducan las versiones de archivos: patrón de conservación, límite de espacio, ajuste versions_retention_obligation y trabajo en segundo plano."
---
# Control de las versiones de archivos y su antigüedad

## Resumen

Esta página explica cómo la app Versiones hace caducar automáticamente las versiones antiguas de los archivos, cómo se cambia el patrón de conservación en `config.php` y cómo se gestiona el trabajo en segundo plano que elimina las versiones caducadas. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/file_versioning.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La app Versiones (files_versions) hace caducar automáticamente las versiones antiguas de los archivos para garantizar que los usuarios no superen sus cuotas de almacenamiento. Este es el patrón predeterminado que se usa para eliminar las versiones antiguas:

- Durante el primer segundo se conserva una versión
- Durante los primeros 10 segundos, Nextcloud conserva una versión cada 2 segundos
- Durante el primer minuto, Nextcloud conserva una versión cada 10 segundos
- Durante la primera hora, Nextcloud conserva una versión cada minuto
- Durante las primeras 24 horas, Nextcloud conserva una versión cada hora
- Durante los primeros 30 días, Nextcloud conserva una versión cada día
- Pasados los primeros 30 días, Nextcloud conserva una versión cada semana

Las versiones se ajustan a este patrón cada vez que se crea una versión nueva. Nextcloud conservará siempre la versión más reciente de cada una de las ventanas de tiempo.

La app Versiones nunca usa más del 50 % del espacio libre del que dispone el usuario en ese momento. Si las versiones almacenadas superan este límite, Nextcloud elimina las versiones de archivo más antiguas hasta volver a cumplir el límite de espacio en disco.

Nextcloud gestiona las versiones de los archivos combinando una depuración al guardar y una limpieza programada. Así se garantiza que las versiones se conserven respetando las cuotas de almacenamiento.

### Durante la creación de versiones

Nextcloud crea automáticamente versiones nuevas de un archivo cada vez que se modifica, lo que permite a los usuarios recuperar estados anteriores cuando lo necesiten. Tras almacenar cada versión nueva, el sistema comprueba automáticamente los límites de almacenamiento y las reglas de retención. Las versiones se filtran según el patrón anterior para conservar las versiones representativas y eliminar las redundantes. Si se supera la cuota del usuario, se activa la caducidad automática.
Cuando queda poco espacio de almacenamiento, Nextcloud ordena todas las versiones de la más antigua a la más reciente y elimina primero las más antiguas, conservando siempre al menos las dos versiones más recientes, para liberar espacio.

### Durante el trabajo en segundo plano periódico

Nextcloud ejecuta una tarea de limpieza en segundo plano que elimina automáticamente las versiones de archivo antiguas de cada usuario. Durante este proceso, el sistema revisa la carpeta en la que se almacenan las versiones del usuario e identifica las versiones cuya antigüedad supera el periodo máximo de retención configurado o cuyos archivos originales ya no existen.
Cuando encuentra una versión obsoleta o huérfana, la elimina de forma segura tanto del sistema de archivos como de la base de datos de versiones, para recuperar espacio de almacenamiento y mantener la coherencia.

:::{note}
Las versiones a las que un usuario ha puesto nombre nunca se eliminarán.
:::

El patrón predeterminado puede modificarse en `config.php`. El ajuste predeterminado es `auto`, que establece el patrón predeterminado:

```
'versions_retention_obligation' => 'auto',
```

Otras opciones posibles son:

- `D, auto`: conservar las versiones al menos durante D días y aplicar las reglas de caducidad a todas las versiones con más de D días de antigüedad
- `auto, D`: eliminar automáticamente todas las versiones con más de D días de antigüedad y eliminar las demás versiones según las reglas de caducidad
- `D1, D2`: conservar las versiones al menos durante D1 días y eliminarlas cuando superen los D2 días.
- *disabled*: desactivar la caducidad automática (depuración) de las versiones de archivo; se seguirán creando versiones de archivo, pero no se eliminará automáticamente ninguna versión antigua.

### Trabajo en segundo plano

Para eliminar las versiones caducadas, se ejecuta un trabajo en segundo plano cada 30 minutos.
Es posible desactivar el trabajo en segundo plano y configurar un cron (del sistema) que haga caducar las versiones mediante occ.

Desactivar el trabajo en segundo plano: `occ config:app:set --value=no files_versions background_job_expire_versions`

Activar el trabajo en segundo plano: `occ config:app:delete files_versions background_job_expire_versions`

Hacer caducar las versiones: `occ versions:expire` o `occ versions:expire --quiet` (sin la barra de progreso)
````
