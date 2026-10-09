---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Punto de entrada a la gestión de ExApps: AppAPI, daemons de despliegue, configuraciones de ejemplo, prueba de despliegue y opciones avanzadas."
---
# Gestión de ExApps

## Resumen

Esta página agrupa, para quienes administran el servidor, los temas de la gestión de ExApps: las aplicaciones externas que AppAPI instala como contenedores Docker. Cada tema se describe en su propia página de esta sección.

````{upstream} admin_manual/exapps_management/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/exapps/index

- {nc-doc}`admin_manual/exapps_management/AppAPIAndExternalApps`
- {nc-doc}`admin_manual/exapps_management/DeployConfigurations`
- {nc-doc}`admin_manual/exapps_management/ManagingDeployDaemons`
- {nc-doc}`admin_manual/exapps_management/TestDeploy`
- {nc-doc}`admin_manual/exapps_management/ManagingExApps`
- {nc-doc}`admin_manual/exapps_management/AdvancedDeployOptions`
````

## En APS Conecta Gestión

APS Conecta Gestión no ejecuta aplicaciones externas (ExApps). AppAPI queda instalada sin cambios porque la hoja de ruta la usa, pero la provisión no registra ningún daemon de despliegue y el contenedor opcional HaRP del AIO viene desactivado. La postura de producción del daemon sigue abierta en [gestion#75](https://github.com/APS-Conecta/gestion/issues/75).

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
