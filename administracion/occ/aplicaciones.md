---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Comandos occ para instalar, activar, actualizar y eliminar apps, elegir el planificador de trabajos en segundo plano y leer o cambiar la configuración."
---
# Comandos de apps, trabajos en segundo plano y configuración

## Resumen

Esta página es la referencia de los comandos `occ` que gestionan las apps (`app`), seleccionan el planificador de los trabajos en segundo plano (`background`) y leen, establecen, importan y eliminan valores de configuración (`config`), con ejemplos y su salida. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/occ_apps.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
(nc-apps_commands_label)=
### Comandos de apps

Los comandos `app` listan, activan y desactivan apps:

```
app
 app:install      install selected app
 app:disable      disable an app
 app:enable       enable an app
 app:getpath      get an absolute path to the app directory
 app:list         list all available apps
 app:update       update an app or all apps
 app:remove       disable and remove an app
```

Descargar e instalar una app:

```
sudo -E -u www-data php occ app:install twofactor_totp
```

Instalar sin activar:

```
sudo -E -u www-data php occ app:install --keep-disabled twofactor_totp
```

Instalar sin tener en cuenta el requisito de versión de Nextcloud:

```
sudo -E -u www-data php occ app:install --force twofactor_totp
```

Listar todas las apps instaladas e indicar si están activadas o desactivadas:

```
sudo -E -u www-data php occ app:list
```

Listar todas las apps instaladas y activadas (opción `--enabled`) o desactivadas (opción `--disabled`):

```
sudo -E -u www-data php occ app:list --enabled
```

Listar solo las apps instaladas que no se distribuyen con el servidor:

```
sudo -E -u www-data php occ app:list --shipped false
```

Activar una app, por ejemplo, la app Soporte de almacenamiento externo:

```
sudo -E -u www-data php occ app:enable files_external
files_external enabled
```

Activar una app sin tener en cuenta el requisito de versión de Nextcloud:

```
sudo -E -u www-data php occ app:enable --force files_external
files_external enabled
```

Activar una app para grupos de usuarios concretos (es decir, restringir una app para que solo determinados grupos puedan verla y usarla):

```
sudo -E -u www-data php occ app:enable --groups admin --groups sales files_external
files_external enabled for groups: admin, sales
```

Activar varias apps a la vez:

```
sudo -E -u www-data php occ app:enable app1 app2 app3
app1 enabled
app2 enabled
app3 enabled
```

Desactivar una app:

```
sudo -E -u www-data php occ app:disable files_external
files_external disabled
```

Desactivar y eliminar una app:

```
sudo -E -u www-data php occ app:remove files_external
files_external disabled
files_external 1.21.0 removed
```

Eliminar una app, pero conservar sus datos:

```
sudo -E -u www-data php occ app:remove --keep-data files_external
files_external 1.21.0 removed
```

Se puede obtener la ruta completa de una app:

```
sudo -E -u www-data php occ app:getpath notifications
/var/www/nextcloud/apps/notifications
```

Para actualizar una app, por ejemplo, Contactos:

```
sudo -E -u www-data php occ app:update contacts
```

Para actualizar todas las apps:

```
sudo -E -u www-data php occ app:update --all
```

Para mostrar las actualizaciones disponibles sin actualizar:

```
sudo -E -u www-data php occ app:update --showonly
```

Para actualizar una app a una versión inestable, por ejemplo, News:

```
sudo -E -u www-data php occ app:update --allow-unstable news
```

(nc-background_jobs_selector_label)=
### Selector de trabajos en segundo plano

Usar los comandos `background` para seleccionar el planificador que controla los trabajos en segundo plano. Equivale a usar la sección **Cron** de la página de administración de Nextcloud:

```
background
 background:cron       Set background jobs to cron mode
 background:ajax       Set background jobs to ajax mode
 background:webcron    Set background jobs to webcron mode
```

Ejemplo:

```
sudo -E -u www-data php occ background:cron
  Set mode for background jobs to 'cron'
```

Los otros dos comandos son:

- `background:ajax`
- `background:webcron`

Consultar {nc-doc}`admin_manual/configuration_server/background_jobs_configuration` para más información.

(nc-config_commands_label)=
### Comandos de configuración

Los comandos `config` se usan para configurar el servidor Nextcloud:

```
config
 config:app:delete      Delete an app config value
 config:app:get         Get an app config value
 config:app:set         Set an app config value
 config:import          Import a list of configs
 config:list            List all configs
 config:system:delete   Delete a system config value
 config:system:get      Get a system config value
 config:system:set      Set a system config value
```

Al establecer un valor de configuración hay varias opciones disponibles:

- `--value=VALUE` cambia el valor de configuración
- `--type=TYPE` cambia el tipo del valor. Usar con cuidado: puede romper la instancia
- `--lazy|--no-lazy` establece el valor como *lazy*
- `--sensitive|--no-sensitive` establece el valor como *sensitive*
- `--update-only` solo actualiza si ya hay un valor almacenado

:::{note}
Consultar [Conceptos de Appconfig][Appconfig Concepts] para saber más sobre *typed value* y las opciones *lazy* y *sensitive*.
:::

Se pueden listar todos los valores de configuración con un solo comando:

```
sudo -E -u www-data php occ config:list
```

De forma predeterminada, las contraseñas y otros datos sensibles se omiten del informe, de modo que la salida puede publicarse (p. ej., como parte de un informe de error). Para generar una exportación completa de todos los valores de configuración, hay que indicar la opción `--private`:

```
sudo -E -u www-data php occ config:list --private
```

El contenido exportado también puede volver a importarse para configurar rápidamente instancias similares. El comando de importación solo añade o actualiza valores. Los valores que existen en la configuración actual, pero no en la que se importa, no se modifican:

```
sudo -E -u www-data php occ config:import filename.json
```

También es posible importar archivos remotos, canalizando la entrada:

```
sudo -E -u www-data php occ config:import < local-backup.json
```

:::{note}
Aunque es posible actualizar, establecer o eliminar las versiones y los estados de instalación de las apps y del propio Nextcloud, **no** se recomienda hacerlo directamente. Usar en su lugar los comandos `occ app:enable`, `occ app:disable` y `occ app:update`.
:::

#### Obtener un único valor de configuración

Estos comandos obtienen el valor de una única configuración de app o del sistema:

```
sudo -E -u www-data php occ config:system:get version
19.0.0.12

sudo -E -u www-data php occ config:app:get activity installed_version
2.2.1
```

#### Establecer un único valor de configuración

Estos comandos establecen el valor de una única configuración de app o del sistema:

```
sudo -E -u www-data php occ config:system:set logtimezone
--value="Europe/Berlin"
System config value logtimezone set to Europe/Berlin

sudo -E -u www-data php occ config:app:set files_sharing
incoming_server2server_share_enabled --value="yes"
Config value incoming_server2server_share_enabled for app files_sharing set to yes
```

El comando `config:system:set` crea el valor si aún no existe. Para actualizar un valor existente, indicar `--update-only`:

```
sudo -E -u www-data php occ config:system:set doesnotexist --value="true"
--type=boolean --update-only
Value not updated, as it has not been set before.
```

Tener en cuenta que, para escribir un valor booleano, de coma flotante o entero en el archivo de configuración, hay que indicar el tipo en el comando. Esto solo se aplica al comando `config:system:set`. Se conocen los siguientes valores:

- `boolean`
- `float`
- `integer`
- `json`
- `null`
- `string` (predeterminado)

Por ejemplo, para desactivar el modo de mantenimiento, ejecutar el siguiente comando:

```
sudo -E -u www-data php occ config:system:set maintenance --value=false --type=boolean
Nextcloud is in maintenance mode - no app have been loaded
System config value maintenance set to boolean false
```

#### Establecer un valor de configuración de tipo array

Algunas configuraciones (p. ej., el ajuste de dominios de confianza) son un array de datos. En ese caso, `config:system:get` devuelve varios valores para esa clave:

```
sudo -E -u www-data php occ config:system:get trusted_domains
localhost
nextcloud.local
sample.tld
```

Para establecer uno de los varios valores, hay que indicar el índice del array como segundo `name` en el comando `config:system:set`, separado por un espacio. Por ejemplo, para sustituir `sample.tld` por `example.com`, hay que establecer `trusted_domains => 2`:

```
sudo -E -u www-data php occ config:system:set trusted_domains 2 --value=example.com
System config value trusted_domains => 2 set to string example.com

sudo -E -u www-data php occ config:system:get trusted_domains
localhost
nextcloud.local
example.com
```

Otra opción es establecer todo el array de una vez usando el tipo `json`:

```
sudo -E -u www-data php occ config:system:set trusted_domains --type json --value '["nextcloud.local","example.com"]'
System config value trusted_domains set to json ["nextcloud.local","example.com"]

sudo -E -u www-data php occ config:system:get trusted_domains
nextcloud.local
example.com
```

#### Establecer un valor de configuración jerárquico

Algunas configuraciones usan datos jerárquicos. Por ejemplo, los ajustes de la caché Redis tendrían este aspecto en el archivo `config.php`:

```
'redis' => array(
  'host' => '/var/run/redis/redis.sock',
  'port' => 0,
  'dbindex' => 0,
  'password' => 'secret',
  'timeout' => 1.5,
)
```

Establecer estos valores jerárquicos funciona de forma similar a establecer un valor de array, como se ha visto arriba. Para este ejemplo de Redis, usar los siguientes comandos:

```
sudo -E -u www-data php occ config:system:set redis host \
--value=/var/run/redis/redis.sock
sudo -E -u www-data php occ config:system:set redis port --value=0
sudo -E -u www-data php occ config:system:set redis dbindex --value=0
sudo -E -u www-data php occ config:system:set redis password --value=secret
sudo -E -u www-data php occ config:system:set redis timeout --value=1.5
```

Otra opción es establecer toda la configuración de la entrada de una vez usando el tipo `json`:

```
sudo -E -u www-data php occ config:system:set redis --type json --value '{"host":"/var/run/redis/redis.sock","port":0,"dbindex":0,"password":"secret","timeout":1.5}'
```

#### Eliminar un único valor de configuración

Estos comandos eliminan la configuración de una app o del sistema:

```
sudo -E -u www-data php occ config:system:delete maintenance:mode
System config value maintenance:mode deleted

sudo -E -u www-data php occ config:app:delete appname provisioning_api
Config value provisioning_api of app appname deleted
```

De forma predeterminada, el comando de eliminación no avisa si la configuración no estaba establecida. Para recibir un aviso en ese caso, indicar la opción `--error-if-not-exists`:

```
sudo -E -u www-data php occ config:system:delete doesnotexist
--error-if-not-exists
System config value doesnotexist could not be deleted because it did not exist
```

[Appconfig Concepts]: https://docs.nextcloud.com/server/latest/developer_manual/digging_deeper/config/appconfig.html#concept-overview
````
