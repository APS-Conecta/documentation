---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Grupos de reglas de File Access Control: qué bloquea el acceso denegado, ejemplos, carpetas y subidas, errores comunes y reglas disponibles."
---
# Control de acceso a archivos

## Resumen

Esta página explica cómo la app File Access Control deniega el acceso a archivos mediante grupos de reglas, con ejemplos para bloquear carpetas y tipos de archivo, los errores de configuración comunes y las reglas disponibles. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/file_workflows/access_control.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La app File Access Control de Nextcloud permite a los administradores crear y gestionar un conjunto de grupos de reglas. Cada grupo de reglas consta de una o más reglas. Si todas las reglas de un grupo se cumplen, el grupo coincide con la solicitud y se deniega el acceso. Los criterios de las reglas abarcan desde la dirección IP hasta los grupos de usuarios, las etiquetas colaborativas y {nc-ref}`algunos más <available-rules-label>`.

:::{note}
Si se usa la {nc-ref}`app Context Chat <ai-app-context_chat>`, tener en cuenta que no se ve afectada por las reglas de File Access Control y que responderá con información indexada, incluso cuando el usuario no pueda acceder al archivo debido a las reglas de control de acceso.
:::

### Acceso denegado

Si se ha denegado a un usuario el acceso a un archivo, el usuario no puede:

- Crear o subir el archivo
- Modificar los archivos
- Eliminar el archivo
- Descargar el archivo
- Sincronizar el archivo con clientes, como los clientes de escritorio y móviles de {vendor}`Nextcloud`

### Ejemplos

Después de instalar la app File Access Control como se describe en {nc-doc}`admin_manual/apps_management`, ir a la configuración y localizar los ajustes de la aplicación Flujo. La pantalla muestra reglas de ejemplo para bloquear en función del grupo de usuarios, la hora y la IP.

El primer grupo de reglas, `Support only 9-5`, deniega cualquier acceso a archivos a los usuarios del grupo de usuarios Support entre las 17:00 y las 9:00.

El segundo grupo de reglas, `Internal testing`, impide que los usuarios del grupo Internal testers accedan a archivos desde fuera de la red local.

### Denegar el acceso a carpetas

La forma más sencilla de bloquear el acceso a una carpeta es usar una etiqueta colaborativa. Como se menciona más abajo en la sección {nc-ref}`Reglas disponibles <available-rules-label>`, el propio archivo o una de sus carpetas superiores debe tener asignada la etiqueta indicada.

Así que basta con asignar la etiqueta a la carpeta o al archivo y, después, bloquear la etiqueta con un grupo de reglas. La comprobación es independiente de los permisos del usuario sobre la etiqueta. Por eso se recomiendan etiquetas restringidas e invisibles; de lo contrario, un usuario podría quitar la etiqueta y volver a asignarla.

Este ejemplo bloquea el acceso a cualquier carpeta con la etiqueta `Confidential`. La pantalla muestra la denegación del acceso en función de una etiqueta colaborativa.

### Impedir la subida de archivos concretos

Es posible impedir que se suban a Nextcloud archivos concretos. Basta con definir una regla basada en el tipo MIME y el potente motor de control de acceso bloqueará cualquier intento de subir el archivo. La forma más segura de definir la regla es usar una expresión regular, ya que ayuda a cubrir todos los tipos de medio conocidos que se usan para el tipo de archivo que se intenta bloquear.

El siguiente ejemplo impide que se suban archivos zip mediante la expresión regular `/^application\/(zip|x-zip-compressed)$/i`. La pantalla muestra cómo se impide la subida en función del tipo MIME.

### Errores de configuración comunes

#### Bloqueo de grupos de usuarios

Al intentar denegar el acceso a un grupo de usuarios, asegurarse de que el uso compartido no les permita crear una vía para volver a entrar. Cuando los usuarios pueden crear un enlace público, pueden cerrar sesión y visitar su propio enlace público para acceder a los archivos. Como en ese momento no son usuarios y, por tanto, no son miembros del grupo bloqueado, podrán leer y modificar el archivo.

La solución alternativa recomendada es crear de nuevo la misma regla y denegar el acceso a todos los usuarios que sean `not member of` un grupo que contenga a todos los usuarios de la instalación.

#### Almacenamiento externo

Aunque no es posible acceder a los archivos de los almacenamientos externos a través de Nextcloud, los usuarios que tienen acceso directo al almacenamiento externo pueden, por supuesto, modificar allí los archivos directamente. Por eso se recomienda desactivar la opción `Allow users to mount external storage` cuando se intenta bloquear por completo a los usuarios.

(nc-available-rules-label)=
### Reglas disponibles

Todas las reglas pueden, además, invertirse mediante la opción del operador, con lo que la condición pasa de `is` a `is not`.

- **Etiqueta colaborativa del archivo:** el propio archivo, o cualquiera de las carpetas superiores del propietario del archivo, debe estar etiquetado con la etiqueta.

  :::{note}
  Las etiquetas que se usan en las reglas de control de acceso deben ser etiquetas restringidas; de lo contrario, cualquier usuario puede quitar la etiqueta para volver a acceder al archivo. La mejor forma de conseguirlo es mediante {nc-doc}`admin_manual/file_workflows/automated_tagging`.
  :::

- **Tipo MIME del archivo:** el tipo MIME del archivo, p. ej., `text/plain` para un archivo de texto o `httpd/unix-directory` para una carpeta.

  :::{note}
  Consultar [mimetypealiases.dist.json](https://github.com/nextcloud/server/blob/master/resources/config/mimetypealiases.dist.json) para ver la lista completa de los tipos MIME posibles.
  :::

- **Nombre del archivo:** el nombre del archivo (`is` y `is not` no distinguen entre mayúsculas y minúsculas)
- **Tamaño del archivo:** el tamaño del archivo (*solo disponible al subirlo*)

- **Dirección remota de la solicitud:** un rango de IP (v4 o v6) del usuario que accede
- **Hora de la solicitud:** el intervalo de tiempo y la zona horaria en que se produce la solicitud
- **URL de la solicitud:** la URL que solicita el archivo. (*Es la URL desde la que se sirve el archivo, no la URL que el usuario está viendo en ese momento.*)
- **Agente de usuario de la solicitud:** el agente de usuario del navegador o del cliente del usuario. Los clientes de escritorio, Android e iOS de Nextcloud están disponibles como opciones preconfiguradas.

- **Pertenencia a un grupo de usuarios:** si el usuario es miembro del grupo indicado.
````
