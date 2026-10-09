---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Activar proveedores de autenticación de dos factores, imponerla a todos o a grupos, y limpiar, desactivar o consultar la 2FA de usuarios con occ."
---
# Autenticación de dos factores

## Resumen

Esta página explica cómo activar los proveedores de autenticación de dos factores, cómo imponer su uso a todo el sistema o a grupos concretos y cómo limpiar, desactivar o consultar la 2FA de los usuarios con `occ`. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_user/two_factor-auth.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La autenticación de dos factores añade una capa adicional de seguridad a las cuentas de usuario. Para iniciar sesión en una cuenta que tiene activada la autenticación de dos factores (2FA), hay que proporcionar tanto la contraseña de inicio de sesión como otro factor.

Para usar 2FA deben cumplirse dos condiciones:

- El administrador debe activar al menos un proveedor de 2FA.
- El usuario debe activar 2FA en su cuenta (o) el administrador debe imponer el uso de 2FA.

Ambos pasos se describen a continuación.

### Activar la autenticación de dos factores

En Nextcloud, 2FA es modular: pueden usarse distintos proveedores de 2FA para admitir distintos tipos de factores. Hay tres proveedores que se instalan automáticamente (aunque puede que haya que activarlos):

**Two-Factor TOTP Provider**

- Un proveedor de factor 2FA que permite usar como factor secundario una app [TOTP](https://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm) (RFC 6238) instalada en un teléfono (u otro dispositivo)
- Compatible con cualquier app cliente TOTP que cumpla RFC 6238 (como [Aegis](https://github.com/beemdevelopment/aegis) o Google Authenticator).
- Desactivado de forma predeterminada. Para activar este factor, ir a *Apps->Apps deshabilitadas* y buscar *Two-Factor TOTP Provider*.

**Two-Factor Authentication via Nextcloud notifications**

- Un proveedor de factor 2FA que permite usar como factor secundario un dispositivo con la sesión iniciada.
- Desactivado de forma predeterminada. Para activar este factor, ir a *Apps->Apps deshabilitadas* y buscar *Two-Factor Authentication via Nextcloud notification*.

**Two-Factor Backup Codes**

- Un proveedor de factor 2FA especial que permite a los usuarios generar códigos de respaldo.
- Facilita recuperar el acceso si un dispositivo 2FA no está disponible (es decir, si lo roban o deja de funcionar).
- Genera diez códigos de respaldo (que, por supuesto, solo pueden usarse una vez).
- Siempre activado.

En la tienda de apps pueden encontrarse otros proveedores de 2FA.

Los desarrolladores también pueden [implementar nuevas apps de proveedor de dos factores](https://docs.nextcloud.com/server/latest/developer_manual/digging_deeper/two-factor-provider.html).

### Imponer la autenticación de dos factores

De forma predeterminada, 2FA es *opcional*, así que los usuarios pueden elegir si la activan para su cuenta [en sus ajustes personales](https://docs.nextcloud.com/server/latest/user_manual/en/user_2fa.html). Sin embargo, los administradores pueden imponer el uso de 2FA.

La imposición puede aplicarse a todo el sistema (todos los usuarios) o solo a grupos seleccionados. También pueden excluirse grupos seleccionados de los requisitos de 2FA.

Estos ajustes están en *Configuraciones de administración->Seguridad*.

Cuando se seleccionan o excluyen grupos, se aplica la siguiente lógica para determinar si un usuario tiene 2FA impuesta:

- Si no se selecciona ningún grupo, 2FA se activa para todos, excepto para los miembros de los grupos excluidos
- Si se seleccionan grupos, 2FA se activa para todos sus miembros. Si un usuario está a la vez en un grupo seleccionado *y* en uno excluido, prevalece el seleccionado y 2FA se impone.

### Eliminación de proveedores

Nextcloud mantiene un registro de los proveedores de autenticación de dos factores activados de cada usuario. Si un proveedor simplemente se elimina o se {nc-ref}`desactiva <apps_commands_label>`, Nextcloud seguirá considerando el proveedor activo para el usuario al iniciar sesión y mostrará una advertencia como *«Could not load at least one of your enabled two-factor auth methods»*.

Las asociaciones de los proveedores eliminados pueden limpiarse con {nc-ref}`occ <occ>`:

```
sudo -E -u www-data php occ twofactorauth:cleanup <provider_id>
```

:::{warning}
Esta operación es irreversible. Ejecutarla solo para proveedores que no se vayan a volver a activar, porque en ese caso habría que repetir la configuración desde cero para todos los usuarios.
:::

### Desactivar la autenticación de dos factores

Los proveedores de dos factores pueden desactivarse con {nc-ref}`occ <occ>`:

```
sudo -E -u www-data php occ twofactorauth:disable <uid> <provider_id>
```

Esto puede ser útil si el usuario olvidó o perdió su segundo factor. Después, los usuarios pueden volver a activar este proveedor desde sus ajustes personales.

:::{note}
El proveedor tiene que admitir esta operación. Si no la admite, Nextcloud la interrumpirá y mostrará un error.
:::

También puede comprobarse el estado actual de dos factores de un usuario con {nc-ref}`occ <occ>`:

```
sudo -E -u www-data php occ twofactorauth:state <uid>
```
````
