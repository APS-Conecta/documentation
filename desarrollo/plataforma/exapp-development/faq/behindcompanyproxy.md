---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo configurar de forma permanente un proxy corporativo para PHP CLI, en php.ini o con variables de entorno, para que los comandos occ accedan a Internet."
---
# Proxy corporativo: ajustes permanentes para PHP CLI

## Resumen

Esta página explica cómo configurar de forma permanente los ajustes de un proxy corporativo para PHP CLI, editando su `php.ini` o definiendo variables de entorno para todo el sistema, cuando los comandos `occ` no logran acceder a Internet. Está dirigida a quienes administran el servidor o desarrollan ExApps.

````{upstream} developer_manual/exapp_development/faq/BehindCompanyProxy.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Si se usa nuestra aplicación dentro de una red corporativa que requiere ajustes de proxy, pueden surgir problemas al ejecutar comandos de PHP CLI que intentan acceder a Internet.

Para resolverlo, es necesario configurar ajustes de proxy permanentes para el entorno de PHP CLI.

### Síntomas

Al ejecutar el comando:

```bash
sudo -E -u www-data php occ app_api:app:register test-deploy docker_socket_proxy --info-xml https://raw.githubusercontent.com/nextcloud/test-deploy/main/appinfo/info.xml --test-deploy-mode --no-ansi --no-warnings
```

Puede aparecer un error similar a:

```text
file_get_contents(https://raw.githubusercontent.com/nextcloud/test-deploy/main/appinfo/info.xml): Failed to open stream: Connection timed out at /var/www/html/custom_apps/app_api/lib/Service/ExAppService.php#277
```

### Causa

Este problema se produce porque el entorno de PHP CLI no tiene configurados los ajustes de proxy, a diferencia del entorno PHP web, que puede estar usando ya los ajustes de proxy especificados en la configuración del servidor web.

### Solución permanente

Para configurar de forma permanente los ajustes de proxy de PHP CLI, se puede modificar el archivo `php.ini` de PHP CLI o bien definir variables de entorno para todo el sistema.

#### Método 1: editar el archivo php.ini de PHP CLI

1. **Localizar el archivo php.ini de PHP CLI**

   Ejecutar el siguiente comando para encontrar el archivo de configuración que carga PHP CLI:

   ```bash
   php --ini
   ```

   Buscar la línea:

   ```text
   Loaded Configuration File: /path/to/php.ini
   ```

2. **Editar el archivo php.ini**

   Abrir el archivo `php.ini` en un editor de texto con los permisos adecuados:

   ```bash
   sudo nano /path/to/php.ini
   ```

3. **Añadir los ajustes de proxy**

   Añadir las siguientes líneas para configurar los ajustes de proxy:

   ```ini
   [HTTP]
   ; Proxy settings for HTTP
   http.proxy_host = "proxy.example.com"
   http.proxy_port = 8080
   http.proxy_user = "username"
   http.proxy_password = "password"

   [HTTPS]
   ; Proxy settings for HTTPS
   https.proxy_host = "proxy.example.com"
   https.proxy_port = 8080
   https.proxy_user = "username"
   https.proxy_password = "password"
   ```

   Sustituir los marcadores de posición por los datos reales del servidor proxy:

   - *proxy.example.com*: la dirección del servidor proxy.
   - *8080*: el puerto del servidor proxy.
   - *username*: el nombre de usuario del proxy (si se requiere).
   - *password*: la contraseña del proxy (si se requiere).

4. **Guardar y cerrar el archivo**

   Guardar los cambios y salir del editor de texto.

5. **Verificar la configuración**

   Ejecutar de nuevo el comando de PHP CLI:

   ```bash
   sudo -E -u www-data php occ app_api:app:register
   ```

   Ahora debería poder acceder a Internet a través del proxy.

:::{note}
No todas las funciones de PHP respetan los ajustes de proxy de `php.ini`.
Si los problemas persisten, considerar el uso de variables de entorno para todo el sistema.
:::

#### Método 2: definir variables de entorno para todo el sistema

1. **Editar el perfil del shell**

   Para una solución permanente, añadir los ajustes de proxy a las variables de entorno de todo el sistema. Abrir el archivo `/etc/environment`:

   ```bash
   sudo nano /etc/environment
   ```

2. **Añadir las variables de entorno del proxy**

   Añadir las siguientes líneas al archivo:

   ```bash
   http_proxy="http://proxy.example.com:8080"
   https_proxy="http://proxy.example.com:8080"

   # If your proxy requires authentication:
   http_proxy="http://username:password@proxy.example.com:8080"
   https_proxy="http://username:password@proxy.example.com:8080"
   ```

   Sustituir los marcadores de posición por los datos reales del proxy.

3. **Aplicar los cambios**

   Cerrar la sesión y volver a iniciarla, o reiniciar el sistema, para aplicar los cambios.

4. **Verificar la configuración**

   Ejecutar de nuevo el comando:

   ```bash
   sudo -E -u www-data php occ app_api:app:register test-deploy docker_socket_proxy --info-xml https://raw.githubusercontent.com/nextcloud/test-deploy/main/appinfo/info.xml --test-deploy-mode --no-ansi --no-warnings
   ```

   Ahora debería funcionar sin problemas de conectividad.

:::{note}
Este método define los ajustes de proxy para todos los usuarios y aplicaciones del sistema.
:::

### Solución de problemas

- **Datos del proxy incorrectos**

  Asegurarse de que todos los datos del proxy sean correctos. Nombres de host, puertos o credenciales incorrectos impedirán la conectividad.

- **Variables de entorno no cargadas**

  Asegurarse de que las variables de entorno se carguen correctamente. Puede ser necesario reiniciar el sistema o volver a iniciar sesión.

- **Restricciones del cortafuegos**

  Confirmar con el administrador de la red que el sistema tiene permitido acceder a Internet a través del proxy.

### Contactar con el soporte

Si después de seguir estos pasos los problemas persisten, contactar con nuestro equipo de soporte para obtener más ayuda.
````
