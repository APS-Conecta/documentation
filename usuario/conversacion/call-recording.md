---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Grabar llamadas de Talk: iniciar y detener una grabación, compartir el archivo grabado y pedir el consentimiento de grabación."
---
(nc-call-recording)=
# Grabación de llamadas

## Resumen

Esta página explica cómo un moderador inicia y detiene la grabación de una llamada de Talk, dónde queda el archivo grabado y cómo funciona el consentimiento de grabación para los participantes.

````{upstream} user_manual/talk/call_recording.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La función de grabación permite:

- Iniciar y detener grabaciones durante una llamada.
- Grabar la transmisión de video y audio de quien habla, así como la pantalla compartida.
- Acceder a los archivos grabados, compartirlos y descargarlos para consultarlos o distribuirlos más adelante.

Para habilitar esta función, la administración del sistema debe configurar el servidor de grabación.

### Gestionar una grabación

El moderador de la conversación puede iniciar una grabación junto con el inicio de una llamada o en cualquier momento durante una llamada:

- **Antes de la llamada**: marcar la casilla «Iniciar la grabación inmediatamente con la llamada» en «Media settings» y luego hacer clic en «Comenzar llamada».
- **Durante la llamada**: hacer clic en el menú de la barra superior y luego en «Empezar a grabar».

La grabación comenzará en breve y se verá un indicador rojo junto al tiempo de la llamada. La grabación se puede detener en cualquier momento mientras la llamada sigue en curso, haciendo clic en ese indicador y seleccionando «Detener grabación», o con la misma acción del menú de la barra superior. Si no se detiene la grabación manualmente, terminará automáticamente cuando termine la llamada.

Después de detener una grabación, el servidor tardará unos segundos en preparar y guardar el archivo grabado. El moderador que inició la grabación recibe una notificación cuando el archivo se ha subido. Desde ahí, se puede compartir en el chat.

### Consentimiento de grabación

Para cumplir con las normativas de privacidad, es posible pedir a los participantes su consentimiento para ser grabados antes de unirse a la llamada. Los administradores pueden configurar esta función de varias maneras:

- Desactivar el consentimiento por completo.
- Activar el consentimiento obligatorio en todo el sistema, exigiéndolo en todas las conversaciones.
- Permitir que los moderadores configuren esta opción a nivel de conversación. En ese caso, los moderadores pueden acceder a los ajustes de la conversación para configurar esta opción según corresponda.

Si el consentimiento de grabación está activado, todos los participantes, incluidos los moderadores, verán una sección resaltada en «Media settings» antes de unirse a una llamada.
Esta sección informa a los participantes de que la llamada puede grabarse. Para dar su consentimiento explícito a la grabación, los participantes deben marcar la casilla. Si no dan su consentimiento, no se les permitirá unirse a la llamada.

Una vez terminada la llamada, la grabación se procesa y se guarda en el chat como archivo compartido. Los participantes pueden reproducirla directamente desde el chat o descargarla desde los elementos compartidos de la conversación.
````
