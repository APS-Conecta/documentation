---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Qué es la firma de código, cómo resolver los mensajes de integridad del código, cómo volver a analizar y qué significa cada error de verificación."
---
# Firma de código

## Resumen

Esta página explica la firma de código del núcleo y de las aplicaciones, responde a sus preguntas frecuentes y describe cómo resolver los mensajes de integridad del código, lanzar nuevos análisis e interpretar los errores de verificación. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/issues/code_signing.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

(nc-code_signing_label)=

Nextcloud admite la firma de código para las versiones del núcleo y para las aplicaciones de Nextcloud. La firma de código da a nuestros usuarios una capa adicional de seguridad, al garantizar que nadie más que las personas autorizadas pueda publicar actualizaciones.

También garantiza que todas las actualizaciones se hayan ejecutado correctamente, de modo que no quede ningún archivo atrás y todos los archivos antiguos se sustituyan como corresponde. En el pasado, las actualizaciones no válidas eran una fuente importante de errores al actualizar Nextcloud.

### Preguntas frecuentes

#### ¿Por qué {vendor}`Nextcloud` añadió la firma de código?

Al admitir la firma de código añadimos otra capa de seguridad, al garantizar que nadie más que las personas autorizadas pueda publicar actualizaciones de las aplicaciones, y al garantizar actualizaciones correctas.

#### ¿Restringimos Nextcloud?

El proyecto {vendor}`Nextcloud` es de código abierto y siempre lo será. No queremos dificultar a nuestros usuarios la ejecución de Nextcloud. Ningún error de firma de código en las actualizaciones impedirá que Nextcloud funcione, pero se mostrará un aviso en la página de administración. Para las aplicaciones que no están etiquetadas como «Official», el proceso de firma de código es opcional.

#### ¿Ya no es de código abierto?

El proyecto {vendor}`Nextcloud` es de código abierto y siempre lo será. El proceso de firma de código es opcional, aunque muy recomendable. La comprobación de código de las partes del núcleo de Nextcloud se activa cuando la rama de versión de la publicación de Nextcloud se ha establecido en stable.

Para las distribuciones personalizadas de Nextcloud se recomienda cambiar la rama de versión de la publicación en version.php a algo distinto de «stable».

#### ¿Es obligatoria la firma de código para las apps?

La firma de código es obligatoria para todas las aplicaciones de apps.nextcloud.com.

(nc-code_signing_fix_warning_label)=
### Corregir los mensajes de integridad del código no válida

En la página de administración de Nextcloud, en «Vista general», aparece un mensaje de error de integridad del código («Algunos archivos no han pasado la verificación de integridad…»), que ofrece las siguientes opciones:

1. Enlace a esta entrada de la documentación.
2. Mostrar una lista de los archivos no válidos.
3. Lanzar un nuevo análisis.

Para depurar los problemas causados por la comprobación de integridad del código, hacer clic en «Lista de archivos inválidos…»; se mostrará un documento de texto con los distintos problemas. El contenido del archivo será similar al del siguiente ejemplo:

```
Technical information
=====================
The following list covers which files have failed the integrity check. Please read
the previous linked documentation to learn more about the errors and how to fix
them.

Results
=======
- core
  - INVALID_HASH
      - /index.php
      - /version.php
  - EXTRA_FILE
      - /test.php
- calendar
  - EXCEPTION
      - OC\IntegrityCheck\Exceptions\InvalidSignatureException
      - Signature data not found.

Raw output
==========
Array
(
    [core] => Array
        (
            [INVALID_HASH] => Array
                (
                    [/index.php] => Array
                        (
                            [expected] =>
                            f1c5e2630d784bc9cb02d5a28f55d6f24d06dae2a0fee685f3
                            c2521b050955d9d452769f61454c9ddfa9c308146ade10546c
                            fa829794448eaffbc9a04a29d216
                            [current] =>
                            ce08bf30bcbb879a18b49239a9bec6b8702f52452f88a9d321
                            42cad8d2494d5735e6bfa0d8642b2762c62ca5be49f9bf4ec2
                            31d4a230559d4f3e2c471d3ea094
                        )

                    [/version.php] => Array
                        (
                            [expected] =>
                            c5a03bacae8dedf8b239997901ba1fffd2fe51271d13a00cc4
                            b34b09cca5176397a89fc27381cbb1f72855fa18b69b6f87d7
                            d5685c3b45aee373b09be54742ea
                            [current] =>
                            88a3a92c11db91dec1ac3be0e1c87f862c95ba6ffaaaa3f2c3
                            b8f682187c66f07af3a3b557a868342ef4a271218fe1c1e300
                            c478e6c156c5955ed53c40d06585
                        )

                )

            [EXTRA_FILE] => Array
                (
                    [/test.php] => Array
                        (
                            [expected] =>
                            [current] =>
                            09563164f9904a837f9ca0b5f626db56c838e5098e0ccc1d8b
                            935f68fa03a25c5ec6f6b2d9e44a868e8b85764dafd1605522
                            b4af8db0ae269d73432e9a01e63a
                        )

                )

        )

    [calendar] => Array
        (
            [EXCEPTION] => Array
                (
                    [class] => OC\IntegrityCheck\Exceptions\InvalidSignature
                    Exception
                    [message] => Signature data not found.
                )

        )

)
```

En la salida de error anterior puede verse que:

1. En el núcleo de Nextcloud (es decir, el propio servidor Nextcloud), los archivos «index.php» y «version.php» tienen una versión incorrecta.
2. En el núcleo de Nextcloud se ha encontrado el archivo adicional innecesario «/test.php».
3. No fue posible verificar la firma de la aplicación de calendario.

La solución es subir los archivos «index.php» y «version.php» correctos y eliminar el archivo «test.php». Para la excepción del calendario, contactar con el desarrollador de la aplicación. Para conocer otras formas de recibir soporte, consultar <https://nextcloud.com/support/>. Después de corregir estos problemas, comprobarlo haciendo clic en «Volver a escanear…».

:::{note}
Al usar un cliente FTP para subir esos archivos, asegurarse de que use el modo de transferencia `Binary` en lugar del modo de transferencia `ASCII`.
:::

(nc-rescans_label)=
### Nuevos análisis

Los nuevos análisis se lanzan en la instalación y con las actualizaciones. Pueden ejecutarse análisis manualmente con el comando `occ`. El primer comando analiza los archivos del servidor Nextcloud y el segundo analiza la app indicada. Todavía no existe un comando para analizar manualmente todas las apps:

```
occ integrity:check-core
occ integrity:check-app $appid
```

Consultar {nc-doc}`admin_manual/occ_command` para saber más sobre el uso de `occ`.

### Errores

:::{warning}
No modificar el propio `signature.json` mencionado.
:::

Al intentar verificar una firma de código pueden encontrarse los siguientes errores.

- `INVALID_HASH`

  - El archivo tiene un hash distinto del especificado en `signature.json`. Esto suele ocurrir cuando el archivo se ha modificado después de escribir los datos de la firma.

- `MISSING_FILE`

  - No se encuentra el archivo, pero está especificado en `signature.json`. O bien se ha omitido un archivo necesario, o bien hay que editar `signature.json`.

- `EXTRA_FILE`

  - El archivo no existe en `signature.json`. Esto suele ocurrir cuando se ha eliminado un archivo y `signature.json` no se ha actualizado. También ocurre si se han colocado archivos adicionales en la carpeta de instalación de Nextcloud.

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
