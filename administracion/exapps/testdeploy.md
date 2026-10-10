---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "La prueba de despliegue de AppAPI: qué verifica cada comprobación de estado, sus errores posibles y cómo descargar los registros del contenedor."
---
(nc-test_deploy)=
# Probar el daemon de despliegue

## Resumen

Esta página describe, para quienes administran el servidor, la prueba de despliegue de AppAPI: qué verifica cada comprobación de estado, qué errores puede mostrar cada una y cómo descargar los registros del contenedor de prueba.

````{upstream} admin_manual/exapps_management/TestDeploy.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/exapps/index

Cada configuración de despliegue del daemon puede probarse desde las configuraciones de administración de AppAPI.

### Comprobaciones de estado

La prueba de despliegue instala una ExApp [test-deploy](https://github.com/nextcloud/test-deploy) para verificar cada paso del proceso de despliegue, incluida una comprobación de compatibilidad del hardware: para cada dispositivo de cómputo hay una imagen Docker distinta.

:::{note}
El contenedor de la ExApp Test Deploy no se elimina después de la prueba, porque se necesita para los registros y las comprobaciones de estado. Puede eliminarse después de la prueba desde la página Apps. Las imágenes Docker tampoco se eliminan del daemon; las imágenes sin usar pueden limpiarse con el comando `docker image prune`.
:::

#### Registro

El paso de registro es el primero: comprueba si la ExApp está registrada en Nextcloud.

#### Descarga de la imagen

El paso de descarga de la imagen obtiene la imagen Docker de la ExApp.

Errores posibles:

- Imagen no encontrada (p. ej., no es pública, o no hay imagen para la arquitectura de hardware)
- Falló la descarga de la imagen (p. ej., por problemas de red)
- Se agotó el tiempo de espera de la descarga de la imagen
- El Docker Socket Proxy o HaRP no está configurado correctamente y bloquea el acceso a esta API de Docker Engine

En los sistemas basados en systemd, véase `journalctl -f -u docker.service` para más detalles.

#### Contenedor iniciado

El paso de contenedor iniciado verifica que el contenedor de la ExApp se haya creado e iniciado correctamente.

Errores posibles:

- El contenedor no pudo iniciarse con soporte de GPU (puede faltar o estar mal configurado)
  - Para NVIDIA, consultar la [documentación de configuración de Docker de NVIDIA](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).
  - Para AMD, consultar la [documentación de configuración de Docker de ROCm](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/docker.html).
- Un problema de la ExApp durante el arranque (p. ej., memoria insuficiente). La app mostraría intentos de arranque repetidos en los registros.

Véase `docker logs nc_app_<app_id>` para más detalles.

#### Heartbeat

El paso Heartbeat comprueba si la verificación de salud del contenedor ha terminado y si el contenedor está en buen estado. La ExApp puede tener lógica adicional de configuración previa durante este paso.

Errores posibles:

- La ExApp no pudo iniciar un servidor web, p. ej., si el puerto ya está en uso (debería verse en los registros del contenedor)
- El heartbeat_count de la ExApp no deja de aumentar; esto puede indicar que la ExApp no pudo iniciarse correctamente
- Nextcloud no puede alcanzar el contenedor de la ExApp, p. ej.:
  - por un problema de red o un cortafuegos (debería verse en los registros del servidor o del cortafuegos)
  - por un daemon de despliegue con protocolo «http». En ese caso, el contenedor de la ExApp escucha en localhost (127.0.0.1 o ::1), que puede no ser accesible desde el servidor Nextcloud, y puede convenir escuchar en otra dirección IP. Véase `OVERRIDE_APP_HOST` en {nc-ref}`Opciones adicionales <additional_options_list>` del formulario del daemon de despliegue. Este problema puede identificarse con este comando: `lsof -i -P -n | grep LISTEN`
- Con HaRP, puede que el proxy principal de Nextcloud no esté configurado para redirigir correctamente las solicitudes al contenedor HaRP. Véase el apartado [Configurar el proxy inverso](https://github.com/nextcloud/harp?tab=readme-ov-file#configuring-your-reverse-proxy) del readme de HaRP.

#### Inicialización

El paso de inicialización comprueba si la ExApp está inicializada y lista para usarse. Durante este paso, la ExApp puede descargar elementos adicionales que necesite.

Errores posibles:

- Falló la inicialización (p. ej., por problemas de red o por tiempo de espera agotado)
- La ExApp no puede alcanzar el servidor Nextcloud (p. ej., por un problema de red o un cortafuegos)

#### Habilitado

El paso Habilitado comprueba si la ExApp está habilitada y lista para usarse. Durante este paso, la ExApp registra todas las API necesarias y disponibles del AppFramework de Nextcloud.

Errores posibles:

- La ExApp no respondió a la solicitud de habilitación
- La ExApp no pudo habilitarse por un fallo al registrar las API de AppAPI del AppFramework de Nextcloud (debería verse tanto en los registros del contenedor como en los registros de Nextcloud, si hay errores)

### Descargar los registros

Es posible descargar los registros del contenedor del último intento de prueba de despliegue.

:::{note}
Solo es posible descargar los registros de contenedores Docker que usan los controladores de registro json-file o journald.
:::
````
