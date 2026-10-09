---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Opciones de despliegue avanzadas de AppAPI: variables de entorno y montajes para el contenedor de una ExApp, desde la página de apps o la CLI."
---
# Opciones de despliegue avanzadas

## Resumen

Esta página explica, para quienes administran el servidor, las opciones de despliegue avanzadas de AppAPI: las variables de entorno y los montajes que pueden configurarse para el contenedor de una ExApp, y dónde se configuran.

````{upstream} admin_manual/exapps_management/AdvancedDeployOptions.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/exapps/index

(nc-ai-app_api_deploy_options)=
AppAPI permite configurar, de forma opcional, variables de entorno y montajes para el contenedor de la ExApp.

Está disponible mediante el modal «Opciones del despliegue», junto al botón «Desplegar y habilitar», en la barra lateral de la página de la ExApp, en la página de gestión de apps. La pantalla muestra el botón «Opciones del despliegue» junto a «Desplegar y habilitar» en la barra lateral de la ExApp, en la página de apps de AppAPI.

O mediante la CLI ({nc-ref}`advanced_deploy_options_cli`).

### Variables de entorno

Las variables de entorno permiten una configuración más precisa de la ExApp. Los desarrolladores de ExApps pueden definir la lista de variables de entorno admitidas, con sus descripciones; solo esas variables estarán disponibles para configurar.

De forma predeterminada, solo hay montajes disponibles para configurar.

Cuando la ExApp está instalada, se muestra la lista de variables de entorno establecidas.

### Montajes

Los montajes pueden usarse para proporcionar datos adicionales al contenedor de la ExApp desde el host. Por ejemplo, para algunas apps será útil proporcionar una carpeta con los certificados SSL de la nube, de modo que la app pueda gestionar HTTPS correctamente sin tener que reinstalar la ExApp.
````
