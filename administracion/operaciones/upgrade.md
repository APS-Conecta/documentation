---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo actualizar Nextcloud: los dos métodos, el paso a paso entre versiones mayores, requisitos previos, modo de mantenimiento y pasos manuales posteriores."
---
# Cómo actualizar

## Resumen

Esta página presenta los métodos para actualizar un servidor Nextcloud, las reglas para avanzar paso a paso entre versiones mayores, las notificaciones de actualización, los requisitos previos, el modo de mantenimiento y los pasos de migración que se ejecutan a mano tras la actualización. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/maintenance/upgrade.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Descripción general

El enfoque para actualizar Nextcloud Server depende del tipo de instalación. Este manual se centra principalmente en los métodos que se aplican a una instalación basada en el archivo comprimido. Si la instalación se hizo con Snap, Docker, una máquina virtual preconstruida o una herramienta de gestión de paquetes, consultar las instrucciones de instalación y actualización de ese método de instalación para obtener las instrucciones de actualización más precisas (en general, se encuentran en el punto de distribución del método de instalación elegido).

Hay dos formas de actualizar una implementación de Nextcloud Server basada en el archivo comprimido:

- Con el {nc-doc}`actualizador integrado <admin_manual/maintenance/update>` (mediante la interfaz web o la de línea de comandos).
- {nc-doc}`Actualizando manualmente <admin_manual/maintenance/manual_upgrade>` (con un archivo comprimido descargado)

El actualizador integrado, en modo web o de línea de comandos, es la opción más sencilla para la mayoría de los entornos. Sin embargo, algunos entornos requieren el enfoque manual. Aquí se tratan por completo ambos enfoques.

:::{important}
Antes de actualizar, especialmente entre versiones mayores (p. ej., v27.y.z -> v28.y.z), revisar primero los {nc-ref}`cambios críticos <critical-changes>`. Son lo más destacado de los cambios que pueden ser necesarios en el entorno para adaptarse a los cambios de Nextcloud Server. Estas notas se revisan periódicamente según sea necesario, por lo que también conviene volver a consultarlas de forma periódica, por ejemplo al aplicar actualizaciones de mantenimiento.
:::

Cuando hay una actualización disponible para el servidor Nextcloud, de forma predeterminada se recibe una notificación. También pueden comprobarse las actualizaciones disponibles visitando la sección de actualización en **Configuraciones de administración->Vista general** de la interfaz web.

:::{note}
Lo mejor es mantener el servidor Nextcloud actualizado con regularidad. Esto significa instalar todas las versiones de mantenimiento/puntuales y actualizar a las nuevas versiones mayores antes de que la actual alcance el estado de {nc-doc}`fin de vida <admin_manual/release_schedule>`. Ejemplos de versiones mayores son 27, 28 o 29. Las versiones de mantenimiento son versiones intermedias de cada versión mayor que corrigen errores críticos de funcionalidad o de seguridad. Por ejemplo, 28.0.4 y 29.0.2 son versiones de mantenimiento.
:::

### Planificar las actualizaciones

- Nextcloud debe actualizarse paso a paso:
  - Antes de poder actualizar a la siguiente versión mayor, hay que actualizar a la última versión puntual de la versión mayor actual.
  - Después, ejecutar de nuevo la actualización para pasar a la última versión puntual de la siguiente versión mayor.
  - **No pueden saltarse versiones mayores.** Volver a ejecutar la actualización hasta alcanzar la versión más alta disponible (o aplicable).
  - Ejemplo: 18.0.5 -> 18.0.11 -> 19.0.5 -> 20.0.2

**Esperar a que terminen las migraciones en segundo plano tras las actualizaciones mayores**. Después de actualizar a una nueva versión mayor, algunas migraciones se programan para ejecutarse como trabajo en segundo plano. Si se planea actualizar directamente a otra versión mayor (p. ej., 24 -> 25 -> 26), hay que asegurarse de que estas migraciones se hayan ejecutado antes de iniciar la siguiente actualización. Para ello, ejecutar el archivo `cron.php` 2-3 veces, por ejemplo:

```
$ sudo -E -u www-data php -f /var/www/nextcloud/cron.php
```

Para más información sobre los trabajos en segundo plano, consultar {nc-doc}`admin_manual/configuration_server/background_jobs_configuration`.

**Actualizar interrumpe el servicio**. El servidor Nextcloud se pondrá en modo de mantenimiento, por lo que los usuarios quedarán sin acceso hasta que se complete la actualización. En instalaciones grandes, la actualización puede tardar varias horas en completarse. No obstante, los tiempos habituales de actualización, incluso en instalaciones más grandes, son de unos pocos minutos.

:::{warning}
**No se admite volver a una versión anterior** y se corre el riesgo de dañar los datos. Si se quiere volver a una versión anterior de Nextcloud, hacer una instalación nueva y limpia y luego restaurar los datos desde la copia de seguridad. Antes de hacerlo, abrir un ticket de soporte (si se cuenta con soporte de pago) o pedir ayuda en los foros de {vendor}`Nextcloud` para ver si el problema puede resolverse sin volver a una versión anterior.
:::

### Notificaciones de actualización

Nextcloud tiene una app de notificación de actualizaciones que informa al administrador de que hay una actualización disponible. Después, se decide qué método de actualización usar.

El banner superior es la notificación de actualización que se muestra en todas las páginas, y la sección de actualizaciones se encuentra en la página de administración.

A partir de ahí, puede usarse el actualizador web para obtener el nuevo código. También hay disponible un actualizador por CLI, que hace exactamente lo mismo que el actualizador web, pero en la línea de comandos.

### Requisitos previos

:::{seealso}
Si se actualiza desde una versión mayor anterior, consultar primero los {nc-ref}`cambios críticos <critical-changes>`.
:::

Siempre hay que mantener {nc-doc}`copias de seguridad periódicas <admin_manual/maintenance/backup>` y hacer una copia de seguridad nueva antes de cada actualización.

Después, revisar la compatibilidad de las apps de terceros, si las hay, con la nueva versión de Nextcloud. Las apps que no desarrolla {vendor}`Nextcloud` muestran la designación de terceros. **Las apps sin soporte se instalan bajo el propio riesgo**. Luego, antes de la actualización, deben desactivarse todas las apps de terceros. Una vez completada la actualización, pueden volver a activarse.

### Modo de mantenimiento

El servidor Nextcloud puede ponerse en modo de mantenimiento antes de realizar actualizaciones, o para resolver problemas o hacer tareas de mantenimiento. Consultar {nc-doc}`admin_manual/occ_command` para saber cómo poner el servidor en modo de mantenimiento (`maintenance:mode`) o ejecutar comandos de reparación (`maintenance:repair`) con el comando `occ`.

El {nc-doc}`actualizador integrado <admin_manual/maintenance/update>` lo hace automáticamente antes de sustituir el código existente de Nextcloud por el código de la nueva versión de Nextcloud.

`maintenance:mode` bloquea las sesiones de los usuarios que han iniciado sesión e impide nuevos inicios de sesión. Este es el modo que hay que usar para las actualizaciones. `occ` debe ejecutarse como el usuario HTTP, como en este ejemplo en Ubuntu Linux:

```
$ sudo -E -u www-data php occ maintenance:mode --on
```

También puede ponerse el servidor en este modo editando {file}`config/config.php`. Cambiar `"maintenance" => false` por `"maintenance" => true`:

```
<?php

 "maintenance" => true,
```

Después, volver a cambiarlo a `false` al terminar.

### Pasos manuales durante la actualización

Algunas operaciones pueden llevar bastante tiempo. Por eso se decidió no añadirlas al proceso normal de actualización. Se recomienda ejecutarlas manualmente una vez completada la actualización. A continuación se encuentra una lista de estos comandos.

#### Pasos de migración de larga duración

De vez en cuando se hacen cambios en la estructura de la base de datos que llevan mucho tiempo, pero que pueden ejecutarse mientras Nextcloud sigue en línea. Por eso se trasladaron a un comando aparte que un administrador puede ejecutar en la CLI sin necesidad de bloquear la instancia en modo de mantenimiento (al menos para algunos de ellos). La instancia también funciona sin aplicar esos cambios, pero con ellos el rendimiento mejora significativamente. También hay siempre un aviso en las comprobaciones de configuración de la interfaz web de las configuraciones de administración.

Entre ellos están, por ejemplo:

```
$ sudo -E -u www-data php occ db:add-missing-columns
$ sudo -E -u www-data php occ db:add-missing-indices
$ sudo -E -u www-data php occ db:add-missing-primary-keys
```

Puede usarse la opción `--dry-run` para mostrar las consultas SQL en lugar de ejecutarlas.
````
