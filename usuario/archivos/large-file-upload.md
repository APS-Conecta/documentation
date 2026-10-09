---
tipo: explicacion
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Por qué las subidas desde el navegador tienen un límite de tamaño y qué hacer cuando se necesita subir archivos más grandes."
---
# Subida de archivos grandes

## Resumen

Esta página explica de dónde viene el límite de tamaño de las subidas desde el cliente web y a quién recurrir para ampliarlo. Está dirigida a usuarios que necesitan subir archivos grandes.

````{upstream} user_manual/files/large_file_upload.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Cuando se suben archivos a través del cliente web, Nextcloud está limitado por la configuración de PHP y Apache. Por defecto, PHP está configurado para aceptar subidas de hasta 2 MB. Como este límite de subida no es útil, le recomendamos que su administrador de Nextcloud aumente las variables de Nextcloud a tamaños apropiados para los usuarios.

Modificar algunas variables de Nextcloud requiere acceso administrativo. Si usted requiere límites de subida mayores que los que le ha ofrecido la configuración por defecto (o configurado por su administrador):

- Contacte con su administrador para solicitar un aumento a estas variables.

- Consulte la [documentación de administración](https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/big_file_upload_configuration.html) para orientarse sobre la gestión de los límites de tamaño de subida de archivos.
````
