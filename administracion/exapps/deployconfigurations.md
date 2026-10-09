---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Configuraciones de ejemplo del daemon de despliegue Docker, con HaRP o con Docker Socket Proxy, y cómo se comunica Nextcloud con las ExApps."
---
(nc-deploy-configs)=
# Configuraciones de despliegue

## Resumen

Esta página reúne, para quienes administran el servidor, configuraciones de ejemplo del daemon de despliegue Docker, con HaRP y con Docker Socket Proxy, y explica cómo AppAPI determina adónde envía las solicitudes a las ExApps.

````{upstream} admin_manual/exapps_management/DeployConfigurations.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/exapps/index

Actualmente se admiten dos tipos de despliegue de aplicaciones:

- {nc-ref}`Daemon de despliegue Docker (Docker Socket Proxy) <ai-app_api_ddd-dsp>`
- {nc-ref}`Daemon de despliegue Docker (HaRP) <ai-app_api_ddd-harp>`

### Daemon de despliegue Docker

Orquesta el despliegue de aplicaciones como contenedores Docker.

:::{warning}
El administrador es responsable de las medidas de seguridad que se tomen al configurar el daemon de Docker conectado a la instancia de Nextcloud.

Estos esquemas son solo ejemplos de configuraciones posibles.

Para el daemon de despliegue Docker (HaRP) se requiere [AppAPI HaRP](https://github.com/nextcloud/harp).

Para el daemon de despliegue Docker (Docker Socket Proxy), se recomienda usar el contenedor [AppAPI Docker Socket Proxy](https://github.com/nextcloud/docker-socket-proxy) o, para Nextcloud AIO, el contenedor [AIO Docker Socket Proxy](#nc-nextcloud-in-docker-aio-all-in-one).
:::

Hay varias configuraciones del daemon de despliegue Docker (esquemas de ejemplo):

- Nextcloud y Docker en el **mismo host** (mediante socket, DockerSocketProxy o HaRP)
- Nextcloud en el host y Docker en un host **remoto** (mediante DockerSocketProxy con HTTPS, o HaRP)
- Nextcloud y las **ExApps** en la **misma red Docker** (mediante DockerSocketProxy o HaRP)
- Nextcloud en Docker AIO y las **ExApps** en la **misma red Docker** (mediante AIO DockerSocketProxy)

(nc-ai-app_api_ddd-harp)=
### Daemon de despliegue Docker (HaRP)

Con HaRP, son las ExApps las que inician la conexión del túnel hacia la instancia de Nextcloud y el contenedor HaRP, por lo que no hace falta exponer ningún puerto ni abrir reglas en el cortafuegos.

Los diagramas de las configuraciones respectivas están en la sección {nc-ref}`Daemon de despliegue Docker (Docker Socket Proxy) <ai-app_api_ddd-dsp>`, más abajo.

A continuación se presentan brevemente los puertos predeterminados del contenedor HaRP. Hay más información en el [readme de HaRP](https://github.com/nextcloud/harp?tab=readme-ov-file#environment-variables).

- El puerto `8780` es el puerto de comunicación HTTP por el que Nextcloud se conecta al contenedor HaRP.
- El puerto `8781` es el puerto de comunicación HTTPS, cuando se configura.
- El puerto `8782` es el puerto del túnel FRP que usan las ExApps para conectarse al contenedor HaRP.

En cualquiera de los casos, las siguientes conexiones deben funcionar:

- Nextcloud -> contenedor HaRP (en el puerto 8780/8781)
- Contenedor HaRP -> Nextcloud (a través del proxy o directamente, según indique la variable de entorno NC_INSTANCE_URL)
- ExApp -> contenedor HaRP (en el puerto 8782)
- ExApp -> Nextcloud (a través del proxy o directamente, según indique la {guilabel}`URL de Nextcloud` de la configuración del daemon)

(nc-ai-app_api_nc-harp-baremetal)=
#### Nextcloud y Docker en el mismo host, con Nextcloud en bare metal

La configuración más sencilla es aquella en la que Nextcloud está instalado en el host, Docker está en el mismo host y las aplicaciones se despliegan en él.

Crear un contenedor HaRP con la opción `--network host` o bien exponiendo al host los puertos `8780` y `8782`.

```bash
docker run \
  -e HP_SHARED_KEY="some_very_secure_password" \
  -e NC_INSTANCE_URL="https://127.0.0.1:8080" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v `pwd`/certs:/certs \
  --name appapi-harp -h appapi-harp \
  --restart unless-stopped \
  -p 8780:8780 \
  -p 8782:8782 \
  -d ghcr.io/nextcloud/nextcloud-appapi-harp:release
```

Ir a los ajustes de administración de AppAPI y registrar un daemon `HaRP Proxy (Host)`.

Por último, probar toda la configuración con «Probar despliegue» en el menú de tres puntos del daemon de despliegue.

#### Nextcloud y Docker en el mismo host, con Nextcloud en Docker

Cuando Nextcloud está instalado en Docker, el contenedor HaRP puede crearse en la misma red Docker que la instancia de Nextcloud.

Crear un contenedor HaRP con la opción `--network <nextcloud_docker_network_name>`, donde `<nextcloud_docker_network_name>` es el nombre de la red Docker en la que Nextcloud es accesible.

```bash
docker run \
  -e HP_SHARED_KEY="some_very_secure_password" \
  -e NC_INSTANCE_URL="https://nextcloud.tld" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v `pwd`/certs:/certs \
  --name appapi-harp -h appapi-harp \
  --restart unless-stopped \
  --net <nextcloud_docker_network_name> \
  -d ghcr.io/nextcloud/nextcloud-appapi-harp:release
```

Ir a los ajustes de administración de AppAPI y registrar un daemon `HaRP Proxy (Docker)`. Tomar nota del valor `<nextcloud_docker_network_name>` en el campo `Docker network`.

Por último, probar toda la configuración con «Probar despliegue» en el menú de tres puntos del daemon de despliegue.

#### Docker en un host remoto, con el contenedor HaRP en el host local

Esta configuración es adecuada para despliegues que quieren descargar en un host remoto el trabajo pesado de las ExApps, especialmente cuando se usan GPU como dispositivos de cómputo. Puede haber varios daemons de despliegue con los que desplegar ExApps en distintos hosts remotos, para distintas capacidades de cómputo. Aquí el contenedor HaRP se despliega en el host local, y el host remoto lleva su socket de Docker hasta el host local a través del túnel seguro de [FRP](https://github.com/fatedier/frp). Las ExApps se despliegan en el host remoto. No se admite una instalación con el propio contenedor HaRP en el host remoto.

1. Crear un contenedor HaRP en el host local siguiendo {nc-ref}`los ejemplos anteriores <ai-app_api_nc-harp-baremetal>`, pero sin montar el socket de Docker.

   ```bash
   docker run \
     -e HP_SHARED_KEY="some_very_secure_password" \
     -e NC_INSTANCE_URL="https://127.0.0.1:8080" \
     -v `pwd`/certs:/certs \
     --name appapi-harp -h appapi-harp \
     --restart unless-stopped \
     -p 8780:8780 \
     -p 8782:8782 \
     -d ghcr.io/nextcloud/nextcloud-appapi-harp:release
   ```

2. Crear un daemon de despliegue correspondiente con `Docker socket proxy port` establecido en `24001`.
3. Los certificados de cliente generados por FRP deberían estar en la carpeta local `certs`. Copiar al host remoto los archivos `client.crt`, `client.key` y `ca.crt` que hay dentro de la carpeta `certs`.
4. Crear una estructura de carpetas en el host remoto: `mkdir -p certs/frp`, y copiar los archivos `client.crt`, `client.key` y `ca.crt` en la carpeta `certs/frp`.
5. Crear un archivo nuevo `frpc.toml` con el siguiente contenido.

   ```toml
   # frpc.toml
   serverAddr = "your.harp.server.address"          # Replace with your HP_FRP_ADDRESS host
   serverPort = 8782                                # Default port for FRP or the port your reverse proxy listens on
   loginFailExit = false                            # If the FRP (HaRP) server is unavailable, continue trying to log in.

   transport.tls.certFile = "certs/frp/client.crt"
   transport.tls.keyFile = "certs/frp/client.key"
   transport.tls.trustedCaFile = "certs/frp/ca.crt"
   transport.tls.serverName = "harp.nc"             # DO NOT CHANGE THIS VALUE

   metadatas.token = "some_very_secure_password"    # HP_SHARED_KEY in quotes

   [[proxies]]
   remotePort = 24001                               # Unique remotePort for each Docker Engine (range: 24001-24099)
   name = "deploy-daemon-1"                         # Unique name for each Docker Engine
   type = "tcp"
   [proxies.plugin]
   type = "unix_domain_socket"
   unixPath = "/var/run/docker.sock"
   ```

   Asegurarse de sustituir `your.harp.server.address` por la dirección real del host local en el que se ejecuta el contenedor HaRP.

   Puede convenir abrir el puerto `8782` en el cortafuegos del host local para que el host remoto pueda conectarse a él, o usar un proxy inverso que reenvíe las solicitudes al contenedor HaRP. A continuación se da un ejemplo con nginx. El puerto de escucha puede ajustarse libremente. El cliente FRP se conectará a este puerto expuesto.

   Con la configuración de proxy inverso siguiente, toda la instalación solo necesitaría que el proxy principal de Nextcloud esté expuesto y sea accesible desde el exterior, lo que simplifica la configuración de red.

   ```nginx
   stream {
       server {
           listen 8782;  # Replace with the port you want to listen on
           proxy_pass 127.0.0.1:8782;
           proxy_protocol off;
           proxy_connect_timeout 10s;
           proxy_timeout 300s;
       }
   }
   ```

6. Descargar una versión del cliente FRP desde [las versiones oficiales](https://github.com/fatedier/frp/releases/latest) o [nuestra instantánea desde aquí](https://github.com/nextcloud/HaRP/tree/main/exapps_dev).
7. Extraer y copiar el binario `frpc` a una ubicación adecuada del host remoto, p. ej., `/usr/local/bin`.
8. Hacerlo ejecutable: `chmod +x /usr/local/bin/frpc`.
9. Iniciar el cliente FRP con el comando: `frpc -c /path/to/frpc.toml`.
10. Por último, probar toda la configuración con «Probar despliegue» en el menú de tres puntos del daemon de despliegue.

(nc-ai-app_api_ddd-dsp)=
#### Docker, proxy inverso y Nextcloud en 3 hosts independientes, con contenedor HaRP

Esta es la infraestructura correspondiente: Host1 aloja Nextcloud; Host2 aloja el daemon de Docker y sus contenedores, entre ellos HaRP, que accede a {file}`/var/run/docker.sock` y conecta con ExApp1, ExApp2 y ExApp3; Host3 aloja el proxy inverso Apache. Host1 se conecta por puerto con Host2, y Host3 se conecta por puerto con Host1 y con Host2.

A continuación se muestran los pasos que sigo. Todos los pasos siguientes se basan en una distribución Almalinux. Adaptarlos a la distribución que se use.

1. En el Docker de Host2

1.1. Creación de la carpeta de certificados (si es necesario)

```bash
mkdir -p /some/path/certs
```

1.2. Apertura de puertos

```bash
firewall-cmd --permanent --zone=public --add-port=8780/tcp
firewall-cmd --permanent --zone=public --add-port=8782/tcp
firewall-cmd --reload
```

1.3. Despliegue del contenedor HaRP

```bash
docker run \
  -e HP_SHARED_KEY="some_very_secure_password" \
  -e NC_INSTANCE_URL="https://cloud.acme.com" \
  -e HP_TRUSTED_PROXY_IPS="192.168.0.0/24" \  # Replace with your actual trusted proxy subnet (Host3's IP or subnet)
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /some/path/certs:/certs \
  -p 8780:8780 \
  -p 8782:8782 \
  --name appapi-harp -h appapi-harp \
  --restart unless-stopped \
  -d ghcr.io/nextcloud/nextcloud-appapi-harp:release
```

2. En el proxy inverso Apache de Host3: redirecciones del proxy inverso

En el host virtual «cloud.acme.com» del archivo de configuración de Apache, añadir las líneas siguientes (antes de la configuración existente)

```apache
#  AppAPI Configuration
ProxyPass /exapps/ http://<IP_host2_docker>:8780/exapps/
ProxyPassReverse /exapps/ http://<IP_host2_docker>:8780/exapps/
```

3. En la interfaz web de Nextcloud: registro del daemon

Añadir la configuración siguiente:

- Plantilla de configuración de daemon: `HaRP Proxy (HOST)`
- Apellido: `appapi-harp`
- Nombre para mostrar: `appapi-harp`
- Método de despliegue: `docker-install`
- Servidor HaRP: `<IP_host2_docker>:8780`
- Clave compartida HaRP: `some_very_secure_password`
- URL de Nextcloud: `https://cloud.acme.com`
- Dirección del servidor FRP: `<IP_host2_docker>:8782`
- Red de Docker: `bridge`

Por último, probar toda la configuración con «Probar despliegue» en el menú de tres puntos del daemon de despliegue.

4. Pruebas adicionales desde la red de los hosts

:::{note}
La cabecera `docker-engine-port` indica a HaRP a qué puerto virtual interno debe enrutar hacia el motor de Docker. Cuando HaRP tiene el socket de Docker montado directamente (como en esta instalación), usa `24000` como puerto virtual predeterminado para ese socket local. Este valor no requiere ninguna configuración adicional de cortafuegos ni de puertos.
:::

```bash
curl -fsS \
  -H "harp-shared-key: some_very_secure_password" \
  -H "docker-engine-port: 24000" \
  http://<IP_host2_docker>:8780/exapps/app_api/v1.41/_ping
```

```bash
curl -fsS \
  -H "harp-shared-key: some_very_secure_password" \
  -H "docker-engine-port: 24000" \
  https://cloud.acme.com/exapps/app_api/v1.41/_ping
```

### Daemon de despliegue Docker (Docker Socket Proxy)

#### NC y Docker en el mismo host

La configuración más sencilla es aquella en la que Nextcloud está instalado en el host, Docker está en el mismo host y las aplicaciones se despliegan en él.

En el host, Nextcloud se comunica con el daemon de Docker a través de {file}`/var/run/docker.sock`, y el daemon ejecuta los contenedores ExApp1, ExApp2 y ExApp3.

Valores de configuración sugeridos (plantilla *Custom default*):

1. Servidor del Daemon: `/var/run/docker.sock`
2. Casilla HTTPS: *no se admite con el socket de Docker*
3. Red: `host`
4. Contraseña de HaProxy: **no se admite con el socket de Docker directo; debe quedar vacía**

---

Forma sugerida de comunicarse con Docker: mediante el [contenedor Docker Socket Proxy](https://github.com/nextcloud/docker-socket-proxy).

En el host, Nextcloud se conecta por puerto al contenedor Docker Socket Proxy, que accede a Docker a través de {file}`/var/run/docker.sock` y conecta con ExApp1, ExApp2 y ExApp3.

Valores de configuración sugeridos (plantilla *Docker Socket Proxy*):

1. Servidor del Daemon: `localhost:2375`

   Elegir la opción **A** o **B**:

   - A. Docker Socket Proxy debe desplegarse con `network=host` y `BIND_ADDRESS=127.0.0.1`
   - B. Docker Socket Proxy debe desplegarse con `network=bridge`, y su puerto debe publicarse en la 127.0.0.1 del host (p. ej., **-p 127.0.0.1:2375:2375**)
2. Casilla HTTPS: **desactivada**
3. Red: `host`
4. Contraseña de HaProxy: **no debe estar vacía**

:::{warning}
Tener cuidado con la opción `A`: de forma predeterminada, **Docker Socket Proxy** se vincula a `*` si no se especifica `BIND_ADDRESS` al crear el contenedor. Comprobar los puertos abiertos después de terminar la configuración.
:::

#### Docker en un host remoto

La configuración distribuida se da cuando Nextcloud está instalado en un host y Docker se encuentra en un host remoto, de modo que las aplicaciones se despliegan en el host remoto.

Ventaja: ningún impacto en el rendimiento del host de Nextcloud.

En este caso, AppAPI usa un Docker Socket Proxy desplegado en el host remoto para acceder al socket de Docker y a las ExApps.

Host1 (Nextcloud) se conecta por puerto con Host2, donde Docker Socket Proxy accede a {file}`/var/run/docker.sock` y conecta con ExApp1, ExApp2 y ExApp3.

Valores de configuración sugeridos (plantilla *Docker Socket Proxy*):

1. Servidor del Daemon: ADDRESS_OF_REMOTE_MACHINE (p. ej., **server_name.com:2375**)
2. Casilla HTTPS: `enabled`
3. Red: `host`
4. Contraseña de HaProxy: **no debe estar vacía**

#### NC y ExApps en el mismo Docker

Las aplicaciones se despliegan en el mismo Docker en el que reside Nextcloud.

Forma sugerida de comunicarse con Docker: mediante `docker-socket-proxy`.

En el mismo host, Nextcloud y Docker Socket Proxy son contenedores del mismo Docker: Nextcloud se conecta por puerto a Docker Socket Proxy, que accede a {file}`/var/run/docker.sock` y conecta con ExApp1 y ExApp2.

Valores de configuración sugeridos (plantilla *Docker Socket Proxy*):

1. Servidor del Daemon: nextcloud-appapi-dsp:2375
2. Casilla HTTPS: `disabled`
3. Red: [red definida por el usuario](https://docs.docker.com/network/#user-defined-networks)
4. Contraseña de HaProxy: **no debe estar vacía**

:::{note}
La red **no debe ser la bridge predeterminada de Docker**, ya que esta no admite la resolución DNS por nombre de contenedor.

Esto significa que los contenedores de **Docker Socket Proxy**, **Nextcloud** y las **ExApps** deben estar todos en la misma red Docker, distinta de la **bridge** predeterminada.
:::

(nc-nextcloud-in-docker-aio-all-in-one)=
#### Nextcloud en Docker AIO (todo en uno)

En el caso de AppAPI en una instalación de Docker AIO (instalada en el contenedor de Nextcloud).

:::{note}
El contenedor AIO Docker Socket Proxy debe estar activado.
:::

En el host, el contenedor maestro de Nextcloud AIO y Docker Socket Proxy acceden a {file}`/var/run/docker.sock`; el contenedor maestro gestiona el contenedor de Nextcloud, donde está instalada AppAPI, y Nextcloud se conecta a Docker Socket Proxy, que conecta con ExApp1, ExApp2 y ExApp3.

AppAPI crea automáticamente el DaemonConfig predeterminado para AIO Docker Socket Proxy, para usarlo como orquestador al crear los contenedores de las ExApps.

:::{note}
El DaemonConfig predeterminado solo se crea si no hay ya un DaemonConfig predeterminado registrado.
:::

##### Daemon de despliegue AIO predeterminado (Docker Socket Proxy)

Nextcloud AIO tiene un contenedor Docker Socket Proxy creado específicamente para usarse como daemon de despliegue en AppAPI. Tiene [parámetros fijos][AIODockerActions]:

- Nombre: `docker_aio`
- Nombre para mostrar: `AIO Docker Socket Proxy`
- Acepta el ID de despliegue: `docker-install`
- Protocolo: `http`
- Servidor: `nextcloud-aio-docker-socket-proxy:2375`
- Dispositivo de cómputo: `CPU`
- Red: `nextcloud-aio`
- URL de Nextcloud (que se pasa a las ExApps): `https://$NC_DOMAIN`

##### Seguridad de Docker Socket Proxy

AIO Docker Socket Proxy tiene un acceso estrictamente limitado a las API de Docker, descrito en la [configuración de HAProxy](https://github.com/nextcloud/all-in-one/blob/main/Containers/docker-socket-proxy/haproxy.cfg).

### Comunicación de NC con las ExApps

La comunicación entre Nextcloud y las ExApps se realiza a través de AppAPI. Con Docker Socket Proxy, las solicitudes se envían directamente al contenedor de la ExApp. Con HaRP, la comunicación pasa por el proxy principal de Nextcloud y por el contenedor HaRP.

Cada tipo de DeployDaemon implementa necesariamente la función `resolveExAppUrl`.

Su prototipo es:

```php
public function resolveExAppUrl(
    string $appId, string $protocol, string $host, array $deployConfig, int $port, array &$auth
) {}
```

donde:

- **protocol** es el valor del protocolo del daemon
- **host** es el valor del host del daemon; *puede ser DNS:port, IP:PORT o incluso la ruta al socket de Docker*.
- **port** es un entero con el puerto de la ExApp
- **deployConfig** puede ser personalizada para cada tipo de daemon
- **auth** es un array opcional con los datos de *autenticación básica*, si se necesitan para acceder a la ExApp

:::{note}
Se aplica solo a Docker Socket Proxy.

El parámetro adicional opcional *OVERRIDE_APP_HOST* puede usarse para sustituir el host al que se vinculará la ExApp.

Puede ser `0.0.0.0` en algunas configuraciones específicas: cuando se usa una VPN, o cuando la instancia de Nextcloud y las ExApps están en la misma máquina física pero en entornos virtuales distintos.

También se puede especificar algo como `10.10.2.5`; en ese caso, `ExApp` intentará vincularse a esa dirección y AppAPI intentará enviar las solicitudes directamente a ella, dando por hecho que la propia ExApp está vinculada a ella.
:::

La implementación más sencilla es la del tipo de despliegue **Manual-Install**:

```php
public function resolveExAppUrl(
    string $appId, string $protocol, string $host, array $deployConfig, int $port, array &$auth
): string {
    if (boolval($deployConfig['harp'] ?? false)) {
        $url = rtrim($deployConfig['nextcloud_url'], '/');
        if (str_ends_with($url, '/index.php')) {
            $url = substr($url, 0, -10);
        }
        return sprintf('%s/exapps/%s', $url, $appId);
    }

    $auth = [];
    if (isset($deployConfig['additional_options']['OVERRIDE_APP_HOST']) &&
        $deployConfig['additional_options']['OVERRIDE_APP_HOST'] !== ''
    ) {
        $wideNetworkAddresses = ['0.0.0.0', '127.0.0.1', '::', '::1'];
        if (!in_array($deployConfig['additional_options']['OVERRIDE_APP_HOST'], $wideNetworkAddresses)) {
            $host = $deployConfig['additional_options']['OVERRIDE_APP_HOST'];
        }
    }
    return sprintf('%s://%s:%s', $protocol, $host, $port);
}
```

Aquí se ve que, para manual-install sin HaRP, AppAPI envía las solicitudes al **host**:**port** especificado al crear el daemon.

En cambio, para los despliegues manuales que usan el proxy HaRP, usa exclusivamente la ruta `http(s)://nextcloud.example.tld/exapps/`. `http(s)://nextcloud.example.tld` es la URL de Nextcloud especificada en la configuración del daemon. Si la instancia de Nextcloud está en una subruta, `https://nextcloud.example.tld/nextcloud`, hay que configurar la ruta `/exapps/` del proxy inverso en consecuencia. Hay ejemplos en [Configurar el proxy inverso](https://github.com/nextcloud/harp?tab=readme-ov-file#configuring-your-reverse-proxy), en el readme de HaRP.

Veamos ahora la implementación de `resolveExAppUrl` en el Docker Daemon:

```php
public function resolveExAppUrl(
    string $appId, string $protocol, string $host, array $deployConfig, int $port, array &$auth
): string {
    if (boolval($deployConfig['harp'] ?? false)) {
        $url = rtrim($deployConfig['nextcloud_url'], '/');
        if (str_ends_with($url, '/index.php')) {
            $url = substr($url, 0, -10);
        }
        return sprintf('%s/exapps/%s', $url, $appId);
    }

    $auth = [];
    if (isset($deployConfig['additional_options']['OVERRIDE_APP_HOST']) &&
        $deployConfig['additional_options']['OVERRIDE_APP_HOST'] !== ''
    ) {
        $wideNetworkAddresses = ['0.0.0.0', '127.0.0.1', '::', '::1'];
        if (!in_array($deployConfig['additional_options']['OVERRIDE_APP_HOST'], $wideNetworkAddresses)) {
            return sprintf(
                '%s://%s:%s', $protocol, $deployConfig['additional_options']['OVERRIDE_APP_HOST'], $port
            );
        }
    }
    $host = explode(':', $host)[0];
    if ($protocol == 'https') {
        $exAppHost = $host;
    } elseif (isset($deployConfig['net']) && $deployConfig['net'] === 'host') {
        $exAppHost = 'localhost';
    } else {
        $exAppHost = $appId;
    }
    if ($protocol == 'https' && isset($deployConfig['haproxy_password']) && $deployConfig['haproxy_password'] !== '') {
        // we only set haproxy auth for remote installations, when all requests come through HaProxy.
        $haproxyPass = $this->crypto->decrypt($deployConfig['haproxy_password']);
        $auth = [self::APP_API_HAPROXY_USER, $haproxyPass];
    }
    return sprintf('%s://%s:%s', $protocol, $exAppHost, $port);
}
```

Para las instalaciones con HaRP, la ruta es la misma que en el ejemplo anterior. Todas las solicitudes se envían a la URL de Nextcloud con la ruta `/exapps/`.

Para Docker Socket Proxy, en cambio, el algoritmo que determina adónde deben enviarse las solicitudes es mucho más complejo.

En primer lugar, si el protocolo es `https`, AppAPI siempre envía las solicitudes al host del daemon y, en ese caso, es un HaProxy el que reenvía las solicitudes a las ExApps, que escuchan en `localhost`.

En resumen, queda así (*haproxy_host==valor del host del daemon*):

NC --> *https* --> `haproxy_host:ex_app_port` --> *http* --> `localhost:ex_app_port`

Cuando el protocolo no es `https` sino `http`, el endpoint al que se envían las solicitudes lo determina el valor de `$deployConfig['net']`.

Si `net` está definido y es igual a `host`, AppAPI supone que la ExApp está instalada en algún lugar de la red del host actual y que estará disponible en el adaptador de loopback `localhost`.

NC --> *http* --> `localhost:ex_app_port`

En todos los demás casos, la ExApp debe estar disponible por su nombre: p. ej., al usar una red Docker **bridge personalizada**, todos los contenedores están disponibles por DNS.

NC --> *http* --> `app_container_name:ex_app_port`

Estos tres tipos distintos de comunicación cubren las configuraciones más habituales.

[AIODockerActions]: <https://github.com/nextcloud/app_api/blob/main/lib/DeployActions/AIODockerActions.php#L52-L74)>
````
