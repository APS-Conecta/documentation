---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo listar las versiones de un archivo y restaurar una de ellas mediante el endpoint WebDAV de versiones."
---
(nc-dev-webdavversions)=
# Versiones

## Resumen

Esta página explica, para quienes desarrollan clientes, cómo listar las versiones de un archivo con una solicitud `PROPFIND` y cómo restaurar una versión moviéndola a la carpeta especial de restauración del endpoint WebDAV.

````{upstream} developer_manual/client_apis/WebDAV/versions.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Nextcloud pone a disposición las versiones de los archivos mediante el endpoint de WebDAV.

### Listar las versiones de un archivo

Para obtener todas las versiones de un archivo, hay que enviar un {code}`PROPFIND` normal a
{code}`https://cloud.example.com/remote.php/dav/versions/USER/versions/FILEID`. Esto
listará las versiones de este archivo.

El nombre es la marca de tiempo de la versión.

### Restaurar una versión

Para restaurar una versión, basta con mover la versión
a la carpeta especial de restauración en {code}`https://cloud.example.com/remote.php/dav/versions/USER/restore`.
````
