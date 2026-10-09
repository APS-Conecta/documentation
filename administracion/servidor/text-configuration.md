---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Ajustes de administración de la app Text con occ y php.ini: espacios de trabajo enriquecidos, extensión predeterminada, edición enriquecida y codificaciones."
---
# App Text

## Resumen

Esta página recoge, para quienes administran el servidor, los ajustes globales de la app Text: desactivar los espacios de trabajo enriquecidos o la edición enriquecida, cambiar la extensión de archivo predeterminada y fijar el orden de detección de codificaciones.

````{upstream} admin_manual/configuration_server/text_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Desactivar globalmente los espacios de trabajo enriquecidos

Quien administra puede desactivar globalmente los espacios de trabajo enriquecidos estableciendo la siguiente opción de configuración en 0 (el valor predeterminado es 1):

```
occ config:app:set text workspace_available --value=0
```

### Extensión de archivo predeterminada

La extensión de archivo predeterminada puede cambiarse a txt para crear siempre archivos de texto sin formato (el valor predeterminado es md):

```
occ config:app:set text default_file_extension --value=txt
```

### Desactivar la edición de texto enriquecido

La edición de texto enriquecido puede desactivarse globalmente para abrir siempre los archivos markdown en su formato sin procesar, sin representar el formato (el valor predeterminado es 1):

```
occ config:app:set text rich_editing_enabled --value=0
```

### Codificaciones de archivo

Text puede detectar automáticamente la codificación de los archivos y la convierte a UTF-8 al guardarlos. Debido a la variedad de codificaciones, no todas pueden detectarse; no obstante, puede configurarse una lista de codificaciones y la prioridad con la que deben detectarse mediante el ajuste de php `mbstring.detect_order` en php.ini:

```
mbstring.detect_order = ASCII,JIS,UTF-8,SJIS,EUC-JP
```
````
