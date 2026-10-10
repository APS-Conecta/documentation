---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Qué son AppAPI y las ExApps, cómo instalar AppAPI, registrar un daemon de despliegue con HaRP o Docker Socket Proxy e instalar ExApps."
---
# AppAPI y aplicaciones externas

## Resumen

Esta página explica, para quienes administran el servidor, qué son AppAPI y las ExApps, cómo instalar AppAPI y registrar un daemon de despliegue (con HaRP o con Docker Socket Proxy), cómo instalar ExApps y en qué se diferencian HaRP y Docker Socket Proxy.

````{upstream} admin_manual/exapps_management/AppAPIAndExternalApps.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/exapps/index

(nc-ai-app_api)=
Antes, Nextcloud solo admitía aplicaciones escritas en el lenguaje de programación PHP. Para dar soporte a una gama más amplia de casos de uso, se introdujo un ecosistema de **ExApps** (abreviatura de «External Apps») que permite instalar aplicaciones como contenedores Docker.

La mayoría de nuestras apps de {nc-doc}`inteligencia artificial <admin_manual/ai/index>` (IA) se desarrollan como ExApps, por lo que pueden requerir cierta preparación de la instancia de Nextcloud antes de poder instalarlas.

:::{tip}
AppAPI y las ExApps son funcionalidades opcionales. Si no se usa ninguna aplicación que no sea PHP, AppAPI puede desactivarse con seguridad: ir a la página de gestión de apps de la instancia de Nextcloud, entrar en «Tus apps» y hacer clic en el botón «Desactivar» junto a AppAPI.
:::

### Instalar AppAPI

Todas las ExApps requieren como dependencia la app de Nextcloud [AppAPI](https://apps.nextcloud.com/apps/app_api). Desde la versión 30.0.1 de Nextcloud, AppAPI se instala automáticamente de forma predeterminada. Si AppAPI no está instalada, aún puede instalarse: basta con ir a la página de gestión de apps de la instancia de Nextcloud y buscar AppAPI en la categoría Herramientas.

### Configurar el daemon de despliegue

Un daemon de despliegue es el medio por el que Nextcloud instala las ExApps, se comunica con ellas y las controla.

:::{note}
Si se usa Nextcloud AIO con el contenedor «HaRP» o «Docker Socket Proxy» activado, se crea automáticamente un daemon de despliegue configurado para funcionar desde el primer momento. En caso contrario, seguir los pasos siguientes para configurar un daemon de despliegue desde las configuraciones de administración de AppAPI.
:::

:::{tip}
Después de registrar un daemon de despliegue, usar la acción **Probar despliegue** para verificar que es accesible y que funciona. En la lista de daemons de despliegue, hacer clic en el menú *...* (tres puntos) junto al daemon que se quiere verificar y elegir Probar despliegue. Para saber qué hace esta comprobación y cómo interpretar sus resultados, véase {nc-ref}`Probar despliegue <test_deploy>`.
:::

(nc-ai-app_api_harp)=
#### HaRP

Esta es la forma más reciente y la **recomendada** de instalar ExApps.

Requiere cambios en el proxy de la instancia de Nextcloud. Si no se tiene acceso al proxy, puede usarse el método habitual {nc-ref}`descrito más abajo <ai-app_api_dsp>`.

1. Configurar un contenedor Docker llamado [HaRP](https://github.com/nextcloud/HaRP?tab=readme-ov-file#how-to-install-it) que hace de proxy del acceso a Docker y a las ExApps para la instancia de Nextcloud. Tener cuidado de cambiar los valores de `HP_SHARED_KEY` y `NC_INSTANCE_URL`.
2. Ir a las configuraciones de administración de AppAPI.
3. Hacer clic en el botón «Registrar Daemon».
4. Debería aparecer un formulario completado. Esta configuración predeterminada, `HaRP Proxy (Host)`, debería funcionar en la mayoría de las instalaciones. Para Nextcloud AIO, usar `HaRP All-in-One`.

   Si se usa Nextcloud en una red Docker personalizada y se quiere limitar el contenedor HaRP a ella, usar la opción `HaRP Proxy (Docker)` para que los campos se completen con las opciones habituales, o cambiarlos manualmente.

   En ese caso, asegurarse de que el propio contenedor HaRP se inicie en el paso 1 en la misma red que la instancia de Nextcloud, opcionalmente sin puertos expuestos al host, y de que esa misma red Docker figure en el campo `Network` de la configuración de despliegue.
5. Asegurarse de usar la misma clave compartida en el contenedor HaRP y en los ajustes de AppAPI.
6. Hacer clic en «Verificar conexión» para comprobar que la configuración es correcta.
7. Hacer clic en «Registrar» para guardar la configuración del daemon de despliegue.
8. Configurar en el proxy principal de Nextcloud una redirección de ubicación que redirija las solicitudes al contenedor HaRP. En el apartado [Configurar el proxy inverso](https://github.com/nextcloud/harp?tab=readme-ov-file#configuring-your-reverse-proxy) del readme de HaRP hay ejemplos para los proxies inversos más populares.
9. Probar toda la configuración con «Probar despliegue» en el menú de tres puntos del daemon de despliegue.

Esto es adecuado para instalaciones locales en las que el servidor Nextcloud y las ExApps están en la misma máquina o en la misma red Docker. En esta configuración, ni las ExApps ni el servidor de ExApps tienen por qué exponer al host ningún puerto relacionado con las ExApps (23000-23999), ni necesitan ser accesibles desde el host. Deben poder alcanzar el contenedor HaRP en el puerto FRP y la instancia de Nextcloud. Para instalaciones distintas o remotas, véanse los ejemplos de configuración de despliegue {nc-doc}`aquí <admin_manual/exapps_management/DeployConfigurations>`.

:::{note}
Las ExApps existentes pueden migrarse al nuevo proxy HaRP siguiendo [esta guía](https://github.com/nextcloud/harp?tab=readme-ov-file#nextcloud-32-migrating-existing-exapps-from-dsp-to-harp).
:::

(nc-ai-app_api_dsp)=
#### Docker Socket Proxy

1. Configurar un contenedor Docker llamado [docker-socket-proxy](https://github.com/nextcloud/docker-socket-proxy#readme) que hace de proxy del acceso a Docker para la instancia de Nextcloud.
2. Ir a las configuraciones de administración de AppAPI.
3. Hacer clic en el botón «Registrar Daemon».
4. Completar los campos obligatorios:
   - {guilabel}`Nombre`: nombre único del daemon de despliegue
   - `Display name`: el nombre que se mostrará en la interfaz
   - `Deployment method`: de forma predeterminada, hay que elegir `docker_install` (`manual_install` es para desarrollo o para un caso de uso personalizado de instalación manual de ExApps)
   - `Daemon Host`: nombre de host o dirección IP + puerto del daemon de despliegue
   - {guilabel}`URL de Nextcloud`: se completa automáticamente con el dominio actual; puede ser necesario cambiar el protocolo a http/https según la instalación
   - `Set as default daemon`: marcar si se quiere establecer el nuevo daemon de despliegue como predeterminado
   - `Enable https`: marcar si el daemon de despliegue (Docker Socket Proxy) está configurado con TLS
   - Configuración de despliegue:
     - `Network`: nombre de la red Docker; depende de la configuración de red; se fuerza a «host» si «Habilitar https» está marcado
     - `HaProxy password`: contraseña de Docker Socket Proxy, si está configurado con TLS
     - `Compute Device`: CPU, CUDA o ROCm, según la configuración de hardware de la máquina host del daemon de despliegue
     - `Add additional option` (véase {nc-ref}`additional_options_list`): configurar opciones adicionales de la configuración de despliegue como CLAVE + VALOR
5. Hacer clic en «Verificar conexión» para comprobar que la configuración es correcta.
6. Hacer clic en «Registrar» para guardar la configuración del daemon de despliegue.

:::{note}
En una instalación remota de DSP, este debe exponer los puertos en el host.
:::

Hay ejemplos de configuración de despliegue {nc-doc}`aquí <admin_manual/exapps_management/DeployConfigurations>`.

### Instalar ExApps

Ahora es posible instalar ExApps desde la tienda de apps de {vendor}`Nextcloud` haciendo clic en «Instalar» en la app correspondiente de la página Apps. Si la instalación tiene éxito, la ExApp se muestra en la lista «Tus apps».

### Preguntas frecuentes

- Tengo dos tarjetas gráficas (p. ej., NVIDIA RTX 3060) con 8 GB de VRAM cada una. ¿Cómo puedo ejecutar algo que no cabe en una sola tarjeta gráfica?
  - Actualmente no se admite distribuir modelos entre varias GPU. Hace falta una GPU en la que quepa todo el modelo que se intenta usar.
- Tengo una tarjeta gráfica que no admite CUDA: ¿puedo usarla, y cómo?
  - No; por ahora, nuestras apps de IA requieren GPU compatibles con CUDA para funcionar.
- ¿Cuál es el requisito mínimo de VRAM de la GPU si quiero instalar varias apps?
  - Cuando se ejecutan varias ExApps en la misma GPU, esta debe poder alojar el modelo más grande de entre las apps que se instalen.
- ¿Es posible añadir más tarjetas gráficas a mi instancia para permitir solicitudes en paralelo o para acelerar una solicitud?
  - Actualmente no se admite el procesamiento en paralelo de cargas de trabajo de IA de una misma app con varias GPU.
- ¿Puedo usar la CPU y la GPU en paralelo para el procesamiento de IA?
  - No; para una app, las cargas de trabajo de IA solo pueden procesarse en la CPU o en la GPU. Para apps distintas, se puede decidir si se ejecutan en la CPU o en la GPU.

### Docker Socket Proxy frente a HaRP

HaRP puede considerarse la versión 2.0 de Docker Socket Proxy. Hace todo lo que hace Docker Socket Proxy, pero además resuelve el principal problema: que el servidor Nextcloud (o AppAPI) no pueda alcanzar las ExApps.

Se usa [FRP](https://github.com/fatedier/frp) para crear un túnel entre la ExApp y el contenedor HaRP, de modo que los contenedores de las ExApps no necesitan exponer ningún puerto al host ni ser accesibles desde el servidor Nextcloud.

El servidor Nextcloud puede alcanzar los contenedores de las ExApps a través del contenedor HaRP.

HaRP tiene la ventaja adicional de poder hacer de proxy de las solicitudes que llegan desde la interfaz web o desde una API hacia el contenedor de la ExApp sin pasar por el servidor Nextcloud, lo que ahorra recursos, mejora el rendimiento y admite protocolos adicionales como WebSockets.

HaRP es la forma recomendada de ejecutar ExApps, pero si no es posible usarlo, Docker Socket Proxy sigue siendo compatible.

Solicitudes del frontend en el caso de Docker Socket Proxy: el frontend, en el navegador, envía todas las solicitudes al proxy; el proxy pasa al servidor Nextcloud / AppAPI tanto las solicitudes habituales como las dirigidas a una ExApp, y el servidor convierte estas últimas a la autenticación de ExApp y las reenvía a la ExApp.

Solicitudes del frontend en el caso de HaRP: el frontend, en el navegador, envía las solicitudes al proxy; el proxy pasa las solicitudes habituales al servidor Nextcloud / AppAPI y envía las dirigidas a una ExApp directamente al contenedor HaRP; HaRP valida la autenticación del usuario con el servidor Nextcloud / AppAPI, convierte la solicitud a la autenticación de ExApp y la reenvía a la ExApp.
````
