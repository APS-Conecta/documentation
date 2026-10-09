---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Disposiciones habituales de una app web: navegación, contenido y barra lateral, sus casos especiales, y navegación, lista y contenido, también en móvil."
---
# Disposición

## Resumen

Esta página explica qué tener en cuenta al decidir el aspecto de una app y describe las disposiciones más usadas en la interfaz web: navegación → contenido → barra lateral, con sus casos especiales, y navegación → lista → contenido, incluido su comportamiento en el móvil. Está dirigida a quienes diseñan o desarrollan apps.

````{upstream} developer_manual/design/layout.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Estas pautas de disposición se centran principalmente en nuestra interfaz web. En Android e iOS seguimos de cerca las pautas de cada plataforma, es decir, [Material Design](https://material.io/design) y las [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/).

Al decidir qué aspecto se quiere dar a la app, hay varios factores que considerar:

- La coherencia con otras apps de Nextcloud
- La adaptabilidad a distintos navegadores, tamaños de navegador y dispositivos
- Los patrones de interfaz típicos de otras apps similares del mercado

El [componente Vue de contenido](https://nextcloud-vue-components.netlify.app/#/Components/App%20containers/NcAppContent?id=ncappcontent-1) envuelve toda la app. Aunque la disposición de los componentes en la app depende de lo que haga la app, la mayoría de las apps de Nextcloud suelen tener 3 niveles de jerarquía. Algunas disposiciones de uso habitual son:
[Plantilla vacía en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=2783d7ad-98f2-804a-8002-750c2585d4f1&section=interactions&index=5&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

- Navegación → contenido → barra lateral (y un par de variantes, p. ej., sin la barra lateral)
- Navegación → lista → contenido

### Navegación → contenido → barra lateral

[Disposición de Archivos en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=2783d7ad-98f2-804a-8002-750c2585d4f1&section=interactions&index=3&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

Esta disposición se usa en Archivos, Calendario, Deck y Tareas.

Esta disposición tiene la {nc-ref}`Navigation` a la izquierda, el {nc-ref}`Content` en el centro y una {nc-ref}`Sidebar` a la derecha. El contenido principal depende de la navegación, y la barra lateral, que está cerrada de forma predeterminada, contiene los detalles de un elemento del contenido principal.

Por ejemplo, en la app Archivos, los archivos del contenido principal varían según lo que se seleccione en la navegación. La barra lateral se abriría cuando la persona usuaria quisiera ver los detalles de un archivo.

En el móvil, el contenido se muestra de forma predeterminada. La navegación y la barra lateral pueden desplegarse mediante iconos a los lados.

#### Caso especial: sin barra lateral

Normalmente, se usa una barra lateral para mostrar más información sobre un elemento. A veces no es necesaria, como en el caso de Actividad. Entonces, la disposición tendrá solo una navegación y el contenido principal.

#### Caso especial: lista en la navegación

[Disposición de Talk en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=2783d7ad-98f2-804a-8002-750c2585d4f1&section=interactions&index=0&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

Otra variante de esta disposición es aquella en la que el {nc-ref}`List` de entradas ocupa el espacio de la izquierda en lugar de la navegación, como se ve en Talk. Muestra la lista de chats a la izquierda, y el contenido principal contiene los mensajes de un chat, mientras que al abrir la barra lateral derecha se muestran los detalles de un chat, como la descripción y los participantes. Talk también contrae la lista de la izquierda y la barra lateral derecha durante una videollamada, de modo que toda la pantalla quede ocupada solo por la llamada.

### Navegación → lista → contenido

Esta disposición se usa en Correo y Contactos.

En esta disposición, los 3 niveles de jerarquía se muestran de forma predeterminada. A la izquierda está la {nc-ref}`Navigation`, justo a su lado hay un {nc-ref}`List` de entradas para la navegación elegida, y el contenido principal corresponde a la entrada seleccionada en la lista.

Un buen ejemplo de esta disposición está en la app Correo. La sección de navegación de la izquierda contiene las distintas bandejas de entrada y categorías. La lista muestra entonces los correos de la bandeja de entrada o carpeta seleccionada, y el contenido principal muestra el contenido del correo que está abierto en ese momento.

En el móvil, la lista se muestra de forma predeterminada. La navegación puede desplegarse mediante un icono en la parte superior izquierda, y el contenido puede abrirse seleccionando una entrada de la lista. La vuelta atrás desde un contenido puede hacerse mediante una acción de flecha «Atrás» en la parte superior izquierda, en lugar del icono de navegación.
````
