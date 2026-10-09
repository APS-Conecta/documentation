---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo preparar el entorno de desarrollo de ExApps: instalar AppAPI desde el código fuente, tipos de daemon de despliegue y comandos make para Docker."
---
# Configuración del entorno de desarrollo

## Resumen

Esta página explica cómo preparar un entorno para desarrollar ExApps: el entorno de desarrollo recomendado, la instalación de AppAPI desde el código fuente, los dos tipos de daemon de despliegue y los comandos make que registran sus configuraciones para Docker. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/DevSetup.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
(nc-dev-dev-setup)=
El desarrollo con AppAPI requiere configurar un entorno de desarrollo de Nextcloud.
Para ello se recomienda encarecidamente usar la configuración [nextcloud-docker-dev](https://github.com/nextcloud/nextcloud-docker-dev) (desarrollada originalmente por Julius Knorr).
Para un entorno alternativo que no use Docker, consultar las instrucciones de configuración en {nc-doc}`Primeros pasos <developer_manual/getting_started/devenv>`.

IDE sugerido: **PhpStorm**, aunque, por supuesto, se puede usar cualquier IDE que se prefiera, como **VS Code** o **Vim**.

### Instalar AppAPI

Todas las ExApps requieren como dependencia la app [AppAPI](https://apps.nextcloud.com/apps/app_api) de Nextcloud.
Desde la versión 30.0.1 de Nextcloud, AppAPI se instala automáticamente de forma predeterminada.
Si se prefiere,
también se puede compilar la última versión de desarrollo de AppAPI desde el código fuente;
en ese caso, desinstalar la versión publicada de AppAPI y seguir los pasos siguientes.

Clonar la rama main más reciente:

```bash
git clone https://github.com/nextcloud/app_api.git && cd app_api
```

o clonar una versión específica indicando su etiqueta de versión:

```bash
git clone https://github.com/nextcloud/app_api.git --branch <version-tag> && cd app_api
```

donde `<version-tag>` es la versión que se desea instalar.

Luego, compilar los recursos del frontend en modo de desarrollo:

```bash
npm ci && npm run dev
```

Habilitar AppAPI desde el directorio donde se encuentra el comando `occ`:

```bash
./occ app:enable --force app_api
```

#### Tipos de daemons de despliegue

Hay dos tipos de daemons de despliegue que pueden usarse para desarrollar y probar ExApps:

1. `manual_install`: este tipo de daemon de despliegue se ejecuta manualmente en la máquina host.
   Es útil para el desarrollo de ExApps, ya que la ExApp puede ejecutarse directamente en el host.
2. `docker_install`: este tipo de daemon de despliegue se ejecuta en un contenedor Docker.

Estos daemons pueden registrarse (crearse) en las configuraciones de administración de AppAPI.
Para el comando `occ` equivalente o una explicación de los parámetros del daemon de despliegue,
consultar {nc-ref}`occ_daemon_config_registration`.

#### Docker Socket Proxy

Para el desarrollo y las pruebas en local,
la forma más sencilla es usar [Nextcloud AppAPI DSP HTTP](https://github.com/nextcloud/docker-socket-proxy?tab=readme-ov-file#httplocal).

### En lugar de una conclusión

Hay varios comandos make disponibles para facilitar las acciones de desarrollo frecuentes.

Para ver la lista completa, ejecutar `make help`.

#### API remota de Docker

La API remota de Docker Engine puede configurarse fácilmente con el comando `make dock2port`.
El comando creará un contenedor de Docker para proporcionar la API remota de Docker Engine.

Después, registrar las DaemonConfigs en Nextcloud con el comando `make dock-port`.

#### Docker mediante socket

Para Docker mediante socket, usar el comando `make dock-sock`.
Este registra las DaemonConfigs en Nextcloud para la conexión de socket predeterminada (`/var/run/docker.sock`).

Asegurarse de que el socket tenga permisos suficientes para que Nextcloud y el usuario del servidor web puedan acceder a él,
y de que realmente se reenvíe al contenedor:

```
...
volumes:
    ...
    - /var/run/docker.sock:/var/run/docker.sock
    ...
```
````
