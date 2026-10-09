---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Comprobar con occ si quedan archivos en el formato de cifrado heredado (sin encabezado) y desactivar su compatibilidad en config.php."
---
# Migración del cifrado en el servidor

## Resumen

Esta página explica el formato de cifrado heredado que el servidor aún admite y cómo comprobar con `occ` si puede desactivarse esa compatibilidad. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/encryption_migration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Formato de cifrado

Nextcloud sigue admitiendo el esquema de cifrado heredado que se usaba para el cifrado en el servidor, en el que los archivos cifrados no contenían información de encabezado. Puede seguir usándose en instalaciones que aún tienen archivos cifrados de ownCloud 6 o anterior. Los archivos se actualizarán al nuevo formato de cifrado cuando vuelvan a escribirse. No obstante, se recomienda comprobar si todavía es necesario admitir este esquema.

A partir de la versión 20, en las instalaciones nuevas el cifrado heredado estará desactivado de forma predeterminada. Sin embargo, si se actualiza una instalación existente, hay una vía de migración para comprobar si puede desactivarse el cifrado heredado.

#### Comprobar si quedan archivos antiguos

En la línea de comandos, ejecutar:

> occ encryption:scan:legacy-format

El comando indica si puede eliminarse el modo de cifrado heredado. En ese caso, establecer *encryption.legacy_format_support* en 'false' en el config.php.
````
