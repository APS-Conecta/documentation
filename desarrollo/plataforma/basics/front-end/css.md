---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo incluir los archivos CSS (y SCSS) de una app en sus plantillas y cómo importar Web Components desde la carpeta component/."
---
# CSS

## Resumen

Esta página explica dónde se ubican los archivos CSS de una app, cómo se incluyen en una plantilla, el soporte nativo de SCSS y cómo importar Web Components. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/front-end/css.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los archivos CSS se ubican en la carpeta **css/** y deben incluirse en la plantilla:

```php
<?php
// include one file
style('myapp', 'style');  // adds css/style.(s)css

// include multiple files for the same app
style('myapp', array('style', 'navigation'));  // adds css/style.(s)css, css/navigation.(s)css

// include vendor file (also allows array syntax)
vendor_style('myapp', 'style');  // adds vendor/style.(s)css
```

:::{note}
`SCSS` se admite de forma nativa.
Los archivos se pueden migrar con solo cambiar el nombre de los archivos `.css` a `.scss`.
El servidor los compilará, los almacenará en caché y los servirá automáticamente.
La prioridad la tiene el archivo scss. Así, tener dos archivos con el mismo nombre y extensión `scss` y `css`
garantiza la retrocompatibilidad con las versiones <12, ya que el servidor ignorará los archivos scss.
:::

Los Web Components van en la carpeta **component/** y se pueden importar así:

```php
<?php
// include one file
component('myapp', 'tabs');  // adds component/tabs.html

// include multiple files for the same app
component('myapp', array('tabs', 'forms'));  // adds component/tabs.html, component/forms.html
```

:::{note}
Hay que tener en cuenta que los Web Components todavía son muy nuevos y que [es posible que haya que agregar polyfills](https://www.webcomponents.org/polyfills/).
:::
````
