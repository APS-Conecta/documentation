---
tipo: guia
audiencia: usuario
apps: [ia]
resumen: "Pedir a «IA» la revisión de un documento, leer «Para ti» y los boletines y, en un grupo editor, preparar boletines, acciones automáticas y «Documentos»."
---
# «IA»

## Objetivo

«IA» revisa documentos y escribe boletines con el modelo de lenguaje que funciona en el servidor del establecimiento.

- **Revisiones:** antes de compartir un protocolo o una circular, pedir a «IA» que lo revise. El informe lista los errores, las faltas y las partes poco claras, cada una con una sugerencia. El documento no se modifica.
- **«Para ti» y boletines:** leer lo que cambió en los documentos que elige un grupo editor, los protocolos por vencer y lo que concierne al cargo propio.
- **Grupos editores:** quien pertenece a uno además prepara boletines, pone acciones automáticas en carpetas y revisa los documentos vigilados en «Documentos».

«IA» no es un chat: no conversa ni responde preguntas. Conversar con un modelo es tarea del {doc}`asistente-ia` de la plataforma base, que APS Conecta Gestión no instala.

Todo texto que escribe el modelo lleva la marca «Escrito por IA»: el informe de una revisión, el resumen de una edición y la lectura de cada documento. Conviene revisar ese texto antes de actuar sobre él. Las reuniones y los documentos para el cargo de cada persona salen de su calendario y de su cargo, no del modelo.

### Privacidad

- El modelo funciona en el servidor del establecimiento, y «IA» le pide todo a través de la inteligencia artificial de la plataforma.
- «IA» lee solo lo que puede abrir la persona para la que trabaja, y lo comprueba cada vez.
- «IA» nunca lee la carpeta Recursos Humanos (Unidades/Recursos Humanos) ni nada de lo que contiene.
- Una revisión pedida la ve solo quien la pidió, mientras pueda abrir el archivo. Una revisión automática la ve cualquier persona que pueda abrir el archivo.
- Un lector ve una edición solo mientras puede abrir cada documento que esa edición leyó.
- Los informes de revisión se borran a los 90 días, y las ediciones a los 12 meses.

## Requisitos

- Una cuenta en la plataforma, con «IA» instalada. «IA» está en construcción y la suite todavía no la instala (vea {doc}`/administracion/ia/ia`).
- Para revisar un documento y abrir «Para ti», ningún grupo ni rol.
- Para leer un boletín, pertenecer a uno de sus grupos lectores.
- Para preparar boletines y acciones automáticas y abrir «Documentos», pertenecer a un grupo editor. La administración elige los grupos editores.
- Documentos en PDF con texto, DOCX, ODT, TXT o MD. «IA» todavía no lee escaneos: un PDF sin texto, como una fotografía de una página, no se puede revisar.

## Pasos

### Abrir «IA»

1. Abrir **IA** en la barra superior. Se abre en «Para ti».
2. Elegir otra vista en la navegación de la izquierda: **Boletines**, con cada boletín debajo, o **Revisiones**. Quien pertenece a un grupo editor ve además, bajo «Para editores», **Documentos** y **Acciones automáticas**.

Arriba de la navegación está el botón **Revisar un documento**. Quien administra «IA» ve además **Estado** al pie de la navegación.

### «Para ti»

«Para ti» reúne lo que concierne a cada persona en la última edición de cada boletín que lee: sus próximas reuniones, los documentos nuevos o cambiados para su cargo, los protocolos por vencer y las últimas ediciones.

:::{figure} ../capturas/ia-para-ti.png
:alt: «Para ti» con el aviso «Estas listas vienen de tu calendario y de tu cargo, no del modelo», una reunión próxima, tres documentos para el cargo, un protocolo por vencer y la última edición de un boletín.

«Para ti» de una persona que lee un boletín.
:::

| Sección | Contenido |
|---|---|
| «Tus próximas reuniones» | Las reuniones con hora de los calendarios propios que todavía no terminan |
| «Documentos nuevos o cambiados para tu cargo» | Los documentos nuevos o cambiados en la última edición cuya lectura nombra el cargo propio |
| «Protocolos por vencer» | Los documentos de esas ediciones que vencen en los próximos 30 días |
| «Últimas ediciones» | La última edición de cada boletín; cada una se abre en su boletín |

Las reuniones y los documentos para el cargo vienen de los datos, no del modelo, como dice el aviso «Estas listas vienen de tu calendario y de tu cargo, no del modelo.».
Presionar un documento abre su lectura: el resumen, marcado «Escrito por IA», la fecha de vencimiento, los cargos a los que se dirige y el botón **Abrir el documento**.

Quien no lee ningún boletín ve «Todavía no recibes ningún boletín».

### Revisar un documento desde «IA»

1. Presionar **Revisar un documento**.
2. En el selector de archivos, elegir un documento y presionar **Revisar**. El selector muestra solo las carpetas y los formatos que «IA» lee.
3. Se abre la revisión, y un aviso dice cuándo estará lista:
   - «Revisión pedida. Te avisaremos cuando esté lista.»: un documento de hasta 10 páginas se revisa de inmediato, en unos minutos.
   - «Es un documento largo: se revisará fuera de horario, de 22:00 a 06:00. Te avisaremos cuando esté lista.»: un documento de más de 10 páginas espera al horario nocturno que fija la administración.
   - «Tu revisión está lista.»: el documento no cambió desde su última revisión pedida.
4. Cuando la revisión termina, llega la notificación «Revisión lista:», seguida del nombre del documento.

:::{figure} ../capturas/ia-revisar-un-documento.png
:alt: El selector de archivos «Revisar un documento» abierto en la carpeta Borradores, con un PDF elegido y el botón «Revisar».

El selector de archivos de **Revisar un documento**.
:::

### Revisar un documento desde Archivos

1. En **Archivos**, abrir el menú ⋯ de un documento.
2. Elegir **Revisar con IA**. La acción aparece en un solo archivo a la vez, de un formato que «IA» lee, y no en **Archivos eliminados**.
3. El aviso dice cuándo estará lista, como en «IA», con el enlace **Ver en «IA»**, que abre la revisión.

:::{figure} ../capturas/ia-archivos-revisar-con-ia.png
:alt: El menú ⋯ de un PDF en Archivos, con la acción «Revisar con IA».

**Revisar con IA** en el menú de un archivo.
:::

### Leer una revisión

**Revisiones** lista las revisiones pedidas por la propia persona y las automáticas de los archivos que puede abrir, cada una con su estado: «En espera», «En curso», «Lista» o «Falló». Una revisión en curso dice en qué paso va, como «Leyendo el documento y escribiendo la revisión: paso 2 de 3…».

:::{figure} ../capturas/ia-revision.png
:alt: Una revisión lista: «Revisión pedida por ti», los botones «Abrir el documento» y «Revisar de nuevo», las marcas «Escrito por IA» y el número de hallazgos por tipo, y los hallazgos con su cita y su sugerencia.

El informe de una revisión pedida.
:::

El informe dice arriba si la revisión se pidió a mano o es automática, y su fecha. Una revisión automática con instrucciones las muestra, como «El grupo editor pidió revisar además: …».
Bajo la marca «Escrito por IA», cada hallazgo dice:

| Parte | Contenido |
|---|---|
| Tipo | «Error», «Falta» (algo que un documento así debería tener y no tiene) o «Poco claro» |
| Dónde | La parte del documento, o «Todo el documento» |
| Cita | El texto del documento al que se refiere, entre comillas, cuando lo hay |
| Qué pasa | Lo que está mal |
| «Sugerencia» | Cómo corregirlo |

«IA» descarta un hallazgo que cita un texto que no está en el documento.
Si no encontró nada, el informe dice «La revisión no encontró qué corregir».
El documento no se modifica: los cambios se aplican en el editor, con **Abrir el documento**.

Para comprobar las correcciones, presionar **Revisar de nuevo** en una revisión pedida a mano. Una revisión automática se repite sola, fuera de horario, cada vez que el archivo cambia.

### Leer un boletín y sus ediciones

Un boletín resume, para sus lectores, lo que cambió en las fuentes que elige su grupo editor: carpetas, documentos y calendarios. Cada edición se escribe fuera de horario y se publica sin aprobación previa, marcada como escrita por IA. Al publicarse, cada lector recibe la notificación «Nueva edición:», seguida del nombre del boletín.

1. Abrir **Boletines**. La lista muestra cada boletín con «Lo lees» o «Lo editas».
2. Presionar un boletín. Se abre su última edición.
3. Para ver una edición anterior, elegirla en **Edición**. Una edición publicada después de su fecha dice «(atrasada)», y una retirada, «(retirada)».

:::{figure} ../capturas/ia-edicion.png
:alt: La edición de un boletín: el resumen con la marca «Escrito por IA» y las secciones «Para ti en esta edición», «Documentos nuevos y cambiados» y «Protocolos por vencer».

Una edición del boletín semanal.
:::

| Sección | Contenido |
|---|---|
| Resumen | El texto que escribe el modelo, el mismo para cada lector, con la marca «Escrito por IA»; si un editor lo corrigió, dice «Corregida por», seguido de su nombre |
| «Para ti en esta edición» | Las reuniones del periodo en los calendarios propios y los documentos de la edición cuya lectura nombra el cargo propio |
| «Documentos nuevos y cambiados» | Los documentos nuevos o cambiados desde la edición anterior |
| «Protocolos por vencer» | Los documentos que vencen en los próximos 30 días |
| Sin fecha de vencimiento | Los documentos en que «IA» no encontró fecha de vencimiento, bajo el aviso «En estos documentos no encontramos una fecha de vencimiento: revisa si la tienen.» |
| «Fuentes que no se pudieron leer» | Los documentos escaneados, dañados o protegidos con contraseña, que la edición no cubre |

Presionar un documento abre su lectura y, desde ella, el archivo con **Abrir el documento**.
Una edición atrasada lleva la marca «Atrasada»: se publicó después de su fecha. Si el servidor estuvo apagado varias fechas seguidas, el boletín publica una sola edición.

### Preparar un boletín (grupos editores)

Cualquier miembro de un grupo editor prepara, cambia y elimina los boletines de su grupo.

1. En **Boletines**, presionar **Nuevo boletín**. Se abre el panel lateral.
2. Escribir el nombre en «Nombre del boletín».
3. En la pestaña **Fuentes**, elegir el **Grupo editor** y agregar las fuentes con **Agregar carpeta o documento** y **Agregar un calendario**. Todo el grupo editor debe poder abrir cada fuente.
4. En la pestaña **Horario**, elegir **Cada día**, **Cada semana** con su **Día de la semana**, **Cada mes** con su **Día del mes** (del 1 al 28) o **Cuando cambien sus fuentes**.
5. En la pestaña **Lectores**, agregar los **Grupos lectores**. Debajo, una línea dice a cuántas personas llega el boletín y quiénes no lo recibirán porque no pueden abrir una fuente.
6. Presionar **Guardar**.

:::{figure} ../capturas/ia-boletin-fuentes.png
:alt: El panel lateral de un boletín, con su nombre, los botones «Guardar» y «Eliminar», las pestañas «Fuentes», «Horario» y «Lectores», y la carpeta Protocolos como fuente.

La pestaña **Fuentes** de un boletín.
:::

El boletín aparece en la navegación, debajo de **Boletines**. Hasta su primera edición, su página dice cuándo sale, como «La primera edición sale el lunes, 30 de noviembre, escrita fuera de horario la noche anterior.». Mientras una edición se escribe, la página dice en qué paso va.

Cada edición cubre todas sus fuentes. Un documento que no cambió reutiliza su lectura, y un boletín grande sigue en las noches siguientes hasta terminar.
Los editores reciben la notificación «Edición atrasada:» cuando una edición pasa de su fecha, y un aviso cuando una fuente no se pudo leer o ya no está.

Para cambiar un boletín, presionar **Editar** en su página. **Eliminar** lo borra, después de confirmar, y sus lectores dejan de recibirlo.

### Corregir o retirar una edición (grupos editores)

1. En la edición, abrir el menú de acciones junto a su título.
2. Elegir **Corregir el resumen**, cambiar el texto y presionar **Guardar corrección**. Los lectores ven el texto corregido, con la marca «Corregida por» y el nombre de quien lo corrigió.
3. Para que deje de circular, elegir **Retirar esta edición**. Los lectores ya no la ven, ni en «Para ti» ni en el boletín, donde solo leen que fue retirada. **Deshacer** la publica de nuevo.

### Poner una acción automática en una carpeta (grupos editores)

Una acción automática revisa, fuera de horario, cada archivo que se agrega a una carpeta o a sus subcarpetas, que cambia en ella o que llega movido o copiado. Cada archivo se revisa una vez por noche, en su última versión, aunque haya cambiado varias veces.
Quien agregó o cambió el archivo recibe la notificación «Revisión lista:» mientras pueda abrirlo, y la revisión la ve cualquier persona que pueda abrir el archivo.

1. Abrir **Acciones automáticas** y presionar **Nueva acción automática**.
2. Escribir el nombre en «Nombre de la acción» y elegir el **Grupo editor**.
3. Presionar **Elegir carpeta** y elegir una carpeta que todo el grupo editor pueda abrir. Una carpeta admite una sola acción automática.
4. Si hace falta, escribir en «Instrucciones (opcional)» lo que la revisión debe comprobar además, como «comprueba que tenga fecha de vigencia y responsables», en hasta 1000 caracteres.
5. Presionar **Guardar**.

:::{figure} ../capturas/ia-acciones-automaticas.png
:alt: «Acciones automáticas» con una acción en la carpeta «Protocolos de enfermería» y su panel lateral abierto: nombre, carpeta e instrucciones.

Una acción automática y su panel lateral.
:::

Debajo, «Reglas de Flujo» lista, solo para ver, las reglas «Revisar con IA» que crea la administración en Flujo, que revisan igual, fuera de horario.
Eliminar una acción automática deja de revisar los archivos nuevos de la carpeta; las revisiones hechas se conservan.

### Ver «Documentos» (grupos editores)

**Documentos** muestra los documentos que vigilan los grupos editores propios, en las fuentes de sus boletines y en las carpetas de sus acciones automáticas, solo los que la persona puede abrir.

:::{figure} ../capturas/ia-documentos.png
:alt: La tabla «Documentos» con sus filtros y las columnas Nombre, Lectura, Vigencia, Le concierne a y Revisión, y el panel lateral de un documento en la pestaña «Lectura».

«Documentos» con el panel lateral de un documento.
:::

| Filtro | Muestra |
|---|---|
| **Todos** | Todos los documentos vigilados |
| **Nuevos y cambiados** | Los que cambiaron en los últimos 7 días |
| **Por vencer** | Los que vencen en los próximos 30 días o no tienen fecha de vencimiento |
| **Con hallazgos** | Aquellos cuya última revisión encontró algo |
| **Para mi cargo** | Aquellos cuya lectura nombra el cargo propio |

La columna **Lectura** dice «Leído», «Sin leer», «Escaneado, sin texto» o «No se pudo leer»; **Vigencia**, la fecha de vencimiento o «Sin fecha»; y **Revisión**, cuántos hallazgos tiene la última revisión.
«IA» hace la lectura de cada documento (resumen, vencimiento y cargos) una vez por versión, fuera de horario, y la usan todos los boletines.

Presionar una fila abre su panel lateral, con **Abrir en Archivos** y tres pestañas: **Lectura**, **Revisión**, con los hallazgos de la última revisión y **Ver la revisión completa** (o **Revisar ahora** si no la tiene), y **Aparece en**, con las ediciones en que aparece.

## Verificación

- Tras pedir una revisión, **Revisiones** la muestra «En espera» o «En curso» y, al terminar, «Lista», con la notificación «Revisión lista:».
- Un lector ve la última edición de cada boletín que lee en «Últimas ediciones» de «Para ti».
- Tras guardar un boletín, aparece en la navegación debajo de **Boletines**, y su página dice cuándo sale su primera edición.
- Tras guardar una acción automática, aparece en **Acciones automáticas** con su carpeta.

## Problemas frecuentes

| Lo que se ve | Qué significa | Qué hacer |
|---|---|---|
| «Por ahora «IA» revisa archivos PDF, DOCX, ODT, TXT y MD.» | El archivo tiene otro formato | Guardar el documento en uno de esos formatos y pedir la revisión de nuevo |
| «Es un documento escaneado: «IA» todavía no lee escaneos.» | El PDF no tiene texto, solo imágenes | Usar una versión del documento con texto |
| «No se pudo leer: puede estar dañado o protegido con contraseña.» | El archivo no se abre sin contraseña, o está dañado | Guardar una copia sin contraseña |
| ««IA» no lee la carpeta Recursos Humanos ni nada de lo que contiene.» | El archivo o la carpeta está en Unidades/Recursos Humanos | Nada: «IA» nunca lee esa carpeta |
| «La revisión falló» | El modelo no pudo terminarla | Presionar **Revisar de nuevo** más tarde; si vuelve a fallar, avisar a quien administra «IA» |
| «Esta revisión ya no está: puede que ya no puedas abrir el archivo.» | La persona ya no puede abrir el archivo, o el informe se borró | Pedir acceso al archivo a quien lo comparte |
| «Esta edición ya no está, o ya no puedes leerla: …» | La persona ya no puede abrir uno de los documentos de la edición | Pedir acceso al documento a quien lo comparte |
| «Todo el grupo editor debe poder abrir cada fuente, y «…» no la puede abrir: …» | Una persona del grupo editor no puede abrir esa fuente | Compartir la fuente con todo el grupo editor |
| «Esa carpeta ya tiene una acción automática.» | Una carpeta admite una sola acción automática | Cambiar la acción que ya tiene |
