---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo listar, restaurar, eliminar y vaciar el contenido de la papelera de un usuario mediante el endpoint WebDAV de la papelera."
---
(nc-dev-webdavtrashbin)=
# Papelera

## Resumen

Esta página explica, para quienes desarrollan clientes, cómo usar el endpoint WebDAV de la papelera de un usuario: listar su contenido y sus propiedades adicionales, restaurar un elemento a su ubicación original, eliminar un elemento y vaciar la papelera.

````{upstream} developer_manual/client_apis/WebDAV/trashbin.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Nextcloud pone a disposición la papelera de un usuario mediante el endpoint de WebDAV.

### Listar el contenido de la papelera

Para obtener todos los archivos de la papelera, hay que enviar un {code}`PROPFIND` normal a
{code}`https://cloud.example.com/remote.php/dav/trashbin/USER/trash`. Esto
listará el contenido de la papelera.

El endpoint ofrece tres propiedades adicionales:

- {code}`{http://nextcloud.org/ns}trashbin-filename`
- {code}`{http://nextcloud.org/ns}trashbin-original-location`
- {code}`{http://nextcloud.org/ns}trashbin-deletion-time`

El resultado es una respuesta normal a un {code}`PROPFIND` y se puede listar como tal.

### Restaurar desde la papelera

Para restaurar desde la papelera, basta con mover el elemento a
la carpeta especial de restauración en {code}`https://cloud.example.com/remote.php/dav/trashbin/USER/restore`.

Esto restaurará automáticamente el elemento a su ubicación original.

### Eliminar de la papelera

Para eliminar de la papelera, basta con realizar un {code}`DELETE` sobre el elemento.

### Vaciar la papelera

Realizar un {code}`DELETE` sobre *<https://cloud.example.com/remote.php/dav/trashbin/USER/trash>*.
````
