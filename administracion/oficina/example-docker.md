---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Instalar Collabora Online con Docker tras un proxy inverso Apache, configurar la app Nextcloud Office y actualizar el contenedor."
---
# Ejemplo de instalación con Docker

## Resumen

Esta página explica cómo poner en marcha Nextcloud Office con la imagen de Docker de Collabora Online: requisitos, instalación del contenedor, proxy inverso Apache, configuración de la app y actualización a una versión nueva. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/office/example-docker.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/oficina/index

A continuación se describe cómo poner en marcha Nextcloud Office en el servidor y cómo integrarlo en Nextcloud mediante la imagen de docker que han creado {vendor}`Nextcloud` y Collabora.

Para instalarlo se requieren las siguientes dependencias:

- Un host que pueda ejecutar un contenedor Docker
- Un subdominio o un segundo dominio en el que pueda ejecutarse el servidor de Collabora Online
- Un servidor Apache con algunos módulos activados
- Un certificado SSL válido para el dominio en el que deba ejecutarse Collabora Online
- Un certificado SSL válido para Nextcloud

### Instalar el servidor de Collabora Online

Los siguientes pasos descargan el docker de Collabora Online. Asegurarse de sustituir «cloud.example.com» por el host en el que se ejecuta el propio Nextcloud. Para usar el contenedor docker con más de un Nextcloud, puede añadirse otro *-e aliasgroup2=<https://cloud2.example.com:443>*.

```bash
docker pull collabora/code
docker run -t -d -p 127.0.0.1:9980:9980 \
    -e 'aliasgroup1=https://cloud.example.com:443' \
    --restart always \
    --cap-add MKNOD \
    collabora/code
```

Con eso basta. Una vez hecho, el servidor escuchará en «localhost:9980». Ahora solo falta configurar el proxy inverso Apache instalado localmente.

### Instalar el proxy inverso Apache

En una versión reciente de Ubuntu o Debian, debería poder hacerse con:

```bash
apt-get install apache2
a2enmod proxy proxy_wstunnel proxy_http ssl
```

Después, configurar correctamente un VirtualHost para que haga de proxy del tráfico. Por motivos de seguridad, se recomienda usar un subdominio como office.example.com en lugar de ejecutarlo en el mismo dominio. Más abajo se encuentra un ejemplo de configuración:

```
########################################
# Reverse proxy for Collabora Online
########################################

AllowEncodedSlashes NoDecode
SSLProxyEngine On
ProxyPreserveHost On

# cert is issued for collaboraonline.example.com and we proxy to localhost
SSLProxyVerify None
SSLProxyCheckPeerCN Off
SSLProxyCheckPeerName Off

# static html, js, images, etc. served from coolwsd
# browser is the client part of Collabora Online
ProxyPass           /browser https://127.0.0.1:9980/browser retry=0
ProxyPassReverse    /browser https://127.0.0.1:9980/browser

# WOPI discovery URL
ProxyPass           /hosting/discovery https://127.0.0.1:9980/hosting/discovery retry=0
ProxyPassReverse    /hosting/discovery https://127.0.0.1:9980/hosting/discovery

# Capabilities
ProxyPass           /hosting/capabilities https://127.0.0.1:9980/hosting/capabilities retry=0
ProxyPassReverse    /hosting/capabilities https://127.0.0.1:9980/hosting/capabilities

# Main websocket
ProxyPassMatch      "/cool/(.*)/ws$"      wss://127.0.0.1:9980/cool/$1/ws nocanon

# Admin Console websocket
ProxyPass           /cool/adminws wss://127.0.0.1:9980/cool/adminws

# Download as, Fullscreen presentation and Image upload operations
ProxyPass           /cool https://127.0.0.1:9980/cool
ProxyPassReverse    /cool https://127.0.0.1:9980/cool
# Compatibility with integrations that use the /lool/convert-to endpoint
ProxyPass           /lool https://127.0.0.1:9980/cool
ProxyPassReverse    /lool https://127.0.0.1:9980/cool
```

Después de configurar esto, reiniciar apache con `systemctl restart apache2`.

:::{seealso}
Los ejemplos de configuración completos para el proxy inverso se encuentran en la documentación de Collabora Online:
<https://sdk.collaboraonline.com/docs/installation/Proxy_settings.html>
:::

### Configurar la app en Nextcloud

- Ir a la sección Apps y elegir «Office & text»
- Instalar la app «Nextcloud Office»
- Ir a Administración -> Office -> indicar el servidor configurado antes (p. ej., «<https://office.example.com>»)

¡Enhorabuena, Nextcloud ya tiene Collabora Online Office integrado!

### Actualización

De vez en cuando se publican versiones nuevas de esta imagen de docker con actualizaciones de seguridad y de funciones. ¡Por supuesto, {vendor}`Nextcloud` avisará cuando eso ocurra! Así se actualiza a una versión nueva:

- Actualizar la imagen de docker:

  ```bash
  docker pull collabora/code
  ```

- Listar los contenedores docker en ejecución:

  ```bash
  docker ps
  ```

- Detener y eliminar el contenedor de Collabora Online con el id de contenedor del que está en ejecución:

  ```bash
  docker stop CONTAINER_ID
  docker rm CONTAINER_ID
  ```

- Iniciar el contenedor nuevo:

  ```bash
  docker run -t -d -p 127.0.0.1:9980:9980 -e 'domain=cloud\\.example\\.com' \
      --restart always --cap-add MKNOD collabora/code
  ```
````
