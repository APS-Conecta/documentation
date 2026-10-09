---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Compartir archivos con usuarios de otros servidores, directamente con su dirección o mediante un enlace enviado por correo electrónico."
---
# Usar recursos compartidos en federación

## Resumen

Esta página explica cómo crear un recurso compartido en federación con un usuario de otro servidor, ya sea con su nombre de usuario y la URL de su servidor o mediante un enlace enviado por correo electrónico, y cómo quitarlo. Está dirigida a usuarios que comparten archivos fuera de su propio servidor.

````{upstream} user_manual/files/federated_cloud_sharing.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La compartición de archivos en federación le permite montar archivos compartidos de otros servidores Nextcloud remotos, en efecto creando su propia nube de Nextclouds. Usted puede crear compartir archivos con usuarios en otros servidores Nextcloud.

### Crear un nuevo recurso compartido en federación

La compartición de archivos en federación está activada en las instalaciones de Nextcloud por defecto, ya sean nuevas o actualizadas. Siga los siguientes pasos para crear una nueva compartición con otros servidores Nextcloud u ownCloud 9+:

1. Vaya a su página {guilabel}`Archivos` y haga clic en el icono **Compartir** del archivo o directorio que quiere compartir. En la barra lateral, introduzca el nombre de usuario y la URL del usuario remoto con este formato: `<username>@<oc-server-url>`. El formulario confirma automáticamente la dirección que escribe y la etiqueta como «remoto». Haga clic en la etiqueta.

2. Cuando su servidor Nextcloud local establezca una conexión correcta con el servidor Nextcloud remoto, verá una confirmación. Su única opción para compartir es **Puede editar**.

Haga clic en el botón **Compartir** en cualquier momento para ver con quién ha compartido su archivo. Elimine su compartición por enlace en cualquier momento haciendo clic en el icono de la papelera. Esto solo borra el enlace de la compartición, y no borra ningún archivo.

### Crear un nuevo recurso compartido en la nube federada por correo electrónico

Utilice este método cuando está compartiendo con usuarios en ownCloud versión 8.x o anterior.

Si no conoce el nombre de usuario o la URL, puede hacer que Nextcloud cree el enlace por usted y lo envíe por correo electrónico a su destinatario.

Cuando su destinatario reciba su correo electrónico, tendrá que seguir una serie de pasos para completar el enlace compartido. Primero debe abrir en un navegador web el enlace que usted le envió y, después, hacer clic en el botón **Añadir a tu Nextcloud**.

El botón **Añadir a tu Nextcloud** se convierte en un formulario, y el recipiente tiene que introducir la URL de su servidor Nextcloud u ownCloud en este campo, y pulsar la tecla de retorno o hacer clic en la flecha.

A continuación verán un diálogo que les solicita confirmación. Todo lo que queda por hacer es hacer clic en el botón **Añadir como archivo compartido remoto** y ya lo han conseguido.

Elimine su compartición por enlace en cualquier momento, haciendo clic en el icono de la papelera. Esto solo borra el enlace de la compartición, y no borra ningún archivo.
````
