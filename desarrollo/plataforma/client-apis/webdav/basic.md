---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Operaciones WebDAV básicas: autenticación, recursos públicos, propiedades, listar, descargar, subir, mover, copiar, favoritos y cabeceras especiales."
---
(nc-dev-webdavindex)=
# Operaciones básicas con archivos y carpetas

## Resumen

Esta página ofrece, para quienes desarrollan clientes, una visión general de las operaciones WebDAV con archivos y carpetas: la autenticación y el endpoint de los recursos compartidos públicos, cómo probar solicitudes, las propiedades que se pueden solicitar, las operaciones para listar, descargar, subir, crear, eliminar, mover y copiar, los favoritos y las cabeceras especiales de solicitud y de respuesta.

````{upstream} developer_manual/client_apis/WebDAV/basic.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Este documento ofrece una visión general rápida de las operaciones WebDAV que admite Nextcloud. Para que resulte legible, no entra en muchos detalles
de cada operación; se puede encontrar más información sobre cada operación en el RFC correspondiente, cuando corresponda.

### Fundamentos de WebDAV

La URL base de todas las operaciones WebDAV (autenticadas) de una instancia de Nextcloud es {code}`/remote.php/dav`. Para las operaciones con archivos, esto suele
significar rutas bajo {code}`/remote.php/dav/files/{user}/...`.

Todas las solicitudes deben proporcionar información de autenticación, ya sea como una cabecera de autenticación básica o pasando un conjunto de cookies de sesión válidas.

Si la instalación de Nextcloud usa un proveedor de autenticación externo (como un servidor OIDC) o impone políticas como la 2FA, puede ser necesario crear una
contraseña de aplicación para los clientes y scripts WebDAV.
Para ello, ir a los ajustes personales de seguridad y crear una. Esta proporcionará un nombre de usuario y una contraseña que se pueden usar en la cabecera Basic Auth.

#### Recursos compartidos públicos

El endpoint {code}`/remote.php/dav` solo permite el acceso autenticado a los recursos WebDAV;
para los archivos compartidos mediante enlaces públicos se ofrece otro endpoint, que no requiere autenticación.

La URL base de los enlaces públicos compartidos es {code}`/public.php/dav`, en concreto para archivos: {code}`/public.php/dav/files/{share_token}`.
Si el recurso compartido tiene una contraseña, hay que enviar una cabecera de autenticación básica con `anonymous` como nombre de usuario y la contraseña del recurso compartido como contraseña.

:::{note}
Este endpoint para recursos compartidos públicos está disponible desde Nextcloud 29.
:::

:::{warning}
En las solicitudes que no son GET (p. ej., PROPFIND, PUT) a `/public.php/dav`, la solicitud debe incluir la cabecera
`X-Requested-With: XMLHttpRequest`, salvo que el uso compartido saliente de servidor a servidor esté habilitado en la instancia.
Sin esta cabecera, el servidor rechazará la solicitud con una respuesta `401 Not Authenticated`.
:::

### Probar solicitudes

#### Con curl

Todas las solicitudes WebDAV se pueden probar fácilmente con {code}`curl`, especificando el método de la solicitud ({code}`GET`, {code}`PROPFIND`, {code}`PUT`, ...) y proporcionando un cuerpo de solicitud cuando sea necesario.

Por ejemplo, se puede realizar una solicitud {code}`PROPFIND` para encontrar los archivos de una carpeta con:

```bash
curl 'https://cloud.example.com/remote.php/dav/files/username/folder' \
  --user username:password \
  --request PROPFIND \
  --data '<?xml version="1.0" encoding="UTF-8"?>
    <d:propfind xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
      <d:prop>
        <d:getlastmodified/>
        <d:getcontentlength/>
        <d:getcontenttype/>
        <oc:permissions/>
        <d:resourcetype/>
        <d:getetag/>
      </d:prop>
    </d:propfind>'
```

#### Realizar solicitudes en JavaScript

Este es un ejemplo de código JavaScript para empezar:

```javascript
import { createClient } from 'webdav'
import { generateRemoteUrl } from '@nextcloud/router'
import { getCurrentUser } from '@nextcloud/auth'

const client = createClient(generateRemoteUrl('dav'))
const response = await client.getDirectoryContents(`/files/${getCurrentUser()?.uid}/folder`, {
    details: true,
    data: `<?xml version="1.0" encoding="UTF-8"?>
        <d:propfind xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
            <d:prop>
                <d:getlastmodified/>
                <d:getcontentlength/>
                <d:getcontenttype/>
                <oc:permissions/>
                <d:resourcetype/>
                <d:getetag/>
            </d:prop>
        </d:propfind>`,
})
```

### Referencia rápida de métodos y cabeceras

La tabla siguiente resume los métodos WebDAV habituales que usa Nextcloud y las cabeceras más relevantes.

| Método | Endpoint típico | Cabeceras de solicitud importantes | Notas |
|---|---|---|---|
| PROPFIND | `/remote.php/dav/files/{user}/path` | `Depth: 0` (solo las propiedades del nodo) | Sin `Depth: 0`, los listados de carpetas incluyen las entradas hijas. |
| REPORT | `/remote.php/dav/files/{user}/path` | (ninguna obligatoria) | Se usa para consultas filtradas, como los favoritos. |
| GET (archivo) | `/remote.php/dav/files/{user}/file` | (ninguna obligatoria) | Descarga el contenido del archivo. |
| GET (directorio) | `/remote.php/dav/files/{user}/folder` | `Accept: application/zip` o `Accept: application/x-tar` | Extensión de Nextcloud para descargar una carpeta como archivo comprimido. |
| PUT | `/remote.php/dav/files/{user}/file` | Opcionales: `X-OC-MTime`, `X-OC-CTime`, `OC-Checksum`, `OC-Total-Length`, `X-NC-WebDAV-AutoMkcol` | Sube o sobrescribe el contenido del archivo. |
| MKCOL | `/remote.php/dav/files/{user}/folder` | (ninguna obligatoria) | Crea una carpeta. |
| DELETE | `/remote.php/dav/files/{user}/path` | (ninguna obligatoria) | La eliminación de una carpeta es recursiva. |
| MOVE | `/remote.php/dav/files/{user}/path` | `Destination: <full URL>` | Opcional: `Overwrite: T` (predeterminado) o `Overwrite: F`. |
| COPY | `/remote.php/dav/files/{user}/path` | `Destination: <full URL>` | Opcional: `Overwrite: T` (predeterminado) o `Overwrite: F`. |
| PROPPATCH | `/remote.php/dav/files/{user}/path` | (ninguna obligatoria) | Establece propiedades como `oc:favorite`. |

### Solicitar propiedades

De forma predeterminada, una solicitud {code}`PROPFIND` solo devuelve un pequeño número de propiedades de cada archivo: la fecha de última modificación, el tamaño del archivo, si es una carpeta, el etag y el tipo MIME.

Se pueden solicitar propiedades adicionales enviando con la solicitud {code}`PROPFIND` un cuerpo que liste todas las propiedades solicitadas.
Si una propiedad no se admite para un recurso, el servidor la indicará como no encontrada en la respuesta multi-status para esa propiedad.

```xml
<?xml version="1.0"?>
<d:propfind xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
  <d:prop>
    <d:getlastmodified />
    <d:getetag />
    <d:getcontenttype />
    <d:resourcetype />
    <oc:fileid />
    <oc:permissions />
    <oc:size />
    <d:getcontentlength />
    <nc:has-preview />
    <oc:favorite />
    <oc:comments-unread />
    <oc:owner-display-name />
    <oc:share-types />
    <nc:contained-folder-count />
    <nc:contained-file-count />
  </d:prop>
</d:propfind>
```

#### Una nota sobre los URI de espacio de nombres

Al construir el cuerpo de la solicitud DAV, se solicitan propiedades que están disponibles bajo URI de espacio de nombres específicos.
Es habitual declarar prefijos para esos espacios de nombres en el elemento `d:propfind` del cuerpo.

Esta es la lista de espacios de nombres disponibles:

| URI | Prefijo |
|---|---|
| DAV: | d |
| <http://owncloud.org/ns> | oc |
| <http://nextcloud.org/ns> | nc |
| <http://open-collaboration-services.org/ns> | ocs |
| <http://open-cloud-mesh.org/ns> | ocm |

Y así es como debería verse en la solicitud DAV:

```xml
<?xml version="1.0"?>
<d:propfind
    xmlns:d="DAV:"
    xmlns:oc="http://owncloud.org/ns"
    xmlns:nc="http://nextcloud.org/ns"
    xmlns:ocs="http://open-collaboration-services.org/ns"
    xmlns:ocm="http://open-cloud-mesh.org/ns">
    ...
</d:propfind>
```

#### Propiedades admitidas

:::{note}
Las propiedades del espacio de nombres `d:` son propiedades WebDAV estándar (RFC 4918).
La mayoría de las propiedades de `oc:`, `nc:`, `ocs:` y `ocm:` son extensiones propias de Nextcloud.
:::

:::{list-table}
:header-rows: 1
:widths: 25 35 40

* - Propiedad
  - Descripción
  - Ejemplo
* - \<d:creationdate />
  - La fecha de creación del nodo.
  - `1970-01-01T00:00:00+00:00`
* - \<d:getlastmodified />
  - La hora de la última modificación.
  - `Wed, 20 Jul 2022 05:12:23 GMT`
* - \<d:getetag />
  - El etag del archivo.
  - `&quot;6436d084d4805&quot;`
* - \<d:getcontenttype />
  - El tipo MIME del archivo.
  - `image/jpeg`
* - \<d:resourcetype />
  - Especifica la naturaleza del recurso.
  - `<d:collection />` para una carpeta
* - \<d:getcontentlength />
  - El tamaño en bytes, si es un archivo.
  - `3030237`
* - \<d:getcontentlanguage />
  - El idioma del contenido.
  - `en`
* - \<d:displayname />
  - Un nombre adecuado para mostrar.
  - `File name`
* - \<d:lockdiscovery />
  - Endpoint ficticio para la compatibilidad con WebDAV de clase 2. Debería devolver la lista de bloqueos, pero siempre devuelve una respuesta vacía.
  - `<d:lockdiscovery />`
* - \<d:quota-available-bytes />
  - Cantidad de bytes disponibles en la carpeta.
  - - `3950773`
    - `-1` Espacio libre no calculado.
    - `-2` Espacio libre desconocido.
    - `-3` Espacio libre ilimitado.
* - \<d:quota-used-bytes />
  - Cantidad de bytes usados en la carpeta.
  - `3950773`
* - \<d:supportedlock />
  - Endpoint ficticio para la compatibilidad con WebDAV de clase 2. Siempre proporciona las mismas capacidades de bloqueo.
  -
    ```xml
    <d:lockentry>
      <d:lockscope><d:exclusive /></d:lockscope>
      <d:locktype><d:write /></d:locktype></d:lockentry>
    </d:lockentry>
    ```

    ```xml
    <d:lockentry>
      <d:lockscope><d:shared /></d:lockscope>
      <d:locktype><d:write /></d:locktype></d:lockentry>
    </d:lockentry>
    ```
* - \<oc:id />
  - El fileid, con el ID de la instancia como espacio de nombres. Único globalmente.
  - `00000007oc9l3j5ur4db`
* - \<oc:fileid />
  - El ID único del archivo dentro de la instancia.
  - `7`
* - \<oc:downloadURL />
  - Una URL para descargar el archivo directamente desde un almacenamiento. Ningún almacenamiento lo implementa todavía.
  -
* - \<oc:permissions />
  - Los permisos que tiene el usuario sobre el archivo o la carpeta. El valor es una cadena que contiene letras para todos los permisos disponibles. En los recursos compartidos públicos, `S` y `M` se eliminan del valor devuelto.
  - - `S`: Compartido
    - `R`: Se puede compartir
    - `M`: Montado
    - `G`: Legible
    - `D`: Se puede eliminar
    - `N`: Se puede renombrar
    - `V`: Se puede mover
    - `W`: Escribible (archivo)
    - `C`: Se puede crear (crear un archivo nuevo dentro de la carpeta)
    - `K`: Se puede crear (crear una carpeta nueva dentro de la carpeta)
* - \<nc:creation_time />
  - Igual que `creationdate`, pero como marca de tiempo.
  - `1675789581`
* - \<nc:mount-type />
  - El tipo de montaje.
  - - `''` = local
    - `'shared'` = recurso compartido recibido
    - `'group'` = carpeta de grupo
    - `'external'` = almacenamiento externo
    - `'external-session'` = almacenamiento externo
* - \<nc:hide-download />
  - En los recursos compartidos, indica si se debe ocultar o no cualquier acción de descarga.
  - `true` o `false`
* - \<nc:is-encrypted />
  - Si la carpeta está cifrada de extremo a extremo.
  - - `0` para `false`
    - `1` para `true`
* - \<nc:is-mount-root />
  - Es una propiedad especial que se usa para determinar si un nodo es una raíz de montaje o no, p. ej., una carpeta compartida. Si lo es, el nodo solo se puede dejar de compartir, no eliminar.
  - `true` o `false`
* - \<oc:tags />
  - Lista de etiquetas especificadas por el usuario.
  - `<oc:tag>test</oc:tag>`
* - \<oc:favorite />
  - El estado de favorito.
  - - `0` si no es favorito
    - `1` si es favorito
* - \<oc:comments-href />
  - El endpoint DAV para obtener los comentarios.
  - `/remote.php/dav/comments/files/{fileId}`
* - \<oc:comments-count />
  - El número de comentarios.
  - `2`
* - \<oc:comments-unread />
  - El número de comentarios no leídos.
  - `0`
* - \<oc:owner-id />
  - El ID de usuario del propietario de un archivo compartido.
  - `alice`
* - \<oc:owner-display-name />
  - El nombre visible del propietario de un archivo compartido.
  - `Alice`
* - \<oc:share-types />
  - Array XML de tipos de recurso compartido.
  - - `<oc:share-type>{shareTypeId}</oc:share-type>`
    - `0` = Usuario
    - `1` = Grupo
    - `3` = Enlace público
    - `4` = Correo electrónico
    - `6` = Recurso compartido de nube federada
    - `7` = Círculo
    - `8` = Invitado
    - `9` = Grupo remoto
    - `10` = Conversación de Talk
    - `12` = Deck
    - `15` = Science mesh
* - \<ocs:share-permissions />
  - Los permisos que tiene el usuario sobre el recurso compartido.
  - - `1` = Leer
    - `2` = Actualizar
    - `4` = Crear
    - `8` = Eliminar
    - `16` = Compartir
    - `31` = Todos
* - \<ocm:share-permissions />
  - Los permisos que tiene el usuario sobre el recurso compartido, como array JSON.
  - `["share", "read", "write"]`
* - \<nc:share-attributes />
  - Atributos establecidos por el usuario, como array JSON.
  - `[{ "scope" => <string>, "key" => <string>, "value" => <bool> }]`
* - \<nc:sharees />
  - La lista de destinatarios del recurso compartido.
  -
    ```xml
    <nc:sharee>
      <nc:id>alice</nc:id>
      <nc:display-name>Alice</nc:display-name>
      <nc:type>0</nc:type>
    </nc:sharee>
    ```
* - \<oc:checksums />
  - Un array de sumas de comprobación almacenadas en la BD por otros clientes. Los algoritmos usados actualmente son: `MD5`, `SHA1`, `SHA256`, `SHA3-256` y `Adler32`.
  - `<oc:checksum>md5:04c36b75222cd9fd47f2607333029106</oc:checksum>`
* - \<nc:has-preview />
  - Si hay una vista previa disponible del archivo.
  - `true` o `false`
* - \<nc:hidden />
  - Define si un archivo debe ocultarse. Actualmente solo se usa para las fotos en vivo.
  - `true` o `false`
* - \<oc:size />
  - A diferencia de `getcontentlength`, esta propiedad también funciona con carpetas e informa del tamaño de todo lo que hay en la carpeta. El tamaño está en bytes.
  - `127815235`
* - \<nc:rich-workspace-file />
  - El ID del archivo del espacio de trabajo.
  - *3456*
* - \<nc:rich-workspace />
  - El contenido del archivo del espacio de trabajo.
  -
* - \<nc:upload_time />
  - Fecha en que se subió este archivo.
  - `1675789581`
* - \<nc:note />
  - Nota del recurso compartido.
  -
* - \<nc:contained-folder-count />
  - El número de carpetas contenidas directamente en la carpeta (no de forma recursiva).
  -
* - \<nc:contained-file-count />
  - El número de archivos contenidos directamente en la carpeta (no de forma recursiva).
  -
* - \<nc:data-fingerprint />
  - Lo usan los clientes para averiguar si se ha restaurado una copia de seguridad.
  -
* - \<nc:acl-enabled>
  - Si la ACL está habilitada para esta carpeta de grupo.
  - `1` o `0`
* - \<nc:acl-can-manage>
  - Si el usuario actual puede gestionar la ACL.
  - `1` o `0`
* - \<nc:acl-list>
  - Array de reglas de ACL.
  -
    ```xml
    <nc:acl>
      <nc:acl-mapping-type>group</nc:acl-mapping-type>
      <nc:acl-mapping-id>admin</nc:acl-mapping-id>
      <nc:acl-mapping-display-name>admin</nc:acl-mapping-display-name>
      <nc:acl-mask>20</nc:acl-mask>
      <nc:acl-permissions>15</nc:acl-permissions>
    </nc:acl>
    ```
* - \<nc:inherited-acl-list>
  - Array de reglas de ACL de las carpetas superiores
  - Ver \<nc:acl-list>
* - \<nc:group-folder-id>
  - ID numérico de esa carpeta de grupo.
  - `1`
* - \<nc:lock>
  - Si el archivo está bloqueado.
  - `1` o `0`
* - \<nc:lock-owner-type>
  - Tipo del propietario del bloqueo.
  - - `0` = Usuario
    - `1` = Office o Text
    - `2` = WebDAV
* - \<nc:lock-owner>
  - ID de usuario del propietario del bloqueo.
  - `alice`
* - \<nc:lock-owner-displayname>
  - Nombre visible del propietario del bloqueo.
  - `Alice`
* - \<nc:lock-owner-editor>
  - ID de la app de un bloqueo que pertenece a una app.
  -
* - \<nc:lock-time>
  - Fecha en que se creó el bloqueo, como marca de tiempo.
  - `1675789581`
* - \<nc:lock-timeout>
  - TTL del bloqueo en segundos, a partir de la hora de creación.
  - `0` = Sin tiempo de espera
* - \<nc:lock-token>
  - El token del bloqueo.
  - `files_lock/0e53dfb6-61b4-46f0-b38e-d9a428292998`
* - \<nc:reminder-due-date>
  - La fecha de vencimiento del recordatorio, como cadena con formato ISO 8601.
  - `1970-01-01T00:00:00+00:00`
* - \<nc:version-label />
  - La etiqueta establecida por el usuario para un archivo.
  -
* - \<nc:version-author />
  - El ID del autor de una versión concreta de un archivo.
  - `admin`, `jane`, `thisAuthorsID`
* - \<nc:is-federated />
  - Si el nodo procede de un recurso compartido federado (de servidor a servidor).
  - `true` o `false`
* - \<nc:metadata_etag />
  - Un etag que cubre los metadatos del archivo. Cambia cuando se actualizan los metadatos (no el contenido).
  -
* - \<nc:download-url-expiration />
  - Fecha y hora de caducidad de una URL de descarga directa (si se ha generado una).
  -
:::

:::{note}
Las propiedades con el prefijo `nc:metadata-` (p. ej., `nc:metadata-blurhash`) son propiedades de metadatos dinámicas, registradas por las apps.
No se enumeran aquí una por una, ya que dependen de las apps que estén habilitadas.
Se pueden solicitar mediante PROPFIND como cualquier otra propiedad.
:::

### Listar carpetas ([rfc4918][rfc4918])

El contenido de una carpeta se puede listar enviando una solicitud {code}`PROPFIND` a la carpeta.

```
PROPFIND remote.php/dav/files/user/path/to/folder
```

#### Obtener las propiedades solo de la carpeta

Se pueden solicitar las propiedades de una carpeta sin obtener también su contenido añadiendo a la solicitud una cabecera {code}`Depth: 0`.

### Descargar archivos

:::{note}
En los archivos compartidos, esto solo funciona si quien los compartió no denegó el permiso de descarga.
:::

Un archivo se puede descargar enviando una solicitud {code}`GET` a la URL WebDAV del archivo.

```
GET remote.php/dav/files/user/path/to/file
```

(nc-dev-webdav-download-folders)=
### Descargar carpetas

:::{note}
El método {code}`GET` no está definido por el estándar WebDAV; es una extensión de WebDAV propia de Nextcloud.
:::

:::{note}
En las carpetas compartidas, esto solo funciona si quien las compartió no denegó el permiso de descarga.
:::

Una carpeta se puede descargar como archivo comprimido enviando una solicitud {code}`GET` a la URL WebDAV de la carpeta.
La cabecera {code}`Accept` debe estar establecida y contener el tipo MIME de los archivos ZIP ({code}`application/zip`) o de los archivos tar ({code}`application/x-tar`).

```
GET remote.php/dav/files/user/path/to/folder
Accept: application/zip
```

Opcionalmente, es posible incluir en el archivo comprimido solo algunos archivos de la carpeta, indicándolos con la cabecera personalizada {code}`X-NC-Files`:

```
GET remote.php/dav/files/user/path/to/folder
Accept: application/zip
X-NC-Files: document.txt
X-NC-Files: image.png
```

Como con los enlaces HTML no es posible establecer cabeceras, también se pueden proporcionar ambas opciones como parámetros de consulta.
En ese caso, el valor de la cabecera {code}`Accept` debe pasarse como el parámetro de consulta {code}`accept`.
Se aceptan tanto los tipos MIME completos ({code}`application/zip`, {code}`application/x-tar`) como los valores abreviados ({code}`zip`, {code}`tar`).
La lista opcional de archivos se puede proporcionar como un array codificado en JSON mediante el parámetro de consulta {code}`files`.

```
GET remote.php/dav/files/user/path/to/folder?accept=zip&files=["image.png","document.txt"]
```

Al usar parámetros de consulta, asegurarse de que los valores estén codificados como URL. En particular, {code}`files` debe ser un array JSON codificado como URL.

### Subir archivos

Un archivo se puede subir enviando una solicitud {code}`PUT` al archivo, con el contenido sin procesar del archivo como cuerpo de la solicitud.

```
PUT remote.php/dav/files/user/path/to/file
```

La solicitud sobrescribirá cualquier archivo existente.

### Crear carpetas ([rfc4918][rfc4918])

Una carpeta se puede crear enviando una solicitud {code}`MKCOL` a la carpeta.

```
MKCOL remote.php/dav/files/user/path/to/new/folder
```

### Eliminar archivos y carpetas ([rfc4918][rfc4918])

Un archivo o una carpeta se puede eliminar enviando una solicitud {code}`DELETE` al archivo o a la carpeta.

```
DELETE remote.php/dav/files/user/path/to/file
```

Al eliminar una carpeta, su contenido se eliminará de forma recursiva.

### Mover archivos y carpetas ([rfc4918][rfc4918])

Un archivo o una carpeta se puede mover enviando una solicitud {code}`MOVE` al archivo o a la carpeta y especificando el destino como URL completa en la cabecera {code}`Destination`.

```
MOVE remote.php/dav/files/user/path/to/file
Destination: https://cloud.example/remote.php/dav/files/user/new/location
```

El comportamiento de sobrescritura del movimiento se puede controlar estableciendo la cabecera {code}`Overwrite` en {code}`T` o {code}`F` para habilitar o deshabilitar la sobrescritura, respectivamente.

### Copiar archivos y carpetas ([rfc4918][rfc4918])

Un archivo o una carpeta se puede copiar enviando una solicitud {code}`COPY` al archivo o a la carpeta y especificando el destino como URL completa en la cabecera {code}`Destination`.

```
COPY remote.php/dav/files/user/path/to/file
Destination: https://cloud.example/remote.php/dav/files/user/new/location
```

El comportamiento de sobrescritura de la copia se puede controlar estableciendo la cabecera {code}`Overwrite` en {code}`T` o {code}`F` para habilitar o deshabilitar la sobrescritura, respectivamente.

### Marcar favoritos

Un archivo o una carpeta se puede marcar como favorito enviando una solicitud {code}`PROPPATCH` al archivo o a la carpeta y estableciendo la propiedad {code}`oc:favorite`.

```xml
PROPPATCH remote.php/dav/files/user/path/to/file
<?xml version="1.0"?>
<d:propertyupdate xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns">
  <d:set>
    <d:prop>
      <oc:favorite>1</oc:favorite>
    </d:prop>
  </d:set>
</d:propertyupdate>
```

Establecer la propiedad {code}`oc:favorite` en `1` marca un archivo como favorito; establecerla en `0` lo desmarca como favorito.

### Listar favoritos

Los favoritos de un usuario se pueden obtener enviando una solicitud {code}`REPORT` y especificando {code}`oc:favorite` como filtro.

```xml
REPORT remote.php/dav/files/user/path/to/folder
<?xml version="1.0"?>
<oc:filter-files  xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
     <oc:filter-rules>
         <oc:favorite>1</oc:favorite>
     </oc:filter-rules>
 </oc:filter-files>
```

Las propiedades de los archivos se pueden solicitar añadiendo a la solicitud un elemento {code}`<d:prop/>` que liste las propiedades solicitadas, del mismo modo que se haría en una solicitud {code}`PROPFIND`.

Al listar favoritos, la solicitud encuentra todos los favoritos de la carpeta de forma recursiva; todos los favoritos de un usuario se pueden encontrar enviando la solicitud a {code}`remote.php/dav/files/user`.

### Cabeceras especiales

#### Cabeceras de solicitud

Se pueden establecer algunas cabeceras especiales que Nextcloud interpretará.

:::{list-table}
:header-rows: 1
:widths: 20 55 25

* - Cabecera
  - Descripción
  - Ejemplo
* - X-OC-MTime
  - Permite especificar una hora de modificación. La respuesta contendrá la cabecera `X-OC-MTime: accepted` si se aceptó el mtime.
  - `1675789581`
* - X-OC-CTime
  - Permite especificar una hora de creación. La respuesta contendrá la cabecera `X-OC-CTime: accepted` si se aceptó el mtime.
  - `1675789581`
* - OC-Checksum
  - Una suma de comprobación que se almacenará en la BD. En las subidas `PUT` normales, el servidor almacena el valor sin validarlo. Durante las subidas masivas, la suma de comprobación **sí** se valida con el contenido subido. Los algoritmos usados actualmente son `MD5`, `SHA1`, `SHA256`, `SHA3-256`, `Adler32`.
  - `md5:04c36b75222cd9fd47f2607333029106`
* - X-Hash
  - En las solicitudes `PUT`, indica al servidor que calcule un hash del contenido del archivo subido durante la escritura. El servidor devuelve el hash o los hashes en cabeceras de respuesta llamadas `X-Hash-MD5`, `X-Hash-SHA1` y/o `X-Hash-SHA256`. Establecer el valor en `all` calcula los tres hashes. ¡Atención a las implicaciones de rendimiento!
  - `md5`, `sha1`, `sha256` o `all`
* - OC-Total-Length
  - Contiene el tamaño total del archivo durante una subida por fragmentos. Esto permite al servidor abortar antes si la cuota restante del usuario no es suficiente.
  - `4052412`
* - X-NC-WebDAV-AutoMkcol
  - Si se establece en `1`, indica al servidor que cree automáticamente cualquier directorio superior que falte al subir un archivo. Disponible desde Nextcloud 32.
  -
* - OC-Chunked

    (obsoleta)
  - Se usaba en la subida por fragmentos heredada para diferenciar una subida normal de una subida por fragmentos. Permitía comprobar la cuota y otras cosas. Hoy en día, en su lugar hay que proporcionar la cabecera `OC-Total-Length` en las solicitudes `PUT`.
  - Obsoleta

    Ya no es necesario proporcionarla
:::

### Cabeceras de respuesta

:::{list-table}
:header-rows: 1
:widths: 20 45 35

* - Cabecera
  - Descripción
  - Ejemplo
* - OC-Etag
  - En la creación, el movimiento y la copia, la respuesta contiene el etag del archivo.
  - `"50ef2eba7b74aa84feff013efee2a5ef"`
* - OC-FileId
  - En la creación, el movimiento y la copia, la respuesta contiene el fileid del archivo.
  - Formato: `<padded-id><instance-id>`.

    Ejemplo: `00000259oczn5x60nrdu`
* - X-NC-OwnerId
  - En la creación, la respuesta contiene el ID del propietario.
  - Ejemplo: `admin`
* - X-NC-Permissions
  - En la creación, la respuesta contiene la cadena de permisos.
  - Ejemplo: `RGDNVW`
:::

[rfc4918]: https://tools.ietf.org/html/rfc4918
````
