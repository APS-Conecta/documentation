---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Compartir archivos y carpetas por enlace público, con usuarios, grupos y conversaciones, y con usuarios de servidores federados."
---
# Compartir archivos

## Resumen

Esta página explica cómo compartir archivos y carpetas mediante enlaces públicos, con usuarios, grupos, círculos y conversaciones de Talk, y con usuarios de otros servidores federados, además de cómo ver quién más tiene acceso. Está dirigida a usuarios que comparten o reciben archivos.

````{upstream} user_manual/files/sharing.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los usuarios de Nextcloud pueden compartir archivos y carpetas. Los destinatarios posibles son:

- enlaces públicos
- usuarios
- grupos
- círculos
- conversaciones de Talk
- usuarios o grupos de servidores Nextcloud federados

:::{note}
Algunas opciones pueden no estar disponibles debido a la configuración administrativa. Consulte la [documentación de administración](https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/file_sharing_configuration.html) para más detalles.
:::

### Compartir mediante enlace público

Las carpetas y archivos se pueden compartir mediante enlaces públicos.

Un identificador de 15 dígitos se creará. El enlace tendrá un formato parecido a este: `https://cloud.example.com/s/yxcFKRWBJqYYzp4`.

Existen varias opciones al compartir *carpetas* al público:

- **Solo lectura** para permitir ver y descargar
- **Permitir la subida y la edición**
- Con **Entrega de archivos**, el destinatario solo puede subir archivos a una carpeta sin ver los archivos que ya hay en ella.
- **Ocultar descarga** oculta los botones de descarga y las opciones predeterminadas del clic derecho del navegador, para dificultarle la descarga al destinatario
- **Proteger con contraseña**
- **Fijar fecha de caducidad** desactivará automáticamente el recurso compartido
- **Nota para el destinatario**
- **No compartir** para revertir el recurso compartido
- **Añadir otro enlace** para crear varios enlaces públicos con distintos permisos

Para *archivos* compartidos por enlace, se puede permitir la edición del archivo con una de las soluciones de edición colaborativas de Nextcloud:

:::{note}
La protección con contraseña y la caducidad de los archivos también se propagan mediante la compartición de archivos en federación desde Nextcloud 22.
:::

### Compartir internamente con usuarios y grupos

Al compartir archivos y carpetas con usuarios, grupos, círculos o miembros de una conversación de Talk, se pueden ajustar los permisos de cada uno:

Al recibir un archivo compartido, puede configurar si quiere aceptar automáticamente los siguientes archivos que se compartan con usted, o si prefiere decidir cada vez entre aceptar o rechazar el archivo compartido.

Para ajustar este ajuste, puede dirigirse a **Configuración** > **Personal** > **Compartir**:

:::{warning}
Si el propietario cambia el nombre de un archivo o carpeta compartidos, el nuevo nombre no se reflejará del lado del destinatario. Esto es necesario para evitar que se sobrescriban archivos o carpetas existentes del lado del destinatario.
:::

### Otros con acceso

Para descubrir si alguien tiene acceso a un archivo o carpeta porque se ha compartido una carpeta que lo contiene, haga clic en **Otros con acceso** en la pestaña Compartir:

La lista muestra a todos los usuarios, grupos, chats, etc. que tienen acceso a ese archivo cuando se ha compartido una carpeta que lo contiene en la jerarquía de carpetas:

Haga clic en los tres puntos para:

- ver quién inició el recurso compartido
- ver dónde se inició el recurso compartido (haga clic para ir a la carpeta, en la medida en que tenga acceso a ella)
- dejar de compartir el recurso compartido inicial (solo disponible para el propietario del recurso compartido)

:::{note}
Esta información solo es visible para el propietario de un archivo o carpeta o para los destinatarios con permiso para volver a compartir.
:::

## Recursos compartidos en federación

La compartición de archivos en federación le permite montar archivos compartidos de otros servidores Nextcloud remotos, en efecto creando su propia nube de Nextclouds. Usted puede crear compartir archivos con usuarios en otros servidores Nextcloud.

### Crear una nueva compartición en federación

La compartición de archivos en federación está activada en las instalaciones de Nextcloud por defecto. Siga los siguientes pasos para crear una nueva compartición con otros servidores Nextcloud u ownCloud:

Vaya a su página `Archivos` y haga clic en el icono Compartir del archivo o carpeta que quiere compartir. En la barra lateral, introduzca el usuario y la URL del usuario remoto en este formato: `<username>@<nc-server-url>`. En este ejemplo, resultaría en `bob@cloud.example.com`:

El usuario destinatario recibirá una notificación en su Nextcloud, que les dará la opción de aceptar o rechazar la transferencia entrante:

### Añadir un recurso compartido por enlace público a su Nextcloud

Las páginas de enlaces públicos compartidos de Nextcloud ofrecen la opción de añadir ese archivo o carpeta como recurso compartido en federación a su propia instancia de Nextcloud. Introduzca su `<username>@<nc-server-url>` como se mostró arriba para los recursos compartidos salientes:
````
