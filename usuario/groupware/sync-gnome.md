---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Conectar el escritorio GNOME mediante Cuentas en línea para ver calendarios, contactos, tareas y archivos en Evolution, Nautilus y sus apps."
---
# Sincronizar con el escritorio GNOME

## Resumen

Esta página explica cómo añadir la cuenta en Cuentas en línea de GNOME para que calendarios, contactos, tareas y archivos aparezcan en Evolution, en las apps de GNOME y en el gestor de archivos Nautilus. Está dirigida a usuarios que trabajan con el escritorio GNOME.

````{upstream} user_manual/groupware/sync_gnome.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El [Escritorio GNOME](https://www.gnome.org) tiene soporte nativo para los calendarios, contactos y tareas de Nextcloud, que serán mostrados por el manejador de información personal (PIM) Evolution, o las apps de Calendario, Tareas, y Contactos. Similarmente, Archivos se integra con el manejador de archivos Nautilus a traves de WebDAV. Este último funciona solo cuando el computador está conectado.

Siga estos pasos para conseguirlo:

1. En los ajustes de GNOME, abra Cuentas en línea.
2. En "Añadir una cuenta", elija `Nextcloud`.
3. Introduzca la URL de su servidor, su nombre de usuario y su contraseña. Si ha habilitado la autenticación de dos factores (2FA), necesita generar una contraseña/token de aplicación, porque Cuentas en línea de GNOME [aún no admite el inicio de sesión WebFlow de Nextcloud](https://gitlab.gnome.org/GNOME/gnome-online-accounts/issues/81) ({nc-ref}`Más información <managing_devices>`).
4. En la siguiente ventana, seleccione a qué recursos debe acceder GNOME y pulse el botón **Cerrar** para cerrar el diálogo.

Las tareas, calendarios y contactos de Nextcloud aparecerán en el gestor de información personal (PIM) Evolution y las aplicaciones de Tareas, Contactos y Calendario.

Archivos se mostrará como recurso WebDAV en el gestor de archivos Nautilus y también estará disponible en los diálogos de abrir/guardar archivos de GNOME. Los documentos deberían quedar integrados en la aplicación de Documentos de GNOME.

Todos los recursos también deberían estar indexados, y puede encontrarlos al pulsar la tecla Windows e introducir un término de búsqueda.
````
