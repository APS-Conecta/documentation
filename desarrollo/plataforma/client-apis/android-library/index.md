---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cliente oficial para Android y biblioteca android-library para comunicarse con el servidor: código fuente, contribución, autenticación e integración en apps."
---
(nc-dev-androidindex)=
# Android

## Resumen

Esta sección presenta el cliente oficial de {vendor}`Nextcloud` para Android, cómo contribuir a su desarrollo y la biblioteca de Android de {vendor}`Nextcloud`, que permite a otras aplicaciones comunicarse con un servidor Nextcloud. Está dirigida a quienes desarrollan para Android.

````{upstream} developer_manual/client_apis/android_library/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

{vendor}`Nextcloud` ofrece un cliente oficial de {vendor}`Nextcloud` para Android, que da a sus usuarios acceso a sus archivos en su Nextcloud. También incluye funciones como la subida automática de fotos y vídeos a Nextcloud.

Para quienes desarrollan aplicaciones de terceros, {vendor}`Nextcloud` ofrece la biblioteca de Android de {vendor}`Nextcloud` bajo la licencia MIT.

### Desarrollo del cliente de {vendor}`Nextcloud` para Android

Si interesa trabajar en el cliente de {vendor}`Nextcloud` para Android, el código fuente se encuentra [en GitHub](https://github.com/nextcloud/android/). La configuración y el proceso de contribución [están documentados aquí](https://github.com/nextcloud/android/blob/master/SETUP.md).

Conviene empezar por resolver una o dos [incidencias para principiantes](https://github.com/nextcloud/android/labels/good%20first%20issue) para familiarizarse con el código, y tener en cuenta nuestro {nc-doc}`developer_manual/prologue/index`.

Para la autenticación se puede usar nuestro flujo de inicio de sesión habitual y, además (o en su lugar, si se acepta que los usuarios dependan de nuestra app Archivos), usar la estupenda [biblioteca Android SingleSignOn](https://github.com/nextcloud/Android-SingleSignOn/#how-to-use-this-library)

### Biblioteca de Android de {vendor}`Nextcloud`

Este documento describe cómo usar la biblioteca de Android de {vendor}`Nextcloud`. La biblioteca de Android de {vendor}`Nextcloud` permite comunicarse con cualquier servidor Nextcloud; entre las funciones incluidas están la sincronización de archivos, la subida y descarga de archivos, eliminar o renombrar archivos y carpetas, etc.

Esta biblioteca se puede añadir a un proyecto e integra sin problemas cualquier aplicación con Nextcloud.

La herramienta necesaria es cualquier IDE para Android; el IDE preferido en este momento es Android Studio.
````

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
