---
tipo: referencia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Dónde está el archivo de configuración del cliente de escritorio en cada sistema y algunos valores que pueden establecerse en él."
---
# Archivo de configuración

## Resumen

Esta página indica dónde se encuentra el archivo de configuración del cliente de escritorio en Linux, Windows y macOS, y describe algunos de los valores que pueden establecerse en él. Está dirigida a usuarios que necesitan ajustar el cliente más allá de su diálogo de configuración.

````{upstream} user_manual/desktop/configfile.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El cliente de {vendor}`Nextcloud` lee un archivo de configuración. Este archivo de configuración se encuentra en las siguientes ubicaciones:

- En distribuciones Linux: `$HOME/.config/Nextcloud/nextcloud.cfg`
- En sistemas Microsoft Windows: `%APPDATA%\Nextcloud\nextcloud.cfg`
- En sistemas macOS:
  - A partir de la versión 33.0.0: `$HOME/Library/Containers/com.nextcloud.desktopclient/Data/Library/Preferences/Nextcloud/nextcloud.cfg`
  - En versiones anteriores: `$HOME/Library/Preferences/Nextcloud/nextcloud.cfg`

:::{note}
En un espacio de trabajo de Citrix, el perfil móvil del usuario debe conservarse entre sesiones. Si no se hace, los usuarios tendrán que volver a configurar su cuenta en cada nueva sesión.
:::

El archivo de configuración contiene los ajustes en el formato de archivo .ini de Microsoft Windows. Los cambios pueden sobrescribirse mediante el diálogo de configuración de Nextcloud.

:::{note}
Tener precaución al modificar el archivo de configuración del cliente de {vendor}`Nextcloud`. Una configuración incorrecta puede producir resultados no deseados.
:::

Algunos valores de interés que pueden establecerse en el archivo de configuración son:

**Sección `[Nextcloud]`**

| Variable | Valor predeterminado | Significado |
|---|---|---|
| `remotePollInterval` | `30000` (30 s) | Especifica el intervalo de sondeo del repositorio remoto en milisegundos. |
| `forceSyncInterval` | `7200000` (2 h) | El tiempo sin actividad tras el cual se desencadena automáticamente una ejecución de sincronización. |
| `fullLocalDiscoveryInterval` | `3600000` (1 h) | El intervalo tras el cual la siguiente sincronización realizará un descubrimiento local completo. |
| `notificationRefreshInterval` | `60000` (1 min) | Especifica el intervalo predeterminado de comprobación de nuevas notificaciones del servidor en milisegundos. |

**Sección `[General]`**

| Variable | Valor predeterminado | Significado |
|---|---|---|
| `chunkSize` | `10000000` (10 MB) | Especifica el tamaño de fragmento de los archivos subidos en bytes. El cliente ajustará dinámicamente este tamaño dentro de los límites máximo y mínimo (ver más abajo). |
| `forceLoginV2` | `false` | Si el cliente debe forzar el nuevo flujo de inicio de sesión, aunque algunas circunstancias puedan requerir el flujo antiguo. |
| `minChunkSize` | `5000000` (5 MB) | Especifica el tamaño mínimo de fragmento de los archivos subidos en bytes. |
| `maxChunkSize` | `5000000000` (5000 MB) | Especifica el tamaño máximo de fragmento de los archivos subidos en bytes. |
| `targetChunkUploadDuration` | `60000` (1 minuto) | Duración objetivo en milisegundos de la subida de cada fragmento. El cliente ajusta el tamaño de fragmento hasta que la subida de cada fragmento tarde aproximadamente ese tiempo. Establecer en 0 para deshabilitar el ajuste dinámico del tamaño de fragmento. |
| `promptDeleteAllFiles` | `false` | Si un aviso de la interfaz debe pedir confirmación cuando se detecta que se eliminaron todos los archivos y carpetas. |
| `timeout` | `300` | El tiempo de espera de las conexiones de red en segundos. |
| `moveToTrash` | `false` | Si los archivos eliminados de forma no local deben moverse a la papelera en lugar de eliminarse por completo. |
| `showExperimentalOptions` | `false` | Si se muestran en la interfaz de usuario las opciones experimentales que aún están en pruebas. Activarlo no habilita por sí solo ningún comportamiento experimental. Sí habilita opciones de la interfaz de usuario que pueden usarse para optar por funciones experimentales. |
| `showMainDialogAsNormalWindow` | `false` | Si el diálogo principal debe mostrarse como una ventana normal aunque haya iconos de bandeja disponibles. |

**Sección `[Proxy]`**

| Variable | Valor predeterminado | Significado |
|---|---|---|
| `host` | `127.0.0.1` | La dirección del servidor proxy. |
| `port` | `8080` | El puerto en el que escucha el proxy. |
| `type` | `2` | `0` para el proxy del sistema. `1` para un proxy SOCKS5. `2` para no usar proxy. `3` para un proxy HTTP(S). |
````
