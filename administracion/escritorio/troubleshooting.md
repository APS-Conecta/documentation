---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Diagnosticar fallos de sincronización del cliente de escritorio: pruebas de servidor y WebDAV, errores conocidos, registros, volcados de memoria y Citrix."
---
# Solución de problemas

## Resumen

Esta página ayuda a aislar la causa de los fallos de sincronización del cliente de escritorio: pruebas básicas del servidor y de WebDAV, mensajes de error conocidos, archivos de registro del cliente, del servidor y del servidor web, volcados de memoria y problemas conocidos en Citrix Workspace. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/desktop/troubleshooting.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los dos problemas generales siguientes pueden hacer que la sincronización falle:

- La configuración del servidor es incorrecta.
- El cliente contiene un error.

Al informar de errores, es útil determinar primero qué parte del sistema está causando el problema.

### Identificar problemas de funcionamiento básico

- Realizar una prueba general del servidor Nextcloud: el primer paso para solucionar problemas de sincronización es verificar que se puede iniciar sesión en la aplicación web de Nextcloud. Para verificar la conectividad con el servidor Nextcloud, intentar iniciar sesión desde el navegador web.

  Si no se piden el nombre de usuario y la contraseña, o si aparece un recuadro de advertencia rojo en la página, la configuración del servidor necesita modificaciones. Verificar que la instalación del servidor funciona correctamente.

- Asegurarse de que la API de WebDAV funciona: si todos los clientes de escritorio fallan al conectarse al servidor Nextcloud, pero el acceso mediante la interfaz web funciona correctamente, el problema suele ser una configuración incorrecta de la API de WebDAV.

  El cliente de {vendor}`Nextcloud` usa el acceso WebDAV integrado del servidor al contenido. Verificar que se puede iniciar sesión en el servidor WebDAV de Nextcloud. Para verificar la conectividad con el servidor WebDAV de Nextcloud:

  - Abrir una ventana del navegador e introducir la dirección del servidor WebDAV de Nextcloud.

  Por ejemplo, si la instancia de Nextcloud está instalada en `http://yourserver.com/nextcloud`, la dirección del servidor WebDAV es `http://yourserver.com/nextcloud/remote.php/dav`.

  Si se piden el nombre de usuario y la contraseña pero, tras introducir las credenciales correctas, la autenticación falla, asegurarse de que el backend de autenticación está configurado correctamente.

- Usar una herramienta de línea de comandos de WebDAV para hacer pruebas: un método de prueba más sofisticado para solucionar problemas de sincronización es usar un cliente WebDAV de línea de comandos e iniciar sesión en el servidor WebDAV de Nextcloud. Uno de estos clientes de línea de comandos, llamado `cadaver`, está disponible para distribuciones Linux. Esta aplicación puede usarse para verificar además que el servidor WebDAV funciona correctamente mediante llamadas PROPFIND.

  Por ejemplo, después de instalar la aplicación `cadaver`, puede ejecutarse el comando `propget` para obtener varias propiedades del directorio actual y verificar también la conexión con el servidor WebDAV.

### «CSync unknown error»

Si aparece este mensaje de error, detener el cliente, eliminar el archivo `.sync_xxxxxxx.db` y luego reiniciar el cliente. Dentro de la carpeta de cada cuenta configurada en el cliente hay un archivo oculto `.sync_xxxxxxx.db`.

:::{note}
Tener en cuenta que esto también borrará algunos de los ajustes sobre qué archivos descargar.
:::

Consultar <https://github.com/owncloud/client/issues/5226> para ver más discusión sobre este problema.

### Mensaje «Connection closed» al sincronizar archivos

Este mensaje puede deberse al uso de fragmentos demasiado grandes o de tiempos de espera configurados con demasiada holgura. El comportamiento de fragmentación del cliente puede configurarse en el archivo de configuración. Por ejemplo, cambiar estos ajustes:

:::{list-table}
* - `chunkSize`
  - `10000000` (10 MB)
  - Especifica el tamaño de fragmento de los archivos subidos, en bytes. El cliente ajustará este tamaño de forma dinámica dentro de los límites máximo y mínimo (ver más abajo).
* - `minChunkSize`
  - `1000000` (1 MB)
  - Especifica el tamaño mínimo de fragmento de los archivos subidos, en bytes.
* - `maxChunkSize`
  - `50000000` (1000 MB)
  - Especifica el tamaño máximo de fragmento de los archivos subidos, en bytes.
* - `targetChunkUploadDuration`
  - `6000` (1 minuto)
  - Duración objetivo, en milisegundos, de la subida de cada fragmento. El cliente ajusta el tamaño de fragmento hasta que la subida de cada fragmento tarda aproximadamente ese tiempo. Establecerla en 0 desactiva el ajuste dinámico del tamaño de fragmento.
:::

Establecer `maxChunkSize` en 50000000, por ejemplo, reducirá cada fragmento a unos 50 mb. Esto genera una sobrecarga adicional, pero puede ser necesario en algunas situaciones, por ejemplo detrás de CloudFlare, que se ha observado que limita los fragmentos de subida a 100 mb. En otras situaciones, limitar `targetChunkUploadDuration` puede ayudar a evitar que se agoten los tiempos de espera.

### Problemas de conexión del cliente de macOS con conexiones «inseguras»

Al usar dispositivos macOS para conectarse a un servidor Nextcloud que usa lo que puede clasificarse como una conexión insegura (es decir, conectarse a un servidor con un certificado autofirmado, o con un certificado que usa un cifrado que Apple puede considerar insuficientemente seguro), es posible que el cliente de macOS no se conecte al servidor. Esto se debe a que macOS exige un certificado válido para establecer una conexión.

Para resolver este problema, hay que asegurarse de que el servidor esté firmado con un certificado que acepten los requisitos de App Transport Security de Apple. Hay más información sobre los requisitos en las páginas de documentación de Apple.

<https://developer.apple.com/documentation/security/preventing-insecure-network-connections>

### Aislar otros problemas

Otros problemas pueden afectar a la sincronización de los archivos de Nextcloud:

- Si los resultados de las sincronizaciones no son fiables, asegurarse de que la carpeta que se sincroniza no esté compartida con otras aplicaciones de sincronización.

- Sincronizar el mismo directorio con Nextcloud y con otro software de sincronización, como Unison, rsync o Microsoft Windows Offline Folders, o con otros servicios en la nube, como Dropbox o Microsoft SkyDrive, no se admite y no debe intentarse. En el peor de los casos, sincronizar carpetas o archivos con Nextcloud y con otro software o servicio de sincronización puede provocar la pérdida de datos.

- Si solo algunos archivos concretos no se sincronizan, puede que influya el protocolo de sincronización. Algunos archivos se ignoran automáticamente porque son archivos del sistema; otros pueden ignorarse porque su nombre contiene caracteres que no son compatibles con determinados sistemas de archivos. Para más información sobre los archivos ignorados, consultar *ignored-files*.

- Si se opera un servidor propio y se usa el backend de almacenamiento local (el predeterminado), asegurarse de que Nextcloud tenga acceso exclusivo al directorio.

  :::{warning}
  El directorio de datos del servidor es exclusivo de Nextcloud y no debe modificarse manualmente.
  :::

- Si se usa otro backend de archivos en el servidor, puede intentar descartarse un error en ese backend volviendo al backend integrado.

- Si las velocidades de subida o descarga son lentas o hay problemas de rendimiento similares, hay que tener en cuenta que pueden deberse a soluciones de análisis antivirus en el acceso, ya sea en el servidor (como la app files_antivirus) o en el cliente.

### Archivos de registro

Depurar software de forma eficaz requiere toda la información relevante que pueda obtenerse. Para ayudar al personal de soporte de {vendor}`Nextcloud`, intentar proporcionar tantos registros relevantes como sea posible. La salida de los registros puede ayudar a localizar problemas y, si se informa de un error, puede ayudar a resolverlo más rápido.

:::{warning}
Los archivos de registro contienen información sensible. Puede convenir ocultar los datos sensibles o compartir solo extractos limitados.
:::

#### Obtener el archivo de registro del cliente

#### Crear un archivo de depuración

Desde la versión 3.1.0 es más fácil que los usuarios proporcionen información de depuración: el registro de depuración está activado de forma predeterminada con un tiempo de caducidad de 24 horas y, en los ajustes «General», se puede hacer clic en «Crear archivo de depuración…» para elegir la ubicación en la que el cliente de escritorio exportará los registros y la base de datos a un archivo zip.

#### Atajo de teclado

Otra forma de obtener el archivo de registro del cliente:

1. Abrir el cliente de escritorio de {vendor}`Nextcloud`.

2. Pulsar F12 o Ctrl-L en el teclado.

Se abre la ventana de salida del registro.

3. Hacer clic en el botón «Guardar».

Se abre la ventana para guardar el archivo de registro.

4. Ir a la ubicación del sistema en la que se quiere guardar el archivo de registro.

5. Dar un nombre al archivo de registro y hacer clic en el botón «Guardar».

   El archivo de registro se guarda en la ubicación indicada.

#### Línea de comandos

Como alternativa, la ventana de salida del registro de Nextcloud puede abrirse con el comando `--logwindow`. Tras ejecutar este comando, se abre la ventana de salida del registro, que muestra el registro actual. Después pueden seguirse los mismos procedimientos descritos arriba para guardar el registro en un archivo.

:::{note}
También puede abrirse una ventana de registro para una sesión que ya está en ejecución, reiniciando el cliente con el siguiente comando:

- Windows: `C:\Program Files\Nextcloud\nextcloud.exe --logwindow`
- macOS: `/Applications/nextcloud.app/Contents/MacOS/nextcloud --logwindow`
- Linux: `nextcloud --logwindow`
:::

#### Archivo de configuración

El cliente de {vendor}`Nextcloud` permite guardar los archivos de registro directamente en un archivo o directorio predefinido. Es una opción útil para solucionar problemas esporádicos, ya que permite registrar grandes cantidades de datos y eludir los ajustes de búfer limitados de la ventana de registro.

Para activar el registro en un directorio, detener el cliente y añadir lo siguiente a la sección General del archivo de configuración:

```
[General]
logDebug=true
logExpire=<hours>
logDir=<dir>
```

Sea cual sea la plataforma, hay que usar la barra (/) como separador de rutas:

:::{note}
- Correcto: C:/Temp
- Incorrecto: C:\Temp
:::

Por ejemplo, para conservar los datos de registro durante dos días en un directorio llamado temp:

```
[General]
logDebug=true
logExpire=48
logDir=C:/Temp
```

Tras reiniciar el cliente, el archivo de registro estará en el `<dir>` definido en `logDir`.

:::{note}
El archivo de configuración se encuentra en las siguientes ubicaciones:

- Sistemas Microsoft Windows: `%APPDATA%\Nextcloud\nextcloud.cfg`
- Sistemas macOS: `$HOME/Library/Preferences/Nextcloud/nextcloud.cfg`
- Distribuciones Linux: `$HOME/.config/Nextcloud/nextcloud.cfg`
:::

Como alternativa, el cliente puede iniciarse desde la línea de comandos con parámetros:

1. Para guardar en un archivo, iniciar el cliente con el comando `--logfile <file>`, donde `<file>` es el nombre del archivo en el que se quiere guardar.

2. Para guardar en un directorio, iniciar el cliente con el comando `--logdir <dir>`, donde `<dir>` es un directorio existente.

Al usar el comando `--logdir`, cada sincronización crea un archivo nuevo. Para limitar la cantidad de datos que se acumula con el tiempo, puede indicarse el comando `--logexpire <hours>`. Combinado con el comando `--logdir`, el cliente borra automáticamente del directorio los datos de registro guardados que tienen más antigüedad que el número de horas indicado.

Por ejemplo, para definir una prueba en la que se conserven los datos de registro durante dos días, puede ejecutarse el siguiente comando:

`` ` nextcloud --logdir /tmp/nextcloud_logs --logexpire 48 ` ``

#### Archivo de registro del servidor Nextcloud

El servidor Nextcloud también mantiene un archivo de registro propio de Nextcloud. Este archivo de registro debe activarse desde la página de administración de Nextcloud. En esa página se puede ajustar el nivel de registro. Al establecer el nivel del archivo de registro, se recomienda elegir un nivel detallado como `Debug` o `Info`.

El archivo de registro del servidor puede consultarse desde la interfaz web o abrirse directamente desde el sistema de archivos, en el directorio de datos del servidor Nextcloud.

Consultar {nc-doc}`admin_manual/configuration_server/logging_configuration` en el manual de administración para más detalles sobre cómo configurar los niveles de registro y las ubicaciones de los archivos de registro.

#### Archivos de registro del servidor web

Puede ser útil consultar el archivo de registro de errores del servidor web para aislar cualquier problema relacionado con Nextcloud. En Apache sobre Linux, los registros de errores suelen estar en el directorio `/var/log/apache2`. Algunos archivos útiles son los siguientes:

- `error_log` – mantiene los errores asociados al código PHP.
- `access_log` – suele registrar todas las peticiones que atiende el servidor; es muy útil como herramienta de depuración, porque la línea de registro contiene información específica de cada petición y de su resultado.

Hay más información sobre el registro de Apache en `http://httpd.apache.org/docs/current/logs.html`.

### Volcados de memoria

En sistemas macOS y Linux, y en el improbable caso de que el software del cliente se bloquee, el cliente puede escribir un archivo de volcado de memoria. Obtener un archivo de volcado de memoria puede ayudar enormemente al servicio de atención al cliente de {vendor}`Nextcloud` en el proceso de depuración.

Para activar la escritura de archivos de volcado de memoria, hay que definir la variable de entorno `OWNCLOUD_CORE_DUMP` en el sistema.

Por ejemplo:

`` ` OWNCLOUD_CORE_DUMP=1 nextcloud ` ``

Este comando inicia el cliente con los volcados de memoria activados y guarda los archivos en el directorio de trabajo actual.

:::{note}
Los archivos de volcado de memoria pueden ser bastante grandes. Antes de activar los volcados de memoria en el sistema, asegurarse de tener espacio en disco suficiente para alojarlos. Además, debido a su tamaño, se recomienda encarecidamente comprimir adecuadamente cualquier archivo de volcado de memoria antes de enviarlo al servicio de atención al cliente de {vendor}`Nextcloud`.
:::

### Problemas conocidos de Citrix Workspace

- Estos son problemas conocidos al ejecutar el cliente de escritorio en un espacio de trabajo de Citrix:
  - El perfil móvil del usuario de Windows debe conservarse entre sesiones. No hacerlo provocará que los usuarios tengan que volver a configurar su cuenta en cada sesión nueva.
  - La carpeta de sincronización del usuario también debe conservarse entre sesiones. El cliente generará errores porque no encuentra la carpeta de sincronización cuando el usuario inicia sesión en una sesión nueva.
  - Cada vez que el usuario inicia sesión en un entorno Citrix, se crea una sesión con el cliente de escritorio y, en esa sesión, el cliente sincroniza los archivos del usuario, lo que puede hacer que el almacenamiento se quede rápidamente sin espacio.
````
