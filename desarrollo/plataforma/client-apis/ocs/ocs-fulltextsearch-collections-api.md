---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de colecciones de FullTextSearch: preparar una colección con occ e indexar el contenido en un motor de búsqueda externo."
---
# API OCS de colecciones de FullTextSearch

## Resumen

Esta página explica, para quienes integran un motor de búsqueda externo, cómo preparar una colección de FullTextSearch con occ y usar su API OCS para obtener, indexar y confirmar los documentos pendientes.

````{upstream} developer_manual/client_apis/OCS/ocs-fulltextsearch-collections-api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

:::{versionadded} 27
:::

FullTextSearch incluye una API OCS para indexar el contenido de Nextcloud en un motor de búsqueda externo.

### Visión general del concepto

Como la estructura propia podría alojar ya su propio motor de búsqueda, las apps de FullTextSearch ofrecen una API OCS que ayuda a indexar el contenido de los usuarios y a mantener un índice actualizado.
La API OCS permitirá que el script:

- devuelva una lista de documentos de Nextcloud no indexados o actualizados recientemente,
- extraiga el contenido de los documentos,
- actualice el índice interno una vez que un documento se ha indexado en el motor de búsqueda externo,

### Primeros pasos

#### Instalar las apps

Además de la app *fulltextsearch*, en Nextcloud debe instalarse al menos un proveedor de contenido; es decir, deben instalarse como mínimo 2 apps antes de usar esta función:

```console
$ ./occ app:enable fulltextsearch files_fulltextsearch
```

#### Inicializar la colección

Con *occ*, crear una nueva colección que se usará para sincronizar el contenido indexado en el motor de búsqueda externo con el contenido actual de Nextcloud.

```console
$ ./occ fulltextsearch:collection:init test
```

:::{note}
*test* será el nombre de la colección que se usa en todos los ejemplos de esta página.
:::

#### Vincular una colección a una cuenta de usuario

De forma predeterminada, esta API solo puede usarse con una cuenta de administración, pero, por motivos de seguridad, se puede optar por vincular una cuenta que no sea de administración y usar esa cuenta al hacer solicitudes a la API.

```console
$ ./occ fulltextsearch:collection:link test user1
```

:::{warning}
Tener en cuenta que la cuenta vinculada tendrá acceso, a través de la API, al contenido de todos los documentos de todos los usuarios de Nextcloud.
:::

### Usar la API OCS de colecciones

Una vez inicializada la colección, el uso normal de esta API implica que el script:

- haga una solicitud OCS para obtener una lista de documentos que se han creado, modificado y compartido,
- haga solicitudes OCS para obtener el contenido de los documentos de la lista,
- indexe el contenido en el motor de búsqueda y haga una solicitud OCS para confirmarlo,
- vuelva al primer paso hasta que la lista de documentos esté vacía,

#### Obtener la lista de documentos que deben (re)indexarse

El endpoint para obtener esta lista es:

`/ocs/v2.php/apps/fulltextsearch/collection/<collection_name>/index`

```console
$ curl -X GET "https://cloud.example.net/ocs/v2.php/apps/fulltextsearch/collection/test/index?format=json&length=50" -H "OCS-APIRequest: true" -u "admin:password"
{
    "ocs": {
        "meta": {
            "status": "ok",
            "statuscode": 200,
            "message": "OK"
        },
        "data": [
            {
                "url": "https://cloud.example.net/ocs/v2.php/apps/fulltextsearch/collection/test/document/files/597996",
                "status": 28
            }
        ]
    }
}
```

Detalles sobre la respuesta:

- `url` es el enlace al documento,
- `status` es un campo de bits (bitflag) basado en esta lista:
  - *1* => el documento ya se había marcado antes como indexado,
  - *4* => se modificaron los metadatos,
  - *8* => se modificó el contenido,
  - *16* => se modificaron las partes
  - *32* => se eliminó el documento

#### Obtener los datos y metadatos de un documento

El endpoint para obtener los datos de un documento es:

`/ocs/v2.php/apps/fulltextsearch/collection/<collection_name>/document/<provider_id>/<document_id>`

```console
$ curl -X GET "https://cloud.example.net/ocs/v2.php/apps/fulltextsearch/collection/test/document/files/597996?format=json" -H "OCS-APIRequest: true" -u "admin:password"
{
    "ocs": {
        "meta": {
            "status": "ok",
            "statuscode": 200,
            "message": "OK"
        },
        "data": {
            "id": "597996",
            "providerId": "files",
            "access": {
                "ownerId": "user1",
                "users": ['user2', 'user3'],
                "groups": ['group1'],
                "circles": [],
                "links": []
            },
            "index": {
                "ownerId": "user1",
                "providerId": "files",
                "collection": "test",
                "source": "files_local",
                "documentId": "597996",
                "lastIndex": 0,
                "errors": [],
                "errorCount": 0,
                "status": 28,
                "options": []
            },
            "title": "640-240-max.png",
            "link": "https://cloud.example.net/index.php/f/597996",
            "parts": {
                "comments": "<user3> This is a comment !"
            },
            "content": "VGhlIHF1aWNrIGJyb3duIGZveApqdW1wcyBvdmVyCnRoZSBsYXp5IGRvZy4=",
            "isContentEncoded": 1
        }
    }
}
```

:::{note}
Si *isContentEncoded* vale 1, el contenido debe decodificarse
:::

```console
$ php -r "echo base64_decode('VGhlIHF1aWNrIGJyb3duIGZveApqdW1wcyBvdmVyCnRoZSBsYXp5IGRvZy4=');"
The quick brown fox
jumps over
the lazy dog.
```

#### Marcar un documento como indexado

Una vez que un documento se ha indexado en el motor de búsqueda externo, hay que notificar esta acción a FullTextSearch. Esto se hace con una solicitud `POST` a la siguiente ruta:

`/ocs/v2.php/apps/fulltextsearch/collection/<collection_name>/document/<provider_id>/<document_id>/done`

```console
$ curl -X POST "https://cloud.example.net/ocs/v2.php/apps/fulltextsearch/collection/test/document/files/597996/done" -H "OCS-APIRequest: true" -u "admin:password"
{
    "ocs": {
        "meta": {
            "status": "ok",
            "statuscode": 200,
            "message": "OK"
        },
        "data": []
    }
}
```

Una vez marcados como indexados, los documentos solo volverán a la lista de documentos que deben (re)indexarse si se modifican.

#### Restablecer la colección

Si hace falta, hay un endpoint disponible para restablecer todo el índice:

`/ocs/v2.php/apps/fulltextsearch/collection/<collection_name>/index`

```console
$ curl -X DELETE -u "user1:password" "https://cloud.example.net/ocs/v2.php/apps/fulltextsearch/collection/test/index" -H "OCS-APIRequest: true" -k
```
````
