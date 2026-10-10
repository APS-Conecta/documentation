---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Conectar un bucket de Amazon S3 o compatible como almacenamiento externo: datos necesarios, campos del formulario, parámetros y clave SSE-C."
---
# Amazon S3

## Resumen

Esta página explica cómo conectar un bucket de Amazon S3, o de un servicio compatible con S3, como almacenamiento externo: qué datos se necesitan y cómo rellenar cada campo del formulario de montaje. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/external_storage/amazons3.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Para conectar un bucket de Amazon S3 (o compatible) a Nextcloud, hay que conocer:

- El nombre del bucket de S3
- El ID de la clave de acceso de S3
- La clave de acceso secreta de S3
- La región de S3 (si está alojado en Amazon) o el nombre de host de S3 (si no está alojado en Amazon) [Nota: si se especifica un nombre de host, usar el nombre de host del endpoint genérico de S3, **no** el nombre de host que contiene el nombre del bucket]

:::{attention}
Algunos almacenamientos compatibles con S3, incluido Amazon S3, permiten delimitadores {code}`/` repetidos ({code}`e.g. Photos//cat.png`). Esto no está admitido, y los prefijos con delimitadores repetidos y su contenido se ignoran.
:::

En el campo **Nombre de la carpeta**, introducir el nombre de carpeta que se usará como punto de montaje local de este almacenamiento externo. Si no existe, se creará.

En el campo **Almacenamiento externo**, seleccionar **Amazon S3**.

En el campo **Autentificación**, seleccionar **Clave de acceso**.

En el campo **Bucket**, introducir el *nombre del bucket de S3*. [Nota: aunque no esté alojado en Amazon, los nombres de bucket deben cumplir los requisitos de nomenclatura de AWS S3, independientemente de lo que el proveedor o la plataforma de S3 considere aceptable; es decir, sin guiones bajos]

En el campo **Clave de acceso**, introducir el *ID de la clave de acceso de S3*.

En el campo **Clave secreta**, introducir la *clave de acceso de S3*.

**Si se usa Amazon S3:** el parámetro {code}`Region` es obligatorio, salvo que se acepte el valor predeterminado {code}`eu-west-1` (que se usará si no se especifica nada). No hace falta sobrescribir {code}`Hostname` ni {code}`Port`. Y {code}`Storage Class` solo debe modificarse si se usa una configuración distinta en AWS. Por último, {code}`Enable Path Style` rara vez es necesario con Amazon, pero algunos centros de datos heredados de Amazon pueden requerirlo. Dejar {code}`Legacy (v2) authentication` sin seleccionar.

**Si se usa un almacenamiento S3 no alojado en Amazon:** hay que establecer el parámetro {code}`Hostname` (y se puede ignorar el parámetro {code}`Region`). Puede ser necesario activar {code}`Enable Path Style` si el almacenamiento S3 no alojado en Amazon *no* admite solicitudes como {code}`https://bucket.hostname.domain/`. Establecer {code}`Enable Path Style` en verdadero configura el cliente de S3 para que haga, en su lugar, solicitudes como {code}`https://hostname.domain/bucket`. Rara vez se necesita {code}`Legacy (v2) authentication`, pero hay que activarla si el almacén de objetos propio o el proveedor de servicios la exige en lugar de la autenticación predeterminada (v4).

En el campo **Disponible para**, introducir los usuarios o grupos a los que se quiere dar acceso al montaje de S3.

La casilla {guilabel}`Habilitar SSL` activa las conexiones HTTPS y, en general, es preferible. Es el valor predeterminado, salvo que se desactive aquí.

Opcionalmente, se puede proporcionar una clave SSE-C de 32 bytes codificada en base64 para el cifrado en el servidor. Consultar {nc-doc}`admin_manual/configuration_files/primary_storage` y la [documentación de AWS sobre SSE-C](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerSideEncryptionCustomerKeys.html) para obtener más información sobre cómo generar una clave.

Consultar {nc-doc}`admin_manual/configuration_files/external_storage_configuration_gui` para ver más opciones de montaje e información.

Consultar {nc-doc}`admin_manual/configuration_files/external_storage/auth_mechanisms` para obtener más información sobre los esquemas de autenticación.
````
