---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo documentar cambios que afectan a quienes desarrollan apps: definición de terminado, notas de versión, API nuevas y obsoletas, y notas de administración."
---
# Compatibilidad con el ecosistema de apps

## Resumen

Esta página explica por qué hay que informar a quienes desarrollan apps de los cambios que les afectan y describe los procedimientos para documentarlos, además del requisito de documentar en las notas de versión de administración los cambios que afectan a quienes administran. Está dirigida a quienes desarrollan sobre la plataforma.

````{upstream} developer_manual/prologue/compatibility_app_ecosystem.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El ecosistema de apps de {vendor}`Nextcloud` está formado por cientos de apps y de mantenedores de apps.

El proceso de desarrollo puede requerir cambios que afecten a las apps de este ecosistema. Estos cambios pueden ser un cambio de estándares o de buenas prácticas, pero, en los casos más extremos, también pueden romper apps.

Aunque se espera que quienes desarrollan procuren limitar el número de cambios que rompen apps, esto no siempre puede evitarse o no siempre es razonable si se quiere mantener un conjunto tecnológico actualizado.

Por eso, informar a quienes desarrollan apps de cualquier cambio que les afecte es clave para un ecosistema próspero. Esta página describe los tres procedimientos para documentar los cambios que son relevantes para quienes desarrollan apps.

### Procedimientos de documentación de los cambios que afectan a quienes desarrollan apps

Hay tres procedimientos establecidos para facilitar la comunicación con quienes desarrollan apps sobre los cambios que les afectan:

1. La definición de **terminado** de una pull request incluye la documentación.

   Esto significa que el desarrollo de la pull request no puede considerarse terminado si se introdujeron cambios (adiciones, eliminaciones o modificaciones) que afectan a quienes desarrollan apps y no se documentaron.

2. Un cambio que quienes desarrollan apps deben aplicar para mantener la compatibilidad de sus apps en una nueva versión debe notificarlo y documentarlo el autor de la pull request en la sección {nc-ref}`Notas de versión <critical-changes>`.

   Los requisitos de esta documentación son:

   - Debe redactarse en formato de tutorial, de modo que quienes desarrollan apps entiendan cómo sortear el cambio en su app
   - Los pasos deben escribirse de forma explícita, de modo que la documentación no dependa de enlaces a recursos externos para los pasos. Aunque se recomienda añadir enlaces externos como referencia adicional, es un requisito estricto que la documentación pueda leerse y aplicarse sin necesidad de abrir ese enlace.
   - El nombre del autor del cambio debe añadirse a la sección para que los lectores puedan contactar con el autor si tienen preguntas o si algo no está claro.
   - Plazo: es obligatorio entregar la documentación al finalizar la pull request, y debería fusionarse en un momento cercano al propio cambio.

3. Las nuevas API se anuncian en {nc-ref}`new-apis`, pero necesitan una sección de documentación propia.

4. Las obsolescencias se recopilan en {nc-ref}`deprecated-apis`.

### Otros requisitos de documentación

Un cambio que afecte a los administradores que actualizan su Nextcloud debe documentarse en la sección de notas de versión de la documentación de administración de esa versión.
````
