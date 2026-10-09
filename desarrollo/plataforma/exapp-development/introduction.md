---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Qué son las ExApps y AppAPI, las tareas principales del ecosistema AppAPI y un glosario de los términos que usa su código."
---
# Introducción

## Resumen

Esta página explica qué son las ExApps y AppAPI, cuáles son las tareas principales del ecosistema AppAPI y qué significan los términos que se usan con frecuencia en su código. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/Introduction.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Las **ExApps** (abreviatura de «External Apps») son apps de Nextcloud desarrolladas en otro lenguaje de programación (fuera de PHP) mediante la API OCS de AppAPI.
[AppAPI](https://apps.nextcloud.com/apps/app_api) es un proyecto que {vendor}`Nextcloud` presentó para revolucionar el proceso de desarrollo de aplicaciones dentro del ecosistema de Nextcloud.

### Descripción general

Las tareas principales del ecosistema AppAPI son:

- Proporcionar un método fiable y rápido para autenticar aplicaciones
- Admitir diversas opciones de despliegue de aplicaciones
- Ofrecer una interfaz de administración de aplicaciones clara y sencilla
- Garantizar una implementación fiable de todas las API faltantes que las aplicaciones necesitan
- Proporcionar documentación clara y comprensible, y soporte, sobre cómo implementar bibliotecas en otros lenguajes de programación para escribir aplicaciones de nueva generación para Nextcloud

El sistema debe admitir la ampliación y la integración de nuevos métodos de despliegue, evitando cualquier acoplamiento estrecho con un tipo de despliegue específico.
Las aplicaciones deben poder indicar los métodos de despliegue que admiten.

Dado el panorama cambiante de las nuevas tecnologías y la posible aparición de opciones de despliegue más complejas o más simplificadas,
el sistema está diseñado para acoger sin fricciones la integración de nuevos modos de despliegue.

Si hay preguntas o correcciones sobre la documentación,
con gusto se atenderán en las discusiones, las correcciones se incorporarán mediante pull requests
y los problemas complejos se tratarán mediante issues.

### Glosario

AppAPI introduce los siguientes términos, de uso frecuente en el código:

- `ExApp` (External App) - la app en otro lenguaje de programación (distinto de PHP), que usa la API OCS de AppAPI
- `DaemonConfig` - configuración del daemon de orquestación (p. ej., Docker) donde se despliegan las ExApps
- `DeployConfig` - opciones adicionales de DaemonConfig para el orquestador (p. ej., la red) y para las ExApps (nextcloud_url, host, etc.)
- `ExAppConfig` - similar a *app_config* de Nextcloud, pero para la configuración de las ExApps
- `ExAppPreferences` - similar a *app_preferences* de Nextcloud, ajustes específicos de cada usuario para las ExApps
- `AppAPIAuth` - autenticación de AppAPI
- `FileActionsMenu` - entrada del menú de acciones de archivos (menú contextual)
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
