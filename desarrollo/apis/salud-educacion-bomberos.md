---
tipo: referencia
audiencia: desarrollo
apps: [Databases, territorio]
resumen: "Capas de salud, educación y bomberos del Geoportal de Chile: servicios, campos, fechas y comparación con el ArcGIS del MINSAL."
---
# Salud, educación y bomberos

## Resumen

Cuatro familias de capas puntuales sirven para ubicar establecimientos en el mapa de territorio. Tres tienen servicio WFS y WMS en vivo en el GeoServer del Geoportal de Chile; los cuarteles de bomberos se publican solo como archivo. Las direcciones son de espacio de trabajo, no del punto general `ows` ({doc}`geoportal-cl`).

## Tabla

| Capa | Servicio | Registros | Fecha |
| --- | --- | --- | --- |
| Establecimientos de salud de Chile, junio de 2026 | `https://geoportal.cl/geoserver/EstablecimientosdesaluddeChile2026/wfs` y `/wms`; capa `EstablecimientosdesaluddeChile2026:establecimientos_de_salud_junio_2026` | 5.295 puntos | Registro de abril de 2026 |
| Educación escolar | `https://geoportal.cl/geoserver/Establecimientos_Educacion_Escolar/wfs` y `/wms`; capa `establecimientos_educacin_escolar` | 11.285 | 2022 |
| Educación parvularia | `https://geoportal.cl/geoserver/Establecimientos_Educacion_Parvularia/wfs` y `/wms`; capa `establecimientos_educacin_parvularia` | 11.951 | 2022 |
| Educación superior | `https://geoportal.cl/geoserver/Establecimientos_Educacion_Superior/wfs` y `/wms`; capa `establecimientos_de_educacin_superior` | 1.297 | 2022 |
| Catastro Nacional de Cuarteles de Bomberos | Descarga `https://geoportal.cl/bomberos/catalog/download/3f6271ef-787f-3a27-9821-307eebc2eecb` | Archivo ZIP de 115 KB | 2025 |

Consulta de ejemplo, con paginación y respuesta en GeoJSON:

```
https://geoportal.cl/geoserver/EstablecimientosdesaluddeChile2026/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=EstablecimientosdesaluddeChile2026:establecimientos_de_salud_junio_2026&outputFormat=application/json&count=100&startIndex=0
```

Un filtro CQL se añade con `cql_filter`, por ejemplo `cql_filter=nom_comuna='Iquique'`. La respuesta trae `totalFeatures` y `numberMatched`; con `resultType=hits` se obtiene solo el conteo.

Campos principales de la capa de salud:

| Grupo | Campos |
| --- | --- |
| Identidad | `cod_vig` (código vigente del DEIS), `nombre`, `tipo`, `ambito`, `nivel`, `complejida`, `estado` |
| Administración | `dependenc`, `dep_adm`, `pertenenci`, `certifi`, `prestador` |
| Urgencia | `urgencia`, `tipo_urge`, `clas_sapu` |
| Ubicación | `cut_region`, `cut_provin`, `cut_comuna`, `nom_region`, `nom_provin`, `nom_comuna`, `direccion`, `numero`, `fono`, `latitud`, `longitud` |

La geometría es un punto en EPSG:4326; la capa trae además `geom_3857` como atributo.

## Notas

**Comparación con ArcGIS del MINSAL.** El servicio `EstablecimientosSaludOficialDEIS_Capavista` de la IDE del MINSAL (catálogo: `arcgis-establecimientos-deis`) tiene 4.337 establecimientos. Al compararlo el 18 de octubre de 2026 por código DEIS con la capa de junio de 2026 del Geoportal, 4.231 códigos están en ambos. Hay 1.064 solo en el Geoportal, en su mayoría centros de salud privados, clínicas dentales, centros de especialidades, salas de toma de muestras y laboratorios. Y hay 106 solo en ArcGIS: 88 «Vigente en operación» y 18 en operación transitoria. Ambas fuentes incluyen únicamente sitios vigentes. El Geoportal es la fuente más completa para prestadores privados, y ArcGIS queda como respaldo oficial.

**Vigencia de la educación.** Las tres capas de educación son de 2022. El MINEDUC publica datos de 2025 en `centroestudios.mineduc.cl/datos-abiertos`, solo como descarga. Cualquier uso debe mostrar la fecha de la fuente.

**Bomberos.** No hay servicio en vivo. El archivo se descarga con una cookie de sesión que el servidor fija en la primera respuesta; no requiere cuenta.

**Paginación.** El WFS entrega el conjunto completo si no se pide `count`. Para capas grandes, como las de educación, conviene paginar con `startIndex` y `count`.
