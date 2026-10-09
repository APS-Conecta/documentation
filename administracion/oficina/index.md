---
tipo: guia
esqueleto: borrador
audiencia: administracion
apps: [gestion]
resumen: "Operar el servidor de documentos Euro-Office de la pila: tokens, almacenamiento y salud."
---
# Oficina

## Resumen

El servidor de documentos Euro-Office es un contenedor dedicado de la pila: valida tokens JWT, responde al almacenamiento por ruta interna y se mantiene en espera bajo demanda para ahorrar recursos. La administración cubre el secreto compartido, el enrutamiento de retorno, la conversión ODF con pérdida y la verificación del backend de oficina.

### En APS Conecta Gestión

La suite de oficina de APS Conecta Gestión es Euro-Office, integrada con la aplicación `eurooffice`. El AIO deja Euro-Office como única opción de oficina y no ofrece Collabora ni OnlyOffice; la aplicación `office` de la plataforma (la vista general de oficina, que no edita documentos) queda desactivada por la política de aplicaciones.

## Secciones previstas

- Arquitectura del servidor de documentos
- Secreto JWT
- Enrutamiento interno
- Compatibilidad de formatos
- Espera bajo demanda
- Verificación del backend

````{upstream} admin_manual/office/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/oficina/index

Nextcloud Office permite editar los documentos en tiempo real junto con varios editores más, con una representación WYSIWYG de alta fidelidad que conserva el diseño y el formato de los documentos.

Los usuarios pueden insertar comentarios y responderlos, e invitar a otras personas sin cuenta de Nextcloud a editar archivos de forma anónima mediante una carpeta compartida con enlace público.

Nextcloud Office admite decenas de formatos de documento, entre ellos DOC, DOCX, PPT, PPTX, XLS, XLSX + ODF, importación/visualización de Visio, Publisher y muchos más...

Nextcloud Office se basa en Collabora Online Development Edition (CODE) y está disponible de forma gratuita y en pleno desarrollo, ¡con nuevas funciones y mejoras todo el tiempo! Los usuarios empresariales tienen acceso a la versión basada en Collabora Online Enterprise, más estable y escalable, mediante una [suscripción de soporte de Nextcloud](https://nextcloud.com/enterprise/).

Gracias a la asociación de {vendor}`Nextcloud` con Collabora, {vendor}`Nextcloud` puede ofrecer una solución de oficina en línea para toda la comunidad de {vendor}`Nextcloud`, con varias opciones de despliegue. Los usuarios empresariales que busquen una solución más fiable deben ponerse en contacto con el equipo de ventas de {vendor}`Nextcloud`.

- {nc-doc}`admin_manual/office/installation`
- {nc-doc}`admin_manual/office/configuration`
- {nc-doc}`admin_manual/office/migration`
- {nc-doc}`admin_manual/office/troubleshooting`
````

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
