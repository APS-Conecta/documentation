---
tipo: guia
audiencia: usuario
apps: [territorio, gestion]
resumen: "Recorrer el mapa del territorio del CESFAM: capas, unidades vecinales y sectores, registro de lugares y exportación de datos."
---
# Territorio

## Objetivo

Territorio muestra en un mapa el territorio que atiende el CESFAM: las unidades vecinales oficiales, los sectores que dibuja el propio establecimiento y los lugares de la comuna, como colegios, plazas, farmacias y organizaciones sociales.
Es un registro único compartido por todo el establecimiento: lo que una persona cambia, cambia para todas.
Lo que cada persona tiene en pantalla, es decir, las capas visibles, la zona del mapa y los filtros, es personal y no cambia nada para las demás.
La aplicación no contiene información de pacientes.
Esta guía recorre el mapa y sus capas, las unidades vecinales y los sectores, el registro de lugares y la exportación de datos.

APS Conecta Gestión instala Territorio como una de sus aplicaciones propias y no instala la aplicación de mapas personales de la plataforma: la geografía del establecimiento vive en un solo registro institucional.
La suite escribe en la configuración de Territorio la comuna que atiende el establecimiento.
El mapa base lo sirve la propia suite, en la misma dirección de la plataforma; {doc}`/administracion/mapas-base` describe ese servicio.
Las unidades vecinales y los establecimientos de salud de la comuna llegan en un paquete de datos que la administración importa cuando el establecimiento empieza a usar Territorio.

## Requisitos

- Una cuenta de la plataforma. Toda persona que abre Territorio puede agregar, editar y retirar registros: el historial y el retiro reemplazan a los permisos.
- Para el control {guilabel}`¿Dónde estoy?`: una conexión HTTPS y el permiso del navegador para usar la ubicación.
- Para buscar calles y trazar el límite de un sector a partir de ellas: las calles, canales y vías de la comuna, importados por la administración. Sin ellos, el sector se dibuja a mano.
- Para exportar datos de contacto: la contraseña de la propia cuenta.

## Pasos

### El mapa y sus capas

1. Abrir {guilabel}`Territorio` en la barra superior.
2. Ubicar el panel {guilabel}`Capas`, sobre la lista de registros; su título lo abre y lo cierra.
3. Marcar o desmarcar una categoría para mostrarla u ocultarla.
4. Desplegar una categoría y marcar o desmarcar cada una de sus subcategorías.
5. Pulsar {guilabel}`Ver todo` para volver a mostrar todas las capas y limpiar la búsqueda.
6. Escribir en {guilabel}`Buscar` para filtrar los registros por texto.
7. Pulsar {guilabel}`¿Dónde estoy?`, bajo los botones de zoom, para centrar el mapa en la ubicación del dispositivo.
8. Escribir parte del nombre de una calle en {guilabel}`Buscar una calle`.
9. Elegir una de las filas para acercar el mapa a esa calle.
10. Cambiar de vista con {guilabel}`Mapa`, {guilabel}`Índice`, {guilabel}`Análisis` o {guilabel}`Posibles duplicados`.

Las capas y la búsqueda filtran a la vez el mapa, la lista, el {guilabel}`Índice` y el {guilabel}`Análisis`.
El {guilabel}`Índice` muestra los registros activos en una tabla, y el {guilabel}`Análisis` los cuenta por categoría y subcategoría.
{guilabel}`Posibles duplicados` reúne los pares de registros que podrían ser el mismo lugar, para que una persona decida: la aplicación nunca los fusiona por su cuenta.
El control {guilabel}`¿Dónde estoy?` dibuja también la precisión de la lectura; sobre 100 m, el mapa avisa que la ubicación es aproximada y que puede no coincidir con el sector que se muestra.
La búsqueda de calles acerca el mapa al nivel de la calle, no al número de una casa, y no consulta ningún servidor externo.

### Unidades vecinales y sectores

Una unidad vecinal es una subdivisión oficial de la comuna: su límite viene del catastro nacional, y el establecimiento lo lee y nunca lo dibuja.
Un sector es una división del territorio que el CESFAM dibuja para sí: cada sector tiene un equipo fijo, para que las mismas personas atiendan a las mismas familias a lo largo del tiempo.
Unidades vecinales y sectores son independientes: ninguno queda dentro del otro.
En el mapa, una unidad vecinal se dibuja sin relleno y con una línea discontinua, y un sector con un relleno tenue y su nombre fijo en el centro.

1. Marcar {guilabel}`Sector` o {guilabel}`Unidad Vecinal` en el panel {guilabel}`Capas`.
2. Hacer clic en un sector o en una unidad vecinal del mapa para abrir su registro.

Para dibujar un sector nuevo:

1. Pulsar {guilabel}`Dibujar Polígono`, en la esquina superior derecha del mapa.
2. Hacer clic en el mapa en cada vértice del sector.
3. Pulsar {guilabel}`Finalizar` para cerrar el polígono.
4. Escribir el {guilabel}`Nombre` del sector.
5. Elegir el {guilabel}`Color` del sector.
6. Escribir el nombre de una calle del límite en {guilabel}`Buscar una calle, canal o vía`.
7. Pulsar la fila de esa calle, o hacer clic en la calle en el mapa.
8. Repetir los dos pasos anteriores con cada calle, canal o vía del límite.
9. Escribir en {guilabel}`Agregar un tramo a mano` cada tramo que no sigue ninguna calle.
10. Pulsar {guilabel}`Agregar tramo`.
11. Pulsar {guilabel}`Generar el polígono`.
12. Hacer clic dentro del sector en el mapa.
13. Arrastrar los vértices para ajustar el límite.
14. Pulsar {guilabel}`Guardar`.

El establecimiento nombra sus sectores como acostumbre: con palabras, números o colores.
La línea {guilabel}`Va por` resume el límite en una frase: lo que diría el equipo si le preguntan dónde termina el sector.
Un sector dibujado a mano, sin elegir calles, es igual de válido, y siempre se puede dibujar a mano en vez de generar.
Al guardar un sector, cada lugar que queda dentro pasa a pertenecer a él.

### Lugares, zonas y rutas

Cada registro es un lugar, una zona o una ruta según su forma en el mapa: una ubicación, un área o una línea.
La herramienta de polígono del mapa dibuja sectores; las zonas y las rutas entran al registro al importar un archivo GeoJSON, KML o KMZ con {guilabel}`Importar / deshacer`. Un CSV solo trae lugares, con su latitud y longitud.

Para registrar un lugar:

1. Pulsar {guilabel}`Agregar`.
2. Escribir el {guilabel}`Nombre`.
3. Elegir la {guilabel}`Subcategoría`.
4. Hacer clic en el mapa para situar el lugar, o escribir la {guilabel}`Latitud` y la {guilabel}`Longitud`.
5. Elegir la {guilabel}`Exactitud`: {guilabel}`Exacta` o {guilabel}`Aproximada`.
6. Completar los campos {guilabel}`Dirección`, {guilabel}`Teléfono`, {guilabel}`Correo`, {guilabel}`Persona de contacto`, {guilabel}`Cargo`, {guilabel}`Horario`, {guilabel}`Fuente` y {guilabel}`Notas` que correspondan.
7. Pulsar {guilabel}`Guardar`.

Un registro sin coordenadas es válido: aparece en la lista y no en el mapa.
El sector y la unidad vecinal de un lugar se deducen de su ubicación y no se escriben: para corregirlos, se corrige la ubicación o el límite.
Un lugar de ubicación aproximada se dibuja con un anillo discontinuo: en Territorio, una línea discontinua significa siempre que el dato no es preciso.

Para retirar un registro:

1. Abrir el registro desde el mapa o desde la lista.
2. Pulsar {guilabel}`Retirar del mapa`.
3. Pulsar {guilabel}`Retirar` para confirmar.

Un registro retirado sale del mapa y de la lista de activos, pero no se borra: conserva su historial y se puede restaurar.

Para restaurar un registro retirado:

1. Pulsar {guilabel}`Ver retirados`.
2. Abrir el registro.
3. Pulsar {guilabel}`Restaurar`.

### Exportación de datos

1. Ajustar las capas y la búsqueda hasta que la lista muestre lo que se quiere exportar.
2. Pulsar {guilabel}`Exportar`, junto a la búsqueda.
3. Elegir el {guilabel}`Formato`.
4. Activar {guilabel}`Incluir datos de contacto` si el archivo debe llevar nombres, teléfonos y correos de personas.
5. Pulsar {guilabel}`Exportar`.
6. Escribir la contraseña de la cuenta cuando la plataforma la pida.

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

- El registro guardado aparece en la lista, que muestra el total de registros, y en el mapa cuando tiene coordenadas.
- El registro de un lugar muestra el sector y la unidad vecinal deducidos de su ubicación.
- El {guilabel}`Historial` de un registro muestra quién hizo cada cambio y cuándo.
- Los cambios de otras personas aparecen en el mapa sin recargar la página, en unos cinco segundos.

## Problemas frecuentes

- **«No se pudo cargar el fondo de mapa. El mapa sigue disponible…»**: los registros y sus formas siguen en pantalla; solo falta el fondo. La administración revisa el mapa base ({doc}`/administracion/mapas-base`).
- **«No hay calles cargadas en este mapa.»**: las calles de la comuna no están importadas. El sector se dibuja a mano.
- **«Las calles elegidas no cierran alrededor de ese punto…»**: elegir más tramos, hacer clic en otro punto dentro del sector o dibujar el sector a mano.
- **«Todavía no se conoce el trazado de todas las calles del límite…»**: acercar el mapa a esas calles para cargarlas, o dibujar el sector a mano.
- **«No tenemos permiso para usar su ubicación…»**: activar el permiso en el candado de la barra de direcciones y volver a pulsar {guilabel}`¿Dónde estoy?`.
- **Una categoría o subcategoría no se deja quitar**: la aplicación rechaza quitarla mientras tenga registros; primero se reclasifican esos registros. La división territorial no se puede quitar nunca, porque todo sector y toda unidad vecinal se guarda en ella.
