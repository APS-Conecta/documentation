---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Subida de archivos grandes por fragmentos (API v2): crear la carpeta, subir y ensamblar los fragmentos, fijar la hora de modificación o abortar."
---
# Subida de archivos por fragmentos

## Resumen

Esta página explica, para quienes desarrollan clientes, cómo subir archivos grandes con la API de fragmentación (versión 2): sus requisitos y límites, cómo crear la carpeta de subida, subir y ensamblar los fragmentos, establecer la hora de modificación y abortar una subida.

````{upstream} developer_manual/client_apis/WebDAV/chunking.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

### Introducción

Subir archivos grandes siempre es algo problemático, ya que la conexión puede interrumpirse,
lo que hará fallar toda la subida. Nextcloud tiene una API de fragmentación con la que se pueden
subir fragmentos más pequeños, que se ensamblarán en el servidor una vez que se hayan subido todos.

Hay dos versiones de la API de fragmentación. La versión 1 es la original, y la versión
2 se creó como una extensión compatible con versiones anteriores para admitir subidas directamente a los
almacenamientos de destino que lo permiten, como S3. La versión 2 es la que se recomienda usar.

La versión 2 trae algunos requisitos y limitaciones adicionales que hay que tener en cuenta
(en comparación con la versión 1):

- Las solicitudes `MKCOL`, `PUT` de cada fragmento y `MOVE` final deben incluir una
  cabecera `Destination` que especifique la ruta de destino del archivo
- El nombre de cada fragmento se limita a un número entre 1 y 10000
- Los fragmentos se ensamblarán en el orden de sus nombres
- El tamaño de los fragmentos debe estar entre 5MB y 5GB (salvo el último fragmento, que puede ser más pequeño)
- Los fragmentos no se pueden descargar desde el directorio de subida

La cabecera `Destination` no es necesaria al abortar una subida con
`DELETE`. El destino y el token de subida del backend se almacenan cuando se
crea la subida.

Nextcloud hará caducar el directorio de subida tras 24 horas de inactividad. Esto significa que, si se inicia una subida y no se termina en 24 horas, el directorio de subida se eliminará y la subida fallará.

### Subida por fragmentos v2

La API solo está disponible para los usuarios registrados de la instancia, y usa la ruta:
`<server>/remote.php/dav/uploads/<userid>`. En esta guía se supondrá:
`https://server/remote.php/dav/uploads/roeland`

#### Iniciar una subida por fragmentos

Una subida por fragmentos se gestiona en 1 carpeta. Esta es la ubicación a la que se suben
todos los fragmentos.

Empezar creando una carpeta con un nombre único. Se pueden listar las carpetas disponibles
actualmente, pero si se usa un UUID aleatorio, las probabilidades de colisión son mínimas.

```console
curl -X MKCOL -u roeland:pass \
    https://server/remote.php/dav/uploads/roeland/myapp-e1663913-4423-4efe-a9cd-26e7beeca3c0 \
    --header 'Destination: https://server/remote.php/dav/files/roeland/dest/file.zip'
```

#### Subir los fragmentos

Una vez creada la carpeta para los fragmentos, se puede empezar a subir los fragmentos.

- El nombre de cada fragmento se limita a un número entre 1 y 10000
- Los fragmentos se ensamblarán en el orden de sus nombres
- El tamaño de los fragmentos debe estar entre 5MB y 5GB (salvo el último fragmento, que puede ser más pequeño)
- Para que se compruebe la cuota del usuario, hay que proporcionar la cabecera `OC-Total-Length` con
  el tamaño total del archivo. Se rechazará el fragmento con un `507 Insufficient Storage error`.
  Si no se proporciona, la subida solo fallará en el paso de ensamblado con `MOVE`.

```console
curl -X PUT -u roeland:pass \
    https://server/remote.php/dav/uploads/roeland/myapp-e1663913-4423-4efe-a9cd-26e7beeca3c0/00001 \
    --data-binary @chunk1 \
    --header 'Destination: https://server/remote.php/dav/files/roeland/dest/file.zip' \
    --header 'OC-Total-Length: 15000000'

curl -X PUT -u roeland:pass \
    https://server/remote.php/dav/uploads/roeland/myapp-e1663913-4423-4efe-a9cd-26e7beeca3c0/00002 \
    --data-binary @chunk2 \
    --header 'Destination: https://server/remote.php/dav/files/roeland/dest/file.zip' \
    --header 'OC-Total-Length: 15000000'
```

Esto subirá 2 fragmentos de un archivo. El primer fragmento tiene un tamaño de 10MB y el segundo
fragmento, de 5MB.

#### Ensamblar los fragmentos

Ensamblar los fragmentos en el servidor consiste en iniciar un movimiento desde el cliente.

```console
curl -X MOVE -u roeland:pass \
    https://server/remote.php/dav/uploads/roeland/myapp-e1663913-4423-4efe-a9cd-26e7beeca3c0/.file \
    --header 'Destination: https://server/remote.php/dav/files/roeland/dest/file.zip' \
    --header 'OC-Total-Length: 15000000'
```

El servidor ensamblará entonces los fragmentos y moverá el archivo final a la carpeta `dest/file.zip`.

##### Establecer la hora de modificación

Si se debe establecer una hora de modificación, se puede hacer añadiéndola como cabecera, con la fecha en tiempo Unix:

```console
curl -X MOVE -u roeland:pass
    --header 'Destination: https://server/remote.php/dav/files/roeland/dest/file.zip' \
    --header 'X-OC-Mtime: 1547545326' \
    --header 'OC-Total-Length: 15000000'
```

En caso contrario, se usará la fecha de subida actual como fecha de modificación.

Después se eliminarán los fragmentos y la carpeta de subida temporal.

#### Abortar la subida

Si hay que abortar la subida, eliminar la carpeta de subida:

```console
curl -X DELETE -u roeland:pass \
    https://server/remote.php/dav/uploads/roeland/myapp-e1663913-4423-4efe-a9cd-26e7beeca3c0/
```

En una subida con Chunking v2, Nextcloud usa los metadatos de subida almacenados para cancelar
la escritura por fragmentos en el backend antes de eliminar la carpeta de subida. Esto también aborta
la subida multipart subyacente cuando el almacenamiento de destino admite subidas
multipart. Esta solicitud no necesita la cabecera `Destination`.

Las subidas sin metadatos de Chunking v2 se gestionan mediante el borrado DAV normal.
````
