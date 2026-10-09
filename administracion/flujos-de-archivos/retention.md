---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Eliminación automática de archivos con una etiqueta colaborativa según su antigüedad: regla de ejemplo, criterios de antigüedad y etiquetas adecuadas."
---
# Retención de archivos

## Resumen

Esta página describe cómo la app Files Retention elimina automáticamente los archivos que llevan una etiqueta colaborativa y alcanzan cierta antigüedad, con una regla de ejemplo, las opciones de antigüedad y un error de configuración común. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/file_workflows/retention.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La app Files Retention de Nextcloud permite eliminar automáticamente los archivos que están etiquetados con una etiqueta colaborativa y que tienen cierta antigüedad.

### Ejemplo

Después de instalar la app Retention como se describe en {nc-doc}`admin_manual/apps_management`, ir a Configuraciones de administración y después a Flujo. La pantalla muestra una regla de ejemplo para eliminar los archivos 14 días después de su creación.

La regla del ejemplo eliminará todos los archivos etiquetados con `Temporary file` 14 días después de su creación.

También puede usarse la opción «Notify owner a day before a file is automatically deleted» para asegurarse de que el propietario del archivo reciba una notificación antes de que se elimine un archivo.

### Antigüedad del archivo

Hay 2 opciones disponibles para decidir cuándo eliminar un archivo:

- **Creación:** el momento en que el archivo se creó en el servidor Nextcloud o se subió a él.
- **Última modificación:** el momento en que el archivo se modificó por última vez. La subida también cuenta como modificación, de modo que los archivos que no se habían modificado desde mucho tiempo antes de subirlos no se eliminan poco después de la subida.

### Errores de configuración comunes

#### Etiqueta colaborativa pública

De forma similar a {nc-doc}`admin_manual/file_workflows/access_control`, la retención debe usar etiquetas `restricted` o `invisible`. De lo contrario, cualquier usuario puede quitar la etiqueta y el archivo no se elimina tras el periodo indicado. Usar {nc-doc}`admin_manual/file_workflows/automated_tagging` para asignar esas etiquetas a los archivos recién subidos.
````
