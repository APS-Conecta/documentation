---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Formas de ejecutar el servicio coolwsd de Nextcloud Office: All In One, paquetes de la distribución, Docker o el servidor CODE integrado."
---
# Instalación

## Resumen

Esta página presenta las formas de desplegar el servicio coolwsd en el que se basa Nextcloud Office: Nextcloud All In One, paquetes de la distribución, Docker y el servidor CODE integrado, y la necesidad de un proxy inverso. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/office/installation.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/oficina/index

Nextcloud Office se basa en Collabora Online, que requiere un servicio dedicado que se ejecute junto a la pila del servidor web de Nextcloud. Hay varias formas de ejecutar el servicio coolwsd.

- **Nextcloud All In One:** Nextcloud Office viene preinstalado de serie en la configuración [Nextcloud All In One](https://github.com/nextcloud/all-in-one), que ofrece un despliegue y un mantenimiento sencillos, con la mayoría de las funciones incluidas en esta única instancia de Nextcloud.

Para las instalaciones manuales hay varias opciones para desplegar Nextcloud Office:

- **Instalación mediante paquetes de la distribución**: Hay paquetes disponibles para todas las distribuciones Linux principales que permiten desplegar un servidor de Collabora Online instalándolo con la gestión de paquetes habitual. Para ver una guía de instalación de ejemplo en Ubuntu, consultar: {nc-doc}`admin_manual/office/example-ubuntu`

  :::{seealso}
  <https://www.collaboraoffice.com/code/linux-packages/>
  <https://sdk.collaboraonline.com/docs/installation/index.html>
  :::

- **Instalación mediante Docker**: Hay imágenes de Docker disponibles para desplegar el servidor de Collabora Online en entornos de contenedores. Para ver una guía detallada paso a paso, consultar: {nc-doc}`admin_manual/office/example-docker`

  :::{seealso}
  <https://sdk.collaboraonline.com/docs/installation/CODE_Docker_image.html>
  :::

- **Servidor CODE integrado**: Esta app proporciona un servidor integrado con todas las funciones de edición de documentos de Collabora Online. Fácil de instalar, para uso personal o para equipos pequeños. Algo más lento que un servidor independiente y sin las funciones avanzadas de escalabilidad. La instalación puede hacerse activando la app de Nextcloud correspondiente. Hay más detalles en la [documentación de la app](https://github.com/CollaboraOnline/richdocumentscode).

  :::{note}
  Esta es la opción predeterminada, que funciona de inmediato en la mayoría de los escenarios; sin embargo, para mejorar el rendimiento se recomienda encarecidamente pasar a una instalación dedicada de Collabora Online mediante una de las otras opciones.
  :::

:::{note}
En la mayoría de los escenarios, ejecutar un servidor dedicado de Collabora Online requiere configurar algún tipo de proxy inverso delante de él. Para más detalles, consultar {nc-doc}`admin_manual/office/proxy`.
:::
````
