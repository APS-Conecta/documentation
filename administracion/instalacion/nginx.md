---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Servir la instancia con NGINX y PHP-FPM: ajustes de la configuración, webroot o subdirectorio, y soluciones a errores frecuentes."
---
(nc-nginx-config)=
# Configuración de NGINX

## Resumen

Esta página explica cómo servir la instancia con NGINX respaldado por PHP-FPM: qué ajustar en la configuración, en qué se diferencian la instalación en el webroot y en un subdirectorio, y cómo resolver errores frecuentes como el «502 Bad Gateway». Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/installation/nginx.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

Esta página explica cómo ejecutar un servidor Nextcloud con NGINX respaldado por PHP-FPM, que también es una configuración con soporte oficial.

- Hay que insertar el siguiente código en **el archivo de configuración de Nginx**. Elegir el ejemplo adecuado según se despliegue {nc-ref}`nginx_webroot_example` (es decir, {code}`https://cloud.example.com/`) o {nc-ref}`nginx_subdir_example` (es decir, {code}`https://cloud.example.com/nextcloud`).
- Ajustar la directiva server de {code}`upstream php-handler` para que coincida con el listener de FPM configurado en la instalación de PHP (una configuración incorrecta aquí provocará un {code}`502 Bad Gateway`; ver {nc-ref}`nginx_php_handler_tips` para más detalles)
- Ajustar las directivas {code}`server_name` existentes en *ambas* secciones {code}`server` al nombre de host real
- Ajustar {code}`root` al webroot de la instalación de Nextcloud
- Ajustar las directivas {code}`ssl_certificate` y {code}`ssl_certificate_key` a las rutas reales del certificado firmado y de la clave privada. Asegurarse de que el proceso del servidor nginx puede leer los certificados SSL (ver la [documentación del módulo HTTPS SSL de nginx](https://wiki.nginx.org/HttpSslModule)).
- Si se usa Let's Encrypt como certificado TLS y nginx como servidor web, establecer *ssl_stapling* y *ssl_stapling_verify* en *off* en la configuración principal de nginx (ver [entrada del blog de Let's Encrypt](https://letsencrypt.org/2024/12/05/ending-ocsp)).
- Tener cuidado con los saltos de línea al copiar los ejemplos, ya que las líneas largas pueden cortarse para mostrarlas en la página y dar lugar a archivos de configuración no válidos.
- Algunos entornos pueden necesitar `cgi.fix_pathinfo` con el valor `1` en su `php.ini`.

(nc-nginx_webroot_example)=
### Nextcloud en el webroot de NGINX

La siguiente configuración debe usarse cuando Nextcloud está en el webroot de la instalación de nginx. En este ejemplo es `/var/www/nextcloud` y se accede mediante `http(s)://cloud.example.com/`

```nginx
# Nextcloud nginx configuration — root installation
# Version 2026-06-09

# PHP-FPM backend.
upstream php-handler {
    # Use one of the options below, not both:
    server 127.0.0.1:9000;
    #server unix:/run/php/php8.2-fpm.sock;
}

# Set the `immutable` cache control options only for assets with a cache busting `v` argument
map $arg_v $asset_immutable {
    "" "";
    default ", immutable";
}

server {
    listen 80;
    listen [::]:80;
    server_name cloud.example.com;

    # Prevent nginx HTTP Server Detection
    server_tokens off;

    # Enforce HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    # With NGinx >= 1.25.1 you should use this instead:
    # listen 443      ssl;
    # listen [::]:443 ssl;
    # http2 on;
    server_name cloud.example.com;

    # Path to the root of your installation
    root /var/www/nextcloud;

    # Use Mozilla's guidelines for SSL/TLS settings
    # https://mozilla.github.io/server-side-tls/ssl-config-generator/
    ssl_certificate     /etc/ssl/nginx/cloud.example.com.crt;
    ssl_certificate_key /etc/ssl/nginx/cloud.example.com.key;

    # Prevent nginx HTTP Server Detection
    server_tokens off;

    # HSTS settings
    # WARNING: Only add the preload option once you read about
    # the consequences in https://hstspreload.org/. This option
    # will add the domain to a hardcoded list that is shipped
    # in all major browsers and getting removed from this list
    # could take several months.
    #add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # set max upload size and increase upload timeout:
    client_max_body_size 512M;
    client_body_timeout 300s;
    fastcgi_buffers 64 4K;

    # Proxy and client response timeouts
    # Uncomment an increase these if facing timeout errors during large file uploads
    #proxy_connect_timeout 60s;
    #proxy_send_timeout 60s;
    #proxy_read_timeout 60s;
    #send_timeout 60s;

    # Enable gzip but do not remove ETag headers
    gzip on;
    gzip_vary on;
    gzip_comp_level 4;
    gzip_min_length 256;
    gzip_proxied expired no-cache no-store private no_last_modified no_etag auth;
    gzip_types application/atom+xml text/javascript application/javascript application/json application/ld+json application/manifest+json application/rss+xml application/vnd.geo+json application/vnd.ms-fontobject application/wasm application/x-font-ttf application/x-web-app-manifest+json application/xhtml+xml application/xml font/opentype image/bmp image/svg+xml image/x-icon text/cache-manifest text/css text/plain text/vcard text/vnd.rim.location.xloc text/vtt text/x-component text/x-cross-domain-policy;

    # Pagespeed is not supported by Nextcloud, so if your server is built
    # with the `ngx_pagespeed` module, uncomment this line to disable it.
    #pagespeed off;

    # The settings allows you to optimize the HTTP2 bandwidth.
    # See https://blog.cloudflare.com/delivering-http-2-upload-speed-improvements/
    # for tuning hints
    client_body_buffer_size 512k;

    # HTTP response headers borrowed from Nextcloud `.htaccess`
    add_header Referrer-Policy                   "no-referrer"       always;
    add_header X-Content-Type-Options            "nosniff"           always;
    add_header X-Frame-Options                   "SAMEORIGIN"        always;
    add_header X-Permitted-Cross-Domain-Policies "none"              always;
    add_header X-Robots-Tag                      "noindex, nofollow" always;

    # Remove X-Powered-By, which is an information leak
    fastcgi_hide_header X-Powered-By;

    # Set .mjs and .wasm MIME types
    # Either include it in the default mime.types list
    # and include that list explicitly or add the file extension
    # only for Nextcloud like below:
    include mime.types;
    types {
        text/javascript mjs;
	application/wasm wasm;
    }

    # Specify how to handle directories -- specifying `/index.php$request_uri`
    # here as the fallback means that Nginx always exhibits the desired behaviour
    # when a client requests a path that corresponds to a directory that exists
    # on the server. In particular, if that directory contains an index.php file,
    # that file is correctly served; if it doesn't, then the request is passed to
    # the front-end controller. This consistent behaviour means that we don't need
    # to specify custom rules for certain paths (e.g. images and other assets,
    # `/updater`, `/ocs-provider`), and thus
    # `try_files $uri $uri/ /index.php$request_uri`
    # always provides the desired behaviour.
    index index.php index.html /index.php$request_uri;

    # Rule borrowed from `.htaccess` to handle Microsoft DAV clients
    location = / {
        if ( $http_user_agent ~ ^DavClnt ) {
            return 302 /remote.php/webdav/$is_args$args;
        }
    }

    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }

    # Make a regex exception for `/.well-known` so that clients can still
    # access it despite the existence of the regex rule
    # `location ~ /(\.|autotest|...)` which would otherwise handle requests
    # for `/.well-known`.
    location ^~ /.well-known {
        # The rules in this block are an adaptation of the rules
        # in `.htaccess` that concern `/.well-known`.

        location = /.well-known/carddav { return 301 /remote.php/dav/; }
        location = /.well-known/caldav  { return 301 /remote.php/dav/; }

        location /.well-known/acme-challenge    { try_files $uri $uri/ =404; }
        location /.well-known/pki-validation    { try_files $uri $uri/ =404; }

        # Let Nextcloud's API for `/.well-known` URIs handle all other
        # requests by passing them to the front-end controller.
        return 301 /index.php$request_uri;
    }

    # Rules borrowed from `.htaccess` to hide certain paths from clients
    location ~ ^/(?:build|tests|config|lib|3rdparty|templates|data)(?:$|/)  { return 404; }
    location ~ ^/(?:\.|autotest|occ|issue|indie|db_|console)                { return 404; }

    # Hide metadata files which would otherwise be served as plain files and
    # leak dependency information (composer.json, package.json, core/shipped.json).
    location ~ ^/(?:composer\.(?:json|lock)|package(?:-lock)?\.json|core/shipped\.json)$ { return 404; }

    # Pass PHP requests to PHP-FPM.
    #
    # Important: this block must appear above the static asset locations
    # below. Those locations fall back to `/index.php$request_uri`; if
    # they appear first, nginx can repeatedly rewrite to `/index.php`,
    # causing an internal redirection loop.
    location ~ \.php(?:$|/) {
        # Rewrite most PHP requests to Nextcloud's front controller (`/index.php`).
        #
        # (Mirrors the rewrite exceptions in Nextcloud's Apache .htaccess.)
        #
        # Exceptions (not rewritten; must remain directly reachable):
        #   index.php, remote.php, public.php, cron.php, status.php
        #   ocs/v1.php, ocs/v2.php, ocs-provider/*
        #   core/ajax/update.php, updater/*
        #   */richdocumentscode(_arm64)?/proxy
        #
        # Other exceptions (e.g. /.well-known) are handled by dedicated
        # location blocks elsewhere in this config.
        #
        # Caution: small edits to this regex can break routing or introduce
        # rewrite loops.
        rewrite ^/(?!index|remote|public|cron|status|ocs\/v[12]|ocs-provider\/.+|core\/ajax\/update|updater\/.+|.+\/richdocumentscode(_arm64)?\/proxy) /index.php$request_uri;

        # Split `/file.php/path/info` into:
        # - $fastcgi_script_name: `/file.php`
        # - $fastcgi_path_info:   `/path/info`
        #
        # This is required for entry-points such as `remote.php` and `public.php`,
        # which route requests based on PATH_INFO.
        fastcgi_split_path_info ^(.+?\.php)(/.*)$;
        set $path_info $fastcgi_path_info;    # Save before try_files resets it

        # Return 404 for nonexistent PHP scripts (avoids passing arbitrary
        # paths to PHP-FPM, which is a known security risk).
        try_files $fastcgi_script_name =404;

        include fastcgi_params;
        fastcgi_pass php-handler;

        fastcgi_param SCRIPT_FILENAME            $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO                  $path_info;
        fastcgi_param HTTPS                      on;       # Assumes TLS terminates here
        fastcgi_param modHeadersAvailable        true;     # Avoid duplicate security headers
        fastcgi_param front_controller_active    true;     # Enable pretty URLs

        # Let nginx handle HTTP error responses from PHP-FPM (e.g. custom
        # error pages). Disable for debugging if PHP errors are being hidden.
        fastcgi_intercept_errors on;

        # Required for uploads: PHP-FPM does not support chunked
        # transfer encoding and needs a Content-Length header.
        fastcgi_request_buffering on;

        # Optional PHP-FPM timeout tuning (e.g. for 504 response timeouts).
        # Increase these only if uploads or long-running PHP requests are
        # timing out in your environment.
        #fastcgi_read_timeout 60s;
        #fastcgi_send_timeout 60s;
        #fastcgi_connect_timeout 60s;

        # Disable on-disk buffering of FastCGI responses (reduces disk I/O at
        # the cost of holding responses in memory).
        fastcgi_max_temp_file_size 0;
    }

    # Serve static files
    location ~ \.(?:css|js|mjs|svg|gif|ico|jpg|png|webp|wasm|tflite|map|ogg|flac|mp4|webm)$ {
        try_files $uri /index.php$request_uri;
	
		# HSTS settings
		# WARNING: Only add the preload option once you read about
		# the consequences in https://hstspreload.org/. This option
		# will add the domain to a hardcoded list that is shipped
		# in all major browsers and getting removed from this list
		# could take several months.
		#add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

        # HTTP response headers borrowed from Nextcloud `.htaccess`
        add_header Cache-Control                     "public, max-age=15778463$asset_immutable";
        add_header Referrer-Policy                   "no-referrer"       always;
        add_header X-Content-Type-Options            "nosniff"           always;
        add_header X-Frame-Options                   "SAMEORIGIN"        always;
        add_header X-Permitted-Cross-Domain-Policies "none"              always;
        add_header X-Robots-Tag                      "noindex, nofollow" always;
        access_log off;     # Optional: Don't log access to assets
    }

    location ~ \.(otf|woff2?)$ {
        try_files $uri /index.php$request_uri;
        expires 7d;         # Cache-Control policy borrowed from `.htaccess`
        access_log off;     # Optional: Don't log access to assets
    }

    # Rule borrowed from `.htaccess`
    location /remote {
        return 301 /remote.php$request_uri;
    }

    location / {
        try_files $uri $uri/ /index.php$request_uri;
    }
}
```

(nc-nginx_subdir_example)=
### Nextcloud en un subdirectorio del webroot de NGINX

La siguiente configuración debe usarse cuando Nextcloud está dentro de un subdirectorio del webroot de la instalación de nginx. En este ejemplo, los archivos de Nextcloud están en `/var/www/nextcloud` y se accede a la instancia de Nextcloud mediante `http(s)://cloud.example.com/nextcloud/`. La configuración se diferencia de la configuración «Nextcloud en el webroot» anterior en lo siguiente:

- Todas las peticiones a `/nextcloud` se encapsulan en un único bloque `location`, concretamente `location ^~ /nextcloud`.
- La cadena `/nextcloud` se antepone a todas las rutas de prefijo.
- La raíz del dominio se asigna a `/var/www` en lugar de a `/var/www/nextcloud`, de modo que la URI `/nextcloud` se asigna al directorio del servidor `/var/www/nextcloud`.
- Los bloques que gestionan las peticiones a rutas fuera de `/nextcloud` (es decir, `/robots.txt` y `/.well-known`) se sacan del bloque `location ^~ /nextcloud`.
- El bloque que gestiona */.well-known* no necesita una excepción de expresión regular, ya que la regla que impide a los usuarios acceder a carpetas ocultas en la raíz de la instalación de Nextcloud ya no coincide con esa ruta.

```nginx
# Nextcloud nginx configuration — subdirectory installation (/nextcloud)
# Version 2026-06-09

# PHP-FPM backend.
upstream php-handler {
    # Use one of the options below, not both:
    server 127.0.0.1:9000;
    #server unix:/run/php/php8.2-fpm.sock;
}

# Set the `immutable` cache control options only for assets with a cache busting `v` argument
map $arg_v $asset_immutable {
    "" "";
    default ", immutable";
}

server {
    listen 80;
    listen [::]:80;
    server_name cloud.example.com;

    # Prevent nginx HTTP Server Detection
    server_tokens off;

    # Enforce HTTPS just for `/nextcloud`
    location /nextcloud {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443      ssl http2;
    listen [::]:443 ssl http2;
    # With NGinx >= 1.25.1 you should use this instead:
    # listen 443      ssl;
    # listen [::]:443 ssl;
    # http2 on;
    server_name cloud.example.com;

    # Path to the root of the domain
    root /var/www;

    # Use Mozilla's guidelines for SSL/TLS settings
    # https://mozilla.github.io/server-side-tls/ssl-config-generator/
    ssl_certificate     /etc/ssl/nginx/cloud.example.com.crt;
    ssl_certificate_key /etc/ssl/nginx/cloud.example.com.key;

    # Prevent nginx HTTP Server Detection
    server_tokens off;

    # Set .mjs and .wasm MIME types
    # Either include it in the default mime.types list
    # and include that list explicitly or add the file extension
    # only for Nextcloud like below:
    include mime.types;
    types {
        text/javascript mjs;
        # uncomment below for Nginx <= 1.21.0 
        # application/wasm wasm;
    }

    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }

    location ^~ /.well-known {
        # The rules in this block are an adaptation of the rules
        # in the Nextcloud `.htaccess` that concern `/.well-known`.

        location = /.well-known/carddav { return 301 /nextcloud/remote.php/dav/; }
        location = /.well-known/caldav  { return 301 /nextcloud/remote.php/dav/; }

        location /.well-known/acme-challenge    { try_files $uri $uri/ =404; }
        location /.well-known/pki-validation    { try_files $uri $uri/ =404; }

        # Let Nextcloud's API for `/.well-known` URIs handle all other
        # requests by passing them to the front-end controller.
        return 301 /nextcloud/index.php$request_uri;
    }

    location ^~ /nextcloud {
        # set max upload size and increase upload timeout:
        client_max_body_size 512M;
        client_body_timeout 300s;
        fastcgi_buffers 64 4K;

        # Proxy and client response timeouts
        # Uncomment an increase these if facing timeout errors during large file uploads
        #proxy_connect_timeout 60s;
        #proxy_send_timeout 60s;
        #proxy_read_timeout 60s;
        #send_timeout 60s;

        # Enable gzip but do not remove ETag headers
        gzip on;
        gzip_vary on;
        gzip_comp_level 4;
        gzip_min_length 256;
        gzip_proxied expired no-cache no-store private no_last_modified no_etag auth;
        gzip_types application/atom+xml text/javascript application/javascript application/json application/ld+json application/manifest+json application/rss+xml application/vnd.geo+json application/vnd.ms-fontobject application/wasm application/x-font-ttf application/x-web-app-manifest+json application/xhtml+xml application/xml font/opentype image/bmp image/svg+xml image/x-icon text/cache-manifest text/css text/plain text/vcard text/vnd.rim.location.xloc text/vtt text/x-component text/x-cross-domain-policy;

        # Pagespeed is not supported by Nextcloud, so if your server is built
        # with the `ngx_pagespeed` module, uncomment this line to disable it.
        #pagespeed off;

        # The settings allows you to optimize the HTTP2 bandwidth.
        # See https://blog.cloudflare.com/delivering-http-2-upload-speed-improvements/
        # for tuning hints
        client_body_buffer_size 512k;

        # HSTS settings
        # WARNING: Only add the preload option once you read about
        # the consequences in https://hstspreload.org/. This option
        # will add the domain to a hardcoded list that is shipped
        # in all major browsers and getting removed from this list
        # could take several months.
        #add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

        # HTTP response headers borrowed from Nextcloud `.htaccess`
        add_header Referrer-Policy                   "no-referrer"       always;
        add_header X-Content-Type-Options            "nosniff"           always;
        add_header X-Frame-Options                   "SAMEORIGIN"        always;
        add_header X-Permitted-Cross-Domain-Policies "none"              always;
        add_header X-Robots-Tag                      "noindex, nofollow" always;

        # Remove X-Powered-By, which is an information leak
        fastcgi_hide_header X-Powered-By;

        # Specify how to handle directories -- specifying `/nextcloud/index.php$request_uri`
        # here as the fallback means that Nginx always exhibits the desired behaviour
        # when a client requests a path that corresponds to a directory that exists
        # on the server. In particular, if that directory contains an index.php file,
        # that file is correctly served; if it doesn't, then the request is passed to
        # the front-end controller. This consistent behaviour means that we don't need
        # to specify custom rules for certain paths (e.g. images and other assets,
        # `/updater`, `/ocs-provider`), and thus
        # `try_files $uri $uri/ /nextcloud/index.php$request_uri`
        # always provides the desired behaviour.
        index index.php index.html /nextcloud/index.php$request_uri;

        # Rule borrowed from `.htaccess` to handle Microsoft DAV clients
        location = /nextcloud {
            if ( $http_user_agent ~ ^DavClnt ) {
                return 302 /nextcloud/remote.php/webdav/$is_args$args;
            }
        }

        # Rules borrowed from `.htaccess` to hide certain paths from clients
        location ~ ^/nextcloud/(?:build|tests|config|lib|3rdparty|templates|data)(?:$|/)    { return 404; }
        location ~ ^/nextcloud/(?:\.|autotest|occ|issue|indie|db_|console)                  { return 404; }

        # Hide metadata files which would otherwise be served as plain files and
        # leak dependency information (composer.json, package.json, core/shipped.json).
        location ~ ^/nextcloud/(?:composer\.(?:json|lock)|package(?:-lock)?\.json|core/shipped\.json)$ { return 404; }

        # Pass PHP requests to PHP-FPM.
        #
        # Important: this block must appear above the static asset locations
        # below. Those locations fall back to `/nextcloud/index.php$request_uri`;
        # if they appear first, nginx can repeatedly rewrite to
        # `/nextcloud/index.php`, causing an internal redirection loop.
        location ~ \.php(?:$|/) {
            # Rewrite most PHP requests to Nextcloud's front controller
            # (`/nextcloud/index.php`).
            #
            # (Mirrors the rewrite exceptions in Nextcloud's Apache .htaccess.)
            #
            # Exceptions (not rewritten; must remain directly reachable):
            #   index.php, remote.php, public.php, cron.php, status.php
            #   ocs/v1.php, ocs/v2.php, ocs-provider/*
            #   core/ajax/update.php, updater/*
            #   */richdocumentscode(_arm64)?/proxy
            #
            # Other exceptions (e.g. /.well-known) are handled by dedicated
            # location blocks elsewhere in this config.
            #
            # Caution: small edits to this regex can break routing or introduce
            # rewrite loops.
            rewrite ^/nextcloud/(?!index|remote|public|cron|status|ocs\/v[12]|ocs-provider\/.+|core\/ajax\/update|updater\/.+|.+\/richdocumentscode(_arm64)?\/proxy) /nextcloud/index.php$request_uri;

            # Split `/file.php/path/info` into:
            # - $fastcgi_script_name: `/file.php`
            # - $fastcgi_path_info:   `/path/info`
            #
            # This is required for entry-points such as `remote.php` and `public.php`,
            # which route requests based on PATH_INFO.
            fastcgi_split_path_info ^(.+?\.php)(/.*)$;
            set $path_info $fastcgi_path_info;    # Save before try_files resets it

            # Return 404 for nonexistent PHP scripts (avoids passing arbitrary
            # paths to PHP-FPM, which is a known security risk).
            try_files $fastcgi_script_name =404;

            include fastcgi_params;
            fastcgi_pass php-handler;

            fastcgi_param SCRIPT_FILENAME            $document_root$fastcgi_script_name;
            fastcgi_param PATH_INFO                  $path_info;
            fastcgi_param HTTPS                      on;       # Assumes TLS terminates here
            fastcgi_param modHeadersAvailable        true;     # Avoid duplicate security headers
            fastcgi_param front_controller_active    true;     # Enable pretty URLs

            # Let nginx handle HTTP error responses from PHP-FPM (e.g. custom
            # error pages). Disable for debugging if PHP errors are being hidden.
            fastcgi_intercept_errors on;

            # Required for uploads: PHP-FPM does not support chunked
            # transfer encoding and needs a Content-Length header.
            fastcgi_request_buffering on;

            # Optional PHP-FPM timeout tuning (e.g. for 504 response timeouts).
            # Increase these only if uploads or long-running PHP requests are
            # timing out in your environment.
            #fastcgi_read_timeout 60s;
            #fastcgi_send_timeout 60s;
            #fastcgi_connect_timeout 60s;

            # Disable on-disk buffering of FastCGI responses (reduces disk I/O at
            # the cost of holding responses in memory).
            fastcgi_max_temp_file_size 0;
        }

        # Serve static files
        location ~ \.(?:css|js|mjs|svg|gif|ico|jpg|png|webp|wasm|tflite|map|ogg|flac|mp4|webm)$ {
            try_files $uri /nextcloud/index.php$request_uri;
            # HTTP response headers borrowed from Nextcloud `.htaccess`
            add_header Cache-Control                     "public, max-age=15778463$asset_immutable";
            add_header Referrer-Policy                   "no-referrer"       always;
            add_header X-Content-Type-Options            "nosniff"           always;
            add_header X-Frame-Options                   "SAMEORIGIN"        always;
            add_header X-Permitted-Cross-Domain-Policies "none"              always;
            add_header X-Robots-Tag                      "noindex, nofollow" always;
            access_log off;     # Optional: Don't log access to assets
        }

        location ~ \.(otf|woff2?)$ {
            try_files $uri /nextcloud/index.php$request_uri;
            expires 7d;         # Cache-Control policy borrowed from `.htaccess`
            access_log off;     # Optional: Don't log access to assets
        }

        # Rule borrowed from `.htaccess`
        location /nextcloud/remote {
            return 301 /nextcloud/remote.php$request_uri;
        }

        location /nextcloud {
            try_files $uri $uri/ /nextcloud/index.php$request_uri;
        }
    }
}
```

### Trucos y consejos

(nc-nginx_php_handler_tips)=
#### Configuración de PHP-Handler / Cómo evitar «502 Bad Gateway»

La línea {code}`server` dentro del {code}`upstream php-handler` anterior debe ajustarse para reflejar la configuración local de PHP FPM. Debe coincidir con lo que esté configurado en la directiva {code}`listen` del pool de PHP FPM que se vaya a usar para NC.

Muchas distribuciones Linux definen un listener para un pool de PHP-FPM predeterminado llamado {code}`www` en un archivo llamado {code}`www.conf`, ubicado en algún lugar como {code}`/etc/php/8.1/pool.d`.

Buscar la línea que tenga un valor parecido a:

{code}`listen = /var/run/php/php-fpm.sock`
o
{code}`listen = 127.0.0.1:9000`

Si PHP FPM se va a ejecutar en el mismo host que NGINX (si hay dudas, probablemente sea una suposición segura), se recomienda usar el socket UNIX (es decir, {code}`/var/run/php/php-fpm.sock`) en lugar de TCP ({code}`127.0.0.1:9000`) para obtener el máximo rendimiento (aunque cualquiera de los dos funciona siempre que las configuraciones de NGINX y de PHP FPM coincidan).

Después de decidir cómo se prefiere conectar NGINX con PHP FPM (y, si es necesario, de actualizar la configuración local de PHP FPM y reiniciar FPM), configurar el {code}`server` del {code}`upstream php-handler` de la configuración de NGINX según esa preferencia (Nota: si se usan sockets UNIX, anteponer {code}`unix:` en la configuración de NGINX, pero *no* en el {code}`www.conf` de PHP FPM).

#### Suprimir mensajes del registro

Si en el archivo de registro aparecen mensajes sin sentido, por ejemplo `client denied by server configuration: /var/www/data/htaccesstest.txt`, añadir esta sección a la configuración de nginx para suprimirlos:

```nginx
location = /data/htaccesstest.txt {
  allow all;
  log_not_found off;
  access_log off;
}
```

#### Archivos JavaScript (.js) o CSS (.css) que no se sirven correctamente

Un problema habitual de las configuraciones personalizadas de nginx es que los archivos JavaScript (.js) o CSS (.css) no se sirven correctamente, lo que provoca un error 404 (archivo no encontrado) en esos archivos y una interfaz web rota.

Puede deberse a que el bloque:

```nginx
location ~* \.(?:css|js)$ {
```

mostrado arriba no esté ubicado **debajo** del bloque:

```nginx
location ~ \.php(?:$|\/) {
```

Otras configuraciones personalizadas, como almacenar en caché los archivos JavaScript (.js) o CSS (.css) mediante gzip, también podrían causar este tipo de problemas.

Otra causa de este problema podría ser no incluir correctamente los mimetypes en el bloque http, como se muestra [aquí.](https://www.nginx.com/resources/wiki/start/topics/examples/full/)

#### Falla la subida de archivos de más de 10 MiB

Si se configura nginx (de forma global) para bloquear todas las peticiones a archivos que empiezan por punto (ocultos), puede que no sea posible subir archivos de más de 10 MiB desde la página web, debido a que Nextcloud exige subir el archivo a una URL que termina en `/.file`.

Puede ser necesario cambiar:

```nginx
location ~ /\. {
```

por lo siguiente para volver a permitir la subida de archivos:

```nginx
location ~ /\.(?!file).* {
```

Ver [issue #8802 en nextcloud/server](https://github.com/nextcloud/server/issues/8802) para más información.

Además de los anteriores, hay otros parámetros relevantes para subir archivos grandes (ver {nc-ref}`uploading_big_files`).

#### Bucle de inicio de sesión sin ninguna pista en access.log, error.log ni nextcloud.log

Si después de una instalación nueva (Centos 7 con nginx) hay problemas con el primer inicio de sesión, lo primero es revisar estos archivos:

```bash
tail /var/www/nextcloud/data/nextcloud.log
tail /var/log/nginx/access.log
tail /var/log/nginx/error.log
```

Si en el registro de acceso solo se ven algunas peticiones correctas, pero no se produce el inicio de sesión, revisar los permisos de acceso de los directorios de sesión de php y de wsdlcache. Comprobar los permisos y cambiarlos si es necesario:

```bash
chown nginx:nginx /var/lib/php/session/
chown root:nginx /var/lib/php/wsdlcache/
chown root:nginx /var/lib/php/opcache/
```
````
