---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Delegar las tareas de IA en proveedores de pago (OpenAI, Replicate, IBM watsonx): apps de integración, compatibilidad y retardo de las tareas."
---
# IA como servicio

## Resumen

Esta página explica, para quienes administran el servidor, la opción de delegar las tareas de IA en un proveedor de «IA como servicio» de pago: las apps de integración que hay que instalar, los límites de compatibilidad de las integraciones con OpenAI e IBM watsonx.ai y el retardo de las tareas. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/ai_as_a_service.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

(nc-ai-ai_as_a_service)=
En {vendor}`Nextcloud` el foco está en crear apps de IA locales que se ejecutan de forma totalmente autoalojada en los servidores propios, para preservar la privacidad y la soberanía de los datos.
Sin embargo, también es posible delegar estas tareas, que consumen muchos recursos, en un proveedor de «IA como servicio» que ofrece acceso a una API a cambio de un pago.
Son ejemplos de estos proveedores [OpenAI](https://platform.openai.com/), con sus API de ChatGPT, que dan acceso a modelos de lenguaje
entre otras API, así como [Replicate](https://replicate.com/) e [IBM watsonx](https://www.ibm.com/watsonx).

### Instalación

Para usar estos proveedores hay que instalar la app correspondiente desde la tienda de apps:

- `integration_openai`

- `integration_replicate`

- `integration_watsonx`

Después pueden añadirse los datos de la cuenta, fijarse límites de tasa y activarse los proveedores en la sección «Inteligencia Artificial» de las configuraciones de administración.

De forma opcional (aunque recomendada), configurar workers en segundo plano para que las tareas se recojan más rápido. Hay más información en {nc-ref}`la sección correspondiente de la visión general de la IA <ai-overview_improve-ai-task-pickup-speed>`.

### Integración con OpenAI

Con esta aplicación también es posible conectarse a una instancia autoalojada de LocalAI u Ollama, o a cualquier servicio que implemente una API lo bastante parecida a la API de OpenAI,
por ejemplo [IONOS AI Model Hub](https://docs.ionos.com/cloud/ai/ai-model-hub),
[Plusserver](https://www.plusserver.com/en/ai-platform/), [Groqcloud](https://console.groq.com), [MistralAI](https://mistral.ai) o [Together AI](https://together.ai).

Hay que tener en cuenta, sin embargo, que {vendor}`Nextcloud` prueba las tareas del asistente que implementa esta app solo con modelos de OpenAI y solo contra la API de OpenAI, por lo que no puede garantizar que otros modelos y API funcionen.
Algunas API que se declaran compatibles con OpenAI podrían no serlo del todo, por lo que no puede garantizarse que funcionen con esta app.

### Integración con IBM watsonx.ai

Con esta aplicación también es posible conectarse a un clúster autoalojado que ejecute el software IBM watsonx.ai.

Hay que tener en cuenta, sin embargo, que {vendor}`Nextcloud` prueba las tareas del asistente que implementa esta app solo con los modelos fundacionales proporcionados y solo contra los servidores de IBM Cloud.
Por tanto, no puede garantizar que otros modelos u otras instancias de servidor funcionen.

### Mejorar el rendimiento

Las instrucciones (prompts) de estas apps pueden tener un retardo de hasta 5 minutos.
Esto puede optimizarse; hay más información en {nc-ref}`la sección correspondiente de la visión general de la IA <ai-overview_improve-ai-task-pickup-speed>`.
````
