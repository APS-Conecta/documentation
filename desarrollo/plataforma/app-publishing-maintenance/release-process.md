---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo publicar una versión de una app: versionado semántico, registro de cambios, versiones preliminares y nightly, pasos de publicación y apps incluidas."
---
(nc-dev-app-release-process)=
# Proceso de publicación de versiones

## Resumen

Esta página documenta el proceso de publicar una versión de una app: la preparación (versionado semántico, registro de cambios, versiones preliminares y nightly), los pasos de la publicación, las tareas posteriores y el caso de las apps incluidas con el servidor. Está dirigida a quienes mantienen apps.

````{upstream} developer_manual/app_publishing_maintenance/release_process.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Visión general

Esta página documenta el proceso general y las tareas de la publicación de una app de Nextcloud al público, así como las tareas de preparación y de seguimiento.

No todos los pasos descritos se aplican a todas las apps. Algunas requieren menos pasos; para otras hay trabajo adicional que hacer. Ajustar el proceso en consecuencia.

### Antes de la publicación

#### Seguimiento de cambios

Si la app usa algún tipo de seguimiento, como milestones de Github, proyectos o similares, asegurarse de que los cambios programados de la app se hayan fusionado en la rama de destino.

En este punto probablemente se pueda asignar una fecha de publicación (si aún no está fijada) al milestone y cerrarlo.

(nc-dev-app-versioning)=
#### Versionado

Cada actualización de una app necesita un número de versión nuevo y mayor. Antes de preparar una versión concreta, quien mantiene la app tiene que decidir qué número de versión tendrá la nueva versión.

Se recomienda encarecidamente que las apps sigan el [versionado semántico](https://semver.org/) (semver). Este esquema permite a quienes administran y a los usuarios entender mejor qué tipo de cambio pueden esperar cuando hay disponible una actualización de una app.

Aplicar semver a las apps de Nextcloud da tres tipos de actualizaciones: mayor, menor y de parche.

##### Actualizaciones de parche

Incrementar el número de versión de parche cuando

- Se corrige un error
- Se añaden o corrigen traducciones, pero **no** se eliminan

:::{tip}
Ejemplo: la app está en la versión 3.7.2. La siguiente versión de parche será la 3.7.3.
:::

##### Actualizaciones menores

Incrementar el número de versión menor cuando

- Hay una función nueva
- Se admite una nueva versión mayor de Nextcloud
- Se admite una nueva versión mayor o menor de PHP
- Se admite un tipo de base de datos adicional
- Se abandona una versión de Nextcloud que ha llegado al fin de su vida útil (EOL), p. ej., cuando se elimina Nextcloud 19
- Se abandona una versión de PHP que ha llegado al fin de su vida útil (EOL), p. ej., cuando se elimina PHP 7.3
- Cualquier otro cambio que mantenga la app compatible con los entornos compatibles anteriormente (compatibilidad hacia delante)

:::{tip}
Ejemplo: la app está en la versión 3.7.2. La siguiente versión menor será la 3.8.0.
:::

##### Actualización mayor

Incrementar el número de versión mayor cuando

- La app deja de admitir una versión mayor de Nextcloud que no ha llegado al fin de su vida útil (EOL), p. ej., cuando se elimina la compatibilidad con Nextcloud 23 y la app pasa a requerir Nextcloud 24 o posterior
- La app deja de admitir una versión mayor o menor de PHP que no ha llegado al fin de su vida útil (EOL), p. ej., cuando se elimina PHP 8.0 y la app pasa a requerir PHP 8.1 o posterior
- Un tipo de base de datos deja de admitirse, p. ej., cuando quien mantiene la app decide dejar de admitir SQLite
- Cualquier otro cambio que haga la app incompatible con un entorno compatible anteriormente (cambio incompatible)

:::{tip}
Ejemplo: la app está en la versión 3.7.2. La siguiente versión mayor será la 4.0.0.
:::

#### Registro de cambios

Si la app [mantiene un registro de cambios](https://keepachangelog.com/en/1.0.0/) (p. ej., CHANGELOG.md en la raíz del proyecto), es el momento de actualizarlo con todos los elementos **añadidos**, **cambiados** y **corregidos**.

:::{tip}
Usar `git log v3.7.1..HEAD --pretty=oneline | grep -v tx-robot | grep -v "Merge " | grep -v "Bump "` en la rama de destino de la versión para obtener una lista compacta de todos los cambios desde la versión v3.7.1. Ajustarlo al número de la versión anterior.
:::

#### Versiones preliminares

Opcionalmente, quienes mantienen apps pueden elegir publicar versiones preliminares de sus apps en la tienda de apps para usuarios pioneros y testers. La periodización precisa queda a criterio de quien mantiene la app. Los periodos habituales incluyen las etapas **alpha**, **beta** y **rc** (release candidate).

El proceso de publicación es idéntico al de una versión final; solo el número de versión lleva un sufijo.

:::{tip}
Ejemplo: la app se publicará como versión 3.7.2. Por tanto, podría haber una **v3.7.2-alpha.1**, **v3.7.2-beta.1**, **v3.7.2-rc.1**, **v3.7.2-rc.2** y la versión final **v3.7.2**.
:::

El canal de actualización define si el servidor instala versiones preliminares. Este ajuste se encuentra en los ajustes de administración o en el archivo `config/config.php`. El servidor instalará versiones preliminares si su canal de actualización está establecido en `beta`, `daily` o `git`. Con cualquier otro ajuste, no se instalarán versiones preliminares.

:::{tip}
No publicar las versiones preliminares como versión nightly en la tienda de apps, o las instalaciones de Nextcloud no podrán actualizarse. Publicar con cualquier sufijo (alfanumérico) basta para marcar la versión como no lista para producción, y las instancias pueden seguir actualizándose a ella.
:::

#### Versiones nightly

Además de publicar versiones preliminares, quienes mantienen apps pueden publicar versiones nightly. Se consideran aún menos estables que las versiones preliminares. En la tienda de apps, estas versiones nightly se marcan por separado.

Los servidores instalarán automáticamente las versiones nightly si el canal de actualización está establecido en `daily` o `git`. Con cualquier otro ajuste, el servidor ignorará las versiones nightly.

:::{tip}
Internamente, el servidor usa la función de PHP `version_compare`. Hay que pensar bien el número de versión de una versión nightly, de modo que las versiones (preliminares) publicadas después se consideren más nuevas que las nightly.
:::

### La publicación

Desde un punto de vista abstracto, la parte principal de publicar una versión consiste en transformar el código fuente en un componente de software instalable.

Esta parte suele estar automatizada con scripts y depende mucho del tipo de app. La siguiente lista está incompleta, pero debería dar una idea aproximada de los pasos que debería contener un script de publicación:

- Cambiar a la rama de destino y traer los últimos cambios
- Etiquetar la versión en Git y enviar los cambios locales, si los hay
- Instalar todas las {nc-ref}`dependencias <app-dependencies>`
  - Ejecutar `composer i --no-dev` si la app usa {nc-ref}`Composer <app-composer>`
  - Ejecutar `npm ci` si la app usa {nc-ref}`npm <app-npm>`
- Generar los artefactos compilados
  - {nc-ref}`Compilar los scripts de producción para el front-end <app-npm-build>`
  - Ejecutar cualquier generación de código (p. ej., mediante un {nc-ref}`script de Composer <app-composer>`)
- Eliminar los archivos de desarrollo
  - Eliminar cualquier tipo de archivo de configuración (`composer.*`, `package.json`, `package-lock.json`, `.babelrc`, etc.) que no se necesite en producción
  - Eliminar el código fuente que no se necesite en producción, p. ej., JavaScript que se compila en un bundle
  - Eliminar las pruebas
- {nc-ref}`Firmar los archivos de la versión <app-code-signing>` para generar un appinfo/signature.json
- Empaquetar el resto en un tarball *.tar.gz*
- Subir el tarball para su distribución, p. ej., como artefacto de una release de Github o a un servidor de descargas dedicado
- {nc-ref}`Publicar <app-store-publishing>` en la tienda de apps

### Después de la publicación

#### Crear la rama

Si quien mantiene la app mantiene ramas estables a las que se retroportan las correcciones de errores, cualquier versión mayor o menor requiere crear una rama a partir de la rama principal actual.

#### Preparar las siguientes versiones

El milestone de destino se cerró durante la preparación de la versión. Ahora es el momento de crear un nuevo milestone para la siguiente o las siguientes versiones.

### Apps incluidas

La mayoría de las apps se distribuyen mediante la tienda de apps de {vendor}`Nextcloud`. Unas pocas apps se empaquetan e incluyen con Nextcloud. Para ellas hay que tener en cuenta algunas cosas.

#### Gestión de ramas de Git

El script de publicación simplemente clona con git los repositorios de las apps. Los repositorios de las apps incluidas necesitan ramas que se correspondan con las ramas del [repositorio del servidor de Nextcloud](https://github.com/nextcloud/server):

- La rama `master` se usa para crear las compilaciones diarias de Nextcloud
- Las ramas `stable*` se usan para compilar las versiones estables, p. ej., `stable24` para Nextcloud 24.x.y.

Como las apps solo se clonan, no es posible tener un paso de compilación para las apps incluidas. Las apps incluidas tienen que *vendorizar* todos sus artefactos de publicación.

Ejemplo:

- La app usa dependencias de `composer`: hacer commit de todas las dependencias de producción en el directorio `vendor`
- La app usa dependencias de `npm` y herramientas de compilación del front-end: hacer commit de todos los artefactos del front-end en el directorio `js`

#### Versionado

Como cada rama `stable*` apunta a una sola versión mayor de Nextcloud y abandona la anterior, lo mejor es tener una versión mayor de la app por cada rama estable. Ver {nc-ref}`el versionado de apps <app-versioning>` para más detalles.

Ejemplo:

- `master`: versión 8.0.0, para Nextcloud 27
- `stable26`: versión 7.0.0, para Nextcloud 26
- `stable25`: versión 6.0.0, para Nextcloud 25

Las correcciones retroportadas incrementan la versión de parche en una rama estable. Las funciones retroportadas incrementan la versión menor.

#### Distribución híbrida

En situaciones muy poco frecuentes, las apps pueden ser apps incluidas **y** distribuirse mediante la tienda de apps. En esos casos es importante asegurarse de que la versión incluida sea igual o superior a la versión de la tienda de apps, para evitar una vuelta a una versión anterior durante la actualización de Nextcloud.

No se recomienda la distribución híbrida.
````
