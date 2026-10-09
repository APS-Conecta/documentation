---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Contextos de archivo y booleanos de SELinux para Nextcloud: escritura en sus directorios, red, base de datos remota, LDAP, correo y almacenamiento."
---
# Configuración de SELinux

## Resumen

Esta página reúne los comandos de SELinux para etiquetar los directorios de Nextcloud, los booleanos que permiten las actualizaciones por la interfaz web, las bases de datos remotas, LDAP, la red, el correo y los almacenamientos CIFS/SMB, NFS o FuseFS, y las herramientas para solucionar problemas. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/installation/selinux_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

Si SELinux está activado en la distribución de Linux, pueden aparecer problemas de permisos después de una instalación nueva de Nextcloud, y errores `permission denied` en los registros de Nextcloud.

:::{tip}
Los problemas de permisos pueden deberse a SELinux *aunque la denegación no aparezca en los registros de auditoría.* Esto se debe a que SELinux no registra todas las llamadas al sistema que se usan para verificar el acceso. Consultar [Posibles causas de denegaciones silenciosas](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/sect-security-enhanced_linux-troubleshooting-fixing_problems#sect-Security-Enhanced_Linux-Fixing_Problems-Possible_Causes_of_Silent_Denials) para resolverlo.
:::

Los siguientes ajustes deberían funcionar en la mayoría de los sistemas SELinux que usan los perfiles predeterminados de la distribución. Ejecutar estos comandos como root y recordar adaptar las rutas de archivo de estos ejemplos a la instalación:

```
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/data(/.*)?'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/config(/.*)?'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/apps(/.*)?'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/.htaccess'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/.user.ini'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/3rdparty/aws/aws-sdk-php/src/data/logs(/.*)?'

restorecon -Rv '/var/www/html/nextcloud/'
```

Si se desinstala Nextcloud, hay que eliminar las etiquetas de los directorios de Nextcloud. Para ello, ejecutar los siguientes comandos como root después de desinstalar Nextcloud:

```
semanage fcontext -d '/var/www/html/nextcloud/data(/.*)?'
semanage fcontext -d '/var/www/html/nextcloud/config(/.*)?'
semanage fcontext -d '/var/www/html/nextcloud/apps(/.*)?'
semanage fcontext -d '/var/www/html/nextcloud/.htaccess'
semanage fcontext -d '/var/www/html/nextcloud/.user.ini'
semanage fcontext -d '/var/www/html/nextcloud/3rdparty/aws/aws-sdk-php/src/data/logs(/.*)?'

restorecon -Rv '/var/www/html/nextcloud/'
```

Si se personalizaron las políticas de SELinux y estos ejemplos no funcionan, hay que dar al servidor HTTP acceso de escritura a estos directorios:

```
/var/www/html/nextcloud/data
/var/www/html/nextcloud/config
/var/www/html/nextcloud/apps
```

### Activar las actualizaciones mediante la interfaz web

Para activar las actualizaciones mediante la interfaz web, puede ser necesario esto para permitir la escritura en los directorios:

```
setsebool httpd_unified on
```

Cuando termine la actualización, desactivar el acceso de escritura:

```
setsebool -P  httpd_unified  off
```

### No permitir el acceso de escritura a todo el directorio web

Por motivos de seguridad, se sugiere desactivar el acceso de escritura a todas las carpetas de /var/www/ (predeterminado):

```
setsebool -P  httpd_unified  off
```

### Permitir el acceso a una base de datos remota

Se necesita un ajuste adicional si la instalación se conecta a una base de datos remota:

```
setsebool -P httpd_can_network_connect_db on
```

### Permitir el acceso al servidor LDAP

Usar este ajuste para permitir las conexiones LDAP:

```
setsebool -P httpd_can_connect_ldap on
```

### Permitir el acceso a la red remota

Nextcloud necesita acceso a redes remotas para funciones como el uso compartido entre servidores, los almacenamientos externos o la tienda de apps. Para permitir este acceso, usar el siguiente ajuste:

```
setsebool -P httpd_can_network_connect on
```

### Permitir el acceso a memcache por red

Este ajuste no es necesario si `httpd_can_network_connect` ya está activado:

```
setsebool -P httpd_can_network_memcache on
```

### Permitir el acceso a SMTP/sendmail

Si se quiere permitir que Nextcloud envíe notificaciones por correo electrónico mediante sendmail, hay que usar el siguiente ajuste:

```
setsebool -P httpd_can_sendmail on
```

### Permitir el acceso a CIFS/SMB

Si el directorio de datos se colocó en un recurso compartido CIFS/SMB, usar el siguiente ajuste:

```
setsebool -P httpd_use_cifs on
```

### Permitir el acceso a NFS

Si el directorio de datos se colocó en un recurso compartido NFS, usar el siguiente ajuste:

```
setsebool -P httpd_use_nfs on
```

### Permitir el acceso a FuseFS

Si la carpeta de datos reside en un sistema de archivos Fuse (p. ej., EncFS, etc.), también se necesita este ajuste:

```
setsebool -P httpd_use_fusefs on
```

### Permitir el acceso a GPG para Rainloop

Si se usa la app de cliente de correo web rainloop, que admite GPG/PGP, puede que se necesite esto:

```
setsebool -P httpd_use_gpg on
```

### Solución de problemas

Para la solución general de problemas de SELinux y de sus perfiles, probar a instalar el paquete `setroubleshoot` y ejecutar:

```
sealert -a /var/log/audit/audit.log > /path/to/mylogfile.txt
```

para obtener un informe que ayuda a configurar los perfiles de SELinux.

Otra herramienta para solucionar problemas es activar un único conjunto de reglas para el directorio de Nextcloud:

```
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud(/.*)?'
restorecon -RF /var/www/html/nextcloud
```

Un conjunto de reglas más detallado, como el de los ejemplos del principio, ofrece una seguridad mucho mayor, así que esto solo debe usarse para pruebas y solución de problemas. Tiene un efecto similar a desactivar SELinux, así que no debe usarse en sistemas de producción.
````
