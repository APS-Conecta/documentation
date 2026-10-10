---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API externa OCS: registrar métodos en routes.php, devolver datos y excepciones, autenticación, formato de salida, códigos de estado y retrocompatibilidad."
---
# API externa

## Resumen

Esta página describe la API externa basada en Open Collaboration Services: cómo registrar métodos, devolver datos y lanzar excepciones, la autenticación, el formato XML o JSON de la salida, los códigos de estado y la política de cambios y retrocompatibilidad. Está dirigida a quienes desarrollan apps que exponen datos a terceros.

````{upstream} developer_manual/server/externalapi.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Introducción

La API externa de Nextcloud permite a desarrolladores externos acceder a los datos
que proporcionan las apps de Nextcloud. Nextcloud sigue la [especificación Open Collaboration
Services](https://open-collaboration-services.org).

### Uso

#### Registrar métodos

Los métodos se registran en {file}`appinfo/routes.php` devolviendo un
array con los metadatos del endpoint.

```php
<?php

return [
  'ocs' => [
    // Apps
    ['name' => 'Bar#getFoo', 'url' => '/foobar', 'verb' => 'GET'],
  ],
];
```

#### Devolver datos

Una vez que el backend de la API ha encontrado la URL, se ejecuta la función invocable definida en
**BarController::getFoo**. El AppFramework se encarga de que los parámetros enviados
se pasen al método según su declaración.

Hay que extender `OCP\AppFramework\OCSController` del AppFramework.
Las funciones deben devolver entonces un `OCP\AppFramework\Http\DataResponse`. El
AppFramework se encarga después de dar el formato adecuado a la respuesta.

#### Excepciones

Para lanzar una excepción al usuario en la respuesta OCS, se puede lanzar una
`OCP\AppFramework\OCS\OCSException`. Se pueden establecer el mensaje y el código.

Hay 3 excepciones de uso frecuente ya disponibles:

- `OCSBadRequestException`
- `OCSForbiddenException`
- `OCSNotFoundException`

#### Autenticación y conceptos básicos

Las peticiones al endpoint OCS a menudo tienen que estar autenticadas.

> `curl -u user:password https://example.com/ocs/v2.php/apps/yourapp/foobar`

#### Salida

La salida es XML de forma predeterminada. Para obtener JSON, agregar esto a la URL:

```
?format=json
```

O establecer la cabecera Accept adecuada:

```
Accept: application/json
```

La salida de la aplicación va envuelta en un elemento **data**:

**XML**:

```xml
<?xml version="1.0"?>
<ocs>
 <meta>
  <status>ok</status>
  <statuscode>200</statuscode>
  <message/>
 </meta>
 <data>
   <!-- data here -->
 </data>
</ocs>
```

**JSON**:

```js
{
  "ocs": {
    "meta": {
      "status": "ok",
      "statuscode": 200,
      "message": null
    },
    "data": {
      // data here
    }
  }
}
```

#### Códigos de estado

El código de estado puede ser cualquiera de los siguientes números:

- **200** - correcto
- **996** - error del servidor
- **401** - no autorizado
- **404** - no encontrado
- **999** - error desconocido

#### Cambios en la API y retrocompatibilidad

Se procura mantener la API lo más estable posible para no romper las apps de terceros.
Antes de que se permita eliminar una API, debe marcarse como obsoleta durante al
menos 3 años (9 versiones de Nextcloud) antes de eliminarla.

Los cambios en la API [deben discutirse en un issue de GitHub del repositorio del
servidor de Nextcloud](https://github.com/nextcloud/server/issues). Una pull request es más que bienvenida.
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
