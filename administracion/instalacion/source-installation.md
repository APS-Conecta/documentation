---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Formas de instalar Nextcloud en Linux y la instalación manual con Apache: módulos, URL amigables, SSL, PHP-FPM, VM en Windows, Snap e instalador web."
---
# Instalación en Linux

## Resumen

Esta página presenta las formas de instalar Nextcloud en Linux y recorre la instalación manual desde el archivo .tar con Apache: configuración del servidor web, URL amigables, SSL, asistente de instalación, tareas en segundo plano y PHP-FPM. También describe las máquinas virtuales para Windows, el paquete Snap, el instalador web y los scripts de instalación. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/installation/source_installation.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

Hay varias formas de instalar Nextcloud según las preferencias, los requisitos y los objetivos.

Si se prefiere una instalación automatizada, existe la opción de:

- usar el [método de instalación oficial de Nextcloud](https://github.com/nextcloud/all-in-one#nextcloud-all-in-one). Nextcloud AIO ofrece un despliegue y un mantenimiento sencillos, con la mayoría de las funciones incluidas en esta única instancia de Nextcloud. Incluye Office, una solución de copias de seguridad llave en mano, Imaginary (para vistas previas de heic, heif, illustrator, pdf, svg, tiff y webp) y más.
- usar el [paquete Snap de la comunidad](https://snapcraft.io/nextcloud). Incluye una pila completa lista para producción, se encarga de mantener los certificados HTTPS y se actualiza automáticamente según sea necesario para seguir siendo seguro.
- usar el [appliance de VM de Nextcloud de la comunidad](https://github.com/nextcloud/vm/) (también conocido como Nextcloud Virtual Machine o NcVM). Ayuda a crear un Nextcloud Server personal o corporativo de forma más rápida y sencilla. Puede usarse para instalar directamente sobre un Ubuntu Server limpio o descargarse como una VM totalmente funcional.
- usar los [scripts de NextcloudPi de la comunidad](https://nextcloudpi.com/) (basados en Debian). Lo configuran todo e incluyen scripts para la instalación automatizada de apps como Collabora, OnlyOffice, Talk, etc.
- usar la [imagen de Docker de Nextcloud de la comunidad](https://hub.docker.com/_/nextcloud/). Esta imagen está diseñada para usarse en un entorno de microservicios. Hay dos versiones de la imagen entre las que elegir: la de Apache contiene una instalación completa de Nextcloud que incluye un servidor web Apache. La segunda opción es una instalación FPM que ejecuta un proceso FastCGI que sirve la instalación de Nextcloud (hay que aportar el servidor web, la base de datos y los demás servicios complementarios que se prefieran).

:::{note}
Tener en cuenta que las opciones de la comunidad no tienen soporte oficial de Nextcloud GmbH.
:::

:::{tip}
Para una instalación lista para empresas y escalable basada en Helm Charts (también disponible para Podman), [contactar con Nextcloud GmbH](https://nextcloud.com/enterprise/).
:::

Si se prefiere instalar desde el tarball del código fuente, se puede configurar Nextcloud desde cero con una pila LAMP clásica (Linux, Apache, MySQL/MariaDB, PHP). Este documento ofrece un recorrido completo para instalar Nextcloud en Ubuntu 24.04 LTS Server con Apache y MariaDB, usando [el archivo .tar de Nextcloud](https://nextcloud.com/install/). Este método es el recomendado para instalar Nextcloud.

Esta guía de instalación ofrece una visión general de las dependencias necesarias y de su configuración. Para una guía de configuración específica de una distribución, consultar {nc-doc}`admin_manual/installation/example_ubuntu` y {nc-doc}`admin_manual/installation/example_centos`.

(nc-prerequisites_label)=

:::{note}
Los administradores de distribuciones con SELinux activado, como CentOS, Fedora y Red Hat Enterprise Linux, pueden necesitar establecer reglas nuevas para permitir la instalación de Nextcloud. Consultar {nc-ref}`selinux_tips_label` para ver una configuración sugerida.
:::

### Requisitos previos para la instalación manual

El archivo .tar de Nextcloud contiene todos los módulos de PHP necesarios. La distribución de Linux debería tener paquetes para todos los módulos necesarios. Consultar {nc-doc}`admin_manual/installation/php_configuration` para ver una lista de los módulos necesarios y de los sugeridos.

No se necesita el módulo WebDAV para el servidor web (es decir, el `mod_webdav` de Apache), porque Nextcloud tiene su propio servidor WebDAV integrado, SabreDAV. Si `mod_webdav` está activado, hay que desactivarlo para Nextcloud. (Consultar {nc-ref}`apache_configuration_label` para ver una configuración de ejemplo).

(nc-apache_configuration_label)=
### Configuración del servidor web Apache

Configurar Apache requiere crear un único archivo de configuración. En Debian, Ubuntu y sus derivados, este archivo será {file}`/etc/apache2/sites-available/nextcloud.conf`. En Fedora, CentOS, RHEL y sistemas similares, el archivo de configuración será {file}`/etc/httpd/conf.d/nextcloud.conf`.

Se puede elegir instalar Nextcloud en un directorio de un servidor web existente, por ejemplo *<https://www.example.com/nextcloud/>*, o en un host virtual si se quiere que Nextcloud sea accesible desde su propio subdominio, como *<https://cloud.example.com/>*.

Para usar la instalación basada en un directorio, poner lo siguiente en {file}`nextcloud.conf`, sustituyendo las rutas de **Directory** y **Alias** por las rutas adecuadas para el sistema:

```
Alias /nextcloud "/var/www/nextcloud/"

<Directory /var/www/nextcloud/>
  Require all granted
  AllowOverride All
  Options FollowSymLinks MultiViews

  <IfModule mod_dav.c>
    Dav off
  </IfModule>
</Directory>
```

Para usar la instalación con host virtual, poner lo siguiente en {file}`nextcloud.conf`, sustituyendo **ServerName**, así como las rutas de **DocumentRoot** y **Directory**, por los valores adecuados para el sistema:

```
<VirtualHost *:80>
  DocumentRoot /var/www/nextcloud/
  ServerName  your.server.com

  <Directory /var/www/nextcloud/>
    Require all granted
    AllowOverride All
    Options FollowSymLinks MultiViews

    <IfModule mod_dav.c>
      Dav off
    </IfModule>
  </Directory>
</VirtualHost>
```

En Debian, Ubuntu y sus derivados, hay que ejecutar el siguiente comando para activar la configuración:

```
a2ensite nextcloud.conf
```

#### Configuraciones adicionales de Apache

**Módulos necesarios:**

- Para que Nextcloud funcione correctamente, se necesita el módulo `mod_rewrite`. Activarlo ejecutando:

  ```
  a2enmod rewrite
  ```

- Si se usa `mod_fcgi` o `php-fpm` (PHP FastCGI Process Manager), hay que activar los módulos de proxy:

  ```
  a2enmod proxy
  a2enmod proxy_fcgi
  ```

Los **módulos recomendados** son `mod_headers`, `mod_env`, `mod_dir` y `mod_mime`:

```
  a2enmod headers
  a2enmod env
  a2enmod dir
  a2enmod mime

If you're running ``mod_fcgi`` instead of the standard ``mod_php`` also enable::

  a2enmod setenvif

and apply the following modifications to the configuration::

  ProxyFCGIBackendType FPM

  <FilesMatch remote.php>
    SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1
  </FilesMatch>
```

**Verificar que los módulos estén activados:**

Para verificar que los módulos necesarios están activados, usar el comando `apache2ctl`:

```
apache2ctl -M | grep -E "rewrite|proxy|proxy_fcgi"
```

Si aparece una salida coincidente para los módulos activados, estos están activos. Si falta algún módulo necesario, revisar el gestor de paquetes del sistema operativo para asegurarse de que los módulos de Apache estén instalados (los nombres de los paquetes pueden variar según la distribución; por ejemplo, en Debian/Ubuntu, buscar `libapache2-mod-fcgid` o similar).

- Hay que desactivar cualquier autenticación configurada en el servidor para Nextcloud, ya que usa internamente la autenticación Basic para los servicios DAV. Si se activó la autenticación en una carpeta superior (por ejemplo, mediante una directiva `AuthType Basic`), se puede desactivar la autenticación específicamente para la entrada de Nextcloud. Siguiendo el archivo de configuración de ejemplo anterior, añadir la siguiente línea en la sección `<Directory>`:

  ```
  Satisfy Any
  ```

- Al usar SSL, prestar especial atención al ServerName. Debería especificarse uno en la configuración del servidor, así como en el campo CommonName del certificado. Si se quiere que Nextcloud sea accesible a través de internet, establecer ambos en el dominio con el que se quiere llegar al servidor Nextcloud.

- Ahora reiniciar Apache:

  ```
  service apache2 restart
  ```

- Si se ejecuta Nextcloud en un subdirectorio y se quieren usar clientes CalDAV o CardDAV, asegurarse de haber configurado correctamente las URL de {nc-ref}`service-discovery-label`.

(nc-pretty_urls_label)=
### URL amigables

Las URL amigables eliminan la parte `index.php` de todas las URL de Nextcloud, por ejemplo en los enlaces para compartir como `https://example.org/nextcloud/index.php/s/Sv1b7krAUqmF8QQ`, lo que hace las URL más cortas y, por tanto, más bonitas.

`mod_env` y `mod_rewrite` deben estar instalados en el servidor web y el usuario HTTP debe poder escribir en el {file}`.htaccess`. Para activar `mod_env` y `mod_rewrite`, ejecutar `sudo a2enmod env` y `sudo a2enmod rewrite`. Después se pueden establecer en {file}`config.php` dos variables:

```
'overwrite.cli.url' => 'https://example.org/nextcloud',
'htaccess.RewriteBase' => '/nextcloud',
```

si la instalación está disponible en `https://example.org/nextcloud`, o:

```
'overwrite.cli.url' => 'https://example.org/',
'htaccess.RewriteBase' => '/',
```

si no está instalada en una subcarpeta.

:::{note}
`htaccess.RewriteBase` debe coincidir con la ruta, relativa al DocumentRoot de Apache, en la que se sirve Nextcloud en el backend, no con el prefijo de la URL pública. En una configuración directa de Apache, ambos son idénticos. Detrás de un proxy inverso que elimina el prefijo de la URL —por ejemplo, `https://domain.com/nextcloud/` reenviado a `http://localhost:8080/`—, el valor correcto es `/` aunque la URL pública contenga `/nextcloud`.
:::

Por último, ejecutar este comando occ para actualizar el archivo `.htaccess`:

```
sudo -E -u www-data php /var/www/nextcloud/occ maintenance:update:htaccess
```

Después de cada actualización, estos cambios se aplican automáticamente al archivo `.htaccess`.

:::{note}
Si la configuración de `.htaccess` añadida automáticamente, *SetEnv front_controller_active true*, no funciona en el entorno: editar `config/config.php` y añadir `'htaccess.IgnoreFrontController' => true`. Consultar {nc-doc}`admin_manual/configuration_server/config_sample_php_parameters` para ver una descripción detallada.
:::

(nc-enabling_ssl_label)=
### Activar SSL

:::{note}
Se puede usar Nextcloud sobre HTTP simple, pero recomendamos encarecidamente usar SSL/TLS para cifrar todo el tráfico del servidor y proteger en tránsito los inicios de sesión y los datos de los usuarios.
:::

Apache instalado en Ubuntu ya viene configurado con un certificado autofirmado sencillo. Solo hay que activar el módulo ssl y el sitio predeterminado. Abrir una terminal y ejecutar:

```
a2enmod ssl
a2ensite default-ssl
service apache2 reload
```

:::{note}
Los certificados autofirmados tienen sus inconvenientes, sobre todo cuando se piensa hacer que el servidor Nextcloud sea accesible públicamente. Conviene obtener un certificado firmado por una autoridad de firma. Consultar con el registrador del nombre de dominio o con el servicio de alojamiento si tienen buenas ofertas de certificados comerciales. O usar uno gratuito de [Let's Encrypt](https://letsencrypt.org/).
:::

(nc-installation_wizard_label)=
### Asistente de instalación

Después de reiniciar Apache, hay que completar la instalación ejecutando el asistente de instalación gráfico o bien por línea de comandos con el comando `occ`. Para permitirlo, cambiar el propietario de los directorios de Nextcloud al usuario HTTP:

```
chown -R www-data:www-data /var/www/nextcloud/
```

:::{note}
`www-data` es el usuario predeterminado del servidor web en los sistemas Debian/Ubuntu. En RHEL/CentOS/Fedora, usar `apache`. El requisito clave es que el usuario del proceso del servidor web tenga **acceso de lectura y escritura** a todos los directorios de Nextcloud; la propiedad no es estrictamente necesaria. En entornos donde no es posible cambiar el propietario (alojamiento compartido, montajes bind de Docker, etc.), basta con añadir el usuario del servidor web al grupo propietario de los directorios y asegurarse de que el grupo tenga permiso de escritura en ellos, por ejemplo:

```
usermod -a -G vboxsf www-data
```
:::

:::{note}
Los administradores de distribuciones con SELinux activado pueden necesitar escribir reglas nuevas de SELinux para completar la instalación de Nextcloud; consultar {nc-ref}`selinux_tips_label`.
:::

Para usar `occ`, consultar {nc-doc}`admin_manual/installation/command_line_installation`.

Para usar el asistente de instalación gráfico, consultar {nc-doc}`admin_manual/installation/installation_wizard`.

(nc-background_jobs_label)=
### Configurar las tareas en segundo plano

Nextcloud requiere que algunas tareas se ejecuten con regularidad. Pueden ser tareas de mantenimiento para garantizar un rendimiento óptimo o tareas que dependen del momento, como el envío de notificaciones.

Consultar {nc-doc}`admin_manual/configuration_server/background_jobs_configuration` para ver una descripción detallada y sus ventajas.

(nc-selinux_tips_label)=
### Consejos de configuración de SELinux

Consultar {nc-doc}`admin_manual/installation/selinux_configuration` para ver una configuración sugerida para distribuciones con SELinux activado, como Fedora y CentOS.

(nc-php_fpm_tips_label)=
### Configuración de PHP-FPM

#### Descripción general

[PHP-FPM](https://www.php.net/manual/en/install.fpm.php) es una implementación de PHP basada en FastCGI, con funciones útiles para sitios web con mucho tráfico y aplicaciones web grandes. Usarla con Nextcloud es un tema avanzado y requiere familiarizarse con el funcionamiento de PHP-FPM. En la mayoría de los casos, los valores predeterminados no son ideales para usarlos con Nextcloud. Aquí destacamos algunas de las áreas más importantes que conviene ajustar.

#### Gestor de procesos

El valor predeterminado de `pm.max_children` en muchas instalaciones de PHP-FPM es más bajo de lo adecuado. Un valor bajo puede causar problemas de conectividad de los clientes, errores inexplicables y problemas de rendimiento. Es una causa habitual de *Gateway Timeouts*. Sin embargo, un valor demasiado alto en relación con los recursos disponibles (como la memoria) también provocará problemas. El valor predeterminado suele ser `5`. Esto limita mucho las conexiones simultáneas a la instancia de Nextcloud y, salvo que haya restricciones graves de recursos, infrautilizará el hardware. Consultar el capítulo {nc-doc}`admin_manual/installation/server_tuning` para ver orientación y recursos con los que llegar a valores adecuados, así como otros parámetros relacionados.

#### Variables de entorno del sistema

Al usar `php-fpm`, las variables de entorno del sistema como PATH, TMP u otras no se rellenan automáticamente de la misma forma que al usar `php-cli`. Por eso, una llamada de PHP como `getenv('PATH');` puede devolver un resultado vacío. Así que puede ser necesario configurar manualmente las variables de entorno en el archivo ini/de configuración de `php-fpm` correspondiente.

A continuación, algunas rutas raíz de ejemplo para estos archivos ini/de configuración:

| Debian/Ubuntu/Mint | CentOS/Red Hat/Fedora |
|---|---|
| `/etc/php/8.3/fpm/` | `/etc/php-fpm.d/` |

En ambos ejemplos, el archivo ini/de configuración se llama `www.conf` y, según la versión de la distribución o las personalizaciones que se hayan hecho, puede estar en un subdirectorio como `pool.d`.

Normalmente, algunas o todas las variables de entorno ya están en el archivo, pero comentadas, así:

```
;env[HOSTNAME] = $HOSTNAME
;env[PATH] = /usr/local/bin:/usr/bin:/bin
;env[TMP] = /tmp
;env[TMPDIR] = /tmp
;env[TEMP] = /tmp
```

Descomentar las entradas existentes que correspondan. Después, ejecutar `printenv PATH` para confirmar las rutas, por ejemplo:

```
$ printenv PATH
/home/user/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:
/sbin:/bin:/
```

Si alguna de las variables de entorno del sistema no está en el archivo, hay que añadirla.

Como alternativa, es posible usar las variables de entorno del sistema modificando:

```
/etc/php/8.3/fpm/pool.d/www.conf
```

y descomentando la línea:

```
clear_env = no
```

Al usar un alojamiento compartido o un panel de control para gestionar la [Nextcloud VM][Nextcloud VM] o el servidor, es casi seguro que los archivos de configuración estarán en otro lugar, por motivos de seguridad y flexibilidad, así que hay que consultar la documentación correspondiente para conocer las ubicaciones correctas.

Tener en cuenta que es posible crear ajustes distintos para `php-cli` y `php-fpm`, y para distintos dominios y sitios web. La mejor forma de comprobar los ajustes es con {nc-ref}`label-phpinfo`.

#### Tamaño máximo de subida

Si se quiere aumentar el tamaño máximo de subida, también habrá que modificar la configuración de `php-fpm` y aumentar los valores de `upload_max_filesize` y `post_max_size`. Habrá que reiniciar `php-fpm` y el servidor HTTP para que se apliquen estos cambios.

#### .htaccess

Nextcloud incluye su propio archivo `nextcloud/.htaccess`. Como `php-fpm` no puede leer los ajustes de PHP de `.htaccess`, estos ajustes y permisos deben establecerse en el archivo `nextcloud/.user.ini`.

(nc-other_http_servers_label)=
### Otros servidores web

- {nc-doc}`admin_manual/installation/nginx`

(nc-vm_label)=
### Instalación en Windows (máquina virtual)

Si se usa Windows, la forma más sencilla de poner en marcha Nextcloud es usar una máquina virtual (VM). Hay dos opciones:

- **Appliance para empresas/pymes**

Nextcloud GmbH mantiene un appliance gratuito basado en [Univention Corporate Server (UCS)](https://www.univention.com/products/univention-app-center/app-catalog/nextcloud/), con una configuración gráfica sencilla y administración basada en web. Incluye la gestión de usuarios mediante LDAP, puede sustituir una configuración existente de Active Directory y tiene integración opcional con ONLYOFFICE y Collabora Online, con muchas más aplicaciones disponibles para una instalación fácil y rápida.

Puede instalarse en hardware o ejecutarse en una máquina virtual con imágenes de VirtualBox, VMWare (ESX) y KVM.

Descargar el appliance aquí:

- [Univention Corporate Server (UCS)](https://www.univention.com/products/univention-app-center/app-catalog/nextcloud/)

* **Appliance para usuarios domésticos/pymes**

La [Nextcloud VM][Nextcloud VM] la mantiene [T&M Hansson IT](https://www.hanssonit.se/nextcloud-vm/) y se ofrecen varias versiones distintas. Collabora, OnlyOffice, Full Text Search y otras apps pueden instalarse fácilmente con los scripts incluidos, que se pueden elegir ejecutar durante la primera configuración, o bien descargarlos más tarde y ejecutarlos después. Todas las instalaciones automatizadas de apps disponibles actualmente están [en GitHub](https://github.com/nextcloud/vm/blob/main/apps/).

La VM está disponible en distintos tamaños y versiones.

Todas las versiones disponibles están [aquí](https://shop.hanssonit.se/product-category/virtual-machine/nextcloud-vm/).

Para ver las instrucciones completas y las descargas, consultar:

- [Nextcloud VM (GitHub)](https://github.com/nextcloud/vm/)
- [Nextcloud VM (T&M Hansson IT)](https://www.hanssonit.se/nextcloud-vm/)

:::{note}
Se puede instalar la VM en varios sistemas operativos distintos, siempre que el hipervisor pueda montar una VM OVA, VMDK o VHD/VHDX. Si se usa KVM, hay que instalar la VM a partir de los scripts de GitHub. Se pueden seguir las [instrucciones del README](https://github.com/nextcloud/vm#build-your-own-vm-or-install-on-a-vps).
:::

(nc-snaps_label)=
### Instalación mediante paquetes Snap

El snap de Nextcloud es un método de instalación impulsado por la comunidad y está diseñado para ser fácil de instalar y sencillo de mantener. El snap de Nextcloud ideal es una instancia de Nextcloud de tipo «instalar y olvidarse» que funciona en la mayoría de las arquitecturas y se actualiza sola sin necesidad de conocimientos de administración. Combinar Nextcloud con snapd lo convierte en una opción perfecta para IoT o para entornos escalables. [Snapd](https://snapcraft.io/docs) es una tecnología segura y robusta que el equipo del snap de Nextcloud ha adoptado.

Sobre todo, los snaps están diseñados para ser aplicaciones seguras, aisladas y en contenedores, separadas del sistema subyacente y de otras aplicaciones.

Sin embargo, el snap impone sus propias decisiones y hay [requisitos](https://github.com/nextcloud-snap/nextcloud-snap/wiki/Installation-requirements) que cumplir.

- El snap de Nextcloud usa el Apache recomendado.
- El snap de Nextcloud usa el MySQL recomendado.
- El snap de Nextcloud usa el PHP recomendado.

#### Instalación

**En Ubuntu**

- <https://snapcraft.io/nextcloud>
- Instalar Nextcloud `sudo snap install nextcloud`

**Todas las demás distribuciones**
[tener cuidado](https://github.com/nextcloud-snap/nextcloud-snap/wiki/Why-Ubuntu-is-the-only-supported-distro/)

De forma predeterminada se instala la última versión estable del snap de Nextcloud, que se actualiza automáticamente a las siguientes versiones estables, pero también hay [otras versiones disponibles](https://github.com/nextcloud/nextcloud-snap/wiki/Release-strategy) y se tiene control total de las [actualizaciones automáticas](https://github.com/nextcloud-snap/nextcloud-snap/wiki/Managing-automatic-updates).

Después de la instalación, Nextcloud se inicia automáticamente. Suponiendo que el equipo desde el que se accede y el dispositivo en el que se instaló estén en la misma red, se llega a la instalación de Nextcloud visitando `<hostname>.local` o la dirección IP de la instancia en el navegador. Si el nombre de host es `localhost` o `localhost.localdomain`, como en un dispositivo Ubuntu Core, se usará en su lugar `nextcloud.local`.

#### Primer inicio de sesión

Al visitar la instalación de Nextcloud por primera vez, se pide introducir un nombre de usuario y una contraseña de administrador antes de que Nextcloud se inicialice. Esto puede tardar un poco según los recursos y el dispositivo. Después de proporcionar esa información, se inicia sesión y ya se pueden instalar apps, crear usuarios y subir archivos.

#### Cifrado HTTPS

El snap de Nextcloud incluye un servicio para el cifrado HTTPS automatizado y su renovación automatizada mediante Lets Encrypt, o con certificados autofirmados. Ejecutar `nextcloud.enable-https -h` para obtener más información. [Gestionar el cifrado](https://github.com/nextcloud-snap/nextcloud-snap/wiki/Managing-HTTP-encryption-(HTTPS)).

#### Configuración

Aunque las configuraciones predeterminadas de Nextcloud suelen estar bien, puede ser necesario afinar el snap de Nextcloud editando manualmente los archivos de configuración o usando la consola de gestión. [Configurar el snap de Nextcloud](https://github.com/nextcloud-snap/nextcloud-snap/wiki/Configure-Nextcloud-snap).

#### Medios externos

El [confinamiento de snap](https://snapcraft.io/docs/snap-confinement) es una función de seguridad que determina el nivel de acceso que tiene una aplicación a los recursos del sistema, como los archivos, la red, los periféricos y los servicios. Así, el snap de Nextcloud está confinado de forma segura respecto al sistema anfitrión. Salvo que se permita específicamente al snap de Nextcloud acceder a los directorios `/media` o `/mnt` del sistema anfitrión, no se podrá acceder a ningún otro directorio fuera del confinamiento.

Los medios extraíbles o el almacenamiento externo deben montarse en `/media` o en `/mnt` como root, con permisos de root, ¡y conectarse a Snap! [Gestionar los medios externos y el almacenamiento](https://github.com/nextcloud-snap/nextcloud-snap/wiki/Managing-external-media,-shares-and-storage)

La interfaz que da la capacidad de acceder a medios extraíbles no se conecta automáticamente al instalar; para usar almacenamiento externo (o usar de otra forma un dispositivo de `/media` o `/mnt` para los datos), hay que dar permiso al snap para acceder a los medios extraíbles conectando esa interfaz:

`sudo snap connect nextcloud:removable-media`

Hay más documentación, una [wiki](https://github.com/nextcloud-snap/nextcloud-snap/wiki) extensa y [preguntas frecuentes](https://github.com/nextcloud-snap/nextcloud-snap/wiki/FAQ's) en el [GitHub de los desarrolladores](https://github.com/nextcloud-snap/nextcloud-snap).

:::{note}
La [tecnología snapd](http://snapcraft.io/docs/core/) es el núcleo que impulsa los snaps y ofrece una nueva forma de empaquetar, distribuir, actualizar y ejecutar componentes del sistema operativo y aplicaciones en un sistema Linux. Hay más información sobre los snaps en [snapcraft.io](http://snapcraft.io/).
:::

### Instalación mediante el instalador web en un VPS o espacio web

Cuando no se tiene acceso a la línea de comandos, por ejemplo en un alojamiento web o un VMPS, una opción sencilla es usar nuestro instalador web. Este script está en nuestra [página de instalación del servidor, aquí.](https://nextcloud.com/install/#instructions-server)

El script comprueba las dependencias, descarga Nextcloud del servidor oficial y lo descomprime con los permisos correctos y la cuenta de usuario correcta. Por último, se redirige al instalador de Nextcloud. Un breve procedimiento:

1. Obtener el archivo de la página de instalación
2. Subir setup-nextcloud.php al espacio web
3. Abrir en el navegador setup-nextcloud.php del espacio web
4. Seguir las instrucciones y configurar Nextcloud
5. ¡Iniciar sesión en la instancia de Nextcloud recién creada!

:::{note}
que el instalador usa la misma versión de Nextcloud que la disponible para el actualizador integrado en Nextcloud. Después de una versión mayor, puede pasar hasta un mes antes de que esté disponible a través del instalador web y del actualizador. Esto se hace para repartir en el tiempo el despliegue de las nuevas versiones mayores.
:::

### Instalación en TrueNAS

Consultar la [documentación de instalación de TrueNAS](https://www.truenas.com/docs/core/solutions/integrations/nextcloud/).

### Instalación mediante script de instalación

Una de las formas más sencillas de instalar es usar los scripts de Nextcloud VM o de NextcloudPI. Básicamente son solo dos pasos:

1. Descargar el último [script de instalación de la VM](https://github.com/nextcloud/vm/blob/main/nextcloud_install_production.sh/).
2. Ejecutar el script con:

   ```
   sudo bash nextcloud_install_production.sh
   ```

o

1. Descargar el último [script de instalación de PI](https://raw.githubusercontent.com/nextcloud/nextcloudpi/master/install.sh).
2. Ejecutar el script con:

   ```
   sudo bash install.sh
   ```

A continuación, seguirá una configuración guiada y lo único que hay que hacer es seguir las instrucciones en pantalla cuando aparezcan.

[Nextcloud VM]: https://github.com/nextcloud/vm
````
