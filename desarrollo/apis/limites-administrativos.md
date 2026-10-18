---
tipo: referencia
audiencia: desarrollo
apps: [Databases, territorio]
resumen: "Límites administrativos de Chile: el servicio WMS de CIREN para el MINAGRI, la descarga de la División Política Administrativa 2023 y los códigos CUT."
---
# Límites administrativos

## Resumen

La División Política Administrativa 2023 del Geoportal de Chile se publica solo como archivo ZIP de 311 MB (`DPA_2023.zip`), sin servicio WFS ni WMS. Para mostrar límites sobre un mapa, el servicio WMS 1.3.0 de CIREN para el MINAGRI es la vía en vivo; para cruzar datos, los establecimientos ya traen los códigos únicos territoriales (CUT) de región, provincia y comuna.

## Tabla

| Pieza | Dirección | Uso |
| --- | --- | --- |
| WMS de límites administrativos | `https://esri.ciren.cl/server/services/IDEMINAGRI/LIMITES_ADMINISTRATIVOS_MINAGRI/MapServer/WMSServer` | Capa raster de fondo; sin consultas de entidades |
| Capacidades | `...WMSServer?service=WMS&version=1.3.0&request=GetCapabilities` | Lista las capas, de nombres numéricos (`1`, `2`, `3`, `4`, `6`, `7`) |
| DPA 2023 (descarga) | `https://geoportal.cl/geoportal/catalog/download/912598ad-ac92-35f6-8045-098f214bd9c2` | ZIP de 311 MB; registro del 10 de noviembre de 2023 |

## Notas

El WMS entrega imágenes, así que un navegador las carga de forma directa y la política de seguridad de contenido de la aplicación debe permitir el servidor `esri.ciren.cl`. Una capa WMS sirve para dibujar, no para saber a qué comuna pertenece un punto; esa pertenencia se obtiene del CUT de la comuna que ya trae cada establecimiento.

Otros servicios del mismo servidor, bajo `/server/services/IDEMINAGRI/`, siguen el mismo patrón, por ejemplo `CATASTRO_FRUTICOLA`, `HUMEDALES` e `INCENDIOS`.

El catálogo de APIs registra el WMS como `ciren-wms-limites-administrativos` y la descarga como `geoportal-dpa-2023` (fuera de alcance, por su tamaño). El Geoportal también publica otras divisiones: la línea digital de los límites interiores (2022), y las divisiones de la Antártica Chilena, Isla de Pascua y Juan Fernández a través de la IDE del MINAGRI, solo como descarga.
