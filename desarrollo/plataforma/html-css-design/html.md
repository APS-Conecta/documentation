---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Elementos HTML con estilo propio: la barra de progreso html5 y las casillas de verificación y botones de opción tematizados, con sus requisitos."
---
(nc-dev-html)=
# Elementos HTML

## Resumen

Esta página describe los elementos HTML que ya vienen tematizados: la barra de progreso html5 y las casillas de verificación y botones de opción personalizados, con los requisitos de su marcado. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/html_css_design/html.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Barra de progreso

Nextcloud admite y proporciona una barra de progreso ya tematizada.

Usar el elemento html5 `progress`.

```html
<progress value="42.79" max="100"></progress>
```

(nc-dev-checkboxes-and-radios)=
### Casillas de verificación y botones de opción

Como las casillas de verificación y los botones de opción predeterminados de html5 **no** son personalizables, se creó una sustitución que usa elementos label y `::after`.

Hay 2 colores:

- El predeterminado, tematizado con el color primario.
- De color blanco.

Requisitos:

- Debe haber un elemento `label` **directamente** después del elemento `input`.
- El input **debe** tener la clase `checkbox` o `radio`.
- Para usar el tema blanco, **también hay que** añadir la clase `checkbox--white` o `radio--white`.
- La etiqueta **debe** tener un texto asociado, por accesibilidad.

```html
<input type="checkbox" id="test1" class="checkbox"
       checked="checked">
<label for="test1">Selected</label><br>
<input type="checkbox" id="test2" class="checkbox">
<label for="test2">Unselected</label><br>
<input type="checkbox" id="test3" class="checkbox"
       disabled="disabled">
<label for="test3">Disabled</label><br>
<input type="checkbox" id="test4" class="checkbox">
<label for="test4">Hovered</label><br>
```

```html
<input type="radio" id="test1" class="radio"
       checked="checked">
<label for="test1">Selected</label><br>
<input type="radio" id="test2" class="radio">
<label for="test2">Unselected</label><br>
<input type="radio" id="test3" class="radio"
       disabled="disabled">
<label for="test3">Disabled</label><br>
<input type="radio" id="test4" class="radio">
<label for="test4">Hovered</label><br>
```

### Botones
````
