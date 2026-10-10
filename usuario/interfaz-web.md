---
tipo: guia
esqueleto: borrador
audiencia: usuario
apps: [gestion]
resumen: "Cómo entrar a la plataforma desde el navegador y orientarse en la interfaz web del establecimiento."
---
# Interfaz web

## Resumen

El acceso a la plataforma se hace por navegador web, con inicio de sesión en el dominio del establecimiento y la identidad del CESFAM visible en la barra superior. La navegación principal es el menú lateral (side_menu), agrupado en Principal, Salud y Comunicaciones y Agenda, complementado por la búsqueda global unificada y por el modo escritorio (desktop_workspace), que ejecuta las aplicaciones en ventanas dentro de una sola pestaña.

## Secciones previstas

- Acceso e inicio de sesión
- Menú lateral
- Barra superior y búsqueda global
- Modo escritorio

### La interfaz web de Nextcloud

````{upstream} user_manual/webinterface.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Abrir la URL del servidor Nextcloud en cualquier navegador web e iniciar sesión con el nombre de cuenta (o la dirección de correo electrónico) y la contraseña.

También se puede iniciar sesión con una llave de acceso o una llave de seguridad física haciendo clic en **Iniciar sesión con dispositivo**.

#### Requisitos del navegador web

Para obtener la mejor experiencia, usar la versión más reciente de uno de estos navegadores:

- Google **Chrome** / Chromium
- Mozilla **Firefox**
- Apple **Safari**
- Microsoft **Edge**

:::{note}
No todas las versiones son compatibles. Nextcloud se orienta a los [navegadores que alcanzan el umbral mínimo de uso](https://browserslist.dev/?q=PjAuMjUlLCBub3Qgb3BfbWluaSBhbGwsIG5vdCBkZWFkLCBGaXJlZm94IEVTUg==).
:::

#### El Dashboard

Después de iniciar sesión, Nextcloud abre el **Dashboard**, una vista general personalizable de la actividad más importante: próximos eventos del calendario, mensajes no leídos, archivos recientes y más.

Usar el botón **Personalizar** en la parte inferior de la página para agregar, quitar o reorganizar widgets y adaptarlo a la propia forma de trabajar.

#### Navegar por la interfaz

La barra de navegación en la parte superior de cada página es el principal punto de acceso:

- El **logotipo de Nextcloud** (arriba a la izquierda) te lleva de vuelta al Dashboard.
- Los **accesos directos a aplicaciones** se muestran junto al logotipo: hacer clic en cualquier icono para cambiar a esa aplicación (Archivos, Calendario, Talk, etc.).
- El **icono de búsqueda** a la derecha abre la {nc-ref}`búsqueda unificada <unified-search>`, que busca en todas las aplicaciones a la vez.
- El **icono de campana** muestra las notificaciones.
- El **icono de contactos** permite buscar y contactar rápidamente a otros usuarios del servidor.
- La **foto de perfil** (en el extremo derecho) abre el menú de ajustes.

Cada aplicación tiene además su propia **barra lateral izquierda** con filtros y acciones específicos de esa aplicación.

#### Ajustes y perfil

Hacer clic en la foto de perfil para acceder a las opciones de la cuenta.

Desde este menú se puede:

- Ver y editar el perfil
- Establecer el estado en línea
- Cambiar los ajustes de apariencia y accesibilidad
- Abrir la página personal de {nc-doc}`Ajustes <user_manual/userpreferences>`
- Acceder a la ayuda y a la información de privacidad
- Cerrar sesión

(nc-unified-search)=
#### Búsqueda unificada

Hacer clic en el icono de búsqueda de la barra de navegación (o pulsar {kbd}`Ctrl+F`) para abrir la ventana modal de búsqueda unificada.

La búsqueda unificada busca en todas las aplicaciones instaladas a la vez: archivos, eventos del calendario, mensajes, contactos y más. Los resultados se agrupan por aplicación para que se pueda ver rápidamente dónde se encontró una coincidencia.

Usar los botones de filtro para acotar los resultados:

- **Ubicaciones**: limita la búsqueda a una aplicación concreta, como Archivos o Calendario.
- **Fecha**: filtra por periodo (hoy, últimos 7 días, últimos 30 días, este año o un rango personalizado).
- **Personas**: muestra solo los resultados relacionados con una persona concreta.
````

### Acceso universal

````{upstream} user_manual/universal_access.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El acceso universal es muy importante para nosotros. Seguimos los estándares web y nos aseguramos de que todo se pueda usar con un teclado y con software de asistencia, como los lectores de pantalla. Nuestro objetivo es cumplir las [Pautas de Accesibilidad para el Contenido Web 2.1](https://www.w3.org/WAI/standards-guidelines/wcag/) en el nivel AA, y con el tema de alto contraste incluso en el nivel AAA. También seguimos las directrices alemanas BITV 2.0.

Si encuentra algún problema, infórmelo en nuestro [centro de incidencias](https://github.com/nextcloud/server/issues/). Y si quiere participar, ¡[únase a nuestro equipo de diseño](https://nextcloud.com/design)!

#### Ampliación y adaptatividad

La interfaz de Nextcloud es completamente adaptativa y se puede usar con pantallas de cualquier tamaño. Puede ampliar y alejar para ajustar el texto y el tamaño de los elementos a su gusto. La barra de navegación y la barra lateral pueden ser expandidas o colapsadas.

#### Navegar con el teclado

Se puede navegar por la interfaz web con un teclado, igual que con un ratón:

- `Tab` y `Shift + Tab` para moverte entre elementos
- `Enter` o `Space` para activar o abrir el elemento (según el tipo de elemento)
- `Escape` se usa para cerrar ventanas modales, menús emergentes y visores de archivos
- `Left arrow` y `Right arrow` para navegar entre fotos en el visor
- `Ctrl + F` para poner el foco en el campo de búsqueda
- `Ctrl + S` para guardar los cambios en editores como Nextcloud Text

Para una navegación más rápida, ofrecemos dos «enlaces de salto» al comienzo del documento, que te permiten:

- Saltar al contenido principal
- Saltar a la navegación de la app

Nextcloud Talk tiene atajos que están documentados también en los ajustes de la propia aplicación:

- `C` para poner el foco en el campo de entrada de mensajes
- `Escape` para quitar el foco del campo de entrada de mensajes y así poder usar los atajos
- `F` para poner el chat o la llamada en pantalla completa
- Durante una llamada:
  - `M` para activar o desactivar el micrófono
  - `V` para activar o desactivar el video
  - `Space` para pulsar para hablar o pulsar para silenciar
  - `R` para levantar o bajar la mano

Nextcloud Mail tiene atajos también, documentados en las preferencias de la propia aplicación:

- `C` para redactar un mensaje nuevo
- `Left arrow` para cambiar a un mensaje más reciente
- `Right arrow` para cambiar a un mensaje más antiguo
- `S` para marcar o desmarcar un mensaje como favorito
- `U` para marcar o desmarcar un mensaje como no leído
- `Del` para eliminar un mensaje
- `Ctrl + Enter` para enviar
- `R` para actualizar y cargar correos nuevos

#### Temas incluídos

Ofrecemos algunos temas que puede activar para mejorar la accesibilidad:

- **Tema de alto contraste:** un modo de alto contraste para facilitar la navegación. La calidad visual se reducirá, pero la claridad aumentará.
- **Tema oscuro:** un tema oscuro para descansar la vista al reducir la luminosidad y el brillo generales. Todavía está en desarrollo, así que se agradece informar de cualquier problema que se encuentre.
- **Tipo de letra para dislexia:** OpenDyslexic es una tipografía/fuente gratuita diseñada para mitigar algunos de los errores de lectura comunes causados por la dislexia.

Para entrar en los ajustes de accesibilidad:

1. Abrir el menú de ajustes al final de la cabecera
2. Seleccionar **Ajustes**
3. En la navegación, elegir **Accesibilidad**

:::{note}
El contraste de los elementos puede variar dependiendo del tema personalizado. Por ejemplo, el color primario del tema es usado como color de fondo por la cabecera, la página de inicio de sesión, y los botones primarios. Si esto causa problemas con el contraste, contacte a su administrador para que le ayude.
:::
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
