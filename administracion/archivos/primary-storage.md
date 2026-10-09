---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Almacén de objetos (OpenStack Swift, S3, Azure Blob Storage) como almacenamiento principal: implicaciones, parámetros, multibucket, multiinstancia y SSE-C."
---
# Configurar el almacenamiento de objetos como almacenamiento principal

## Resumen

Esta página explica cómo configurar en `config.php` un almacén de objetos (OpenStack Swift, S3 o Azure Blob Storage) como almacenamiento principal, en qué se diferencia del almacenamiento externo, cómo repartir los datos entre varios buckets o instancias y cómo activar el cifrado SSE-C de S3. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/primary_storage.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud permite configurar almacenamientos de objetos como OpenStack Swift o Amazon Simple Storage Service (S3), o cualquier implementación compatible con S3 (p. ej., Minio o Ceph Object Gateway), como almacenamiento principal en sustitución del almacenamiento predeterminado de los archivos.

De forma predeterminada, los archivos se almacenan en {code}`nextcloud/data` o en otro directorio configurado en el {code}`config.php` de la instancia de Nextcloud. Es posible que este directorio de datos se siga usando por motivos de compatibilidad)

### Diferencias con el almacenamiento externo

Cuando se usa un almacén de objetos como almacenamiento principal, Nextcloud necesita acceso exclusivo al bucket que se utiliza. Todos los metadatos (nombres de archivo, estructuras de directorios, etc.) se almacenan en Nextcloud y no en el almacén de objetos. Los metadatos solo se almacenan en la base de datos, y el almacén de objetos solo guarda el contenido de los archivos por identificador único.

#### Implicaciones para el rendimiento

Por ello, los almacenes de objetos configurados como almacenamiento principal suelen rendir mejor que cuando se usa el mismo almacén de objetos mediante la aplicación de compatibilidad con almacenamiento externo, pero la desventaja es que no se puede acceder a los archivos desde fuera de Nextcloud. Esto hace que usar un almacén de objetos como almacenamiento principal sea distinto de usar un almacén de objetos mediante el almacenamiento externo.

#### Implicaciones para las copias de seguridad y la recuperación de datos

Una consecuencia de usar un almacén de objetos como almacenamiento principal es que la estrategia de copias de seguridad de los datos debe tenerlo en cuenta. **Los datos ya no se almacenan en el servidor Nextcloud, pero tampoco se puede acceder a los archivos simplemente eludiendo el servidor Nextcloud y accediendo directamente al almacén de objetos.**

### Configuración

Los almacenes de objetos principales deben configurarse en {code}`config.php`, especificando el backend de objectstore y cualquier configuración específica de ese backend.

:::{note}
Configurar un almacén de objetos principal en una instancia de Nextcloud existente hará que todos los archivos existentes de la instancia queden inaccesibles.
:::

La configuración tiene la siguiente estructura:

```
'objectstore' => [
    'class' => 'Object\\Storage\\Backend\\Class',
    'arguments' => [
        ...
    ],
],
```

#### OpenStack Swift

El backend de OpenStack Swift monta un contenedor de un servidor OpenStack Object Storage en el sistema de archivos virtual.

La clase que debe usarse es {code}`\\OC\\Files\\ObjectStore\\Swift`

Se admiten tanto la autenticación v2 como la v3 de openstack,

Autenticación V2:

```
'objectstore' => [
    'class' => '\\OC\\Files\\ObjectStore\\Swift',
    'arguments' => [
        'username' => 'username',
        'password' => 'Secr3tPaSSWoRdt7',
        // the container to store the data in
        'bucket' => 'nextcloud',
        'autocreate' => true,
        'region' => 'RegionOne',
        // The Identity / Keystone endpoint
        'url' => 'http://example.com/v2.0',
        // optional on some swift implementations
        'tenantName' => 'username',
        'serviceName' => 'swift',
        // The Interface / url Type, optional
        'urlType' => 'internal'
    ],
],
```

Autenticación V3:

```
'objectstore' => [
    'class' => 'OC\\Files\\ObjectStore\\Swift',
    'arguments' => [
        'autocreate' => true,
        'user' => [
            'name' => 'UserName',
            'password' => 'Secr3tPaSSWoRdt7',
            'domain' => [
                'name' => 'Default',
            ],
        ],
        'scope' => [
            'project' => [
                'name' => 'TenantName',
                'domain' => [
                    'name' => 'Default',
                ],
            ],
        ],
        'serviceName' => 'swift',
        'region' => 'regionOne',
        'url' => 'http://example.com/v3',
        'bucket' => 'nextcloud',
    ],
],
```

#### Simple Storage Service (S3)

El backend de Simple Storage Service (S3) monta un bucket de un almacenamiento de objetos Amazon S3 o de una implementación compatible (p. ej., Minio o Ceph Object Gateway) en el sistema de archivos virtual.

La clase que debe usarse es {code}`\\OC\\Files\\ObjectStore\\S3`

S3 alojado en Amazon:

```
'objectstore' => [
    'class' => '\\OC\\Files\\ObjectStore\\S3',
    'arguments' => [
        'bucket' => 'my-nextcloud-store',
        'region' => 'us-east-1',
        'key' => 'EJ39ITYZEUH5BGWDRUFY',
        'secret' => 'M5MrXTRjkyMaxXPe2FRXMTfTfbKEnZCu+7uRTVSj',
    ],
],
```

S3 no alojado en Amazon:

```
'objectstore' => [
    'class' => '\\OC\\Files\\ObjectStore\\S3',
    'arguments' => [
        'bucket' => 'my-nextcloud-store',
        'hostname' => 's3.example.com',
        'key' => 'EJ39ITYZEUH5BGWDRUFY',
        'secret' => 'M5MrXTRjkyMaxXPe2FRXMTfTfbKEnZCu+7uRTVSj',
        'port' => 8443,
        // required for some non-Amazon S3 implementations
        'use_path_style' => true,
    ],
],
```

Los parámetros mínimos obligatorios son:

- {code}`bucket` \[Nota: aunque no esté alojado en Amazon, los nombres de bucket deben cumplir los requisitos de nomenclatura de AWS S3, independientemente de lo que el proveedor o la plataforma de S3 considere aceptable; es decir, sin guiones bajos\]
- {code}`key`
- {code}`secret`

:::{note}
*Probablemente* será necesario especificar más parámetros además de estos, salvo que los valores predeterminados (ver más abajo) se ajusten exactamente a la situación. En particular, {code}`region` (si está alojado en Amazon) o {code}`hostname` (si no está alojado en Amazon).
:::

Parámetros opcionales que con más frecuencia hay que ajustar (y sus valores predeterminados si no se configuran):

- {code}`region` tiene como valor predeterminado {code}`eu-west-1`
- {code}`storageClass` tiene como valor predeterminado {code}`STANDARD`
- {code}`hostname` tiene como valor predeterminado {code}`s3.REGION.amazonaws.com` \[Nota: si se usa este parámetro (fuera de Amazon), indicar el nombre de host genérico del endpoint de S3, **no** el nombre de host que contiene el nombre del bucket\]
- {code}`use_ssl` tiene como valor predeterminado {code}`true`

Parámetros opcionales que a veces hay que ajustar:

- {code}`use_path_style` tiene como valor predeterminado {code}`false`
- {code}`port` tiene como valor predeterminado {code}`443`
- {code}`sse_c_key` no tiene valor predeterminado

Parámetros opcionales que con menos frecuencia hay que ajustar:

- {code}`concurrency` tiene como valor predeterminado {code}`5` \[Nota: define el número máximo de subidas multiparte simultáneas\]
- {code}`proxy` tiene como valor predeterminado {code}`false`
- {code}`connect_timeout` tiene como valor predeterminado {code}`5` \[Nota: el tiempo de espera de la conexión se establece en segundos, pero puede usarse precisión decimal para lograr una exactitud inferior al segundo (por ejemplo, 4.2 para 4200 milisegundos)\]
- {code}`timeout` tiene como valor predeterminado {code}`15`
- {code}`uploadPartSize` tiene como valor predeterminado {code}`524288000`
- {code}`putSizeLimit` tiene como valor predeterminado {code}`104857600`
- {code}`useMultipartCopy` tiene como valor predeterminado {code}`true`
- {code}`copySizeLimit` tiene como valor predeterminado {code}`5242880000`
- {code}`legacy_auth` no tiene valor predeterminado
- {code}`version` tiene como valor predeterminado {code}`latest`
- {code}`verify_bucket_exists` tiene como valor predeterminado {code}`true` \[Nota: establecerlo en {code}`false` *después* de confirmar que el bucket se ha creado puede mejorar el rendimiento, pero puede no ser posible en escenarios multibucket.\]

**Si se usa Amazon S3:** el parámetro {code}`region` es obligatorio, salvo que el valor predeterminado {code}`eu-west-1` resulte adecuado. No es necesario sustituir {code}`hostname` ni {code}`port`. Y {code}`storageClass` solo debe modificarse si se usa una configuración distinta en AWS. Por último, {code}`use_path_style` rara vez es necesario con Amazon, pero algunos centros de datos antiguos de Amazon pueden requerirlo.

**Si se usa un almacén S3 no alojado en Amazon:** será necesario establecer el parámetro {code}`hostname` (y puede ignorarse el parámetro {code}`region`). Puede ser necesario usar {code}`use_path_style` si el almacén S3 no alojado en Amazon *no* admite peticiones como {code}`https://bucket.hostname.domain/`. Establecer {code}`use_path_style` en true configura el cliente S3 para que haga, en su lugar, peticiones como {code}`https://hostname.domain/bucket`.

#### Microsoft Azure Blob Storage

El backend de Azure Blob Storage monta un contenedor de Azure Blob Storage de Microsoft en el sistema de archivos virtual.

La clase que debe usarse es {code}`\\OC\\Files\\ObjectStore\\Azure`

```
'objectstore' => [
    'class' => '\\OC\\Files\\ObjectStore\\Azure',
    'arguments' => [
        'container' => 'nextcloud',
        'autocreate' => true,
        'account_name' => 'account_name',
        'account_key' => 'xxxxxxxxxx'
    ],
],
```

### Almacén de objetos multibucket

Es posible configurar Nextcloud para que distribuya los datos entre varios buckets con fines de escalabilidad.

Para configurar varios buckets, establecer {code}`'multibucket => true'` en la configuración del almacén de objetos de {code}`config.php`:

```
'objectstore' => [
    'class' => 'Object\\Storage\\Backend\\Class',
    'arguments' => [
        'multibucket' => true,
        // optional, defaults to 64
        'num_buckets' => 64,
        // will be postfixed by an integer in the range from 0 to (num_nuckets-1)
        'bucket' => 'nextcloud_',
        ...
    ],
],
```

El backend de almacén de objetos multibucket asigna a cada usuario un rango de buckets y guarda todos los archivos de ese usuario en su bucket correspondiente.

:::{note}
Aunque es posible cambiar el número de buckets que usa una instancia de Nextcloud existente, la asignación de usuarios a buckets solo se crea una vez, por lo que solo los usuarios creados a partir de entonces se asignarán al rango de buckets actualizado.
:::

Hay más información sobre el escalado con almacenamiento de objetos y Nextcloud en el [portal de clientes de {vendor}`Nextcloud`](https://portal.nextcloud.com/article/object-store-as-primary-storage-16.html).

### Almacén de objetos multibucket con configuración sustituida por bucket

Al usar un almacén de objetos con {code}`'multibucket => true'`, es posible configurar, para cada bucket, valores que sustituyan a todas las opciones de configuración:

```
'objectstore' => [
    'class' => 'Object\\Storage\\Backend\\Class',
    'arguments' => [
        'multibucket' => true,
        'bucket' => 'nextcloud_',
        'perBucket' => [
            'nextcloud_1' => [
                'port' => 9999,
            ],
        ],
    ],
],
```

Esto puede ser útil, por ejemplo, para configurar credenciales propias de cada bucket que use una carpeta de equipo.
Un script para aprovisionar de este modo carpetas de equipo nuevas podría tener este aspecto (antes, asegurarse de que el bucket existe con esas credenciales):

```
occ config:system:set --type=string --value=KEYVALUE objectstore arguments perBucket BUCKETNAME key
occ config:system:set --type=string --value=SECRETVALUE objectstore arguments perBucket BUCKETNAME secret
occ groupfolders:create --bucket BUCKETNAME TEAMFOLDERNAME
```

Las credenciales deben establecerse antes de crear la carpeta de equipo nueva.

### Almacén de objetos multiinstancia

Es posible configurar Nextcloud para que distribuya los datos entre varias instancias de almacén de objetos, para escalar aún más y para migrar de forma gradual.

Para configurar varios buckets, establecer {code}`'objectstore'` en un array de configuraciones con nombre en {code}`config.php` y establecer {code}`'default'` en el nombre de la configuración que debe usarse para los usuarios nuevos:

```
'objectstore' => [
    'default' => 'server2',
    'root' => 'server1',
    'server1' => [
        'class' => 'Object\\Storage\\Backend\\Class',
        'arguments' => [
            'hostname' => 's3-server1.example.com',
            'bucket' => 's1_nextcloud',
            ...
        ],
    ],
    'server2' => [
    'class' => 'Object\\Storage\\Backend\\Class',
        'arguments' => [
            'multibucket' => true,
            'hostname' => 's3-server2.example.com',
            'bucket' => 's2_nextcloud_',
            ...
        ],
    ],
],
```

:::{note}
Los nombres de los buckets deben ser únicos entre todas las instancias de almacén de objetos configuradas.
:::

Los usuarios nuevos se asignarán a la instancia de almacén de objetos establecida en {code}`default`. Los archivos que no forman parte del almacenamiento de los usuarios se colocan en la instancia {code}`root`, o en la instancia {code}`default` si no hay ninguna instancia {code}`root` configurada.

En el ejemplo anterior, si {code}`server2` empieza a quedarse sin capacidad, quien administra el servidor puede preparar y configurar un {code}`server3` nuevo y cambiar {code}`default` a {code}`server3`. A partir de entonces, los archivos de cualquier usuario nuevo se guardarán en {code}`server3`.

:::{note}
Al igual que con el almacén de objetos multibucket, la asignación de usuarios a instancias solo se crea una vez, por lo que solo los usuarios creados a partir de entonces se asignarán a la nueva instancia predeterminada.
:::

En una configuración multiinstancia es posible combinar distintos backends de almacén de objetos, así como instancias multibucket y no multibucket.

### Compatibilidad con el cifrado SSE-C de S3

Nextcloud admite el cifrado del lado del servidor, también conocido como [SSE-C](http://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html), con proveedores de buckets S3 compatibles. El cifrado y el descifrado se realizan en el lado del bucket S3 con una clave proporcionada por el servidor Nextcloud.

La clave puede especificarse con el parámetro {code}`sse_c_key`, que debe proporcionarse como una cadena codificada en base64 con una longitud máxima de 32 bytes. Puede generarse una clave aleatoria con el siguiente comando:

```
openssl rand 32 | base64
```

El siguiente ejemplo muestra cómo configurar el almacén de objetos S3 con compatibilidad con el cifrado SSE-C en la sección objectstore del archivo config.php de Nextcloud:

```
'objectstore' => [
    array (
        'class' => 'OC\\Files\\ObjectStore\\S3',
        'arguments' =>
        array (
            'bucket' => 'nextcloud',
            'key' => 'nextcloud',
            'secret' => 'nextcloud',
            'hostname' => 's3',
            'port' => '443',
            'use_ssl' => true,
            'use_path_style' => true,
            'autocreate' => true,
            'verify_bucket_exists' => true,
            'sse_c_key' => 'o9d3Q9tHcPMv6TIpH53MSXaUmY91YheZRwuIhwCFRSs=',
        ),
    );
],
```
````
