---
tipo: explicacion
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "La integración de archivos virtuales en macOS: funciones, configuración, Finder, indicadores de estado, menú contextual y problemas conocidos."
---
# Cliente de archivos virtuales para macOS

## Resumen

Esta página explica cómo el cliente de escritorio integra los archivos en macOS como extensión de proveedor de archivos: qué funciones ofrece, cómo se configura, cómo se ve en Finder y qué problemas conocidos tiene. Está dirigida a usuarios de macOS.

````{upstream} user_manual/desktop/macosvfs.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
En macOS, nuestro cliente también puede integrar de forma transparente los archivos de Nextcloud en macOS como una extensión de proveedor de archivos. Toda cuenta de Nextcloud recién configurada tendrá la integración habilitada de forma predeterminada.

### Funciones compatibles

- Mantener archivos o carpetas enteras disponibles sin conexión
- Liberar espacio en el disco local desalojando las copias locales sin eliminar los elementos
- Desalojo inteligente y automático de los datos locales
- Vistas previas en Finder de archivos que aún no se han descargado
- Compatibilidad con formatos específicos de Apple, por ejemplo, paquetes de Pages, Numbers o Keynote
- Compatibilidad con el bloqueo de archivos en el servidor (si el servidor conectado lo admite)
- Compatibilidad con «Editar localmente»
- Compartir con otros usuarios
- Acciones del servidor integradas directamente en el menú contextual de Finder
- Detección automática de los cambios en el servidor

### Configuración

Los ajustes relacionados con los archivos virtuales pueden modificarse por cuenta desde la ventana de ajustes del cliente de escritorio de {vendor}`Nextcloud`.

Aquí se puede habilitar o deshabilitar la integración con Finder.

Si se deshabilita la extensión de proveedor de archivos mientras aún hay cambios sin sincronizar, macOS guardará los elementos no sincronizados en una carpeta que se muestra automáticamente después de deshabilitar la integración.

### Integración con Finder

En macOS, un almacenamiento remoto, como una cuenta de archivos de Nextcloud, aparece como una ubicación propia en la barra lateral de Finder. La ubicación real del contenido en el disco la define macOS.

:::{note}
Para acelerar la detección de cambios en el servidor, recomendamos habilitar la app `notify_push` en el servidor Nextcloud. Esta app notifica al cliente de escritorio los cambios en el servidor en cuanto se producen, lo que reduce el tiempo que tardan los cambios en aparecer en Finder. De lo contrario, el cliente tiene que consultar periódicamente el servidor, lo que provoca un mayor retraso entre un cambio en el servidor y su visibilidad local.
:::

### Indicadores de estado de sincronización

Al igual que en las carpetas de sincronización clásicas, Finder muestra indicadores de estado junto a los elementos. A diferencia de los indicadores personalizados de las carpetas de sincronización clásicas, estos indicadores estandarizados los proporciona macOS para garantizar un aspecto coherente en todas las apps de almacenamiento en la nube que un usuario pueda usar en su sistema.

- *Nube con flecha hacia abajo*: el elemento y sus descendientes aún no se han descargado. Pueden descargarse, siempre que haya una conexión de red disponible.
- *Nube con contorno*: el elemento aún no se ha subido por completo en su estado local actual.
- *Nube tachada*: el elemento está excluido de la sincronización.
- *Gráfico circular*: el elemento se está subiendo o descargando, y se muestra el progreso.
- *Círculo relleno con una chincheta*: el elemento está disponible sin conexión y se mantendrá localmente.
- *Sin icono*: el elemento está disponible sin conexión y actualizado.

### Acciones del menú contextual

La extensión de proveedor de archivos también ofrece funciones especiales de Nextcloud a través del menú contextual de Finder.

#### Mantener descargado

Los archivos y carpetas pueden marcarse para mantenerse descargados y disponibles sin conexión de forma permanente. Si se elige en carpetas, también se aplica a todo su contenido. Esto es especialmente útil para usuarios con acceso a la red limitado o nulo, ya que garantiza que siempre puedan acceder a sus archivos importantes sin preocuparse por la conectividad. macOS **no** liberará espacio en el disco local desalojando elementos marcados para mantenerse descargados, aunque no se hayan usado durante mucho tiempo.

Esto puede deshacerse seleccionando «Permitir liberar espacio automáticamente» en los mismos elementos.

Para mantener siempre disponible localmente todo el contenido de una cuenta, se puede seleccionar «Mantener siempre descargado» en la raíz de la ubicación, en la barra lateral de Finder.

#### Bloqueo

Si el servidor admite el bloqueo de archivos, el cliente ofrece el bloqueo y desbloqueo manual de archivos en Finder.

#### Compartir

Cuando el servidor admite el uso compartido y está permitido compartir el elemento, se pueden crear nuevos recursos compartidos o gestionar los existentes de un elemento directamente desde el menú contextual de Finder, igual que en la interfaz web de Nextcloud.

#### Acciones de archivo

Si el servidor tiene instaladas apps que ofrecen acciones de archivo para los tipos de archivo seleccionados, estas acciones también estarán disponibles en el menú contextual de Finder. Esto permite usar funciones del servidor de la instancia de Nextcloud directamente desde Finder.

### Problemas conocidos

#### Conflicto de extensiones de macOS

Debido a limitaciones técnicas de macOS impuestas por Apple, no es posible tener la integración con Finder de las carpetas de sincronización clásicas funcionando en paralelo con una integración de archivos virtuales habilitada. Esto significa que las decoraciones de los elementos y las opciones del menú contextual no estarán disponibles para las carpetas de sincronización clásicas mientras la extensión de proveedor de archivos esté habilitada.

#### Archivos de alias

Al abrir por primera vez un archivo de alias de macOS almacenado en Nextcloud en un dispositivo donde aún no se ha descargado, el archivo puede abrirse como un documento binario en un editor de texto en lugar de saltar a su destino. Esto ocurre porque macOS decide cómo abrir un archivo antes de descargarlo, y los archivos de alias no llevan en el servidor ninguna extensión de archivo ni información de tipo reconocible: la única forma de identificarlos es leyendo su contenido. Una vez que el archivo se ha abierto o descargado una vez, Nextcloud Desktop aprende que es un alias y guarda esa información localmente, de modo que todas las aperturas posteriores funcionarán correctamente. Para evitar el problema por completo, hacer clic con el botón derecho en el archivo de alias en Finder y elegir **Mantener descargado** antes de abrirlo por primera vez.
````
