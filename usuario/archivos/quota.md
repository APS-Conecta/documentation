---
tipo: explicacion
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Cómo se calcula la cuota de almacenamiento: qué cuenta y qué no, archivos compartidos, versiones y el límite propio de la papelera."
---
# Cuota de almacenamiento

## Resumen

Esta página explica qué se descuenta de la cuota de almacenamiento de una cuenta y qué no, incluidos los archivos compartidos, las versiones y la papelera. Está dirigida a usuarios que quieren entender cómo se calcula su espacio usado.

````{upstream} user_manual/files/quota.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Su administrador de Nextcloud puede establecer una cuota de almacenamiento para su cuenta. Abra su página de ajustes personales para ver su cuota y cuánto almacenamiento ha usado.

Puede ser útil entender cómo se calcula su cuota.

Los metadatos, como miniaturas, archivos temporales, cachés y claves de cifrado, pueden usar espacio en disco sin descontarse de su cuota de usuario. Algunas aplicaciones, como Calendario y Contactos, almacenan datos en la base de datos. Estos datos no se incluyen en la cuota de almacenamiento de archivos.

Cuando otros usuarios comparten archivos con usted, los archivos compartidos normalmente se descuentan de la cuota del propietario original. Cuando usted comparte una carpeta y permite que otros usuarios o grupos suban o editen archivos en ella, esos archivos se descuentan de su cuota. Cuando vuelve a compartir archivos que se compartieron con usted, lo que vuelve a compartir normalmente se sigue descontando de la cuota del propietario original.

Los archivos cifrados pueden usar más almacenamiento físico que los archivos sin cifrar. El cálculo de la cuota usa el tamaño de archivo que informa la capa de almacenamiento de Nextcloud.

Cuando la aplicación Versiones está habilitada, las versiones anteriores de los archivos se gestionan por separado de la cuota de almacenamiento normal, según las reglas de retención y almacenamiento de la aplicación.

Si crea un recurso compartido público mediante una URL y permite subidas, los archivos subidos se descuentan de su cuota.

### Archivos eliminados y la papelera

Los archivos y carpetas de su papelera no se descuentan de su cuota de almacenamiento normal. Sin embargo, la papelera tiene su propio límite de almacenamiento.

En las cuentas con cuota, el espacio predeterminado disponible para la papelera se calcula como el 50 % del espacio restante de la cuota de la cuenta. Este cálculo se hace después de tener en cuenta los archivos activos de la cuenta; no es el 50 % de la cuota total.

En las cuentas sin cuota, el límite predeterminado de la papelera se calcula, en cambio, a partir del espacio disponible en el sistema de archivos. Un administrador puede configurar un tamaño de papelera global o por cuenta que reemplaza el valor predeterminado calculado.

Su administrador también puede configurar periodos mínimos y máximos de retención en la papelera, o desactivar la caducidad automática. Consulte la [sección Archivos eliminados del Manual de administración](https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/trashbin_configuration.html) para más detalles.
````
