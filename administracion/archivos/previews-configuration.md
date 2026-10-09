---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Parámetros de las vistas previas en config.php: desactivarlas, tamaño máximo, factor de escala, calidad JPEG y memoria máxima de generación."
---
# Configuración de las vistas previas

## Resumen

Esta página describe el sistema de vistas previas de archivos y los parámetros de `config/config.php` que lo controlan: desactivar las vistas previas, su tamaño máximo, el factor de escala máximo, la calidad JPEG y la memoria máxima para generarlas. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/previews_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El sistema de miniaturas de Nextcloud genera vistas previas de los archivos para todas las apps de Nextcloud que muestran archivos, como Archivos y Gallery.

La siguiente imagen muestra algunos ejemplos de vistas previas de distintos tipos de archivo. En ella aparecen miniaturas de varios archivos de imagen y de audio/video.

De forma predeterminada, Nextcloud puede generar vistas previas de los siguientes tipos de archivo:

- Archivos de imagen
- Documentos de texto

:::{note}
Nextcloud también puede generar vistas previas de otros tipos de archivo (como PDF, SVG, varios formatos de documentos de Office y varios formatos de video). Por motivos de seguridad y rendimiento, esos proveedores están desactivados de forma predeterminada. Aunque esos proveedores siguen disponibles, se desaconseja activarlos y se consideran sin soporte. La lista completa de los proveedores de vistas previas activados de forma predeterminada (así como de los desactivados de forma predeterminada) se encuentra en el {nc-doc}`parámetro de configuración <admin_manual/configuration_server/config_sample_php_parameters>` `enabledPreviewProviders`.
:::

### Parámetros

Debe tenerse en cuenta que el sistema de vistas previas de Nextcloud ya viene con valores predeterminados razonables, por lo que normalmente no es necesario ajustar esos valores de configuración.

Pero, si se considera necesario, los siguientes cambios deben hacerse en el archivo `config/config.php`. Como buena práctica, hacer una copia de seguridad de este archivo de configuración antes de hacer muchos cambios.

Después de cambiar uno o varios de los siguientes parámetros, puede convenir ejecutar el comando occ `preview:cleanup` para eliminar las vistas previas generadas con ajustes obsoletos.
Consultar {nc-ref}`occ_cleanup_previews` para obtener más información.

#### Desactivar las vistas previas:

En determinadas circunstancias, por ejemplo, si el servidor tiene recursos limitados, puede convenir desactivar la generación de vistas previas. Hay que tener en cuenta que, al hacerlo, se desactivan todas las vistas previas en todas las apps, incluida la app Gallery, que mostrarán iconos genéricos en lugar de miniaturas.

Establecer la opción de configuración `enable_previews` en `false`:

```
<?php
  'enable_previews' => false,
```

#### Tamaño máximo de las vistas previas:

Hay dos opciones de configuración para establecer el tamaño máximo de una vista previa.

```
<?php
  'preview_max_x' => null,
  'preview_max_y' => null,
```

De forma predeterminada, ambas opciones están establecidas en null. 'Null' equivale a sin límite. Los valores numéricos representan el tamaño en píxeles. El siguiente código limita las vistas previas a un tamaño máximo de 100×100px:

```
<?php
  'preview_max_x' => 100,
  'preview_max_y' => 100,
```

'preview_max_x' representa el eje x y 'preview_max_y' representa el eje y.

#### Factor de escala máximo:

Si en la instancia de Nextcloud hay almacenadas muchas imágenes pequeñas y el sistema de vistas previas genera vistas previas borrosas, puede convenir establecer un factor de escala máximo. De forma predeterminada, las imágenes se amplían hasta 10 veces su tamaño original:

```
<?php
  'preview_max_scale_factor' => 10,
```

Para desactivar por completo el escalado, puede establecerse el valor de configuración en '1':

```
<?php
  'preview_max_scale_factor' => 1,
```

Para desactivar el factor de escala máximo, puede establecerse el valor de configuración en 'null':

```
<?php
  'preview_max_scale_factor' => null,
```

#### Ajuste de calidad JPEG:

El ajuste de calidad JPEG predeterminado para las imágenes de vista previa es '80'. Puede cambiarse con:

```
occ config:app:set preview jpeg_quality --value="60"
```

#### Memoria máxima para la generación de imágenes:

De forma predeterminada, Nextcloud genera las vistas previas de las imágenes con la biblioteca gráfica GD. Esta opción de configuración limita la cantidad de memoria que se permite usar para generar vistas previas. Si crear la imagen de vista previa requiriera asignar más memoria que el límite, se desactivará la generación de la vista previa y se mostrará el icono predeterminado del tipo MIME.

El límite predeterminado es de 256 MB. Establecerlo en `-1` para no tener límite.

```
<?php
  'preview_max_memory' => 256,
```
````
