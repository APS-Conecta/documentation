---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Referencia de config/config.php: carga, formato, archivos combinados, variables de entorno y todos los parámetros admitidos con sus valores predeterminados."
---
# Parámetros de configuración

## Resumen

Esta página explica cómo funciona el archivo `config/config.php` de Nextcloud (carga, formato, modificación, archivos de configuración combinados y la variable `NEXTCLOUD_CONFIG_DIR`) y documenta todos los parámetros que admite, con sus valores de ejemplo y predeterminados. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_server/config_sample_php_parameters.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Introducción

Nextcloud usa `config/config.php` como archivo de configuración principal. Este archivo controla varios aspectos fundamentales del funcionamiento del servidor. Normalmente se modifica durante el despliegue inicial, al solucionar problemas y al hacer ajustes en la infraestructura circundante.

Es un archivo obligatorio en todos los despliegues de Nextcloud, por lo que es fundamental que los administradores de Nextcloud sepan gestionarlo.

Esta sección del *Manual de administración* documenta cómo ajustar este archivo esencial, ciertas características especiales del directorio `config/` y todos los parámetros admitidos que pueden especificarse en un archivo `config/config.php`.

:::{note}
Aunque `config/config.php` es un archivo obligatorio, muchos ajustes de Nextcloud o de sus apps se gestionan en otros lugares y, por tanto, no se incluyen en él. Estos ajustes suelen gestionarse desde cada app.
:::

### Carga

Los archivos de configuración ubicados en `config/` se analizan automáticamente cuando Nextcloud se inicia. También se comprueba periódicamente si han cambiado (aproximadamente cada dos segundos en un entorno PHP estándar con los ajustes predeterminados de *OPcache*; aproximadamente cada sesenta segundos en muchos métodos de instalación de Nextcloud preempaquetados).

El archivo `config/config.php` puede complementarse con archivos `*.config.php` adicionales colocados en el directorio `config/` (si tienen el nombre y el formato adecuados).

:::{danger}
Hay que tener cuidado al nombrar o crear copias de seguridad del `config/config.php` activo. ¡Si una copia de seguridad está dentro de `config/` y se llama `(ANYTHING).config.php`, se cargará como parte de la configuración en uso y sobrescribirá los valores de `config/config.php`!
:::

:::{tip}
Si los cambios de configuración no parecen surtir efecto, comprobar: (a) la configuración de opcache de PHP; (b) si hay archivos `*.config.php` adicionales en `config/`; (c) la documentación del método o paquete de instalación de Nextcloud; (d) la salida de `occ config:list system`.
:::

### Formato

En resumen, los archivos de `config/` son archivos de texto plano con algunos requisitos de formato especiales para los distintos tipos de parámetros y valores. Esto los hace extensibles y fáciles de manejar para Nextcloud. También facilita que los administradores los consulten con cualquier visor de texto y desde la línea de comandos.

Técnicamente, estos archivos de configuración son archivos PHP que contienen una matriz PHP especial (para Nextcloud) llamada `$CONFIG`. Esta matriz consta de varios pares «clave-valor» propios de Nextcloud (que en algunos casos son a su vez matrices). Cada par tiene la forma `key => value` y se separa con comas.

#### Tipos de valores

Cadenas:

- `"thisIsAnImportantValue"`
- Nota: deben ir entre comillas simples o dobles, es decir, `"string"` o `'string'`.
- Nota: las direcciones IP se consideran cadenas.
- Ejemplos:
  - `'logo_url' => 'https://example.org',`
  - `'versions_retention_obligation' => 'auto, D',`
  - `'logtimezone' => 'Europe/Berlin',`

Booleanos:

- `true` o `false`
- Nota: **no** deben ir entre comillas en el propio archivo de configuración.
- Ejemplos:
  - `'session_keepalive' => true,`
  - `'hide_login_form' => false,`

Numéricos:

- `12`
- Incluye tanto números enteros como de coma flotante.
- Nota: **no** deben ir entre comillas en el propio archivo de configuración.
- Ejemplos:
  - `'loglevel' => 2,`
  - `'session_lifetime' => 60 * 60 * 24,`

Matrices de cualquiera de los tipos anteriores:

- `[ 'value1', 'value2' ]`
- Las matrices pueden incluir todos los tipos de valor (incluidas otras matrices).
- Nota: solo algunos parámetros admiten valores de tipo matriz.
- Ejemplos:
  - `'connectivity_check_domains' => [ 'www.nextcloud.com', 'www.eff.org', ],`
  - `'enabledPreviewProviders' => [ 'OC\Preview\BMP', 'OC\Preview\GIF', 'OC\Preview\JPEG', ],`

:::{tip}
Nextcloud intenta corregir algunos errores de tipo o de formato de los valores, pero no es infalible. Conviene usar el formato correcto (para el tipo de valor en cuestión) para evitar resultados inesperados derivados de conversiones imprevistas de los valores.
:::

### Modificación

Los parámetros pueden modificarse con un editor de texto estándar (es decir, desde la línea de comandos o externamente para después volver a subir el archivo). En la mayoría de los casos también pueden modificarse con los comandos del espacio de nombres `occ config:system:*`.

:::{tip}
Las entradas `key => value` con formato incorrecto (o los valores mal especificados) pueden no generar errores o problemas inmediatos (como errores de análisis o de sintaxis), pero aun así provocar resultados inesperados e indeseados. Para detectar cualquier cosa inesperada, revisar la configuración completamente analizada (por PHP) con el comando `occ config:list system` y/o `occ config:list system --private`.
:::

### Valores predeterminados

Nextcloud crea durante la instalación un archivo `config/config.php` base que contiene los parámetros más esenciales para funcionar. Estos valores son en parte generados automáticamente y en parte extraídos de la información que el administrador proporciona durante la instalación.

El archivo `config/config.sample.php` enumera todos los parámetros de Nextcloud que pueden especificarse en los archivos de `config/`, junto con valores de ejemplo y predeterminados para cada uno. El contenido de ese archivo de configuración de ejemplo se incluye {nc-ref}`más abajo <config-php-sample>` para facilitar su consulta, junto con contexto adicional.

:::{tip}
Añadir a `config/config.php` solo los parámetros que se quieran modificar.
:::

:::{danger}
¡No copiar todo el contenido de `config/config.sample.php` en el propio `config/config.php`! Además de ser innecesario, romperá cosas y puede que incluso obligue a reinstalar.
:::

### Archivos de configuración múltiples o combinados

Nextcloud admite cargar parámetros de configuración desde varios archivos. Pueden añadirse en el directorio `config/` archivos cualesquiera que terminen en `.config.php*` (es decir, `*.config.php`). Los valores de estos archivos tienen prioridad sobre `config/config.php`. Esto permite crear y gestionar fácilmente configuraciones personalizadas, o dividir un archivo de configuración grande y complejo en un conjunto de archivos más pequeños. Nextcloud no sobrescribe estos archivos personalizados.

Por ejemplo, la configuración del servidor de correo puede colocarse en `config/email.config.php`, y los parámetros que se especifiquen en él se combinarán con `config/config.php`.

:::{note}
Los valores de estos archivos de configuración adicionales **siempre** tienen prioridad sobre `config/config.php`.
:::

:::{tip}
Para ver la configuración completa combinada (es decir, incorporando todos los archivos de configuración), usar `occ config:list system` y/o `occ config:list system --private`.
:::

:::{danger}
Hay que tener cuidado al nombrar o crear copias de seguridad del `config/config.php` activo. ¡Si un archivo de configuración de copia de seguridad está dentro de `config/` y resulta llamarse `(ANYTHING).config.php`, se cargará como parte de la configuración en uso y sobrescribirá los valores de `config/config.php`!
:::

### Variables de entorno

La variable de entorno `NEXTCLOUD_CONFIG_DIR` sustituye la ruta predeterminada del directorio de configuración. Cuando está definida, Nextcloud carga `config.php` (y cualquier archivo `*.config.php`) desde esa ruta en lugar de desde el directorio `config/` de la raíz web.

```bash
NEXTCLOUD_CONFIG_DIR=/etc/nextcloud php /var/www/nextcloud/cron.php
```

Esto es útil para:

- Sacar `config.php` de la raíz web como medida de refuerzo: las credenciales no son accesibles por HTTP aunque el listado de directorios esté activado o mal configurado.
- Ejecutar varias instancias de Nextcloud que comparten un único código base pero necesitan directorios de configuración separados.

:::{note}
`NEXTCLOUD_CONFIG_DIR` debe definirse **tanto** para el proceso del servidor web como para cualquier invocación desde la CLI (`occ`, trabajos cron). Definirla en la configuración del host virtual del servidor web y en el entorno de shell que se usa para trabajar en la CLI.
:::

:::{seealso}
{nc-ref}`Colocar el directorio de configuración fuera de la raíz web <harden_config_dir>`, en la guía de refuerzo, para una recomendación de despliegue.
:::

### Ejemplos

Estos son algunos ejemplos del contenido de archivos `config/config.php` típicos inmediatamente después de una instalación básica de Nextcloud.

Cuando se usa SQLite como base de datos de Nextcloud, `config.php` tiene este aspecto después de la instalación. La base de datos SQLite se almacena en el directorio `data/` de Nextcloud:

```
<?php
$CONFIG = array (
  'instanceid' => 'occ6f7365735',
  'passwordsalt' => '2c5778476346786306303',
  'trusted_domains' =>
  array (
    0 => 'localhost',
    1 => 'studio',
  ),
  'datadirectory' => '/var/www/nextcloud/data',
  'dbtype' => 'sqlite3',
  'version' => '7.0.2.1',
  'installed' => true,
);
```

:::{note}
SQLite es una base de datos integrada, sencilla y ligera, adecuada para pruebas e instalaciones sencillas, pero en entornos de producción conviene usar MySQL/MariaDB, Oracle o PostgreSQL.
:::

Este ejemplo es de una instalación nueva de Nextcloud con MariaDB:

```
<?php
$CONFIG = array (
  'instanceid' => 'oc8c0fd71e03',
  'passwordsalt' => '515a13302a6b3950a9d0fdb970191a',
  'trusted_domains' =>
  array (
    0 => 'localhost',
    1 => 'studio',
    2 => '192.168.10.155'
  ),
  'datadirectory' => '/var/www/nextcloud/data',
  'dbtype' => 'mysql',
   'version' => '7.0.2.1',
  'dbname' => 'nextcloud',
  'dbhost' => 'localhost',
  'dbtableprefix' => 'oc_',
  'dbuser' => 'oc_carla',
  'dbpassword' => '67336bcdf7630dd80b2b81a413d07',
  'installed' => true,
);
```

### Parámetros predeterminados

El instalador de Nextcloud configura estos parámetros, que son necesarios para que el servidor Nextcloud funcione.

#### instanceid

```
'instanceid' => '',
```

Es un identificador único de la instalación de Nextcloud, creado automáticamente por el instalador. Este ejemplo solo sirve como documentación y no debe usarse nunca, porque no funcionará. Al instalar Nextcloud se crea un `instanceid` válido.

#### serverid

```
'serverid' => -1,
```

Es un identificador único del servidor.

Es útil cuando la instancia de Nextcloud usa distintos servidores PHP. Una vez establecido, no debe cambiarse.

El valor debe ser un entero comprendido entre 0 y 511.

Cuando config.php se comparte entre distintos servidores, este valor debe sustituirse con «NC_serverid=\<int\>» en cada servidor. Hay que tener en cuenta que debe sustituirse tanto para la CLI como para el servidor web.

Ejemplo para la CLI: NC_serverid=42 occ config:list system

#### passwordsalt

```
'passwordsalt' => '',
```

La sal usada para generar el hash de todas las contraseñas, generada automáticamente por el instalador de Nextcloud. (También hay sales por usuario.) Si se pierde esta sal, se pierden todas las contraseñas. Este ejemplo solo sirve como documentación y no debe usarse nunca.

:::{deprecated} 9.0.0
Esta sal está obsoleta y solo se usa por compatibilidad con versiones anteriores; hoy en día los desarrolladores *NO* deben usar este valor para nada.
:::

#### secret

```
'secret' => '',
```

Secreto que Nextcloud usa con diversos fines, p. ej., para cifrar datos. Si se pierde esta cadena, se corromperán datos.

#### trusted_domains

```
'trusted_domains' => [
        'demo.example.org',
        'otherdomain.example.org',
        '10.111.112.113',
        '[2001:db8::1]'
    ],
```

La lista de dominios de confianza en los que los usuarios pueden iniciar sesión. Especificar dominios de confianza evita el envenenamiento de la cabecera Host. No eliminar este parámetro, ya que realiza comprobaciones de seguridad necesarias.

Puede especificarse:

- El nombre de host exacto del host o del host virtual, p. ej., `demo.example.org`.
- El nombre de host exacto con el puerto permitido, p. ej., `demo.example.org:443`. Esto prohíbe todos los demás puertos de este host
- Usar `*` como comodín; p. ej., `ubos-raspberry-pi*.local` permitirá `ubos-raspberry-pi.local` y `ubos-raspberry-pi-2.local`
- La dirección IP con o sin puerto permitido, p. ej., `[2001:db8::1]:8080`. El uso de certificados TLS con `commonName=<IP address>` está obsoleto

#### cookie_domain

```
'cookie_domain' => '',
```

El dominio de validez de las cookies, por ejemplo `''` (las cookies se enviarán solo al dominio que las definió, p. ej., `'demo.example.org'`), `'demo.example.org'` (las cookies serán válidas para el dominio y todos sus subdominios), ...

Valor predeterminado: `''` (opción segura)

#### datadirectory

```
'datadirectory' => '/var/www/nextcloud/data',
```

Dónde se almacenan los archivos de los usuarios. Si se usa SQLite, aquí también se almacena la base de datos SQLite.

Valor predeterminado: `data/` en el directorio de Nextcloud.

#### version

```
'version' => '',
```

El número de versión actual de la instalación de Nextcloud. Se establece durante la instalación y la actualización, así que no debería ser necesario cambiarlo.

#### dbtype

```
'dbtype' => 'sqlite3',
```

Identifica la base de datos que usa esta instalación. Ver también la opción de configuración `supportedDatabases`

- Disponibles:
  - sqlite3 (SQLite3)
  - mysql (MySQL/MariaDB)
  - pgsql (PostgreSQL)

Valor predeterminado: `sqlite3`

#### dbhost

```
'dbhost' => '',
```

El nombre del servidor host, por ejemplo `localhost`, `hostname`, `hostname.example.com`, o la dirección IP.

Para especificar un puerto, usar `hostname:####`; para direcciones IPv6, usar la notación URI `[ip]:port`. Para especificar un socket Unix, usar `localhost:/path/to/directory/containing/socket` o `:/path/to/directory/containing/socket`, p. ej., `localhost:/run/postgresql/`.

#### dbname

```
'dbname' => 'nextcloud',
```

El nombre de la base de datos de Nextcloud, que se establece durante la instalación. No debería ser necesario cambiarlo.

#### dbuser

```
'dbuser' => '',
```

El usuario con el que Nextcloud escribe en la base de datos. Debe ser único entre las instancias de Nextcloud que usan la misma base de datos SQL. Se establece durante la instalación, así que no debería ser necesario cambiarlo.

#### dbpassword

```
'dbpassword' => '',
```

La contraseña del usuario de la base de datos. Se establece durante la instalación, así que no debería ser necesario cambiarla.

#### dbtableprefix

```
'dbtableprefix' => 'oc_',
```

Prefijo de las tablas de Nextcloud en la base de datos.

Valor predeterminado: `oc_`

#### dbpersistent

```
'dbpersistent' => '',
```

Activa las conexiones persistentes a la base de datos.

Este ajuste usa la opción `persistent` de Doctrine DBAL, que a su vez usa la opción PDO::ATTR_PERSISTENT del controlador PDO.

#### dbreplica

```
'dbreplica' => [
        ['user' => 'nextcloud', 'password' => 'password1', 'host' => 'replica1', 'dbname' => ''],
        ['user' => 'nextcloud', 'password' => 'password2', 'host' => 'replica2', 'dbname' => ''],
    ],
```

Especifica réplicas de solo lectura que Nextcloud usa al consultar la base de datos

#### db.log_request_id

```
'db.log_request_id' => false,
```

Añade el ID de la solicitud a la consulta de la base de datos, en un comentario.

Puede activarse para ayudar a relacionar los registros de la base de datos con los de Nextcloud.

#### installed

```
'installed' => false,
```

Indica si la instancia de Nextcloud se instaló correctamente; `true` indica una instalación correcta y `false`, una instalación fallida.

Valor predeterminado: `false`

(nc-config-php-sample)=
### Experiencia de usuario

Estos parámetros opcionales controlan algunos aspectos de la interfaz de usuario. Se muestran los valores predeterminados, cuando los hay.

#### default_language

```
'default_language' => 'en',
```

Establece el idioma predeterminado del servidor Nextcloud mediante códigos de idioma ISO_639-1, como `en` para inglés, `de` para alemán y `fr` para francés. El parámetro default_language solo se usa cuando el navegador no envía ningún idioma y el usuario no ha configurado sus propias preferencias de idioma.

Nextcloud tiene dos códigos de idioma distintos para el alemán, `de` y `de_DE`. `de` se usa para el alemán informal y `de_DE` para el formal. Si se establece este valor en `de_DE`, puede imponerse la versión formal del alemán, salvo que el usuario haya elegido explícitamente otra cosa.

Valor predeterminado: `en`

#### force_language

```
'force_language' => 'en',
```

Con este ajuste puede imponerse un idioma a todos los usuarios. Si se impone un idioma, los usuarios tampoco pueden cambiarlo en los ajustes personales. Si los usuarios no deben poder cambiar su idioma, pero tienen idiomas distintos, este valor puede establecerse en `true` en lugar de un código de idioma.

Valor predeterminado: `false`

#### default_locale

```
'default_locale' => 'en_US',
```

Establece la configuración regional predeterminada del servidor Nextcloud mediante códigos de idioma ISO_639, como `en` para inglés, `de` para alemán y `fr` para francés, y códigos de país ISO-3166, como `GB`, `US`, `CA`, según se definen en la RFC 5646. Sustituye la detección automática de la configuración regional en las páginas públicas, como el inicio de sesión o los elementos compartidos. Las preferencias de configuración regional que el usuario haya configurado en «Personal -> Región» prevalecen sobre este ajuste una vez que ha iniciado sesión.

Valor predeterminado: `en`

#### reduce_to_languages

```
'reduce_to_languages' => [],
```

Con este ajuste es posible reducir los idiomas disponibles en el selector de idioma. Los idiomas deben indicarse como valores de una matriz con códigos de idioma ISO_639-1, como `en` para inglés, `de` para alemán, etc.

Por ejemplo: establecerlo en `['de', 'fr']` para permitir solo los idiomas alemán y francés.

#### default_phone_region

```
'default_phone_region' => 'GB',
```

Establece la región predeterminada de los números de teléfono del servidor Nextcloud mediante códigos de país ISO 3166-1, como `DE` para Alemania, `FR` para Francia, … Es necesario para poder introducir en los perfiles de usuario números de teléfono que no empiezan por el código de país (p. ej., +49 para Alemania).

¡No tiene valor predeterminado!

#### force_locale

```
'force_locale' => 'en_US',
```

Con este ajuste puede imponerse una configuración regional a todos los usuarios. Si se impone una configuración regional, los usuarios tampoco pueden cambiarla en los ajustes personales. Si los usuarios no deben poder cambiar su configuración regional, pero tienen idiomas distintos, este valor puede establecerse en `true` en lugar de un código de configuración regional.

Valor predeterminado: `false`

#### default_timezone

```
'default_timezone' => 'Europe/Berlin',
```

Establece la zona horaria predeterminada del servidor Nextcloud mediante identificadores IANA como `Europe/Berlin` o `Pacific/Auckland`. El parámetro de zona horaria predeterminada solo se usa cuando no puede determinarse la zona horaria del usuario.

Valor predeterminado: `UTC`

#### knowledgebaseenabled

```
'knowledgebaseenabled' => true,
```

`true` activa la opción Ayuda en el menú de usuario (arriba a la derecha de la interfaz web de Nextcloud).

`false` elimina la opción Ayuda.

#### knowledgebase.embedded

```
'knowledgebase.embedded' => false,
```

`true` incrusta la documentación en un iframe dentro de Nextcloud.

`false` solo muestra botones que llevan a la documentación en línea.

#### allow_user_to_change_display_name

```
'allow_user_to_change_display_name' => true,
```

`true` permite a los usuarios cambiar su nombre mostrado (en sus páginas personales) y `false` les impide cambiarlo.

#### skeletondirectory

```
'skeletondirectory' => '/path/to/nextcloud/core/skeleton',
```

El directorio donde se encuentran los archivos de esqueleto. Estos archivos se copian en el directorio de datos de los usuarios nuevos. Establecer una cadena vacía para no copiar ningún archivo de esqueleto. Si no está definido y templatedirectory es una cadena vacía, se usan las plantillas incluidas para crear un directorio de plantillas para el usuario.

`{lang}` puede usarse como marcador de posición del idioma del usuario. Si el directorio no existe, se recurre a la variante sin dialecto (de `de_DE` a `de`). Si esta tampoco existe, se recurre a `default`

Valor predeterminado: `core/skeleton` en el directorio de Nextcloud.

#### templatedirectory

```
'templatedirectory' => '/path/to/nextcloud/templates',
```

El directorio donde se encuentran los archivos de plantilla. Estos archivos se copian en el directorio de plantillas de los usuarios nuevos. Establecer una cadena vacía para no copiar ningún archivo de plantilla.

`{lang}` puede usarse como marcador de posición del idioma del usuario. Si el directorio no existe, se recurre a la variante sin dialecto (de `de_DE` a `de`). Si esta tampoco existe, se recurre a `default`

Para no crear un directorio de plantillas, establecer tanto skeletondirectory como templatedirectory en cadenas vacías.

### Sesión de usuario

#### remember_login_cookie_lifetime

```
'remember_login_cookie_lifetime' => 60 * 60 * 24 * 15,
```

Duración de la cookie de recordar inicio de sesión. Debe ser mayor que session_lifetime. Si se establece en 0, la opción de recordar la sesión queda desactivada.

Valor predeterminado: `60*60*24*15` segundos (15 días)

#### session_lifetime

```
'session_lifetime' => 60 * 60 * 24,
```

La duración de una sesión tras un periodo de inactividad.

El tiempo máximo posible está limitado por el ajuste `session.gc_maxlifetime` de php.ini, que prevalecería sobre esta opción si es menor que el valor de `config.php`

Valor predeterminado: `60*60*24` segundos (24 horas)

#### davstorage.request_timeout

```
'davstorage.request_timeout' => 30,
```

El tiempo de espera, en segundos, de las solicitudes a servidores que hace el componente DAV (p. ej., necesario para los recursos compartidos federados).

#### carddav_sync_request_timeout

```
'carddav_sync_request_timeout' => 30,
```

El tiempo de espera, en segundos, de la sincronización de libretas de direcciones, p. ej., las libretas de direcciones del sistema federadas (como las que ejecuta `occ federation:sync-addressbooks`).

Valor predeterminado: `30` segundos

#### carddav_sync_request_truncation

```
'carddav_sync_request_truncation' => 2500,
```

El límite que se aplica a la solicitud de informe de sincronización, p. ej., de las libretas de direcciones del sistema federadas (como las que ejecuta `occ federation:sync-addressbooks`).

#### session_relaxed_expiry

```
'session_relaxed_expiry' => false,
```

`true` activa un tiempo de espera de sesión relajado, en el que ya no es Nextcloud quien gestiona la expiración de la sesión, sino la recolección de basura de PHP o la expiración de otros posibles backends de sesión, como Redis.

Esto puede hacer que las sesiones sigan disponibles más tiempo del que indica `session_lifetime`, pero aporta ventajas de rendimiento, ya que las sesiones dejan de ser una operación de bloqueo para las solicitudes concurrentes.

#### session_keepalive

```
'session_keepalive' => true,
```

Activa o desactiva el mantenimiento de la sesión cuando un usuario ha iniciado sesión en la interfaz web.

Al activarlo se envía un «latido» al servidor para evitar que la sesión caduque.

Valor predeterminado: `true`

#### auto_logout

```
'auto_logout' => false,
```

Activa o desactiva el cierre de sesión automático tras session_lifetime, aunque el mantenimiento de la sesión esté activado. Esto garantiza que un navegador inactivo cierre la sesión por sí solo aunque las solicitudes al servidor pudieran prolongar la duración de la sesión.

:::{note}
El cierre de sesión se gestiona en el lado del cliente. No es una forma de limitar la duración de sesiones potencialmente comprometidas.
:::

Valor predeterminado: `false`

#### token_auth_enforced

```
'token_auth_enforced' => false,
```

Impone la autenticación por token a los clientes, lo que bloquea las solicitudes que usan la contraseña del usuario, para mayor seguridad. Los usuarios deben generar en los ajustes personales tokens que pueden usar como contraseñas en sus clientes.

Valor predeterminado: `false`

#### token_auth_activity_update

```
'token_auth_activity_update' => 60,
```

El intervalo con que debe actualizarse la actividad de los tokens.

Aumentar este valor hace que la última actividad que muestra la página de seguridad esté más desactualizada.

Los tokens se siguen comprobando cada 5 minutos para verificar su validez
valor máximo: 300

Valor predeterminado: `60`

#### auth.bruteforce.protection.enabled

```
'auth.bruteforce.protection.enabled' => true,
```

Si debe activarse o no la protección contra fuerza bruta incluida en Nextcloud.

:::{warning}
Desactivarla se desaconseja por motivos de seguridad.
:::

Valor predeterminado: `true`

#### auth.bruteforce.protection.force.database

```
'auth.bruteforce.protection.force.database' => false,
```

Si la protección contra fuerza bruta debe escribir en la base de datos aunque haya una caché de memoria disponible

Usar la base de datos probablemente empeora el rendimiento, pero facilita mucho investigar problemas, ya que permite consultar directamente la tabla para ver todas las direcciones remotas y acciones registradas.

Valor predeterminado: `false`

#### auth.bruteforce.protection.testing

```
'auth.bruteforce.protection.testing' => false,
```

Si la protección contra fuerza bruta incluida en Nextcloud debe ponerse en modo de prueba.

En el modo de prueba, los intentos de fuerza bruta se siguen registrando, pero las solicitudes no se detienen ni esperan el tiempo indicado. Siguen abortándose con «429 Too Many Requests» cuando se alcanza el retraso máximo. Activarlo se desaconseja por motivos de seguridad y solo debe hacerse para depurar y en la CI al ejecutar pruebas.

Valor predeterminado: `false`

#### auth.bruteforce.max-attempts

```
'auth.bruteforce.max-attempts' => 10,
```

Protección contra fuerza bruta: número máximo de intentos antes del bloqueo

Cuando se envían a Nextcloud más solicitudes de inicio de sesión que max-attempts, las solicitudes se abortan con «429 Too Many Requests». Por motivos de seguridad, cambiarlo solo si se sabe lo que se está haciendo.

Valor predeterminado: `10`

#### ratelimit.protection.enabled

```
'ratelimit.protection.enabled' => true,
```

Si debe activarse o no la protección de límite de solicitudes incluida en Nextcloud.

:::{warning}
Desactivarla se desaconseja por motivos de seguridad.
:::

Valor predeterminado: `true`

#### ratelimit_overwrite

```
'ratelimit_overwrite' => [
        'profile.profilepage.index' => [
            'user' => ['limit' => 300, 'period' => 3600],
            'anon' => ['limit' => 1, 'period' => 300],
        ]
    ],
```

Sustituye el límite de solicitudes individual de una ruta concreta

De vez en cuando puede ser necesario ampliar el límite de solicitudes de una ruta concreta, según el patrón de uso o cuando se automatizan acciones con scripts. En lugar de desactivar por completo el límite de solicitudes o de excluir una dirección IP de él, la siguiente configuración permite sustituir la duración y el periodo del límite.

La clave de primer nivel es el nombre de la ruta. El nombre de la ruta de una URL puede obtenerse con el comando `occ router:list` del servidor.

También pueden indicarse límites distintos para los usuarios con sesión iniciada, con la clave `user`, y para los usuarios sin sesión iniciada, con la clave `anon`. Sin embargo, si no hay un límite `user` específico, el límite `anon` se aplica también a los usuarios con sesión iniciada.

Valor predeterminado: matriz vacía `[]`

#### security.ipv6_normalized_subnet_size

```
'security.ipv6_normalized_subnet_size' => 56,
```

Tamaño de la subred usada para normalizar IPv6

Para la protección contra fuerza bruta y el límite de solicitudes, las direcciones IPv6 se truncan según el tamaño de subred. El valor predeterminado es /56, pero puede establecerse entre /32 y /64

Valor predeterminado: `56`

#### auth.webauthn.enabled

```
'auth.webauthn.enabled' => true,
```

De forma predeterminada, WebAuthn está disponible, pero los administradores pueden desactivarlo explícitamente

#### auth.storeCryptedPassword

```
'auth.storeCryptedPassword' => true,
```

Si deben almacenarse contraseñas cifradas en la base de datos

Las contraseñas solo se descifran con el token de inicio de sesión almacenado de forma exclusiva en los clientes y permiten conectarse a almacenamientos externos, configurar automáticamente cuentas de correo en la app de correo y comprobar periódicamente si la contraseña sigue siendo válida.

Puede ser conveniente desactivar esta funcionalidad al usar contraseñas de un solo uso o cuando una política de contraseñas impone contraseñas largas (> 300 caracteres).

De forma predeterminada, las contraseñas se almacenan cifradas en la base de datos.

:::{warning}
Si se desactiva, los cambios de contraseña en el backend de usuarios (p. ej., en LDAP) ya no cierran automáticamente la sesión de los clientes conectados. Los usuarios aún pueden desconectar los clientes eliminando el token de la app desde los ajustes de seguridad.
:::

#### hide_login_form

```
'hide_login_form' => false,
```

De forma predeterminada, el formulario de inicio de sesión siempre está disponible. Hay casos (SSO) en los que un administrador quiere evitar que los usuarios introduzcan sus credenciales en el sistema si la app de SSO no está disponible.

Esto mostrará un error. Pero el inicio de sesión directo sigue funcionando si se añade `?direct=1`

#### lost_password_link

```
'lost_password_link' => 'https://example.org/link/to/password/reset',
```

Si el backend de usuarios no permite restablecer contraseñas (p. ej., cuando es un backend de usuarios de solo lectura como LDAP), puede indicarse un enlace personalizado al que se redirige al usuario cuando hace clic en el enlace «Restablecer contraseña» tras un intento de inicio de sesión fallido.

Si no se quiere ofrecer ningún enlace, sustituir la URL por `'disabled'`

#### logo_url

```
'logo_url' => 'https://example.org',
```

URL que se usa como destino del enlace del logotipo en la cabecera (el logotipo de arriba a la izquierda)

Valor predeterminado: la URL base de la instancia de Nextcloud

### Parámetros de correo

Configuran el correo electrónico para las notificaciones de Nextcloud y los restablecimientos de contraseña.

#### mail_domain

```
'mail_domain' => 'example.com',
```

La dirección de remitente que se quiere que aparezca en los correos que envía el servidor Nextcloud, por ejemplo `nc-admin@example.com`, sustituyendo, por supuesto, el dominio por el propio.

#### mail_from_address

```
'mail_from_address' => 'nextcloud',
```

Dirección FROM que sustituye a las direcciones FROM integradas `sharing-noreply` y `lostpassword-noreply`.

Valor predeterminado: distintas direcciones FROM según la función.

#### mail_smtpdebug

```
'mail_smtpdebug' => false,
```

Activa la depuración de la clase SMTP.

:::{note}
- Probablemente también haya que ajustar `loglevel`. Consultar la documentación: https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/email_configuration.html#enabling-debug-mode
:::

Valor predeterminado: `false`

#### mail_smtpmode

```
'mail_smtpmode' => 'smtp',
```

Qué modo usar para enviar correo: `sendmail`, `smtp`, `qmail` o `null`.

Si se usa SMTP local o remoto, establecerlo en `smtp`.

Para la opción `sendmail` hace falta un sistema de correo instalado y operativo en el servidor, con `/usr/sbin/sendmail` instalado en el sistema Unix.

Para `qmail`, el binario es /var/qmail/bin/sendmail, y debe estar instalado en el sistema Unix.

Usar la cadena `null` para no enviar correos (desactivar el envío de correo). Puede ser útil si los correos deben enviarse mediante API y no es necesario generar los mensajes.

Valor predeterminado: `smtp`

#### mail_smtphost

```
'mail_smtphost' => '127.0.0.1',
```

Depende de `mail_smtpmode`. Indicar la dirección IP del servidor de correo. Puede contener varios hosts separados por punto y coma. Si hay que indicar el número de puerto, añadirlo a la dirección IP separado por dos puntos, así: `127.0.0.1:24`.

Valor predeterminado: `127.0.0.1`

#### mail_smtpport

```
'mail_smtpport' => 25,
```

Depende de `mail_smtpmode`. Indicar el puerto para enviar correo.

Valor predeterminado: `25`

#### mail_smtptimeout

```
'mail_smtptimeout' => 10,
```

Depende de `mail_smtpmode`. Establece el tiempo de espera del servidor SMTP, en segundos. Puede ser necesario aumentarlo si se usa un analizador antimalware o antispam.

Valor predeterminado: `10` segundos

#### mail_smtpsecure

```
'mail_smtpsecure' => '',
```

Depende de `mail_smtpmode`. Indicar `ssl` cuando se usa SSL/TLS. Cualquier otro valor se ignora.

Si el servidor anuncia capacidades STARTTLS, pueden usarse, pero esta opción de configuración no puede imponerlas.

Valor predeterminado: `''` (cadena vacía)

#### mail_smtpauth

```
'mail_smtpauth' => false,
```

Depende de `mail_smtpmode`. Cambiarlo a `true` si el servidor de correo requiere autenticación.

Valor predeterminado: `false`

#### mail_smtpname

```
'mail_smtpname' => '',
```

Depende de `mail_smtpauth`. Indicar el nombre de usuario para autenticarse en el servidor SMTP.

Valor predeterminado: `''` (cadena vacía)

#### mail_smtppassword

```
'mail_smtppassword' => '',
```

Depende de `mail_smtpauth`. Indicar la contraseña para autenticarse en el servidor SMTP.

Valor predeterminado: `''` (cadena vacía)

#### mail_template_class

```
'mail_template_class' => '\OC\Mail\EMailTemplate',
```

Sustituye el diseño predeterminado de la plantilla de correo. Puede usarse si las opciones para modificar los textos de los correos con la app de temas no son suficientes.

La clase debe extender `\OC\Mail\EMailTemplate`

#### mail_send_plaintext_only

```
'mail_send_plaintext_only' => false,
```

De forma predeterminada, los correos se envían con un cuerpo HTML y otro de texto plano. Esta opción permite enviar solo correos de texto plano.

#### mail_smtpstreamoptions

```
'mail_smtpstreamoptions' => [],
```

Depende de `mail_smtpmode`. Matriz de opciones de flujo adicionales que se pasan a la implementación subyacente de Swift mailer.

Valor predeterminado: una matriz vacía.

#### mail_sendmailmode

```
'mail_sendmailmode' => 'smtp',
```

Qué modo se usa para sendmail/qmail: `smtp` o `pipe`.

- Para `smtp`, el binario sendmail se inicia con el parámetro `-bs`:
  - Usar el protocolo SMTP en la entrada y la salida estándar.

- Para `pipe`, el binario se inicia con los parámetros `-t`:
  - Leer el mensaje desde STDIN y extraer los destinatarios.

Valor predeterminado: `smtp`

### Configuraciones de proxy

#### overwritehost

```
'overwritehost' => '',
```

La detección automática del nombre de host de Nextcloud puede fallar en ciertas situaciones de proxy inverso y de CLI/cron. Esta opción permite sustituir manualmente la detección automática; por ejemplo, `www.example.com`, o indicar el puerto, `www.example.com:8080`.

#### overwriteprotocol

```
'overwriteprotocol' => '',
```

Al generar URL, Nextcloud intenta detectar si se accede al servidor por `https` o por `http`. Sin embargo, si Nextcloud está detrás de un proxy y es el proxy el que gestiona las llamadas `https`, Nextcloud no sabría que se está usando `ssl`, y se generarían URL incorrectas.

Los valores válidos son `http` y `https`.

#### overwritewebroot

```
'overwritewebroot' => '',
```

Nextcloud intenta detectar automáticamente la raíz web para generar las URL.

Por ejemplo, si `www.example.com/nextcloud` es la URL que apunta a la instancia de Nextcloud, la raíz web es `/nextcloud`. Cuando se usan proxies, puede resultar difícil para Nextcloud detectar este parámetro, lo que da lugar a URL no válidas.

#### overwritecondaddr

```
'overwritecondaddr' => '',
```

Esta opción permite definir una condición de sustitución manual en forma de expresión regular para la dirección IP remota. Por ejemplo, para definir un rango de direcciones IP que empiezan por `10.0.0.` y terminan en 1 a 3: `^10\.0\.0\.[1-3]$`

Valor predeterminado: `''` (cadena vacía)

#### overwrite.cli.url

```
'overwrite.cli.url' => '',
```

Establece la URL base canónica que Nextcloud debe usar al generar URL fuera de una solicitud web normal, por ejemplo en los trabajos en segundo plano o en la línea de comandos.

El valor debe ser la URL base completa, incluida la raíz web, por ejemplo: `https://www.example.com/nextcloud`

En la mayoría de las instalaciones, debe coincidir con la URL que los usuarios usan normalmente para acceder a Nextcloud. Si es incorrecta, la generación de URL puede fallar en los trabajos cron, en `occ`, en las notificaciones y en contextos similares.

:::{note}
Durante la instalación, Nextcloud inicializa este valor a partir del contexto de acceso que tiene en ese momento el instalador. Si no se configuró previamente (por ejemplo, mediante `autoconfig.php`), el valor deducido puede no coincidir con la URL pública que los usuarios usan normalmente para acceder a Nextcloud y puede que haya que ajustarlo.
:::

Valor predeterminado: `''` (cadena vacía)

#### htaccess.RewriteBase

```
'htaccess.RewriteBase' => '/',
```

Para tener URL limpias sin `/index.php`, hay que configurar este parámetro.

Este parámetro se escribe como «RewriteBase» en el archivo `.htaccess` al actualizar e instalar Nextcloud. Aunque este valor suele ser simplemente la ruta URL de la instalación de Nextcloud, no puede establecerse automáticamente de forma correcta en todos los escenarios, por lo que requiere cierta configuración manual.

En una instalación estándar de Apache, suele coincidir con la carpeta en la que se accede a Nextcloud. Así, si se accede a Nextcloud a través de `https://mycloud.org/nextcloud`, lo más probable es que el valor correcto sea `/nextcloud`. Si Nextcloud se ejecuta en `https://mycloud.org/`, sería `/`.

Hay que tener en cuenta que la regla anterior no vale en todos los casos, ya que hay algunas instalaciones poco habituales en las que puede no aplicarse. No obstante, para evitar problemas de actualización, este valor de configuración debe activarse explícitamente.

Después de establecer este valor, ejecutar `occ maintenance:update:htaccess`. A partir de entonces, cuando se cumplan las siguientes condiciones, las URL de Nextcloud no contendrán `index.php`:

- `mod_rewrite` está instalado
- `mod_env` está instalado

Valor predeterminado: `''` (cadena vacía)

#### htaccess.IgnoreFrontController

```
'htaccess.IgnoreFrontController' => false,
```

En las instalaciones de servidor que no tienen `mod_env` activado o lo tienen restringido (p. ej., suEXEC), este parámetro debe establecerse en true y se supondrá mod_rewrite.

Antes de establecer este parámetro, comprobar que `mod_rewrite` esté activo y funcione, y que se haya actualizado .htaccess con `occ maintenance:update:htaccess`. De lo contrario, puede que la instalación de Nextcloud deje de ser accesible. Por ejemplo, probar a acceder a los recursos omitiendo `index.php` en la URL.

#### proxy

```
'proxy' => '',
```

La URL del servidor proxy, por ejemplo, `proxy.example.com:8081`.

:::{note}
Guzzle (la biblioteca HTTP que usa Nextcloud) lee de forma predeterminada las variables de entorno `HTTP_PROXY` (solo para las solicitudes de la CLI), `HTTPS_PROXY` y `NO_PROXY`.
:::

Si se configura un proxy en Nextcloud, se sobrescribe cualquier configuración predeterminada de Guzzle. Asegurarse de establecer `proxyexclude` en consecuencia si es necesario.

Valor predeterminado: `''` (cadena vacía)

#### proxyuserpwd

```
'proxyuserpwd' => '',
```

La autenticación opcional que el proxy usa para conectarse a internet.

El formato es: `username:password`.

Valor predeterminado: `''` (cadena vacía)

#### proxyexclude

```
'proxyexclude' => [],
```

Lista de nombres de host a los que no debe accederse a través del proxy.

Por ejemplo: `['.mit.edu', 'foo.com']`.

Consejo: usar algo como `explode(',', getenv('NO_PROXY'))` para sincronizar este valor con la opción global `NO_PROXY`.

Valor predeterminado: matriz vacía.

#### allow_local_remote_servers

```
'allow_local_remote_servers' => true,
```

Permite servidores remotos con direcciones locales, p. ej., en recursos compartidos federados, servicios webcal y más

Valor predeterminado: `false`

#### http_client_add_user_agent_url

```
'http_client_add_user_agent_url' => false,
```

Añade la URL del servidor Nextcloud en las cabeceras User-Agent de las llamadas HTTP.

Esto ayuda a los proveedores de servicios a identificar las llamadas procedentes del servidor, lo que puede serles útil, pero puede suponer un problema de privacidad en servidores Nextcloud pequeños.

Valor predeterminado: `false`

### Elementos eliminados (papelera)

Estos parámetros controlan la app Archivos eliminados.

#### trashbin_retention_obligation

```
'trashbin_retention_obligation' => 'auto',
```

Si la app de papelera está activada (opción predeterminada), este ajuste define la política que determina cuándo se eliminan definitivamente los archivos y carpetas de la papelera.

Si se supera el límite de cuota del usuario por los archivos eliminados que hay en la papelera, se ignoran los ajustes de retención y se limpian archivos hasta cumplir los requisitos de la cuota.

La app admite dos ajustes: un tiempo mínimo y un tiempo máximo de retención en la papelera.

El tiempo mínimo es el número de días que se conserva un archivo, tras los cuales *puede* eliminarse. Un archivo puede eliminarse una vez transcurrido el número mínimo de días si se necesita espacio. Si no se necesita espacio, el archivo no se elimina.

Que «se necesite espacio» depende de si hay definida una cuota de usuario o no:

- Si no hay definida una cuota de usuario, el espacio disponible en la partición de datos de Nextcloud fija el límite de la papelera (incidencias: ver https://github.com/nextcloud/server/issues/28451).
- Si hay definida una cuota de usuario, el 50 % del espacio restante de la cuota del usuario fija el límite de la papelera.

El tiempo máximo es el número de días tras los cuales está *garantizado* que se elimine. No depende además del espacio disponible.

Pueden establecerse a la vez el tiempo mínimo y el máximo para definir explícitamente la eliminación de archivos y carpetas. Para facilitar la migración, este ajuste se instala con el valor inicial «auto», que equivale al ajuste predeterminado de Nextcloud.

Valores disponibles (D1 y D2 son números configurables):

- `auto`: Ajuste predeterminado. Conserva los archivos y carpetas en la papelera durante al menos **30** días.\
  Después, **si se necesita espacio**, elimina los archivos de la papelera en cualquier momento a partir de entonces.
- `D1, auto`: Conserva los archivos y carpetas en la papelera durante al menos **D1** días.\
  Después, **si se necesita espacio**, elimina los archivos de la papelera en cualquier momento a partir de entonces.
- `auto, D2`: **Si se necesita espacio**, elimina los archivos de la papelera en cualquier momento.\
  Pasados **D2** días, elimina automáticamente todos los archivos de la papelera
- `D1, D2`: Conserva los archivos y carpetas en la papelera durante al menos **D1** días.\
  Después, pasados **D2** días, elimina automáticamente todos los archivos de la papelera.
- `disabled`: La limpieza automática de la papelera está desactivada; los archivos y carpetas se conservan para siempre.

Valor predeterminado: `auto`

### Versiones de archivos

Estos parámetros controlan la app Versiones.

#### versions_retention_obligation

```
'versions_retention_obligation' => 'auto',
```

Si la app de versiones está activada (opción predeterminada), este ajuste define la política que determina cuándo se eliminan definitivamente las versiones.

La app admite dos ajustes: un tiempo mínimo y un tiempo máximo de retención de versiones. El tiempo mínimo es el número de días que se conserva una versión, tras los cuales puede eliminarse. El tiempo máximo es el número de días tras los cuales está garantizado que se elimine. Pueden establecerse a la vez el tiempo mínimo y el máximo para definir explícitamente la eliminación de versiones. Para facilitar la migración, este ajuste se instala con el valor inicial «auto», que equivale al ajuste predeterminado de Nextcloud.

Valores disponibles:

- `auto`: ajuste predeterminado. Las versiones caducan automáticamente según las reglas de caducidad. Hay más información en {nc-doc}`Controlar las versiones de archivos y su antigüedad <admin_manual/configuration_files/file_versioning>`.
- `D, auto`: conservar las versiones al menos D días y aplicar las reglas de caducidad a todas las versiones con más de D días de antigüedad
- `auto, D`: eliminar automáticamente todas las versiones con más de D días de antigüedad y eliminar las demás versiones según las reglas de caducidad
- `D1, D2`: conservar las versiones al menos D1 días y eliminarlas cuando superen los D2 días
- `disabled`: limpieza automática de versiones desactivada; las versiones se conservan para siempre

Valor predeterminado: `auto`

### Verificaciones de Nextcloud

Nextcloud realiza varias comprobaciones de verificación. Hay dos opciones, `true` y `false`.

#### appcodechecker

```
'appcodechecker' => true,
```

Comprueba antes de instalar una app si usa API privadas en lugar de las API públicas adecuadas. Si se establece en true, solo se permitirá instalar o activar las apps que superen esta comprobación.

Valor predeterminado: `false`

#### updatechecker

```
'updatechecker' => true,
```

Comprueba si Nextcloud está actualizado y muestra una notificación si hay una versión nueva disponible. Envía la versión actual, la versión de PHP, la fecha de instalación y de la última actualización, y el canal de publicación al servidor de actualizaciones, que responde con la última versión disponible según esos datos.

Valor predeterminado: `true`

#### integrity.check.scheduled

```
'integrity.check.scheduled' => true,
```

Vuelve a ejecutar la comprobación de integridad del código una vez al día en un trabajo en segundo plano y avisa a los administradores cuando cambia su resultado, por ejemplo cuando se modifica o se añade un archivo dentro de las carpetas de Nextcloud o de las apps.

Valor predeterminado: `true`

#### updater.server.url

```
'updater.server.url' => 'https://updates.nextcloud.com/updater_server/',
```

URL que Nextcloud debe usar para buscar actualizaciones

Valor predeterminado: `https://updates.nextcloud.com/updater_server/`

#### updater.release.channel

```
'updater.release.channel' => 'stable',
```

El canal que Nextcloud debe usar para buscar actualizaciones

Valores admitidos:

- `daily`
- `beta`
- `stable`

#### has_internet_connection

```
'has_internet_connection' => true,
```

¿Está Nextcloud conectado a internet o funciona en una red cerrada?

Valor predeterminado: `true`

#### connectivity_check_domains

```
'connectivity_check_domains' => [
        'https://www.nextcloud.com',
        'https://www.startpage.com',
        'https://www.eff.org',
        'https://www.edri.org'
    ],
```

Qué dominios consultar para determinar si hay conexión a internet. Si no se puede llegar a ninguno de estos hosts, el panel de administración muestra una advertencia. Establecer una lista vacía para no hacer este tipo de comprobaciones (la advertencia seguirá mostrándose).

Si no se indica ningún protocolo, se prueban tanto http como https. Por ejemplo, para `www.nextcloud.com` se prueban `http://www.nextcloud.com` y `https://www.nextcloud.com`. Si se indica un protocolo, solo se prueba ese.

Valor predeterminado: los siguientes dominios:

- https://www.nextcloud.com
- https://www.startpage.com
- https://www.eff.org
- https://www.edri.org

#### check_for_working_wellknown_setup

```
'check_for_working_wellknown_setup' => true,
```

Permite a Nextcloud verificar que las redirecciones de las URL .well-known funcionan. Para ello intenta hacer una solicitud desde JS a `https://example.tld/.well-known/caldav/`

Valor predeterminado: `true`

#### check_for_working_htaccess

```
'check_for_working_htaccess' => true,
```

Es una comprobación de seguridad crucial en los servidores Apache que siempre debe estar establecida en `true`. Verifica que el archivo `.htaccess` se pueda escribir y funcione.

Si no es así, ninguna de las opciones que controla `.htaccess`, como la subida de archivos grandes, funcionará. También ejecuta comprobaciones en el directorio `data/`, que verifican que no se pueda acceder a él directamente a través del servidor web.

Valor predeterminado: `true`

#### check_data_directory_permissions

```
'check_data_directory_permissions' => true,
```

En instalaciones poco habituales (p. ej., en OpenShift o en Docker sobre Windows), la comprobación de permisos puede bloquear la instalación mientras el sistema subyacente no ofrece forma de «corregir» los permisos. En ese caso, establecer el valor en false.

En los casos normales, si aparecen problemas con los permisos, estos deben ajustarse en consecuencia. Se desaconseja cambiar el indicador.

Valor predeterminado: `true`

#### config_is_read_only

```
'config_is_read_only' => false,
```

En ciertos entornos se quiere que el archivo de configuración sea de solo lectura.

Cuando este interruptor se establece en `true`, se prohíbe escribir en el archivo de configuración. Por tanto, no será posible configurar todas las opciones desde la interfaz web. Además, al actualizar Nextcloud, hay que volver a hacer que el archivo de configuración se pueda escribir y establecer este interruptor en `false` durante el proceso de actualización.

Valor predeterminado: `false`

### Registro

#### log_type

```
'log_type' => 'file',
```

Este parámetro determina adónde se envían los registros de Nextcloud.

- `file`: los registros se escriben en el archivo `nextcloud.log` del directorio de datos predeterminado de Nextcloud. El archivo de registro puede cambiarse con el parámetro `logfile`.
- `syslog`: los registros se envían al registro del sistema. Requiere que haya un demonio syslog activo.
- `errorlog`: los registros se envían a la función `error_log` de PHP.
- `systemd`: los registros se envían al diario de Systemd. Requiere un sistema que ejecute Systemd y el diario de Systemd. La extensión PHP `systemd` debe estar instalada y activa.

Valor predeterminado: `file`

#### log_type_audit

```
'log_type_audit' => 'file',
```

Este parámetro determina adónde se envían los registros de auditoría. Ver `log_type` para más información.

Valor predeterminado: `file`

#### logfile

```
'logfile' => '/var/log/nextcloud.log',
```

Nombre del archivo en el que se escriben los registros de Nextcloud si el parámetro `log_type` está establecido en `file`.

Valor predeterminado: `[datadirectory]/nextcloud.log`

#### logfile_audit

```
'logfile_audit' => '/var/log/audit.log',
```

Nombre del archivo en el que se escriben los registros de auditoría si el parámetro `log_type` está establecido en `file`.

Valor predeterminado: `[datadirectory]/audit.log`

#### logfilemode

```
'logfilemode' => 0640,
```

Modo del archivo de registro para el tipo de registro de Nextcloud, en notación octal.

Valor predeterminado: `0640` (escritura para el usuario, lectura para el grupo).

#### loglevel

```
'loglevel' => 2,
```

Nivel de registro a partir del cual se empieza a registrar. Los valores válidos son:

- `0` = Depuración
- `1` = Información
- `2` = Advertencia
- `3` = Error
- `4` = Fatal.

Valor predeterminado: `2` (Advertencia)

#### loglevel_frontend

```
'loglevel_frontend' => 2,
```

Nivel de registro a partir del cual empieza a registrar el frontend. Pueden usarse los mismos valores que para `loglevel`. Si no está definido, toma el valor configurado en `loglevel` o Advertencia si este tampoco está definido.

Valor predeterminado: `2`

#### loglevel_dirty_database_queries

```
'loglevel_dirty_database_queries' => 0,
```

Nivel de registro que usa la detección de consultas sucias a la base de datos. Útil para identificar posibles errores de la base de datos en producción. Establecerlo en loglevel o superior para ver las consultas sucias en los registros.

Valor predeterminado: `0` (depuración)

#### syslog_tag

```
'syslog_tag' => 'Nextcloud',
```

Si se mantienen distintas instancias y se agregan sus registros, puede convenir distinguirlas. `syslog_tag` puede establecerse por instancia con un ID único. Solo está disponible si `log_type` está establecido en `syslog` o `systemd`.

El valor predeterminado es `Nextcloud`.

#### syslog_tag_audit

```
'syslog_tag_audit' => 'Nextcloud',
```

Si se mantienen distintas instancias y se agregan sus registros, puede convenir distinguirlas. `syslog_tag_audit` puede establecerse por instancia con un ID único. Solo está disponible si `log_type` está establecido en `syslog` o `systemd`.

El valor predeterminado es el valor de `syslog_tag`.

#### log.condition

```
'log.condition' => [
        'shared_secret' => '57b58edb6637fe3059b3595cf9c41b9',
        'users' => ['sample-user'],
        'apps' => ['files'],
        'matches' => [
            [
                'shared_secret' => '57b58edb6637fe3059b3595cf9c41b9',
                'users' => ['sample-user'],
                'apps' => ['files'],
                'loglevel' => 1,
                'message' => 'contains substring'
            ],
        ],
    ],
```

Condición de registro para aumentar el nivel de registro según condiciones. En cuanto se cumple una de estas condiciones, el nivel de registro requerido pasa a depuración. Esto permite depurar solicitudes, usuarios o apps concretos

- Condiciones admitidas:
  - `shared_secret`: si un parámetro de la solicitud con el nombre *log_secret* tiene este valor, la condición se cumple
  - `users`: si la solicitud actual la hace uno de los usuarios indicados, esta condición se cumple
  - `apps`: si el mensaje de registro lo invoca una de las apps indicadas, esta condición se cumple
  - `matches`: si se cumplen todas las condiciones de un grupo, esta condición se cumple. Esto permite registrar solo las entradas de una app de unos pocos usuarios.

Valor predeterminado: una matriz vacía.

#### log.backtrace

```
'log.backtrace' => false,
```

Activa el registro de una traza con cada línea de registro. Normalmente, solo las excepciones llevan información de traza, y se registran automáticamente. Este interruptor la activa para cualquier mensaje de registro. Activar esta opción aumentará el tamaño de los datos de registro.

Valor predeterminado: `false`.

#### logdateformat

```
'logdateformat' => 'F d, Y H:i:s',
```

Usa el formato de PHP.date; ver https://www.php.net/manual/en/function.date.php

Valor predeterminado: ISO 8601 `2005-08-15T15:52:01+00:00`, ver `\DateTime::ATOM` https://www.php.net/manual/en/class.datetimeinterface.php#datetimeinterface.constants.atom

#### logtimezone

```
'logtimezone' => 'Europe/Berlin',
```

La zona horaria de los archivos de registro. Ver https://www.php.net/manual/en/timezones.php

Valor predeterminado: `UTC`

#### log_query

```
'log_query' => false,
```

Añade todas las consultas a la base de datos y sus parámetros al archivo de registro. Usarlo solo para depurar, ya que el archivo de registro se volverá enorme.

#### log_rotate_size

```
'log_rotate_size' => 100 * 1024 * 1024,
```

Activa la rotación de registros y limita el tamaño total de los archivos de registro. Establecerlo en 0 para no rotar. Indicar un tamaño en bytes, por ejemplo, 104857600 (100 megabytes = 100 \* 1024 \* 1024 bytes). Cuando el archivo de registro antiguo alcanza el límite, se crea uno nuevo con otro nombre. Si ya existe un archivo de registro rotado, se sobrescribe.

Valor predeterminado: 100 MB

#### profiler

```
'profiler' => false,
```

Activa el perfilador integrado. Útil para depurar problemas de rendimiento.

Hay que tener en cuenta que afecta al rendimiento y no debe activarse en producción.

#### profiling.request

```
'profiling.request' => false,
```

Activa el perfilado de solicitudes individuales si el perfilado de solicitudes sueltas está activado o se pasa el secreto.

Requiere que la extensión excimer esté instalada. Usarlo con cuidado, ya que puede generar muchos datos.

Los datos de perfilado se almacenan como archivo JSON en el directorio profiling.path y pueden analizarse con speedscope.

Valor predeterminado: `false`

#### profiling.request.rate

```
'profiling.request.rate' => 0.001,
```

La frecuencia con que se recogen datos de perfilado de las solicitudes individuales.

Un valor más bajo supone más puntos de datos, pero una sobrecarga mayor.

Valor predeterminado: `0.001`

#### profiling.secret

```
'profiling.secret' => '',
```

Un token secreto que puede pasarse mediante ?profile_secret=\<secret\> para activar el perfilado de una solicitud concreta.

Esto permite perfilar solicitudes concretas en producción sin activarlo de forma global.

Sin valor predeterminado.

#### profiling.sample

```
'profiling.sample' => false,
```

Activa el perfilado por muestreo. Recoge datos de perfilado periódicamente en lugar de por solicitud.

Requiere que la extensión excimer esté instalada. Usarlo con cuidado, ya que puede generar muchos datos.

Los datos de perfilado se almacenan como archivo de texto plano en el directorio profiling.path y pueden analizarse con speedscope.

Valor predeterminado: `false`

#### profiling.sample.rate

```
'profiling.sample.rate' => 1,
```

La frecuencia, en segundos, con que se recogen los datos del perfilado por muestreo.

Un valor más bajo supone muestras más frecuentes, pero una sobrecarga mayor.

Valor predeterminado: `1`

#### profiling.sample.rotation

```
'profiling.sample.rotation' => 60,
```

Cada cuánto tiempo (en minutos) se rotan los archivos de registro de las muestras.

Valor predeterminado: `60`

#### profiling.path

```
'profiling.path' => '/tmp',
```

El directorio donde se almacenan los datos de perfilado.

Hay que tener en cuenta que el usuario del servidor web debe poder escribir en este directorio y que no se limpia automáticamente.

### Ubicaciones alternativas del código

Parte del código de Nextcloud puede almacenarse en ubicaciones alternativas.

#### customclient_desktop

```
'customclient_desktop'
        => 'https://nextcloud.com/install/#install-clients',
    'customclient_android'
        => 'https://play.google.com/store/apps/details?id=com.nextcloud.client',
    'customclient_ios'
        => 'https://itunes.apple.com/us/app/nextcloud/id1125420102?mt=8',
    'customclient_ios_appid'
        => '1125420102',
    'customclient_fdroid'
        => 'https://f-droid.org/packages/com.nextcloud.client/',
```

Esta sección sirve para configurar los enlaces de descarga de los clientes de Nextcloud que aparecen en el asistente de primera ejecución y en las páginas personales.

Valores predeterminados:

- Cliente de escritorio: `https://nextcloud.com/install/#install-clients`
- Cliente de Android: `https://play.google.com/store/apps/details?id=com.nextcloud.client`
- Cliente de iOS: `https://itunes.apple.com/us/app/nextcloud/id1125420102?mt=8`
- ID de app del cliente de iOS: `1125420102`
- Cliente de F-Droid: `https://f-droid.org/packages/com.nextcloud.client/`

### Actividad

Opciones de la app de actividad.

#### activity_expire_days

```
'activity_expire_days' => 365,
```

Retención de las actividades.

Un trabajo cron diario elimina todas las actividades de todos los usuarios con más antigüedad que el número de días indicado aquí.

Valor predeterminado: `365`

#### activity_use_cached_mountpoints

```
'activity_use_cached_mountpoints' => false,
```

Actividades en carpetas de equipo y almacenamientos externos.

De forma predeterminada, las actividades en carpetas de equipo o almacenamientos externos solo se generan para el usuario actual. Esto se debe a limitaciones de las implementaciones actuales. Este indicador de configuración hace que las actividades en carpetas de grupo y almacenamientos externos funcionen como en los recursos compartidos normales (cuando se establece en `true`). Establecer este indicador no permite mostrar actividades pasadas (no hay retroactividad).

:::{warning}
Activarlo conlleva algunas contrapartidas CRÍTICAS:

- Si se usan los «Permisos avanzados» (ACL) de las carpetas de equipo, las actividades no respetan los permisos y, por tanto, todos los usuarios ven todas las actividades, incluso las de archivos y directorios a los que no tienen acceso.
- Los usuarios que tenían acceso a una carpeta de equipo, un recurso compartido o un almacenamiento externo pueden ver en su flujo y en sus correos las actividades que ocurren después de que se les retire el acceso, hasta que vuelvan a iniciar sesión.
- Los usuarios recién añadidos a una carpeta de equipo, un recurso compartido o un almacenamiento externo no pueden ver en su flujo ni en sus correos las actividades que ocurren después de ser añadidos, hasta que vuelvan a iniciar sesión.
:::

Valor predeterminado: `false`

### Apps

Opciones de la carpeta de apps, la tienda de apps y el verificador de código de las apps.

#### defaultapp

```
'defaultapp' => 'dashboard,files',
```

Establece la app predeterminada que se abre al iniciar sesión. Los ID de las entradas pueden obtenerse del endpoint de la API OCS de navegación: https://docs.nextcloud.com/server/latest/developer_manual/_static/openapi.html#/operations/core-navigation-get-apps-navigation.

Puede usarse una lista de nombres de apps separados por comas, de modo que, si la primera app no está activada para un usuario, Nextcloud prueba con la segunda, y así sucesivamente. Si no se encuentra ninguna app activada, se usa la app Dashboard.

Valor predeterminado: `dashboard,files`

#### appstoreenabled

```
'appstoreenabled' => true,
```

Si está activado, los administradores pueden instalar apps desde la tienda de apps de Nextcloud.

Valor predeterminado: `true`

#### appstoreurl

```
'appstoreurl' => 'https://apps.nextcloud.com/api/v1',
```

Permite instalar apps desde una tienda de apps autoalojada.

Requiere que se pueda escribir en al menos uno de los directorios de apps configurados.

Valor predeterminado: `https://apps.nextcloud.com/api/v1`

#### appsallowlist

```
'appsallowlist' => [],
```

Filtra las apps de la tienda de apps que se permite instalar.

Una matriz vacía impide que se encuentre ninguna app de la tienda.

#### apps_paths

```
'apps_paths' => [
        [
            'path' => '/var/www/nextcloud/apps',
            'url' => '/apps',
            'writable' => true,
        ],
    ],
```

Usar el parámetro `apps_paths` para establecer la ubicación del directorio de apps, en el que se buscan las apps disponibles y en el que se instalan desde la tienda de apps las apps específicas de los usuarios. `path` define la ruta absoluta en el sistema de archivos de la carpeta de apps. La clave `url` define la ruta web HTTP de esa carpeta, a partir de la raíz web de Nextcloud. La clave `writable` indica si un servidor web puede escribir archivos en esa carpeta.

### Vistas previas

Nextcloud admite generar vistas previas de varios tipos de archivo, como imágenes, archivos de audio y archivos de texto. Estas opciones controlan la activación y desactivación de las vistas previas y el tamaño de las miniaturas.

#### enable_previews

```
'enable_previews' => true,
```

De forma predeterminada, Nextcloud puede generar vistas previas de los siguientes tipos de archivo:

- Archivos de imagen
- Documentos de texto

Los valores válidos son `true`, para activar las vistas previas, o `false`, para desactivarlas

Valor predeterminado: `true`

#### preview_concurrency_all

```
'preview_concurrency_all' => 8,
```

Número total de solicitudes de vista previa que se procesan simultáneamente, incluidas las vistas previas que deben generarse de nuevo y las que ya se han generado.

Debe ser mayor que `preview_concurrency_new`. Si no se indica, el valor predeterminado es el doble del valor de `preview_concurrency_new`.

#### preview_concurrency_new

```
'preview_concurrency_new' => 4,
```

Número de vistas previas nuevas que se generan simultáneamente.

Según el tamaño máximo de vista previa fijado por `preview_max_x` y `preview_max_y`, el proceso de generación puede consumir considerables recursos de CPU y memoria. Se recomienda limitarlo a no más del número de núcleos de CPU. Si no se indica, el valor predeterminado es el número de núcleos de CPU, o 4 si no puede determinarse.

#### preview_max_x

```
'preview_max_x' => 4096,
```

La anchura máxima de una vista previa, en píxeles. Un valor `null` significa que no hay límite.

Valor predeterminado: `4096`

#### preview_max_y

```
'preview_max_y' => 4096,
```

La altura máxima de una vista previa, en píxeles. Un valor `null` significa que no hay límite.

Valor predeterminado: `4096`

#### preview_max_filesize_image

```
'preview_max_filesize_image' => 50,
```

Tamaño máximo de archivo para generar vistas previas de imágenes con imagegd (comportamiento predeterminado).

Si la imagen es mayor, se prueban otros generadores de vistas previas, pero lo más probable es que se muestre el icono predeterminado del tipo MIME o que no se muestre la imagen. Establecer `-1` para no tener límite e intentar generar vistas previas de imágenes de cualquier tamaño.

Valor predeterminado: `50` megabytes

#### preview_max_memory

```
'preview_max_memory' => 256,
```

Memoria máxima para generar vistas previas de imágenes con imagegd (comportamiento predeterminado). Lee las dimensiones de la imagen de la cabecera y supone 32 bits por píxel.

Si crear la imagen requiriera más memoria, se desactiva la generación de la vista previa y se muestra el icono predeterminado del tipo MIME. Establecer `-1` para no tener límite.

Valor predeterminado: `256` megabytes

#### preview_libreoffice_path

```
'preview_libreoffice_path' => '/usr/bin/libreoffice',
```

Ruta personalizada del binario de LibreOffice/OpenOffice

Valor predeterminado: `''` (cadena vacía)

#### preview_ffmpeg_path

```
'preview_ffmpeg_path' => '/usr/bin/ffmpeg',
```

Ruta personalizada del binario de ffmpeg

Valor predeterminado: `null`; en ese caso se busca `ffmpeg` en el entorno `PATH` configurado

#### preview_ffprobe_path

```
'preview_ffprobe_path' => '/usr/bin/ffprobe',
```

Ruta personalizada del binario de ffprobe

Valor predeterminado: `null`; en ese caso se usa la misma ruta que ffmpeg. ffprobe suele empaquetarse con ffmpeg y es necesario para la generación mejorada de vistas previas de vídeos HDR.

#### preview_imaginary_url

```
'preview_imaginary_url' => 'http://previews_hpb:8088/',
```

Establece la URL del servicio Imaginary al que se envían las vistas previas de imágenes.

También requiere que el proveedor `OC\Preview\Imaginary` esté activado en la matriz `enabledPreviewProviders` para crear vistas previas de estos tipos MIME: bmp, x-bitmap, png, jpeg, gif, heic, heif, svg+xml, tiff, webp e illustrator.

Si se quiere que Imaginary cree también imágenes de vista previa a partir de documentos PDF, hay que añadir además el proveedor `OC\Preview\ImaginaryPDF`.

Ver https://github.com/h2non/imaginary

#### preview_imaginary_key

```
'preview_imaginary_key' => 'secret',
```

Para establecer una clave de API para Imaginary.

#### enabledPreviewProviders

```
'enabledPreviewProviders' => [
        'OC\Preview\PNG',
        'OC\Preview\JPEG',
        'OC\Preview\GIF',
        'OC\Preview\BMP',
        'OC\Preview\XBitmap',
        'OC\Preview\Krita',
        'OC\Preview\WebP',
        'OC\Preview\MarkDown',
        'OC\Preview\TXT',
        'OC\Preview\OpenDocument',
    ],
```

Solo registrar los proveedores que se hayan activado explícitamente

Los siguientes proveedores están desactivados de forma predeterminada por motivos de rendimiento o de privacidad:

- `OC\Preview\EMF`
- `OC\Preview\Font`
- `OC\Preview\HEIC`
- `OC\Preview\Illustrator`
- `OC\Preview\Movie`
- `OC\Preview\MP3`
- `OC\Preview\MSOffice2003`
- `OC\Preview\MSOffice2007`
- `OC\Preview\MSOfficeDoc`
- `OC\Preview\PDF`
- `OC\Preview\Photoshop`
- `OC\Preview\Postscript`
- `OC\Preview\SGI`
- `OC\Preview\StarOffice`
- `OC\Preview\SVG`
- `OC\Preview\TGA`
- `OC\Preview\TIFF`

Los siguientes proveedores están desactivados de forma predeterminada porque ofrecen una alternativa a los proveedores integrados:

- `OC\Preview\Imaginary`
- `OC\Preview\ImaginaryPDF`

Valor predeterminado: los siguientes proveedores:

- `OC\Preview\PNG`
- `OC\Preview\JPEG`
- `OC\Preview\GIF`
- `OC\Preview\BMP`
- `OC\Preview\XBitmap`
- `OC\Preview\Krita`
- `OC\Preview\WebP`
- `OC\Preview\MarkDown`
- `OC\Preview\TXT`
- `OC\Preview\OpenDocument`

#### metadata_max_filesize

```
'metadata_max_filesize' => 256,
```

Tamaño máximo de archivo para generar metadatos de archivos.

Los archivos que superen este límite se omiten.

Este límite ayuda a acotar el uso de recursos durante la generación de metadatos. El uso real de recursos depende de los proveedores de metadatos activos y de cómo procesan los archivos. Como referencia aproximada, el uso de memoria puede crecer con el tamaño del archivo.

Valor predeterminado: 256 MiB.

#### max_file_conversion_filesize

```
'max_file_conversion_filesize' => 100,
```

Tamaño máximo de archivo para la conversión de archivos.

Los archivos que superen este límite se omiten.

Aumentar este límite puede incrementar el tiempo de conversión, el uso de recursos y el riesgo de tiempos de espera agotados o de fallos de conversión, según el proveedor.

Valor predeterminado: 100 MiB.

### LDAP

Ajustes globales que usa el backend de usuarios y grupos LDAP

#### ldapUserCleanupInterval

```
'ldapUserCleanupInterval' => 51,
```

Define el intervalo, en minutos, del trabajo en segundo plano que comprueba la existencia de los usuarios y los marca como listos para limpiarse. El número siempre son minutos. Establecerlo en 0 desactiva la función.

Ver los métodos de línea de comandos (occ) `ldap:show-remnants` y `user:delete`

Valor predeterminado: `51` minutos

#### sort_groups_by_name

```
'sort_groups_by_name' => false,
```

Ordena los grupos en los ajustes de usuarios por nombre en lugar de por número de usuarios

Al activarlo, también se desactiva el número de usuarios que aparece junto al nombre del grupo.

:::{deprecated} 29.0.0
Usar en su lugar el frontend o establecer el valor de configuración de app `group.sortBy` de `core` en `2`
:::

### Comentarios

Ajustes globales de la infraestructura de comentarios

#### comments.managerFactory

```
'comments.managerFactory' => '\OC\Comments\ManagerFactory',
```

Sustituye la fábrica predeterminada del gestor de comentarios. Puede usarse si se quiere usar un CommentsManager propio o de terceros que, por ejemplo, use el sistema de archivos en lugar de la base de datos para guardar los comentarios.

Valor predeterminado: `\OC\Comments\ManagerFactory`

#### systemtags.managerFactory

```
'systemtags.managerFactory' => '\OC\SystemTag\ManagerFactory',
```

Sustituye la fábrica predeterminada del gestor de etiquetas del sistema. Puede usarse si se quiere usar un SystemTagsManager propio o de terceros que, por ejemplo, use el sistema de archivos en lugar de la base de datos para guardar las etiquetas.

Valor predeterminado: `\OC\SystemTag\ManagerFactory`

### Mantenimiento

Estas opciones sirven para detener la actividad de los usuarios mientras se realiza el mantenimiento del servidor.

#### maintenance

```
'maintenance' => false,
```

Activa el modo de mantenimiento para desactivar Nextcloud

Para impedir que los usuarios inicien sesión en Nextcloud antes de empezar algún trabajo de mantenimiento, hay que establecer el valor del parámetro maintenance en true. Hay que tener en cuenta que los usuarios que ya han iniciado sesión son expulsados de Nextcloud al instante.

Valor predeterminado: `false`

#### maintenance_window_start

```
'maintenance_window_start' => 1,
```

Hora UTC de las ventanas de mantenimiento

Algunos trabajos en segundo plano solo se ejecutan una vez al día. Cuando en este ajuste se define una hora, los trabajos en segundo plano que se declaran no sensibles al tiempo se aplazan durante las horas «laborables» y solo se ejecutan en las 4 horas siguientes a la hora indicada. Esto se usa, p. ej., para la caducidad de la actividad, el entrenamiento de inicios de sesión sospechosos y las comprobaciones de actualizaciones.

Un valor de 1, p. ej., solo ejecutará estos trabajos en segundo plano entre las 01:00 a. m. UTC y las 05:00 a. m. UTC.

Valor predeterminado: `100`, que desactiva la función

#### ldap_log_file

```
'ldap_log_file' => '',
```

Registra todas las solicitudes LDAP en un archivo

Advertencia: esto reduce mucho el rendimiento del servidor y solo está pensado para depurar o perfilar manualmente la interacción con LDAP. Además, puede registrar datos sensibles en un archivo de texto plano.

### SSL

#### openssl

```
'openssl' => [
        'config' => '/absolute/location/of/openssl.cnf',
    ],
```

Opciones SSL adicionales que se usan para la configuración.

Valor predeterminado: una matriz vacía.

### Configuración del backend de caché de memoria

Backends de caché disponibles:

- `\OC\Memcache\APCu` Backend de usuario de APC
- `\OC\Memcache\ArrayCache` Backend en memoria basado en matrices (no recomendado)
- `\OC\Memcache\Memcached` Backend de Memcached
- `\OC\Memcache\Redis` Backend de Redis

Consejos para elegir entre los distintos backends:

- APCu debería ser el más fácil de instalar. Casi todas las distribuciones tienen paquetes. Usarlo en entornos de un solo usuario para todas las cachés.
- Usar Redis o Memcached en entornos distribuidos. Para la caché local (pueden configurarse dos), usar APCu.

#### memcache.local

```
'memcache.local' => '\\OC\\Memcache\\APCu',
```

Backend de caché de memoria para los datos almacenados localmente

- Se usa para datos específicos del host, p. ej., rutas de archivos

Valor predeterminado: `none`

#### memcache.distributed

```
'memcache.distributed' => '\\OC\\Memcache\\Memcached',
```

Backend de caché de memoria para los datos distribuidos

- Se usa para datos específicos de la instalación, p. ej., la caché de la base de datos
- Si no está definido, toma el valor de memcache.local

Valor predeterminado: `none`

#### memcache_customprefix

```
'memcache_customprefix' => 'mycustomprefix',
```

Prefijo de las claves de caché para Redis o Memcached

- Se usa para evitar colisiones en el sistema de caché
- Puede usarse para restricciones de ACL en Redis

Valor predeterminado: `''` (cadena vacía)

#### memcache.kvstore

```
'memcache.kvstore' => [
```

Datos de conexión del almacén clave-valor que se usa para la caché en memoria, por ejemplo al usar Valkey o Redis.

Es la versión independiente de la marca de las opciones `redis` y `redis.cluster` que aparecen más abajo, sin depender de `php-redis`, lo que significa que no hay que instalar ninguna extensión PHP adicional. Se admiten Redis y Valkey de la 4.0 a la 8.0; para la compatibilidad con SSL se requiere Redis v6 o superior; Valkey 9 se admite, pero sin compatibilidad con bases de datos numeradas al usar el modo clúster.

Advertencia: si el servidor de caché no está alojado en la misma máquina que Nextcloud, puede haber una sobrecarga de red en comparación con el backend basado en `php-redis` que aparece más abajo.

Se admiten tres topologías: un único servidor, un conjunto de replicación gestionado por Sentinel y un clúster de servidores. Configurar exactamente uno de `server`, `sentinel` o `seeds`.

Para mayor seguridad, se recomienda configurar ACL en el servidor de caché y configurar `user` y `password` (o un certificado de cliente TLS). Como alternativa, también puede configurarse el servidor de caché para que use solo un `password`. Ver https://valkey.io/topics/security/ para más información al usar Valkey.

#### server

```
'server' => [
            'host' => 'localhost', // can also be a Unix domain socket: '/tmp/cache.sock'
            'port' => 6379, // ignored for Unix domain sockets
            // Protocol used to connect. One of 'tcp', 'tls' or 'unix'.
            // When omitted it is derived from the host (a leading '/' means 'unix').
            'protocol' => 'tcp',
        ],
```

Configuración de un único servidor.

También se usa como plantilla de conexión para las conexiones primaria/réplica gestionadas por `sentinel`.

### Configuración de replicación gestionada por Sentinel.

Indicar el nombre del servicio supervisado y una entrada por cada nodo Sentinel. Cada semilla usa el mismo formato que la entrada `server` anterior. Descomentar para activarlo y eliminar las entradas `server` / `seeds`.

#### user

```
//'seeds' => [
        //    ['host' => 'localhost', 'port' => 7000],
        //    ['host' => 'localhost', 'port' => 7001],
        //],

        // Optional: username, only sent when the cache server uses ACLs.
        'user' => '',
        // Optional: if not defined, no password will be used.
        'password' => '',
        // Optional: select a numbered database. Only supported for single
        // servers and Sentinel setups, clusters always use database 0.
        'dbindex' => 0,
        // Optional: connection timeout in seconds (float). 0 means no timeout.
        'timeout' => 0.0,
        // Optional: read/write timeout in seconds (float). 0 means no timeout.
        'read_timeout' => 0.0,
        // Optional: keep the connection open across requests. Defaults to false.
        'persistent' => false,
        // Optional: when the 'tls' protocol is used, provide the SSL context.
        // SSL context options, see https://www.php.net/manual/en/context.ssl.php
        //'ssl_context' => [
        //    'local_cert' => '/certs/cache.crt',
        //    'local_pk' => '/certs/cache.key',
        //    'cafile' => '/certs/ca.crt',
        //],
    ],
```

Configuración en clúster.

Indicar algunos o todos los nodos del clúster para arrancar el descubrimiento. Cada semilla usa el mismo formato que la entrada `server` anterior. Descomentar para activarlo y eliminar las entradas `server` / `sentinel`.

#### redis

```
'redis' => [
        'host' => 'localhost', // can also be a Unix domain socket: '/tmp/redis.sock'
        'port' => 6379,
        'timeout' => 0.0,
        'read_timeout' => 0.0,
        'user' => '', // Optional: if not defined, no password will be used.
        'password' => '', // Optional: if not defined, no password will be used.
        'dbindex' => 0, // Optional: if undefined, SELECT will not run and will use Redis Server's default DB Index.
        // If Redis in-transit encryption is enabled, provide certificates
        // SSL context https://www.php.net/manual/en/context.ssl.php
        'ssl_context' => [
            'local_cert' => '/certs/redis.crt',
            'local_pk' => '/certs/redis.key',
            'cafile' => '/certs/ca.crt'
        ]
    ],
```

Datos de conexión de Redis para la caché de memoria en una configuración de un único servidor.

Para mayor seguridad, se recomienda configurar Redis para que requiera una contraseña. Ver http://redis.io/topics/security para más información.

También se admite el cifrado SSL/TLS de Redis a partir de la versión 6. Ver https://redis.io/topics/encryption para más información.

#### redis.cluster

```
'redis.cluster' => [
        'seeds' => [ // provide some or all of the cluster servers to bootstrap discovery, port required
            'localhost:7000',
            'localhost:7001',
        ],
        'timeout' => 0.0,
        'read_timeout' => 0.0,
        'failover_mode' => \RedisCluster::FAILOVER_ERROR,
        'user' => '', // Optional: if not defined, no password will be used.
        'password' => '', // Optional: if not defined, no password will be used.
        // If Redis in-transit encryption is enabled, provide certificates
        // SSL context https://www.php.net/manual/en/context.ssl.php
        'ssl_context' => [
            'local_cert' => '/certs/redis.crt',
            'local_pk' => '/certs/redis.key',
            'cafile' => '/certs/ca.crt'
        ]
    ],
```

Datos de conexión de un clúster de Redis.

La compatibilidad con clústeres de Redis requiere el módulo PHP phpredis en la versión 3.0.0 o superior.

- Modos de conmutación por error disponibles:
  - `\RedisCluster::FAILOVER_NONE` - enviar los comandos solo a los nodos maestros (predeterminado)
  - `\RedisCluster::FAILOVER_ERROR` - conmutar a los esclavos para los comandos de lectura si el maestro no está disponible (recomendado)
  - `\RedisCluster::FAILOVER_DISTRIBUTE` - distribuir aleatoriamente los comandos de lectura entre el maestro y los esclavos

:::{warning}
`\RedisCluster::FAILOVER_DISTRIBUTE` es un ajuste no recomendado, y se aconseja encarecidamente no usarlo si se usa Redis para el bloqueo de archivos. Por la forma en que se sincroniza Redis, podría ocurrir que la lectura de un bloqueo existente se asigne a un esclavo que no está totalmente sincronizado con el maestro conectado, lo que provoca una excepción FileLocked.
:::

Ver https://redis.io/topics/cluster-spec para más detalles sobre el clúster de Redis

La autenticación funciona con phpredis 4.2.1 o superior. Ver https://github.com/phpredis/phpredis/commit/c5994f2a42b8a348af92d3acb4edff1328ad8ce1

#### memcached_servers

```
'memcached_servers' => [
        // hostname, port and optional weight
        // or path and port 0 for Unix socket. Also see:
        // https://www.php.net/manual/en/memcached.addservers.php
        // https://www.php.net/manual/en/memcached.addserver.php
        ['localhost', 11211],
        //array('other.host.local', 11211),
    ],
```

Datos de uno o varios servidores Memcached que se usan para la caché de memoria.

#### memcached_options

```
'memcached_options' => [
        // Set timeouts to 50ms
        \Memcached::OPT_CONNECT_TIMEOUT => 50,
        \Memcached::OPT_RETRY_TIMEOUT => 50,
        \Memcached::OPT_SEND_TIMEOUT => 50,
        \Memcached::OPT_RECV_TIMEOUT => 50,
        \Memcached::OPT_POLL_TIMEOUT => 50,

        // Enable compression
        \Memcached::OPT_COMPRESSION => true,

        // Turn on consistent hashing
        \Memcached::OPT_LIBKETAMA_COMPATIBLE => true,

        // Enable Binary Protocol
        \Memcached::OPT_BINARY_PROTOCOL => true,

        // Binary serializer will be enabled if the igbinary PECL module is available
        //\Memcached::OPT_SERIALIZER => \Memcached::SERIALIZER_IGBINARY,
    ],
```

Opciones de conexión de Memcached

#### cache_path

```
'cache_path' => '',
```

Ubicación de la carpeta de caché; el valor predeterminado es `data/$user/cache`, donde `$user` es el usuario actual. Si se indica, el formato pasa a ser `$cache_path/$user`, donde `$cache_path` es el directorio de caché configurado y `$user` es el usuario.

Valor predeterminado: `''` (cadena vacía)

#### cache_chunk_gc_ttl

```
'cache_chunk_gc_ttl' => 60 * 60 * 24,
```

TTL (en segundos) de los fragmentos ubicados en la carpeta de caché antes de que los elimine la recolección de basura. Aumentar este valor si los usuarios tienen problemas para subir archivos muy grandes con el cliente de Nextcloud porque la subida no termina en un día.

Valor predeterminado: `60*60*24` (1 día)

#### cache_app_config

```
'cache_app_config' => true,
```

Activa la caché de los valores de configuración de las apps.

Si está activada, la configuración de las apps se almacena en caché localmente durante un TTL corto, lo que reduce considerablemente la carga de la base de datos en instalaciones grandes.

Valor predeterminado: `true`

### Uso de un almacenamiento de objetos con Nextcloud

#### objectstore

```
'objectstore' => [
        'class' => 'OC\\Files\\ObjectStore\\Swift',
        'arguments' => [
            // trystack will use your Facebook ID as the username
            'username' => 'facebook100000123456789',
            // in the trystack dashboard, go to user -> settings -> API Password to
            // generate a password
            'password' => 'Secr3tPaSSWoRdt7',
            // must already exist in the objectstore, name can be different
            'container' => 'nextcloud',
            // prefix to prepend to the fileid, default is 'oid:urn:'
            'objectPrefix' => 'oid:urn:',
            // create the container if it does not exist. default is false
            'autocreate' => true,
            // required, dev-/trystack defaults to 'RegionOne'
            'region' => 'RegionOne',
            // The Identity / Keystone endpoint
            'url' => 'http://8.21.28.222:5000/v2.0',
            // uploadPartSize: size of the uploaded chunks, defaults to 524288000
            'uploadPartSize' => 524288000,
            // required on dev-/trystack
            'tenantName' => 'facebook100000123456789',
            // dev-/trystack uses swift by default, the lib defaults to 'cloudFiles'
            // if omitted
            'serviceName' => 'swift',
            // The Interface / URL Type, optional
            'urlType' => 'internal',
            // Maximum amount of data that can be uploaded
            'totalSizeLimit' => 1024 * 1024 * 1024,
        ],
    ],
```

Este ejemplo muestra cómo configurar Nextcloud para almacenar todos los archivos en un almacenamiento de objetos Swift.

Es importante tener en cuenta que Nextcloud, en modo de almacenamiento de objetos, espera acceso exclusivo al contenedor del almacenamiento de objetos, porque solo almacena los datos binarios de cada archivo. Los metadatos se guardan actualmente en la base de datos local por motivos de rendimiento.

:::{warning}
La implementación actual es incompatible con cualquier app que use E/S de archivos directa y eluda el sistema de archivos virtual. Eso incluye el cifrado y Gallery. Gallery almacena las miniaturas directamente en el sistema de archivos, y el cifrado provoca una sobrecarga considerable porque hay que obtener los archivos de claves además de cada archivo solicitado.
:::

#### objectstore

```
'objectstore' => [
        'class' => 'OC\\Files\\ObjectStore\\Swift',
        'arguments' => [
            'autocreate' => true,
            'user' => [
                'name' => 'swift',
                'password' => 'swift',
                'domain' => [
                    'name' => 'default',
                ],
            ],
            'scope' => [
                'project' => [
                    'name' => 'service',
                    'domain' => [
                        'name' => 'default',
                    ],
                ],
            ],
            'tenantName' => 'service',
            'serviceName' => 'swift',
            'region' => 'regionOne',
            'url' => 'http://yourswifthost:5000/v3',
            'bucket' => 'nextcloud',
        ],
    ],
```

Para usar Swift V3

#### objectstore

```
'objectstore' => [
        'class' => 'OC\\Files\\ObjectStore\\S3',
        'arguments' => [
            'bucket' => 'nextcloud',
            'key' => 'your-access-key',
            'secret' => 'your-secret-key',
            'hostname' => 's3.example.com',
            'port' => 443,
            'use_ssl' => true,
            'region' => 'us-east-1',
            // optional: Maximum number of retry attempts for failed S3 requests
            // Default: 5
            'retriesMaxAttempts' => 5,
            // Data Integrity Protections for Amazon S3 (https://docs.aws.amazon.com/sdkref/latest/guide/feature-dataintegrity.html)
            // Valid values are "when_required" (default) and "when_supported".
            // To ensure compatibility with 3rd party S3 implementations, Nextcloud disables it by default. However, if you are
            // using Amazon S3 (or any other implementation that supports it) we recommend enabling it by using "when_supported".
            'request_checksum_calculation' => 'when_required',
            'response_checksum_validation' => 'when_required',
        ],
    ],
```

Para usar el almacenamiento de objetos S3

#### objectstore.multibucket.preview-distribution

```
'objectstore.multibucket.preview-distribution' => false,
```

Si se establece en true y hay configurado un almacenamiento de objetos con varios buckets, las vistas previas recién creadas se colocan en 256 buckets dedicados.

Esos buckets se nombran como en la versión con varios buckets, pero con el sufijo `-preview-NUMBER`, donde NUMBER está entre 0 y 255.

Hay que tener en cuenta que allí solo se colocan las vistas previas de archivos que aún no tienen ninguna. En caso contrario, se usa el bucket antiguo.

Para migrar las vistas previas existentes a esta nueva distribución en varios buckets, usar el comando occ `preview:repair`. Por ahora, solo migra las vistas previas que se generaron antes de Nextcloud 19 en la estructura de carpetas plana `appdata_INSTANCEID/previews/FILEID`.

### Compartir

Ajustes globales de Compartir

#### sharing.managerFactory

```
'sharing.managerFactory' => '\OC\Share20\ProviderFactory',
```

Sustituye la fábrica predeterminada de proveedores de recursos compartidos. Puede usarse si se usan proveedores de recursos compartidos propios o de terceros que, por ejemplo, usen el sistema de archivos en lugar de la base de datos para guardar la información de los recursos compartidos.

Valor predeterminado: `\OC\Share20\ProviderFactory`

#### sharing.enable_mail_link_password_expiration

```
'sharing.enable_mail_link_password_expiration' => false,
```

Activa la caducidad de las contraseñas de los enlaces compartidos enviadas por correo electrónico (sharebymail).

Las contraseñas caducan tras el intervalo configurado; los usuarios aún pueden solicitar una nueva en la página del enlace público.

#### sharing.mail_link_password_expiration_interval

```
'sharing.mail_link_password_expiration_interval' => 3600,
```

Intervalo de caducidad de las contraseñas, en segundos.

#### sharing.maxAutocompleteResults

```
'sharing.maxAutocompleteResults' => 25,
```

Define el número máximo de resultados que devuelve la búsqueda de autocompletado de usuarios, grupos, etc. El valor no debe ser menor que 0 (sin límite).

Si se consultan varias fuentes distintas (p. ej., distintos backends de usuarios, o tanto usuarios como grupos), el valor se aplica por fuente y puede que no se trunque tras reunir los resultados. Es decir, pueden aparecer más resultados de los configurados aquí.

El valor predeterminado es 25.

#### sharing.minSearchStringLength

```
'sharing.minSearchStringLength' => 0,
```

Define la longitud mínima de la cadena de búsqueda antes de empezar el autocompletado. El valor predeterminado es sin límite (valor establecido en 0)

#### sharing.enable_share_accept

```
'sharing.enable_share_accept' => false,
```

Establecerlo en true para que, de forma predeterminada, los usuarios tengan que aceptar los recursos compartidos internos.

Los usuarios pueden cambiarlo para su cuenta en sus ajustes personales de compartir

#### sharing.force_share_accept

```
'sharing.force_share_accept' => false,
```

Establecerlo en `true` para obligar a aceptar los recursos compartidos internos

#### sharing.allow_custom_share_folder

```
'sharing.allow_custom_share_folder' => true,
```

Establecerlo en `false` para impedir que los usuarios establezcan un share_folder personalizado

#### share_folder

```
'share_folder' => '/',
```

Define una carpeta predeterminada, distinta de la raíz, para los archivos y carpetas compartidos.

Los cambios de este valor solo afectan a los recursos compartidos nuevos.

Valor predeterminado: `/`

#### sharing.enable_share_mail

```
'sharing.enable_share_mail' => true,
```

Establecerlo en `false` para dejar de enviar un correo cuando los usuarios reciben un recurso compartido

#### sharing.allow_disabled_password_enforcement_groups

```
'sharing.allow_disabled_password_enforcement_groups' => false,
```

Establecerlo en true para activar la función de añadir excepciones a la obligatoriedad de contraseña en los recursos compartidos

#### transferIncomingShares

```
'transferIncomingShares' => false,
```

Establecerlo en true para transferir siempre, de forma predeterminada, los recursos compartidos entrantes al ejecutar `occ files:transfer-ownership`.

Valor predeterminado: `false`, de modo que los recursos compartidos entrantes no se transfieren si no se solicita expresamente con un argumento de línea de comandos.

### Compartir en la nube federada

#### sharing.federation.allowSelfSignedCertificates

```
'sharing.federation.allowSelfSignedCertificates' => false,
```

Permite certificados autofirmados en los recursos compartidos federados

### Hash

#### hashing_default_password

```
'hashing_default_password' => false,
```

De forma predeterminada, Nextcloud usa el hash de contraseñas Argon2 si está disponible.

Sin embargo, si por cualquier motivo se quiere mantener el PASSWORD_DEFAULT de la versión de PHP, establecer el ajuste en true.

Nextcloud usa el algoritmo Argon2 (con PHP >= 7.2) para crear hashes por sí mismo y expone sus opciones de configuración como se indica a continuación. Hay más información en: https://www.php.net/manual/en/function.password-hash.php

#### hashingThreads

```
'hashingThreads' => PASSWORD_ARGON2_DEFAULT_THREADS,
```

El número de hilos de CPU que usa el algoritmo para calcular un hash.

El valor debe ser un entero, y el valor mínimo es `1`. Lógicamente, no sirve de nada indicar un número mayor que los hilos disponibles en la máquina. Los valores inferiores al mínimo se ignoran y se usa el mínimo.

#### hashingMemoryCost

```
'hashingMemoryCost' => PASSWORD_ARGON2_DEFAULT_MEMORY_COST,
```

La memoria, en KiB, que usa el algoritmo para calcular un hash. El valor debe ser un entero, y el valor mínimo es 8 veces el número de hilos de CPU.

Los valores inferiores al mínimo se ignoran y se usa el mínimo.

#### hashingTimeCost

```
'hashingTimeCost' => PASSWORD_ARGON2_DEFAULT_TIME_COST,
```

El número de iteraciones que usa el algoritmo para calcular un hash.

El valor debe ser un entero, y el valor mínimo es `1`. Los valores inferiores al mínimo se ignoran y se usa el mínimo.

#### hashingCost

```
'hashingCost' => 10,
```

El coste de hash que usan los hashes que genera Nextcloud. Usar un valor más alto requiere más tiempo y potencia de CPU para calcular los hashes

### Todas las demás opciones de configuración

#### dbdriveroptions

```
'dbdriveroptions' => [
        PDO::MYSQL_ATTR_SSL_CA => '/file/path/to/ca_cert.pem',
        PDO::MYSQL_ATTR_SSL_KEY => '/file/path/to/mysql-client-key.pem',
        PDO::MYSQL_ATTR_SSL_CERT => '/file/path/to/mysql-client-cert.pem',
        PDO::MYSQL_ATTR_SSL_VERIFY_SERVER_CERT => false,
        PDO::MYSQL_ATTR_INIT_COMMAND => 'SET wait_timeout = 28800'
    ],
```

Opciones adicionales del controlador para la conexión a la base de datos, p. ej., para activar el cifrado SSL en MySQL o indicar un tiempo de espera personalizado en un alojamiento barato.

Al configurar TLS/SSL para cifrar las conexiones, hay que asegurarse de que el proceso de PHP pueda leer las claves y los certificados que se le pasan. Además, puede que haya que establecer `PDO::MYSQL_ATTR_SSL_VERIFY_SERVER_CERT` en false si el CN del certificado del servidor de base de datos no coincide con el nombre de host usado para conectarse. El comportamiento estándar aquí es distinto del del cliente de línea de comandos de MySQL/MariaDB, que no verifica el certificado del servidor salvo que se pase manualmente `--ssl-verify-server-cert`.

#### sqlite.journal_mode

```
'sqlite.journal_mode' => 'DELETE',
```

El modo de diario de SQLite3 puede indicarse con este parámetro de configuración; puede ser `'WAL'` o `'DELETE'`. Ver https://www.sqlite.org/wal.html para más detalles.

#### mysql.utf8mb4

```
'mysql.utf8mb4' => false,
```

Durante la instalación, si se cumplen los requisitos (ver más abajo), este ajuste se establece en true para que MySQL pueda manejar caracteres de 4 bytes en lugar de caracteres de 3 bytes.

Para convertir una instalación existente de 3 bytes en una de 4 bytes, configurar los parámetros de MySQL como se describe más abajo y ejecutar el comando de migración: `./occ db:convert-mysql-charset`. Este ajuste de configuración se actualiza automáticamente tras una migración correcta.

Consultar la documentación para más detalles.

MySQL requiere ajustes específicos para los índices más largos (> 767 bytes), necesarios para admitir caracteres de 4 bytes:

```
[mysqld]
innodb_large_prefix=ON
innodb_file_format=Barracuda
innodb_file_per_table=ON
```

- Las tablas se crearán con:
  - juego de caracteres: `utf8mb4`
  - intercalación: `utf8mb4_bin`
  - row_format: `dynamic`

- Ver:
  - https://dev.mysql.com/doc/refman/5.7/en/charset-unicode-utf8mb4.html
  - https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_large_prefix
  - https://mariadb.com/kb/en/mariadb/xtradbinnodb-server-system-variables/#innodb_large_prefix
  - http://www.tocker.ca/2013/10/31/benchmarking-innodb-page-compression-performance.html
  - http://mechanics.flite.com/blog/2014/07/29/using-innodb-large-prefix-to-avoid-error-1071/

#### mysql.collation

```
'mysql.collation' => null,
```

En las consultas de búsqueda a la base de datos se elige una intercalación predeterminada según el juego de caracteres. En algunos casos se quiere otra intercalación, por ejemplo para búsquedas que distinguen acentos.

MariaDB y MySQL comparten algunas intercalaciones, pero también tienen otras incompatibles, según la versión del servidor de base de datos.

Esta opción permite sustituir la elección automática de la intercalación. Ejemplo:

```
'mysql.collation' => 'utf8mb4_0900_as_ci',
```

Este ajuste no afecta a la creación de tablas ni a la instalación, donde siempre se usa utf8[mb4]_bin. Solo se aplica a las consultas SQL que usan operadores de comparación LIKE.

#### pgsql_ssl

```
'pgsql_ssl' => [
        'mode' => '',
        'cert' => '',
        'rootcert' => '',
        'key' => '',
        'crl' => '',
    ],
```

Conexión SSL de PostgreSQL

#### supportedDatabases

```
'supportedDatabases' => [
        'sqlite',
        'mysql',
        'pgsql',
        'oci',
    ],
```

Tipos de base de datos admitidos para la instalación.

- Disponibles:
  - sqlite (SQLite3)
  - mysql (MySQL)
  - pgsql (PostgreSQL)
  - oci (Oracle)

- Valores predeterminados:
  - sqlite (SQLite3)
  - mysql (MySQL)
  - pgsql (PostgreSQL)

#### tempdirectory

```
'tempdirectory' => '/tmp/nextcloudtemp',
```

Sustituye la ubicación en la que Nextcloud almacena los archivos temporales. Útil en instalaciones en las que el directorio temporal del sistema está en un disco RAM de espacio limitado o restringido, o al usar un almacenamiento externo que no admite streaming.

El usuario del servidor web/PHP debe tener acceso de escritura a este directorio. Asegurarse de que la configuración de PHP lo reconozca como directorio temporal válido estableciendo en consecuencia las variables de entorno TMP, TMPDIR y TEMP. Puede que se requieran permisos adicionales para AppArmor o SELinux.

#### updatedirectory

```
'updatedirectory' => '',
```

Sustituye la ubicación en la que Nextcloud almacena los archivos de actualización durante las actualizaciones.

Útil cuando el `datadirectory` predeterminado está en un disco de red como NFS o está restringido de algún otro modo. Si no está definido, toma el valor de `datadirectory`.

Si se define, el directorio debe estar fuera del directorio de instalación de Nextcloud y el usuario del servidor web debe poder escribir en él.

#### forbidden_filenames

```
'forbidden_filenames' => ['.htaccess'],
```

Bloquea archivos o nombres de archivo concretos, impidiendo subirlos o acceder a ellos (lectura y escritura).

`.htaccess` está bloqueado de forma predeterminada.

:::{warning}
Usarlo solo si se comprenden sus implicaciones.
:::

:::{note}
Esta lista no distingue mayúsculas de minúsculas.
:::

Valor predeterminado: `['.htaccess']`

#### forbidden_filename_basenames

```
'forbidden_filename_basenames' => [],
```

Impide subir archivos con nombres base concretos. Los archivos existentes que coincidan no pueden actualizarse, y no pueden crearse archivos nuevos en las carpetas que coincidan.

El nombre base es el nombre del archivo sin la extensión; p. ej., para «archive.tar.gz», el nombre base es «archive».

:::{note}
Esta lista no distingue mayúsculas de minúsculas.
:::

Valor predeterminado: `[]` (matriz vacía)

#### forbidden_filename_characters

```
'forbidden_filename_characters' => [],
```

Bloquea caracteres concretos en los nombres de archivo. Útil para sistemas de archivos o sistemas operativos (p. ej., Windows) que no admiten ciertos caracteres. Los archivos existentes que coincidan no pueden actualizarse, y no pueden crearse archivos nuevos en las carpetas que coincidan.

Los caracteres `/` y `\`, así como los caracteres ASCII [0-31], siempre están prohibidos.

Ejemplo para Windows: `['?', '<', '>', ':', '*', '|', '"']` Ver: https://en.wikipedia.org/wiki/Comparison_of_file_systems#Limits

Valor predeterminado: `[]` (matriz vacía)

#### forbidden_filename_extensions

```
'forbidden_filename_extensions' => ['.part', '.filepart'],
```

Prohíbe extensiones de archivo concretas. Los archivos existentes que coincidan no pueden actualizarse, y no pueden crearse archivos nuevos en las carpetas que coincidan.

La extensión `'.part'` siempre está prohibida, ya que Nextcloud la usa internamente.

Valor predeterminado: `['.filepart', '.part']`

#### theme

```
'theme' => '',
```

Indica el nombre de un tema que se aplica a Nextcloud. De forma predeterminada, los temas están en `nextcloud/themes/`.

Valor predeterminado: la app de temas, incluida desde Nextcloud 9.

#### enforce_theme

```
'enforce_theme' => '',
```

Impone un tema de usuario concreto y desactiva los ajustes de tema de los usuarios. Debe ser un ID de ITheme válido, p. ej., `dark`, `dark-highcontrast`, `default`, `light`, `light-highcontrast`, `opendyslexic`.

#### theming.standalone_window.enabled

```
'theming.standalone_window.enabled' => true,
```

Activa o desactiva la funcionalidad de aplicación web progresiva (PWA), que permite a los navegadores abrir aplicaciones web en ventanas propias.

Valor predeterminado: `true`

#### cipher

```
'cipher' => 'AES-256-CTR',
```

- Indica el cifrado predeterminado para cifrar archivos. Cifrados admitidos:
  - AES-256-CTR
  - AES-128-CTR
  - AES-256-CFB
  - AES-128-CFB

Valor predeterminado: `AES-256-CTR`

#### encryption.use_legacy_base64_encoding

```
'encryption.use_legacy_base64_encoding' => false,
```

Usa el formato base64 heredado para los archivos cifrados en lugar del formato binario, que ocupa menos espacio. Solo afecta a los archivos que se escriban a partir de ese momento; los archivos cifrados existentes siguen siendo legibles sea cual sea su formato.

Valor predeterminado: `false`

#### minimum.supported.desktop.version

```
'minimum.supported.desktop.version' => '3.2.50',
```

Indica la versión mínima del cliente de escritorio de Nextcloud que puede sincronizar con este servidor. Se rechazan las conexiones de clientes anteriores. El valor predeterminado es la versión mínima con soporte oficial en el momento de publicarse esta versión del servidor.

Cambiarlo puede hacer que los clientes más antiguos y sin soporte funcionen mal, lo que podría provocar pérdida de datos o comportamientos inesperados.

Valor predeterminado: `3.2.50`

#### maximum.supported.desktop.version

```
'maximum.supported.desktop.version' => '99.99.99',
```

Indica la versión máxima del cliente de escritorio de Nextcloud que puede sincronizar con este servidor. Se rechazan las conexiones de clientes posteriores.

Valor predeterminado: `99.99.99`

#### localstorage.allowsymlinks

```
'localstorage.allowsymlinks' => false,
```

Permite que el almacenamiento local contenga enlaces simbólicos.

:::{warning}
No se recomienda, ya que permite a Nextcloud acceder a archivos fuera del directorio de datos, lo que supone un posible riesgo de seguridad.
:::

Valor predeterminado: `false`

#### localstorage.umask

```
'localstorage.umask' => 0022,
```

Nextcloud sustituye la umask para garantizar unos permisos de acceso adecuados, sea cual sea la configuración del servidor web o de PHP-FPM. Modificar este valor tiene implicaciones de seguridad y puede causar problemas en la instalación.

La mayoría de las instalaciones no deben modificar este valor.

Valor predeterminado: `0022`

#### localstorage.unlink_on_truncate

```
'localstorage.unlink_on_truncate' => false,
```

Permite que los sistemas de almacenamiento que no admiten modificar archivos existentes superen esta limitación eliminando los archivos antes de sobrescribirlos.

Valor predeterminado: `false`

#### quota_include_external_storage

```
'quota_include_external_storage' => false,
```

Incluye los montajes de almacenamiento externo en el cálculo de la cuota.

Si está activado, las cuotas de almacenamiento de los usuarios también incluyen los archivos almacenados en montajes de almacenamiento externo (como SMB, SFTP, S3, etc.) configurados para el usuario (ya sean montajes personales o globales/del sistema).

Solo cuentan para la cuota del usuario los archivos visibles para él en esos puntos de montaje. Los archivos visibles solo para otros usuarios (en sus propios montajes) no cuentan.

De forma predeterminada, los montajes de almacenamiento externo globales/del sistema son compartidos: todos los usuarios con acceso ven los mismos archivos y carpetas del almacenamiento externo. Para aislar a cada usuario, configurar el montaje con una ruta o credenciales específicas del usuario, o usar un montaje personal.

Activar esta opción puede afectar al rendimiento si los almacenamientos externos son lentos o poco fiables.

Advertencia: este ajuste se considera EXPERIMENTAL y puede no funcionar con todos los backends de almacenamiento externo.

Valor predeterminado: `false`.

#### external_storage.auth_availability_delay

```
'external_storage.auth_availability_delay' => 1800,
```

Cuando un almacenamiento externo no está disponible (p. ej., por un fallo de autenticación), se marca como tal durante un tiempo determinado. Para los fallos de autenticación, este retraso puede personalizarse para reducir la probabilidad de bloqueos de cuentas en sistemas como Active Directory.

Valor predeterminado: `1800` segundos (30 minutos)

#### files_external_allow_create_new_local

```
'files_external_allow_create_new_local' => true,
```

Permite crear almacenamientos externos de tipo «Local» desde la interfaz web y las API. Si está desactivado, los almacenamientos locales todavía pueden crearse con el comando occ:

```
occ files_external:create /mountpoint local null::null -c datadir=/path/to/data
```

Valor predeterminado: `true`

#### filesystem_check_changes

```
'filesystem_check_changes' => 0,
```

Indica con qué frecuencia se comprueba si el sistema de archivos local (el directorio data/ de Nextcloud y los montajes NFS dentro de data/) tiene cambios hechos fuera de Nextcloud. No se aplica al almacenamiento externo.

- `0` -> No comprobar nunca si el sistema de archivos tiene cambios externos, lo que mejora el rendimiento cuando no se esperan cambios externos.
- `1` -> Comprobar cada archivo o carpeta como máximo una vez por solicitud; recomendado para el uso general si son posibles los cambios externos.

Valor predeterminado: `0`

#### part_file_in_storage

```
'part_file_in_storage' => true,
```

Controla dónde se escriben los archivos temporales «.part» durante las subidas directas (no fragmentadas).

Mientras una subida está en curso, Nextcloud escribe los datos en un archivo temporal «.part» y lo renombra con el nombre de archivo definitivo cuando termina la subida.

- true: crear el archivo temporal «.part» en el almacenamiento/ruta de destino. Esto suele evitar movimientos entre almacenamientos y puede mejorar la fiabilidad y el rendimiento en los backends en los que renombrar dentro del mismo almacenamiento es barato/atómico.
- false: crear primero el archivo temporal «.part» en la carpeta raíz del usuario. Puede ayudar con algunos almacenamientos externos que tienen un comportamiento limitado al renombrar/mover, pero puede añadir sobrecarga de copia/movimiento.

Nota: este ajuste solo se aplica a las subidas directas (no fragmentadas). Las subidas fragmentadas/reanudables usan un mecanismo de preparación de subidas aparte y esta opción no las controla.

Valor predeterminado: `true`.

#### filesystem_cache_readonly

```
'filesystem_cache_readonly' => false,
```

Modo de solo lectura para las escrituras de conciliación de análisis/detección en la caché de archivos.

Si es true, Nextcloud no almacena los cambios de metadatos de la caché de archivos que se identifican a través de las rutas de conciliación del analizador/detección de cambios (global: todos los almacenamientos).

Nota de alcance:

- Las operaciones originadas en Nextcloud (interfaz/WebDAV/clientes) suelen gestionarse por las rutas de escritura normales de la aplicación y, por tanto, siguen actualizando la caché de archivos aunque esto esté establecido en true.
- Mientras está activado, se impide que las rutas de conciliación/actualización vuelvan a escribir las diferencias de metadatos descubiertas.

Efecto práctico:

- Los cambios hechos directamente en el almacenamiento fuera de Nextcloud generalmente no se reflejan mientras está activado.
- Algunos comportamientos que dependen de los metadatos pueden parecer desactualizados hasta que se desactive este parámetro (lo que vuelve a permitir las escrituras de conciliación).

Advertencia: es un ajuste experto/global para entornos especializados y, de forma deliberada, no es seguro de forma predeterminada para despliegues generales.

Valor predeterminado: `false`.

#### trusted_proxies

```
'trusted_proxies' => ['203.0.113.45', '198.51.100.128', '192.168.2.0/24'],
```

Lista de servidores proxy de confianza. Formatos admitidos:

- Direcciones IPv4, p. ej., `192.168.2.123`
- Rangos IPv4 en notación CIDR, p. ej., `192.168.2.0/24`
- Direcciones IPv6, p. ej., `fd9e:21a7:a92c:2323::1`
- Rangos IPv6 en notación CIDR, p. ej., `2001:db8:85a3:8d3:1319:8a20::/95`

Si el `REMOTE_ADDR` de una solicitud coincide con una dirección de esta lista, se trata como proxy y la IP del cliente se lee de la cabecera HTTP indicada en `forwarded_for_headers` en lugar de `REMOTE_ADDR`.

Asegurarse de configurar `forwarded_for_headers` si se establece `trusted_proxies`.

Valor predeterminado: `[]` (matriz vacía)

#### forwarded_for_headers

```
'forwarded_for_headers' => ['HTTP_X_FORWARDED', 'HTTP_FORWARDED_FOR'],
```

Cabeceras en las que se confía como portadoras de la dirección IP del cliente cuando se usan con `trusted_proxies`. Por ejemplo, usar `HTTP_X_FORWARDED_FOR` para la cabecera `X-Forwarded-For`.

Una configuración incorrecta permite a los clientes falsificar su dirección IP, eludiendo los controles de acceso y haciendo que los registros no sean fiables.

Valor predeterminado: `['HTTP_X_FORWARDED_FOR']`

#### allowed_admin_ranges

```
'allowed_admin_ranges' => ['192.0.2.42/32', '233.252.0.0/24', '2001:db8::13:37/64'],
```

Lista de rangos IP de confianza para las acciones de administración. Si no está vacía, todas las acciones de administración deben proceder de IP dentro de estos rangos.

Formatos admitidos:

- Direcciones o rangos IPv4, p. ej., `192.0.2.42/32`, `233.252.0.0/24`
- Direcciones o rangos IPv6, p. ej., `2001:db8::13:37/64`

Valor predeterminado: `[]` (matriz vacía)

#### allowed_no_password_confirmation_ranges

```
'allowed_no_password_confirmation_ranges' => ['192.0.2.42/32', '233.252.0.0/24', '2001:db8::13:37/64'],
```

Lista de rangos IP de confianza que pueden omitir la confirmación de contraseña.

Si no está vacía, ninguno de los endpoints marcados con el atributo PasswordConfirmationRequired necesitará confirmación de contraseña cuando la solicitud proceda de IP dentro de estos rangos.

Formatos admitidos:

- Direcciones o rangos IPv4, p. ej., `192.0.2.42/32`, `233.252.0.0/24`
- Direcciones o rangos IPv6, p. ej., `2001:db8::13:37/64`

Valor predeterminado: `[]` (matriz vacía)

#### max_filesize_animated_gifs_public_sharing

```
'max_filesize_animated_gifs_public_sharing' => 10,
```

Tamaño máximo de archivo (en megabytes) para animar los GIF en las páginas de recursos compartidos públicos.

Si un GIF supera este tamaño, se muestra una vista previa estática.

Establecer `-1` para no tener límite.

Valor predeterminado: `10` megabytes

#### filelocking.ttl

```
'filelocking.ttl' => 60 * 60,
```

Establece el tiempo de vida (TTL) de los bloqueos, en segundos. Los bloqueos más antiguos se limpian automáticamente.

Valor predeterminado: `3600` segundos (1 hora) o el `max_execution_time` de PHP, el que sea mayor.

#### memcache.locking

```
'memcache.locking' => '\\OC\\Memcache\\Redis',
```

Backend de caché de memoria para el bloqueo de archivos. Se recomienda encarecidamente Redis para evitar la pérdida de datos, ya que muchos backends de memcache pueden descartar valores de forma inesperada.

Valor predeterminado: `none`

#### filelocking.debug

```
'filelocking.debug' => false,
```

Activa el registro de depuración del bloqueo de archivos. Puede generar un gran volumen de entradas de registro, lo que puede degradar el rendimiento y producir archivos de registro grandes en instancias con mucha actividad.

Usarlo con `log.condition` para limitar el registro en entornos de producción.

Valor predeterminado: `false`

#### upgrade.disable-web

```
'upgrade.disable-web' => false,
```

Desactiva el actualizador web.

Valor predeterminado: `false`

#### upgrade.cli-upgrade-link

```
'upgrade.cli-upgrade-link' => '',
```

Personaliza el enlace a la documentación de actualización por CLI.

#### user_ini_additional_lines

```
'user_ini_additional_lines' => '',
```

Línea(s) adicional(es) (cadena o matriz de cadenas) que el actualizador añade a .user.ini en cada actualización.

Valor predeterminado: `''` (cadena vacía)

#### documentation_url.server_logs

```
'documentation_url.server_logs' => '',
```

Personaliza el enlace a la documentación de los registros del servidor para la gestión de excepciones.

#### debug

```
'debug' => false,
```

Activa el modo de depuración de Nextcloud. Usarlo solo para el desarrollo local, no en producción, ya que desactiva la minificación y muestra información de depuración adicional.

Valor predeterminado: `false`

#### data-fingerprint

```
'data-fingerprint' => '',
```

Establece la huella de datos de los datos que se sirven actualmente. Los clientes la usan para detectar si se ha restaurado una copia de seguridad. Para actualizarla, ejecutar:

```
occ maintenance:data-fingerprint
```

Cambiar o eliminar este valor puede hacer que los clientes conectados se queden detenidos hasta que se resuelvan los conflictos.

Valor predeterminado: `''` (cadena vacía)

#### configfilemode

```
'configfilemode' => 0640,
```

Modo del archivo config.php en notación octal.

Valor predeterminado: `0640` (escritura para el usuario, lectura para el grupo).

#### copied_sample_config

```
'copied_sample_config' => true,
```

Esta entrada sirve de advertencia si se copió la configuración de ejemplo.

¡NO AÑADIR ESTO A LA CONFIGURACIÓN!

Asegurarse de modificar cualquier ajuste solo después de consultar la documentación.

#### lookup_server

```
'lookup_server' => 'https://lookup.nextcloud.com',
```

Usa un servidor de búsqueda personalizado para publicar los datos de los usuarios.

Valor predeterminado: `https://lookup.nextcloud.com`

#### gs.enabled

```
'gs.enabled' => false,
```

Activa la arquitectura Global Scale de Nextcloud.

Valor predeterminado: `false`

#### gs.federation

```
'gs.federation' => 'internal',
```

Configura la federación en las instalaciones Global Scale. Establecerlo en `global` para permitir la federación fuera del entorno.

Valor predeterminado: `internal`

#### csrf.optout

```
'csrf.optout' => [
        '/^WebDAVFS/', // OS X Finder
        '/^Microsoft-WebDAV-MiniRedir/', // Windows WebDAV drive
    ],
```

Lista de agentes de usuario exentos de la protección de cookies SameSite por su comportamiento HTTP no estándar.

:::{warning}
Usarlo solo si se comprenden sus implicaciones.
:::

Valores predeterminados:

- `/^WebDAVFS/` (Finder de OS X)
- `/^Microsoft-WebDAV-MiniRedir/` (unidad WebDAV de Windows)

#### core.login_flow_v2.allowed_user_agents

```
'core.login_flow_v2.allowed_user_agents' => [],
```

Indica, mediante expresiones regulares, los agentes de usuario permitidos para Login Flow V2.

A los agentes de usuario que no coincidan con esta lista se les deniega el acceso a Login Flow V2.

:::{warning}
Usarlo solo si se comprenden sus implicaciones.
:::

Ejemplo: permitir solo la app de Nextcloud para Android:

```
'core.login_flow_v2.allowed_user_agents' => ['/Nextcloud-android/i'],
```

Valor predeterminado: `[]` (matriz vacía)

#### simpleSignUpLink.shown

```
'simpleSignUpLink.shown' => true,
```

Muestra u oculta el enlace de «registro sencillo» en las páginas públicas.

Ver: https://nextcloud.com/signup/

Valor predeterminado: `true`

#### login_form_autocomplete

```
'login_form_autocomplete' => true,
```

Activa o desactiva el autocompletado del formulario de inicio de sesión. Desactivarlo impide que los navegadores recuerden las credenciales de inicio de sesión, lo que puede ser necesario para cumplir ciertas políticas de seguridad.

Valor predeterminado: `true`

#### login_form_timeout

```
'login_form_timeout' => 300,
```

Establece un tiempo de espera (en segundos) para el formulario de inicio de sesión. Pasado ese tiempo, el formulario se restablece para evitar filtraciones de contraseñas en dispositivos públicos si el usuario olvida borrarlo.

Un valor de 0 desactiva el tiempo de espera.

Valor predeterminado: `300` segundos (5 minutos)

#### no_unsupported_browser_warning

```
'no_unsupported_browser_warning' => false,
```

Suprime las advertencias de navegadores obsoletos o sin soporte. Si está activado, los usuarios pueden omitir la advertencia después de leerla.

Establecerlo en `true` para desactivar la advertencia.

Valor predeterminado: `false`

#### files_no_background_scan

```
'files_no_background_scan' => false,
```

Desactiva el análisis de archivos en segundo plano. Si está activado, un trabajo en segundo plano se ejecuta cada 10 minutos para sincronizar el sistema de archivos y la base de datos de hasta 500 usuarios con archivos sin analizar (tamaño < 0 en la caché de archivos).

Valor predeterminado: `false`

#### query_log_file

```
'query_log_file' => '',
```

Registra todas las consultas a la base de datos en un archivo.

:::{warning}
Reduce considerablemente el rendimiento del servidor y solo está pensado para depurar o perfilar las interacciones de las consultas. Pueden registrarse datos sensibles en texto plano.
:::

#### query_log_file_requestid

```
'query_log_file_requestid' => '',
```

Antepone el ID de la solicitud a todas las consultas cuando se establece en *yes*.

Requiere que `query_log_file` esté definido.

#### query_log_file_parameters

```
'query_log_file_parameters' => '',
```

Incluye todos los parámetros de las consultas en el registro de consultas cuando se establece en *yes*.

Requiere que `query_log_file` esté definido.

:::{warning}
Puede registrar datos sensibles en texto plano.
:::

#### query_log_file_backtrace

```
'query_log_file_backtrace' => '',
```

Incluye una traza en el registro de consultas cuando se establece en *yes*.

Requiere que `query_log_file` esté definido.

#### redis_log_file

```
'redis_log_file' => '',
```

Registra todas las solicitudes a Redis en un archivo.

:::{warning}
Reduce considerablemente el rendimiento del servidor y solo está pensado para depurar o perfilar las interacciones con Redis. Pueden registrarse datos sensibles en texto plano.
:::

#### diagnostics.logging

```
'diagnostics.logging' => true,
```

Activa el registro de eventos de diagnóstico. Registra, con nivel de depuración, los tiempos de los pasos de ejecución habituales. Usarlo con `log.condition` para activarlo de forma condicional en producción.

Valor predeterminado: `true`

#### diagnostics.logging.threshold

```
'diagnostics.logging.threshold' => 0,
```

Limita el registro de eventos de diagnóstico a los eventos que duran más que el umbral indicado (en milisegundos). Un valor de 0 desactiva el registro de eventos de diagnóstico.

#### profile.enabled

```
'profile.enabled' => true,
```

Activa o desactiva la disponibilidad de los perfiles de usuario.

Las páginas de perfil de usuario contienen información que puede compartirse con otros usuarios, como el nombre completo, el número de teléfono, la organización, el cargo y campos similares.

Los perfiles están activados de forma predeterminada, y otras funciones pueden usar los datos del perfil (por ejemplo, la libreta de direcciones del sistema).

La visibilidad del perfil funciona por capas: lo que se comparte depende de una combinación de controles de privacidad de todo el sistema y de cada cuenta, y la visibilidad de cada campo puede configurarse.

Si se establece en false, la funcionalidad de perfiles se desactiva en toda la instancia.

Nota: afecta a los perfiles de las cuentas de usuario, no al perfilador de rendimiento para desarrolladores.

Valor predeterminado: *true*

#### account_manager.default_property_scope

```
'account_manager.default_property_scope' => [],
```

Sustituye los ámbitos predeterminados de los datos de las cuentas. Las propiedades y los ámbitos válidos se definen en `OCP\Accounts\IAccountManager`. Los valores se combinan con los predeterminados de `OC\Accounts\AccountManager`.

Ejemplo: establecer la propiedad del teléfono en el ámbito privado: `[\OCP\Accounts\IAccountManager::PROPERTY_PHONE => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE]`

#### projects.enabled

```
'projects.enabled' => false,
```

Activa la función obsoleta Proyectos, sustituida por Recursos relacionados desde Nextcloud 25.

Valor predeterminado: `false`

#### bulkupload.enabled

```
'bulkupload.enabled' => true,
```

Activa la función de subida masiva.

Valor predeterminado: `true`

#### reference_opengraph

```
'reference_opengraph' => true,
```

Activa la obtención de metadatos Open Graph de URL remotas.

Valor predeterminado: `true`

#### unified_search.enabled

```
'unified_search.enabled' => false,
```

Activa la búsqueda unificada heredada.

Valor predeterminado: `false`

#### enable_non-accessible_features

```
'enable_non-accessible_features' => true,
```

Activa funciones que aún no cumplen los estándares de accesibilidad.

Valor predeterminado: `true`

#### binary_search_paths

```
'binary_search_paths' => [
        '/usr/local/sbin',
        '/usr/local/bin',
        '/usr/sbin',
        '/usr/bin',
        '/sbin',
        '/bin',
        '/opt/bin',
    ],
```

Directorios en los que Nextcloud busca binarios externos (p. ej., LibreOffice, sendmail, ffmpeg).

Valores predeterminados:

- /usr/local/sbin
- /usr/local/bin
- /usr/sbin
- /usr/bin
- /sbin
- /bin
- /opt/bin

#### files.chunked_upload.max_size

```
'files.chunked_upload.max_size' => 100 * 1024 * 1024,
```

Tamaño máximo de fragmento en las subidas fragmentadas (en bytes). Los fragmentos más grandes aumentan el rendimiento, pero con beneficios decrecientes por encima de 100 MiB. Servicios como Cloudflare pueden limitarlo a 100 MiB.

Valor predeterminado: `100 * 1024 * 1024` (100 MiB)

#### files.chunked_upload.max_parallel_count

```
'files.chunked_upload.max_parallel_count' => 5,
```

Número máximo de fragmentos que se suben en paralelo durante las subidas fragmentadas. Un número mayor aumenta el rendimiento, pero consume más recursos del servidor, con beneficios decrecientes. El valor debe ser un entero positivo.

Valor predeterminado: `5`

#### files.trash.delete

```
'files.trash.delete' => true,
```

Permite a los usuarios eliminar manualmente archivos de su papelera. Las eliminaciones automáticas (p. ej., por falta de cuota) no se ven afectadas.

Valor predeterminado: `true`

#### enable_lazy_objects

```
'enable_lazy_objects' => true,
```

Activa los objetos perezosos de PHP 8.4 para la inyección de dependencias, lo que mejora el rendimiento al evitar instanciar objetos que no se usan.

Valor predeterminado: `true`

#### default_certificates_bundle_path

```
'default_certificates_bundle_path' => \OC::$SERVERROOT . '/resources/config/ca-bundle.crt',
```

Cambia el paquete de certificados predeterminado que se usa para confiar en los certificados.

Nextcloud incluye su propio paquete de certificados actualizado, pero en ciertos casos los administradores pueden querer indicar otro paquete, por ejemplo el que incluye su distribución.

Valor predeterminado: *\\OC::$SERVERROOT . '/resources/config/ca-bundle.crt'*.

#### openmetrics_skipped_classes

```
'openmetrics_skipped_classes' => [
        'OC\OpenMetrics\Exporters\FilesByType',
        'OCA\Files_Sharing\OpenMetrics\SharesCount',
    ],
```

Exportadores omitidos de OpenMetrics. Permite omitir algunos exportadores en el endpoint de OpenMetrics `/metrics`.

Valor predeterminado: `[]` (matriz vacía)

#### openmetrics_allowed_clients

```
'openmetrics_allowed_clients' => [
        '192.168.0.0/16',
        'fe80::/10',
        '10.0.0.1',
    ],
```

Direcciones IP de cliente permitidas en OpenMetrics. Restringe las direcciones IP que pueden hacer solicitudes al endpoint `/metrics`.

Mantener esta lista lo más restrictiva posible, ya que las métricas pueden consumir muchos recursos.

Valor predeterminado: `[127.0.0.0/16', '::1/128]` (solo se permite la interfaz de bucle local)

#### preview_expiration_days

```
'preview_expiration_days' => 0,
```

Elimina las vistas previas con más antigüedad que un número de días determinado para reducir el uso de almacenamiento.

No se permite menos de un día, así que establecerlo en 0 para desactivar la eliminación.

Valor predeterminado: `0`.

#### background_jobs_expiration_days

```
'background_jobs_expiration_days' => 60,
```

Elimina las ejecuciones de trabajos con más antigüedad que un número de días determinado.

No se permite menos de un día.

Valor predeterminado: `60`.
````
