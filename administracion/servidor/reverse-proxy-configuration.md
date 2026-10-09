---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Nextcloud detrás de un proxy inverso: proxies de confianza, parámetros overwrite, redirecciones de descubrimiento de servicios y ejemplos de config.php."
---
(nc-serverconf_reverseproxy)=
# Proxy inverso

## Resumen

Esta página explica, para quienes administran el servidor, cómo ejecutar Nextcloud detrás de un proxy inverso: definir los proxies de confianza, sustituir la detección automática con los parámetros overwrite, configurar las redirecciones de descubrimiento de servicios en varios proxies y ajustar `config.php` en dos escenarios de ejemplo.

````{upstream} admin_manual/configuration_server/reverse_proxy_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud puede ejecutarse detrás de un proxy inverso, que puede almacenar en caché recursos estáticos como imágenes o archivos CSS o JS, trasladar a otro servidor la carga de gestionar HTTPS o repartir la carga entre varios servidores.

### Definir los proxies de confianza

Por seguridad, hay que definir explícitamente los servidores proxy en los que Nextcloud debe confiar. Las conexiones de los proxies de confianza reciben un tratamiento especial para obtener la información real del cliente, que se usa en el control de acceso y en el registro. Los parámetros se configuran en {file}`config/config.php`

Establecer el parámetro {file}`trusted_proxies` como una matriz de:

- direcciones IPv4
- rangos IPv4 en notación CIDR
- direcciones IPv6
- rangos IPv6 en notación CIDR

para definir los servidores en los que Nextcloud debe confiar como proxies. Este parámetro protege contra la suplantación de clientes, y esos servidores deben protegerse igual que el servidor Nextcloud.

Un proxy inverso puede definir cabeceras HTTP con la dirección IP original del cliente, y Nextcloud puede usar esas cabeceras para obtener esa dirección IP. De forma predeterminada, Nextcloud usa la cabecera estándar de facto 'X-Forwarded-For', pero esto puede configurarse con el parámetro **forwarded_for_headers**. Este parámetro es una matriz de cadenas de búsqueda de PHP; por ejemplo, 'X-Forwarded-For' pasa a ser 'HTTP_X_FORWARDED_FOR'. ¡Establecer mal este parámetro puede permitir que los clientes falsifiquen la dirección IP que ve Nextcloud, incluso cuando pasan por el proxy de confianza! El valor correcto de este parámetro depende del software de proxy.

### Parámetros overwrite

La detección automática del nombre de host, el protocolo o la raíz web de Nextcloud puede fallar en ciertas situaciones con proxy inverso. Esta configuración permite sustituir manualmente la detección automática. Si Nextcloud no consigue detectar automáticamente el nombre de host, el protocolo o la raíz web, pueden usarse los parámetros **overwrite** en {file}`config/config.php`.

- {file}`overwritehost` establece el nombre de host del proxy. También puede indicarse un puerto.
- {file}`overwriteprotocol` establece el protocolo del proxy. Puede elegirse entre las dos opciones **http** y **https**.
- {file}`overwritewebroot` establece la ruta web absoluta del proxy a la carpeta de Nextcloud.
- {file}`overwritecondaddr` sustituye los valores en función de la dirección remota. El valor debe ser una **expresión regular** de las direcciones IP del proxy. Esto es útil cuando se usa un proxy SSL inverso solo para el acceso https y se quiere usar la detección automática para el acceso http.
- {file}`overwrite.cli.url` es la URL base de las URL que se generan dentro de Nextcloud con cualquier tipo de herramienta de línea de comandos. Por ejemplo, el área de notificaciones usará el valor establecido aquí.

Dejar el valor vacío u omitir el parámetro para mantener la detección automática.

### Descubrimiento de servicios

Las redirecciones de CalDAV o CardDAV no funcionan si Nextcloud se ejecuta detrás de un proxy inverso. La solución recomendada es que el proxy inverso haga las redirecciones.

#### Apache2

```
RewriteEngine On
RewriteRule ^/\.well-known/carddav https://%{SERVER_NAME}/remote.php/dav/ [R=301,L]
RewriteRule ^/\.well-known/caldav https://%{SERVER_NAME}/remote.php/dav/ [R=301,L]
```

Gracias a [@ffried](https://github.com/ffried) por el ejemplo de apache2.

#### Traefik 1

Con etiquetas de Docker:

```
traefik.frontend.redirect.permanent: 'true'
traefik.frontend.redirect.regex: 'https://(.*)/.well-known/(?:card|cal)dav'
traefik.frontend.redirect.replacement: 'https://$$1/remote.php/dav'
```

Con traefik.toml:

```
[frontends.frontend1.redirect]
  regex = "https://(.*)/.well-known/(?:card|cal)dav"
  replacement = "https://$1/remote.php/dav
  permanent = true
```

Gracias a [@pauvos](https://github.com/pauvos) y [@mrtumnus](https://github.com/mrtumnus) por los ejemplos de traefik.

#### Traefik 2

Con etiquetas de Docker:

```
- "traefik.http.routers.nextcloud.middlewares=nextcloud_redirectregex@docker"
- "traefik.http.middlewares.nextcloud_redirectregex.redirectregex.permanent=true"
- "traefik.http.middlewares.nextcloud_redirectregex.redirectregex.regex=https://(.*)/.well-known/(?:card|cal)dav"
- "traefik.http.middlewares.nextcloud_redirectregex.redirectregex.replacement=https://$${1}/remote.php/dav"
```

Con un archivo TOML:

```
[http.middlewares]
  [http.middlewares.nextcloud-redirectregex.redirectRegex]
    permanent = true
    regex = "https://(.*)/.well-known/(?:card|cal)dav"
    replacement = "https://${1}/remote.php/dav"
```

#### HAProxy

```
acl url_discovery path /.well-known/caldav /.well-known/carddav
http-request redirect location /remote.php/dav/ code 301 if url_discovery
```

#### NGINX

Si se usa nginx como servidor web de Nextcloud detrás de otro proxy inverso nginx, poner esto solo en la configuración del proxy inverso.

```
location /.well-known/carddav {
    return 301 $scheme://$host/remote.php/dav;
}

location /.well-known/caldav {
    return 301 $scheme://$host/remote.php/dav;
}

location ^~ /.well-known {
    return 301 $scheme://$host/index.php$uri;
}
```

Con NGINX Proxy Manager, hay que añadir la entrada `proxy_hide_header Upgrade;` en *«Advanced Settings»* del host del proxy, en *«Custom Nginx Configuration»*; de lo contrario, los dispositivos móviles (iPad, iPhone, etc.) simplemente recibirán el mensaje de error «Connection Closed».

#### Caddy

```
subdomain.example.com {
    redir /.well-known/carddav /remote.php/dav/ 301
    redir /.well-known/caldav /remote.php/dav/ 301

    reverse_proxy {$NEXTCLOUD_HOST:localhost}
}
```

#### Pomerium

```
- from: https://subdomain.example.com
  path: /.well-known/carddav
  redirect:
    path_redirect: /remote.php/dav/
- from: https://subdomain.example.com
  path: /.well-known/caldav
  redirect:
    path_redirect: /remote.php/dav/
```

Gracias a [@JeffMatson](https://github.com/JeffMatson) por el ejemplo de Pomerium.

### Ejemplos

#### Nextcloud detrás de un proxy inverso (subdirectorio)

Si Nextcloud se sirve en un subdirectorio, por ejemplo **<https://example.com/nextcloud>**, detrás de un proxy inverso con la dirección IP **10.0.0.1** que termina TLS, establecer los siguientes parámetros en {file}`config/config.php`:

```
<?php
$CONFIG = array (
  'trusted_proxies'   => ['10.0.0.1'],
  'overwriteprotocol' => 'https',
  'overwritewebroot'  => '/nextcloud',
  'overwrite.cli.url' => 'https://example.com/nextcloud',
);
```

:::{note}
`overwritehost` no es necesario en la mayoría de las configuraciones: Nextcloud leerá el nombre de host de la cabecera `Host` que reenvía el proxy. Establecerlo solo si hay que forzar un nombre de host concreto con independencia de la solicitud entrante. Dejar cualquier parámetro sin establecer o vacío para mantener la detección automática.
:::

#### Nextcloud accesible mediante varios dominios / sustitución condicional

Si Nextcloud es accesible tanto directamente (HTTP) como a través de un proxy inverso (HTTPS), o a través de varios proxies que sirven distintos dominios públicos, usar `overwritecondaddr` para aplicar los parámetros overwrite solo cuando las solicitudes llegan desde la dirección IP de un proxy concreto. Las solicitudes que no proceden de ese proxy usarán la detección automática.

En el ejemplo siguiente, los parámetros overwrite solo se aplican cuando las solicitudes llegan desde el proxy en **10.0.0.1**, que sirve Nextcloud como **<https://public.example.com>**:

```
<?php
$CONFIG = array (
  'trusted_proxies'   => ['10.0.0.1'],
  'overwritehost'     => 'public.example.com',
  'overwriteprotocol' => 'https',
  'overwritecondaddr' => '^10\.0\.0\.1$',
  'overwrite.cli.url' => 'https://public.example.com',
);
```

:::{note}
`overwritecondaddr` recibe una expresión regular que coincide con la dirección remota del proxy. Cuando está establecido, los parámetros overwrite solo se aplican si la dirección remota coincide. Esto es útil cuando la misma instancia de Nextcloud es accesible tanto con proxy inverso como sin él, o cuando distintos proxies sirven la instancia con distintos nombres de host.
:::
````
