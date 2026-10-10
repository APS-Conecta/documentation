---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "El rol de quien mantiene una app: clasificar errores, gestionar pull requests, versiones y vulnerabilidades, y contar con mantenedores de respaldo."
---
(nc-dev-app-maintainer)=
# Mantenedores

## Resumen

Esta página describe el rol de quien mantiene una app y sus responsabilidades: clasificar los informes de errores y gestionar los pull requests, las versiones y las vulnerabilidades. Está dirigida a quienes mantienen apps.

````{upstream} developer_manual/app_publishing_maintenance/maintainer.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El rol de quien mantiene una app de Nextcloud es supervisar todos los procesos relacionados con una app. Sus responsabilidades son:

- Clasificar los informes de errores

  - Asegurarse de que los errores informados sean reproducibles y pedir más información si es necesario
  - Comprobar si hay duplicados
  - Cerrar los tickets resueltos

- Gestionar los pull requests

  - Asegurarse de que los pull requests reciban una revisión en un tiempo razonable
  - Fusionar los pull requests que superen la revisión por pares y todas las comprobaciones de integración continua
  - Lanzar los backports cuando corresponda

- Gestionar las versiones

  - Asegurarse de que las versiones preliminares estén listas para desplegarse en la preproducción del servidor Nextcloud
  - Asegurarse de que las versiones compatibles estén listas para los despliegues de las versiones del servidor Nextcloud

- Gestionar las vulnerabilidades

  - Vigilar las dependencias vulnerables, p. ej., mediante las alertas de seguridad de Github, y publicar actualizaciones a tiempo
  - Coordinar las vulnerabilidades divulgadas con el equipo de seguridad de {vendor}`Nextcloud`

Para evitar el llamado [factor bus](https://en.wikipedia.org/wiki/Bus_factor), se recomienda encarecidamente tener más de un mantenedor para cada app. Las apps pueden tener un mantenedor principal y uno o más mantenedores de respaldo. Por transparencia, puede tener sentido declarar los mantenedores de una app en el archivo README del repositorio de la app, para que otras personas sepan a quién contactar.
````
