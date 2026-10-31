---
tipo: referencia
audiencia: desarrollo
apps: [eurooffice]
resumen: "Edición de documentos, planillas y presentaciones con el conector oficial y DocumentServer oficial."
---
# eurooffice

## Resumen

La suite instala el [conector oficial de Euro-Office](https://github.com/Euro-Office/eurooffice-nextcloud) desde la tienda de aplicaciones de Nextcloud. El servidor utiliza [Euro-Office DocumentServer](https://github.com/Euro-Office/DocumentServer). Ambos conservan el código oficial.

APS Conecta configura las direcciones pública e interna, la autenticación JWT y la conexión con Nextcloud.

## Tabla

| Hecho | Valor |
|---|---|
| Instalación | Paquete oficial compatible con Nextcloud 34, verificado por Nextcloud. |
| Integridad | Firma oficial presente y comprobación nativa `occ integrity:check-app eurooffice`. |
| Validación funcional | Apertura, edición compartida y conservación de los cambios al cerrar el documento. |
| Administración | [Configuración de oficina](/administracion/oficina/index). |
| Registro de cambios | [Novedades](/proyecto/novedades/eurooffice). |

## Notas

La configuración pertenece a la suite; la identidad y los archivos del conector pertenecen al proyecto oficial.
