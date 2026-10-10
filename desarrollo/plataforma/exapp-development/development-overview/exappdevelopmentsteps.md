---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Pasos para desarrollar una ExApp: entorno, plantilla, métodos del ciclo de vida, empaquetado en Docker, publicación en la AppStore y pruebas."
---
(nc-dev-exappdevelopment)=
# Desarrollo de una ExApp

## Resumen

Esta página repasa los pasos del desarrollo de una ExApp: preparar el entorno, partir de una plantilla, implementar los métodos del ciclo de vida, empaquetarla como imagen Docker, publicarla en la AppStore y probarla. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/development_overview/ExAppDevelopmentSteps.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El proceso de desarrollo de una ExApp es similar al de una app normal de Nextcloud (PHP),
y debe seguir las mismas pautas en cuanto a seguridad, diseño y estilo de código (ver {nc-doc}`developer_manual/getting_started/development_process` para más detalles),
conforme a los estándares del lenguaje de programación que se use.

Aunque una ExApp puede desarrollarse en cualquier lenguaje, se sigue recomendando comprender
el {nc-doc}`ciclo de vida de las solicitudes en PHP <developer_manual/basics/request_lifecycle>` de Nextcloud y otros conceptos básicos,
ya que suelen ser similares en el backend de la ExApp con el que se comunica Nextcloud.

Cada ExApp puede entenderse como un microservicio (contenedor Docker)
que se ejecuta por separado de Nextcloud en el daemon de despliegue, que puede ser remoto o local.
La comunicación entre Nextcloud y la ExApp se realiza por red, protegida con {nc-doc}`AppAPIAuth <developer_manual/exapp_development/tech_details/Authentication>`.

A continuación se repasan brevemente los pasos del desarrollo de una ExApp.

### 0. Configuración del entorno de desarrollo

En primer lugar, se necesita una instalación de desarrollo de Nextcloud; consultar {nc-doc}`developer_manual/exapp_development/DevSetup` para más detalles.

### 1. Partir de una plantilla

Lo siguiente es preparar el esqueleto de la ExApp.
Hay varios ejemplos de ExApps disponibles, que pueden revisarse y usarse como punto de partida.
La plantilla y los ejemplos de ExApps:

- `[Python]` [Esqueleto de app](https://github.com/nextcloud/app-skeleton-python)
- `[Python]` [Esqueleto de UI Example](https://github.com/nextcloud/ui_example)
- `[Python]` [Ejemplo más complejo de interfaz de ExApp con un servicio de terceros](https://github.com/cloud-py-api/visionatrix)
- `[GoLang]` [Ejemplo de ExApp en Go Lang](https://github.com/nextcloud/file_to_text_example)
- etc.

Contienen la estructura básica de la ExApp, incluidos:

- Dockerfile
- Backend de la ExApp
- Frontend de la ExApp
- Configuración manual de las herramientas de traducción y un script de ejemplo para convertir los archivos de traducción al formato l10n de Nextcloud y al del lenguaje de programación que se use
- Algunos flujos de trabajo de GitHub necesarios (p. ej., [flujos de trabajo de compilación de imágenes Docker](https://github.com/cloud-py-api/visionatrix/tree/main/.github/workflows))

Hay más detalles en la sección {nc-ref}`ExAppOverview`.

### 3. Desarrollo

El proceso básico de desarrollo consta de los siguientes pasos:

- Implementar los {nc-ref}`métodos del ciclo de vida <ex_app_lifecycle_methods>` ExApp <-> Nextcloud:
  1. `/heartbeat`: método de latido (heartbeat) de la ExApp
  2. `/init`: método de inicialización de la ExApp
  3. `/enabled`: método de habilitación/deshabilitación de la ExApp
- Implementar la API y la lógica del backend de la ExApp
- Implementar el frontend de la ExApp (app Vue.js de Nextcloud) [opcional]

### 4. Empaquetado

El empaquetado de la ExApp puede hacerse manualmente o mediante GitHub Actions.
Se recomienda usar GitHub Actions para el empaquetado,
ya que automatiza el proceso de compilar la imagen Docker y subirla al registro de Docker.
El flujo de trabajo de GitHub Actions para compilar imágenes Docker se encuentra en el [ejemplo de servicio de terceros](https://github.com/cloud-py-api/visionatrix).

#### 4.1 Aceleración por hardware

Si la ExApp trabaja con GPU, conviene considerar compilar imágenes Docker distintas para cada dispositivo de cómputo.
Actualmente hay 3 dispositivos de cómputo principales a los que apuntar con imágenes Docker personalizadas:

- CPU (predeterminado, sin etiqueta específica)
- GPU: CUDA (NVIDIA) (`<image_name>:<version>-cuda`)
- GPU: ROCm (AMD) (`<image_name>:<version>-rocm`)

:::{note}
Si el daemon de despliegue está configurado con el dispositivo de cómputo GPU,
AppAPI intentará descargar primero la imagen Docker con soporte de GPU (`<image_name>:<version>-<cuda|rocm>`, [PR de referencia](https://github.com/nextcloud/app_api/pull/340)).
Si no encuentra la imagen, AppAPI intentará descargar la imagen base (CPU) (`<image_name>:<version>`).
:::

#### Dockerfile

El Dockerfile es necesario para compilar la imagen Docker de la ExApp.
Las pautas para escribir el Dockerfile se encuentran en las [buenas prácticas para Dockerfile](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/).

Recomendaciones breves:

1. Mantener el Dockerfile lo más pequeño posible.
2. Usar imágenes base mínimas para que el tamaño de la imagen sea pequeño.
3. Colocar las instrucciones que cambian con poca frecuencia al principio del Dockerfile para aprovechar el mecanismo de caché de Docker.

#### Registros

Los registros del contenedor Docker se muestran en los flujos de salida estándar y de error estándar.
Para que quien administra pueda ver los registros importantes del contenedor de la ExApp,
conviene considerar redirigir los registros a los flujos de salida estándar y de error estándar.
Para más información, ver [la documentación oficial sobre registros](https://docs.docker.com/config/containers/logging/).

### 5. Publicación en la AppStore

Una vez que la ExApp esté lista y la imagen Docker esté disponible en el registro de Docker,
se puede seguir [el proceso de publicación en la AppStore](https://nextcloudappstore.readthedocs.io/en/latest/developer.html).
Es el mismo que para una app normal de Nextcloud, pero con el requisito de {nc-ref}`los campos específicos de ExApp <ex_app_info_xml_metadata>` en el archivo `appinfo/info.xml`.

### 6. Pruebas

Es importante asegurarse de que la ExApp funcione como se espera.
Se recomienda tener distintos tipos de configuraciones de desarrollo para probarlas todas.
Aunque el desarrollo principal se hace en local mediante `manual_install`, también hay que asegurarse de que
la ExApp funcione correctamente en un contenedor Docker con Docker Socket Proxy (HTTP y HTTPS).
````
