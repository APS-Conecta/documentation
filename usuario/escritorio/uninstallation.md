---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Cómo desinstalar el cliente de escritorio en Windows, macOS y Linux, y dónde queda la configuración del usuario, que la desinstalación no elimina."
---
# Desinstalación

## Resumen

Esta página explica cómo desinstalar el cliente de escritorio con las herramientas del sistema operativo en Windows, macOS y Linux, cómo eliminar sus datos relacionados y dónde se encuentra la configuración del usuario, que la desinstalación no elimina. Está dirigida a usuarios que retiran el cliente de su equipo.

````{upstream} user_manual/desktop/uninstallation.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Es seguro desinstalar el cliente de escritorio de archivos usando las herramientas integradas del sistema operativo.

### Instrucciones generales

En cada sistema operativo:

1. Asegurarse de *salir del cliente de escritorio* antes de eliminarlo.

2. *Desinstalar* el cliente de escritorio.

3. También puede ser necesario tener en cuenta que desinstalar el cliente de escritorio no eliminará el archivo de {nc-doc}`configuración del usuario <user_manual/desktop/configfile>` ni los datos sincronizados.

   Para eliminar los datos (carpetas de sincronización), considerar el uso de la función del servidor [borrado remoto](https://nextcloud.com/de/blog/nextcloud-desktop-client-2-6-1-brings-remote-wipe-dark-mode-support-to-mac-os-x-and-more/). Esta función está disponible en todos los clientes.

A continuación se encuentran las instrucciones específicas de cada plataforma.

#### Windows

Hay dos formas de eliminar el cliente de escritorio:

1. Usando *Agregar o quitar programas*.

2. Pueden usarse las opciones de línea de comandos de [msiexec](https://learn.microsoft.com/en-us/windows/win32/msi/standard-installer-command-line-options):

```shell
msiexec /uninstall Nextcloud-x.y.z-x64.msi /quiet``
```

3. La {nc-doc}`configuración del usuario <user_manual/desktop/configfile>` se encuentra en `%APPDATA%\Nextcloud\nextcloud.cfg`.

#### macOS

Además de eliminar el cliente de escritorio de la carpeta *Aplicaciones*, puede ser necesario eliminar también todos los datos relacionados, especialmente si se usan archivos virtuales.

1. Para simplemente desinstalar el software: puede hacerse desde el [Launchpad o el Finder](https://support.apple.com/en-us/102610).

2. Para eliminar por completo todos los datos relacionados, pueden usarse los siguientes comandos:

```bash
rm -rf "$HOME/Library/Application Scripts/com.nextcloud.desktopclient"*
rm -f  "$HOME/Library/Application Support/CrashReporter/Nextcloud_"*
rm -rf "$HOME/Library/Application Support/Nextcloud"
rm -rf "$HOME/Library/Caches/Nextcloud"
rm -rf "$HOME/Library/Containers/com.nextcloud.desktopclient"*
rm -rf "$HOME/Library/Group Containers/NKUJUXUJ3B.com.nextcloud.desktopclient"
rm -rf "$HOME/Library/Group Containers/com.nextcloud.desktopclient"
rm -f  "$HOME/Library/LaunchAgents/com.nextcloud.desktopclient.plist"
rm -rf "$HOME/Library/Preferences/Nextcloud"
rm -f  "$HOME/Library/Preferences/com.nextcloud.desktopclient.plist"
```

3. A partir de la versión 33.0.0, la {nc-doc}`configuración del usuario <user_manual/desktop/configfile>` se encuentra en `$HOME/Library/Containers/com.nextcloud.desktopclient/Data/Library/Preferences/Nextcloud/nextcloud.cfg`.
   En versiones anteriores se encuentra en `$HOME/Library/Preferences/Nextcloud/nextcloud.cfg`.

#### Linux

Depende de cómo se haya instalado el cliente de escritorio:

1. Si se usa la AppImage de Nextcloud, basta con eliminar el archivo AppImage.

2. Si se usó el gestor de paquetes para instalar el cliente de escritorio, también puede usarse para desinstalar el cliente de escritorio. Por ejemplo, en Ubuntu puede usarse el siguiente comando:

```bash
sudo apt remove nextcloud-desktop
```

3. La {nc-doc}`configuración del usuario <user_manual/desktop/configfile>` se encuentra en *$HOME/.config/Nextcloud/nextcloud.cfg*.
````
