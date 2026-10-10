---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "El Docker Socket Proxy para el daemon de despliegue de AppAPI: el DSP de AppAPI, el de Nextcloud AIO y otras implementaciones."
---
# Docker Socket Proxy

## Resumen

Esta página explica el Docker Socket Proxy recomendado para el daemon de despliegue de AppAPI: cómo se protege el DSP de AppAPI, cómo lo activa Nextcloud AIO y qué requieren otras implementaciones. Está dirigida a quienes desarrollan o despliegan ExApps.

````{upstream} developer_manual/exapp_development/faq/DockerSocketProxy.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

La forma recomendada de configurar el daemon de despliegue de AppAPI
es usar nuestra [implementación de Docker Socket Proxy](https://github.com/nextcloud/docker-socket-proxy).

### Nextcloud AppAPI DSP

Nextcloud AppAPI DSP (Docker Socket Proxy) es un contenedor Docker sencillo que proporciona una forma segura de acceder a la API de Docker Engine y a las ExApps.
Está protegido con la autenticación Basic de haproxy.
La configuración del proxy inverso tiene dos partes:

- Configuración de HaProxy para la [API de Docker Engine](https://github.com/nextcloud/docker-socket-proxy/blob/main/haproxy.cfg.template)
- Configuración de HaProxy para las [ExApps](https://github.com/nextcloud/docker-socket-proxy/blob/main/haproxy_ex_apps.cfg.template)

:::{note}
En una configuración remota de Docker Socket Proxy, este debe exponer los puertos en el host.
:::

(nc-dev-faq_nextcloud-aio-docker-socket-proxy)=
### Nextcloud AIO

Nextcloud AIO implementa su propio [contenedor Docker Socket Proxy](https://github.com/nextcloud/all-in-one/tree/main/Containers/docker-socket-proxy);
basta con marcar la casilla en la interfaz de configuración de AIO para habilitarlo.
AppAPI crea automáticamente la configuración predeterminada del daemon de despliegue para Nextcloud AIO.

Véase [Nextcloud en Docker AIO (todo en uno)](https://docs.nextcloud.com/server/latest/admin_manual/exapps_management/DeployConfigurations.html#nextcloud-in-docker-aio-all-in-one) para más detalles.

:::{note}
Nextcloud AIO no se limita a su daemon de despliegue predeterminado.
Se puede configurar cualquier otro daemon de despliegue (local o remoto) para usarlo en AppAPI.
:::

### Otras implementaciones

Nuestra implementación está inspirada en [Tecnativa Docker Socket Proxy](https://github.com/Tecnativa/docker-socket-proxy).
De forma predeterminada, esta restringe el acceso a las API de Docker Engine que AppAPI necesita.
En ese caso, habrá que habilitar estas API mediante las variables de entorno:

- `IMAGES=1`
- `CONTAINER=1`
- `POST=1`

:::{note}
Para una configuración local del daemon de despliegue, otras implementaciones de Docker Socket Proxy pueden ser suficientes.
Pero para una configuración remota del daemon de despliegue, se recomienda usar nuestro DSP,
ya que [permitimos](https://github.com/nextcloud/docker-socket-proxy/blob/main/haproxy.cfg.template) únicamente las API de Docker Engine que realmente usamos en AppAPI,
y además está protegido con la autenticación de haproxy.
:::
````
