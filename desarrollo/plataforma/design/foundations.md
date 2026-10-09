---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Elementos de diseño comunes a todas las apps: colores y sus variables por plataforma, tipografía, iconos, nombres de apps y redacción."
---
# Fundamentos

## Resumen

Esta página describe los elementos de diseño comunes a todas las apps: los colores (primario, de fondo, de texto y de estado) con sus valores y variables en cada plataforma, la tipografía, los iconos, cómo nombrar una app y las pautas de redacción. Está dirigida a quienes diseñan o desarrollan apps.

````{upstream} developer_manual/design/foundations.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Hay varios elementos de diseño comunes a todas las apps de Nextcloud. Si se desarrolla para una plataforma que tiene sus propias especificaciones de diseño, por ejemplo Android, conviene tenerlas en cuenta al diseñar la app.

Para las apps web existen la [biblioteca Vue](https://nextcloud-vue-components.netlify.app/) y el [kit de diseño de Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=db3839da-807b-8052-8002-576401e9a376&section=interactions&index=0&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5).

### Color

[Colores en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab128f3ffe2&section=interactions&index=3&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

#### Color primario

#0082C9

Aunque este es el color primario asociado a {vendor}`Nextcloud` y puede usarse para llamar la atención sobre un elemento, es mejor limitar su uso a las acciones primarias y otros elementos importantes.

:::{note}
Quienes administran pueden personalizar el color primario mediante la tematización, pero la experiencia predeterminada será el azul de {vendor}`Nextcloud`. Si el color primario se tematiza con algo muy claro, como un tono de amarillo, el texto o los iconos de la cabecera se invertirán automáticamente a oscuro.
:::

- En la web: `var(--color-primary-element)`
- Android: usa los colores predeterminados de Material Design
- iOS: [systemFill](https://developer.apple.com/documentation/uikit/uicolor/3255070-systemfill)
- Escritorio: [pautas predeterminadas de Qt](https://doc.qt.io/qt-5/qpalette.html#ColorRole-enum)

#### Color de fondo

Fondo para el tema claro: #FFFFFF

Fondo para el tema oscuro: #181818

Las apps de Nextcloud tienen un tema claro y uno oscuro, con colores elegidos de forma adecuada para todos los elementos.

- En la web: `var(--color-main-background)`
- Android: usa los colores predeterminados de Material Design
- iOS: [systemBackground](https://developer.apple.com/documentation/uikit/uicolor/3173140-systembackground)
- Escritorio: [pautas predeterminadas de Qt](https://doc.qt.io/qt-5/qpalette.html#ColorRole-enum)

#### Color del texto

Texto en el tema claro: #222222

Texto en el tema oscuro: #D8D8D8

Este es el color principal del texto en el tema claro y en el tema oscuro.

- En la web: `var(--color-main-text)`
- Android: usa el color predeterminado de Material Design «high emphasis»
- iOS: [label](https://developer.apple.com/documentation/uikit/uicolor/3173131-label) (en UITextView, dejar el textColor predeterminado)
- Escritorio: [pautas predeterminadas de Qt](https://doc.qt.io/qt-5/qpalette.html#ColorRole-enum)

Texto secundario en el tema claro: #767676

Texto secundario en el tema oscuro: #8C8C8C

Además, se usa un color más suave para el texto secundario, como líneas secundarias, marcas de tiempo y similares.

- En la web: `var(--color-text-maxcontrast)`
- Android: usa el color predeterminado de Material Design «medium emphasis»
- iOS: [secondaryLabel](https://developer.apple.com/documentation/uikit/uicolor/3173136-secondarylabel)
- Escritorio: [pautas predeterminadas de Qt](https://doc.qt.io/qt-5/qpalette.html#ColorRole-enum)

#### Estado e indicadores

Información: #006AA3

Éxito: #46BA61

Error: #E9322D

Advertencia: #ECA700

Los elementos de la interfaz asociados a un estado, como información, éxito, error o advertencia, también pueden colorearse para comunicar mejor la acción.

Aunque los elementos de la interfaz, como los botones, se colorean de forma distinta según su acción, el color del texto de ese elemento es casi siempre uno de los colores principales del texto, es decir, claro u oscuro.

- En la web:

  - Color de información: `var(--color-info)`
  - Color de éxito: `var(--color-success)`
  - Color de advertencia: `var(--color-warning)`
  - Color de error: `var(--color-error)`

- Android: pautas de Material Design
- iOS: [colores de las Apple HIG](https://developer.apple.com/design/human-interface-guidelines/ios/visual-design/color/)

  - éxito: systemGreen
  - error: systemRed

- Escritorio: [pautas predeterminadas de Qt](https://doc.qt.io/qt-5/qpalette.html#ColorRole-enum)

### Tipografía

[Tipografía en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab128f3ffe2&section=interactions&index=1&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

Para asegurar la compatibilidad con las distintas plataformas, las apps de Nextcloud usan siempre la fuente nativa del sistema.

Por legibilidad, asegurarse de que el texto del contenido use:

- **Negrita** para dar énfasis
- Un interlineado de entre el 130 % y el 150 %
- El espaciado entre caracteres predeterminado de la fuente
- Nada de *cursiva* ni MAYÚSCULAS, ya que estos estilos de texto son menos legibles

Los tamaños de texto para las distintas plataformas son:

- Web: 16px para el texto principal y las líneas secundarias, **20px en negrita** para los encabezados
- Android: 14sp para el texto principal, 16sp para los encabezados
- iOS: valores de [Dynamic Type Sizes, para el tamaño Large (predeterminado)](https://developer.apple.com/design/human-interface-guidelines/ios/visual-design/typography#dynamic-type-sizes)
- Escritorio: [pautas predeterminadas de Qt](https://doc.qt.io/qt-5/qpalette.html#ColorRole-enum)

### Iconos

[Iconos en Penpot](https://design.penpot.app/#/view/db3839da-807b-8052-8002-576401e9a375?page-id=3f784c86-6c27-80c6-8002-6ab128f3ffe2&section=interactions&index=0&share-id=11fde340-21f4-802e-8002-8d8d305e7ab5)

Los iconos pueden usarse para comunicar la intención de una acción o para dar interés visual a la pantalla. Usamos iconos monocromos en todas las plataformas: [Material Symbols (no Material Icons, y el estilo con contorno predeterminado de 20 px)](https://fonts.google.com/icons?icon.set=Material+Symbols&selected=Material+Symbols+Outlined:search:FILL@0;wght@400;GRAD@0;opsz@20&icon.size=20) para web, Android, Windows y Linux, y [SF Symbols (grosor, escala y variante predeterminados)](https://developer.apple.com/sf-symbols/) para iOS y macOS.

La excepción es el icono de la propia app, que puede ser un icono personalizado. Aun así, la mayoría usa también un icono de app de Material Symbols para mantener la coherencia.

Asegurarse de:

- No abusar de los iconos
- Cuando sea posible, usar texto junto con los iconos para que quede claro a qué se refieren
- En casos especiales, como las advertencias, combinar el icono con un color para realzar su visibilidad

### Nombres

Para que se entiendan de inmediato, elegimos nombres de apps genéricos y fáciles de traducir. Además, son cortos y caben fácilmente en la navegación superior sin cortarse.

Archivos, Contactos, Calendario y Correo no necesitan más explicación, por eso recomendamos elegir un nombre de app que se explique por sí mismo.

Otros buenos ejemplos de esto: Notas, Marcadores, Mapas, Formularios, Tareas, Música.

### Redacción

La redacción y el lenguaje de la app marcan su tono y lo cercana que resulta.

- {vendor}`Nextcloud` debe escribirse siempre completo, y solo con N mayúscula. No «{vendor}`NextCloud`» ni «Nc».
- Ser cercano y accesible, no condescendiente.
- Usar un lenguaje comprensible, no jerga técnica. Por ejemplo, «enlace» es mucho mejor que «URL», y explicar los errores es mejor que mostrar códigos de error.
- No escribir TODO EN MAYÚSCULAS, ya que no es tan legible y da la impresión de estar gritando, lo que resulta agresivo. Usar también mayúscula de oración y no Mayúscula En Cada Palabra, con la excepción de los nombres de productos como Nextcloud Talk, Nextcloud Hub, etc.
- Somos una comunidad, así que es mejor escribir «Nos complace anunciar» en lugar de «Me complace anunciar».
- Si el contenido de la app está vacío, puede ser útil añadir un mensaje atractivo. «¡Añada o importe su primer marcador!» es mucho más agradable que «Aún no hay marcadores».
- Intentar evitar usar «mis» o «sus», como en «Mis archivos» o «Sus archivos», y usar en su lugar «Todos los archivos». En las frases más largas en que no se pueda evitar, usar «su», nunca «mi».
- Usar lenguaje neutro en cuanto al género. Esta [guía internacional de escritura inclusiva en cuanto al género](https://uxcontent.com/the-international-guide-to-gender-inclusive-writing/) contiene información y ejemplos sobre la redacción neutra en cuanto al género en distintos idiomas.
- Usar el nombre completo en lugar de solo el nombre de pila al dirigirse a la persona que usa la app.
- En cualquier acción «Eliminar», dar contexto sobre lo que eliminará, como «Borrar conversación» o «Eliminar usuario», para que quede claro específicamente en esta acción destructiva.
- Mantener un lenguaje breve y conciso, y tener en cuenta que debe ser fácil de traducir.
- Asegurarse de pasar el corrector ortográfico a todo lo que se escriba.
````
