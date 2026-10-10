---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Menú emergente que se abre al hacer clic en el icono de tres puntos: disposición básica, detalles técnicos de su marcado y alineación."
---
(nc-dev-popovermenu)=
# Menú emergente

## Resumen

Esta página describe el menú emergente, el menú rápido que se abre al hacer clic en el icono de tres puntos: su disposición básica, las reglas técnicas de su marcado y las clases para alinearlo. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/html_css_design/popovermenu.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Qué es un menú emergente

Es un menú rápido que se abre al hacer clic. Para los menús se usa el icono de tres puntos.

Es exactamente igual que el {nc-ref}`menú de navegación <navigation_menu>`. La única diferencia es la clase popovermenu.

### Disposición básica

```html
<div class="popovermenu">
    <ul>
       <li>
           <a href="#" class="icon-details">
               <span>Details</span>
           </a>
       </li>
       <li>
           <button class="icon-close">
               <span>Remove</span>
           </button>
       </li>
       <li>
           <button>
               <span class="icon-favorite"></span>
               <span>Favorite</span>
           </button>
       </li>
       <li>
           <a>
               <span class="icon-rename"></span>
               <span>Edit</span>
           </a>
       </li>
       <li>
           <span class="menuitem">
               <input id="check1" type="checkbox" class="checkbox" />
               <label for="check1">Enable</label>
           </span>
       </li>
       <li>
           <span class="menuitem">
               <input id="radio1" type="radio" class="radio" />
               <label for="radio1">Select</label>
           </span>
       </li>
        <li>
            <span class="menuitem">
                <span class="icon icon-user"></span>
                <form>
                        <input id="input-folder" type="text" value="new email">
                        <input type="submit" value=" " class="primary icon-checkmark-white">
                </form>
            </span>
        </li>
         <li>
             <span class="menuitem">
                 <span class="icon icon-folder"></span>
                 <form>
                         <input id="input-folder" type="text" value="New folder">
                         <input type="submit" value=" " class="icon-confirm">
                 </form>
             </span>
         </li>
    </ul>
</div>
```

### Detalles técnicos

- Los únicos elementos permitidos para los elementos del menú son **a**, **button** y **span**, este último solo para la casilla de verificación y el botón de opción.
- Se pueden combinar a y button en el mismo menú (en caso de formulario o de enlace directo), como en el ejemplo anterior
- Hay que poner el menú entero justo después del icono de tres puntos `<div><span class="icon-more"></span><div class="popovermenu">...</div></div>`
- No se necesita JS: solo con CSS basta para el posicionamiento. JS **sigue** siendo necesario para gestionar el ocultar/mostrar.
- Solo se permite **un** ul.
- Solo se permite **un nivel** de menú.
- Cada entrada **debe** tener su propio icono. Esto mejora mucho la UX.
- La distancia **derecha** necesaria hasta el borde (o el padding, lo que se prefiera usar) del icono de tres puntos debe ser de 14px (5 para el margen del menú y 6 para la posición de la flecha)
- El elemento `span` **debe** tener la clase `menuitem`.
- La casilla de verificación o el botón de opción deben usar los {nc-ref}`personalizados de nextcloud <checkboxes-and-radios>`
- El elemento form es opcional si se usan inputs.
- Los inputs admitidos son todos los basados en texto y los de tipo botón

### Alineación

Para alinear el menú, se puede añadir la clase al div popovermenu principal.

- Centro: `menu-center`
- Izquierda: `menu-left`
- La derecha es la predeterminada
````
