---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "OpenID Connect: autenticar contra un proveedor de identidad externo con user_oidc, usar el servidor como proveedor con oidc y validar tokens bearer."
---
# Autenticación de usuarios con OpenID Connect

## Resumen

Esta página explica cómo los usuarios pueden autenticarse contra un proveedor de identidad OpenID Connect externo con la app `user_oidc`, cómo el propio servidor puede actuar como proveedor de identidad con la app `oidc` y cómo se validan los tokens bearer en las solicitudes a la API. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_user/user_auth_oidc.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los usuarios de Nextcloud pueden autenticarse mediante un proveedor de identidad externo. Nextcloud también puede ser, a su vez, un proveedor de identidad.

### Autenticación en Nextcloud

La [app OpenID Connect user backend](https://apps.nextcloud.com/apps/user_oidc) permite que los usuarios se autentiquen mediante proveedores de identidad Oidc externos.

Opcionalmente, esta app puede encargarse del aprovisionamiento de usuarios (creando los usuarios cuando se conectan por primera vez) o bien apoyarse en otros backends de usuarios y ocuparse solo de la autenticación.

[Más detalles en el README del proyecto](https://github.com/nextcloud/user_oidc#user_oidc)

### Usar Nextcloud como proveedor de identidad

La [app comunitaria OIDC Identity Provider](https://apps.nextcloud.com/apps/oidc) puede instalarse para convertir Nextcloud en un proveedor de identidad para otros servicios.

Esta app permite que cualquier usuario de Nextcloud (gestionado por cualquier backend de usuarios) se autentique durante un flujo de inicio de sesión Oidc. Resulta útil cuando se quiere que la instancia de Nextcloud sea la autoridad en materia de autenticación y de datos del perfil de usuario entre varios servicios.

### Validación de tokens bearer

Nextcloud puede aceptar los tokens de ID y los tokens de acceso de Oidc como token bearer válido en las solicitudes a la API. Si se usa un proveedor de identidad externo, solo hace falta la app `user_oidc`.

Si Nextcloud es el proveedor de identidad, naturalmente hará falta la app `oidc` para convertir Nextcloud en un proveedor Oidc, y también la app `user_oidc`, porque será la que se encargue de validar la autenticación de las solicitudes a la API. En user_oidc, el indicador de configuración `oidc_provider_bearer_validation` debe establecerse en true para que `user_oidc` sepa que tiene que pedir a la app `oidc` que valide los tokens bearer recibidos.

[Más detalles sobre la validación de tokens bearer](https://github.com/nextcloud/user_oidc#bearer-token-validation)
````
