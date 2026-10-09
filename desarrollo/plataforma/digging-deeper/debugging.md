---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo depurar: modo de depuración, registro de errores, variables, XDebug, JavaScript, plantillas, consultas SQL de MariaDB y directorios de apps alternativos."
---
# Depuración

## Resumen

Esta página explica cómo depurar el servidor y las apps: el modo de depuración, dónde se registran los errores, cómo inspeccionar variables, cómo usar XDebug, cómo depurar JavaScript, plantillas y consultas SQL de MariaDB, y el uso de directorios de apps alternativos. Está dirigida a quienes desarrollan sobre la plataforma.

````{upstream} developer_manual/digging_deeper/debugging.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
(nc-dev-debug-mode)=
### Modo de depuración

Cuando el modo de depuración está activado en Nextcloud, se activan diversas funciones de depuración; ver la documentación de depuración. Para activarlo, establecer `debug` en `true` en {file}`/config/config.php`:

```php
<?php
$CONFIG = array (
    'debug' => true,
    ... configuration goes here ...
);
```

### Identificar errores

Nextcloud usa un manejo de errores de PHP personalizado que impide que los errores se impriman en los archivos de registro del servidor web o en la salida de la línea de comandos. En su lugar, los errores se guardan generalmente en el propio archivo de registro de Nextcloud, ubicado en: {file}`/data/nextcloud.log`

### Depurar variables

Si se necesita depurar manualmente valores de variables, se deben usar excepciones, y no alternativas como trigger_error() (que puede no registrarse).

p. ej.:

```php
<?php throw new \Exception( "\$user = $user" ); // should be logged in Nextcloud ?>
```

no:

```php
<?php trigger_error( "\$user = $user" ); // may not be logged anywhere ?>
```

Para desactivar el manejo de errores personalizado de Nextcloud (y que PHP y el servidor web manejen los errores en su lugar), ver Modo de depuración.

### Usar un depurador de PHP (XDebug)

Usar un depurador conectado a PHP permite recorrer el código línea a línea, ver las variables en cada línea e incluso cambiar valores mientras el código se ejecuta. El depurador estándar de facto para PHP es XDebug, disponible como paquete instalable en muchas distribuciones. Sin embargo, solo proporciona la parte de PHP, por lo que se necesita una interfaz para controlar realmente XDebug. Una vez instalado, debe activarse en {file}`php.ini`, junto con algunos parámetros para permitir las conexiones con la interfaz de depuración:

```ini
zend_extension=/usr/lib/php/modules/xdebug.so
xdebug.remote_enable=on
xdebug.remote_host=127.0.0.1
xdebug.remote_port=9000
xdebug.remote_handler=dbgp
```

XDebug intentará ahora (cuando esté activado) conectarse a localhost en el puerto 9000 y se comunicará mediante el protocolo estándar DBGP. Este protocolo lo admiten muchas interfaces de depuración, como las siguientes, que son populares:

- vdebug - cliente depurador DBGP multilenguaje para Vim
- SublimeTextXdebug - cliente de XDebug para Sublime Text
- PHPStorm - depurador DBGP integrado

Para más información, ver la documentación de XDebug: <https://xdebug.org/docs/remote>

Una vez que se conoce el funcionamiento del cliente de depuración, se puede empezar a depurar con XDebug. Para probar Nextcloud a través de la interfaz web u otras solicitudes HTTP, establecer la cookie o el parámetro POST `XDEBUG_SESSION_START`. Como alternativa, hay extensiones de navegador que lo facilitan:

- The Easiest XDebug (Firefox): <https://addons.mozilla.org/en-US/firefox/addon/the-easiest-xdebug/>
- XDebug Helper (Chrome): <https://chrome.google.com/extensions/detail/eadndfjplgieldjbigjakmdgkmoaaaoc>

Para depurar scripts en la línea de comandos, como `occ` o las pruebas unitarias, establecer la variable de entorno `XDEBUG_CONFIG`.

### Depurar JavaScript

De forma predeterminada, todos los archivos JavaScript de Nextcloud se minifican (comprimen) en un único archivo sin espacios en blanco. Para evitarlo, ver Modo de depuración.

### Depurar HTML y plantillas

De forma predeterminada, Nextcloud almacena en caché el HTML generado por las plantillas. Esto puede impedir, por ejemplo, que los cambios en las plantillas de las apps se apliquen al recargar la página. Para desactivar la caché, ver Modo de depuración.

### Depurar consultas SQL

Al encontrar errores de base de datos durante consultas o migraciones, puede ser útil obtener un registro completo de las consultas.

#### Depurar consultas de MariaDB

MariaDB puede registrar todas las consultas en un archivo o en una tabla.

```sql
SET GLOBAL general_log = 'ON';
SET GLOBAL log_output = 'table';
```

Estos ajustes globales activan el registro sobre la marcha. No es necesario reiniciar la base de datos.

```sql
SELECT * FROM mysql.general_log
```

Esto consulta todas las consultas registradas.

:::{note}
En la {nc-ref}`integración continua <app-ci>`, este truco puede dar con bastante facilidad las SQL de varios tipos y versiones de una base de datos, por si hay que depurar una matriz de configuraciones.
:::

### Usar directorios de apps alternativos

Puede ser útil tener varios directorios de apps con fines de prueba, para poder alternar cómodamente entre distintas versiones de las aplicaciones. Ver la documentación del archivo de configuración para más detalles.
````
