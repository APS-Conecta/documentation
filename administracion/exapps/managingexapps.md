---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Comandos occ de AppAPI para registrar, anular el registro, actualizar, habilitar, deshabilitar y listar ExApps, con sus argumentos y opciones."
---
# Comandos occ de ExApps

## Resumen

Esta página describe, para quienes administran el servidor, los comandos `occ` de AppAPI que registran, anulan el registro, actualizan, habilitan, deshabilitan y listan ExApps, con sus argumentos y opciones.

````{upstream} admin_manual/exapps_management/ManagingExApps.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/exapps/index

Las ExApps pueden gestionarse desde la interfaz de gestión de apps, como las demás apps de Nextcloud, pero también pueden usarse los comandos de AppAPI de la herramienta CLI de OCC.

Hay varios comandos para trabajar con ExApps:

1. Registrar
2. Anular el registro
3. Actualizar
4. Habilitar
5. Deshabilitar
6. Listar las ExApps

### Registrar

Comando: `app_api:app:register [--force-scopes] [--info-xml INFO-XML] [--json-info JSON-INFO] [--wait-finish] [--silent] [--test-deploy-mode] [--env [ENV]] [--mount [MOUNT]] [--] <appid> [<daemon-config-name>]`

El comando de registro es el primer paso de la instalación de una ExApp.

#### Argumentos

- `appid` - nombre único de la ExApp (p. ej., `app_python_skeleton`; debe ser el mismo que en el contenedor desplegado)
- `daemon-config-name` - nombre único del daemon (p. ej., `docker_local_sock`)

#### Opciones

- `--json-info JSON-INFO` *[opcional]* - información de despliegue de la ExApp en JSON (cadena JSON)
- `--info-xml INFO-XML` *[opcional]* - ruta al archivo info.xml (URL o ruta absoluta local)
- `--wait-finish` *[opcional]* - esperar a que termine la inicialización
- `--silent` *[opcional]* - no imprimir en la consola
- `--test-deploy-mode` *[opcional]* - modo de prueba de despliegue, con comprobaciones de estado adicionales y una lógica ligeramente distinta

(nc-advanced_deploy_options_cli)=
#### Opciones de despliegue avanzadas

- `--env` *[opcional]* - entorno (ENV_NAME=ENV_VALUE), que se pasa al contenedor de la ExApp como variables de entorno (se admiten varios valores)
- `--mount` *[opcional]* - opciones de montaje (SRC_PATH=DST_PATH), que se pasan al contenedor de la ExApp como montajes de volúmenes (se admiten varios valores)

### Anular el registro

Comando: `app_api:app:unregister [--rm-data] [--force] [--silent] [--] <appid>`

Para eliminar una ExApp se puede usar el comando de anulación del registro. De forma predeterminada, este comando *no* elimina el almacenamiento persistente de la ExApp (volumen de datos), para evitar borrar por accidente datos de usuario.

#### Argumentos

- `appid` - nombre único de la ExApp (p. ej., `app_python_skeleton`; debe ser el mismo que en el contenedor desplegado)

#### Opciones

- `--rm-data` *[opcional]* - eliminar el almacenamiento persistente de la ExApp (volumen de datos)
- `--force` *[opcional]* - continuar con la eliminación aunque se produzca algún error
- `--silent` *[opcional]* - imprimir el mínimo de información y mostrar solo algunos errores, si los hay

### Actualizar

Comando: `app_api:app:update [--info-xml INFO-XML] [--force-update] [-e|--enabled] [--] <appid>`

La ExApp se actualiza si hay una versión nueva disponible.

#### Argumentos

- `appid` - nombre único de la ExApp (p. ej., `app_python_skeleton`; debe ser el mismo que en el contenedor desplegado)

#### Opciones

- `--info-xml INFO-XML` *[opcional]* - ruta al archivo info.xml (URL o ruta absoluta local)
- `-e|--enabled` *[opcional]* - habilitar la ExApp después de la actualización

### Habilitar

Comando: `app_api:app:enable <appid>`

### Deshabilitar

Comando: `app_api:app:disable <appid>`

### Listar las ExApps

Comando: `app_api:app:list`

El comando ListExApps muestra todas las ExApps:

```
ExApps:
appid (Display Name): version [enabled/disabled]
to_gif_example (To Gif Example): 1.0.0 [enabled]
upscaler_example (Upscaler Example): 1.0.0 [enabled]
```
````
