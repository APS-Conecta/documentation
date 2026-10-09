---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo carga las clases el cargador automático: mapa de clases del servidor, PSR-4 en las apps y reemplazo por un cargador de clases de Composer."
---
(nc-dev-appclassloader)=
# Cargador de clases

## Resumen

Esta página explica cómo funciona la carga automática de clases: el mapa de clases autoritativo del servidor y cómo actualizarlo, la asignación PSR-4 de los espacios de nombres de las apps y cómo reemplazar el cargador automático por uno de Composer. Está dirigida a quienes desarrollan apps o el servidor.

````{upstream} developer_manual/digging_deeper/classloader.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El cargador de clases lo proporciona Nextcloud y carga automáticamente todas las clases. Ver {nc-ref}`la sección de Composer <app-composer>` si se quieren incluir y cargar automáticamente bibliotecas de terceros.

### Carga automática del servidor

Las clases del servidor de Nextcloud usan un mapa de clases autoritativo, y el mapa de clases se confirma en git.

Al agregar, mover o eliminar un archivo de clase hay que actualizar los cargadores automáticos para que la clase se encuentre. El proceso es ligeramente distinto para las clases que pertenecen al propio servidor y para las apps que se incluyen en el repositorio del servidor:

1. Usar `composer dump-autoload` para actualizar el mapa de clases del servidor.
2. Usar `composer -d apps/dav/composer dump-autoload` para actualizar el mapa de clases de la app dav. Lo mismo se aplica a todas las demás apps que forman parte del repositorio del servidor.

:::{tip}
Usar la [opción patch de git](https://git-scm.com/docs/git-add#Documentation/git-add.txt---patch) al agregar archivos del cargador automático. Permite elegir solo las líneas relevantes para las clases que se agregaron, movieron o eliminaron. P. ej., `git add -p apps/dav/composer`.
:::

(nc-dev-app-psr4-autoloader)=
### Carga automática de las apps

Nextcloud usa un {nc-ref}`cargador automático PSR-4 <psr4>`. El espacio de nombres **\\OCA\\MyApp**
se asigna a {file}`/apps/myapp/lib/`. A partir de ahí se aplican las reglas normales de PSR-4, de modo
que una carpeta es una sección del espacio de nombres con las mismas mayúsculas y minúsculas, y el nombre de la clase coincide
con el nombre del archivo.

Si el ID de la app no puede convertirse en el espacio de nombres poniendo en mayúscula el primer
carácter, se puede especificar en el **appinfo/info.xml** proporcionando un campo
llamado **namespace**. El espacio de nombres requerido es el que va después del espacio de nombres
de nivel superior **OCA\\**; p. ej., para **OCA\\MyBeautifulApp\\Some\\OtherClass**
el espacio de nombres necesario sería **MyBeautifulApp** y se agregaría al
info.xml de la siguiente manera:

```xml
<?xml version="1.0"?>
<info>
   <namespace>MyBeautifulApp</namespace>
   <!-- other options here ... -->
</info>
```

Al ejecutar pruebas hay disponible una segunda raíz PSR-4. **\\OCA\\MyApp\\Tests** se
asigna así a {file}`/apps/myapp/tests/`.

(nc-dev-app-custom-classloader)=
#### Reemplazar el cargador automático de Nextcloud

El cargador automático de Nextcloud para las apps es flexible y robusto, pero no siempre es el más rápido. Se puede mejorar la velocidad de carga de la app incluyendo y optimizando un cargador de clases de Composer en la app.

En primer lugar, conviene familiarizarse con las [opciones de optimización del cargador automático de Composer](https://getcomposer.org/doc/articles/autoloader-optimization.md) y con su funcionamiento. Solo la optimización de nivel 1 es adecuada para Nextcloud, porque los mapas de clases autoritativos rompen los procesos de actualización en los que el código se reemplaza dinámicamente, y APCu no es una extensión obligatoria.

Una vez configurado Composer y volcados los mapas de clases, se puede reemplazar el cargador de clases genérico de Nextcloud por el cargador de clases de Composer. Para ello se coloca un archivo en *composer/autoload.php*. Si Nextcloud encuentra este archivo para una app, no se registrará ningún cargador de clases genérico. El siguiente contenido conecta el archivo con el archivo `autoloader.php` generado por Composer:

**Archivo {file}`composer/autoload.php`**:

```php
<?php

declare(strict_types=1);

require_once __DIR__ . '/../vendor/autoload.php';
```

:::{note}
Asegurarse de que el cargador automático se genere en el momento de la publicación y de que todos los archivos se incluyan en el tarball de la versión.
:::
````
