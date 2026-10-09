---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Por qué vías se exponen las API de Nextcloud (REST, OCS y WebDAV) y el error genérico del modo de mantenimiento: HTTP 503 con su cabecera."
---
# Generalidades

## Resumen

Esta página indica, para quienes desarrollan clientes, por qué vías se exponen las API de Nextcloud y describe el error genérico que se devuelve durante el modo de mantenimiento.

````{upstream} developer_manual/client_apis/general.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Las API de Nextcloud están disponibles principalmente a través de {nc-ref}`rest-apis`, {nc-ref}`OCS <ocsapiindex>` y {nc-ref}`webdavapiindex`.

### Errores genéricos

Además de los errores específicos de cada API, hay algunos errores genéricos que Nextcloud puede lanzar en las API web.

#### Modo de mantenimiento

Si Nextcloud está fuera de servicio por mantenimiento, envía una respuesta HTTP con el código de estado 503 y la cabecera `x-nextcloud-maintenance-mode: 1`.
````
