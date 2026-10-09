---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Comandos occ de LDAP: buscar y comprobar usuarios y grupos, y crear, modificar, probar y eliminar configuraciones de LDAP."
---
# Comandos de LDAP

## Resumen

Esta página es la referencia de los comandos `occ` de LDAP, disponibles cuando la app de LDAP está activada: buscar usuarios, comprobar usuarios y grupos, y crear, mostrar, modificar, probar y eliminar configuraciones de LDAP. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/occ_ldap.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
(nc-ldap_commands_label)=
### Comandos de LDAP

:::{note}
Estos comandos solo están disponibles cuando la app «Motor de usuarios y grupos LDAP» (`user_ldap`) está activada.
:::

Estos comandos de LDAP solo aparecen cuando se ha activado la app de LDAP. Entonces se pueden ejecutar los siguientes comandos de LDAP con `occ`:

```
ldap
 ldap:check-user               checks whether a user exists on LDAP.
 ldap:check-group              checks whether a group exists on LDAP.
 ldap:create-empty-config      creates an empty LDAP configuration
 ldap:delete-config            deletes an existing LDAP configuration
 ldap:search                   executes a user or group search
 ldap:set-config               modifies an LDAP configuration
 ldap:show-config              shows the LDAP configuration
 ldap:show-remnants            shows which users are not available on
                               LDAP anymore, but have remnants in
                               Nextcloud.
 ldap:test-config              tests an LDAP configuration
 ldap:test-user-settings       runs tests and show information about user
                               related LDAP settings
```

#### ldap:search

Buscar un usuario de LDAP, con esta sintaxis

> sudo -E -u www-data php occ ldap:search [--group] [--offset="..."]
> [--limit="..."] search

Las búsquedas solo coinciden con el comienzo del valor del atributo. Este ejemplo busca los givenName que empiezan por «rob»:

```
sudo -E -u www-data php occ ldap:search "rob"
```

Esto encuentra a robbie, roberta y robin. Para ampliar la búsqueda y encontrar, por ejemplo, `jeroboam`, usar el comodín asterisco:

```
sudo -E -u www-data php occ ldap:search "*rob"
```

Los atributos de búsqueda de usuarios se establecen con `ldap:set-config` (más abajo). Por ejemplo, si los atributos de búsqueda son `givenName` y `sn`, se pueden encontrar usuarios por nombre + apellido muy rápidamente. Por ejemplo, Terri Hanson se encuentra buscando `te ha`. Los espacios en blanco finales se ignoran.

#### ldap:check-user

Comprobar si existe un usuario de LDAP. Solo funciona si el servidor Nextcloud está conectado a un servidor LDAP:

```
sudo -E -u www-data php occ ldap:check-user robert
```

Usar `--update` para actualizar los campos de la cuenta desde LDAP:

```
sudo -E -u www-data php occ ldap:check-user --update robert
```

No ejecuta ninguna comprobación cuando encuentra una conexión LDAP desactivada. Así se evita que los usuarios que existen en conexiones LDAP desactivadas se marquen como eliminados. Si se sabe con certeza que el usuario buscado no está en una de las conexiones desactivadas y existe en una conexión activa, usar la opción `--force` para forzar la comprobación en todas las conexiones LDAP activas:

```
sudo -E -u www-data php occ ldap:check-user --force robert
```

También se puede usar `--all-seen-users` para ejecutar la comprobación en todos los usuarios que han iniciado sesión en Nextcloud al menos una vez. Se pueden usar `--limit` y `--offset` para hacerlo por lotes. Puede combinarse con `--update` para actualizar la información de los usuarios vistos.

#### ldap:check-group

Comprueba si un grupo sigue existiendo en el directorio LDAP. Usarlo con `--update` para actualizar la caché de miembros del grupo en el lado de Nextcloud:

```
sudo -E -u www-data php occ ldap:check-group --update mygroup
```

#### ldap:create-empty-config

Crea una configuración de LDAP vacía. La primera que se crea tiene el `configID` `s01`, y a todas las configuraciones que se creen después se les asignan ID automáticamente:

```
sudo -E -u www-data php occ ldap:create-empty-config
   Created new configuration with configID 's01'
```

Después se pueden listar y ver las configuraciones:

```
sudo -E -u www-data php occ ldap:show-config
```

Y ver la configuración de un único configID:

```
sudo -E -u www-data php occ ldap:show-config s01
```

#### ldap:delete-config

Elimina una configuración de LDAP existente:

```
sudo -E -u www-data php occ ldap:delete  s01
Deleted configuration with configID 's01'
```

#### ldap:set-config

Este comando sirve para modificar configuraciones, como en este ejemplo, que establece los atributos de búsqueda:

```
sudo -E -u www-data php occ ldap:set-config s01 ldapAttributesForUserSearch
"cn;givenname;sn;displayname;mail"
```

#### ldap:test-config

Comprueba si la configuración es correcta y puede vincularse al servidor:

```
sudo -E -u www-data php occ ldap:test-config s01
The configuration is valid and the connection could be established!
```

#### ldap:test-user-settings

Comprueba los ajustes de LDAP relacionados con los usuarios:

```
sudo -E -u www-data php occ ldap:test-user-settings "cn=philip j. fry,ou=people,dc=planetexpress,dc=com" --group "Everyone"

User cn=philip j. fry,ou=people,dc=planetexpress,dc=com is mapped with account name fry.
Known UUID is ce6cd914-71d5-103f-95a8-ad2dab17b2f9.
Configuration prefix is s01

Attributes set in configuration:
- ldapExpertUsernameAttr: uid
- ldapUuidUserAttribute: auto
- ldapEmailAttribute: mail
- ldapUserDisplayName: cn

Attributes fetched from LDAP using filter (|(objectclass=inetOrgPerson)):
- entryuuid: ["ce6cd914-71d5-103f-95a8-ad2dab17b2f9"]
- uid: ["fry"]
- mail: ["fry@planetexpress.com"]
- cn: ["Philip J. Fry"]

Detected UUID attribute: entryuuid

UUID for cn=philip j. fry,ou=people,dc=planetexpress,dc=com: ce6cd914-71d5-103f-95a8-ad2dab17b2f9

Group information:
Configuration:
- ldapGroupFilter: (|(objectclass=groupOfNames))
- ldapGroupMemberAssocAttr: member

Primary group:
Group from gidNumber:
All known groups: ["Ship crew", "Everyone"]
MemberOf usage: off (0,1)

Group Everyone:
Group cn=everyone,ou=groups,dc=planetexpress,dc=com is mapped with name Everyone.
Known UUID is ce8b61c2-71d5-103f-95af-ad2dab17b2f9.
Members: ["bender", "fry", "leela"]
```

#### ldap:show-remnants

Se usa para limpiar la tabla de asignaciones de LDAP y está documentado en {nc-doc}`admin_manual/configuration_user/user_auth_ldap_cleanup`.
````
