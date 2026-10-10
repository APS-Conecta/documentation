---
tipo: guia
audiencia: desarrollo
apps: [gestion]
resumen: "Levantar la pila de desarrollo de gestion: sus servicios, la imagen derivada con Xdebug, los permisos de los montajes y el lugar donde corre el humo."
---
# Entorno

## Objetivo

Esta guía levanta la pila de desarrollo de gestion: la composición de Docker local sobre la que se trabajan la provisión, el tema y las aplicaciones montadas. La pila es desechable: el objetivo `install` del Makefile la reconstruye. Un establecimiento no corre esta pila: instala la suite con el instalador AIO, descrito en {doc}`/administracion/aio`. territorio, farmacia y estadistica tienen además su propia instancia de prueba, descrita en {doc}`desarrollo-de-aplicaciones`.

La pila Compose se mantiene como régimen interino mientras la suite pasa a AIO: `install` la levanta con `up` como antes, y la provisión llega al contenedor por la misma vía que en AIO, `docker exec`.

### Servicios

| Servicio | Imagen | Función |
|---|---|---|
| `nextcloud` | `nextcloud:34-apache` | El servidor, publicado solo en loopback en `HTTP_PORT` (8180 en la plantilla `.env.example`) |
| `cron` | La misma imagen | Ejecuta los trabajos de fondo con `/cron.sh` |
| `db` | `postgres:18-alpine` | La base de datos, sin puerto publicado |
| `redis` | `redis:8-alpine` | Caché y bloqueos de archivos y transacciones |
| `eurooffice` | `ghcr.io/euro-office/documentserver:latest` | El servidor de documentos, publicado solo en loopback en `OFFICE_PORT` (9980 en la plantilla); trae su propio PostgreSQL, Redis y RabbitMQ y no se conecta a los de la pila |

Cada imagen está fijada por digest; la etiqueta queda solo para leerla. El objetivo `images` refresca los digests de `compose.yaml` y `Dockerfile.dev` juntos, e `images-check` informa si alguna etiqueta se movió más allá de su digest.

`nextcloud` y `cron` corren la misma imagen sobre los mismos volúmenes: `cron.php` carga las aplicaciones, así que también necesita `custom_apps` y `themes`. Un ancla de YAML hace que esa igualdad sea estructural. Los directorios `apps/` y `themes/` del repositorio se montan sobre `custom_apps` y `themes` del contenedor: el código propio se edita en vivo, sin reconstruir la imagen.

La tienda de aplicaciones está apagada por variable de entorno, `NC_appstoreenabled` en `"0"`, en `nextcloud` y en `cron`: el `occ upgrade` que corre el entrypoint ante un cambio de imagen volvería a descargar de la tienda cada aplicación activa y anularía los paquetes fijados.

Todos los servicios usan `restart: unless-stopped`: la pila vuelve tras un reinicio del anfitrión, y una pila detenida a propósito sigue detenida. El costo aceptado es que un computador de desarrollo levanta la pila completa al encender, Euro-Office incluido; el objetivo `down` es la salida.

### Imagen derivada con Xdebug

La depuración paso a paso usa una imagen derivada solo para desarrollo. `compose.dev.yaml` cambia únicamente de dónde sale la imagen del servicio `nextcloud` y hereda todo lo demás de `compose.yaml`; ni `compose.yaml` ni la imagen oficial se modifican.

`Dockerfile.dev` parte del mismo digest que corre `compose.yaml` y solo agrega Xdebug 3 por PECL: una imagen de depuración sobre otra compilación depuraría algo distinto de lo que se despliega. `dev/xdebug.ini` activa el modo `debug`, inicia una sesión solo ante un disparador (`XDEBUG_TRIGGER` o `XDEBUG_SESSION`) y conecta hacia el editor en el anfitrión por `host.docker.internal`. La configuración de VS Code confirmada en `.vscode/launch.json`, «Listen for Xdebug (APS Conecta)», escucha en el puerto 9003 y mapea `/var/www/html/custom_apps` a `apps/`.

### Permisos de los montajes

En Linux, un montaje conserva el dueño del anfitrión, pero el usuario del servidor web, uid 33, debe poder escribir en `custom_apps` y `themes`. El objetivo `fix-mount-perms` asigna `www-data` como dueño y el grupo del anfitrión con permiso de escritura de grupo, desde dentro del contenedor y sin `sudo` en el anfitrión. `up` y `up-dev` lo vuelven a aplicar cada vez. Un `chown www-data:www-data` simple dejaba los archivos en solo lectura para el anfitrión (B-002).

## Requisitos

- Docker Engine 24 o posterior con Compose v2, `make` y `git`. Los comandos corren en el anfitrión, desde la raíz del repositorio.
- Memoria para Euro-Office, unos 2,5 GB; el piso multiusuario de unos 8 GB es un requisito de todo anfitrión.
- Un establecimiento: `SITE` en `.env` nombra un `sites/<slug>/site.sh`, que `scripts/deis.py` escribe a partir del registro DEIS. El repositorio no trae ningún establecimiento, y el archivo queda fuera de git, como `.env`.

## Pasos

1. Ejecutar el objetivo `setup` del Makefile. Genera los cuatro secretos en `.env` con modo 600 y se niega a correr si `.env` ya existe.
2. Fijar `SITE` en `.env` con el establecimiento elegido.
3. Ejecutar el objetivo `install`. Levanta la pila, ejecuta las fases de provisión, guarda el detalle en `.install.log` y termina con un resumen del establecimiento.
4. Repetir `install` después de editar `sites/<slug>/site.sh` o de un `git pull`: converge y omite en segundos lo ya aplicado.
5. Para depurar paso a paso, ejecutar el objetivo `up-dev` en lugar de `up`.
6. En VS Code, iniciar «Listen for Xdebug (APS Conecta)» y enviar una solicitud con el disparador de Xdebug.
7. Detener la pila con el objetivo `down`, que conserva los volúmenes. Para recuperar la memoria de Euro-Office sin detener el resto, ejecutar el objetivo `office-down`.

## Verificación

- El resumen de `install` nombra el establecimiento con su número de equipos, carpetas de grupo y permisos, y termina con la dirección `http://localhost:` seguida de `HTTP_PORT`.
- El objetivo `test` corre los chequeos estáticos, que no necesitan una pila. Sin una pila AIO en marcha, informa como omitidos los chequeos contra el contenedor, el humo y el humo de oficina.
- El humo (`smoke`) solo responde una instancia AIO: en la pila Compose falla por diseño con un mensaje que nombra el contenedor AIO, de modo que el chequeo de salud con que termina `install` informa `health: FAIL`.
- El humo completo corre en el workflow Clean boot de gestion, sobre un banco de pruebas AIO desechable, después de instalar un establecimiento generado:

  ```bash
  bash scripts/aio-testbed.sh up
  ```

  El banco necesita un anfitrión Ubuntu con Docker y al menos 3,5 GiB disponibles; nunca ocupa los puertos 80 ni 443 del anfitrión. Las compuertas están en {doc}`calidad`.

## Problemas frecuentes

- **Archivos de `apps/` o `themes/` de solo lectura en el anfitrión.** Ejecutar el objetivo `fix-mount-perms`.
- **La pila Compose y el banco AIO corren a la vez.** La provisión elige el contenedor AIO. Para provisionar la pila Compose, fijar `NC_CONTAINER` en `.env`.
- **Xdebug no escribe registro.** Es deliberado: Xdebug se niega a abrir un registro que no le pertenece en un directorio que todos pueden escribir, como `/tmp` (B-006).
- **El editor de documentos no carga desde otro equipo.** `localhost:9980` es el loopback del navegador, no el del servidor, y el editor lo informa como un problema de token. Fijar `OFFICE_PUBLIC_URL` en `.env` con una dirección que el navegador alcance, en https si el servidor usa https. El humo de oficina no detecta este error porque corre en el mismo anfitrión.
- **Una contraseña cambiada en `.env` no cambia el inicio de sesión.** El servidor lee la contraseña de administración solo al instalarse: primero se restablece en el servidor y después se actualiza `.env`.
