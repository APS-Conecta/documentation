---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Solución de problemas del groupware: calendarios compartidos que faltan, errores 501 en contactos y diagnóstico de la app Correo con occ y registros."
---
(nc-troubleshooting_groupware)=
# Solución de problemas

## Resumen

Esta página reúne problemas conocidos del groupware y cómo diagnosticarlos: calendarios compartidos que no aparecen, errores al actualizar contactos o eventos, y en la app Correo la configuración automática, la base de datos, los hilos, los ID de cuenta, Outlook.com, el registro de conexiones, la conectividad y la sincronización manual. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/groupware/troubleshooting.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Calendario

#### Calendarios compartidos que faltan

- **Problema:** Un usuario debería tener acceso a un calendario compartido, pero el calendario no se muestra en el Calendario de Nextcloud ni en otros clientes CalDAV (p. ej., DAVx⁵ o Thunderbird).
- **Versiones afectadas:**
  - Nextcloud Server 31.0.5 y anteriores
  - Nextcloud Server 30.0.11 y anteriores
- **Posible motivo:** Un error de versiones anteriores de Nextcloud Server podía añadir por equivocación una anulación de uso compartido del calendario en lugar de quitar el permiso del recurso compartido. Por ejemplo, un usuario tiene acceso de lectura mediante su pertenencia a un grupo, y el propietario concede a un único usuario permiso para modificar un calendario. Cuando se quita el permiso de modificación, se crea incorrectamente un registro de anulación de uso compartido.

**Pasos para solucionar el problema:**

1. **Comprobar si hay calendarios ocultos:** Un usuario puede ocultar un calendario. Comprobar en el Calendario de Nextcloud si el calendario que falta aparece en la sección «hidden». Si es así, marcar la casilla que hay delante del calendario para volver a activarlo.

2. **Listar los calendarios compartidos:** Ejecutar el comando `occ dav:list-calendar-shares <uid>` para listar todos los recursos compartidos de un usuario. Buscar líneas con el «Calendar URI»/«Calendar Name» del calendario que falta y «Permissions = Unshare». Si existe una línea así, pero el usuario debería tener acceso, hay tres opciones:

A. **Crear un recurso compartido de usuario y volver a eliminarlo:** En la mayoría de los casos, volver a compartir el calendario con el usuario (como recurso compartido individual o de usuario) corregirá el estado en la base de datos.

B. **Eliminar todas las anulaciones de uso compartido de calendario de un usuario:** Ejecutar `occ dav:clear-calendar-unshares <uid>`.

C. **Eliminar anulaciones de uso compartido concretas:** Algunos usuarios pueden tener muchas anulaciones de uso compartido de calendario, por lo que puede ser más fácil eliminar solo la anulación no deseada. `Share Id` se refiere al ID de una fila de la tabla de base de datos `oc_dav_shares`. Eliminar la fila con el ID coincidente para quitar la anulación de uso compartido.

- **¿Por qué no hay una migración automática que corrija el problema?** Anular el uso compartido de un calendario es una función, y con la información disponible no puede determinarse si un calendario dejó de compartirse intencionadamente o como consecuencia del error.

### Contactos

#### No se pueden actualizar contactos ni eventos

Si aparece un error como:

`PATCH https://example.com/remote.php/dav HTTP/1.0 501 Not Implemented`

lo más probable es que se deba a un servidor web mal configurado. Consultar {nc-ref}`trouble-webdav-label` para ver los pasos de solución de problemas.

### Correo

#### Falla la configuración automática del dominio de correo

Si falla la configuración automática del dominio, se puede crear un archivo de configuración automática y colocarlo como `https://autoconfig.yourdomain.tld/mail/config-v1.1.xml`. Para más información, consultar la [documentación de Mozilla](https://wiki.mozilla.org/Thunderbird:Autoconfiguration:ConfigFileFormat).

#### Problemas de inserción en la base de datos con MySQL

Si la app de correo no consigue insertar filas nuevas de mensajes (*oc_mail_messages*), destinatarios (*oc_mail_recipients*) o tablas similares, es posible que no se esté usando la compatibilidad con 4 bytes.

Consultar {nc-doc}`admin_manual/configuration_database/mysql_4byte_support` para saber cómo actualizar la configuración de la base de datos.

#### Exportar los datos de hilos

Si hay un problema con los hilos, p. ej., mensajes que pertenecen al mismo hilo de conversación no aparecen como uno solo, se pueden exportar los datos que el algoritmo usará para construir los hilos. Aquí se trata con datos sensibles, pero el comando puede ocultarlos opcionalmente con la opción `--redact`. Así, los datos exportados solo conservarán los ID originales de la base de datos; el resto de los datos se aleatoriza. Este formato no exporta los detalles de los mensajes, pero sigue conteniendo metadatos sobre cuántos mensajes hay y cómo se relacionan. Hay que tenerlo en cuenta antes de publicar los datos en línea.

```
sudo -E -u www-data php occ mail:account:export-threads 1393
```

:::{note}
1393 representa el {nc-ref}`ID de cuenta <mail_get_account_ids_groupware>`.
:::

La salida será similar a esta:

```
[
    {
        "subject": "83379f9bc36915d5024de878386060b5@redacted",
        "id": "2def0f3597806ecb886da1d9cc323a7c@redacted",
        "references": [],
        "databaseId": 261535
    },
        {
        "subject": "Re: 1d4725ae1ac4e4798b541ca3f3cdce6e@redacted",
        "id": "ce9e248333c44a5a64ccad26f2550f95@redacted",
        "references": [
            "bc95cbaff3abbed716e1d40bbdaa58a0@redacted",
            "8651a9ac37674907606c936ced1333d7@redacted",
            "4a87e94522a3cf26dba8977ae901094d@redacted",
            "a3b30430b1ccb41089170eecbe315d3a@redacted",
            "8e9f60369dce3d8b2b27430bd50ec46d@redacted",
            "46cfa6e729ff329e6ede076853154113@redacted",
            "079e7bc89d69792839a5e1831b1cbc80@redacted",
            "079e7bc89d69792839a5e1831b1cbc80@redacted"
        ],
        "databaseId": 262086
    },
    {
        "subject": "Re: 1d4725ae1ac4e4798b541ca3f3cdce6e@redacted",
        "id": "8dd0e0ef2f7ab100b75922489ff26306@redacted",
        "references": [
            "bc95cbaff3abbed716e1d40bbdaa58a0@redacted",
            "8651a9ac37674907606c936ced1333d7@redacted",
            "4a87e94522a3cf26dba8977ae901094d@redacted",
            "a3b30430b1ccb41089170eecbe315d3a@redacted",
            "8e9f60369dce3d8b2b27430bd50ec46d@redacted",
            "46cfa6e729ff329e6ede076853154113@redacted",
            "079e7bc89d69792839a5e1831b1cbc80@redacted",
            "ce9e248333c44a5a64ccad26f2550f95@redacted",
            "ce9e248333c44a5a64ccad26f2550f95@redacted"
        ],
        "databaseId": 262087
    }
]
```

Es una práctica recomendada redirigir la exportación a un archivo, que después puede compartirse con la comunidad y los desarrolladores de la app Correo:

```
sudo -E -u www-data php occ mail:account:export-threads 1393 | gzip -c > /tmp/nextcloud-mail-threads-1393.json.gz
```

(nc-mail_get_account_ids_groupware)=
#### Obtener los ID de cuenta

Para muchas instrucciones de solución de problemas hace falta conocer el *id* de una cuenta de correo. Puede obtenerse en la base de datos, pero también es posible usar el comando de exportación de cuentas de {nc-doc}`occ <admin_manual/occ_command>` si se conoce el UID del usuario que usa la cuenta de correo:

```
sudo -E -u www-data php occ mail:account:export user123
```

La salida será similar a esta:

```
Account 1393:
- E-Mail: christoph@domain.com
- Name: Christoph Wurst
- IMAP user: christoph
- IMAP host: mx.domain.com:993, security: ssl
- SMTP user: christoph
- SMTP host: mx.domain.com:587, security: tls
```

En este ejemplo, `1393` es el *ID de cuenta*.

#### Problemas al conectar con Outlook.com

Si no se puede acceder a la cuenta de Outlook.com, probar a activar la [verificación en dos pasos](https://account.live.com/proofs/Manage) y a configurar una [contraseña de aplicación](https://account.live.com/proofs/AppPassword), que después se usa en la app Nextcloud Mail.

#### Registro de las conexiones IMAP/SMTP/Sieve

La app Nextcloud Mail ofrece un amplio sistema de registro para facilitar la identificación y el seguimiento de errores. Como puede incluir datos sensibles, hay que asegurarse de eliminarlos u ocultarlos antes de publicarlos.

##### Por cuenta de correo

:::{versionadded} 5.1.0 Nextcloud 30 o posterior
:::

A partir de la versión 5.1.0 de la app de correo, se puede activar el registro de las conexiones IMAP/SMTP/Sieve salientes limitado a una cuenta de correo concreta. Como esto ahorra muchos recursos del sistema, es el método preferido para depurar problemas relacionados con las conexiones IMAP/SMTP/Sieve.

Primero hay que obtener el accountId de la cuenta de correo en la que se quiere activar el registro de depuración. Consultar {nc-ref}`mail_get_account_ids_groupware` para más información.

Una vez conocido el accountId de la cuenta de correo en cuestión, puede usarse para activar el registro de depuración ejecutando el siguiente comando en el servidor:

```
sudo -E -u www-data php occ mail:account:debug <accountId> --on
```

Todas las conexiones salientes posteriores que haga la app de correo se escribirán entonces en el directorio `data`. Los archivos se nombran con el siguiente formato: `mail-{{userId}}-{{accountId}}-{{protocol}}.log` (p. ej., *mail-admin-49-imap.log*).

El registro de depuración de esa cuenta concreta puede desactivarse, una vez recopilados los datos necesarios, ejecutando el siguiente comando en el servidor:

```
occ mail:account:debug <accountId> --off
```

##### De forma global

Esto activa el registro de las conexiones IMAP/SMTP/Sieve de **todas** las cuentas de correo configuradas en el servidor. Debe usarse con precaución, ya que puede suponer una gran carga en entornos grandes.

:::{versionadded} 5.1.0 Nextcloud 30 o posterior
:::

Para activar el registro de depuración global en las versiones 5.1.0 y posteriores, basta con ejecutar el siguiente comando en el servidor:

```
sudo -E -u www-data php occ config:system:set app.mail.debug --value true --type bool
```

Todas las conexiones salientes posteriores que haga la app de correo se escribirán entonces en el directorio `data`. Los archivos se nombran con el siguiente formato: `mail-{{userId}}-{{accountId}}-{{protocol}}.log` (p. ej., *mail-admin-49-imap.log*).

El registro de depuración global puede desactivarse, una vez recopilados los datos necesarios, ejecutando el siguiente comando en el servidor:

```
sudo -E -u www-data php occ config:system:set app.mail.debug --value false --type bool
```

:::{note}
Los pasos siguientes solo se aplican a las versiones de la 1.6.2 a la 5.0.8. En ellas no está disponible la restricción del registro de las conexiones salientes a una cuenta de correo concreta.
:::

:::{versionadded} 1.6.2 Nextcloud 20 o posterior
:::

Para activar el registro de depuración global, es necesario activar tanto el modo de depuración como el registro de depuración de toda la instancia de nextcloud, ejecutando los siguientes comandos en el servidor:

```
sudo -E -u www-data php occ config:system:set debug --value true --type bool
sudo -E -u www-data php occ config:system:set loglevel --value 0 --type int
```

Todas las conexiones salientes posteriores que haga la app de correo se escribirán entonces en el directorio `data`. Los archivos se nombran con el siguiente formato: `horde_{{protocol}}.log` (p. ej., *horde_imap.log*).

Una vez recopilados los datos necesarios, es muy recomendable desactivar el modo de depuración y restablecer el nivel de registro al valor predeterminado ejecutando los siguientes comandos:

```
sudo -E -u www-data php occ config:system:set debug --value false --type bool
sudo -E -u www-data php occ config:system:set loglevel --value 2 --type int
```

#### Tiempos de espera y otros problemas de conectividad

Se puede usar OpenSSL para probar y medir el rendimiento de la conexión desde el host de nextcloud hasta el host IMAP/SMTP:

```
openssl s_time -connect imap.domain.tld:993
```

La salida debería ser similar a esta:

```
Collecting connection statistics for 30 seconds
***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

483 connections in 0.94s; 513.83 connections/user sec, bytes read 0
483 connections in 31 real seconds, 0 bytes read per connection


Now timing with session id reuse.
starting
*****************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

497 connections in 0.97s; 512.37 connections/user sec, bytes read 0
497 connections in 31 real seconds, 0 bytes read per connection
```

#### Sincronización manual de cuentas y creación de hilos

Para solucionar problemas de sincronización o de hilos, resulta útil ejecutar la sincronización desde la línea de comandos mientras el usuario no usa la interfaz web (así se reducen las posibilidades de un conflicto):

```
sudo -E -u www-data php occ mail:account:sync -vvv 1393
```

:::{note}
1393 representa el {nc-ref}`ID de cuenta <mail_get_account_ids_groupware>`.
:::

El comando ofrece una opción `--force`. Usarla con prudencia, ya que no sigue el mismo camino que una petición de sincronización típica lanzada desde la web.

La salida será similar a esta:

```
[debug] Skipping mailbox sync for Archive
[debug] Skipping mailbox sync for Archive.2020
[debug] partial sync 1393:Drafts - get all known UIDs took 0s
[debug] partial sync 1393:Drafts - get new messages via Horde took 0s
[debug] partial sync 1393:Drafts - persist new messages took 0s
[debug] partial sync 1393:Drafts - get changed messages via Horde took 0s
[debug] partial sync 1393:Drafts - persist changed messages took 0s
[debug] partial sync 1393:Drafts - get vanished messages via Horde took 0s
[debug] partial sync 1393:Drafts - persist new messages took 0s
[debug] partial sync 1393:Drafts took 0s
[debug] partial sync 1393:INBOX - get all known UIDs took 0s
[debug] partial sync 1393:INBOX - get new messages via Horde took 0s
[debug] partial sync 1393:INBOX - classified a chunk of new messages took 1s
[debug] partial sync 1393:INBOX - persist new messages took 0s
[debug] partial sync 1393:INBOX - get changed messages via Horde took 1s
[debug] partial sync 1393:INBOX - persist changed messages took 0s
[debug] partial sync 1393:INBOX - get vanished messages via Horde took 0s
[debug] partial sync 1393:INBOX - persist new messages took 0s
[debug] partial sync 1393:INBOX took 2s
[debug] Skipping mailbox sync for Sent
[debug] Skipping mailbox sync for Sentry
[debug] Skipping mailbox sync for Trash
[debug] Account 1393 has 19417 messages for threading
[debug] Threading 19417 messages - build ID table took 1s
[debug] Threading 19417 messages - build root container took 0s
[debug] Threading 19417 messages - free ID table took 0s
[debug] Threading 19417 messages - prune containers took 0s
[debug] Threading 19417 messages - group by subject took 0s
[debug] Threading 19417 messages took 1s
[debug] Account 1393 has 9839 threads
[debug] Account 1393 has 0 messages with a new thread IDs
62MB of memory used
```
````
