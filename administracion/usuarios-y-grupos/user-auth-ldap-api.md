---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "La API OCS de user_ldap para crear, leer, modificar y eliminar configuraciones LDAP, con ejemplos curl, salida XML y la tabla de claves."
---
# La API de configuración de LDAP

## Resumen

Esta página describe la API OCS de la app `user_ldap` para crear, eliminar, leer y modificar configuraciones LDAP, con un ejemplo `curl` y la salida XML de cada método, y la tabla de claves de configuración. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_user/user_auth_ldap_api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Todos los métodos exigen que la cabecera «OCS-APIREQUEST» tenga el valor «true». Los métodos admiten un parámetro opcional «format», que puede ser «xml» (el predeterminado) o «json».

### Crear una configuración

Crea una configuración LDAP nueva y vacía. Devuelve su ID. La autenticación se hace enviando una cabecera de autenticación HTTP básica.

**Sintaxis: ocs/v2.php/apps/user_ldap/api/v1/config**

- Método HTTP: POST

#### Ejemplo

```
$ curl -X POST https://admin:secret@example.com/ocs/v2.php/apps/user_ldap/api/v1/config -H "OCS-APIREQUEST: true"
```

- Crea una configuración nueva y vacía

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
 <meta>
  <status>ok</status>
  <statuscode>200</statuscode>
  <message>OK</message>
 </meta>
 <data>
  <configID>s01</configID>
 </data>
</ocs>
```

### Eliminar una configuración

Elimina una configuración LDAP dada. La autenticación se hace enviando una cabecera de autenticación HTTP básica.

**Sintaxis: ocs/v2.php/apps/user_ldap/api/v1/config/{configID}**

- Método HTTP: DELETE

#### Ejemplo

```
$ curl -X DELETE ``https://admin:secret@example.com/ocs/v2.php/apps/user_ldap/api/v1/config/s02 -H "OCS-APIREQUEST: true"
```

- elimina la configuración LDAP

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
 <meta>
  <status>ok</status>
  <statuscode>200</statuscode>
  <message>OK</message>
 </meta>
 <data/>
</ocs>
```

### Leer una configuración

Devuelve todas las claves y valores de la configuración LDAP indicada. La autenticación se hace enviando una cabecera de autenticación HTTP básica.

**Sintaxis: ocs/v2.php/apps/user_ldap/api/v1/config/{configID}**

- Método HTTP: GET
- argumento de URL: showPassword - int, opcional, predeterminado 0, si se devuelve la contraseña en texto claro

#### Ejemplo

```
$ curl -X GET https://admin:secret@example.com/ocs/v2.php/apps/user_ldap/api/v1/config/s02?showPassword=1 -H "OCS-APIREQUEST: true"
```

- obtiene la configuración LDAP

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
 <meta>
  <status>ok</status>
  <statuscode>200</statuscode>
  <message>OK</message>
 </meta>
 <data>
  <ldapHost>ldap://ldap.server.tld</ldapHost>
  <ldapPort>389</ldapPort>
  <ldapBackupHost></ldapBackupHost>
  <ldapBackupPort></ldapBackupPort>
  <ldapBase>ou=Department XLII,dc=example,dc=com</ldapBase>
  <ldapBaseUsers>ou=users,ou=Department XLII,dc=example,dc=com</ldapBaseUsers>
  <ldapBaseGroups>ou=Department XLII,dc=example,dc=com</ldapBaseGroups>
  <ldapAgentName>cn=root,dc=example,dc=com</ldapAgentName>
  <ldapAgentPassword>Secret</ldapAgentPassword>
  <ldapTLS>1</ldapTLS>
  <turnOffCertCheck>0</turnOffCertCheck>
  <ldapIgnoreNamingRules/>
  <ldapUserDisplayName>displayname</ldapUserDisplayName>
  <ldapUserDisplayName2>uid</ldapUserDisplayName2>
  <ldapGidNumber>gidNumber</ldapGidNumber>
  <ldapUserFilterObjectclass>inetOrgPerson</ldapUserFilterObjectclass>
  <ldapUserFilterGroups></ldapUserFilterGroups>
  <ldapUserFilter>(&amp;(objectclass=nextcloudUser)(nextcloudEnabled=TRUE))</ldapUserFilter>
  <ldapUserFilterMode>1</ldapUserFilterMode>
  <ldapGroupFilter>(&amp;(|(objectclass=nextcloudGroup)))</ldapGroupFilter>
  <ldapGroupFilterMode>0</ldapGroupFilterMode>
  <ldapGroupFilterObjectclass>nextcloudGroup</ldapGroupFilterObjectclass>
  <ldapGroupFilterGroups></ldapGroupFilterGroups>
  <ldapGroupMemberAssocAttr>memberUid</ldapGroupMemberAssocAttr>
  <ldapGroupDisplayName>cn</ldapGroupDisplayName>
  <ldapLoginFilter>(&amp;(|(objectclass=inetOrgPerson))(uid=%uid))</ldapLoginFilter>
  <ldapLoginFilterMode>0</ldapLoginFilterMode>
  <ldapLoginFilterEmail>0</ldapLoginFilterEmail>
  <ldapLoginFilterUsername>1</ldapLoginFilterUsername>
  <ldapLoginFilterAttributes></ldapLoginFilterAttributes>
  <ldapQuotaAttribute></ldapQuotaAttribute>
  <ldapQuotaDefault>20 MB</ldapQuotaDefault>
  <ldapEmailAttribute>mail</ldapEmailAttribute>
  <ldapCacheTTL>600</ldapCacheTTL>
  <ldapUuidUserAttribute>auto</ldapUuidUserAttribute>
  <ldapUuidGroupAttribute>auto</ldapUuidGroupAttribute>
  <ldapOverrideMainServer></ldapOverrideMainServer>
  <ldapConfigurationActive>1</ldapConfigurationActive>
  <ldapAttributesForUserSearch>uid;sn;givenname</ldapAttributesForUserSearch>
  <ldapAttributesForGroupSearch></ldapAttributesForGroupSearch>
  <ldapExperiencedAdmin>0</ldapExperiencedAdmin>
  <homeFolderNamingRule>attr:mail</homeFolderNamingRule>
  <hasPagedResultSupport></hasPagedResultSupport>
  <hasMemberOfFilterSupport>1</hasMemberOfFilterSupport>
  <useMemberOfToDetectMembership>1</useMemberOfToDetectMembership>
  <ldapExpertUsernameAttr></ldapExpertUsernameAttr>
  <ldapExpertUUIDUserAttr></ldapExpertUUIDUserAttr>
  <ldapExpertUUIDGroupAttr></ldapExpertUUIDGroupAttr>
  <lastJpegPhotoLookup>0</lastJpegPhotoLookup>
  <ldapNestedGroups>0</ldapNestedGroups>
  <ldapPagingSize>500</ldapPagingSize>
  <turnOnPasswordChange>1</turnOnPasswordChange>
  <ldapDynamicGroupMemberURL></ldapDynamicGroupMemberURL>
  <ldapDefaultPPolicyDN></ldapDefaultPPolicyDN>
 </data>
</ocs>
```

### Modificar una configuración

Actualiza una configuración con los valores proporcionados. La autenticación se hace enviando una cabecera de autenticación HTTP básica.

**Sintaxis: ocs/v2.php/apps/user_ldap/api/v1/config/{configID}**

- Método HTTP: PUT
- argumento de URL: configData - array, los campos están en la tabla de más abajo. Todos los campos son opcionales. Los valores deben ir codificados para URL.

#### Ejemplo

```
$ curl -X PUT https://admin:secret@example.com/ocs/v2.php/apps/user_ldap/api/v1/config/s01 -H "OCS-APIREQUEST: true" -d "configData[ldapHost]=ldap%3A%2F%2Fldap.server.tld &configData[ldapPort]=389"
```

- actualiza la configuración LDAP

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
 <meta>
  <status>ok</status>
  <statuscode>200</statuscode>
  <message>OK</message>
 </meta>
 <data/>
</ocs>
```

### Claves de configuración

| Clave | Modo | Obligatoria | Descripción |
|---|---|---|---|
| ldapHost | rw | sí | Host del servidor LDAP; admite indicar el protocolo |
| ldapPort | rw | sí | Puerto del servidor LDAP |
| ldapBackupHost | rw | no | Host de la réplica LDAP |
| ldapBackupPort | rw | no | Puerto de la réplica LDAP |
| ldapOverrideMainServer | rw | no | Si se usa la réplica en su lugar |
| ldapBase | rw | sí | Base |
| ldapBaseUsers | rw | no | Base para los usuarios; si no se especifica, se usa la base general |
| ldapBaseGroups | rw | no | Base para los grupos; si no se especifica, se usa la base general |
| ldapAgentName | rw | no | DN del usuario (de servicio) con el que conectarse a LDAP |
| ldapAgentPassword | rw | no | Contraseña del usuario de servicio |
| ldapTLS | rw | no | Si se usa StartTLS |
| turnOffCertCheck | rw | no | Desactiva la validación de certificados en las conexiones TLS |
| ldapIgnoreNamingRules | rw | no | Compatibilidad con versiones anteriores; no establecerla. |
| ldapUserDisplayName | rw | sí | Atributo usado como nombre mostrado de los usuarios |
| ldapUserDisplayName2 | rw | no | Atributo adicional; si se establece, se muestra entre paréntesis junto al atributo principal |
| ldapUserAvatarRule | rw | no | Especifica el comportamiento de la integración de avatares; valores posibles: «default», «none», «data:$ATTRIBUTENAME» |
| ldapGidNumber | rw | no | atributo de ID de grupo, necesario para los grupos primarios en OpenLDAP (y compatibles) |
| ldapUserFilterObjectclass | rw | no | lo establece el asistente de configuración (interfaz web) |
| ldapUserFilterGroups | rw | no | lo establece el asistente de configuración (interfaz web) |
| ldapUserFilter | rw | sí | Filtro LDAP usado para obtener el usuario |
| ldapUserFilterMode | rw | no | lo usa el asistente de configuración; establecerlo en 1 para la edición manual |
| ldapAttributesForUserSearch | rw | no | atributos que deben coincidir al buscar usuarios; separarlos con ; |
| ldapGroupFilter | rw | no | Filtro LDAP usado para obtener los grupos |
| ldapGroupFilterMode | rw | no | lo usa el asistente de configuración; establecerlo en 1 para la edición manual |
| ldapGroupFilterObjectclass | rw | no | lo establece el asistente de configuración (interfaz web) |
| ldapGroupFilterGroups | rw | no | lo establece el asistente de configuración (interfaz web) |
| ldapGroupMemberAssocAttr | rw | no | atributo que indica los miembros del grupo; uno de: member, memberUid, uniqueMember, gidNumber |
| ldapGroupDisplayName | rw | no | Atributo usado como nombre mostrado de los grupos; obligatorio si se usan grupos |
| ldapAttributesForGroupSearch | rw | no | atributos que deben coincidir al buscar grupos; separarlos con ; |
| ldapLoginFilter | rw | sí | Filtro LDAP usado para autenticar a los usuarios |
| ldapLoginFilterMode | rw | no | lo usa el asistente de configuración; establecerlo en 1 para la edición manual |
| ldapLoginFilterEmail | rw | no | lo establece el asistente de configuración (interfaz web) |
| ldapLoginFilterUsername | rw | no | lo establece el asistente de configuración (interfaz web) |
| ldapLoginFilterAttributes | rw | no | lo establece el asistente de configuración (interfaz web) |
| ldapQuotaAttribute | rw | no | Atributo LDAP que contiene el valor de la cuota (por usuario) |
| ldapQuotaDefault | rw | no | Cuota predeterminada, si el atributo de cuota especificado está vacío |
| ldapEmailAttribute | rw | no | Atributo LDAP que contiene la dirección de correo electrónico (toma la primera si hay varias almacenadas) |
| ldapCacheTTL | rw | no | Cuánto tiempo se almacenan en caché los resultados de LDAP; por defecto, 10 min |
| ldapUuidUserAttribute | r | no | se establece en tiempo de ejecución |
| ldapUuidGroupAttribute | r | no | se establece en tiempo de ejecución |
| ldapConfigurationActive | rw | no | si esta configuración está activa. 1 es activada, 0 es desactivada. |
| ldapExperiencedAdmin | rw | no | lo usa el asistente de configuración; establecerlo en 1 para la edición manual |
| homeFolderNamingRule | rw | no | Atributo LDAP que se usa como nombre de la carpeta del usuario |
| hasPagedResultSupport | r | no | se establece en tiempo de ejecución |
| hasMemberOfFilterSupport | r | no | se establece en tiempo de ejecución |
| useMemberOfToDetectMembership | rw | no | Si se usa memberOf para detectar la pertenencia a grupos |
| ldapExpertUsernameAttr | rw | no | Atributo LDAP que se usa como nombre de usuario interno. Puede modificarse (p. ej., para evitar colisiones de nombres o restricciones de caracteres) |
| ldapExpertUUIDUserAttr | rw | no | sustituye el atributo UUID de los servidores LDAP para identificar los registros de usuarios LDAP |
| ldapExpertUUIDGroupAttr | rw | no | sustituye el atributo UUID de los servidores LDAP para identificar los registros de grupos LDAP |
| lastJpegPhotoLookup | r | no | se establece en tiempo de ejecución |
| ldapNestedGroups | rw | no | Si LDAP admite grupos anidados |
| ldapPagingSize | rw | no | Número de resultados que se devuelven por página |
| turnOnPasswordChange | rw | no | Si los usuarios pueden cambiar sus contraseñas (¡el hash debe hacerse en LDAP!) |
| ldapDynamicGroupMemberURL | rw | no | URL para los grupos dinámicos |
| ldapDefaultPPolicyDN | rw | no | DN de PPolicy para las reglas de contraseñas |
| ldapConnectionTimeout | rw | no | Establece la opción de conexión `LDAP_OPT_NETWORK_TIMEOUT`. Por defecto, 15 s. |
````
