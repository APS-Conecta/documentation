---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Etiquetas del sistema: niveles de acceso, explorar archivos por etiqueta, asignar etiquetas a uno o varios archivos y crearlas."
---
# Etiquetas del sistema

## Resumen

Esta página explica qué son las etiquetas del sistema y sus niveles de acceso, cómo explorar archivos por etiqueta, cómo asignar y quitar etiquetas en uno o varios archivos y cómo crear etiquetas nuevas. Está dirigida a usuarios que organizan archivos y carpetas con etiquetas.

````{upstream} user_manual/files/tagging.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Las etiquetas del sistema son rótulos de alcance de todo el servidor que se pueden asignar a archivos y carpetas para organizarlos, filtrar la lista de archivos y activar flujos de trabajo automatizados, como reglas de retención y control de acceso.

Las etiquetas aparecen directamente en las filas de archivos y carpetas de la aplicación **Archivos**, de modo que se ve de un vistazo qué etiquetas están asignadas.

Los administradores crean las etiquetas en los ajustes del servidor. Según la configuración del servidor, es posible que los usuarios normales también puedan crear etiquetas; el administrador puede restringir la creación de etiquetas solo a los administradores.

### Niveles de acceso de las etiquetas

Cada etiqueta tiene uno de tres niveles de acceso, que controlan lo que los usuarios normales pueden ver y hacer:

| Nivel | Visible para los usuarios | Los usuarios pueden asignarla / quitarla |
|---|---|---|
| Público | Sí | Sí |
| Restringido | Sí | No |
| Invisible | No | No |

Los administradores usan las etiquetas restringidas e invisibles para flujos de trabajo automatizados. No es posible eludirlas quitando uno mismo la etiqueta.

### Explorar archivos por etiqueta

Hacer clic en el icono de navegación (≡) en la parte superior izquierda de la aplicación **Archivos** para abrir el panel de navegación y, luego, hacer clic en **Etiquetas**. La vista muestra todas las etiquetas visibles para el usuario. Al hacer clic en el nombre de una etiqueta se ven todos los archivos y carpetas que tienen esa etiqueta asignada.

### Asignar etiquetas a archivos

Se pueden asignar o quitar etiquetas en un archivo a la vez o en una selección de archivos en un solo paso.

**Un solo archivo**

1. Hacer clic en el menú de acciones de tres puntos (**…**) junto a un archivo o carpeta y seleccionar **Detalles** para abrir la barra lateral de detalles.
2. En la barra lateral de detalles, hacer clic en **Añadir etiquetas**.
3. Escribir el nombre de una etiqueta en el campo de búsqueda y seleccionar la etiqueta de la lista.
4. Hacer clic fuera del selector para cerrarlo. Los cambios se guardan de inmediato.

Para quitar una etiqueta, abrir el mismo selector y hacer clic en la **×** junto al nombre de la etiqueta.

:::{note}
Solo las etiquetas públicas aparecen en el selector para los usuarios normales. Las etiquetas restringidas e invisibles solo pueden asignarlas los administradores.
:::

**Varios archivos**

1. Seleccionar dos o más archivos haciendo clic en la casilla a la izquierda de cada fila.
2. Hacer clic en **··· Acciones** en la barra de herramientas sobre la lista de archivos y, luego, seleccionar **Gestionar etiquetas**.
3. Marcar o desmarcar etiquetas en el diálogo que aparece. Una línea informativa muestra cómo se aplicará el cambio a los archivos seleccionados.
4. Hacer clic en **Aplicar**.

### Crear y gestionar etiquetas

Si el administrador no ha restringido la creación de etiquetas, se puede crear una etiqueta nueva directamente desde el diálogo **Gestionar etiquetas** o desde el selector de etiquetas de un solo archivo: escribir un nombre nuevo en el campo **Buscar o crear etiqueta** y seleccionar la opción **Crear etiqueta** que aparece.

Los administradores crean, renombran y eliminan etiquetas en {guilabel}`Configuraciones de administración` > {guilabel}`Servidor`. Para obtener detalles sobre la gestión de etiquetas y las herramientas de línea de comandos, consultar la sección [Etiquetado automatizado](https://docs.nextcloud.com/server/latest/admin_manual/file_workflows/automated_tagging.html) del manual de administración.
````
