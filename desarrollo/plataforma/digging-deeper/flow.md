---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo una app se integra en el motor de flujos de trabajo Flow: entidades que exponen eventos, operaciones que actúan sobre ellos y su configuración."
---
# Nextcloud Flow

## Resumen

Esta página explica el motor de flujos de trabajo basado en eventos Flow y cómo una app lo extiende: las entidades que exponen eventos, las operaciones que actúan sobre ellos y el componente de JavaScript con el que se configuran. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/flow.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud Flow es un motor de flujos de trabajo basado en eventos y definido por el usuario.

Las aplicaciones pueden exponer, por un lado, entidades con eventos específicos y, por otro, operaciones que actúan sobre esos eventos. Un usuario define una regla de flujo de trabajo que se dispara con un evento determinado y que luego ejecuta la operación en función de comprobaciones definidas por el usuario.

Un flujo de ejemplo podría ser convertir documentos de Word en PDF cuando se añaden a una carpeta y, una vez terminado, mover ese documento de Word a otra carpeta. Este flujo de trabajo trataría con el evento de creación de la entidad de archivo y actuaría sobre ese archivo.

En el 36c3, blizzz dio una charla en la que explicaba Flow y [cómo escribir acciones y disparadores.](https://media.ccc.de/v/36c3-oio-174-building-nextcloud-flow) Se pueden [encontrar aquí las diapositivas de su charla.](https://web.archive.org/web/20220219081809/https://nextcloud.com/wp-content/themes/next/assets/files/Building_nextcloud_flow.pdf)

### Entidades

Para exponer eventos a través de Nextcloud Flow hay que definir una entidad, que es una clase que implementa `OCP\WorkflowEngine\IEntity`.

La clase de la entidad expone un nombre para la interfaz de usuario mediante `getName()` y una URL de icono mediante `getIcon()`.

El método `getEvents()` devuelve un array con todos los eventos que puede experimentar esta entidad, que el usuario podrá seleccionar en la interfaz de flujos.

Para todos los eventos que ocurren en la instancia de nextcloud (ver {nc-ref}`Events` para todos los eventos integrados conocidos), se llamará a `prepareRuleMatcher()`, para que pueda comprobar si este evento es uno de los que la entidad pone a disposición en flow.

Si es así, la entidad puede asignarse a sí misma al comparador de reglas.

De forma similar, `isLegitimatedForUserId()` comprobará si el usuario pasado tiene permitido ver el evento actual (lo que requiere guardar el evento que se pasó a `prepareRuleMatcher()`).

### Operaciones

Las operaciones son acciones que los usuarios pueden configurar para que ocurran cuando se producen eventos específicos.

Una operación es una clase que implementa ISpecificOperation, IOperation o IComplexOperation. Las operaciones específicas solo pueden actuar sobre una entidad concreta (p. ej., un archivo), mientras que las operaciones normales pueden actuar sobre todos los eventos. Las operaciones complejas no escuchan eventos, sino que configuran su propio listener o sus propios listeners.

La operación debe implementar el método `validateOperation`, al que se llamará al validar en los ajustes una configuración de flujo para el flujo propio. La función debe comprobar que la configuración es correcta y lanzar una excepción si no lo es.
Una vez que el usuario ha configurado la operación, se llamará a su método `onEvent` en cualquier evento para el que esté configurada, aunque las reglas no coincidan. Por eso hay que usar el parámetro `$ruleMatcher` para recorrer las reglas coincidentes y comprobar si hay alguna. Para cada coincidencia, la clave 'operation' del array es lo que el usuario configuró para esta regla en los ajustes.

### Componente de configuración

El componente de configuración es lo que ve el usuario cuando añade el flujo y pasa a configurar sus reglas.

Para el componente de configuración se crea un nuevo bundle de JavaScript

```
import ConvertToPdf from './ConvertToPdf' // A Vue component

OCA.WorkflowEngine.registerOperator({
    id: 'OCA\\WorkflowPDFConverter\\Operation',
    operation: 'keep;preserve',
    options: ConvertToPdf,
    color: '#dc5047'
})
```

En el listener de `RegisterOperationsEvent` hay que registrar el bundle de JS anterior.

La función `OCA.WorkflowEngine.registerOperator` informa a Nextcloud de la operación, junto con el color y el componente que contiene la configuración específica del flujo.
````
