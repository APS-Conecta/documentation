---
tipo: referencia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Variables de entorno que controlan el cliente de escritorio, con sus valores predeterminados, y su comportamiento cuando queda poco espacio en disco."
---
# Variables de entorno

## Resumen

Esta página enumera las variables de entorno que controlan el comportamiento del cliente de escritorio y sus valores predeterminados, y explica cómo actúa el cliente cuando queda poco espacio en disco. Está dirigida a usuarios que necesitan ajustar el cliente sin modificar su archivo de configuración.

````{upstream} user_manual/desktop/envvars.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El comportamiento del cliente también puede controlarse mediante variables de entorno. El valor de las variables de entorno prevalece sobre los valores del archivo de configuración.

Las variables de entorno son:

- *OWNCLOUD_CHUNK_SIZE* (predeterminado: 5242880; 5 MiB) – Especifica el tamaño de fragmento de los archivos subidos en bytes. Aumentar este valor puede ayudar con problemas de sincronización en determinadas configuraciones.
- *OWNCLOUD_TIMEOUT* (predeterminado: 300 s) – El tiempo de espera de las conexiones de red en segundos.
- *OWNCLOUD_CRITICAL_FREE_SPACE_BYTES* (predeterminado: 512\*1000\*1000 bytes) - El espacio mínimo en disco necesario para funcionar. Se produce un error fatal si hay menos espacio libre disponible.
- *OWNCLOUD_FREE_SPACE_BYTES* (predeterminado: 1000\*1000\*1000 bytes) - Las descargas que reducirían el espacio libre por debajo de este valor se omiten. Hay más información en la sección «Poco espacio en disco».
- *OWNCLOUD_MAX_PARALLEL* (predeterminado: 6) - Número máximo de trabajos en paralelo.
- *OWNCLOUD_BLACKLIST_TIME_MIN* (predeterminado: 25 s) - Tiempo de espera mínimo para los archivos en la lista de bloqueo.
- *OWNCLOUD_BLACKLIST_TIME_MAX* (predeterminado: 24\*60\*60 s; un día) - Tiempo de espera máximo para los archivos en la lista de bloqueo.
- *OWNCLOUD_HTTP2_ENABLED* (predeterminado: false) - Si el cliente debe comunicarse con el servidor mediante HTTP/2. (Puede no ser compatible con todas las configuraciones de servidor)

### Poco espacio en disco

Cuando queda poco espacio en disco, el cliente de {vendor}`Nextcloud` no puede sincronizar todos los archivos. Esta sección describe su comportamiento en una situación de poco espacio en disco, así como las opciones que influyen en él.

1. La sincronización de una carpeta se interrumpe por completo si el espacio restante en disco cae por debajo de 512 MB. Este umbral puede ajustarse con la variable de entorno `OWNCLOUD_CRITICAL_FREE_SPACE_BYTES`.

2. Las descargas que reducirían el espacio libre en disco por debajo de 1 GB se omiten o se interrumpen. La descarga se reintenta periódicamente y el resto de la sincronización no se ve afectada. Este umbral puede ajustarse con la variable de entorno `OWNCLOUD_FREE_SPACE_BYTES`.
````
