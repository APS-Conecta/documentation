---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "El asistente de instalación web: cuenta de administración, directorio de datos, elección de base de datos, autoconfiguración y dominios de confianza."
---
# Asistente de instalación

## Resumen

Esta página recorre el asistente de instalación web: los tres pasos básicos, la ubicación del directorio de datos, la elección y los campos de la base de datos, la creación automática de su usuario, la autoconfiguración y los dominios de confianza. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/installation/installation_wizard.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

### Inicio rápido

Cuando se cumplen los requisitos previos de Nextcloud y todos los archivos de Nextcloud están instalados, el último paso para completar la instalación es ejecutar el asistente de instalación. Son solo tres pasos:

1. Abrir en el navegador web `http://localhost/nextcloud`
2. Introducir el nombre y la contraseña que se quieran para la cuenta de administración.
3. Hacer clic en **Instalar**.

Con esto se ha terminado y ya puede empezar a usarse el nuevo servidor Nextcloud.

:::{note}
El asistente incluye un indicador en tiempo real de la solidez de la contraseña, que califica la contraseña elegida desde «muy débil» hasta «extremadamente fuerte». Por seguridad, elegir una contraseña calificada al menos como «fuerte».
:::

Por supuesto, se puede hacer mucho más para configurar el servidor Nextcloud con el mejor rendimiento y la mejor seguridad. En las secciones siguientes se tratan pasos importantes de la instalación y posteriores a ella.

- {nc-ref}`Ubicación del directorio de datos <data_directory_location_label>`
- {nc-ref}`Elección de la base de datos <database_choice_label>`
- {nc-ref}`Dominios de confianza <trusted_domains_label>`

(nc-data_directory_location_label)=
### Ubicación del directorio de datos

Desplegar la sección **Almacenamiento y base de datos** para ver opciones adicionales de configuración de la instalación para el directorio de datos y la base de datos de Nextcloud.

Conviene ubicar el directorio de datos de Nextcloud fuera del Web root si se usa un servidor HTTP distinto de Apache; también puede quererse guardar los datos de Nextcloud en otra ubicación por otros motivos (p. ej., en un servidor de almacenamiento). Lo mejor es configurar la ubicación del directorio de datos durante la instalación, ya que después es difícil moverlo. Puede ponerse en cualquier lugar; en este ejemplo está en `/opt/nextcloud/`. Este directorio debe existir de antemano y su propietario debe ser el usuario HTTP.

:::{note}
Si el asistente detecta que el archivo `.htaccess` no funciona (por ejemplo, porque se usa Nginx u otro servidor web que no es Apache), muestra una **Advertencia de seguridad** que indica que el directorio de datos y los archivos podrían ser accesibles desde internet. Consultar la documentación {nc-doc}`admin_manual/installation/harden_server` para ver cómo proteger el directorio de datos.
:::

(nc-database_choice_label)=
### Elección de la base de datos

SQLite es la base de datos predeterminada de Nextcloud Server. Cuando se selecciona SQLite, el asistente muestra una **Advertencia de rendimiento**:

> *SQLite solo debería usarse para instancias mínimas y de desarrollo. Para producción recomendamos un motor de bases de datos diferente. Si usas clientes para sincronizar archivos, el uso del SQLite está muy desaconsejado.*

Las bases de datos admitidas son MySQL, MariaDB, Oracle y PostgreSQL, y recomendamos {nc-doc}`MySQL/MariaDB <admin_manual/installation/system_requirements>`. La base de datos y los conectores de PHP deben estar instalados antes de ejecutar el asistente de instalación. Al instalar Nextcloud desde paquetes se satisfacen todas las dependencias necesarias (ver {nc-doc}`admin_manual/installation/source_installation` para una lista detallada de los módulos de PHP necesarios y opcionales). Si solo hay un controlador de base de datos disponible, el asistente muestra un aviso y un enlace a la documentación sobre cómo instalar módulos de PHP adicionales.

Al seleccionar una base de datos distinta de SQLite, el asistente muestra campos adicionales:

- **Usuario de la base de datos**: el nombre de usuario para conectarse al servidor de base de datos. Si este usuario tiene privilegios suficientes (p. ej., la capacidad de consultar `mysql.user` en MySQL, o el privilegio `CREATEROLE` en PostgreSQL), el asistente intentará crear un usuario de base de datos dedicado para Nextcloud con privilegios limitados (ver más abajo). Si el usuario no tiene esos privilegios, el asistente recurre sin problemas a usar directamente las credenciales proporcionadas.
- **Contraseña de la base de datos**: la contraseña del usuario de base de datos anterior.
- **Nombre de la base de datos**: el nombre que se quiera para la base de datos de Nextcloud. El asistente la creará si todavía no existe y el usuario tiene privilegios `CREATE DATABASE`.
- **Host de la base de datos**: el nombre de host (y, opcionalmente, el puerto) del servidor de base de datos, p. ej., `localhost` o `db.example.com:3306`. El valor predeterminado es `localhost`. Aquí también puede indicarse la ruta de un socket Unix. El asistente muestra una indicación de ayuda: *«Por favor especifique el numero del puerto junto al nombre del host (p.e., localhost:5432).»*
- **Espacio de tablas de la base de datos** *(solo Oracle)*: solo se muestra cuando se selecciona Oracle.

#### Creación automática del usuario de la base de datos

Cuando el usuario de base de datos proporcionado tiene privilegios de administración, el instalador intenta crear un usuario de base de datos dedicado con privilegios limitados a la base de datos de Nextcloud. Así se evita guardar las credenciales de administración de la base de datos en `config.php`.

Si los privilegios son suficientes, la instalación crea un usuario llamado `oc_admin`. Si ese usuario ya existe, se añade un sufijo numérico (`oc_admin1`, `oc_admin2`, etc.) hasta encontrar un nombre de usuario disponible.

Se genera una contraseña aleatoria para el nuevo usuario. Las credenciales resultantes se escriben en `config.php`:

```
'dbuser' => 'oc_admin',
'dbpassword' => 'pX65Ty5DrHQkYPE5HRsDvyFHlZZHcm',
```

Si el usuario proporcionado no tiene privilegios para crear nuevos usuarios de base de datos, el instalador recurre a usar directamente las credenciales proporcionadas.

:::{tip}
También puede impedirse de forma explícita la creación automática del usuario definiendo lo siguiente en `config.php` antes de ejecutar el asistente (o mediante un archivo de autoconfiguración):

```
'setup_create_db_user' => false,
```

Esto es útil cuando el administrador de la base de datos ya ha creado un usuario dedicado para Nextcloud. En ese caso, el asistente usará directamente las credenciales de base de datos proporcionadas, sin intentar crear un nuevo usuario ni consultar privilegios de administración.
:::

#### Autoconfiguración

Si se detecta un archivo de autoconfiguración, el asistente muestra un aviso de éxito: *«Se ha detectado un archivo de autoconfiguración — El formulario de instalación a continuación ha sido pre-cargado con los valores desde el archivo de configuración.»* La sección **Almacenamiento y base de datos** se pliega automáticamente cuando la autoconfiguración aporta valores válidos. Para más detalles sobre los archivos de autoconfiguración, ver {nc-doc}`admin_manual/installation/automatic_configuration`.

#### Completar la instalación

Hacer clic en **Instalar** y empezar a usar el nuevo servidor Nextcloud.

Ahora se revisan algunos pasos importantes posteriores a la instalación.

(nc-trusted_domains_label)=
### Dominios de confianza

Todas las URL que se usan para acceder al servidor Nextcloud deben estar en la lista blanca del archivo `config.php`, en el ajuste `trusted_domains`. Los usuarios solo pueden iniciar sesión en Nextcloud cuando abren en el navegador una URL que figura en el ajuste `trusted_domains`. No es una lista de dominios ni de direcciones IP permitidos del lado del cliente. Pueden usarse direcciones IP y nombres de dominio. También se admiten patrones con comodín mediante `*` (p. ej., `*.example.com`). Una configuración típica tiene este aspecto:

```
'trusted_domains' =>
  array (
   0 => 'localhost',
   1 => 'server1.example.com',
   2 => '192.168.1.50',
   3 => '[fe80::1:50]',
),
```

:::{note}
Las direcciones de loopback `localhost`, `127.0.0.1` y `[::1]` siempre se consideran de confianza, independientemente de la configuración de `trusted_domains`. Esto significa que, mientras se tenga acceso al servidor físico, siempre se podrá iniciar sesión. Si hay un balanceador de carga o un proxy inverso, no habrá problemas siempre que envíe la cabecera `X-Forwarded-Host` correcta.
:::

Cuando un usuario prueba una URL que no está en la lista blanca, aparece el siguiente error. La pantalla muestra el mensaje de error de una URL que no está en la lista blanca.
````
