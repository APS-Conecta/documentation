---
tipo: guia
esqueleto: borrador
audiencia: administracion
apps: [gestion]
resumen: "Mantenimiento diario: salud de la pila, deriva de la configuración, imágenes, respaldos y actualizaciones."
---
# Operaciones

## Resumen

El Mantenimiento diario de la instalación abarca la salud de la pila, la deriva de la configuración, el seguimiento de las imágenes de contenedores, el ciclo de vida de las aplicaciones vendored y la arquitectura de bitácoras con sus volúmenes.

## Secciones previstas

- Mantenimiento — Monitoreo de salud
- Respaldo
- Actualización de imágenes
- Solución de problemas

````{upstream} admin_manual/maintenance/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
- {nc-doc}`admin_manual/maintenance/backup`
- {nc-doc}`admin_manual/maintenance/restore`
- {nc-doc}`admin_manual/maintenance/upgrade`
- {nc-doc}`admin_manual/maintenance/update`
- {nc-doc}`admin_manual/maintenance/manual_upgrade`
- {nc-doc}`admin_manual/maintenance/package_upgrade`
- {nc-doc}`admin_manual/maintenance/migrating`
- {nc-doc}`admin_manual/maintenance/migrating_owncloud`
````

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
