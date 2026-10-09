---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Transcripción y traducción en directo de las llamadas de Talk: instalación, requisitos de hardware, registros y limitaciones de live_transcription."
---
# App: Transcripción y traducción en directo en Nextcloud Talk (live_transcription)

## Resumen

Esta página explica, para quienes administran el servidor, cómo instalar la app live_transcription, que transcribe y traduce en directo la voz de las llamadas de Talk, junto con sus requisitos de hardware, sus registros y sus limitaciones. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/app_live_transcription.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

(nc-ai-live-transcription)=
Esta app ofrece transcripción y traducción en directo de la voz en las llamadas de Nextcloud Talk mediante modelos de IA de código abierto que proporciona [Vosk](https://alphacephei.com/vosk/).\
La transcripción se realiza en el propio servidor, lo que preserva la privacidad y la soberanía de los datos, mientras que la traducción la realiza un proveedor de procesamiento de tareas de traducción como la {nc-ref}`app translate2 <ai-app-translate2>`. Pronto también se admitirán para la traducción las apps [Integración con OpenAI y LocalAI](https://apps.nextcloud.com/apps/integration_openai) e [Integración con DeepL](http://apps.nextcloud.com/apps/integration_deepl).

Se descarga automáticamente un buen conjunto de modelos de lenguaje para la transcripción. Incluyen árabe, árabe (tunecino), bretón, catalán, checo, alemán, inglés, esperanto, español, persa (farsi), francés, hindi, italiano, japonés, kazajo, coreano, neerlandés, polaco, portugués (de Brasil), ruso, telugu, tayiko, turco, ucraniano, uzbeko, vietnamita y chino.\
Las capacidades de traducción dependen de la app de proveedor de procesamiento de tareas de traducción instalada. Hay una lista de apps con capacidad de traducción {nc-ref}`aquí <mt-consumer-apps>`, en la sección «Apps de backend».

### Instalación

1. Asegurarse de que esté instalada la [app Nextcloud Talk](https://apps.nextcloud.com/apps/spreed).
2. Asegurarse de que el High-Performance Backend (la última versión o una publicada después de septiembre de 2025) esté instalado y configurado en los ajustes de Nextcloud Talk. Hay más información en el [manual de instalación de Nextcloud Talk](https://nextcloud-talk.readthedocs.io/en/latest/quick-install/).
3. Configurar un {nc-ref}`Deploy Daemon <ai-app_api>` en las configuraciones de administración de AppAPI.
4. Instalar la app **live_transcription** desde la página «Apps» de Nextcloud o ejecutando

   ```
   occ app_api:app:register live_transcription \
     --env LT_HPB_URL=wss://cloud.example.com/standalone-signaling/spreed \
     --env LT_INTERNAL_SECRET=1234 \
     --wait-finish
   ```

   :::{important}
   Las variables de entorno `LT_HPB_URL` y `LT_INTERNAL_SECRET` deben fijarse en las {nc-ref}`Opciones del despliegue <ai-app_api_deploy_options>` durante la instalación,
   y el High-Performance Backend debe estar configurado y en funcionamiento en los ajustes de Nextcloud Talk para que la app funcione.

   Estas variables de entorno pueden cambiarse después de la instalación volviendo a instalar la app tras desinstalarla primero.
   :::

5. Instalar una app de proveedor de procesamiento de tareas de texto a texto para disponer de capacidades de traducción, de la sección «Apps de backend» {nc-ref}`aquí <mt-consumer-apps>`.

### Requisitos

- Versión mínima de Nextcloud: 33
- Nextcloud AIO es compatible
- Actualmente se admiten GPU NVIDIA y CPU x86_64. También se admite la transcripción solo con CPU, que funciona bien en CPU x86 modernas.
- CUDA >= v12.4.1 en el sistema anfitrión para la transcripción con GPU
- Dimensionamiento con GPU

   - Una GPU NVIDIA con al menos 10 GB de VRAM
   - 16 GB de RAM del sistema deberían bastar para una o dos llamadas simultáneas

- Dimensionamiento con CPU

   - CPU x86 con 4 hilos. 2 hilos adicionales por cada llamada simultánea.
   - 16 GB de RAM deberían bastar para una o dos llamadas simultáneas

- Uso de espacio
   - ~ 2.8 GB para el contenedor de docker
   - ~ 6.0 GB para los modelos predeterminados

:::{note}
Actualmente {vendor}`Nextcloud` tiene muy poca experiencia real ejecutando este software en instancias de producción.
Las recomendaciones de dimensionamiento anteriores proceden de estimaciones de {vendor}`Nextcloud` y no son mediciones reales.
Los requisitos reales variarán según factores como el número de llamadas simultáneas, la calidad del audio y los idiomas seleccionados.
Hacer pruebas exhaustivas para confirmar que el hardware cubre las necesidades.
:::

### Registros

Las advertencias y los errores se registran en los registros principales del servidor Nextcloud.\
Para revisar los registros JSON detallados de los niveles inferiores, pueden ayudar los siguientes comandos.

Para ver los registros stdout/err de docker:

```bash
docker logs -f -n400 nc_app_live_transcription
```

Para ver los registros JSON:\
Los registros se rotan cuando el tamaño del archivo supera los 20 MiB. Los archivos de registro más antiguos se llaman `lt.log.1`, `lt.log.2`, etc.

```bash
docker exec -it nc_app_live_transcription tail -f -n400 /nc_app_live_transcription_data/logs/lt.log
```

Para descargar los registros JSON:

```bash
docker cp nc_app_live_transcription:/nc_app_live_transcription_data/logs/ /tmp/nc_app_live_transcription_logs
```

### Tienda de apps

La app también está en la tienda de apps de {vendor}`Nextcloud`, donde puede escribirse una reseña: <https://apps.nextcloud.com/apps/live_transcription>

### Repositorio

El repositorio de código de la app está en GitHub, donde pueden informarse errores y aportarse correcciones y funciones: <https://github.com/nextcloud/live_transcription>

Los clientes de {vendor}`Nextcloud` deben informar de los errores directamente al soporte al cliente de {vendor}`Nextcloud`.

### Limitaciones

- Las transcripciones generadas pueden no ser perfectas y contener errores. También pueden depender de la calidad del audio y del acento de quien habla.
- Actualmente la app solo admite un número limitado de idiomas. En el futuro podrían añadirse más.
- Los idiomas distintos del inglés pueden tener una precisión menor, principalmente porque los modelos incluidos son más pequeños.
- Actualmente la app no admite la puntuación en la transcripción.
- Las apps [Integración con OpenAI y LocalAI](https://apps.nextcloud.com/apps/integration_openai) e [Integración con DeepL](http://apps.nextcloud.com/apps/integration_deepl) aún no se admiten para la traducción.
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
