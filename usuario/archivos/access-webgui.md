---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "La aplicación Archivos en el navegador: navegar, ver detalles y actividad, buscar, subir y crear, seleccionar, mover y previsualizar archivos."
---
# Acceder a los archivos con la interfaz web de Nextcloud

## Resumen

Esta página recorre la aplicación Archivos en el navegador: las vistas de la barra lateral, el menú de acciones, la barra lateral de detalles, la búsqueda, la vista de cuadrícula, la subida y creación de archivos, la selección múltiple, los iconos de estado de compartición, y cómo mover y previsualizar archivos. Está dirigida a todos los usuarios.

````{upstream} user_manual/files/access_webgui.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Puede acceder a sus archivos en Nextcloud con la interfaz web de Nextcloud, y crear, previsualizar, editar, borrar, compartir y volver a compartir archivos. Su administrador de Nextcloud tiene la opción de deshabilitar estas características, así que consulte con su administrador de sistemas si echa en falta alguna de ellas.

### Navegar por sus archivos

La barra lateral izquierda le permite cambiar entre distintas vistas de sus archivos. Haga clic en el nombre de una carpeta de la lista de archivos para abrirla, y use el botón Atrás de su navegador o la barra de ruta de navegación de la parte superior de la lista de archivos para volver a un nivel anterior.

La barra lateral contiene las siguientes entradas:

- Todos los archivos: la vista predeterminada, que muestra todos los archivos y carpetas a los que tiene acceso.
- Reciente: archivos que ha visto o modificado recientemente.
- Favoritos: archivos y carpetas que ha marcado con una estrella.
- Compartidos: archivos compartidos con usted, por usted o mediante un enlace público, todos en una sola vista.
- Etiquetas: explore los archivos por etiqueta del sistema. Consulte {nc-doc}`user_manual/files/tagging` para obtener detalles sobre cómo asignar etiquetas y filtrar sus archivos.
- Archivos eliminados: archivos que ha eliminado y que todavía se pueden recuperar de la papelera.

Cuando entra en una carpeta, aparece una ruta de navegación en la parte superior de la lista de archivos para que pueda volver a cualquier carpeta superior con un solo clic:

### Control sobre archivos

Nextcloud muestra miniaturas de vista previa de imágenes, archivos de texto y otros tipos compatibles; la lista exacta depende de la configuración de su servidor.

Cada fila de archivo y de carpeta tiene un botón de menú de acciones de tres puntos. Haga clic en él para renombrar, mover, copiar, descargar o eliminar el elemento, o para marcarlo como favorito. Los archivos marcados como favoritos muestran un icono de estrella:

:::{note}
Puede encontrar rápidamente todos sus favoritos con la entrada **Favoritos** de la barra lateral izquierda.
:::

### Barra lateral de detalles

Seleccione **Detalles** en el menú de acciones de tres puntos para abrir la barra lateral de detalles. La barra lateral muestra información sobre el archivo seleccionado y ofrece acceso, mediante pestañas, a su historial de actividad, sus opciones para compartir y su historial de versiones:

### Actividad y comentarios

La pestaña **Actividad** de la barra lateral de detalles muestra un registro cronológico de los cambios del archivo: subidas, ediciones, recursos compartidos y comentarios. Puede dejar un comentario directamente en esta pestaña; los comentarios son visibles para todas las personas que tienen acceso al archivo:

### Buscar y filtrar

Use la barra de búsqueda de la parte superior de la página para buscar archivos por nombre en todos sus archivos, o escriba en el campo de búsqueda de la barra lateral izquierda para filtrar la vista actual:

### Vista de cuadrícula

La aplicación Archivos usa de forma predeterminada una vista de lista. Haga clic en el botón para alternar a cuadrícula, situado sobre la lista de archivos, para cambiar a una cuadrícula de miniaturas, útil para explorar carpetas de imágenes:

Haga clic de nuevo en el botón para volver a la vista de lista.

### Subir y crear archivos

Haga clic en el botón **+** cerca de la parte superior de la lista de archivos para subir archivos desde su ordenador o crear elementos nuevos en la carpeta actual:

El menú ofrece las siguientes opciones:

- Subir archivo: abre un selector de archivos para subir uno o más archivos desde su ordenador. También puede arrastrar y soltar archivos directamente desde su gestor de archivos sobre la lista de archivos.
- Subir carpeta: sube una carpeta completa conservando su estructura.
- Nueva carpeta: crea una carpeta vacía en la ubicación actual.
- Nuevo documento / Nueva hoja de cálculo / Nueva presentación: crea un archivo nuevo con el editor integrado Nextcloud Text u Office, si su administrador lo ha habilitado.

### Seleccionar archivos o carpetas

Haga clic en la casilla a la izquierda de un archivo o carpeta para seleccionarlo. Para seleccionar todos los elementos de la carpeta actual, haga clic en la casilla del encabezado de la columna.

Con uno o más elementos seleccionados, aparecen botones de acción en la parte superior de la lista. Puede eliminar o descargar todos los elementos seleccionados a la vez. Al descargar varios elementos se genera un archivo ZIP.

:::{note}
Si el botón **Descargar** no está visible, su administrador ha deshabilitado esta función.
:::

### Iconos del estado de compartición

Las carpetas y los archivos que se han compartido muestran una insignia **Compartido** en su miniatura o icono. Los elementos compartidos mediante un enlace público muestran además un icono de eslabón de cadena. Los elementos que no están compartidos no tienen ningún indicador adicional.

Consulte {nc-doc}`user_manual/files/sharing` para obtener instrucciones sobre cómo crear y gestionar recursos compartidos.

### Mover archivos

Arrastre cualquier archivo o carpeta y suéltelo sobre una carpeta de destino para moverlo. También puede usar **Mover o copiar** en el menú de acciones de tres puntos para mover o copiar elementos a una carpeta que elija en un diálogo de selección.

### Previsualizar archivos

Haga clic en el nombre de un archivo para abrir una vista previa directamente en Nextcloud. Los formatos compatibles incluyen imágenes, texto plano, PDF y, según su servidor, documentos de ofimática y archivos de audio. Si Nextcloud no puede previsualizar un formato de archivo, descarga el archivo a su ordenador.

### Reproductor de vídeo

Puede reproducir vídeos directamente en Nextcloud haciendo clic en el archivo. La reproducción depende de su navegador y del códec del vídeo. Consulte [MDN: formatos multimedia compatibles](https://developer.mozilla.org/en-US/docs/Web/HTML/Supported_media_formats#Browser_compatibility) como referencia de compatibilidad.

### Conectarse a un recurso compartido en federación

La compartición en la nube federada le permite montar recursos compartidos de archivos de servidores Nextcloud remotos y gestionarlos igual que los recursos compartidos locales. Consulte {nc-doc}`user_manual/files/federated_cloud_sharing` para aprender a crear recursos compartidos en la nube federada y a conectarse a ellos.
````
