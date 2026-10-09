---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Comandos occ de AppAPI para registrar, anular el registro y listar daemons de despliegue, sus opciones, DeployConfig y opciones adicionales."
---
(nc-managing-deploy-daemons)=
# Gestión de los daemons de despliegue

## Resumen

Esta página describe, para quienes administran el servidor, los comandos `occ` de AppAPI que registran, anulan el registro y listan los daemons de despliegue, con sus argumentos, opciones y ejemplos, el formato DeployConfig y las opciones adicionales.

````{upstream} admin_manual/exapps_management/ManagingDeployDaemons.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/exapps/index

### CLI de OCC

Hay algunos comandos de la CLI de OCC para gestionar los daemons de despliegue:

1. Registrar `occ app_api:daemon:register`
2. Anular el registro `occ app_api:daemon:unregister`
3. Listar los daemons registrados `occ app_api:daemon:list`

#### Registrar

Registra un daemon de despliegue (DaemonConfig).

Comando: `app_api:daemon:register [--net NET] [--haproxy_password HAPROXY_PASSWORD] [--compute_device COMPUTE_DEVICE] [--set-default] [--harp] [--harp_frp_address HARP_FRP_ADDRESS] [--harp_shared_key HARP_SHARED_KEY] [--harp_docker_socket_port HARP_DOCKER_SOCKET_PORT] [--harp_exapp_direct] [--] <name> <display-name> <accepts-deploy-id> <protocol> <host> <nextcloud_url>`

##### Argumentos

- `name` - nombre único del daemon (p. ej., `docker_local_sock`)
- `display-name` - nombre del daemon (p. ej., `My Local Docker`; se mostrará en la interfaz)
- `accepts-deploy-id` - tipo de despliegue (`docker-install` o `manual-install`)
- `host` - **ruta al docker-socket** o al Docker Socket Proxy: `address:port`
- `protocol` - protocolo usado para comunicarse con el daemon o las ExApps (`http` o `https`)
- `nextcloud_url` - URL de Nextcloud, opción obligatoria de la configuración del daemon (p. ej., `https://nextcloud.local`)

##### Opciones

- `--net [network-name]` - `[required]` nombre de la red a la que se vincula el contenedor Docker (predeterminado: `host`)
- `--haproxy_password HAPROXY_PASSWORD` - `[optional]` contraseña de AppAPI Docker Socket Proxy
- `--compute_device GPU` - `[optional]` dispositivo GPU que se expone al daemon (p. ej., `cpu|cuda|rocm`; predeterminado: `cpu`)
- `--set-default` - `[optional]` establece el daemon creado como predeterminado para la instalación de ExApps
- `--harp` - `[optional]` indicador para que el daemon use HaRP en toda la comunicación con Docker y con las ExApps
- `--harp_frp_address` - `[optional]` [host]:[port] del servidor FRP de HaRP; el host predeterminado es el mismo que el de HaRP, y el puerto, 8782
- `--harp_shared_key` - `[optional]` clave compartida de HaRP para la comunicación segura entre HaRP y AppAPI
- `--harp_docker_socket_port` - `[optional]` el 'remotePort' del cliente FRP del docker socket proxy remoto. El contenedor de HaRP incluye uno, así que puede omitirse en las instalaciones predeterminadas. (predeterminado: "24000")
- `--harp_exapp_direct` - `[optional]` indicador solo para instalaciones avanzadas. Desactiva el túnel FRP entre las ExApps y HaRP.

##### Ejemplos de uso

- Registrar un daemon de despliegue HaRP dentro de la red Docker `nextcloud`, con el contenedor `appapi-harp` como host y `appapi-harp:8782` como dirección del servidor FRP. Puede combinarse con un contenedor HaRP que se ejecute en la misma red.

  ```bash
  occ app_api:daemon:register harp_proxy_docker "Harp Proxy (Docker)" "docker-install" "http" "appapi-harp:8780" "http://nextcloud.local" --net nextcloud --harp --harp_frp_address "appapi-harp:8782" --harp_shared_key "some_very_secure_password" --set-default --compute_device=cuda
  ```

- Registrar un daemon de despliegue HaRP con `localhost` como host y `localhost:8782` como dirección del servidor FRP. Puede combinarse con un contenedor HaRP que se ejecute en el modo de red host o que haya expuesto al host los puertos `8780` y `8782`.

  ```bash
  app_api:daemon:register harp_proxy_host "Harp Proxy (Host)" "docker-install" "http" "localhost:8780" "http://nextcloud.local" --harp --harp_frp_address "localhost:8782" --harp_shared_key "some_very_secure_password" --set-default --compute_device=cuda
  ```

- Registrar un daemon de despliegue de instalación manual con soporte de HaRP. Puede combinarse con un contenedor HaRP que se ejecute en la misma red. El contenedor HaRP no necesita acceso a un socket de Docker ni ningún otro puerto expuesto al host. No creará contenedores Docker de las ExApps: solo hará de proxy de las solicitudes hacia el proceso de la ExApp que el usuario haya iniciado manualmente.

  :::{note}
  El proceso de la ExApp debe tener un cliente FRP (frpc) ejecutándose en la misma red que el contenedor HaRP, o debe poder conectarse a los puertos expuestos por el contenedor HaRP.

  Si la comunicación tiene que hacerse sin el cliente FRP, hay que pasar la opción `--harp_exapp_direct`. En ese caso, para los despliegues manuales siempre se usa como host la dirección IP de localhost, y para los despliegues de ExApps se usa `OVERRIDE_APP_HOST` o el `<app_id>`. Tener cuidado de no usar para esto el modo de red host ni la red bridge predeterminada.
  :::

  ```bash
  app_api:daemon:register manual_install_harp "Harp Manual Install" "manual-install" "http" "appapi-harp:8780" "http://nextcloud.local" --net nextcloud --harp --harp_frp_address "appapi-harp:8782" --harp_shared_key "some_very_secure_password"
  ```

- Registrar un daemon de despliegue Docker Socket Proxy con `nextcloud-appapi-dsp:2375` como host y la red Docker `nextcloud`. Puede combinarse con un contenedor Docker Socket Proxy que se ejecute en la misma red con el puerto predeterminado `2375`.

  ```bash
  app_api:daemon:register docker_install "Docker Socket Proxy" "docker-install" "http" "nextcloud-appapi-dsp:2375" "http://nextcloud.local" --net=nextcloud --set-default --compute_device=cuda
  ```

- Registrar un daemon de despliegue manual con `host.docker.internal` como host con el que conectarse a las ExApps.

  ```bash
  app_api:daemon:register manual_install "Manual Install" "manual-install" "http" null "http://nextcloud.local"
  ```

- Registrar un daemon de despliegue Docker local con `/var/run/docker.sock` como socket y como host, y la red Docker `nextcloud`. No necesita un contenedor Docker Socket Proxy. El dispositivo de cómputo que usa este daemon es `CPU`.

  ```bash
  app_api:daemon:register local_docker "Docker Local" "docker-install" "http" "/var/run/docker.sock" "http://nextcloud.local" --net=nextcloud
  ```

- Registrar un daemon de despliegue Docker local con `/var/run/docker.sock` como socket y como host, y la red Docker `nextcloud`. No necesita un contenedor Docker Socket Proxy. El dispositivo de cómputo que usa este daemon es `CUDA` (NVIDIA).

  ```bash
  app_api:daemon:register local_docker "Docker Local" "docker-install" "http" "/var/run/docker.sock" "http://nextcloud.local" --net=nextcloud --set-default --compute_device=cuda
  ```

##### DeployConfig

DeployConfig es un conjunto de opciones adicionales de la configuración del daemon que los algoritmos de despliegue usan para configurar el contenedor de la ExApp.

```json
{
    "net": "host",
    "nextcloud_url": "https://nextcloud.local",
    "haproxy_password": "some_secure_password",
    "computeDevice": {
        "id": "cuda",
        "name": "CUDA (NVIDIA)",
    },
    "harp": {
        "frp_address": "localhost:8782",
        "docker_socket_port": "24000",
        "exapp_direct": false
    }
}
```

##### Opciones de DeployConfig

- `net` **[obligatorio]** - nombre de la red a la que se vincula el contenedor Docker (predeterminado: `host`)
- `nextcloud_url` **[obligatorio]** - URL de Nextcloud (p. ej., `https://nextcloud.local`)
- `haproxy_password` *[opcional]* - contraseña de AppAPI Docker Socket Proxy
- `computeDevice` *[opcional]* - dispositivo de cómputo que se asocia al daemon (p. ej., `{ "id": "cuda", "label": "CUDA (NVIDIA)" }`)
- `harp` *[opcional]* - opciones de HaRP; puede ser `null` en las instalaciones sin HaRP
  - `frp_address` *[opcional]* - [host]:[port] del servidor FRP de HaRP; el host predeterminado es el mismo que el de HaRP, y el puerto, 8782
  - `docker_socket_port` *[opcional]* - el 'remotePort' del cliente FRP del docker socket proxy remoto. El contenedor de HaRP incluye uno, así que puede omitirse en las instalaciones predeterminadas. [predeterminado: "24000"]
  - `exapp_direct` *[opcional]* - indicador solo para instalaciones avanzadas. Desactiva el túnel FRP entre las ExApps y HaRP.

#### Anular el registro

Anula el registro de un daemon de despliegue (DaemonConfig).

Comando: `app_api:daemon:unregister <daemon-config-name>`

#### Listar los daemons registrados

Lista los daemons de despliegue registrados (DaemonConfigs).

Comando: `app_api:daemon:list`

### Nextcloud AIO

Cuando AppAPI está instalada en AIO, se registra automáticamente un daemon de despliegue predeterminado. Es posible registrar daemons de despliegue adicionales con los mismos métodos descritos más arriba.

(nc-additional_options_list)=
### Opciones adicionales

Es posible añadir a la configuración del daemon de despliegue opciones adicionales, que son pares clave-valor.

No debe usarse con HaRP.

Actualmente están disponibles las siguientes opciones:

- `OVERRIDE_APP_HOST` - puede usarse para sustituir el host al que se vinculará la ExApp (no se pasa a las variables de entorno del contenedor de la ExApp)
````
