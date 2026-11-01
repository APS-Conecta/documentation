---
tipo: guia
audiencia: usuario
apps: [territorio, gestion]
resumen: "Recorrer el territorio del CESFAM: diseño Google Maps, panel de activos, capas, sectores, escudo de duplicados y exportación."
---
# Territorio

## Objetivo

Territorio muestra en un mapa el territorio que atiende el CESFAM: las unidades vecinales oficiales, los sectores que dibuja el propio establecimiento y los activos comunitarios de la comuna, como colegios, plazas, farmacias, juntas de vecinos y organizaciones sociales.
Es un registro único compartido por todo el establecimiento: lo que una persona cambia, cambia para todas.
Lo que cada persona tiene en pantalla, es decir, las capas visibles, la zona del mapa y los filtros, es personal y no cambia nada para las demás.
La aplicación no contiene información de pacientes.
Esta guía recorre el diseño del mapa, el panel lateral de activos comunitarios, las unidades vecinales y los sectores, el escudo proactivo de duplicados, la taxonomía y la exportación de datos.

APS Conecta Gestión instala Territorio como una de sus aplicaciones propias y no instala la aplicación de mapas personales de la plataforma: la geografía del establecimiento vive en un solo registro institucional.
La suite escribe en la configuración de Territorio la comuna que atiende el establecimiento.
El mapa base es el de OpenStreetMap, que cada navegador carga directamente: hace falta internet para verlo, y {doc}`/administracion/mapas-base` describe el servicio.
El mapa abre sobre la parte de la comuna donde están los establecimientos de salud; si esa extensión no se conoce, sobre las unidades vecinales, luego sobre los registros y, por último, sobre el centro del país. El desplazamiento no tiene límites.
Cada petición de teselas lleva a OpenStreetMap las coordenadas de la zona que se ve, con una precisión de unos 300 m en el zoom 17, y la dirección de la instancia; ningún registro ni nombre.
En la próxima versión, la instalación carga las unidades vecinales y los establecimientos de salud de la comuna elegida. La administración puede repetir la carga; los registros existentes y las ediciones locales se conservan.

## Requisitos

- Una cuenta de la plataforma. Toda persona que abre Territorio puede agregar, consultar, editar y retirar registros: el historial y el retiro reemplazan a los permisos.
- Para ver el mapa base: una conexión a internet. Sin ella, los registros, el dibujo y las capas siguen funcionando sobre un fondo liso.
- Para el control {guilabel}`¿Dónde estoy?`: una conexión HTTPS y el permiso del navegador para usar la ubicación.
- Para buscar calles y trazar el límite de un sector a partir de ellas: las calles, canales y vías de la comuna, importados por la administración. Sin ellos, el sector se dibuja a mano.
- Para exportar datos de contacto: la contraseña de la propia cuenta.

## Pasos

### Estructura de la pantalla y navegación

Territorio adopta una distribución basada en el diseño de escritorio de Google Maps: el mapa ocupa el 100 % del lienzo y las herramientas flotan sobre él de manera compacta.

```
+-----------------------------------------------------------------------------------+
| [ 🔍 Buscar lugares, activos o calles… ]   [ 🗂️ Tipo de Activo ▾ ]  [ ✏️ Dibujar Sector ] |
| [ Mapa | Índice | Análisis | Posibles duplicados ]                                 |
+----------------------+------------------------------------------------------------+
| Panel lateral 408 px |                                                            |
|                      |                                                            |
|  Directorio de       |                     LIENZO DEL MAPA                        |
|  activos y ficha     |                       (100 % ancho)                        |
|  de inspección       |                                                            |
|  o edición           |                                                            |
|                      |                                                            |
+----------------------+------------------------------------------------------------+
Una pestaña con flecha (◀ / ▶) en el borde del panel lo repliega o lo despliega.
```

1. **Barra de comandos superior flotante**:
   - **Cuadro de búsqueda unificada (Omnibox)**: permite escribir el nombre, la dirección o la categoría de un activo comunitario, o el nombre de una calle de la comuna. Al teclear, despliega hasta diez sugerencias: cada activo con su subcategoría y su dirección, y cada calle con la indicación «Calle o vía de la comuna». Elegir un activo lo abre en el panel lateral y acerca el mapa a él; elegir una calle acerca el mapa a la calle. Las flechas del teclado recorren las sugerencias, {kbd}`Enter` elige la resaltada y {kbd}`Esc` limpia el cuadro.
   - **Selector de vista**, bajo el cuadro de búsqueda: pestañas para alternar entre {guilabel}`Mapa`, {guilabel}`Índice` tabular, {guilabel}`Análisis` estadístico y la cola de {guilabel}`Posibles duplicados`. La pestaña activa aparece resaltada.
   - **Selector desplegable de capas** ({guilabel}`Tipo de Activo`): reúne las categorías en un menú con casillas de verificación, indicando entre paréntesis cuántas están activas.
   - **Botón de diseño territorial** ({guilabel}`Dibujar Sector`): arma de inmediato la herramienta de trazado de polígonos sobre el mapa. Mientras dibuja, el botón cambia a {guilabel}`Cancelar Dibujo`.
2. **Panel lateral acoplable (408 px)**:
   - Se sitúa en el costado izquierdo sobre el mapa.
   - Cuenta con una pestaña de borde con flecha ({guilabel}`◀` / {guilabel}`▶`) para replegar el panel y dejar el mapa completamente despejado, o volver a desplegarlo en cualquier momento.
   - Contiene el directorio ordenado de activos comunitarios cuando no hay un registro abierto, o la ficha dual (inspección / edición) cuando se selecciona o crea un activo.
3. **Control de ubicación** ({guilabel}`¿Dónde estoy?`), bajo los botones de zoom: centra el mapa en la ubicación del dispositivo y dibuja también la precisión de la lectura. Sobre 100 m, el mapa avisa que la ubicación es aproximada y que puede no coincidir con el sector que se muestra.

La búsqueda de calles acerca el mapa al nivel de la calle, no al número de una casa, y no consulta ningún servidor externo.

### Consulta e inspección de activos comunitarios

1. Abrir {guilabel}`Territorio` en la barra superior.
2. En el panel lateral izquierdo, revisar la lista de activos comunitarios, que indica cuántos registros muestra. Escribir en {guilabel}`Buscar` filtra la lista por texto. En {guilabel}`Ordenar` se elige {guilabel}`Nombre (A-Z)`, {guilabel}`Nombre (Z-A)`, {guilabel}`Sector` o {guilabel}`Más reciente`, y en {guilabel}`Sector` se elige un sector específico o {guilabel}`Todos`.
3. Al hacer clic en un activo en la lista o en su marcador en el mapa, el panel lateral pasa automáticamente al **Modo Inspección**:
   - Muestra el nombre del registro y su subcategoría, con la categoría.
   - Presenta el sector y la unidad vecinal, que la aplicación deduce de la ubicación geográfica, con la forma {guilabel}`Sector: …` y {guilabel}`UV: …` (o {guilabel}`sin asignar`).
   - Proporciona botones de acción directa: {guilabel}`Editar` (pasa al formulario editable) y {guilabel}`Centrar` (aproxima el mapa al activo). Si el registro tiene teléfono o correo, aparecen como enlaces ({guilabel}`📞` y {guilabel}`✉️`) que abren la aplicación de llamadas o de correo del dispositivo.
   - Detalla la dirección, el horario, la persona de contacto con su cargo, las notas y la fuente.
   - Al final, el {guilabel}`Historial` del registro muestra quién hizo cada cambio y cuándo.
   - {guilabel}`← Volver a la lista`, arriba de la ficha, cierra el registro y devuelve el panel a la lista de activos.

### Registro y edición de un activo con escudo de duplicados

1. En el panel lateral, pulsar {guilabel}`Agregar` (o el botón {guilabel}`Editar` en un activo existente).
2. Escribir el {guilabel}`Nombre` del lugar o institución.
3. Elegir la {guilabel}`Subcategoría` correspondiente.
4. Hacer clic en el mapa para situar el punto geográfico, o escribir manualmente la {guilabel}`Latitud` y {guilabel}`Longitud`.
5. Indicar la {guilabel}`Exactitud`: {guilabel}`Exacta` o {guilabel}`Aproximada`. Un lugar de ubicación aproximada se dibuja con un anillo discontinuo: en Territorio, una línea discontinua significa siempre que el dato no es preciso.
6. **Escudo Proactivo de Duplicados**: mientras se completa el formulario, la aplicación compara el lugar con los registros activos y, si encuentra uno que podría ser el mismo, muestra una advertencia amarilla ({guilabel}`⚠️ Posible duplicado detectado`) con el nombre del registro existente y la distancia en metros. La advertencia aparece en dos casos: cuando otro registro está a 25 metros o menos, sea cual sea su nombre; o cuando está a 150 metros o menos y el nombre es parecido (igual sin contar mayúsculas, tildes ni signos, uno contenido en el otro, como «CESFAM Bellavista» y «CESFAM Bellavista (SSMSO)», o con una similitud de 85 % o más). Los registros retirados no cuentan. La advertencia no impide guardar: previene registrar dos veces el mismo centro o junta vecinal bajo nombres ligeramente distintos, y quien sabe que se trata de otra sede puede guardar igual.
7. Completar los campos de contacto y referencia: {guilabel}`Dirección`, {guilabel}`Teléfono`, {guilabel}`Correo`, {guilabel}`Persona de contacto`, {guilabel}`Cargo`, {guilabel}`Horario`, {guilabel}`Fuente` y {guilabel}`Notas`.
8. Pulsar {guilabel}`Guardar`.

Un registro sin coordenadas es válido: aparece en la lista y no en el mapa.
Elegirlo en la búsqueda lo abre en el panel, pero el mapa no se mueve, porque no hay adónde ir.
El sector y la unidad vecinal de un lugar se deducen de su ubicación y no se escriben: para corregirlos, se corrige la ubicación o el límite.

Para retirar un registro:

1. Abrir el activo y pulsar {guilabel}`Retirar del mapa`.
2. Pulsar {guilabel}`Retirar` para confirmar. El registro no se elimina: conserva su historial completo, sale del mapa y de la lista de activos, y queda disponible en {guilabel}`Ver retirados`.

Para restaurar un registro retirado:

1. En la lista, pulsar {guilabel}`Ver retirados` (el botón pasa a decir {guilabel}`Ver activos`).
2. Abrir el registro.
3. Pulsar {guilabel}`Restaurar`.

### Lugares, zonas y rutas

Cada registro es un lugar, una zona o una ruta según su forma en el mapa: una ubicación, un área o una línea.
El botón {guilabel}`Dibujar Sector` dibuja sectores; las zonas y las rutas entran al registro al importar un archivo GeoJSON, KML o KMZ con {guilabel}`Importar / deshacer`, en la lista de activos. Un CSV solo trae lugares, con su latitud y longitud.
El mismo diálogo permite deshacer un lote importado.

### Filtrado por capas y gestión de taxonomía

1. Pulsar el botón {guilabel}`Tipo de Activo` en la barra superior.
2. Marcar o desmarcar categorías o subcategorías individuales en la lista desplegable. El mapa y la lista se actualizan inmediatamente.
3. Para mostrar todas las categorías nuevamente, pulsar {guilabel}`Todas`. Para ocultarlas, pulsar {guilabel}`Limpiar`. Ninguno de los dos cambia el texto de la búsqueda ni las divisiones territoriales.
4. Bajo {guilabel}`División Territorial`, una casilla por cada división (por ejemplo, el sector y la unidad vecinal) la muestra u oculta. Llevan el nombre que el establecimiento les dio en su taxonomía.
5. Para volver a mostrar todo, incluidas las divisiones, y limpiar la búsqueda, pulsar {guilabel}`Ver todo` en el panel de taxonomía.
6. Para ajustar o ampliar las categorías del establecimiento, pulsar {guilabel}`Configurar taxonomía y capas` al final del menú. Se abrirá un panel deslizante lateral (*drawer*) que permite agregar nuevas categorías, asignarles pictogramas oficiales y renombrar clasificaciones sin interrumpir la vista del mapa.

### Unidades vecinales y diseño de sectores

Una unidad vecinal es una subdivisión oficial de la comuna: su límite proviene del catastro nacional; el establecimiento la consulta y no la modifica.
Un sector es una división operativa que el CESFAM define para organizar el trabajo de sus equipos de cabecera con las familias del territorio.
Unidades vecinales y sectores son independientes: ninguno queda dentro del otro.
El establecimiento nombra sus sectores como acostumbre: con palabras, números o colores.
En el mapa, las unidades vecinales se dibujan con línea discontinua sin relleno; los sectores muestran un relleno tenue en su color distintivo y su etiqueta centrada.
Hacer clic en un sector o en una unidad vecinal del mapa abre su registro.

Para diseñar un sector nuevo:

1. Pulsar {guilabel}`Dibujar Sector` en la barra de herramientas superior. El cursor del mapa cambiará a modo de trazado de polígonos.
2. Hacer clic en el mapa en cada vértice que delimite el sector. Las líneas se ajustan automáticamente a los vértices y calles adyacentes gracias al sistema de encaje (*snapping*).
3. Cerrar el polígono haciendo clic en el primer vértice.
4. En el panel lateral, escribir el {guilabel}`Nombre` del sector (por ejemplo, «Sector 1», «Sector Azul» o «Sector Cordillera») y elegir su {guilabel}`Color`.
5. Si prefiere generar el sector a partir del catastro de calles:
   - Escribir el nombre de una calle del límite en {guilabel}`Buscar una calle, canal o vía`, y pulsar su fila (o hacer clic en la calle en el mapa). Repetir con cada calle, canal o vía del límite.
   - Escribir en {guilabel}`Agregar un tramo a mano` cada tramo que no sigue ninguna calle, y pulsar {guilabel}`Agregar tramo`.
   - Pulsar {guilabel}`Generar el polígono` y hacer clic en el interior del área deseada.
6. Ajustar los vértices arrastrándolos con el ratón si se requiere precisión adicional.
7. Pulsar {guilabel}`Guardar`. Todo activo comunitario contenido dentro de los nuevos límites quedará automáticamente asignado a este sector.

La línea {guilabel}`Va por` resume el límite en una frase: lo que diría el equipo si le preguntan dónde termina el sector.
Un sector dibujado a mano, sin elegir calles, es igual de válido, y siempre se puede dibujar a mano en vez de generar.

### Vistas complementarias: Índice, Análisis y Duplicados

Las capas y la búsqueda filtran a la vez el mapa, la lista, el {guilabel}`Índice` y el {guilabel}`Análisis`.
La cola de {guilabel}`Posibles duplicados` no se filtra: lista lo que espera una decisión.

- **{guilabel}`Índice`**: despliega los registros activos en una tabla a pantalla completa. Permite ordenar por cualquier columna, ocultar o mostrar columnas desde {guilabel}`Columnas` y abrir la ficha de cualquier registro. {guilabel}`← Volver al mapa` regresa al mapa, igual que la pestaña {guilabel}`Mapa`.
- **{guilabel}`Análisis`**: cuenta los registros filtrados por categoría y subcategoría, con barras de proporción.
- **{guilabel}`Posibles duplicados`**: reúne los pares de registros que podrían ser el mismo lugar (por ejemplo, registros importados con discrepancias ortográficas), para que una persona decida: la aplicación nunca los fusiona por su cuenta. Cada lado del par ofrece {guilabel}`Abrir ficha`, para ver el registro completo, y {guilabel}`Conservar este`, que deja ese registro como el único y retira el otro, que conserva su historial. {guilabel}`No son duplicados` descarta el par y deja ambos registros como están.

### Exportación de datos

1. Aplicar las capas y filtros deseados hasta visualizar exactamente el conjunto requerido.
2. En la lista de activos del panel lateral, pulsar {guilabel}`Exportar`.
3. Elegir el {guilabel}`Formato`.
4. Si requiere incluir nombres, teléfonos o correos de personas, activar {guilabel}`Incluir datos de contacto`.
5. Pulsar {guilabel}`Exportar` e ingresar la contraseña de su cuenta cuando el sistema lo solicite.

| Formato | Contenido |
|---|---|
| GeoJSON | Completo: se puede volver a importar. |
| CSV | Para planilla de cálculo: sirve para leer, ordenar e imprimir, y no vuelve a importarse. |
| KML | Solo nombre y ubicación, para Google Earth. |
| KMZ | El KML comprimido. |

La exportación lleva los registros activos que muestran el mapa y la lista, con las capas y la búsqueda aplicadas.
Un GeoJSON que se piensa volver a importar se exporta con datos de contacto: sin ellos, el archivo queda marcado como parcial y la importación lo rechaza.
Una exportación con datos de contacto pide la contraseña y queda registrada: quién exportó, cuándo, en qué formato y cuántos registros.
La administración consulta ese registro en la sección {guilabel}`Territorio` de las configuraciones de administración.

## Verificación

- Las unidades vecinales y los establecimientos de salud de la comuna aparecen en el registro después de la carga inicial. Si faltan, solicite revisar la carga según {doc}`/administracion/aio`.
- El mapa se despliega en pantalla completa y el panel lateral de 408 px se abre o cierra al accionar el botón de pestaña {guilabel}`◀` / {guilabel}`▶`.
- El cuadro de búsqueda superior localiza tanto activos comunitarios como calles del catastro comunal.
- Al seleccionar un activo, el panel muestra la ficha de inspección con sus datos, los botones {guilabel}`Editar` y {guilabel}`Centrar`, y los enlaces de teléfono y correo si los tiene.
- Al registrar un lugar a 25 metros o menos de otro, o a 150 metros o menos de uno con nombre parecido, el formulario muestra la advertencia del escudo de duplicados.
- El registro guardado aparece en la lista, que muestra el total de registros, y en el mapa cuando tiene coordenadas.
- El {guilabel}`Historial` de un registro muestra quién hizo cada cambio y cuándo.
- El botón {guilabel}`Dibujar Sector` activa el dibujo de polígonos y permite guardar sectores con su color y asignación territorial.
- Los cambios realizados por otros usuarios se reflejan en el mapa de forma automática en un lapso de cinco segundos.

## Problemas frecuentes

- **«No se pudo cargar el fondo de mapa. El mapa sigue disponible…»**: el navegador no llegó a las teselas de OpenStreetMap, por falta de internet o por un filtro de la red. Los registros, sectores y activos comunitarios continúan operativos sobre un fondo liso; {guilabel}`Ocultar` cierra el aviso, y la administración puede revisar la conexión según {doc}`/administracion/mapas-base`.
- **El mapa muestra una imagen de «acceso bloqueado» y ningún aviso**: OpenStreetMap bloqueó el servicio y la aplicación no puede detectarlo. Informar a la administración: lo corrige una versión nueva de Territorio, y {doc}`/administracion/mapas-base` explica el caso.
- **«No hay calles cargadas en este mapa.»**: las vías de la comuna no han sido importadas en el catastro; trace el sector a mano utilizando {guilabel}`Dibujar Sector`.
- **«Las calles elegidas no cierran alrededor de ese punto…»**: seleccione tramos adicionales que completen un circuito cerrado, haga clic en otro punto dentro del sector o dibuje el sector directamente en el mapa.
- **«Todavía no se conoce el trazado de todas las calles del límite…»**: acerque el mapa a esas calles para cargarlas, o dibuje el sector a mano.
- **«⚠️ Posible duplicado detectado…»**: verifique si el establecimiento ya cuenta con dicho activo registrado. Si se trata de una sede distinta, puede guardar normalmente ignorando la advertencia.
- **«No tenemos permiso para usar su ubicación…»**: conceda el permiso de geolocalización en el navegador y vuelva a presionar {guilabel}`¿Dónde estoy?`.
- **Una categoría o subcategoría no se puede quitar**: la aplicación rechaza quitarla mientras tenga registros activos; primero se reclasifican esos registros. La división territorial no se puede quitar nunca, porque todo sector y toda unidad vecinal se guarda en ella.
