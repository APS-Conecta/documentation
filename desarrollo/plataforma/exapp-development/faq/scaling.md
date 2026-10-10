---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo escalan las ExApps con AppAPI: escalado vertical a cargo de la ExApp, horizontal con servidor-trabajador, y GPU compartidas por daemon."
---
# Escalado

## Resumen

Esta página explica que AppAPI delega el escalado en la propia ExApp, cómo lograr un escalado horizontal básico con una arquitectura servidor-trabajador y cómo se comparten las GPU de un daemon de despliegue. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/faq/Scaling.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

AppAPI delega la tarea de escalado en la propia ExApp.
Esto significa que la ExApp debe diseñarse de forma que pueda escalar verticalmente.
En cuanto al escalado horizontal, actualmente no es posible salvo usando,
por ejemplo, una arquitectura servidor-trabajador, que es una buena forma de ofrecer capacidades básicas de escalado.
En ese caso, el servidor es la ExApp propia y los trabajadores son las máquinas externas que pueden trabajar con la ExApp
mediante la autenticación de usuarios de Nextcloud.
Se pueden añadir (o conectar), opcionalmente, clientes (o trabajadores) adicionales a la ExApp
para aumentar la capacidad y el rendimiento.

### Escalado de GPU

Actualmente, si un daemon de despliegue está configurado con GPU disponibles,
AppAPI conectará de forma predeterminada todos los dispositivos GPU disponibles a cada contenedor de ExApp de ese daemon de despliegue.
Esto significa que esas GPU se comparten entre todas las ExApps del mismo daemon de despliegue.
Por lo tanto, para las ExApps que hacen un uso intensivo de GPU,
se recomienda disponer de un daemon de despliegue (host) separado para ellas.
````
