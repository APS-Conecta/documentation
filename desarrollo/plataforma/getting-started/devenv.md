---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Preparar a mano un entorno de desarrollo sin docker: servidor web, código fuente desde GitHub, apps incluidas, modo de depuración y código al día."
---
# Entorno de desarrollo

## Resumen

Esta página explica cómo preparar manualmente un entorno de desarrollo sin docker: el servidor web y la base de datos, el código fuente obtenido desde GitHub, las apps externas incluidas, el modo de depuración y cómo mantener el código al día. Está dirigida a quienes desarrollan sobre la plataforma.

````{upstream} developer_manual/getting_started/devenv.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Hay disponible un tutorial para configurar el entorno de desarrollo con docker. El tutorial puede encontrarse [aquí](https://cloud.nextcloud.com/s/iyNGp8ryWxc7Efa?path=%2F). Se recomienda seguir ese tutorial.

Esta página describe cómo configurar el entorno de desarrollo sin docker.

Seguir los pasos de esta página para configurar el entorno de desarrollo manualmente.

### Configurar el servidor web y la base de datos

Primero, [configurar el servidor web y la base de datos](https://docs.nextcloud.com/server/latest/admin_manual/installation/index.html) (**Sección**: «Manual Installation - Prerequisites»).

### Obtener el código fuente

Hay dos formas de obtener el código fuente de Nextcloud:

- Usando la [versión estable](https://docs.nextcloud.com/server/latest/admin_manual/installation/index.html)
- Usando la versión de desarrollo de [GitHub][GitHub], que se explica a continuación.

Para obtener el código fuente de [GitHub][GitHub] es necesario instalar Git (consultar [Configurar Git](https://help.github.com/articles/set-up-git) en la ayuda de GitHub)

#### Recopilar información sobre la configuración del servidor

Para empezar, hay que clonar los repositorios básicos de Git en el directorio del servidor web. Según la distribución, será uno de estos:

- **/var/www**
- **/var/www/html**
- **/srv/http**

Luego, identificar el usuario y el grupo con los que se ejecuta el servidor web; el usuario y el grupo de Apache para el comando **chown** serán uno de estos:

- **http**
- **www-data**
- **apache**
- **wwwrun**

#### Obtener el código

Los siguientes comandos usan **/var/www** como directorio del servidor web y **www-data** como nombre de usuario y grupo.

Dar permiso de escritura sobre el directorio para poder instalar el código con el usuario habitual, sin necesitar privilegios de root:

```
sudo chmod o+rw /var/www
```

Luego, instalar Nextcloud en la raíz del sitio desde Git:

```
git clone https://github.com/nextcloud/server.git /var/www/
cd /var/www
git submodule update --init
```

Si se prefiere instalar Nextcloud en una subcarpeta, reemplazar */var/www* por */var/www/\<folder\>*.

Crear la carpeta de datos:

```
cd /var/www
mkdir data
```

Ajustar los permisos:

```
cd /var/www
sudo chown -R www-data:www-data config data apps
sudo chmod o-rw /var/www
```

Por último, reiniciar el servidor web (esto puede variar según la distribución):

```
sudo systemctl restart httpd.service
```

o:

```
sudo systemctl restart apache2.service
```

o:

```
sudo /etc/init.d/apache2 restart
```

Ahora, acceder a la instalación en <http://localhost/> (o en la URL correspondiente) desde el navegador web para configurar la instancia.

#### Obtener las apps externas incluidas

Este paso opcional es especialmente necesario si se quiere probar la actualización, ya que las siguientes apps deben estar presentes durante una actualización.

Instalar la app viewer:

```
cd /var/www/apps
git clone https://github.com/nextcloud/viewer.git
```

Asegurarse de usar una versión compatible con el servidor haciendo checkout de la etiqueta correspondiente. Puede revisarse el `appinfo/info.xml` de la app para ver si su campo `min-version` es compatible con el servidor actual.

Al actualizar el código del servidor, puede que también haya que actualizar el código de la app antes de ejecutar `occ upgrade`.

:::{note}
Lo mismo se aplica a todas las apps listadas en `alwaysEnabled` de [shipped.json](https://github.com/nextcloud/server/blob/master/core/shipped.json#L49), aunque la mayoría ya están presentes en el repositorio del servidor.
:::

(nc-dev-debugmode)=
#### Activar el modo de depuración

:::{note}
¡No activar esto en producción! Puede crear problemas de seguridad y está pensado únicamente para depuración y desarrollo.
:::

Para desactivar la caché de JavaScript y CSS, hay que activar la depuración estableciendo `debug` en `true` en {file}`config/config.php`:

```
<?php
$CONFIG = array (
    'debug' => true,
    ... configuration goes here ...
);
```

#### Mantener el código actualizado

Si se tiene más de un repositorio clonado, hacer la misma acción en todos los repositorios uno por uno puede llevar mucho tiempo. Para resolverlo, puede usarse la siguiente plantilla de comando:

```
find . -maxdepth <DEPTH> -type d -name .git -exec sh -c 'cd "{}"/../ && pwd && <GIT COMMAND>' \;
```

luego, p. ej., para traer todos los cambios en todos los repositorios, basta con esto:

```
find . -maxdepth 3 -type d -name .git -exec sh -c 'cd "{}"/../ && pwd && git pull --rebase' \;
```

o, para podar todas las ramas fusionadas, se ejecutaría esto:

```
find . -maxdepth 3 -type d -name .git -exec sh -c 'cd "{}"/../ && pwd && git remote prune origin' \;
```

Es aún más fácil si se crean alias para estos comandos, para no tener que volver a escribirlos cada vez que se necesiten.

[GitHub]: https://github.com/nextcloud
[GitHub Help Page]: https://help.github.com/
````
