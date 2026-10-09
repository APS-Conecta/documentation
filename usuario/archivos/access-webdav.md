---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Conectar Linux, macOS, Windows y dispositivos móviles a los archivos por WebDAV: URL, montajes, clientes de terceros y problemas conocidos."
---
# Acceder a los archivos de Nextcloud mediante WebDAV

## Resumen

Esta página explica cómo conectar equipos Linux, macOS y Windows y dispositivos móviles a los archivos del servidor mediante WebDAV, con los clientes oficiales, con clientes de terceros, desde la línea de comandos y con cURL o WinSCP, además de los problemas conocidos y sus soluciones. Está dirigida a usuarios que quieren acceder a sus archivos fuera del navegador.

````{upstream} user_manual/files/access_webdav.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud es totalmente compatible con el protocolo WebDAV, y puede conectarse a Nextcloud Files y sincronizarse con él mediante WebDAV. Este capítulo explica cómo conectar dispositivos Linux, macOS, Windows y móviles a su servidor Nextcloud.

WebDAV significa Distributed Authoring and Versioning. Es una extensión de HTTP que facilita crear, leer y editar archivos alojados en servidores web remotos. Con un cliente WebDAV, puede acceder a Nextcloud Files (incluidos los recursos compartidos) en Linux, macOS y Windows de forma similar a cualquier recurso compartido de red remoto, y mantenerse sincronizado.

Antes de configurar WebDAV, revise la forma recomendada de conectar dispositivos cliente a Nextcloud.

### Clientes oficiales Nextcloud para escritorio y móviles

El modo recomendado de sincronizar un PC de escritorio con un servidor Nextcloud es usando [clientes oficiales de sincronización de Nextcloud](https://nextcloud.com/install/#install-clients). Puede configurar los clientes para guardar archivos en cualquier directorio local y puede elegir qué directorios sincronizar del servidor Nextcloud. El cliente muestra el estado de la conexión actual y registra toda la actividad, de modo que usted siempre pueda verificar que los archivos creados y actualizados en su ordenador estén adecuadamente sincronizados con el servidor.

El modo recomendado de sincronizar dispositivos Android o Apple iOS es utilizando las [aplicaciones oficiales móviles Nextcloud](https://nextcloud.com/install/).

Para conectar las aplicaciones oficiales Nextcloud a un servidor Nextcloud utilice el mismo URL que utiliza para acceder a Nextcloud desde su navegador web / p.ej.:

```
https://cloud.example.com
```

Si Nextcloud está instalado en un subdirectorio llamado «nextcloud»:

```
https://example.com/nextcloud
```

### Clientes WebDAV de terceros

Si lo prefiere, puede conectar su computador a su servidor Nextcloud utilizando cualquier cliente de terceros que soporte el protocolo WebDAV (incluyendo aquellos que podrían estar ya incluidos en su sistema operativo)

Puede utilizar clientes compatibles con WebDAV de terceros para conectar su dispositivo móvil a Nextcloud.

Cuando utilice clientes de terceros, tenga en cuenta que podrían no estar optimizados para su uso con Nextcloud o implementar funcionalidades que Ud. considere importantes para su caso de uso.

Los clientes móviles que los miembros de la comunidad de Nextcloud han reportado estar usando incluyen:

- [FolderSync (Android)](https://foldersync.io/)
- [WebDAV Navigator (iPhone)](https://apps.apple.com/us/app/webdav-navigator/id382551345)

La URL que debe utilizar cuando configure aplicaciones de terceros para conectarse a Nextcloud es un poco más larga que la que se usa para los clientes oficiales:

```
https://cloud.example.com/remote.php/dav/files/USERNAME/
```

Si Nextcloud está instalado en un subdirectorio llamado «nextcloud»:

```
https://example.com/nextcloud/remote.php/dav/files/USERNAME/
```

:::{note}
Cuando use un cliente WebDAV de terceros (incluido el cliente integrado de su sistema operativo), debe iniciar sesión con una contraseña de aplicación en lugar de su contraseña habitual. Además de mejorar la seguridad, esto [aumenta el rendimiento de forma significativa](https://github.com/nextcloud/server/issues/32729#issuecomment-1556667151). Para configurar una contraseña de aplicación, inicie sesión en la interfaz web de Nextcloud, haga clic en su avatar y elija *Ajustes personales*. Luego elija *Seguridad* en la barra lateral izquierda y desplácese hasta el final. Ahí puede crear una contraseña de aplicación (que también se puede revocar en el futuro sin cambiar la contraseña principal de su usuario).
:::

:::{note}
En los siguientes ejemplos, debe sustituir **example.com/nextcloud** por la URL de su servidor Nextcloud (omita la parte del directorio si la instalación está en la raíz de su dominio) y **USERNAME** por el nombre de usuario del usuario que se conecta.

Puede encontrar la URL de WebDAV en **Configuración de archivos**, en **WebDAV**, en su cuenta de Nextcloud.
:::

### Acceder a archivos desde Linux

Usted puede acceder a sus archivos desde sistemas operativos Linux utilizando los siguientes métodos.

#### Gestor de archivos Nautilus

**Cuando configure su cuenta de Nextcloud en el** {nc-doc}`Centro de control de GNOME <user_manual/groupware/sync_gnome>`**, Nautilus montará automáticamente sus archivos como recurso compartido WebDAV, a menos que desmarque el acceso a archivos**.

También puede montar sus archivos de Nextcloud manualmente. Utilice el protocolo `davs://` para conectar el gestor de archivos Nautilus a su carpeta compartida en Nextcloud:

```
davs://example.com/nextcloud/remote.php/dav/files/USERNAME/
```

:::{note}
Si la conexión con su servidor no está protegida con HTTPS, use `dav://` en lugar de `davs://`.
:::

:::{note}
El mismo método funciona con otros gestores de archivos que usan GVFS, como Caja de MATE y Nemo de Cinnamon.
:::

#### Acceder a archivos con KDE y Dolphin

1. Vaya a System Settings -> Networking -> Online Accounts
2. Haga clic en «Add Account...»
3. Haga clic en Nextcloud
4. Introduzca la dirección de su servidor
5. Siga las instrucciones en pantalla para iniciar sesión
6. Después de iniciar sesión, asegúrese de habilitar «Storage» en la sección «Use This Account For»
7. Ahora puede acceder a sus archivos en Dolphin, en «Network», en la barra lateral
8. (Opcional) Para añadir esta ubicación como acceso directo en la barra lateral, haga clic con el botón derecho en «Nextcloud Storage» y luego haga clic en «Add to Places»
9. (Opcional) Para personalizar el acceso directo, haga clic con el botón derecho en él en la barra lateral, luego haga clic en «Edit...» y personalice el icono y la etiqueta

### Crear una unidad WebDAV en la consola de Linux

Usted puede crear una unidad WebDAV desde la consola de Linux. Esto es útil si prefiere acceder a Nextcloud del mismo modo que cualquier otra unidad del sistema de archivos. El siguiente ejemplo muestra cómo crear una unidad personal y configurarla para que se monte automáticamente cada vez que inicie sesión en su ordenador Linux.

1. Instale el driver `davfs2` para el sistema de archivos WebDAV, que le permite montar unidades WebDAV como cualquier otro sistema de archivos remoto. Utilice este comando para instalarlo en Debian/Ubuntu:

   ```
   apt-get install davfs2
   ```

2. Utilice este comando para instalarlo en CentOS, Fedora y openSUSE:

   ```
   yum install davfs2
   ```

3. Añádase al grupo `davfs2`:

   ```
   usermod -aG davfs2 <username>
   ```

:::{note}
Si el grupo davfs2 no existe después de instalar el paquete, es posible que tenga que crearlo usted mismo y, posiblemente, ajustar el archivo de configuración de davfs para que use el grupo después de haberlo creado.
:::

4. A continuación, cree un directorio `nextcloud` en su directorio de usuario para el punto de montaje y `.davfs2/` para su archivo de configuración personal:

   ```
   mkdir ~/nextcloud
   mkdir ~/.davfs2
   ```

5. Copie `/etc/davfs2/secrets` a `~/.davfs2`:

   ```
   cp  /etc/davfs2/secrets ~/.davfs2/secrets
   ```

6. Establézcase como el propietario y seleccione permisos de lectura y escritura para el propietario exclusivamente:

   ```
   chown <linux_username>:<linux_username> ~/.davfs2/secrets
   chmod 600 ~/.davfs2/secrets
   ```

7. Añada sus credenciales de acceso a Nextcloud al final del archivo `secrets`, utilizando su URL del servidor Nextcloud y su nombre de usuario y contraseña de Nextcloud:

   ```
   https://example.com/nextcloud/remote.php/dav/files/USERNAME/ <username> <password>
   or
   $PathToMountPoint $USERNAME $PASSWORD
   for example
   /home/user/nextcloud john 1234
   ```

8. Añada la información de la unidad a `/etc/fstab`:

   ```
   https://example.com/nextcloud/remote.php/dav/files/USERNAME/ /home/<linux_username>/nextcloud davfs user,rw,auto 0 0
   ```

9. Y entonces compruebe que se monta y autentica, ejecutando el siguiente comando. Si lo ha configurado correctamente, no necesitará permisos de administrador:

   ```
   mount ~/nextcloud
   ```

10. También debería ser capaz de desmontarla:

    ```
    umount ~/nextcloud
    ```

Ahora cada vez que inicie sesión en su sistema Linux, su unidad Nextcloud debería montarse automáticamente vía WebDAV en su directorio `~/nextcloud`. Si prefiere montarlo manualmente, cambie `auto` por `noauto` en `/etc/fstab`.

### Problemas conocidos

#### Problema

Recurso temporalmente no disponible

#### Solución

Si tiene problemas al crear un archivo en el directorio, edite `/etc/davfs2/davfs2.conf` y añada:

```
use_locks 0
```

#### Problema

Avisos de certificados

#### Solución

Si utiliza un certificado auto-firmado, recibirá un aviso. Para evitarlo, configure `davfs2` para que reconozca su certificado. Copie `mycertificate.pem` a `/etc/davfs2/certs/`, edite `/etc/davfs2/davfs2.conf` y descomente la línea `servercert`. Entonces puede añadir la ruta del su certificado, como en este ejemplo:

```
servercert /etc/davfs2/certs/mycertificate.pem
```

### Acceder a archivos desde macOS

Para acceder archivos a través de Finder en macOS:

1. Desde la barra de menú de Finder, elija **Ir > Conectarse a un servidor...**.

2. Cuando la ventana **Conectarse a un servidor...** se abra, introduzca la dirección WebDAV del servidor Nextcloud en el campo **Dirección del servidor**, p. ej.:

   ```
   https://cloud.YOURDOMAIN.com/remote.php/dav/files/USERNAME/
   ```

3. Haga clic en **Conectar**. Su servidor WebDAV debería aparecer en el Escritorio como una unidad de disco compartido.

### Acceder a ficheros desde Microsoft Windows

Si utiliza la implementación nativa WebDAV de Windows, puede asignar Nextcloud a una nueva unidad utilizando el explorador de Windows. Asignar una unidad le permitirá explorar los archivos guardados en un servidor Nextcloud del mismo modo que lo haría con archivos guardados en una unidad de red.

Esta herramienta requiere conectividad a la red. Si quiere acceder a sus archivos sin conexión, utilice el Cliente de Escritorio para sincronizar todos sus archivos de Nextcloud en uno o más carpetas de su disco duro local.

:::{note}
En Windows 10, la autenticación básica está permitida de forma predeterminada cuando HTTPS está habilitado antes de asignar la unidad.

En versiones más antiguas de Windows, debe permitir el uso de la Autenticación Básica en el registro de Windows:

- Inicie `regedit` y vaya a `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WebClient\Parameters`.
- Cree o edite el valor `DWORD` `BasicAuthLevel` (Windows Vista, 7 y 8) o `UseBasicAuth` (Windows XP y Windows Server 2003) y establezca sus datos del valor en `1` para las conexiones SSL. Un valor de `0` significa que la autenticación básica está deshabilitada, y un valor de `2` permite conexiones SSL y no SSL (no recomendado).
- Después, salga del Editor del Registro y reinicie el equipo.
:::

#### Asignar unidades desde la línea de comandos

El siguiente ejemplo muestra cómo asignar una unidad utilizando la línea de comandos. Para asignar la unidad:

1. Abra un símbolo del sistema en Windows.
2. Introduzca la siguiente línea en el símbolo del sistema para asignar la unidad Z del equipo:

   ```
   net use Z: https://<drive_path>/remote.php/dav/files/USERNAME/ /user:youruser yourpassword
   ```

   con <drive_path> como la URL de su servidor Nextcloud. Por ejemplo:

   ```
   net use Z: https://example.com/nextcloud/remote.php/dav/files/USERNAME/ /user:youruser yourpassword
   ```

   El ordenador asigna a la unidad Z los archivos de su cuenta de Nextcloud.

:::{error}
Si recibe el siguiente error, `System error 67 has occurred. The network name cannot be found.`, o desconexiones frecuentes, abra la aplicación **Services** y asegúrese de que el servicio `WebClient` esté en ejecución y se inicie automáticamente al arrancar.
:::

:::{note}
Aunque no se recomienda, también puede montar el servidor Nextcloud mediante HTTP, dejando la conexión sin cifrar.

Si planea utilizar conexiones HTTP en cualquier dispositivo mientras está en un lugar público, le recomendamos con ahínco que utilice un túnel VPN para que este le provea la seguridad necesaria.

Una sintaxis alternativa del comando es:

```
net use Z: \\example.com@ssl\nextcloud\remote.php\dav /user:youruser
yourpassword
```
:::

#### Asignar unidades desde el Explorador de Archivos de Windows

Para asignar una unidad usando el Explorador de Archivos de Microsoft Windows:

1. Abra el Explorador de Windows en su equipo con MS Windows.
2. Haga clic con el botón derecho en la entrada **Computer** y seleccione **Map network drive…** en el menú desplegable.
3. Elija una unidad de red local a la que quiera asignar Nextcloud.
4. Especifique la dirección de su instancia de Nextcloud, seguida de **/remote.php/dav/files/USERNAME/**.

   Por ejemplo:

   ```
   https://example.com/nextcloud/remote.php/dav/files/USERNAME/
   ```

   :::{note}
   En los servidores protegidos con SSL, marque **Reconnect at sign-in** para que la asignación se mantenga en los reinicios posteriores. Si quiere conectarse al servidor Nextcloud como un usuario distinto, marque **Connect using different credentials**.
   :::

5. Haga clic en el botón `Finalizar`.

El Explorador de archivos de Windows asigna la unidad de red, dándole acceso a su instancia de Nextcloud.

### Acceder a archivos desde Cyberduck

[Cyberduck](https://cyberduck.io/) es un explorador de FTP, SFTP, WebDAV, OpenStack Swift y de Amazon S3 de código abierto, diseñado para la transferencia de archivos en macOS y Windows.

:::{note}
Este ejemplo usa la versión 4.2.1 de Cyberduck.
:::

Para utilizar Cyberduck:

1. Especifique un servidor sin el prefijo que indica el protocolo.

   Por ejemplo: `example.com`

2. Especifique el puerto apropiado.

   El puerto a elegir depende de si su servidor Nextcloud soporta SSL o no. Cyberduck requiere que seleccione un tipo de conexión distinto si planea utilizar SSL.

   Por ejemplo:

   - `80` para WebDAV sin cifrar
   - `443` para WebDAV seguro (HTTPS/SSL)

3. Utilice el menú desplegable 'Más Opciones' para añadir el resto de su URL WebDAV en el campo 'Ruta'.

   Por ejemplo: `remote.php/dav/files/USUARIO/`

Ahora Cyberduck le permite el acceso a ficheros de su servidor Nextcloud.

### Acceder a archivos compartidos públicamente a través de WebDAV

Nextcloud ofrece la posibilidad de acceder a archivos compartidos públicamente a través de WebDAV.

Para acceder a un archivo compartido públicamente, abra:

```
https://example.com/nextcloud/public.php/dav/files/USERNAME
```

En un cliente WebDAV, utilice el token del recurso compartido como el nombre de usuario y la contraseña del recurso compartido (opcional) como contraseña. Por ejemplo, en un enlace compartido <https://example.com/s/kFy9Lek5sm928xP>, `kFy9Lek5sm928xP` será el nombre de usuario.

:::{note}
**Ajustes** → **Administración** → **Compartir** → **Permitir a los usuarios en este servidor enviar recursos compartidos a otros servidores**. Esta opción también permite el acceso por WebDAV a los recursos compartidos públicos y debe estar habilitada para que esta función funcione, salvo si se usa cURL (véase más abajo).
:::

### Problemas conocidos

#### Problema

Windows no se conecta usando HTTPS.

#### Solución 1

Puede que el cliente WebDAV de Windows no soporte la indicación del nombre de servidor (Server Name Indication o SNI) en conexiones encriptadas. Si se encuentra con un error al asignar a una instancia encriptada por SSL de Nextcloud, contacte con su proveedor para que le asigne una dirección IP dedicada para su servidor con SSL.

#### Solución 2

Puede que el cliente de WebDAV de Windows no soporte conexiones TLSv1.1 y TLSv1.2. Si la configuración de su servidor está restringida a las versiones TLSv1.1 y superior, la conexión a su servidor puede fallar. Por favor, consulte la documentación de [WinHTTP][WinHTTP] para obtener más información.

#### Problema

Recibe el siguiente mensaje: **Error 0x800700DF: El tamaño del archivo excede el límite permitido y no puede ser guardado.**

#### Solución

Windows limita el tamaño máximo que puede tener un archivo transferido desde o hacia un recurso compartido WebDAV. Puede aumentar el valor `FileSizeLimitInBytes` en `HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\WebClient\\Parameters` haciendo clic en **Modify**.

Para aumentar el límite al valor máximo de 4GB, seleccione **Decimal**, introduzca el valor `4294967295` y reinicie Windows o reinicie el servicio **WebClient**.

#### Problema

Al añadir una unidad WebDAV en Windows con los pasos anteriores, no se muestra el espacio disponible correcto de Nextcloud, sino el tamaño y el espacio libre de la unidad C:.

#### Respuesta

Lamentablemente, se trata de una limitación del propio WebDAV, porque no ofrece al cliente ninguna forma de obtener del servidor el espacio libre disponible. Windows recurre automáticamente al tamaño y al espacio libre de la unidad C:. No hay una solución directa para esta limitación.

#### Problema

El acceso a sus archivos desde Microsoft Office a través de WebDAV falla.

#### Solución

Los problemas conocidos y sus soluciones están documentados en el artículo [KB2123563][KB2123563].

#### Problema

No se puede asignar Nextcloud a una unidad WebDAV en Windows utilizando un certificado auto-firmado.

#### Solución

1. Acceda a su instancia de Nextcloud en su navegador web preferido.
2. Haga clic hasta llegar al error de certificado en la línea de estado del navegador.
3. Vea el certificado y, luego, en la pestaña Details, seleccione «Copy to File».
4. Guarde el archivo en su escritorio con un nombre arbitrario, por ejemplo `myNextcloud.pem`.
5. Vaya a Start menu > Run, escriba MMC y haga clic en «OK» para abrir Microsoft Management Console.
6. Vaya a File > Add/Remove Snap-In.
7. Seleccione Certificates, haga clic en {guilabel}`Add`, elija «My User Account», luego «Finish» y, por último, «OK».
8. Profundice hasta Trust Root Certification Authorities, Certificates.
9. Haga clic con el botón derecho en Certificate y seleccione All Tasks e Import.
10. Seleccione el certificado guardado en el escritorio.
11. Seleccione Place all Certificates in the following Store y haga clic en Browse.
12. Marque la casilla Show Physical Stores, despliegue Trusted Root Certification Authorities, seleccione allí Local Computer, haga clic en «OK» y complete la importación.
13. Revise la lista para asegurarse de que aparece el certificado. Probablemente tendrá que usar Refresh antes de verlo.
14. Salga de MMC.

Para usuarios de Firefox:

1. Abra su navegador y vaya a Application menu > History > Clear recent history...
2. Seleccione «Everything» en el menú desplegable «Time range to clear»
3. Marque la casilla «Active Logins»
4. Haga clic en el botón «Clear now»
5. Cierre el navegador, vuelva a abrirlo y pruebe.

Para los usuarios que usan navegadores basados en Chrome (Chrome, Chromium, Microsoft Edge):

1. Abra el Panel de control de Windows y baje hasta Internet Options
2. En la pestaña Content, haga clic en el botón Clear SSL State.
3. Cierre el navegador, vuelva a abrirlo y pruebe.

### Acceder a archivos desde cURL.

Como WebDAV es una extensión de HTTP, se puede utilizar cURL para programar o automatizar operaciones sobre archivos.

:::{note}
**Ajustes** → **Administración** → **Compartir** → **Permitir a los usuarios en este servidor enviar recursos compartidos a otros servidores**. Si esta opción está deshabilitada, hay que pasar a cURL la opción `--header "X-Requested-With: XMLHttpRequest"`.
:::

Para crear una carpeta con la fecha actual como nombre:

```bash
$ curl -u user:pass -X MKCOL "https://example.com/nextcloud/remote.php/dav/files/USERNAME/$(date '+%d-%b-%Y')"
```

Para subir el archivo `error.log` a esa carpeta:

```bash
$ curl -u user:pass -T error.log "https://example.com/nextcloud/remote.php/dav/files/USERNAME/$(date '+%d-%b-%Y')/error.log"
```

Para mover un archivo:

```bash
$ curl -u user:pass -X MOVE --header 'Destination: https://example.com/nextcloud/remote.php/dav/files/USERNAME/target.jpg' https://example.com/nextcloud/remote.php/dav/files/USERNAME/source.jpg
```

Para obtener las propiedades de los archivos de la carpeta raíz:

```bash
$ curl -X PROPFIND -H "Depth: 1" -u user:pass https://example.com/nextcloud/remote.php/dav/files/USERNAME/ | xml_pp
<?xml version="1.0" encoding="utf-8"?>
<d:multistatus xmlns:d="DAV:" xmlns:oc="http://nextcloud.org/ns" xmlns:s="http://sabredav.org/ns">
  <d:response>
    <d:href>/nextcloud/remote.php/dav/files/USERNAME/</d:href>
    <d:propstat>
      <d:prop>
        <d:getlastmodified>Tue, 13 Oct 2015 17:07:45 GMT</d:getlastmodified>
        <d:resourcetype>
          <d:collection/>
        </d:resourcetype>
        <d:quota-used-bytes>163</d:quota-used-bytes>
        <d:quota-available-bytes>11802275840</d:quota-available-bytes>
        <d:getetag>"561d3a6139d05"</d:getetag>
      </d:prop>
      <d:status>HTTP/1.1 200 OK</d:status>
    </d:propstat>
  </d:response>
  <d:response>
    <d:href>/nextcloud/remote.php/dav/files/USERNAME/welcome.txt</d:href>
    <d:propstat>
      <d:prop>
        <d:getlastmodified>Tue, 13 Oct 2015 17:07:35 GMT</d:getlastmodified>
        <d:getcontentlength>163</d:getcontentlength>
        <d:resourcetype/>
        <d:getetag>"47465fae667b2d0fee154f5e17d1f0f1"</d:getetag>
        <d:getcontenttype>text/plain</d:getcontenttype>
      </d:prop>
      <d:status>HTTP/1.1 200 OK</d:status>
    </d:propstat>
  </d:response>
</d:multistatus>
```

### Acceder a archivos utilizando WinSCP

[WinSCP](https://winscp.net/eng/docs/introduction/) es un cliente SFTP, FTP, WebDAV, S3 y SCP gratuito y de código abierto para Windows. Su función principal es la transferencia de archivos entre un equipo local y uno remoto. WinSCP también ofrece funciones de scripting y de gestión básica de archivos.

Puede [descargar](https://winscp.net/eng/downloads.php/) la versión portatil de WinSCP y ejecutarla en Linux usando [Wine](https://wiki.winehq.org/Main_Page/).

Para ejecutar WinSCP en Linux, instale Wine con el gestor de paquetes de su distribución y luego ejecute: `wine WinSCP.exe`.

Para conectarse a Nextcloud:

- Inicie WinSCP
- Pulse «Session» en el menú
- Pulse la opción de menú «New Session»
- Establezca el desplegable «File protocol» en WebDAV
- Establezca el desplegable «Encryption» en TLS/SSL Implicit encryption
- Rellene el campo del nombre de host: `example.com`
- Rellene el campo del nombre de usuario: `NEXTCLOUDUSERNAME`
- Rellene el campo de la contraseña: `NEXTCLOUDPASSWORD`
- Pulse el botón «Advanced...»
- Vaya a «Environment», «Directories» en el lado izquierdo
- Rellene el campo «Remote directory» con lo siguiente: `/nextcloud/remote.php/dav/files/NEXTCLOUDUSERNAME/`
- Pulse el botón «OK»
- Pulse el botón {guilabel}`Save`
- Seleccione las opciones deseadas y pulse el botón «OK»
- Pulse el botón {guilabel}`Login` para conectarse a Nextcloud

:::{note}
Si usa TOTP, use una contraseña de aplicación. En el momento de escribir esto (2022-11-07), WinSCP no admite TOTP con Nextcloud.
:::

[WinHTTP]: https://msdn.microsoft.com/en-us/library/windows/desktop/aa382925.aspx#WinHTTP_5.1_Features
[KB2668751]: https://web.archive.org/web/20211008025539/https://support.microsoft.com/en-us/topic/you-cannot-download-more-than-50-mb-or-upload-large-files-when-the-upload-takes-longer-than-30-minutes-using-web-client-in-windows-7-8709ae9d-e808-c5a0-95d0-9a7143c50b11
[KB2123563]: https://support.microsoft.com/kb/2123563
````
