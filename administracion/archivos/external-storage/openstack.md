---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Conectar OpenStack Swift o Rackspace como almacenamiento externo: los datos que pide cada mecanismo de autenticación, la región y el tiempo de espera."
---
# Almacenamiento de objetos OpenStack

## Resumen

Esta página explica cómo conectar un servidor OpenStack Swift o Rackspace como almacenamiento externo: los datos que requiere cada uno de sus dos mecanismos de autenticación, la región y el tiempo de espera de las solicitudes. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/external_storage/openstack.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El almacenamiento de objetos OpenStack se usa para conectarse a un servidor OpenStack Swift o a Rackspace. Hay dos mecanismos de autenticación disponibles: uno es el mecanismo genérico de OpenStack, y el otro se usa exclusivamente para Rackspace, un proveedor de almacenamiento de objetos que usa el protocolo OpenStack Swift.

El mecanismo de autenticación de OpenStack usa el protocolo OpenStack Keystone v2. La configuración de Nextcloud necesita:

- **Bucket**. Lo define el usuario; puede pensarse en él como un subdirectorio del almacenamiento total. El bucket se creará si no existe.
- **Nombre de usuario** de la cuenta.
- **Contraseña** de la cuenta.
- **Nombre del inquilino** de la cuenta. (Un inquilino es similar a un grupo de usuarios).
- **URL del endpoint de identidad**, la URL para iniciar sesión en la cuenta de OpenStack.

El mecanismo de autenticación de Rackspace requiere:

- **Bucket**
- **Nombre de usuario**
- **Clave de la API**.

También hay que introducir el término **cloudFiles** en el campo **Nombre del servicio**.

Puede ser necesario especificar una **Región**. La región debería figurar en la información de la cuenta, y se puede leer sobre las regiones de Rackspace en [Acerca de las regiones](https://support.rackspace.com/how-to/about-regions/).

El tiempo de espera de las solicitudes HTTP se establece en el campo **Tiempo agotado para petición**, en segundos.

Consultar {nc-doc}`admin_manual/configuration_files/external_storage_configuration_gui` para ver más opciones de montaje e información.

Consultar {nc-doc}`admin_manual/configuration_files/external_storage/auth_mechanisms` para obtener más información sobre los esquemas de autenticación.
````
