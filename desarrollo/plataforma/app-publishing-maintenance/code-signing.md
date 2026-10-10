---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Firma de código de las apps: por qué existe, cómo funciona con certificados X.509, cómo firmar una app y qué significa cada error de verificación."
---
(nc-dev-app-code-signing)=
# Firma de código

## Resumen

Esta página explica la firma de código de las apps: sus preguntas frecuentes, los detalles técnicos basados en X.509, cómo afecta a las apps de la tienda de apps, cómo obtener la firma de una app y qué significa cada error de verificación. Está dirigida a quienes desarrollan y publican apps.

````{upstream} developer_manual/app_publishing_maintenance/code_signing.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud admite la firma de código para las versiones del núcleo y para las aplicaciones de Nextcloud. La firma de código da a nuestros usuarios una capa adicional de seguridad, al garantizar que nadie más que las personas autorizadas pueda publicar actualizaciones.

También garantiza que todas las actualizaciones se hayan ejecutado correctamente, de modo que no quede ningún archivo atrás y todos los archivos antiguos se sustituyan como corresponde. En el pasado, las actualizaciones no válidas eran una fuente importante de errores al actualizar Nextcloud.

### Preguntas frecuentes

#### ¿Por qué {vendor}`Nextcloud` añadió la firma de código?

Al admitir la firma de código añadimos otra capa de seguridad, al garantizar que nadie más que las personas autorizadas pueda publicar actualizaciones de las aplicaciones, y al garantizar actualizaciones correctas.

#### ¿Restringimos Nextcloud?

El proyecto {vendor}`Nextcloud` es de código abierto y siempre lo será. No queremos dificultar a nuestros usuarios la ejecución de Nextcloud. Ningún error de firma de código en las actualizaciones impedirá que Nextcloud funcione, pero se mostrará un aviso en la página de administración. Para las aplicaciones que no están etiquetadas como «Featured», el proceso de firma de código es opcional.

#### ¿Ya no es de código abierto?

El proyecto {vendor}`Nextcloud` es de código abierto y siempre lo será. El proceso de firma de código es opcional, aunque muy recomendable. La comprobación de código de las partes del núcleo de Nextcloud se activa cuando la rama de versión de la publicación de Nextcloud se ha establecido en stable.

Para las distribuciones personalizadas de Nextcloud se recomienda cambiar la rama de versión de la publicación en version.php a algo distinto de «stable».

#### ¿Es obligatoria la firma de código para las apps?

La firma de código es obligatoria para todas las aplicaciones de apps.nextcloud.com.

### Detalles técnicos

Nextcloud usa un enfoque basado en X.509 para gestionar la autenticación del código. Cada versión de Nextcloud contiene el certificado de una autoridad raíz de firma de código de {vendor}`Nextcloud` incluida en ella. La clave privada de este certificado solo es accesible para quien lidera el proyecto, que puede entregar una copia de esta clave privada a miembros de confianza del proyecto.

Esta autoridad raíz solo se usa para firmar solicitudes de firma de certificado (CSR) de certificados adicionales. Los certificados emitidos por la autoridad raíz deben limitarse siempre a un ámbito específico, normalmente el identificador de la aplicación. Esta restricción se impone mediante el atributo `CN` del certificado.

La firma de código se realiza entonces creando un archivo `signature.json` con el siguiente contenido:

```json
{
    "hashes": {
        "/filename.php":
        "2401fed2eea6f2c1027c482a633e8e25cd46701f811e2d2c10dc213fd95fa60e350b
        ccbbebdccc73a042b1a2799f673fbabadc783284cc288e4f1a1eacb74e3d",
        "/lib/base.php":
        "55548cc16b457cd74241990cc9d3b72b6335f2e5f45eee95171da024087d114fcbc2
        effc3d5818a6d5d55f2ae960ab39fd0414d0c542b72a3b9e08eb21206dd9"
    },
    "certificate": "-----BEGIN CERTIFICATE-----
    MIIBvTCCASagAwIBAgIUPvawyqJwCwYazcv7iz16TWxfeUMwDQYJKoZIhvcNAQEF\
    nBQAwIzEhMB8GA1UECgwYb3duQ2xvdWQgQ29kZSBTaWduaW5nIENBMB4XDTE1MTAx\
    nNDEzMTcxMFoXDTE2MTAxNDEzMTcxMFowEzERMA8GA1UEAwwIY29udGFjdHMwgZ8w\
    nDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBANoQesGdCW0L2L+a2xITYipixkScrIpB\
    nkX5Snu3fs45MscDb61xByjBSlFgR4QI6McoCipPw4SUr28EaExVvgPSvqUjYLGps\
    nfiv0Cvgquzbx/X3mUcdk9LcFo1uWGtrTfkuXSKX41PnJGTr6RQWGIBd1V52q1qbC\
    nJKkfzyeMeuQfAgMBAAEwDQYJKoZIhvcNAQEFBQADgYEAvF/KIhRMQ3tYTmgHWsiM\
    nwDMgIDb7iaHF0fS+/Nvo4PzoTO/trev6tMyjLbJ7hgdCpz/1sNzE11Cibf6V6dsz\
    njCE9invP368Xv0bTRObRqeSNsGogGl5ceAvR0c9BG+NRIKHcly3At3gLkS2791bC\
    niG+UxI/MNcWV0uJg9S63LF8=\n
    -----END CERTIFICATE-----",
    "signature": "U29tZVNpZ25lZERhdGFFeGFtcGxl"
}
```

`hashes` es un array con todos los archivos de la carpeta y sus hashes SHA-512 correspondientes. `certificate` es el certificado usado para firmar. Debe haberlo emitido la autoridad raíz de {vendor}`Nextcloud`, y su CN debe tener permiso para realizar la acción requerida. `signature` es entonces una firma de los hashes que puede verificarse con el certificado.

Incluir el certificado dentro del archivo `signature.json` tiene la ventaja de que, aunque un desarrollador pierda su certificado, las actualizaciones futuras pueden seguir garantizándose con la emisión de un certificado nuevo.

### Cómo afecta la firma de código a las apps de la tienda de apps

- Las apps que tienen la etiqueta `Featured` **DEBEN** estar firmadas.
  Las apps `Featured` sin firmar ya no podrán instalarse.
- Las apps que se firmaron en una versión anterior **DEBEN** firmarse también en todas las versiones futuras; de lo contrario, se rechazará la actualización.

### Cómo obtener la firma de la app

Los siguientes comandos requieren tener OpenSSL instalado en el equipo. Conservar todos los archivos generados para firmar la aplicación. Los siguientes ejemplos suponen que se intenta firmar una aplicación llamada *contacts*.

1. Generar una clave privada y una CSR: `openssl req -nodes -newkey rsa:4096 -keyout contacts.key -out contacts.csr -subj "/CN=contacts"`. Sustituir *contacts* por el identificador de la aplicación.
2. Publicar la CSR en <https://github.com/nextcloud/app-certificate-requests>, en un nuevo pull request con el enlace a un repositorio público con el código de la app. Mantener en secreto el archivo de clave privada (`contacts.key`) y no revelarlo a terceros.
3. {vendor}`Nextcloud` proporcionará el certificado firmado.
4. Ejecutar `./occ integrity:sign-app` para firmar la aplicación e indicar las claves privada y pública, así como la ruta a la aplicación.
   Un ejemplo válido sería: `./occ integrity:sign-app --privateKey=/Users/lukasreschke/contacts.key --certificate=/Users/lukasreschke/CA/contacts.crt --path=/Users/lukasreschke/Programming/contacts`

La herramienta occ guardará un archivo `signature.json` dentro de la carpeta `appinfo` de la aplicación. Después, comprimir la carpeta de la aplicación y subirla a apps.nextcloud.com. Tener en cuenta que cualquier cambio en la aplicación después de firmarla exige volver a firmarla. Por eso, si no se quiere distribuir algunos archivos, eliminarlos antes de ejecutar el comando de firma.

En caso de perder el certificado, enviar una nueva CSR como se describe arriba e indicar que se perdió el anterior. {vendor}`Nextcloud` revocará el certificado anterior.

Si se mantiene una app junto con varias personas, se recomienda designar a un responsable de publicación encargado del proceso de firma y de la subida a apps.nextcloud.com. Si hay casos en que esto no es viable y se necesitan varios certificados, {vendor}`Nextcloud` puede crearlos caso por caso. No recomendamos que los desarrolladores compartan su clave privada.

### Errores

Al intentar verificar una firma de código pueden encontrarse los siguientes errores.
Para saber cómo acceder a esos resultados, consultar la sección de problemas del manual de administración de Nextcloud Server.

- `INVALID_HASH`

  - El archivo tiene un hash distinto del especificado en `signature.json`. Esto suele ocurrir cuando el archivo se ha modificado después de escribir los datos de la firma.

- `MISSING_FILE`

  - No se encuentra el archivo, pero está especificado en `signature.json`. O bien se ha omitido un archivo necesario, o bien hay que editar `signature.json`.

- `EXTRA_FILE`

  - El archivo no existe en `signature.json`. Esto suele ocurrir cuando se ha eliminado un archivo y `signature.json` no se ha actualizado.

- `EXCEPTION`

  - Otra excepción ha impedido la verificación del código. Actualmente existen las siguientes excepciones:

    - «`Signature data not found.`»

      - La app tiene la firma de código obligatoria activada, pero no se ha encontrado ningún archivo `signature.json` en su carpeta `appinfo`.

    - «`Certificate is not valid.`»

      - El certificado no lo ha emitido la autoridad raíz oficial de firma de código de {vendor}`Nextcloud`.

    - «`Certificate is not valid for required scope. (Requested: %s, current: %s)`»

      - El certificado no es válido para la aplicación definida. Los certificados solo son válidos para el identificador de app definido y no pueden usarse para otras.

    - «`Signature could not get verified.`»

      - Hubo un problema al verificar la firma de `signature.json`.
````
