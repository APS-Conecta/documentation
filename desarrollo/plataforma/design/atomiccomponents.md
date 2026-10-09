---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Componentes atómicos de la interfaz: botones, menú de acciones, campos de entrada, selectores, etiquetas, modal, avatar, burbujas y estados de carga o vacíos."
---
# Componentes atómicos

## Resumen

Esta página describe los componentes atómicos de la interfaz y cuándo usar cada uno: botones, menú de acciones, campos de entrada, selectores de fecha y de color, etiquetas, modal, avatar, barras de progreso, burbujas de usuario y de contador, contenido vacío y pantallas esqueleto. Está dirigida a quienes diseñan o desarrollan apps.

````{upstream} developer_manual/design/atomiccomponents.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
(nc-dev-buttons)=
### Botones

[Componente Vue de botones](https://nextcloud-vue-components.netlify.app/#/Components/NcButton).
[Botones en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=0&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

Los botones se usan para iniciar acciones en la app. Puede tratarse de una acción primaria, o pueden usarse para confirmar una acción en un diálogo, o simplemente para cualquier acción importante de la app.

Por lo general hay distintos tipos de botones para distintos fines:

- Los botones primarios se usan para indicar la acción principal (el botón «Comenzar llamada» en Talk, «Mover» en Archivos). De forma predeterminada, los botones primarios tienen el estilo del azul de {vendor}`Nextcloud`, o el color de la tematización cuando se ha tematizado. Deben usarse con moderación e, idealmente, solo para 1 acción visible a la vez.
- Los botones secundarios se usan para acciones con menos peso que la acción primaria (el botón «Hoy» en Calendario, «Copiar» en Archivos)
- Los botones terciarios, que son los botones sin fondo, pueden usarse para otras acciones de la app que son importantes, pero no el foco principal. Estos botones suelen combinarse con un botón primario o secundario. Por ejemplo, «Marcar como leído» es un botón terciario que se usa junto a un botón secundario
- Los botones solo con icono pueden usarse si la acción se usa con frecuencia y el icono es fácil de reconocer, de modo que no necesita ningún texto que lo acompañe (las acciones de silenciar/vídeo/compartir pantalla en Talk, y el icono del menú de 3 puntos)
- Los botones de éxito se usan para una acción positiva (el botón «Unirse a la llamada» en Talk)
- Los botones de peligro se usan para indicar una acción potencialmente peligrosa o negativa (el botón «Remove account» del diálogo de confirmación cuando se quiere quitar una cuenta en Correo, o «Borrar conversación» en los ajustes de conversación de Talk)

(nc-dev-action menu)=
### Menú de acciones

[Componente Vue de menú de acciones](https://nextcloud-vue-components.netlify.app/#/Components/NcActions).
[Menú de acciones en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=4&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

El menú de acciones contiene las acciones de uso habitual asociadas a un elemento. Cada entrada del menú de acciones tiene un texto acompañado de un icono adecuado. En algunos casos, el menú de acciones también puede contener:

- casillas de verificación para alternar rápidamente un estado, como en Correo
- botones de opción para elegir entre unas pocas opciones, como las notificaciones del chat en Talk
- elementos de nueva entrada para añadir elementos rápidamente, como añadir un buzón nuevo en Correo
- un segundo nivel de acciones, como para configurar permisos personalizados para los enlaces compartidos en Archivos

Algunas acciones de uso habitual en el menú de acciones son marcar como favorito, renombrar, descargar y eliminar. Eliminar debe estar siempre en la última posición para que no se confunda con otras acciones.

Es importante mantener el menú de acciones sencillo y su longitud al mínimo. Demasiadas entradas en el menú de acciones pueden causar confusión y que las personas no encuentren lo que buscan.

En la mayoría de los casos, al menú de acciones se accede mediante un menú de 3 puntos. En ciertos casos, es mejor usar un icono específico en lugar del icono genérico de 3 puntos. Por ejemplo, en Talk se usa un icono de clip para acceder al menú de acciones para adjuntar un elemento, y en la barra de formato de Text se usa un icono de encabezado para seleccionar el nivel de encabezado.

En Android e iOS, el menú de acciones suele abrirse como una hoja inferior.

(nc-dev-input fields)=
### Campos de entrada

[Componente Vue de campo de entrada](https://nextcloud-vue-components.netlify.app/#/Components/NcFields?id=ncinputfield).
[Campos de texto en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=2&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

(nc-dev-text input)=
#### Entrada de texto

Las entradas de texto suelen usarse para entradas de formato libre. Asegurarse de que la etiqueta de un campo de entrada de texto sea sencilla y clara. También puede ser buena idea usar un texto de marcador de posición en el campo.

(nc-dev-dropdowns)=
#### Desplegables

[Componente Vue de desplegable](https://nextcloud-vue-components.netlify.app/#/Components/NcSelect).
[Desplegables en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=1&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

Los desplegables permiten a la persona usuaria seleccionar uno o varios elementos de una lista. Los desplegables pueden tener opciones predefinidas entre las que la persona usuaria puede seleccionar uno o varios elementos, como se ve en Contactos para seleccionar el tipo de un número de teléfono. Si no hay demasiadas entradas, también se puede pensar en usar en su lugar un conjunto de {nc-ref}`checkboxes and radio buttons`.

Aunque no siempre es necesario, en general es buena idea tener un elemento predeterminado ya seleccionado, sobre todo cuando un menú desplegable es un elemento clave que se va a usar mucho. Esto puede decidirse según varios factores, como el elemento más seleccionado por esa persona usuaria, el elemento seleccionado más recientemente, etc. Por ejemplo, al añadir un número de teléfono nuevo en Contactos, el tipo «Casa» se establece automáticamente en el desplegable.

Otra variante del desplegable permite a la persona usuaria encontrar la opción que prefiere escribiéndola, como en Correo, donde el campo «Para» del editor permite escribir una dirección de correo y, mientras se escribe, muestra un desplegable con los resultados que coinciden con lo introducido. Este tipo de desplegable es útil cuando hay muchas opciones y la persona usuaria ya sabría lo que busca. También puede ser buena idea permitir entradas nuevas si no hay coincidencias.

(nc-dev-checkboxes and radio buttons)=
#### Casillas de verificación y botones de opción

[Componentes Vue de casilla de verificación y botón de opción](https://nextcloud-vue-components.netlify.app/#/Components/NcCheckboxRadioSwitch).
[Casillas de verificación y botones de opción en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=5&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

Las casillas de verificación y los botones de opción son métodos de entrada muy comunes. Se usan sobre todo en el {nc-ref}`action menu`, la {nc-ref}`sidebar` y los {nc-ref}`settings`.

Deben tener una etiqueta concisa, sobre todo si están dentro de un menú de acciones. Si hace falta más explicación, también se puede añadir una línea secundaria.

### Selectores

(nc-dev-datetime picker)=
#### Selector de fecha y hora

[Componente Vue de selector de fecha y hora](https://nextcloud-vue-components.netlify.app/#/Components/NcPickers?id=ncdatetimepicker).

Con el selector de fecha y hora, una persona usuaria puede seleccionar rápidamente fechas, horas e intervalos de fechas. Usar fechas predeterminadas adecuadas y pertinentes para la tarea en curso. Por ejemplo, al establecer una fecha de caducidad, salvo que el servidor imponga algo como predeterminado, 1 semana es un buen valor predeterminado.

(nc-dev-color picker)=
#### Selector de color

[Componente Vue de selector de color](https://nextcloud-vue-components.netlify.app/#/Components/NcPickers?id=nccolorpicker).

En ciertos elementos de la interfaz puede interesar permitir que las personas elijan colores. Esto se consigue fácilmente con un selector de color con algunos colores predefinidos. Hay que ser prudente al usar distintos colores en la interfaz. En la mayoría de las apps de Nextcloud, como Deck y Calendario, los colores definidos por las personas usuarias para los elementos de la interfaz se usan con moderación y se muestran como un círculo junto al elemento al que se refieren.

Además de estos 2 selectores, también existen el [selector de emojis](https://nextcloud-vue-components.netlify.app/#/Components/NcPickers?id=ncemojipicker) y el [selector de zona horaria](https://nextcloud-vue-components.netlify.app/#/Components/NcPickers?id=nctimezonepicker), que también pueden usarse en la app.

(nc-dev-tags)=
### Etiquetas

Las personas usuarias usan las etiquetas para gestionar sus elementos. Pueden colorearse para identificarlas fácilmente, pero hay que asegurarse de usar colores sutiles si las etiquetas de colores son una parte principal de la interfaz, como se ve en Correo.

(nc-dev-modal)=
### Modal

[Componente Vue de modal](https://nextcloud-vue-components.netlify.app/#/Components/NcModal).
[Modales en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=12&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

Un modal es un elemento situado encima de la interfaz principal, y la interacción con el elemento principal queda desactivada.

El modal se usa cuando hay una tarea o una información concreta en la que la persona usuaria necesita concentrarse. Los modales son buena idea si mostrar cierta información en la interfaz principal la recargaría demasiado y la información no depende necesariamente de la interfaz. Los modales también se usan para confirmar al realizar tareas peligrosas, como una eliminación permanente.

Ejemplos de modales son:

- el modal de ajustes de Talk y Correo
- la vista modal de una tarjeta en Deck
- el diálogo de mover o copiar en Archivos
- el selector de archivos en Correo y Talk

En Android e iOS, el contenido que está en un modal se mostraría normalmente como una superposición a pantalla completa, como por ejemplo al redactar un correo nuevo en [Mail de iOS](https://developer.apple.com/documentation/messageui/mfmailcomposeviewcontroller).

(nc-dev-avatar)=
### Avatar

[Componente Vue de avatar](https://nextcloud-vue-components.netlify.app/#/Components/NcAvatar).
[Avatares en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=3&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

Un avatar se usa al referirse a cualquier persona usuaria y muestra su foto o sus iniciales. Al hacer clic en él, el componente de avatar también muestra un menú para esa persona usuaria.

Cuando se usa un avatar, suele ir acompañado también del nombre de la persona usuaria y, a veces, también puede mostrar su estado, aunque no siempre es necesario. Los estados pueden ser útiles cuando la persona usuaria interactúa con otra y espera una respuesta, por ejemplo al @mencionar a otra persona en Talk, o en cualquier vista de compartir.

Cuando varias personas trabajan en el mismo elemento o están asignadas a él, como en Text, Office, una tarjeta de Deck o en la lista de Archivos para compartir, se muestran superpuestas.

(nc-dev-progress bars and meters)=
### Barras de progreso y medidores

[Componente Vue de barra de progreso](https://nextcloud-vue-components.netlify.app/#/Components/NcProgressBar).

Las barras de progreso muestran el progreso de un proceso potencialmente largo, como una subida, una descarga o una sincronización. Al usar una barra de progreso, también puede ser buena idea tener una indicación del progreso en forma de texto, como el porcentaje o el tiempo restante, y asegurarse de dar retroalimentación cuando el proceso haya terminado.

El componente de barra de progreso también se usa a veces como medidor para visualizar datos, como se ve en los ajustes de Archivos para mostrar la cuota.

(nc-dev-user bubbles)=
### Burbujas de usuario

[Componente Vue de burbuja de usuario](https://nextcloud-vue-components.netlify.app/#/Components/NcUserBubble).
[Burbujas de usuario en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=6&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

Al referirse a una persona usuaria dentro del texto de la app, puede usarse un elemento de burbuja de usuario. En Talk y Comentarios, las burbujas de usuario se usan en el contenido cuando alguien menciona a una persona usuaria. En Correo, se usa en la cabecera para los destinatarios del mensaje.

(nc-dev-counter bubbles)=
### Burbujas de contador

[Componente Vue de burbuja de contador](https://nextcloud-vue-components.netlify.app/#/Components/NcCounterBubble).
[Burbujas de contador en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=7&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

En Talk, se usa para mostrar qué chats no están leídos y si se ha mencionado a la persona o a su grupo.

(nc-dev-empty content)=
### Contenido vacío

[Componente de contenido vacío](https://nextcloud-vue-components.netlify.app/#/Components/NcEmptyContent).
[Contenido vacío en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=10&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

El estado de contenido vacío indica que una vista está vacía, p. ej., una carpeta nueva. Sirve para diferenciarlo del estado de carga, o del de haber cargado y mostrar datos.

Asegurarse de que las vistas de contenido vacío solo se muestren cuando la vista está realmente vacía, y no mientras se carga: de lo contrario, las personas se alarmarán preguntándose adónde han ido sus datos. La redacción de la vista de contenido vacío debe ser cercana y ayudar a las personas a salir de la situación, por ejemplo en la app Marcadores.

(nc-dev-skeleton screens)=
### Pantallas esqueleto

Mientras la app se carga, lo mejor es mostrar como indicación de carga una vista esqueleto del contenido probable de la app. Un buen ejemplo de esto es Talk en la web, así como Archivos y Talk en Android.
````
