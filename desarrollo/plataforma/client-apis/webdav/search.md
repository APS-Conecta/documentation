---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Búsqueda WebDAV (RFC 5323): cómo enviar solicitudes SEARCH, qué propiedades DAV admite, el ámbito de búsqueda y cuerpos de consulta de ejemplo."
---
(nc-dev-webdavsearch)=
# Búsqueda

## Resumen

Esta página describe, para quienes desarrollan clientes, la búsqueda WebDAV según el RFC 5323: cómo enviar una solicitud `SEARCH`, qué propiedades DAV se pueden seleccionar, buscar y ordenar, cuál es el ámbito de una búsqueda y varios cuerpos de consulta de ejemplo.

````{upstream} developer_manual/client_apis/WebDAV/search.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Nextcloud implementa la búsqueda WebDAV de [rfc5323][rfc5323] para que los clientes puedan buscar archivos en el servidor.
La búsqueda WebDAV permite consultas de búsqueda bastante complejas, con filtrado y ordenación por varias propiedades.

Este documento describe cómo usar la búsqueda WebDAV con un servidor Nextcloud y ofrece algunas consultas de ejemplo;
los detalles completos de la API se encuentran en [rfc5323][rfc5323].

### Realizar solicitudes de búsqueda

Las solicitudes de búsqueda se realizan enviando una solicitud HTTP {code}`SEARCH` a {code}`https://cloud.example.com/remote.php/dav/`
con un tipo de contenido {code}`text/xml` y la consulta como XML en el cuerpo de la solicitud.

Por ejemplo, para buscar archivos de texto del usuario 'test':

```bash
curl -u test:password 'https://cloud.example.com/remote.php/dav/' -X SEARCH -H "content-Type: text/xml" --data '<?xml version="1.0" encoding="UTF-8"?>
 <d:searchrequest xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns">
     <d:basicsearch>
         <d:select>
             <d:prop>
                 <oc:fileid/>
                 <d:displayname/>
                 <d:getcontenttype/>
                 <d:getetag/>
                 <oc:size/>
             </d:prop>
         </d:select>
         <d:from>
             <d:scope>
                 <d:href>/files/test</d:href>
                 <d:depth>infinity</d:depth>
             </d:scope>
         </d:from>
         <d:where>
             <d:like>
                 <d:prop>
                     <d:getcontenttype/>
                 </d:prop>
                 <d:literal>text/%</d:literal>
             </d:like>
         </d:where>
         <d:orderby/>
    </d:basicsearch>
</d:searchrequest>'
```

### Propiedades DAV admitidas

Las siguientes propiedades DAV se pueden usar en {code}`select`, {code}`where` y {code}`orderby`;
no todas las propiedades se pueden usar en cada operación.

| Nombre de la propiedad | Descripción | Seleccionable | Buscable | Ordenable | Tipo |
|---|---|---|---|---|---|
| {code}`{DAV:}displayname` | Nombre del archivo | ✓ | ✓ | ✓ | Cadena |
| {code}`{DAV:}getcontenttype` | Tipo MIME | ✓ | ✓ | ✓ | Cadena |
| {code}`{DAV:}getlastmodified` | Fecha de modificación | ✓ | ✓ | ✓ | Fecha y hora |
| {code}`{DAV:}creationdate` | Fecha de creación | ✓ | ✓ | ✓ | Fecha y hora |
| {code}`{http://nextcloud.org/ns}upload_time` | Fecha de subida | ✓ | ✓ | ✓ | Fecha y hora |
| {code}`{http://nextcloud.org/ns}last_activity` | La más reciente entre la fecha de subida y la de modificación | ✓ | ❌ | ✓ | Fecha y hora |
| {code}`{http://owncloud.org/ns}size` | Tamaño del archivo o de la carpeta | ✓ | ✓ | ✓ | Entero |
| {code}`{http://owncloud.org/ns}favorite` | Estado de favorito | ✓ | ✓ | ✓ | Booleano |
| {code}`{http://owncloud.org/ns}fileid` | ID de archivo de Nextcloud | ✓ | ✓ | ❌ | Entero |
| {code}`{DAV:}resourcetype` | Archivo o carpeta | ✓ | ❌ | ❌ | Cadena |
| {code}`{DAV:}getcontentlength` | Tamaño del archivo, no para carpetas | ✓ | ❌ | ❌ | Cadena |
| {code}`{http://owncloud.org/ns}checksums` | Sumas de comprobación almacenadas del archivo | ✓ | ❌ | ❌ | Cadena |
| {code}`{http://owncloud.org/ns}permissions` | Permisos del archivo | ✓ | ❌ | ❌ | Cadena |
| {code}`{DAV:}getetag` | Etag del archivo | ✓ | ❌ | ❌ | Cadena |
| {code}`{http://owncloud.org/ns}owner-id` | Propietario del archivo | ✓ | ❌ | ❌ | Cadena |
| {code}`{http://owncloud.org/ns}owner-display-name` | Nombre visible del propietario del archivo | ✓ | ❌ | ❌ | Cadena |
| {code}`{http://owncloud.org/ns}data-fingerprint` | Huella para el estado de recuperación | ✓ | ❌ | ❌ | Cadena |
| {code}`{http://nextcloud.org/ns}has-preview` | Estado de la vista previa | ✓ | ❌ | ❌ | Booleano |

### Ámbito de búsqueda

Todas las consultas de búsqueda se limitan a una única carpeta relativa a la raíz de DAV.
Por ahora solo se admiten consultas de búsqueda de archivos, lo que significa que el ámbito siempre debe empezar por {code}`files/$username`.

Dentro de los archivos del usuario, cualquier carpeta existente se puede usar como ámbito de búsqueda.

### Ejemplos de cuerpos de búsqueda

Buscar todos los archivos de texto plano en la carpeta {code}`Documents`, ordenados por tamaño.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<d:searchrequest xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns">
    <d:basicsearch>
        <d:select>
            <d:prop>
                <d:displayname/>
            </d:prop>
        </d:select>
        <d:from>
            <d:scope>
                <d:href>/files/test/Documents</d:href>
                <d:depth>infinity</d:depth>
            </d:scope>
        </d:from>
        <d:where>
            <d:like>
                <d:prop>
                    <d:getcontenttype/>
                </d:prop>
                <d:literal>text/%</d:literal>
            </d:like>
        </d:where>
        <d:orderby>
            <d:order>
                <d:prop>
                    <oc:size/>
                </d:prop>
                <d:ascending/>
            </d:order>
        </d:orderby>
    </d:basicsearch>
</d:searchrequest>
```

Obtener un archivo por su ID.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<d:searchrequest xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns">
    <d:basicsearch>
        <d:select>
            <d:prop>
                <d:displayname/>
            </d:prop>
        </d:select>
        <d:from>
            <d:scope>
                <d:href>/files/test</d:href>
                <d:depth>infinity</d:depth>
            </d:scope>
        </d:from>
        <d:where>
            <d:eq>
                <d:prop>
                    <oc:fileid/>
                </d:prop>
                <d:literal>12345</d:literal>
            </d:eq>
        </d:where>
        <d:orderby/>
    </d:basicsearch>
</d:searchrequest>
```

Obtener todos los archivos png y jpg de más de 10MB.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<d:searchrequest xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns">
    <d:basicsearch>
        <d:select>
            <d:prop>
                <d:displayname/>
            </d:prop>
        </d:select>
        <d:from>
            <d:scope>
                <d:href>/files/test</d:href>
                <d:depth>infinity</d:depth>
            </d:scope>
        </d:from>
        <d:where>
            <d:and>
                <d:or>
                    <d:eq>
                        <d:prop>
                            <d:getcontenttype/>
                        </d:prop>
                        <d:literal>image/png</d:literal>
                    </d:eq>
                    <d:eq>
                        <d:prop>
                            <d:getcontenttype/>
                        </d:prop>
                        <d:literal>image/jpg</d:literal>
                    </d:eq>
                </d:or>
                    <d:gt>
                        <d:prop>
                            <oc:size/>
                        </d:prop>
                        <d:literal>10000000</d:literal>
                    </d:gt>
            </d:and>
        </d:where>
        <d:orderby/>
    </d:basicsearch>
</d:searchrequest>
```

Buscar todos los archivos comunes (sin directorios) y limitar el resultado a los últimos 5 archivos, ordenados por última modificación

```xml
 <d:searchrequest xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns">
     <d:basicsearch>
         <d:select>
             <d:prop>
                 <oc:fileid/>
                 <d:getcontenttype/>
                 <d:getetag/>
                 <oc:size/>
                 <d:getlastmodified/>
                 <d:resourcetype/>
             </d:prop>
         </d:select>
         <d:from>
             <d:scope>
                 <d:href>/files/test</d:href>
                 <d:depth>infinity</d:depth>
             </d:scope>
         </d:from>
         <d:where>
             <d:not>
                 <d:is-collection/>
             </d:not>
         </d:where>
         <d:orderby>
            <d:order>
                <d:prop>
                    <d:getlastmodified/>
                </d:prop>
                <d:descending/>
             </d:order>
         </d:orderby>
         <d:limit>
           <d:nresults>5</d:nresults>
         </d:limit>
    </d:basicsearch>
</d:searchrequest>
```

Obtener todos los archivos modificados por última vez después de una fecha dada.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<d:searchrequest xmlns:d="DAV:">
    <d:basicsearch>
        <d:select>
            <d:prop>
                <d:displayname/>
                <d:getlastmodified />
            </d:prop>
        </d:select>
        <d:from>
            <d:scope>
                <d:href>/files/test</d:href>
                <d:depth>infinity</d:depth>
            </d:scope>
        </d:from>
        <d:where>
            <d:gt>
                <d:prop>
                    <d:getlastmodified/>
                </d:prop>
                <d:literal>2021-01-01T17:00:00Z</d:literal>
            </d:gt>
        </d:where>
        <d:orderby/>
    </d:basicsearch>
</d:searchrequest>
```

[rfc5323]: https://tools.ietf.org/html/rfc5323
````
