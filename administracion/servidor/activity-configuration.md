---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "App Actividad: correos de notificación, opciones de config.php, carpetas de equipo, caducidad, programación de envíos y solución de problemas."
---
# App Actividad

## Resumen

Esta página explica cómo configurar la app Actividad: los correos de notificación y sus ajustes de administración, las opciones de `config.php`, las actividades en carpetas de equipo y almacenamientos externos, la caducidad de los registros y la programación de los envíos, con una sección de solución de problemas. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_server/activity_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La app Actividad registra y resume los eventos visibles para los usuarios en toda la instancia de Nextcloud y puede avisar a los usuarios mediante el flujo de actividad, el correo electrónico y las notificaciones push. Viene incluida y está activada de forma predeterminada.

:::{note}
La app Actividad está pensada para notificar a los usuarios, no para el cumplimiento normativo ni la auditoría. Los usuarios pueden activar o desactivar el seguimiento de actividad de su propia cuenta, por lo que el flujo de actividad no es un registro de auditoría fiable. Si se necesita un registro completo de todas las acciones de la instancia, debe usarse en su lugar la app **admin_audit**; consultar {nc-doc}`Registro <admin_manual/configuration_server/logging_configuration>`.
:::

*La página de ajustes de administración de Actividad, que muestra las preferencias de notificación predeterminadas para las cuentas nuevas.*

### Configurar Nextcloud para la app Actividad

#### Activar los correos de notificación

Para enviar correos de notificación de actividad se requiere una configuración de {nc-doc}`Correo electrónico <admin_manual/configuration_server/email_configuration>` que funcione.

También se recomienda configurar el modo de ejecución de los trabajos en segundo plano en un modo de ejecución del sistema (`System Cron` o `systemd`), como se describe en {nc-doc}`Trabajos en segundo plano <admin_manual/configuration_server/background_jobs_configuration>`. Los modos `Ajax` y `Webcron` pueden retrasar u omitir el envío de correos.

#### Ajustes de administración

Un administrador puede:

- Activar o desactivar globalmente los correos de notificación con la casilla **Activar las notificaciones de emails** en **Ajustes** > **Administración** > **Actividad**.
- Configurar las preferencias de notificación predeterminadas para las cuentas nuevas. Los usuarios existentes conservan sus ajustes personales. Los valores predeterminados se aplican a las cuentas creadas después del cambio.

:::{note}
El interruptor **Activar las notificaciones de emails** impide que se pongan en cola correos **nuevos**. No elimina retroactivamente los correos que ya esperan en la cola. Los correos puestos en cola antes de desactivar el interruptor los seguirá enviando el trabajo en segundo plano en su próxima ejecución. Para detener esos correos de inmediato, truncar o vaciar la tabla `oc_activity_mq` de la base de datos.
:::

- Configurar el número máximo de actividades que se muestran completas en los correos de notificación mediante el ajuste `mail_max_items`. Las actividades que superan este límite se resumen como *«y X más»* al final del correo. El valor predeterminado es `200` y el valor máximo permitido es `1000`. Por ejemplo, para establecerlo en `500`:

```
occ config:app:set activity mail_max_items --value=500
```

### Referencia de configuración

Las siguientes opciones de `config.php` controlan el comportamiento de la app Actividad.

| Opción | Predeterminado | Descripción |
|---|---|---|
| `activity_expire_days` | `365` | Número de días que se conservan los registros de actividad. Un trabajo diario en segundo plano elimina todas las actividades más antiguas que este valor. El mínimo es `1` día. |
| `activity_use_cached_mountpoints` | `false` | Si es `true`, las actividades en carpetas de equipo y almacenamientos externos se generan para todos los usuarios con acceso, no solo para el usuario que actúa. Consultar {nc-ref}`Actividades en carpetas de equipo o almacenamientos externos <label-activities-groupfolders>` para los detalles y las salvedades. |
| `activity_expire_exclude_users` | `[]` | Una matriz de ID de usuario cuyos registros de actividad el trabajo de caducidad no elimina nunca. Consultar {nc-ref}`Excluir usuarios de la caducidad de la actividad <label-activities-exclude-users>`. |

(nc-label-activities-groupfolders)=
### Actividades en carpetas de equipo o almacenamientos externos

De forma predeterminada, las actividades en carpetas de equipo o almacenamientos externos solo se generan para el usuario actual. Esto se debe a la lógica subyacente de estos backends de almacenamiento. El indicador de configuración `activity_use_cached_mountpoints`, establecido en `true`, hace que las actividades funcionen como en los recursos compartidos normales.

```
'activity_use_cached_mountpoints' => true,
```

:::{danger}
Si los «Permisos avanzados» (ACL) están activados en una carpeta de equipo, las actividades no respetan esos permisos. En consecuencia, los usuarios pueden ver entradas de actividad de archivos y directorios a los que no tienen acceso. **Esto puede filtrar información sensible.** Hay más información en [esta incidencia](https://github.com/nextcloud/groupfolders/issues/1057).
:::

:::{warning}
Los usuarios que tenían acceso a una carpeta de equipo, un recurso compartido o un almacenamiento externo pueden seguir viendo nuevas entradas de actividad en su flujo y en sus correos hasta que vuelvan a iniciar sesión después de que se les retire el acceso.
:::

:::{note}
Los usuarios recién añadidos a una carpeta de equipo, un recurso compartido o un almacenamiento externo no verán nuevas entradas de actividad en su flujo ni en sus correos hasta que vuelvan a iniciar sesión después de que se les conceda el acceso.
:::

(nc-label-activities-exclude-users)=
### Excluir usuarios de la caducidad de la actividad

Para ciertos usuarios, por ejemplo los administradores, puede tener sentido que sus datos de actividad no caduquen nunca. Establecer el valor de configuración `activity_expire_exclude_users` en `config.php`:

```
'activity_expire_exclude_users' => [
  'admin',
  'group_admin',
  'second_admin'
]
```

Los registros de actividad de estos usuarios nunca se eliminarán de la base de datos.

### Mejor programación de los correos de actividad

En ciertos escenarios tiene sentido enviar los correos de actividad con más regularidad. Por ejemplo, puede quererse enviar los correos horarios siempre a la hora en punto, los diarios antes de que la gente empiece a trabajar por la mañana y los semanales el lunes por la mañana.

Hay un comando de consola para lanzar el envío de esos correos. Esto permite configurar trabajos cron personalizados con horarios concretos en lugar de depender del trabajo en segundo plano de Nextcloud:

```
# crontab -u www-data -e
 0  *  *  *  *    php -f /var/www/nextcloud/occ activity:send-mails hourly
30  7  *  *  *    php -f /var/www/nextcloud/occ activity:send-mails daily
30  7  *  *  MON  php -f /var/www/nextcloud/occ activity:send-mails weekly
```

Para enviar manualmente todos los correos de actividad en cola, puede ejecutarse `occ activity:send-mails` sin ningún argumento.

### Solución de problemas

#### Los usuarios no reciben los correos de notificación

1. Verificar que el correo electrónico esté configurado correctamente. Enviar un correo de prueba desde **Ajustes** > **Administración** > **Ajustes básicos**.
2. Comprobar que **Activar las notificaciones de emails** esté activado en **Ajustes** > **Administración** > **Actividad**.
3. Verificar que el usuario tenga activadas las notificaciones por correo en sus ajustes personales de notificaciones (**Ajustes** > **Personal** > **Notificaciones**).
4. Asegurarse de que el trabajo en segundo plano se esté ejecutando. Si se usa `Cron`, comprobar que el trabajo cron del sistema ejecute `php -f /var/www/nextcloud/cron.php` con regularidad.
5. Revisar el registro de Nextcloud (`data/nextcloud.log`) en busca de errores relacionados con el correo.

#### Faltan actividades de archivos compartidos o carpetas de equipo

De forma predeterminada, las actividades en carpetas de equipo y almacenamientos externos solo se generan para el usuario que actúa. Consultar {nc-ref}`Actividades en carpetas de equipo o almacenamientos externos <label-activities-groupfolders>` para saber cómo activar las actividades para todos los usuarios con acceso.

#### La base de datos crece mucho por los datos de actividad

La app Actividad almacena todos los eventos en la base de datos. En instancias con muchos usuarios o con mucha rotación de archivos, esto puede provocar un crecimiento considerable de la base de datos. Para gestionarlo:

- Establecer `activity_expire_days` en un valor menor (p. ej., `90` o `180`) para limpiar automáticamente los registros más antiguos.
- Asegurarse de que el trabajo en segundo plano de Nextcloud se esté ejecutando para que se ejecute el trabajo diario de caducidad.
- Para evaluar el uso actual de la base de datos, comprobar directamente el tamaño de las tablas `oc_activity` y `oc_activity_mq`.

#### Se siguen enviando correos después de desactivar los correos de notificación

El interruptor **Activar las notificaciones de emails** se comprueba al *poner en cola* los correos nuevos. El trabajo en segundo plano que realmente entrega los correos (`MailQueueHandler`) no vuelve a leer el interruptor antes de enviar, por lo que los correos que ya estaban en la cola cuando se desactivó el interruptor se entregarán igualmente.

Para detener esos correos de inmediato, vaciar la tabla `oc_activity_mq`:

```
DELETE FROM oc_activity_mq;
```

Después de vaciar la tabla no se enviarán más correos de actividad en cola hasta que se pongan en cola otros nuevos (lo que requiere volver a activar el interruptor).
````
