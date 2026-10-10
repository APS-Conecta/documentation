---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo probar en desarrollo el envío de correo, Redis, almacenamiento S3 y SMB, SAML, OnlyOffice, Collabora sin SSL y WebAuthn sin SSL."
---
# Cómo probar ...

## Resumen

Esta página reúne recetas para probar funciones concretas en un entorno de desarrollo local: envío de correo, Redis y su clúster, almacenamiento de objetos primario y externo con S3, almacenamiento externo SMB, SAML con onelogin, OnlyOffice con un certificado autofirmado, Collabora sin SSL y WebAuthn sin SSL. Está dirigida a quienes desarrollan sobre la plataforma.

````{upstream} developer_manual/how_to/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Esta página debería explicar cómo probar determinadas funciones en Nextcloud.

### Envío de correo electrónico

```
docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
occ config:system:set mail_smtpmode --value=smtp
occ config:system:set mail_smtphost --value=127.0.0.1
occ config:system:set mail_smtpport --value=1025 --type=integer
```

Luego, después de hacer que Nextcloud envíe algunos correos, abrir <http://127.0.0.1:8025> para verlos.

### Redis

Primero hay que instalar la [extensión phpredis](https://github.com/phpredis/phpredis). Hay un documento de instalación disponible [dentro del repositorio](https://github.com/phpredis/phpredis/blob/develop/INSTALL.markdown), y muchas distribuciones de Linux también la incluyen en sus repositorios.

> pecl install redis

### Clúster de Redis

Para montar un clúster de Redis local hay algunos scripts de Docker reunidos en [este repositorio](https://github.com/Grokzen/docker-redis-cluster). Basta con clonar el repositorio y ejecutar *make up*. Después, el clúster de Redis queda disponible en `localhost:7000`.

Puede usarse el siguiente `config.php`:

```
'memcache.distributed' => '\OC\Memcache\Redis',
'redis.cluster' => [
   'seeds' => [ // provide some/all of the cluster servers to bootstrap discovery, port required
      'localhost:7000',
   ],
   'timeout' => 0.0,
   'read_timeout' => 0.0,
   'failover_mode' => \RedisCluster::FAILOVER_ERROR,
],
```

### Almacenamiento de objetos primario con S3

```
docker run -p 9000:9000 minio/minio server /data
```

Después, editar `config.php` y añadir la siguiente sección:

```
'objectstore' =>
    array (
        'class' => 'OC\\Files\\ObjectStore\\S3',
        'arguments' =>
        array (
            'bucket' => 'nextcloud-dev',
            'key' => 'minioadmin',
            'secret' => 'minioadmin',
            'hostname' => 'localhost',
            'port' => '9000',
            'use_ssl' => false,
            'use_path_style' => true,
        ),
    ),
```

### Almacenamiento externo S3

```
occ app:enable files_external

docker run -p 9000:9000 minio/minio server /data
```

Después, añadir un almacenamiento externo en la interfaz web con la siguiente configuración:

- Tipo de autenticación: Clave de acceso
- Clave de acceso: minioadmin
- Clave secreta: minioadmin
- Bucket: nextcloud-dev
- Dirección del servidor: localhost
- Puerto: 9000
- Región: dejar vacío
- Clase de almacenamiento: dejar vacío
- Habilitar SSL: false
- Habilitar Estilo de Ruta: sí

### Almacenamiento externo SMB

El almacenamiento externo SMB puede probarse con Docker. Los siguientes comandos crean un servidor SMB con un directorio público (compartido) y directorios personales de usuario para las credenciales `smb1:pwd1` y `smb2:pwd2`.

```
occ app:enable files_external

mkdir -p /tmp/samba/{public,home/{smb1,smb2}}
chmod a+rw /tmp/samba/home/smb*
docker run -it -p 139:139 -p 445:445 \
    -v /tmp/samba/public:/smbpublic \
    -v /tmp/samba/home:/smbhome \
    dperson/samba \
    -u "smb1;pwd1" \
    -u "smb2;pwd2" \
    -s "public;/smbmount;yes;no;yes" \
    -s "home;/smbhome/%U;yes;no;no;all;none"
```

Hay que asegurarse de que smbclient esté instalado en el servidor de Nextcloud y tenga la siguiente configuración:

```
# /etc/samba/smb.conf
[global]
client min protocol = SMB2
client max protocol = SMB3
hide dot files = no
```

La configuración puede verificarse con

```
smbclient //127.0.0.1/public -U smb1                 # Shared storage for all users
smbclient //127.0.0.1/home -U smb1 --password=pwd1   # Home storage
```

### Configuración de SAML con onelogin

- crear una cuenta de desarrollador en onelogin.com
- iniciar sesión en onelogin.com
- crear una app nueva: SAML Test Connector (Advanced)
    - ir a «Configuration»
        - Audience: <https://localhost/apps/user_saml/saml/metadata>
        - Recipient: <https://localhost/apps/user_saml/saml/acs>
        - ACS (Consumer) URL Validator: <https://localhost/apps/user_saml/saml/acs>
    - ir a «Parameters»
        - Añadir «User.email» -> email (y añadirlo a la aserción)
        - Añadir «User.FirstName» -> first name (y añadirlo a la aserción)
        - Añadir «User.LastName» -> last name (y añadirlo a la aserción)
- abrir los ajustes de SAML de Nextcloud
    - Seleccionar SAML
    - Configurarlo según <https://portal.nextcloud.com/article/configuring-single-sign-on-10.html>

### Collabora sin SSL

**1) Iniciar Collabora en un contenedor de Docker**

```
docker run -p 127.0.0.1:9980:9980 -e 'domain=172.17.0.1' \
    -e 'username=admin' -e 'password=487903ffcf4' \
    -e extra_params='--o:ssl.enable=false' \
    --restart always --cap-add MKNOD collabora/code
```

- 172.17.0.1 es localhost, que es el valor predeterminado de Docker
- obtener la IP del contenedor de Collabora: docker inspect --format='{{ .NetworkSettings.IPAddress }}' $containerName

* **2) Configurar Nextcloud**:
    - ir a la nube local (p. ej., 172.17.0.1/nc) -> Ajustes -> Collabora:
        - establecer como URL la IP averiguada arriba, p. ej.: <http://172.17.0.2:9980>
        - marcar «Desactivar la verificación de certificados (inseguro)»
* **3) Uso**:
    - tener en cuenta que no se puede usar con localhost, sino que hay que introducir una dirección IP válida de localhost
    - con este método también se puede usar con clientes móviles
* **4) Solución de problemas**:
    - <http://172.17.0.2:9980/hosting/capabilities> debería devolver:

```
{"convert-to":{"available":false},"hasMobileSupport":true,"hasTemplateSaveAs":true,"productName":"Collabora Online Development Edition"}
```

### OnlyOffice

1. Crear un certificado autofirmado; debería estar en una ruta permanente:

   ```
   mkdir -p /tmp/oo/certs
   cd /tmp/oo/certs
   openssl genrsa -out onlyoffice.key 4096
   openssl req -new -key onlyoffice.key -out onlyoffice.csr
   openssl x509 -req -days 3650 -in onlyoffice.csr -signkey onlyoffice.key -out onlyoffice.crt
   openssl dhparam -out dhparam.pem 4096
   chmod 400 onlyoffice.key
   chmod 400 onlyoffice.crt
   chmod 400 onlyoffice.csr
   chmod 400 dhparam.pem
   ```

2. Iniciar Docker; importante: no usar la carpeta certs, sino su carpeta superior:

   ```
   docker run --name=ONLYOFFICEDOCKER -i -t -d -p 4433:443 \
   -e JWT_ENABLED='true' -e JWT_SECRET='secret' --restart=always \
   -v /tmp/oo/:/var/www/onlyoffice/Data onlyoffice/documentserver
   ```

3. Entrar en el contenedor de Docker:

   - docker exec -it ONLYOFFICEDOCKER /bin/bash
   - apt-get update
   - apt-get install vim -y
   - vim /etc/onlyoffice/documentserver/default.json
     - cambiar rejectUnauthorized a false
   - vim /etc/onlyoffice/documentserver/local.json
     - cambiar token -> inbox -> header a «AuthorizationJWT»
     - cambiar token -> outbox -> header a «AuthorizationJWT»
   - Añadir lo siguiente a config.php

   ```
   'onlyoffice' => array (
       'verify_peer_off' => true,
       'jwt_secret' => 'secret',
       'jwt_header' => 'AuthorizationJWT'
   ),
   ```

- Probar con la IP local: <https://localhost:4433>
    - aceptar la advertencia del certificado
    - verificar que se muestre «Document Server is running»
- Probar con Nextcloud:
    - descargar y activar la app OnlyOffice
    - configurar:
        - «Document Editing Service address»: <https://localhost:4433/>
        - «Secret key»: secret (como arriba)
        - «Document Editing Service address for internal requests from the server»: <https://localhost:4433/>
        - «Server address for internal requests from the Document Editing Service»: <http://192.168.1.95/nc16/> (tiene que ser una dirección IP real, ya que localhost apunta a Docker)

### WebAuthn sin SSL

[Chrome ofrece la opción de probar WebAuthn con un dispositivo simulado](https://developer.chrome.com/docs/devtools/webauthn/). Los navegadores admiten WebAuthn en sitios protegidos con HTTPS y en dominios localhost. Lamentablemente, la biblioteca PHP utilizada no lo admite, por lo que hay que comentar la comprobación de HTTPS para hacer pruebas en entornos de desarrollo localhost sin HTTPS.

```
diff --git a/3rdparty/web-auth/webauthn-lib/src/AuthenticatorAssertionResponseValidator.php b/3rdparty/web-auth/webauthn-lib/src/AuthenticatorAssertionResponseValidator.php
index 8400ba9c..49279cc7 100644
--- a/3rdparty/web-auth/webauthn-lib/src/AuthenticatorAssertionResponseValidator.php
+++ b/3rdparty/web-auth/webauthn-lib/src/AuthenticatorAssertionResponseValidator.php
@@ -152,7 +152,7 @@ class AuthenticatorAssertionResponseValidator
             Assertion::isArray($parsedRelyingPartyId, 'Invalid origin');
             if (!in_array($facetId, $securedRelyingPartyId, true)) {
                 $scheme = $parsedRelyingPartyId['scheme'] ?? '';
-                Assertion::eq('https', $scheme, 'Invalid scheme. HTTPS required.');
+                #Assertion::eq('https', $scheme, 'Invalid scheme. HTTPS required.');
             }
             $clientDataRpId = $parsedRelyingPartyId['host'] ?? '';
             Assertion::notEmpty($clientDataRpId, 'Invalid origin rpId.');
diff --git a/3rdparty/web-auth/webauthn-lib/src/AuthenticatorAttestationResponseValidator.php b/3rdparty/web-auth/webauthn-lib/src/AuthenticatorAttestationResponseValidator.php
index f3e5a15d..3927bf23 100644
--- a/3rdparty/web-auth/webauthn-lib/src/AuthenticatorAttestationResponseValidator.php
+++ b/3rdparty/web-auth/webauthn-lib/src/AuthenticatorAttestationResponseValidator.php
@@ -150,7 +150,7 @@ class AuthenticatorAttestationResponseValidator

             if (!in_array($facetId, $securedRelyingPartyId, true)) {
                 $scheme = $parsedRelyingPartyId['scheme'] ?? '';
-                Assertion::eq('https', $scheme, 'Invalid scheme. HTTPS required.');
+                #Assertion::eq('https', $scheme, 'Invalid scheme. HTTPS required.');
             }

             /* @see 7.1.6 */
```
````

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
