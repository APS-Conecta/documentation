---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Pasar de CODE 6.4 a CODE 21.11: rutas del proxy inverso renombradas, paquetes loolwsd → coolwsd y actualización de la imagen de docker."
---
# Migración desde Collabora Online

## Resumen

Esta página explica cómo actualizar una instalación de Collabora Online de CODE 6.4 a CODE 21.11 para usar Nextcloud Office: los cambios de nombre en las rutas del proxy inverso, el paso de los paquetes loolwsd a coolwsd y la actualización de la imagen de docker. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/office/migration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/oficina/index

Nextcloud Office se basa en Collabora Online, así que para activar toda la funcionalidad de Nextcloud Office bastaría con actualizar a la versión más reciente. Nextcloud Office está disponible desde CODE 21.11.

:::{note}
Esta guía de actualización está pensada para actualizar de CODE 6.4 a CODE 21.11.
:::

### Actualizar la configuración del proxy inverso

Debido a los cambios de nombre en las versiones de Collabora Online, puede ser necesario ajustar las configuraciones de proxy inverso que ya se usan en instalaciones existentes.

- Las rutas con `lool` se han renombrado a `cool`
- Las rutas con `loleaflet` se han renombrado a `browser`

Hay guías completas y detalladas de configuración del proxy inverso para distintas soluciones en <https://sdk.collaboraonline.com/docs/installation/Proxy_settings.html>

### Actualizar los paquetes de la distribución

- El servicio principal se ha renombrado de `loolwsd` a `coolwsd`
- El cambio de nombre del servicio también afecta a la ubicación del archivo de configuración `/etc/coolwsd/coolwsd.xml`

Pasos de actualización necesarios:

- Detener el servicio `loolwsd`
- Hacer una copia de seguridad del archivo de configuración `/etc/loolwsd/loolwsd.xml`.
- Eliminar los paquetes `loolwsd` y `collaboraoffice*`.
- Cambiar el número de versión en la URL del repositorio, p. ej., de 6.4 a 21.11
- Instalar el paquete `coolwsd`
- Adaptar el nuevo archivo de configuración en `/etc/coolwsd/coolwsd.xml` para que coincida con la configuración anterior
- Iniciar y activar el servicio `coolwsd`

### Actualizar la imagen de docker

Para actualizar las imágenes de docker basta con descargar la imagen de CODE más reciente de Docker Hub.
````
