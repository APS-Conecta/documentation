---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo restaurar una copia de seguridad de Nextcloud: carpetas, base de datos (MariaDB, MySQL, SQLite, PostgreSQL) y resincronización con los clientes."
---
# Restaurar una copia de seguridad

## Resumen

Esta página explica cómo restaurar una instalación de Nextcloud desde una copia de seguridad: las carpetas, la eliminación y recreación de la base de datos, la importación del volcado según el motor y la sincronización con los clientes tras recuperar los datos. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/maintenance/restore.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Para restaurar una instalación de Nextcloud hay cuatro elementos principales que restaurar:

1. El directorio de configuración
2. El directorio de datos
3. La base de datos
4. El directorio del tema

:::{note}
Se necesitan la base de datos, el directorio de datos y los archivos de configuración. La restauración no puede completarse sin los tres.
:::

### Restaurar las carpetas

:::{note}
Esta guía supone que la copia de seguridad anterior se llama «nextcloud-dirbkp»
:::

Basta con copiar la carpeta de configuración y la de datos (o incluso toda la instalación de Nextcloud y la carpeta de datos) al entorno de Nextcloud. Puede usarse este comando:

```
rsync -Aax nextcloud-dirbkp/ nextcloud/
```

### Restaurar la base de datos

:::{warning}
Antes de restaurar una copia de seguridad hay que asegurarse de eliminar todas las tablas existentes de la base de datos.
:::

La forma más sencilla de hacerlo es eliminar la base de datos y volver a crearla. SQLite lo hace automáticamente.

#### MariaDB

MariaDB es el motor de base de datos recomendado. Para restaurar MariaDB con el cliente [mariadb](https://mariadb.com/docs/server/clients-and-utilities/mariadb-client/mariadb-command-line-client):

```
mariadb -h [server] -u [username] -p[password] -e "DROP DATABASE nextcloud"
mariadb -h [server] -u [username] -p[password] -e "CREATE DATABASE nextcloud"
```

Si se usa UTF8 con compatibilidad multibyte (p. ej., para emojis en los nombres de archivo), usar:

```
mariadb -h [server] -u [username] -p[password] -e "DROP DATABASE nextcloud"
mariadb -h [server] -u [username] -p[password] -e "CREATE DATABASE nextcloud CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"
```

#### MySQL

Para restaurar MySQL:

```
mysql -h [server] -u [username] -p[password] -e "DROP DATABASE nextcloud"
mysql -h [server] -u [username] -p[password] -e "CREATE DATABASE nextcloud"
```

Si se usa UTF8 con compatibilidad multibyte (p. ej., para emojis en los nombres de archivo), usar:

```
mysql -h [server] -u [username] -p[password] -e "DROP DATABASE nextcloud"
mysql -h [server] -u [username] -p[password] -e "CREATE DATABASE nextcloud CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"
```

#### PostgreSQL

```
PGPASSWORD="password" psql -h [server] -U [username] -d template1 -c "DROP DATABASE \"nextcloud\";"
PGPASSWORD="password" psql -h [server] -U [username] -d template1 -c "CREATE DATABASE \"nextcloud\";"
```

### Restauración

:::{note}
Esta guía supone que la copia de seguridad anterior se llama «nextcloud-sqlbkp.bak»
:::

#### MariaDB

MariaDB es el motor de base de datos recomendado. Para restaurar MariaDB con el cliente [mariadb](https://mariadb.com/docs/server/clients-and-utilities/mariadb-client/mariadb-command-line-client):

```
mariadb -h [server] -u [username] -p[password] [db_name] < nextcloud-sqlbkp.bak
```

#### MySQL

Para restaurar MySQL:

```
mysql -h [server] -u [username] -p[password] [db_name] < nextcloud-sqlbkp.bak
```

#### SQLite

```
rm data/owncloud.db
sqlite3 data/owncloud.db < nextcloud-sqlbkp.bak
```

#### PostgreSQL

```
PGPASSWORD="password" psql -h [server] -U [username] -d nextcloud -f nextcloud-sqlbkp.bak
```

### Sincronizar con los clientes tras recuperar los datos

De forma predeterminada, el servidor Nextcloud se considera la fuente autorizada de los datos. Si los datos del servidor y los del cliente difieren, los clientes obtendrán de forma predeterminada los datos del servidor.

Si la copia de seguridad recuperada está desactualizada, el estado de los clientes puede estar más actualizado que el del servidor. En este caso, asegurarse también de ejecutar después el comando {nc-ref}`maintenance:data-fingerprint <maintenance_commands_label>`. Este comando cambia la lógica del algoritmo de sincronización para intentar recuperar tantos datos como sea posible. Por tanto, los archivos que faltan en el servidor se recuperan de los clientes y, en caso de contenido distinto, se pregunta a los usuarios.

Esto también puede ayudar en casos poco frecuentes en que la base de datos es más reciente que el directorio de datos. El servidor restaurará los datos desde los clientes y conservará los elementos compartidos. Hasta entonces, los archivos serían visibles pero no accesibles. Después se necesita un {nc-ref}`files:scan <occ_files_scan_label>` para actualizar la base de datos.

:::{note}
El uso de *maintenance:data-fingerprint* puede provocar diálogos de conflicto y dificultades para eliminar archivos en el cliente. Por eso solo se recomienda para evitar la pérdida de datos si la copia de seguridad estaba desactualizada. Este comando no requiere que el servidor esté en modo de mantenimiento.
:::

Si se ejecutan varios servidores de aplicaciones, hay que asegurarse de que los archivos de configuración estén sincronizados entre ellos para que el *data-fingerprint* actualizado se aplique en todas las instancias.
````
