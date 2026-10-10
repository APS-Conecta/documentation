---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Estructura estándar para mostrar una lista de elementos en el contenido principal: disposición, reglas y menú emergente dentro de un elemento."
---
# Lista de contenido

## Resumen

Esta página describe la estructura estándar para mostrar una lista de elementos en el contenido principal de una app: su disposición básica, las reglas de uso y cómo poner un menú emergente dentro de un elemento. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/html_css_design/list.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Introducción

En el contenido principal, puede quererse mostrar una lista de elementos (como en los contactos o en la app de correo).
Se proporciona una estructura estandarizada para este fin concreto.

### Disposición básica

La captura muestra el componente de lista de contenido: filas de entradas con títulos, metadatos y botones de acción.

```html
<div id="app-content-wrapper">
    <div class="app-content-list">
        <a href="#" class="app-content-list-item">
            <input type="checkbox" id="test1" class="app-content-list-item-checkbox checkbox" checked="checked"><label for="test1"></label>
            <div class="app-content-list-item-icon" style="background-color: rgb(231, 192, 116);">C</div>
            <div class="app-content-list-item-line-one">Contact 1</div>
            <div class="icon-delete"></div>
        </a>
        <a href="#" class="app-content-list-item">
            <div class="app-content-list-item-star icon-starred"></div>
            <div class="app-content-list-item-icon" style="background-color: rgb(151, 72, 96);">T</div>
            <div class="app-content-list-item-line-one">Favourited task #2</div>
            <div class="icon-more"></div>
        </a>
        <a href="#" class="app-content-list-item">
            <div class="app-content-list-item-icon" style="background-color: rgb(152, 59, 144);">T</div>
            <div class="app-content-list-item-line-one">Task #2</div>
            <div class="icon-more"></div>
        </a>
        <a href="#" class="app-content-list-item">
            <div class="app-content-list-item-icon" style="background-color: rgb(31, 192, 216);">M</div>
            <div class="app-content-list-item-line-one">Important mail is very important! Don't ignore me</div>
            <div class="app-content-list-item-line-two">Hello there, here is an important mail from your mom</div>
        </a>
        <a href="#" class="app-content-list-item">
            <div class="app-content-list-item-icon" style="background-color: rgb(41, 97, 156);">N</div>
            <div class="app-content-list-item-line-one">Important mail with a very long subject</div>
            <div class="app-content-list-item-line-two">Hello there, here is an important mail from your mom</div>
            <span class="app-content-list-item-details">8 hours ago</span>
            <div class="icon-delete"></div>
        </a>
        <a href="#" class="app-content-list-item">
            <div class="app-content-list-item-icon" style="background-color: rgb(141, 197, 156);">N</div>
            <div class="app-content-list-item-line-one">New contact</div>
            <div class="app-content-list-item-line-two">blabla@bla.com</div>
            <div class="icon-delete"></div>
        </a>
    </div>
    <div class="app-content-detail">
    </div>
</div>
```

### Reglas e información

- El contenido global debe tener la siguiente estructura:

```html
<div id="app-content-wrapper">
    <div class="app-content-list">HERE YOUR CONTENT LIST</div>
    <div class="app-content-detail">HERE YOUR GLOBAL CONTENT</div>
</div>
```

- El primer ejemplo de código/captura de pantalla muestra todas las combinaciones permitidas/disponibles.
- Al mostrar la casilla de verificación, la estrella se ocultará automáticamente.
- Las casillas de verificación están ocultas de forma predeterminada. Se muestran cuando están marcadas o en hover/focus/active
- Para mostrar **todas** las casillas de verificación, aplicar la clase `selection` a `app-content-list`.
- **NO** puede haber más de un botón en una entrada. Si se necesitan varias opciones, hay que crear un {nc-ref}`menú emergente <popovermenu>`.
  - En el caso de un popovermenu, ver el {nc-ref}`menú emergente <popovermenulist>`.
  - Como siempre, el **JS** sigue siendo necesario para alternar la clase `open` en este menú
- Si se usa el estándar `app-content-list`, el div `app-content-details` se ocultará en el modo móvil (pantalla completa).
  Habrá que añadir la clase `showdetails` a `app-content-list` para mostrar el contenido principal.
  En la vista móvil, toda la sección de lista/detalles (según cuál se muestre) desplazará el body.

(nc-dev-popovermenulist)=
### Menú emergente en un elemento

Si se necesita un menú dentro de un elemento, hay que envolverlo con el `div` `icon-more` dentro de un div `app-content-list-menu`.

```html
<div class="app-content-list-item-menu">
    <div class="icon-more"></div>
    <div class="popovermenu">
        <ul>
            <li>
                <a href="#" class="icon-details">
                    <span>Details</span>
                </a>
            </li>
            <li>
                <button class="icon-details">
                    <span>Details</span>
                </button>
            </li>
            <li>
                <button>
                    <span class="icon-details"></span>
                    <span>Details</span>
                </button>
            </li>
            <li>
                <a>
                    <span class="icon-details"></span>
                    <span>Details</span>
                </a>
            </li>
        </ul>
    </div>
</div>
```
````
