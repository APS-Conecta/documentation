---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "text2image_stablediffusion2, generación de imágenes local: requisitos, instalación, escalado, tienda de apps, repositorio y limitaciones conocidas."
---
# App: Generación de imágenes local (text2image_stablediffusion2)

## Resumen

Esta página describe, para quienes administran el servidor, la app text2image_stablediffusion2, que genera imágenes con modelos de código abierto ejecutados en el propio servidor: sus requisitos, su instalación, el escalado y sus limitaciones conocidas. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/app_text2image_stablediffusion2.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

(nc-ai-app-text2image_stablediffusion2)=
La app *text2image_stablediffusion2* es una de las apps que aportan funcionalidad de generación de imágenes en Nextcloud y actúan como backend de generación de imágenes para la {nc-ref}`app Asistente de Nextcloud <ai-app-assistant>` y otras apps que usan la funcionalidad de generación de imágenes. La app *text2image_stablediffusion2* en concreto solo ejecuta modelos de código abierto, y lo hace íntegramente en las instalaciones propias. {vendor}`Nextcloud` puede ofrecer soporte al cliente previa solicitud; las posibilidades pueden consultarse con el gestor de cuenta.

### Requisitos

- Esta app está construida como app externa (External App) y, por tanto, depende de AppAPI v3.1.0 o superior
- Nextcloud AIO es compatible
- Actualmente se admiten GPU NVIDIA y CPU x86_64
- CUDA >= v12.2 en el sistema anfitrión
- Dimensionamiento con GPU

   - Una GPU NVIDIA con al menos 8GB de VRAM

- Dimensionamiento con CPU

   - Al menos 8GB de RAM del sistema
   - Cuantos más núcleos y más potente sea la CPU, mejor; se recomiendan entre 10 y 20 núcleos
   - De forma predeterminada, la app acapara todos los núcleos, por lo que suele ser mejor ejecutarla en una máquina aparte

### Instalación

- Asegurarse de que esté instalada la {nc-ref}`app Asistente de Nextcloud <ai-app-assistant>`
- {nc-ref}`Instalar AppAPI y configurar un Deploy Demon <ai-app_api>`
- Instalar la ExApp «Local large language model» desde la página «Apps» de la interfaz web de administración de Nextcloud

### Escalado

Actualmente no es posible escalar esta app; {vendor}`Nextcloud` está trabajando en ello. Según los cálculos de {vendor}`Nextcloud`, una instancia tiene una capacidad aproximada de 120 solicitudes de imágenes por hora (cada solicitud de usuario puede pedir varias imágenes). Sin embargo, esta cifra es teórica, y {vendor}`Nextcloud` agradece los comentarios basados en el uso real.

### Tienda de apps

La app también está en la tienda de apps de {vendor}`Nextcloud`, donde puede escribirse una reseña: <https://apps.nextcloud.com/apps/text2image_stablediffusion2>

### Repositorio

El repositorio de código de la app está en GitHub, donde pueden informarse errores y aportarse correcciones y funciones: <https://github.com/nextcloud/text2image_stablediffusion2>

Los clientes de {vendor}`Nextcloud` deben informar de los errores directamente al sistema de soporte de {vendor}`Nextcloud`.

### Limitaciones conocidas

- Las imágenes generadas tienen una resolución fija (512x512 píxeles), y el modelo no logra un fotorrealismo perfecto
- El modelo no puede representar texto legible
- Los rostros y las personas en general pueden no generarse correctamente
- Los resultados de ciertas solicitudes de generación de imágenes pueden estar sesgados y reforzar estereotipos
- Actualmente solo se admiten los idiomas que admite el modelo subyacente; la corrección del uso del idioma en idiomas distintos del inglés puede ser deficiente según la cobertura del idioma en los datos de entrenamiento del modelo
- Asegurarse de probar la app para comprobar si cumple los requisitos de calidad del caso de uso
- El soporte al cliente está disponible previa solicitud; sin embargo, {vendor}`Nextcloud` no puede resolver resultados falsos o problemáticos, la mayoría de los problemas de rendimiento ni otros problemas causados por el modelo subyacente. Por tanto, el soporte se limita a los errores causados directamente por la implementación de la app (conectores, API, frontend, AppAPI)
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
