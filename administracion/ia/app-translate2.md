---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "translate2, traducción automática local: idiomas, requisitos, espacio, instalación, cambio de modelo, clasificación de IA ética y limitaciones."
---
# App: Traducción automática local 2 (translate2)

## Resumen

Esta página describe, para quienes administran el servidor, la app translate2, que traduce texto con modelos de código abierto ejecutados en el propio servidor: los idiomas, los requisitos y el espacio que ocupa, la instalación, el cambio de modelo, su clasificación de IA ética y sus limitaciones conocidas. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/app_translate2.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

(nc-ai-app-translate2)=
La app *translate2* es una de las apps que aportan funcionalidad de traducción automática en Nextcloud y actúan como backend de traducción para la {nc-ref}`app Asistente de Nextcloud <ai-app-assistant>`. La app *translate2* en concreto solo ejecuta modelos de código abierto, y lo hace íntegramente en las instalaciones propias. {vendor}`Nextcloud` puede ofrecer soporte al cliente previa solicitud; las posibilidades pueden consultarse con el gestor de cuenta.

Actualmente la app admite más de 400 idiomas. La lista completa está aquí: <https://huggingface.co/datasets/allenai/MADLAD-400>

### Requisitos

- Versión mínima de Nextcloud: 30
- Esta app está construida como app externa (External App) y, por tanto, depende de AppAPI v3.1.0 o superior
- Nextcloud AIO es compatible
- Actualmente se admiten GPU NVIDIA y CPU x86_64
- CUDA >= v12.2.2 en el sistema anfitrión
- Dimensionamiento con GPU

   - Una GPU NVIDIA con al menos 4 GB de VRAM
   - Al menos 6 GB de RAM del sistema

- Dimensionamiento con CPU

   - CPU x86 con 4-8 núcleos para uso de la app (cuantos más núcleos, más rápida será)
   - Al menos 6 GB de RAM para la app deberían bastar (incluye el software y las bibliotecas, y el modelo)

#### Uso de espacio

- ~ 2.95 GB para el contenedor de docker
- ~ 2.77 GB para el modelo predeterminado

### Instalación

0. Asegurarse de que esté instalada la {nc-ref}`app Asistente de Nextcloud <ai-app-assistant>`
1. {nc-ref}`Instalar AppAPI y configurar un Deploy Demon <ai-app_api>`
2. Instalar la ExApp «Local Machine Translation» (translate2) desde la página «Apps» de la interfaz web de administración de Nextcloud

(model-switch)=
### Cambio de modelo

1. Quitar la clave `hf_model_path` del objeto `loader` en el archivo `config.json` del contenedor de docker llamado `nc_app_translate2`.
2. Cambiar `model_name` al nuevo nombre de modelo, `Nextcloud-AI/madlad400-7b-mt-bt-ct2-int8_float32`.
3. Reiniciar el contenedor de docker `docker restart nc_app_translate2`

### Tienda de apps

La app también está en la tienda de apps de {vendor}`Nextcloud`, donde puede escribirse una reseña: <https://apps.nextcloud.com/apps/translate2>

### Repositorio

El repositorio de código de la app está en GitHub, donde pueden informarse errores y aportarse correcciones y funciones: <https://github.com/nextcloud/translate2>

Los clientes de {vendor}`Nextcloud` deben informar de los errores directamente al soporte al cliente de {vendor}`Nextcloud`.

### Clasificación de IA ética

#### Clasificación: 🟢

Positivo:
\* el software de entrenamiento e inferencia de este modelo es de código abierto
\* el modelo entrenado está disponible libremente y, por tanto, puede ejecutarse en las instalaciones propias
\* los datos de entrenamiento están disponibles libremente, lo que permite comprobar o corregir sesgos u optimizar el rendimiento y el consumo de CO2.

Más información sobre la clasificación de IA ética de {vendor}`Nextcloud` [en su blog](https://nextcloud.com/blog/nextcloud-ethical-ai-rating).

### Limitaciones conocidas

- Las traducciones con IA no sustituyen a las traducciones profesionales hechas por personas y, en muchos casos, requieren posedición. Las traducciones con IA sirven para entender el contenido principal de un texto, pero no para traducciones que requieren conocimientos especiales (como contenido técnico o jurídico) ni para traducciones que requieren un estilo de redacción específico para transmitir estilo, un significado más profundo o emociones (como contenido de marketing o la traducción de libros).
- Aunque la calidad del resultado será buena en los idiomas más comunes (inglés, francés, español), la calidad empeorará en los idiomas con menos cobertura en el conjunto de entrenamiento original.
- Asegurarse de probar el modelo de traducción que se usa para comprobar si cumple los requisitos de calidad del caso de uso. El modelo predeterminado es el más pequeño del lote y puede producir traducciones duplicadas. Si se necesita mejor calidad y menos artefactos, cambiar a un modelo más grande; ver [Cambio de modelo](#model-switch).
- Los modelos de lenguaje tienen un consumo de energía notoriamente alto.
- El soporte al cliente está disponible previa solicitud; sin embargo, {vendor}`Nextcloud` no puede resolver resultados falsos o problemáticos, la mayoría de los problemas de rendimiento ni otros problemas causados por los modelos subyacentes. Por tanto, el soporte se limita a los errores causados directamente por la implementación de la app (conectores, API, frontend, AppAPI).
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
