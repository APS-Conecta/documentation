---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "La aplicación Correo: cuentas y ajustes, redacción, bandeja de salida, acciones sobre mensajes, filtros, seguridad e integración con el calendario."
---
# Usar la aplicación Correo

## Resumen

Esta página describe la aplicación Correo: la gestión de cuentas y sus ajustes, la redacción de mensajes, la bandeja de salida, las acciones sobre buzones y mensajes, los filtros y la respuesta automática, la seguridad y la integración con el panel y el calendario. Está dirigida a usuarios que leen y envían correo desde la interfaz web.

````{upstream} user_manual/groupware/mail.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: usuario/groupware/correo
:::{note}
La aplicación Correo viene instalada de forma predeterminada con Nextcloud Hub, pero se puede deshabilitar. Consultar al administrador.
:::

### Gestionar la cuenta de correo

#### Cambiar el diseño

:::{versionadded} 3.6 Nextcloud 26 o posterior
:::

1. Ir a los ajustes del correo
2. Elegir entre *Lista*, *División vertical* y *División horizontal*

#### Usar el modo compacto

:::{versionadded} 5.7 Nextcloud 32 o posterior
:::

El modo compacto ofrece una forma más limpia y eficiente de ver los mensajes. Los avatares se ocultan, las casillas de selección están siempre visibles y se elimina la vista previa de los mensajes. Ahorra espacio y permite ver más correos a la vez.

1. Ir a los ajustes del correo
2. Ir a **Apariencia**
3. Activar el modo compacto

#### Visualización de mensajes / modo de operación

:::{versionadded} 5.2 Nextcloud 30 o posterior
:::

Correo puede alternar entre dos modos distintos de vista y de operación de mensajes: *Por hilos* e *Individual*.

En el modo *Por hilos*, los mensajes se agrupan por conversación. En la lista de mensajes del buzón, los mensajes relacionados se apilan de modo que solo se muestra el más reciente, y todos los mensajes relacionados se muestran en el panel de visualización de mensajes al seleccionar el mensaje apilado. Esto es útil para seguir discusiones y comprender el contexto de las respuestas. En este modo, las operaciones sobre mensajes, como mover y eliminar, se aplican a todo el hilo; es decir, al mover o eliminar un hilo, se ven afectados todos los mensajes de ese hilo.

En el modo *Individual*, los mensajes se muestran por separado, tanto en la lista de mensajes del buzón como en el panel de visualización de mensajes, y las operaciones como mover y eliminar se aplican solo al mensaje seleccionado. Este modo es útil cuando se desea gestionar los mensajes por separado sin afectar a toda la conversación.

1. Ir a los ajustes del correo
2. Elegir entre *Por hilos* e *Individual*

#### Añadir una cuenta de correo nueva

1. Habilitar la aplicación Correo desde las aplicaciones
2. Hacer clic en el icono de correo de la cabecera
3. Rellenar el formulario de inicio de sesión (automático o manual)

#### Cambiar el orden

:::{versionadded} 3.5 Nextcloud 26 o posterior
:::

1. Ir a los ajustes del correo
2. Ir a *Ordenamiento*
3. Se puede elegir que aparezca primero el correo *más antiguo* o el *más reciente*

:::{note}
Este cambio se aplicará a todas las cuentas y buzones
:::

#### Ordenar los favoritos arriba

:::{versionadded} 5.7 Nextcloud 31 o posterior
:::

Este ajuste permite mostrar los mensajes marcados como favoritos en una sección aparte, encima de la lista de mensajes.

1. Ir a los ajustes del correo
2. Ir a *Apariencia*
3. Habilitar la ordenación de favoritos arriba

(nc-mail-scheduled-messages)=
#### Mensajes programados

1. Hacer clic en el botón **Nuevo mensaje**
2. Hacer clic en el menú de acciones (...) del compositor modal
3. Hacer clic en *Enviar más tarde*

#### Bandeja prioritaria

La bandeja prioritaria tiene 2 secciones: *Importante* y *Otros*. Los mensajes se marcarán automáticamente como importantes según los mensajes con los que se haya interactuado o que se hayan marcado como importantes. Al principio puede que sea necesario cambiar la importancia manualmente para enseñar al sistema, pero irá mejorando con el tiempo.

La clasificación automática es opcional. Se puede desactivar al configurar una cuenta. La clasificación también se puede activar y desactivar en cualquier momento en los ajustes de la cuenta.

#### Todas las bandejas de entrada

Aquí se mostrarán en orden cronológico todos los mensajes de todas las cuentas en las que se haya iniciado sesión.

(nc-mail-account-settings)=
#### Ajustes de la cuenta

Los ajustes de la cuenta, como:

1. Aliases
2. Firma
3. Carpetas predeterminadas
4. Respuestas automáticas
5. Remitentes de confianza
6. ...y más

Se encuentran en el menú de acciones de una cuenta de correo. Allí se pueden editar, añadir o eliminar ajustes según las necesidades.

#### Mover mensajes a la carpeta de correo no deseado

:::{versionadded} 3.4 Nextcloud 26 o posterior
:::

Correo puede mover un mensaje a otra carpeta cuando se marca como no deseado.

1. Ir a los ajustes de la cuenta
2. Ir a Carpetas predeterminadas
3. Comprobar que haya una carpeta seleccionada para los mensajes no deseados
4. Ir a los ajustes de correo no deseado
5. Hacer clic en Mover mensajes a la carpeta de correo no deseado

#### Actualizar el buzón

Se puede iniciar manualmente una sincronización del buzón haciendo clic en el botón de actualizar, situado en la parte superior de la lista del buzón. A partir de la `version 5.7`, iniciar la sincronización también actualiza la lista de carpetas de la cuenta seleccionada.

#### Búsqueda unificada

La aplicación Correo se integra con la función de {nc-ref}`búsqueda unificada <unified-search>` de Nextcloud (consultar {nc-doc}`Interfaz web <user_manual/webinterface>` para más detalles). Se pueden buscar correos en todas las cuentas usando la barra de búsqueda de la cabecera de Nextcloud.

Correo busca en los asuntos de los correos y en los campos de remitente y destinatario. Para buscar en el cuerpo de los correos, usar la función de búsqueda en el buzón de la aplicación.

#### Buscar en el buzón

:::{versionadded} 2.1 Nextcloud 25 o posterior
:::

En la parte superior de la lista de sobres, en cualquier diseño del correo, hay un atajo de campo de búsqueda para buscar en los asuntos de los correos. A partir de la `version 3.7`, este atajo permite buscar de forma predeterminada por asunto, destinatario (para) o remitente (de).

#### Búsqueda avanzada en el buzón

:::{versionadded} 3.4 Nextcloud 26 o posterior
:::

Se puede acceder a la función de búsqueda avanzada mediante una ventana modal situada al final del atajo de búsqueda.

#### Habilitar la búsqueda en el cuerpo de los mensajes

:::{versionadded} 3.5 Nextcloud 26 o posterior
:::

Ahora se puede buscar en el cuerpo de los correos; esta función es opcional debido a posibles problemas de rendimiento.

Para habilitarla:

1. Ir a los ajustes de la cuenta
2. Ir a Búsqueda en el buzón
3. Habilitar la búsqueda en el cuerpo de los mensajes

:::{warning}
Si también se desea habilitarla para los buzones unificados, hay que hacerlo en los ajustes del correo
:::

Al habilitarla, el cuadro de búsqueda principal buscará tanto en los asuntos como en el cuerpo de los correos, y aparecerá una opción *Cuerpo* separada en la búsqueda avanzada.

#### Delegación de cuentas

La aplicación permite la delegación de cuentas, de modo que un usuario puede enviar correos desde la dirección de otro.

1. Un administrador debe configurar la delegación en el servidor de correo
2. Añadir la otra dirección de correo como alias de la propia cuenta de correo
3. Al enviar un correo, seleccionar el alias como remitente

:::{warning}
Es posible que el correo enviado no sea visible para la cuenta original si se guarda en el buzón personal de *Enviados*.
:::

#### Eliminación automática de la papelera

:::{versionadded} 3.4 Nextcloud 26 o posterior
:::

La aplicación Correo puede eliminar automáticamente los mensajes de la carpeta de papelera después de un número determinado de días.

1. Ir a los ajustes de la cuenta
2. Ir a Vaciado automático de la papelera
3. Introducir el número de días después del cual se deben eliminar los mensajes

Para deshabilitar la retención de la papelera, dejar el campo vacío o establecerlo en 0.

:::{note}
Solo se procesarán los correos eliminados después de habilitar la retención de la papelera.
:::

### Redactar mensajes

1. Hacer clic en el botón **Nuevo mensaje**
2. Empezar a escribir el mensaje

#### Minimizar el compositor modal

:::{versionadded} 3.2 Nextcloud 26 o posterior
:::

El compositor modal se puede minimizar mientras se escribe un mensaje nuevo o se edita un borrador existente o un mensaje de la bandeja de salida. Basta con hacer clic en el botón **Minimizar** de la ventana modal o hacer clic en cualquier lugar fuera de ella.

Se puede retomar el mensaje minimizado haciendo clic en cualquier lugar del indicador del compositor minimizado.

Pulsar el botón **Cerrar** de la ventana modal o del indicador del compositor minimizado para dejar de editar un mensaje. Se guardará automáticamente un borrador en el buzón de borradores.

### Información del destinatario en el compositor

:::{versionadded} 4.2 Nextcloud 30 o posterior
:::

Al añadir el primer destinatario o contacto en el campo "Para", aparecerá un panel a la derecha con los datos de perfil guardados de ese contacto. Al añadir un segundo contacto, la lista se contraerá y se podrá seleccionar y expandir cualquiera de los contactos añadidos para ver sus datos. Si se prefiere centrarse solo en escribir en el compositor, se puede ocultar el panel derecho haciendo clic en el icono **Expandir** de la barra de herramientas del compositor. Para volver a mostrar el panel derecho, basta con hacer clic en el icono **Minimizar** de la misma barra de herramientas.

### Mencionar contactos

:::{versionadded} 4.2 Nextcloud 30 o posterior
:::

Se pueden mencionar contactos en el mensaje escribiendo `@` y luego seleccionando el contacto de la lista. Al hacerlo, el contacto se añadirá automáticamente como destinatario.

:::{note}
Solo se sugerirán contactos con una dirección de correo electrónico válida.
:::

### Bloques de texto

:::{versionadded} 5.2 Nextcloud 30 o posterior
:::

Los bloques de texto son fragmentos de texto predefinidos que se pueden insertar en el correo. Se pueden crear y gestionar en los ajustes del correo. Se pueden insertar en el compositor escribiendo `!` y luego seleccionando el bloque de la lista, o desde las acciones del compositor. Los bloques de texto se pueden compartir con usuarios y grupos de usuarios.

### Bandeja de salida

Cuando se ha redactado un mensaje y se ha hecho clic en el botón "Enviar", el mensaje se añade a la **Bandeja de salida**, que aparece en la parte inferior de la barra lateral izquierda.

También se puede fijar la fecha y la hora del envío en un momento futuro (ver {nc-ref}`Mensajes programados <mail-scheduled-messages>`): el mensaje se conservará en la bandeja de salida hasta que llegue la fecha y la hora elegidas, y entonces se enviará automáticamente.

La bandeja de salida solo es visible cuando hay un mensaje esperando a que la bandeja de salida lo procese.

Se puede volver a abrir el compositor de un mensaje de la bandeja de salida en cualquier momento antes de que se inicie el envío.

:::{note}
Cuando se produce un error durante el envío, hay tres mensajes de error posibles:

- No se pudo copiar a la carpeta "Enviados": el correo se envió, pero no se pudo copiar al buzón "Enviados". La bandeja de salida gestionará este error y volverá a intentar la copia.
- Error del servidor de correo: el envío no tuvo éxito, con un estado que permite reintentarlo (p. ej., no se pudo contactar con el servidor SMTP). La bandeja de salida volverá a intentar enviar el mensaje.
- No se ha podido enviar el mensaje: es posible que el envío haya fallado o no. El servidor de correo no puede informarnos del estado del mensaje. Como la aplicación Correo no tiene forma de determinar el estado del mensaje (enviado o no enviado), el mensaje permanecerá en la bandeja de salida y el usuario de la cuenta tendrá que decidir cómo proceder.
:::

### Acciones de buzón

#### Añadir un buzón

1. Abrir el menú de acciones de una cuenta
2. Hacer clic en añadir buzón

#### Añadir un subbuzón

1. Abrir el menú de acciones de un buzón
2. Hacer clic en añadir subbuzón

#### Buzón compartido

Si se ha compartido un buzón con ciertos permisos específicos, ese buzón aparecerá como un buzón nuevo con un icono de compartido, como se muestra a continuación:

### Acciones de sobre

#### Crear un evento

Crear un evento para un mensaje o hilo concreto directamente desde la aplicación Correo

1. Abrir el menú de acciones de un sobre
2. Hacer clic en *Más acciones*
3. Hacer clic en *Crear un evento*

:::{note}
Se crean un título y un orden del día del evento si el administrador lo ha habilitado.
:::

#### Crear una tarea

:::{versionadded} 3.2 Nextcloud 26 o posterior
:::

Crear una tarea para un mensaje o hilo concreto directamente desde la aplicación Correo

1. Abrir el menú de acciones de un sobre
2. Hacer clic en *Más acciones*
3. Hacer clic en *Crear una tarea*

:::{note}
Las tareas se guardan en calendarios compatibles. Si no hay ningún calendario compatible, se puede crear uno nuevo con la {nc-ref}`aplicación Calendario <calendar-app>`.
:::

#### Editar etiquetas

1. Abrir el menú de acciones de un sobre
2. Hacer clic en *Editar etiquetas*
3. En la ventana modal de etiquetas, asignar o quitar etiquetas

#### Cambiar el color de las etiquetas

:::{versionadded} 3.5 Nextcloud 26 o posterior
:::

Al crear una etiqueta, se elige automáticamente un color asignado al azar. Una vez guardada la etiqueta, se puede personalizar su color según las preferencias. Esta función se encuentra en el menú de acciones de la ventana modal de etiquetas.

#### Eliminar etiquetas

:::{versionadded} 3.5 Nextcloud 26 o posterior
:::

Ahora es posible eliminar las etiquetas creadas previamente. Para acceder a esta función:

1. Abrir el menú de acciones de un sobre o hilo.
2. Seleccionar Editar etiquetas.
3. En la ventana modal de etiquetas, abrir el menú de acciones de la etiqueta concreta que se desea eliminar.

:::{note}
Tener en cuenta que las etiquetas predeterminadas, como Trabajo, Por hacer, Personal y Después, no se pueden eliminar; solo se pueden renombrar.
:::

#### Resumen con IA

:::{versionadded} 4.2 Nextcloud 30 o posterior
:::

Al revisar el buzón, se verá como vista previa un breve resumen de los correos generado por IA.

:::{note}
Tener en cuenta que el administrador debe habilitar esta función
:::

### Acciones rápidas

:::{versionadded} 5.5 Nextcloud 30 o posterior
:::

Permiten agrupar los pasos de acción que normalmente se realizarían sobre los sobres, como etiquetar, mover, marcar como leído..., en acciones rápidas que se pueden ejecutar con un solo clic. Las acciones rápidas se limitan a una cuenta de correo y se pueden crear y gestionar en los ajustes del correo, en "Acciones rápidas", o directamente desde el menú de acciones del sobre.

:::{note}
Algunos pasos de acción, como *Marcar como correo no deseado*, *Mover hilo* y *Borrar hilo*, son mutuamente excluyentes y no pueden formar parte de la misma acción rápida; además, no se pueden reordenar y siempre se ejecutarán en último lugar.
:::

:::{note}
Tener en cuenta que, cuando se ejecutan sobre un mensaje, las acciones rápidas se aplicarán a todos los mensajes de su hilo.
:::

### Acciones de mensaje

#### Cancelar la suscripción a una lista de correo

:::{versionadded} 3.1 Nextcloud 26 o posterior
:::

Algunas listas de correo y boletines permiten cancelar la suscripción fácilmente. Si la aplicación Correo detecta mensajes de un remitente así, mostrará un botón *Desuscribirse* junto a la información del remitente. Hacer clic y confirmar para cancelar la suscripción a la lista.

#### Diferir

:::{versionadded} 3.4 Nextcloud 26 o posterior
:::

Diferir un mensaje o hilo lo mueve a un buzón dedicado hasta que llega la fecha de diferido seleccionada; entonces el mensaje o hilo se vuelve a mover al buzón original.

1. Abrir el menú de acciones de un sobre o hilo
2. Hacer clic en *Diferir*
3. Seleccionar durante cuánto tiempo se debe diferir el mensaje o hilo

#### Respuestas inteligentes

:::{versionadded} 3.6 Nextcloud 26 o posterior
:::

Al abrir un mensaje en la aplicación Correo, esta propone respuestas generadas por IA. Con solo hacer clic en una respuesta sugerida, se abre el compositor con la respuesta ya rellenada.

:::{note}
Tener en cuenta que el administrador debe habilitar esta función
:::

:::{note}
Los idiomas admitidos dependen del modelo de lenguaje grande que se use
:::

#### Traducción de correos

:::{versionadded} 4.2 Nextcloud 30 o posterior
:::

Se pueden traducir los mensajes a los idiomas configurados, de forma similar a Talk.

:::{note}
Tener en cuenta que las funciones de traducción deben estar habilitadas en el servidor
:::

:::{note}
Desde la versión 5.3, si el administrador ha habilitado un LLM, se sugerirán traducciones
:::

### Resumen del hilo

La aplicación Correo permite resumir hilos de mensajes que contienen 3 o más mensajes.

:::{versionadded} 3.4 Nextcloud 26 o posterior
:::

:::{note}
Tener en cuenta que el administrador debe habilitar esta función
:::

:::{note}
Tener en cuenta que esta función solo funciona bien con integration_openai. Los LLM locales tardan demasiado en responder, y es probable que la solicitud de resumen agote el tiempo de espera y que, aun así, genere una carga significativa en el sistema.
:::

### Filtros y respuesta automática

La aplicación Correo tiene un editor de scripts Sieve, una interfaz para configurar respuestas automáticas y una interfaz para configurar filtros. Sieve debe estar habilitado en los {nc-ref}`ajustes de la cuenta <mail-account-settings>`.

#### Respuestas automáticas

:::{versionadded} 3.5 Nextcloud 26 o posterior
:::

La respuesta automática está desactivada de forma predeterminada. Se puede configurar manualmente o hacer que siga los ajustes del sistema. Seguir los ajustes del sistema significa que el mensaje de ausencia largo introducido en la {nc-ref}`sección de ajustes de Ausencia <groupware-absence>` se aplica automáticamente.

#### Filtro

:::{versionadded} 4.1 Nextcloud 30 o posterior
:::

Correo 4.1 incluye un editor sencillo para configurar reglas de filtrado.

:::{note}
No se admite importar filtros existentes. Sin embargo, todos los filtros existentes seguirán activos y sin cambios. Como precaución, se recomienda hacer una copia de seguridad del script actual mediante el editor de scripts Sieve.
:::

##### Cómo añadir un filtro nuevo

1. Abrir los ajustes de la cuenta.
2. Comprobar que Sieve esté habilitado para la cuenta (ver los ajustes del servidor Sieve).
3. Hacer clic en Filtros.
4. Seleccionar Nuevo filtro para crear una regla nueva.

##### Cómo eliminar un filtro

1. Abrir los ajustes de la cuenta.
2. Asegurarse de que Sieve esté habilitado para la cuenta (ver los ajustes del servidor Sieve).
3. Hacer clic en Filtros.
4. Pasar el cursor sobre el filtro que se desea eliminar y luego hacer clic en el icono de la papelera.

##### Condiciones

Las condiciones se aplican a los correos entrantes en el servidor de correo y se dirigen a campos como Asunto, Remitente y Destinatario. Se pueden usar los siguientes operadores para definir condiciones para estos campos:

- **es exactamente**: una coincidencia exacta. El campo debe ser idéntico al valor indicado.
- **contiene**: una coincidencia de subcadena. El campo coincide si el valor indicado está contenido en él. Por ejemplo, "report" coincidiría con "port".
- **coincide**: una coincidencia de patrón con comodines. El símbolo "\*" representa cualquier número de caracteres (incluido ninguno), mientras que "?" representa exactamente un carácter. Por ejemplo, "\*report\*" coincidiría con "Business report 2024".

##### Acciones

Las acciones se activan cuando las pruebas especificadas son verdaderas. Están disponibles las siguientes acciones:

- **fileinto**: mueve el mensaje a una carpeta especificada.
- **addflag**: añade una marca al mensaje.
- **stop**: detiene la ejecución del script de filtros. No se procesarán más filtros después de esta acción.

#### Crear un filtro a partir de un mensaje

:::{versionadded} 5.2 Nextcloud 30 o posterior
:::

Para crear un filtro a partir de un mensaje concreto, abrir el mensaje y luego abrir el menú haciendo clic en los tres puntos. A continuación, hacer clic en "Más acciones" y luego en "Crear filtro de correo".

En el diálogo, seleccionar las condiciones que deben cumplir los mensajes entrantes y continuar haciendo clic en "Crear filtro de correo".

### Recordatorios de seguimiento

:::{versionadded} 4.0 Nextcloud 30 o posterior
:::

La aplicación Correo recordará automáticamente cuando un correo saliente no haya recibido respuesta. Una IA analizará cada correo enviado para comprobar si se espera una respuesta. Al cabo de cuatro días, todos los correos relevantes se mostrarán en la bandeja prioritaria.

Al hacer clic en uno de esos correos, se mostrará un botón para hacer rápidamente un seguimiento con todos los destinatarios. También es posible deshabilitar los recordatorios de seguimiento para un correo enviado.

:::{note}
Tener en cuenta que el administrador debe habilitar esta función.
:::

### Seguridad

#### Detección de suplantación de identidad

:::{versionadded} 4.0 Nextcloud 30 o posterior
:::

La aplicación Correo comprobará posibles intentos de suplantación de identidad (phishing) y mostrará una advertencia al usuario.

Las comprobaciones son las siguientes:

- La dirección del remitente guardada en la libreta de direcciones no es la misma que la de la cuenta de correo
- El remitente usa una dirección de correo electrónico personalizada que no coincide con la dirección del campo «De»
- La fecha de envío está en el futuro
- Los enlaces del cuerpo del mensaje no apuntan al texto mostrado
- La dirección de respuesta («Responder a») no es la misma que la dirección del remitente

:::{note}
Tener en cuenta que la advertencia no significa que el mensaje sea un intento de suplantación de identidad. Solo significa que la aplicación Correo detectó un posible intento de suplantación de identidad.
:::

#### Direcciones internas

:::{versionadded} 4.0 Nextcloud 30 o posterior
:::

La aplicación Correo permite añadir direcciones y dominios internos, y advertirá al usuario si la dirección no está en la lista, al enviar y al recibir un mensaje.

Para añadir una dirección interna:

1. Abrir los ajustes del correo
2. Ir a la sección Privacidad y seguridad
3. Habilitar las direcciones internas marcando la casilla
4. Hacer clic en el botón Añadir dirección interna
5. Introducir la dirección o el dominio y hacer clic en Añadir

### Integración con el panel

:::{versionadded} 1.8 Nextcloud 20 o posterior
:::

La aplicación Correo ofrece dos widgets diseñados para integrarse con el panel de Nextcloud:

- Correo no leído: este widget muestra los correos no leídos.
- Correo importante: este widget muestra los correos que se han marcado como importantes.

Estos widgets usan los correos de las cuentas de correo configuradas en la cuenta del usuario.

### Integración con el calendario

La aplicación Correo se integra con la aplicación Calendario para ayudar a gestionar las invitaciones a reuniones y a mantener el calendario al día.

#### Invitaciones a reuniones

Al recibir un mensaje que contiene una invitación a una reunión, la aplicación Correo detecta automáticamente el archivo de calendario adjunto y muestra una sección de acciones con formato para ayudar a responder.

Se puede:

- **Aceptar** la invitación
- **Declinar** la invitación
- **Aceptar tentativamente** la invitación

La respuesta se envía directamente desde la aplicación Correo, y el evento se añade en consecuencia al calendario principal.

También se puede añadir manualmente una invitación a una reunión a un calendario concreto:

1. Abrir el mensaje con la invitación a la reunión
2. Desplazarse hasta el final del mensaje, a la sección de adjuntos
3. Seleccionar el archivo de calendario (normalmente con la extensión .ics) y luego hacer clic en el menú de tres puntos.
4. Hacer clic en "Importar al calendario" y elegir el calendario deseado.

#### Automatización de las invitaciones a reuniones

Cuando el organizador de una reunión envía actualizaciones de un evento existente (como cambios de hora o de ubicación), la aplicación Correo las procesa automáticamente y actualiza el evento correspondiente en el calendario.

:::{versionadded} 5.7 Nextcloud 32 o posterior
:::

También se puede configurar Correo para que añada automáticamente al calendario todas las invitaciones nuevas a reuniones, sin necesidad de aceptarlas manualmente. Las invitaciones se añadirán al calendario como tentativas.

Para habilitar esta función:

1. Ir a los ajustes de la cuenta de una cuenta de correo concreta
2. Ir a la sección de ajustes del calendario
3. Habilitar *Crear automáticamente citas tentativas en el calendario*

:::{note}
Con este ajuste habilitado, las invitaciones seguirán apareciendo en la lista de correo, pero se añadirán automáticamente al calendario.
:::

### Atajos de teclado

La aplicación Correo implementa varios atajos de teclado para agilizar su uso.

Para ver la lista completa de los atajos admitidos, consultar los ajustes del correo en la instancia.
````

## En APS Conecta Gestión

APS Conecta Gestión no incluye Correo. La suite instala un conjunto fijo de aplicaciones y deja desactivada la tienda de aplicaciones: Correo no aparece en el menú y no se puede agregar desde la interfaz.
