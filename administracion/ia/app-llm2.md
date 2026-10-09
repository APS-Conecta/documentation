---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "llm2, modelo de lenguaje local: modelos recomendados, idiomas, requisitos, instalación, modelos alternativos y su configuración, escalado y limitaciones."
---
# App: Modelo de lenguaje de gran tamaño local (llm2)

## Resumen

Esta página describe, para quienes administran el servidor, la app llm2, que ejecuta modelos de lenguaje de código abierto en el propio servidor: los modelos recomendados, los idiomas, los requisitos, la instalación, el uso y la configuración de modelos alternativos, el escalado y las limitaciones conocidas. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/app_llm2.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

(nc-ai-app-llm2)=
La app *llm2* es una de las apps que aportan funcionalidad de procesamiento de texto mediante modelos de lenguaje de gran tamaño en Nextcloud y actúan como backend de procesamiento de texto para la {nc-ref}`app Asistente de Nextcloud <ai-app-assistant>`, la app *mail* y {nc-ref}`otras apps que usan la API central de procesamiento de texto <tp-consumer-apps>`. La app *llm2* en concreto solo ejecuta modelos de código abierto, y lo hace íntegramente en las instalaciones propias. {vendor}`Nextcloud` puede ofrecer soporte al cliente previa solicitud; las posibilidades pueden consultarse con el gestor de cuenta.

Esta app usa internamente [llama.cpp](https://github.com/abetlen/llama-cpp-python) y, por tanto, es compatible con cualquier modelo en formato *gguf*.

Sin embargo, {vendor}`Nextcloud` solo hace pruebas con Llama 3.1. La calidad de los resultados variará según el modelo que se use, y las tareas posteriores, como el resumen o Context Chat, pueden no funcionar con otros modelos.
Por tanto, se recomiendan los siguientes modelos:

- [Llama3.1 8b Instruct](https://huggingface.co/QuantFactory/Meta-Llama-3.1-8B-Instruct-GGUF) (calidad razonable; rápido; buena acogida; viene incluido con la app)
- [Llama3.1 70B Instruct](https://huggingface.co/bartowski/Meta-Llama-3.1-70B-Instruct-GGUF) (buena calidad; buena acogida)

### Multilingüismo

Esta app admite entradas y salidas en idiomas distintos del inglés si el modelo subyacente admite el idioma.

Llama 3.1 [admite los siguientes idiomas:](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct#multilingual-benchmarks)

- inglés
- portugués
- español
- italiano
- alemán
- francés
- hindi
- tailandés

Tener en cuenta que otros idiomas también pueden funcionar, pero solo se garantiza el funcionamiento de los idiomas anteriores.

### Requisitos

- Esta app está construida como app externa (External App) y, por tanto, depende de AppAPI v3.1.0 o superior
- Nextcloud AIO es compatible
- Actualmente se admiten GPU NVIDIA y CPU x86_64
- CPU compatible con las instrucciones AVX y AVX2
- CUDA >= v12.4 en el sistema anfitrión
- Dimensionamiento con GPU

   - Una GPU NVIDIA con al menos 8GB de VRAM
   - Al menos 12GB de RAM del sistema

- Dimensionamiento con CPU

   - Al menos 12GB de RAM del sistema
   - Cuantos más núcleos y más potente sea la CPU, mejor; se recomiendan entre 10 y 20 núcleos
   - De forma predeterminada, la app acapara todos los núcleos, por lo que suele ser mejor ejecutarla en una máquina aparte

### Instalación

0. Asegurarse de que esté instalada la {nc-ref}`app Asistente de Nextcloud <ai-app-assistant>`
1. {nc-ref}`Instalar AppAPI y configurar un Deploy Demon <ai-app_api>`
2. Instalar la ExApp «Local large language model» desde la página «Apps» de la interfaz web de administración de Nextcloud

#### Suministrar modelos alternativos

Esta app permite suministrar modelos LLM alternativos como archivos *gguf* en el directorio `/nc_app_llm2_data` del contenedor de docker.

1. Descargar un modelo **gguf**, por ejemplo desde huggingface
2. Copiar el archivo **gguf** a `/nc_app_llm2_data` dentro del contenedor de docker
3. Reiniciar la ExApp llm2
4. Seleccionar el nuevo modelo en las configuraciones de administración de IA de Nextcloud

#### Configurar modelos alternativos

Como cada modelo requiere parámetros de inferencia ligeramente distintos, puede facilitarse un archivo de configuración para los archivos de modelo alternativos que se suministren.

El archivo de configuración de un archivo de modelo debe tener el mismo nombre que el archivo de modelo, pero debe terminar en `.json` en lugar de `.gguf`.

Las cadenas `{system_prompt}` y `{user_prompt}` son variables que rellena la app, por lo que deben formar parte de la plantilla de instrucciones (prompt template).

Este es un ejemplo de archivo de configuración para Llama 2:

```json
{
  "prompt": "<|im_start|> system\n{system_prompt}\n<|im_end|>\n<|im_start|> user\n{user_prompt}\n<|im_end|>\n<|im_start|> assistant\n",
  "loader_config": {
     "n_ctx": 4096,
     "max_tokens": 2048,
     "stop": ["<|im_end|>"]
  }
}
```

Este es un ejemplo de configuración para Llama 3:

```json
{
  "prompt": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{user_prompt}<|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>\n",
  "loader_config": {
      "n_ctx": 8000,
      "max_tokens": 4000,
      "stop": ["<|eot_id|>"],
      "temperature": 0.3
  }
}
```

### Escalado

Actualmente no es posible escalar esta app; {vendor}`Nextcloud` está trabajando en ello. Según los cálculos de {vendor}`Nextcloud`, una instancia tiene una capacidad aproximada de 1000 solicitudes de usuario por hora. Sin embargo, esta cifra es teórica, y {vendor}`Nextcloud` agradece los comentarios basados en el uso real.
Si se quiere ampliar el uso de modelos de lenguaje, se recomienda usar un {nc-ref}`proveedor de IA como servicio <ai-ai_as_a_service>` o alojar uno mismo un servicio compatible con la API de OpenAI que pueda escalarse, y conectar nextcloud a él mediante la [app integration_openai](https://apps.nextcloud.com/apps/integration_openai).

### Tienda de apps

La app también está en la tienda de apps de {vendor}`Nextcloud`, donde puede escribirse una reseña: <https://apps.nextcloud.com/apps/llm2>

### Repositorio

El repositorio de código de la app está en GitHub, donde pueden informarse errores y aportarse correcciones y funciones: <https://github.com/nextcloud/llm2>

Los clientes de {vendor}`Nextcloud` deben informar de los errores directamente al sistema de soporte de {vendor}`Nextcloud`.

### Limitaciones conocidas

- Actualmente solo se admiten los idiomas que admite el modelo subyacente; la corrección del uso del idioma en idiomas distintos del inglés puede ser deficiente según la cobertura del idioma en los datos de entrenamiento del modelo (se recomienda el modelo Llama 3 u otros modelos entrenados explícitamente con varios idiomas)
- Los modelos de lenguaje pueden ser malos en tareas de razonamiento
- Los modelos de lenguaje pueden ser malos en matemáticas
- Los modelos de lenguaje tienden a generar información falsa, por lo que solo deben usarse en situaciones que no sean críticas. Se recomienda usar la IA solo al principio de un proceso de creación y no al final, de modo que sus resultados sirvan, por ejemplo, como borrador y no como producto final. Revisar siempre los resultados de los modelos de lenguaje antes de usarlos.
- Asegurarse de probar el modelo de lenguaje que se usa para comprobar si cumple los requisitos de calidad del caso de uso
- Los modelos de lenguaje tienen un consumo de energía notoriamente alto; para reducir la carga del servidor pueden elegirse modelos más pequeños o cuantizados a cambio de una menor precisión
- El soporte al cliente está disponible previa solicitud; sin embargo, {vendor}`Nextcloud` no puede resolver resultados falsos o problemáticos, la mayoría de los problemas de rendimiento ni otros problemas causados por el modelo subyacente. Por tanto, el soporte se limita a los errores causados directamente por la implementación de la app (conectores, API, front-end, AppAPI)

### Apéndice: ejecutar con un modelo totalmente abierto

Si se quiere usar un modelo totalmente abierto que obtenga una puntuación verde en la clasificación de IA ética de {vendor}`Nextcloud`, se recomienda el siguiente modelo:

- Olmo 3 (en 7B o en 32B): <https://huggingface.co/allenai/Olmo-3-7B-Instruct>

#### ¿Qué hace de OLMo un modelo totalmente abierto?

- El código de entrenamiento, ajuste fino e inferencia del modelo está disponible públicamente y es totalmente de código abierto
- Los datos de entrenamiento con los que se preentrena el modelo están disponibles públicamente
- El propio modelo está disponible públicamente y es totalmente de código abierto
- Los datos de ajuste por instrucciones están disponibles públicamente
- El modelo de aprendizaje por refuerzo está disponible públicamente y es totalmente de código abierto

#### Limitaciones

- Actualmente OLMo solo funciona bien con entradas en inglés
- En las pruebas de {vendor}`Nextcloud` produjo a veces resultados alucinados o ininteligibles; asegurarse de probar a fondo el modelo para el caso de uso
- No puede usar herramientas, por lo que no puede usarse junto con {nc-ref}`Context Agent <ai-app-context_agent>`
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
