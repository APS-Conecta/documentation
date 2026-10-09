---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Esquema del módulo de cifrado predeterminado: tipos de clave, formato y ubicación de cada archivo de clave, y los pasos de cifrado, firma y descifrado."
---
# Detalles del cifrado en el servidor

## Resumen

Esta página describe el esquema de cifrado en el servidor que implementa el módulo de cifrado predeterminado: los tipos de clave, el formato y la ubicación de los archivos de clave y de los archivos cifrados, y los pasos de generación de claves, cifrado, firma y descifrado. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/encryption_details.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Este documento describe el esquema de cifrado en el servidor que implementa el módulo de cifrado predeterminado de Nextcloud. Esto incluye:

- el cifrado y la firma de archivos con una clave maestra.
- el cifrado y la firma de archivos con una clave de compartición pública.
- el cifrado y la firma de archivos con una clave de recuperación.
- el cifrado y la firma de archivos con una clave de usuario.

Estas convenciones se aplican en todo el documento:

- Las rutas de archivo indicadas en este documento son relativas al directorio de datos de Nextcloud, que puede obtenerse como `datadirectory` del `config.php`.
- Los marcadores de posición se indican como `$variable`. La variable debe sustituirse por la información correspondiente.
- Las cadenas estáticas se indican como `"some string"`.
- La concatenación de cadenas se indica como `$variable."some string"`.

:::{note}
No obstante, los archivos cifrados en las versiones 15 y anteriores de Nextcloud pueden tener estructuras ligeramente distintas.
:::

### Tipo de clave: clave maestra

Este es el modo de cifrado predeterminado de Nextcloud. Con el cifrado de clave maestra activado hay una clave central que se usa para proteger los archivos que gestiona Nextcloud. La clave maestra está protegida por el *secret* de la instancia, que se genera en el momento de la instalación. La ventaja del cifrado de clave maestra es que el cifrado es transparente para los usuarios, pero tiene la desventaja de que el administrador del servidor puede descifrar los archivos de los usuarios sin conocer ninguna contraseña de usuario.

### Tipo de clave: clave de compartición pública

La clave de compartición pública se usa para proteger los archivos que se han compartido públicamente. La ventaja de la clave de compartición pública es que es independiente del modo de cifrado seleccionado, de modo que Nextcloud puede proporcionar a terceros los archivos compartidos públicamente.

### Tipo de clave: clave de recuperación

La clave de recuperación se usa para ofrecer un mecanismo de restauración en los casos en que está activado el cifrado con claves de usuario, el administrador ha activado la función de clave de recuperación y el usuario ha optado por usar la función de clave de recuperación. La clave de recuperación puede usarse entonces para restaurar archivos cuando los usuarios han perdido sus contraseñas. La clave de recuperación está protegida por una contraseña de recuperación que el administrador del servidor debe guardar de forma segura. La ventaja de la clave de recuperación es que los archivos pueden recuperarse, pero tiene la desventaja de que el administrador del servidor puede descifrar los archivos de los usuarios sin conocer ninguna contraseña de usuario.

### Tipo de clave: clave de usuario

El cifrado con claves de usuario debe activarse explícitamente llamando a `./occ encryption:disable-master-key`. En versiones anteriores de Nextcloud estaba activado de forma predeterminada. Con el cifrado con claves de usuario activado, cada usuario tiene sus propias claves de usuario, que se usan para proteger los archivos que gestiona Nextcloud. Las claves de usuario están protegidas por las contraseñas de los usuarios. La ventaja es que el administrador del servidor no puede descifrar los archivos de los usuarios sin conocer ninguna contraseña de usuario (salvo que el archivo esté compartido públicamente o se haya definido una clave de recuperación), pero tiene la desventaja de que los archivos se pierden de forma permanente si los usuarios olvidan sus contraseñas (salvo que los archivos estén compartidos (públicamente) o se haya definido una clave de recuperación).

:::{note}
Este método no puede usarse con la autenticación SAML, porque Nextcloud no obtiene ninguna credencial en absoluto y, por tanto, no puede usar la contraseña de ningún usuario para el cifrado.
:::

(nc-file_type_public_key_file_label)=
### Tipo de archivo: archivo de clave pública

Los archivos de clave pública contienen claves públicas RSA que se usan para cifrar/sellar los archivos de clave de compartición.

#### Formato del archivo

Los archivos de clave pública se guardan en formato PEM.

#### Ubicaciones de los archivos

Las ubicaciones de los archivos de clave pública dependen de su tipo de clave:

- clave pública maestra: `"files_encryption/OC_DEFAULT_MODULE/master_".$random.".publicKey"`
- clave pública de compartición pública: `"files_encryption/OC_DEFAULT_MODULE/pubShare_".$random.".publicKey"`
- clave pública de recuperación: `"files_encryption/OC_DEFAULT_MODULE/recoveryKey_".$random.".publicKey"`
- clave pública de usuario: `$username."/files_encryption/OC_DEFAULT_MODULE/".$username.".publicKey"`

(nc-file_type_private_key_file_label)=
### Tipo de archivo: archivo de clave privada

Los archivos de clave privada contienen claves privadas RSA que se usan para descifrar/abrir los archivos de clave de compartición. La clave privada RSA se cifra y se firma con una contraseña y se guarda en un formato propio del módulo de cifrado de Nextcloud.

#### Formato del archivo

La clave privada RSA, representada en formato PEM, se cifra y se codifica en Base64 (se indica como `$encryption`). Para el cifrado se elige un vector de inicialización de 16 bytes (se indica como `$iv`). Además, se calcula un código de autenticación de mensajes de 64 bytes codificado en hexadecimal (se indica como `$signature`). El archivo resultante contiene:

```
"HBEGIN:cipher:AES-256-CTR:keyFormat:hash:HEND".
$encrypted."00iv00".$iv."00sig00".$signature."xxx"
```

#### Ubicaciones de los archivos

Las ubicaciones de los archivos de clave privada dependen de su tipo de clave:

- clave privada maestra: `"files_encryption/OC_DEFAULT_MODULE/master_".$random.".privateKey"`
- clave privada de compartición pública: `"files_encryption/OC_DEFAULT_MODULE/pubShare_".$random.".privateKey"`
- clave privada de recuperación: `"files_encryption/OC_DEFAULT_MODULE/recoveryKey_".$random.".privateKey"`
- clave privada de usuario: `$username."/files_encryption/OC_DEFAULT_MODULE/".$username.".privateKey"`

(nc-file_type_share_key_file_label)=
### Tipo de archivo: archivo de clave de compartición

Los archivos de clave de compartición contienen las llamadas claves de sobre, que son necesarias para descifrar los archivos de clave de archivo. Las claves de sobre las crea `openssl_seal()` durante el cifrado y son necesarias para `openssl_open()` durante el descifrado. Las claves de sobre se cifran con las claves públicas de los destinatarios a los que se permite leer los archivos propiamente dichos.

#### Formato del archivo

Las claves de sobre se guardan en formato binario.

#### Ubicaciones de los archivos

Las ubicaciones de los archivos de clave de compartición dependen del tipo de archivo cifrado:

- archivo normal: `$username."/files_encryption/keys/files/".$filename."/OC_DEFAULT_MODULE/".$recipient.".shareKey"`
- archivo de versión: *los archivos de versión usan para el archivo de clave de compartición la misma ubicación que su archivo normal*
- archivo en la papelera: `$username."/files_encryption/keys/files_trashbin/files/".$filename.".d".$timestamp."/OC_DEFAULT_MODULE/".$recipient.".shareKey"`
- archivo de versión en la papelera: *los archivos de versión en la papelera usan para el archivo de clave de compartición la misma ubicación que su archivo en la papelera*

(nc-file_type_file_key_file_label)=
### Tipo de archivo: archivo de clave de archivo

Los archivos de clave de archivo contienen las claves simétricas que se usan para cifrar los archivos propiamente dichos. Las claves de archivo constan de 32 bytes aleatorios y se cifran/sellan con las claves de sobre guardadas en los archivos de clave de compartición.

#### Formato del archivo

Las claves de archivo se guardan en formato binario.

#### Ubicaciones de los archivos

Las ubicaciones de los archivos de clave de archivo dependen del tipo de archivo cifrado:

- archivo normal: `$username."/files_encryption/keys/files/".$filename."/OC_DEFAULT_MODULE/fileKey"`
- archivo de versión: *los archivos de versión usan para el archivo de clave de archivo la misma ubicación que su archivo normal*
- archivo en la papelera: `$username."/files_encryption/keys/files_trashbin/files/".$filename.".d".$delete_timestamp."/OC_DEFAULT_MODULE/fileKey"`
- archivo de versión en la papelera: *los archivos de versión en la papelera usan para el archivo de clave de archivo la misma ubicación que su archivo en la papelera*

(nc-file_type_file_label)=
### Tipo de archivo: archivo

Los archivos contienen el contenido propiamente dicho. El contenido del archivo se cifra y se firma con una contraseña y se guarda en un formato propio del módulo de cifrado de Nextcloud.

#### Formato del archivo

El contenido del archivo se divide en bloques de 6072 bytes. Cada bloque se cifra y se codifica en Base64 (se indica como `$encryption[0..$n]`). Para el cifrado se elige un vector de inicialización de 16 bytes para cada bloque (se indica como `$iv[0..$n]`). Además, se calcula un código de autenticación de mensajes de 64 bytes codificado en hexadecimal para cada bloque (se indica como `$signature[0..$n]`). Un bloque cifrado tiene un tamaño total de 8192 bytes (8096 bytes para `$encrypted[]`, 6 bytes para `"00iv00"`, 16 bytes para `$iv[]`, 7 bytes para `"00sig00"`, 64 bytes para `$signature[]` y 3 bytes para `"xxx"`). Solo el último bloque cifrado puede ser más corto. El encabezado del archivo cifrado se rellena con 8147 bytes de `"-"` (se indica como `$padding`) hasta un total de 8192 bytes. El archivo resultante contiene:

```
"HBEGIN:cipher:AES-256-CTR:keyFormat:hash:HEND".$padding.
$encrypted[0]."00iv00".$iv[0]."00sig00".$signature[0]."xxx".
$encrypted[1]."00iv00".$iv[1]."00sig00".$signature[1]."xxx".
$encrypted[2]."00iv00".$iv[2]."00sig00".$signature[2]."xxx".
[...]
$encrypted[$n]."00iv00".$iv[$n]."00sig00".$signature[$n]."xxx"
```

#### Ubicaciones de los archivos

Las ubicaciones de los archivos dependen del tipo de archivo cifrado:

- archivo normal: `$username."/files/".$filename`
- archivo de versión: `$username."/files_versions/".$filename.".v".$version_timestamp`
- archivo en la papelera: `$username."/files_trashbin/files/".$filename.".d".$delete_timestamp`
- archivo de versión en la papelera: `$username."/files_trashbin/versions/".$filename.".v".$version_timestamp.".d".$delete_timestamp`

### Generación de claves: generar el par de claves

El par de claves debe generarse con la función `openssl_pkey_new()`. Después, la clave privada y la clave pública se extraen del recurso de clave con la función `openssl_pkey_export()`.

### Generación de claves: guardar la clave pública

La clave pública se escribe en el archivo `$username.".publicKey"` tal como se documenta en {nc-ref}`Tipo de archivo: archivo de clave pública <file_type_public_key_file_label>`.

### Generación de claves: guardar la clave privada

#### Derivar la clave de cifrado

La sal de la clave de cifrado se deriva creando un hash SHA256 en bruto de `$uid.$instanceId.$instanceSecret` con la función `hash()`. `$instanceId` puede obtenerse como `instanceid` del `config.php`. `$instanceSecret` puede obtenerse como `secret` del `config.php`.

Después, la clave de cifrado se deriva creando un hash SHA256-PBKDF2 en bruto de la contraseña con la sal, 100.000 rondas y (de forma predeterminada) un tamaño de destino de 32 bytes (como requiere AES-256-CTR) con la función `hash_hmac()` (se indica como `$passphrase`).

La contraseña usada depende del tipo de clave:

- clave privada maestra: usar `secret` del `config.php`
- clave privada de compartición pública: usar una contraseña vacía
- clave privada de recuperación: usar la contraseña de recuperación
- clave privada de usuario: usar la contraseña del usuario

#### Cifrar la clave privada

El vector de inicialización se genera como una cadena aleatoria de 16 bytes con la función `random_bytes()` (se indica como `$iv`). La clave privada se cifra (de forma predeterminada) con AES-256-CTR con el `$iv` y la `$passphrase` mediante la función `openssl_encrypt()` y se devuelve codificada en Base64 sin relleno de ceros (se indica como `$encrypted`).

#### Firmar la clave privada

La clave de autenticación de mensajes se deriva creando un hash SHA512 en bruto de `$passphrase.$version.$position."a"` con la función `hash()`.

- `$version` es siempre `"0"`.
- `$position` es siempre `"0"`.

Después, la firma se deriva creando un SHA256-HMAC codificado en hexadecimal de `$encrypted` y la clave de autenticación de mensajes con la función `hash_hmac()` (se indica como `$signature`).

#### Guardar la clave privada

La clave privada se escribe en el archivo `$username.".privateKey"` con los valores derivados `$encrypted`, `$iv` y `$signature` tal como se documenta en {nc-ref}`Tipo de archivo: archivo de clave privada <file_type_private_key_file_label>`.

### Cifrado: generar la clave de archivo

#### Generar la clave de archivo

La clave de archivo se genera como una cadena aleatoria de 32 bytes con la función `random_bytes()` (se indica como `$filekey`).

#### Leer la clave pública

Las claves públicas de los destinatarios se leen de los archivos `$username.".publicKey"` tal como se documenta en {nc-ref}`Tipo de archivo: archivo de clave pública <file_type_public_key_file_label>`.

#### Cifrar/sellar la clave de archivo

La clave de archivo se cifra/sella con la función `openssl_seal()` con las claves públicas. Esto devuelve la clave de archivo cifrada y las claves de sobre cifradas de los destinatarios.

#### Guardar la clave de archivo

La clave de archivo cifrada se guarda en el archivo `"fileKey"` tal como se documenta en {nc-ref}`Tipo de archivo: archivo de clave de archivo <file_type_file_key_file_label>`.

#### Guardar las claves de sobre

Las claves de sobre cifradas de los destinatarios se guardan en los archivos `$username.".shareKey"` tal como se documenta en {nc-ref}`Tipo de archivo: archivo de clave de compartición <file_type_share_key_file_label>`.

### Cifrado: cifrar el archivo

#### Dividir el archivo

El archivo se divide en bloques de 6072 bytes. Solo el último bloque cifrado puede ser más corto. Cada bloque se identifica por su índice, empezando en cero, dentro del archivo (se indica como `$position`).

#### Cifrar los bloques

Para cada bloque, el vector de inicialización se genera como una cadena aleatoria de 16 bytes con la función `random_bytes()` (se indica como `$iv[$position]`). El bloque se cifra (de forma predeterminada) con AES-256-CTR con el `$iv[$position]` y la `$filekey` mediante la función `openssl_encrypt()` y se devuelve codificado en Base64 sin relleno de ceros (se indica como `$encrypted[$position]`).

#### Firmar los bloques

La clave de autenticación de mensajes se deriva creando un hash SHA512 en bruto de `$filekey.$version.$position."a"` con la función `hash()`.

- `$version` es el valor `encrypted` que puede obtenerse de la tabla `oc_filecache` de la base de datos y no debe ser cero. Hay que tener en cuenta que un archivo de la tabla `oc_filecache` se identifica por su valor `path` y también por su valor `storage`, que hace referencia al campo `numeric_id` de la tabla `oc_storages`. Incluir `$version` en la clave de autenticación de mensajes impide que se intercambien bloques entre distintas versiones del mismo archivo.
- `$position` es el índice del bloque actual, empezando en `"0"`, y se le añade `"end"` en el último bloque del archivo. Incluir `$position` en la clave de autenticación de mensajes impide que se intercambien bloques dentro del mismo archivo. Además, añadir `"end"` a la clave de autenticación de mensajes del último bloque impide los ataques de truncamiento de archivos.

Después, la firma se deriva creando un SHA256-HMAC codificado en hexadecimal de `$encrypted[$position]` y la clave de autenticación de mensajes con la función `hash_hmac()` (se indica como `$signature[$position]`).

#### Guardar el archivo

El archivo cifrado se escribe en el archivo con los valores derivados `$encrypted[0..$n]`, `$iv[0..$n]` y `$signature[0..$n]` tal como se documenta en {nc-ref}`Tipo de archivo: archivo <file_type_file_label>`.

### Descifrado: leer la clave privada

#### Leer el archivo de clave privada

La clave privada se lee del archivo `$username.".privateKey"` y los valores `$encrypted`, `$iv` y `$signature` se analizan tal como se documenta en {nc-ref}`Tipo de archivo: archivo de clave privada <file_type_private_key_file_label>`.

#### Derivar la clave de descifrado

La sal de la clave de descifrado se deriva creando un hash SHA256 en bruto de `$uid.$instanceId.$instanceSecret` con la función `hash()`. `$instanceId` puede obtenerse como `instanceid` del `config.php`. `$instanceSecret` puede obtenerse como `secret` del `config.php`.

Después, la clave de descifrado se deriva creando un hash SHA256-PBKDF2 en bruto de la contraseña con la sal, 100.000 rondas y (de forma predeterminada) un tamaño de destino de 32 bytes (como requiere AES-256-CTR) con la función `hash_hmac()` (se indica como `$passphrase`).

La contraseña usada depende del tipo de clave:

- clave privada maestra: usar `secret` del `config.php`
- clave privada de compartición pública: usar una contraseña vacía
- clave privada de recuperación: usar la contraseña de recuperación
- clave privada de usuario: usar la contraseña del usuario

#### Comprobar la firma

La clave de autenticación de mensajes se deriva creando un hash SHA512 en bruto de `$passphrase.$version.$position."a"` con la función `hash()`.

- `$version` es siempre `"0"`.
- `$position` es siempre `"0"`.

Después, la firma se deriva creando un SHA256-HMAC codificado en hexadecimal de `$encrypted` y la clave de autenticación de mensajes con la función `hash_hmac()`. Continuar solo si la firma derivada es igual a *$signature*, lo que se comprueba con la función `hash_equals()`.

#### Descifrar la clave privada

La clave privada se descifra (de forma predeterminada) con AES-256-CTR con el `$iv` y la `$passphrase` mediante la función `openssl_decrypt()`.

### Descifrado: leer la clave de archivo

#### Leer la clave de archivo

La clave de archivo cifrada se lee del archivo `"fileKey"` tal como se documenta en {nc-ref}`Tipo de archivo: archivo de clave de archivo <file_type_file_key_file_label>`.

#### Leer la clave de sobre

La clave de sobre cifrada del destinatario se lee del archivo `$username.".shareKey"` tal como se documenta en {nc-ref}`Tipo de archivo: archivo de clave de compartición <file_type_share_key_file_label>`.

#### Descifrar/abrir la clave de archivo

La clave de archivo cifrada se descifra/abre con la función `openssl_open()` con la clave privada y la clave de sobre cifrada del destinatario (se indica como `$filekey`).

### Descifrado: descifrar el archivo

#### Dividir el archivo

El archivo cifrado se divide en un encabezado de 8192 bytes y uno o más bloques de 8192 bytes. Solo el último bloque cifrado puede ser más corto. Cada bloque se identifica por su índice, empezando en cero, dentro del archivo (se indica como `$position`). Los valores `$encrypted[0..$n]`, `$iv[0..$n]` y `$signature[0..$n]` se analizan tal como se documenta en {nc-ref}`Tipo de archivo: archivo <file_type_file_label>`.

#### Comprobar las firmas de los bloques

La clave de autenticación de mensajes se deriva creando un hash SHA512 en bruto de `$filekey.$version.$position."a"` con la función `hash()`.

- `$version` es el valor `encrypted` que puede obtenerse de la tabla `oc_filecache` de la base de datos y no debe ser cero. Hay que tener en cuenta que un archivo de la tabla `oc_filecache` se identifica por su valor `path` y también por su valor `storage`, que hace referencia al campo `numeric_id` de la tabla `oc_storages`. Incluir `$version` en la clave de autenticación de mensajes impide que se intercambien bloques entre distintas versiones del mismo archivo.
- `$position` es el índice del bloque actual, empezando en `"0"`, y se le añade `"end"` en el último bloque del archivo. Incluir `$position` en la clave de autenticación de mensajes impide que se intercambien bloques dentro del mismo archivo. Además, añadir `"end"` a la clave de autenticación de mensajes del último bloque impide los ataques de truncamiento de archivos.

Después, la firma se deriva creando un SHA256-HMAC codificado en hexadecimal de `$encrypted[$position]` y la clave de autenticación de mensajes con la función `hash_hmac()`. Continuar solo si la firma derivada es igual a `$signature[$position]`, lo que se comprueba con la función `hash_equals()`.

#### Descifrar los bloques

Cada bloque se descifra (de forma predeterminada) con AES-256-CTR con el `$iv[$position]` y la `$filekey` mediante la función `openssl_decrypt()`.

### Fuentes

- [Repositorio encryption-recovery-tools en GitHub](https://github.com/nextcloud/encryption-recovery-tools)
- {nc-doc}`Documentación de configuración del cifrado de Nextcloud <admin_manual/configuration_files/encryption_configuration>`
- [Respuesta en el foro de ayuda de {vendor}`Nextcloud` sobre el uso de la información de versión](https://help.nextcloud.com/t/allow-file-decryption-with-only-the-files-keys-and-passwords/436/12)
- [Código fuente: creación del código de autenticación de mensajes](https://github.com/nextcloud/server/blob/a374d8837d6de459500e619cf608e0721ea14574/apps/encryption/lib/Crypto/Crypt.php#L504)
- [Código fuente: derivación de la clave de cifrado](https://github.com/nextcloud/server/blob/a374d8837d6de459500e619cf608e0721ea14574/apps/encryption/lib/Crypto/Crypt.php#L346)
- [Código fuente: cifrado del archivo](https://github.com/nextcloud/server/blob/a374d8837d6de459500e619cf608e0721ea14574/apps/encryption/lib/Crypto/Crypt.php#L234)
- [Código fuente: cifrado/sellado de la clave de archivo](https://github.com/nextcloud/server/blob/a374d8837d6de459500e619cf608e0721ea14574/apps/encryption/lib/Crypto/Crypt.php#L686)
- [Código fuente: extracción de la clave privada y la clave pública](https://github.com/nextcloud/server/blob/a374d8837d6de459500e619cf608e0721ea14574/apps/encryption/lib/Crypto/Crypt.php#L124)
- [Código fuente: generación de la clave de archivo](https://github.com/nextcloud/server/blob/a374d8837d6de459500e619cf608e0721ea14574/apps/encryption/lib/Crypto/Crypt.php#L645)
- [Código fuente: generación del vector de inicialización](https://github.com/nextcloud/server/blob/a374d8837d6de459500e619cf608e0721ea14574/apps/encryption/lib/Crypto/Crypt.php#L634)
- [Código fuente: generación de un par de claves](https://github.com/nextcloud/server/blob/a374d8837d6de459500e619cf608e0721ea14574/apps/encryption/lib/Crypto/Crypt.php#L153)
````
