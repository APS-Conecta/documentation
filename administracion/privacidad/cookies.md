---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Las cookies que establece el servidor: nombre, finalidad, datos personales y duración, y la base jurídica de las cookies de «Recordarme»."
---
(nc-cookies)=
# Cookies

## Resumen

Esta página enumera las cookies que establece el servidor, con su finalidad, si contienen datos personales y su duración, y explica las cookies de «Recordarme» y cómo acortar su duración. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/gdpr/cookies.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud solo almacena las cookies necesarias para funcionar. Todas las cookies las establece directamente el servidor de Nextcloud: no interviene ninguna cookie de terceros.

Según el RGPD, solo las cookies que almacenan o transmiten datos personales requieren una base jurídica o consentimiento. De las cookies que se enumeran a continuación, solo las cookies de «Recordarme» contienen datos personales (el nombre de usuario). Todas las demás cookies contienen tokens generados aleatoriamente, sin información personal intrínseca.

:::{note}
El prefijo `__Host-` se aplica a las cookies del mismo sitio solo cuando se accede a Nextcloud mediante HTTPS. Con HTTP sin cifrar se omite el prefijo y las cookies se llaman `nc_sameSiteCookiestrict` y `nc_sameSiteCookielax`.
:::

### Cookies que almacena Nextcloud

| Tipo | Nombre | Finalidad | Datos personales | Duración |
|---|---|---|---|---|
| Cookie de sesión | `<instance_id>` | Lleva un ID de sesión de PHP aleatorio que se usa para identificar la sesión del usuario en el servidor. | No | Hasta que se cierra el navegador. |
| Cookie de sesión | `oc_sessionPassphrase` | Lleva un token aleatorio que se usa para descifrar los datos de sesión almacenados en el servidor. | No | Hasta que se cierra el navegador. |
| Cookie del mismo sitio | `__Host-nc_sameSiteCookiestrict` | Se usa para detectar si una solicitud se origina en el mismo sitio (`SameSite=Strict`). Ayuda a prevenir ataques CSRF. No contiene información del usuario. | No | Caduca el 2100-12-31 (en la práctica, permanente). |
| Cookie del mismo sitio | `__Host-nc_sameSiteCookielax` | Se usa para detectar solicitudes de navegación entre sitios (`SameSite=Lax`). Ayuda a prevenir ataques CSRF. No contiene información del usuario. | No | Caduca el 2100-12-31 (en la práctica, permanente). |
| Cookie de «Recordarme» | `nc_username` | Almacena el nombre de inicio de sesión del usuario para permitir un inicio de sesión persistente entre sesiones del navegador. | **Sí**: contiene el nombre de usuario. | 15 días de forma predeterminada. Configurable mediante `remember_login_cookie_lifetime`. |
| Cookie de «Recordarme» | `nc_token` | Un token aleatorio emparejado con `nc_username` para autenticar el inicio de sesión persistente sin almacenar la contraseña. | No | La misma que `nc_username`. |
| Cookie de «Recordarme» | `nc_session_id` | El ID de sesión original, que se conserva para permitir la continuidad de la sesión cuando se usa el token de «Recordarme». | No | La misma que `nc_username`. |
| Ayudante de descarga | `ocDownloadStarted` | Un token aleatorio de corta duración que se establece cuando empieza la descarga de un archivo y se usa para indicar al navegador que la descarga ha comenzado (p. ej., para ocultar un indicador de carga). | No | 20 segundos. |

### Cookies de «Recordarme»

Las cookies de «Recordarme» (`nc_username`, `nc_token`, `nc_session_id`) solo se establecen cuando el usuario selecciona explícitamente **Recordarme** al iniciar sesión. Se eliminan de inmediato cuando el usuario cierra la sesión.

Como `nc_username` contiene el nombre de inicio de sesión del usuario, es un dato personal según el RGPD. La base jurídica para almacenarlo suele ser el **interés legítimo** o la **ejecución de un contrato** (hacer posible el servicio que el usuario ha solicitado), siempre que se haya informado de ello al usuario en la política de privacidad.

La duración es de 15 días de forma predeterminada y puede acortarse en `config/config.php`:

```
'remember_login_cookie_lifetime' => 60 * 60 * 24 * 15,
```
````
