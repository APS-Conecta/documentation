---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo adaptar una ExApp a HaRP: cliente FRP con start.sh, certificados y permisos, ejecución con un usuario que no es root y una prueba de integración."
---
# Adaptar las ExApps a HaRP

## Resumen

Esta página explica cómo adaptar una ExApp al proxy inverso HaRP: qué tener en cuenta en la integración, los pasos para incluir el cliente FRP con start.sh, cómo ejecutar la ExApp con un usuario que no es root y un ejemplo de prueba de integración. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/development_overview/ExAppHarpIntegration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Síntesis

HaRP es un sistema de proxy inverso diseñado para simplificar el flujo de despliegue
de AppAPI de Nextcloud 32.

Permite la comunicación directa entre los clientes y las ExApps, sin pasar por
la instancia de Nextcloud, para mejorar el rendimiento y reducir la complejidad
que tradicionalmente se asocia a las configuraciones con *DockerSocketProxy*.

HaRP proporciona un transporte [basado en FRP](https://github.com/fatedier/frp)
para las ExApps y recomienda copiar
[start.sh](https://github.com/nextcloud/HaRP/blob/main/exapps_dev/start.sh)
en la imagen de la ExApp y usarlo como punto de entrada (entrypoint) del contenedor.
El script instala o inicia el cliente FRP y ejecuta el proceso de la app.

:::{warning}
Se recomienda encarecidamente empezar a dar soporte a HaRP en las ExApps desde el comienzo
de Nextcloud 32, ya que la antigua forma [DSP](https://github.com/nextcloud/docker-socket-proxy)
quedará obsoleta y marcada para su eliminación en Nextcloud 35.

Añadir soporte para HaRP es totalmente compatible con el sistema DSP existente,
por lo que no será necesario mantener dos tipos de versiones separadas de la ExApp.
:::

### Consideraciones clave de integración

- **Conexión a HaRP con FRPC**: la ExApp no necesita exponer ningún puerto al host
  ni ser accesible desde el servidor de Nextcloud. El cliente FRP (*FRPC*) dentro del
  contenedor de la ExApp creará una conexión saliente hacia HaRP, que hará de proxy
  de las solicitudes de los clientes hacia la ExApp.
- **Permisos de archivos**: AppAPI puede copiar archivos de certificados en el contenedor y
  ejecutar comandos dentro de él. Si el contenedor ejecuta el proceso principal como un
  usuario de servicio que no es root, las escrituras de archivos o las ejecuciones (exec) de AppAPI pueden fallar, a menos que
  las rutas de destino sean escribibles/legibles por ese usuario.
- **Certificados y configuración de FRP**: HaRP espera que los archivos de certificados de FRP estén accesibles en
  */certs/frp* (client.crt, client.key, ca.crt). La ruta de configuración del cliente FRP
  que usan muchos scripts *start.sh* de ejemplo es */frpc.toml*.
- **Comandos que requieren root**: algunos pasos de configuración (por ejemplo, actualizar los paquetes de CA con
  *update-ca-certificates*) requieren root; puede que AppAPI necesite ejecutarlos mediante
  *docker exec ...* al configurar los contenedores.

### Pasos necesarios para adaptar una ExApp

1. Copiar el script [start.sh](https://github.com/nextcloud/HaRP/blob/main/exapps_dev/start.sh)
   de la carpeta exapps_dev del repositorio de HaRP en la imagen Docker
   (p. ej., con una instrucción *COPY*).

2. En el Dockerfile de la ExApp, establecer el *ENTRYPOINT* para que ejecute *start.sh* seguido del
   **comando y los argumentos necesarios para lanzar** la aplicación propiamente dicha. El script *start.sh*
   lanzará el cliente FRP si es necesario y luego usará *exec* para
   ejecutar el comando que se le pase como argumentos.

3. Asegurarse de que la utilidad de línea de comandos *curl* esté instalada en la imagen Docker de la ExApp,
   ya que el siguiente script la necesita para descargar el cliente FRP.

4. Añadir las siguientes líneas al Dockerfile para incluir automáticamente los binarios del cliente FRP
   en la imagen Docker:

   ```dockerfile
   # Download and install FRP client
   RUN set -ex; \
       ARCH=$(uname -m); \
       if [ "$ARCH" = "aarch64" ]; then \
         FRP_URL="https://raw.githubusercontent.com/nextcloud/HaRP/main/exapps_dev/frp_0.61.1_linux_arm64.tar.gz"; \
       else \
         FRP_URL="https://raw.githubusercontent.com/nextcloud/HaRP/main/exapps_dev/frp_0.61.1_linux_amd64.tar.gz"; \
       fi; \
       echo "Downloading FRP client from $FRP_URL"; \
       curl -L "$FRP_URL" -o /tmp/frp.tar.gz; \
       tar -C /tmp -xzf /tmp/frp.tar.gz; \
       mv /tmp/frp_0.61.1_linux_* /tmp/frp; \
       cp /tmp/frp/frpc /usr/local/bin/frpc; \
       chmod +x /usr/local/bin/frpc; \
       rm -rf /tmp/frp /tmp/frp.tar.gz
   ```

   :::{note}
   En Alpine 3.21 Linux se puede simplemente instalar FRP desde el repositorio con el comando apk add frp.
   :::

### Ejecutar la ExApp con un usuario que no es root

:::{note}
En las [buenas prácticas de compilación de Docker](https://docs.docker.com/build/building/best-practices/#user)
se recomienda ejecutar los contenedores de aplicaciones como usuarios que no sean root por motivos de seguridad,
siempre que sea posible.
:::

Para ejecutar el proceso principal como un usuario que no sea root sin perder la compatibilidad con HaRP y AppAPI,
asegurarse de lo siguiente:

1. Mantener *root* como usuario predeterminado de la imagen y pasar en tiempo de ejecución a un usuario de servicio con menos privilegios.

   - Facilitar que AppAPI realice operaciones privilegiadas (copiar archivos,
     establecer permisos, ejecutar *update-ca-certificates*) dejando *root* como
     usuario predeterminado del contenedor en la imagen.
   - Reducir los privilegios del proceso principal en el *ENTRYPOINT* mediante *gosu*
     o *su-exec*, de modo que el proceso en tiempo de ejecución se ejecute como un usuario de servicio que no sea root.

   Fragmento de ejemplo (Dockerfile):

   ```dockerfile
   FROM python:3.12-alpine AS app

   ARG USER=serviceuser

   ENV USER=$USER
   ENV HOME=/home/$USER
   ENV GOSU_VERSION=1.19

   # ... other Dockerfile instructions ..

   # Install GOSU
   RUN set -eux; \
     \
     apk add --no-cache --virtual .gosu-deps \
       ca-certificates \
       dpkg \
       gnupg \
     ; \
     \
     dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
     wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
     wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
     \
     export GNUPGHOME="$(mktemp -d)"; \
     gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
     gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
     gpgconf --kill all; \
     rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc; \
     \
     apk del --no-network .gosu-deps; \
     \
     chmod +x /usr/local/bin/gosu

   # Use gosu in combination with start.sh
   ENTRYPOINT ["/bin/sh", "-c", "exec gosu \"$USER\" /start.sh python3 -u main.py"]
   ```

:::{note}
Ver la [documentación de gosu](https://github.com/tianon/gosu/blob/master/INSTALL.md)
para más detalles.
:::

2. Asegurarse de que las rutas de configuración y de certificados de FRP estén preparadas para el usuario de servicio

   - **Crear */frpc.toml*** o el directorio que lo contendrá en tiempo de compilación
     de la imagen, y asignar su propiedad al usuario de servicio, para que en tiempo de ejecución *start.sh* pueda
     escribir en él sin necesitar root.
   - **Crear el directorio */certs/frp*** y hacerlo legible por el usuario de servicio.
     AppAPI copiará los archivos de certificados en esa carpeta mediante un comando *docker cp ...*
     con el usuario predeterminado del contenedor (que sigue siendo *root*). Al asignar la propiedad
     del directorio al usuario de servicio, se garantiza que este pueda leer los certificados en tiempo de ejecución.

   Usar comandos similares a estos en el Dockerfile:

   ```dockerfile
   RUN touch /frpc.toml && \
     mkdir -p /certs/frp && \
     chown $USER:$USER /frpc.toml && \
     chown -R $USER:$USER /certs/frp && \
     chmod 600 /frpc.toml
   ```

**Todo junto:**

```dockerfile
FROM python:3.12-alpine AS app

ARG USER=serviceuser

ENV USER=$USER
ENV HOME=/home/$USER
ENV GOSU_VERSION=1.19

# Install dependencies and create service user. You might want to
# add additional packages depending on your app requirements.
# Make sure curl and FRP are installed.
RUN apk update && \
    apk add --no-cache curl frp ca-certificates && \
    adduser -D $USER && \
    touch /frpc.toml && \
    mkdir -p /certs/frp && \
    chown $USER:$USER /frpc.toml && \
    chown -R $USER:$USER /certs/frp && \
    chmod 600 /frpc.toml

# Install GOSU
RUN set -eux; \
  \
  apk add --no-cache --virtual .gosu-deps \
    ca-certificates \
    dpkg \
    gnupg \
  ; \
  \
  dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
  wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
  wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
  \
  export GNUPGHOME="$(mktemp -d)"; \
  gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
  gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
  gpgconf --kill all; \
  rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc; \
  \
  apk del --no-network .gosu-deps; \
  \
  chmod +x /usr/local/bin/gosu

WORKDIR /app

# Copy your app code
COPY --chown=$USER:$USER <files> .

# Copy the start.sh script and make it executable
COPY --chown=$USER:$USER start.sh /start.sh
RUN chmod +x /start.sh && \
  chown -R $USER:$USER /app && \
  pip install -r requirements.txt

# Run the start.sh as entrypoint with non-root user and point it to your app
ENTRYPOINT ["/bin/sh", "-c", "exec gosu \"$USER\" /start.sh python3 -u main.py"]
```

### Ejemplo de prueba de integración

Hay un conjunto de pruebas de ejemplo para validar el soporte de HaRP en una ExApp
en el repositorio *workflow_ocr_backend* (un commit de ejemplo que añadió el soporte de HaRP
y las pruebas):

- <https://github.com/R0Wi-DEV/workflow_ocr_backend/blob/f5ae6efb6e4a3307328a188898968abf000511ab/test/test_harp_integration.py>

Esta prueba demuestra la verificación automatizada de la conexión FRP y del comportamiento
en tiempo de ejecución; puede usarse como referencia al añadir comprobaciones de CI para la
compatibilidad con HaRP.
````
