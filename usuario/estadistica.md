---
tipo: guia
audiencia: usuario
apps: [estadistica]
resumen: "Ver las Metas Sanitarias del establecimiento de un vistazo, consultar sus cifras REM frente al país y a sus pares, y guardarlas en preguntas y tableros."
---
# Estadística

## Objetivo

Ver de un vistazo, en el **Resumen**, dónde está el establecimiento en cada una de sus Metas Sanitarias.
Consultar en **Estadística** las cifras REM del establecimiento al lado del promedio nacional y del de establecimientos parecidos, los pares.
Guardar esas consultas como preguntas y reunirlas en tableros para el resto del personal.
Seguir mes a mes el avance de las Metas Sanitarias de Atención Primaria.

Las cifras son las que el DEIS publica para todos los establecimientos del país, etiquetadas con el diccionario oficial de cada año.
Estadística guarda solo conteos agregados que publican el DEIS y FONASA, o que el establecimiento escribe en su propia planilla REM: no contiene información de pacientes.
Un archivo de FONASA que trae una columna de más, como un RUT o un nombre, se rechaza entero y no se guarda nada de él.
La aplicación no llena ni valida la planilla REM, y no lee las series BS, BM ni D.
Quien administra Estadística además carga y mantiene las cifras, la carpeta de planillas del establecimiento, la población de FONASA y los compromisos de las Metas Sanitarias desde **Administración → Estadística**.

## Requisitos

- Una cuenta en APS Conecta Gestión. Estadística es consultable por todo el personal: cualquier cuenta consulta, guarda preguntas y crea tableros.
- Cifras REM cargadas. La aplicación las descarga sola del DEIS en segundo plano, y quien administra Estadística también las carga desde un archivo; mientras no haya ninguna, **Consultar** muestra «Todavía no hay cifras REM».
- Para ver las cifras propias, el establecimiento configurado en la instalación. Lo define el instalador de la suite: ninguna pantalla permite elegir otro centro como «el propio».
- Para elegir pares por sus rasgos, la Base de Establecimientos del DEIS cargada.

## Pasos

### Abrir Estadística

1. Abrir **Estadística** en la barra superior. Se abre en **Resumen**.
2. Elegir otra de sus cinco vistas en la navegación de la izquierda si hace falta: **Metas Sanitarias**, **Consultar**, **Preguntas** o **Tableros**.
   En un teléfono la navegación se pliega; se abre con el botón **Abrir navegación**, en la esquina superior.

Si la instalación no tiene su establecimiento configurado, un aviso lo dice arriba: «Esta instalación todavía no tiene su establecimiento configurado: verá las cifras nacionales y de pares, pero no las propias».

### Resumen

El **Resumen** muestra las Metas Sanitarias más nuevas cargadas, una tarjeta por meta, con las cifras del propio establecimiento en el año más reciente con cifras y en cada año anterior comparable.
Mientras el año de esas metas no tiene cifras, como las metas 2027 cargadas en octubre de 2026, se cuentan sobre las cifras del año anterior.

La aplicación trae las metas 2027 de la Res. Exenta 732: el Resumen muestra «Meta I 2027» a «Meta VIII 2027», contadas sobre las cifras de 2026.
Hasta que el MINSAL publique las Orientaciones Técnicas 2027, cada meta con cifras REM dice «Esperando ruta oficial», «Sin porcentaje: esperando ruta oficial» y «Sin meta mínima 2027: esperando ruta oficial», y la Meta VIII muestra su cumplimiento informado y «Meta mínima 2027: 100,0 %».
Mientras alguna meta espera su ruta oficial, un aviso arriba de las tarjetas lo dice, «Las metas tendrán cifras cuando MINSAL confirme sus rutas REM», con el botón **Ver las Metas Sanitarias 2026**, que abre la vista **Metas Sanitarias** en el año anterior a las metas.

Arriba de las tarjetas, una sola línea dice hasta qué mes tiene cifras del establecimiento cada serie del REM que cuentan las metas, como «REM Serie A: datos al octubre de 2026 · REM Serie P: corte de junio de 2026».
Si ninguna serie tiene cifras todavía, como mientras las metas 2027 esperan sus rutas oficiales, la línea dice «Metas Sanitarias 2027: sin cifras todavía».

Arriba de las tarjetas puede aparecer una **nota**: un texto breve sobre lo que cambió desde el cálculo anterior del Resumen, con sus cifras.
La escribe un modelo de IA, y debajo dice «Escrita por un modelo de IA a partir de las cifras».

Sobre las tarjetas, un recuadro por estado dice cuántas metas lo tienen, como «2 Cumplen», y **Todas las metas** las cuenta todas; solo aparece el recuadro de un estado que alguna meta tiene.
Presionar un recuadro muestra solo las metas de ese estado, y debajo una línea dice cuántas se ven, como «2 metas: no cumplen.»; un lector de pantalla la anuncia.

Cada tarjeta dice:

| Parte | Contenido |
|---|---|
| Meta | «Meta», su número y el año de las metas, como «Meta I 2027» |
| Título | El nombre de la meta. Si la meta tiene histórico, el título es un botón que lo abre y lo cierra dentro de la tarjeta |
| Cifra | El porcentaje del último mes con cifra y, a su lado, el numerador y el denominador, como «58,3 % 7 de 12». Debajo, una barra con el porcentaje y una marca en la meta, como «meta 50 %» |
| Estado | Un ícono y una palabra: «Cumple» o «No cumple» la meta comprometida, o la meta nacional si no hay meta comprometida; «Falta el denominador oficial»; «Esperando ruta oficial», o «Sin informar». El color acompaña a la palabra, nunca la reemplaza |
| Bajo el estado | La distancia a la meta en puntos, como «+8,3 puntos frente a la meta comprometida (50 %).», o por qué la meta no tiene porcentaje |
| Meta mínima | «Meta mínima 2027: 70,8 % — referencia: la meta la fija el Servicio de Salud», y debajo el año del cierre del que sale, como «Desde el cierre 2025.» |
| Histórico | Al abrirlo desde el título, un gráfico con una línea por año comparable, la del año más reciente destacada, y la meta como línea discontinua. Debajo, la tabla con el porcentaje de cada mes por año, su numerador y su denominador, y el **Cierre** de cada año terminado |

Para leer las tarjetas:

- Un mes sin ningún número escrito en las celdas de la meta no tiene cifra, y nunca se muestra como 0: la tarjeta muestra el último mes que sí la tiene, y «Sin informar» con «Nadie informó esta meta en el periodo.» si ninguno la tiene.
- «Sin porcentaje: esperando ruta oficial» dice que las Orientaciones Técnicas del año todavía no confirman cómo se cuenta esa meta en el REM.
- «Sin porcentaje: falta el denominador oficial de 2026», con el año de las cifras, dice que la meta cuenta personas en un rango de edad que corta los tramos de FONASA, y que quien administra Estadística todavía no escribe su **Denominador comprometido** de ese año. La tarjeta muestra igual el numerador ya contado, como «140 en el numerador, a octubre de 2026», o en una meta de REM Serie P «al corte de junio de 2026». Un año anterior en esa situación lo dice bajo el gráfico, como «2025: falta el denominador oficial de 2025».
- Cada año anterior se cuenta con la ruta de las metas más nuevas, corrida en años enteros. La ventana de octubre a septiembre de la Meta I se corre igual.
- Un año dice «sin datos comparables» bajo el gráfico, y no muestra cifras, cuando su diccionario del REM nombra de otra forma alguna prestación o columna de la ruta, aparte de mayúsculas, tildes y plurales. Lo mismo ocurre cuando ese año no tiene diccionario propio, o cuando la ruta necesita meses anteriores al primer año que guarda la instalación.
- En el gráfico, un mes sin cifra es un hueco en la línea, nunca 0, y la tabla dice «sin informar». Las metas de REM Serie P se dibujan en sus cortes de junio y diciembre; un corte que el establecimiento no informó es un hueco, nunca el corte anterior repetido.
- El **Cierre** de un año terminado es su porcentaje de diciembre: lo sumado en su periodo hasta diciembre en REM Serie A, el corte de diciembre en REM Serie P. Un año sin corte de diciembre no tiene cierre.
- La **Meta mínima** es la meta comprometida más baja que permite la resolución de metas, desde el **Cierre** del último año terminado con diciembre publicado: el de 2025 hasta que se publica diciembre de 2026. Es una referencia: la meta comprometida la fija el Servicio de Salud. Con la Res. Exenta 732:
  - Meta I: cerrar al menos el 30 % de la distancia a la meta nacional, y no menos de 60 %;
  - Meta II: cerrar el 30 % de la distancia a 80 % si el cierre alcanzó la meta comprometida de ese año para la Meta II, y el 40 % si no; un cierre de 40 % o menos se compromete al menos a 50 %;
  - Metas III a VI: cerrar al menos el 50 % de la distancia a la meta nacional;
  - Meta VII: 80 %, y Meta VIII: 100 %.

  Un cierre igual o mayor que la meta nacional se mantiene. La meta mínima se calcula exacta y se muestra con un decimal.
- Sin la meta comprometida del año del cierre, la Meta II cierra el 40 % y lo dice, como «Desde el cierre 2025; sin la meta comprometida 2025, se cierra el 40 % de la brecha.»
- Una meta sin cifra no tiene meta mínima y dice por qué, como «Sin meta mínima 2027: esperando ruta oficial», «Sin meta mínima 2027: falta el denominador oficial de 2025» o «Sin meta mínima 2027: no hay cierre comparable de 2025».
- La Meta VIII no tiene cifras REM: su cifra es el cumplimiento que se escribió a mano, sin numerador ni denominador, y sin él dice «Todavía no se ha informado su cumplimiento.».
- El Resumen muestra solo las cifras del propio establecimiento. Las nacionales y las de pares están en **Metas Sanitarias** y en **Consultar**.
- La nota dice solo qué cifras cambiaron, sin causas ni consejos. Se muestra solo cuando cada número que trae es una cifra del Resumen tal como la muestran las tarjetas, o un año o un mes que el Resumen nombra; si no, no hay nota. El modelo recibe solo las cifras agregadas que cambiaron, nunca datos de pacientes.
- Sin un servicio de generación de texto conectado a Nextcloud no hay nota, y el resto del Resumen se ve igual.
- La cifra de una tarjeta, su porcentaje con el numerador y el denominador, y cada cifra de su tabla, el **Cierre** incluido, se puede presionar o elegir con el teclado. Abre, en la barra lateral, de dónde sale la cifra en su mes y su año:
  - el origen del mes y su fecha, como «Origen: datos públicos DEIS, con cifras hasta noviembre de 2026», o «Origen: planilla del establecimiento, guardada el 9 de noviembre de 2026» en un mes que cubre una planilla;
  - para el numerador y el denominador, el nombre de su fuente, como «REM Serie A», y el periodo de ese año, y los códigos que se suman y los que se restan, cada uno con su hoja, su sección y sus columnas, con los nombres del diccionario de ese año;
  - para un denominador que no sale del REM, «Población inscrita validada (FONASA)» o «Lo comprometió el establecimiento»;
  - la referencia de las metas: la resolución y las Orientaciones Técnicas que las fijan.

  La barra lateral se cierra con Escape o con su botón de cerrar, y el teclado vuelve a la cifra.
- El Resumen se calcula en segundo plano después de cada carga de cifras REM, de metas o de la población de FONASA, de cada planilla que se lee o se quita de la carpeta y de cada cambio en los compromisos o en la **Población de su establecimiento**, y todos ven las mismas cifras hasta el cálculo siguiente.

### Cifras REM

Una consulta se arma en cuatro pasos, **1. Datos**, **2. Filtrar**, **3. Resumir** y **4. Visualizar**, y se hace al presionar **Consultar**, no antes.
Al abrirse, **Consultar** propone el año cargado más reciente, de enero al último mes con cifras, agrupado por **Mes** y comparado con **Todo el país**.
Los pasos quedan a la izquierda y el resultado a su derecha, a la vista mientras se recorren los pasos; en una pantalla angosta, el resultado queda debajo de ellos.

1. Abrir **Consultar** en la navegación.
2. En **1. Datos**, elegir la fuente: **REM Serie A** o **REM Serie P**.
3. En **2. Filtrar**, elegir el primer mes en **Desde**.
4. Elegir el último mes en **Hasta**.
5. Elegir la **Hoja del REM**, por ejemplo la hoja A03.
6. Elegir la **Sección** de esa hoja.
7. Elegir las prestaciones en **Prestaciones (vacío: todas las de la sección)**, o dejar el campo vacío para sumar la sección completa.
8. Elegir al menos una columna en **Columnas que se suman**.
9. En **3. Resumir**, elegir hasta dos dimensiones en **Agrupar por (hasta 2)**.
10. Elegir la **Métrica**: **Suma** o **Promedio por establecimiento**.
11. En **4. Visualizar**, elegir en **Mostrar como** una forma: **Barras**, **Líneas** o **Solo tabla**.
12. Presionar **Consultar**.

La Serie A es mensual.
La Serie P es un corte: sus filas traen solo los meses 6 y 12, y cuentan a las personas en control a esa fecha.
Bajo cada fuente se lee su origen, los años cargados y el mes hasta el que llegan sus cifras.
Una hoja con una sola sección la deja elegida.
En lugar de los pasos 5 a 7, **Buscar una prestación** encuentra una prestación por su código o por parte de su nombre, sin importar tildes ni mayúsculas, y lista hasta 50.
Al elegir una, quedan elegidas su hoja y su sección, y la prestación se agrega a **Prestaciones (vacío: todas las de la sección)**.
Las dimensiones de **Agrupar por (hasta 2)** son **Año**, **Mes**, **Prestación**, **Columna** y los rasgos del establecimiento: **Tipo de establecimiento**, **Dependencia**, **Nivel de atención**, **Servicio de salud**, **Región** y **Comuna**.
Mientras falte algo, el botón **Consultar** queda inactivo y a su lado se lee qué falta, por ejemplo, «Elija una hoja del REM».

Cuando un año no trae un diccionario que se pueda leer, sus hojas y columnas son las del diccionario del año posterior más cercano, y la pantalla lo avisa.
Una prestación que ningún diccionario nombra aparece como «sin descripción».

### Comparación nacional y de pares

La comparación pone las cifras en las mismas filas, en tres series: **Su establecimiento**, **Nacional** y **Pares**.
**Nacional** reúne a todos los establecimientos que informaron.
**Pares** reúne a los establecimientos que comparten los rasgos elegidos: el valor elegido de la lista, o el mismo valor del propio establecimiento.

Antes de presionar **Consultar**:

1. En **3. Resumir**, bajo **Comparar con**, marcar **Todo el país**.
2. En un rasgo que deben compartir los pares, elegir un valor de la lista, o **Igual que su establecimiento**.
3. Dejar en **Sin usar** los rasgos que no cuentan.

Cada valor de un rasgo muestra entre paréntesis cuántos establecimientos lo tienen.
La **Comuna** se elige solo como **Igual que su establecimiento**.
Al comparar dos o más series, la métrica es siempre **Promedio por establecimiento**: la suma de todo el país no se puede poner al lado de la de un solo establecimiento.
El promedio por establecimiento es la suma dividida por los informantes, y un informante es un establecimiento que informó al menos una de las celdas elegidas en el periodo.

Para leer el resultado:

- La línea «Fuente: …» dice de qué fuente vienen las cifras y hasta qué mes llegan.
- Todo gráfico trae debajo su tabla, con las mismas cifras.
- En las series **Nacional** y **Pares**, el número entre paréntesis es la cantidad de establecimientos que informaron.
- Una celda sin cifra muestra una raya.
- «Qué se contó» despliega cada prestación sumada, con su hoja, su sección y sus columnas.
- Bajo la tabla, una línea dice el código DEIS del propio establecimiento y otra, los rasgos que comparten los pares.
- Con dos dimensiones, cada valor de la segunda tiene su propio gráfico; con más de 12 valores, las cifras quedan solo en la tabla.
- Si algún año de la fuente está incompleto, un aviso dice que el DEIS lo publicó cortado y que sus cifras pueden quedar bajo lo real.

### Guardar una consulta como pregunta

1. Escribir un título en **Título de la pregunta**, bajo el resultado.
2. Presionar **Guardar como pregunta**.
3. Abrir **Preguntas** en la navegación.
4. Presionar **Ver** en la pregunta para hacerla de nuevo con las cifras de hoy.

Lo que se guarda queda visible para todo el personal.
La pregunta guarda la consulta tal como se hizo y la forma en que se muestra.
Cada pregunta de la lista muestra su autor y la fecha de su último cambio.
Quien creó una pregunta, y quien administra Estadística, ven además su menú de acciones, con **Editar** y **Eliminar**.
**Editar** cambia el **Título** y **Mostrar como**; para cambiar lo que la pregunta consulta, se guarda una pregunta nueva desde **Consultar**.
**Eliminar** pide confirmación en un diálogo que avisa que los tableros que muestran la pregunta dirán que fue eliminada.

### Reunir preguntas en un tablero

1. Abrir **Tableros** en la navegación.
2. Escribir un título en **Título del nuevo tablero**.
3. Presionar **Crear tablero**.
4. Elegir una pregunta en **Pregunta guardada**.
5. Presionar **Agregar una pregunta**.
6. Abrir el menú de acciones de una tarjeta para ordenarla con **Subir** y **Bajar**, elegir su ancho (**1 columna**, **2 columnas** o **3 columnas**) o **Quitar** la tarjeta del tablero.

El tablero recién creado queda abierto.
Los demás tableros se abren eligiéndolos en **Tablero**, que muestra a su autor al lado.
Cada cambio se guarda al hacerlo, y un tablero tiene hasta 24 tarjetas.
Cada tarjeta hace su propia consulta: si una falla, las demás siguen mostrándose.
Si alguien elimina una pregunta que el tablero muestra, su tarjeta dice «Esta pregunta fue eliminada. Quien edita el tablero puede quitar la tarjeta».
Quien creó el tablero, y quien administra Estadística, pueden **Cambiar el título** o **Eliminar el tablero**; eliminar un tablero pide confirmarlo y no elimina sus preguntas.

### Metas Sanitarias

La vista muestra las Metas Sanitarias del año (Ley 19.813), una fila por meta, que se abre en su tabla mes a mes.

1. Abrir **Metas Sanitarias** en la navegación.
2. Elegir el año en **Año**, cuando hay metas cargadas de más de un año. La vista parte en el año en curso, y las metas 2027 se eligen ahí.
3. Marcar, bajo «Pares: los establecimientos que comparten con el suyo», los rasgos que deben compartir los pares.

Los pares se eligen solo cuando la instalación tiene su establecimiento configurado, y la vista parte con **Tipo de establecimiento** marcado.
Si se desmarcan todos los rasgos, la columna **Pares** desaparece.

Cada fila dice:

| Parte | Contenido |
|---|---|
| Meta | Su número y su nombre |
| Meta y peso | La meta con que se juzga, la comprometida por el establecimiento o, si no hay, la nacional, y el peso de la meta |
| Gráfico | Los porcentajes de los meses del año frente a esa meta, en pequeño |
| Última cifra | El porcentaje del último mes con cifra, o el cumplimiento informado; una raya si no hay |
| Estado | Un ícono y una palabra, como en el Resumen: «Cumple», «No cumple», «Falta el denominador oficial», «Esperando ruta oficial» o «Sin informar» |

Presionar una fila la abre y cierra la que estaba abierta. La fila abierta dice:

| Parte | Contenido |
|---|---|
| Indicador | Lo que mide la meta |
| Metas y peso | La meta nacional, la meta comprometida por el establecimiento («Sin meta comprometida» si no hay) y el peso de la meta, con una raya si la resolución de metas no lo fija, como en 2027 |
| Denominador | La población inscrita validada por FONASA a una fecha de corte, o la cifra que el establecimiento comprometió |
| Tabla | Una fila por mes, con **Numerador**, **Denominador**, **Su establecimiento**, **Frente a la meta comprometida**, **Frente a la meta nacional**, **Nacional** y **Pares** |

Para leer la tabla:

- Las metas que se cuentan en la Serie P se miden en sus cortes de junio y diciembre: cada mes muestra el último corte hasta ese mes, y no hay cifra antes de junio.
- Un mes que el DEIS todavía no publica aparece con una raya.
- En las columnas de su establecimiento, un mes de la Serie A posterior al último que su establecimiento informó aparece con una raya, aunque otros establecimientos ya lo hayan informado. La línea de las fuentes, bajo el nombre de las metas, dice hasta qué mes llegan las cifras de cada serie y hasta cuál informó su establecimiento.
- **Frente a la meta comprometida** y **Frente a la meta nacional** dan la diferencia en puntos: con «+» sobre la meta y con «−» bajo ella.
- Un año sin corte propio de FONASA usa el último corte anterior más un 3 %, y lo dice.
- Toda cifra es oficial. Una meta que cuenta personas en un rango de edad que corta los tramos de FONASA no tiene porcentaje, ni propio, ni nacional, ni de pares, y dice «Sin porcentaje: falta el denominador oficial de 2027», con el año de las metas. Cuando quien administra Estadística escribe su **Denominador comprometido**, aparece el porcentaje de su establecimiento; el nacional y el de pares siguen vacíos.
- La Meta VIII no tiene cifras REM: muestra el «Cumplimiento informado» que se escribió a mano.
- La aplicación no calcula un cumplimiento global: el oficial es el de la SEREMI.
- Las cifras **Nacional** y **Pares** suman a todos los establecimientos que informaron: es el mismo cálculo para todos, no la evaluación de la SEREMI.
- Sin establecimiento configurado, la tabla no trae las columnas propias.

### Administrar Estadística

Esta parte es para quien administra Estadística: los administradores de la plataforma y los grupos a los que se delega la sección en **Administración → Privilegios de administración**.
Todo está en **Administración → Estadística**; los administradores de la plataforma llegan también desde **Ajustes de Estadística**, al pie de la navegación de la app.

Arriba, la sección dice qué establecimiento sirve la instalación.
Ese establecimiento se define en el instalador, no en esta pantalla.
Si dice «Todavía no se ha configurado el establecimiento de esta instalación», avisar a quien instaló la suite.

#### Años de historia nacional

1. Elegir el **Primer año** de cifras nacionales que se guardan, hasta el año en curso.
2. Leer cuánto ocupará en la base de datos y en cada respaldo.
3. Presionar **Guardar**.

Los años se cargan o se quitan en segundo plano.
Si el nuevo primer año deja fuera años ya cargados, o un ZIP que espera cargarse, la pantalla lo avisa y pide confirmar antes de guardar.

#### Cifras REM cargadas

La tabla **Cifras REM cargadas** muestra cada año y serie con su origen (el DEIS o un archivo cargado a mano), su estado, su fecha de corte, sus filas, sus códigos «Sin descripción» y su último intento.
La fecha de corte es hasta cuándo llegan las cifras de una fuente.
Un año que el DEIS publicó cortado figura como incompleto: se cargan solo sus filas enteras, se muestra igual y el motivo queda escrito en esta tabla.

La aplicación revisa el DEIS una vez al día y carga una serie por hora.
Si una carga falla, sigue mostrándose la carga anterior y la tabla dice por qué falló.
Más abajo se ve la Base de Establecimientos en uso.

#### Planillas del establecimiento

El establecimiento guarda en una carpeta de **Archivos** el formulario REM del DEIS que llena cada mes, en `.xlsm` o `.xlsx`: una planilla por serie y mes.

1. Crear la carpeta en **Archivos**, o usar una compartida con quienes llenan las planillas.
2. Presionar **Elegir la carpeta en Archivos…** y elegirla.

La sección muestra «Carpeta: «…», en los archivos de …».
La carpeta se revisa cada hora como la persona que la eligió, así que se lee solo lo que esa persona puede ver.
Cada archivo de la carpeta aparece con su estado:

| Estado | Qué significa |
|---|---|
| Leída: Serie A, marzo de 2026 | La planilla se leyó con el diccionario de su año |
| Reemplazada por una más reciente | Hay otra planilla de la misma serie y mes guardada después, y cuenta la más reciente |
| Rechazada: … | No se leyó, y el motivo dice por qué: es de otro establecimiento, su versión del formulario no es la del diccionario de ese año, no es un formulario REM del DEIS, o el archivo no se puede leer. Una planilla de un año cuyo diccionario el DEIS todavía no publica espera: se lee sola cuando el DEIS publica el primer archivo de ese año, con las cifras de enero, así que no hace falta volver a guardarla |

Las macros de la planilla nunca se ejecutan: solo se leen sus celdas.
Un archivo que se quita de la carpeta deja de contar.
Por cada serie y mes, la planilla más reciente reemplaza las cifras del DEIS en las del propio establecimiento: en el **Resumen**, en **Metas Sanitarias** y en **Consultar**.
Una celda en blanco de la planilla queda sin informar, aunque el DEIS tenga un número.
Los meses sin planilla, las cifras nacionales y las de pares siguen siendo las del DEIS.

#### Población inscrita validada (FONASA)

FONASA no publica su población inscrita en un archivo que se pueda descargar solo, así que se carga a mano.
Hay dos caminos:

- Cargar el CSV «Inscritos APS» que exporta el reporte de FONASA, con **Cargar un archivo a mano**.
- Escribir en **Población de su establecimiento** las cifras del establecimiento por tramo de edad y sexo, para el corte al 31 de diciembre del año elegido, cuando FONASA todavía no las entrega o para corregirlas.

Una casilla en blanco usa la cifra de FONASA, que se ve en gris.
Lo escrito vale solo para el establecimiento propio: el país y los pares siguen con las cifras de FONASA.
Un año sin corte propio usa el último corte anterior multiplicado por 1,03.

#### Compromisos de las Metas Sanitarias

1. Elegir el año en **Metas de**.
2. Escribir la **Meta comprometida (%)** de cada meta.
3. Escribir el **Denominador comprometido** de las metas que se cuentan sobre población, si se comprometió otro que la población de FONASA. Una meta cuyo rango de edad corta los tramos de FONASA solo tiene denominador con él.
4. Escribir el **Cumplimiento (%)** de las metas que se informan a mano, como la Meta VIII.
5. Presionar **Guardar**.

Una casilla en blanco no compromete nada.
La **Meta comprometida (%)** de la Meta II del año del cierre decide qué regla sigue su **Meta mínima** en el Resumen.

La sección dice cuándo se calculó el Resumen en uso.
Si su último cálculo falló, lo dice con el motivo, y sigue en uso el anterior.

#### Cargar un archivo a mano

Para lo que la instalación no descarga sola:

1. Subir el archivo a **Archivos**.
2. Elegirlo en **Cargar un archivo a mano**.

El archivo se revisa al momento, y uno que no sea de los cuatro tipos siguientes se rechaza sin guardar nada.

| Archivo | Cuándo queda en uso |
|---|---|
| El ZIP de cifras REM que publica el DEIS, por ejemplo `SERIE_REM_2024.zip` | En segundo plano, una serie por hora, igual que una descarga automática |
| La Base de Establecimientos del DEIS (.xlsx) | De inmediato |
| El CSV «Inscritos APS» de FONASA | De inmediato. Un archivo con columnas de más o de menos, por ejemplo un RUT o un nombre, se rechaza entero y dice cuáles sobran y cuáles faltan |
| Un archivo de Metas Sanitarias (.json), como el que la aplicación trae para 2026 | De inmediato: crea o reemplaza las metas de su año, y lo comprometido para ese año se mantiene |

Cada octubre, cuando el Ministerio publica las Orientaciones Técnicas del año siguiente, se carga así el archivo nuevo, sin actualizar la aplicación.

## Verificación

- La consulta muestra la línea «Fuente: …» y, bajo el gráfico, la tabla con las mismas cifras.
- Al guardar una pregunta, un aviso dice que «quedó guardada en Preguntas», y la pregunta aparece en **Preguntas** con su autor y la fecha de hoy.
- Estadística se abre en **Resumen**, marcada en la navegación, con una tarjeta por meta.
- La vista **Metas Sanitarias** muestra una fila por meta, con su última cifra y su estado, y cada fila se abre en su tabla mes a mes.
- Tras cargar un archivo a mano, la tabla **Cifras REM cargadas** o la sección correspondiente de **Administración → Estadística** muestra lo cargado, o dice por qué se rechazó.

## Problemas frecuentes

| Lo que se ve | Qué significa | Qué hacer |
|---|---|---|
| «Todavía no hay cifras REM» | Todavía no se carga ningún año | Avisar a quien administra Estadística, que lo revisa en «Cifras REM cargadas» |
| Faltan las cifras propias | La instalación no tiene su establecimiento configurado | Avisar a quien instaló la suite |
| «Base de Establecimientos: todavía no se ha cargado, así que no hay pares con qué comparar» | Falta el registro de establecimientos del DEIS | Avisar a quien administra Estadística |
| Una meta sin porcentaje | Falta la población de FONASA de ese año, o el mes todavía no se publica | Avisar a quien administra Estadística si falta la población |
| No aparece la nota | Nextcloud no tiene un servicio de generación de texto conectado, las cifras no cambiaron en el último cálculo, o el texto del modelo traía un número que no está en el Resumen | Nada: las tarjetas muestran las cifras igual |
| «Sin porcentaje: esperando ruta oficial» | Las Orientaciones Técnicas del año todavía no confirman la ruta REM de esa meta | Esperar la versión de las metas que la confirma |
| «Sin meta mínima 2027: no hay cierre comparable de 2025» | Ese año no tiene cifra de diciembre del establecimiento, o no es comparable | Abrir el histórico desde el título de la tarjeta y revisar qué le falta a ese año |
| «Todavía no hay Metas Sanitarias cargadas» | No hay metas cargadas hasta el año en curso | Avisar a quien administra Estadística, que las carga como un archivo en «Cargar un archivo a mano» |
| «La consulta se canceló antes de terminar» | La consulta superó el límite de 10 s | Acotar el periodo, las prestaciones o la comparación |
| «No se encuentra la carpeta de planillas elegida» | La carpeta se borró, o quien la eligió ya no tiene acceso a ella | Elegir otra carpeta en «Planillas del establecimiento» |
| Un mensaje de error rojo | Dice qué falló | Si pide recargar la página y el problema sigue, avisar a quien administra Estadística |
| «Si este mensaje no desaparece, la aplicación no pudo cargar: avise al administrador» | La aplicación no llegó a abrirse en el navegador | Avisar a quien administra la instalación |
