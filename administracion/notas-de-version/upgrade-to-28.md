---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cambios al actualizar a Nextcloud 28: PHP, archivos .mjs en el servidor web, comprobaciones de configuración, monitorización y vistas previas de Office."
---
# Actualización a Nextcloud 28

## Resumen

Esta página recoge los cambios que hay que conocer al actualizar a Nextcloud 28: la compatibilidad con PHP, cómo debe servir el servidor web los archivos `.mjs`, las comprobaciones de configuración que ahora se ejecutan en el servidor, el endpoint de monitorización y las vistas previas de archivos de Office con LibreOffice. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/release_notes/upgrade_to_28.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Requisitos del sistema

- PHP 8.3 ya es compatible, pero se recomienda 8.2.

### Configuración del servidor web

- La {nc-ref}`configuración de nginx <nginx-config>` recomendada ha cambiado, ya que Nextcloud Talk ahora sirve archivos de audio con las extensiones `.ogg` / `.flac`; asegurarse de añadir estas extensiones a la lista de archivos estáticos.
- Como algunas apps del núcleo ahora usan módulos de JavaScript, asegurarse de que el servidor web no reescribe las peticiones a archivos `.mjs`, sino que los sirve con el tipo MIME `text/javascript` y la cabecera `Cache-Control` adecuada, igual que `.js` y otras extensiones de archivos estáticos.

  - Si se usa Apache con la configuración de `.htaccess`, esto se hará automáticamente.
  - Para Nginx, consultar la {nc-ref}`configuración de Nginx <nginx-config>` recomendada.
  - Para otras configuraciones, asegurarse de añadir `.mjs` a la lista de extensiones de archivos estáticos en las configuraciones del servidor web y, en su caso, definir su tipo MIME en `/etc/mime.types`.

### Comprobaciones de configuración

Las comprobaciones de configuración (las que se ven en *Configuraciones de administración->Vista general*) que antes se ejecutaban desde el navegador web ahora se ejecutan en el servidor y no desde el navegador.

Esto significa que, tras la actualización, pueden aparecer algunos falsos positivos en instalaciones existentes. Esto no significa que las comprobaciones no sean válidas o estén rotas. Sí significa que ciertos aspectos de la configuración local que antes quizá no tenían efectos secundarios evidentes pueden ahora impedir que las pruebas obtengan resultados precisos.

En casi todos los casos, la solución es una o varias de las siguientes:

- verificar que todas las entradas de `trusted_domains` y el valor de `overwrite.cli.url` son válidos, se resuelven en DNS y son accesibles *desde el propio Nextcloud Server*
- verificar que el servidor puede acceder a su propia URL o a sus propias URL
- verificar que todos los valores de configuración `overwrite*` son razonables

Al diagnosticar lo anterior, muchos administradores han encontrado útil revisar no solo su *config.php* (para limpiarlo), sino también:

- que sus resolutores de DNS locales y sus archivos `/etc/hosts` sean razonables
- sus configuraciones de cortafuegos
- su configuración de red de contenedores si usan Docker o similares (especialmente para la conectividad saliente)

:::{tip}
La conectividad y la accesibilidad de URL concretas normalmente pueden probarse desde servidores o contenedores mediante `curl` o `wget`.
:::

### Monitorización

A partir de Nextcloud 28, el endpoint de monitorización ya no ofrece información sobre las actualizaciones de apps disponibles, ya que reunir esos datos siempre implica al menos una petición externa a apps.nextcloud.com.

Todavía se puede pedir al endpoint de monitorización que muestre las nuevas actualizaciones de apps usando el parámetro de URL skipApps=false. Sin embargo, no consultar este endpoint con demasiada frecuencia.

<https://github.com/nextcloud/serverinfo#api>

### Vistas previas de archivos de Office con LibreOffice

Nextcloud puede generar vistas previas de archivos de Office con LibreOffice.

Desde Nextcloud 28 también pueden crearse vistas previas de archivos EMF. Para activarlo, añadir `'OC\Preview\EMF'` a `enabledPreviewProviders`.

Hasta Nextcloud 28 se usaba el mismo perfil de usuario de LibreOffice para generar las vistas previas. LibreOffice solo puede invocarse una vez por perfil de usuario, así que la generación de la vista previa de un archivo de Office fallaba si en ese mismo momento se estaba creando otra.

A partir de Nextcloud 28 se usa un perfil de usuario de LibreOffice distinto para cada archivo. Inconveniente: si se suben 100 archivos emf, pueden acabar produciéndose 100 invocaciones de LibreOffice. No obstante, pueden usarse `preview_concurrency_new` y `preview_concurrency_all` para limitar el número de vistas previas que pueden generarse simultáneamente cuando php-sysvsem está disponible.

La opción de configuración `preview_office_cl_parameters` se eliminó con Nextcloud 28. Se espera que LibreOffice se inicie con los parámetros indicados, por lo que no es conveniente tener una opción de configuración para cambiarlos. Si esto causa algún problema, contactar con {vendor}`Nextcloud` a través de <https://github.com/nextcloud/server/pull/41395>.

:::{tip}
Las vistas previas de archivos EMF pueden activarse sin una instalación local de LibreOffice si ya se usa Nextcloud Office / Collabora. Asegurarse de tener instalado Nextcloud Office 8.3.0 y añadir `'OCA\Richdocuments\Preview\EMF'` a `enabledPreviewProviders`.
:::
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
