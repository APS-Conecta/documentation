---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Agregar una entrada de navegación en appinfo/info.xml y los eventos de inicialización para cargar JavaScript y CSS solo en las páginas necesarias."
---
# Navegación y configuración previa a la app

## Resumen

Esta página explica cómo agregar una entrada de navegación de una app en {file}`appinfo/info.xml` y enumera los eventos de inicialización a los que una app puede reaccionar para cargar su JavaScript y su CSS solo donde hace falta. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/app_development/init.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Agregar una entrada de navegación

Las entradas de navegación de las apps se pueden crear agregando una sección de navegación al archivo {file}`appinfo/info.xml`, con el nombre, el orden y la ruta a la que debe enlazar la entrada de navegación. Para conocer los detalles del esquema XML, consultar la [documentación de la tienda de apps](https://nextcloudappstore.readthedocs.io/en/latest/developer.html#info-xml).

```xml
<navigation>
    <name>MyApp</name>
    <route>myapp.page.index</route>
    <order>0</order>
</navigation>
```

### Eventos de inicialización

A menudo las apps no necesitan cargar su JavaScript y su CSS en todas las páginas. Para ello se emiten varios eventos sobre los que una app puede actuar.

* `OCA\Files::loadAdditionalScripts` (cadena): se carga en la página de la lista de archivos
* `OCA\Files_Sharing::loadAdditionalScripts` (cadena): se carga en la página pública de recursos compartidos
* `OCA\Files_Sharing::loadAdditionalScripts::publicShareAuth` (cadena): se carga en la página de autenticación de recursos compartidos públicos
* `OCP\AppFramework\Http\TemplateResponse::EVENT_LOAD_ADDITIONAL_SCRIPTS` (constante): se carga cuando termina una respuesta de plantilla
* `OCP\AppFramework\Http\TemplateResponse::EVENT_LOAD_ADDITIONAL_SCRIPTS_LOGGEDIN` (constante): se carga cuando termina una respuesta de plantilla para un usuario con la sesión iniciada

Los listeners de estos eventos se pueden registrar en el {nc-ref}`código de arranque <Bootstrapping>` de la app. Consultar la {nc-ref}`documentación de eventos <Events>` para conocer más detalles sobre el despachador de eventos y los eventos disponibles.
````
