---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo convertir una base de datos SQLite a MySQL, MariaDB o PostgreSQL con occ db:convert-type, y qué tablas antiguas no se convierten."
---
# Conversión del tipo de base de datos

## Resumen

Esta página explica cómo pasar de una base de datos SQLite a MySQL, MariaDB o PostgreSQL: preparar la base de datos de destino, ejecutar `occ db:convert-type` y reconocer las tablas antiguas que no se convierten. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_database/db_conversion.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Una base de datos SQLite puede convertirse en una base de datos MySQL, MariaDB o PostgreSQL, de mejor rendimiento, con la herramienta de línea de comandos de Nextcloud. SQLite sirve para pruebas y para servidores Nextcloud sencillos de un solo usuario, pero no escala para servidores de producción con varios usuarios.

### Ejecutar la conversión

La conversión consta de dos pasos:

1. Preparar la base de datos de destino (incluidas sus credenciales)
2. Iniciar la herramienta de conversión, que migra el contenido de la base de datos existente a la base de datos de destino

#### Preparar la base de datos de destino

Primero, crear la base de datos de destino (nueva), junto con su nombre de usuario y su contraseña asociados, siguiendo las instrucciones de configuración manual de la base de datos para el tipo de base de datos de destino elegido:

- {nc-ref}`Configurar una base de datos MySQL o MariaDB <db-config-mysql-label>`
- {nc-ref}`Base de datos PostgreSQL <db-config-postgresql-label>`

Como las instrucciones de base de datos anteriores usan el nombre `nextcloud` para la base de datos recién creada, aquí se usa el mismo por coherencia, aunque se puede usar el nombre de base de datos que se prefiera. Usar el nombre de la base de datos, el nombre de usuario y la contraseña de la base de datos que se especificaron al crear la nueva base de datos.

#### Iniciar la conversión

El comando `occ db:convert-type` se encarga de todas las tareas de la conversión. Estos son los parámetros disponibles:

```
sudo -E -u www-data php occ db:convert-type [options] type username hostname database
```

`type` debe ser el tipo de la base de datos de destino. Aquí están disponibles los mismos valores que para el parámetro `dbtype` de `config.php`. Debe ser uno de estos: `mysql` para MariaDB/MySQL, `pgsql` para PostgreSQL u `oci` para Oracle.

Las opciones:

- `--port="3306"`: el puerto de la base de datos (opcional) [valor predeterminado: "3306"]
- `--password="mysql_user_password"`: la contraseña de la nueva base de datos. Si se omite, la herramienta la pide (opcional)
- `--clear-schema`: vaciar el esquema (opcional)
- `--all-apps`: de forma predeterminada se convierten las tablas de las apps habilitadas; usar esta opción para convertir también las tablas de las apps desactivadas (opcional)
- `-n, --no-interaction`: no hacer ninguna pregunta interactiva

:::{note}
La herramienta de conversión busca las apps en las carpetas de apps configuradas y usa las definiciones de esquema (tablas) de las apps para crear las tablas nuevas. Las tablas que aún existan de apps eliminadas no se convierten (ni siquiera con la opción `--all-apps`).
:::

A continuación se convierte una instalación sqlite3 existente (y en funcionamiento) para que use MariaDB/MySQL:

```
sudo -E -u www-data php occ db:convert-type --password="<password>" --port="3306" --all-apps mysql <username> <hostname> nextcloud
```

:::{note}
En este ejemplo no era necesario especificar el puerto, porque `3306` ya es el valor predeterminado. Se especificó solo con fines de demostración y para que el ejemplo quede completo, por si se usa un puerto no estándar en el servidor de base de datos de destino.
:::

Si la conversión tiene éxito, el conversor configura automáticamente la nueva base de datos en la configuración de Nextcloud, `config.php`.

Si la conversión es a una base de datos MySQL/MariaDB, también conviene establecer en true el parámetro `mysql.utf8mb4` de `config.php`:

```
sudo -E -u www-data php occ config:system:set mysql.utf8mb4 --type boolean --value="true"
```

Si se desea, pueden verse los cambios realizados buscando los parámetros `db*` en `config.php` (este comando también puede usarse antes de la conversión, para comparar la configuración antes y después):

```
grep db config/config.php
```

### Tablas no convertibles

Si se actualizó la instancia de Nextcloud, puede haber restos de tablas antiguas que ya no se usan. El actualizador indica cuáles son.

```
The following tables will not be converted:
oc_permissions
...
```

Estas tablas pueden ignorarse. Esta es una lista de tablas antiguas conocidas:

- oc_calendar_calendars
- oc_calendar_objects
- oc_calendar_share_calendar
- oc_calendar_share_event
- oc_fscache
- oc_log
- oc_media_albums
- oc_media_artists
- oc_media_sessions
- oc_media_songs
- oc_media_users
- oc_permissions
- oc_privatedata - esta tabla volvió a añadirse más tarde con la app *privatedata* (<https://apps.nextcloud.com/apps/privatedata>) y puede eliminarse sin riesgo si esa app no está habilitada
- oc_queuedtasks
- oc_sharing
````
