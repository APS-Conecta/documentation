---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Instalar sin el asistente gráfico: descomprimir el código, asignar el directorio al usuario HTTP y completar la instalación con occ."
---
# Instalación desde la línea de comandos

## Resumen

Esta página describe las tres etapas de una instalación hecha completamente desde la línea de comandos con `occ maintenance:install`, y las bases de datos que admite. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/installation/command_line_installation.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

Ahora es posible instalar Nextcloud completamente desde la línea de comandos. Esto resulta práctico para operaciones automatizadas con scripts, para servidores sin interfaz gráfica y para administradores de sistemas que prefieren la línea de comandos. La instalación de Nextcloud desde la línea de comandos tiene tres etapas:

1. Descargar el código de Nextcloud y descomprimir el tarball en los directorios correspondientes. (Ver {nc-doc}`admin_manual/installation/source_installation`.)

2. Cambiar el propietario del directorio `nextcloud` al usuario HTTP, como en este ejemplo para Debian/Ubuntu. `occ` debe ejecutarse como el usuario HTTP; ver {nc-ref}`http_user_label`:

   ```
   $ sudo chown -R www-data:www-data /var/www/nextcloud/
   ```

3. Usar el comando `occ` para completar la instalación. Esto sustituye la ejecución del asistente de instalación gráfico:

   ```
   $ cd /var/www/nextcloud/
   $ sudo -E -u www-data php occ  maintenance:install \
   --database 'mysql' --database-name 'nextcloud' \
   --database-user 'nextcloud' --database-pass 'password' \
   --admin-user 'admin' --admin-pass 'password'
   ```

Tener en cuenta que, para ejecutar `occ maintenance:install`, hay que cambiarse al directorio raíz de Nextcloud, como en el ejemplo anterior; de lo contrario, la instalación fallará con un mensaje de error fatal de PHP.

Las bases de datos admitidas son:

```
- sqlite (SQLite3 - Nextcloud Community edition only)
- mysql (MySQL/MariaDB)
- pgsql (PostgreSQL)
- oci (Oracle currently only possible if you contact us at https://nextcloud.com/enterprise as part of a subscription)
```

Ver {nc-ref}`command_line_installation_label` para más información.
````
