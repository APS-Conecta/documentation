---
tipo: referencia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Opciones de línea de comandos para iniciar el cliente de escritorio: registro, directorio de configuración e inicio en segundo plano."
---
# Opciones de línea de comandos

## Resumen

Esta página enumera las opciones con las que puede iniciarse el cliente de escritorio desde la línea de comandos, sobre todo las de registro, el directorio de configuración y el inicio en segundo plano. Está dirigida a usuarios que inician el cliente desde una terminal o un script.

````{upstream} user_manual/desktop/options.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El cliente de escritorio de Nextcloud puede iniciarse con el comando `nextcloud`. Se admiten las siguientes opciones:

- `nextcloud -h` o `nextcloud --help`: muestra todas las opciones del comando.

Las demás opciones son:

- `--logwindow`: abre una ventana que muestra la salida del registro.
- `--logfile` *\<filename\>*: escribe la salida del registro en el archivo especificado. Para escribir en stdout, especificar *-* como nombre de archivo.
- `--logdir` *\<name\>*: escribe la salida del registro de cada sincronización en un archivo nuevo dentro del directorio especificado.
- `--logexpire` *\<hours\>*: elimina los registros más antiguos que el valor especificado (en horas). Este comando se usa con `--logdir`.
- `--logflush`: vacía (flush) el archivo de registro después de cada acción de escritura.
- `--logdebug`: también incluye en el registro los mensajes de nivel de depuración (equivale a establecer la variable de entorno QT_LOGGING_RULES="qt.\*=true;\*.debug=true").
- `--confdir` *\<dirname\>*: usa el directorio de configuración especificado.
- `--background`: inicia la aplicación en segundo plano (es decir, sin abrir el diálogo principal).
````
