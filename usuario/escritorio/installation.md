---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Descargar e instalar el cliente de escritorio en Windows, macOS y Linux, sus requisitos y la configuración inicial con el asistente."
---
# Instalación

## Resumen

Esta página explica dónde descargar el cliente de escritorio, qué sistemas y versiones de servidor admite, cómo instalarlo en macOS, Windows y Linux, y cómo completar el asistente de configuración inicial. Está dirigida a usuarios que instalan el cliente en su equipo.

````{upstream} user_manual/desktop/installation.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Descarga

La última versión del cliente de sincronización de escritorio de Nextcloud puede descargarse desde la [página de descargas de Nextcloud][Nextcloud download page]. Hay clientes disponibles para Linux, macOS y Microsoft Windows.

En la página de descargas también hay enlaces a archivos de código fuente y a versiones anteriores.

### Versiones de servidor compatibles

Cada versión del cliente de escritorio es compatible con las tres últimas versiones principales estables del servidor Nextcloud en el momento de su publicación. Consultar el [calendario de publicaciones de Nextcloud Server][Nextcloud Server release schedule] para conocer las versiones principales compatibles.

### Requisitos del sistema

- Windows 10+ (solo 64 bits)
- macOS 12.0+ (solo 64 bits)
- Linux (Ubuntu 24.04 u openSUSE 15.5 o Alma 8 o ...) (solo 64 bits)

  Para las distribuciones Linux, damos soporte, si es técnicamente viable, a las versiones LTS actuales. A BSD le damos soporte si es técnicamente viable, pero no lo probamos.

:::{note}
No damos soporte a Citrix.

- Haremos todo lo posible por asesorar a los usuarios de Citrix desde el punto de vista del cliente de escritorio.
- Corregiremos los problemas que también puedan reproducirse en los sistemas estándar compatibles.
- Todo lo demás queda fuera de nuestro alcance.
:::

### Instalación en macOS y Windows

La instalación en macOS y Windows es igual que la de cualquier otra aplicación de software: descargar el programa, hacer doble clic en él para iniciar la instalación y seguir el asistente de instalación. Una vez instalado y configurado, el cliente de escritorio se mantiene actualizado automáticamente; consultar {nc-doc}`El actualizador automático <user_manual/desktop/autoupdate>` para más información.

Para opciones de despliegue orientadas a administradores, como la configuración avanzada del MSI de Windows, el aprovisionamiento no interactivo de cuentas y la preconfiguración del asistente por línea de comandos, consultar el capítulo del manual de administración sobre el despliegue y la configuración del cliente de escritorio.

### Instalación en Linux

Para Linux, {vendor}`Nextcloud` ofrece oficialmente el cliente de escritorio como AppImage en la [página de descargas de Nextcloud][Nextcloud download page].

Algunas distribuciones Linux también ofrecen el cliente de escritorio de {vendor}`Nextcloud` a través de sus gestores de paquetes. Estos paquetes los mantiene la distribución o la comunidad, no {vendor}`Nextcloud`. Si se prefiere una instalación gestionada por paquetes, consultar la documentación de la distribución.

Los usuarios de Linux también deben tener habilitado un gestor de contraseñas, como GNOME Keyring o KWallet, para que el cliente de escritorio pueda iniciar sesión automáticamente.

### Configuración inicial

Tras la instalación, se abre el asistente de configuración inicial. En el asistente de configuración se puede iniciar sesión en el servidor, crear una cuenta con un proveedor y configurar qué carpetas sincronizar. El asistente guía paso a paso por las opciones de configuración esenciales y la configuración básica de la cuenta.

Primero, hay que introducir la URL del servidor Nextcloud.

La pantalla muestra un formulario para elegir entre iniciar sesión y registrarse.

Si ya se tiene una cuenta en una instancia de Nextcloud, hacer clic en `Login to your
Nextcloud`. Si todavía no se tiene una instancia de Nextcloud o una cuenta, puede que haya que crear una primero.
Como alternativa, puede registrarse una cuenta con un proveedor. En ese caso, pulsar `Create account with Provider`.

:::{note}
Es posible que la compilación del cliente de escritorio que se está usando se haya creado sin soporte para proveedores. En ese caso, no se verá esta pantalla y se pasará directamente a la siguiente.
:::

Introducir la URL de la instancia de Nextcloud. La URL es la misma que se escribe en el navegador para acceder a la instancia de Nextcloud.

Ahora el navegador web debería abrirse y pedir que se inicie sesión en la instancia de Nextcloud. Introducir el nombre de usuario y la contraseña en el navegador web y hacer clic en *Conceder acceso* cuando se solicite. Después, volver al asistente.

:::{note}
Puede que no sea necesario introducir el nombre de usuario y la contraseña si ya se ha iniciado sesión en el navegador web.
:::

En la pantalla de opciones de la carpeta local, se pueden sincronizar todos los archivos del servidor Nextcloud o seleccionar carpetas individuales. La carpeta de sincronización local predeterminada es `Nextcloud`, en el directorio personal. También puede cambiarse.

Una vez seleccionadas las carpetas de sincronización, hacer clic en el botón *Conectar*. El cliente intentará conectarse al servidor Nextcloud. Si lo consigue, el asistente se cerrará solo. Después se puede observar la actividad de sincronización y abrir el diálogo principal haciendo clic en el icono de la bandeja.

[Nextcloud download page]: https://nextcloud.com/download/#install-clients
[Nextcloud Server release schedule]: https://github.com/nextcloud/server/wiki/Maintenance-and-Release-Schedule
````
