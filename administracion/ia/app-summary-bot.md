---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Summary Bot, bot de resúmenes para los chats de Talk: requisitos, instalación desde la tienda o manual, uso, clasificación de IA ética y limitaciones."
---
# App: Summary Bot (bot de resúmenes del chat de Talk)

## Resumen

Esta página explica, para quienes administran el servidor, cómo instalar y configurar Summary Bot, el bot que resume los mensajes de una conversación de Talk, desde la tienda de apps o de forma manual, y recoge sus requisitos, su uso, su clasificación de IA ética y sus limitaciones. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/app_summary_bot.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

(nc-ai-app-summary-bot)=
La app *Summary Bot* utiliza proveedores de modelos de lenguaje de gran tamaño (LLM) en Nextcloud y puede añadirse a una conversación de *Nextcloud Talk* para generar resúmenes de los mensajes de chat de esa sala, ya sea bajo demanda o siguiendo una programación.
Puede funcionar con modelos únicamente de código abierto o con modelos propietarios, ya sea en las instalaciones propias o en la nube, aprovechando apps como la [app de modelo de lenguaje de gran tamaño local](https://apps.nextcloud.com/apps/llm2) o la [app de integración con OpenAI y LocalAI](https://apps.nextcloud.com/apps/integration_openai).

{vendor}`Nextcloud` puede ofrecer soporte al cliente previa solicitud; las posibilidades pueden consultarse con el gestor de cuenta.

Actualmente la app admite los siguientes idiomas:

- inglés (en)

La calidad de los resúmenes depende directamente de la calidad del modelo subyacente. Se recomienda probar el modelo para el caso de uso deseado antes de aplicarlo.

### Requisitos

- Versión mínima de Nextcloud: 30
- Docker
- AppAPI >= 3.0.0
- Talk
- Un proveedor de procesamiento de tareas, como la app de modelo de lenguaje de gran tamaño local (llm2) o la app de integración con OpenAI y LocalAI (integration_openai)

#### Uso de espacio

- ~100MB

### Instalación

0. Asegurarse de que estén instaladas las siguientes apps:

   - [App AppAPI de Nextcloud](https://apps.nextcloud.com/apps/app_api)

   - [App Nextcloud Talk (Spreed)](https://apps.nextcloud.com/apps/spreed)

   - Uno de los siguientes proveedores de modelos de IA:

     - [App de modelo de lenguaje de gran tamaño local de Nextcloud](https://apps.nextcloud.com/apps/llm2)

     - [App de integración con OpenAI y LocalAI de Nextcloud](https://apps.nextcloud.com/apps/integration_openai)

     - [App de integración con IBM watsonx.ai de Nextcloud](https://apps.nextcloud.com/apps/integration_watsonx)

#### Configuración (desde la tienda de apps)

1. Instalar la app *Summary Bot* desde la página «Apps» de Nextcloud

2. Activar el bot *Summary Bot* para la sala de chat seleccionada mediante el menú de tres puntos de la sala de chat (los ajustes de bots están en la sección *Bots*)

#### Configuración (manual)

Después de clonar esta app *manualmente* (clonada mediante git en el directorio de apps), hay que ejecutar los siguientes pasos:

1. Cambiar a la carpeta en la que se clonó el código fuente:

   ```
   cd  /path/to/your/nextcloud/webroot/apps/summary_bot/
   ```

2. Construir la imagen de docker:

   ```
   docker build --no-cache -f Dockerfile -t local_summary_bot .
   ```

3. Ejecutar la imagen de docker:

   *Información:*

   - La variable de entorno APP_VERSION debe ser igual a la versión de *Summary Bot* que se esté usando

   - La variable de entorno NEXTCLOUD_URL debe fijarse con la URL de la instancia de Nextcloud, asegurándose de que la imagen de docker pueda alcanzarla.

   ```
   sudo docker run -ti -v /etc/localtime:/etc/localtime:ro -v /etc/timezone:/etc/timezone:ro -e APP_ID=summary_bot -e APP_DISPLAY_NAME="Summary Bot" -e APP_HOST=0.0.0.0 -e APP_PORT=9031 -e APP_SECRET=12345 -e APP_VERSION=1.0.0 -e NEXTCLOUD_URL='<YOUR_NEXTCLOUD_URL_REACHABLE_FROM_INSIDE_DOCKER>' -p 9031:9031 local_summary_bot
   ```

4. Anular el registro de Summary Bot si ya está instalado

   ```
   sudo -E -u www-data php occ app_api:app:unregister summary_bot
   ```

5. Registrar Summary Bot para que la instancia de Nextcloud lo conozca

   *Información:* Ajustar el valor de host del siguiente ejemplo a la dirección IP del contenedor de docker (para mayor seguridad)

   ```
   sudo -E -u www-data php occ app_api:app:register summary_bot manual_install --json-info '{ "id": "summary_bot", "name": "Summary Bot", "daemon_config_name": "manual_install", "version": "1.0.0", "secret": "12345", "host": "0.0.0.0", "port": 9031, "scopes": ["AI_PROVIDERS", "TALK", "TALK_BOT"], "protocol": "http"}' --force-scopes --wait-finish
   ```

6. Activar *Summary Bot* para la sala de chat seleccionada mediante el menú de tres puntos de la sala de chat (los ajustes de bots están en la sección *Bots*)

### Uso

Después de activar *Summary Bot* en una sala de chat, puede probarse su funcionamiento simplemente enviando el siguiente mensaje:

> «@summary» o «@summary help»

### Tienda de apps

La app también está en la tienda de apps de {vendor}`Nextcloud`, donde puede escribirse una reseña: <https://apps.nextcloud.com/apps/summary_bot>

### Repositorio

El repositorio de código de la app está en GitHub, donde pueden informarse errores y aportarse correcciones y funciones: <https://github.com/nextcloud/summary_bot>

Los clientes de {vendor}`Nextcloud` deben informar de los errores directamente al soporte al cliente de {vendor}`Nextcloud`.

### Clasificación de IA ética

La clasificación ética de *Summary Bot*, que usa un modelo para el procesamiento de texto a través de la app Asistente de Nextcloud, depende en gran medida de la elección e implementación del modelo subyacente.

Más información sobre la clasificación de IA ética de {vendor}`Nextcloud` [en su blog](https://nextcloud.com/blog/nextcloud-ethical-ai-rating/).

### Limitaciones conocidas

- Summary Bot no puede acceder a conversaciones anteriores; solo reconoce los mensajes desde el momento en que se activó en la sala de chat.
- Se admite un resumen de 40000 caracteres como máximo. Esto supone que el modelo subyacente puede manejar esta cantidad de texto (lo que debería rondar una longitud de contexto de 16000).
- No se admiten idiomas distintos del inglés. Aun así, el modelo subyacente puede entender otros idiomas.
- Los modelos de IA pueden producir ocasionalmente información inexacta. Por tanto, deben emplearse con precaución en escenarios no críticos. Es fundamental verificar la exactitud de los resultados del bot antes de aplicarlos.
- Tener en cuenta que los modelos de IA pueden consumir una cantidad considerable de energía. Es aconsejable considerar este factor en la planificación y el funcionamiento de los sistemas de IA si se alojan en las instalaciones propias o si la sostenibilidad es una preocupación.
- Los modelos de IA pueden tener tiempos de procesamiento prolongados cuando se ejecutan en CPU. Para mejorar la eficiencia, se recomienda usar soporte de GPU para agilizar la atención de las solicitudes.
- El soporte al cliente está disponible previa solicitud; sin embargo, {vendor}`Nextcloud` no puede resolver resultados falsos o problemáticos (alucinaciones), la mayoría de los problemas de rendimiento ni otros problemas causados por los modelos subyacentes. Por tanto, el soporte se limita a los errores causados directamente por la implementación de la app (conectores, API, frontend, AppAPI)
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
