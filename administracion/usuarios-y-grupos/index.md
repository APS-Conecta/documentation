---
tipo: guia
esqueleto: borrador
audiencia: administracion
apps: [gestion]
resumen: "Control de acceso por grupos: roles del CESFAM, categorías, equipos y la carga del personal."
---
# Usuarios y grupos

## Resumen

El control de acceso se administra por grupos: el grupo es la única llave de autorización, con los roles estándar del CESFAM, las cuatro categorías funcionales y las carpetas de grupo montadas por área. El ciclo de vida de las cuentas — creación, pertenencias, contraseñas y baja — se opera por línea de comandos y por el aprovisionamiento declarativo.

## Secciones previstas

- El grupo como llave única
- Los roles estándar
- Categorías funcionales
- Carpetas de grupo y ACL
- Ciclo de vida de cuentas

````{upstream} admin_manual/configuration_user/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

- {nc-doc}`admin_manual/configuration_user/user_configuration`
- {nc-doc}`admin_manual/configuration_user/reset_admin_password`
- {nc-doc}`admin_manual/configuration_user/reset_user_password`
- {nc-doc}`admin_manual/configuration_user/user_password_policy`
- {nc-doc}`admin_manual/configuration_user/authentication`
- {nc-doc}`admin_manual/configuration_user/two_factor-auth`
- {nc-doc}`admin_manual/configuration_user/user_auth_ldap`
- {nc-doc}`admin_manual/configuration_user/user_auth_ldap_cleanup`
- {nc-doc}`admin_manual/configuration_user/user_auth_ldap_api`
- {nc-doc}`admin_manual/configuration_user/user_provisioning_api`
- {nc-doc}`admin_manual/configuration_user/profile_configuration`
- {nc-doc}`admin_manual/configuration_user/user_auth_oidc`
````

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
