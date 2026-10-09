---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Paquetes PHP de terceros con Composer en una app: autoloader, archivos a quitar, conflictos entre apps y herramientas aisladas con composer-bin-plugin."
---
(nc-dev-app-dependencies)=
# Gestión de dependencias

## Resumen

Esta página explica cómo usar paquetes PHP de terceros con Composer en una app: cargar su autoloader, quitar los archivos que no hacen falta en producción, por qué dos apps que comparten un paquete pueden entrar en conflicto y cómo aislar las herramientas de desarrollo con composer-bin-plugin. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/app_development/dependency_management.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Se pueden aprovechar paquetes de software existentes para construir una app de Nextcloud.

(nc-dev-app-composer)=
### Composer

Se pueden añadir paquetes php de terceros con [Composer][Composer]. Composer descarga los paquetes indicados en el directorio que se elija, normalmente en `/vendor`. Para aprovechar el autoloader de Composer, conviene añadir un `require_once` al método `register` de la clase `Application` en el código de {nc-ref}`arranque <Bootstrapping>` de la app.

#### Quitar de los paquetes los archivos innecesarios

Se recomienda encarecidamente quitar de los paquetes finales los archivos que no se necesitan en producción.
Esto se refiere especialmente, pero no exclusivamente, a:

* Archivos de desarrollo, p. ej., `/Makefile`
* Flujos de trabajo de CI, p. ej., `/.github`
* Recursos de pruebas, p. ej., `/tests`
* Configuración de herramientas de desarrollo, p. ej., `/phpunit.xml`, `/psalm.xml`
* Código de git o de otro control de versiones, p. ej., `/.git`

Se puede consultar el archivo [.gitignore del servidor](https://github.com/nextcloud/3rdparty/blob/master/.gitignore) para inspirarse más.

(nc-dev-app-composer-dependency-hell)=
#### Infierno de dependencias

Hay que tener cuidado con los paquetes que se añaden a una app. PHP no puede cargar dos veces la misma clase en dos versiones, así que puede haber conflictos entre el servidor de Nextcloud y una app, o entre dos o más apps, si requieren el mismo paquete. Por eso conviene mantener al mínimo el número de dependencias de producción y consultar {nc-ref}`app-composer-bin-tools`.

Como alternativa, se puede usar \[composer-bin-plugin\]\(<https://github.com/bamarni/composer-bin-plugin>) para evitar conflictos de dependencias entre apps.

1. Instalar composer-bin-plugin según su documentación.

   ```shell
   composer require --dev bamarni/composer-bin-plugin
   ```

2. Instalar las herramientas necesarias en el directorio vendor-bin.

   ```shell
   composer bin psalm require --dev psalm/phar
   composer bin psalm require --dev nextcloud/ocp:dev-master
   ```

3. Ajustar algo de configuración (ver abajo)
   - Añadir en *composer.json*:

   **Archivo {file}`composer.json`**:

   ```json
   {
       "extra": {
           "bamarni-bin": {
               "bin-links": true,
               "forward-command": true
           }
       }
   }
   ```

   - Añadir en *composer.json*:

   **Archivo {file}`composer.json`**:

   ```json
   {
       "scripts": {
           "post-install-cmd": [
               "[ $COMPOSER_DEV_MODE -eq 0 ] || composer bin all install --ansi"
           ],
           "post-update-cmd": [
               "[ $COMPOSER_DEV_MODE -eq 0 ] || composer bin all update --ansi"
           ]
       }
   }
   ```

   - Ajustar *psalm.xml*:
     - Comprobar que schemaLocation es correcto:

     **Archivo {file}`psalm.xml`**:

     ```xml
     xsi:schemaLocation="https://getpsalm.org/schema/config vendor-bin/psalm/vendor/vimeo/psalm/config.xsd"
     ```

     - Comprobar que tiene algo como esto:

     **Archivo {file}`psalm.xml`**:

     ```xml
     <projectFiles>
         <directory name="lib" />
         <ignoreFiles>
             <directory name="vendor" />
             <directory name="vendor-bin" />
         </ignoreFiles>
     </projectFiles>
     <extraFiles>
         <directory name="vendor" />
         <directory name="vendor-bin/psalm/vendor" />
     </extraFiles>
     ```

   - Ajustar *.php-cs-fixer.dist.php*

   **Archivo {file}`.php-cs-fixer.dist.php`**:

   ```PHP
   require_once __DIR__ . '/vendor-bin/cs-fixer/vendor/autoload.php';
   ```

##### Ejemplo de conflicto

Para ilustrar el problema, imaginar que la app *A* depende del paquete *foo* en la versión 1 y la app *B* depende del paquete *foo* en la versión 2. El paquete *foo* tuvo un cambio incompatible al que la app *B* se ha adaptado, mientras que *A* usa la API antigua.

Ambas apps incluyen un autoloader de Composer que carga automáticamente las funciones y clases de *foo*. Hay una carrera entre los dos autoloaders. Si al autoloader de *A* se le pide cargar la clase primero, se usará la v1. Si el autoloader de *B* carga primero las funciones y clases, será la v2. En algunos escenarios puede haber clases de la v1 y de la v2 cuando los autoloaders se invocan sin un orden definido.

Según qué funciones y clases se carguen, la app *A* puede funcionar o romperse. Lo mismo vale para *B*.

(nc-dev-app-composer-bin-tools)=
#### Herramientas de desarrollo

Es muy habitual que una app use herramientas de línea de comandos para comprobaciones de sintaxis, pruebas y compilación. Como muchas herramientas dependen de paquetes de Composer comunes, como `psr/*` y `symfony/console`, es probable que las apps produzcan un {nc-ref}`infierno de dependencias <app-composer-dependency-hell>` en los entornos de desarrollo.

El infierno de dependencias de las herramientas de línea de comandos se puede evitar usando el *Composer bin plugin*. Es un plugin de Composer que coloca las dependencias de desarrollo en un subdirectorio con un autoloader propio. Ese autoloader solo se usa si se usa la herramienta de línea de comandos. Para las apps de Nextcloud, esto significa que dos apps pueden usar versiones en conflicto de una misma herramienta. Además, los conflictos de dependencias entre las herramientas de una misma app dejan de ser un problema.

Entre las herramientas que se sabe que dan problemas y que deberían trasladarse a directorios del bin plugin están

* `friendsofphp/php-cs-fixer`
* `phpunit/phpunit`
* `vimeo/psalm`

Consultar la [página del paquete](https://packagist.org/packages/bamarni/composer-bin-plugin) para ver instrucciones de instalación actualizadas.

[Composer]: https://getcomposer.org/
````
