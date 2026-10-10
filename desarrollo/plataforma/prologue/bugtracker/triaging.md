---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo hacer el triaje de informes de errores en GitHub: buscar duplicados, juzgar relevancia y completitud, reproducirlos y etiquetarlos."
---
# Triaje de errores de Nextcloud

## Resumen

Esta página explica cómo hacer el triaje de los informes de errores en GitHub: qué es, cómo encontrar errores que revisar, cómo comprobar si un informe es útil (duplicados, relevancia, completitud, reproducción) y cómo etiquetarlo. Está dirigida a quienes quieren contribuir revisando informes de errores.

````{upstream} developer_manual/prologue/bugtracker/triaging.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El triaje de errores es el proceso de revisar los informes de errores para ver si siguen siendo válidos (puede que el problema se haya resuelto desde que se informó del error), reproducirlos cuando sea posible (para asegurarse de que realmente es un problema de Nextcloud y no un problema de configuración) y, en general, asegurarse de que el error resulte útil para un desarrollador que quiera corregirlo. Si el error no es útil y ni quien lo informó originalmente ni quien hace el triaje pueden completarlo, hay que cerrarlo.

### Por qué sumarse

¡Ayudar a reducir el número de incidencias facilita que quienes desarrollan dediquen su tiempo de forma productiva y, por tanto, quienes hacen el triaje de errores **contribuyen enormemente al desarrollo de Nextcloud**! El triaje de un error no lleva mucho tiempo, así que el trabajo llega en pequeñas porciones y no hacen falta muchos conocimientos, solo algo de paciencia y, a veces, perseverancia.

¡Quienes hacen el triaje de errores y contribuyen de forma significativa deberían pedir que se les incluya como colaboradores activos en la página de [nextcloud.com](https://nextcloud.com)!

### Cómo se hace el triaje de errores

El proceso de revisar, reproducir y cerrar las incidencias no válidas se llama «triaje de errores». Las incidencias se pueden clasificar en uno de estos tres tipos:

1. Errores o solicitudes de funcionalidades que incluyen toda la información necesaria para que un desarrollador pueda corregirlos o trabajar en ellos
2. Informes de errores o solicitudes de funcionalidades incompletos o duplicados
3. Informes de errores o solicitudes de funcionalidades irrelevantes o erróneos

La tarea de quien hace el triaje es identificar las incidencias de la categoría 1 para que las revisen quienes desarrollan, ayudar a eliminar, fusionar o mejorar cualquier incidencia de la categoría 2 hasta convertirla en una de la categoría 1, y descartar las incidencias de la categoría 3 de forma amable y empática.

El triaje sigue estos pasos:

- Encontrar una incidencia que alguien debería revisar
- Ser ese alguien y ver si el contenido de la incidencia es útil para un desarrollador
- Responder y cerrar, hacer una pregunta, añadir información o una etiqueta
- ¡Buscar el siguiente error pendiente y repetir!

### Consideraciones generales

- Se necesita una [cuenta de GitHub](https://github.com) para contribuir al triaje de errores.
- Si no se está familiarizado con la interfaz del gestor de incidencias de GitHub (que {vendor}`Nextcloud` usa para gestionar los informes de errores), [esta guía puede resultar útil](https://guides.github.com/features/issues/).
- Al principio solo se podrá comentar en las incidencias. La posibilidad de cerrar incidencias o asignar etiquetas se concederá con generosidad a quienes han demostrado estar dispuestos a contribuir y ser capaces de hacerlo.
- Leer [nuestras pautas para informar de errores](https://github.com/nextcloud/server/blob/master/CONTRIBUTING.md#submitting-issues) para saber cómo debe ser un buen informe y dónde va cada cosa. La [plantilla de incidencias](https://raw.github.com/nextcloud/server/master/issue_template.md) pide específicamente cierta información que quienes desarrollan necesitan para resolver las incidencias.
- ¡A veces puede que incluso ya esté corregido! También puede ser fructífero contactar con quienes desarrollan. Decirles que se está haciendo el triaje de errores y compartir con qué problema se ha tropezado.
- Para que no haya dos personas trabajando en la misma incidencia, pedimos simplemente añadir un comentario como «I am triaging this» en la incidencia en la que se quiere trabajar y, al terminar, antes o después de ejecutar las acciones de triaje, indicar del mismo modo que se ha terminado.

  > Para poder etiquetar y cerrar incidencias se necesita acceso al repositorio. En los repositorios del núcleo y de la app de sincronización, esto también implica haber firmado el acuerdo de contribución. Sin embargo, no es realmente necesario para el triaje, ya que se puede comentar al terminar el triaje y otra persona puede ejecutar esas acciones.

### Encontrar errores para el triaje

GitHub ofrece varias consultas de búsqueda que pueden ser útiles para encontrar una lista de errores que merecen una revisión más detallada:

- [Los errores comentados hace más tiempo](https://github.com/search?q=is%3Aissue+user%3Anextcloud+is%3Aopen+sort%3Aupdated-asc+is%3Apublic+)
- [Las incidencias con menos comentarios](https://github.com/search?q=is%3Aissue+user%3Anextcloud+is%3Aopen+no%3Aassignee+no%3Amilestone+no%3Alabel+sort%3Acomments-asc+)
- [Errores que necesitan información](https://github.com/search?q=is%3Aissue+user%3Anextcloud+is%3Aopen+label%3A%22Needs+info%22+sort%3Acreated-asc+)

Pero hay más métodos. Por ejemplo, quien use Nextcloud con una configuración específica, como nginx como servidor web, un almacenamiento externo personalizado o la app de cifrado, puede buscar errores con esas palabras clave. Luego puede usar su conocimiento de su instalación y la propia instalación para ver si los errores son (aún) válidos o para reproducirlos.

Una vez elegida una incidencia, añadir un comentario indicando que se ha empezado el triaje:

> «I am triaging this bug»

### Comprobar si la incidencia es útil

Gran parte del contenido procede de <https://community.kde.org/Guidelines_and_HOWTOs/Bug_triaging>

El objetivo del triaje es que quienes desarrollan solo tengan informes de errores útiles. Y no hace falta saber mucho para poder juzgar que al menos algunos informes de errores son poco útiles. Hay duplicados, informes incompletos, etc. Este es el flujo de trabajo para cada error. La imagen muestra un diagrama del flujo de triaje de errores con los pasos para evaluar y clasificar los informes de incidencias.

Repasemos cada paso.

#### Encontrar duplicados

Para encontrar duplicados, la herramienta de búsqueda de GitHub es la primera parada.
En [esta pantalla](https://github.com/nextcloud/server/issues) se pueden buscar fácilmente algunas palabras clave del informe de error.
Si se encuentran otros errores con el mismo contenido, decidir cuál es el mejor informe de error (a menudo el más antiguo o aquel en el que uno o más desarrolladores ya han empezado a implicarse y a discutir el problema).
Ese es el informe de error «principal»; ahora se puede cerrar el otro (o comentar que se puede cerrar como duplicado).

Si el informe de error que se estaba revisando contiene información adicional, se puede añadir esa información al informe de error «principal» en un comentario.
Mencionar este informe de error (con #\<número del informe de error>) para que un desarrollador pueda consultar el informe original, ya cerrado, y quizá pedir allí información adicional a quien informó inicialmente.

Si no se encuentra nada, buscar en los informes de errores cerrados.
¡Puede que el problema ya esté resuelto y figure allí!
Por supuesto, esos otros informes de errores pueden haberse cerrado como duplicados del que se está revisando ahora; si no se encuentra uno resuelto ni ningún duplicado, se puede pasar al siguiente paso.
En caso de duda, basta con añadir un comentario: «might be a duplicate of #\<bug nr here>» suele ser suficiente.

Cuando la incidencia es una solicitud de funcionalidad, se puede ayudar del mismo modo: fusionar las solicitudes relacionadas añadiendo la información de una a la otra y cerrando la primera.

:::{note}
Ser cortés: cuando haya que pedir información o comentarios, hacerlo con claridad y cortesía, y se obtendrá más información en menos tiempo. ¡Pensar en cómo le gustaría a uno que lo trataran si fuera quien informa de un error!
:::

:::{note}
Se puede responder de forma más rápida y amable usando una de [estas plantillas](https://gist.github.com/jancborchardt/6155185#clean-up-inactive-issues).
:::

:::{note}
A menudo, nuestro gestor de incidencias de GitHub es un lugar de debate sobre soluciones. Ser amable e inclusivo, y respetar la postura de los demás.
:::

#### Determinar la relevancia de la incidencia

No todas las incidencias son relevantes para Nextcloud. Los errores pueden deberse a una configuración específica o a plataformas no compatibles. Las Raspberry Pi sufren tiempos de espera agotados de SQLite, nginx tiene problemas que Apache no tiene y Microsoft Server con IIS no tiene un buen soporte. Aunque los problemas externos no siempre son motivo para cerrar un informe, asegurarse de que estén claros: ¿usa el usuario la plataforma «estándar»? Pedir esa información si falta.

Por último, pero no por ello menos importante, el problema puede deberse a que el usuario hace algo que simplemente no funciona. Aquí puede ser útil el conocimiento general que se tenga de Nextcloud; si es el caso, a menudo se puede cerrar rápidamente la incidencia con un comentario sobre lo que salió mal.

:::{note}
Puede que haya que decir que no a algunas solicitudes, por ejemplo cuando un problema se ha resuelto en una versión nueva pero no estará disponible para la versión que usa quien lo informó, o cuando se ha elegido una solución que no satisface a quien lo informó. Ser considerado. La gente tiene opiniones sorprendentemente fuertes sobre Nextcloud, y hay que tener cuidado de explicar que no pretendemos ignorarla; al contrario. Pero a veces las decisiones que benefician a la mayoría de los usuarios no ayudan a una persona concreta. La extensibilidad y la libre disponibilidad del código de Nextcloud están para aliviar lo que duelan esas decisiones.
:::

#### Determinar si el informe está completo

Ahora que se sabe que el informe de error es único y que no se trata de un problema externo, hay que comprobar que está toda la información necesaria.

¡Consultar [nuestras pautas para informar de errores](https://github.com/nextcloud/server/blob/master/CONTRIBUTING.md#submitting-issues) y asegurarse de que los informes de errores las cumplen! La información que pide la [plantilla de incidencias](https://raw.github.com/nextcloud/server/master/issue_template.md) es necesaria para que quienes desarrollan resuelvan las incidencias.

Una vez añadida una solicitud de más información, añadir una etiqueta #needinfo.

Si se ha pedido más información en el informe, ya sea quien hace el triaje, un desarrollador u otra persona, pero quien lo informó originalmente (u otra persona que pueda tener la respuesta) no ha respondido en 1 mes o más, se puede cerrar la incidencia. ¡Ser cortés e indicar que quien pueda responder a la pregunta puede reabrir la incidencia!

#### Reproducir la incidencia

Un paso importante del triaje de errores es intentar reproducir los errores, es decir, usar la información que quienes informaron añadieron al informe de error para provocar (recrear, reproducir, repetir) el error en la aplicación.

Esto es necesario para distinguir los errores aleatorios o de condición de carrera de los reproducibles (que quienes desarrollan también pueden reproducir, y que pueden corregir).

Si no se puede reproducir una incidencia en una versión más reciente de Nextcloud, lo más probable es que esté corregida y se pueda cerrar. Comentar que no se ha conseguido reproducir el problema y, si quien la informó puede confirmarlo (o no responde durante mucho tiempo), se puede cerrar la incidencia. Además, no olvidar añadir con qué se probó exactamente: ¿con la rama Master de Nextcloud o con una rama (y, en ese caso, cuándo), o con una versión publicada y, en ese caso, cuál?

#### Finalizar y etiquetar

Una vez terminado el intento de reproducir una incidencia, es hora de rematar el trabajo y dejar claro a quienes desarrollan qué pueden hacer:

- Si es un error genuino (o se está bastante seguro de que lo es), añadir la etiqueta «bug».
- Si es una solicitud de funcionalidad genuina (o se está bastante seguro de que lo es), añadir la etiqueta «enhancement».
- Si la incidencia está claramente relacionada con algo específico, poner la etiqueta de esa funcionalidad concreta y @mencionar a un mantenedor

Ahora, quienes desarrollan pueden hacerse cargo de la incidencia. Hay que tener en cuenta que, aunque nos gustaría hacernos cargo de los problemas y resolverlos siempre con prontitud, no todas las áreas de Nextcloud reciben la misma atención y las mismas contribuciones, así que esto a veces puede llevar mucho tiempo.

**Créditos:** este documento está en deuda con la extensa [guía de KDE sobre el triaje de errores](https://community.kde.org/Guidelines_and_HOWTOs/Bug_triaging).
````
