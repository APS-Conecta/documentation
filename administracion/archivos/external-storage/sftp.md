---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Conectar un servidor SFTP como almacenamiento externo: servidor y puerto, autenticación por contraseña o por clave pública, y subcarpeta remota."
---
# SFTP

## Resumen

Esta página explica cómo conectar un servidor SFTP como almacenamiento externo: el servidor y el puerto, la autenticación por contraseña o por clave pública y la subcarpeta remota. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/external_storage/sftp.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El backend SFTP (SSH File Transfer Protocol) de Nextcloud admite autenticación tanto por contraseña como por clave pública.

El campo **Servidor** es obligatorio. El puerto predeterminado es el 22 (SSH).

Para la autenticación por clave pública, se puede generar un par de claves pública/privada desde la configuración **Inicio de sesión SFTP con clave secreta**.

Después de generar las claves, hay que copiar la nueva clave pública al servidor de destino, en `.ssh/authorized_keys`. Nextcloud usará entonces su clave privada para autenticarse en el servidor SFTP.

La **Subcarpeta remota** predeterminada es el directorio raíz (`/`) del servidor SFTP remoto, y se puede introducir cualquier directorio que se desee.

Consultar {nc-doc}`admin_manual/configuration_files/external_storage_configuration_gui` para ver más opciones de montaje e información.

Consultar {nc-doc}`admin_manual/configuration_files/external_storage/auth_mechanisms` para obtener más información sobre los esquemas de autenticación.
````
