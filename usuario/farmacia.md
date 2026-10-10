---
tipo: guia
audiencia: usuario
apps: [farmacia]
resumen: "Consultar el vademécum del CESFAM en Farmacia, editar, retirar y restaurar medicamentos, e importar o exportar la planilla CSV del arsenal."
---
# Farmacia

## Objetivo

Farmacia es el vademécum digital del CESFAM: cada medicamento que el centro receta y despacha, con su cobertura (GES, canales de abastece) y su seguridad clínica (categoría FDA en embarazo, ajuste renal, riesgo colinérgico en adulto mayor). No contiene información de pacientes y no gestiona stock ni vencimientos.

Esta guía recorre el uso de la aplicación: consultar el arsenal, agregar y editar medicamentos, retirarlos y restaurarlos, importar y exportar la planilla, y mantener las categorías terapéuticas y los canales de abastece.

APS Conecta Gestión instala Farmacia en cada establecimiento y la habilita para todas las cuentas: todo el equipo consulta y edita el mismo arsenal. La red de seguridad no son los permisos, sino el retiro reversible y la revisión fila por fila de cada importación. La aplicación llega con 16 categorías terapéuticas y sin canales de abastece: cada CESFAM declara los suyos.

## Requisitos

- Una cuenta en la plataforma del establecimiento. Farmacia no exige un grupo ni un rol.
- Para importar, un archivo CSV con una fila de encabezado que tenga la columna «Código», de 8 MB como máximo.

## Pasos

### Consultar el arsenal

1. Abrir la aplicación {guilabel}`Farmacia`.
2. Elegir una lente en la columna izquierda.
3. Escribir en {guilabel}`Buscar` parte del producto, del fármaco (DCI) o de la categoría terapéutica.
4. Presionar un medicamento de la lista para abrir su ficha a la derecha.

| Lente | Muestra |
|---|---|
| {guilabel}`Arsenal Farmacológico` | Todos los medicamentos activos. |
| {guilabel}`Fármacos en embarazo` | Los que tienen categoría FDA informada (A, B, C, D o X). |
| {guilabel}`Ajuste farmacológico ERC` | Los que tienen ajuste renal informado. |

Una lente cambia el filtro inicial y deja la búsqueda en blanco; el arsenal sigue siendo uno solo, y volver a {guilabel}`Arsenal Farmacológico` muestra todo. La búsqueda no distingue acentos ni mayúsculas, y el botón «×» del campo {guilabel}`Buscar` (etiqueta accesible «Limpiar la búsqueda») la deja en blanco. El encabezado de la lista indica cuántos medicamentos hay a la vista.

Una categoría FDA vacía significa «sin dato», no que el medicamento sea seguro en el embarazo.

### Agregar un medicamento

1. Presionar {guilabel}`Agregar medicamento` en el pie del menú izquierdo.
2. Escribir el {guilabel}`Código`.
3. Escribir el {guilabel}`Producto`.
4. Elegir la {guilabel}`Categoría terapéutica`.
5. Completar las demás secciones de la ficha.
6. Presionar {guilabel}`Guardar`.

El código, el producto y la categoría terapéutica son obligatorios. Si falta el código o el producto, el navegador no deja guardar y señala el campo vacío; si falta la categoría, la ficha muestra en rojo la frase que dice qué corregir. El código es la identidad del registro: la importación lo usa para reconocer el medicamento, y dos medicamentos no pueden compartirlo.

| Sección | Campos |
|---|---|
| Identidad | {guilabel}`Código`, {guilabel}`Producto`, {guilabel}`Fármaco (DCI)`, {guilabel}`Mg`, {guilabel}`Presentación`, {guilabel}`Categoría terapéutica` |
| Cobertura | {guilabel}`Abastece`, {guilabel}`Programa`, {guilabel}`Trazador (uso monitorio / epidemiológico)`, los números GES y las restricciones |
| Clínica | {guilabel}`Indicación`, {guilabel}`Dosificación`, {guilabel}`Precauciones`, {guilabel}`Observaciones` |
| Seguridad | {guilabel}`Riesgo colinérgico en adulto mayor`, {guilabel}`Categoría FDA en embarazo`, {guilabel}`Ajuste renal (ERC)` |
| Estado | La fecha de la última escritura: «Actualizado: …», o «Sin guardar todavía.» en una ficha nueva |

Los números GES y las restricciones se agregan de a uno: se escribe el valor en {guilabel}`Agregar número GES` o en {guilabel}`Agregar restricción` y se presiona {guilabel}`Agregar`. {guilabel}`Quitar` elimina un valor de la lista.

### Editar un medicamento

1. Abrir la ficha del medicamento desde la lista.
2. Cambiar los campos que correspondan.
3. Presionar {guilabel}`Guardar`.

Después de guardar, la ficha muestra lo que quedó almacenado, no lo que se escribió: los textos sin espacios sobrantes y los números GES sin repeticiones.

### Retirar un medicamento

1. Abrir la ficha del medicamento.
2. Presionar {guilabel}`Retirar del arsenal`.
3. Leer el aviso «Se retira del arsenal y de la lista. No se borra: conserva sus datos y se puede restaurar.».
4. Presionar {guilabel}`Retirar`.

{guilabel}`Cancelar` deja el medicamento como estaba. Un medicamento retirado sale de las listas activas y de la planilla exportada, pero conserva todos sus datos.

### Restaurar un medicamento retirado

1. Presionar {guilabel}`Ver retirados` sobre la lista.
2. Abrir el medicamento retirado.
3. Presionar {guilabel}`Restaurar`.
4. Presionar {guilabel}`Ver activos` para volver a la lista normal.

La ficha de un medicamento retirado se abre en solo lectura, con el aviso «Este registro está retirado: no aparece en el arsenal.». La búsqueda funciona en {guilabel}`Ver retirados`; las lentes no, porque es una pantalla de recuperación y no un filtro clínico. Elegir una lente vuelve a la lista de activos.

### Importar una planilla

1. Presionar {guilabel}`Importar planilla` en el pie del menú izquierdo.
2. Elegir el archivo CSV en {guilabel}`Archivo`.
3. Presionar {guilabel}`Revisar`.
4. Leer el resumen del lote y el veredicto de cada fila.
5. Marcar {guilabel}`Solo filas que esperan una decisión`, si el resumen indica filas pendientes.
6. Presionar {guilabel}`Resolver` en una fila pendiente.
7. Elegir la {guilabel}`Categoría terapéutica` o los canales de {guilabel}`Abastece` que corresponden.
8. Presionar {guilabel}`Resolver` para guardar la decisión.
9. Repetir los pasos 6 a 8 hasta que ninguna fila espere una decisión.
10. Presionar {guilabel}`Aplicar`.

Revisar no escribe nada: la aplicación estudia cada fila por separado y muestra el lote («Lote #N en revisión») con su resumen y el veredicto de cada fila. {guilabel}`Aplicar` se habilita cuando ninguna fila espera una decisión, y escribe el lote completo en una sola operación: o entra todo lo revisado, o no entra nada. {guilabel}`Descartar` cierra el lote sin escribir nada.

| Veredicto | Significado |
|---|---|
| crear | Ningún medicamento tiene ese código: la fila crea uno nuevo. |
| actualizar | Un medicamento activo tiene ese código y la fila lo cambia. |
| sin cambios | Un medicamento activo tiene ese código y la fila dice lo mismo que él. |
| omitido | El medicamento con ese código está retirado: la importación no lo toca. |
| duplicado | La planilla repite un código; la nota indica en qué línea apareció primero. |
| con problemas | Una celda no se pudo leer; la nota dice cuál. La fila no entra y no impide que entren las demás. |

La planilla sigue estas reglas:

- **Columnas.** Se leen Código, Producto, Fármaco (DCI), Mg, Presentación, Categoría, Trazador, GES, Restricciones, Abastece, Programa, Indicación, Dosificación, Precauciones, Observaciones, Riesgo colinérgico AM, FDA embarazo y Ajuste renal; las demás se ignoran. Los encabezados se reconocen sin importar acentos ni mayúsculas.
- **Columnas ausentes.** Una columna que el archivo no trae deja ese dato del medicamento como estaba: una planilla con tres columnas actualiza solo esas tres.
- **Separadores.** Las columnas van separadas por punto y coma o por coma. Las celdas con varios valores (GES, restricciones, abastece) van unidas con «|».
- **Valores.** Trazador y Riesgo colinérgico AM aceptan Sí o No; FDA embarazo acepta A, B, C, D, X o la celda vacía, que significa sin dato.
- **Palabras desconocidas.** Si la planilla nombra una categoría o un canal que no existe, la fila queda esperando una decisión. Si la palabra misma falta, cerrar el diálogo con {guilabel}`Cerrar` (el lote sigue en revisión), declararla en {guilabel}`Categorías` o {guilabel}`Abastece` y volver a abrir el lote desde {guilabel}`Lotes recientes`. Al resolver los canales, no marcar ninguno deja el medicamento sin canal.

Un lote en revisión sobrevive al cierre de la página: {guilabel}`Lotes recientes` lo reabre con las decisiones ya tomadas. Un lote aplicado ofrece {guilabel}`Deshacer`: lo que la importación creó se retira y lo que actualizó vuelve a como estaba, salvo los medicamentos que alguien editó después de aplicar, que se conservan. Un deshacer no se puede deshacer; la salida es importar la planilla de nuevo.

### Exportar el arsenal

1. Presionar {guilabel}`Exportar planilla` en el pie del menú izquierdo.
2. Leer lo que lleva el archivo.
3. Presionar {guilabel}`Descargar`.

El archivo `farmacia-AAAA-MM-DD.csv` lleva el arsenal farmacológico completo, con todas las columnas y separado por punto y coma, listo para abrir en Excel o LibreOffice. Los medicamentos retirados no van. El archivo se puede reimportar: la revisión lo recibe fila por fila como cualquier planilla. Una celda que empieza con «=», «+», «-» o «@» sale con un apóstrofo delante, para que la hoja de cálculo no la ejecute como fórmula; la importación quita ese apóstrofo.

### Mantener las categorías y los canales

1. Presionar {guilabel}`Categorías` o {guilabel}`Abastece` en el pie del menú izquierdo.
2. Escribir el nombre nuevo en {guilabel}`Nueva categoría` o en {guilabel}`Nuevo canal`.
3. Presionar {guilabel}`Agregar`.

Para renombrar una palabra:

1. Presionar el nombre en la lista.
2. Escribir el nombre nuevo.
3. Presionar {guilabel}`Guardar`.

Para quitar una palabra:

1. Presionar {guilabel}`Quitar` junto al nombre.
2. Confirmar con {guilabel}`Quitar`.

Una categoría o un canal no se puede quitar mientras algún medicamento, activo o retirado, lo use. Los nombres no pueden quedar vacíos, ni pasar de 128 caracteres, ni contener «|». Al agregar, un nombre que coincide con otro sin contar acentos, mayúsculas ni signos se rechaza con «Ya existe una categoría con ese nombre.» o «Ya existe un canal con ese nombre.». Renombrar cambia solo el nombre visible: la palabra conserva el identificador interno que se derivó del nombre con que se creó. Una planilla que traiga ese nombre original la sigue reconociendo; una planilla exportada después del cambio trae el nombre nuevo, y si este difiere del original en algo más que acentos, mayúsculas o signos, la revisión pide decidir esa palabra.

## Verificación

- Después de {guilabel}`Guardar`, la sección Estado de la ficha muestra «Actualizado:» con la fecha y la hora de la escritura.
- Un medicamento retirado aparece en {guilabel}`Ver retirados` con la marca «Retirado».
- Después de {guilabel}`Aplicar`, la página se recarga con el arsenal al día, y {guilabel}`Lotes recientes` muestra el lote como «aplicado».
- Después de {guilabel}`Deshacer`, {guilabel}`Lotes recientes` muestra un lote nuevo que «deshace el lote #N».
- Después de {guilabel}`Descargar`, el navegador guarda el archivo `farmacia-AAAA-MM-DD.csv` con la fecha del día.

## Problemas frecuentes

| Mensaje o síntoma | Qué hacer |
|---|---|
| «Todavía no hay medicamentos» | Ningún medicamento activo entra en la lente elegida; con {guilabel}`Arsenal Farmacológico`, el arsenal está vacío. Elegir {guilabel}`Arsenal Farmacológico`; si sigue vacío, importar la planilla o agregar el primer medicamento. |
| «Nada coincide con «…»» | La búsqueda no encontró el texto en producto, fármaco ni categoría. Probar con menos palabras o limpiar la búsqueda. |
| «No hay medicamentos retirados» | No queda ningún medicamento retirado; la pantalla de recuperación está vacía. |
| {guilabel}`Aplicar` no se habilita | Hay filas que esperan una decisión de vocabulario. Marcar {guilabel}`Solo filas que esperan una decisión` y resolverlas. |
| «El archivo supera los 8 MB.» | Elegir un archivo más pequeño; una planilla de cientos de filas pesa mucho menos. |
| «La primera fila debe ser el encabezado y no tiene una columna «Código». …» | Agregar la columna Código a la fila de encabezado del archivo. |
| «No se puede quitar «…»: hay … incluidos los retirados. …» | Reclasificar los medicamentos que usan esa palabra, o quitarles el canal, y volver a intentarlo. |
| La lista no muestra el cambio de un colega | Al volver a la ventana de Farmacia después de usar otra, la página se recarga sola, salvo que haya una ficha o un diálogo abierto. Cerrar la ficha y volver a la ventana. |
| Un mensaje de error rojo en la ficha, la importación o un vocabulario | El mensaje dice qué falló. Corregir lo que nombra y repetir la acción; si se repite, avisar a la administración de la plataforma. |
