---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Categorías de la API pública de PHP (OCP) según sus atributos, y reglas para publicar una API inestable en el espacio de nombres NCU."
---
# Referencia de la API

## Resumen

Esta página explica cómo se divide la API pública de PHP del espacio de nombres OCP según los atributos de sus interfaces, enums y clases, y qué reglas rigen la API inestable del espacio de nombres NCU. Está dirigida a quienes desarrollan sobre la plataforma.

````{upstream} developer_manual/digging_deeper/api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### API pública de PHP

La API pública está contenida en el espacio de nombres OCP. Ver la [referencia de la API OCP](https://nextcloud-server.netlify.app/) para más detalles.

La API se divide en dos categorías, que se indican mediante atributos.

#### `Consumable`, `Listenable` y `Catchable`

Las interfaces, enums y clases que tienen el atributo `OCP\AppFramework\Attribute\Consumable` solo deben ser consumidas por las apps y las apps no pueden implementarlas por sí mismas.
Esto significa que el lado del servidor puede extender la interfaz con nuevos métodos o reducir los tipos devueltos de los métodos existentes sin que se considere una ruptura de la API.
Sin embargo, los tipos de los argumentos de los métodos existentes **no** se pueden reducir.
Las mismas reglas se aplican a los `OCP\EventsDispatcher\Event` que tienen el atributo `OCP\AppFramework\Attribute\Listenable` y a las `Exception` con el atributo `OCP\AppFramework\Attribute\Catchable`.

#### `Implementable`, `Dispatchable` y `Throwable`

Las interfaces, enums y clases que tienen el atributo `OCP\AppFramework\Attribute\Implementable` pueden ser implementadas por las apps.
Esto significa que el lado del servidor **no** puede extender la interfaz con nuevos métodos ni reducir los tipos devueltos de los métodos existentes sin que se considere una ruptura de la API.
Sin embargo, los tipos de los argumentos de los métodos existentes se pueden reducir.
Las mismas reglas se aplican a los `OCP\EventsDispatcher\Event` que tienen el atributo `OCP\AppFramework\Attribute\Dispatchable` y a las `Exception` con el atributo `OCP\AppFramework\Attribute\Throwable`.

##### `ExceptionalImplementable`

Aunque no son implementables por todas las apps, algunas interfaces pueden tener el atributo `OCP\AppFramework\Attribute\ExceptionalImplementable`, que indica que una sola app (o varias) puede implementarlas.
En esos casos se aplican las reglas generales de `OCP\AppFramework\Attribute\Consumable`, pero hay que informar a los mantenedores de las apps o al repositorio de las excepciones nombradas durante el proceso de una pull request, de modo que tengan tiempo suficiente para adaptarse al cambio que se avecina.

### API inestable de PHP

Para evitar publicar una API pública incompleta, es posible publicar una primera versión de la futura API en el espacio de nombres *NCU*, siguiendo estas reglas:

- Los archivos se ubican en `/lib/unstable/`
- Se espera que la calidad del código, los comentarios, las pruebas y la comprobación de psalm sean idénticos a los del espacio de nombres *OCP*.
- Las clases deben etiquetarse como `@experimental`, incluyendo la versión actual de Nextcloud.
- La etiqueta `@since` no debe usarse en el espacio de nombres *NCU*.
- El código del espacio de nombres *OCP* nunca debe mencionar nada que provenga del espacio de nombres *NCU*. No puede requerirlo como argumento ni como constante, ni devolver algo de *NCU*.
- Una API solo puede vivir en este espacio de nombres inestable durante una versión mayor.
- Durante esta fase de pruebas, el código y la API pueden modificarse o reestructurarse sin limitación.
- La API dentro del espacio de nombres de pruebas debe tener documentación actualizada.
- Si se acepta, la API se copiará al espacio de nombres público *OCP*.
- Una vez probada, la versión del espacio de nombres *NCU* se marcará como obsoleta.
- Las API obsoletas del espacio de nombres *NCU* se mantienen durante 2 versiones mayores.

:::{note}
- Las API de *NCU* se incluyen en el paquete `nextcloud-deps/OCP` para facilitar las pruebas con psalm
:::
````
