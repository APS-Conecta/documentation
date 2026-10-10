---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "text2speech_kokoro, texto a voz local con Kokoro: idiomas, requisitos, instalación, escalado, tienda de apps, repositorio y limitaciones conocidas."
---
# App: Texto a voz local (text2speech_kokoro)

## Resumen

Esta página describe, para quienes administran el servidor, la app text2speech_kokoro, que genera voz a partir de texto con modelos Kokoro de código abierto ejecutados en el propio servidor: los idiomas que admite, sus requisitos, su instalación, el escalado y sus limitaciones conocidas. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/app_text2speech_kokoro.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

(nc-ai-app-text2speech_kokoro)=
La app *text2speech_kokoro* es una de las apps que aportan funcionalidad de texto a voz en Nextcloud y actúan como backend de generación de voz para la {nc-ref}`app Asistente de Nextcloud <ai-app-assistant>` y {nc-ref}`otras apps que usan el tipo de tarea central de texto a voz <t2s-consumer-apps>`. La app *text2speech_kokoro* en concreto solo ejecuta modelos de código abierto, y lo hace íntegramente en las instalaciones propias. {vendor}`Nextcloud` puede ofrecer soporte al cliente previa solicitud; las posibilidades pueden consultarse con el gestor de cuenta.

Esta app usa internamente [Kokoro](https://github.com/hexgrad/kokoro).

El modelo usado admite los siguientes idiomas:

- inglés estadounidense
- inglés británico
- español
- francés
- italiano
- hindi
- portugués
- japonés
- mandarín

### Requisitos

- Versión mínima de Nextcloud: 31
- Esta app está construida como app externa (External App) y, por tanto, depende de AppAPI v2.3.0
- Nextcloud AIO es compatible
- Actualmente se admiten CPU x86_64
- No se admiten GPU

- Dimensionamiento con CPU

   - Cuantos más núcleos y más potente sea la CPU, mejor; se recomiendan unos 10 núcleos
   - De forma predeterminada, la app acapara todos los núcleos, por lo que suele ser mejor ejecutarla en una máquina aparte
   - 800MB de RAM

### Instalación

0. Asegurarse de que esté instalada la {nc-ref}`app Asistente de Nextcloud <ai-app-assistant>`
1. {nc-ref}`Instalar AppAPI y configurar un Deploy Demon <ai-app_api>`
2. Instalar la ExApp *text2speech_kokoro* «Local Text-To-Speech» desde la página «Apps» de la interfaz web de administración de Nextcloud

### Escalado

Actualmente no es posible escalar esta app; {vendor}`Nextcloud` está trabajando en ello. Según los cálculos de {vendor}`Nextcloud`, una instancia tiene una capacidad aproximada de 4 h de rendimiento de transcripción por minuto (medida con 8 hilos de CPU en un Intel(R) Xeon(R) Gold 6226R). No está claro hasta qué punto esta cifra se acerca al uso real, por lo que {vendor}`Nextcloud` agradece los comentarios basados en el uso real.

### Tienda de apps

Esta app también está en la tienda de apps de {vendor}`Nextcloud`, donde puede escribirse una reseña: <https://apps.nextcloud.com/apps/text2speech_kokoro>

### Repositorio

El repositorio de código de la app está en GitHub, donde pueden informarse errores y aportarse correcciones y funciones: <https://github.com/nextcloud/text2speech_kokoro>

Los clientes de {vendor}`Nextcloud` deben informar de los errores directamente al soporte al cliente de {vendor}`Nextcloud`.

### Limitaciones conocidas

- Actualmente solo se admiten los idiomas que admite el modelo Kokoro subyacente
- Los modelos Kokoro rinden de forma desigual según el idioma, y pueden mostrar menor precisión en idiomas con pocos recursos o poca visibilidad, o en idiomas para los que había menos datos de entrenamiento disponibles.
- Asegurarse de probar el modelo de lenguaje que se usa para comprobar si cumple los requisitos de calidad del caso de uso
- El soporte al cliente está disponible previa solicitud; sin embargo, {vendor}`Nextcloud` no puede resolver resultados falsos o problemáticos, la mayoría de los problemas de rendimiento ni otros problemas causados por el modelo subyacente. Por tanto, el soporte se limita a los errores causados directamente por la implementación de la app (conectores, API, frontend, AppAPI)
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
