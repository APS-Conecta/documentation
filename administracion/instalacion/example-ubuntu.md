---
tipo: tutorial
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Recorrido de instalación en Ubuntu 24.04 LTS con Apache y MariaDB: paquetes .deb, base de datos, descarga verificada y copia al document root."
---
# Ejemplo de instalación en Ubuntu 24.04 LTS

## Resumen

Este tutorial recorre una instalación típica sobre Ubuntu 24.04 LTS con Apache y MariaDB: los paquetes .deb, la creación de la base de datos y su usuario, la descarga y verificación del archivo, y su copia al document root. Está dirigido a quienes administran el servidor.

````{upstream} admin_manual/installation/example_ubuntu.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

Pueden usarse paquetes .deb para instalar los módulos necesarios y recomendados de una instalación típica de Nextcloud, con Apache y MariaDB, ejecutando los siguientes comandos en una terminal:

```
sudo apt update && sudo apt upgrade
sudo apt install apache2 mariadb-server libapache2-mod-php php-gd php-mysql \
php-curl php-mbstring php-intl php-gmp php-xml php-imagick php-zip
```

- Esto instala los paquetes del sistema central de Nextcloud. Si se piensa ejecutar apps adicionales, tener en cuenta que podrían necesitar paquetes adicionales. Ver {nc-ref}`Requisitos previos para la instalación manual <prerequisites_label>` para más detalles.

Ahora hay que crear un usuario de base de datos y la propia base de datos con la interfaz de línea de comandos de MySQL. Nextcloud creará las tablas de la base de datos cuando se inicie sesión por primera vez.

Para iniciar el modo de línea de comandos de MySQL, usar el siguiente comando:

```
sudo mysql
```

Aparecerá entonces un prompt **MariaDB [root]>**. Ahora, introducir las siguientes líneas, reemplazando `username` y `password` por los valores adecuados, y confirmarlas con la tecla Intro:

```
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE IF NOT EXISTS nextcloud CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
GRANT ALL PRIVILEGES ON nextcloud.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
```

Para salir del prompt, introducir:

```
quit;
```

Ahora, descargar el archivo comprimido de la última versión de Nextcloud:

- Ir a la [página de instalación de Nextcloud](https://nextcloud.com/install).
- Ir a **Download Server > Community Projects** y descargar el archivo tar.bz2 o el .zip.
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

- Ahora puede extraerse el contenido del archivo. Ejecutar el comando de descompresión que corresponda al tipo de archivo:

  ```
  tar -xjvf nextcloud-x.y.z.tar.bz2
  unzip nextcloud-x.y.z.zip
  ```

- Esto se descomprime en un único directorio `nextcloud`. Copiar el directorio de Nextcloud a su destino final. Si se usa el servidor HTTP Apache, puede instalarse Nextcloud sin riesgo en el document root de Apache:

  ```
  sudo cp -r nextcloud /var/www
  ```

- Por último, cambiar el propietario de los directorios de Nextcloud al usuario HTTP:

  ```
  sudo chown -R www-data:www-data /var/www/nextcloud
  ```

En otros servidores HTTP se recomienda instalar Nextcloud fuera del document root.

### Próximos pasos

Después de instalar los requisitos previos y extraer el directorio nextcloud, conviene seguir las instrucciones de configuración de Apache en {nc-ref}`apache_configuration_label`. Una vez instalado Apache, puede seguirse opcionalmente la guía {nc-doc}`admin_manual/installation/source_installation` desde {nc-ref}`pretty_urls_label` hasta {nc-ref}`other_HTTP_servers_label`
````
