---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Funciones de IA de la plataforma base: apps que las aportan, clasificación de IA ética, apps que las usan, workers de tareas de IA y preguntas frecuentes."
---
# Visión general

## Resumen

Esta página explica, para quienes administran el servidor, las funciones de inteligencia artificial de la plataforma base: qué apps las aportan y cómo se clasifican según la clasificación de IA ética, qué apps las usan, cómo acelerar la recogida de las tareas de IA con workers y por qué una instrucción puede ser lenta. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/overview.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

{vendor}`Nextcloud` se esfuerza por llevar funciones de inteligencia artificial a Nextcloud. Esta sección destaca estas funciones, cómo funcionan y dónde encontrarlas.
Todas estas funciones son completamente opcionales. Si se quieren tener en el servidor, hay que instalarlas mediante apps de Nextcloud independientes.

### Visión general de las funciones de IA

Nextcloud usa la modularidad para separar la funcionalidad de IA en bruto de las interfaces gráficas de usuario y de las apps que usan esa funcionalidad. Así, cada instancia puede usar varios backends que aportan la funcionalidad a los mismos frontends, y la misma funcionalidad puede implementarse en varias apps que usan procesamiento en las instalaciones propias o proveedores externos de servicios de IA.

| Función | App | Clasificación | Código abierto | Modelo disponible libremente | Datos de entrenamiento disponibles libremente | Privacidad: mantiene los datos en las instalaciones propias |
|---|---|---|---|---|---|---|
| Bandeja de entrada inteligente | [Mail](https://apps.nextcloud.com/apps/mail) | Verde | Sí | Sí | Sí | Sí |
| Reconocimiento de objetos en imágenes | [Recognize](https://apps.nextcloud.com/apps/recognize) | Verde | Sí | Sí | Sí | Sí |
| Reconocimiento facial en imágenes | [Recognize](https://apps.nextcloud.com/apps/recognize) | Verde | Sí | Sí | Sí | Sí |
| Reconocimiento de acciones en vídeo | [Recognize](https://apps.nextcloud.com/apps/recognize) | Verde | Sí | Sí | Sí | Sí |
| Reconocimiento del género musical en audio | [Recognize](https://apps.nextcloud.com/apps/recognize) | Verde | Sí | Sí | Sí | Sí |
| Detección de inicios de sesión sospechosos | [Suspicious Login](https://apps.nextcloud.com/apps/suspicious_login) | Verde | Sí | Sí | Sí | Sí |
| Recursos relacionados | [Related Resources](https://apps.nextcloud.com/apps/related_resources) | Verde | Sí | Sí | Sí | Sí |
| Archivos recomendados | recommended_files | Verde | Sí | Sí | Sí | Sí |
| Procesamiento de texto con LLM | [Local large language model 2 (ExApp) (ExApp)](https://apps.nextcloud.com/apps/llm2) | Verde | Sí | Sí - modelo Llama 3.1 de Meta | Sí | Sí |
| | [OpenAI and LocalAI integration (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) | Rojo | No | No | No | No |
| | [OpenAI and LocalAI integration (mediante LocalAI)](https://apps.nextcloud.com/apps/integration_openai) | Amarillo | Sí | Sí - p. ej., modelos Llama de Meta | No | Sí |
| | [OpenAI and LocalAI integration (mediante Ollama)](https://apps.nextcloud.com/apps/integration_openai) | Amarillo | Sí | Sí - p. ej., modelos Llama de Meta | No | Sí |
| | [OpenAI and LocalAI integration (mediante IONOS AI Model Hub)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| | [OpenAI and LocalAI integration (mediante Plusserver)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| | [OpenAI and LocalAI integration (mediante Groqcloud)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| | [OpenAI and LocalAI integration (mediante MistralAI)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| | [IBM watsonx.ai integration (mediante IBM watsonx.ai como servicio)](https://apps.nextcloud.com/apps/integration_watsonx) | Naranja | No | Sí - p. ej., modelos Granite de IBM | No | No |
| | [IBM watsonx.ai integration (mediante el software IBM watsonx.ai)](https://apps.nextcloud.com/apps/integration_watsonx) | Naranja | No | Sí - p. ej., modelos Granite de IBM | No | Sí |
| Traducción automática | [Local Machine Translation 2 (ExApp)](https://apps.nextcloud.com/apps/translate2) | Verde | Sí | Sí - modelos MADLAD de Google | Sí | Sí |
| | [DeepL integration](https://apps.nextcloud.com/apps/integration_deepl) | Rojo | No | No | No | No |
| | [OpenAI and LocalAI integration (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) | Rojo | No | No | No | No |
| | [OpenAI and LocalAI integration (mediante LocalAI)](https://apps.nextcloud.com/apps/integration_openai) | Verde | Sí | Sí | Sí | Sí |
| | [OpenAI and LocalAI integration (mediante Ollama)](https://apps.nextcloud.com/apps/integration_openai) | Amarillo | Sí | Sí - p. ej., modelos Llama de Meta | No | Sí |
| | [OpenAI and LocalAI integration (mediante IONOS AI Model Hub)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| | [OpenAI and LocalAI integration (mediante Plusserver)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| | [OpenAI and LocalAI integration (mediante Groqcloud)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| | [OpenAI and LocalAI integration (mediante MistralAI)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| Voz a texto | [Local Whisper Speech-To-Text 2 (ExApp)](https://apps.nextcloud.com/apps/stt_whisper2) | Amarillo | Sí | Sí - modelos Whisper de OpenAI | No | Sí |
| | [OpenAI and LocalAI integration](https://apps.nextcloud.com/apps/integration_openai) | Amarillo | Sí | Sí - modelos Whisper de OpenAI | No | No |
| | [OpenAI and LocalAI integration (mediante LocalAI)](https://apps.nextcloud.com/apps/integration_openai) | Verde | Sí | Sí | Sí | Sí |
| | [OpenAI and LocalAI integration (mediante Ollama)](https://apps.nextcloud.com/apps/integration_openai) | Amarillo | Sí | Sí - p. ej., Whisper | No | Sí |
| | [OpenAI and LocalAI integration (mediante IONOS AI Model Hub)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| | [OpenAI and LocalAI integration (mediante Plusserver)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| | [OpenAI and LocalAI integration (mediante Groqcloud)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| | [OpenAI and LocalAI integration (mediante MistralAI)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| | [Replicate integration](https://apps.nextcloud.com/apps/integration_replicate) | Amarillo | Sí | Sí - modelos Whisper de OpenAI | No | No |
| Generación de imágenes | [Local Stable Diffusion 2 (ExApp)](https://apps.nextcloud.com/apps/text2image_stablediffusion2) | Amarillo | Sí | Sí - modelo StableDiffusion XL de StabilityAI | No | Sí |
| | [Replicate integration](https://apps.nextcloud.com/apps/integration_replicate) | Amarillo | Sí | Sí - modelos StableDiffusion de StabilityAI | No | No |
| | [OpenAI and LocalAI integration (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) | Rojo | No | No | No | No |
| | [OpenAI and LocalAI integration (mediante LocalAI)](https://apps.nextcloud.com/apps/integration_openai) | Verde | Sí | Sí | Sí | Sí |
| | [OpenAI and LocalAI integration (mediante Ollama)](https://apps.nextcloud.com/apps/integration_openai) | Amarillo | Sí | Sí - p. ej., modelos Llama de Meta | No | Sí |
| | [OpenAI and LocalAI integration (mediante IONOS AI Model Hub)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| | [OpenAI and LocalAI integration (mediante Plusserver)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| | [OpenAI and LocalAI integration (mediante Groqcloud)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| | [OpenAI and LocalAI integration (mediante MistralAI)](https://apps.nextcloud.com/apps/integration_openai) | Naranja | No | Sí | No | No |
| Context Chat | [Nextcloud Assistant Context Chat](https://apps.nextcloud.com/apps/context_chat) | Amarillo | Sí | Sí | No | Sí |
| | [Nextcloud Assistant Context Chat (Backend)](https://apps.nextcloud.com/apps/context_chat_backend) | Amarillo | Sí | Sí | No | Sí |
| Búsqueda de Context Chat | [Nextcloud Assistant Context Chat](https://apps.nextcloud.com/apps/context_chat) | Amarillo | Sí | Sí | No | Sí |
| Context Agent | [Nextcloud Context Agent (ExApp)](https://apps.nextcloud.com/apps/context_agent) | Verde | Sí | Sí | Sí | Sí |
| Texto a voz | [Open AI Text To Speech](https://apps.nextcloud.com/apps/integration_openai) | Rojo | No | No | No | No |
| | [Local Text To Speech (ExApp)](https://apps.nextcloud.com/apps/text2speech_kokoro) | Amarillo | Sí | Sí | No | Sí |
| Generación de documentos | [Nextcloud Office](https://apps.nextcloud.com/apps/richdocuments) | Verde | Sí | Sí | Sí | Sí |
| Transcripción en directo | [Local Live Transcription](https://apps.nextcloud.com/apps/live_transcription) | Amarillo | Sí | Sí | No | Sí |

### Clasificación de IA ética

Hasta Hub 3, {vendor}`Nextcloud` logró ofrecer funciones sin depender de blobs propietarios ni de servicios de terceros. Sin embargo, aunque existe una gran comunidad que desarrolla tecnologías éticas, seguras y respetuosas con la privacidad, hay muchas otras tecnologías relevantes que los usuarios podrían querer usar. {vendor}`Nextcloud` quiere ofrecer a los usuarios estas tecnologías de vanguardia, pero también ser transparente. Para algunos casos de uso, ChatGPT puede ser una solución razonable, mientras que para datos más privados, profesionales o sensibles es primordial contar con una solución local, en las instalaciones propias y abierta. Para diferenciarlas, {vendor}`Nextcloud` desarrolló una clasificación de IA ética (Ethical AI Rating).

- La clasificación tiene cuatro niveles:
  - Rojo
  - Naranja
  - Amarillo
  - Verde

- Se basa en puntos de estos factores:
  - ¿El software (tanto el de inferencia como el de entrenamiento) tiene una licencia libre y de código abierto?
  - ¿El modelo entrenado está disponible libremente para el autoalojamiento?
  - ¿Los datos de entrenamiento están disponibles y son de uso libre?

Si se cumplen todos estos puntos, se otorga una etiqueta verde. Si no se cumple ninguno, es roja. Si se cumple 1 condición, es naranja, y si se cumplen 2 condiciones, amarilla.

### Funciones usadas por otras apps

Algunas de las funciones de IA de {vendor}`Nextcloud` se realizan como API genéricas que cualquier app puede usar y para las que cualquier app puede aportar una implementación registrando un proveedor. Hasta ahora, son
la traducción automática, la voz a texto, el texto a voz, la generación de imágenes, el procesamiento de texto y Context Chat.

#### Procesamiento de texto

(nc-tp-consumer-apps)=
Como se ve en la tabla anterior, hay varias apps que ofrecen procesamiento de texto con modelos de lenguaje de gran tamaño.
En las apps que lo consumen, como Context Chat y el asistente, los usuarios pueden usar la funcionalidad de procesamiento de texto independientemente de qué app la implemente internamente.

##### Apps de frontend

- [Assistant](https://apps.nextcloud.com/apps/assistant) para ofrecer una interfaz gráfica para las distintas tareas, un selector inteligente y la funcionalidad «Chat with AI»
- [Mail](https://apps.nextcloud.com/apps/mail) para resumir hilos de correo (cómo activarlo se explica en {nc-ref}`la documentación de Nextcloud Mail <mail_thread_summary>`)
- [Summary Bot](https://apps.nextcloud.com/apps/summary_bot) para resumir historiales de chat en [Talk](https://apps.nextcloud.com/apps/spreed)
- [Talk](https://apps.nextcloud.com/apps/spreed) para resumir el historial de chat (cómo activarlo se explica en la [documentación de Nextcloud Talk](https://nextcloud-talk.readthedocs.io/en/latest/settings/#app-configuration))
- [Text](https://apps.nextcloud.com/apps/text) para ofrecer una interfaz gráfica integrada en el texto para las distintas tareas
- [Collectives](https://apps.nextcloud.com/apps/collectives), que integra el asistente mediante el selector inteligente para ofrecer una interfaz gráfica para las distintas tareas
- [Notes](https://apps.nextcloud.com/apps/notes), que integra el asistente mediante el selector inteligente para ofrecer una interfaz gráfica para las distintas tareas
- [Whiteboard](https://apps.nextcloud.com/apps/whiteboard), que integra el asistente mediante el selector inteligente para ofrecer una interfaz gráfica para las distintas tareas
- [Deck](https://apps.nextcloud.com/apps/deck), que integra el asistente mediante el selector inteligente para ofrecer una interfaz gráfica para las distintas tareas
- [Nextcloud Office](https://apps.nextcloud.com/apps/richdocuments), que integra el asistente mediante el selector inteligente para ofrecer una interfaz gráfica para las distintas tareas en los documentos
- [Clientes de escritorio](https://docs.nextcloud.com/server/latest/user_manual/en/desktop/index.html) para un «Chat with AI» sencillo

##### Apps de backend

- {nc-ref}`llm2 <ai-app-llm2>` - Ejecuta modelos LLM de IA de código abierto en el hardware del propio servidor (soporte al cliente disponible previa solicitud)
- [OpenAI and LocalAI integration (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) - Se integra con la API de OpenAI para aportar funcionalidad de IA desde los servidores de OpenAI (soporte al cliente disponible previa solicitud; ver {nc-ref}`IA como servicio <ai-ai_as_a_service>`)
- [IBM watsonx.ai integration (mediante IBM watsonx.ai como servicio)](https://apps.nextcloud.com/apps/integration_watsonx) - Se integra con la API de IBM watsonx.ai para aportar funcionalidad de IA desde los servidores de IBM Cloud (soporte al cliente disponible previa solicitud; ver {nc-ref}`IA como servicio <ai-ai_as_a_service>`)

#### Traducción automática

(nc-mt-consumer-apps)=
Como se ve en la tabla anterior, hay varias apps que ofrecen capacidades de traducción automática. Cada app aporta su propio conjunto de idiomas admitidos.
En las apps que la consumen, como la app Text, los usuarios pueden usar la funcionalidad de traducción independientemente de qué app la implemente internamente.

##### Apps de frontend

- [Assistant](https://apps.nextcloud.com/apps/assistant), que ofrece una interfaz gráfica de traducción
- [Analytics](https://apps.nextcloud.com/apps/analytics) para traducir las etiquetas de los gráficos
- [Talk](https://apps.nextcloud.com/apps/spreed) para traducir mensajes y para traducciones en directo en las llamadas, junto con la {nc-ref}`app Live Transcription <ai-live-transcription>`
- [Deck](https://apps.nextcloud.com/apps/deck) para ofrecer una interfaz de traducción en la descripción de las tarjetas
- *Text* para ofrecer el menú de traducción
- [Notes](https://apps.nextcloud.com/apps/notes) para ofrecer una interfaz de traducción en el contenido de las notas
- [Collectives](https://apps.nextcloud.com/apps/collectives) para ofrecer una interfaz de traducción en el contenido de las páginas
- [Whiteboard](https://apps.nextcloud.com/apps/whiteboard) para ofrecer una interfaz de traducción mediante el asistente
- [Nextcloud Office](https://apps.nextcloud.com/apps/richdocuments) para ofrecer una interfaz de traducción en el contenido de los documentos

##### Apps de backend

- {nc-ref}`translate2 (ExApp) <ai-app-translate2>` - Ejecuta modelos de traducción de IA de código abierto localmente en el hardware del propio servidor (soporte al cliente disponible previa solicitud)
- [OpenAI and LocalAI integration (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) - Se integra con la API de OpenAI para aportar funcionalidad de IA desde los servidores de OpenAI (soporte al cliente disponible previa solicitud; ver {nc-ref}`IA como servicio <ai-ai_as_a_service>`)
- [DeepL integration](http://apps.nextcloud.com/apps/integration_deepl) - Se integra con la API de deepl para aportar funcionalidad de traducción desde los servidores de Deepl.com (solo con soporte de la comunidad)

#### Voz a texto

(nc-stt-consumer-apps)=
Como se ve en la tabla anterior, hay varias apps que ofrecen capacidades de voz a texto. En las apps que la consumen, como la app Talk, los usuarios pueden usar la funcionalidad de transcripción independientemente de qué app la implemente internamente.

##### Apps de frontend

- [Assistant](https://apps.nextcloud.com/apps/assistant), que ofrece una interfaz gráfica de traducción, un selector inteligente y chat de audio
- [Talk](https://apps.nextcloud.com/apps/spreed) para transcribir llamadas (cómo activarlo se explica en la [documentación de Nextcloud Talk](https://nextcloud-talk.readthedocs.io/en/latest/settings/#app-configuration))

##### Apps de backend

- {nc-ref}`stt_whisper2 <ai-app-stt_whisper2>` - Ejecuta modelos de IA de voz a texto de pesos abiertos en el hardware del propio servidor (soporte al cliente disponible previa solicitud)
- [OpenAI and LocalAI integration (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) - Se integra con la API de OpenAI para aportar funcionalidad de IA desde los servidores de OpenAI (soporte al cliente disponible previa solicitud; ver {nc-ref}`IA como servicio <ai-ai_as_a_service>`)

#### Generación de imágenes

(nc-t2i-consumer-apps)=
Como se ve en la tabla anterior, hay varias apps que ofrecen capacidades de generación de imágenes. En las apps que la consumen, como la app auxiliar Text-to-Image, los usuarios pueden usar la funcionalidad de generación de imágenes independientemente de qué app la implemente internamente.

##### Apps de frontend

- [Assistant](https://apps.nextcloud.com/apps/assistant) para ofrecer una interfaz gráfica y un selector inteligente
- [Deck](https://apps.nextcloud.com/apps/deck) para insertar imágenes con el selector inteligente
- *Text* para insertar imágenes con el asistente y el selector inteligente
- [Notes](https://apps.nextcloud.com/apps/notes) para insertar imágenes con el asistente y el selector inteligente
- [Collectives](https://apps.nextcloud.com/apps/collectives) para insertar imágenes con el asistente y el selector inteligente
- [Whiteboard](https://apps.nextcloud.com/apps/whiteboard) para insertar imágenes con el asistente y el selector inteligente, y para generar diagramas y diagramas de flujo con Mermaid
- [Nextcloud Office](https://apps.nextcloud.com/apps/richdocuments) para insertar imágenes con el asistente y el selector inteligente

##### Apps de backend

- [Local Stable Diffusion 2 (ExApp)](https://apps.nextcloud.com/apps/text2image_stablediffusion2) (soporte al cliente disponible previa solicitud)
- [OpenAI and LocalAI integration (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) - Se integra con la API de OpenAI para aportar funcionalidad de IA desde los servidores de OpenAI (soporte al cliente disponible previa solicitud; ver {nc-ref}`IA como servicio <ai-ai_as_a_service>`)
- *integration_replicate* - Se integra con la API de replicate para aportar funcionalidad de IA desde los servidores de replicate (ver {nc-ref}`IA como servicio <ai-ai_as_a_service>`)

#### Texto a voz

(nc-t2s-consumer-apps)=
Como se ve en la tabla anterior, hay varias apps que ofrecen capacidades de generación de voz. En las apps que la consumen, como la app del asistente, los usuarios pueden usar la funcionalidad de generación de voz independientemente de qué app la implemente internamente.

##### Apps de frontend

- [Assistant](https://apps.nextcloud.com/apps/assistant) para ofrecer un chat de audio

##### Apps de backend

- [OpenAI and LocalAI integration (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) - Se integra con la API de OpenAI para aportar funcionalidad de IA desde los servidores de OpenAI (soporte al cliente disponible previa solicitud; ver {nc-ref}`IA como servicio <ai-ai_as_a_service>`)
- [Local Text To Speech (ExApp)](https://apps.nextcloud.com/apps/text2speech_kokoro) (soporte al cliente disponible previa solicitud)

#### Context Chat

La función Context Chat de {vendor}`Nextcloud` se introdujo en Nextcloud Hub 7 (v28). Permite hacer preguntas al asistente sobre los propios documentos en Nextcloud. Hay que instalar tanto la app context_chat como la app externa context_chat_backend. Conviene estar preparado para que algunas cosas fallen o estén algo por pulir. ¡{vendor}`Nextcloud` espera con interés los comentarios!

##### Apps de frontend

- [Assistant](https://apps.nextcloud.com/apps/assistant) para ofrecer una interfaz gráfica para las tareas de Context Chat
- [Nextcloud Context Agent](https://apps.nextcloud.com/apps/context_agent) para ofrecer Context Chat como herramienta que el agente puede ejecutar en la función «Chat with AI»

##### Apps de backend

- {nc-ref}`context_chat + context_chat_backend <ai-app-context_chat>` -  (soporte al cliente disponible previa solicitud)

##### Apps proveedoras

Las apps pueden integrar su contenido con Context Chat para que pueda consultarse con Context Chat. Hasta ahora, las siguientes apps han implementado esta integración:

- *files*
- [Analytics](https://apps.nextcloud.com/apps/analytics)
- [Mail](https://apps.nextcloud.com/apps/mail) (próximamente)
- [Bookmarks](https://apps.nextcloud.com/apps/bookmarks)

#### Búsqueda de Context Chat

La función de búsqueda de Context Chat de {vendor}`Nextcloud` permite buscar en los propios documentos con lenguaje natural. Hay que instalar tanto la app context_chat como la app externa context_chat_backend. ¡{vendor}`Nextcloud` espera con interés los comentarios!

##### Apps de frontend

- [Assistant](https://apps.nextcloud.com/apps/assistant) para ofrecer una interfaz gráfica para las tareas de búsqueda de Context Chat

##### Apps de backend

- {nc-ref}`context_chat + context_chat_backend <ai-app-context_chat>` -  (soporte al cliente disponible previa solicitud)

##### Apps proveedoras

Ver la sección *Context Chat* anterior.

#### Context Agent

La función Context Agent de {vendor}`Nextcloud` se introdujo en Nextcloud Hub 9 (v30). Permite pedir al asistente que ejecute tareas relacionadas con Nextcloud. Hay que instalar tanto la app context_agent como un proveedor de procesamiento de texto.

##### Apps de frontend

- [Assistant](https://apps.nextcloud.com/apps/assistant) para ofrecer una interfaz gráfica para la función «Chat with AI»

##### Apps de backend

- [Nextcloud Context Agent](https://apps.nextcloud.com/apps/context_agent) para capacidades de IA agéntica en la función «Chat with AI» (soporte al cliente disponible previa solicitud)

##### Apps proveedoras

- {nc-ref}`llm2 <ai-app-llm2>` - Ejecuta modelos LLM de IA de código abierto en el hardware del propio servidor (soporte al cliente disponible previa solicitud)
- [OpenAI and LocalAI integration (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) - Se integra con la API de OpenAI para aportar funcionalidad de IA desde los servidores de OpenAI (soporte al cliente disponible previa solicitud; ver {nc-ref}`IA como servicio <ai-ai_as_a_service>`)

#### Generación de documentos

Desde Hub 11 puede hacerse que Nextcloud genere automáticamente documentos de Office con contenido.
Esta funcionalidad está disponible en la app del asistente y es posible gracias a la app Nextcloud Office.

##### Apps de frontend

- [Assistant](https://apps.nextcloud.com/apps/assistant) para ofrecer una interfaz gráfica para las tareas de búsqueda de Context Chat

##### Apps de backend

- [Nextcloud Office](https://apps.nextcloud.com/apps/richdocuments)

##### Apps proveedoras

- {nc-ref}`llm2 <ai-app-llm2>` - Ejecuta modelos LLM de IA de código abierto en el hardware del propio servidor (soporte al cliente disponible previa solicitud)
- [OpenAI and LocalAI integration (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai) - Se integra con la API de OpenAI para aportar funcionalidad de IA desde los servidores de OpenAI (soporte al cliente disponible previa solicitud; ver {nc-ref}`IA como servicio <ai-ai_as_a_service>`)
- [IBM watsonx.ai integration (mediante IBM watsonx.ai como servicio)](https://apps.nextcloud.com/apps/integration_watsonx) - Se integra con la API de IBM watsonx.ai para aportar funcionalidad de IA desde los servidores de IBM Cloud (soporte al cliente disponible previa solicitud; ver {nc-ref}`IA como servicio <ai-ai_as_a_service>`)

#### Transcripción en directo

Desde Hub 25 Autumn puede hacerse que Nextcloud genere automáticamente subtítulos para las videollamadas y las llamadas de audio en Nextcloud Talk.

##### Apps de frontend

- [Talk](https://apps.nextcloud.com/apps/spreed) para mostrar los subtítulos en las llamadas

##### Apps de backend

- {nc-ref}`live_transcription <ai-live-transcription>` - Ejecuta modelos de IA de voz a texto de pesos abiertos en el hardware del propio servidor (soporte al cliente disponible previa solicitud)

(nc-ai-overview_improve-ai-task-pickup-speed)=
#### Flujos de trabajo de Windmill

Los endpoints de IA pueden usarse en los {nc-ref}`flujos de trabajo de Windmill <windmill_workflows>`. En el [Windmill Hub](https://hub.windmill.dev/integrations/nextcloud/flows) hay algunos flujos de trabajo de ejemplo que muestran las posibilidades de combinar los flujos de trabajo de Windmill con la IA de Nextcloud.

### Acelerar la recogida de las tareas de IA

La mayoría de las tareas de IA se ejecutan como parte del sistema de trabajos en segundo plano de Nextcloud, que de forma predeterminada solo ejecuta trabajos cada 5 minutos.
Para recoger antes los trabajos programados, pueden configurarse workers de trabajos en segundo plano dentro del servidor o contenedor principal de Nextcloud que procesen las tareas de IA en cuanto se programan.
Si el código PHP o los valores de configuración de Nextcloud cambian mientras un worker está en ejecución, esos cambios no surtirán efecto dentro del ejecutor. Por eso, el worker debe reiniciarse periódicamente. Esto se hace con un tiempo de espera de N segundos, lo que significa que cualquier cambio en la configuración o en el código se aplicará al cabo de N segundos (en el peor de los casos). Este tiempo de espera no afecta en modo alguno al procesamiento ni al tiempo de espera de las tareas de IA.

:::{versionchanged} 32.0.7
El comando para ejecutar el worker cambió de `background-job:worker` a `taskprocessing:worker`. Si se usa una versión anterior de Nextcloud, usar el comando antiguo.
:::

#### Sesión de screen o tmux

Ejecutar el siguiente comando occ dentro de una sesión de screen o tmux, preferiblemente 4 o más veces, para procesar en paralelo varias solicitudes de usuarios distintos o del mismo usuario (y como requisito de algunas apps, como context_chat).
Lo mejor es ejecutar un comando por sesión de screen o por ventana o panel de tmux, para mantener los registros visibles y el worker fácil de reiniciar.

```
set -e; while true; do sudo -E -u www-data php occ taskprocessing:worker -v -t 60; done
```

Para Nextcloud-AIO, usar este comando en el servidor anfitrión.

```
set -e; while true; do docker exec -it nextcloud-aio-nextcloud sudo -E -u www-data php occ taskprocessing:worker -v -t 60; done
```

Puede ajustarse el número de workers y el tiempo de espera (en segundos) según las necesidades.
Los registros del worker pueden consultarse conectándose a la sesión de screen o tmux.

#### Servicio de systemd

1. Crear un archivo de servicio de systemd en `/etc/systemd/system/nextcloud-ai-worker@.service` con el siguiente contenido:

```
[Unit]
Description=Nextcloud AI worker %i
After=network.target

[Service]
ExecStart=/opt/nextcloud-ai-worker/taskprocessing.sh %i
Restart=always
StartLimitInterval=60
StartLimitBurst=10

[Install]
WantedBy=multi-user.target
```

2. Crear un script de shell en `/opt/nextcloud-ai-worker/taskprocessing.sh` con el siguiente contenido y asegurarse de hacerlo ejecutable:

```
#!/bin/sh
echo "Starting Nextcloud AI Worker $1"
cd /path/to/nextcloud
sudo -E -u www-data php occ taskprocessing:worker -v -t 60
```

Puede ajustarse el tiempo de espera según las necesidades (en segundos).

3. Activar e iniciar el servicio 4 o más veces:

```
for i in {1..4}; do systemctl enable --now nextcloud-ai-worker@$i.service; done
```

El estado de los workers puede comprobarse con (sustituir 1 por el número del worker):

```
systemctl status nextcloud-ai-worker@1.service
```

La lista de workers puede comprobarse con:

```
systemctl list-units --type=service | grep nextcloud-ai-worker
```

Los registros completos de los workers pueden consultarse con (sustituir 1 por el número del worker):

```
journalctl -xeu nextcloud-ai-worker@1.service -f
```

### Preguntas frecuentes

#### ¿Por qué es lenta mi instrucción?

Los motivos de un rendimiento lento desde la perspectiva del usuario pueden ser

- Usar procesamiento por CPU en lugar de GPU (a veces este límite lo impone la app usada)
- Alta demanda de la función por parte de los usuarios: las instrucciones de los usuarios y las tareas de IA suelen procesarse en el orden en que se reciben, lo que puede causar retrasos cuando muchos usuarios acceden a estas funciones al mismo tiempo.
````
