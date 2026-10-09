---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Imponer nombres de archivo válidos en Windows: activarlo desde la interfaz web o con occ, sus consecuencias y cómo sanear los nombres no válidos."
---
# Nombres de archivo compatibles con Windows

## Resumen

Esta página explica cómo imponer nombres de archivo válidos en Windows, desde la interfaz web o con un comando `occ`, qué ajustes de configuración cambia y cómo renombrar los archivos con nombres no válidos. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/windows_compatible_filenames.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Esta función se introdujo en Nextcloud 31.
:::

De forma predeterminada, Nextcloud admite todos los nombres de archivo que son válidos en el servidor subyacente. Como Nextcloud solo se ejecuta en sistemas operativos compatibles con POSIX (Linux), esto significa que Nextcloud también admite nombres de archivo que no son válidos en los sistemas Microsoft Windows.

Si los usuarios usan Windows y los clientes Nextcloud Desktop para sincronizar su trabajo con su equipo, pueden encontrarse con archivos creados en la interfaz web o en una máquina Linux que no pueden sincronizarse porque el nombre de archivo no es válido.

Para resolver este problema, es posible imponer únicamente nombres de archivo válidos en Windows; esto, por ejemplo, prohíbe en los nombres de archivo caracteres como `*` o nombres de archivo como `AUX.txt` (en Windows, `AUX` es un nombre reservado y no puede usarse).

:::{note}
Activar este ajuste no impondrá la insensibilidad a mayúsculas y minúsculas, ya que los sistemas Windows modernos admiten nombres de archivo que distinguen entre mayúsculas y minúsculas.
:::

### Activar los nombres de archivo compatibles con Windows

Esta función puede activarse desde la interfaz web o mediante un comando `occ`.

:::{note}
Esta función actúa estableciendo un conjunto predefinido de ajustes de configuración del sistema. Por tanto, después de activarla se ajustará el `config.php`, lo que también significa que activar esta función requiere una configuración con permisos de escritura.
:::

#### Desde la interfaz web

El ajuste se encuentra en {guilabel}`Configuraciones de administración`, en {guilabel}`Ajustes básicos`. En la sección {guilabel}`Compatibilidad de archivos` puede activarse la compatibilidad con Windows.

#### Con el comando occ

:::{note}
Este comando se introdujo en Nextcloud 32.
:::

Para activar o desactivar rápidamente la función, se proporciona un {nc-ref}`comando occ <occ_files_windows_filenames>`.

### Consecuencias

Después de activar los nombres de archivo compatibles con Windows, los usuarios no pueden crear ni modificar archivos con nombres de archivo no válidos. Pero sí pueden seguir eliminando esos archivos o renombrándolos (con nombres válidos).

Esto funciona estableciendo un conjunto predefinido de ajustes de configuración:

- `forbidden_filename_basenames` se establecerá en los nombres reservados en Windows.
- `forbidden_filename_characters` se establecerá en los caracteres no válidos para nombres de archivo en Windows.
- `forbidden_filename_extensions` se establecerá en las cadenas no permitidas como parte final, como un punto o espacios al final.

### Sanear los nombres de archivo no válidos

Después de activar la función, los usuarios tienen que ajustar manualmente todos los nombres de archivo no válidos para poder seguir trabajando con esos archivos.
Como alternativa, Nextcloud proporciona el comando {nc-ref}`occ files:sanitize-filenames <occ_files_sanitize_filenames>` para renombrar automáticamente todos los archivos no válidos.
````
