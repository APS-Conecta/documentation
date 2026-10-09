---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Crear alias de tipos MIME y asignaciones de extensiones en Nextcloud con archivos JSON propios, y cómo se elige el icono si falta el del tipo completo."
---
# Gestión de tipos MIME

## Resumen

Esta página explica, para quienes administran el servidor, cómo definir en Nextcloud alias de tipos MIME y asignaciones de extensiones de archivo a tipos MIME mediante archivos JSON propios. También describe cómo se recurre a un icono genérico cuando no existe el del tipo MIME completo.

````{upstream} admin_manual/configuration_mimetypes/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Alias de tipos MIME

Nextcloud permite crear alias para los tipos MIME, de modo que puedan mostrarse iconos personalizados para los archivos. Por ejemplo, puede interesar un icono de audio atractivo para los archivos de audio en lugar del icono de archivo predeterminado.

De forma predeterminada, Nextcloud se distribuye con `nextcloud/resources/config/mimetypealiases.dist.json`. No debe modificarse este archivo, ya que se sustituirá cuando se actualice Nextcloud. En su lugar, crear un archivo propio `nextcloud/config/mimetypealiases.json` con los alias personalizados. Usar la misma sintaxis que en `nextcloud/resources/config/mimetypealiases.dist.json`.

Una vez hechos los cambios en `mimetypealiases.json`, usar el comando `occ` para propagar los cambios por el sistema. Este ejemplo es para Ubuntu Linux:

```
$ sudo -E -u www-data php occ maintenance:mimetype:update-js

# you may also need to update the mimetype for existing files, see nextcloud/server#30566
$ sudo -E -u www-data php occ maintenance:mimetype:update-db --repair-filecache
```

Consultar {nc-doc}`admin_manual/occ_command` para saber más sobre `occ`.

Algunos tipos MIME habituales que pueden ser útiles al crear alias son:

- image: imagen genérica
- image/vector: imagen vectorial
- audio: archivo de audio genérico
- x-office/document: documento de procesador de textos
- x-office/spreadsheet: hoja de cálculo
- x-office/presentation: presentación
- text: documento de texto genérico
- text/code: código fuente

### Asignación de tipos MIME

Nextcloud permite a los administradores especificar la asignación de una extensión de archivo a un tipo MIME. Por ejemplo, los archivos que terminan en `mp3` se asignan a `audio/mpeg`. Esto, a su vez, permite a Nextcloud mostrar el icono de audio.

De forma predeterminada, Nextcloud incluye `mimetypemapping.dist.json`. Se trata de un array JSON sencillo. Los administradores no deben actualizar este archivo, ya que se sustituirá en las actualizaciones de Nextcloud. En su lugar, debe crearse y modificarse el archivo `mimetypemapping.json`; este archivo tiene prioridad sobre el archivo incluido.

### Obtención de iconos

Cuando se obtiene un icono para un tipo MIME, si no se encuentra el tipo MIME completo, la búsqueda recurre a la parte anterior a la barra. Dado un archivo con el tipo MIME 'image/my-custom-image', si no existe ningún icono para el tipo MIME completo, se usará en su lugar el icono de 'image'. Esto permite que los tipos MIME especializados recurran a iconos genéricos cuando los iconos correspondientes no están disponibles.
````
