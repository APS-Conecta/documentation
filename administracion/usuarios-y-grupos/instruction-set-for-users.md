---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Llamadas OCS para crear, buscar, editar, desactivar y eliminar usuarios y gestionar sus grupos y subadministración, con ejemplos y salida XML."
---
# Conjunto de instrucciones para usuarios

## Resumen

Esta página es la referencia de las llamadas de la API OCS que gestionan los usuarios: crearlos, buscarlos, editar sus datos, desactivarlos, activarlos y eliminarlos, gestionar sus grupos y su subadministración, y reenviar el correo de bienvenida. Está dirigida a quienes administran el servidor o lo automatizan.

````{upstream} admin_manual/configuration_user/instruction_set_for_users.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Añadir un usuario nuevo

Crea un usuario nuevo en el servidor Nextcloud. La autenticación se realiza enviando una cabecera de autenticación HTTP básica.

**Sintaxis: ocs/v1.php/cloud/users**

- Método HTTP: POST
- Argumento POST: userid - cadena, el nombre de usuario obligatorio del usuario nuevo
- Argumento POST: password - cadena, la contraseña del usuario nuevo; dejarla vacía para enviar el correo de bienvenida
- Argumento POST: displayName - cadena, el nombre mostrado del usuario nuevo
- Argumento POST: email - cadena, el correo electrónico del usuario nuevo; obligatorio si la contraseña está vacía
- Argumento POST: groups - matriz, los grupos del usuario nuevo
- Argumento POST: subadmin - matriz, los grupos en los que el usuario nuevo es subadministrador
- Argumento POST: quota - cadena, la cuota del usuario nuevo
- Argumento POST: language - cadena, el idioma del usuario nuevo

Códigos de estado:

- 101 - argumento no válido
- 102 - el usuario ya existe
- 103 - no se pueden crear subadministradores para el grupo admin
- 104 - el grupo no existe
- 105 - privilegios insuficientes para el grupo
- 106 - no se indicó ningún grupo (obligatorio para los subadministradores)
- 107 - excepciones de sugerencia
- 108 - se necesita una dirección de correo electrónico para enviar al usuario un enlace de contraseña.
- 109 - el grupo de subadministración no existe
- 110 - no se proporcionó la dirección de correo electrónico obligatoria
- 111 - no se pudo crear el ID de usuario inexistente

#### Ejemplo

```
$ curl -X POST http://admin:secret@example.com/ocs/v1.php/cloud/users -d userid="Frank" -d password="frankspassword" -H "OCS-APIRequest: true"
```

- Crea el usuario `Frank` con la contraseña `frankspassword`
- opcionalmente, pueden indicarse grupos con uno o más parámetros de consulta `groups[]`:
  `URL -d groups[]="admin" -D groups[]="Team1"`

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message/>
 </meta>
 <data/>
</ocs>
```

### Buscar u obtener usuarios

Obtiene una lista de usuarios del servidor Nextcloud. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/users**

- Método HTTP: GET
- Argumentos de URL: search - cadena, cadena de búsqueda opcional
- Argumentos de URL: limit - int, valor de límite opcional
- Argumentos de URL: offset - int, valor de desplazamiento opcional

Códigos de estado:

- 100 - correcto

#### Ejemplo

```
$ curl -X GET http://admin:secret@example.com/ocs/v1.php/cloud/users?search=Frank -H "OCS-APIRequest: true"
```

- Devuelve la lista de usuarios que coinciden con la cadena de búsqueda.

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <statuscode>100</statuscode>
    <status>ok</status>
  </meta>
  <data>
    <users>
      <element>Frank</element>
     </users>
  </data>
</ocs>
```

### Obtener los datos de un usuario

Obtiene información sobre un usuario. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/users/{userid}**

- Método HTTP: GET

Códigos de estado:

- 100 - correcto

#### Ejemplo

```
$ curl -X GET http://admin:secret@example.com/ocs/v1.php/cloud/users/Frank -H "OCS-APIRequest: true"
```

- Devuelve información sobre el usuario `Frank`

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <statuscode>100</statuscode>
    <status>ok</status>
  </meta>
  <data>
    <enabled>true</enabled>
    <id>Frank</id>
    <quota>0</quota>
    <email>frank@example.org</email>
    <displayname>Frank K.</displayname>
    <display-name>Frank K.</display-name>
    <phone>0123 / 456 789</phone>
    <address>Foobar 12, 12345 Town</address>
    <website>https://nextcloud.com</website>
    <twitter>Nextcloud</twitter>
    <groups>
     <element>group1</element>
     <element>group2</element>
    </groups>
  </data>
</ocs>
```

### Editar los datos de un usuario

Edita los atributos de un usuario. Los usuarios pueden editar el correo electrónico, el nombre mostrado y la contraseña; los administradores también pueden editar el valor de la cuota. Pueden aplicarse más restricciones: consultar el endpoint {ref}`Lista de campos de datos editables <nc-editable_field_list>`. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/users/{userid}**

- Método HTTP: PUT
- Argumento PUT: key, el campo que se edita:

  - email
  - quota
  - displayname
  - display (**obsoleto**, usar *displayname* en su lugar)
  - phone
  - address
  - website
  - twitter
  - password

- Argumento PUT: value, el nuevo valor del campo

Códigos de estado:

- 101 - argumento no válido
- 107 - política de contraseñas (excepción de sugerencia)
- 112 - el backend de usuarios no admite establecer la contraseña
- 113 - no se permite editar el campo / el campo no existe

#### Ejemplos

```
$ curl -X PUT http://admin:secret@example.com/ocs/v1.php/cloud/users/Frank -d key="email" -d value="franksnewemail@example.org" -H "OCS-APIRequest: true"
```

- Actualiza la dirección de correo electrónico del usuario `Frank`

```
$ curl -X PUT http://admin:secret@example.com/ocs/v1.php/cloud/users/Frank -d key="quota" -d value="100MB" -H "OCS-APIRequest: true"
```

- Actualiza la cuota del usuario `Frank`

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <statuscode>100</statuscode>
    <status>ok</status>
  </meta>
  <data/>
</ocs>
```

(nc-editable_field_list)=
### Lista de campos de datos editables

Edita los atributos de un usuario. Los usuarios pueden editar el correo electrónico, el nombre mostrado y la contraseña; los administradores también pueden editar el valor de la cuota. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/user/fields**

- Método HTTP: GET

Códigos de estado:

- 100 - correcto

#### Ejemplos

```
$ curl -X GET http://admin:secret@example.com/ocs/v1.php/cloud/user/fields -H "OCS-APIRequest: true"
```

- Obtiene la lista de campos

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
 </meta>
 <data>
  <element>displayname</element>
  <element>email</element>
  <element>phone</element>
  <element>address</element>
  <element>website</element>
  <element>twitter</element>
 </data>
</ocs>
```

### Desactivar un usuario

Desactiva un usuario en el servidor Nextcloud para que ya no pueda iniciar sesión. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/users/{userid}/disable**

- Método HTTP: PUT

Códigos de estado:

- 100 - correcto
- 101 - error

#### Ejemplo

```
$ curl -X PUT http://admin:secret@example.com/ocs/v1.php/cloud/users/Frank/disable -H "OCS-APIRequest: true"
```

- Desactiva al usuario `Frank`

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <status>ok</status>
    <statuscode>100</statuscode>
    <message/>
  </meta>
  <data/>
</ocs>
```

### Activar un usuario

Activa un usuario en el servidor Nextcloud para que pueda volver a iniciar sesión. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/users/{userid}/enable**

- Método HTTP: PUT

Códigos de estado:

- 100 - correcto
- 101 - error

#### Ejemplo

```
$ curl -X PUT http://admin:secret@example.com/ocs/v1.php/cloud/users/Frank/enable -H "OCS-APIRequest: true"
```

- Activa al usuario `Frank`

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <status>ok</status>
    <statuscode>100</statuscode>
    <message/>
  </meta>
  <data/>
</ocs>
```

### Eliminar un usuario

Elimina un usuario del servidor Nextcloud. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/users/{userid}**

- Método HTTP: DELETE

Códigos de estado:

- 100 - correcto
- 101 - error

#### Ejemplo

```
$ curl -X DELETE http://admin:secret@example.com/ocs/v1.php/cloud/users/Frank -H "OCS-APIRequest: true"
```

- Elimina al usuario `Frank`

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <statuscode>100</statuscode>
    <status>ok</status>
  </meta>
  <data/>
</ocs>
```

### Obtener los grupos de un usuario

Obtiene la lista de grupos de los que es miembro el usuario indicado. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/users/{userid}/groups**

- Método HTTP: GET

Códigos de estado:

- 100 - correcto

#### Ejemplo

```
$ curl -X GET http://admin:secret@example.com/ocs/v1.php/cloud/users/Frank/groups -H "OCS-APIRequest: true"
```

- Obtiene la lista de grupos de los que `Frank` es miembro

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <statuscode>100</statuscode>
    <status>ok</status>
  </meta>
  <data>
    <groups>
      <element>admin</element>
      <element>group1</element>
    </groups>
  </data>
</ocs>
```

### Añadir un usuario a un grupo

Añade el usuario indicado al grupo indicado. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/users/{userid}/groups**

- Método HTTP: POST
- Argumento POST: groupid, cadena - el grupo al que se añade el usuario

Códigos de estado:

- 100 - correcto
- 101 - no se indicó ningún grupo
- 102 - el grupo no existe
- 103 - el usuario no existe
- 104 - privilegios insuficientes
- 105 - no se pudo añadir el usuario al grupo

#### Ejemplo

```
$ curl -X POST http://admin:secret@example.com/ocs/v1.php/cloud/users/Frank/groups -d groupid="newgroup" -H "OCS-APIRequest: true"
```

- Añade el usuario `Frank` al grupo `newgroup`

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <statuscode>100</statuscode>
    <status>ok</status>
  </meta>
  <data/>
</ocs>
```

### Quitar un usuario de un grupo

Quita el usuario indicado del grupo indicado. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/users/{userid}/groups**

- Método HTTP: DELETE
- Argumento DELETE: groupid, cadena - el grupo del que se quita el usuario

Códigos de estado:

- 100 - correcto
- 101 - no se indicó ningún grupo
- 102 - el grupo no existe
- 103 - el usuario no existe
- 104 - privilegios insuficientes
- 105 - no se pudo quitar el usuario del grupo

#### Ejemplo

```
$ curl -X DELETE http://admin:secret@example.com/ocs/v1.php/cloud/users/Frank/groups -d groupid="newgroup" -H "OCS-APIRequest: true"
```

- Quita el usuario `Frank` del grupo `newgroup`

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <statuscode>100</statuscode>
    <status>ok</status>
  </meta>
  <data/>
</ocs>
```

### Promover un usuario a subadministrador

Convierte a un usuario en subadministrador de un grupo. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/users/{userid}/subadmins**

- Método HTTP: POST
- Argumento POST: groupid, cadena - el grupo del que el usuario pasa a ser
  subadministrador

Códigos de estado:

- 100 - correcto
- 101 - el usuario no existe
- 102 - el grupo no existe
- 103 - error desconocido

#### Ejemplo

```
$ curl -X POST https://admin:secret@example.com/ocs/v1.php/cloud/users/Frank/subadmins -d groupid="group" -H "OCS-APIRequest: true"
```

- Convierte al usuario `Frank` en subadministrador del grupo `group`

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <statuscode>100</statuscode>
    <status>ok</status>
  </meta>
  <data/>
</ocs>
```

### Retirar a un usuario como subadministrador

Quita los derechos de subadministrador del usuario indicado en el grupo indicado. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/users/{userid}/subadmins**

- Método HTTP: DELETE
- Argumento DELETE: groupid, cadena - el grupo en el que se quitan los derechos de
  subadministrador del usuario

Códigos de estado:

- 100 - correcto
- 101 - el usuario no existe
- 102 - el usuario no es subadministrador del grupo / el grupo no existe
- 103 - error desconocido

#### Ejemplo

```
$ curl -X DELETE https://admin:secret@example.com/ocs/v1.php/cloud/users/Frank/subadmins -d groupid="oldgroup" -H "OCS-APIRequest: true"
```

- Quita los derechos de subadministrador de `Frank's` en el grupo `oldgroup`

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <statuscode>100</statuscode>
    <status>ok</status>
  </meta>
  <data/>
</ocs>
```

### Obtener los grupos en los que un usuario es subadministrador

Devuelve los grupos en los que el usuario es subadministrador. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/users/{userid}/subadmins**

- Método HTTP: GET

Códigos de estado:

- 100 - correcto
- 101 - el usuario no existe
- 102 - error desconocido

#### Ejemplo

```
$ curl -X GET https://admin:secret@example.com/ocs/v1.php/cloud/users/Frank/subadmins -H "OCS-APIRequest: true"
```

- Devuelve los grupos de los que `Frank` es subadministrador

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
      <status>ok</status>
      <statuscode>100</statuscode>
    <message/>
  </meta>
  <data>
    <element>testgroup</element>
  </data>
</ocs>
```

### Reenviar el correo de bienvenida

La petición a este endpoint vuelve a enviar el correo de bienvenida a este usuario.

**Sintaxis: ocs/v1.php/cloud/users/{userid}/welcome**

- Método HTTP: POST

Códigos de estado:

- 100 - correcto
- 101 - dirección de correo electrónico no disponible
- 102 - falló el envío del correo

#### Ejemplo

```
$ curl -X POST https://admin:secret@example.com/ocs/v1.php/cloud/users/Frank/welcome -H "OCS-APIRequest: true"
```

- Envía el correo de bienvenida a `Frank`

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
      <status>ok</status>
      <statuscode>100</statuscode>
    <message/>
  </meta>
  <data/>
</ocs>
```
````
