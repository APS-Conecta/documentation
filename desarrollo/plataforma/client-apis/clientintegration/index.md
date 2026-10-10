---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API de integración de clientes: cómo una app de servidor añade acciones al menú contextual de archivos y carpetas en los clientes de escritorio y móviles."
---
(nc-dev-clientintegrationindex)=
# Integración de clientes

## Resumen

Esta página describe, para quienes desarrollan apps de servidor, la API de integración de clientes: cómo exponer acciones en el menú contextual de archivos y carpetas de los clientes de escritorio y móviles mediante capacidades, qué forma tienen los endpoints y las respuestas, y cómo crear una primera app que la use.

````{upstream} developer_manual/client_apis/ClientIntegration/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Con Nextcloud Hub 26 Winter se introduce una nueva API de integración de clientes. Permite que las apps del lado del servidor expongan integraciones en escritorio y en móviles. Por ahora se admite añadir acciones definidas por la app a un «menú contextual» de archivos y carpetas.

Permite integrar fácilmente acciones específicas en los clientes sin necesidad de escribir ni mantener código en esas plataformas.

### Clientes compatibles

Android: 3.36.0 y posteriores

Escritorio: 33.0.0 y posteriores

iOS: 7.3.0 y posteriores

### Apps de servidor compatibles

richdocuments: convertir .docx a .md

assistant: transcribir un archivo de audio

files_zip: comprimir en zip un archivo o una carpeta

contacts: crear un contacto nuevo a partir de un vcf

### Exponer acciones mediante capacidades

Cada app puede añadir acciones nuevas mediante capacidades, siguiendo la sintaxis «app-id», «hook-name» y la lista de todos los endpoints.

```php
'client_integration' => [
    Application::APP_ID => [
        'version' => 0.1,
        'context-menu' => [
            // ... endpoints ...
        ]
    ]
]
```

### Ganchos

Actualmente solo se admite «context-menu».

(nc-dev-endpoint-section)=
### Endpoint

El endpoint indica al cliente qué aspecto debe tener la entrada del menú y cómo puede el cliente enviar una solicitud al servidor.

Requisitos:

- Todo texto debe traducirlo la propia app.
- Los parámetros predefinidos actuales son `fileId` y `filePath`,
- los clientes reemplazarán `{fileId}` y `{filePath}` por los valores reales,
- los marcadores de posición de `url` siempre se reemplazan,
- `mimetype_filters` es una lista de filtros separados por comas (coincide con todo lo que empiece por el filtro). Si no hay ningún filtro, la acción se muestra para cada archivo o carpeta.
- Todas las `urls` deben ser relativas.
- `params` se usa para los parámetros del cuerpo (actualmente solo con POST).
- El campo `icon` debe proporcionar siempre un SVG.
- `method` admite POST/GET.

```javascript
[
    'name' => 'translated title',
    'url' => '/ocs/v2.php/apps/abc',
    'method' => 'POST/GET',
    'mimetype_filters' => 'text/, application/pdf', // will match text/* and PDFs
    'params' => ['file_id' => '{fileId}','file_path' => '{filePath}'], // only for POST; the key can vary depending on the app
    'icon' => '/apps/abc/img/app.svg'
],
```

### Respuestas

Al pulsar una entrada del menú, el cliente envía una solicitud predefinida al servidor. La app en cuestión puede entonces gestionar la solicitud y enviar dos tipos de respuesta distintos:

#### Respuesta de IU declarativa

La respuesta de IU declarativa permite a la app devolver una nueva IU para que el cliente la represente:
- version: indica de qué versión se trata. Los clientes serán retrocompatibles. Si el servidor envía una versión más reciente de la que el cliente puede entender, la respuesta se ignorará.
- tooltip: texto traducido, que se mostrará como tooltip / snackbar.

```javascript
{
  "ocs": {
    "meta": {
      "status": "ok",
      "statuscode": 200,
      "message": "OK"
    },
    "data": {
      "version": 0.1,
      "root": {
        "orientation": "vertical",
        "rows": [
          {
            "children": [
              {
                "element": "URL",
                "text": "Link created",
                "url": "/some/link/to/a/page"
              }
            ]
          }
        ]
      }
    }
  }
}
```

Por ahora solo se admiten filas con elementos de texto y url, pero en el futuro se añadirán más elementos y opciones.

#### Respuesta de tooltip

La respuesta de tooltip es un tipo DataResponse normal, con esta carga útil:
- version: indica de qué versión se trata. Los clientes serán retrocompatibles. Si el servidor envía una versión más reciente de la que el cliente puede entender, la respuesta se ignorará.
- tooltip: texto traducido, que se mostrará como tooltip / snackbar.

```javascript
{
  "ocs": {
    "meta": {
      "status": "ok",
      "statuscode": 200,
      "message": "OK"
    },
    "data": {
      "version": "0.1",
      "tooltip": "Task submitted successfully"
    }
  }
}
```

### Ejemplo

Este es un ejemplo de uso de la app Assistant.

**Capacidades:**

*ocs/v1.php/cloud/capabilities* devuelve la siguiente capacidad:

```javascript
"client_integration": {
  "assistant": {
    "version": 0.1,
    "context-menu": [
      {
        "name": "Summarize using AI",
        "url": "/ocs/v2.php/apps/assistant/api/v1/file-action/{fileId}/core:text2text:summary",
        "method": "POST",
        "mimetype_filters": "text/, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/vnd.oasis.opendocument.text, application/pdf",
        "icon": "/apps/assistant/img/client_integration/summarize.svg"
      },
      {
        "name": "Transcribe audio using AI",
        "url": "/ocs/v2.php/apps/assistant/api/v1/file-action/{fileId}/core:audio2text",
        "method": "POST",
        "mimetype_filters": "audio/",
        "icon": "/apps/assistant/img/client_integration/speech_to_text.svg"
      },
      {
        "name": "Text-To-Speech using AI",
        "url": "/ocs/v2.php/apps/assistant/api/v1/file-action/{fileId}/core:text2speech",
        "method": "POST",
        "mimetype_filters": "text/, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/vnd.oasis.opendocument.text, application/pdf",
        "icon": "/apps/assistant/img/client_integration/text_to_speech.svg"
      }
    ]
  },
},
```

La integración de Assistant tiene algunos endpoints que el cliente muestra y ejecuta. «Summarize using AI» y «Text-To-Speech using AI» aparecen al final de cada menú en el lado del cliente.

Si se observa la acción «Summarize using AI», solo se mostrará para archivos cuyo tipo MIME empiece por «text/» o para los tipos MIME de documento y PDF indicados, tal como se describe en *mimetype_filters*. Al pulsar la acción, el cliente enviará una solicitud POST a la URL indicada, reemplazando {fileId} por el ID real del archivo. La app puede entonces gestionar la solicitud y, por ejemplo, devolver al cliente una respuesta de tooltip. El cliente mostrará el tooltip al usuario:

```javascript
{
    "ocs": {
        "meta": {
            "status": "ok",
            "statuscode": 200,
            "message": "OK"
        },
        "data": {
            "version": 0.1,
            "tooltip": "Summarization task submitted successfully"
        }
    }
}
```

### Desarrollar la primera app con integración de clientes

1. Familiarizarse con cómo crear una app mediante [Desarrollar la primera app Hello World](https://cloud.nextcloud.com/s/iyNGp8ryWxc7Efa?dir=%2F%2F2%20Develop%20your%20first%20Hello%20World%20app) para obtener más ayuda sobre ese tema:

2. Crear `Capabilities.php` en la carpeta `/lib` y añadir al array de `getCapabilities()`:

   ```php
   'client_integration' => [
                   'pingpong' => [
                       'version' => 0.1,
                       'context-menu' => [
                           [
                               'name' => $this->l10n->t('Ping'),
                               'url' => '/ocs/v2.php/apps/pingpong/ping/{fileId}',
                               'method' => 'GET',
                           ],
                       ],
                   ],
               ],
   ```

Consultar {nc-ref}`endpoint-section` para los detalles del endpoint.

3. Registrar la app en `lib/AppInfo/Application.php`

   ```php
   public function register(IRegistrationContext $context): void {
       $context->registerCapability(Capabilities::class);
   }
   ```

4. Añadir la función consumidora en `/lib/Controller/ApiController.php`:

   ```php
   #[NoAdminRequired]
   #[ApiRoute(verb: 'GET', url: '/ping/{fileId}')]
   public function ping(int $fileId = 1): DataResponse {
       return new DataResponse(
           ['version' => 0.1,
               'tooltip' => $this->l10n->t("Pong file %s", $fileId)]
       );
   }
   ```

5. La respuesta es un `DataResponse` con una versión (actualmente 0.1) y un tooltip traducido.

### Incidencias/errores

Se ruega informar de los problemas, errores o solicitudes de funcionalidades en <https://github.com/nextcloud/files-clients> con la etiqueta «Client integration».
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
