---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Asignación de etiquetas colaborativas restringidas e invisibles a archivos según reglas: un ejemplo, las reglas disponibles y las acciones."
---
# Etiquetado automatizado de archivos

## Resumen

Esta página describe cómo la app Files Automated Tagging asigna etiquetas colaborativas a archivos y carpetas según reglas, para que las etiquetas restringidas e invisibles sostengan la retención y el control de acceso. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/file_workflows/automated_tagging.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La app Files Automated Tagging de Nextcloud permite asignar etiquetas colaborativas a archivos y carpetas en función de reglas, de forma similar a {nc-doc}`admin_manual/file_workflows/access_control`.

### Asignar etiquetas restringidas e invisibles

La función principal de esta app es permitir que los usuarios asignen de forma indirecta etiquetas restringidas e invisibles a los archivos que suben.

Esto resulta especialmente útil para la retención y para {nc-doc}`admin_manual/file_workflows/access_control`, de modo que las personas que recibieron los archivos compartidos no puedan quitar la etiqueta para detener la retención o para permitir el acceso en contra de la voluntad del propietario.

### Ejemplo

Después de instalar la app Files automated tagging como se describe en {nc-doc}`admin_manual/apps_management`, ir a la configuración y localizar los ajustes de flujo de trabajo. La pantalla muestra una regla de ejemplo para asignar una etiqueta restringida.

En el ejemplo se ve una regla sencilla con una sola condición. Etiquetará con la etiqueta restringida `Protected file` todos los archivos que se suban a una carpeta etiquetada con `Protect content`. Ningún usuario puede quitar la etiqueta `Protected file` y, por tanto, tanto el control de acceso como la retención funcionan correctamente sin que los usuarios puedan eludirlos.

En este caso, la carpeta también quedará etiquetada con la etiqueta `Protected file`; para evitarlo, basta con modificar la regla para excluir de ella los directorios (`httpd/unix-directory`).

### Reglas disponibles

Las reglas disponibles pueden consultarse en la sección de control de acceso: {nc-ref}`Reglas disponibles <available-rules-label>`.

:::{note}
Tener en cuenta que las reglas no se aplican al crear almacenamientos externos y carpetas de grupo. Las carpetas raíz de estos deben etiquetarse manualmente con las etiquetas iniciales deseadas. A los elementos que se creen después dentro de ellas se les aplican las reglas tal como estén definidas.
:::

### Ejecutar acciones

Es posible ejecutar acciones como `` `convert to PDF` `` en función de las etiquetas asignadas. Nextcloud GmbH ayuda a los clientes en esto con asistencia práctica y documentación en su [portal de clientes](https://portal.nextcloud.com).
````
