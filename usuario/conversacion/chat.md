---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Escribir mensajes en Talk: Markdown, emojis, selector inteligente, respuestas, mensajes silenciosos y programados, y resumen del chat con IA."
---
# Enviar mensajes

## Resumen

Esta página explica a las personas usuarias cómo redactar y enviar mensajes en el chat de Talk: el formato Markdown admitido, los emojis, el selector inteligente, las respuestas, los mensajes silenciosos y programados, y el resumen del chat generado con IA.

````{upstream} user_manual/talk/chat.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Usar Markdown

Los mensajes se pueden enriquecer con sintaxis Markdown. Elementos admitidos:

**Títulos y separadores**

```none
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

Heading
===
Normal text
***
Normal text
```

**Formato en línea**

~~~none
**bold text** __bold text__
*italicized text* _italicized text_
`inline code` ``inline code``
```
.code-block {
  display: pre;
}
```
~~~

**Listas**

```none
1. Ordered list
2. Ordered list

* Unordered list
- Unordered list
+ Unordered list
```

**Citas**

```none
> blockquote
second line of blockquote
```

**Listas de tareas**

```none
- [ ] task to be done
- [x] completed task
```

**Tablas**

```none
Column A | Column B
-- | --
Data A | Data B
```

### Insertar emojis

Se pueden añadir emojis con el selector situado a la izquierda del campo de entrada de texto.

### Selector inteligente

El selector inteligente facilita insertar enlaces, archivos u otro contenido en las conversaciones. Basta con elegir el tipo de contenido que se quiere insertar (archivos, conversaciones de Talk, tarjetas de Deck, GIF, etc.). También se puede escribir {title-reference}`/` en el campo de entrada del chat para abrir el selector.

Varias aplicaciones de integración pueden ampliar el selector inteligente con tipos de contenido adicionales, como incidencias de GitHub y GitLab, GIF de Giphy y más. Preguntar a la administración qué integraciones están disponibles en la instancia.

### Responder a mensajes y más

Se puede responder a un mensaje con la flecha que aparece al pasar el cursor sobre él.

En el menú `...` también se puede elegir responder en privado. Esto abre una conversación uno a uno.

Aquí también se puede crear un enlace directo al mensaje o marcarlo como no leído para volver a ese punto la próxima vez que se entre en el chat. Cuando se trata de un archivo, se puede ver el archivo en Archivos.

### Mensajes silenciosos

Si no se quiere molestar a nadie en mitad de la noche, existe un modo silencioso para chatear. Mientras está activado, los demás participantes no reciben notificaciones de los mensajes que se envían.

### Programar mensajes

Si se quiere enviar un mensaje no en este momento, sino a una hora concreta, se puede programar. Basta con seleccionar la fecha y la hora deseadas en las acciones rápidas junto al campo de entrada.

Todos los mensajes programados se encuentran haciendo clic en el icono del reloj junto al campo de entrada. Ahí se pueden editar, reprogramar o eliminar los mensajes que estén preparados.

### Resumen del chat

Cuando el asistente de IA está activado, se puede generar un resumen de una conversación si hay más de 100 mensajes sin leer. Se genera pulsando el botón visible en el chat encima de los primeros mensajes sin leer.
````
