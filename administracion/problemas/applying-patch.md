---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo obtener el parche de un pull request de GitHub, aplicarlo al servidor o a una app y revertirlo."
---
# Aplicar parches a Nextcloud

## Resumen

Esta página explica cómo obtener el parche de un pull request de GitHub, aplicarlo al servidor o a una app, revertirlo y qué mensajes de error pueden ignorarse al hacerlo. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/issues/applying_patch.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

### Obtener un parche

Si se ha encontrado en GitHub un pull request relacionado que soluciona el problema, o si se quiere ayudar a los desarrolladores y verificar que una corrección funciona, puede obtenerse un parche del pull request.

1. Se usa <https://github.com/nextcloud/server/pull/26396> como ejemplo.
2. Añadir `.diff` a la URL: <https://github.com/nextcloud/server/pull/26396.diff>
3. Descargar el parche al servidor, por ejemplo con `wget https://github.com/nextcloud/server/pull/26396.diff` (esto deja `26396.diff` en el directorio local)
4. Seguir los pasos de «Aplicar un parche».
5. Si se usa una versión anterior de Nextcloud, puede que primero haya que ir al parche de backport correcto para esa versión.
6. La versión adecuada puede encontrarse buscando un enlace publicado por `backportbot-nextcloud` al pull request de backport de la versión en uso, o buscando un comentario de un desarrollador con un enlace a un backport manual. Usar la URL `.diff` de ese PR de backport.

### Aplicar un parche

#### Aplicar parches al servidor

1. Ir al directorio raíz del servidor Nextcloud (el que contiene el archivo `status.php`).
2. Descargar el parche al servidor, por ejemplo con `wget https://github.com/nextcloud/server/pull/26396.diff` (esto deja `26396.diff` en el directorio local)
3. Aplicar el parche con el siguiente comando:

   ```
   patch -p 1 < ./26396.diff
   ```

4. Como alternativa, si el comando patch no está disponible, usar:

   ```
   git apply --check ./26396.diff
   git apply ./26396.diff
   ```

#### Aplicar parches a las apps

1. Ir a la raíz de la app (normalmente `apps/[APPID]/`). Si la app no está ahí, usar el comando `sudo -E -u www-data php occ app:getpath APPID` para encontrar la ruta.
2. Descargar el parche al servidor, por ejemplo con `wget https://github.com/nextcloud/<app>/pull/26396.diff` (esto deja `26396.diff` en el directorio local)
3. Aplicar el parche con el mismo comando que en «Aplicar parches al servidor».

### Revertir un parche

1. Ir al directorio en el que se aplicó el parche.
2. Revertir el parche con la opción `-R`:

   ```
   patch -R -p 1 < ./26396.diff
   ```

3. Como alternativa, si el comando patch no está disponible, usar:

   ```
   git apply --reverse ./26396.diff
   ```

### Notas y solución de problemas

:::{note}
Pueden aparecer errores sobre archivos que no se encuentran, sobre todo al aplicar parches de GitHub. Los parches pueden incluir archivos de desarrollo o de prueba (por ejemplo, archivos bajo `build/` o `tests/`) que no están presentes en la instalación. Estos mensajes son esperables y pueden ignorarse si solo se refieren a esos archivos.
:::
````
