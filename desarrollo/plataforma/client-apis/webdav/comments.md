---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API WebDAV de comentarios: el endpoint por objeto y por comentario, los métodos que acepta y un ejemplo de solicitud REPORT con su respuesta."
---
# Comentarios

## Resumen

Esta página describe, para quienes desarrollan clientes y apps, el acceso a los comentarios mediante WebDAV: el endpoint del recurso, los métodos que aceptan sus endpoints por objeto y por comentario, y un ejemplo de solicitud `REPORT` con su respuesta.

````{upstream} developer_manual/client_apis/WebDAV/comments.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Los comentarios tienen una API PHP dentro de OCP y también vía WebDAV. A continuación, la documentación básica.

### Endpoint

El recurso de comentarios tiene un endpoint:

`` ` remote.php/comments/$OBJECTTYPE/$OBJECTID [/$COMMENTID] ` ``

El endpoint *ObjectID* acepta:
\* *POST* para crear un comentario
\* *PROPFIND* para listar los comentarios, y también la marca de lectura. Hay que especificar
los atributos en la solicitud.
\* *PROPPATCH* para actualizar la marca de lectura, nombre de la propiedad:
{code}`{http://owncloud.org/ns}readMarker`
\* *REPORT* para buscar comentarios

El endpoint *CommentID* acepta:
\* *PROPPATCH* para actualizar el comentario
\* *DELETE* para eliminarlo
\* *PROPFIND* para listar todas las propiedades

Para ver una lista de propiedades, consultar: *<https://github.com/nextcloud/server/blob/master/apps/dav/lib/Comments/CommentNode.php#L108>*

#### Ejemplos

Solicitud REPORT:

```
curl -u user:pwd -i --data-binary "@report.xml" -X REPORT -H "Content-Type: text/xml" http://test.nextcloud.bla/master/remote.php/dav/comments/files/2156
```

report.xml que se recibe:

```xml
<?xml version="1.0" encoding="utf-8" ?>
<D:report xmlns:D="DAV:" xmlns:oc="http://owncloud.org/ns" >
  <oc:limit>5</oc:limit>
  <oc:offset>0</oc:offset>
  <oc:datetime>2016-01-18 22:10:30</oc:datetime>
</D:report>
```

Ejemplo de salida (sin cabeceras):

```xml
<?xml version="1.0"?>
<d:multistatus xmlns:d="DAV:" xmlns:s="http://sabredav.org/ns" xmlns:cal="urn:ietf:params:xml:ns:caldav" xmlns:cs="http://calendarserver.org/ns/" xmlns:card="urn:ietf:params:xml:ns:carddav" xmlns:oc="http://owncloud.org/ns">
 <d:response>
  <oc:comment>
   <oc:id>3</oc:id>
   <oc:parentId>0</oc:parentId>
   <oc:topmostParentId>0</oc:topmostParentId>
   <oc:childrenCount>0</oc:childrenCount>
   <oc:message>first</oc:message>
   <oc:verb>comment</oc:verb>
   <oc:actorType>users</oc:actorType>
   <oc:actorId>master</oc:actorId>
   <oc:objectType>files</oc:objectType>
   <oc:objectId>2156</oc:objectId>
   <oc:creationDateTime>2016-01-18 22:01:16</oc:creationDateTime>
   <oc:latestChildDateTime>2016-01-20 14:01:24</oc:latestChildDateTime>
  </oc:comment>
 </d:response>
 <d:response>
  <oc:comment>
   <oc:id>2</oc:id>
   <oc:parentId>0</oc:parentId>
   <oc:topmostParentId>0</oc:topmostParentId>
   <oc:childrenCount>0</oc:childrenCount>
   <oc:message>first</oc:message>
   <oc:verb>comment</oc:verb>
   <oc:actorType>users</oc:actorType>
   <oc:actorId>master</oc:actorId>
   <oc:objectType>files</oc:objectType>
   <oc:objectId>2156</oc:objectId>
   <oc:creationDateTime>2016-01-18 22:01:12</oc:creationDateTime>
   <oc:latestChildDateTime>2016-01-20 14:01:24</oc:latestChildDateTime>
  </oc:comment>
 </d:response>
</d:multistatus>
```

Para un ejemplo de uso real, el centro de anuncios tiene los comentarios implementados.
Para lo relativo al frontend, consultar los archivos relacionados con los comentarios en *<https://github.com/nextcloud/announcementcenter/tree/master/js>*.
En cuanto al backend, *OCP\Comments\ICommentsManager* es, en su mayor parte, lo más cercano para las tareas de mantenimiento.
Se introdujo en <https://github.com/nextcloud/announcementcenter/pull/12>, pero
también hay algunas PR de seguimiento.
````
