---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Preguntas frecuentes del cliente de escritorio: Editar localmente, subidas repetidas, límites de sincronización, mover la carpeta y cambiar el idioma."
---
# Preguntas frecuentes

## Resumen

Esta página responde preguntas frecuentes sobre el cliente de escritorio: cómo funciona «Editar localmente», por qué algunos archivos se suben una y otra vez, los límites de profundidad y de supervisión de carpetas, cómo mover la carpeta de sincronización local y cómo cambiar el idioma de la interfaz. Está dirigida a usuarios del cliente de escritorio.

````{upstream} user_manual/desktop/faq.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Cómo funciona la función «Editar localmente»

Esta función depende de la capacidad del cliente de escritorio de registrar el manejador del protocolo nc://. Ese es el manejador que usa el servidor para abrir un archivo localmente. Esto permite que el cliente de escritorio abra un documento con el editor local al hacer clic en la opción «Editar localmente» en la instancia de Nextcloud.

:::{note}
Si el mime no se registra correctamente, independientemente del navegador y la distribución que se usen, el cliente de escritorio no podrá abrir un documento con el editor local al hacer clic en la opción «Editar localmente» en la instancia de Nextcloud.

El navegador mostrará una advertencia sobre el fallo: «Failed to launch 'nc://...' because the scheme does not have a registered handler.»
:::

#### Cómo habilitarla

Para ello, hay que instalar el cliente de escritorio con el instalador MSI en Windows, o usar un software de terceros para integrar la AppImage en el sistema en Linux.

#### En Linux

Usamos AppImage por su compatibilidad universal, pero para aprovechar al máximo las funciones del cliente de escritorio se necesitará un software de terceros que integre la AppImage en el sistema: hemos probado [AppImageLauncher](https://github.com/TheAssassin/AppImageLauncher) y, como alternativa, existe [Go AppImage](https://github.com/probonopd/go-appimage).

#### En Windows

El instalador MSI modifica el registro del sistema para registrar el manejador del protocolo nc://.

Como alternativa, se puede registrar manualmente el manejador del protocolo nc://:

1. Guardar el siguiente contenido en un archivo .reg:

```none
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\nc\shell\open\command]
@="\"C:\\Program Files\\Nextcloud\\nextcloud.exe\" \"%1\""
```

2. Hacer doble clic en el archivo .reg para importarlo en el registro.

Consultar <https://nextcloud.com/blog/nextcloud-office-release-solves-document-compatibility-overhauls-knowledge-management/> para más información.

### Algunos archivos se suben continuamente al servidor, incluso cuando no se han modificado.

Es posible que otro programa esté cambiando la fecha de modificación del archivo. Si el archivo usa la extensión `.eml`, Windows cambia automática y continuamente todos los archivos, a menos que se elimine `\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\PropertySystem\PropertyHandlers` del registro de Windows. Consultar <http://petersteier.wordpress.com/2011/10/22/windows-indexer-changes-modification-dates-of-eml-files/> para más información.

### La sincronización se detiene al intentar sincronizar a más de 100 subdirectorios de profundidad.

El cliente de sincronización se ha limitado intencionadamente para no sincronizar a más de 100 subdirectorios de profundidad. Este límite estricto existe para protegerse de errores con ciclos, como los bucles de enlaces simbólicos. Cuando un directorio anidado a gran profundidad se excluye de la sincronización, aparece junto con los demás archivos y directorios ignorados en la pestaña «No sincronizado» del panel «Actividad».

### Apareció una advertencia de que los cambios en las carpetas sincronizadas no se rastrean de forma fiable.

En Linux, cuando la carpeta sincronizada contiene muchísimas subcarpetas, puede que el sistema operativo no permita suficientes vigilancias de inotify para supervisar los cambios en todas ellas.

En este caso, el cliente no podrá iniciar inmediatamente el proceso de sincronización cuando cambie un archivo en una de las carpetas no supervisadas. En su lugar, el cliente mostrará la advertencia y buscará cambios en las carpetas manualmente a intervalos regulares (cada dos horas de forma predeterminada).

Este problema puede resolverse asignando un valor más alto al parámetro sysctl fs.inotify.max_user_watches. Normalmente esto puede hacerse de forma temporal:

```
echo 524288 > /proc/sys/fs/inotify/max_user_watches
```

o de forma permanente, ajustando `/etc/sysctl.conf`.

### Quiero mover mi carpeta de sincronización local

El cliente de escritorio de {vendor}`Nextcloud` no ofrece una forma de cambiar el directorio de sincronización local. Sin embargo, puede hacerse, aunque de una manera algo poco ortodoxa. En concreto, hay que:

1. Eliminar la conexión existente que sincroniza con el directorio equivocado
2. Añadir una nueva conexión que sincronice con el directorio deseado

Para ello, hacer clic en el menú desplegable «**Cuenta**» y luego en «Eliminar». Se mostrará una ventana de diálogo «**Confirmar la eliminación de la cuenta**».

Si se está seguro, hacer clic en «**Eliminar conexión**».

Luego, hacer clic de nuevo en el menú desplegable Cuenta y, esta vez, hacer clic en «**Añadir nueva**».

Esto abre el asistente de conexión de Nextcloud, *pero* con una opción adicional. Esta opción permite: conservar los datos existentes (sincronizados por la conexión anterior) o iniciar una sincronización limpia (borrando los datos existentes).

:::{important}
Tener cuidado antes de elegir la opción «Iniciar una sincronización limpia». La carpeta de sincronización antigua *puede* contener una cantidad considerable de datos, del orden de gigabytes o terabytes. Si es así, después de que el cliente cree la nueva conexión, tendrá que descargar **toda** esa información de nuevo. En su lugar, primero mover o copiar la carpeta de sincronización local antigua, que contiene una copia de los archivos existentes, a la nueva ubicación. Después, al crear la nueva conexión, elegir en cambio «*conservar los datos existentes*». El cliente de {vendor}`Nextcloud` comprobará los archivos de la carpeta de sincronización recién añadida, verá que coinciden con lo que hay en el servidor y no necesitará descargar nada.
:::

Elegir una opción y hacer clic en «**Conectar...**». Esto guiará por el asistente de conexión, igual que al configurar la conexión de sincronización anterior, pero dando la oportunidad de elegir un nuevo directorio de sincronización.

### Quisiera cambiar el idioma de la interfaz de usuario

Para ello, hay que modificar el archivo de configuración `nextcloud.cfg`. Hay que añadir una línea con el idioma deseado a la sección `General`.

```none
[General]
language=de
```
````
