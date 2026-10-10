---
tipo: explicacion
audiencia: administracion
apps: [gestion, AIO]
resumen: "Almacenamiento externo en APS Conecta Gestión: la app queda desactivada, los documentos viven en carpetas de equipo y la copia diaria no cubre montajes."
---
# Almacenamiento externo

## Contexto

Esta sección reúne, para quienes administran el servidor, las páginas de la plataforma base sobre los backends del almacenamiento externo —Amazon S3, FTP/FTPS, local, la propia plataforma, almacenamiento de objetos OpenStack, SFTP, SMB/CIFS y WebDAV— y sus mecanismos de autenticación. Los monta la app Soporte de almacenamiento externo, que viene incluida en la plataforma y desactivada de forma predeterminada; {doc}`../external-storage-configuration-gui` explica cómo se activa y se configura.

## Diseño

APS Conecta Gestión no usa almacenamiento externo, y su instalación deja la app como la entrega la plataforma:

- **La app queda desactivada.** Ninguna fase de provisión la activa, y el asistente de AIO arranca con `NEXTCLOUD_STARTUP_APPS` vacío, sin instalaciones ni activaciones al inicio: las aplicaciones de la suite vienen dentro de la imagen.
- **Los documentos viven en carpetas de equipo.** La provisión crea el árbol del centro como carpetas de equipo (Group Folders) dentro del almacenamiento de la instancia, con el acceso concedido por grupo; {doc}`/administracion/usuarios-y-grupos/index` describe ese modelo.
- **Sin montajes locales.** El contenedor de la plataforma en AIO no ve los directorios del servidor, salvo que el asistente se cree con la variable `NEXTCLOUD_MOUNT`. La orden de arranque que genera la suite no la lleva, y sin ella el entrypoint de AIO fija `files_external_allow_create_new_local` en `false` en cada arranque: la interfaz web y las API no crean montajes del backend {doc}`local`, que solo `occ` puede crear.

## Compromisos y límites

- **La copia diaria no cubre montajes externos.** La copia de borg del asistente respalda la base de datos, los archivos y la configuración del asistente, pero no lo que se monta con almacenamiento externo. Un montaje externo quedaría fuera de la copia y de su restauración.
- **Nada vigila la app.** La política de aplicaciones no la nombra, y el informe de divergencia revisa solo las aplicaciones de `custom_apps`, mientras que esta viene con la plataforma. La política deja todas las aplicaciones al grupo `admin`: si una cuenta de ese grupo activa el almacenamiento externo, la re-provisión semanal no lo desactiva y ningún informe lo nombra.
- **Un directorio con el mismo nombre.** El volumen de datos contiene `files_external/rootcerts.crt` aunque la app esté desactivada: es el paquete de certificados que amplía la fase 07, con el certificado intermedio de `www.ispch.gob.cl`, el servidor nacional del ISP que entrega solo su certificado final, y, en una instalación por IP, la CA del instalador. El archivo sobrevive a un reinicio pero no a un volumen borrado, y por eso lo escribe una fase de provisión.

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
