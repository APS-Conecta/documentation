---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Distribuir archivos y carpetas predeterminados a los usuarios nuevos con skeletondirectory y cambiar la carpeta de plantillas predeterminada con occ."
---
# Proporcionar archivos predeterminados

## Resumen

Esta página explica cómo entregar un conjunto de archivos y carpetas predeterminados a cada usuario nuevo mediante un directorio skeleton propio y cómo cambiar la ruta predeterminada de las plantillas de usuario. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/default_files_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Es posible distribuir un conjunto de archivos y carpetas predeterminados a todos los usuarios colocándolos en un directorio que el usuario del servidor web pueda leer. Esto permite sustituir los archivos que Nextcloud incluye de forma predeterminada en `core/skeleton`. Ese directorio personalizado debe configurarse después en el `config.php` mediante la opción de configuración `skeletondirectory` (consultar {nc-doc}`admin_manual/configuration_server/config_sample_php_parameters`). Dejarla vacía para no copiar ningún archivo skeleton.

Estos archivos solo se copian a los usuarios nuevos tras su primer inicio de sesión, y los usuarios existentes no verán los archivos que se añadan a este directorio después de su primer inicio de sesión. Los archivos del directorio `skeleton` se copian en los directorios de datos de los usuarios, por lo que estos pueden modificar y eliminar los archivos sin afectar a los originales.

Esta captura de pantalla muestra un conjunto de fotos en el directorio `skeleton`. La pantalla muestra el conjunto de fotos en el directorio skeleton de Nextcloud.

Aparecen en la página Archivos de Nextcloud del usuario igual que cualquier otro archivo.

:::{note}
No se recomienda sobrescribir los archivos de `core/skeleton`, porque esos cambios se sobrescribirán en la próxima actualización del servidor Nextcloud.
:::

### Plantillas de archivo predeterminadas

La ruta predeterminada de las plantillas de usuario es `/Templates` (traducida al idioma del usuario). Si es necesario cambiar esta ruta para todos los usuarios, puede establecerse con

```
occ config:app:set core defaultTemplateDirectory --value="CustomPath"
```

Esto solo se aplica a los usuarios nuevos.

:::{note}
Para crear su propio directorio de plantillas, los usuarios deben hacer clic en el botón `+ New` y después en {guilabel}`Crear carpeta de plantillas`.
:::
````
