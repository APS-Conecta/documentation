---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo procesa Nextcloud una solicitud HTTP: el controlador frontal, la carga de las apps básicas, la autenticación, las rutas y la ejecución del enrutador."
---
# Ciclo de vida de una solicitud

## Resumen

Esta página describe las partes de una solicitud HTTP y los pasos con que el servidor la procesa, desde el controlador frontal {file}`index.php` hasta la ejecución del enrutador. Está dirigida a quienes desarrollan apps y quieren entender el funcionamiento interno antes de definir sus rutas.

````{upstream} developer_manual/basics/request_lifecycle.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Una solicitud HTTP típica consta de lo siguiente:

* **Una URL**: p. ej., /index.php/apps/myapp/something
* **Parámetros de la solicitud**: p. ej., ?something=true&name=tom
* **Un método**: p. ej., GET
* **Cabeceras de la solicitud**: p. ej., Accept: application/json

Las secciones siguientes presentan un panorama de cómo se procesa esa solicitud, para dar una visión en profundidad de cómo funciona Nextcloud. Si no interesan los detalles internos o no se quiere ejecutar nada antes y después del controlador, se puede omitir esta sección y pasar directamente a definir {nc-doc}`las rutas de la app <developer_manual/basics/routing>`.

### Controlador frontal

Al principio, todas las solicitudes se envían al {file}`index.php` de Nextcloud, que a su vez ejecuta {file}`lib/base.php`. Este archivo inspecciona las cabeceras HTTP, abstrae las diferencias entre los distintos servidores web e inicializa las clases básicas. Después se cargan las apps básicas en el siguiente orden:

* Backends de autenticación
* Sistema de archivos
* Registro

El tipo de la app se determina inspeccionando su {nc-doc}`archivo de configuración <developer_manual/app_development/info>` ({file}`appinfo/info.xml`). Cada app instalada se carga y se ejecuta (ver {nc-doc}`Arranque <developer_manual/app_development/bootstrap>`). Eso significa que, si se quiere ejecutar código antes de que se ejecute una app concreta, se puede colocar ese código en el archivo {nc-doc}`developer_manual/app_development/init` de la app.

Después se realizan los pasos siguientes:

* Intentar autenticar al usuario
* Cargar y ejecutar los archivos {nc-doc}`developer_manual/app_development/init` de todas las apps restantes
* Cargar y ejecutar todas las rutas de los {file}`appinfo/routes.php` de las apps
* Ejecutar el enrutador
````
