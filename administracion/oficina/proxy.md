---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Rutas que un proxy inverso debe reenviar al demonio coolwsd de Nextcloud Office en el puerto 9980."
---
# Proxy inverso

## Resumen

Esta página enumera las rutas y las conexiones de web socket que un proxy inverso debe reenviar al demonio coolwsd, que escucha en el puerto 9980. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/office/proxy.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/oficina/index

La parte de servidor de Nextcloud Office (el demonio coolwsd) escucha de forma predeterminada en el puerto 9980, y los clientes deben poder comunicarse con ella a través del puerto 9980. Sin embargo, en la mayoría de las instalaciones es habitual usar un proxy inverso para gestionar más fácilmente la terminación SSL y disponer de un punto de entrada unificado para las peticiones HTTP.

Deben existir las siguientes reglas para reenviar las peticiones al demonio coolwsd en el puerto 9980:

- /browser
- /hosting/discovery
- /hosting/capabilities
- /cool/adminws
- /cool
- Conexiones de web socket a través de /cool/(.*)/ws

:::{seealso}
Hay ejemplos de configuración completos en la documentación de Collabora Online:
<https://sdk.collaboraonline.com/docs/installation/Proxy_settings.html>
:::
````
