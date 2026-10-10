---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Escribir y ejecutar pruebas unitarias de PHP con PHPUnit y de JavaScript con Karma y Jasmine para el servidor y sus apps."
---
# Pruebas unitarias

## Resumen

Esta página explica cómo escribir y ejecutar pruebas unitarias de PHP con PHPUnit, cómo inicializar Nextcloud para ellas y cómo correr las del proyecto del servidor con distintas bases de datos, y cómo ejecutar y depurar las pruebas de JavaScript con Karma y Jasmine. Está dirigida a quienes desarrollan el servidor y sus apps.

````{upstream} developer_manual/server/unit-testing.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Pruebas unitarias de PHP

#### Obtener PHPUnit

Nextcloud usa PHPUnit >= 8.5 para las pruebas unitarias.

Documentación de PHPUnit: <https://phpunit.de/documentation.html>

#### Escribir pruebas unitarias de PHP

Para empezar, hacer lo siguiente:

- Crear un directorio llamado `tests` en el nivel superior de la aplicación
- Crear un archivo PHP en el directorio y hacer `require_once` de la clase que se quiere probar

Después basta con ejecutar la prueba creada con **phpunit**.

:::{note}
Si la clase que se prueba usa funciones de Nextcloud (p. ej., OC::getUser()), hay que inicializar Nextcloud o usar inyección de dependencias.
:::

:::{note}
Lo más probable es que las pruebas se ejecuten con un usuario distinto al del servidor web. Esto puede causar problemas con los ajustes de PHP (p. ej., open_basedir) y obliga a ajustar la configuración.
:::

Un ejemplo de prueba sencilla sería:

{file}`/srv/http/nextcloud/apps/myapp/tests/testaddtwo.php`

```php
<?php
namespace OCA\Myapp\Tests;

class TestAddTwo extends \Test\TestCase {
    protected $testMe;

    protected function setUp() {
        parent::setUp();
        $this->testMe = new \OCA\Myapp\TestMe();
    }

    public function testAddTwo(){
          $this->assertEquals(5, $this->testMe->addTwo(3));
    }

}
```

{file}`/srv/http/nextcloud/apps/myapp/lib/testme.php`

```php
<?php
namespace OCA\Myapp;

class TestMe {
    public function addTwo($number){
        return $number + 2;
    }
}
```

En {file}`/srv/http/nextcloud/apps/myapp/` la prueba se ejecuta con:

```
phpunit tests/testaddtwo.php
```

La prueba debe extender la clase `\Test\TestCase`, y al sobrescribir los métodos `setUp()`, `setUpBeforeClass()`, `tearDown()` o `tearDownAfterClass()`
de TestCase hay que llamar siempre a los métodos padre. Estos métodos preparan cosas importantes y limpian el sistema después de la prueba,
para que la siguiente prueba pueda ejecutarse sin efectos secundarios, como archivos restantes y entradas en la caché de archivos, etc.

Para más recursos sobre PHPUnit, visitar: <https://www.phpunit.de/manual/current/en/writing-tests-for-phpunit.html>

#### Inicializar Nextcloud

Si el código usa funciones o clases de Nextcloud, hay que ponerlas a disposición de la prueba inicializando Nextcloud.

Para ello, hay que pasar el argumento `--bootstrap` al ejecutar PHPUnit:

{file}`/srv/http/nextcloud`:

```
phpunit --bootstrap tests/bootstrap.php apps/myapp/tests/testsuite.php
```

Si la prueba se ejecuta con un usuario distinto al del servidor web, hay que
ajustar el php.ini y los permisos de los archivos.

{file}`/etc/php/php.ini`:

```
open_basedir = none
```

{file}`/srv/http/nextcloud`:

```
su -c "chmod a+r config/config.php"
su -c "chmod a+rx data/"
su -c "chmod a+w data/nextcloud.log"
```

#### Ejecutar las pruebas unitarias del proyecto del servidor de Nextcloud

El proyecto del servidor proporciona pruebas unitarias del servidor con distintos backends de base de datos, como sqlite, mysql, pgsql y oci (para Oracle).
Cada base de datos que se quiera probar debe ser accesible, ya sea

- de forma nativa, configurada con

  - Host: localhost
  - Base de datos: oc_autotest
  - Usuario: oc_autotest
  - Contraseña: owncloud

- o mediante docker, definiendo la variable de entorno USEDOCKER.

Las notas sobre cómo configurar las bases de datos para esta prueba se encuentran en <https://github.com/nextcloud/server/blob/master/autotest.sh>.

Para ejecutar las pruebas con todos los motores de base de datos:

```
./autotest.sh
```

Para ejecutar las pruebas solo con sqlite:

```
./autotest.sh sqlite
```

Para ejecutar un conjunto de pruebas concreto (tener en cuenta que la ruta del archivo de prueba es relativa al directorio «tests»):

```
./autotest.sh sqlite lib/share/share.php
```

#### Lecturas adicionales

- <https://googletesting.blogspot.de/2008/08/by-miko-hevery-so-you-decided-to.html>
- <https://www.phpunit.de/manual/current/en/writing-tests-for-phpunit.html>
- <https://www.youtube.com/watch?v=4E4672CS58Q&feature=bf_prev&list=PLBDAB2BA83BB6588E>
- Clean Code: A Handbook of Agile Software Craftsmanship (Robert C. Martin)

### Pruebas unitarias de JavaScript para el servidor

Las pruebas unitarias de JavaScript para el **servidor** y las **apps del servidor** se hacen con el ejecutor de pruebas [Karma](http://karma-runner.github.io) y [Jasmine](https://jasmine.github.io/).

#### Instalar Node JS

Para ejecutar las pruebas unitarias de JavaScript hay que instalar **Node JS**.

Puede obtenerse aquí: <https://nodejs.org/>

Después hay que configurar el entorno de pruebas de **Karma**.
La forma más sencilla de hacerlo es ejecutar primero el script de pruebas automático; ver la sección siguiente.

#### Ejecutar todas las pruebas

Para ejecutar todas las pruebas, basta con ejecutar:

```
./autotest-js.sh
```

Esto también configura automáticamente el entorno de pruebas.

#### Depurar las pruebas en el navegador

Para depurar las pruebas en el navegador, hay que ejecutar **Karma** en modo navegador:

```
karma start tests/karma.config.js
```

Desde ahí, abrir la URL <http://localhost:9876> en un navegador web.

En esa página, hacer clic en el botón «Debug».

Aparecerá una página vacía, desde la que hay que abrir la consola del navegador (F12 en Firefox/Chrome).

Cada vez que se recargue la página, las pruebas unitarias se volverán a lanzar y mostrarán los resultados en la consola del navegador.

#### Rutas de las pruebas unitarias

Hay ejemplos de pruebas unitarias de JavaScript en {file}`apps/files/tests/js/`.

Las pruebas unitarias del código JavaScript de la app core están en {file}`core/js/tests/specs`.

#### Documentación

Estos son algunos enlaces útiles sobre cómo escribir pruebas unitarias con Jasmine y Sinon:

- Ejecutor de pruebas Karma: <https://karma-runner.github.io/>
- Jasmine: <https://pivotal.github.io/jasmine>
- Sinon (para mocks y stubs): <http://sinonjs.org/>
````
