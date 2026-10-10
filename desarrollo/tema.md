---
tipo: guia
audiencia: desarrollo
apps: [gestion]
resumen: "Cambiar el tema de servidor de la suite: sus capas, las claves que fija la provisión, las reglas del motor de temas, las pantallas heredadas y las fuentes."
---
# Tema

## Objetivo

Cambiar la apariencia de la suite sin editar el núcleo ni una aplicación de terceros. Todo se aplica encima: la app Theming, `occ`, el tema de servidor `themes/apsconecta/` y los recursos propios. Un cambio dentro del núcleo o de una aplicación ajena se perdería en la siguiente actualización.

La suite fija la misma apariencia en cada establecimiento: el nombre y el lema del producto, los colores de APS Conecta, los logotipos, el tema claro como único tema, el nombre corto del establecimiento en la barra superior y la marca también en las pantallas de mantenimiento, actualización y error. Una pantalla tiene la marca cuando cumple cuatro condiciones: lleva el logotipo, el fondo, los colores y las fuentes de la suite; ningún texto visible nombra al fabricante; no ofrece publicidad ni enlaces del fabricante; y su texto cumple el contraste AA.

La página {doc}`/administracion/servidor/theming` describe la app Theming de la plataforma. En la suite nadie la configura a mano: la fase `15-branding` de gestion es la única que escribe sus claves.

### Las cuatro capas

| Capa | Qué fija | Dónde vive | Quién la escribe |
|---|---|---|---|
| Identidad | Nombre, lema, direcciones, colores, `productName` e imágenes de marca | La configuración de la app Theming | `provisioning/phases/15-branding.sh` |
| CSS y fuentes | `@font-face`, tipografía de títulos, barra superior, foco y alto contraste | `themes/apsconecta/core/css/server.css` | El propio archivo |
| Iconos por aplicación | Reemplazos de iconos que desentonan | `themes/apsconecta/apps/<appid>/img/` | Nadie: el directorio no existe |
| Fuente de la marca | Fichas de color, arte de los logotipos y manual de marca | El kit de marca, fuera de git | Diseño |

La capa CSS y las pantallas heredadas son las únicas razones de que exista el directorio del tema. Las imágenes se registran con `occ theming:config` desde rutas absolutas, y la identidad y el color son configuración; solo `@font-face` y los tres archivos de las pantallas heredadas necesitan una ruta que el servidor lea.

### Las claves que fija la provisión

| Clave | Valor | Efecto |
|---|---|---|
| `name`, `slogan`, `url`, `imprintUrl`, `privacyUrl` | El nombre del producto, su lema y las direcciones del sitio de APS Conecta | Título, inicio de sesión, correos y pie |
| `productName` | El nombre del producto | `/status.php`, `OC.theme`, las capacidades OCS y el botón de los enlaces públicos; sin esta clave, el nombre del fabricante se filtra |
| `primary_color` | `#7f21fe` | Botones, casillas, iconos de carpetas y la familia `--color-primary-*` |
| `background_color` | `#5315a8` | El color del texto sobre el fondo y la inversión de los iconos de la barra superior |
| `logo`, `logoheader`, `favicon`, `background` | Los SVG de `themes/apsconecta/core/img/` | El logotipo del inicio de sesión, el del menú lateral, el favicon y el fondo de toda la interfaz |
| `enforce_theme` | `light` | Bloquea la apariencia en el tema claro |
| `disable-user-theming` | `yes` | Impide fondos y colores personales |
| `customclient_ios_appid` | Vacío | Quita el aviso que invita a abrir la aplicación de iOS |
| `theme` | `apsconecta` | Activa el tema de servidor |

La misma fase pinta el menú lateral con el violeta del fondo, hace que el icono de inicio lleve a la intranet (`defaultapp` en `intravox`) y deja vacía la carpeta de una cuenta nueva (`skeletondirectory` vacío).

### Colores y contraste

| Color | Hex | Contraste sobre blanco | Uso permitido |
|---|---|---|---|
| Violeta principal | `#7f21fe` | 5,57:1 | Texto e interfaz (`primary_color`) |
| Violeta oscuro | `#5315a8` | ~8:1 | Títulos y fondo (`background_color`) |
| Rosa de error | `#ea003e` | 4,33:1 | Interfaz, bordes y texto grande; nunca texto de cuerpo |
| Oro | `#e06f00` | 3,07:1 | Rellenos, iconos y texto grande |
| Oro oscuro | `#9a4c00` | ≥4,5:1 | Texto pequeño |
| Tinta | `#101828` | ~16:1 | Texto principal |
| Apagado | `#485363` | ~7:1 | Texto secundario |

El oro de la marca no cumple AA en texto pequeño sobre blanco: se reserva para rellenos, iconos, insignias y texto grande (24 px, o 19 px en negrita), y el texto pequeño usa el oro oscuro. Los dos violetas no son intercambiables: `background_color` debe quedar en el oscuro, porque de él se calculan el color del texto sobre el fondo y la inversión de los iconos.

### Las reglas del motor de temas

1. **`:root` es inerte.** El servidor declara sus variables en `body[data-theme-light]` y carga su hoja después de `server.css`, así que una variable declarada en `:root` pierde dentro de `body`. Para ganar, se declara en `body` con `!important`, como `--font-face`. Los selectores de elemento (`h1`, `#header`, `:focus-visible`) sí ganan.
2. **Se mide en `document.body`.** `document.documentElement` solo ve la capa `:root` y da falsas alarmas.
3. **`--color-error` y `--color-success` son fondos.** Para texto se usan `--color-text-error` y `--color-text-success`.
4. **`enforce_theme=light` quita más que el tema oscuro.** También desaparecen el alto contraste y la fuente para dislexia. El bloque `@media (prefers-contrast: more)` de `server.css` es la única opción de alto contraste de la instancia.
5. **`background_color` debe coincidir con la imagen de fondo.** El servidor calcula desde ese valor el color del texto sobre el fondo y la inversión de los iconos: un blanco sobre un fondo violeta dio texto negro e iconos invertidos. Por la misma razón, nada se pinta sobre el fondo.
6. **`themes/` es un mecanismo heredado y sin documentar.** No tiene aviso de obsolescencia, así que se verifica en cada versión mayor.
7. **Un SVG que no se analiza se sirve con 200 y no dibuja nada.** Basta un doble guion dentro de un comentario XML.
8. **El nombre visible de una aplicación de terceros no es trabajo del tema.** Es un literal de PHP sin traducción; se cambia con un parche de la aplicación (gestion ADR-0002).

### La doble ruta de render

Una pantalla renderizada por el framework emite `BeforeTemplateRenderedEvent`; ese evento agrega `server.css` y las hojas de variables de la app Theming. Una pantalla heredada pasa por `Template::printPage()` y no emite nada: mantenimiento, las dos pantallas de actualización, 429, la excepción fatal, el dominio no confiable, el error de configuración y las tres pantallas de instalación. Ninguna aplicación alcanza esas pantallas; `themes/` es el único mecanismo.

Tres archivos del tema las cubren:

- `core/css/guest.css` declara variables en `:root` sin `!important`, la única excepción a la regla 1, y es deliberada: gana donde no hay hojas generadas y queda inerte en `/login`, donde la app Theming ya acierta.
- `defaults.php` aporta las cadenas de identidad. En un host no confiable, o con `installed` en falso, el servidor responde con un `\OC_Defaults` cuyas cadenas son literales sin configuración. No reemplaza la dirección de la documentación ni las de los clientes de sincronización: apuntan a destinos reales.
- `core/l10n/es.json` reemplaza dos cadenas de esas pantallas.

PHP guarda `defaults.php` en OPcache: después de cambiarlo, hay que reiniciar el contenedor del servidor. Una siembra no lo escribe; cambia con un `git pull`.

### Las fuentes

Fraunces se usa en los títulos (`h1` a `h3`) y en la barra superior, y Nunito Sans en todo lo demás. Las sirve el propio servidor en WOFF2, sin TTF de respaldo y sin peticiones a terceros. Nunito Sans entra por `--font-face`, la única variable tipográfica documentada, con `!important`; Fraunces, por selectores de elemento, porque no hay una variable documentada para una fuente de títulos.

Los SVG de los logotipos incrustan su propio subconjunto de fuentes: un SVG servido como imagen no alcanza el `@font-face` de `server.css`, y sin el subconjunto se dibujaban en Georgia (B-011). `themes/apsconecta/tools/embed-fonts.py` regenera ese subconjunto. Los WOFF2 servidos no son subconjuntos; los subconjuntos de los logotipos son una versión modificada que la licencia OFL permite ({doc}`/_generated/componentes`).

### La barra superior

Sobre 601 px de ancho, la barra superior muestra tres casillas: la marca `logo-mark.svg`, el icono de inicio y el nombre corto del establecimiento. Bajo ese ancho, las dos casillas generadas se retiran y vuelve la casilla de fábrica con la misma marca. Las reglas apuntan a `a#nextcloud`, no a `#nextcloud`: el encabezado de un enlace público usa el mismo id en un `<div>` y recibía el relleno de la barra (B-012).

El nombre del establecimiento viene de `core/css/site.css`, que la fase `15-branding` genera en cada instalación a partir de `SITE_NOMBRE_CORTO`. Es el único contenido del tema que cambia por instalación, no se confirma en git, y mientras falta, `server.css` muestra el nombre del producto.

### El indicador de carga de las aplicaciones

`server.css` define una sola vez las clases `.aps-mount-loading` y `.aps-mount-noscript`. territorio, epidemiologia y la página de administración de estadistica pegan dentro de su punto de montaje el fragmento que fija `themes/apsconecta/MAPEO.md`, idéntico en todas, y Vue lo reemplaza al montar: el componente no depende de ninguna aplicación. Una aplicación se suma pegando el mismo fragmento; la página principal de farmacia muestra en su lugar un aviso propio.

## Requisitos

- La pila de desarrollo de gestion ({doc}`entorno`): `themes/` se monta en vivo en el contenedor, sin reconstruir la imagen.
- Las reglas del motor de temas de esta página, leídas antes de tocar `server.css`.

## Pasos

1. Para una clave de identidad, de color o de imagen, editar `provisioning/phases/15-branding.sh`, nunca el panel de administración.
2. Para tipografía, barra superior, foco o alto contraste, editar `themes/apsconecta/core/css/server.css`.
3. No escribir una ruta del tema en el texto de un comentario de `server.css`: la compuerta la extrae y la busca en disco igual que una referencia real.
4. Si cambia el arte de un logotipo, regenerar su subconjunto de fuentes con `themes/apsconecta/tools/embed-fonts.py`.
5. Converger con el objetivo `seed` o `install` del Makefile. La siembra vuelve a registrar las cuatro imágenes de marca y así renueva el parámetro de caché de `server.css`.
6. Si cambió `defaults.php`, reiniciar el contenedor del servidor.

## Verificación

- El objetivo `test` comprueba que cada SVG del tema se analiza como XML y que cada `url()` de `server.css` existe en disco. Con una pila AIO en marcha, comprueba además en el contenedor las plantillas de las que depende el tema: `a#nextcloud` como enlace en el diseño autenticado y como `<div>` en el público, el bloque de publicidad que el tema oculta y las siete llamadas heredadas.
- El objetivo `smoke`, en una instancia AIO, comprueba que `/status.php` responde 200 sin la cadena `Nextcloud`, que un host no confiable rebota con 302 en vez de mostrar una pantalla heredada, y que el tema activo trae `core/css/guest.css` y `defaults.php`.
- Dos siembras seguidas no cambian nada, salvo los cuatro registros de imágenes de marca, que se reescriben por diseño.
- En el navegador, sobre `document.body`: `--font-face` empieza por Nunito Sans, `--color-background-plain-text` es `#ffffff` sobre el violeta, `--background-image-invert-if-bright` es `no` y `--color-primary-element` es `#7f21fe`.

## Problemas frecuentes

- **Un cambio en `server.css`, correcto en disco, no se ve en el navegador.** El parámetro de caché de `server.css` cambia con la configuración de Theming, no con el archivo: ejecutar el objetivo `seed`. `side_menu` sirve su hoja con un `?v=0` fijo, así que un navegador que vuelve no ve su cambio de color.
- **Texto negro e iconos invertidos sobre el violeta.** `background_color` no coincide con la imagen de fondo (regla 5).
- **Un logotipo no aparece y los chequeos de existencia están en verde.** El SVG no se analiza (regla 7).
- **El tema no se aplica en Linux.** El contenedor, uid 33, no puede usar los archivos montados: `up` corre `fix-mount-perms` en cada arranque.

### Compromisos y límites

- No hay tema oscuro, por decisión del responsable del 2026-07-12.
- No hay iconos por aplicación: ninguna aplicación activa tiene iconos de varios tonos, el único criterio que justifica uno.
- La publicidad del fabricante se oculta, no se reestiliza, y cada ocultamiento lleva una compuerta que comprueba que su selector todavía coincide.
- La página de ajustes del conector de Euro-Office conserva unas veinte cadenas que dicen «Nextcloud Office»: renombrarlas en bloque haría falsas algunas, como la que apunta al servidor de demostración del fabricante (B-008).
- El fondo de toda la interfaz está en revisión por su legibilidad en jornadas de ocho horas.
- El barrido de contraste del 2026-07-28 es una muestra, no una prueba: no cubre aplicaciones desactivadas, estados vacíos, plantillas de correo, vistas públicas de recursos compartidos ni impresión.
