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
El mapa base lo sirve la propia suite, en la misma dirección de la plataforma; {doc}`/administracion/mapas-base` describe ese servicio.
Las unidades vecinales y los establecimientos de salud de la comuna llegan en un paquete de datos que la administración importa cuando el establecimiento empieza a usar Territorio.

## Requisitos

- Una cuenta de la plataforma. Toda persona que abre Territorio puede agregar, consultar, editar y retirar registros: el historial y el retiro reemplazan a los permisos.
- Para el control {guilabel}`¿Dónde estoy?`: una conexión HTTPS y el permiso del navegador para usar la ubicación.
- Para buscar calles y trazar el límite de un sector a partir de ellas: las calles, canales y vías de la comuna, importados por la administración. Sin ellos, el sector se dibuja a mano.
- Para exportar datos de contacto: la contraseña de la propia cuenta.

## Pasos

### Estructura de la pantalla y navegación

Territorio adopta una distribución basada en el diseño de escritorio de Google Maps: el mapa ocupa el 100 % del lienzo y las herramientas flotan sobre él de manera compacta.

```
+-----------------------------------------------------------------------------------+
| [ Omnibox: Activos y Calles... ]  [ 🗂️ Tipo de Activo ▾ ]  [ 📐 Dibujar Sector ]   |
| [ 🗺️ Mapa | 📋 Índice | 📊 Análisis | ⚠️ Duplicados ]                              |
+----------------------+------------------------------------------------------------+
| Panel lateral 408 px |                                                            |
| [◀ Ocultar panel]    |                                                            |
|                      |                                                            |
|  Directorio de       |                     LIENZO DEL MAPA                        |
|  activos y ficha     |                       (100 % ancho)                        |
|  de inspección       |                                                            |
|  o edición           |                                                            |
|                      |                                                            |
+----------------------+------------------------------------------------------------+
```

1. **Barra de comandos superior flotante**:
   - **Cuadro de búsqueda unificada (Omnibox)**: permite escribir el nombre de un activo comunitario o el de una calle de la comuna. Al teclear, despliega sugerencias coincidentes con su ubicación y sector.
   - **Selector desplegable de capas** ({guilabel}`Tipo de Activo`): reúne todas las categorías y subcategorías en un menú desplegable con casillas de verificación múltiple, indicando el número de capas activas.
   - **Botón de diseño territorial** ({guilabel}`Dibujar Sector`): arma de inmediato la herramienta de trazado de polígonos sobre el mapa.
   - **Selector de vista**: botones para alternar entre {guilabel}`Mapa`, {guilabel}`Índice` tabular, {guilabel}`Análisis` estadístico y cola de {guilabel}`Posibles duplicados`.
2. **Panel lateral acoplable (408 px)**:
   - Se sitúa en el costado izquierdo sobre el mapa.
   - Cuenta con una pestaña de borde con flecha ({guilabel}`◀` / {guilabel}`▶`) para replegar el panel y dejar el mapa completamente despejado, o volver a desplegarlo en cualquier momento.
   - Contiene el directorio ordenado de activos comunitarios cuando no hay un registro abierto, o la ficha dual (inspección / edición) cuando se selecciona o crea un activo.

### Consulta e inspección de activos comunitarios

1. Abrir {guilabel}`Territorio` en la barra superior.
2. En el panel lateral izquierdo, revisar la lista de activos comunitarios. Puede ordenar por {guilabel}`Nombre`, {guilabel}`Más recientes` o {guilabel}`Subcategoría`, y filtrar por un sector específico.
3. Al hacer clic en un activo en la lista o en su marcador en el mapa, el panel lateral pasa automáticamente al **Modo Inspección**:
   - Muestra el nombre oficial, su categoría, subcategoría y el pictograma representativo.
   - Presenta el {guilabel}`Sector` y la {guilabel}`Unidad Vecinal` calculados automáticamente a partir de la ubicación geográfica.
   - Proporciona botones de acción directa: {guilabel}`Centrar` (aproxima el mapa al activo), {guilabel}`Editar` (pasa al formulario editable), {guilabel}`Llamar` (si tiene teléfono registrado) y {guilabel}`Correo` (para redactar un mensaje).
   - Detalla la dirección, horarios de atención, persona de contacto, cargo y notas comunitarias.

### Registro y edición de un activo con escudo de duplicados

1. En el panel lateral, pulsar {guilabel}`Agregar activo` (o el botón {guilabel}`Editar` en un activo existente).
2. Escribir el {guilabel}`Nombre` del lugar o institución.
3. Elegir la {guilabel}`Subcategoría` correspondiente.
4. Hacer clic en el mapa para situar el punto geográfico, o escribir manualmente la {guilabel}`Latitud` y {guilabel}`Longitud`.
5. Indicar la {guilabel}`Exactitud`: {guilabel}`Exacta` o {guilabel}`Aproximada`. Un lugar de ubicación aproximada se dibuja con borde discontinuo para advertir que el dato no es milimétrico.
6. **Escudo Proactivo de Duplicados**: si el nombre ingresado presenta alta similitud con otro activo situado a menos de 50 metros, aparece una advertencia en amarillo ({guilabel}`⚠️ Posible duplicado detectado`) que indica el nombre del activo existente y la distancia calculada. Esto previene registrar dos veces el mismo centro o junta vecinal bajo nombres ligeramente distintos.
7. Completar los campos de contacto y referencia: {guilabel}`Dirección`, {guilabel}`Teléfono`, {guilabel}`Correo`, {guilabel}`Persona de contacto`, {guilabel}`Cargo`, {guilabel}`Horario`, {guilabel}`Fuente` y {guilabel}`Notas`.
8. Pulsar {guilabel}`Guardar`.

Para retirar un registro:

1. Abrir el activo y pulsar {guilabel}`Retirar del mapa`.
2. Confirmar la acción en {guilabel}`Retirar`. El registro no se elimina de la base de datos: conserva su historial completo y queda disponible en {guilabel}`Ver retirados` para su posterior restauración.

### Filtrado por capas y gestión de taxonomía

1. Pulsar el botón {guilabel}`Tipo de Activo` en la barra superior.
2. Marcar o desmarcar categorías o subcategorías individuales en la lista desplegable. El mapa y la lista se actualizan inmediatamente.
3. Para mostrar todas las capas nuevamente, pulsar {guilabel}`Todos`. Para desmarcarlas, pulsar {guilabel}`Limpiar`.
4. Para ajustar o ampliar las categorías del establecimiento, pulsar {guilabel}`Configurar taxonomía y capas` al final del menú. Se abrirá un panel deslizante lateral (*drawer*) que permite agregar nuevas categorías, asignarles pictogramas oficiales y renombrar clasificaciones sin interrumpir la vista del mapa.

### Unidades vecinales y diseño de sectores

Una unidad vecinal es una subdivisión oficial de la comuna: su límite proviene del catastro nacional; el establecimiento la consulta y no la modifica.
Un sector es una división operativa que el CESFAM define para organizar el trabajo de sus equipos de cabecera con las familias del territorio.
En el mapa, las unidades vecinales se dibujan con línea discontinua sin relleno; los sectores muestran un relleno tenue en su color distintivo y su etiqueta centrada.

Para diseñar un sector nuevo:

1. Pulsar {guilabel}`Dibujar Sector` en la barra de herramientas superior. El cursor del mapa cambiará a modo de trazado de polígonos.
2. Hacer clic en el mapa en cada vértice que delimite el sector. Las líneas se ajustan automáticamente a los vértices y calles adyacentes gracias al sistema de encaje (*snapping*).
3. Cerrar el polígono haciendo clic en el primer vértice.
4. En el panel lateral, escribir el {guilabel}`Nombre` del sector (por ejemplo, «Sector 1», «Sector Azul» o «Sector Cordillera») y elegir su {guilabel}`Color`.
5. Si prefiere generar el sector a partir del catastro de calles:
   - Buscar y seleccionar cada calle, canal o vía limítrofe.
   - Pulsar {guilabel}`Generar el polígono` y hacer clic en el interior del área deseada.
6. Ajustar los vértices arrastrándolos con el ratón si se requiere precisión adicional.
7. Pulsar {guilabel}`Guardar`. Todo activo comunitario contenido dentro de los nuevos límites quedará automáticamente asignado a este sector.

### Vistas complementarias: Índice, Análisis y Duplicados

- **{guilabel}`Índice`**: despliega la totalidad de los registros activos en una tabla interactiva a pantalla completa. Permite ordenar por cualquier columna, ocultar o mostrar columnas específicas y acceder directamente a la ficha de cualquier registro mediante {guilabel}`← Volver al mapa`.
- **{guilabel}`Análisis`**: muestra la distribución estadística de los registros filtrados, agrupados por categorías y subcategorías con barras de proporción visual.
- **{guilabel}`Posibles duplicados`**: exhibe la lista de pares de registros que podrían corresponder al mismo lugar físico (por ejemplo, registros importados con discrepancias ortográficas). Cada par permite decidir si se fusiona ({guilabel}`Fusionar`), descartando el registro secundario e incorporando su historial al principal, o si se desestima ({guilabel}`Descartar`).

### Exportación de datos

1. Aplicar las capas y filtros deseados hasta visualizar exactamente el conjunto requerido.
2. En la lista de activos del panel lateral, pulsar {guilabel}`Exportar`.
3. Seleccionar el formato: {guilabel}`GeoJSON` (completo y apto para reimportación), {guilabel}`CSV` (para planillas de cálculo), {guilabel}`KML` o {guilabel}`KMZ`.
4. Si requiere incluir nombres, teléfonos o correos, activar {guilabel}`Incluir datos de contacto`.
5. Pulsar {guilabel}`Exportar` e ingresar la contraseña de su cuenta cuando el sistema lo solicite.

## Verificación

- El mapa se despliega en pantalla completa y el panel lateral de 408 px se abre o cierra al accionar el botón de pestaña {guilabel}`◀` / {guilabel}`▶`.
- El cuadro de búsqueda superior localiza tanto activos comunitarios como calles del catastro comunal.
- Al seleccionar un activo, el panel muestra la ficha de inspección con sus datos y botones de centrado y llamada.
- Al escribir un nombre parecido a menos de 50 metros de un registro previo, el formulario muestra la advertencia del escudo de duplicados.
- El botón {guilabel}`Dibujar Sector` activa el dibujo de polígonos y permite guardar sectores con su color y asignación territorial.
- Los cambios realizados por otros usuarios se reflejan en el mapa de forma automática en un lapso de cinco segundos.

## Problemas frecuentes

- **«No se pudo cargar el fondo de mapa. El mapa sigue disponible…»**: los registros, sectores y activos comunitarios continúan operativos sobre el plano vectorial; la administración puede revisar el estado del mapa base en {doc}`/administracion/mapas-base`.
- **«No hay calles cargadas en este mapa.»**: las vías de la comuna no han sido importadas en el catastro; trace el sector a mano utilizando {guilabel}`Dibujar Sector`.
- **«Las calles elegidas no cierran alrededor de ese punto…»**: seleccione tramos adicionales que completen un circuito cerrado o dibuje el sector directamente en el mapa.
- **«⚠️ Posible duplicado detectado…»**: verifique si el establecimiento ya cuenta con dicho activo registrado. Si se trata de una sede distinta, puede guardar normalmente ignorando la advertencia.
- **«No tenemos permiso para usar su ubicación…»**: conceda el permiso de geolocalización en el navegador y vuelva a presionar {guilabel}`¿Dónde estoy?`.
- **Una categoría o subcategoría no se puede quitar**: el sistema impide eliminar clasificaciones que contengan activos activos; primero reasigne dichos registros a otra subcategoría.
