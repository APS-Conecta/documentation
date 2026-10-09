---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Llamadas OCS para listar las apps instaladas, consultar la información de una app y activarla o desactivarla, con ejemplos y su salida XML."
---
# Conjunto de instrucciones para apps

## Resumen

Esta página es la referencia de las llamadas de la API OCS que gestionan las apps del servidor: listarlas, consultar su información, activarlas y desactivarlas. Está dirigida a quienes administran el servidor o lo automatizan.

````{upstream} admin_manual/configuration_user/instruction_set_for_apps.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Obtener la lista de apps

Devuelve la lista de apps instaladas en el servidor Nextcloud. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/apps/**

- Método HTTP: GET
- Argumento de URL: filter, cadena - opcional (`enabled` o `disabled`)

Códigos de estado:

- 100 - correcto
- 101 - datos de entrada no válidos

#### Ejemplo

```
$ curl -X GET http://admin:secret@example.com/ocs/v1.php/cloud/apps?filter=enabled -H "OCS-APIRequest: true"
```

- Obtiene las apps activadas

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <statuscode>100</statuscode>
    <status>ok</status>
  </meta>
  <data>
    <apps>
      <element>files</element>
      <element>provisioning_api</element>
    </apps>
  </data>
</ocs>
```

### Obtener la información de una app

Proporciona información sobre una aplicación concreta. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/apps/{appid}**

- Método HTTP: GET

Códigos de estado:

- 100 - correcto

#### Ejemplo

```
$ curl -X GET http://admin:secret@example.com/ocs/v1.php/cloud/apps/files -H "OCS-APIRequest: true"
```

- Obtiene la información de la app `files`

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <statuscode>100</statuscode>
    <status>ok</status>
  </meta>
  <data>
    <info/>
    <remote>
      <files>appinfo/remote.php</files>
      <webdav>appinfo/remote.php</webdav>
      <filesync>appinfo/filesync.php</filesync>
    </remote>
    <public/>
    <id>files</id>
    <name>Files</name>
    <description>File Management</description>
    <licence>AGPL-3.0-or-later</licence>
    <author>Robin Appelman</author>
    <require>4.9</require>
    <shipped>true</shipped>
    <active>true</active>
    <standalone></standalone>
    <default_enable></default_enable>
    <types>
      <element>filesystem</element>
    </types>
  </data>
</ocs>
```

### Activar una app

Activa una app. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/apps/{appid}**

- Método HTTP: POST

Códigos de estado:

- 100 - correcto

#### Ejemplo

```
$ curl -X POST http://admin:secret@example.com/ocs/v1.php/cloud/apps/files_texteditor -H "OCS-APIRequest: true"
```

- Activa la app `files_texteditor`

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <statuscode>100</statuscode>
    <status>ok</status>
  </meta>
</ocs>
```

### Desactivar una app

Desactiva la app indicada. La autenticación se realiza enviando una cabecera Basic HTTP Authorization.

**Sintaxis: ocs/v1.php/cloud/apps/{appid}**

- Método HTTP: DELETE

Códigos de estado:

- 100 - correcto

#### Ejemplo

```
$ curl -X DELETE http://admin:secret@example.com/ocs/v1.php/cloud/apps/files_texteditor -H "OCS-APIRequest: true"
```

- Desactiva la app `files_texteditor`

#### Salida XML

```xml
<?xml version="1.0"?>
<ocs>
  <meta>
    <statuscode>100</statuscode>
    <status>ok</status>
  </meta>
</ocs>
```
````
