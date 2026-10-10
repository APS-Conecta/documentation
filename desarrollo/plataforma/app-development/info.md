---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Referencia de appinfo/info.xml: ejemplos mínimo y completo, cómo se valida y usa cada etiqueta, límites de longitud, elementos obsoletos y changelog."
---
(nc-dev-app metadata)=
# Metadatos de la app

## Resumen

Esta página es la referencia del archivo {file}`appinfo/info.xml`, que contiene los metadatos de una app: un ejemplo mínimo y uno completo, cómo se valida y se usa cada etiqueta, los límites de longitud, los elementos obsoletos o internos y cómo una app ofrece su registro de cambios. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/app_development/info.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El archivo {file}`appinfo/info.xml` contiene metadatos sobre la app. Hay documentación detallada en la [documentación de la tienda de apps](https://nextcloudappstore.readthedocs.io/en/latest/developer.html#info-xml).

El info.xml se valida con un esquema XML que se puede consultar [en línea](https://apps.nextcloud.com/schema/apps/info.xsd).

Un **info.xml** mínimo válido se vería así:

**Archivo {file}`appinfo/info.xml`**:

```xml
<?xml version="1.0"?>
<info xmlns:xsi= "http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="https://apps.nextcloud.com/schema/apps/info.xsd">
    <id>news</id>
    <name>News</name>
    <summary>An RSS/Atom feed reader</summary>
    <description>An RSS/Atom feed reader</description>
    <version>8.8.2</version>
    <licence>AGPL-3.0-or-later</licence>
    <author>Bernhard Posselt</author>
    <category>multimedia</category>
    <bugs>https://github.com/nextcloud/news/issues</bugs>
    <dependencies>
        <nextcloud min-version="31"/>
    </dependencies>
</info>
```

Un ejemplo completo se vería así (debe estar codificado en utf-8):

**Archivo {file}`appinfo/info.xml`**:

```xml
<?xml version="1.0"?>
<info xmlns:xsi= "http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="https://apps.nextcloud.com/schema/apps/info.xsd">
    <id>news</id>
    <name lang="de">Nachrichten</name>
    <name>News</name>
    <summary lang="en">An RSS/Atom feed reader</summary>
    <description lang="en"># Description\nAn RSS/Atom feed reader</description>
    <description lang="de"><![CDATA[# Beschreibung\nEine Nachrichten App, welche mit [RSS/Atom](https://en.wikipedia.org/wiki/RSS) umgehen kann]]></description>
    <version>8.8.2</version>
    <licence>AGPL-3.0-or-later</licence>
    <author mail="mail@provider.com" homepage="http://example.com">Bernhard Posselt</author>
    <author>Alessandro Cosentino</author>
    <author>Jan-Christoph Borchardt</author>
    <documentation>
        <user>https://github.com/nextcloud/news/wiki#user-documentation</user>
        <admin>https://github.com/nextcloud/news#readme</admin>
        <developer>https://github.com/nextcloud/news/wiki#developer-documentation</developer>
    </documentation>
    <category>multimedia</category>
    <category>tools</category>
    <website>https://github.com/nextcloud/news</website>
    <discussion>https://your.forum.com</discussion>
    <bugs>https://github.com/nextcloud/news/issues</bugs>
    <repository>https://github.com/nextcloud/news</repository>
    <screenshot small-thumbnail="https://example.com/1-small.png">https://example.com/1.png</screenshot>
    <screenshot>https://example.com/2.jpg</screenshot>
    <dependencies>
        <php min-version="5.6" min-int-size="64"/>
        <database min-version="9.4">pgsql</database>
        <database>sqlite</database>
        <database min-version="5.5">mysql</database>
        <command>grep</command>
        <command>ls</command>
        <lib min-version="2.7.8">libxml</lib>
        <lib>curl</lib>
        <lib>SimpleXML</lib>
        <lib>iconv</lib>
        <nextcloud min-version="31" max-version="32"/>
    </dependencies>
    <background-jobs>
        <job>OCA\DAV\CardDAV\Sync\SyncJob</job>
    </background-jobs>
    <repair-steps>
        <pre-migration>
            <step>OCA\DAV\Migration\Classification</step>
        </pre-migration>
        <post-migration>
            <step>OCA\DAV\Migration\Classification</step>
        </post-migration>
        <live-migration>
            <step>OCA\DAV\Migration\GenerateBirthdays</step>
        </live-migration>
        <install>
            <step>OCA\DAV\Migration\GenerateBirthdays</step>
        </install>
        <uninstall>
            <step>OCA\DAV\Migration\GenerateBirthdays</step>
        </uninstall>
    </repair-steps>
    <two-factor-providers>
        <provider>OCA\AuthF\TwoFactor\Provider</provider>
    </two-factor-providers>
    <commands>
        <command>A\Php\Class</command>
    </commands>
    <settings>
        <admin>OCA\Theming\Settings\Admin</admin>
        <admin-section>OCA\Theming\Settings\Section</admin-section>
    </settings>
    <activity>
        <settings>
            <setting>OCA\Files\Activity\Settings\FavoriteAction</setting>
            <setting>OCA\Files\Activity\Settings\FileChanged</setting>
            <setting>OCA\Files\Activity\Settings\FileCreated</setting>
            <setting>OCA\Files\Activity\Settings\FileDeleted</setting>
            <setting>OCA\Files\Activity\Settings\FileFavorite</setting>
            <setting>OCA\Files\Activity\Settings\FileRestored</setting>
        </settings>

        <filters>
            <filter>OCA\Files\Activity\Filter\FileChanges</filter>
            <filter>OCA\Files\Activity\Filter\Favorites</filter>
        </filters>

        <providers>
            <provider>OCA\Files\Activity\FavoriteProvider</provider>
            <provider>OCA\Files\Activity\Provider</provider>
        </providers>
    </activity>
    <navigations>
        <navigation role="admin">
            <id>files</id>
            <name>Files</name>
            <route>files.view.index</route>
            <order>0</order>
            <icon>app.svg</icon>
            <type>link</type>
        </navigation>
    </navigations>
    <collaboration>
        <plugins>
            <plugin type="collaborator-search" share-type="SHARE_TYPE_CIRCLE">OCA\Circles\Collaboration\v1\CollaboratorSearchPlugin</plugin>
        </plugins>
    </collaboration>
</info>
```

Las siguientes etiquetas se validan y se usan de la siguiente manera:

- id:
  * obligatoria
  * solo debe contener caracteres ASCII en minúscula y guion bajo
  * debe coincidir con la primera carpeta del archivo comprimido
  * se usará para identificar la app
- name:
  * obligatoria
  * debe aparecer al menos una vez con **lang="en"** o sin atributo lang
  * se puede traducir usando varios elementos con distintos valores del atributo **lang**; el código de idioma debe indicarse en el atributo **lang**
  * se mostrará en la página de detalle de la app
- summary:
  * opcional
  * si no se indica, se usará el texto del elemento description
  * debe aparecer al menos una vez con **lang="en"** o sin atributo lang
  * se puede traducir usando varios elementos con distintos valores del atributo **lang**; el código de idioma debe indicarse en el atributo **lang**
  * se mostrará en la página de la lista de apps como descripción corta
- description:
  * obligatoria
  * debe aparecer al menos una vez con **lang="en"** o sin atributo lang
  * puede contener Markdown
  * se puede traducir usando varios elementos con distintos valores del atributo **lang**; el código de idioma debe indicarse en el atributo **lang**
  * se mostrará en la página de detalle de la app
- version:
  * obligatoria
  * debe ser una [versión semántica](http://semver.org/) sin metadatos de compilación, p. ej., 9.0.1 o 9.1.0-alpha.1
  * {nc-ref}`más información sobre el versionado de apps <app-versioning>`
- licence:
  * obligatoria
  * puede aparecer varias veces con distintas licencias
  * debe contener una de las siguientes licencias (para apps destinadas a la v31 o superior; consultar la [lista de licencias SPDX](https://spdx.org/licenses/) para conocer los detalles):

    * **AGPL-3.0-only**
    * **AGPL-3.0-or-later**
    * **Apache-2.0**
    * **GPL-3.0-only**
    * **GPL-3.0-or-later**
    * **MIT**
    * **MPL-2.0**

  * (obsoleto, para apps destinadas a la v30 o inferior) también se usan los siguientes alias abreviados:

    * **agpl** (AGPL-3.0)
    * **apache** (Apache-2.0)
    * **gpl3** (GPL-3.0)
    * **mit** (MIT)
    * **mpl** (MPL-2.0)

- author:
  * obligatoria
  * puede aparecer varias veces con distintos autores
  * puede contener un atributo **mail**, que debe ser un correo electrónico
  * puede contener un **homepage**, que debe ser una URL
  * (todavía) no se mostrará en la App Store
  * se ofrecerá mediante la API REST
- documentation/user:
  * opcional
  * debe contener una URL a la documentación de usuario
  * se mostrará en la página de detalle de la app
- documentation/admin:
  * opcional
  * debe contener una URL a la documentación de administración
  * se mostrará en la página de detalle de la app
- documentation/developer:
  * opcional
  * debe contener una URL a la documentación para desarrolladores
  * se mostrará en la página de detalle de la app
- category:
  * opcional
  * si no se indica, se usará la categoría **tools**
  * debe contener uno de los siguientes valores:

    * **customization**
    * **files**
    * **games**
    * **integration**
    * **monitoring**
    * **multimedia**
    * **office**
    * **organization**
    * **security**
    * **social**
    * **tools**

  * las categorías antiguas se migran:

    * **auth** se convertirá en **security**

  * puede aparecer más de una vez con distintas categorías
- website:
  * opcional
  * debe contener una URL a la página principal del proyecto
  * se mostrará en la página de detalle de la app
- discussion:
  * opcional
  * debe contener una URL a la página de discusión o al foro del proyecto
  * se mostrará en la página de detalle de la app como el botón «ask question or discuss»
  * si no está, se usará de forma predeterminada nuestro foro en <https://help.nextcloud.com/>
- bugs:
  * obligatoria
  * debe contener una URL al gestor de incidencias del proyecto
  * se mostrará en la página de detalle de la app
- repository:
  * opcional
  * debe contener una URL al repositorio del proyecto
  * puede contener un atributo **type**; los valores permitidos son **git**, **mercurial**, **subversion** y **bzr**, y el predeterminado es **git**
  * actualmente no se usa
- screenshot:
  * opcional
  * debe contener una URL HTTPS a una imagen
  * puede contener un atributo **small-thumbnail**, que debe contener una url https a una imagen. Esta imagen se usará como vista previa pequeña (p. ej., en la vista general de la lista de apps). Conviene que sea pequeña para que se muestre rápido
  * se mostrará en la lista de apps y en la página de detalle, en el orden indicado
- dependencies/php:
  * opcional
  * puede contener un atributo **min-version** (como máximo 3 dígitos separados por puntos)
  * puede contener un atributo **max-version** (como máximo 3 dígitos separados por puntos)
  * puede contener un atributo **min-int-size**; los valores válidos son 32 o 64
  * se mostrará en la página de versiones de la app
- dependencies/database:
  * opcional
  * debe contener como texto el nombre de la base de datos; los valores válidos son **sqlite**, **pgsql** y **mysql**
  * puede aparecer varias veces con distintas bases de datos
  * puede contener un atributo **min-version** (como máximo 3 dígitos separados por puntos)
  * puede contener un atributo **max-version** (como máximo 3 dígitos separados por puntos)
  * se mostrará en la página de versiones de la app
- dependencies/command:
  * opcional
  * debe contener como valor de texto un comando de linux
  * puede aparecer varias veces con distintos comandos
  * se mostrará en la página de versiones de la app
- dependencies/lib:
  * opcional
  * se mostrará en la página de versiones de la app
  * debe contener una extensión de php requerida
  * puede aparecer varias veces con distintas extensiones de php
  * puede contener un atributo **min-version** (como máximo 3 dígitos separados por puntos)
  * puede contener un atributo **max-version** (como máximo 3 dígitos separados por puntos)
- dependencies/nextcloud:
  * obligatoria
  * debe contener un atributo **min-version** (como máximo 3 dígitos separados por puntos)
  * debe contener un atributo **max-version** (como máximo 3 dígitos separados por puntos)

:::{note}
Las dependencias *dependencies/php*, *dependencies/database* y *dependencies/lib* se comprueban en el momento de la instalación (no en el de la actualización), por lo que las aplicaciones deben ceñirse a las dependencias que admite una versión mayor de Nextcloud en el momento en que una app publica la compatibilidad con esa versión; es decir, la app debe admitir el mismo rango de versiones de PHP que admite la versión de Nextcloud compatible.
:::

- background-jobs/job:
  * opcional
  * debe contener una clase php que se ejecuta como trabajo en segundo plano
  * no se usará, solo se valida
- repair-steps/pre-migration/step:
  * opcional
  * debe contener una clase php que se ejecuta antes de ejecutar las migraciones de la base de datos
  * no se usará, solo se valida
- repair-steps/post-migration/step:
  * opcional
  * debe contener una clase php que se ejecuta después de ejecutar las migraciones de la base de datos
  * no se usará, solo se valida
- repair-steps/live-migration/step:
  * opcional
  * debe contener una clase php que se ejecuta después de ejecutar los trabajos posteriores a la migración
  * no se usará, solo se valida
- repair-steps/install/step:
  * opcional
  * debe contener una clase php que se ejecuta después de instalar la app
  * no se usará, solo se valida
- repair-steps/uninstall/step:
  * opcional
  * debe contener una clase php que se ejecuta después de desinstalar la app
  * no se usará, solo se valida
- two-factor-providers/provider:
  * opcional
  * debe contener una clase php que se registra como proveedor de autenticación de dos factores
  * no se usará, solo se valida
- commands/command:
  * opcional
  * debe contener una clase php que se registra como comando de occ
  * no se usará, solo se valida
- activity/settings/setting:
  * opcional
  * debe contener una clase php que implementa OCP\Activity\ISetting y se usa para añadir elementos de interfaz de ajustes adicionales a la app de actividad
- activity/filters/filter:
  * opcional
  * debe contener una clase php que implementa OCP\Activity\IFilter y se usa para añadir filtros adicionales a la app de actividad
- activity/providers/provider:
  * opcional
  * debe contener una clase php que implementa OCP\Activity\IProvider y se usa para reaccionar a eventos de la app de actividad
- settings/admin:
  * opcional
  * debe contener una clase php que implementa OCP\Settings\ISettings y devuelve el formulario que se muestra en el área de configuraciones de administración
- settings/admin-section:
  * opcional
  * debe contener una clase php que implementa OCP\Settings\ISection y devuelve los datos para mostrar entradas de navegación en el área de configuraciones de administración
- settings/personal:
  * opcional
  * debe contener una clase php que implementa OCP\Settings\ISettings y devuelve el formulario que se muestra en el área de ajustes personales
- settings/personal-section:
  * opcional
  * debe contener una clase php que implementa OCP\Settings\ISection y devuelve los datos para mostrar entradas de navegación en el área de ajustes personales
- settings/admin-delegation:
  * opcional
  * debe contener una clase php que implementa OCP\Settings\ISettings y no tiene interfaz (en los ajustes), porque solo está pensada para usarse en la delegación de administración
- settings/admin-delegation-section:
  * opcional
  * debe contener una clase php que implementa OCP\Settings\ISection y que contiene clases de ajustes solo de delegación, como se definen arriba
- navigations:
  * opcional
  * debe contener al menos un elemento navigation
- navigations/navigation:
  * obligatoria
  * debe contener un elemento name y uno route
  * indica una entrada de navegación
  * role indica la visibilidad: all significa que todos pueden verla y admin significa que solo un administrador puede ver la entrada de navegación; el valor predeterminado es all
- navigations/navigation/id:
  * opcional
  * el id de la app
  * también se pueden crear entradas para otras apps indicando un id distinto del de la propia app
- navigations/navigation/name:
  * obligatoria
  * se mostrará debajo del icono de la entrada de navegación
  * lo traducirán las herramientas de traducción predeterminadas
- navigations/navigation/route:
  * obligatoria
  * nombre de la ruta que se usará para generar el enlace
- navigations/navigation/icon:
  * opcional
  * nombre del icono, que se busca en la carpeta **img/** de la app
  * el valor predeterminado es app.svg
- navigations/navigation/order:
  * opcional
  * se usa para ordenar las entradas de navegación
  * un número de orden mayor significa que la entrada se ordenará más abajo
- navigations/navigation/type:
  * opcional
  * puede ser link o settings
  * link significa que la entrada se añade al menú de apps predeterminado
  * settings significa que la entrada se añade al menú del lado derecho, que también contiene las entradas personal, admin, users, help y logout
- collaboration:
  * opcional
  * puede contener plugins para la búsqueda de colaboración (p. ej., para alimentar el diálogo de compartir)
- collaboration/plugins:
  * opcional
  * debe contener al menos un plugin
- collaboration/plugins/plugin:
  * obligatoria
  * el nombre de la clase PHP del plugin
  * debe contener el atributo **type** (actualmente solo *collaboration-search*). La clase debe implementar OCP\Collaboration\Collaborators\ISearchPlugin.
  * debe contener el atributo **share-type**, según las constantes concretas de \OCP\Share

Se aplican las siguientes longitudes máximas de caracteres:

* Todas las cadenas de descripción son campos de texto de la base de datos y, por lo tanto, no tienen límite de tamaño
* Todas las demás cadenas tienen un máximo de 256 caracteres

Los siguientes elementos están obsoletos o son solo para uso interno, y harán fallar la validación si están presentes:

* **standalone**
* **default_enable**
* **shipped**
* **public**
* **remote**
* **requiremin**
* **requiremax**

(nc-dev-app changelog)=
### Registro de cambios

Las apps pueden ofrecer un registro de cambios. Debe escribirse siguiendo [keep a changelog](https://keepachangelog.com/).

Si la app incluye un archivo `CHANGELOG.md` en la raíz del proyecto, ese archivo se usará para mostrar los cambios de la versión publicada en la tienda de apps y, a quienes administran, en los ajustes de las apps.

Además, desde Nextcloud 29, si la app `updatenotification` está activada, las apps también pueden ofrecer un registro de cambios para los usuarios.
La app avisará a los usuarios después de la actualización de la app si hay disponible un `CHANGELOG.language.md` (donde `language` es el código de idioma de ese usuario) o un `CHANGELOG.en.md` de respaldo.
````
