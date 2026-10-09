---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Panorama de los endpoints de la API OCS: autenticación, pruebas con curl, usuarios, capacidades, descarga directa, autocompletado e idioma forzado."
---
# Panorama general de las API OCS

## Resumen

Esta página resume, para quienes desarrollan clientes o apps, los endpoints de la API OCS: cómo autenticarse y probar llamadas con curl, y las API de metadatos de usuario, capacidades, descarga directa, notificaciones, autocompletado e idioma forzado.

````{upstream} developer_manual/client_apis/OCS/ocs-api-overview.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Este documento ofrece un panorama rápido de los endpoints de la API OCS compatibles con Nextcloud.

Todas las solicitudes deben proporcionar información de autenticación, ya sea como cabecera Basic Auth o pasando un conjunto de cookies de sesión válidas, salvo que se indique lo contrario.

### Autenticación

La autenticación puede hacerse con nombre de usuario y contraseña (o un token de app) o con tokens OIDC; ver los ejemplos a continuación:

Nombre de usuario/contraseña:

```bash
curl -u username:password -X GET 'https://cloud.example.com/ocs/v1.php/...' -H "OCS-APIRequest: true"
```

Token OIDC:

```bash
curl -X GET 'https://cloud.example.com/ocs/v1.php/...' -H "OCS-APIRequest: true" -H "Authorization: Bearer ID_TOKEN"
```

### Probar solicitudes con curl

Todas las solicitudes OCS pueden probarse fácilmente con {code}`curl`, indicando el método de la solicitud ({code}`GET`, {code}`PUT`, etc.) y estableciendo un cuerpo de solicitud cuando haga falta.

Por ejemplo, se puede hacer una solicitud {code}`GET` para obtener información sobre un usuario:

```bash
curl -u username:password -X GET 'https://cloud.example.com/ocs/v1.php/...' -H "OCS-APIRequest: true"
```

Se puede cambiar el tipo de respuesta de la solicitud añadiendo una cabecera Accept. Por ejemplo, si se prefieren respuestas JSON:

```bash
curl -u username:password -X GET 'https://cloud.example.com/ocs/v1.php/...' -H "Accept: application/json" -H "OCS-APIRequest: true"
```

Añadir la cabecera Accept también garantiza la coherencia de las respuestas, ya que algunas solicitudes OCS heredadas devuelven XML como respuesta predeterminada, mientras que las solicitudes más recientes devuelven JSON.

### Metadatos de usuario

Desde: 11.0.2, 12.0.0

Esta solicitud devuelve los metadatos disponibles de un usuario. Los usuarios administradores pueden ver la información de todos los usuarios, mientras que un usuario normal solo puede acceder a sus propios metadatos.

```
GET /ocs/v1.php/cloud/users/USERID
```

```xml
<?xml version="1.0"?>
<ocs>
    <meta>
        <status>ok</status>
        <statuscode>100</statuscode>
        <message>OK</message>
        <totalitems></totalitems>
        <itemsperpage></itemsperpage>
    </meta>
    <data>
        <enabled>1</enabled>
        <storageLocation>/path/to/storage/location/userid</storageLocation>
        <id>userid</id>
        <lastLogin>1578283711000</lastLogin>
        <backend>Database</backend>
        <subadmin/>
        <quota>
            <free>20632824998</free>
            <used>842011482</used>
            <total>21474836480</total>
            <relative>3.92</relative>
            <quota>21474836480</quota>
        </quota>
        <email>user@foo.de</email>
        <displayname>John Doe</displayname>
        <display-name>John Doe</display-name>
        <phone></phone>
        <address></address>
        <website>https://example.com</website>
        <twitter></twitter>
        <groups>
            <element>1st group</element>
            <element>2nd group</element>
            <element>3rd group</element>
            <element>... group</element>
        </groups>
        <language>de</language>
        <locale>de_DE</locale>
        <backendCapabilities>
            <setDisplayName>1</setDisplayName>
            <setPassword>1</setPassword>
        </backendCapabilities>
    </data>
</ocs>
```

### Metadatos de usuario: listar los ID de usuario

Esta solicitud devuelve una lista con todos los ID de usuario. Solo los usuarios administradores pueden consultar la lista.

```
GET /ocs/v1.php/cloud/users
```

```xml
<?xml version="1.0"?>
<ocs>
    <meta>
        <status>ok</status>
        <statuscode>100</statuscode>
        <message>OK</message>
        <totalitems></totalitems>
        <itemsperpage></itemsperpage>
    </meta>
    <data>
        <users>
            <element>1st_user</element>
            <element>2nd_user</element>
            <element>3rd_user</element>
            <element>..._user</element>
        </users>
    </data>
</ocs>
```

### API de capacidades

Los clientes pueden obtener las capacidades que ofrecen el servidor Nextcloud y sus apps mediante la API OCS de capacidades.

```
GET /ocs/v1.php/cloud/capabilities
```

```xml
<?xml version="1.0"?>
<ocs>
    <meta>
        <status>ok</status>
        <statuscode>100</statuscode>
        <message>OK</message>
        <totalitems></totalitems>
        <itemsperpage></itemsperpage>
    </meta>
    <data>
        <version>
            <major>17</major>
            <minor>0</minor>
            <micro>2</micro>
            <string>17.0.2</string>
            <edition></edition>
            <extendedSupport></extendedSupport>
        </version>
        <capabilities>
            <core>
                <pollinterval>60</pollinterval>
                <webdav-root>remote.php/webdav</webdav-root>
            </core>
        </capabilities>
    </data>
</ocs>
```

### Capacidades de tematización

Los valores de la app de tematización se exponen a través de la API de capacidades, lo que permite a quienes desarrollan clientes ajustar el aspecto de los clientes a la tematización de distintas instancias de Nextcloud.

```xml
<theming>
    <name>Nextcloud</name>
    <url>https://nextcloud.com</url>
    <slogan>A safe home for all your data</slogan>
    <color>#0082c9</color>
    <color-text>#ffffff</color-text>
    <color-element>#0082c9</color-element>
    <color-element-bright>#aaaaaa</color-element-bright>
    <color-element-dark>#555555</color-element-dark>
    <logo>http://cloud.example.com/index.php/apps/theming/logo?v=1</logo>
    <background>http://cloud.example.com/index.php/apps/theming/logo?v=1</background>
    <background-plain></background-plain>
    <background-default></background-default>
</theming>
```

Para elementos como botones de opción, bordes de campos de entrada y otros, en lugar del valor primario `color` debe usarse `color-element-bright` sobre fondos claros y `color-element-dark` sobre fondos oscuros.
Así, cuando el color primario se establece, p. ej., en `#000000`, `color-elemenet-dark` se establecerá en `#555555`, de modo que los elementos sigan siendo visibles. En la interfaz web de Nextcloud solo la cabecera superior usa `color`; todo lo demás usa `color-element-*`.
El texto y los iconos sobre estos elementos deben usar `color-text`.

El valor de fondo puede ser una URL a la imagen de fondo o un valor de color hexadecimal.

### Descarga directa

Puede ser necesario dar a un tercero acceso a un archivo sin querer entregarle las credenciales. Un ejemplo de esto es reproducir archivos en un reproductor multimedia externo en dispositivos móviles.

Para resolver este problema existe una forma de solicitar un enlace público único a un solo archivo.
Este enlace es válido durante 8 horas; después se elimina.

Para obtener un enlace directo:

```
POST /ocs/v2.php/apps/dav/api/v1/direct
```

Con el {code}`fileId` en el cuerpo (por ejemplo, {code}`fileId=42`).
Esto devuelve el enlace que debe usarse para obtener el archivo.

### Notificaciones

También existe la [API de notificaciones](https://github.com/nextcloud/notifications/blob/master/docs/ocs-endpoint-v2.md),
así como documentación sobre cómo [registrar un dispositivo para notificaciones push](https://github.com/nextcloud/notifications/blob/5a2d3607952bad675e4057620a9c7de8a7f84f0b/docs/push-v3.md).

### Autocompletado y búsqueda de usuarios

Es posible buscar usuarios con la API de autocompletado, que se usa para autocompletar nombres de usuario en comentarios y en el chat, o para encontrar cuentas de invitado. El código [puede encontrarse aquí](https://github.com/nextcloud/server/blob/master/core/Controller/AutoCompleteController.php#L69).

Un ejemplo de comando curl sería:

```
curl -i -u master -X GET -H "OCS-APIRequest: true" 'https://my.nextcloud/ocs/v2.php/core/autocomplete/get?search=JOANNE%40EMAIL.ISP&itemType=%20&itemId=%20&shareTypes[]=8&limit=2'
```

Esto buscaría JOANNE@EMAIL.ISP como usuario invitado. Se devuelven como máximo 2 resultados para un usuario normal, y el array shareTypes llevaría solo "8". `itemType` e `itemId` se omiten (se establecen en un espacio en blanco);
en esencia sirven para dar contexto sobre el caso de uso, de modo que los ordenadores (sorters) puedan hacer su trabajo (como quién comentó por última vez).
Puede ser una opción para filtrar en una etapa posterior, pero también se pueden omitir, como en el ejemplo siguiente.

```
curl -i -u master -X GET -H "OCS-APIRequest: true" 'https://my.nextcloud/ocs/v2.php/core/autocomplete/get?search=JOANNE%40EMAIL.ISP&shareTypes[]=8&limit=2'
```

El shareType es, de forma predeterminada, el de los usuarios normales si se omitió), y el límite es 10 de forma predeterminada.

#### Filtrar los resultados del autocompletado

Si hace falta, también se pueden filtrar más los resultados del autocompletado en el lado de PHP con el evento
`OCP\Collaboration\AutoComplete\AutoCompleteEvent`. El evento da acceso al conjunto de resultados actual,
al elemento y a los tipos de recurso compartido, y a algo más de información que puede usarse, p. ej., para limitar los resultados
del autocompletado a los usuarios que realmente están en la conversación de chat actual.

(nc-dev-api-force-language)=
### Forzar el idioma de una llamada

Todas las llamadas a la API de Nextcloud permiten forzar el idioma con el parámetro de consulta `forceLanguage`. Este anula cualquier ajuste del usuario para esa llamada.

```bash
curl -u username:password -X GET 'https://cloud.example.com/ocs/v1.php/...?forceLanguage=en' -H "OCS-APIRequest: true"
```
````
