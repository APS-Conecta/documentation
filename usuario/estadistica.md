---
tipo: guia
audiencia: usuario
apps: [estadistica]
resumen: "Consultar las cifras REM del establecimiento frente al país y a sus pares, guardarlas en preguntas y tableros, y seguir las Metas Sanitarias mes a mes."
---
# Estadística

## Objetivo

Consultar en **Estadística** las cifras REM del establecimiento al lado del promedio nacional y del de establecimientos parecidos, los pares.
Guardar esas consultas como preguntas y reunirlas en tableros para el resto del personal.
Seguir mes a mes el avance de las Metas Sanitarias de Atención Primaria.

Las cifras son las que el DEIS publica para todos los establecimientos del país, etiquetadas con el diccionario oficial de cada año.
Estadística guarda solo conteos agregados que publican el DEIS y FONASA: no contiene información de pacientes.
Un archivo de FONASA que trae una columna de más, como un RUT o un nombre, se rechaza entero y no se guarda nada de él.
La aplicación no llena ni valida la planilla REM, y no lee las series BS, BM ni D.

## Requisitos

- Una cuenta en APS Conecta Gestión. Estadística es consultable por todo el personal: cualquier cuenta consulta, guarda preguntas y crea tableros.
- Cifras REM cargadas. La aplicación las descarga sola del DEIS en segundo plano, y quien administra Estadística también las carga desde un archivo; mientras no haya ninguna, **Consultar** muestra «Todavía no hay cifras REM».
- Para ver las cifras propias, el establecimiento configurado en la instalación. Lo define el instalador de la suite: ninguna pantalla permite elegir otro centro como «el propio».
- Para elegir pares por sus rasgos, la Base de Establecimientos del DEIS cargada.

## Pasos

### Abrir Estadística

1. Abrir **Estadística** en la barra superior.
2. Elegir una de sus cuatro pestañas: **Consultar**, **Preguntas**, **Tableros** o **Metas Sanitarias**.

Si la instalación no tiene su establecimiento configurado, un aviso lo dice arriba: «Esta instalación todavía no tiene su establecimiento configurado: verá las cifras nacionales y de pares, pero no las propias».

### Cifras REM

Una consulta se arma en cuatro pasos, **1. Datos**, **2. Filtrar**, **3. Resumir** y **4. Visualizar**, y se hace al presionar **Consultar**, no antes.
Al abrirse, la pestaña propone el año cargado más reciente, de enero al último mes con cifras, agrupado por **Mes** y comparado con **Todo el país**.

1. Abrir la pestaña **Consultar**.
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
3. Abrir la pestaña **Preguntas**.
4. Presionar **Ver** en la pregunta para hacerla de nuevo con las cifras de hoy.

Lo que se guarda queda visible para todo el personal.
La pregunta guarda la consulta tal como se hizo y la forma en que se muestra.
Cada pregunta de la lista muestra su autor.
Quien creó una pregunta, y quien administra Estadística, ven además **Editar** y **Eliminar**.
**Editar** cambia el **Título** y **Mostrar como**; para cambiar lo que la pregunta consulta, se guarda una pregunta nueva desde **Consultar**.

### Reunir preguntas en un tablero

1. Abrir la pestaña **Tableros**.
2. Escribir un título en **Título del nuevo tablero**.
3. Presionar **Crear tablero**.
4. Elegir una pregunta en **Agregar una pregunta guardada**.
5. Presionar **Agregar tarjeta**.
6. Ordenar las tarjetas con **Subir** y **Bajar**.
7. Elegir el ancho de cada tarjeta: **1 columna**, **2 columnas** o **3 columnas**.
8. Presionar **Quitar** en una tarjeta para sacarla del tablero.

El tablero recién creado queda abierto.
Cada cambio se guarda al hacerlo, y un tablero tiene hasta 24 tarjetas.
Cada tarjeta hace su propia consulta: si una falla, las demás siguen mostrándose.
Si alguien elimina una pregunta que el tablero muestra, su tarjeta dice «Esta pregunta fue eliminada. Quien edita el tablero puede quitar la tarjeta».
Quien creó el tablero, y quien administra Estadística, pueden **Cambiar el título** o **Eliminar el tablero**; eliminar un tablero no elimina sus preguntas.

### Metas Sanitarias

La pestaña muestra las Metas Sanitarias del año (Ley 19.813), una tarjeta por meta, cada una con su tabla mes a mes.

1. Abrir la pestaña **Metas Sanitarias**.
2. Elegir el año en **Año**, cuando hay metas cargadas de más de un año.
3. Marcar, bajo «Pares: los establecimientos que comparten con el suyo», los rasgos que deben compartir los pares.

Los pares se eligen solo cuando la instalación tiene su establecimiento configurado, y la pestaña parte con **Tipo de establecimiento** marcado.
Si se desmarcan todos los rasgos, la columna **Pares** desaparece.

Cada tarjeta dice:

| Parte | Contenido |
|---|---|
| Título | «Meta» con su número y su nombre, y debajo su indicador |
| Metas y peso | La meta nacional, la meta comprometida por el establecimiento («Sin meta comprometida» si no hay) y el peso de la meta |
| Denominador | La población inscrita validada por FONASA a una fecha de corte, o la cifra que el establecimiento comprometió |
| Tabla | Una fila por mes, con **Numerador**, **Denominador**, **Su establecimiento**, **Frente a la meta comprometida**, **Frente a la meta nacional**, **Nacional** y **Pares** |

Para leer la tabla:

- Las metas que se cuentan en la Serie P se miden en sus cortes de junio y diciembre: cada mes muestra el último corte hasta ese mes, y no hay cifra antes de junio.
- Un mes que el DEIS todavía no publica aparece con una raya.
- **Frente a la meta comprometida** y **Frente a la meta nacional** dan la diferencia en puntos: con «+» sobre la meta y con «−» bajo ella.
- Un año sin corte propio de FONASA usa el último corte anterior más un 3 %, y lo dice.
- Una meta que cuenta personas en un rango de edad que corta los tramos de FONASA dice que su población está «estimada por prorrateo de los tramos de edad».
- La Meta VIII no tiene cifras REM: muestra el «Cumplimiento informado» que se escribió a mano.
- La aplicación no calcula un cumplimiento global: el oficial es el de la SEREMI.
- Las cifras **Nacional** y **Pares** suman a todos los establecimientos que informaron: es el mismo cálculo para todos, no la evaluación de la SEREMI.
- Sin establecimiento configurado, la tabla no trae las columnas propias.

## Verificación

- La consulta muestra la línea «Fuente: …» y, bajo el gráfico, la tabla con las mismas cifras.
- Al guardar una pregunta, un aviso dice que «quedó guardada en Preguntas», y la pregunta aparece en la pestaña **Preguntas** con su autor.
- La pestaña **Metas Sanitarias** muestra una tarjeta por meta, con su tabla mes a mes.

## Problemas frecuentes

| Lo que se ve | Qué significa | Qué hacer |
|---|---|---|
| «Todavía no hay cifras REM» | Todavía no se carga ningún año | Avisar a quien administra Estadística, que lo revisa en «Cifras REM cargadas» |
| Faltan las cifras propias | La instalación no tiene su establecimiento configurado | Avisar a quien instaló la suite |
| «Base de Establecimientos: todavía no se ha cargado, así que no hay pares con qué comparar» | Falta el registro de establecimientos del DEIS | Avisar a quien administra Estadística |
| Una meta sin porcentaje | Falta la población de FONASA de ese año, o el mes todavía no se publica | Avisar a quien administra Estadística si falta la población |
| «Todavía no hay Metas Sanitarias cargadas» | No hay metas cargadas hasta el año en curso | Avisar a quien administra Estadística, que las carga como un archivo en «Cargar un archivo a mano» |
| «La consulta se canceló antes de terminar» | La consulta superó el límite de 10 s | Acotar el periodo, las prestaciones o la comparación |
| Un mensaje de error rojo | Dice qué falló | Si pide recargar la página y el problema sigue, avisar a quien administra Estadística |
| «Si este mensaje no desaparece, la aplicación no pudo cargar: avise al administrador» | La aplicación no llegó a abrirse en el navegador | Avisar a quien administra la instalación |
