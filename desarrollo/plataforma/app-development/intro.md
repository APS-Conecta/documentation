---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Crear una app desde un esqueleto de la tienda de apps o contribuir a una existente desde apps-extra, activarla y conocer sus directorios."
---
# Introducción

## Resumen

Esta página explica cómo crear una app nueva a partir de un esqueleto generado en la tienda de apps o contribuir a una app existente desde la carpeta *apps-extra*, cómo activarla y qué contiene cada directorio de una app. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/app_development/intro.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Crear una app

Después de {nc-doc}`haber configurado el entorno de desarrollo <developer_manual/getting_started/devenv>`, cambiar al directorio de apps de Nextcloud:

```
cd /var/www/nextcloud/apps
```

Luego crear un esqueleto de app en la [tienda de apps](https://apps.nextcloud.com/developer/apps/generate). Esto todavía no publica nada en la tienda de apps; solo entrega una descarga.

### Editar una app existente

Como alternativa, si se quiere contribuir a una app existente en lugar de crear una nueva, primero {nc-doc}`configurar el entorno de desarrollo <developer_manual/getting_started/devenv>` y luego crear una carpeta *apps-extra* en el directorio raíz de Nextcloud:

```
cd /var/www/nextcloud/apps-extra
```

Después se puede configurar Nextcloud para que ejecute apps desde este directorio, cambiando la configuración del sistema *app_paths* en el *config.php*

```php
'apps_paths' => array (
    0 => array (
        'path' => '/var/www/html/apps',
        'url' => '/apps',
        'writable' => false,
    ),
    1 => array (
        'path' => '/var/www/html/apps-extra',
        'url' => '/apps-extra',
        'writable' => false,
    ),
),
```

Por último, clonar la app a la que se quiere contribuir dentro de la carpeta *apps-extra*. Por ejemplo:

> git clone <https://github.com/nextcloud/cookbook.git>

### Activar la app

Ahora la app se puede activar en la página de apps de Nextcloud.

### Arquitectura de la app

Ahora se han creado los siguientes directorios:

* **appinfo/**: contiene los metadatos y la configuración de la app
* **css/**: contiene el CSS
* **img/**: contiene iconos e imágenes
* **js/**: contiene los archivos JavaScript
* **lib/**: contiene los archivos de clases PHP de la app
* **src/**: contiene el código fuente de la app de vue.js
* **templates/**: contiene las plantillas
* **tests/**: contiene las pruebas
````
