---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Asistente de IA de la plataforma base: ajustes personales, ejecutar tareas, notificaciones, historial, chat con IA y selectores inteligentes."
---
(nc-ai-assistant)=
# Asistente de IA

## Resumen

Esta página describe el asistente de IA de la plataforma base: sus ajustes personales, cómo ejecutar tareas y recibir sus resultados, el historial de tareas, el chat con IA y los selectores inteligentes. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} user_manual/ai_assistant.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: usuario/asistente-ia
El asistente de IA de Nextcloud da acceso a herramientas basadas en IA directamente desde la interfaz web. Se pueden ejecutar tareas como el resumen de textos, la generación de imágenes y la transcripción de voz, mantener conversaciones de ida y vuelta con un modelo de lenguaje conectado e insertar contenido generado por IA en documentos y mensajes mediante los selectores inteligentes.

:::{note}
El asistente de IA requiere que el administrador haya instalado y configurado al menos una aplicación de backend de IA. Consultar la [documentación de administración del asistente de IA](https://docs.nextcloud.com/server/latest/admin_manual/ai/app_assistant.html) para más detalles.
:::

### Ajustes personales

Los ajustes personales del asistente están en **Ajustes personales**, en la sección **Inteligencia Artificial**. Allí se puede desactivar la entrada del asistente en el menú superior y habilitar o deshabilitar los selectores inteligentes relacionados con la IA.

### Ejecutar una tarea

Para abrir el asistente, hacer clic en el icono del asistente en la barra de navegación superior derecha.

Elegir un tipo de tarea en la parte superior del panel del asistente, completar el formulario de entrada y hacer clic en el botón de envío en la parte inferior derecha.

La tarea se ejecutará de inmediato si es posible, o se programará para ejecutarse más tarde.

### Notificaciones

Si una tarea quedó programada, se puede pedir recibir una notificación cuando termine. Hacer clic en el botón **Ver resultados** de la notificación para mostrar el resultado de la tarea.

### Historial de tareas

El panel izquierdo del asistente muestra una lista del historial de tareas filtrada por el tipo de tarea seleccionado en ese momento. Desde esta lista se pueden relanzar, eliminar o cancelar tareas anteriores.

### Chat con IA

La pestaña **Chat con IA** del asistente permite mantener una conversación de ida y vuelta con la IA conectada. Escribir un mensaje en el campo de texto de la parte inferior y pulsar {kbd}`Enter` para enviarlo. Hacer clic en **Nueva conversación** para iniciar un hilo de conversación aparte.

Cada conversación tiene su propio contexto. Activar **Recordar esto** en una conversación la agrega a la memoria a largo plazo de la IA, de modo que su contexto esté disponible en cualquier conversación futura. Desactivarlo de nuevo quita la conversación de la memoria.

En la sección **Asistente de IA** de los ajustes personales se pueden revisar todas las conversaciones recordadas.

### Selectores inteligentes

La aplicación del asistente ofrece tres selectores inteligentes, accesibles en Talk, en el editor Text y en cualquier otro lugar donde haya edición de texto enriquecido. Escribir `/` seguido de `ai` para ver la lista filtrada de proveedores.

Cualquier resultado generado mediante el selector inteligente se puede insertar directamente en el contexto actual.
````

## En APS Conecta Gestión

APS Conecta Gestión no incluye el Asistente ni otras funciones de inteligencia artificial. La suite instala un conjunto fijo de aplicaciones y deja desactivada la tienda de aplicaciones: el Asistente no aparece en el menú y no se puede agregar desde la interfaz.
