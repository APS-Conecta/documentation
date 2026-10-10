---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo un cliente obtiene credenciales propias con el flujo de inicio de sesión (v1 y v2) y cómo convierte y elimina contraseñas de aplicación."
---
(nc-dev-loginflowindex)=
# Flujo de inicio de sesión

## Resumen

Esta página explica, para quienes desarrollan clientes, cómo obtener credenciales de inicio de sesión propias de cada cliente con el flujo de inicio de sesión y con su versión 2, cómo convertir una configuración con usuario y contraseña en una contraseña de aplicación y cómo eliminar esa contraseña. Cierra con un caso de solución de problemas sobre el nombre de inicio de sesión y el inicio de sesión con correo electrónico.

````{upstream} developer_manual/client_apis/LoginFlow/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Este documento ofrece una visión general rápida del nuevo flujo de inicio de sesión que deben usar los clientes para obtener
credenciales de inicio de sesión. Así se garantiza que cada cliente obtenga su propio conjunto de credenciales. Esto tiene varias ventajas:

1. Un cliente nunca almacena la contraseña del usuario
2. El usuario puede revocar el acceso cliente por cliente desde la web

### Abrir la vista web

El cliente debe abrir una vista web en {code}`<server>/index.php/login/flow`. Hay que asegurarse de establecer la cabecera {code}`OCS-APIREQUEST`
en {code}`true`.

El cliente registrará un manejador de URL para capturar las URL del protocolo {code}`nc`. Esto es necesario para obtener las
credenciales en la etapa final.

Debe ser una vista web de un solo uso. Esto significa:

- No debe haber cookies establecidas al crear la vista web
- No deben almacenarse contraseñas
- No debe conservarse ningún estado después de que la vista web haya terminado

Para lograr una buena experiencia de usuario, conviene tener en cuenta lo siguiente:

- establecer una cabecera {code}`ACCEPT_LANGUAGE` adecuada
- establecer una cabecera {code}`USER_AGENT` adecuada

### Iniciar la sesión del usuario

El usuario verá ahora una página web que le indica que concederá acceso a {code}`USER_AGENT`. Al seguir los pasos,
se le pedirá que inicie sesión. Si tiene habilitada la autenticación de dos factores, la necesitará para iniciar sesión. Pero, como
todo esto ocurre dentro de la propia vista web, el cliente no necesita ocuparse de ello.

### Obtener las credenciales de inicio de sesión

En el inicio de sesión final, el servidor hará una redirección a una URL con el siguiente formato:

```
nc://login/server:<server>&user:<loginname>&password:<password>
```

- `server`: la dirección del servidor al que conectarse. El servidor puede especificar un protocolo (http o https). Si no se especifica ningún protocolo, el cliente supondrá https.
- `loginname`: el nombre de usuario que el cliente debe usar para iniciar sesión. **Nota:** hay que tener en cuenta que este es el nombre de inicio de sesión y que podría ser distinto del nombre de usuario. Por ejemplo, la dirección de correo electrónico podría usarse para iniciar sesión, pero no para generar la URL de WebDAV. El nombre de usuario real se puede obtener del endpoint de la API OCS `<server>/ocs/v1.php/cloud/user`.
- `password`: la contraseña que el cliente debe usar para iniciar sesión y almacenar de forma segura

:::{note}
`loginname` y `password` se codifican con [urlencode](https://www.php.net/manual/en/function.urlencode.php) de PHP, que difiere de [RFC 3986](http://www.faqs.org/rfcs/rfc3986.html). Puede ser necesario sustituir los signos más {code}`'+'` por espacios {code}`' '` antes de decodificar.
:::

El cliente usará esta información para crear una cuenta nueva.
Después, la vista web se destruye, incluido todo el estado que contiene.

### Convertir a contraseñas de aplicación

Las configuraciones antiguas de los clientes podrían seguir usando nombre de usuario y contraseñas. El flujo de inicio de sesión garantiza que cada dispositivo tenga una contraseña de aplicación única. Para facilitar una migración transparente a contraseñas de aplicación, existe un endpoint al que el cliente puede llamar.

Si el cliente está autenticado con una contraseña de aplicación, se devolverá un 403. Si el cliente se autentica con una contraseña real, se generará y se devolverá una contraseña de aplicación.

La cabecera de agente de usuario se usará para dar nombre a la contraseña de aplicación.

```bash
curl -u username:password -H 'OCS-APIRequest: true' https://cloud.example.com/ocs/v2.php/core/getapppassword
```

La respuesta se vería (en XML) más o menos así:

```xml
<?xml version="1.0"?>
<ocs>
        <meta>
                <status>ok</status>
                <statuscode>200</statuscode>
                <message>OK</message>
        </meta>
        <data>
                <apppassword>M1DqHwuZWwjEC3ku7gJsspR7bZXopwf01kj0XGppYVzEkGtbZBRaXlOUxFZdbgJ6Zk9OwG9x</apppassword>
        </data>
</ocs>
```

### Eliminar una contraseña de aplicación

Cuando se elimina una cuenta en un cliente por tareas de limpieza, es deseable destruir el token de aplicación en uso.
Esto se puede hacer con una simple llamada:

```bash
curl -u username:app-password -X DELETE -H 'OCS-APIREQUEST: true'  http://localhost/ocs/v2.php/core/apppassword
```

La respuesta debería ser una respuesta OCS simple con un estado 200

```xml
<?xml version="1.0"?>
<ocs>
        <meta>
                <status>ok</status>
                <statuscode>200</statuscode>
                <message>OK</message>
        </meta>
        <data/>
</ocs>
```

Si se devuelve un código de estado distinto de 200, el cliente debe continuar igualmente con la eliminación de la cuenta.

### Flujo de inicio de sesión v2

Aunque el flujo de inicio de sesión funciona muy bien en muchos casos, existen ciertos obstáculos, especialmente en las aplicaciones de escritorio. Una configuración especial de proxy, los certificados del lado del cliente y similares pueden causar problemas. Para resolverlo, se ha ideado un segundo flujo de inicio de sesión que usa el navegador web predeterminado del usuario para autenticarse. Así se garantiza que, si puede iniciar sesión a través de la web, también pueda iniciar sesión en el cliente.

Para comenzar un inicio de sesión, hacer una solicitud POST anónima

```bash
curl -X POST https://cloud.example.com/index.php/login/v2
```

Esto devolverá un objeto JSON como

```json
{
    "poll":{
        "token":"mQUYQdffOSAMJYtm8pVpkOsVqXt5hglnuSpO5EMbgJMNEPFGaiDe8OUjvrJ2WcYcBSLgqynu9jaPFvZHMl83ybMvp6aDIDARjTFIBpRWod6p32fL9LIpIStvc6k8Wrs1",
        "endpoint":"https:\/\/cloud.example.com\/login\/v2\/poll"
    },
    "login":"https:\/\/cloud.example.com\/login\/v2\/flow\/guyjGtcKPTKCi4epIRIupIexgJ8wNInMFSfHabACRPZUkmEaWZSM54bFkFuzWksbps7jmTFQjeskLpyJXyhpHlgK8sZBn9HXLXjohIx5iXgJKdOkkZTYCzUWHlsg3YFg"
}
```

La URL que figura en login debe abrirse en el navegador predeterminado; ahí es donde el usuario seguirá el procedimiento de inicio de sesión.
El programa debe empezar de inmediato a sondear el endpoint poll:

```bash
curl -X POST https://cloud.example.com/login/v2/poll -d "token=mQUYQdffOSAMJYtm8pVpkOsVqXt5hglnuSpO5EMbgJMNEPFGaiDe8OUjvrJ2WcYcBSLgqynu9jaPFvZHMl83ybMvp6aDIDARjTFIBpRWod6p32fL9LIpIStvc6k8Wrs1"
```

El token será válido durante 20 minutos.
Esto devolverá un 404 hasta que se complete la autenticación. Cuando se devuelve un 200, se trata de otro objeto JSON.

```json
{
    "server":"https:\/\/cloud.example.com",
    "loginName":"username",
    "appPassword":"yKTVA4zgxjfivy52WqD8kW3M2pKGQr6srmUXMipRdunxjPFripJn0GMfmtNOqOolYSuJ6sCN"
}
```

Usar el servidor y las credenciales proporcionadas para conectarse.
Hay que tener en cuenta que el 200 solo se devolverá una vez.

### Solución de problemas

#### Nombre de inicio de sesión frente a inicio de sesión con correo electrónico

Nextcloud permite la autenticación con el *nombre de inicio de sesión* del usuario, que puede ser su UID, una dirección de correo electrónico o similar. El identificador usado en la sesión en la que el usuario genera la contraseña de aplicación se almacenará en el registro de la base de datos de la contraseña de aplicación generada. Por lo tanto, el identificador usado en la sesión web que autoriza a un cliente debe coincidir con el identificador usado en el cliente que se conecta.
````

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
