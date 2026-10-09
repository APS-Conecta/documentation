---
tipo: explicacion
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Cómo se guardan y caducan las versiones de los archivos, cómo restaurarlas o descargarlas, y que se pueden nombrar o eliminar."
---
# Control de versiones

## Resumen

Esta página explica cuándo se crean versiones de un archivo, con qué patrón caducan y cuánto espacio pueden ocupar, cómo restaurar o descargar una versión, y que una versión se puede nombrar, para excluirla de la caducidad automática, o eliminar manualmente. Está dirigida a usuarios que necesitan recuperar estados anteriores de sus archivos.

````{upstream} user_manual/files/version_control.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud admite un sistema sencillo de control de versiones para archivos. El versionado crea copias de seguridad de los archivos, accesibles mediante la pestaña Versiones de la barra lateral Detalles. Esta pestaña contiene el historial del archivo, desde donde puede revertir un archivo a cualquier versión anterior. Solo se guarda una nueva versión si han pasado al menos dos minutos desde que se creó la última. Las versiones se almacenan en `data/[user]/files_versions`.

Para restaurar una versión específica de un archivo, haga clic en la flecha circular a la derecha. Haga clic en la fecha específica para descargarlo.

La app de versiones hace caducar automáticamente las versiones antiguas para asegurarse de que no se quede sin espacio. Para eliminar las versiones antiguas se usa este patrón:

- Durante el primer segundo se conserva una versión
- Durante los primeros 10 segundos, Nextcloud conserva una versión cada 2 segundos
- Durante el primer minuto, Nextcloud conserva una versión cada 10 segundos
- Durante la primera hora, Nextcloud conserva una versión cada minuto
- Durante las primeras 24 horas, Nextcloud conserva una versión cada hora
- Durante los primeros 30 días, Nextcloud conserva una versión cada día
- Después de los primeros 30 días, Nextcloud conserva una versión cada semana

Las versiones se ajustan a este patrón cada vez que se genera una nueva versión.

La app de versiones nunca usa más del 50% del espacio actualmente disponible. Si las versiones almacenadas exceden este límite, Nextcloud borra las versiones más antiguas hasta cumplir con esta restricción.

### Nombramiento de versiones

Puede darle un nombre a una versión.

Cuando una versión tiene nombre. Será excluida del proceso automático de expiración.

### Borrando una versión

Puede también borrar una versión manualmente sin esperar por el proceso automático de expiración.
````
