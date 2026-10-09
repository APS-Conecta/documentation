---
tipo: referencia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "El cliente de línea de comandos nextcloudcmd: paquetes, sintaxis, opciones, credenciales, lista de exclusión y un ejemplo de sincronización."
---
# Uso del cliente de línea de comandos

## Resumen

Esta página describe `nextcloudcmd`, el cliente de línea de comandos que realiza una única sincronización entre un directorio local y el servidor: dónde obtenerlo, su sintaxis y opciones, el manejo de credenciales y la lista de exclusión. Está dirigida a usuarios que sincronizan desde la terminal o mediante scripts.

````{upstream} user_manual/desktop/commandline.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los paquetes del cliente de Nextcloud contienen un cliente de línea de comandos, `nextcloudcmd`, que puede usarse para sincronizar archivos de Nextcloud con los equipos cliente.

`nextcloudcmd` realiza una única *ejecución de sincronización* y después finaliza el proceso de sincronización. De este modo, `nextcloudcmd` procesa las diferencias entre los directorios del cliente y del servidor y propaga los archivos para llevar ambos repositorios al mismo estado. A diferencia del cliente con interfaz gráfica, `nextcloudcmd` no repite las sincronizaciones por sí mismo. Tampoco supervisa los cambios en el sistema de archivos.

### Instalación

| SO | Paquete |
|---|---|
| Alpine | <https://pkgs.alpinelinux.org/package/edge/community/x86_64/nextcloud-client> |
| Debian | <https://packages.debian.org/search?suite=all&arch=any&searchon=names&keywords=nextcloud-desktop-cmd> |
| Fedora | <https://packages.fedoraproject.org/pkgs/nextcloud-client/nextcloud-client/> |
| Ubuntu | <https://packages.ubuntu.com/search?keywords=nextcloud-desktop-cmd> |
| Ubuntu (PPA) | <https://launchpad.net/~nextcloud-devs/+archive/ubuntu/client> |
| Windows | <https://nextcloud.com/install/#install-clients> |

### Uso

Para invocar `nextcloudcmd`, hay que indicar la URL del repositorio local y la del remoto con el siguiente comando:

```
nextcloudcmd [OPTIONS...] sourcedir nextcloudurl
```

donde `sourcedir` es el directorio local y `nextcloudurl` es la URL del servidor.

Otras opciones de línea de comandos que admite `nextcloudcmd` son las siguientes:

- `--path`: sustituye la carpeta raíz remota predeterminada por una subcarpeta concreta del servidor (p. ej.: /Documents sincronizaría la subcarpeta Documents del servidor)
- `--user`, `-u` *\<user\>*: usa `user` como nombre de inicio de sesión.
- `--password`, `-p` *\<password\>*: usa *password* como contraseña.
- `-n`: usa `netrc(5)` para iniciar sesión.
- `--non-interactive`: no hace preguntas e intenta leer $NC_USER y $NC_PASSWORD del entorno.
- `--silent`, `--s`: suprime la salida detallada del registro.
- `--trust`: confía en cualquier certificado SSL, incluidos los no válidos.
- `--httpproxy` *http://[user@pass:]\<server\>:\<port\>*: usa *server* como proxy HTTP.
- `--exclude` *\<file\>*: archivo de lista de exclusión
- `--unsyncedfolders` *\<file\>*: archivo que contiene la lista de carpetas no sincronizadas (sincronización selectiva)
- `--max-sync-retries` *\<n\>*: reintenta como máximo n veces (3 de forma predeterminada)
- `-h`: sincroniza los archivos ocultos, no los ignora

### Manejo de credenciales

`nextcloudcmd` requiere que el usuario indique el nombre de usuario y la contraseña mediante el patrón de URL estándar, p. ej.:

```
$ nextcloudcmd /home/user/my_sync_folder https://carla:secret@server/nextcloud
```

Para sincronizar el directorio `Music` de Nextcloud con el directorio local `media/music`, a través de un proxy que escucha en el puerto `8080` y en una máquina pasarela con la dirección IP `192.168.178.1`, la línea de comandos sería:

```
$ nextcloudcmd --httpproxy http://192.168.178.1:8080 --path /Music \
              $HOME/media/music \
              https://server/nextcloud
```

`nextcloudcmd` pedirá el nombre de usuario y la contraseña, a menos que se hayan especificado en la línea de comandos o se haya pasado `-n`.

### Lista de exclusión

`nextcloudcmd` requiere acceso a un archivo de lista de exclusión. Este debe estar instalado junto con `nextcloudcmd` y, por tanto, disponible en una ubicación del sistema, estar colocado junto al binario como `sync-exclude.lst` o especificarse explícitamente con la opción `--exclude`.

El contenido requerido del archivo es un elemento de exclusión por línea, donde se permiten comodines, p. ej.:

```
~*.tmp
._*
]Thumbs.db
]photothumb.db
System Volume Information
```

### Ejemplo

- Sincronizar un directorio local con el directorio indicado del servidor nextcloud

```
$ nextcloudcmd --path /<Directory_that_has_been_created> /home/user/<my_sync_folder> \
https://<username>:<secret>@<server_address>
```
````
