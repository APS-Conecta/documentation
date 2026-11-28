---
tipo: guia
audiencia: desarrollo
apps: [gestion-aio]
resumen: "Cómo llega la marca a cada pantalla de la suite: la ficha de tokens, el mapa de variables, las pantallas heredadas, las guardas y el cambio de un color."
---
# Tema

## Objetivo

Cambiar la apariencia de la suite sin editar el núcleo de Nextcloud ni una aplicación. La marca llega a cada pantalla por un solo camino, y cada paso vive en gestion-aio:

1. El manual de marca, la página {doc}`marca`, fija las reglas: la paleta por roles y dónde se usa cada color, la tipografía y el logotipo. Donde el manual y el código difieren, gana el manual.
2. La ficha de tokens de marca, [`aps/brand/tokens.css`](https://github.com/APS-Conecta/gestion-aio/blob/main/aps/brand/tokens.css), guarda los valores por rol y el par de fuentes. Es el único archivo que escribe un color de la marca.
3. El paso «Tema y marca» del Provisionador, [`aps/provisionador/steps/theme.py`](https://github.com/APS-Conecta/gestion-aio/blob/main/aps/provisionador/steps/theme.py), le da a la app Theming el color primario (el violeta), el color de fondo (el violeta oscuro), el nombre «APS Conecta Gestión», el lema y las imágenes, y deja el tema claro como único tema (`enforce_theme` en `light`). Copia además la carpeta del tema, `apsconecta`, a la carpeta `themes` de Nextcloud, con la ficha y sus fuentes, el arte SVG dibujado con los valores de la ficha y el nombre corto del establecimiento en `core/css/site.css`.
4. El mapa de variables del tema, [`aps/theme/apsconecta/core/css/variable-map.css`](https://github.com/APS-Conecta/gestion-aio/blob/main/aps/theme/apsconecta/core/css/variable-map.css), da a las demás variables de Nextcloud 34 el rol que les toca. Las declara en `body` con `!important`, porque Nextcloud declara las suyas en `body` para el tema activo. Esta página enlaza el mapa y no lo copia: el mapa es la fuente.

La hoja principal del tema, [`aps/theme/apsconecta/core/css/server.css`](https://github.com/APS-Conecta/gestion-aio/blob/main/aps/theme/apsconecta/core/css/server.css), importa la ficha, el mapa y `site.css`, y agrega las reglas propias del tema. El menú personalizado toma el violeta oscuro de la ficha en el paso [`aps/provisionador/steps/menu.py`](https://github.com/APS-Conecta/gestion-aio/blob/main/aps/provisionador/steps/menu.py). Así, un cambio de token llega al tema, al Provisionador, a la página de AIO y a cada aplicación, sin publicar una aplicación nueva.

La página {doc}`/administracion/servidor/theming` describe la app Theming de la plataforma. En la suite nadie la configura a mano: el paso «Tema y marca» escribe sus claves.

### La regla de las aplicaciones

Una aplicación se estiliza solo con los componentes de `@nextcloud/vue` y las variables de Nextcloud, nunca con los tokens de marca ni con colores literales: la marca le llega por el mapa de variables. La decisión y las opciones descartadas están en el [ADR 0003 de gestion-aio](https://github.com/APS-Conecta/gestion-aio/blob/main/docs/adr/0003-the-brand-reaches-apps-only-through-nextcloud-s-variables.md). Un color que es dato, como el de una unidad o el de una categoría de Territorio, se queda en los datos o en los scripts de la aplicación.

### Lo que queda de Nextcloud

El mapa fija solo las variables cuyo valor de Nextcloud difiere del rol. No repite lo que la app Theming ya da (el color primario, sus colores de elemento y de texto, y el fondo), ni los alias que Nextcloud escribe como `var()` de una variable del mapa. Quedan de Nextcloud, a propósito:

- Los fondos pálidos de estado, como `--color-error` y `--color-warning`: la ficha no tiene un fondo pálido de estado. El texto de error y el de advertencia que van sobre ellos sí toman la marca, y el control de aceptación mide su contraste.
- El texto de éxito: la ficha da al éxito un solo color, para iconos, bordes y texto grande, sin un paso más oscuro para texto.
- Los bordes de los campos de formulario: con los valores de Nextcloud conservan el contraste de 3:1 que pide un control.
- El área clicable, el tamaño de letra (`--default-font-size`), el interlineado (`--default-line-height`) y los radios de elemento, grande y de píldora: sus valores de Nextcloud ya son los del manual.

### Las reglas propias del tema

`server.css` agrega lo que el manual pide y Nextcloud no da:

- **Las fuentes.** `--font-face` toma la fuente de texto, Nunito Sans, y `body` la usa con `!important`, porque el `body` de las páginas de invitado usa una lista propia de fuentes del sistema. Los títulos `h1` a `h3` usan la fuente de títulos, Fraunces, con el espaciado entre letras del manual, `-0.015em`. La ficha declara las dos fuentes solo en WOFF2 y sin cursivas.
- **El anillo de foco.** Lo que tiene el foco del teclado lleva un contorno de 3 px en `--color-primary-element`, separado 2 px, por encima de los anillos de Nextcloud y de sus componentes. En la barra superior el anillo toma `--color-background-plain-text`, salvo en los paneles blancos de sus menús.
- **Más contraste.** Cuando el sistema pide más contraste (`prefers-contrast: more`), el mapa da la tinta al texto secundario y el gris apagado a los bordes, y el anillo de foco pasa a 4 px.
- **Movimiento reducido.** Cuando el sistema pide menos movimiento (`prefers-reduced-motion: reduce`), `--animation-quick` y `--animation-slow` pasan a `0s`. El tema no tiene movimiento propio.
- **La barra superior.** Solo la barra superior de una sesión iniciada (`#header:not(.header-guest)`) lleva el degradado del violeta oscuro al violeta. La zona superior de las páginas de invitado queda sin franja, y el fondo principal es un color sólido.
- **El establecimiento.** El inicio de sesión muestra el nombre corto del establecimiento sobre el formulario, y la barra superior lo muestra después del logotipo desde 601 px de ancho.

### Las pantallas heredadas

Las pantallas de mantenimiento, de actualización y de error no pasan por la app Theming. El tema las cubre con dos archivos:

- La hoja de invitados del tema, [`aps/theme/apsconecta/core/css/guest.css`](https://github.com/APS-Conecta/gestion-aio/blob/main/aps/theme/apsconecta/core/css/guest.css), que esas pantallas cargan junto a la de Nextcloud, importa la hoja principal, y con ella la ficha, el mapa y las fuentes: no tiene reglas propias que puedan separarse del tema.
- [`aps/theme/apsconecta/defaults.php`](https://github.com/APS-Conecta/gestion-aio/blob/main/aps/theme/apsconecta/defaults.php) da el nombre, el título, el nombre HTML, la dirección base, el lema y el pie. El paso del tema lo escribe con las constantes que ya tiene: `SUITE`, `SITE` y el lema `MOTTO` de [`aps/provisionador/brand.py`](https://github.com/APS-Conecta/gestion-aio/blob/main/aps/provisionador/brand.py). El pie no enlaza al sitio de Nextcloud.

Un cambio de `defaults.php` rige en 60 s, sin reinicio: la imagen de Nextcloud de AIO revalida los archivos PHP cada 60 s (`opcache.revalidate_freq=60` en [`Containers/nextcloud/Dockerfile`](https://github.com/APS-Conecta/gestion-aio/blob/main/Containers/nextcloud/Dockerfile)). El control de fin de instalación compara el `defaults.php` colocado con el que dibuja el paso, y si difieren el paso «Tema y marca» queda fallido; «Reintentar» lo vuelve a colocar.

### Las guardas

- **El control de aceptación del tema**, [`aps/acceptance/checks/60-theme.py`](https://github.com/APS-Conecta/gestion-aio/blob/main/aps/acceptance/checks/60-theme.py), corre en la corrida de aceptación en máquina limpia ([`aps/acceptance/run.sh`](https://github.com/APS-Conecta/gestion-aio/blob/main/aps/acceptance/run.sh), flujo [`.github/workflows/aps-acceptance.yml`](https://github.com/APS-Conecta/gestion-aio/blob/main/.github/workflows/aps-acceptance.yml)). En el inicio de sesión, «Inicio», Archivos, Talk y los ajustes personales, mide en `document.body` cada variable del mapa contra el valor de su rol en la ficha. Mide también el contraste: cada color de texto, al menos 4,5:1 sobre su fondo, y cada color de elemento, al menos 3:1 sobre el fondo principal. Comprueba además las fuentes, el degradado de la barra superior, el anillo de foco, las dos preferencias del sistema y la pantalla de mantenimiento con el mapa.
- **La compuerta de marca**, [`aps/gates/brand.py`](https://github.com/APS-Conecta/gestion-aio/blob/main/aps/gates/brand.py), corre con las compuertas estáticas ([`aps/gates/run.sh`](https://github.com/APS-Conecta/gestion-aio/blob/main/aps/gates/run.sh), flujo [`.github/workflows/aps-gates.yml`](https://github.com/APS-Conecta/gestion-aio/blob/main/.github/workflows/aps-gates.yml)). Rechaza un color de la marca escrito fuera de la ficha, en hexadecimal o en notación RGB, y cualquier color literal en las hojas propias, las del tema incluidas: el mapa solo nombra roles.
- **La revisión de estilo compartida**, [`.github/workflows/style-check.yml`](https://github.com/APS-Conecta/.github/blob/main/.github/workflows/style-check.yml) con [`scripts/style-check.sh`](https://github.com/APS-Conecta/.github/blob/main/scripts/style-check.sh) en el repositorio `.github` de la organización. Cada aplicación propia del menú de aplicaciones debe llamarla desde su CI, fijada por el SHA de un commit. Lee las hojas de estilo (`.css`, `.scss` y los bloques `<style>` de Vue) y las plantillas de Vue, y rechaza con archivo y línea un color literal fuera del respaldo de un `var()`, un tamaño de letra en px y un `<button>` simple. No lee scripts ni datos, donde vive un color que es dato, y falla si no encuentra estilos que leer.

### Las reglas medidas

1. **Una variable de Nextcloud declarada en `:root` no tiene efecto.** Nextcloud declara sus variables en `body` para el tema activo, así que el tema las declara en `body` con `!important`. Una variable propia del tema, como `--aps-establishment` de `site.css`, sí va en `:root`: no compite con ninguna de Nextcloud.
2. **Se mide en `document.body`.** Ahí lee el control de aceptación: una declaración en `body` no sube a la raíz del documento.
3. **`--color-error` y `--color-warning` son fondos.** El texto de error usa `--color-text-error` o `--color-error-text`, y el de advertencia, `--color-warning-text`.
4. **El fondo es un color, no una imagen.** El paso del tema fija `background` en `backgroundColor`, y `background_color` es el violeta oscuro. El control de aceptación mide que el texto sobre el fondo, `--color-background-plain-text`, quede blanco.
5. **Hay un solo tema.** Con `enforce_theme` en `light`, el alto contraste de la suite es el que pide el sistema, no una opción de la cuenta.
6. **El arte SVG nombra tokens.** Un SVG del tema o de la ficha escribe un color como `var(--aps-…)`, y la función `render` de `brand.py` escribe el valor al colocarlo. Un token que la ficha no declara hace fallar el paso del tema.

## Requisitos

- Un clon de gestion-aio con su rama principal.
- La página {doc}`marca`, leída antes de cambiar un valor: el manual fija qué rol va en cada uso.

## Pasos

1. Si cambia una regla de la marca, cambiar primero el manual, la página {doc}`marca`.
2. Para cambiar un color, editar el valor de su rol en `tokens.css`. Nunca escribir el color en otro archivo: la compuerta de marca lo rechaza.
3. Si una variable de Nextcloud debe tomar otro rol, o un rol nuevo, editar `variable-map.css` y, en el mismo cambio, la expectativa del control de aceptación, `VARIABLE_MAP` de `60-theme.py`.
4. Un rol nuevo necesita además su uso en `tools/gen-marca.py` de este sitio: sin él, la compilación del sitio falla.
5. Correr las compuertas estáticas con `aps/gates/run.sh`.
6. Correr la corrida de aceptación sobre una versión de prueba: el control del tema prueba el cambio en el navegador.

## Verificación

- La compuerta de marca pasa: ningún archivo escribe un color de la marca fuera de la ficha.
- El control de aceptación del tema pasa: cada variable del mapa tiene el valor de su rol, y cada contraste llega a su mínimo.
- En la siguiente compilación de este sitio, la tabla de la paleta de {doc}`marca` muestra el valor nuevo.

## Problemas frecuentes

- **Una variable nueva del mapa no cambia nada.** Está declarada en `:root` o sin `!important` (regla 1).
- **Un texto de error se lee mal sobre blanco.** Usa `--color-error`, que es un fondo pálido (regla 3).
- **El paso «Tema y marca» queda fallido al final de la instalación.** El `defaults.php` colocado difiere del que dibuja el paso: presionar «Reintentar».
- **Tras una versión mayor de Nextcloud, el control del tema falla en una variable.** El mapa nombra las variables de Nextcloud 34; hay que buscar el nombre que tiene en la versión nueva y actualizar el mapa y su expectativa.
- **La revisión de estilo falla sin reportar ninguna línea.** No encontró ninguna hoja `.css`, `.scss` ni `.vue` en la ruta que recibió.
