---
tipo: explicacion
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Qué es un conflicto de sincronización en el cliente de escritorio, cómo se avisa, cómo resolverlo y la subida experimental de conflictos."
---
# Conflictos

## Resumen

Esta página explica qué ocurre cuando un archivo cambia a la vez en el equipo y en el servidor, cómo lo avisa el cliente de escritorio y cómo resolver el conflicto. Está dirigida a usuarios que sincronizan archivos con el cliente de escritorio.

````{upstream} user_manual/desktop/conflicts.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Descripción general

El cliente de escritorio de Nextcloud sube los cambios locales y descarga los cambios remotos. Cuando un archivo ha cambiado tanto en el lado local como en el remoto entre ejecuciones de sincronización, el cliente no puede resolver la situación por sí solo. Crea un archivo de conflicto con la versión local, descarga la versión remota y notifica al usuario que se produjo un conflicto que requiere atención.

### Ejemplo

Supóngase que hay un archivo llamado `mydata.txt` en la carpeta sincronizada. No ha cambiado desde hace un tiempo y contiene el texto «contenido» tanto en local como en remoto. Ahora, casi al mismo tiempo, el archivo se actualiza localmente para que diga «contenido local», mientras que otra persona actualiza el archivo del servidor para que contenga «contenido remoto».

Al intentar subir los cambios locales, el cliente de escritorio detecta que la versión del servidor también ha cambiado. Crea un conflicto y ahora habrá dos archivos en el equipo local:

- `mydata.txt`, que contiene «contenido remoto»
- `mydata (conflicted copy 2018-04-10 093612).txt`, que contiene «contenido local»

En esta situación, el archivo `mydata.txt` tiene los cambios remotos (y seguirá actualizándose con los nuevos cambios remotos cuando se produzcan), pero los cambios locales no se han enviado al servidor (a menos que el servidor habilite la subida de conflictos; ver más abajo).

El cliente de escritorio notifica esta situación mediante notificaciones del sistema, el icono de la bandeja del sistema y una insignia amarilla de «conflictos sin resolver» en la ventana de ajustes de la cuenta. Al hacer clic en esta insignia se muestra una lista que incluye los conflictos sin resolver, y al hacer clic en uno de ellos se abre una ventana del explorador que apunta al archivo correspondiente.

Para resolver este conflicto, abrir ambos archivos, comparar las diferencias y copiar los cambios locales del archivo «conflicted copy» al archivo base cuando corresponda. En este ejemplo, se podría cambiar `mydata.txt` para que diga «contenido local y remoto» y eliminar el archivo que lleva «conflicted copy» en su nombre. Con eso, el conflicto queda resuelto.

### Subida de conflictos (experimental)

De forma predeterminada, el archivo de conflicto (el archivo con «conflicted copy» en su nombre que contiene los cambios locales en conflicto) no se sube al servidor. La idea es que quien es autor de los cambios es la persona más indicada para resolver el conflicto, y mostrar el conflicto a otros usuarios podría crear confusión.

Sin embargo, en algunos escenarios tiene mucho sentido subir estos cambios en conflicto, de modo que el trabajo local pueda hacerse visible aunque el conflicto no se resuelva de inmediato.

En el futuro podría haber un ajuste para todo el servidor que controle este comportamiento. Por ahora, ya puede probarse estableciendo la variable de entorno `OWNCLOUD_UPLOAD_CONFLICT_FILES=1`.
````
