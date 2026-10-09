---
tipo: explicacion
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Cómo funciona la papelera: restaurar archivos eliminados, qué pasa al borrar archivos compartidos, y sus límites de espacio y de retención."
---
# Archivos eliminados

## Resumen

Esta página explica qué ocurre con un archivo o una carpeta al eliminarlo, cómo restaurarlo desde la papelera, qué pasa cuando se borran archivos compartidos y cómo la papelera limita el espacio que ocupa y el tiempo que conserva los elementos. Está dirigida a usuarios que eliminan o necesitan recuperar archivos.

````{upstream} user_manual/files/deleted_file_management.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Cuando usted elimina un archivo o una carpeta en Nextcloud, normalmente se mueve a la papelera en lugar de eliminarse de inmediato. Esto le permite restaurarlo más tarde.

Los elementos de la papelera se eliminan de forma permanente cuando ocurre una de las siguientes situaciones:

- Usted selecciona manualmente *Eliminar de forma permanente*.
- La aplicación Archivos eliminados quita el elemento según la política de retención configurada.
- Se supera el límite efectivo de tamaño de la papelera y el elemento reúne las condiciones para quitarse a fin de liberar espacio.

Encuentre sus archivos eliminados seleccionando **Archivos eliminados** en el área Archivos de la interfaz web de Nextcloud. Desde ahí puede restaurar elementos, descargarlos a su dispositivo o eliminarlos de forma permanente.

Cuando restaura un elemento, Nextcloud normalmente intenta devolverlo a su ubicación original. Si esa ubicación ya no existe o no admite escritura, el elemento se restaura en la raíz de su área Archivos. Si ya existe un elemento con el mismo nombre, Nextcloud le da al elemento restaurado un nombre único.

:::{note}
Si la aplicación Versiones está habilitada, las versiones asociadas a un archivo eliminado se mueven a la papelera y se restauran cuando se restaura el archivo.
:::

### Cuotas

Los archivos y las carpetas de su papelera no cuentan para su cuota de almacenamiento normal.

Consulte {nc-doc}`user_manual/files/quota` para obtener más información sobre cómo se calculan las cuotas de almacenamiento.

### ¿Qué pasa cuando se borran archivos compartidos?

El comportamiento de los archivos compartidos eliminados depende de quién elimina el elemento y de quién es su propietario.

Por ejemplo, User1 comparte una carpeta llamada `TheProject/` con User2 y User3:

1. User2, un destinatario del recurso compartido (sharee), elimina una carpeta o un archivo llamado `Phase2` dentro de `TheProject/`.

   `TheProject/Phase2` se mueve a la papelera de User1, el propietario, y se coloca una copia en la papelera de User2 cuando es posible. El elemento se quita de la carpeta compartida para User3, pero User3 no recibe una copia en su papelera.

2. User1, el propietario, elimina `TheProject/Phase2`.

   El elemento se mueve a la papelera de User1 y se quita de la carpeta compartida para User2 y User3. No se coloca en sus papeleras.

El comportamiento exacto puede depender del tipo de recurso compartido y de los permisos que este otorga. Según esos permisos, otros usuarios pueden copiar, renombrar, mover o volver a compartir archivos compartidos. Estas operaciones pueden influir en qué cuenta es propietaria de los archivos resultantes y en qué papelera recibe un elemento eliminado.

:::{note}
Cuando un destinatario elimina un elemento cuyo propietario es otro usuario, Nextcloud mueve el elemento a la papelera del propietario. También se crea una copia en la papelera del usuario que lo elimina (en la mayoría de los casos; la copia se intenta en la medida de lo posible y no está garantizada).
:::

### Cómo gestiona el espacio de almacenamiento la aplicación Archivos eliminados

La aplicación Archivos eliminados gestiona el contenido de la papelera mediante dos reglas relacionadas:

- Un límite de almacenamiento determina cuánto espacio puede usar la papelera.
- Una política de retención determina cuándo los elementos eliminados reúnen las condiciones para eliminarse de forma permanente.

#### Límite de almacenamiento de la papelera

Para las cuentas con cuota de almacenamiento, el límite predeterminado de la papelera es de hasta el 50 % del espacio restante de la cuota de la cuenta. Se calcula después de tener en cuenta los archivos activos de la cuenta; no es el 50 % de la cuota total de la cuenta.

Por ejemplo, si su cuota es de 10 GB y sus archivos activos usan 8 GB, la asignación predeterminada de la papelera se calcula a partir de los 2 GB restantes.

Para las cuentas sin cuota de almacenamiento, el límite predeterminado se calcula, en cambio, a partir del espacio disponible en el sistema de archivos. Su administrador puede sustituir cualquiera de los dos valores predeterminados configurando un tamaño de papelera global o por cuenta.

Cuando se supera el límite efectivo de la papelera, Nextcloud quita los elementos eliminados que reúnen las condiciones, empezando por los más antiguos, hasta que se vuelve a cumplir el límite.

#### Retención y eliminación permanente

De forma predeterminada, los archivos eliminados se conservan durante al menos 30 días. Después de ese plazo, los elementos que reúnen las condiciones pueden eliminarse de forma permanente cuando se necesita espacio; no se eliminan necesariamente en cuanto se cumplen los 30 días.

Su administrador puede configurar periodos de retención mínimos y máximos distintos. Según la configuración, los elementos pueden eliminarse de forma permanente al alcanzar una antigüedad máxima aunque en ese momento no se necesite espacio de almacenamiento. La caducidad automática también puede desactivarse.

En las políticas con un periodo de retención mínimo configurado, un elemento solo reúne las condiciones para la limpieza por espacio después de que haya transcurrido ese periodo. Las políticas sin periodo de retención mínimo pueden permitir la limpieza por espacio sea cual sea la antigüedad del elemento. Los elementos que han superado un periodo de retención máximo configurado pueden eliminarse de forma permanente se necesite o no espacio en ese momento.

El ajuste de configuración correspondiente es `trashbin_retention_obligation`. Para obtener detalles sobre los valores disponibles y su interacción con las cuotas y los tamaños de la papelera, consulte la [sección Archivos eliminados del Manual de administración](https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/trashbin_configuration.html).

:::{note}
La aplicación Archivos eliminados puede eliminar de forma permanente un elemento antes de su periodo de retención máximo cuando se supera el límite efectivo de la papelera y ya ha transcurrido el periodo de retención mínimo del elemento.
:::
````
