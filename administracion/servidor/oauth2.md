---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Conectar servicios externos a Nextcloud con OAuth2: alta del cliente, extremos, token de acceso, seguridad y cómo omitir el aviso previo al inicio de sesión."
---
# OAuth2

## Resumen

Esta página explica, para quienes administran el servidor, cómo registrar un cliente OAuth2 para conectar un servicio externo a Nextcloud, qué extremos usar, cómo se envía el token de acceso, qué limitaciones de seguridad tiene y cómo omitir el aviso previo al inicio de sesión.

````{upstream} admin_manual/configuration_server/oauth2.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud permite conectar servicios externos (por ejemplo, Moodle) a Nextcloud. Esto se hace mediante `OAuth2`. La especificación de OAuth2 está en la [RFC6749](https://tools.ietf.org/html/rfc6749).

:::{note}
Nextcloud solo admite clientes confidenciales.
:::

### Añadir una aplicación OAuth2

Ir a {guilabel}`Configuraciones de administración` → {guilabel}`Seguridad`. Ahí puede añadirse un nuevo cliente `OAuth2`.

Introducir el nombre de la aplicación e indicar una URL de redirección. Ahora debería disponerse de un identificador de cliente y de un secreto. Introducirlos en el cliente `OAuth2`.

Facilitar a la aplicación OAuth2 los siguientes datos:

- Extremo de autorización: `https://cloud.example.org/apps/oauth2/authorize`
- Extremo de token: `https://cloud.example.org/apps/oauth2/api/v1/token`

Hay que tener en cuenta que debe incluirse `index.php` si no están configuradas las URL amigables, es decir, `https://cloud.example.org/index.php/apps/oauth2/api/v1/token`.

### El token de acceso

El token de acceso que se obtiene es un token llamado Bearer. Esto significa que en las solicitudes al servidor Nextcloud hay que enviar la cabecera de autorización correspondiente.

Authorization: Bearer \<TOKEN>

Hay que tener en cuenta que apache la elimina de forma predeterminada. Asegurarse de tener activados `mod_headers`, `mod_rewrite` y `mod_env`.

### Consideraciones de seguridad

Por ahora, la implementación de `OAuth2` de Nextcloud no admite el acceso limitado por ámbitos. Esto significa que cada token tiene acceso total a la cuenta completa, incluidos los permisos de lectura y escritura sobre los archivos almacenados. ¡Es imprescindible guardar los tokens `OAuth2` de forma segura!

Sin ámbitos ni acceso restringible, no se recomienda usar una instancia de Nextcloud como servicio de autenticación de usuarios.

### Omitir el aviso previo al inicio de sesión

En el flujo `OAuth2` predeterminado de Nextcloud se muestra un paso de confirmación antes del inicio de sesión si el usuario aún no ha iniciado sesión, y un segundo paso después del inicio de sesión. Para omitir el previo al inicio de sesión en una aplicación de confianza, puede establecerse con occ la opción de configuración `skipAuthPickerApplications`:

```
sudo -E -u www-data php occ config:app:set oauth2 skipAuthPickerApplications --type array --value '["myapplication"]'
```
````
