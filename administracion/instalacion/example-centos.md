---
tipo: tutorial
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Recorrido de instalación en CentOS 8, sin soporte desde 2021: Apache, PHP, MariaDB, Redis como memcache y SELinux, conservado como referencia."
---
(nc-centos7_installation_label)=
# Ejemplo de instalación en CentOS 8

## Resumen

Este tutorial recorre una instalación básica sobre CentOS 8 con Apache, PHP, MariaDB y Redis como memcache, incluidos los ajustes de cortafuegos y SELinux. CentOS 8 ya no recibe actualizaciones de seguridad y la página se conserva solo como referencia. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/installation/example_centos.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

:::{warning}
CentOS 8 llegó al final de su vida útil el 31 de diciembre de 2021 y ya no recibe actualizaciones de seguridad. Esta guía se conserva solo como referencia y puede estar desactualizada. Para despliegues en producción, usar una distribución Linux con soporte vigente.
:::

En este tutorial de instalación se despliegan CentOS 8, PHP 7.4, MariaDB, Redis como memcache y Nextcloud funcionando sobre Apache.

Se empieza con una instalación mínima de CentOS 8. Debería ofrecer una plataforma suficiente para ejecutar con éxito una instancia de Nextcloud.

Primero, instalar algunas dependencias que se necesitarán durante la instalación, pero que también serán útiles en el uso diario:

```
dnf install -y epel-release yum-utils unzip curl wget \
bash-completion policycoreutils-python-utils mlocate bzip2
```

Ahora, asegurarse de que el sistema está actualizado:

```
dnf update -y
```

### Apache

```
dnf install -y httpd
```

Crear un virtualhost en `/etc/httpd/conf.d/nextcloud.conf` y añadirle el siguiente contenido:

```
<VirtualHost *:80>
  DocumentRoot /var/www/html/nextcloud/
  ServerName  your.server.com

  <Directory /var/www/html/nextcloud/>
    Require all granted
    AllowOverride All
    Options FollowSymLinks MultiViews

    <IfModule mod_dav.c>
      Dav off
    </IfModule>

  </Directory>
</VirtualHost>
```

Ver {nc-ref}`apache_configuration_label` para más detalles.

Asegurarse de que el servicio web apache está habilitado e iniciado:

```
systemctl enable httpd.service
systemctl start httpd.service
```

### PHP

:::{note}
CentOS 8 no incluye paquetes para las extensiones php redis e imagick. Pueden instalarse mediante pecl. Además de los paquetes oficiales de PHP, hay repositorios de terceros disponibles en `https://rpms.remirepo.net`. Con remirepo también se puede instalar la versión más reciente de PHP en lugar de la que se distribuye de serie.
:::

#### Configurar remirepo con PHP 8.2

Hay más detalles en `https://blog.remirepo.net/pages/Config-en`

Comando para instalar el paquete de configuración del repositorio Remi:

```
dnf install https://rpms.remirepo.net/enterprise/remi-release-8.rpm
```

Comando para instalar el paquete yum-utils (para el comando yum-config-manager):

```
dnf install yum-utils
```

Se quiere una única versión, lo que implica reemplazar los paquetes base de la distribución. Los paquetes tienen el mismo nombre que en el repositorio base, es decir, php-\*. Algunas dependencias comunes están disponibles en el repositorio remi-safe, que está habilitado de forma predeterminada.

Hay que habilitar el flujo del módulo para 8.2:

```
dnf module reset php
dnf module install php:remi-8.2
dnf update
```

#### Instalar PHP y los módulos necesarios

A continuación, instalar los módulos de PHP necesarios para esta instalación. Recordar que, como se trata de una instalación básica limitada, solo se instalan los módulos necesarios, no todos. Para una instalación más completa, consultar la lista de módulos de PHP en la documentación de instalación desde el código fuente, {nc-doc}`admin_manual/installation/source_installation`:

```
dnf install -y php php-cli php-gd php-mbstring php-intl php-pecl-apcu\
     php-mysqlnd php-opcache php-json php-zip
```

#### Instalar los módulos opcionales redis/imagick

```
dnf install -y php-redis php-imagick
```

### Base de datos

Como se ha mencionado, se usará MySQL/MariaDB como base de datos:

```
dnf install -y mariadb mariadb-server
```

Asegurarse de que el servicio de base de datos está habilitado para iniciarse al arrancar:

```
systemctl enable mariadb.service
systemctl start mariadb.service
```

Mejorar la seguridad de MariaDB:

```
mysql_secure_installation
```

Después, asegurarse de crear una base de datos con un nombre de usuario y una contraseña para que Nextcloud tenga acceso a ella. Para más detalles sobre la instalación y la configuración de la base de datos, consultar la documentación {nc-doc}`admin_manual/configuration_database/linux_database_configuration`.

### Redis

```
dnf install -y redis
systemctl enable redis.service
systemctl start redis.service
```

### Instalar Nextcloud

Ya casi está: hay que seguir así, ¡va muy bien!

Ahora, descargar el archivo comprimido de la última versión de Nextcloud:

- Ir a la [página de descargas de Nextcloud](https://nextcloud.com/install).
- Ir a *Download Nextcloud Server > Download > Archive file for server owners* y descargar el archivo tar.bz2 o el .zip.
- Así se descarga un archivo llamado nextcloud-x.y.z.tar.bz2 o nextcloud-x.y.z.zip (donde x.y.z es el número de versión).
- Descargar su archivo de suma de verificación correspondiente, p. ej., nextcloud-x.y.z.tar.bz2.md5 o nextcloud-x.y.z.tar.bz2.sha256.
- Verificar la suma MD5 o SHA256:

  ```
  md5sum -c nextcloud-x.y.z.tar.bz2.md5 < nextcloud-x.y.z.tar.bz2
  sha256sum -c nextcloud-x.y.z.tar.bz2.sha256 < nextcloud-x.y.z.tar.bz2
  md5sum  -c nextcloud-x.y.z.zip.md5 < nextcloud-x.y.z.zip
  sha256sum  -c nextcloud-x.y.z.zip.sha256 < nextcloud-x.y.z.zip
  ```

- También se puede verificar la firma PGP:

  ```
  wget https://download.nextcloud.com/server/releases/nextcloud-x.y.z.tar.bz2.asc
  wget https://nextcloud.com/nextcloud.asc
  gpg --import nextcloud.asc
  gpg --verify nextcloud-x.y.z.tar.bz2.asc nextcloud-x.y.z.tar.bz2
  ```

Para este recorrido se descargó la última versión de Nextcloud en forma de archivo zip, se comprobó la descarga con el comando mencionado arriba y ahora se descomprime:

```
unzip nextcloud-*.zip
```

Copiar el contenido al directorio raíz del servidor web. En este caso se usa apache, así que será `/var/www/html/`:

```
cp -R nextcloud/ /var/www/html/
```

Durante el proceso de instalación no se crea ninguna carpeta de datos, así que se crea una manualmente para ayudar al asistente de instalación:

```
mkdir /var/www/html/nextcloud/data
```

Asegurarse de que apache tiene acceso de lectura y escritura a toda la carpeta nextcloud:

```
chown -R apache:apache /var/www/html/nextcloud
```

Reiniciar apache:

```
systemctl restart httpd.service
```

Crear una regla de cortafuegos para el acceso a apache:

```
firewall-cmd --zone=public --add-service=http --permanent
firewall-cmd --reload
```

### SELinux

De nuevo, hay una descripción extensa de SELinux en {nc-doc}`admin_manual/installation/selinux_configuration`; si se usa SELinux en modo Enforcing, ejecutar los comandos que sugiere esa página. Los siguientes comandos se refieren solo a este tutorial:

```
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/data(/.*)?'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/config(/.*)?'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/apps(/.*)?'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/.htaccess'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/.user.ini'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/3rdparty/aws/aws-sdk-php/src/data/logs(/.*)?'

restorecon -R '/var/www/html/nextcloud/'

setsebool -P httpd_can_network_connect on
```

Si se necesitan más configuraciones de SELinux, consultar la URL mencionada arriba y volver a este tutorial.

Una vez terminado con SELinux, ir a `http://your.server.com/nextcloud` y seguir los pasos que se encuentran en {nc-doc}`admin_manual/installation/installation_wizard`, donde se explica exactamente cómo continuar con la parte final de la instalación, que se hace como usuario administrador a través del navegador web.

:::{note}
Si se sigue este tutorial y, después de la instalación, el navegador muestra advertencias de que `OPcache` no está habilitado o configurado correctamente, hay que hacer los cambios sugeridos en `/etc/opt/rh/rh-php74/php.d/10-opcache.ini` para que los errores desaparezcan. Estas advertencias aparecen en la página de administración, en Ajustes básicos.
:::

Como se usó `Redis` como memcache, hará falta una configuración similar al siguiente ejemplo en `/var/www/html/nextcloud/config/config.php`, que se genera automáticamente al ejecutar el asistente de instalación en línea mencionado antes.

Configuración de ejemplo:

```
'memcache.distributed' => '\OC\Memcache\Redis',
'memcache.locking' => '\OC\Memcache\Redis',
'memcache.local' => '\OC\Memcache\APCu',
'memcache_customprefix' => 'nextcloud_centos',
'redis' => array(
  'host' => 'localhost',
  'port' => 6379,
),
```

Recordar que este tutorial es solo para una instalación básica de Nextcloud en CentOS 8, con PHP 7.4. Si se van a usar más funciones, como LDAP o Single Sign On, harán falta módulos de PHP adicionales y configuraciones extra. Por eso, consultar el resto del manual de administración, {nc-doc}`admin_manual/index`, para ver descripciones detalladas de cómo hacerlo.
````
