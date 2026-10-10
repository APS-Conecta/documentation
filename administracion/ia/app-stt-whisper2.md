---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "stt_whisper2, voz a texto local con Whisper: modelos recomendados, requisitos, instalación, modelos alternativos, escalado y limitaciones."
---
# App: Voz a texto local con Whisper (stt_whisper2)

## Resumen

Esta página describe, para quienes administran el servidor, la app stt_whisper2, que transcribe voz a texto con modelos Whisper de código abierto ejecutados en el propio servidor: los modelos recomendados, sus requisitos, su instalación, el uso de modelos alternativos, el escalado y sus limitaciones conocidas. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/app_stt_whisper2.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

(nc-ai-app-stt_whisper2)=
La app *stt_whisper2* es una de las apps que aportan funcionalidad de voz a texto en Nextcloud y actúan como backend de transcripción multimedia para la {nc-ref}`app Asistente de Nextcloud <ai-app-assistant>`, la app *talk* y {nc-ref}`otras apps que usan la API central de voz a texto <stt-consumer-apps>`. La app *stt_whisper2* en concreto solo ejecuta modelos de código abierto, y lo hace íntegramente en las instalaciones propias. {vendor}`Nextcloud` puede ofrecer soporte al cliente previa solicitud; las posibilidades pueden consultarse con el gestor de cuenta.

Esta app admite entradas y salidas en idiomas distintos del inglés si el modelo subyacente admite el idioma.

Esta app usa internamente [faster-whisper](https://github.com/SYSTRAN/faster-whisper). La calidad de los resultados variará según el modelo que se use; se recomiendan los siguientes modelos:

- OpenAI Whisper large v3 turbo (multilingüe)
- OpenAI Whisper medium.en (solo inglés)

Whisper large v3 admite unos ~100 idiomas y muestra un rendimiento sobresaliente en ~10 de ellos. Hay más detalles en el [artículo de OpenAI Whisper](https://cdn.openai.com/papers/whisper.pdf)

### Requisitos

- Versión mínima de Nextcloud: 28
- Esta app está construida como app externa (External App) y, por tanto, depende de AppAPI v2.3.0
- Nextcloud AIO es compatible
- Actualmente se admiten GPU NVIDIA y CPU x86_64
- CUDA >= v12.2 en el sistema anfitrión
- Dimensionamiento con GPU

   - Una GPU NVIDIA con al menos 4GB de VRAM

- Dimensionamiento con CPU

   - Cuantos más núcleos y más potente sea la CPU, mejor; se recomiendan entre 10 y 20 núcleos
   - De forma predeterminada, la app acapara todos los núcleos, por lo que suele ser mejor ejecutarla en una máquina aparte
   - 4GB para la app

### Instalación

0. Asegurarse de que esté instalada la {nc-ref}`app Asistente de Nextcloud <ai-app-assistant>`
1. {nc-ref}`Instalar AppAPI y configurar un Deploy Demon <ai-app_api>`
2. Instalar la ExApp *stt_whisper2* «Local Speech-To-Text» desde la página «Apps» de la interfaz web de administración de Nextcloud

#### Suministrar modelos alternativos

Esta app permite suministrar modelos alternativos en el directorio `/nc_app_stt_whisper2_data` del contenedor de docker. Puede usarse cualquier [modelo *faster-whisper* de Systran en hugging face](https://huggingface.co/Systran) de la siguiente manera:

1. clonando con git el repositorio correspondiente
2. Copiando la carpeta con el repositorio git a `/nc_app_stt_whisper2_data` dentro del contenedor de docker.
3. Reiniciando la ExApp Whisper
4. Seleccionando el modelo correspondiente en las configuraciones de administración de IA de Nextcloud

### Escalado

Actualmente no es posible escalar esta app; {vendor}`Nextcloud` está trabajando en ello. Según los cálculos de {vendor}`Nextcloud`, una instancia tiene una capacidad aproximada de 4 h de transcripción por minuto (medida con 8 hilos de CPU en un Intel(R) Xeon(R) Gold 6226R). No está claro hasta qué punto esta cifra se acerca al uso real, por lo que {vendor}`Nextcloud` agradece los comentarios basados en el uso real.

### Tienda de apps

Esta app también está en la tienda de apps de {vendor}`Nextcloud`, donde puede escribirse una reseña: <https://apps.nextcloud.com/apps/stt_whisper2>

### Repositorio

El repositorio de código de la app está en GitHub, donde pueden informarse errores y aportarse correcciones y funciones: <https://github.com/nextcloud/stt_whisper2>

Los clientes de {vendor}`Nextcloud` deben informar de los errores directamente al soporte al cliente de {vendor}`Nextcloud`.

### Limitaciones conocidas

- Actualmente no se admite la transcripción en directo
- Actualmente solo se admiten los idiomas que admiten los modelos Whisper subyacentes
- Los modelos whisper rinden de forma desigual según el idioma, y pueden mostrar menor precisión en idiomas con pocos recursos o poca visibilidad, o en idiomas para los que había menos datos de entrenamiento disponibles. Los modelos también muestran un rendimiento dispar con distintos acentos y dialectos de determinados idiomas, lo que puede incluir una mayor tasa de error de palabras entre hablantes de distintos géneros, razas, edades u otros criterios demográficos.
- Los modelos de lenguaje tienden a generar información falsa, por lo que solo deben usarse en situaciones que no sean críticas. Se recomienda usar la IA solo al principio de un proceso de creación y no al final, de modo que sus resultados sirvan, por ejemplo, como borrador y no como producto final. Revisar siempre los resultados de los modelos de lenguaje antes de usarlos.
- Asegurarse de probar el modelo de lenguaje que se usa para comprobar si cumple los requisitos de calidad del caso de uso
- Los modelos de lenguaje tienen un consumo de energía notoriamente alto; para reducir la carga del servidor pueden elegirse modelos más pequeños o cuantizados a cambio de una menor precisión
- El soporte al cliente está disponible previa solicitud; sin embargo, {vendor}`Nextcloud` no puede resolver resultados falsos o problemáticos, la mayoría de los problemas de rendimiento ni otros problemas causados por el modelo subyacente. Por tanto, el soporte se limita a los errores causados directamente por la implementación de la app (conectores, API, frontend, AppAPI)
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
