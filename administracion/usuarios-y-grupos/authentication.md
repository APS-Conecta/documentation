---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Contraseñas de aplicación de Nextcloud, el borrado remoto y la limpieza automática de las que no se usan, con los parámetros que fijan sus plazos."
---
(nc-authentication)=
# Autenticación

## Resumen

Esta página explica qué son las contraseñas de aplicación, cuándo son obligatorias y cómo Nextcloud elimina automáticamente las que no se usan, con los parámetros que ajustan esos plazos. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_user/authentication.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Contraseñas de aplicación

Las contraseñas de aplicación permiten a los usuarios autenticar varias aplicaciones cliente contra su cuenta de Nextcloud sin entregar a la aplicación la contraseña de inicio de sesión. Las contraseñas de aplicación son obligatorias en las cuentas que tienen activada la {nc-ref}`autenticación de dos factores <two-factor-auth>`.

Algunos clientes admiten el *borrado remoto*, que hace que la aplicación conectada elimine sus datos locales.

(nc-authentication-app-password-clean-up)=
#### Limpieza automática

:::{versionadded} 30
:::

Nextcloud elimina las contraseñas que no se usan. Las contraseñas configuradas para el *borrado remoto* se eliminan tras 60 días sin uso. Las contraseñas de aplicación de las aplicaciones cliente se eliminan tras 365 días sin uso.

Estos plazos pueden sobrescribirse mediante la configuración:

```
sudo -E -u www-data php occ config:system:set token_auth_wipe_token_retention --type=int --value 2592000 # 60*60*24*30 - 30 days
sudo -E -u www-data php occ config:system:set token_auth_token_retention --type=int --value 63072000     # 60*60*24*365*2 - 2 years
```

Los valores se indican en **segundos**.
````
