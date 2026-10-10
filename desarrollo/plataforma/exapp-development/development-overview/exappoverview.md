---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo se organiza una ExApp: estructura de carpetas, metadatos de info.xml, backend, frontend vía el proxy de AppAPI, traducciones y comandos del Makefile."
---
(nc-dev-exappoverview)=
# Visión general de las ExApps

## Resumen

Esta página explica cómo se organiza una ExApp: su estructura de carpetas y sus metadatos en info.xml, el backend y su almacenamiento persistente, los ajustes del frontend para cargarse mediante el proxy de AppAPI, las traducciones y los comandos recomendados del Makefile. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/development_overview/ExAppOverview.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El concepto básico de AppAPI es ofrecer una forma de desarrollar o escribir una app para Nextcloud en cualquier lenguaje, en especial su parte de backend.
La parte de frontend suele mantenerse igual. La ExApp puede entenderse como un microservicio.

### Estructura de una ExApp

La estructura de carpetas típica de una ExApp es la siguiente:

- **appinfo/**: contiene los metadatos de la ExApp, que se basan en el {nc-doc}`appinfo de las apps PHP de Nextcloud <developer_manual/app_development/info>` habitual,
  pero con nuevos campos adicionales bajo la clave `external-app`.
- **ex_app/**: la carpeta específica de la ExApp, que contiene las partes de frontend y backend de la ExApp.
  - **lib/**: contiene la parte de backend de la ExApp, que puede escribirse en cualquier lenguaje.
  - **src/**: contiene la parte de frontend de la ExApp, que es una aplicación Vue.js normal de Nextcloud, con pequeños ajustes en las rutas de carga de los scripts (ver {nc-ref}`Cambios específicos del frontend de las ExApps <ex_app_specific_frontend_changes>`).
  - **img/**: contiene las imágenes de la ExApp.
  - **css/**: contiene los archivos CSS de la ExApp.
- **l10n**: contiene las {nc-ref}`traducciones de la ExApp <ex_app_translations>`.
- **translationfiles**: contiene los archivos de traducción de origen (`.po`, `.mo`) de la ExApp.
- **otras carpetas o archivos**: depende de cada caso, p. ej., capturas de pantalla, scripts, etc.

(nc-dev-ex_app_info_xml_metadata)=
#### Metadatos de la ExApp

La etiqueta `<external-app>` de info.xml es obligatoria para los metadatos de la ExApp.
Debe contener los siguientes campos:

```
<external-app>
    <docker-install>
        <registry>ghcr.io</registry>
        <image>nextcloud/skeleton</image>
        <image-tag>latest</image-tag>
    </docker-install>
</external-app>
```

- **docker-install**: contiene la información de la imagen Docker de la ExApp.
  - **registry**: el registro de Docker donde se almacena la imagen.
  - **image**: el nombre de la imagen Docker.
  - **image-tag**: la etiqueta de la imagen Docker (etiqueta de versión).

### Backend

La parte de backend de la ExApp puede implementarse en cualquier lenguaje y framework que se desee.
El único requisito es seguir la arquitectura de microservicios y el {nc-ref}`flujo de comunicación <ex_app_lifecycle_methods>` ExApp <-> Nextcloud.

:::{note}
Hay una limitación del proxy de ExApps de AppAPI: no se admiten las conexiones websocket.
:::

Cada contenedor de ExApp tiene variables de entorno establecidas por AppAPI; puede encontrarse más información sobre ellas {nc-ref}`aquí <ex_app_env_vars>`.

#### Almacenamiento persistente

Para cada ExApp, AppAPI crea un volumen Docker (`nc_app_<app_id>_data`) que se conecta al contenedor de la ExApp como almacenamiento persistente.
Está disponible dentro del contenedor en la ruta `/nc_app_<app_id>_data` o mediante la variable de entorno `APP_PERSISTENT_STORAGE` que pasa AppAPI.

(nc-dev-ex_app_specific_frontend_changes)=
### Frontend

La parte de frontend de la ExApp se carga solo para la {nc-ref}`entrada de TopMenu <top_menu_section>`.
Es una aplicación Vue.js normal de Nextcloud con un pequeño ajuste de enrutamiento en las rutas,
ya que estas se cargan mediante el proxy de AppAPI desde el servidor de la ExApp.

Para simplificar el uso, se declaran algunas constantes:

```
export const EX_APP_ID = 'ui_example'
export const EX_APP_MENU_ENTRY_NAME = 'first_menu'
export const APP_API_PROXY_URL_PREFIX = '/apps/app_api/proxy'
export const APP_API_ROUTER_BASE = '/apps/app_api/embedded'
```

El arranque de la app Vue ([arranque de UI Example](https://github.com/nextcloud/ui_example/blob/main/src/bootstrap.js)) se modifica de la siguiente manera:

```
import Vue from 'vue'
import { translate, translatePlural } from '@nextcloud/l10n'
import { generateUrl } from '@nextcloud/router'
import { APP_API_PROXY_URL_PREFIX, EX_APP_ID } from './constants/AppAPI.js'
import { getCSPNonce } from '@nextcloud/auth'

Vue.prototype.t = translate
Vue.prototype.n = translatePlural
Vue.prototype.OC = window.OC
Vue.prototype.OCA = window.OCA

__webpack_public_path__ = generateUrl(`${APP_API_PROXY_URL_PREFIX}/${EX_APP_ID}/js/`) // eslint-disable-line
__webpack_nonce__ = getCSPNonce() // eslint-disable-line
```

#### Enrutamiento del frontend

La URL base del enrutamiento del frontend también se ajusta para cargarse mediante el proxy de AppAPI.
Por ejemplo, el router **vuex** tiene la siguiente configuración de URL base:

```
...
const router = new VueRouter({
    mode: 'history',
    base: generateUrl(`${APP_API_ROUTER_BASE}/${EX_APP_ID}/${EX_APP_MENU_ENTRY_NAME}`, ''), // setting base to AppAPI embedded URL
    linkActiveClass: 'active',
...
```

Lo mismo se aplica a las solicitudes que el frontend hace a la API del backend de la ExApp:

```
...
axios.get(generateUrl(`${APP_API_PROXY_URL_PREFIX}/${EX_APP_ID}/some_api_endpoint`))
...
```

(nc-dev-ex_app_translations)=
### Traducciones L10n

Para añadir compatibilidad con un lenguaje de programación en la extracción de cadenas de traducción con la herramienta de traducción de Nextcloud,
basta con añadirle las extensiones de archivo [en createPotFile](https://github.com/nextcloud/docker-ci/blob/master/translations/translationtool/src/translationtool.php#L69)
y, más abajo, ajustar los parámetros `--language` y `keyword`.

Actualmente solo Python se admite como lenguaje adicional en translationtool para ExApps.
Este es un ejemplo de translationtool ajustado para Python:

```
diff --git a/translations/translationtool/src/translationtool.php b/translations/translationtool/src/translationtool.php
index 42513563..8aa06618 100644
--- a/translations/translationtool/src/translationtool.php
+++ b/translations/translationtool/src/translationtool.php
@@ -67,7 +67,7 @@ public function createPotFile() {
        $this->createFakeFileForVueFiles();
        $this->createFakeFileForLocale();
        $translatableFiles = $this->findTranslatableFiles(
-           ['.php', '.js', '.jsx', '.mjs', '.html', '.ts', '.tsx'],
+           ['.php', '.js', '.jsx', '.mjs', '.html', '.ts', '.tsx', '.py'],
            ['.min.js']
        );

@@ -79,6 +79,8 @@ public function createPotFile() {
            $keywords = '';
            if (substr($entry, -4) === '.php') {
                $keywords = '--keyword=t --keyword=n:1,2';
+           } elseif (substr($entry, -3) === '.py') {
+               $keywords = '--keyword=_ --keyword=_n:1,2';
            } else {
                $keywords = '--keyword=t:2 --keyword=n:2,3';
            }
@@ -86,6 +88,8 @@ public function createPotFile() {
            $language = '--language=';
            if (substr($entry, -4) === '.php') {
                $language .= 'PHP';
+           } elseif (substr($entry, -3) === '.py') {
+               $language .= 'Python';
            } else {
                $language .= 'Javascript';
            }
```

donde se declaran los métodos que se usan en el código fuente para traducir cadenas.

Las traducciones de la ExApp se almacenan en el directorio `l10n`, dentro del directorio raíz del proyecto de la ExApp.
En el lado de Nextcloud, este debe seguir conteniendo los archivos de traducción igual que en las apps normales de Nextcloud (.js y .json).
Los archivos de traducción de la ExApp se copian al servidor de Nextcloud durante la instalación (y se eliminan al desinstalarla),
y pueden usarse para traducir las cadenas de la ExApp en el backend o en el frontend de la misma forma que en las apps PHP.

:::{note}
En una configuración de Nextcloud en clúster, las traducciones de la ExApp también deben copiarse a las demás instancias de Nextcloud,
si la carpeta de apps no se comparte entre ellas.
Esto se hace automáticamente solo en la instancia donde se realiza la instalación.
:::

Puede ser necesario convertir los archivos de traducción al formato que usa el lenguaje en cuestión.
Y esto puede hacerse con scripts bash sencillos, como [en nuestro ejemplo para Python](https://github.com/nextcloud/ui_example):

- [scripts/compile_po_to_mo.sh](https://github.com/nextcloud/ui_example/tree/main/scripts/compile_po_to_mo.sh): compila los archivos `.po` en archivos `.mo`. (necesario en caso de sincronización con Transifex: solo se proporcionan los archivos `.po` y `l10n/*js|json`)
- [scripts/copy_translations.sh](https://github.com/nextcloud/ui_example/tree/main/scripts/copy_translations.sh): en la ExApp de ejemplo en Python, transforma `translationfiles/<lang>/*.(po|mo)` en la estructura de carpetas de locale: `<locale_dir>/<lang>/LC_MESSAGES/*.(po|mo)`. Esto puede ajustarse a las necesidades de cada caso, según el lenguaje que se use.

:::{note}
La conversión de las traducciones también debe incluirse en el proceso de compilación del [Dockerfile](https://github.com/nextcloud/ui_example/blob/main/Dockerfile), para que las traducciones de la ExApp estén disponibles en la imagen Docker.
:::

### Makefile

Se recomienda usar el siguiente conjunto predeterminado de comandos:

- `help`: muestra la lista de comandos disponibles.
- `build-push-cpu`: compila la imagen Docker para CPU y la sube al registro de Docker.
- `build-push-cuda`: compila la imagen Docker para CUDA y la sube al registro de Docker.
- `build-push-rocm`: compila la imagen Docker para ROCm y la sube al registro de Docker.
- `run`: instala la ExApp para la última versión de Nextcloud mediante el comando `occ app_api:app:register`, como desde la interfaz de usuario.
- `register`: registra una ExApp que se ejecuta manualmente, usando el daemon de despliegue `manual_install`.
- `translation_templates`: ejecuta translationtool.phar para extraer las cadenas de traducción de las fuentes (frontend y backend).
- `convert_translations_nc`: convierte las traducciones a archivos con el formato de Nextcloud (json, js).
- `compile_po_to_mo`: compila los archivos `.po` en archivos `.mo` mediante el script `scripts/compile_po_to_mo.sh`.
- `copy_translations`: copia las traducciones a la ubicación necesaria según el lenguaje de programación del backend de la ExApp.

:::{note}
Estos Makefiles suelen escribirse para funcionar en el entorno de desarrollo [nextcloud-docker-dev](https://github.com/nextcloud/nextcloud-docker-dev).
:::

Para ver un ejemplo completo, se puede consultar nuestro [Makefile del ejemplo de servicio de terceros](https://github.com/cloud-py-api/visionatrix/blob/main/Makefile).
Este ejemplo también requiere tener instalado el programa `xmlstarlet`, para que el Makefile pueda detectar automáticamente la versión de la ExApp a partir del archivo info.xml.
````
