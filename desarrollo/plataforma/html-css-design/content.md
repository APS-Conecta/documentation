---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Estructura HTML estándar en la que se inyecta una app (el div #content) y reglas sobre cabecera, desplazamiento, navegación y lista de contenido."
---
# Contenido principal

## Resumen

Esta página muestra la estructura HTML estándar desde la versión 14, en la que la app se inyecta dentro del div `#content`, y las reglas que la acompañan sobre la cabecera, el desplazamiento, la navegación y la lista de contenido en el móvil. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/html_css_design/content.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Desde la versión 14, la estructura se estandarizó.

La aplicación se inyectará directamente en el div `#content`.

```html
<header>
    <div class="header-left">
        <!-- apps menu -->
    </div>
    <div class="header-right">
        <!-- search - contactsmenu - settingsmenu - ... -->
    </div>
</header>
<div id="content" class="app-YOURAPPID">
    <div id="app-navigation" class="">
        <div class="app-navigation-new">
            <!-- app 'new' button -->
        </div>
        <ul id="usergrouplist">
            <!-- app navigation -->
        </ul>
        <div id="app-settings">
            <!-- app settings -->
        </div>
    </div>
    <div id="app-content">
        <div id="app-navigation-toggle" class="icon-menu"></div>
        <!-- app-content-wrapper is optional, only use if app-content-list  -->
        <div id="app-content-wrapper">
            <div class="app-content-list">
                <!-- app list -->
            </div>
            <div class="app-content-details"></div>
            <!-- app content -->
        </div>
    </div>
    <div id="app-sidebar"></div>
</div>
```

### Reglas e información

- No se puede ni se necesita modificar la cabecera ni los elementos exteriores de la aplicación.
- Todo el body debe desplazarse para ser compatible con las vistas móviles. Por eso, la barra lateral y la app-navigation son fixed/sticky.
- Salvo que la aplicación no requiera un área desplazable, no usar ninguna propiedad overflow en los elementos padre del contenido.
- El `app-navigation-toggle` se inyecta automáticamente. Mostrar u ocultar la navegación se gestiona automáticamente.
- No usar más `#content-wrapper`
- Si la app se inyecta reemplazando el elemento #content, asegurarse de conservar el id `#content`
- Si se usa el estándar `app-content-list`, el div `app-content-details` se ocultará en el modo móvil (pantalla completa).
  Habrá que añadir la clase `showdetails` a `app-content-list` para mostrar el contenido principal.
  En la vista móvil, toda la sección de lista/detalles (según cuál se muestre) desplazará el body
````
