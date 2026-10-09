---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cambios al actualizar a Nextcloud 27: versiones de PHP, libreta de direcciones del sistema expuesta y nuevas extensiones estáticas en nginx."
---
# Actualización a Nextcloud 27

## Resumen

Esta página recoge los cambios que hay que conocer al actualizar a Nextcloud 27: las versiones de PHP recomendadas, la exposición de la libreta de direcciones del sistema y las nuevas extensiones de archivos estáticos en la configuración recomendada de nginx. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/release_notes/upgrade_to_27.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Requisitos del sistema

- Se recomienda PHP 8.2 antes que PHP 8.1.
- PHP 8.0 está obsoleto y podría eliminarse en Nextcloud 28.

### Libreta de direcciones del sistema expuesta

Nextcloud 27 expone la {nc-ref}`libreta de direcciones del sistema <system-address-book>`. Restringir los ajustes de enumeración si los usuarios no deben ver a otros usuarios.

### Configuración del servidor web

- La {nc-ref}`configuración de nginx <nginx-config>` recomendada ha cambiado, ya que Nextcloud ahora admite JavaScript de módulos con la extensión `.mjs` y archivos de audio con las extensiones `.ogg` / `.flac`; asegurarse de añadir estas extensiones a la lista de archivos estáticos.
````
