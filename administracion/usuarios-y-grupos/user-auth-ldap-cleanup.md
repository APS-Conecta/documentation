---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "La limpieza de usuarios LDAP: el proceso que marca como deleted a los que ya no están disponibles y los comandos occ para revisarlos y borrar sus datos."
---
# Limpieza de usuarios LDAP

## Resumen

Esta página explica el proceso en segundo plano que marca como `deleted` a los usuarios que ya no están disponibles en LDAP, sus requisitos y cómo ajustarlo, y los comandos `occ` para revisar esos usuarios y borrar sus datos. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_user/user_auth_ldap_cleanup.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La limpieza de usuarios LDAP es una nueva función de la aplicación `LDAP user and group backend`. La limpieza de usuarios LDAP es un proceso en segundo plano que busca automáticamente en la tabla de correspondencias LDAP de Nextcloud y verifica si los usuarios LDAP siguen disponibles. Los usuarios que no están disponibles se marcan como `deleted` en la tabla de base de datos `oc_preferences`. Después se puede ejecutar un comando que muestra esta tabla, solo con los usuarios marcados como `deleted`, y a continuación existe la opción de eliminar sus datos del directorio de datos de Nextcloud.

En la limpieza se eliminan estos elementos:

- Las asignaciones locales a grupos de Nextcloud
- Las preferencias del usuario (tabla de base de datos `oc_preferences`)
- La carpeta personal del usuario en Nextcloud
- La entrada correspondiente al usuario en `oc_storages`

La limpieza de usuarios LDAP tiene dos requisitos previos para funcionar:

1. Establecer `ldapUserCleanupInterval` en `config.php` con el intervalo de comprobación deseado, en minutos. El valor predeterminado es 51 minutos.

2. Que todas las conexiones LDAP configuradas estén activadas y funcionen correctamente. Como los usuarios pueden existir en varios servidores LDAP, conviene asegurarse de que todos los servidores LDAP estén disponibles, para que un usuario de un servidor LDAP desconectado temporalmente no quede marcado como `deleted`.

El proceso en segundo plano examina 50 usuarios cada vez y se ejecuta con el intervalo configurado en `ldapUserCleanupInterval`. Por ejemplo, con 200 usuarios LDAP y un `ldapUserCleanupInterval` de 20 minutos, el proceso examinará los primeros 50 usuarios, 20 minutos después los 50 siguientes, otros 20 minutos después los 50 siguientes, y así sucesivamente.

La cantidad de usuarios que se comprueban puede fijarse en un valor personalizado mediante un comando occ. El siguiente ejemplo la fija en 300:

`sudo -E -u www-data php occ config:app:set --value=300 user_ldap cleanUpJobChunkSize`

Hay dos comandos `occ` para examinar una tabla de los usuarios marcados como eliminados y después borrarlos manualmente. El comando `occ` está en el directorio de Nextcloud, por ejemplo `/var/www/nextcloud/occ`, y debe ejecutarse como el usuario HTTP. Para saber más sobre `occ`, véase {nc-doc}`admin_manual/occ_command`.

Estos ejemplos son para Ubuntu Linux:

1. `sudo -E -u www-data php occ ldap:show-remnants` muestra una tabla con todos los usuarios que se han marcado como eliminados, y sus datos LDAP.

2. `sudo -E -u www-data php occ user:delete [user]` elimina los datos del usuario del directorio de datos de Nextcloud.

Este ejemplo muestra el aspecto de la tabla de usuarios marcados como `deleted`:

```
$ sudo -E -u www-data php occ ldap:show-remnants
+-----------------+-----------------+------------------+--------------------------------------+
| Nextcloud name  | Display Name    | LDAP UID         | LDAP DN                              |
+-----------------+-----------------+------------------+--------------------------------------+
| aaliyah_brown   | aaliyah brown   | aaliyah_brown    | uid=aaliyah_brown,ou=people,dc=com   |
| aaliyah_hammes  | aaliyah hammes  | aaliyah_hammes   | uid=aaliyah_hammes,ou=people,dc=com  |
| aaliyah_johnston| aaliyah johnston| aaliyah_johnston | uid=aaliyah_johnston,ou=people,dc=com|
| aaliyah_kunze   | aaliyah kunze   | aaliyah_kunze    | uid=aaliyah_kunze,ou=people,dc=com   |
+-----------------+-----------------+------------------+--------------------------------------+
```

Además, pueden especificarse las siguientes opciones:

- `--short-date`: da a las fechas de `Last login` y `Detected on` un formato corto Y-m-d (p. ej., 2019-01-14)
- `--json`: en lugar de una tabla, la salida se codifica en json. Así es fácil procesar los datos mediante programación.

Después se puede ejecutar `sudo -E -u www-data php occ user:delete aaliyah_brown` para eliminar al usuario aaliyah_brown. Hay que usar el nombre de Nextcloud del usuario.

### Eliminar usuarios locales de Nextcloud

También puede usarse `occ user:delete [user]` para eliminar a un usuario local de Nextcloud; esto elimina su cuenta de usuario y sus datos.
````
