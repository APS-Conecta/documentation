---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de recursos compartidos: crear, consultar, actualizar y eliminar recursos compartidos locales y federados; atributos y envío de correo."
---
# API OCS de recursos compartidos

## Resumen

Esta página describe, para quienes desarrollan clientes o apps, la API OCS de recursos compartidos: las llamadas para listar, crear, actualizar y eliminar recursos compartidos locales, sus atributos, el envío de correo a los destinatarios y la gestión de recursos compartidos de nube federada.

````{upstream} developer_manual/client_apis/OCS/ocs-share-api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

La API OCS de recursos compartidos permite acceder a la API de uso compartido desde fuera mediante llamadas OCS predefinidas.

La URL base de todas las llamadas a la API de recursos compartidos es: `<nextcloud_base_url>/ocs/v2.php/apps/files_sharing/api/v1`

Todas las llamadas a endpoints OCS requieren que la cabecera `OCS-APIRequest` tenga el valor `true`.

### Recursos compartidos locales

#### Obtener todos los recursos compartidos

Obtener todos los recursos compartidos del usuario.

- Sintaxis: /shares
- Método: GET
- Resultado: XML con todos los recursos compartidos

Códigos de estado:

- 100 - correcto
- 404 - no se pudieron obtener los recursos compartidos

#### Obtener los recursos compartidos de un archivo o carpeta concretos

Obtener todos los recursos compartidos de un archivo o carpeta dados.

- Sintaxis: /shares
- Método: GET
- Argumentos de URL: path - (string) ruta al archivo o carpeta
- Argumentos de URL: reshares - (boolean) devuelve no solo los recursos compartidos del usuario actual, sino todos los recursos compartidos del archivo dado.
- Argumentos de URL: subfiles - (boolean) devuelve todos los recursos compartidos dentro de una carpeta, siempre que
  *path* defina una carpeta
- Campos obligatorios: path
- Resultado: XML con los recursos compartidos

Códigos de estado:

- 100 - correcto
- 400 - no es un directorio (si se usó el argumento 'subfile')
- 404 - el archivo no existe

#### Obtener información sobre un recurso compartido conocido

Obtener información sobre un recurso compartido dado.

- Sintaxis: /shares/*<share_id>*
- Método: GET
- Argumentos: share_id - (int) ID del recurso compartido
- Resultado: XML con la información del recurso compartido

Códigos de estado:

- 100 - correcto
- 404 - el recurso compartido no existe

(ocs-share-api-create-a-new-share)=
#### Crear un nuevo recurso compartido

Compartir un archivo o carpeta con un usuario o grupo, o como enlace público.

- Sintaxis: /shares
- Método: POST
- Argumentos POST: path - (string) ruta al archivo o carpeta que se debe compartir
- Argumentos POST: shareType - (int) 0 = usuario; 1 = grupo; 3 = enlace público; 4 = correo electrónico; 6 = recurso compartido de nube federada; 7 = círculo; 10 = conversación de Talk
- Argumentos POST: shareWith - (string) ID de usuario / de grupo / dirección de correo electrónico / circleID / nombre de la conversación con quien se debe compartir el archivo
- Argumentos POST: publicUpload - (string) permitir la subida pública a una carpeta compartida públicamente (true/false)
- Argumentos POST: password - (string) contraseña con la que proteger el recurso compartido por enlace público
- Argumentos POST: permissions - (int) 1 = leer; 2 = actualizar; 4 = crear; 8 = eliminar;
  16 = compartir; 31 = todos (predeterminado: 31; para recursos compartidos públicos: 1)
- Argumentos POST: expireDate - (string) establecer una fecha de caducidad para los recursos compartidos por
  enlace público. Este argumento espera una cadena de fecha con formato correcto, p. ej., 'YYYY-MM-DD'
- Argumentos POST: note - (string) añade una nota para el destinatario del recurso compartido.
- Argumentos POST: label - (string) añade una etiqueta para el destinatario del recurso compartido.
- Argumentos POST: attributes - (string) cadena JSON serializada y codificada como URI para los {nc-ref}`atributos del recurso compartido<Share attributes>`
- Argumentos POST: sendMail - (string) enviar un correo electrónico al destinatario tras la creación (true/false)
- Campos obligatorios: shareType, path y shareWith para shareType 0 o 1.
- Resultado: XML que contiene el ID (int) del recurso compartido recién creado

Códigos de estado:

- 100 - correcto
- 400 - tipo de recurso compartido desconocido
- 403 - la administración desactivó la subida pública
- 404 - no se pudo compartir el archivo

#### Eliminar un recurso compartido

Quitar el recurso compartido dado.

- Sintaxis: /shares/*<share_id>*
- Método: DELETE
- Argumentos: share_id - (int) ID del recurso compartido

Códigos de estado:

- 100 - correcto
- 404 - no se pudo eliminar el archivo

#### Actualizar un recurso compartido

Actualizar un recurso compartido dado.

- Sintaxis: /shares/*<share_id>*
- Método: PUT
- Argumentos: share_id - (int) ID del recurso compartido
- Argumentos PUT: permissions - (int) actualizar los permisos (ver «Crear recurso compartido»
  más arriba)
- Argumentos PUT: password - (string) contraseña actualizada para el recurso compartido por enlace público
- Argumentos PUT: publicUpload - (string) activar (true) / desactivar (false) la subida
  pública para los recursos compartidos públicos.
- Argumentos PUT: expireDate - (string) establecer una fecha de caducidad para los recursos compartidos por
  enlace público. Este argumento espera una cadena de fecha con formato correcto, p. ej., 'YYYY-MM-DD'
- Argumentos PUT: note - (string) añade una nota para el destinatario del recurso compartido.
- Argumentos PUT: attributes - (string) cadena JSON serializada para los {nc-ref}`atributos del recurso compartido<Share attributes>`
- Argumentos PUT: sendMail - (string) enviar un correo electrónico al destinatario. Esto no envía un correo por sí solo. Hay que usar el endpoint {nc-ref}`send-email<Send email>` para enviar el correo. (true/false)

Códigos de estado:

- 100 - correcto
- 400 - parámetro de actualización incorrecto o ausente
- 403 - la administración desactivó la subida pública
- 404 - no se pudo actualizar el recurso compartido

(nc-dev-share attributes)=
#### Atributos del recurso compartido

Los atributos del recurso compartido se usan para indicadores más avanzados, como los permisos.

```json
[
    { "scope": "permissions", "key": "download", "value": false }
]
```

:::{warning}
Desde Nextcloud 30, la clave `enabled` pasó a llamarse `value` y admite más que valores booleanos.
:::

##### Permiso de descarga

Para quitar el permiso de descarga de un recurso compartido, usar la siguiente cadena serializada en el parámetro "attributes":

```json
[
    { "scope": "permissions", "key": "download", "value": false }
]
```

Esto impide que los usuarios descarguen los archivos del recurso compartido.
Para algunos tipos de archivo concretos, como los archivos de ofimática, seguirá siendo posible verlos con la app visor correspondiente,
que presentará el archivo de forma que no se permita descargarlo.

De forma predeterminada, cuando no está establecido, el atributo "download" vale true, de modo que se concede el permiso de descarga.

##### Solicitud de archivos

Al crear un recurso compartido por enlace o por correo, se puede activar la función de solicitud de archivos.
Esta pide a los destinatarios que introduzcan su nombre, y todos los archivos subidos se guardan en una
carpeta aparte con el nombre proporcionado.

```json
[
    { "scope": "fileRequest", "key": "enabled", "value": true }
]
```

Al crear la solicitud de archivos, también se puede proporcionar un array de correos electrónicos.
Tradicionalmente solo se permite uno con el parámetro *shareWith*,
pero se puede proporcionar una lista de correos mediante los atributos. Esto solo funciona con recursos compartidos de tipo MAIL.

```json
[
    { "scope": "fileRequest", "key": "enabled", "value": true },
    { "scope": "shareWith", "key": "emails", "value": ["maria@company.com", "paul@company.com"] }
]
```

:::{note}
Hay que proporcionar una cadena vacía como parámetro *shareWith* al crear el recurso compartido.
Actualizar o crear el recurso compartido con esos parámetros NO envía un correo electrónico a los destinatarios.
Hay que usar el endpoint *send-email* para enviar el correo.
:::

(nc-dev-send email)=
#### Enviar correo electrónico

Enviar un correo electrónico a los destinatarios de un recurso compartido.

- Sintaxis: /shares/*<share_id>*/send-email
- Método: POST
- Argumentos: share_id - (int) ID del recurso compartido
- Argumentos POST: password - (string) la contraseña del recurso compartido, si está activada.

Códigos de estado:

- 200 - correcto
- 400 - parámetro de actualización incorrecto o ausente
- 403 - sin permiso para enviar correo sobre este recurso compartido
- 404 - no se encontró el recurso compartido

### Recursos compartidos de nube federada

Tanto la instancia que envía como la que recibe deben tener activado y configurado el uso compartido
en la nube federada. Ver [Configurar el uso compartido en la nube federada](https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/federated_cloud_sharing_configuration.html).

#### Crear un nuevo recurso compartido de nube federada

Un recurso compartido de nube federada puede crearse mediante el endpoint de recursos compartidos locales, usando
(int) 6 como shareType y el [ID de nube federada](https://nextcloud.com/federation/)
del destinatario como shareWith. Ver [Crear un nuevo recurso compartido](#ocs-share-api-create-a-new-share) para más información.

#### Listar los recursos compartidos de nube federada aceptados

Obtener todos los recursos compartidos de nube federada que el usuario ha aceptado.

- Sintaxis: /remote_shares
- Método: GET
- Resultado: XML con todos los recursos compartidos de nube federada aceptados

Códigos de estado:

- 100 - correcto

#### Obtener información sobre un recurso compartido de nube federada conocido

Obtener información sobre un recurso compartido de nube federada recibido dado, que se envió desde una instancia remota.

- Sintaxis: /remote_shares/*<share_id>*
- Método: GET
- Argumentos: share_id - (int) ID del recurso compartido, tal como figura en el campo id de la lista `remote_shares`
- Resultado: XML con la información del recurso compartido

Códigos de estado:

- 100 - correcto
- 404 - el recurso compartido no existe

#### Eliminar un recurso compartido de nube federada aceptado

Eliminar localmente un recurso compartido de nube federada recibido que se envió desde una instancia remota.

- Sintaxis: /remote_shares/*<share_id>*
- Método: DELETE
- Argumentos: share_id - (int) ID del recurso compartido, tal como figura en el campo id de la lista `remote_shares`
- Resultado: XML con la información del recurso compartido

Códigos de estado:

- 100 - correcto
- 404 - el recurso compartido no existe

#### Listar los recursos compartidos de nube federada pendientes

Obtener todos los recursos compartidos de nube federada pendientes que el usuario ha recibido.

- Sintaxis: /remote_shares/pending
- Método: GET
- Resultado: XML con todos los recursos compartidos de nube federada pendientes

Códigos de estado:

- 100 - correcto

#### Aceptar un recurso compartido de nube federada pendiente

Aceptar localmente un recurso compartido de nube federada recibido que se envió desde una instancia remota.

- Sintaxis: /remote_shares/pending/*<share_id>*
- Método: POST
- Argumentos: share_id - (int) ID del recurso compartido, tal como figura en el campo id de la lista `remote_shares/pending`
- Resultado: XML con la información del recurso compartido

Códigos de estado:

- 100 - correcto
- 404 - el recurso compartido no existe

#### Rechazar un recurso compartido de nube federada pendiente

Rechazar localmente un recurso compartido de nube federada recibido que se envió desde una instancia remota.

- Sintaxis: /remote_shares/pending/*<share_id>*
- Método: DELETE
- Argumentos: share_id - (int) ID del recurso compartido, tal como figura en el campo id de la lista `remote_shares/pending`
- Resultado: XML con la información del recurso compartido

Códigos de estado:

- 100 - correcto
- 404 - el recurso compartido no existe
````
