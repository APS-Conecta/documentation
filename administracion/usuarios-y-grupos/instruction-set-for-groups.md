---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Llamadas OCS para buscar, crear, editar y eliminar grupos y para consultar sus miembros y subadministradores, con ejemplos y su salida XML."
---
# Conjunto de instrucciones para grupos

## Resumen

Esta página es la referencia de las llamadas de la API OCS que gestionan los grupos: buscarlos, crearlos, editarlos y eliminarlos, y consultar sus miembros y subadministradores. Está dirigida a quienes administran el servidor o lo automatizan.

````{upstream} admin_manual/configuration_user/instruction_set_for_groups.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Buscar u obtener grupos

Obtiene una lista de grupos del servidor Nextcloud. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/groups**

- Método HTTP: GET
- Argumentos de URL: search - cadena, cadena de búsqueda opcional
- Argumentos de URL: limit - int, valor de límite opcional
- Argumentos de URL: offset - int, valor de desplazamiento opcional

Códigos de estado:

- 100 - correcto

#### Ejemplo

```
$ curl -X GET http://admin:secret@example.com/ocs/v1.php/cloud/groups?search=adm -H "OCS-APIRequest: true"
```

- Devuelve la lista de grupos que coinciden con la cadena de búsqueda.

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
    </groups>
  </data>
</ocs>
```

### Crear un grupo

Añade un grupo nuevo. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/groups**

- Método HTTP: POST
- Argumento POST: groupid, cadena - el nombre del grupo nuevo

Códigos de estado:

- 100 - correcto
- 101 - datos de entrada no válidos
- 102 - el grupo ya existe
- 103 - no se pudo añadir el grupo

#### Ejemplo

```
$ curl -X POST http://admin:secret@example.com/ocs/v1.php/cloud/groups -d groupid="newgroup" -H "OCS-APIRequest: true"
```

- Añade un grupo nuevo llamado `newgroup`

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

### Obtener los miembros de un grupo

Obtiene la lista de miembros del grupo. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/groups/{groupid}**

- Método HTTP: GET

Códigos de estado:

- 100 - correcto

#### Ejemplo

```
$ curl -X GET http://admin:secret@example.com/ocs/v1.php/cloud/groups/admin -H "OCS-APIRequest: true"
```

- Devuelve la lista de usuarios del grupo `admin`

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

### Obtener los subadministradores de un grupo

Devuelve los subadministradores del grupo. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/groups/{groupid}/subadmins**

- Método HTTP: GET

Códigos de estado:

- 100 - correcto
- 101 - el grupo no existe
- 102 - error desconocido

#### Ejemplo

```
$ curl -X GET https://admin:secret@example.com/ocs/v1.php/cloud/groups/mygroup/subadmins -H "OCS-APIRequest: true"
```

- Devuelve los subadministradores del grupo: `mygroup`

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
    <element>Tom</element>
  </data>
</ocs>
```

### Editar los datos de un grupo

Edita los atributos de un grupo. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/groups/{groupid}**

- Método HTTP: PUT
- Argumento PUT: key, cadena - el campo que se edita:

  - displayname

- Argumento PUT: value, cadena - el nuevo valor del campo

Códigos de estado:

- 100 - correcto
- 101 - el backend no lo admite

#### Ejemplos

```
$ curl -X PUT http://admin:secret@example.com/ocs/v1.php/cloud/groups/mygroup -d key="displayname" -d value="My Group Name" -H "OCS-APIRequest: true"
```

- Actualiza el nombre mostrado del grupo `mygroup`

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

### Eliminar un grupo

Elimina un grupo. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/groups/{groupid}**

- Método HTTP: DELETE

Códigos de estado:

- 100 - correcto
- 101 - el grupo no existe
- 102 - no se pudo eliminar el grupo

#### Ejemplo

```
$ curl -X DELETE http://admin:secret@example.com/ocs/v1.php/cloud/groups/mygroup -H "OCS-APIRequest: true"
```

- Elimina el grupo `mygroup`

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
````
