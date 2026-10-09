---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Conectar Nextcloud a un servidor de correo: asistente, SMTP, Sendmail y qmail, plantillas de correo, parámetros de config.php y solución de problemas."
---
# Correo electrónico

## Resumen

Esta página explica, para quienes administran el servidor, cómo conectar Nextcloud a un servidor de correo con el asistente o con los parámetros de `config.php` (SMTP, Sendmail y qmail), cómo personalizar las plantillas de correo y cómo diagnosticar los problemas de envío.

````{upstream} admin_manual/configuration_server/email_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud puede enviar correos de restablecimiento de contraseña y avisar a los usuarios de nuevos archivos compartidos, de cambios en archivos y de notificaciones de actividad. Los usuarios configuran en sus páginas personales qué notificaciones quieren recibir.

Nextcloud no incluye un servidor de correo completo, sino que se conecta al servidor de correo existente. Para que Nextcloud pueda enviar correos debe haber un servidor de correo en funcionamiento. El servidor de correo puede estar en la misma máquina que Nextcloud o ser un servidor remoto.

Para acceder a la página de configuración que se muestra abajo, iniciar sesión con una cuenta de administración. Hacer clic en el avatar y después en {guilabel}`Ajustes`. En el lado izquierdo, en {guilabel}`Administración`, hacer clic en {guilabel}`Ajustes básicos`.

La página muestra la sección {guilabel}`Servidor de correo electrónico`, con sus campos de configuración y el botón {guilabel}`Enviar mensaje`.

Con el asistente, conectar Nextcloud al servidor de correo es rápido y sencillo. El asistente rellena los valores de `config/config.php`, así que puede usarse uno u otro, o ambos, según se prefiera.

El asistente de correo de Nextcloud admite tres tipos de conexión con el servidor de correo: SMTP, qmail y Sendmail. Usar el configurador SMTP para un servidor remoto, o Sendmail cuando el servidor de correo está en la misma máquina que Nextcloud.

:::{note}
La opción Sendmail se refiere al servidor SMTP Sendmail y a cualquier sustituto directo de Sendmail, como Postfix, Exim o Courier. Todos ellos incluyen un binario `sendmail` y son libremente intercambiables.
:::

(nc-email-smtp-config)=
### Proveedores de correo

:::{versionadded} 30
:::

Un proveedor de correo es una app que presta a Nextcloud un servicio de correo saliente y permite enviar los correos del sistema directamente desde la cuenta de correo personal que el usuario ha configurado, en lugar de desde la cuenta de correo del sistema. Por ahora, esta función se limita a las invitaciones de calendario. Cuando se envía un mensaje del sistema, esta función asocia automáticamente la dirección de correo del usuario con una cuenta configurada de un proveedor de correo. Por ahora, la única app que admite esta función es Nextcloud Mail 4.1 o superior, y se requiere una cuenta de correo configurada.

### Configurar un servidor SMTP

Para conectar Nextcloud a un servidor SMTP remoto se necesita la siguiente información de quien administra el servidor de correo:

:::{warning}
Hubo cambios en la biblioteca de envío de correo de terceros en Nextcloud 26:

- STARTTLS no puede forzarse; se usa automáticamente si el servidor de correo lo admite. Establecer el tipo de cifrado en {guilabel}`Ninguno/STARTTLS` para permitir esta mejora automática. Consultar {nc-ref}`aquí <tlspeerverification>` un ejemplo de cómo configurar certificados autofirmados.
- La nueva biblioteca de envío no admite la autenticación NTLM para Microsoft Exchange. Probar en su lugar con la [autenticación básica](https://learn.microsoft.com/en-us/exchange/client-developer/exchange-web-services/authentication-and-ews-in-exchange#basic-authentication).
- Outlook y Microsoft Exchange han dejado de admitir la autenticación básica. Ya no es posible usar sus servicios como gestor de correo predeterminado.
:::

- Tipo de cifrado: Ninguno/STARTTLS o SSL
- La dirección de remitente que deben usar los correos salientes de Nextcloud
- Si se requiere autenticación
- Autenticación: cuando se requiere autenticación, la biblioteca de envío subyacente prueba los siguientes métodos de autenticación en el orden en que aparecen:

  - CramMd5
  - Login
  - Plain
  - XOAuth2

- La dirección IP o el nombre de dominio completo del servidor, y el puerto SMTP
- Las credenciales de inicio de sesión (si se requieren)

:::{note}
El parámetro `overwrite.cli.url` de `config.php` se usará para el EHLO de SMTP.
:::

Los cambios se guardan inmediatamente, y puede hacerse clic en el botón {guilabel}`Enviar mensaje` para probar la configuración. Esto envía un mensaje de prueba a la dirección de correo configurada en la página personal. El mensaje de prueba dice:

```
If you received this email, the settings seem to be correct.

--
Nextcloud
a safe home for all your data
```

### Configurar Sendmail/qmail

Para configurar Sendmail o qmail basta con seleccionar uno de ellos en lugar de SMTP y después introducir la dirección de correo de retorno deseada.

En la mayoría de los casos la opción `SMTP` es la mejor, ya que así todas las opciones del servidor de correo se controlan en un solo lugar: la configuración del servidor de correo.

### Usar plantillas de correo

{vendor}`Nextcloud` diseñó un mecanismo que genera correos que siguen los ajustes del tema y se ven igual en todos los distintos clientes de correo que existen.

:::{note}
Si por algún motivo se necesitan correos solo de texto, conviene simplemente configurarlo en el lado del cliente o dejar que el servidor de correo receptor (o incluso el emisor) descarte la parte HTML. Hay que tener en cuenta que **enviar** correos HTML no tiene ningún impacto en la seguridad; solo lo tiene mostrarlos, por lo que cualquier riesgo de seguridad solo puede mitigarse desactivando la visualización de HTML en el cliente (o eliminando la parte HTML en el servidor de correo).
:::

#### Modificar el aspecto de los correos más allá de las capacidades de la app de temas

Las plantillas pueden sobrescribirse escribiendo una clase que implemente la interfaz de plantilla (o que la extienda, para no tener que copiarlo todo). Lo más sencillo es después poner esta clase en una app y cargarla, para no tener que parchearla en cada actualización.

Esta es la interfaz de la clase que hay que implementar: <https://github.com/nextcloud/server/blob/master/lib/public/Mail/IEMailTemplate.php>

Esta es la implementación que podría extenderse y usarse para ver cómo funciona: <https://github.com/nextcloud/server/blob/master/lib/private/Mail/EMailTemplate.php>

Un ejemplo de [un artículo del portal de {vendor}`Nextcloud`](https://portal.nextcloud.com/article/customized-email-templates-29.html):

1. Revisar el código fuente de la clase extendida [OC\\Mail\\EMailTemplate::class](https://github.com/nextcloud/server/blob/master/lib/private/Mail/EMailTemplate.php)

2. Después, sobrescribir lo necesario en la extensión propia de *OC\\Mail\\EMailTemplate::class*

**Ejemplo:**

Supongamos que hay que sobrescribir la cabecera del correo:

```
<?php

namespace \OCA\MyApp;

use OC\Mail\EMailTemplate;

class MyClass extends EMailTemplate
{
   protected string $header = <<<EOF
      <table align="center" class="wrapper">
            // your theme email header modification
      </table>
   EOF;
}
```

3. Después, en `config/config.php`, cambiar `mail_template_class` al espacio de nombres de la clase propia:

   ```
   'mail_template_class' => 'OCA\\MyApp\\MyClass',
   ```

Hay una guía detallada paso a paso en el [portal de soporte de {vendor}`Nextcloud`](https://portal.nextcloud.com/article/customized-email-templates-29.html).

### Configurar los parámetros del servidor de correo en config.php

Si se prefiere, los parámetros del servidor de correo pueden establecerse en `config/config.php`. Los siguientes ejemplos son para SMTP, Sendmail y Qmail.

#### SMTP

Para enviar correo mediante un servidor SMTP local o remoto, hay que introducir el nombre o la dirección IP del servidor, seguido opcionalmente de un número de puerto separado por dos puntos, p. ej., **:425**. Si no se indica este valor, se usará el puerto predeterminado 25/tcp, a menos que se cambie modificando el parámetro **mail_smtpport**.

```
"mail_smtpmode"     => "smtp",
"mail_smtphost"     => "smtp.server.dom:425",
```

o

```
"mail_smtpmode"     => "smtp",
"mail_smtphost"     => "smtp.server.dom",
"mail_smtpport"     => 425,
```

Si en el servidor SMTP se ejecuta un analizador de malware o de SPAM, puede ser necesario aumentar el tiempo de espera de SMTP a, p. ej., 30s:

```
"mail_smtptimeout"  => 30,
```

Si el servidor SMTP acepta conexiones no seguras, puede usarse el ajuste predeterminado:

```
"mail_smtpsecure"   => '',
```

La conexión se actualizará automáticamente mediante STARTTLS si el servidor SMTP lo admite.

Si el servidor SMTP lo requiere, puede forzarse una conexión segura SSL/TLS mediante el protocolo SMTPS, que usa el puerto 465/tcp:

```
"mail_smtphost"     => "smtp.server.dom:465",
"mail_smtpsecure"   => 'ssl',
```

Por último, hay que configurar si el servidor SMTP requiere autenticación; si no la requiere, pueden dejarse los valores predeterminados tal cual.

```
"mail_smtpauth"     => false,
"mail_smtpname"     => "",
"mail_smtppassword" => "",
```

Si se requiere autenticación SMTP, hay que establecer el nombre de usuario y la contraseña requeridos.

```
"mail_smtpauth"     => true,
"mail_smtpname"     => "username",
"mail_smtppassword" => "password",
```

#### Sendmail

Para usar el conocido programa Sendmail para enviar correo, es necesario tener un sistema de correo instalado y en funcionamiento en el servidor \*nix. El binario sendmail (**/usr/sbin/sendmail**) suele formar parte de ese sistema. Nextcloud debería poder enviar correo sin configuración adicional.

```
"mail_smtpmode"     => "sendmail",
"mail_smtphost"     => "127.0.0.1",
"mail_smtpport"     => 25,
"mail_smtptimeout"  => 10,
"mail_smtpsecure"   => "",
"mail_smtpauth"     => false,
"mail_smtpauthtype" => "LOGIN",
"mail_smtpname"     => "",
"mail_smtppassword" => "",
```

#### qmail

Para usar el programa qmail para enviar correo, es necesario tener un sistema de correo qmail instalado y en funcionamiento en el servidor. Entonces se usará para enviar correo el binario qmail instalado en el servidor. Nextcloud debería poder enviar correo sin configuración adicional.

```
"mail_smtpmode"     => "qmail",
"mail_smtphost"     => "127.0.0.1",
"mail_smtpport"     => 25,
"mail_smtptimeout"  => 10,
"mail_smtpsecure"   => "",
"mail_smtpauth"     => false,
"mail_smtpauthtype" => "LOGIN",
"mail_smtpname"     => "",
"mail_smtppassword" => "",
```

### Enviar un correo de prueba

Para probar la configuración de correo, guardar la dirección de correo propia en los ajustes personales y después usar el botón {guilabel}`Enviar mensaje` de la sección {guilabel}`Servidor de correo electrónico` de la página de configuraciones de administración.

### Solución de problemas

#### Activar el modo de depuración

Si no es posible enviar correo, puede ser útil activar mensajes de depuración adicionales activando el parámetro `mail_smtpdebug` y estableciendo temporalmente el nivel de registro de NC en DEBUG:

```
"mail_smtpdebug" => true,
"loglevel" => 0,
```

Hay que tener cuidado al establecer `loglevel` en DEBUG (`0`), ya que se aplicará a todo lo que ocurra en la instancia de NC, no solo al correo. Y no olvidar devolverlo a un nivel más razonable al terminar de solucionar el problema:

```
"mail_smtpdebug" => false,
"loglevel" => 2,
```

:::{note}
Inmediatamente después de pulsar el botón {guilabel}`Enviar mensaje`, como se ha descrito antes, aparecen en pantalla varios mensajes **SMTP -> get_lines(): ...**. Es el comportamiento esperado y pueden ignorarse.
:::

#### ¿Por qué el dominio web es distinto del dominio de correo?

El nombre de dominio predeterminado que se usa en la dirección del remitente es el nombre de host desde el que se sirve la instalación de Nextcloud. Si se tiene un nombre de dominio de correo distinto, este comportamiento puede sustituirse estableciendo el siguiente parámetro de configuración:

```
"mail_domain" => "example.com",
```

Con este ajuste, en todos los correos que envía Nextcloud (por ejemplo, el de restablecimiento de contraseña) la parte de dominio de la dirección del remitente aparece así:

```
no-reply@example.com
```

#### ¿Cómo saber si un servidor SMTP es accesible?

Usar el comando ping para comprobar la disponibilidad del servidor:

```
ping smtp.server.dom
```

```
PING smtp.server.dom (ip-address) 56(84) bytes of data.
64 bytes from your-server.local.lan (192.168.1.10): icmp_req=1 ttl=64
time=3.64ms
```

#### ¿Cómo saber si el servidor SMTP escucha en un puerto TCP concreto?

La mejor forma de obtener información del servidor de correo es preguntar a quien lo administra. Si se administra el servidor de correo, o se necesita la información con urgencia, puede usarse el comando `netstat`. Este ejemplo muestra todos los servidores activos del sistema y los puertos en los que escuchan. El servidor SMTP escucha en el puerto 25 de localhost.

```
# netstat -pant
```

```
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address   Foreign Address  State  ID/Program name
tcp    0      0    0.0.0.0:631     0.0.0.0:*        LISTEN   4418/cupsd
tcp    0      0    127.0.0.1:25    0.0.0.0:*        LISTEN   2245/exim4
tcp    0      0    127.0.0.1:3306  0.0.0.0:*        LISTEN   1524/mysqld
```

- 25/tcp es smtp sin cifrar
- 110/tcp/udp es pop3 sin cifrar
- 143/tcp/udp es imap4 sin cifrar
- 465/tcp es submissions cifrado
- 587/tcp es submission con cifrado oportunista
- 993/tcp/udp es imaps cifrado
- 995/tcp/udp es pop3s cifrado

#### ¿Cómo determinar si el servidor SMTP admite el protocolo SMTPS?

Un buen indicio de que el servidor SMTP admite el protocolo SMTPS es que escuche en el puerto *submissions* **465**.

#### ¿Cómo determinar qué protocolos de autorización y cifrado admite el servidor de correo?

Los servidores SMTP suelen anunciar la disponibilidad de STARTTLS inmediatamente después de establecerse una conexión. Puede comprobarse fácilmente con el comando `telnet`.

:::{note}
Hay que introducir las líneas marcadas para obtener la información que se muestra.
:::

```
telnet smtp.domain.dom 25
```

```
Trying 192.168.1.10...
Connected to smtp.domain.dom.
Escape character is '^]'.
220 smtp.domain.dom ESMTP Exim 4.80.1 Tue, 22 Jan 2013 22:39:55 +0100
EHLO your-server.local.lan                   # <<< enter this command
250-smtp.domain.dom Hello your-server.local.lan [ip-address]
250-SIZE 52428800
250-8BITMIME
250-PIPELINING
250-AUTH PLAIN LOGIN CRAM-MD5                 # <<< Supported auth protocols
250-STARTTLS                                  # <<< Encryption is supported
250 HELP
QUIT                                          # <<< enter this command
221 smtp.domain.dom closing connection
Connection closed by foreign host.
```

(nc-tlspeerverification)=
#### ¿Cómo enviar correo con certificados autofirmados o usar STARTTLS con certificados autofirmados?

Para desactivar la verificación del par o usar certificados autofirmados, añadir lo siguiente a `config/config.php`:

```
"mail_smtpstreamoptions" => array(
    'ssl' => array(
        'allow_self_signed' => true,
        'verify_peer' => false,
        'verify_peer_name' => false
    )
),
```

#### Todos los correos se rechazan aunque solo una dirección de correo no sea válida.

El envío parcial, es decir, enviar a todas las direcciones excepto a la errónea, no es posible.

:::{note}
Inmediatamente después de pulsar el botón {guilabel}`Enviar mensaje`, como se ha descrito antes, aparecen en pantalla varios mensajes **SMTP -> get_lines(): ...**. Es el comportamiento esperado y pueden ignorarse.
:::
````
