---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo desplegar una ExApp: registrar el DaemonConfig y la ExApp con occ, instalación manual, variables de entorno y el esquema del info.xml."
---
(nc-dev-app_deployment)=
# Despliegue

## Resumen

Esta página explica los dos pasos del despliegue de una ExApp, el registro del DaemonConfig y el de la ExApp con sus comandos `occ`, además de la instalación manual para desarrollo, las variables de entorno de despliegue, el esquema de instalación y los campos adicionales del info.xml. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/Deployment.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Descripción general

El proceso de despliegue de una ExApp consta de 2 pasos:

1. [Registro de DaemonConfig](#nc-dev-occ_daemon_config_registration)
2. [Registro de la ExApp](#deployment-exapp-registration)

(nc-dev-occ_daemon_config_registration)=
### Registro de DaemonConfig

El primer paso es registrar el DaemonConfig donde se desplegarán las ExApps.
Antes, hay que configurar el socket de Docker para que la instancia de Nextcloud y el usuario del servidor web puedan acceder a él.
Si se usa la API remota de Docker Engine, hay que exponerla para que la instancia de Nextcloud pueda acceder a ella, e importar los certificados.

:::{note}
Por ahora, solo se admite el daemon de Docker `accepts-deploy-id: docker-install`.
Para el desarrollo y las apps desplegadas manualmente en Docker, existe `accepts-deploy-id: manual-install`.
:::

Esto se hace con el comando `occ` **app_api:daemon:register**:

```bash
app_api:daemon:register <name> <display-name> <accepts-deploy-id> <protocol> <host> <nextcloud_url> [--net NET] [--haproxy_password PASSWORD] [--compute_device DEVICE] [--set-default] [--]
```

#### Argumentos

- `name` - nombre único del daemon (p. ej., `docker_local_sock`)
- `display-name` - nombre del daemon (p. ej., `My Local Docker`; se mostrará en la interfaz)
- `accepts-deploy-id` - tipo de despliegue (`docker-install` o `manual-install`)
- `protocol` - protocolo usado para conectarse al daemon (`http` o `https`)
- `host` - host del daemon (p. ej., `/var/run/docker.sock` o `host:port`)
- `nextcloud_url` - URL de Nextcloud, opción obligatoria de la configuración del daemon (p. ej., `https://nextcloud.local`)

#### Opciones

- `--net [network-name]` - `[required]` nombre de la red a la que se vincula el contenedor Docker (predeterminado: `host`)
- `--haproxy_password PASSWORD` - `[optional]` contraseña de la autenticación Basic de HAProxy si se usa `AppAPI Docker Socket Proxy`
- `--compute_device DEVICE` - `[optional]` dispositivo GPU que se expone al daemon (el predeterminado es `cpu`, pero también se admiten `cuda` y `rocm`)
- `--set-default` - `[optional]` establece el daemon recién creado como predeterminado

:::{note}
La CI de nuestro repositorio prueba las configuraciones habituales; ver los [flujos de trabajo en GitHub](https://github.com/nextcloud/app_api/blob/main/.github/workflows/tests-deploy.yml).
:::

#### Ejemplo

Ejemplo del comando `occ` **app_api:daemon:register**:

```bash
sudo -E -u www-data php occ app_api:daemon:register docker_local_sock "My Local Docker" docker-install http /var/run/docker.sock "https://nextcloud.local" --net nextcloud
```

(deployment-exapp-registration)=
### Registro de la ExApp

El segundo y último paso es desplegar y registrar la ExApp en Nextcloud en un daemon registrado previamente.
Esto se hace con el comando `occ` **app_api:app:register**:

```bash
app_api:app:register [--info-xml INFO-XML] [--json-info JSON-INFO] [--] <appid> <daemon-config-name>
```

#### Argumentos

- `appid` - nombre único de la ExApp (p. ej., `app_python_skeleton`; debe ser el mismo que en el contenedor desplegado)
- `daemon-config-name` - nombre único del daemon (p. ej., `docker_local_sock`)

#### Opciones

- `--info-xml INFO-XML` *[opcional]* - ruta al archivo info.xml (URL o ruta absoluta local)
- `--json-info JSON-INFO` *[opcional]* - información de despliegue de la ExApp en JSON (cadena JSON)

:::{warning}
Tras un despliegue correcto (pull, creación e inicio del contenedor), se hace una comprobación de heartbeat con un tiempo de espera de 90 segundos (será configurable).
:::

#### Instalación manual para desarrollo

Con fines de desarrollo, la ExApp se puede instalar manualmente.
Existe un tipo de DeployConfig `manual-install`, que puede usarse durante el desarrollo.
Para registrar una ExApp con él, hay que proporcionar la información de la app como cadena JSON o como ruta al archivo info.xml de la app.

En todos los ejemplos y aplicaciones que publicamos, solemos añadir el comando `manual_install` en su Makefile para facilitar el desarrollo.

```
sudo -E -u www-data php occ app_api:app:register nc_py_api manual_install --json-info \
        "{\"id\":\"nc_py_api\",\"name\":\"nc_py_api\",\"daemon_config_name\":\"manual_install\",\"version\":\"1.0.0\",\"secret\":\"12345\",\"port\":$APP_PORT}" \
```

:::{note}
Cuando se usa el tipo de DeployConfig `manual-install`, el despliegue y el arranque de la app corren a cargo de quien desarrolla.
:::

(nc-dev-ex_app_env_vars)=
#### Variables de entorno de despliegue

Las variables de entorno de despliegue se usan para configurar el contenedor de la ExApp.
Las siguientes variables son obligatorias y se generan automáticamente:

- `AA_VERSION` - versión de AppAPI
- `APP_SECRET` - secreto compartido generado que se usa para la autenticación de AppAPI
- `APP_ID` - ID de app de la ExApp
- `APP_DISPLAY_NAME` - nombre visible de la ExApp
- `APP_VERSION` - versión de la ExApp
- `APP_HOST` - host en el que escucha la ExApp
- `APP_PORT` - puerto en el que escucha la ExApp (AppAPI lo selecciona al azar)
- `APP_PERSISTENT_STORAGE` - ruta al volumen montado para el almacenamiento persistente de datos entre actualizaciones de la ExApp
- `NEXTCLOUD_URL` - URL de Nextcloud a la que conectarse

### Esquema de instalación de la aplicación

1. AppAPI despliega la aplicación y la inicia.
2. Durante *N* segundos (`90` de forma predeterminada), AppAPI comprueba el endpoint `/heartbeat` con una solicitud `GET`.
3. AppAPI envía una solicitud `POST` al endpoint `/init`. Si la ExApp no implementa el endpoint `/init` y AppAPI recibe un código de estado 501 o 404, AppAPI habilita la aplicación y pasa directamente al paso 5.
4. La ExApp envía un entero de `0` a `100` al endpoint OCS `apps/app_api/apps/status` para indicar el progreso de la inicialización. Tras enviar `100`, la aplicación se considera inicializada.
5. AppAPI envía una solicitud `PUT` al endpoint `/enabled`.

### Esquema del info.xml de la ExApp

El archivo info.xml de la ExApp ([ejemplo](https://github.com/cloud-py-api/nc_py_api/blob/main/examples/as_app/talk_bot/appinfo/info.xml)) se usa para describir los parámetros de la ExApp.
Se usa para generar el contenedor Docker de la ExApp y para registrar la ExApp en Nextcloud.
Tiene la misma estructura que los demás archivos appinfo/info.xml de Nextcloud, pero con algunos campos adicionales:

```xml
...
<external-app>
    <docker-install>
        <registry>ghcr.io</registry>
        <image>nextcloud/talk_bot</image>
        <image-tag>latest</image-tag>
    </docker-install>
</external-app>
...
```
````
