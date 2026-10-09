---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Trabajos en segundo plano de Nextcloud: la ventana de mantenimiento y los modos AJAX, Webcron, cron del sistema y temporizador de systemd."
---
# Trabajos en segundo plano

## Resumen

Esta página explica qué son los trabajos en segundo plano de Nextcloud, cómo acotarlos con `maintenance_window_start` y cómo programarlos con AJAX, Webcron, el cron del sistema o un temporizador de systemd, con las ventajas y límites de cada modo. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_server/background_jobs_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Un sistema como Nextcloud a veces necesita realizar tareas de forma periódica sin requerir la interacción del usuario y sin afectar al rendimiento de Nextcloud. Para ello, el administrador del sistema puede definir trabajos en segundo plano (por ejemplo, limpiezas de la base de datos) que se ejecutan sin necesidad de interacción del usuario.

Estos trabajos suelen denominarse *trabajos cron*. Los trabajos cron son comandos o scripts de shell programados para ejecutarse periódicamente en horas, fechas o intervalos fijos. `cron.php` es un proceso interno de Nextcloud que ejecuta esos trabajos en segundo plano a demanda.

Las apps de Nextcloud registran automáticamente acciones en `cron.php` para ocuparse de las tareas de mantenimiento habituales, como la recolección de basura de archivos temporales o la comprobación de archivos recién actualizados con `filescan()` en los sistemas de archivos montados externamente.

### Parámetros

#### `maintenance_window_start`

:::{note}
Este ajuste solo se tiene en cuenta en el modo `cron`.
:::

Este ajuste puede especificarse en el archivo `config/config.php`. Algunos trabajos en segundo plano solo se ejecutan una vez al día. Cuando en este ajuste se define una hora (la zona horaria es UTC), los trabajos en segundo plano que se declaran no sensibles al tiempo se aplazan durante las horas «laborables» y solo se ejecutan en las 4 horas siguientes a la hora indicada. Esto se usa, p. ej., para la caducidad de la actividad, el entrenamiento de inicios de sesión sospechosos y las comprobaciones de actualizaciones.

Un valor de 1, p. ej., solo ejecutará estos trabajos en segundo plano entre las 01:00 a. m. UTC y las 05:00 a. m. UTC:

```
'maintenance_window_start' => 1,
```

Si no importa cuándo se ejecutan estos trabajos, puede establecerse el valor en `100`, pero hay que tener en cuenta que entonces los trabajos que consumen muchos recursos pueden ejecutarse innecesariamente en periodos de uso intenso. Esto puede reducir el rendimiento y empeorar la experiencia de usuario.

Este ajuste también puede establecerse directamente con `occ`, como cualquier otro parámetro de configuración:

```
occ config:system:set maintenance_window_start --type=integer --value=1
```

### Trabajos cron

Los trabajos cron pueden programarse de tres maneras: con AJAX, con Webcron o con cron. El método predeterminado es AJAX. Sin embargo, el método recomendado es cron. Las siguientes secciones describen las diferencias entre los métodos.

#### AJAX

**Caso de uso: instancia de un solo usuario**

El método de programación AJAX es la opción predeterminada. Por desgracia, también es el menos fiable. Cada vez que un usuario visita la página de Nextcloud se ejecuta un único trabajo en segundo plano. La ventaja de este mecanismo es que no requiere acceso al sistema ni registrarse en un servicio de terceros. Su desventaja, en comparación con el servicio Webcron, es que requiere visitas regulares a la página para activarse.

:::{warning}
Se recomienda usar `cron` especialmente cuando se usa la app Actividad o almacenamientos externos, donde se añaden, actualizan o eliminan archivos nuevos, o cuando **varios usuarios** usan el servidor.
:::

#### Webcron

**Caso de uso: instancia muy pequeña** (1–5 usuarios, según el uso)

Al registrar la dirección del script `cron.php` de Nextcloud en un servicio webcron externo (por ejemplo, [easyCron][easyCron]), se garantiza que los trabajos en segundo plano se ejecuten con regularidad. Para usar este tipo de servicio con el servidor, este debe ser accesible desde Internet. Por ejemplo:

```
URL to call: http[s]://<domain-of-your-server>/nextcloud/cron.php
```

:::{warning}
Como WebCron se sigue ejecutando a través de la web, en la mayoría de los casos el servidor web limita los recursos de la ejecución. Para evitar interrupciones dentro de los trabajos, solo se ejecuta 1 trabajo por llamada. Si webcron se llama una vez cada 5 minutos, la instancia queda limitada a 288 trabajos en segundo plano al día, lo que solo es adecuado para instancias muy pequeñas. Para instancias más grandes se recomienda usar `cron`.
:::

(nc-system-cron-configuration-label)=
#### Cron

Usar la función cron del sistema operativo es el método preferido para ejecutar tareas periódicas. Este método permite ejecutar los trabajos programados sin las limitaciones inherentes que pueda tener el servidor web.

Para ejecutar un trabajo cron en un sistema \*nix cada 5 minutos con el usuario predeterminado del servidor web (a menudo, `www-data` o `wwwrun`), debe configurarse el siguiente trabajo cron que llama al script **cron.php**:

```
# crontab -u www-data -e
```

Y añadir esta línea:

```
*/5  *  *  *  * php -f /var/www/nextcloud/cron.php
```

Para verificar que el trabajo cron se ha añadido y programado, ejecutar:

```
# crontab -u www-data -l
```

Lo que devuelve:

```
[snip]
*/5  *  *  *  * php -f /var/www/nextcloud/cron.php
```

:::{note}
Debe sustituirse la ruta `/var/www/nextcloud/cron.php` por la ruta de la instalación actual de Nextcloud.
:::

:::{note}
En algunos sistemas puede ser necesario llamar a **php-cli** en lugar de **php**.
:::

:::{note}
La sintaxis exacta del comando está en la página de manual de crontab.
:::

#### systemd

Si systemd está instalado en el sistema, un temporizador de systemd puede ser una alternativa a un trabajo cron.

Este método requiere dos archivos: **nextcloudcron.service** y **nextcloudcron.timer**. Crear estos dos archivos en `/etc/systemd/system/`.

**nextcloudcron.service** debe tener este aspecto:

```
[Unit]
Description=Nextcloud cron.php job

[Service]
User=www-data
ExecCondition=php -f /var/www/nextcloud/occ status -e
ExecStart=/usr/bin/php -f /var/www/nextcloud/cron.php
KillMode=process
```

Sustituir el usuario `www-data` por el usuario del servidor http y `/var/www/nextcloud/cron.php` por la ubicación de **cron.php** en el directorio de nextcloud.

*ExecCondition* comprueba que la instancia de nextcloud funcione con normalidad antes de ejecutar el trabajo en segundo plano y, si no es así, lo omite.

El ajuste `KillMode=process` es necesario para que los programas externos iniciados por el trabajo cron sigan ejecutándose después de que el trabajo cron haya terminado.

Hay que tener en cuenta que el archivo de unidad **.service** no necesita una sección `[Install]`. Conviene revisar la configuración, porque versiones anteriores de este manual de administración la recomendaban.

**nextcloudcron.timer** debe tener este aspecto:

```
[Unit]
Description=Run Nextcloud cron.php every 5 minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=5min
Unit=nextcloudcron.service

[Install]
WantedBy=timers.target
```

Las partes importantes de la unidad de temporizador son `OnBootSec` y `OnUnitActiveSec`. `OnBootSec` inicia el temporizador 5 minutos después del arranque; de lo contrario, habría que iniciarlo manualmente después de cada arranque. `OnUnitActiveSec` fija un temporizador de 5 minutos desde la última activación de la unidad de servicio.

Ahora solo queda iniciar y activar el temporizador ejecutando este comando:

```
systemctl enable --now nextcloudcron.timer
```

Cuando se usa la opción `--now` con `enable`, la unidad correspondiente también se inicia.

:::{note}
No es obligatorio seleccionar la opción `Cron` en el menú de administración de los trabajos en segundo plano, porque en cuanto *cron.php* se ejecuta desde la línea de comandos o desde el servicio cron, la establece automáticamente en `Cron`.
:::

[easyCron]: https://www.easycron.com/
````
