---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Estándares de código de HTML y CSS: HTML5, sangría, clases en lugar de ID, CSS reutilizable y la convención de nombres BEM, con ejemplos."
---
# Estándares de código de CSS y HTML

## Resumen

Esta página recoge los estándares de código de HTML y CSS: cómo escribir y sangrar el HTML, cómo desacoplar el CSS de la estructura HTML y la convención de nombres BEM para las clases, con ejemplos de qué hacer y qué no. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/getting_started/coding_standards/html_css.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

### HTML

- El HTML debe cumplir con HTML5
- Evitar más de una etiqueta por línea
- Sangrar siempre los bloques
- Intentar evitar los ID; en su lugar, preferir las clases.

**HACER**

```html
<button>
    <span class="icon icon-close"></span>
    Close
</button>
```

**NO HACER**

```html
<button><span class="icon icon-close"></span>Close</button>
```

### CSS

- No ligar demasiado el CSS a la estructura HTML.
- Intentar evitar los ID y las etiquetas en los selectores de consulta; usar clases en su lugar.
- Intentar que el CSS sea reutilizable agrupando los atributos comunes en clases.
- Ver el vídeo [Writing Tactical CSS & HTML](https://www.youtube.com/watch?v=hou2wJCh3XE&feature=plcp) en YouTube.

**HACER**:

```css
.list {
    list-style-type: none;
}

.list > .list__item {
    display: inline-block;
}

.important_list_item {
    color: red;
}
```

**NO HACER**:

```css
#content .myHeader ul {
    list-style-type: none;
}

#content .myHeader ul li.list_item {
    color: red;
    display: inline-block;
}
```

#### Convención de nombres

Recomendamos usar la convención de nombres BEM (Block-Element-Modifier) para las clases CSS.
BEM ayuda a que el CSS sea reutilizable y más fácil de mantener, sobre todo al usar preprocesadores como SASS.

**HACER**:

```css
.button {
    background-color: var(--color-main-background);
}

.button--primary {
    background-color: var(--color-primary);
}

.button__icon {
    width: 20px;
}
```

**NO HACER**:

```css
button.btn {
    background-color: var(--color-main-background);
}

button.btn.primary {
    background-color: var(--color-primary);
}
button.btn span.myIcon {
    width: 20px;
}
```
````
