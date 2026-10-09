---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Módulos de PHP necesarios y recomendados para Nextcloud, conectores de base de datos y ajustes de php.ini para el servidor web y la CLI."
---
# Preparación de PHP

## Resumen

Esta página enumera los módulos de PHP que Nextcloud necesita y los que se recomiendan, los conectores de base de datos y los ajustes de php.ini que conviene revisar para el servidor web y para la línea de comandos. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/installation/php_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

Antes de instalar Nextcloud Server, hay que asegurarse de que el entorno de PHP esté bien configurado. Esto incluye instalar la versión correcta de PHP, activar los módulos de PHP necesarios y ajustar parámetros importantes de *php.ini*. Esta guía explica qué módulos de PHP son necesarios, cuáles se recomiendan para un rendimiento y una compatibilidad óptimos, y cómo configurar el entorno de PHP tanto para el uso con el servidor web como para la línea de comandos.

:::{note}
Este capítulo puede ignorarse sin problema si se piensa usar un método de instalación de Nextcloud Server llave en mano (como AIO, Snap, NCP o Community Docker). Esos métodos de instalación proporcionan entornos de PHP ya preconfigurados para usarse con Nextcloud Server. Para orientación sobre cómo personalizar PHP en esos entornos, consultar la documentación proporcionada específicamente para esos métodos de instalación o por ellos.
:::

### Instalación de PHP

Consultar la documentación de la distribución del sistema operativo para obtener instrucciones sobre cómo establecer una instalación base de PHP. Puede que sea posible elegir entre varias versiones de PHP. Consultar {nc-doc}`admin_manual/installation/system_requirements` para ver qué versiones de PHP admite esta versión de Nextcloud Server. Después de completar una instalación base de PHP, seguir las indicaciones siguientes para configurar la nueva instalación de PHP para el nuevo despliegue de Nextcloud Server.

### Módulos de PHP necesarios

Los siguientes módulos de PHP **deben** estar instalados y activados para que Nextcloud Server funcione:

- *ctype* (incluido con PHP)
- *curl*
- *DOM*
- *fileinfo* (incluido con PHP)
- *filter* (solo en Mageia y FreeBSD)
- *GD*
- *xml* (proporciona SimpleXML, XMLReader y XMLWriter; requiere el paquete de Linux *libxml2* en versión >= 2.7.0)
- *mbstring*
- *OpenSSL* (incluido con PHP)
- *posix*
- *session* (incluido con PHP)
- *zip*
- *zlib*

:::{note}
La extensión «xml» de PHP suele empaquetarse como *php-xml* o mostrarse como *libxml* en los gestores de paquetes del sistema operativo. Esta extensión proporciona los enlaces subyacentes de libxml2 y expone SimpleXML, XMLReader y XMLWriter. Hay que asegurarse de que esté instalado el paquete *php-xml* correspondiente (o el específico de la distribución) para que SimpleXML, XMLReader y XMLWriter estén disponibles para PHP.
:::

Los módulos *ctype*, *fileinfo* y *OpenSSL* suelen venir incluidos y activados en PHP de forma predeterminada. A menudo, los gestores de paquetes de las distribuciones del sistema operativo instalan automáticamente algunos de los otros módulos necesarios.

:::{note}
**Información específica de cada versión de PHP:**

- **PHP 8.3 y 8.4:** Ahora varios módulos vienen incluidos en PHP de forma predeterminada, como *curl*, *zlib* y otros. Al actualizar a estas versiones, puede que algunos módulos que antes eran opcionales ya estén activados. Si aparecen errores «module not found» al ejecutar los comandos habituales de instalación de paquetes, puede que el módulo ya esté incluido y activado: verificarlo con el comando de comprobación de módulos que aparece más abajo.
- **Paquetes de Debian/Ubuntu:** La disponibilidad de los módulos varía según la versión de la distribución. Si un módulo de la lista no se encuentra en el gestor de paquetes, consultar la documentación de PHP o la lista de módulos de PHP de la distribución para confirmar si esa funcionalidad viene incluida en la versión de PHP instalada.
:::

**Cómo comprobar si un módulo está activado:**

- Ejecutar `php -m | grep -i <module_name>`. Si aparece una salida, el módulo está activo.

:::{note}
El módulo *filter* solo es necesario en Mageia y FreeBSD.
:::

### Conectores de base de datos de PHP necesarios

Instalar el módulo conector de PHP para la base de datos que se piensa usar (elegir uno):

- *pdo_sqlite* (>= 3, normalmente no recomendado por motivos de rendimiento)
- *pdo_mysql* (MySQL/MariaDB)
- *pdo_pgsql* (PostgreSQL)

### Módulos de PHP generales recomendados

Estos módulos no son necesarios, pero se recomiendan encarecidamente para mejorar la funcionalidad o la seguridad:

- *intl*: corrige la ordenación de los caracteres no ASCII y mejora el rendimiento de la traducción de idiomas.
- *sodium*: proporciona el hash de contraseñas Argon2 (necesario si se usa PHP < 8.4 y PHP se compiló sin *libargon2*). A partir de PHP 8.0, *sodium* suele estar activado de forma predeterminada. En PHP 8.4, *sodium* suele venir incluido.

  Si Argon2 no está disponible se usará bcrypt, pero si el hash de las contraseñas se generó antes con Argon2 (por ejemplo, al migrar una instalación existente de Nextcloud Server a un nuevo entorno de servidor) y falta este módulo, las cuentas no podrán iniciar sesión).
- *sysvsem*: activa los semáforos de System V que Nextcloud usa para coordinar la generación de vistas previas entre procesos de PHP. Recomendado; si falta, las vistas previas siguen funcionando, pero pueden ser menos fiables con carga alta.

### Módulos de caché de PHP recomendados

La caché de memoria no es obligatoria, así que estos módulos no son necesarios, pero se recomiendan encarecidamente para un rendimiento y una fiabilidad óptimos. Elegir e instalar la combinación preferida de módulos de caché de memoria:

- *APCu* (>= 4.0.6)
- *redis* / *phpredis* (>= 2.2.6, necesario para el bloqueo transaccional de archivos)
- *memcached* (una alternativa más antigua a *redis* que no se recomienda para instalaciones nuevas)

:::{note}
La caché de memoria se recomienda encarecidamente para un rendimiento óptimo. En la mayoría de los casos, una combinación de *APCu* y *redis* es la mejor opción para instalaciones nuevas.
:::

Consultar {nc-doc}`admin_manual/configuration_server/caching_configuration` para los detalles de configuración.

### Módulos de PHP recomendados para la CLI

**Para el procesamiento en línea de comandos** (opcional):

- *pcntl*: permite interrumpir comandos (p. ej., mediante `ctrl-c`).

  Asegurarse de que `pcntl_signal` y `pcntl_signal_dispatch` *no* estén desactivadas en *php.ini* mediante la opción `disable_functions`.

**Para el actualizador en línea de comandos** (opcional):

- *phar*: necesario para ejecutar el actualizador con:

  `sudo -E -u www-data php /var/www/nextcloud/updater/updater.phar`

### Módulos de PHP para la gestión de multimedia

**Metadatos y orientación de imágenes** (opcional):

- *exif*: carga de metadatos de imágenes y rotación

**Generación de vistas previas** (opcional):

- *imagick* (para vistas previas de imágenes)
- *avconv* o *ffmpeg* (para vistas previas de vídeo)
- OpenOffice o LibreOffice (para vistas previas de documentos)

:::{note}
Si la vista previa de archivos PDF falla con un error «not authorized», puede que haya que ajustar el archivo de políticas de *imagick*. Consultar <https://cromwell-intl.com/open-source/pdf-not-authorized.html>
:::

Consultar {nc-doc}`admin_manual/configuration_files/previews_configuration` para más contexto sobre la generación de vistas previas.

### Módulos de PHP para aplicaciones específicas

Algunas apps o funciones opcionales de Nextcloud requieren módulos adicionales. Instalarlos según sea necesario:

- *ldap*: integración con LDAP
- *smbclient*: integración con SMB/CIFS (consultar {nc-doc}`admin_manual/configuration_files/external_storage/smb`)
- *ftp*: almacenamiento FTP o autenticación de usuarios externa
- *imap*: autenticación de usuarios externa

**Recomendados/opcionales:**

- *gmp*: almacenamiento SFTP

### Ajustes *ini* de PHP

Ajustar los siguientes parámetros de *php.ini* según lo necesite Nextcloud:

- `disable_functions`: evitar desactivar funciones salvo que sea necesario.
- `max_execution_time`: consultar {nc-doc}`admin_manual/configuration_files/big_file_upload_configuration`
- `memory_limit`: debería ser de al menos 512MB. Consultar también {nc-doc}`admin_manual/configuration_files/big_file_upload_configuration`
- `opcache.enable` y los ajustes relacionados: consultar {nc-doc}`admin_manual/configuration_server/caching_configuration` y {nc-doc}`admin_manual/installation/server_tuning`
- `open_basedir`: consultar {nc-doc}`admin_manual/installation/harden_server`
- `upload_tmp_dir`: consultar {nc-doc}`admin_manual/configuration_files/big_file_upload_configuration`

### Notas sobre la configuración *ini* de PHP

- **Varios archivos php.ini:**

  - Puede ser necesario configurar los ajustes en más de un archivo *php.ini* (p. ej., para el servidor web y para la CLI).

    - Servidor web: */etc/php/\<version\>/apache2/php.ini* o */etc/php/\<version\>/fpm/php.ini*

    - CLI (la usan las tareas CRON de Nextcloud): */etc/php/\<version\>/cli/php.ini*

- **Averiguar qué php.ini está activo para cada SAPI:**

  - Usar `php --ini` para la CLI, o revisar `phpinfo()` en una página web.

- **Buscar un parámetro:**

  - Ejecutar `grep -r <parameter_name> /etc/php` (p. ej., `grep -r date.timezone /etc/php`)

- **Sustituir *\<version\>* por la versión de PHP realmente instalada (p. ej., 8.1, 8.2, etc.).**

### Tabla de referencia rápida de módulos de PHP

| Módulo | Necesario | Recomendado | Para una app específica | Descripción |
|---|---|---|---|---|
| ctype | ✓ | | | Funcionalidad básica |
| curl | ✓ | | | Solicitudes HTTP |
| DOM | ✓ | | | Document Object Model (manejo de XML/HTML) |
| fileinfo | ✓ | | | Detección del tipo de archivo |
| filter\* | ✓\* | | | Filtrado y validación de datos (Mageia/FreeBSD) |
| GD | ✓ | | | Procesamiento de imágenes |
| xml | ✓ | | | Análisis de XML (libxml2 >= 2.7.0): proporciona la extensión «xml» de PHP, que expone SimpleXML, XMLReader y XMLWriter |
| mbstring | ✓ | | | Manejo de caracteres multibyte |
| OpenSSL | ✓ | | | Comunicaciones seguras |
| posix | ✓ | | | Funciones POSIX |
| session | ✓ | | | Soporte de sesiones |
| zip | ✓ | | | Manejo de archivos zip |
| zlib | ✓ | | | Compresión y descompresión |
| intl | | ✓ | | Mejora las traducciones y la ordenación |
| sodium | | ✓ | | Hash de contraseñas Argon2 |
| sysvsem | | ✓ | | Soporte de semáforos de System V, que se usa para coordinar la generación de vistas previas entre procesos de PHP. |
| ldap | | | ✓ | Integración con LDAP |
| smbclient | | | ✓ | Integración con SMB/CIFS |
| ftp | | | ✓ | Almacenamiento/autenticación FTP |
| imap | | | ✓ | Autenticación de usuarios externa |
| gmp | | | ✓ (opcional) | Almacenamiento SFTP |
| exif | | | ✓ (opcional) | Rotación de imágenes en la app de imágenes |
| apcu | | ✓ | | Caché para el rendimiento |
| memcached | | ✓ | | Caché para el rendimiento |
| redis | | ✓ | | Bloqueo transaccional de archivos |
| imagick | | | ✓ (opcional) | Vistas previas de imágenes |
| avconv/ffmpeg | | | ✓ (opcional) | Vistas previas de vídeo |
| Open/LibreOffice | | | ✓ (opcional) | Vistas previas de documentos |
| pcntl | | | ✓ (opcional) | Interrupción de comandos en la CLI |
| phar | | | ✓ (opcional) | Necesario para el actualizador en línea de comandos |

\*El módulo filter solo es necesario en Mageia y FreeBSD.

### Más recursos

- Para más detalles sobre cada módulo, consultar la [documentación oficial de PHP](https://php.net/manual/en/extensions.php).
- Consultar la documentación de la distribución del sistema operativo para conocer los detalles de la instalación de módulos de PHP en ese entorno.
- Las palabras *extensión* y *módulo* son intercambiables en PHP. En nuestra documentación usamos la palabra *módulos*.
- Reiniciar siempre el servidor web y PHP-FPM después de hacer cambios en un archivo *php.ini* o en los módulos instalados.
````
