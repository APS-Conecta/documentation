---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Índice de la IA de la plataforma base: visión general, asistente, apps de IA locales, IA como servicio, diagnóstico y cumplimiento de la Ley de IA de la UE."
---
# Inteligencia artificial

## Resumen

Esta sección reúne, para quienes administran el servidor, las páginas sobre las funciones de inteligencia artificial de la plataforma base: la visión general, el asistente, las apps que ejecutan modelos de IA en el propio servidor, la IA como servicio, el diagnóstico y el cumplimiento de la Ley de IA de la UE. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

- {nc-doc}`admin_manual/ai/overview`
- {nc-doc}`admin_manual/ai/app_assistant`
- {nc-doc}`admin_manual/ai/app_translate2`
- {nc-doc}`admin_manual/ai/app_llm2`
- {nc-doc}`admin_manual/ai/app_stt_whisper2`
- {nc-doc}`admin_manual/ai/app_text2image_stablediffusion2`
- {nc-doc}`admin_manual/ai/app_recognize`
- {nc-doc}`admin_manual/ai/app_context_chat`
- {nc-doc}`admin_manual/ai/app_context_agent`
- {nc-doc}`admin_manual/ai/app_summary_bot`
- {nc-doc}`admin_manual/ai/app_text2speech_kokoro`
- {nc-doc}`admin_manual/ai/app_live_transcription`
- {nc-doc}`admin_manual/ai/ai_as_a_service`
- {nc-doc}`admin_manual/ai/insight_and_debugging`
- {nc-doc}`admin_manual/ai/eu_ai_act`
````

## En APS Conecta Gestión

APS Conecta Gestión no incluye el Asistente ni otras funciones de inteligencia artificial. La suite instala un conjunto fijo de aplicaciones y deja desactivada la tienda de aplicaciones, de modo que las aplicaciones de IA no se agregan desde la interfaz de administración. Las que corren como aplicaciones externas (ExApps) necesitarían además un daemon de despliegue de AppAPI, y la provisión no registra ninguno ([gestion#75](https://github.com/APS-Conecta/gestion/issues/75)). Lo que ve cada persona usuaria está en {doc}`/usuario/asistente-ia`.

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
