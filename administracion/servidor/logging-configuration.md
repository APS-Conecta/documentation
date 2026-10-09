---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Registro de Nextcloud: niveles y tipos de registro, parámetros de config.php, registro condicional, campos y registros de auditoría y de flujos."
---
# Registro

## Resumen

Esta página describe, para quienes administran el servidor, los niveles y tipos de registro de Nextcloud, sus parámetros en `config.php`, el registro condicional, los campos de cada entrada y la configuración de los registros de auditoría y de flujos.

````{upstream} admin_manual/configuration_server/logging_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El registro de Nextcloud sirve para revisar el estado del sistema o para ayudar a depurar problemas. Pueden ajustarse los niveles de registro y elegirse cómo y dónde se almacenan los datos de registro. Si se necesita un registro de eventos adicional, puede activarse opcionalmente la app **admin_audit**.

Cuando se usa el registro basado en `file`, tanto el registro de Nextcloud como, opcionalmente, el registro de la app **admin_audit** pueden verse en la interfaz de Nextcloud, en {guilabel}`Configuraciones de administración` → {guilabel}`Registros` (esta función la aporta la app **logreader**).

Más abajo hay más detalles de configuración y uso, tanto del registro estándar de Nextcloud como del registro opcional de la app **admin_audit**.

### Nivel de registro

Los niveles de registro van desde **DEBUG**, que registra toda la actividad, hasta **FATAL**, que registra solo los errores fatales.

- **0**: DEBUG: toda la actividad; el registro más detallado.
- **1**: INFO: actividad como los inicios de sesión de los usuarios y la actividad de archivos, además de advertencias, errores y errores fatales.
- **2**: WARN: las operaciones se completan, pero con advertencias de posibles problemas, además de errores y errores fatales.
- **3**: ERROR: una operación falla, pero los demás servicios y operaciones continúan, además de errores fatales.
- **4**: FATAL: el servidor se detiene.

De forma predeterminada, el nivel de registro está establecido en **2** (WARN). Usar **DEBUG** cuando haya un problema que diagnosticar y después devolver el nivel de registro a uno menos detallado, ya que **DEBUG** genera mucha información y puede afectar al rendimiento del servidor.

Los parámetros del nivel de registro se establecen en el archivo {file}`config/config.php`.

### Tipo de registro

#### errorlog

Toda la información de registro se enviará a `error_log()` de PHP.

```
"log_type" => "errorlog",
```

Las entradas de registro llevarán el prefijo `[nextcloud]`.

#### file

Toda la información de registro se escribirá en un archivo de registro aparte, que puede verse con el visor de registros de la página de administración. De forma predeterminada, se creará un archivo de registro llamado **nextcloud.log** en el directorio configurado con el parámetro **datadirectory** en {file}`config/config.php`.

Opcionalmente, el formato de fecha deseado puede definirse con el parámetro **logdateformat** en {file}`config/config.php`. De forma predeterminada se usa el parámetro `c` de la [función date de PHP][PHP date function], por lo que la fecha y hora se escriben con el formato `2013-01-10T15:20:25+02:00`. Con el formato de fecha del ejemplo siguiente, la fecha y hora se escribirán con el formato `January 10, 2013 15:20:25`.

```
"log_type" => "file",
"logfile" => "nextcloud.log",
"loglevel" => 3,
"logdateformat" => "F d, Y H:i:s",
```

##### Parámetros adicionales del registro basado en archivo

En {file}`config/config.php` también pueden establecerse los siguientes parámetros opcionales:

- **logfilemode**: establece los permisos del archivo de registro (en notación octal).

  El valor predeterminado es `0640`.

  ```
  "logfilemode" => 0640,
  ```

- **logtimezone**: establece la zona horaria que se usa en las marcas de tiempo del registro. Consultar la [lista de zonas horarias admitidas de PHP](https://www.php.net/manual/en/timezones.php).

  El valor predeterminado es `UTC`.

  ```
  "logtimezone" => "Europe/Berlin",
  ```

- **log_rotate_size**: activa la rotación del registro y limita el tamaño total de los archivos de registro. El valor se indica en bytes. Cuando el archivo de registro actual alcanza este tamaño, se crea un nuevo archivo de registro. Si ya existe un archivo de registro rotado, se sobrescribe. Establecer en `0` para desactivar la rotación.

  El valor predeterminado es `104857600` (100 MB).

  ```
  "log_rotate_size" => 100 * 1024 * 1024,
  ```

- **log.backtrace**: cuando está activado, se añade una traza a cada línea de registro, no solo a las excepciones. Esto aumenta notablemente el tamaño del registro y solo debe usarse para depurar.

  El valor predeterminado es `false`.

  ```
  "log.backtrace" => true,
  ```

- **log_query**: añade al archivo de registro todas las consultas a la base de datos y sus parámetros. Usarlo solo para depurar, ya que genera archivos de registro muy grandes.

  El valor predeterminado es `false`.

  ```
  "log_query" => true,
  ```

- **loglevel_frontend**: establece un nivel de registro aparte para los mensajes que se originan en el frontend de Nextcloud (navegador). Acepta los mismos valores que `loglevel` (0–4).

  El valor predeterminado es `2` (WARN).

  ```
  "loglevel_frontend" => 2,
  ```

- **loglevel_dirty_database_queries**: establece el nivel de registro con el que se registran las consultas sucias a la base de datos (consultas que se ejecutan después de que la respuesta ya se haya enviado).

  El valor predeterminado es `0` (DEBUG).

  ```
  "loglevel_dirty_database_queries" => 0,
  ```

#### syslog

Toda la información de registro se enviará al demonio syslog predeterminado.

```
"log_type" => "syslog",
"syslog_tag" => "Nextcloud",
"logfile" => "",
"loglevel" => 3,
```

#### systemd

Toda la información de registro se enviará al journal de Systemd. Requiere la extensión [php-systemd](https://github.com/systemd/php-systemd).

```
"log_type" => "systemd",
"syslog_tag" => "Nextcloud",
```

### Registro condicional (log.condition)

Nextcloud admite sustituciones condicionales que elevan temporalmente el nivel de registro a **DEBUG** cuando se cumplen ciertos criterios. Esto es útil para diagnosticar problemas en producción sin inundar todo el registro con salida de depuración.

El parámetro `log.condition` se establece en {file}`config/config.php`.

#### Condiciones básicas

En el nivel superior pueden indicarse una o varias de las siguientes claves. Cuando *cualquiera* de ellas coincide, el nivel de registro de esa solicitud se establece en **DEBUG**:

- **shared_secret**: coincide con las solicitudes que pasan el parámetro de consulta `log_secret` con este valor.
- **users**: una matriz de ID de usuario. Si el usuario autenticado en ese momento está en la lista, la condición se cumple.
- **apps**: una matriz de identificadores de app. Cualquier mensaje de registro cuyo contexto de app coincida con una de estas apps se registrará con el nivel DEBUG.

Ejemplo – activar el registro de depuración para el usuario `jane` y la app `files`:

```
'log.condition' => [
    'users' => ['jane'],
    'apps' => ['files'],
],
```

#### Condiciones compuestas avanzadas (matches)

La clave `matches` acepta una matriz de grupos de condiciones. Cada grupo puede combinar todas las claves anteriores y, además:

- **message**: una subcadena que debe aparecer en el mensaje de registro.
- **loglevel**: el nivel de registro que se aplica cuando este grupo coincide (en lugar del predeterminado, DEBUG / `0`).

Para que un grupo se aplique, deben coincidir todas las claves de ese grupo (Y lógico). Los distintos grupos se evalúan de forma independiente (O lógico).

Ejemplo – registrar todos los mensajes de la app `files` con el nivel INFO, y registrar con el nivel DEBUG cualquier mensaje que contenga `"Lock"` para el usuario `admin`:

```
'log.condition' => [
    'matches' => [
        [
            'apps' => ['files'],
            'loglevel' => 1,
        ],
        [
            'users' => ['admin'],
            'message' => 'Lock',
            'loglevel' => 0,
        ],
    ],
],
```

#### Usar un secreto compartido para depurar bajo demanda

Puede activarse el registro de depuración para una sola solicitud añadiendo el parámetro de consulta `log_secret`. Establecer un secreto en {file}`config/config.php`:

```
'log.condition' => [
    'shared_secret' => '57b58edb6637fe3059b3595cf9c41b9',
],
```

Después, llamar a la URL de Nextcloud con el secreto añadido:

```
https://cloud.example.com/index.php?log_secret=57b58edb6637fe3059b3595cf9c41b9
```

:::{warning}
Mantener privado el secreto compartido. Cualquiera que lo conozca puede activar el registro con nivel de depuración en la instancia.
:::

### Explicación de los campos del registro

#### Ejemplos de entradas de registro

```
{
    "reqId":"TBsuA2uE86DiOD0S8f9j",
    "level":1,
    "time":"April 13, 2021 16:55:37",
    "remoteAddr":"192.168.56.1",
    "user":"admin",
    "app":"admin_audit",
    "method":"GET",
    "url":"/ocs/v1.php/cloud/users?disabled",
    "message":"Login successful: \"admin\"",
    "userAgent":"curl/7.68.0",
    "version":"21.0.1.1"
}

{
    "reqId":"ByeDVLuwkXKMfLpBgvxC",
    "level":2,
    "time":"April 14, 2021 09:03:29",
    "remoteAddr":"192.168.56.1",
    "user":"--",
    "app":"no app in context",
    "method":"POST",
    "url":"/login",
    "message":"Login failed: asdf (Remote IP: 192.168.56.1)",
    "userAgent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "version":"21.0.1.1"
}
```

#### Desglose de los campos del registro

- **reqId** (ID de solicitud): todas las líneas de registro relacionadas con una misma solicitud tienen el mismo valor
- **level**: nivel del incidente registrado; siempre 1 en audit.log
- **time**: fecha y hora (el formato y la zona horaria pueden configurarse en config.php)
- **remoteAddr**: la dirección IP del usuario (si corresponde – vacía en los comandos occ)
- **user**: ID del usuario que actúa (si corresponde)
- **app**: app afectada (siempre admin_audit en audit.log)
- **method**: método HTTP, por ejemplo GET, POST, PROPFIND, etc. – vacío en las llamadas occ
- **url**: ruta de la solicitud (si corresponde – vacía en las llamadas occ)
- **scriptName**: el nombre del script PHP que gestionó la solicitud
- **message**: mensaje con la información del evento
- **userAgent**: agente de usuario (si corresponde – vacío en las llamadas occ)
- **exception**: excepción completa con la traza (si corresponde)
- **data**: datos estructurados adicionales (si corresponde)
- **version**: versión de Nextcloud en el momento de la solicitud
- **clientReqId**: valor de la cabecera HTTP `X-Request-Id` que envía el cliente (solo presente cuando la cabecera está establecida)
- **occ_command**: el comando occ que se ejecutó, como una matriz de hasta dos argumentos (solo presente en modo CLI)
- **backtrace**: traza PHP completa (solo presente cuando `log.backtrace` está activado en config.php)

Los valores vacíos se escriben como dos guiones: `--`.

### Registro de auditoría de administración (opcional)

(nc-config-admin-audit)=

Al activar la app **admin_audit** puede registrarse información adicional sobre diversos eventos. El registro de auditoría admite todos los backends de registro descritos arriba (file, syslog, systemd, errorlog).

#### Ubicación predeterminada del registro de auditoría

Con el backend predeterminado `file`, el registro de auditoría se escribe en **audit.log**, dentro del directorio configurado con `datadirectory` en {file}`config/config.php` (p. ej., `/var/www/html/data/audit.log`).

La ruta puede sustituirse con la clave de configuración del sistema `logfile_audit`:

```
'logfile_audit' => '/var/log/nextcloud/audit.log',
```

#### Configuración específica del registro de auditoría

El backend del registro de auditoría puede configurarse con independencia del registro principal de Nextcloud mediante tres claves específicas en {file}`config/config.php`:

- **log_type_audit**: el backend de registro de los eventos de auditoría. Acepta los mismos valores que `log_type`: `file`, `syslog`, `systemd` o `errorlog`.

  El valor predeterminado es `file`.

- **logfile_audit**: ruta del archivo de registro de auditoría (solo se usa cuando `log_type_audit` es `file`). Si está vacía, se usa el `audit.log` predeterminado del directorio de datos.

- **syslog_tag_audit**: el identificador de syslog de los mensajes de auditoría (solo se usa cuando `log_type_audit` es `syslog` o `systemd`). El valor predeterminado es el de `syslog_tag`.

Ejemplo – enviar los eventos de auditoría a syslog en lugar de a un archivo:

```
'log_type_audit' => 'syslog',
'syslog_tag_audit' => 'Nextcloud',
'logfile_audit' => '',
```

#### Interacción con el nivel de registro

La app **admin_audit** escribe sus mensajes con el nivel **INFO** (`1`). Como el `loglevel` predeterminado del sistema es **WARN** (`2`), los mensajes de auditoría se suprimen a menos que se baje explícitamente el nivel de registro del sistema o se añada una sustitución condicional.

Lo recomendado es añadir una entrada `log.condition` que fuerce el registro con nivel DEBUG para el contexto de la app `admin_audit`, sin afectar a las demás apps:

```
'log.condition' => [
    'apps' => ['admin_audit'],
],
```

Así los eventos de auditoría se escriben siempre, independientemente del ajuste global `loglevel`.

#### Integración en la interfaz web

La app integrada **logreader** (que aporta {guilabel}`Configuraciones de administración` → {guilabel}`Registros`) solo lee el `nextcloud.log` basado en archivo. De forma predeterminada, el registro de auditoría se escribe en un archivo `audit.log` aparte, por lo que las entradas de auditoría no aparecerán en la interfaz web.

Para que los eventos de auditoría aparezcan en logreader, apuntar `logfile_audit` al mismo archivo que `nextcloud.log`:

```
'log.condition' => [
    'apps' => ['admin_audit'],
],
'logfile_audit' => '/var/www/html/data/nextcloud.log',
```

:::{note}
Ajustar la ruta anterior a la ubicación real de `datadirectory`. Esto fusiona las entradas de auditoría en el archivo de registro principal; el `audit.log` aparte dejará de escribirse.
:::

#### Configuración mediante los ajustes de la app admin_audit (heredada)

Antes, el archivo del registro de auditoría se definía mediante la configuración de la app. Este ajuste se sigue leyendo como alternativa cuando `logfile_audit` no está establecido en {file}`config/config.php`, pero se considera un parámetro **heredado**. En las instalaciones nuevas debe preferirse la clave de configuración del sistema.

```
occ config:app:set admin_audit logfile --value=/var/log/nextcloud/audit.log
```

### Registro de flujos

La app **workflowengine** registra los eventos relacionados con Nextcloud Flow (flujos de trabajo automatizados que se configuran en {guilabel}`Configuraciones de administración` → {guilabel}`Flujo`). De forma predeterminada, estos eventos se escriben en `flow.log`, dentro del directorio de datos.

La ruta del registro de flujos puede cambiarse con:

```
occ config:app:set workflowengine logfile --value=/var/log/nextcloud/flow.log
```

Para desactivar por completo el registro de flujos, redirigir la salida a `/dev/null`:

```
occ config:app:set workflowengine logfile --value=/dev/null
```

### Sustituciones temporales

El nivel de registro de config.php puede sustituirse para los comandos `occ`, {nc-ref}`como se documenta aquí <occ_debugging>`.

[PHP date function]: http://www.php.net/manual/en/function.date.php
````
