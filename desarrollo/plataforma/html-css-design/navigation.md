---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Barra lateral de navegación de una app: botón de acción primaria, menú de navegación con sus utilidades y tipos de entrada, y área de ajustes."
---
# Introducción

## Resumen

Esta página describe la barra lateral de navegación de una app: el botón de acción primaria, el menú de navegación con sus utilidades (menú, contador y botones) y sus tipos de entrada, y el área de ajustes, con el marcado y las reglas de cada parte. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/html_css_design/navigation.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La sección de navegación de cualquier app de Nextcloud es la barra lateral izquierda.
Básicamente se compone de

- un botón de acción primaria
- un menú
- un área de ajustes

El botón de acción primaria y el área de ajustes son opcionales.

### Botón Nuevo

#### Introducción

Un botón de acción primaria es simplemente un botón estilizado situado encima de la parte de navegación de la app.
El objetivo es lograr homogeneidad de diseño en todas las apps que usan este botón.

#### Disposición básica

```html
<div id="app-navigation">
    <div class="app-navigation-new">
        <button type="button" class="icon-add">
            Add user
        </button>
    </div>

    <!-- Your navigation here -->
    <!-- Your settings here -->

</div>
```

#### Reglas

- Mantenerlo simple: no usar textos demasiado complicados en este botón.
- Evitar frases de más de una línea.
- No modificar el estilo de este botón.
- Aquí solo se permite **un** botón.

(nc-dev-appnavigation)=
### Menú de navegación de la app

#### Introducción

El menú de navegación principal representa la navegación principal de la app.

Debe ser:

- Organizado
- Simple
- Adaptable

Nextcloud ofrece una forma muy organizada de construir menús.
Se implementaron varias funciones esenciales y se ofrece una manera fácil de usarlas.

#### Disposición básica

```html
<div id="app-navigation">

    <!-- Your primary action button here -->

    <ul>
        <li><a href="#">First level entry</a></li>
        <li>
            <a href="#">First level container</a>
            <ul>
                <li><a href="#">Second level entry</a></li>
                <li><a href="#">Second level entry</a></li>
            </ul>
        </li>
    </ul>

    <!-- Your settings here -->

</div>
```

#### Reglas básicas

- **No** se puede cambiar el padding predeterminado de los elementos de navegación.
- Se recomienda añadir iconos en cada elemento de primer nivel de la navegación, por accesibilidad.
- **No** sobrescribir la estructura y/o el CSS predeterminados. Todo se ha ajustado con cuidado.

#### Utilidades: menú, contador y botones

Cada entrada puede tener un contador y/o un botón para la interacción del usuario.

- El fragmento `app-navigation-entry-utils` debe colocarse justo al lado del enlace principal de la entrada.
- En la sección de utilidades se permiten **dos** elementos como máximo. Puede haber:
  - Dos {nc-ref}`botones <navigation_buttons>`
  - Un {nc-ref}`botón <navigation_buttons>` y un {nc-ref}`botón <navigation_counter>`
- **No** puede haber más de dos botones; si se necesitan más, hay que añadir un menú.
- El orden del botón y del contador **no** es intercambiable. Hay que poner el contador antes del menú.

```html
<div class="app-navigation-entry-utils">
    <ul>
        <li class="app-navigation-entry-utils-counter">1</li>
        <li class="app-navigation-entry-utils-menu-button">
            <button></button>
        </li>
    </ul>
</div>
```

(nc-dev-navigation_menu)=
##### Menú

Si se necesita añadir algunas interacciones a la entrada, se puede poner todo en un menú emergente.
El menú debe colocarse después de `app-navigation-entry-utils`.

Para las reglas generales y/o la disposición, se puede consultar la {nc-ref}`sección dedicada al menú emergente <popovermenu>`.

```html
<div class="app-navigation-entry-menu">
    <ul>
        <li>
            <a href="#">
                <span class="icon-add"></span>
                <span>Add</span>
            </a>
        </li>
        <li>
            <a href="#">
                <span class="icon-rename"></span>
                <span>Edit</span>
            </a>
        </li>
        <li>
            <a href="#">
                <span class="icon-delete"></span>
                <span>Remove</span>
            </a>
        </li>
    </ul>
</div>
```

El menú está oculto de forma predeterminada y hay que activarlo añadiendo la clase `open` al div `app-navigation-entry-menu`.
En el caso de AngularJS, puede añadirse la siguiente pequeña directiva para gestionar de entrada toda la lógica de visualización y de clics:

```js
app.run(function ($document, $rootScope) {
    'use strict';
    $document.click(function (event) {
        $rootScope.$broadcast('documentClicked', event);
    });
});

app.directive('appNavigationEntryUtils', function () {
    'use strict';
    return {
        restrict: 'C',
        link: function (scope, elm) {
            var menu = elm.siblings('.app-navigation-entry-menu');
            var button = $(elm)
                .find('.app-navigation-entry-utils-menu-button button');

            button.click(function () {
                menu.toggleClass('open');
            });

            scope.$on('documentClicked', function (scope, event) {
                if (event.target !== button[0]) {
                    menu.removeClass('open');
                }
            });
        }
    };
});
```

(nc-dev-navigation_counter)=
##### Contador

Si se necesita añadir un contador a la entrada del menú, basta con usar esta estructura.
No cambiar la alineación del texto. Si se está usando

```html
<li class="app-navigation-entry-utils-counter">1</li>
```

El contador debe limitarse a 999 y pasar a 999+ si se da cualquier número mayor. Si se usa AngularJS, puede usarse el siguiente filtro para obtener el comportamiento correcto:

```js
app.filter('counterFormatter', function () {
    'use strict';
    return function (count) {
        if (count > 999) {
            return '999+';
        }
        return count;
    };
});
```

Se usa así:

```html
<li class="app-navigation-entry-utils-counter">{{ count | counterFormatter }}</li>
```

###### Contador destacado

El contador también puede destacarse para atraer la atención, p. ej., para mensajes de chat no leídos

```html
<li class="app-navigation-entry-utils-counter highlighted"><span>99+</span></li>
```

(nc-dev-navigation_buttons)=
##### Botones

Del mismo modo que se muestra el botón del icono de tres puntos del menú, se permite usar hasta 2 botones en una sola entrada.

- La clase del icono va directamente en el elemento `button`.
- Si no se define ninguna clase, se usará de forma predeterminada el icono de tres puntos

```html
<div class="app-navigation-entry-utils">
    <ul>
        <li class="app-navigation-entry-utils-menu-button">
            <button class="icon-edit"></button>
        </li>
        <li class="app-navigation-entry-utils-menu-button">
            <button class="icon-delete"></button>
        </li>
    </ul>
</div>
```

#### Arrastrar y soltar

La clase que debe aplicarse a un elemento **li** de primer nivel que aloja o puede alojar un segundo nivel es **drag-and-drop**.
Esto hace que la entrada sobre la que se pasa el cursor se desplace hacia abajo, lo que da una indicación visual de que puede aceptar el elemento arrastrado.
En el caso de la funcionalidad droppable de jQuery UI, la opción **hoverClass** debe establecerse en la clase **drag-and-drop**.

```html
<div id="app-navigation">
    <ul>
        <li><a href="#">First level entry</a></li>
        <li class="drag-and-drop">
            <a href="#" class="icon-folder">Folder name</a>
            <ul>
                <li><a href="#">Folder contents</a></li>
                <li><a href="#">Folder contents</a></li>
            </ul>
        </li>
    </ul>
</div>
```

#### Entrada plegable

De forma predeterminada, se muestran todas las subentradas.
Este comportamiento puede cambiarse creando un menú plegable.
Así, el menú quedará oculto y se añadirá una flecha delante de él (que sustituye al icono, si lo hay).

La apertura del menú se activa y se anima mediante la clase `open` en el `li` principal.

- **No** puede haber un menú plegable en un subelemento; solo puede existir en un elemento de primer nivel.
- Si se quiere, se puede establecer la clase open de forma predeterminada.
- **No** usar el menú plegable si el elemento no tiene subelementos.
- **Sigue** siendo necesario usar JS para gestionar el evento de clic.

:::{important}
- Si el enlace de primer nivel solo se usa como encabezado, hay que usar el `a` **entero** para alternar la clase `open`.
- Si el enlace de primer nivel se usa para redirigir al usuario o para activar otra cosa, **hay que** añadir el botón de plegado y usarlo como disparador para alternar la clase `open`.
:::

```html
<li class="collapsible open">

    <!-- This is optional -->
    <button class="collapse"></button>

    <a href="#" class="icon-folder">Folder collapsed menu</a>
    <ul>
        <li><a href="#">Simple entry</a></li>
        <li><a href="#">Simple entry</a></li>
        <li><a href="#">Simple entry</a></li>
        <li>
            <a class="icon-folder" href="#">Simple folder</a>
        </li>
    </ul>
</li>
```

#### Viñeta de la entrada

Cada entrada puede tener un marcador de color delante.
Se le llama *viñeta*.

- **No** se puede combinar un icono con una viñeta.
- Hay que usar el CSS para definir el color de la viñeta.

```html
<li>
    <div class="app-navigation-entry-bullet"></div>
    <a href="#">Entry with bullet</a>
</li>
```

#### Entrada de deshacer

- Las entradas de deshacer pueden usarse en cualquier nivel.
- Cuando se elimina una entrada, usar la habitual **respuesta con 7 segundos de retardo** antes de la eliminación definitiva.
- Usar la frase *Deleted XXXX* como mensaje de respuesta.
- Hay que usar la clase `deleted` para activar la animación que oculta/muestra la entrada de deshacer.

```html
<li class="deleted">
    <a href="#" class="hidden">Important entry</a>
    <div class="app-navigation-entry-utils">
        <ul>
            <li class="app-navigation-entry-utils-menu-button">
                <button class="icon-delete"></button>
            </li>
        </ul>
    </div>
    <div class="app-navigation-entry-deleted">
        <div class="app-navigation-entry-deleted-description">Deleted important entry</div>
        <button class="app-navigation-entry-deleted-button icon-history" title="Undo"></button>
    </div>
</li>
```

#### Entrada editable

- Las entradas editables pueden usarse en cualquier nivel.
- Se puede sustituir el `form` por un `div` si se quiere hacer la petición con JS.
- Hay que usar la clase `editing` para activar la animación que oculta/muestra el campo de entrada.
- Solo se permite usar un input de tipo submit. **Debe** ser el botón de validación.
- El input **debe** tener el mismo valor que el texto del enlace de la entrada.

```html
<li class="editing">
    <a href="#" class="icon-folder">Folder entry</a>
    <div class="app-navigation-entry-utils">
        <ul>
            <li class="app-navigation-entry-utils-menu-button">
                <button class="icon-rename"></button>
            </li>
        </ul>
    </div>
    <div class="app-navigation-entry-edit">
        <form>
            <input type="text" value="Folder entry">
            <input type="submit" value="" class="icon-close">
            <input type="submit" value="" class="icon-checkmark">
        </form>
    </div>
</li>
```

#### Entrada fijada

Toda entrada de primer nivel puede *fijarse* en la parte inferior.

- Todas las entradas fijadas pueden intercalarse entre entradas no fijadas.
- Todas las entradas fijadas **deben** tener la clase `pinned`.
- La **primera** entrada fijada **también debe** tener la clase `first-pinned`.

```html
<ul>
    <li><a href="#">Non-pinned entry</a></li>
    <li><a href="#">Non-pinned entry</a></li>
    <li class="pinned first-pinned">
        <a href="#">Pinned entry</a>
    </li>
    <li class="pinned"><a href="#">Pinned entry</a></li>
    <li><a href="#">Non-pinned entry</a></li>
    <li><a href="#">Non-pinned entry</a></li>
    <li class="pinned"><a href="#">Pinned entry</a></li>
    <li class="pinned"><a href="#">Pinned entry</a></li>
</ul>
```

#### Información diversa

- Se puede añadir la clase `icon-loading-small` a cualquier elemento `li` para ponerlo en estado de *carga*.
- Cada elemento tiene un `min-height` de 44px, ya que es el objetivo táctil mínimo recomendado. También ayuda a la facilidad de clic y a la separación en entornos de escritorio.

### Ajustes

#### Introducción

Para crear un área de ajustes, crear un div con el id `app-settings` dentro del div `app-navigation`.

- El atributo de datos `data-apps-slide-toggle` despliega hacia arriba un área de destino mediante un selector de jQuery y oculta el área si el usuario hace clic fuera de ella.
- La altura máxima del área de ajustes es de 300px. **No** cambiarla.
- Mantenerla clara, organizada y simple.

#### Disposición básica

```html
<div id="app-navigation">

    <!-- Your primary action button here -->
    <!-- Your navigation here -->

    <div id="app-settings">
        <div id="app-settings-header">
            <button class="settings-button"
                    data-apps-slide-toggle="#app-settings-content">
                Settings
            </button>
        </div>
        <div id="app-settings-content">
            <!-- Your settings content here -->
        </div>
    </div>
</div>
```
````
