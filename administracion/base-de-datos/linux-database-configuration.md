---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Requisitos y parámetros de la base de datos: configurar MySQL, MariaDB o PostgreSQL, SSL para MySQL, solución de problemas y comandos SQL útiles."
---
# Configuración de la base de datos

## Resumen

Esta página cubre las bases de datos que admite el servidor y cómo prepararlas: el nivel de aislamiento de transacciones, la configuración de MySQL o MariaDB (con SSL) y de PostgreSQL, la solución de problemas de conexión y algunos comandos SQL útiles. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_database/linux_database_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud necesita una base de datos en la que se almacenan los datos administrativos. Actualmente se admiten las siguientes bases de datos:

- [MySQL](https://www.mysql.com/) / [MariaDB](https://mariadb.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Oracle](http://www.oracle.com/) (*solo para Nextcloud Enterprise*)

Las bases de datos PostgreSQL o MariaDB son los motores de base de datos recomendados.

:::{tip}
No se recomiendan todas las versiones de cada base de datos compatible. Revisar los {nc-doc}`Requisitos del sistema <admin_manual/installation/system_requirements>` de Nextcloud antes de decidirse por una versión concreta.
:::

### Requisitos

- Decidir si se desea usar MySQL / MariaDB, PostgreSQL u Oracle como base de datos
- Elegir una versión recomendada de la base de datos consultando los {nc-doc}`Requisitos del sistema <admin_manual/installation/system_requirements>` de Nextcloud
- Instalar y configurar el software de servidor de base de datos elegido (y la versión preferida) antes de desplegar Nextcloud Server

:::{note}
Los pasos para configurar una base de datos de terceros quedan fuera del alcance de este documento. Consultar la documentación de la base de datos elegida para obtener instrucciones.
:::

(nc-db-transaction-label)=
#### Nivel de aislamiento de transacciones "READ COMMITTED" de la base de datos

Como se indicó más arriba, Nextcloud usa el nivel de aislamiento de transacciones `TRANSACTION_READ_COMMITTED`. Algunas configuraciones de base de datos imponen otros niveles de aislamiento de transacciones. Para evitar la pérdida de datos en escenarios de carga alta (p. ej., al usar el cliente de sincronización con muchos clientes/usuarios y muchas operaciones en paralelo), hay que configurar el nivel de aislamiento de transacciones en consecuencia. Consultar el [manual de MySQL](https://dev.mysql.com/doc/refman/8.0/en/set-transaction.html) para obtener información detallada.

### Parámetros

Para configurar Nextcloud con cualquier base de datos, seguir las instrucciones de {nc-doc}`Asistente de instalación <admin_manual/installation/installation_wizard>`. No debería ser necesario editar los valores correspondientes en {file}`config/config.php`. Sin embargo, en casos especiales (por ejemplo, si se quiere conectar la instancia de Nextcloud a una base de datos creada por una instalación anterior de Nextcloud), puede hacer falta alguna modificación.

(nc-db-config-mysql-label)=
#### Configurar una base de datos MySQL o MariaDB

Si se decide usar una base de datos MySQL o MariaDB, asegurarse de lo siguiente:

- El nivel de aislamiento de transacciones está establecido en "READ-COMMITTED" en la configuración del servidor MariaDB, {file}`/etc/mysql/my.cnf`, para que se mantenga incluso después de reiniciar el servidor de base de datos.

  Verificar **transaction_isolation** y **binlog_format**:

```
[mysqld]
...
transaction_isolation = READ-COMMITTED
binlog_format = ROW
...
```

El archivo {file}`/etc/mysql/my.cnf` podría quedar así:

```
[server]
skip_name_resolve = 1
innodb_buffer_pool_size = 128M
innodb_buffer_pool_instances = 1
innodb_flush_log_at_trx_commit = 2
innodb_log_buffer_size = 32M
innodb_max_dirty_pages_pct = 90
query_cache_type = 1
query_cache_limit = 2M
query_cache_min_res_unit = 2k
query_cache_size = 64M
tmp_table_size= 64M
max_heap_table_size= 64M
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 1

[client-server]
!includedir /etc/mysql/conf.d/
!includedir /etc/mysql/mariadb.conf.d/

[client]
default-character-set = utf8mb4

[mysqld]
character_set_server = utf8mb4
collation_server = utf8mb4_bin
transaction_isolation = READ-COMMITTED
binlog_format = ROW
innodb_large_prefix=on
innodb_file_format=barracuda
innodb_file_per_table=1
```

Consultar la [página del manual de MySQL](https://mariadb.com/kb/en/library/set-transaction/#read-committed).

- Que se haya instalado y habilitado la extensión pdo_mysql en PHP

- Que **mysql.default_socket** apunte al socket correcto (si la base de datos se ejecuta en el mismo servidor que Nextcloud).

:::{note}
MariaDB es retrocompatible con MySQL. Todas las instrucciones sirven para ambos. No hace falta sustituir mysql por nada.
:::

La configuración de PHP en {file}`/etc/php7/conf.d/mysql.ini` podría quedar así:

```
# configuration for PHP MySQL module
extension=pdo_mysql.so

[mysql]
mysql.allow_local_infile=On
mysql.allow_persistent=On
mysql.cache_size=2000
mysql.max_persistent=-1
mysql.max_links=-1
mysql.default_port=
mysql.default_socket=/var/lib/mysql/mysql.sock  # Debian squeeze: /var/run/mysqld/mysqld.sock
mysql.default_host=
mysql.default_user=
mysql.default_password=
mysql.connect_timeout=60
mysql.trace_mode=Off
```

A continuación hay que crear un usuario de base de datos y la propia base de datos mediante la interfaz de línea de comandos de MySQL. Nextcloud crea las tablas de la base de datos la primera vez que se inicia sesión.

Para iniciar el modo de línea de comandos de MySQL, usar:

```
mysql -uroot -p
```

Si se usa MariaDB, usar:

```
mariadb -uroot -p
```

Aparecerá entonces el indicador **mysql>** o **MariaDB [root]>**. Introducir las siguientes líneas y confirmarlas con la tecla Intro:

```
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE IF NOT EXISTS nextcloud CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
GRANT ALL PRIVILEGES on nextcloud.* to 'username'@'localhost';
```

Para salir del indicador, introducir:

```
quit;
```

Una instancia de Nextcloud configurada con MySQL contendría el nombre del host en el que se ejecuta la base de datos, un nombre de usuario y una contraseña válidos para acceder a ella, y el nombre de la base de datos. Por lo tanto, el archivo {file}`config/config.php` creado por el {nc-doc}`Asistente de instalación <admin_manual/installation/installation_wizard>` contendría entradas como estas:

```
<?php

  "dbtype"        => "mysql",
  "dbname"        => "nextcloud",
  "dbuser"        => "username",
  "dbpassword"    => "password",
  "dbhost"        => "localhost",
  "dbtableprefix" => "oc_",
```

En el caso de UTF8MB4, también aparecerá:

```
"mysql.utf8mb4" => true,
```

#### SSL para la base de datos MySQL

Habilitar SSL solo es necesario si la base de datos no está en el mismo servidor que la instancia de Nextcloud. Si la conexión no se hace por localhost y hay que permitir conexiones remotas, se debería habilitar SSL. Aquí solo se trata la configuración SSL de la base de datos en el servidor Nextcloud. Primero hay que configurar el servidor de base de datos en consecuencia.

```
'dbdriveroptions' => [
  \PDO::MYSQL_ATTR_SSL_KEY => '/../ssl-key.pem',
  \PDO::MYSQL_ATTR_SSL_CERT => '/../ssl-cert.pem',
  \PDO::MYSQL_ATTR_SSL_CA => '/../ca-cert.pem',
  \PDO::MYSQL_ATTR_SSL_VERIFY_SERVER_CERT => true,
],
```

Ajustar las rutas de los archivos pem al entorno propio.

(nc-db-config-postgresql-label)=
#### Base de datos PostgreSQL

Para ejecutar Nextcloud de forma segura sobre PostgreSQL, se supone que solo Nextcloud usa esta base de datos y, por tanto, que solo un usuario accede a ella. Para otros servicios y usuarios, se recomienda crear una base de datos o una instancia de PostgreSQL separada.

Si se decide usar una base de datos PostgreSQL, asegurarse de haber instalado y habilitado la extensión PostgreSQL en PHP. La configuración de PHP en {file}`/etc/php7/conf.d/pgsql.ini` podría quedar así:

```
# configuration for PHP PostgreSQL module
extension=pdo_pgsql.so
extension=pgsql.so

[PostgreSQL]
pgsql.allow_persistent = On
pgsql.auto_reset_persistent = Off
pgsql.max_persistent = -1
pgsql.max_links = -1
pgsql.ignore_notice = 0
pgsql.log_notice = 0
```

La configuración predeterminada de PostgreSQL (al menos en Ubuntu 14.04) usa el método de autenticación peer. Revisar {file}`/etc/postgresql/9.3/main/pg_hba.conf` para saber qué método de autenticación se usa en la instalación propia. Para iniciar el modo de línea de comandos de postgres, usar:

```
sudo -u postgres psql -d template1
```

Aparecerá entonces el indicador **template1=#**. Introducir las siguientes líneas y confirmarlas con la tecla Intro:

```
CREATE USER username CREATEDB;
CREATE DATABASE nextcloud OWNER username TEMPLATE template0 ENCODING 'UTF8';
GRANT CREATE ON SCHEMA public TO username;
```

Para salir del indicador, introducir:

```
\q
```

Una instancia de Nextcloud configurada con PostgreSQL contendría, como nombre del host, la ruta al socket en el que se ejecuta la base de datos; el nombre de usuario del sistema que usa el proceso de PHP y una contraseña vacía para acceder a ella; y el nombre de la base de datos. Por lo tanto, el archivo {file}`config/config.php` creado por el {nc-doc}`Asistente de instalación <admin_manual/installation/installation_wizard>` contendría entradas como estas:

```
<?php

  "dbtype"        => "pgsql",
  "dbname"        => "nextcloud",
  "dbuser"        => "username",
  "dbpassword"    => "",
  "dbhost"        => "/var/run/postgresql",
  "dbtableprefix" => "oc_",
```

:::{note}
En realidad, el host apunta al socket que se usa para conectarse a la base de datos. Usar localhost aquí no funciona si PostgreSQL está configurado para usar la autenticación peer. Además, no se especifica ninguna contraseña, porque este método de autenticación no usa contraseña.
:::

Si se usa otro método de autenticación (no peer), hay que seguir los pasos siguientes para preparar la base de datos: ahora hay que crear un usuario de base de datos y la propia base de datos mediante la interfaz de línea de comandos de PostgreSQL. Nextcloud crea las tablas de la base de datos la primera vez que se inicia sesión.

Para iniciar el modo de línea de comandos de postgres, usar:

```
psql -hlocalhost -Upostgres
```

Aparecerá entonces el indicador **postgres=#**. Introducir las siguientes líneas y confirmarlas con la tecla Intro:

```
CREATE USER username WITH PASSWORD 'password' CREATEDB;
CREATE DATABASE nextcloud TEMPLATE template0 ENCODING 'UTF8';
ALTER DATABASE nextcloud OWNER TO username;
GRANT ALL PRIVILEGES ON DATABASE nextcloud TO username;
GRANT ALL PRIVILEGES ON SCHEMA public TO username;
```

Para salir del indicador, introducir:

```
\q
```

Una instancia de Nextcloud configurada con PostgreSQL contendría el nombre del host en el que se ejecuta la base de datos, un nombre de usuario y una contraseña válidos para acceder a ella, y el nombre de la base de datos. Por lo tanto, el archivo {file}`config/config.php` creado por el {nc-doc}`Asistente de instalación <admin_manual/installation/installation_wizard>` contendría entradas como estas:

```
<?php

  "dbtype"        => "pgsql",
  "dbname"        => "nextcloud",
  "dbuser"        => "username",
  "dbpassword"    => "password",
  "dbhost"        => "localhost",
  "dbtableprefix" => "oc_",
```

(nc-db-troubleshooting-label)=
### Solución de problemas

#### Cómo sortear «general error: 2006 MySQL server has gone away»

La consulta a la base de datos tarda demasiado y, por eso, se agota el tiempo de espera del servidor MySQL. También es posible que el servidor esté descartando un paquete demasiado grande. Consultar el manual de la base de datos para saber cómo aumentar las opciones de configuración `wait_timeout` y/o `max_allowed_packet`.

Algunos proveedores de alojamiento compartido no permiten acceder a estas opciones de configuración. Para esos sistemas, Nextcloud ofrece la opción de configuración `dbdriveroptions` en {file}`config/config.php`, con la que se pueden pasar esas opciones al controlador de la base de datos. Consultar {nc-doc}`Parámetros de configuración <admin_manual/configuration_server/config_sample_php_parameters>` para ver un ejemplo.

#### ¿Cómo saber si el servidor MySQL/PostgreSQL es accesible?

Para comprobar la disponibilidad de red del servidor, usar el comando ping con el nombre de host del servidor (db.server.com en este ejemplo):

```
ping db.server.com
```

```
PING db.server.com (ip-address) 56(84) bytes of data.
64 bytes from your-server.local.lan (192.168.1.10): icmp_req=1 ttl=64 time=3.64 ms
64 bytes from your-server.local.lan (192.168.1.10): icmp_req=2 ttl=64 time=0.055 ms
64 bytes from your-server.local.lan (192.168.1.10): icmp_req=3 ttl=64 time=0.062 ms
```

Para una comprobación más detallada de si el acceso al propio software del servidor de base de datos funciona correctamente, ver la siguiente pregunta.

#### ¿Cómo saber si un usuario creado puede acceder a una base de datos?

La forma más sencilla de comprobar si una base de datos es accesible es iniciar la interfaz de línea de comandos:

**MySQL**:

Suponiendo que el servidor de base de datos está instalado en el mismo sistema desde el que se ejecuta el comando, usar:

```
mysql -uUSERNAME -p
```

Para acceder a una instalación de MySQL en otra máquina, añadir la opción -h con el nombre de host correspondiente:

```
mysql -uUSERNAME -p -h HOSTNAME
```

```
mysql> SHOW VARIABLES LIKE "version";
+---------------+--------+
| Variable_name | Value  |
+---------------+--------+
| version       | 8.0.36 |
+---------------+--------+
1 row in set (0.00 sec)
mysql> quit
```

**PostgreSQL**:

Suponiendo que el servidor de base de datos está instalado en el mismo sistema desde el que se ejecuta el comando, usar:

```
psql -Uusername -dnextcloud
```

Para acceder a una instalación de PostgreSQL en otra máquina, añadir la opción -h con el nombre de host correspondiente:

```
psql -Uusername -dnextcloud -h HOSTNAME
```

```
postgres=# SELECT version();
PostgreSQL 16.2 on i686-pc-linux-gnu, compiled by GCC gcc (GCC) 4.1.3 20080704 (prerelease), 32-bit
(1 row)
postgres=# \q
```

#### Comandos SQL útiles

**Mostrar los usuarios de la base de datos**:

```
MySQL     : SELECT User,Host FROM mysql.user;
PostgreSQL: SELECT * FROM pg_user;
```

**Mostrar las bases de datos disponibles**:

```
MySQL     : SHOW DATABASES;
PostgreSQL: \l
```

**Mostrar las tablas de Nextcloud en la base de datos**:

```
MySQL     : USE nextcloud; SHOW TABLES;
PostgreSQL: \c nextcloud; \d
```

**Salir de la base de datos**:

```
MySQL     : quit
PostgreSQL: \q
```
````
