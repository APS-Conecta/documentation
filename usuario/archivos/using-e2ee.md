---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Cifrado de extremo a extremo: qué es, dónde habilitarlo, qué no se puede hacer desde el navegador y por qué guardar el mnemónico."
---
# Usar el cifrado de extremo a extremo

## Resumen

Esta página explica qué es el cifrado de extremo a extremo (E2EE), dónde habilitarlo en la aplicación cliente, que solo se pueden cifrar carpetas vacías, qué no se puede hacer desde el navegador y por qué es importante guardar el mnemónico. Está dirigida a usuarios que necesitan que el servidor nunca vea sus archivos sin cifrar.

````{upstream} user_manual/files/using_e2ee.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Si está habilitado en el servidor, Nextcloud ofrece la posibilidad de cifrar los archivos en los propios dispositivos. Esto se llama cifrado de extremo a extremo, o E2EE, porque los archivos se cifran en el propio dispositivo y solo se descifran en el propio dispositivo. El servidor nunca ve los archivos sin cifrar, lo que protege aún más la privacidad de los usuarios y la seguridad de los datos.

### Habilitar el E2EE

Si el administrador ha habilitado la [aplicación End-to-End Encryption](https://apps.nextcloud.com/apps/end_to_end_encryption), se puede empezar a usar desde uno de los propios dispositivos. Abrir los ajustes del cliente de Nextcloud y buscar los ajustes de cifrado E2EE.

:::{warning}
No es posible habilitar el cifrado en una carpeta desde el navegador. Debe hacerse en una aplicación cliente, ya sea un cliente de escritorio o un cliente móvil.
:::

### Cifrar una carpeta

:::{warning}
Solo se puede habilitar el cifrado en carpetas vacías.
:::

:::{warning}
No es posible habilitar el cifrado en una carpeta desde el navegador. Debe hacerse en una aplicación cliente, ya sea un cliente de escritorio o un cliente móvil.
:::

### Añadir un dispositivo con E2EE

En el navegador, primero hay que habilitar el E2EE en los ajustes personales. Esto es necesario porque el E2EE es menos seguro en el navegador y exige confiar plenamente en que el administrador no altere el código fuente que ejecutará el navegador. Las carpetas con E2EE son actualmente de solo lectura. Por lo tanto, no es posible añadir, quitar, editar ni compartir un archivo con E2EE desde el navegador.

### Mostrar el mnemónico

El mnemónico es una lista de palabras que se usa para cifrar y descifrar los archivos. Es importante guardar este mnemónico en un lugar seguro, ya que es la única forma de acceder a los archivos si se pierde el acceso al dispositivo. Si se pierde el acceso al mnemónico, se pierde el acceso a los archivos.

:::{warning}
No es posible mostrar el mnemónico en el navegador.
:::
````
