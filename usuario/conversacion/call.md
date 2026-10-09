---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Iniciar una llamada de Talk o unirse a ella en el navegador, Talk Desktop o móvil, y usar los controles durante la llamada."
---
# Unirse a una llamada

## Resumen

Esta página explica cómo iniciar una llamada de Talk o unirse a ella desde el navegador, el cliente Talk Desktop o los clientes móviles, qué ajustes se pueden elegir antes de entrar y qué controles ofrece la vista de llamada.

````{upstream} user_manual/talk/call.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Iniciar una llamada o unirse a ella

#### Navegador y cliente Talk Desktop

Al formar parte de una conversación y tener permiso para hacerlo, se puede iniciar una llamada en cualquier momento haciendo clic en {guilabel}`Comenzar llamada` en la barra superior.
Cuando ya hay una llamada en curso, para unirse a ella se hace clic en el botón verde {guilabel}`Unirse a la llamada` del área del chat o de la barra superior.

:::{note}
Si todavía no se dio permiso al navegador o al cliente Talk Desktop para usar el micrófono y la cámara, se pedirá hacerlo al hacer clic en {guilabel}`Comenzar llamada` o {guilabel}`Unirse a la llamada`.
Elegir el micrófono y la cámara que se quieren usar y hacer clic en `Allow` para conceder acceso a los dispositivos.
:::

Se mostrará `Media settings`, donde se puede personalizar la experiencia de la llamada.

##### Controlar el audio y el video

Usar los iconos de micrófono y cámara de la parte inferior de la vista previa del video para silenciar o reactivar el micrófono y activar o desactivar la cámara antes de unirse.

:::{note}
Si uno o ambos iconos aparecen en gris, o no hay un micrófono o una cámara instalados, o no se dio permiso al navegador o al cliente Talk Desktop para usar el micrófono o la cámara. Comprobar que se haya concedido el permiso al navegador o al cliente Talk Desktop y asegurarse de que el micrófono y la cámara no los esté usando otra aplicación.
:::

Los ajustes de dispositivos permiten elegir qué micrófono y qué cámara usar. Esto es útil si hay más de un micrófono o más de una cámara disponibles.

##### Supresión de ruido

Para activar la supresión de ruido y reducir el ruido de fondo durante las llamadas, seguir estos pasos:

1. Abrir `Media settings` antes o durante una llamada
2. Buscar la sección `Microphone settings`
3. Activar `Noise suppression` en el nivel deseado

Las opciones de control automático de ganancia y de cancelación de eco también están disponibles en la misma sección.

##### Fondos

Los fondos permiten reemplazar el fondo del video por una de las imágenes predefinidas.
También se puede subir una imagen propia o elegir una que ya esté en Nextcloud Files.
Otra posibilidad es elegir la opción `blur` para desenfocar el fondo del video en vivo.

##### Unirse inmediatamente a una llamada

Para omitir `Media settings` en el futuro, activar el interruptor `Skip device preview before joining a call` en los ajustes de la aplicación.
En las próximas llamadas de esta conversación se entrará directamente, sin el diálogo de vista previa.

##### Grabar una llamada

Si se inició la llamada y se quiere grabarla, marcar la casilla {guilabel}`Iniciar la grabación inmediatamente con la llamada`.
Es posible que la opción de grabar la llamada no esté disponible, según si los administradores del sistema la habilitaron y si se tiene el permiso {guilabel}`Moderador` en la conversación.
Al unirse a una llamada que se está grabando, puede que se pida dar el consentimiento antes de poder entrar.
Para más información, consultar {nc-ref}`Grabación de llamadas <call-recording>`.

##### Iniciar la llamada

Hacer clic en el botón {guilabel}`Comenzar llamada` de la parte inferior de `Media settings` para notificar la llamada a todos los participantes de la conversación.
Para no notificar a los demás participantes, iniciar una llamada silenciosa: abrir el menú de tres puntos a la izquierda del botón {guilabel}`Comenzar llamada`
y elegir `Call without notification`.

:::{note}
Los demás participantes pueden modificar las notificaciones conversación por conversación, incluido si quieren recibir notificaciones de llamadas.
:::

El estado de usuario pasará a `In a call` y el icono de estado mostrará el emoji de bocadillo de diálogo.

#### Clientes móviles

Al formar parte de una conversación y tener permiso para hacerlo, se puede iniciar una llamada en cualquier momento
tocando el icono `Phone` o `Video` de la barra superior.
El icono `Phone` inicia una llamada solo de voz; el icono `Video` inicia una videollamada.

Una llamada de voz usa el micrófono y el auricular del dispositivo, como una llamada telefónica normal.
Una videollamada usa el altavoz en modo manos libres y activa la cámara frontal de forma predeterminada; se puede desactivar en cualquier momento.

Si otra persona inicia una llamada, puede llegar una notificación y el dispositivo puede sonar o vibrar,
según los ajustes de notificaciones.
Tocar `Phone` o `Video` para unirse, o tocar el botón rojo para rechazarla. Rechazarla descarta la notificación de la llamada en ese dispositivo.

El micrófono y la cámara (si es una videollamada) se controlan con las opciones que aparecen en la parte inferior de la pantalla.

El estado de usuario pasará a `In a call` y el icono de estado mostrará un bocadillo de diálogo.

### Durante una llamada

Después de unirse a una llamada se verá la vista de llamada. Muestra las transmisiones de video de todos los participantes que están en la llamada en ese momento, con información y controles adicionales.

El elemento situado más a la izquierda muestra el tiempo transcurrido de la llamada.

A su lado se verá el número de participantes que se han unido a la llamada actual.
Al hacer clic en el número se abre la barra lateral derecha y se muestra la lista de participantes.
Los participantes que se han unido a la llamada aparecen primero.

También se verá el tiempo de palabra de cada participante, si ha hablado durante la llamada.

Se puede acceder a opciones y ajustes adicionales de la llamada desde el menú de tres puntos de la barra superior.

#### Configurar salas de grupos

Las salas de grupos permiten dividir una llamada en grupos más pequeños para conversaciones más centradas.
Según los permisos y la configuración de la instancia, es posible que esta opción no esté disponible.
Para más información, consultar {nc-ref}`Salas de grupos <breakout-rooms>`.

#### Descargar la lista de participantes de la llamada

La lista de participantes de una llamada se puede descargar desde el menú de tres puntos de la barra superior. Así se descarga un archivo CSV con los nombres y las direcciones de correo electrónico de todos los participantes.

El archivo CSV contiene las siguientes columnas:

- **Name**: el nombre del participante.
- **Email**: la dirección de correo electrónico del participante.
- **Type**: indica si el participante es un usuario registrado o un invitado.
- **Identifier**: identificador único del participante.

#### Controlar el audio y el video

La barra inferior de la vista de llamada ofrece controles multimedia, ajustes de diseño y otras funciones que se pueden usar durante una llamada.

Usar los iconos de micrófono y cámara para silenciar o reactivar el micrófono y activar o desactivar la cámara.
También se pueden usar los atajos de teclado `M` para silenciar o reactivar el micrófono y `V` para activar o desactivar la cámara.
Usar la barra espaciadora para pulsar y hablar: mantener pulsada la barra espaciadora reactiva temporalmente el micrófono si está silenciado, o lo silencia temporalmente si está activo.

#### Reacciones

El botón de reacciones permite enviar una reacción con emoji a todos los participantes de la llamada.

Todos los participantes verán el emoji subir desde la parte inferior de su pantalla de llamada. El emoji desaparece después de dos segundos.

##### Levantar la mano

Al hacer clic en {guilabel}`Levantar la mano` se notificará a los moderadores y se mostrará un icono junto al nombre. También está disponible con el atajo de teclado `R`.

##### Pantalla completa

Cambia la ventana del navegador o el cliente Talk Desktop al modo de pantalla completa.
También está disponible con el atajo de teclado `F`. Pulsar `ESC` para volver a la vista normal.
````
