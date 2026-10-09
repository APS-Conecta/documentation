---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Preconfigurar la instalación con config/autoconfig.php: parámetros con otro nombre y ejemplos para el directorio de datos y cada base de datos."
---
# Configuración automática

## Resumen

Esta página explica cómo preconfigurar la instalación con el archivo `config/autoconfig.php`, qué parámetros se llaman distinto que en `config.php` y qué pide la pantalla final según los parámetros dados. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/installation/automatic_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

Cuando hay que instalar Nextcloud en varios servidores, normalmente no se quiere configurar cada instancia por separado como se describe en {nc-doc}`admin_manual/configuration_database/linux_database_configuration`. Por este motivo, Nextcloud ofrece una función de configuración automática.

Para aprovechar esta función, hay que crear un archivo de configuración llamado {file}`config/autoconfig.php` y definir en él los parámetros que se necesiten. En este archivo puede indicarse cualquier cantidad de parámetros. Los parámetros que no se indiquen aparecen en la pantalla «Finish setup» la primera vez que se inicia Nextcloud.

El archivo {file}`config/autoconfig.php` se elimina automáticamente después de aplicar la configuración inicial.

:::{note}
Tener en cuenta que la configuración automática no elimina la necesidad de crear de antemano el usuario de la base de datos y la base de datos, como se describe en {nc-doc}`admin_manual/configuration_database/linux_database_configuration`.
:::

### Parámetros

Al configurar los parámetros, hay que tener en cuenta que dos parámetros tienen en este archivo de configuración un nombre distinto del que tienen en el archivo estándar {file}`config.php`.

| autoconfig.php | config.php |
|---|---|
| directory | datadirectory |
| dbpass | dbpassword |

### Ejemplos de configuración automática

Las secciones siguientes ofrecen ejemplos de configuración automática e indican qué información se solicita al final de la configuración.

#### Directorio de datos

Con los siguientes valores de parámetros, la pantalla «Finish setup» solicita la configuración de la base de datos y las credenciales del administrador.

```
<?php
$AUTOCONFIG = [
  "directory"     => "/www/htdocs/nextcloud/data",
];
```

#### Base de datos SQLite

Con los siguientes valores de parámetros, la pantalla «Finish setup» solicita la configuración del directorio de datos y las credenciales del administrador.

```
<?php
$AUTOCONFIG = [
  "dbtype"        => "sqlite",
  "dbname"        => "nextcloud",
  "dbtableprefix" => "",
];
```

#### Base de datos MySQL

Con los siguientes valores de parámetros, la pantalla «Finish setup» solicita la configuración del directorio de datos y las credenciales del administrador.

```
<?php
$AUTOCONFIG = array(
  "dbtype"        => "mysql",
  "dbname"        => "nextcloud",
  "dbuser"        => "username",
  "dbpass"        => "password",
  "dbhost"        => "localhost",
  "dbtableprefix" => "",
);
```

#### Base de datos PostgreSQL

Con los siguientes valores de parámetros, la pantalla «Finish setup» solicita la configuración del directorio de datos y las credenciales del administrador.

```
<?php
$AUTOCONFIG = array(
  "dbtype"        => "pgsql",
  "dbname"        => "nextcloud",
  "dbuser"        => "username",
  "dbpass"        => "password",
  "dbhost"        => "localhost",
  "dbtableprefix" => "",
);
```

:::{note}
Tener en cuenta que la configuración automática no elimina la necesidad de crear de antemano el usuario de la base de datos y la base de datos, como se describe en {nc-doc}`admin_manual/configuration_database/linux_database_configuration`.
:::

#### Todos los parámetros

Con los siguientes valores de parámetros, como todos los parámetros ya están configurados en el archivo, la instalación de Nextcloud omite la pantalla «Finish setup».

```
<?php
$AUTOCONFIG = array(
  "dbtype"        => "mysql",
  "dbname"        => "nextcloud",
  "dbuser"        => "username",
  "dbpass"        => "password",
  "dbhost"        => "localhost",
  "dbtableprefix" => "",
  "adminlogin"    => "root",
  "adminpass"     => "root-password",
  "directory"     => "/www/htdocs/nextcloud/data",
);
```

:::{note}
Tener en cuenta que la configuración automática no elimina la necesidad de crear de antemano el usuario de la base de datos y la base de datos, como se describe en {nc-doc}`admin_manual/configuration_database/linux_database_configuration`.
:::
````
