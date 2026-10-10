---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Variables CSS de color, fondo, estado y estructura, clases CSS predefinidas y pautas de RTL para dar a los componentes un aspecto coherente."
---
(nc-dev-css)=
# CSS

## Resumen

Esta página lista las variables CSS de color primario, fondo, color general, estados y estructura de los elementos, las clases CSS predefinidas de uso público y las pautas para escribir CSS compatible con idiomas RTL. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/html_css_design/css.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Aunque la forma recomendada de desarrollar la interfaz de usuario es usar Vue con los componentes que proporciona Nextcloud,
Nextcloud también proporciona variables y clases CSS para dar estilo a los componentes y lograr un aspecto coherente.

(nc-dev-cssvars)=
### Variables CSS

Se recomienda encarecidamente usar las variables CSS que proporciona Nextcloud para dar estilo a los componentes.
Así se tiene la seguridad de que la app de tematización y accesibilidad puede ajustar los valores de forma dinámica.
Hacerlo también permite a los usuarios forzar el tema oscuro o claro, el alto contraste u otras opciones relacionadas con la tematización.

#### Variables del color primario

El color primario es el color de acento principal, que puede configurar el administrador o el usuario (si la tematización por usuario está habilitada).

| Variable | Ejemplo | Uso |
|---|---|---|
| `--color-primary` | `#00679e` | Color primario configurado por el usuario |
| `--color-primary-text` | `#ffffff` | Color de texto para usar sobre `--color-primary` |
| `--color-primary-hover` | `#3285b1` | Variante de `--color-primary` para efectos al pasar el cursor |
| `--color-primary-light` | `#e5eff5` | Variante clara de `--color-primary` que se usa para acciones secundarias |
| `--color-primary-light-text` | `#00293f` | Color de texto para usar sobre `--color-primary-light` |
| `--color-primary-light-hover` | `#dbe4ea` | Variante de `--color-primary-light` para efectos al pasar el cursor |
| `--color-primary-element` | `#00679e` | Variante de `--color-primary` ajustada para accesibilidad, para usar en elementos interactivos |
| `--color-primary-element-text` | `#ffffff` | Color de texto para usar sobre `--color-primary-element` |
| `--color-primary-element-text-dark` | `#f5f5f5` | Versión de menor contraste de `--color-primary-element-text` |
| `--color-primary-element-hover` | `#005a8a` | Variante de `--color-primary-element` para efectos al pasar el cursor |
| `--color-primary-element-light` | `#e5eff5` | Variante clara de `--color-primary-element` que se usa para acciones secundarias |
| `--color-primary-element-light-text` | `#00293f` | Color de texto para usar sobre `--color-primary-element-light` |
| `--color-primary-element-light-hover` | `#dbe4ea` | Variante de `--color-primary-element-light` para efectos al pasar el cursor |
| `--primary-invert-if-bright` | `invert(100%)` | Filtro para invertir los iconos colocados sobre fondos del color primario si el color primario es claro |
| `--primary-invert-if-dark` | `invert(100%)` | Filtro para invertir los iconos colocados sobre fondos del color primario si el color primario es oscuro |

#### Variables del fondo

| Variable | Ejemplo | Uso |
|---|---|---|
| `--color-background-plain` | `#00679e` | El color de fondo del elemento `body` |
| `--color-background-plain-text` | `#ffffff` | Color de texto para usar directamente sobre el fondo (p. ej., el menú de la cabecera) |
| `--image-background` | `url('clouds.jpg')` | Imagen de fondo que se usa en el elemento `body` (opcional) |
| `--background-image-invert-if-bright` | `invert(100%)` | Filtro para invertir los iconos (claros) colocados directamente sobre el fondo del body (menú de apps) |

#### Variables de color generales

| Variable | Ejemplo | Uso |
|---|---|---|
| `--color-main-text` | `#222222` | Color principal del texto |
| `--color-text-maxcontrast` | `#6b6b6b` | Color de texto más claro que sigue cumpliendo los requisitos de accesibilidad |
| `--color-text-maxcontrast-background-blur` | `#595959` | `--color-text-maxcontrast` para fondos difuminados, ver `--color-main-background-blur` |
| `--color-main-background` | `#fffff` | Color principal del fondo |
| `--color-main-background-rgb` | `255,255,255` | Variante RGB de `--color-main-background` |
| `--color-main-background-blur` | `rgba(var(--color-main-background-rgb), .8)` | Color de fondo que se usa para fondos difuminados, ver `--filter-background-blur` |
| `--color-background-hover` | `#f5f5f5` | Color de fondo para efectos al pasar el cursor |
| `--color-background-dark` | `#ededed` | Puede usarse, p. ej., para colorear las filas seleccionadas de una tabla |
| `--color-background-darker` | `#dbdbdb` | ¡Solo debe usarse para elementos, no como fondo de texto! De lo contrario, no funcionará para la accesibilidad. |
| `--color-border` | `#ededed` | Color predeterminado del borde de los elementos |
| `--color-border-dark` | `#dbdbdb` | Versión más oscura del color del borde |
| `--color-border-maxcontrast` | `#7d7d7d` | El color de borde más claro posible para la accesibilidad |
| `--color-placeholder-light` | `#e6e6e6` | Color para los marcadores de posición de los campos de entrada |
| `--color-placeholder-dark` | `#cccccc` | Versión más oscura de `--color-placeholder-light` |
| `--color-scrollbar` | `#33333344` | Color para las barras de desplazamiento |
| `--color-loading-light` | `#cccccc` | Color para el indicador de carga (su parte clara) |
| `--color-loading-dark` | `#444444` | Color para el indicador de carga (su parte oscura) |
| `--color-box-shadow-rgb` | `77,77,77` | Color para los efectos de sombra de caja, en notación RGB |
| `--color-box-shadow` | `rgba(var(--color-box-shadow-rgb), 0.5)` | Color para los efectos de sombra de caja |
| `--background-invert-if-dark` | `invert(100%)` | Filtro para invertir los iconos (oscuros) (p. ej., establecido si el tema de color es oscuro) |
| `--background-invert-if-bright` | `invert(100%)` | Filtro para invertir los iconos (claros) (p. ej., establecido si el tema de color es claro) |

#### Variables de los colores de estado

| Variable | Ejemplo | Uso |
|---|---|---|
| `--color-text-error` | `#c90000` | Para texto sobre un fondo **normal** que deba tener un estado de error |
| `--color-text-success` | `#099f05` | Para texto sobre un fondo **normal** que deba tener un estado de éxito |
| `--color-element-error` | `#c90000` | Color con el contraste adecuado para elementos que tienen un estado de error, por ejemplo, iconos |
| `--color-element-info` | `#0077C7` | Color con el contraste adecuado para elementos que tienen un estado de información, por ejemplo, iconos |
| `--color-element-success` | `#099f05` | Color con el contraste adecuado para elementos que tienen un estado de éxito, por ejemplo, iconos |
| `--color-element-warning` | `#BF7900` | Color con el contraste adecuado para elementos que tienen un estado de advertencia, por ejemplo, iconos |
| `--color-border-error` | `#c90000` | Color del borde para elementos que tienen un estado de error, como los campos de entrada cuya validación falla |
| `--color-border-success` | `#099f05` | Color del borde para elementos que tienen un estado de éxito, como los campos de entrada que se han guardado |
| `--color-favorite` | `#a37200` | Color para marcar favoritos; puede usarse, p. ej., para colorear un icono de estrella de los favoritos |
| `--color-error` | `#FFE7E7` | Color para mostrar el estado de error; no debe usarse para texto, sino para fondos de elementos |
| `--color-error-hover` | `#ffc3c3` | Color de fondo para los efectos al pasar el cursor de `--color-error` |
| `--color-error-text` | `#8A0000` | Color del texto sobre elementos que usan `--color-error` como fondo |
| `--color-warning` | `#FFEEC5` | Color para mostrar el estado de advertencia; no debe usarse para texto, sino para fondos de elementos |
| `--color-warning-hover` | `#ffe4a1` | Color de fondo para los efectos al pasar el cursor de `--color-warning` |
| `--color-warning-text` | `#664700` | Color del texto sobre elementos que usan `--color-warning` como fondo |
| `--color-success` | `#D8F3DA` | Color para mostrar el estado de éxito; no debe usarse para texto, sino para fondos de elementos |
| `--color-success-hover` | `#bdebc0` | Color de fondo para los efectos al pasar el cursor de `--color-success` |
| `--color-success-text` | `#005416` | Color del texto sobre elementos que usan `--color-success` como fondo |
| `--color-info` | `#D5F1FA` | Color para mostrar el estado de información; no debe usarse para texto, sino para fondos de elementos |
| `--color-info-hover` | `#b5e6f6` | Color de fondo para los efectos al pasar el cursor de `--color-info` |
| `--color-info-text` | `#0066AC` | Color del texto sobre elementos que usan `--color-info` como fondo |
| `--color-error-rgb` | `219,6,6` | (⚠️ obsoleta desde 32.0.0) Variante RGB de `--color-error` |
| `--color-info-rgb` | `0,113,173` | (⚠️ obsoleta desde 32.0.0) Variante RGB de `--color-info` |
| `--color-success-rgb` | `45,123,65` | (⚠️ obsoleta desde 32.0.0) Variante RGB de `--color-success` |
| `--color-warning-rgb` | `163,114,0` | (⚠️ obsoleta desde 32.0.0) Variante RGB de `--color-warning` |

#### Variables de la estructura de los elementos

| Variable | Ejemplo | Uso |
|---|---|---|
| `--animation-quick` | `100ms` | Duración de la animación para transiciones CSS ágiles |
| `--animation-slow` | `300ms` | Duración de la animación para transiciones más complejas |
| `--breakpoint-mobile` | `1024px` | Punto de ruptura para la disposición adaptable al móvil (p. ej., si la navegación de la app debe estar siempre visible) |
| `--filter-background-blur` | `blur(25px)` | Filtro para usar en elementos con fondo difuminado (p. ej., la navegación de la app) |
| `--font-face` | `system-ui, 'Segoe UI', Roboto, Oxygen-Sans` | Fuente que se usa en la interfaz de usuario de Nextcloud |
| `--default-font-size` | `15px` | Tamaño de fuente para el texto normal |
| `--default-line-height` | `1.5` | Altura de línea para el texto normal |
| `--default-grid-baseline` | `4px` | Base de todos los tamaños de espaciado que se usan en Nextcloud, que son múltiplos del tamaño de la línea base |
| `--border-width-input` | `1px` | Ancho del borde de los elementos interactivos, como los campos de texto y los selectores |
| `--border-width-input-focused` | `2px` | Ancho del borde de los elementos interactivos cuando tienen el foco (ajustado para la accesibilidad) |
| `--border-radius-small` | `4px` | Radio del borde que se usa para los elementos más pequeños |
| `--border-radius-element` | `8px` | Radio del borde de los elementos interactivos, como botones, campos de entrada, elementos de navegación y elementos de lista. |
| `--border-radius-container` | `12px` | Para contenedores más pequeños, como los menús de acciones. |
| `--border-radius-container-large` | `16px` | Para contenedores más grandes, como el body o los modales. |
| `--default-clickable-area` | `34px` | Tamaño predeterminado (ancho y alto) de los elementos interactivos, como los botones |
| `--clickable-area-large` | `48px` | Tamaño mayor para los elementos principales de la interfaz |
| `--clickable-area-small` | `24px` | El tamaño más pequeño posible de los elementos interactivos, que usan las acciones terciarias, como los chips de filtro |
| `--body-container-radius` | `calc(var(--default-grid-baseline) * 3)` | Radio del borde del contenedor del body |
| `--body-container-margin` | `calc(var(--default-grid-baseline) * 2)` | Margen del contenedor del body |
| `--header-height` | `50px` | Altura de la barra principal de navegación de apps |
| `--navigation-width` | `300px` | Ancho de la barra lateral de navegación dentro de la app |
| `--sidebar-min-width` | `300px` | Ancho mínimo de la barra lateral de la app en pantallas pequeñas |
| `--sidebar-max-width` | `500px` | Ancho máximo de la barra lateral de la app en pantallas anchas |

(nc-dev-cssclasses)=
### Clases CSS

Hay algunas clases predefinidas de uso público para facilitar el desarrollo de una aplicación para Nextcloud.

| Clase CSS | Uso |
|---|---|
| `.hidden-visually` | Oculta visualmente un elemento de la página, pero lo mantiene en el árbol de accesibilidad |
| `.hidden` | Oculta un elemento por completo de la página (también se elimina del árbol de accesibilidad) |
| `.bold` | Pone en negrita el contenido del elemento para enfatizarlo |
| `.center` | Centra el texto del elemento |
| `.clear-left` | Anula el float a la izquierda |
| `.clear-right` | Anula el float a la derecha |
| `.clear-both` | Anula el float en ambos lados |
| `.pull-left` | Float a la izquierda |
| `.pull-right` | Float a la derecha |
| `.inlineblock` | Convierte un elemento en un bloque en línea |

### Pautas de RTL

#### Qué hacer y qué no

| Incorrecto | Correcto | Descripción |
|---|---|---|
| Usar propiedades físicas `margin-left` | Usar propiedades lógicas `margin-inline-start` | Usar propiedades lógicas se adapta automáticamente a LTR/RTL |
| Usar `left` o `right` | Usar inset-inline-start/end | Mantener el posicionamiento consciente de la dirección |
| Usar text-align: left/right | Usar text-align: start/end | El texto se alinea correctamente en ambos modos |
| Usar border-left/right | Usar border-inline-start/end | Los bordes se invierten correctamente |
| Usar float: left/right | Usar float: inline-start/end | El float respeta la dirección |
| Suponer que RTL «simplemente funciona» | Probar la app con idiomas RTL | Usar el valor de CSS correcto no siempre basta para evitar errores |
````
