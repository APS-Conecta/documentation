---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo autentica AppAPI las solicitudes de las ExApps: flujo, cabeceras requeridas, el atributo AppAPIAuth y la clave de sesión app_api."
---
(nc-dev-app_api_auth)=
# Autenticación

## Resumen

Esta página explica el método de autenticación de AppAPI para las ExApps, basado en un secreto compartido: el flujo de validación de una solicitud, las cabeceras que debe llevar, el atributo `AppAPIAuth` y la clave de sesión que AppAPI establece tras autenticar. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/Authentication.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
AppAPI introduce un método de autenticación propio para las apps externas.
Esta autenticación se basa en un secreto compartido entre Nextcloud y la app externa.

### Flujo de autenticación

1. La ExApp envía una solicitud a Nextcloud
2. Nextcloud pasa la solicitud a AppAPI
3. AppAPI valida la solicitud (ver el [flujo de autenticación en detalle](#authentication-authentication-flow-in-details))
4. La solicitud se acepta o se rechaza

(nc-dev-auth-headers)=
### Cabeceras de autenticación

Cada solicitud de una ExApp a una API protegida con AppAPIAuth debe contener las siguientes cabeceras:

1. `AA-VERSION` - versión mínima de AppAPI
2. `EX-APP-ID` - ID de la ExApp
3. `EX-APP-VERSION` - versión de la ExApp
4. `AUTHORIZATION-APP-API` - `userid:secret` codificado en base64

(authentication-authentication-flow-in-details)=
#### Flujo de autenticación en detalle

El diagrama de secuencia de esta sección muestra el orden de las comprobaciones: Nextcloud rechaza la solicitud si falta la cabecera AUTHORIZATION-APP-API o si AppAPI no existe o está deshabilitada; AppAPI la rechaza si la ExApp no existe o está deshabilitada o si el secreto compartido no coincide, comprueba que el usuario no esté vacío y esté activo y establece el usuario activo; Nextcloud responde con 200 o 401.

### AppAPIAuth

AppAPI proporciona un atributo `AppAPIAuth` con un middleware para validar las solicitudes de las ExApps.
En los controladores de la API se puede usar como atributo de PHP.

### Claves de sesión de AppAPI

Tras una autenticación correcta, AppAPI establece la clave de sesión *app_api* en `true`.

```php
$this->session->set('app_api', true);
```

:::{note}
El servidor de Nextcloud verifica esta clave de sesión y permite omitir la **protección CORS** y la **autenticación de dos factores** en las solicitudes que provienen de las ExApps.
Además, el límite de tasa no se aplica a las solicitudes que provienen de las ExApps.
:::
````
