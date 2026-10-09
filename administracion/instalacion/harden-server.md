---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Endurecer el servidor: contraseñas y tokens, sistema operativo, despliegue, HTTPS y HSTS, cabeceras, conexiones remotas y fail2ban."
---
# Endurecimiento y recomendaciones de seguridad

## Resumen

Esta página reúne las medidas adicionales de seguridad para un servidor bajo control total de su administración: cómo se guardan contraseñas y tokens, el sistema operativo, el despliegue, HTTPS y HSTS, las cabeceras de seguridad, las conexiones a servidores remotos y fail2ban. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/installation/harden_server.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

{vendor}`Nextcloud` procura que el software se distribuya con valores predeterminados seguros que los administradores no necesiten modificar. Sin embargo, en algunos casos puede aplicarse un endurecimiento de la seguridad adicional, en escenarios en los que el administrador tiene control total sobre la instancia de Nextcloud. Esta página supone que Nextcloud Server se ejecuta sobre Apache2 en un entorno Linux.

:::{note}
Nextcloud avisa en la interfaz de administración si faltan algunas opciones críticas para la seguridad. Sin embargo, sigue siendo responsabilidad del administrador del servidor revisar y mantener la seguridad del sistema.
:::

### Contraseñas

#### Almacenamiento de las contraseñas de las cuentas

El backend de usuarios de base de datos integrado en Nextcloud guarda un hash unidireccional con sal de la contraseña de cada cuenta. Prefiere Argon2id (cuando la instalación de PHP lo admite) y usa Argon2i y bcrypt como alternativas. El algoritmo, la sal y los parámetros de coste se incluyen en el hash guardado. Los hashes existentes se actualizan automáticamente tras una verificación de contraseña correcta cuando ya no coinciden con el algoritmo o los parámetros preferidos.

El hash se usa para verificar los intentos de inicio de sesión con contraseña y no está pensado para descifrarse. Cuando se usa un backend de usuarios externo (como LDAP), el almacenamiento y la verificación de la contraseña de la cuenta los controla ese backend.

Este hash de la contraseña de la cuenta es independiente de cualquier copia recuperable de la contraseña de inicio de sesión que Nextcloud guarde en relación con los tokens de autenticación, como se describe a continuación.

#### Almacenamiento de los tokens de autenticación

Tras una autenticación correcta, Nextcloud emite un token de autenticación que el cliente presenta en las siguientes peticiones autenticadas. Un token válido puede autenticarse como el usuario asociado, sujeto al alcance, la caducidad y el tipo del token y a las comprobaciones de validez del lado del servidor. Según el tipo de token y el cliente, el token puede transmitirse en una cookie de sesión, usarse como contraseña de aplicación o enviarse como bearer token.

Nextcloud no guarda en la base de datos el token de autenticación en texto plano. En su lugar, guarda un hash SHA-512 derivado del token y del `secret` propio de la instancia. El registro del token correspondiente en el servidor contiene la identidad del usuario asociado, metadatos de autenticación y material de claves criptográficas. Por tanto, los tokens de autenticación deben protegerse como contraseñas. No deben escribirse en los registros, ponerse en URL ni conservarse intencionadamente fuera del cliente que los usa.

#### Almacenamiento de contraseñas de inicio de sesión asociado a los tokens

De forma predeterminada, `auth.storeCryptedPassword` está habilitado. Cuando este ajuste está habilitado y la contraseña de inicio de sesión está disponible durante la creación del token, Nextcloud guarda una copia cifrada de forma reversible de esa contraseña en el registro del token de autenticación del servidor.

En una cuenta que usa el backend de usuarios de base de datos integrado, esta copia cifrada es independiente del hash unidireccional de la contraseña de la cuenta. La base de datos contiene el hash unidireccional de la contraseña de la cuenta y también una copia cifrada de la contraseña por cada registro de token de autenticación creado con el almacenamiento de contraseñas habilitado y con una contraseña de inicio de sesión proporcionada.

La copia recuperable la usan las funciones que necesitan las credenciales de inicio de sesión originales, como la conexión a almacenamiento externo, la configuración automática de cuentas en la app Mail y la comprobación periódica de que las credenciales de inicio de sesión siguen siendo válidas. Cuando la creación del token no recibe ninguna contraseña de inicio de sesión, el registro del token resultante no contiene ninguna contraseña recuperable. Ese registro de token sigue sin contraseña guardada hasta que Nextcloud recibe la contraseña en un inicio de sesión o una actualización de contraseña posteriores.

El propio token de autenticación no contiene la contraseña de inicio de sesión. Cada registro de token tiene un par de claves RSA propio. Nextcloud cifra la contraseña de inicio de sesión con la clave pública del registro y cifra la clave privada correspondiente con el token de autenticación junto con el `secret` propio de la instancia, de `config.php`. Por tanto, tener el token de autenticación, el secreto de la instancia y el registro correspondiente de la base de datos basta para descifrar una contraseña guardada en ese registro.

Los administradores pueden desactivar este comportamiento con `auth.storeCryptedPassword`. Desactivarlo no afecta al hash unidireccional de la contraseña de la cuenta que usa el backend de usuarios de base de datos integrado. Las funciones que dependen de recuperar la contraseña de inicio de sesión de un registro de token de autenticación no pueden obtenerla de los registros creados sin contraseña guardada.

Cuando un token de autenticación contiene una contraseña guardada, Nextcloud comprueba periódicamente esa contraseña contra el backend de usuarios. Si la contraseña ya no es válida, Nextcloud marca el token como poseedor de una contraseña no válida y rechaza la autenticación con ese token. Cuando el token no contiene ninguna contraseña guardada, Nextcloud omite esta comprobación de la contraseña. En consecuencia, cambiar una contraseña directamente en un backend de usuarios externo no hace que un token sin contraseña guardada se rechace mediante la comprobación periódica de credenciales. El cambio de contraseña por sí solo no invalida el token; el token sigue siendo válido hasta que caduca, se invalida de otro modo o se desactiva el usuario.

#### Consecuencias para la seguridad

La filtración de datos de autenticación tiene las siguientes consecuencias para la seguridad:

- Quien tenga un token de autenticación válido puede autenticarse como el usuario asociado, sujeto al alcance, la caducidad y el tipo del token y a las comprobaciones de validez del lado del servidor.
- Quien tenga el token de autenticación, el `secret` propio de la instancia de `config.php` y el registro correspondiente de la base de datos puede descifrar la contraseña de inicio de sesión guardada en ese registro.
- Un hash de contraseña de cuenta no revela directamente la contraseña original, pero quien lo obtenga puede realizar ataques de adivinación de contraseñas sin conexión.

(nc-password_length_limits)=
#### Límites de longitud de las contraseñas

Nextcloud acepta contraseñas de cuenta de hasta 469 bytes en sus interfaces estándar de creación de cuentas, cambio de contraseña y restablecimiento de contraseña. Es la longitud máxima de contraseña de cuenta que imponen estas interfaces. Como el límite se mide en bytes, una contraseña con caracteres multibyte (como emojis o caracteres de escrituras no latinas) puede alcanzar el límite con menos de 469 caracteres.

Los administradores pueden usar la {nc-doc}`app Password Policy <admin_manual/configuration_user/user_password_policy>` para configurar requisitos como una longitud mínima de contraseña y otras reglas de complejidad. Los backends de usuarios externos pueden imponer requisitos adicionales o diferentes.

Los siguientes detalles de implementación no cambian el máximo de 469 bytes para las contraseñas de cuenta, pero son relevantes al elegir una política de contraseñas:

- Rendimiento del cifrado de tokens: cuando `auth.storeCryptedPassword` está habilitado y la contraseña de una cuenta tiene más de 214 bytes, Nextcloud usa una clave RSA más grande al crear los registros de tokens de autenticación. Esto aumenta la carga de la generación de tokens, pero no impide que se acepten contraseñas de entre 215 y 469 bytes. Por tanto, el umbral de 214 bytes es una cuestión de rendimiento, no un límite de longitud de contraseña.

  Los administradores que esperen que se usen contraseñas muy largas o de un solo uso pueden plantearse desactivar `auth.storeCryptedPassword` para evitar esta carga, con las consecuencias funcionales descritas arriba.
- Truncamiento algorítmico (alternativa bcrypt): Nextcloud prefiere Argon2id para el hash unidireccional de contraseñas (cuando la instalación de PHP lo admite), con Argon2i y bcrypt como alternativas. Bcrypt solo tiene en cuenta los primeros 72 bytes de su entrada. Por tanto, si se selecciona bcrypt, lo que va después de los primeros 72 bytes no contribuye a la verificación de la contraseña. Es un comportamiento propio de bcrypt, no un límite general de 72 bytes impuesto por Nextcloud.

Las contraseñas que protegen los recursos compartidos mediante enlace público y por correo usan el mismo hasher unidireccional de contraseñas y están sujetas a la política de contraseñas de recursos compartidos aplicable. No se guardan en registros de tokens de autenticación, así que no se les aplican las consideraciones de rendimiento relacionadas con el cifrado descritas arriba.

### Sistema operativo

(nc-dev-urandom-label)=
#### Dar a PHP acceso de lectura a `/dev/urandom`

Nextcloud usa un mezclador conforme con [RFC 4086 («Randomness Requirements for Security»)][RFC 4086 ("Randomness Requirements for Security")] para generar números pseudoaleatorios criptográficamente seguros. Esto significa que, al generar un número aleatorio, Nextcloud pide varios números aleatorios a distintas fuentes y deriva de ellos el número aleatorio final.

La generación de números aleatorios también intenta pedir números aleatorios a `/dev/urandom`, por lo que se recomienda encarecidamente configurar el entorno de forma que PHP pueda leer datos aleatorios de él.

:::{note}
Si hay un `open_basedir` configurado en el archivo `php.ini`, asegurarse de incluir `/dev/urandom`.
:::

#### Activar módulos de endurecimiento como SELinux

Se recomienda encarecidamente activar módulos de endurecimiento como SELinux siempre que sea posible. Ver {nc-doc}`admin_manual/installation/selinux_configuration` para saber más sobre SELinux.

### Despliegue

#### Ubicar el directorio de datos fuera del web root

Se recomienda encarecidamente ubicar el directorio de datos fuera del Web root (es decir, fuera de `/var/www`). Lo más fácil es hacerlo en una instalación nueva.

(nc-harden_config_dir)=
#### Ubicar el directorio de configuración fuera del web root

El directorio `config/` puede moverse fuera del web root con la variable de entorno `NEXTCLOUD_CONFIG_DIR`. Así se garantiza que `config.php`, que contiene las credenciales de la base de datos, claves secretas y otros valores sensibles, no sea accesible por HTTP ni siquiera si el servidor web está mal configurado.

Definir la variable en la configuración del virtual host del servidor web:

```apache
# Apache
SetEnv NEXTCLOUD_CONFIG_DIR /etc/nextcloud
```

```nginx
# nginx — set via fastcgi_param or the PHP-FPM pool's env[] setting
fastcgi_param NEXTCLOUD_CONFIG_DIR /etc/nextcloud;
```

Definirla también para el trabajo en la línea de comandos (`occ`, cron):

```bash
export NEXTCLOUD_CONFIG_DIR=/etc/nextcloud
```

:::{note}
La variable debe definirse **tanto** para el proceso del servidor web como para las invocaciones en la línea de comandos. Verificarlo con `occ config:list system` después de cambiarla.
:::

:::{seealso}
{nc-doc}`admin_manual/configuration_server/config_sample_php_parameters` para ver todos los detalles sobre `NEXTCLOUD_CONFIG_DIR` y otros aspectos de la carga de la configuración.
:::

#### Desactivar la generación de imágenes de vista previa

Nextcloud puede generar imágenes de vista previa de tipos de archivo habituales, como imágenes o archivos de texto. De forma predeterminada está habilitada la generación de vistas previas para algunos tipos de archivo que consideramos lo bastante seguros para el despliegue. Sin embargo, los administradores deben saber que estas vistas previas se generan con bibliotecas de PHP escritas en C que podrían ser vulnerables a vectores de ataque.

Para despliegues de alta seguridad, recomendamos desactivar la generación de vistas previas poniendo el interruptor `enable_previews` en `false` en `config.php`. Como administrador, también se puede gestionar qué proveedores de vistas previas están habilitados modificando la opción `enabledPreviewProviders`.

#### Desactivar el modo de depuración

Verificar que `debug` es `false` en `config.php`. El valor predeterminado es `false` en las instalaciones nuevas (o cuando no se indica). No debe habilitarse en entornos de producción ni fuera de situaciones concretas de resolución de problemas. Cuando está habilitado, se permiten cosas como los listados de colecciones WebDAV de todo el servidor. Está pensado solo para el desarrollo local y el uso en entornos controlados.

(nc-use_https_label)=
### Usar HTTPS

Usar Nextcloud sin una conexión HTTPS cifrada expone el servidor a un ataque de intermediario (MITM) y pone en riesgo la interceptación de datos y contraseñas de los usuarios. Es una buena práctica, muy recomendable, usar siempre HTTPS en los servidores de producción y no permitir nunca HTTP sin cifrar.

Cómo configurar HTTPS en el servidor web depende de cada instalación; consultar la documentación del servidor HTTP. Los siguientes ejemplos son para Apache.

#### Redirigir todo el tráfico sin cifrar a HTTPS

Para redirigir todo el tráfico HTTP a HTTPS, se recomienda a los administradores emitir una redirección permanente con el código de estado 301. Con Apache puede lograrse con un ajuste como el siguiente en la configuración de los VirtualHosts de Apache:

```
<VirtualHost *:80>
   ServerName cloud.nextcloud.com
   Redirect permanent / https://cloud.nextcloud.com/
</VirtualHost>
```

(nc-enable-hsts-label)=
#### Activar HTTP Strict Transport Security

Aunque redirigir todo el tráfico a HTTPS es bueno, puede no evitar por completo los ataques de intermediario. Por eso se recomienda a los administradores definir la cabecera HTTP Strict Transport Security, que indica a los navegadores que no permitan ninguna conexión a la instancia de Nextcloud por HTTP e intenta impedir que los visitantes del sitio pasen por alto las advertencias de certificado no válido.

Puede lograrse definiendo los siguientes ajustes en el archivo VirtualHost de Apache:

```
<VirtualHost *:443>
  ServerName cloud.nextcloud.com
    <IfModule mod_headers.c>
      Header always set Strict-Transport-Security "max-age=15552000; includeSubDomains"
    </IfModule>
 </VirtualHost>
```

:::{warning}
Recomendamos añadir a esa cabecera el ajuste adicional `; preload`. Así, el dominio se añadirá a una lista fija que se distribuye con todos los navegadores principales, que imponen HTTPS en esos dominios. Ver el [sitio web de HSTS preload para más información](https://hstspreload.org/). Por la política de esta lista, hay que añadirlo uno mismo al ejemplo anterior una vez que se esté seguro de que es lo que se quiere. [Quitar el dominio de esta lista](https://hstspreload.org/#removal) podría tardar algunos meses hasta llegar a todos los navegadores instalados.
:::

Esta configuración de ejemplo hace que todos los subdominios solo sean accesibles por HTTPS. Si hay subdominios que no son accesibles por HTTPS, quitar `includeSubDomains`.

Esto requiere la extensión `mod_headers` de Apache.

#### Configuración SSL adecuada

Las configuraciones SSL predeterminadas de los servidores web a menudo no están al día y requieren ajustes finos para lograr un rendimiento y una seguridad óptimos. Los cifrados y las opciones SSL disponibles dependen por completo de cada entorno, por lo que no es realmente posible dar una recomendación genérica.

Recomendamos usar el [Mozilla SSL Configuration Generator][Mozilla SSL Configuration Generator] para generar una configuración adecuada para el entorno. Para verificar la configuración puede usarse el servicio gratuito [Web TLS Profiler][Web TLS Profiler]. Este servicio da mensajes de error detallados si los ajustes TLS del servidor se apartan de la configuración de Mozilla. Otra herramienta útil para comprobar la configuración TLS del servidor es el gratuito [Qualys SSL Labs Test][Qualys SSL Labs Test], que ofrece información general sobre los ajustes TLS.

Asegurarse también de que la compresión HTTP está desactivada para mitigar el ataque BREACH.

### Restringir las acciones de administración a un rango concreto de direcciones IP

Configurar `allowed_admin_ranges` en `config.php` para restringir las acciones de administración a rangos de IP de confianza.

Puede lograrse con un ajuste de este tipo, normalmente con rangos de IP privados:

```
'allowed_admin_ranges' => [
  '127.0.0.1/8',
  '192.168.0.0/16',
  'fd00::/8',
],
```

Ninguna petición que provenga de direcciones IP fuera de estos rangos podrá ejecutar acciones de administración.

Los administradores conectados desde direcciones IP que no son de confianza podrán usar Nextcloud, pero todas las acciones específicas de administración quedarán ocultas.

### Usar un dominio dedicado para Nextcloud

Se recomienda a los administradores instalar Nextcloud en un dominio dedicado, como cloud.domain.tld en lugar de domain.tld, para obtener todas las ventajas que ofrece la Same-Origin-Policy.

### Asegurarse de que la instancia de Nextcloud está instalada en una DMZ

Como Nextcloud admite funciones como la compartición federada de archivos, no consideramos la falsificación de peticiones del lado del servidor (SSRF) parte de nuestro modelo de amenazas. De hecho, dados todos nuestros adaptadores de almacenamiento externo, puede considerarse una función y no una vulnerabilidad.

Esto significa que un usuario de la instancia de Nextcloud podría sondear si otros hosts son accesibles desde la red de Nextcloud. Si no se quiere esto, hay que asegurarse de que Nextcloud está correctamente instalado en una red segregada y de que hay reglas de cortafuegos adecuadas.

### Servir las cabeceras relacionadas con la seguridad desde el servidor web

Nextcloud ya sirve cabeceras de seguridad básicas en un entorno predeterminado. Entre ellas:

- `X-Content-Type-Options: nosniff`
  - Indica a algunos navegadores que no deduzcan el tipo MIME de los archivos. Se usa, por ejemplo, para evitar que los navegadores interpreten archivos de texto como JavaScript.
- `X-Robots-Tag: noindex, nofollow`
  - Indica a los motores de búsqueda que no indexen estas páginas ni sigan sus enlaces.
- `X-Frame-Options: SAMEORIGIN`
  - Impide incrustar la instancia de Nextcloud en un iframe desde otros dominios, para evitar el clickjacking y otros ataques similares.
- `Referrer-Policy: no-referrer`
  - La política predeterminada *no-referrer* indica al navegador que no envíe información del referente junto con las peticiones a ningún origen.

Estas cabeceras están fijadas en el código del servidor Nextcloud y no requieren ninguna intervención del administrador del servidor.

Para una seguridad óptima, se recomienda a los administradores servir estas cabeceras HTTP básicas desde el servidor web para imponerlas en la respuesta. Para ello, Apache debe configurarse para usar el archivo `.htaccess` y deben estar habilitados los siguientes módulos de Apache:

- mod_headers
- mod_env

Los administradores pueden verificar si este cambio de seguridad está activo accediendo a un recurso estático servido por el servidor web y comprobando que se envían las cabeceras de seguridad mencionadas.

(nc-connections_to_remote_servers)=
### Conexiones a servidores remotos

Algunas funciones requieren que el servidor Nextcloud pueda conectarse a sistemas remotos mediante https/443. Este apartado incluye también los datos que se transmiten a Nextcloud GmbH. Según la configuración del servidor, estas son las conexiones posibles:

- connectivity.nextcloud.com, www.eff.org, edri.org
  - [opcional (config)][optional (config)]
  - para comprobar la conexión a internet
- cloud.nextcloud.com
  - se usa para supervisar las licencias empresariales
  - datos enviados: clave de suscripción, número de usuarios
- updates.nextcloud.com
  - para comprobar si hay actualizaciones disponibles del servidor Nextcloud
  - datos enviados: versión del servidor, clave de suscripción, fecha de instalación, id de la instancia, tamaño de la instancia
- apps.nextcloud.com, ltd[1-3].nextcloud.com, garm[1-5].nextcloud.com
  - para comprobar si hay apps disponibles y sus actualizaciones
  - el origen es apps.nextcloud.com; los servidores ltd y garm solo replican el archivo apps.json
  - datos enviados: clave de suscripción
- github.com, objects.githubusercontent.com, release-assets.githubusercontent.com
  - para descargar las apps estándar de Nextcloud
  - para descargar las versiones del servidor Nextcloud
- push-notifications.nextcloud.com
  - envío de notificaciones push a los clientes móviles
  - datos enviados: identificador único del dispositivo, clave pública, token push
- pushfeed.nextcloud.com
  - opcional
  - comprobar si hay novedades que mostrar en la app Nextcloud Announcements
- lookup.nextcloud.com
  - opcional
  - para actualizar y consultar la libreta de direcciones de la compartición federada
  - datos enviados: *pendiente*
- surveyserver.nextcloud.com
  - opcional
  - si el administrador ha aceptado compartir datos anonimizados del servidor
  - datos enviados: datos estadísticos. ver aquí la [lista detallada de campos][detailed field list]
- nominatim.openstreetmap.org
  - opcional
  - si la app de estado del tiempo está habilitada y en uso
  - datos enviados: dirección introducida manualmente por el usuario para convertirla en longitud y latitud
- api.opentopodata.org
  - opcional
  - si la app de estado del tiempo está habilitada y en uso
  - datos enviados: dirección introducida manualmente por el usuario para obtener la altitud de la ubicación
- api.met.no
  - opcional
  - si la app de estado del tiempo está habilitada y en uso
  - datos enviados: longitud y latitud configuradas en la app de estado del tiempo por cada usuario
- Cualquier servidor Nextcloud remoto conectado mediante compartición federada
- Al descargar apps de la tienda de aplicaciones podría accederse a otros dominios, según dónde decidan alojar las versiones los desarrolladores de las apps. Sin embargo, no es el caso de ninguna app oficial de {vendor}`Nextcloud`, porque están alojadas en Github.

(nc-setup_fail2ban)=
### Configurar fail2ban

Exponer el servidor a internet conlleva inevitablemente que los servicios que se ejecutan en los puertos expuestos a internet queden expuestos a intentos de inicio de sesión por fuerza bruta.

Esta guía permite bloquear las direcciones IP de origen a nivel del sistema operativo, de modo que el servidor web, PHP y la base de datos no tengan que gestionar en absoluto este tráfico innecesario.

#### Requisitos previos de Nextcloud

Nextcloud registra los intentos de inicio de sesión fallidos en `nextcloud.log` con el nivel de registro `2`, así que hay que definir un `loglevel` de `2` o menos en `config.php`.

Asegurarse de que el usuario del servidor web puede escribir en `nextcloud.log`, si es necesario definiendo un `logfilemode` correcto en `config.php`.

Hacer un intento de inicio de sesión incorrecto y comprobar si queda registrado en `nextcloud.log`.

Tener en cuenta que `audit.log` (si está habilitado) actualmente solo registra los inicios de sesión correctos y no puede usarse.

#### Introducción a Fail2ban

Fail2ban es un servicio que usa iptables para descartar automáticamente, durante un tiempo predefinido, las conexiones de las IP que fallan continuamente al autenticarse en los servicios configurados.

Para configurar fail2ban, primero hay que descargarlo e instalarlo en el servidor. Las descargas para varias distribuciones están en la [página de descargas de fail2ban][fail2ban download page]. A menudo está disponible en los gestores de paquetes de la mayoría de las distribuciones (p. ej., `apt-get`).

La ruta estándar de la configuración de fail2ban es `/etc/fail2ban`.

#### Configurar un filtro y una jaula para Nextcloud

Un filtro define reglas de expresiones regulares para identificar cuándo los usuarios no consiguen autenticarse en la interfaz de usuario de Nextcloud o en WebDAV, o usan un dominio que no es de confianza para acceder al servidor.

Crear en `/etc/fail2ban/filter.d` un archivo llamado `nextcloud.conf` con el siguiente contenido:

```
[Definition]
_groupsre = (?:(?:,?\s*"\w+":(?:"[^"]+"|\w+))*)
failregex = ^\{%(_groupsre)s,?\s*"remoteAddr":"<HOST>"%(_groupsre)s,?\s*"message":"Login failed:
            ^\{%(_groupsre)s,?\s*"remoteAddr":"<HOST>"%(_groupsre)s,?\s*"message":"Two-factor challenge failed:
            ^\{%(_groupsre)s,?\s*"remoteAddr":"<HOST>"%(_groupsre)s,?\s*"message":"Trusted domain error.
datepattern = ,?\s*"time"\s*:\s*"%%Y-%%m-%%d[T ]%%H:%%M:%%S(%%z)?"
```

El archivo de la jaula define cómo tratar los intentos de autenticación fallidos que encuentra el filtro de Nextcloud.

Crear en `/etc/fail2ban/jail.d` un archivo llamado `nextcloud.local` con el siguiente contenido:

```
[nextcloud]
backend = auto
enabled = true
port = 80,443
protocol = tcp
filter = nextcloud
maxretry = 3
bantime = 86400
findtime = 43200
logpath = /path/to/data/directory/nextcloud.log
```

Asegurarse de reemplazar `logpath` por la ubicación del `nextcloud.log` de la instalación. Si el servidor web usa puertos distintos de `80` y `443`, hay que reemplazarlos también. `bantime` y `findtime` se definen en segundos.

Reiniciar el servicio fail2ban. El estado de la jaula de Nextcloud puede comprobarse ejecutando:

```
fail2ban-client status nextcloud
```

Si hay que desbloquear ciertas direcciones IP (`1.2.3.4` en este ejemplo), puede hacerse ejecutando:

```
fail2ban-client unban 1.2.3.4
```

Puede haber escenarios en los que se quiera bloquear de forma más permanente ciertas direcciones IP que generan repetidamente intentos de inicio de sesión incorrectos (u otros ataques), con la función `recidive` de fail2ban.

[RFC 4086 ("Randomness Requirements for Security")]: https://tools.ietf.org/html/rfc4086#section-5.2
[Mozilla SSL Configuration Generator]: https://mozilla.github.io/server-side-tls/ssl-config-generator/
[Web TLS Profiler]: https://tlsprofiler.danielfett.de/
[Qualys SSL Labs Test]: https://www.ssllabs.com/ssltest/
[optional (config)]: https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/config_sample_php_parameters.html#has-internet-connection
[detailed field list]: https://github.com/nextcloud/survey_client
[fail2ban download page]: https://www.fail2ban.org/wiki/index.php/Downloads
````
