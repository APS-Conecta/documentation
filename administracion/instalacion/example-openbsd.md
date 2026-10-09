---
tipo: tutorial
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Recorrido de instalación en OpenBSD, sin soporte oficial: httpd(8), PHP-FPM, PostgreSQL, redis, tarea cron, chroot y asistente web."
---
(nc-openbsd_installation_label)=
# Ejemplo de instalación en OpenBSD

## Resumen

Este tutorial recorre una instalación sobre un OpenBSD mínimo con httpd(8), PHP, PostgreSQL y redis: paquetes, servidor web, base de datos, caché, tarea cron, chroot y los pasos finales en el asistente web. La plataforma no tiene soporte oficial. Está dirigido a quienes administran el servidor.

````{upstream} admin_manual/installation/example_openbsd.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

:::{warning}
{vendor}`Nextcloud` no ofrece soporte oficial para OpenBSD ni para otros BSD
:::

En este tutorial de instalación se despliega Nextcloud sobre un OpenBSD mínimo con nuestro propio httpd(8), PHP, PostgreSQL y redis (los pasos son los mismos para -stable y para -current).

Desde un sistema OpenBSD con la instalación base, basta con ejecutar:

```
# pkg_add nextcloud
```

Los paquetes adicionales:

```
# pkg_add postgresql-server redis pecl82-redis php-pdo_pgsql
```

Esto se encarga de las dependencias y ofrece las opciones para elegir la versión de PHP que se quiera.

### HTTPD(8)

Crear un virtualhost en `/etc/httpd.conf` y añadirle el siguiente contenido:

```
  server "domain.tld" {
      listen on egress tls port 443
      hsts {
    max-age 15768000
    preload
    subdomains
  }

    tls {
          certificate "/etc/ssl/domain.tld_fullchain.pem"
          key "/etc/ssl/private/domain.tld_private.pem"
    }

    # Set max upload size to 513M (in bytes)
    connection max request body 537919488
    connection max requests 1000
    connection request timeout 3600
    connection timeout 3600

    root "/nextcloud"
    directory index "index.php"

    # Ensure that no '*.php*' files can be fetched from these directories
    location "/config/*" {
        block drop
    }

    location "/data/*" {
        block drop
    }

    # Note that this matches "*.php*" anywhere in the request path.
    location "/nextcloud/*.php*" {
        fastcgi socket "/run/php-fpm.sock"
    }

    location "/apps/*" {
        pass
    }

    location "/core/*" {
        pass
    }

    location "/.well-known/carddav" {
        block return 301 "https://$SERVER_NAME/remote.php/dav"
    }

    location "/.well-known/caldav" {
        block return 301 "https://$SERVER_NAME/remote.php/dav"
    }

    location "/.well-known/webfinger" {
        block return 301 "https://$SERVER_NAME/public.php?service=webfinger"
    }

    location match "/ocs-provider/*" {
        pass
    }
}
```

Asegurarse de que httpd(8) está habilitado e iniciado:

```
# rcctl enable httpd
# rcctl start httpd
```

### PHP

Suponiendo que se usa OpenBSD -current (o >= 6.8-stable), se puede usar PHP 8.2, así que aquí se mantiene esa versión, pero el concepto es el mismo para otras versiones.

Los paquetes de PHP estarán disponibles, ya que Nextcloud se instaló con pkg_add, así que solo hace falta ajustar un poco el php.ini.

Se recomienda añadirle opcache:

```
[opcache]
opcache.enable=1
opcache.memory_consumption=512
opcache.interned_strings_buffer=8
opcache.max_accelerated_files=10000
opcache.revalidate_freq=1
opcache.save_comments=1
```

Y aumentar algunos límites:

```
post_max_size = 513M
upload_max_filesize = 513M
```

Los módulos de PHP pueden habilitarse con:

```
# cd /etc/php-8.2.sample
# for i in *; do ln -sf ../php-8.2.sample/$i ../php-8.2/; done
```

Y luego solo queda habilitar e iniciar PHP:

```
# rcctl enable php82_fpm
# rcctl start php82_fpm
```

### Base de datos

Como se ha mencionado, se usará PostgreSQL como base de datos; ya está instalado y ahora hay que inicializarlo:

```
$ su - _postgresql
$ mkdir /var/postgresql/data
$ initdb -D /var/postgresql/data -U postgres -A md5 -E UTF8 -W
...
Enter new superuser password: PASSWORD
Enter it again: PASSWORD
...
Success. You can now start the database server using:

pg_ctl -D /var/postgresql/data -l logfile start

$ pg_ctl -D /var/postgresql/data -l logfile start
server starting
$ exit
```

Hay que comprobar, habilitar e iniciar postgres:

```
# rcctl check postgresql
# rcctl enable postgresql
# rcctl start postgresql
```

Para crear usuarios y permisos, puede seguirse el README de `/usr/local/share/doc/pkg-readmes/postgresql-server`.

### Redis

Redis se instaló antes; hay que habilitarlo e iniciarlo, y también añadirlo a la configuración de Nextcloud:

```
# rcctl enable redis
# rcctl start redis
# mg /var/www/nextcloud/config/config.php
...
  'memcache.local' => '\OC\Memcache\Redis',
  'redis' => array(
  'host' => 'localhost',
  'port' => 6379,
  'timeout' => 0.0,
),
...
```

### Tarea cron

Hay que añadir la tarea cron de Nextcloud para que se realicen algunas tareas, agregando esta entrada al cronjob:

```
*/5 * * * * /usr/bin/ftp -Vo - https://domain.tld/cron.php >/dev/null
```

### Chroot

Como en OpenBSD httpd(8) funciona de forma predeterminada con un chroot(8), hay que asegurarse de que los archivos necesarios están dentro de la jaula /var/www:

```
# mkdir -p /var/www/etc/ssl
# install -m 444 -o root -g bin /etc/ssl/cert.pem /etc/ssl/openssl.cnf \
        /var/www/etc/ssl/
# cp /etc/resolv.conf /var/www/etc
```

### Pasos finales de Nextcloud

Los pasos de instalación restantes se completan en el asistente de instalación web.

Para activar este asistente, crear un archivo llamado CAN_INSTALL dentro de la carpeta config de la instalación:

> \# touch /var/www/nextcloud/config/CAN_INSTALL

Usar el navegador para ir a la URL de la instalación:

> <https://domain.tld>

Ahora solo hay que seguir los pasos e indicar el nombre de la base de datos, el usuario y las contraseñas.

Tener en cuenta que las actualizaciones de Nextcloud pueden hacerse ejecutando, en -current:

```
# pkg_add -u -Dsnap
```

Y en -stable:

```
# pkg_add -u
```

Después solo hay que seguir los pasos desde el navegador.

### NOTA

Recordar leer siempre todos los README de los paquetes de OpenBSD en:

```
/usr/local/share/doc/pkg-readmes/
```

Allí está disponible toda esta información y más.
````
