---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Traducir una app: herramienta de traducción, sincronización con Transifex (.tx/config, ramas, .l10nignore, permisos) y traducción manual con gettext."
---
(nc-dev-translation)=
# Traducción

## Resumen

Esta página explica cómo traducir una app: la herramienta que extrae las cadenas, la configuración de la sincronización con Transifex en la comunidad (archivo de configuración, ramas, archivos excluidos, validación y permisos del repositorio), la traducción manual sin Transifex, y enumera los cuatro procesos de traducción. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/app_development/translation.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El sistema de traducción de {vendor}`Nextcloud` funciona con [Transifex](https://explore.transifex.com/nextcloud/). Para empezar a traducir, registrarse y entrar en un grupo. Si la app de la comunidad debe traducirla la [comunidad de {vendor}`Nextcloud` en Transifex](https://explore.transifex.com/nextcloud/), basta con seguir la sección de configuración de más abajo.

### Herramienta de traducción

:::{note}
Por ahora, la traducción basada en la herramienta solo admite repositorios alojados en `github.com`. Si la app está alojada en otro lugar, se puede intentar seguir en su lugar la {nc-ref}`manual-translation`.
:::

La [herramienta de traducción](https://github.com/nextcloud/docker-ci/tree/master/translations/translationtool) recorre el código fuente en busca de llamadas a los métodos `t()`
o `n()` para extraer las cadenas que deben traducirse. Si, por ejemplo, se incluye en el repositorio código JS minificado, esos nombres de métodos también son bastante
comunes y podrían provocar extracciones erróneas. Por eso se permite
indicar una lista de archivos en los que la herramienta de traducción no buscará
cadenas. Basta con añadir un archivo llamado {file}`.l10nignore` en
la carpeta raíz de la app e indicar los archivos, uno por línea:

```
# compiled vue templates
js/bruteforcesettings.js
```

### Configuración de la sincronización con Transifex

#### Configuración de Transifex `.tx/config`

Para configurar la sincronización con Transifex dentro de la comunidad de {vendor}`Nextcloud`, primero hay que añadir
la configuración de Transifex a la carpeta de la app en {file}`.tx/config` (reemplazar `MYAPP` por el id de la app):

```ini
[main]
host     = https://www.transifex.com
lang_map = hu_HU: hu, nb_NO: nb, sk_SK: sk, th_TH: th, ja_JP: ja, bg_BG: bg, cs_CZ: cs, fi_FI: fi

[o:nextcloud:p:nextcloud:r:{{APPID}}]
file_filter = translationfiles/<lang>/{{APPID}}.po
source_file = translationfiles/templates/{{APPID}}.pot
source_lang = en
type        = PO
```

Luego crear una carpeta {file}`l10n` y un archivo {file}`l10n/.gitkeep` para crear una
carpeta vacía que más adelante contendrá las traducciones.

#### Selección de ramas `.tx/backport`

El bot se ejecutará cada noche y solo enviará commits a las siguientes ramas cuando haya una actualización de la traducción:

* main
* master
* stableX (siendo X las 3 versiones recientes de Nextcloud Server)

Esta lista se puede sobrescribir creando en el repositorio un archivo `.tx/backport` con el siguiente contenido:

```
develop stable
```

Eso sincronizaría las traducciones de las ramas (`main` y `master` se añaden automáticamente):

* main
* master
* develop
* stable

#### Excluir archivos `.l10nignore`

Añadir un archivo más, llamado {file}`.l10nignore`, en la raíz del repositorio, con los archivos y carpetas que se deben ignorar en las traducciones.
Debe usarse para excluir archivos que generan falsos positivos en las traducciones, como:

- Archivos JavaScript compilados `js/`
- Dependencias PHP de terceros `vendor/`
- Archivos y documentación que no se distribuyen `docs/`

#### Validar las cadenas de origen

Una vez terminada la configuración, se pueden validar las cadenas de origen de la traducción, lo que señala algunos errores comunes.
Clonar el repositorio [nextcloud/docker-ci](https://github.com/nextcloud/docker-ci/) y después ejecutar el siguiente script:

```sh
bash translations/validateSyncSetup.sh Owner Repository
```

#### Permisos del repositorio

Ahora la cuenta de GitHub [@nextcloud-bot](https://github.com/nextcloud-bot) necesita acceso `write` al repositorio.
Se la puede invitar desde los ajustes del repositorio:

```
https://github.com/<user-name>/<repo-name>/settings/access
```

Después de enviar la invitación, [abrir un ticket con la plantilla «Request translations»](https://github.com/nextcloud/docker-ci/issues/new/choose).

:::{attention}
En general, conviene activar la
[función de ramas protegidas](https://help.github.com/articles/configuring-protected-branches/)
para las ramas predeterminada y estables. Si se hace, hay que conceder a
[@nextcloud-bot](https://github.com/nextcloud-bot) permisos `admin` y permitir que los administradores se salten la protección.
Sin embargo, esta función solo es posible en repositorios que pertenecen a organizaciones, ¡no en repositorios que pertenecen a personas!
Se puede [crear una organización propia](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/creating-a-new-organization-from-scratch)
:::

Si se necesita ayuda, basta con [abrir un ticket con la solicitud](https://github.com/nextcloud/docker-ci/issues/new/choose)
y también se puede recibir orientación a lo largo de los pasos.

(nc-dev-manual-translation)=
### Traducción manual

Si Transifex no es la opción adecuada o la app no se acepta para traducción,
generar las cadenas de gettext por cuenta propia ejecutando nuestra
[herramienta de traducción](https://github.com/nextcloud/docker-ci/tree/master/translations/translationtool)
en la carpeta de la app:

```
cd /srv/http/nextcloud/apps/myapp
translationtool.phar create-pot-files
```

La herramienta de traducción requiere `gettext`, que se puede instalar con:

```
apt-get install gettext
```

La herramienta anterior genera una plantilla que se puede usar para traducir todas las cadenas
de una app. Esta plantilla se encuentra en la carpeta {file}`translationfiles/template/` con el
nombre {file}`myapp.pot`. Se puede usar con la herramienta de traducción que se prefiera, como
[Poedit](https://poedit.net). Esta crea entonces un archivo {file}`.po`.
El archivo {file}`.po` debe colocarse en una carpeta con el nombre del código de idioma
y con el nombre de la app como nombre de archivo; por ejemplo, {file}`translationfiles/es/myapp.po`.
Después de este paso, hay que invocar la herramienta para pasar el archivo po a nuestro
propio formato de archivo, que el código del servidor lee más fácilmente:

```
translationtool.phar convert-po-files
```

Ahora está disponible la siguiente estructura de carpetas:

```
myapp/l10n
|-- es.js
|-- es.json
myapp/translationfiles
|-- es
|   |-- myapp.po
|-- templates
    |-- myapp.pot
```

Después solo se necesitan los archivos {file}`.json` y {file}`.js` para tener una app localizada que funcione.

### Documentación sobre el proceso de traducción

A continuación se describen cuatro procesos:

1. Proceso para traducir una cadena nueva

2. Proceso para corregir un error tipográfico o gramatical en una cadena traducida

3. Proceso para hacer traducible una cadena que no lo es

4. Proceso para corregir un problema en la cadena de origen
````
