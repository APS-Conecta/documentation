---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo interactúan las apps con user_oidc y oidc mediante eventos: obtener el token de inicio de sesión, intercambiar tokens y generar un token interno."
---
# OpenID Connect (Oidc)

## Resumen

Esta página describe los eventos de la app `user_oidc` con los que otras apps obtienen el token de inicio de sesión de un proveedor de identidad externo, piden un intercambio de tokens o, con la app `oidc`, generan un token propio. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/oidc.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Hay varias formas de que las apps interactúen con las apps `user_oidc` y `oidc`.
Es posible obtener tokens de esas apps y pedirles que validen tokens.
Todos los eventos disponibles están en la app `user_oidc`, aunque algunos casos de uso no impliquen la función principal de esta app.

[Documentación de los eventos de user_oidc](https://github.com/nextcloud/user_oidc/tree/main/docs)

### Obtener el token de inicio de sesión

Al usar `user_oidc`, que usa un proveedor de identidad externo, el token de inicio de sesión puede almacenarse para que las apps
lo obtengan más tarde mediante un evento.

Hay que habilitar el indicador de configuración `store_login_token`.
`user_oidc` actualiza automáticamente el token de inicio de sesión cuando hace falta durante la sesión del usuario.
Las apps pueden obtener el token de inicio de sesión emitiendo el evento `OCA\UserOIDC\Event\ExternalTokenRequestedEvent`.

### Intercambio de tokens

Si el proveedor de identidad externo admite el intercambio de tokens, las apps pueden pedir a `user_oidc` que realice uno
y entregue el token intercambiado emitiendo el evento `OCA\UserOIDC\Event\ExchangedTokenRequestedEvent`.

### Generar un token si Nextcloud es el proveedor

Si se usa la app `oidc` para convertir Nextcloud en un proveedor de identidad, algunas apps de Nextcloud podrían necesitar pedir
a Nextcloud que genere un token que usarán para autenticarse ante un servicio externo.
Esto requiere tener instaladas las apps `oidc` y `user_oidc` (aunque `user_oidc` no se use como backend de usuarios).
El token puede generarse emitiendo el evento `OCA\UserOIDC\Event\InternalTokenRequestedEvent`.
````
