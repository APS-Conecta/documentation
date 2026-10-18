---
tipo: explicacion
audiencia: desarrollo
apps: [Databases, territorio]
resumen: "Dos fuentes que no se integran: el geoportal de FONASA, cuya API exige sesión, y el Visor de Ciclovías de SECTRA, un panel y no una API."
---
# FONASA y ciclovías

## Contexto

Al mapear las fuentes geoespaciales aparecieron dos que parecen APIs y no lo son. Se documentan para que nadie repita la investigación, y ambas figuran en el catálogo de APIs ({doc}`/desarrollo/databases`) con alcance excluido.

## Diseño

### Geoportal de FONASA

`geoportal.fonasa.cl` es una aplicación de página única en React que carga mapas de Google. Su backend está en `https://api.cloud-prd.fonasa.cl/geoportal` y expone rutas de colecciones (`colecciones-grupos`, `colecciones-region`), geocodificación (`geo/coordinates`), un mantenedor y administración de usuarios y de carga de planillas. Todas las rutas sondeadas sin credenciales responden 403, y los nombres de las rutas indican una herramienta de administración interna, no una API pública.

La entrada del catálogo es `fonasa-geoportal`, con estado `gated` y alcance excluido. El camino para usar sus datos es pedir acceso oficial a FONASA; no se extraen datos ni se reproducen las llamadas privadas de la aplicación. Mientras tanto, los registros del DEIS cubren los establecimientos ({doc}`salud-educacion-bomberos`).

### Visor de Ciclovías Chile

El panel de ArcGIS `d2c380a49743480e86a628daeb696e9f` es el «Visor de Ciclovías Chile» de SECTRA, del Ministerio de Transportes y Telecomunicaciones. Un panel es un visor, no una API. Su mapa web (`bbe5baae95aa4896bd976121e1667efd`, `CICLOV_validVisor`) tiene una sola capa operativa: la línea `CICLOVIA_jul2026`, con 4.850 entidades y un máximo de 2.000 registros por consulta, en `https://services6.arcgis.com/feQ9HId8vmgonvvD/arcgis/rest/services/CICLOV_validVisor_WFL1/FeatureServer/0`. Sus campos incluyen región, comuna, eje de la vía, kilómetros y tipo. Otros dos elementos del panel son privados.

La entrada del catálogo es `sectra-ciclovias-featureserver`. Se excluye porque no corresponde a un caso de uso de la atención primaria; queda registrada con su capa real por si el caso aparece.

## Compromisos y límites

Ninguna de las dos fuentes alimenta hoy el mapa de territorio. Si FONASA concede acceso, esta página cambia a una referencia de la API con sus condiciones. La capa de ciclovías puede cambiar de dirección sin aviso, porque depende del panel de un tercero.
