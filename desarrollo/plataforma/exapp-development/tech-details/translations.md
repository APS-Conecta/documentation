---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo se traducen las ExApps: archivos l10n del front-end y del back-end, sincronización con Transifex e instalación de traducciones manual o con Docker."
---
(nc-dev-ex_app_translations_page)=
# Traducciones

## Resumen

Esta página explica cómo funcionan las traducciones de las ExApps, igual que en las apps PHP salvo algunos ajustes: los archivos l10n del front-end y del back-end, la sincronización con Transifex, cómo llegan las traducciones al servidor en los tipos `manual-install` y `docker-install`, y cómo ampliar el translationtool. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/Translations.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Las traducciones de las ExApps funcionan {nc-ref}`de la misma manera que en las apps PHP <Translations>`, con algunos ajustes y diferencias.

En resumen, basta con proporcionar para la app los archivos `l10n/<lang>.js` (para el front-end) y `l10n/<lang>.json` (para el back-end).

### Front-end

Para la parte del front-end, AppAPI inyectará el script `l10n/<lang>.js` de la configuración regional del usuario actual, de modo que el acceso a las cadenas traducidas se mantiene igual que antes en las apps PHP.

:::{note}
Los archivos l10n de la ExApp se incluyen solo en las páginas de interfaz de la ExApp ({nc-ref}`Menú superior <top_menu_section>`), en Archivos (para {nc-ref}`FileAction <file_actions_menu_section>`) y en Ajustes (para {nc-ref}`DeclarativeSettings <exapp_declarative_settings_section>`).
:::

### Back-end

En la parte del back-end de la ExApp, que puede escribirse en distintos lenguajes de programación, **corresponde a quien desarrolla decidir** cómo manejar los archivos de traducciones.
Hay un repositorio de ejemplo con traducciones: [ejemplo de interfaz con traducciones](https://github.com/nextcloud/ui_example).

Hay dos funciones de Python que [translationtool](https://github.com/nextcloud/docker-ci/tree/master/translations/translationtool) usa para extraer las cadenas de traducción: `_('singular string')` y `_n('singular string', 'plural string', count)`.

### Traducciones manuales

Las instrucciones de las traducciones manuales se encuentran {nc-ref}`aquí <ex_app_translations>`.

#### Sincronización con Transifex

Para la sincronización automática con Transifex solo se incluyen archivos `.po`.
Luego se pueden compilar a archivos `.mo` con el script `scripts/compile_po_to_mo.sh` de [ui_example](https://github.com/nextcloud/ui_example/tree/main/scripts/compile_po_to_mo.sh).

### Instalación manual

En el tipo `manual-install`, quien administra tendrá que extraer manualmente la carpeta `l10n` de la ExApp al [directorio de apps con permisos de escritura](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/config_sample_php_parameters.html#apps-paths) del servidor
(p. ej., `/path/to/apps-writable/<appid>/l10n/*.(js|json)`).
Esto permitirá que el servidor acceda a las cadenas de la ExApp con sus traducciones.

:::{note}
Solo la carpeta `l10n` debe estar presente en el lado del servidor; `appinfo/info.xml` podría hacer que el servidor la detecte por error como carpeta de una app PHP.
:::

### Instalación con Docker

En el tipo `docker-install`, AppAPI extraerá automáticamente al servidor la carpeta `l10n` desde el archivo de publicación de la ExApp durante la instalación.

### Herramienta de traducción

Para añadir compatibilidad con el lenguaje que se use al [translationtool de Nextcloud](https://github.com/nextcloud/docker-ci/tree/master/translations/translationtool),
se puede crear un issue en el repositorio [nextcloud/docker-ci](https://github.com/nextcloud/docker-ci)
o abrir un pull request con los cambios realizados en la función `createPotFile` para extraer y convertir las cadenas de traducción.
````
