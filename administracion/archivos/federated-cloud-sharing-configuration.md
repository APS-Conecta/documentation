---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Configurar la compartición federada entre servidores: crear recursos compartidos federados, servidores de confianza, enlaces públicos y ajustes relacionados."
---
# Configurar la compartición federada

## Resumen

Esta página explica cómo usar la app Federación para compartir archivos entre servidores: crear un recurso compartido federado, mantener una lista de servidores de confianza, crear recursos compartidos federados desde un enlace público y ajustar la configuración y la presentación de los recursos compartidos federados. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/federated_cloud_sharing_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La compartición federada en la nube la gestiona ahora la app Federación (9.0+) y ahora se llama compartición federada. Al activar la app Federación es posible vincular de forma fácil y segura recursos compartidos de archivos entre servidores Nextcloud, lo que en la práctica crea una nube de Nextclouds.

(nc-label-direct-share-link)=
### Crear un nuevo recurso compartido federado

Seguir estos pasos para crear un nuevo recurso compartido federado entre dos servidores Nextcloud. No requiere ninguna acción del usuario en el servidor remoto; basta con unos pocos pasos en el servidor de origen.

1. Activar la app Federación.

2. Ir a la página de administración de Nextcloud y desplazarse hasta la sección Compartir. Comprobar que están activadas **Permitir a los usuarios de este servidor enviar recursos compartidos a otros servidores** y **Permitir a los usuarios de este servidor recibir recursos compartidos de otros servidores**.

3. Ir ahora a la sección Federación. La app Federación permite crear una lista de servidores Nextcloud de confianza, lo que permite a los servidores de confianza intercambiar directorios de usuarios y autocompletar los nombres de los usuarios externos al crear recursos compartidos.

4. Ir ahora a la página Archivos y seleccionar una carpeta para compartir. Hacer clic en el icono de compartir y después introducir el nombre de usuario y la URL del usuario en el servidor Nextcloud remoto. En este ejemplo, es `freda@https://example.com/nextcloud`. Cuando Nextcloud verifica el enlace, lo muestra con la etiqueta **(remoto)**. Hacer clic en esta etiqueta para establecer el enlace.

5. Cuando el enlace se completa correctamente, hay una única opción de compartición, que es **puede editar**.

El recurso compartido puede desconectarse en cualquier momento haciendo clic en el icono de la papelera.

### Configurar servidores Nextcloud de confianza

Es posible crear una lista de servidores Nextcloud de confianza para la compartición federada. Esto permite que los servidores Nextcloud vinculados compartan directorios de usuarios y autocompleten los nombres de usuario en los diálogos de compartición.

También pueden introducirse URL de servidores Nextcloud en el campo **Añadir servidor Nextcloud**.

Una luz roja significa que la conexión falló. La luz amarilla indica una conexión correcta sin intercambio de nombres de usuario. La luz verde indica una conexión correcta con intercambio de nombres de usuario.

El requisito previo para un estado verde es que los servidores de confianza estén registrados en los dos servidores Nextcloud que interactúan. Además, debe haberse ejecutado `occ federation:sync-addressbooks` (forma parte de la lista de trabajos cron). El retraso hasta que se ejecuta el cron depende de la configuración local de la frecuencia del cron.

(nc-label-public-link-share)=
### Crear recursos compartidos federados mediante un enlace público

Marcar la entrada {guilabel}`Compartir enlace` para mostrar más opciones de compartición (que se describen con más detalle en {nc-doc}`admin_manual/configuration_files/file_sharing_configuration`). Es posible crear un recurso compartido federado dejando que Nextcloud cree un enlace público y enviándolo después por correo electrónico a la persona con la que se quiere crear el recurso compartido.

Opcionalmente puede establecerse una contraseña y una fecha de caducidad. Cuando el destinatario recibe el correo, debe hacer clic en el enlace o copiarlo en un navegador web. Verá una página que muestra una miniatura del archivo, con un botón para {guilabel}`Añadir a tu Nextcloud`.

El destinatario debe hacer clic en el botón {guilabel}`Añadir a tu Nextcloud`. En la siguiente pantalla, el destinatario debe introducir la URL de su servidor Nextcloud y pulsar la tecla Intro.

Al destinatario le queda un paso más: confirmar la creación del enlace de recurso compartido federado en la nube haciendo clic en el botón **Aceptar**.

Desmarcar la casilla {guilabel}`Compartir enlace` para desactivar cualquier recurso compartido federado en la nube creado de esta forma.

### Consejos de configuración

La sección Compartir de la página de administración permite controlar cómo gestionan los usuarios los recursos compartidos federados en la nube:

- Marcar {guilabel}`Forzar la protección por contraseña` para exigir contraseñas en los recursos compartidos por enlace.
- Marcar `Set default expiration date` para exigir una fecha de caducidad en los recursos compartidos por enlace.
- Marcar {guilabel}`Permitir subidas públicas` para permitir la compartición de archivos en ambos sentidos.
- Si se producen tiempos de espera agotados al descargar o subir archivos grandes, puede usarse la opción `davstorage.request_timeout` del `config.php` para aumentar el tiempo de espera. El valor predeterminado es de 30 segundos.

El servidor web Apache debe tener activado `mod_rewrite`, y `trusted_domains` debe estar correctamente configurado en `config.php` para permitir conexiones externas (consultar {nc-doc}`admin_manual/installation/installation_wizard`). Conviene también activar SSL para cifrar todo el tráfico entre los servidores.

El servidor Nextcloud crea el enlace de recurso compartido a partir de la URL que se usó para iniciar sesión en el servidor, así que hay que asegurarse de iniciar sesión en el servidor con una URL accesible para los usuarios. Por ejemplo, si se inicia sesión mediante la dirección IP del servidor en la LAN, como `http://192.168.10.50`, la URL del recurso compartido será algo parecido a `http://192.168.10.50/nextcloud/index.php/s/jWfCfTVztGlWTJe`, que no es accesible fuera de la LAN. Lo mismo ocurre con el nombre del servidor: para el acceso desde fuera de la LAN hay que usar un nombre de dominio completo como `http://myserver.example.com`, en lugar de `http://myserver`.

(nc-federated_shares_display)=
### Cambiar la presentación de los recursos compartidos federados

De forma predeterminada, los recursos compartidos federados se muestran en una sección aparte de la interfaz de Nextcloud. Es posible cambiar este comportamiento y mostrarlos en la misma sección que los recursos compartidos internos. Esto se controla con un comando `occ`:

```bash
occ config:app:set --value false --type boolean files_sharing show_federated_shares_as_internal
```

Establecer el valor en `true` para mostrar los recursos compartidos federados mezclados con los internos, o en `false` para mantenerlos en una sección aparte (predeterminado).
````
