---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Reglas de la tienda de apps: pautas legales, técnicas y de respeto a los usuarios, pérdida de la calificación y cómo mover el repositorio a la organización."
---
(nc-dev-app-store-publishing)=
# Las reglas de la tienda de apps de {vendor}`Nextcloud`

## Resumen

Esta página reúne las reglas de la tienda de apps: los principios de la publicación, cuándo una app pierde su calificación, las pautas legales, técnicas y de respeto a los usuarios que debe cumplir, y cómo mover su repositorio a la organización de GitHub del proyecto. Está dirigida a quienes publican apps.

````{upstream} developer_manual/app_publishing_maintenance/publishing.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La tienda de apps de {vendor}`Nextcloud` está integrada en Nextcloud para permitir hacer llegar las apps propias a los usuarios de la forma más fácil y segura posible.
La tienda de apps y el proceso de publicación de apps pretenden ser:

- seguros
- transparentes
- acogedores
- justos
- fáciles de mantener

### Pérdida de la calificación

Las apps pueden perder su calificación:

- cuando se determina que ya no cumplen los requisitos
- cuando se encuentran problemas de seguridad o de intención maliciosa
- cuando un desarrollador lo solicita

### Pautas para las apps

Estas son las pautas para las apps que una app debe cumplir para tener la posibilidad de ser aprobada.

#### Aspectos legales y de seguridad

- Las apps deben tener la licencia AGPL-3.0-or-later o cualquier licencia compatible.
- Las apps no deben usar «{vendor}`Nextcloud`» en su nombre.
- Pueden realizarse, y se realizarán, auditorías de seguridad irregulares y sin previo aviso de todas las apps.
- Si se encuentra cualquier indicio de intención maliciosa o mala fe, los desarrolladores en cuestión pueden contar con una prohibición mínima de 2 años en cualquier infraestructura de {vendor}`Nextcloud`.
  - La intención maliciosa incluye espiar deliberadamente a los usuarios filtrando datos de usuario a un sistema de terceros o añadir una puerta trasera (como una cuenta de usuario codificada de forma fija) a Nextcloud. Un fallo de seguridad no intencionado que se corrija a tiempo no se considerará mala fe.
- Las apps no infringen ninguna ley; deben cumplir la legislación sobre derechos de autor y sobre marcas.
- Los autores de las apps deben responder a tiempo a los problemas de seguridad y no hacer que Nextcloud sea más vulnerable a ataques.

:::{note}
Distribuir aplicaciones maliciosas o ilegales puede tener consecuencias legales, entre ellas, aunque no solo, que {vendor}`Nextcloud` o los usuarios afectados emprendan acciones legales.
:::

#### Solidez técnica

- Las apps solo pueden usar la API pública de Nextcloud.
- En el momento de publicar una app, solo puede configurarse como compatible con la última versión de Nextcloud +1.
- Las apps no deberían hacer que Nextcloud falle, consumir memoria en exceso ni ralentizar Nextcloud.
- Las apps no deberían entorpecer la funcionalidad de Nextcloud, a menos que ese sea explícitamente el objetivo de la app.

#### Respetar a los usuarios

- Las apps deben seguir las pautas de diseño y las {nc-doc}`pautas de maquetación HTML/CSS <developer_manual/html_css_design/css>`.
- Las apps se limpian correctamente al desinstalarse y gestionan correctamente las actualizaciones y las vueltas a versiones anteriores.
- Las apps comunican claramente su propósito y sus funciones activas, incluidas las funciones introducidas mediante actualizaciones.
- Las apps respetan las decisiones de los usuarios y no hacen cambios inesperados ni limitan la capacidad de los usuarios de revertirlos. Por ejemplo, no eliminan otras apps ni desactivan ajustes.
- Las apps deben respetar la privacidad de los usuarios. Si se envían datos de usuario a algún lugar, esto debe explicarse claramente y reducirse al mínimo necesario para el funcionamiento de la app. Usar las medidas de seguridad adecuadas cuando sea necesario.
- Los autores de las apps deben ofrecer medios para contactarlos, ya sea mediante un gestor de errores, un foro o correo.

Las apps que incumplan las pautas perderán su estado «aprobada» u «oficial», y podrían bloquearse por completo en la tienda de apps. Esto también tiene repercusiones para el autor: especialmente en caso de problemas de seguridad, podría verse bloqueado para enviar aplicaciones.

### Mover el repositorio a la organización de {vendor}`Nextcloud`

¡Siempre nos alegra saber que quienes desarrollan apps están interesados en mover su app a la organización de {vendor}`Nextcloud` en [github.com/nextcloud](https://github.com/nextcloud)! Estar ahí tiene ventajas para los usuarios y para los desarrolladores. Sin embargo, también conlleva algunos requisitos.

#### Ventajas

- Se pueden usar las herramientas y los bots que tenemos configurados, incluidas las traducciones, entre otros
- Todas las personas de la organización de {vendor}`Nextcloud` pueden contribuir con más facilidad
- Aumenta la propia visibilidad ante quienes desarrollan apps
- Los usuarios pueden esperar que las apps de nuestro proyecto estén mejor mantenidas

#### Requisitos

Para cumplir las promesas anteriores, tenemos dos reglas sencillas.

- Se trabaja y se comunica según los valores de nuestro [Código de conducta](https://nextcloud.com/contribute/code-of-conduct/)
- Cuando se deja de estar activo, nuestros administradores pueden decidir traspasar el mantenimiento a otra persona colaboradora

Queremos asegurarnos de que, cuando aparezcan otras cosas en la vida que sean más urgentes o, por otros motivos, ya no se pueda ayudar al proyecto, este no se convierta en «código muerto» mientras haya personas que quieran mantenerlo vivo. Eso no es justo para los usuarios, que se verían obligados a eliminar la app e instalar otra.

¡Tener en cuenta que el rol de quien mantiene un proyecto no es ser la persona colaboradora más activa o más prolífica del proyecto! Ser amable, acogedor y receptivo es lo que hace falta para ser un mantenedor exitoso. No ser el desarrollador más brillante de la historia ni pasar noches y fines de semana programando.

El objetivo de estas reglas es sencillo: ayudar a que el proyecto tenga más éxito. También sugerimos ver esta charla de [Jan sobre cómo construir una gran comunidad.](https://www.youtube.com/watch?v=UtAoRIKVpW4)

#### Cómo moverlo

Para mover el repositorio a nuestra organización de GitHub, basta con pedírselo a cualquiera de nuestros colaboradores, [especialmente a quienes son administradores.](https://github.com/orgs/nextcloud/people?utf8=%E2%9C%93&query=+role%3Aowner) ¡Estarán encantados de ayudar!
````
