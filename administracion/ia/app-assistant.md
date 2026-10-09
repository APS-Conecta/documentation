---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "El asistente de IA en el servidor: instalación, apps de backend por función, opciones de configuración y comandos occ de procesamiento de tareas."
---
# Asistente de Nextcloud

## Resumen

Esta página reúne, para quienes administran el servidor, lo necesario para el asistente de IA: su instalación, las apps de backend que aporta cada función, sus opciones de configuración y los comandos `occ` de procesamiento de tareas. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/app_assistant.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

(nc-ai-app-assistant)=
El asistente de Nextcloud es la interfaz gráfica de usuario principal para interactuar con las funciones de inteligencia artificial de Nextcloud.

Ofrece la interfaz gráfica de usuario de la API unificada de procesamiento de tareas de IA, con funciones como resumir textos, generar titulares, hacer preguntas arbitrarias, transcribir archivos multimedia y generar imágenes, y se integra con la app context_chat para dar respuestas en contexto sobre los datos propios almacenados en Nextcloud. La app del asistente ofrece además una interfaz de chat para interactuar con el modelo de lenguaje elegido. {vendor}`Nextcloud` puede ofrecer soporte al cliente previa solicitud; las posibilidades pueden consultarse con el gestor de cuenta.

La documentación de usuario se encuentra aquí: [documentación de usuario del asistente de IA](https://docs.nextcloud.com/server/latest/user_manual/ai_assistant.html)

### Instalación

La app *assistant* puede instalarse desde la página «Apps» de Nextcloud o ejecutando

```
sudo -E -u www-data php occ app:enable assistant
```

### Tienda de apps

La app también está en la tienda de apps de {vendor}`Nextcloud`, donde puede escribirse una reseña: <https://apps.nextcloud.com/apps/assistant>

### Repositorio

El repositorio de código de la app está en GitHub, donde pueden informarse errores y aportarse correcciones y funciones: <https://github.com/nextcloud/assistant>

Los clientes de {vendor}`Nextcloud` deben informar de los errores directamente al soporte al cliente de {vendor}`Nextcloud`.

### Apps relacionadas

La inteligencia artificial en Nextcloud está construida de forma modular, lo que permite elegir entre distintas soluciones según las necesidades. Para usar las distintas funciones del asistente se necesitan apps adicionales que actúan como backends y aportan la implementación real de la funcionalidad de IA. En las configuraciones de administración de Nextcloud, en «Inteligencia Artificial», puede elegirse qué app de backend de IA usar para cada tarea. Tener en cuenta que algunas de las apps de backend solo las mantiene la comunidad, mientras que otras cuentan con soporte al cliente previa solicitud.

Las configuraciones de administración de IA muestran todos los tipos de tareas del asistente que implementan todas las apps instaladas. Los tipos de tarea pueden desactivarse en las configuraciones de administración de IA, de modo que no estén disponibles para el asistente ni para otras apps aunque estén implementados. Todos los tipos de tarea implementados están activados de forma predeterminada.

**Nota**: En {vendor}`Nextcloud` el foco está en crear apps de IA locales que se ejecutan de forma totalmente autoalojada en los servidores propios, para preservar la privacidad y la soberanía de los datos. Sin embargo, también es posible delegar estas tareas, que consumen muchos recursos, en un {nc-ref}`proveedor de «IA como servicio» <ai-ai_as_a_service>`.

**Nota**: Al usar las apps de IA locales de {vendor}`Nextcloud`, asegurarse de tener una GPU con VRAM suficiente para todas las funciones que se necesiten. Cada app documentada aquí indica sus requisitos de hardware.

(nc-machine_translation)=
#### Traducción automática

Para usar las funciones de traducción automática en el asistente se necesita una app que aporte un backend de traducción:

- {nc-ref}`translate2 (ExApp) <ai-app-translate2>` - Ejecuta modelos de IA de traducción de código abierto localmente en el hardware del propio servidor (soporte al cliente disponible previa solicitud)
- *integration_deepl* - Se integra con la API de DeepL para ofrecer funciones de traducción desde los servidores de Deepl.com (solo con soporte de la comunidad)

#### Voz a texto

Para usar la conversión de voz a texto se necesita una app que aporte un backend de voz a texto:

- {nc-ref}`stt_whisper2 <ai-app-stt_whisper2>` - Ejecuta modelos de IA de voz a texto de código abierto en el hardware del propio servidor (soporte al cliente disponible previa solicitud)
- [Integración con OpenAI y LocalAI (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) - Se integra con la API de OpenAI para ofrecer funcionalidad de IA desde los servidores de OpenAI (soporte al cliente disponible previa solicitud; consultar {nc-ref}`IA como servicio <ai-ai_as_a_service>`)

#### Procesamiento de texto

Para usar las funciones de procesamiento de texto en el asistente se necesita una app que aporte un backend de procesamiento de texto:

- {nc-ref}`llm2 <ai-app-llm2>` - Ejecuta modelos de lenguaje de IA de código abierto localmente en el hardware del propio servidor (soporte al cliente disponible previa solicitud)
- [Integración con OpenAI y LocalAI (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) - Se integra con la API de OpenAI para ofrecer funcionalidad de IA desde los servidores de OpenAI (soporte al cliente disponible previa solicitud; consultar {nc-ref}`IA como servicio <ai-ai_as_a_service>`)
- *integration_watsonx* - Se integra con la API de IBM watsonx.ai para ofrecer funcionalidad de IA desde los servidores de IBM Cloud (soporte al cliente disponible previa solicitud; consultar {nc-ref}`IA como servicio <ai-ai_as_a_service>`)

Estas apps implementan actualmente las siguientes tareas del asistente:

- *Generar texto* (probado con OpenAI GPT-3.5 y Llama 3.1 8B)
- *Resumir* (probado con OpenAI GPT-3.5 y Llama 3.1 8B)
- *Generar titular* (probado con OpenAI GPT-3.5 y Llama 3.1 8B)
- *Extraer temas* (probado con OpenAI GPT-3.5 y Llama 3.1 8B)
- *Escritura en contexto* (probado con OpenAI GPT-3.5 y Llama 3.1 8B)
- *Reformular texto* (probado con OpenAI GPT-3.5 y Llama 3.1 8B)

Estas tareas pueden funcionar con otros modelos, pero no se ofrece ninguna garantía.

#### Texto a imagen

Para usar las funciones de texto a imagen se necesita una app que aporte un backend de generación de imágenes:

- {nc-ref}`tex2image_stablediffusion2 <ai-app-text2image_stablediffusion2>` (soporte al cliente disponible previa solicitud)
- [Integración con OpenAI y LocalAI (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) - Se integra con la API de OpenAI para ofrecer funcionalidad de IA desde los servidores de OpenAI (soporte al cliente disponible previa solicitud; consultar {nc-ref}`IA como servicio <ai-ai_as_a_service>`)
- *integration_replicate* - Se integra con la API de Replicate para ofrecer funcionalidad de IA desde los servidores de Replicate (consultar {nc-ref}`IA como servicio <ai-ai_as_a_service>`)

#### Context Chat

Para usar la función especial Context Chat, que ofrece información sobre los documentos y datos propios almacenados en Nextcloud, se necesitan las siguientes apps:

- {nc-ref}`context_chat + context_chat_backend <ai-app-context_chat>` - (soporte al cliente disponible previa solicitud)

También se necesita un proveedor de procesamiento de texto de los indicados arriba (es decir, llm2, integration_openai o integration_watsonx).

#### Chat

Para usar la función «Chat con IA» se necesita cualquiera de las siguientes apps:

- {nc-ref}`llm2 <ai-app-llm2>` - Ejecuta modelos de lenguaje de IA de código abierto localmente en el hardware del propio servidor (soporte al cliente disponible previa solicitud)
- [Integración con OpenAI y LocalAI (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) - Se integra con la API de OpenAI para ofrecer funcionalidad de IA desde los servidores de OpenAI (soporte al cliente disponible previa solicitud; consultar {nc-ref}`IA como servicio <ai-ai_as_a_service>`)

#### Chat de voz

Para usar la función «Chat de audio», que permite interactuar con el chat del asistente mediante la voz y el oído como en una conversación real, se necesita cualquiera de los siguientes conjuntos de apps:

- Bien
    - [Integración con OpenAI y LocalAI (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) - Se integra con la API de OpenAI para ofrecer funcionalidad de IA desde los servidores de OpenAI (soporte al cliente disponible previa solicitud; consultar {nc-ref}`IA como servicio <ai-ai_as_a_service>`)

- O bien
    - {nc-ref}`llm2 <ai-app-llm2>` - Ejecuta modelos de lenguaje de IA de código abierto localmente en el hardware del propio servidor (soporte al cliente disponible previa solicitud)
    - {nc-ref}`stt_whisper2 <ai-app-stt_whisper2>` - Ejecuta modelos de IA de voz a texto de código abierto en el hardware del propio servidor (soporte al cliente disponible previa solicitud)
    - {nc-ref}`text2speech_kokoro <ai-app-text2speech_kokoro>` - Ejecuta modelos de IA de texto a voz de código abierto en el hardware del propio servidor (soporte al cliente disponible previa solicitud)

#### Context Agent

Para usar la función de agente de IA, que ejecuta acciones en nombre del usuario a partir del chat con IA, se necesitan las siguientes apps:

- {nc-ref}`context_agent <ai-app-context_agent>` - (soporte al cliente disponible previa solicitud)

También se necesita un proveedor de procesamiento de texto de los indicados arriba (es decir, *llm2* o *integration_openai*).

#### Texto a voz

Para usar la conversión de texto a voz se necesita una app que aporte un backend de texto a voz, que puede ser una de las siguientes:

- [Integración con OpenAI y LocalAI (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) - Se integra con la API de OpenAI para ofrecer funcionalidad de IA desde los servidores de OpenAI (soporte al cliente disponible previa solicitud; consultar {nc-ref}`IA como servicio <ai-ai_as_a_service>`)
- {nc-ref}`text2speech_kokoro <ai-app-text2speech_kokoro>` - Ejecuta modelos de IA de texto a voz de código abierto en el hardware del propio servidor (soporte al cliente disponible previa solicitud)

### Configuración

Las configuraciones de administración del asistente se encuentran en la sección «Inteligencia Artificial».
Allí puede desactivarse la entrada del asistente en el menú superior. También pueden desactivarse los selectores inteligentes relacionados con la IA.
Los comandos occ para cambiar estas opciones se indican a continuación.

#### Configuración del asistente

1. Asistente arriba a la derecha

   ```
   occ config:app:set assistant assistant_enabled --value=1 --type=string
   ```

   Para activar o desactivar el botón del asistente en la barra de navegación para todos los usuarios.

2. Selector inteligente de generación de texto con IA

   ```
   occ config:app:set assistant free_prompt_picker_enabled --value=1 --type=string
   ```

   Para activar o desactivar el selector inteligente de generación de texto con IA para todos los usuarios.

3. Selector inteligente de texto a imagen

   ```
   occ config:app:set assistant text_to_image_picker_enabled --value=1 --type=string
   ```

   Para activar o desactivar el selector inteligente de texto a imagen para todos los usuarios.

4. Selector inteligente de voz a texto

   ```
   occ config:app:set assistant speech_to_text_picker_enabled --value=1 --type=string
   ```

   Para activar o desactivar el selector inteligente de voz a texto para todos los usuarios.

#### Procesamiento de tareas

1. Listar tareas

   ```
   occ taskprocessing:task:list
   ```

   lista todas las tareas de procesamiento de tareas.

2. Obtener una tarea

   ```
   occ taskprocessing:task:get $TASK_ID
   ```

   muestra toda la información de una tarea concreta.

3. Activar o desactivar un tipo de tarea

   ```
   occ taskprocessing:task-type:set-enabled $TASK_TYPE_ID 1
   ```

   Poner 1 para activar y 0 para desactivar un tipo de tarea implementado.

4. Obtener estadísticas de tareas

   ```
   occ taskprocessing:task:stats
   ```

   muestra estadísticas de todas las tareas de procesamiento de tareas.

5. Limpiar tareas antiguas

   ```
   occ taskprocessing:task:cleanup
   ```

   elimina las tareas con una antigüedad superior a este número de segundos; el valor predeterminado es de 4 meses.

#### Almacenamiento de imágenes

Días que pasan hasta que se eliminan las imágenes generadas si no se han visto.

```
occ config:app:set assistant max_image_generation_idle_time --value=90 --type=integer
```

#### Chat con IA

1. Instrucciones de usuario del chat para las respuestas del chat

   ```
   occ config:app:set assistant chat_user_instructions --value="hello world"
   ```

   Las instrucciones de usuario que se anteponen a los mensajes del chat para que el modelo de IA entienda el contexto del bloque de texto. Es un buen lugar no solo para indicar al modelo de IA que sea educado y amable, sino también, por ejemplo, para que responda todas las consultas en un idioma concreto o, mejor aún, que siga el idioma del usuario. El cielo es el límite.

   **Nota**: Las instrucciones predeterminadas están optimizadas para funcionar bien con una variedad de modelos de lenguaje, pero pueden no ser óptimas para el modelo concreto que se elija. En particular, el modelo puede tender a mencionar el nombre del usuario con demasiada frecuencia y a mencionar el idioma del usuario de una forma inusual.

2. Instrucciones de usuario del chat para la generación de títulos

   ```
   occ config:app:set assistant chat_user_instructions_title --value="hello title"
   ```

   Este campo se añade a continuación del bloque de mensajes del chat, es decir, se adjunta después de los mensajes. Se hace así para que pueda usarse incluso con modelos de completado de texto, que podrían tener las instrucciones como «The title for the above conversation could be "».

3. Últimos N mensajes que se consideran para las respuestas del chat

   ```
   occ config:app:set assistant chat_last_n_messages --value=10
   ```

   El número de mensajes más recientes que se consideran para generar el siguiente mensaje. No incluye las instrucciones de usuario, que siempre se consideran además de estos. Este valor debe ajustarse si se alcanza con demasiada frecuencia el límite de tokens en las conversaciones.
   Lo ideal es que el proveedor de generación de texto con IA gestione el caso del límite máximo de tokens.

#### Mejorar la velocidad de recogida de las tareas de IA

Hay más información en {nc-ref}`la sección correspondiente de la visión general de la IA <ai-overview_improve-ai-task-pickup-speed>`.
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
