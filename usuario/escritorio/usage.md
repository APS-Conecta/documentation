---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Uso del cliente de escritorio: iconos de estado, menú de la bandeja, ajustes de cuenta, estado de usuario, compartir, red y editor de archivos ignorados."
---
# Uso del cliente de sincronización

## Resumen

Esta página explica cómo usar el cliente de escritorio: sus iconos de estado, el menú de la bandeja del sistema, los ajustes de cuenta, las cuentas adicionales, los iconos superpuestos del gestor de archivos, el estado de usuario, el uso compartido desde el escritorio, los ajustes de red y el editor de archivos ignorados. Está dirigida a usuarios del cliente de escritorio.

````{upstream} user_manual/desktop/usage.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El cliente de escritorio de Nextcloud permanece en segundo plano y se muestra como un icono en la bandeja del sistema (Windows, KDE), en la barra de menús (macOS) o en el área de notificación (Linux).

El indicador de estado usa iconos para indicar el estado actual de la sincronización. El círculo verde con la marca de verificación blanca indica que la sincronización está al día y que hay conexión con el servidor Nextcloud.

El icono azul con los semicírculos blancos significa que la sincronización está en curso.

El icono gris con las líneas paralelas indica que la sincronización se ha pausado. (Lo más probable, por el propio usuario).

El icono gris con tres puntos blancos significa que el cliente de sincronización ha perdido la conexión con el servidor Nextcloud.

Cuando se ve un círculo amarillo con el signo «!», ese es el icono informativo, así que conviene hacer clic en él para ver lo que tiene que comunicar.

El círculo rojo con la «x» blanca indica un error de configuración, como un inicio de sesión o una URL de servidor incorrectos.

### Icono de la bandeja del sistema

Al hacer clic con el botón derecho en el icono de la bandeja del sistema se abre un menú de acceso rápido a varias operaciones.

Este menú ofrece las siguientes opciones:

- Abrir el diálogo principal
- Pausar la sincronización/Reanudar la sincronización
- Ajustes
- Salir de Nextcloud, lo que cierra la sesión y el cliente

Al hacer clic con el botón izquierdo en el icono de la bandeja del sistema se abre el diálogo principal del cliente de escritorio.

Los diálogos principales muestran las actividades recientes, los errores y las notificaciones del servidor.

Al hacer clic en el diálogo principal y luego en el avatar del usuario, se pueden abrir los Ajustes.

### Configurar los ajustes de la cuenta de Nextcloud

En la parte superior de la ventana hay pestañas para cada cuenta de sincronización configurada, y otras dos para los ajustes General y Red. En las pestañas de cuenta se dispone de las siguientes funciones:

- Estado de la conexión, que muestra a qué servidor Nextcloud se está conectado y el nombre de usuario de Nextcloud.
- Espacio usado y disponible en el servidor.
- Estado actual de la sincronización.
- Botón **Añadir conexión de sincronización de carpetas**.

El pequeño botón con tres puntos (el menú de desbordamiento) situado a la derecha de la barra de estado de sincronización ofrece opciones adicionales:

- Abrir carpeta
- Elegir qué sincronizar (solo aparece cuando el árbol de archivos está contraído, y despliega el árbol de archivos)
- Pausar sincronización / Reanudar sincronización
- Eliminar la conexión de sincronización de carpetas
- Disponibilidad (solo está disponible si el soporte de archivos virtuales está habilitado)
- Habilitar el soporte de archivos virtuales/Deshabilitar el soporte de archivos virtuales

**Abrir carpeta** abre la carpeta local de sincronización de Nextcloud.

**Pausar sincronización** pausa las operaciones de sincronización sin realizar ningún cambio en la cuenta. Seguirá actualizando las listas de archivos y carpetas, sin descargar ni actualizar archivos. Para detener toda la actividad de sincronización, usar **Eliminar conexión de sincronización de carpetas**.

:::{note}
Nextcloud no conserva el mtime (hora de modificación) de los directorios, aunque sí actualiza el mtime de los archivos. Consultar [Fecha de carpeta incorrecta al sincronizar](https://github.com/owncloud/core/issues/7009) para ver la discusión al respecto.
:::

### Añadir cuentas nuevas

Se pueden configurar varias cuentas de Nextcloud en el cliente de sincronización de escritorio. Basta con hacer clic en el botón **Cuenta** > **Añadir nueva** en cualquier pestaña de cuenta para añadir una cuenta nueva y, a continuación, seguir el asistente de creación de cuentas. La cuenta nueva aparecerá como una pestaña nueva en el diálogo de ajustes, donde se pueden modificar sus ajustes en cualquier momento. Usar **Cuenta** > **Eliminar** para borrar cuentas.

### Iconos superpuestos del gestor de archivos

El cliente de sincronización de Nextcloud ofrece iconos superpuestos, además de los iconos normales de tipo de archivo, para el gestor de archivos del sistema (el Explorador en Windows, Finder en Mac y Nautilus en Linux), que indican el estado de sincronización de los archivos de Nextcloud.

Los iconos superpuestos son similares a los iconos de la bandeja del sistema presentados más arriba. Se comportan de forma diferente en archivos y en directorios según el estado de sincronización y los errores.

El icono superpuesto de un archivo individual indica su estado de sincronización actual. Si el archivo está sincronizado con la versión del servidor, muestra una marca de verificación verde.

Si el archivo se ignora en la sincronización, por ejemplo porque está en la lista de exclusión o porque es un enlace simbólico, muestra un icono de advertencia.

Si hay un error de sincronización, o el archivo está en la lista negra, muestra una llamativa X roja.

Si el archivo está a la espera de sincronizarse, o se está sincronizando, el icono superpuesto muestra un icono azul giratorio.

Cuando el cliente está sin conexión, no se muestra ningún icono, para reflejar que la carpeta no está sincronizada en ese momento y que no se sincroniza ningún cambio con el servidor.

El icono superpuesto de un directorio sincronizado indica el estado de los archivos del directorio. Si hay algún error de sincronización, el directorio se marca con un icono de advertencia.

Si un directorio incluye archivos ignorados marcados con iconos de advertencia, eso no cambia el estado de los directorios padre.

### Establecer el estado de usuario

Si el servidor Nextcloud tiene instalada la app de estado de usuario, el estado de usuario puede establecerse desde el cliente de escritorio. Para ello, abrir el diálogo principal. Luego hacer clic en el avatar y después en los tres puntos. En el menú que se abre, hacer clic en **Establecer estado**.

En el diálogo que se abre, se puede establecer el estado de conexión haciendo clic en **En línea**, **Ausente**, **No molestar** o **Invisible**. También se puede establecer un mensaje de estado personalizado con el campo de texto de abajo o elegir uno de los mensajes de estado predefinidos que aparecen debajo. También es posible establecer un emoji personalizado haciendo clic en el botón con el emoji que hay junto al campo de entrada de texto. Lo último que quizá se quiera establecer es cuándo debe borrarse el estado de usuario. Se puede elegir el periodo tras el cual se borrará el estado de usuario haciendo clic en el botón situado a la izquierda del texto **Borrar el mensaje de estado tras**.

Si se está conforme con el estado creado, se puede activar con el botón **Establecer mensaje de estado**. Si ya se había establecido un estado, se puede borrar haciendo clic en el botón **Borrar mensaje de estado**.

### Compartir desde el escritorio

El cliente de sincronización de escritorio de Nextcloud se integra con el gestor de archivos: Finder en macOS y el Explorador en Windows. Los usuarios de Linux deben instalar un paquete adicional según el gestor de archivos que usen. Están disponibles, por ejemplo, `nautilus-nextcloud` (Ubuntu/Debian), `dolphin-nextcloud` (Kubuntu), `nemo-nextcloud` y `caja-nextcloud`. Se pueden crear enlaces para compartir, y compartir con usuarios internos de Nextcloud, de la misma forma que en la interfaz web de Nextcloud.

En el explorador de archivos, hacer clic en un archivo y, en el menú contextual, ir a **Nextcloud** y luego hacer clic en **Opciones de compartir** para abrir el diálogo de compartir.

Desde este diálogo se puede compartir un archivo.

### Ventana General

La ventana General tiene opciones de configuración como **Iniciar al arrancar el sistema**, **Usar iconos monocromáticos** y **Mostrar notificaciones del servidor**. Aquí se encuentra el botón **Editar archivos ignorados**, que abre el editor de archivos ignorados, y **Pedir confirmación antes de descargar carpetas de más de [tamaño de carpeta]**.

### Usar la ventana Red

La ventana de ajustes de Red permite definir los ajustes del proxy de red y también limitar el ancho de banda de descarga y de subida.

(nc-usingignoredfileseditor-label)=
### Usar el editor de archivos ignorados

Puede haber algunos archivos o directorios locales de los que no se quiera hacer copia de seguridad ni guardar en el servidor. Para identificar y excluir estos archivos o directorios, se puede usar el *Editor de archivos ignorados* (pestaña General).

Por comodidad, el editor viene precargado con una lista predeterminada de patrones de exclusión típicos. Estos patrones se encuentran en un archivo del sistema (normalmente `sync-exclude.lst`) situado en el directorio de la aplicación del cliente de Nextcloud. Estos patrones precargados no pueden modificarse directamente desde el editor. Sin embargo, si es necesario, se puede pasar el cursor sobre cualquier patrón de la lista para mostrar la ruta y el nombre de archivo asociados a ese patrón, localizar el archivo y editar el archivo `sync-exclude.lst`.

:::{note}
Modificar el archivo global de definición de exclusiones puede dejar el cliente inutilizable o provocar un comportamiento no deseado.
:::

Cada línea del editor contiene una cadena de patrón de exclusión. Al crear patrones personalizados, además de poder usar caracteres normales para definir un patrón de exclusión, se pueden usar caracteres comodín para buscar coincidencias. Por ejemplo, se puede usar un asterisco (`*`) para representar un número arbitrario de caracteres o un signo de interrogación (`?`) para representar un único carácter.

Los patrones que terminan en una barra (`/`) solo se aplican a los componentes de directorio de la ruta que se comprueba.

:::{note}
Actualmente, el editor no valida la corrección sintáctica de las entradas personalizadas, por lo que no se verá ninguna advertencia por una sintaxis incorrecta. Si la sincronización no funciona como se esperaba, revisar la sintaxis.
:::

Cada cadena de patrón de la lista va seguida de una casilla. Cuando la casilla contiene una marca de verificación, además de ignorarse el archivo o el componente de directorio que coincide con el patrón, los archivos coincidentes también se consideran «metadatos efímeros» y el cliente los elimina.

Además de excluir los archivos y directorios que usan patrones definidos en esta lista:

- El cliente de Nextcloud siempre excluye los archivos que contienen caracteres que no pueden sincronizarse con otros sistemas de archivos.

- Se eliminan los archivos que provocan errores individuales tres veces durante una sincronización. Sin embargo, el cliente ofrece la opción de reintentar la sincronización tres veces más en los archivos que producen errores.

### Archivos virtuales en macOS

Para obtener información sobre el uso de la integración de archivos virtuales en macOS, consultar:

- {nc-doc}`user_manual/desktop/macosvfs`
````
