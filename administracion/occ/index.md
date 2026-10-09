---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Qué es occ y cómo ejecutarlo como usuario HTTP: ayuda, formatos de salida, autocompletado, límites del modo de mantenimiento y depuración."
---
(nc-occ)=
# Uso del comando occ

## Resumen

Esta página explica qué es el comando `occ`, cómo ejecutarlo como el usuario HTTP, cómo consultar su ayuda y elegir el formato de salida, cómo activar el autocompletado, qué limita el modo de mantenimiento y cómo depurar un comando. Enlaza además la referencia de comandos por área. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/occ_command.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El comando `occ` de Nextcloud (su nombre proviene de «ownCloud Console») es la interfaz de línea de comandos de Nextcloud. Con `occ` se pueden realizar muchas operaciones habituales del servidor, como instalar y actualizar Nextcloud, gestionar usuarios, el cifrado, las contraseñas, los ajustes de LDAP y más.

`occ` está en el directorio {file}`nextcloud/`; por ejemplo, {file}`/var/www/nextcloud` en Ubuntu Linux. `occ` es un script PHP. **Hay que ejecutarlo como el usuario HTTP** para garantizar que se mantengan los permisos correctos de los archivos y directorios de Nextcloud.

(nc-http_user_label)=
### Ejecución de occ

Hay que ejecutar `occ` como el usuario HTTP para que la propiedad y los permisos de los archivos del directorio de datos de Nextcloud sigan siendo coherentes con el servidor web.

El usuario HTTP es distinto en las distintas distribuciones de Linux:

- En Debian/Ubuntu, el usuario y el grupo HTTP son www-data.
- En Fedora/CentOS, el usuario y el grupo HTTP son apache.
- En Arch Linux, el usuario y el grupo HTTP son http.
- En openSUSE, el usuario HTTP es wwwrun y el grupo HTTP es www.

:::{note}
APCu está desactivado de forma predeterminada en el modo de línea de comandos de PHP, lo que puede causar problemas con el comando `occ` de Nextcloud. Asegurarse de establecer el parámetro `apc.enable_cli` en `1` en el archivo de configuración `php.ini` de PHP CLI, o añadir `--define apc.enable_cli=1` cada vez que se invoque `occ`; por ejemplo:

```
sudo -u www-data php --define apc.enable_cli=1 occ config:list system
```

Si no se hace, se obtiene una salida como la siguiente:

```
An unhandled exception has been thrown:
OCP\HintException: [0]: Memcache \OC\Memcache\APCu not available for local cache (Is the matching PHP module installed and enabled?)
```
:::

Si el servidor HTTP está configurado para usar una versión de PHP distinta de la predeterminada (/usr/bin/php), `occ` debe ejecutarse con esa misma versión. Por ejemplo, en CentOS 6.5 con SCL-PHP70 instalado, el comando tiene este aspecto:

```
sudo -u apache /opt/rh/php70/root/usr/bin/php /var/www/html/nextcloud/occ
```

:::{note}
Aunque los ejemplos siguientes usan el método `sudo -u ... /path/to/php /path/to/occ`, el entorno puede requerir una utilidad envolvente distinta de `sudo` para ejecutar el comando como el usuario apropiado. Otras utilidades envolventes habituales:

- `su --command '/path/to/php ...' username`: aquí la especificación del usuario de destino va al final, y el comando que se ejecuta se indica primero.
- `runuser --user username -- /path/to/php ...`: esta utilidad envolvente puede usarse en contextos de contenedores (p. ej., Docker / `arm32v7/nextcloud`) donde no pueden usarse las utilidades envolventes `sudo` ni `su`.
:::

Al ejecutar `occ` sin opciones se listan todos los comandos y opciones, como en este ejemplo en Ubuntu:

```
sudo -E -u www-data php occ
Nextcloud version 19.0.0

Usage:
 command [options] [arguments]

Options:
 -h, --help            Display this help message
 -q, --quiet           Do not output any message
 -V, --version         Display this application version
     --ansi            Force ANSI output
     --no-ansi         Disable ANSI output
 -n, --no-interaction  Do not ask any interactive question
     --no-warnings     Skip global warnings, show command output only
 -v|vv|vvv, --verbose  Increase the verbosity of messages: 1 for normal output,
                       2 for more verbose output and 3 for debug

Available commands:
 check                 check dependencies of the server
                       environment
 help                  Displays help for a command
 list                  Lists commands
 status                show some status information
 upgrade               run upgrade routines after installation of
                       a new release. The release has to be
                       installed before.
```

Equivale a `sudo -E -u www-data php occ list`.

Ejecutarlo con la opción `-h` para obtener ayuda sobre la sintaxis:

```
sudo -E -u www-data php occ -h
```

Mostrar la versión de Nextcloud:

```
sudo -E -u www-data php occ -V
  Nextcloud version 19.0.0
```

Consultar el estado del servidor Nextcloud:

```
sudo -E -u www-data php occ status
  - installed: true
  - version: 19.0.0.12
  - versionstring: 19.0.0
  - edition:
```

`occ` tiene opciones, comandos y argumentos. Las opciones y los argumentos son opcionales, mientras que los comandos son obligatorios. La sintaxis es:

```
occ [options] command [arguments]
```

Para obtener información detallada sobre cada comando, usar el comando `help`, como en este ejemplo para el comando `maintenance:mode`:

```
sudo -E -u www-data php occ help maintenance:mode
Usage:
 maintenance:mode [options]

Options:
     --on              enable maintenance mode
     --off             disable maintenance mode
 -h, --help            Display this help message
 -q, --quiet           Do not output any message
 -V, --version         Display this application version
     --ansi            Force ANSI output
     --no-ansi         Disable ANSI output
 -n, --no-interaction  Do not ask any interactive question
     --no-warnings     Skip global warnings, show command output only
 -v|vv|vvv, --verbose  Increase the verbosity of messages: 1 for normal output,
                       2 for more verbose output and 3 for debug
```

El comando `status` anterior tiene una opción para definir el formato de salida. El predeterminado es texto plano, pero también puede ser `json`:

```
sudo -E -u www-data php occ status --output=json
{"installed":true,"version":"19.0.0.9","versionstring":"19.0.0","edition":""}
```

o `json_pretty`:

```
sudo -E -u www-data php occ status --output=json_pretty
{
   "installed": true,
   "version": "19.0.0.12",
   "versionstring": "19.0.0",
   "edition": ""
}
```

Esta opción de salida está disponible en todos los comandos de listado y similares: `status`, `check`, `app:list`, `config:list`, `encryption:status` y `encryption:list-modules`

#### Variables de entorno

`sudo` no reenvía las variables de entorno de forma predeterminada. Se puede anteponer la variable y usar la opción `-E` para transmitirla:

```
NC_debug=true sudo -E -u www-data php occ status
```

Otra opción es exportar primero la variable con `export`:

```
export NC_debug=true
sudo -E -u www-data php occ status
```

### Activación del autocompletado

:::{note}
Actualmente, el autocompletado de comandos solo funciona si el usuario con el que se ejecutan los comandos occ tiene un perfil. En la mayoría de los casos, `www-data` es `nologon` y, por tanto, **no puede** usar esta función.
:::

El autocompletado está disponible para bash (y las consolas basadas en bash). Para activarlo, hay que ejecutar **uno** de los siguientes comandos:

```
# BASH ~4.x, ZSH
source <(/var/www/html/nextcloud/occ _completion --generate-hook)

# BASH ~3.x, ZSH
/var/www/html/nextcloud/occ _completion --generate-hook | source /dev/stdin

# BASH (any version)
eval $(/var/www/html/nextcloud/occ _completion --generate-hook)
```

Esto permite usar el autocompletado con la ruta completa `/var/www/html/nextcloud/occ <tab>`.

Si también se quiere usar el autocompletado de occ desde dentro del directorio, sin la ruta completa, hay que indicar `--program occ` después de `--generate-hook`.

Si se quiere que el autocompletado se aplique automáticamente en todas las sesiones de shell nuevas, añadir el comando al perfil de la shell (p. ej., `~/.bash_profile` o `~/.zshrc`).

(nc-run_commands_in_maintenance_mode)=
### Limitaciones en el modo de mantenimiento

En el modo de mantenimiento, las apps no se cargan[^1], por lo que los comandos de las apps no están disponibles. Los comandos integrados en el servidor Nextcloud sí están disponibles en el modo de mantenimiento.

Se desaconseja usar el modo de mantenimiento salvo que el comando lo pida explícitamente o que la documentación del comando indique explícitamente que debe usarse el modo de mantenimiento.

Un comando puede usar eventos para comunicarse con otras apps. Una app solo puede reaccionar a un evento si está cargada. Ejemplo: el comando user:delete elimina una cuenta de usuario y se emite UserDeletedEvent. La app Calendario implementa un receptor de eventos que elimina los datos del usuario[^2]. En el modo de mantenimiento, la app Calendario no se carga y, por tanto, los datos del usuario no se eliminan.

[^1]: Excepción: [la app de ajustes sí se carga](https://github.com/nextcloud/server/blob/75f17b60945e15effc3eea41393eef2b13937226/lib/base.php#L780)

[^2]: [Receptor de eventos de la app Calendario para UserDeletedEvent](https://github.com/nextcloud/calendar/blob/87e8586971a8676dc15a90f0cd969274678b7009/lib/Listener/UserDeletedListener.php)

(nc-occ_debugging)=
### Depuración

Todos los comandos `occ` aceptan las opciones de verbosidad estándar de Symfony Console:

- `-v`: salida normal (errores, advertencias y mensajes clave)
- `-vv`: salida detallada (más detalle sobre el progreso)
- `-vvv`: salida de depuración (traza completa, útil para diagnosticar fallos de comandos)

Ejemplo:

```
sudo -E -u www-data php occ files:scan --all -vv
```

Para activar también la salida de registro de nivel de depuración del propio Nextcloud, establecer la variable de entorno `NC_loglevel`:

```
NC_loglevel=0 sudo -E -u www-data php occ status
```

Consultar {nc-doc}`admin_manual/configuration_server/logging_configuration` para más información sobre los niveles de registro.

### Referencia de comandos

- {nc-doc}`admin_manual/occ_apps`
- {nc-doc}`admin_manual/occ_database`
- {nc-doc}`admin_manual/occ_encryption`
- {nc-doc}`admin_manual/occ_files`
- {nc-doc}`admin_manual/occ_ldap`
- {nc-doc}`admin_manual/occ_ocm`
- {nc-doc}`admin_manual/occ_users`
- {nc-doc}`admin_manual/occ_system`
````

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
