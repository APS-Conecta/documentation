---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Context Chat: requisitos, instalación de sus dos apps, indexación, escalado, comandos occ, opciones, registros, solución de problemas y limitaciones."
---
# App: Context Chat

## Resumen

Esta página describe, para quienes administran el servidor, Context Chat, la función del asistente que responde sobre los documentos y datos propios: sus requisitos, la instalación de sus dos apps, la carga inicial de datos, el escalado, los comandos `occ`, las opciones de configuración, los registros, la solución de problemas y sus limitaciones. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/app_context_chat.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

(nc-ai-app-context_chat)=
Context Chat es una función del {nc-ref}`asistente <ai-app-assistant>` que se implementa mediante un conjunto de dos apps:

- la app `context_chat`, escrita íntegramente en PHP
- la ExternalApp `context_chat_backend`, escrita en Python

Juntas aportan las tareas de *procesamiento de texto* y de *búsqueda* de ContextChat, accesibles desde la {nc-ref}`app Asistente de Nextcloud <ai-app-assistant>`.

Las apps `context_chat` y `context_chat_backend` usan el proveedor de procesamiento de tareas de texto a texto configurado, que es obligatorio en una instalación nueva. Puede configurarse para ejecutar modelos de código abierto íntegramente en las instalaciones propias; la lista de proveedores está {nc-ref}`aquí <tp-consumer-apps>`, en la sección «Apps de backend».

Esta app admite entradas y salidas en los mismos idiomas que admite el proveedor de procesamiento de tareas de texto a texto configurado en ese momento.

### Requisitos

- Versión mínima de Nextcloud: 32
- Nextcloud AIO es compatible
- Actualmente se admiten GPU NVIDIA, GPU AMD (mediante Vulkan) y CPU x86_64
- CPU compatible con las instrucciones AVX y AVX2
- CUDA >= v12.8 en el sistema anfitrión si se usan GPU NVIDIA
- Se admiten tanto podman como docker
- Dimensionamiento con GPU

   - Una GPU con al menos 2GB de VRAM
      - Los requisitos de los proveedores de texto a texto deben comprobarse por separado para cada app {nc-ref}`aquí <tp-consumer-apps>`, en la sección «Apps de backend», ya que pueden variar mucho según el modelo usado y según si el proveedor está alojado local o remotamente.
   - Al menos 8GB de RAM del sistema
      - 2 GB + 500MB adicionales por cada solicitud simultánea al backend si se cambian los parámetros de configuración

- Dimensionamiento con CPU

   - Al menos 12GB de RAM del sistema
      - 2 GB + 500MB adicionales por cada solicitud de consulta simultánea adicional
      - En el caso anterior se recomiendan 8 GB con los ajustes predeterminados
   - De forma predeterminada, esta app usa el proveedor de procesamiento de tareas de texto a texto configurado en lugar de ejecutar su propio modelo de lenguaje, por lo que se necesitan 4 o más núcleos para el modelo de embeddings

- Se recomienda una máquina dedicada

#### Uso de espacio

Esta app usa una base de datos incluida con soporte vectorial llamada [PostgreSQL](https://www.postgresql.org/). Todos los datos textuales de los usuarios se duplican, se dividen en fragmentos y se almacenan en disco en esta base de datos vectorial, junto con vectores de embeddings semánticos del contenido.

### Instalación

1. Asegurarse de que esté instalada la {nc-ref}`app Asistente de Nextcloud <ai-app-assistant>`
2. Configurar un {nc-ref}`Deploy Daemon <ai-app_api>` en las configuraciones de administración de AppAPI
3. Instalar la ExApp `context_chat_backend` desde la página «Apps» de Nextcloud o ejecutando lo siguiente (los pasos de instalación manual están en el readme de <https://github.com/nextcloud/context_chat_backend>)

   ```
   occ app_api:app:register context_chat_backend
   ```

4. Instalar la app `context_chat` desde la página «Apps» de Nextcloud o ejecutando

   ```
   occ app:enable context_chat
   ```

5. Instalar un proveedor de texto a texto (proveedor de generación de texto) desde la página «Apps» de Nextcloud. Hay una lista de proveedores {nc-ref}`aquí <tp-consumer-apps>`, en la sección «Apps de backend».

6. De forma opcional, aunque recomendada, configurar workers en segundo plano para que las tareas se recojan más rápido. Hay más información en {nc-ref}`la sección correspondiente de la visión general de la IA <ai-overview_improve-ai-task-pickup-speed>`.

:::{note}
Ambas apps deben estar instaladas, y tanto la versión mayor como la versión menor de las dos apps deben coincidir para que la funcionalidad funcione (es decir, «v1.3.4» y «v1.3.1» sí; pero no «v1.3.4» y «v2.1.6», ni «v1.3.4» y «v1.4.5»). Tenerlo en cuenta al actualizar.
:::

### Carga inicial de datos

#### Indexación automática

Context Chat carga automáticamente los datos de los usuarios en la base de datos vectorial. El backend de Context Chat toma de la app PHP de Context Chat los archivos en cola y los elementos de los proveedores de contenido, y los indexa.\
La carga inicial de datos puede tardar mucho, según el número de archivos y su tamaño.

(nc-scaling-context-chat)=
### Escalado

A continuación se enumeran las partes principales del sistema que pueden escalarse de forma independiente para mejorar el rendimiento:

1. El proveedor de procesamiento de tareas de texto a texto (de la lista de proveedores {nc-ref}`aquí <tp-consumer-apps>`, en la sección «Apps de backend»)

   El proveedor de procesamiento de tareas de texto a texto puede escalarse usando un servicio alojado mediante la [integración con OpenAI y LocalAI (mediante la API de OpenAI)](https://apps.nextcloud.com/apps/integration_openai), como OpenAI, o alojando un modelo propio en hardware potente.

2. El rendimiento de la base de datos vectorial

   El rendimiento de la base de datos vectorial puede escalarse con una instalación dedicada o en clúster de PostgreSQL con la extensión pgvector.\
   La cadena de conexión de la base de datos vectorial externa puede fijarse con la variable de entorno `EXTERNAL_DB` durante el despliegue, en «Opciones del despliegue».

3. El rendimiento del modelo de embeddings

   El rendimiento del modelo de embeddings puede escalarse usando un servicio de embeddings alojado, local o remotamente. Debe poder servir una API compatible con OpenAI.\
   La URL del servicio de embeddings puede fijarse con la variable de entorno `CC_EM_BASE_URL` durante el despliegue, en «Opciones del despliegue». Otras opciones, como el nombre del modelo, la clave de API o el nombre de usuario y la contraseña, pueden fijarse con las variables de entorno `CC_EM_MODEL_NAME`, `CC_EM_APIKEY`, `CC_EM_USERNAME` y `CC_EM_PASSWORD`, respectivamente.

   :::{warning}
   El modelo de embeddings no puede cambiarse después de instalar la app. Para usar otro modelo o servicio de embeddings,
   hay que desinstalar la app por completo (eliminando todos los datos de la ExApp) y volver a instalar la ExApp `context_chat_backend`
   con las nuevas variables de entorno y una base de datos vectorial vacía. Si la base de datos vectorial es externa, la base de datos conectada
   (que puede llamarse `ccb`) debe eliminarse antes de volver a instalar la ExApp.

   Para la app `context_chat`, partir de cero eliminando todas las tablas `<PREFIX>_context_chat_*` de la base de datos y eliminando todos los valores de configuración: y volviéndola a instalar.

   ```sql
   drop table if exists oc_context_chat_action_queue;
   drop table if exists oc_context_chat_content_queue;
   drop table if exists oc_context_chat_fs_events;
   drop table if exists oc_context_chat_queue;
   delete from oc_appconfig where appid = 'context_chat';
   ```
   :::

4. El análisis de los documentos para extraer el texto

   El análisis de los documentos para extraer el texto se realiza en una única instancia de la ExApp `context_chat_backend`, en un entorno basado en docker. Es una tarea limitada por la CPU, así que una CPU potente ayuda a acelerar el análisis.\
   Puede escalarse usando Kubernetes para el despliegue, lo que permite que varias instancias de la ExApp `context_chat_backend` se encarguen del análisis de forma simultánea; consultar {nc-ref}`la sección de Kubernetes <kubernetes-context-chat>`.

Si `context_chat_backend` ya está desplegada, estas variables de entorno pueden cambiarse volviéndola a desplegar con los nuevos valores.

1. Ir a la página «Apps» → buscar «Context Chat Backend»
2. Desactivar y eliminar la app procurando que no se eliminen los datos (salvo cuando se cambia el modelo de embeddings, en cuyo caso los datos deben eliminarse)
3. Fijar las «Opciones del despliegue» con las nuevas variables de entorno
4. Volver a instalar la app

(nc-kubernetes-context-chat)=
#### Kubernetes

A partir de la versión 5.4.0 de la app y de Nextcloud 34, se admite Kubernetes para desplegar el backend y escalar ContextChat a instancias grandes. Los clientes de {vendor}`Nextcloud` encontrarán los detalles sobre el despliegue con Kubernetes en la documentación para clientes o contactando con el soporte.

### Tienda de apps

La app `context_chat` también está en la tienda de apps de {vendor}`Nextcloud`, donde puede escribirse una reseña: <https://apps.nextcloud.com/apps/context_chat>

### Repositorio

Los repositorios de código de las apps están en GitHub, donde pueden informarse errores y aportarse correcciones y funciones: <https://github.com/nextcloud/context_chat> y <https://github.com/nextcloud/context_chat_backend>

Los clientes de {vendor}`Nextcloud` deben informar de los errores directamente al soporte al cliente de {vendor}`Nextcloud`.

### Comandos (OCC)

Las opciones de cada comando pueden consultarse así, con scan como ejemplo: `context_chat:scan --help`

- `context_chat:prompt`: Hacer una pregunta sobre los datos propios, con opciones para un contexto selectivo.

- `context_chat:search`: Realizar una búsqueda semántica (basada en la base de datos vectorial) en los documentos indexados, con opciones para un contexto selectivo.

- `context_chat:stats`: Muestra el tiempo que tardó en completarse la indexación inicial de los documentos, si ha terminado,\
  y el número actual de elementos en el indexador y en la cola de acciones.\
  «Acciones» se refiere a tareas como eliminaciones de archivos, cambios de propietario debidos a cambios en los recursos compartidos, etc.\
  Estos cambios de archivos y de propietario se sincronizan con el backend a través de esta cola de acciones.

- `context_chat:reindex`: Programar un rastreo completo de todos los archivos de todos los montajes. Los archivos indexados no se vuelven a indexar cuando se comparan con la base de datos vectorial de context_chat_backend.\
  Los proveedores de contenido no se vuelven a indexar.

### Opciones de configuración

- `auto_indexing` cadena (valor predeterminado: 'true'): Para permitir o impedir que IndexerJob se ejecute en segundo plano. Normalmente no hace falta configurarla.

```
occ config:app:set context_chat auto_indexing --value='true' --type=string
```

Las opciones de configuración del backend de Context Chat están disponibles mediante las variables de entorno de las {nc-ref}`Opciones del despliegue <ai-app_api_deploy_options>`.

### Registros

Los registros de la app PHP `context_chat` y de la ExApp `context_chat_backend` pueden consultarse en las configuraciones de administración de la interfaz gráfica de Nextcloud, así como en el archivo de registro de Context Chat, que suele estar en el directorio de datos de Nextcloud. El archivo de registro se llama `context_chat.log`.

Los registros internos de la base de datos vectorial PostgreSQL (en instalaciones sin Kubernetes) se encuentran dentro del contenedor de docker en `/nc_app_context_chat_backend_data/vector_db_data/pgsql/logfile`. Pueden copiarse al anfitrión con `docker cp nc_app_context_chat_backend:/nc_app_context_chat_backend_data/vector_db_data/pgsql/logfile /tmp/vectordb-logfile`.\
Puede ser necesario cuando la configuración automática de la base de datos vectorial falla con algo como: «pg_ctl: could not start server».

Al ejecutarse en Kubernetes, los registros del backend están en los registros del pod correspondiente, a los que se accede con el comando `kubectl logs <pod_name>`.

### Solución de problemas

1. Si el contenedor de docker parece reiniciarse de repente durante la indexación o las consultas, puede deberse a que se llena la RAM o el almacenamiento, o a que AVX no está disponible en el sistema. AVX puede comprobarse con el comando `grep -i avx /proc/cpuinfo` en el sistema anfitrión. Si AVX no está disponible, la app no funcionará.
2. Buscar problemas en los registros de diagnóstico, en los registros del servidor y en los registros del contenedor de docker `nc_app_context_chat_container`. En caso de duda, abrir una incidencia en cualquiera de los dos repositorios.
3. Consultar «Configuraciones de administración → Context Chat» para ver estadísticas e información sobre el proceso de indexación.

### Reglas de control de acceso a archivos no admitidas

En Nextcloud pueden configurarse reglas de control de acceso a archivos con la app [files_accesscontrol](https://apps.nextcloud.com/apps/files_accesscontrol) para restringir el acceso a determinados archivos.

Context Chat **no** respeta estas reglas.

Por tanto, es posible que usuarios a los que se ha denegado el acceso a un documento mediante la app files_accesscontrol obtengan acceso a él a través de Context Chat
si el documento es visible en la app Archivos para el usuario en cuestión.

### Limitaciones conocidas

- Los modelos de lenguaje tienden a generar información falsa, por lo que solo deben usarse en situaciones que no sean críticas. Se recomienda usar la IA solo al principio de un proceso de creación y no al final, de modo que sus resultados sirvan, por ejemplo, como borrador y no como producto final. Revisar siempre los resultados de los modelos de lenguaje antes de usarlos y asegurarse de que cumplen los requisitos de calidad del caso de uso.
- El soporte al cliente está disponible previa solicitud; sin embargo, {vendor}`Nextcloud` no puede resolver resultados falsos o problemáticos, la mayoría de los problemas de rendimiento ni otros problemas causados por el modelo subyacente. Por tanto, el soporte se limita a los errores causados directamente por la implementación de la app (conectores, API, front-end, AppAPI).
- No se admiten archivos de más de 100MB
- No se admiten los PDF ni ningún otro archivo protegidos con contraseña. Cuando se encuentren estos archivos, aparecerán en el contenedor de docker registros de error que mencionan criptografía y AES, pero no hay de qué preocuparse: simplemente se ignorarán y el sistema seguirá funcionando con normalidad.
- Los almacenamientos externos (mediante `files_external`) pueden no funcionar tan bien como el almacenamiento local.
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
