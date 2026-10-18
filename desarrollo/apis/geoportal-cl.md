---
tipo: referencia
audiencia: desarrollo
apps: [Databases, territorio]
resumen: "El catálogo CSW y el GeoServer del Geoportal de Chile: cómo descubrir capas, qué dirección usar y por qué el punto general de GeoServer aparece vacío."
---
# Geoportal de Chile

## Resumen

El Geoportal de Chile (`geoportal.cl`) publica sus capas por dos vías que no requieren credenciales: un catálogo de metadatos OGC CSW y un GeoServer con un espacio de trabajo por capa publicada. La interfaz web del portal es una aplicación de página única que redirige a un inicio de sesión, pero esa pantalla no protege las dos vías anteriores.

El catálogo CSW lo sirve pycsw 2.6.1 con el nombre «GeoNodo Geospatial Catalogue», en las versiones 2.0.2 y 3.0.0. El 17 de octubre de 2026 tenía 996 registros. Cada registro lista sus servicios en `dct:references`, con el esquema que indica el protocolo.

## Tabla

| Pieza | Dirección | Notas |
| --- | --- | --- |
| Capacidades del catálogo | `https://geoportal.cl/csw?service=CSW&version=2.0.2&request=GetCapabilities` | Sin parámetros responde las capacidades de la versión 3.0.0 |
| Registros | `https://geoportal.cl/csw?service=CSW&version=2.0.2&request=GetRecords&typenames=csw:Record&resulttype=results&elementsetname=full&startposition=1&maxrecords=100` | Un máximo de 100 registros por página; se avanza con `startposition` |
| Un registro | `.../csw?service=CSW&version=2.0.2&request=GetRecordById&id=<id>` | El identificador es el `dc:identifier` del registro, con sus llaves codificadas (`%7B…%7D`) |
| WFS de un espacio de trabajo | `https://geoportal.cl/geoserver/<espacio>/wfs` | Versión 2.0.0; `outputFormat=application/json` entrega GeoJSON |
| WMS de un espacio de trabajo | `https://geoportal.cl/geoserver/<espacio>/wms` | Versión 1.3.0 |
| Descarga de una capa | `https://geoportal.cl/geoportal/catalog/download/<uuid>` | Entrega un archivo ZIP; fija una cookie de sesión, sin inicio de sesión |

Las referencias de los 996 registros suman 1.517 enlaces: 1.190 descargas, 163 servicios WMS 1.3.0, 72 de ArcGIS FeatureServer, 55 de ArcGIS MapServer, 30 archivos shapefile y 7 servicios WFS 2.0.0. La lista completa se regenera con `make inventory` en `APIs/` y queda en `APIs/inventory/geoportal-cl.csv` del repositorio Databases.

## Notas

El punto general `https://geoportal.cl/geoserver/ows` responde 200, pero no lista ninguna capa: el documento de capacidades WFS no trae tipos de entidad y el WMS no trae capas. Una verificación del 1 de agosto de 2026 concluyó a partir de eso que el GeoServer no tenía capas anónimas, y el catálogo lo registró así. Esa conclusión era errónea: cada espacio de trabajo publicado responde de forma anónima en su propia dirección, y los registros del catálogo CSW enlazan a esas direcciones. La entrada `geoportal-cl` del catálogo de APIs quedó corregida.

Los nombres de capa pueden perder los acentos del título, por ejemplo `establecimientos_educacin_escolar`. Se toman siempre del documento de capacidades y no se deducen del título.

Los registros declaran los derechos de uso de forma heterogénea y varios no declaran licencia. La entrada del catálogo marca `license: unknown` y {doc}`/desarrollo/licencias` recoge los términos de uso de las coordenadas del Geoportal como punto pendiente de revisión legal.
