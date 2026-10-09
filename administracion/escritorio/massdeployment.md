---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Implementar el cliente de escritorio de forma gestionada: opciones del instalador MSI, creación de cuentas sin interacción y preconfiguración del asistente."
---
# Implementación y configuración del cliente de escritorio

## Resumen

Esta página describe las opciones de implementación y configuración del cliente de escritorio pensadas para administradores: personalizar la instalación en Windows con el instalador MSI, crear una cuenta desde la línea de comandos sin interacción del usuario y precargar o restringir el asistente de configuración. Está dirigida a quienes preparan despliegues gestionados del cliente.

````{upstream} admin_manual/desktop/massdeployment.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Este capítulo describe las opciones de implementación y configuración del cliente de escritorio de Nextcloud destinadas a administradores.

Estas opciones están pensadas para despliegues gestionados y otros escenarios administrativos, como scripts de implementación, plataformas de gestión de software, scripts de inicio de sesión, flujos de trabajo de MDM o RMM y otros procesos automatizados de instalación o configuración.

Según los objetivos de la implementación, el cliente de escritorio puede usarse de varias maneras:

- personalizar el comportamiento de la instalación en Windows,
- crear una cuenta automáticamente durante la implementación, sin interacción del usuario, o
- precargar o restringir el asistente de configuración interactivo.

### Elegir el enfoque adecuado

Usar la opción que mejor se ajuste al objetivo de la implementación:

- **Quiero personalizar cómo se instala el cliente en sistemas Windows gestionados.** Consultar {nc-ref}`windows-installation-customization`.

- **Quiero crear una cuenta de forma silenciosa durante la implementación.** Consultar {nc-ref}`non-interactive-account-provisioning`.

- **Quiero que los usuarios completen la configuración de forma interactiva, pero con valores predefinidos o restricciones.** Consultar {nc-ref}`interactive-wizard-preconfiguration`.

(nc-windows-installation-customization)=
### Opciones avanzadas de implementación en Windows

Si solo se quiere instalar el cliente de escritorio en el sistema local, basta con ejecutar el archivo `.msi` y seguir el asistente de instalación.

Las siguientes opciones están pensadas para instalaciones avanzadas en Windows, por ejemplo al automatizar la implementación o al personalizar las funciones instaladas.

:::{note}
La personalización de la instalación en Windows controla cómo se instala el cliente. Por sí sola no crea ni configura una cuenta en el cliente de escritorio. Si se quiere configurar una cuenta después de la instalación, consultar {nc-ref}`non-interactive-account-provisioning` o {nc-ref}`interactive-wizard-preconfiguration`.
:::

#### Funciones

El instalador MSI ofrece varias funciones que pueden instalarse o quitarse por separado y que también pueden controlarse desde la línea de comandos. Si se está automatizando la instalación, ejecutar el siguiente comando:

```
msiexec /passive /i Nextcloud-x.y.z-x64.msi
```

El comando instala el cliente en la ubicación predeterminada, con las funciones predeterminadas activadas.

Si se quieren desactivar, por ejemplo, los iconos de acceso directo en el escritorio, el comando puede cambiarse por el siguiente:

```
msiexec /passive /i Nextcloud-x.y.z-x64.msi REMOVE=DesktopShortcut
```

Consultar la siguiente tabla para ver la lista de funciones disponibles:

| Función | Activada de forma predeterminada | Descripción | Propiedad para desactivarla |
|---|---|---|---|
| Client | Sí, obligatoria | El cliente propiamente dicho | |
| DesktopShortcut | Sí | Añade un acceso directo en el escritorio | `NO_DESKTOP_SHORTCUT` |
| StartMenuShortcuts | Sí | Añade un acceso directo en el menú Inicio | `NO_START_MENU_SHORTCUTS` |
| ShellExtensions | Sí | Añade la integración con el Explorador | `NO_SHELL_EXTENSIONS` |

#### Instalación

También puede optarse por instalar solo el cliente propiamente dicho con el siguiente comando:

```
msiexec /passive /i Nextcloud-x.y.z-x64.msi ADDDEFAULT=Client
```

Por ejemplo, si se quiere instalar todo excepto las funciones `DesktopShortcut` y `ShellExtensions`, hay dos posibilidades:

1. Nombrar explícitamente todas las funciones que realmente se quieren instalar (lista blanca); `Client` se instala siempre de todos modos:

   ```
   msiexec /passive /i Nextcloud-x.y.z-x64.msi ADDDEFAULT=StartMenuShortcuts
   ```

2. Pasar las propiedades `NO_DESKTOP_SHORTCUT` y `NO_SHELL_EXTENSIONS`:

   ```
   msiexec /passive /i Nextcloud-x.y.z-x64.msi NO_DESKTOP_SHORTCUT="1" NO_SHELL_EXTENSIONS="1"
   ```

:::{note}
El `.msi` de Nextcloud recuerda estas propiedades, por lo que no hace falta volver a indicarlas en las actualizaciones.
:::

:::{note}
No pueden usarse para cambiar las funciones instaladas después de la instalación. Para hacerlo, consultar la sección siguiente.
:::

#### Cambiar las funciones instaladas

Las funciones instaladas pueden cambiarse más adelante con las propiedades `REMOVE` y `ADDDEFAULT`.

Para añadir más adelante el acceso directo en el escritorio, ejecutar el siguiente comando:

```
msiexec /passive /i Nextcloud-x.y.z-x64.msi ADDDEFAULT="DesktopShortcut"
```

Para quitarlo, ejecutar el siguiente comando:

```
msiexec /passive /i Nextcloud-x.y.z-x64.msi REMOVE="DesktopShortcut"
```

Windows lleva el registro de las funciones instaladas, y `REMOVE` o `ADDDEFAULT` afectan solo a las funciones indicadas.

:::{note}
No puede indicarse `REMOVE` en la instalación inicial, ya que desactivaría todas las funciones.
:::

#### Carpeta de instalación

La carpeta de instalación puede ajustarse indicando la propiedad `INSTALLDIR`:

```
msiexec /passive /i Nextcloud-x.y.z-x64.msi INSTALLDIR="C:\Program Files\Non Standard Nextcloud Client Folder"
```

Hay que tener cuidado al usar PowerShell en lugar de `cmd.exe`: escapar correctamente los espacios en blanco puede ser complicado.

Indicar `INSTALLDIR` de esta forma solo funciona en la primera instalación; no basta con volver a ejecutar el `.msi` con otra ruta. Si aun así hay que cambiarla, desinstalar primero el cliente y luego reinstalarlo en la nueva ubicación.

#### Desactivar las actualizaciones automáticas

Para desactivar las actualizaciones automáticas, pasar la propiedad `SKIPAUTOUPDATE`:

```
msiexec /passive /i Nextcloud-x.y.z-x64.msi SKIPAUTOUPDATE="1"
```

#### Iniciar después de la instalación

Para iniciar el cliente automáticamente después de la instalación, pasar la propiedad `LAUNCH`:

```
msiexec /i Nextcloud-x.y.z-x64.msi LAUNCH="1"
```

Esta opción también quita la casilla que permite a los usuarios decidir si se inicia el cliente durante las instalaciones que no son pasivas ni silenciosas.

:::{note}
Esta opción no tiene ningún efecto sin interfaz gráfica.
:::

#### Sin reinicio después de la instalación

El cliente programa un reinicio después de la instalación para asegurarse de que la extensión del Explorador se carga o descarga correctamente. Si los reinicios se gestionan por cuenta propia, puede establecerse la propiedad `REBOOT`:

```
msiexec /i Nextcloud-x.y.z-x64.msi REBOOT=ReallySuppress
```

Esto hace que `msiexec` termine con el error `ERROR_SUCCESS_REBOOT_REQUIRED` (3010). Si las herramientas de implementación lo interpretan como un error real y se quiere evitar, puede convenir establecer en su lugar `DO_NOT_SCHEDULE_REBOOT`:

```
msiexec /i Nextcloud-x.y.z-x64.msi DO_NOT_SCHEDULE_REBOOT="1"
```

(nc-non-interactive-account-provisioning)=
### Aprovisionamiento de cuentas no interactivo

El cliente de escritorio de Nextcloud admite el aprovisionamiento de cuentas no interactivo desde la línea de comandos.

Está pensado para la automatización de implementaciones y otros escenarios de instalación gestionada en los que un administrador quiere crear una cuenta en el cliente de escritorio sin que el usuario tenga que pasar por el asistente de configuración gráfico.

En un flujo de implementación típico, primero se implementa el paquete del cliente de escritorio y después se invoca el ejecutable del cliente de escritorio con los parámetros de aprovisionamiento como parte de la automatización.

Cuando se proporcionan los parámetros obligatorios, el cliente intenta crear una cuenta y guardarla en su configuración habitual, de modo que los inicios posteriores se comporten como si la cuenta se hubiera añadido mediante la interfaz gráfica de usuario.

Si la creación de la cuenta tiene éxito, el cliente termina con el código `0`. Si la creación de la cuenta falla, el cliente termina con el código `1`.

La información detallada de estado y de errores se escribe en los registros del cliente de escritorio.

:::{note}
Este flujo de trabajo es distinto de la preconfiguración interactiva del asistente. Si se quiere precargar o restringir el asistente de configuración en lugar de aprovisionar directamente una cuenta, consultar {nc-ref}`interactive-wizard-preconfiguration`.
:::

#### Parámetros obligatorios

Los siguientes parámetros son obligatorios para el aprovisionamiento de cuentas no interactivo:

- `--userid`: el ID de usuario que se configurará en el cliente de escritorio.

- `--apppassword`: la contraseña de aplicación que se usará para la autenticación.

  Deben usarse contraseñas de aplicación en lugar de la contraseña de inicio de sesión habitual del usuario. Consultar la documentación del servidor sobre el flujo de inicio de sesión y el proceso de generación de contraseñas de aplicación.

- `--serverurl`: la URL base del servidor Nextcloud que se usará para la cuenta.

#### Parámetros opcionales

- `--localdirpath`: la ruta local que se usará para la carpeta de sincronización.

  Si se omite, el cliente de escritorio elige la ubicación predeterminada habitual de la carpeta de sincronización en la plataforma.

  Si se indica esta opción y el directorio de destino ya existe y no está vacío, el aprovisionamiento de la cuenta falla.

  Si se indica esta opción y el directorio aún no existe, el cliente intenta crearlo.

- `--remotedirpath`: la ruta remota que se sincronizará.

  Si se omite, el valor predeterminado es `/` (la raíz de la cuenta en el servidor).

  Ejemplo: si el servidor contiene carpetas como `/Photos`, `/Documents` y `/Music`, indicar `/Music` crea una conexión de sincronización para esa subcarpeta remota en lugar de para toda la raíz de la cuenta.

- `--isvfsenabled`: controla si la conexión de sincronización creada debe usar archivos virtuales.

  Usar `1` para activar los archivos virtuales y `0` para desactivarlos.

  La compatibilidad con archivos virtuales depende de la compilación del cliente, del sistema operativo y de la disponibilidad en tiempo de ejecución de la funcionalidad de archivos virtuales necesaria. Activar esta opción solo en plataformas y compilaciones en las que los archivos virtuales sean compatibles.

- `--confdir`: anula el directorio de configuración que usa el proceso del cliente.

  Es una opción general del cliente, no una opción específica del aprovisionamiento. Solo hace falta si se quiere usar intencionadamente un directorio de configuración no predeterminado.

  Si se usa esta opción durante el aprovisionamiento, los inicios posteriores del cliente de escritorio deben usar el mismo directorio de configuración; de lo contrario, puede que la cuenta aprovisionada no aparezca en sesiones posteriores de la interfaz gráfica.

#### Comportamiento

Al iniciarse con los parámetros de aprovisionamiento obligatorios, el cliente de escritorio intenta:

1. validar los parámetros de línea de comandos proporcionados,
2. crear la carpeta de sincronización local si hace falta,
3. autenticarse en el servidor con la contraseña de aplicación proporcionada,
4. verificar el acceso al servidor, y
5. guardar la cuenta resultante en la configuración habitual del cliente.

En los inicios posteriores, la cuenta configurada está disponible como una cuenta normal del cliente de escritorio, siempre que el cliente se inicie con el mismo contexto de configuración.

:::{important}
El cliente de escritorio no monta el servidor en la ruta local como un sistema de archivos de red. Crea una conexión de sincronización. Una carpeta local vacía no significa por sí sola que el aprovisionamiento haya fallado.
:::

#### Casos de error habituales

El aprovisionamiento de cuentas puede fallar por motivos como estos:

- faltan uno o más parámetros obligatorios o no son válidos,
- ya existe una cuenta para el mismo usuario y servidor,
- la carpeta de sincronización local indicada ya existe y no está vacía,
- no se pudo crear la carpeta de sincronización local indicada,
- la URL del servidor es incorrecta,
- la contraseña de aplicación no es válida,
- la petición autenticada se redirige de forma inesperada,
- el servidor deniega el acceso a la cuenta configurada, o
- el servidor devuelve una respuesta no válida a la petición WebDAV autenticada.

En estos casos, el cliente termina con el código `1` y escribe información más detallada en los registros.

#### Ejemplos

Windows:

```powershell
"C:\Program Files\Nextcloud\nextcloud.exe" ^
  --userid admin ^
  --apppassword Jliy12356785jxnHa2ZCiZ9MX48ncECwDso95Pq3a5HABjY34ZvhZiXrPfpKWUg7aOHAX5 ^
  --serverurl https://cloud.example.com ^
  --localdirpath "D:\Nextcloud-sync-folder" ^
  --remotedirpath /Music ^
  --isvfsenabled 1
```

Linux:

```bash
nextcloud \
  --userid admin \
  --apppassword Jliy12356785jxnHa2ZCiZ9MX48ncECwDso95Pq3a5HABjY34ZvhZiXrPfpKWUg7aOHAX5 \
  --serverurl https://cloud.example.com \
  --localdirpath "/home/admin/Nextcloud-sync-folder" \
  --remotedirpath /Music \
  --isvfsenabled 0
```

macOS:

```bash
nextcloud \
  --userid admin \
  --apppassword Jliy12356785jxnHa2ZCiZ9MX48ncECwDso95Pq3a5HABjY34ZvhZiXrPfpKWUg7aOHAX5 \
  --serverurl https://cloud.example.com \
  --localdirpath "/Users/admin/Nextcloud-sync-folder" \
  --remotedirpath /Music \
  --isvfsenabled 1
```

#### Recomendaciones

Para una automatización de implementaciones fiable:

- usar contraseñas de aplicación en lugar de las contraseñas habituales de los usuarios,
- asegurarse de que la URL del servidor es la URL base correcta de la instancia de Nextcloud,
- usar un directorio de sincronización local nuevo o vacío,
- validar que la ruta remota de destino existe y que el usuario puede acceder a ella,
- activar `--isvfsenabled` solo en plataformas y compilaciones compatibles, y
- evitar `--confdir` salvo que se necesite intencionadamente una ubicación de configuración no predeterminada.

(nc-interactive-wizard-preconfiguration)=
### Preconfiguración del asistente interactivo

Si se quiere automatizar el asistente de configuración de cuentas para que los usuarios no tengan que introducir en la interfaz la URL del servidor ni la ruta de la carpeta de sincronización local, pueden usarse parámetros de línea de comandos.

Cuando se indican ambos, el asistente de configuración de cuentas del cliente de escritorio pasa directamente a abrir un navegador para la autenticación o la conexión de la cuenta, sin necesidad de introducir ninguno de los datos de conexión.

Además, como carpeta de sincronización local se selecciona la que se indique, en lugar de usar la ruta predeterminada.

Se admiten los siguientes parámetros:

- `--overridelocaldir`: indica un directorio local que se usará en el asistente de configuración de cuentas.

  Ejemplo: `/home/nextcloud-sync-folder`

- `--overrideserverurl`: indica una URL de servidor que se usará para la anulación forzada en el asistente de configuración de cuentas.

  Ejemplo: `https://cloud.example.com`

#### Comportamiento

Estas opciones afectan al comportamiento del asistente de configuración interactivo. No crean directamente una cuenta del mismo modo que el aprovisionamiento de cuentas no interactivo.

Usar este enfoque cuando se quiere que el usuario complete la configuración de forma interactiva, pero se desea precargar, restringir o guiar el proceso.

#### Ejemplos

Windows:

```powershell
"C:\Program Files\Nextcloud\nextcloud.exe" --overridelocaldir "D:/work/nextcloud-sync-folder" --overrideserverurl https://cloud.example.com
```

Linux y macOS:

```bash
nextcloud --overridelocaldir "/home/<user>/nextcloud-sync-folder" --overrideserverurl https://cloud.example.com
```

#### Diferencia importante con el aprovisionamiento no interactivo

Usar la preconfiguración del asistente cuando se sigue queriendo que el usuario complete la configuración en la interfaz gráfica.

Usar el aprovisionamiento de cuentas no interactivo cuando se quiere que la automatización de la implementación cree la cuenta directamente.

En otras palabras:

- el aprovisionamiento no interactivo crea la cuenta automáticamente;
- la preconfiguración del asistente influye en el asistente de configuración, pero sigue dependiendo de que la configuración se complete de forma interactiva.

### Resumen

El cliente de escritorio de Nextcloud admite varios flujos de implementación y configuración destinados a administradores.

Elegir el flujo de trabajo que mejor se ajuste al entorno:

- usar las opciones avanzadas de implementación en Windows para controlar el comportamiento de la instalación en sistemas Windows gestionados,
- usar el aprovisionamiento de cuentas no interactivo para crear cuentas del cliente de escritorio automáticamente durante la implementación,
- usar la preconfiguración del asistente interactivo para guiar a los usuarios por un proceso de configuración inicial restringido o precargado.
````
