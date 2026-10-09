---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Qué respaldar en una instalación de Nextcloud y cómo: modo de mantenimiento, copia de las carpetas y volcado de MariaDB, MySQL, SQLite o PostgreSQL."
---
# Copia de seguridad

## Resumen

Esta página enumera los cinco elementos que hay que conservar para respaldar una instalación de Nextcloud y da los comandos para activar el modo de mantenimiento, copiar las carpetas y volcar la base de datos según su motor. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/maintenance/backup.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Para hacer una copia de seguridad de una instalación de Nextcloud hay cinco elementos principales que conservar:

1. La carpeta de configuración
2. La carpeta de apps personalizadas (solo si hay apps personalizadas instaladas)
3. La carpeta de datos
4. La carpeta del tema
5. La base de datos

### Modo de mantenimiento

`maintenance:mode` bloquea las sesiones de los usuarios que han iniciado sesión e impide nuevos inicios de sesión para evitar incoherencias en los datos. `occ` debe ejecutarse como el usuario HTTP, como en este ejemplo en Ubuntu Linux:

```
$ sudo -E -u www-data php occ maintenance:mode --on
```

También puede ponerse el servidor en este modo editando {file}`config/config.php`. Cambiar `"maintenance" => false` por `"maintenance" => true`:

```
<?php

 "maintenance" => true,
```

No hay que olvidar volver a cambiarlo a `false` al terminar.

### Copia de seguridad de las carpetas

Copiar los directorios de configuración, datos y tema a una ubicación fuera del entorno de Nextcloud. Como alternativa, copiar todo el directorio de instalación de Nextcloud (incluido el directorio de datos). Puede usarse este comando:

```
rsync -Aavx nextcloud/ nextcloud-dirbkp_`date +"%Y%m%d"`/
```

### Copia de seguridad de la base de datos

:::{warning}
Antes de restaurar una copia de seguridad, consultar {nc-doc}`admin_manual/maintenance/restore`
:::

#### MariaDB

MariaDB es el motor de base de datos recomendado. Para hacer una copia de seguridad de MariaDB con [mariadb-dump](https://mariadb.com/docs/server/clients-and-utilities/backup-restore-and-import-clients/mariadb-dump):

```
mariadb-dump --single-transaction -h [server] -u [username] -p[password] [db_name] > nextcloud-sqlbkp_`date +"%Y%m%d"`.bak
```

Si se ha activado la compatibilidad de MariaDB con 4 bytes ({nc-doc}`admin_manual/configuration_database/mysql_4byte_support`, necesaria para los emoji), añadir `--default-character-set=utf8mb4`:

```
mariadb-dump --single-transaction --default-character-set=utf8mb4 -h [server] -u [username] -p[password] [db_name] > nextcloud-sqlbkp_`date +"%Y%m%d"`.bak
```

#### MySQL

Para hacer una copia de seguridad de MySQL:

```
mysqldump --single-transaction -h [server] -u [username] -p[password] [db_name] > nextcloud-sqlbkp_`date +"%Y%m%d"`.bak
```

Si se ha activado la compatibilidad de MySQL con 4 bytes ({nc-doc}`admin_manual/configuration_database/mysql_4byte_support`, necesaria para los emoji), añadir `--default-character-set=utf8mb4`:

```
mysqldump --single-transaction --default-character-set=utf8mb4 -h [server] -u [username] -p[password] [db_name] > nextcloud-sqlbkp_`date +"%Y%m%d"`.bak
```

#### SQLite

```
sqlite3 data/owncloud.db .dump > nextcloud-sqlbkp_`date +"%Y%m%d"`.bak
```

#### PostgreSQL

```
PGPASSWORD="password" pg_dump [db_name] -h [server] -U [username] -f nextcloud-sqlbkp_`date +"%Y%m%d"`.bak
```
````
