---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Recognize: etiquetado de fotos, audio y vídeo y reconocimiento facial; requisitos, instalación, escalado, limitaciones y clasificación de IA ética."
---
# App: Recognize

## Resumen

Esta página describe, para quienes administran el servidor, la app Recognize, que etiqueta fotos, audio y vídeo y reconoce caras con modelos de código abierto ejecutados en el propio servidor: dónde se ven sus resultados, sus requisitos, su instalación, su escalado, sus limitaciones y su clasificación de IA ética. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/app_recognize.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

(nc-ai-app-recognize)=
La app *recognize* aporta funciones de etiquetado multimedia y de reconocimiento facial para la app Memories. *Recognize* puede agrupar caras similares en las fotos de los usuarios («reconocimiento facial»); puede añadir etiquetas adecuadas a las fotos detectando paisajes, comida, vehículos, edificios, animales y otros objetos, así como lugares emblemáticos y monumentos conocidos; puede reconocer géneros musicales en los archivos de audio de los usuarios y añade etiquetas para ellos; puede reconocer acciones humanas en los archivos de vídeo de los usuarios y añadir etiquetas para ellas. En concreto, solo ejecuta modelos de código abierto, y lo hace íntegramente en las instalaciones propias. {vendor}`Nextcloud` puede ofrecer soporte al cliente previa solicitud; las posibilidades pueden consultarse con el gestor de cuenta.

### Interfaz

Los archivos etiquetados aparecen en la app Memories, en la sección «Etiquetas», y también en la app Archivos normal. Los resultados del reconocimiento facial aparecen en la sección «Personas» de la app Memories.

### Requisitos

- Nextcloud AIO no es compatible, pero probablemente funcione a una velocidad inferior a la óptima
- Versión mínima compatible de Nextcloud: 26
- CPU x86
- GNU lib C
- Los trabajos en segundo plano deben ejecutarse mediante cron
- El procesamiento con GPU es compatible, pero no obligatorio; sin GPU cabe esperar un rendimiento lento
- Actualmente solo se admiten GPU NVIDIA
- Para el soporte de GPU hay que instalar:

   - Controladores de GPU NVIDIA® versión 450.80.02 o superior.
   - CUDA® Toolkit 11.x
   - cuDNN SDK 8.x

- Dimensionamiento con GPU

   - Los modelos que usa recognize requieren alrededor de 1GB de VRAM o menos

- Dimensionamiento con CPU

   - Si no hay GPU, esta app usa los núcleos de la CPU
   - Cuantos más núcleos y más potente sea la CPU, mejor; se recomiendan entre 10 y 20 núcleos
   - En los ajustes de la app puede fijarse el número de núcleos que se usan
   - Al menos ~4GB de RAM dedicados a recognize

#### Uso de espacio en disco

- ~1.5GB para todos los modelos en total

### Instalación

1. Instalar la app *recognize* desde la página «Apps» de Nextcloud o ejecutando

   occ app:enable recognize

2. Ejecutar el siguiente comando en el terminal del servidor de cada nodo que ejecute trabajos en segundo plano:

   occ recognize:download-models

3. Ir a las configuraciones de administración de Nextcloud y abrir la página de ajustes de administración de *recognize*
4. Activar todos los modos de funcionamiento que se quiera que lleve a cabo la app
5. Activar el modo GPU si se tiene una GPU que se quiera usar; si se quiere usar solo la CPU, aquí puede fijarse el número de núcleos que se usan
6. Ejecutar el siguiente comando en el terminal del servidor para detener el procesamiento en segundo plano de los archivos existentes:

   occ recognize:clear-background-jobs

7. Ejecutar el siguiente comando en el terminal del servidor para procesar en bloque todos los archivos existentes (puede tardar mucho, según cuántos archivos haya en la instancia):

   occ recognize:classify

8. Ejecutar el siguiente comando en el terminal del servidor para calcular los grupos de caras a partir de las caras encontradas en todos los archivos existentes (ejecutarlo repetidamente hasta que no se encuentren más grupos):

   occ recognize:cluster-faces

9. A partir de este momento, todos los archivos nuevos se procesarán automáticamente en tareas en segundo plano, sin intervención manual

### Escalado

Es posible escalar esta app añadiendo al clúster varios nodos «de segundo plano» que solo procesen trabajos en segundo plano ejecutando cron.php.

### Tienda de apps

La app también está en la tienda de apps de {vendor}`Nextcloud`, donde puede escribirse una reseña: <https://apps.nextcloud.com/apps/recognize>

### Repositorio

El repositorio del código fuente de la app está en GitHub, donde pueden informarse errores y aportarse correcciones y funciones: <https://github.com/nextcloud/recognize>

Los clientes de {vendor}`Nextcloud` deben informar de los errores directamente al sistema de soporte de {vendor}`Nextcloud`.

### Limitaciones conocidas

- Asegurarse de probar si la funcionalidad cumple los requisitos de calidad del caso de uso
- Los modelos de aprendizaje automático tienen un consumo de energía notoriamente alto
- El soporte al cliente está disponible previa solicitud; sin embargo, {vendor}`Nextcloud` no puede resolver resultados falsos o problemáticos, la mayoría de los problemas de rendimiento ni otros problemas causados por el modelo subyacente. Por tanto, el soporte se limita a los errores causados directamente por la implementación de la app (conectores, API, front-end, AppAPI)

### Clasificación de IA ética

#### Clasificación para la detección de objetos en fotos: verde

Aspectos positivos:

- El software de entrenamiento e inferencia de este modelo es de código abierto
- El modelo entrenado está disponible libremente y, por tanto, puede ejecutarse en las instalaciones propias
- Los datos de entrenamiento están disponibles libremente, lo que permite comprobar o corregir sesgos u optimizar el rendimiento y el uso de CO2.

#### Clasificación para el reconocimiento facial en fotos: verde

Aspectos positivos:

- El software de entrenamiento e inferencia de este modelo es de código abierto
- El modelo entrenado está disponible libremente y, por tanto, puede ejecutarse en las instalaciones propias
- Los datos de entrenamiento están disponibles libremente, lo que permite comprobar o corregir sesgos u optimizar el rendimiento y el uso de CO2.

#### Clasificación para el reconocimiento de acciones en vídeo: verde

Aspectos positivos:

- El software de entrenamiento e inferencia de este modelo es de código abierto
- El modelo entrenado está disponible libremente y, por tanto, puede ejecutarse en las instalaciones propias
- Los datos de entrenamiento están disponibles libremente, lo que permite comprobar o corregir sesgos u optimizar el rendimiento y el uso de CO2.

#### Clasificación del reconocimiento de géneros musicales: amarillo

Aspectos positivos:

- El software de entrenamiento e inferencia de este modelo es de código abierto
- El modelo entrenado está disponible libremente y, por tanto, puede ejecutarse en las instalaciones propias

Aspectos negativos:

- Los datos de entrenamiento no están disponibles libremente, lo que limita la capacidad de terceros para comprobar y corregir sesgos u optimizar el rendimiento y el uso de CO2 del modelo.

Más información sobre la clasificación de IA ética de {vendor}`Nextcloud` [en su blog](https://nextcloud.com/blog/nextcloud-ethical-ai-rating/).
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
