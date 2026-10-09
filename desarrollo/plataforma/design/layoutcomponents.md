---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Componentes de disposición de una app: navegación y sus partes, ajustes, elemento de lista, contenido (vistas y tamaños) y barra lateral con sus pestañas."
---
# Componentes de disposición

## Resumen

Esta página describe los componentes reutilizables que forman la disposición de una app: la navegación (botón de acción principal, entradas, elemento para nuevos elementos y ajustes), el elemento de lista, el contenido con sus vistas y tamaños, y la barra lateral con sus pestañas de detalles, actividad y compartir. Está dirigida a quienes diseñan o desarrollan apps.

````{upstream} developer_manual/design/layoutcomponents.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Todas las apps de Nextcloud se construyen con componentes individuales reutilizables, por coherencia y eficiencia. Actualmente, estos componentes están escritos en Vue y se encuentran en el [repositorio nextcloud-vue en Github](https://github.com/nextcloud/nextcloud-vue/), con la documentación disponible en [la guía de estilo de los componentes Vue de {vendor}`Nextcloud`](https://nextcloud-vue-components.netlify.app/).

### Navegación

[Componente Vue para la navegación de la app](https://nextcloud-vue-components.netlify.app/#/Components/App%20containers/NcAppNavigation?id=ncappnavigation-1).

[Elementos de navegación en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=8&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

La navegación de la izquierda ofrece a las personas usuarias una forma de moverse por las distintas secciones de la app.

La navegación consta de 4 elementos principales:

- Botón de acción principal
- Entradas de navegación
- Elemento para nuevos elementos (opcional)
- Menú de ajustes (opcional)

#### Botón de acción principal

[Componente Vue AppNew de la navegación](https://nextcloud-vue-components.netlify.app/#/Components/App%20containers/NcAppNavigation?id=ncappnavigationnew).

[Botones en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=0&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

En la mayoría de las apps, el primer elemento de la navegación es el botón de acción principal. Por ejemplo:

- Correo tiene un botón «Nuevo mensaje» para redactar un correo nuevo
- Contactos tiene un botón «Nuevo contacto»
- en Talk, se puede crear una conversación nueva
- en Calendario hay un botón «New event»
- Formularios tiene una acción «New form»

#### Entradas de navegación

[Componente Vue de entradas de navegación](https://nextcloud-vue-components.netlify.app/#/Components/App%20containers/NcAppNavigation?id=ncappnavigationitem).

[Elementos de navegación en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=8&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

Las distintas secciones de la app se organizarían mediante distintas entradas de navegación. Por ejemplo, la app Archivos contiene distintas categorías de archivos en su navegación, y la app Contactos contiene distintos grupos y círculos. Al crear la navegación, asegurarse de que las entradas de esta sección:

- sean fáciles de entender
- se usen con frecuencia
- estén organizadas
- no cambien de posición con frecuencia

Lo ideal es que las entradas de navegación de primer nivel tengan un icono adecuado justo a su izquierda. Opcionalmente, también pueden tener:

- un menú de acciones de 3 puntos (como en Correo)
- un contador (como en Contactos y Correo)

Es posible un subnivel de navegación, pero puede hacer que las entradas sean difíciles de descubrir. Solo se aconseja si realmente hay una jerarquía, como en las carpetas de Correo o News.

#### Elemento para nuevos elementos

[Componente Vue de nuevo elemento](https://nextcloud-vue-components.netlify.app/#/Components/App%20containers/NcAppNavigation?id=ncappnavigationnewitem).

Las personas usuarias pueden crear fácilmente un elemento nuevo con un nombre adecuado mediante el elemento para nuevos elementos. Este elemento puede usarse en la navegación, como en el caso de Deck, o en el contenido. Otras apps que lo usan:

- «Create a new group» en Contactos
- «Add mailbox» en Correo
- «Nuevo calendario» en Calendario

(nc-dev-settings)=
#### Ajustes

[Componente Vue de ajustes](https://nextcloud-vue-components.netlify.app/#/Components/App%20containers/NcAppNavigation?id=ncappnavigationsettings).

[Modales en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=12&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

Los ajustes específicos de cada persona usuaria para la app pueden mostrarse en un modal de ajustes, al que se accede mediante una entrada de ajustes en la parte inferior de la navegación. Intentar mantener los ajustes al mínimo, ya que demasiadas opciones configurables pueden ser una carga para la persona usuaria. Si la app no necesita ajustes, eso es estupendo y el modal de ajustes puede omitirse. Dentro del modal, clasificar los ajustes en categorías puede ofrecer a veces una mejor experiencia si hay muchos ajustes. Si es necesario, las categorías se colocan a la izquierda del modal de ajustes.

También se puede incluir una entrada «Ayuda» en los ajustes de la app y ofrecer información sencilla sobre la app y cómo usarla. Algunas apps, como Talk y Correo, también incluyen atajos de teclado, si la persona usuaria no los ha desactivado.
Para comprobarlo se puede usar la función global de javascript `OCP.Accessibility.disableKeyboardShortcuts()`.

Ver también: {nc-ref}`Modal`

(nc-dev-list)=
### Elemento de lista

[Componente Vue de elemento de lista](https://nextcloud-vue-components.netlify.app/#/Components/NcListItems).

[Elemento de lista en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=9&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

Los elementos de lista pueden usarse para mostrar una colección de elementos entre los que se puede seleccionar uno. Se ven elementos de lista en la lista de chats de la izquierda en Talk, así como en la lista de mensajes de Correo y en la lista de contactos de Contactos. Los elementos de lista suelen tener un avatar o un icono descriptivo, una línea principal y, opcionalmente, una línea secundaria. Un elemento de lista también puede contener:

- un {nc-ref}`Action menu` con las acciones de uso habitual para ese tipo de elemento
- una burbuja de contador: Talk, por ejemplo, usa un contador de mensajes no leídos

(nc-dev-content)=
### Contenido

La sección de contenido de la app ocupa la mayor parte del espacio de la pantalla y es el núcleo de lo que hace la app. El contenido de cada app es único, pero hay que asegurarse de que siga algunas reglas básicas, como la adaptabilidad, la accesibilidad y la compatibilidad con distintos idiomas, para que todo el mundo pueda usarlo. La disposición del contenido depende de lo que haga la app, ya que el contenido de casi todas las apps de Nextcloud tiene un aspecto distinto. Para el contenido de la app debe usarse el [componente Vue appContent](https://nextcloud-vue-components.netlify.app/#/Components/App%20containers?id=appcontent).

#### Vistas

Algunas apps ofrecen distintas vistas de su contenido para que las personas puedan elegir una preferencia, que debería recordarse automáticamente. Es importante pensar cuál debe ser la predeterminada y si conviene tener distintas vistas, ya que la mayoría de las personas no cambia la predeterminada.

- Archivos (web, Android e iOS), Marcadores: vista de lista o vista de cuadrícula
- Calendario: vista de mes, vista de semana, vista de día, vista de lista / agenda
- Talk (web, Android e iOS): vista de orador y vista de cuadrícula en una llamada

El contenido es también la sección en la que se puede explicar rápidamente a las personas cómo empezar a usar la app, por ejemplo con un componente atómico {nc-ref}`Empty content`.

#### Tamaño

En las apps basadas en texto, como el chat, los correos y otros párrafos de texto, el ancho del contenido no debe superar cierto ancho, para facilitar la lectura. En Nextcloud Text, por ejemplo, el ancho está limitado a 650px, y lo hacemos de forma similar en Correo y Talk, aunque el tamaño de la pantalla sea mayor.

En cada elemento en el que se pueda hacer clic de la interfaz, asegurarse de que tenga un área de clic mínima de al menos 44px por 44px (48px en Android). Cualquier tamaño menor hará que la app sea inaccesible y difícil de usar en el móvil, ya que las personas usuarias podrían fallar al intentar tocar el elemento.

El espaciado entre los elementos de la app debe ser en múltiplos de 4px.

(nc-dev-sidebar)=
### Barra lateral

[Componente Vue de la barra lateral](https://nextcloud-vue-components.netlify.app/#/Components/App%20containers/NcAppSidebar?id=ncappsidebar-1).

[Barra lateral en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=11&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

Los detalles de una entrada concreta del contenido, así como algunas acciones asociadas a ella, se muestran en la barra lateral derecha. En las apps que usan la barra lateral, esta solo se abre cuando hace falta. La barra lateral nunca se usa en la disposición de 3 columnas (navegación + lista + contenido). Contiene la información principal y, a veces, una vista previa del elemento seleccionado, así como un máximo de 3 pestañas posibles.

Las pestañas de uso habitual en la barra lateral son:

#### Detalles

[Componente Vue de pestañas de la barra lateral](https://nextcloud-vue-components.netlify.app/#/Components/App%20containers/NcAppSidebar?id=ncappsidebartabs).

[Barra lateral en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab157b6bd27&section=interactions&index=11&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

La pestaña de detalles contiene información sobre la entrada a la que se refiere, que a menudo puede editarse mediante distintos campos de entrada. Los detalles que se incluyen aquí dependen de la app. Por ejemplo, la pestaña de detalles de la barra lateral de la app Calendario contiene información sobre el evento seleccionado, como la ubicación, la descripción y el estado. Ver también {nc-ref}`Input fields` en la sección de componentes atómicos para más detalles sobre los distintos campos de entrada que pueden usarse aquí.

#### Actividad

Los cambios importantes hechos en el elemento seleccionado, así como los comentarios que dejan las personas usuarias, se muestran en la pestaña de actividad. Estos detalles se muestran con la actividad más reciente arriba.

Si la app admite comentarios, el cuadro de entrada «Write comment» debe colocarse aquí para que quede bien integrado.

Si existe la posibilidad de restaurar versiones anteriores, puede integrarse mediante un menú de acciones de 3 puntos en cualquier actividad pasada.

#### Compartir

La pestaña de compartir permite a las personas usuarias compartir el elemento seleccionado con otras personas de distintas formas. Un elemento puede compartirse con usuarios o grupos concretos de la instancia simplemente seleccionando con quién se quiere compartir. Otra forma muy sencilla de compartir es mediante un enlace compartido, que opcionalmente también puede configurarse con la opción «Advanced settings».
````
