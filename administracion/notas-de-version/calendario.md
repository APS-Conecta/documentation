---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo se publican y mantienen las versiones mayores y de mantenimiento de Nextcloud: calendario, fin de vida, canales, betas y regresión de versión."
---
# Calendario de mantenimiento y publicación

## Resumen

Esta página explica los dos tipos de versiones de Nextcloud Server, su ritmo de publicación, cuánto dura el soporte de cada versión mayor y qué significa el fin de vida, además de los canales de publicación, las versiones beta y candidatas, la regresión de versión y el informe de errores. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/release_schedule.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Descripción general

{vendor}`Nextcloud` publica varias versiones mayores *a lo largo* del año, pero mantiene el soporte de *cada* versión mayor durante un año completo mediante actualizaciones de mantenimiento «más ligeras» (y [retroportando](https://en.wikipedia.org/wiki/Backporting) con regularidad las correcciones de seguridad y de errores aplicables). Esto permite un ritmo de desarrollo muy rápido y, a la vez, da a los administradores flexibilidad al planificar despliegues, actualizaciones y tareas de mantenimiento.

Un [calendario detallado de las próximas versiones mayores y de mantenimiento](https://github.com/nextcloud/server/wiki/Maintenance-and-Release-Schedule) (así como las previsiones de fin de vida) se actualiza con regularidad para facilitar la planificación del despliegue, de las pruebas y de las actualizaciones.

Tanto si se quieren las funciones y optimizaciones más recientes, como si se quiere ayudar con las pruebas o simplemente esperar a que todo esté perfectamente listo, hay opciones en cuanto a qué versión de Nextcloud Server desplegar inicialmente y con qué frecuencia hacer actualizaciones mayores.

:::{danger}
Se recomienda siempre instalar las últimas versiones de **mantenimiento** lo antes posible, sea cual sea la versión mayor de Nextcloud Server que se use. Y se recomienda siempre, encarecidamente, actualizar desde las versiones en **fin de vida** lo antes posible.
:::

:::{tip}
El mantenimiento extendido y el soporte adicional están disponibles mediante [opciones de suscripción para soporte empresarial](https://nextcloud.com/enterprise/) que ofrecen los desarrolladores de {vendor}`Nextcloud` a través de [Nextcloud GmbH](https://nextcloud.com).
:::

### Tipos de versiones

{vendor}`Nextcloud` tiene dos tipos de versiones en el canal de publicación predeterminado:

1. Versiones mayores
2. Versiones de mantenimiento

Las versiones **mayores** de Nextcloud Server (p. ej., `28.X.X`) introducen nuevas funciones y funcionalidades.

Cada versión mayor recibe, a su vez, soporte durante *un año* mediante versiones de **mantenimiento** periódicas (p. ej., `X.X.4`), que corrigen errores críticos y vulnerabilidades de seguridad.

#### Versiones mayores

Las versiones mayores suelen introducir funciones nuevas y a menudo incluyen también cambios «bajo el capó». Estos cambios pueden ser extensos.

Una versión mayor concreta se indica con la primera parte de la cadena de versión. Por ejemplo, Nextcloud Server `28.0.4` es la versión mayor `28`. Y `27.1.7` es la versión mayor `27`.

:::{tip}
La versión mayor de número más alto ofrece las funciones más recientes, mientras que la versión mayor de número más bajo ofrece el mayor tiempo de uso en producción.
:::

:::{note}
Puede ser necesario cumplir nuevos requisitos del sistema antes de que el Updater ofrezca una nueva versión mayor. Incluso si la ofrece, puede haber otros cambios necesarios que el Updater no puede comprobar por completo. Se intenta destacarlos, en cada nueva edición del Manual de administración, en la sección Cambios críticos del capítulo *Notas de versión*.
:::

:::{warning}
Las apps suelen definir su compatibilidad en función de la versión o versiones mayores de Nextcloud Server que admiten. Conviene tener en cuenta la compatibilidad de las apps preferidas y más críticas con una posible versión mayor de Nextcloud Server antes de elegir qué versión mayor desplegar o de decidir cuándo actualizar a una versión mayor recién disponible. Además, como muchas apps las aporta la comunidad y las mantienen voluntarios, puede ser conveniente ofrecerse a probar la app con una nueva versión mayor de Nextcloud (o a adaptarla, si se está en condiciones de hacerlo) para propiciar una publicación más rápida (o de mayor calidad).
:::

#### Versiones de mantenimiento

Las versiones de mantenimiento, deliberadamente, **no** introducen funciones nuevas ni cambios incompatibles. Con ello se busca reducir los riesgos y el impacto asociados al despliegue de actualizaciones, de modo que los errores críticos o las vulnerabilidades de seguridad puedan corregirse de forma rápida y rutinaria.

Las versiones de mantenimiento se publican (en general, simultáneamente) para todas las versiones mayores estables que no han llegado al estado de fin de vida.

Estas versiones no deberían plantear problemas de compatibilidad de las apps ni introducir cambios que exijan volver a formar a los usuarios finales.

Una versión de mantenimiento concreta se indica con la última parte del número de versión. Por ejemplo, `28.0.4` es la *cuarta* versión de mantenimiento de la versión mayor `28` de Nextcloud Server. Ofrece correcciones de todos los errores críticos y vulnerabilidades de seguridad resueltos desde la versión de mantenimiento anterior (`28.0.3` en este ejemplo).

:::{note}
Todas las correcciones de errores críticos, incluidas las relacionadas con la seguridad, se [retroportan](https://en.wikipedia.org/wiki/Backporting) a **todas** las versiones mayores mantenidas.
:::

### Calendario de publicación

Las nuevas versiones **mayores** de Nextcloud Server se publican aproximadamente cada dieciséis semanas.

Las nuevas versiones de **mantenimiento** se publican aproximadamente cada cuatro semanas.

#### Duración del soporte («mantenimiento»)

El calendario de publicación implica que varias versiones mayores (p. ej., 26.X.X, 27.X.X, 28.X.X) reciben soporte simultáneamente. Cada vez que se corrige un error crítico o una vulnerabilidad, si afecta a más de una versión mayor, se **retroporta** a todas las versiones mayores correspondientes y se publica en la siguiente versión de mantenimiento (p. ej., `28.0.3` -> `28.0.4`). Toda versión mayor que no haya llegado al estado de fin de vida recibe estas actualizaciones de mantenimiento.

Este calendario solapado y su ritmo predecible permiten un desarrollo rápido y, a la vez, dan a los administradores visibilidad, acceso a las correcciones de errores críticos y flexibilidad en cuanto a con qué rapidez actualizar a nuevas versiones mayores.

:::{note}
Como cada versión mayor recibe soporte durante un año desde su publicación inicial, lo mínimo que hay que hacer para mantenerse al día es instalar las versiones de mantenimiento a medida que se publican y actualizar a la siguiente versión mayor cuando la que se usa llega al estado de fin de vida. Como las versiones de mantenimiento solo aplican al servidor las últimas correcciones de errores y de vulnerabilidades de seguridad, y **no** introducen otros cambios significativos, el riesgo de actualizar a una nueva versión de mantenimiento es mucho menor que el de actualizar a una nueva versión mayor.
:::

#### Fin de vida

El estado de fin de vida significa que termina el soporte o mantenimiento. Las versiones de mantenimiento de una versión mayor cesan al cumplirse un año de su publicación inicial. La versión mayor pasa entonces al estado de fin de vida y no recibirá más correcciones de errores ni de vulnerabilidades de seguridad.

:::{note}
El soporte de las versiones mayores puede ampliarse mediante [servicios de suscripción para empresas](https://nextcloud.com/enterprise/) que ofrecen los desarrolladores de {vendor}`Nextcloud` a través de [Nextcloud GmbH](https://nextcloud.com).
:::

Las fechas de fin de vida de todas las versiones mayores se [publican](https://github.com/nextcloud/server/wiki/Maintenance-and-Release-Schedule) con antelación para facilitar la planificación.

:::{note}
Mientras una versión mayor siga figurando en el [calendario de mantenimiento](https://github.com/nextcloud/server/wiki/Maintenance-and-Release-Schedule) como *Currently Maintained*, cabe esperar que reciba todas las correcciones pertinentes de errores críticos o vulnerabilidades de seguridad (incluso las que se publiquen para versiones mayores más nuevas, si son pertinentes para una versión mayor anterior que aún tenga soporte).
:::

### Versión de instalación

Como a lo largo del año se publican varias versiones mayores y cada una recibe soporte durante un año con todas las correcciones pertinentes de errores y de seguridad, se puede decidir qué versión mayor desplegar inicialmente y cuándo actualizar a una nueva versión mayor.

:::{note}
Si se planea desplegar Nextcloud en un entorno empresarial y su uso va a ser de misión crítica, los desarrolladores pueden ayudar, mediante un [acuerdo de servicios empresariales](https://nextcloud.com/enterprise/), a elegir la versión mayor más adecuada para el caso de uso concreto, así como a asegurar que se despliegue de forma óptima, atendiendo de forma personalizada cualquier problema crítico que surja.
:::

### Canales de publicación

De forma predeterminada, todas las instalaciones de Nextcloud usan el canal de publicación `stable`. Este canal ofrece las funciones más recientes que están listas para la mayoría de los usuarios, con un riesgo mínimo.

:::{note}
{vendor}`Nextcloud` despliega las nuevas versiones de forma escalonada para reducir aún más el riesgo de actualizaciones generalizadas. Las nuevas versiones, en particular las mayores, normalmente solo se ponen a disposición de un pequeño porcentaje de sistemas al principio. Cuando ha pasado una semana (o más) sin que se hayan informado errores críticos generalizados, se ofrece la actualización a más sistemas. A veces las versiones mayores se limitan a <100% de los sistemas hasta que se publica la primera versión de mantenimiento (de corrección de errores).
:::

:::{warning}
Al usar el canal `stable`, es posible que se *ofrezca* actualizar a una versión mayor más nueva *aunque* la versión mayor actual **no** haya llegado al estado de fin de vida. Corresponde a quien administra decidir si actualizar en ese momento o esperar a un momento más oportuno para desplegar una nueva versión mayor. En cambio, las nuevas versiones de **mantenimiento** (dentro de la versión mayor que ya se ejecuta) deben desplegarse lo antes posible para mantenerse al día con las correcciones de seguridad y de otros errores críticos.
:::

:::{danger}
Es fundamental asegurarse de ejecutar una versión **mayor** con mantenimiento activo. Una vez que una versión mayor llega al estado de fin de vida, no recibirá más versiones de mantenimiento que corrijan errores críticos o vulnerabilidades.
:::

El calendario detallado de todas las versiones mayores y de mantenimiento del canal estable, incluidas las fechas de fin de vida, está en el [Calendario de mantenimiento y publicación](https://github.com/nextcloud/server/wiki/Maintenance-and-Release-Schedule), que se actualiza con regularidad.

### Actualizaciones de versión mayor

Antes de actualizar de una versión mayor a otra, se recomienda encarecidamente revisar la sección *Cambios críticos* del capítulo **Notas de versión** para minimizar la posibilidad de introducir cambios incompatibles inesperados en el entorno.

:::{warning}
Tener buenas copias de seguridad de los datos (¡y un procedimiento de restauración probado!) es recomendable en general, pero sin duda antes de realizar una actualización, ya sea mayor o simplemente de mantenimiento.
:::

### Versiones beta y candidatas a versión final

Antes de publicar una nueva versión mayor final, normalmente se publican al menos cuatro versiones beta, seguidas de dos candidatas a versión final, con un intervalo de una semana entre cada una.

Antes de publicar una nueva versión de mantenimiento final, se publica una candidata a versión final aproximadamente una semana antes.

Las fechas previstas de cada versión se encuentran en el [calendario detallado](https://github.com/nextcloud/server/wiki/Maintenance-and-Release-Schedule).

:::{tip}
Para actualizar antes a una nueva versión mayor o a una versión beta, se puede, a criterio propio, configurar la instancia para que use el canal `beta`. En torno a las grandes publicaciones, el canal `beta` también ofrece antes la versión mayor más reciente, independientemente de los parámetros del despliegue escalonado.
:::

Toda la comunidad se beneficia considerablemente de las generosas pruebas y comentarios de quienes deciden evaluar versiones beta o candidatas a versión final, ya sea en sus entornos de prueba o, los más audaces, en condiciones reales.

Si se está en condiciones de evaluar una versión previa a la final, ¡los desarrolladores y toda la comunidad lo agradecen!

:::{tip}
Se sugiere centrar las pruebas en verificar las funciones y características de las que se depende a diario (para asegurarse de que funcionan como se espera). Después, si se desea, considerar la evaluación de cualquier funcionalidad nueva que resulte de interés. Conviene plantear los problemas que surjan en el [Foro de ayuda](https://help.nextcloud.com) e informar de los presuntos errores en [el repositorio de GitHub](https://github.com/nextcloud/server/issues).
:::

### Regresión a una versión anterior

Volver a una versión anterior no está admitido oficialmente entre ninguna versión mayor, de mantenimiento o previa a la final.

### Informe de errores

Antes de informar de errores, conviene asegurarse de ejecutar una versión mayor que aún tenga soporte *y* la última versión de mantenimiento de esa versión mayor.

:::{tip}
Nextcloud GmbH, que emplea a muchos de los desarrolladores principales, ofrece [servicios de Nextcloud Enterprise](https://nextcloud.com/enterprise/) que dan acceso directo a la experiencia en ingeniería de {vendor}`Nextcloud` cuando el uso es de misión crítica. Entre otras cosas, pueden ayudar a elegir la versión mayor más adecuada para el caso de uso (y asegurar que se despliegue de forma óptima).
:::
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
