---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo probar una app: PHPUnit para las clases PHP con el bootstrap de pruebas y el contenedor, y Karma para el JavaScript."
---
# Pruebas

## Resumen

Esta página explica cómo probar una app: las clases PHP con PHPUnit, arrancando desde `tests/bootstrap.php` y obteniendo las clases desde el contenedor, y el JavaScript con Karma. Incluye un ejemplo de prueba con servicios simulados. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/testing.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Todas las clases PHP se pueden probar con [PHPUnit](https://phpunit.de/); el JavaScript se puede probar usando [Karma](http://karma-runner.github.io).

(nc-dev-testing-php)=
### PHP

Las pruebas de PHP van en el directorio **tests/** y PHPUnit se puede ejecutar con:

```
phpunit tests/
```

Al escribir pruebas propias, hay que asegurarse de que PHPUnit arranque desde {file}`tests/bootstrap.php`, para configurar correctamente varias variables de entorno y el registro del autoloader. Sin esto, aparecerán errores, ya que la política de seguridad del autoloader de Nextcloud impide el acceso al subdirectorio tests/. Esto se puede configurar en el archivo {file}`phpunit.xml` de la siguiente manera:

```xml
<phpunit bootstrap="../../tests/bootstrap.php">
```

Las clases PHP se deben probar accediendo a ellas desde el contenedor, para asegurarse de que el contenedor está bien conectado. Los servicios que deban simularse se pueden reemplazar directamente en el contenedor.

Una prueba para la clase **AuthorStorage** de {nc-doc}`developer_manual/basics/storage/filesystem`:

```php
<?php
namespace OCA\MyApp\Storage;

class AuthorStorage {

    private $storage;

    public function __construct($storage){
        $this->storage = $storage;
    }

    public function getContent($id) {
        // check if file exists and write to it if possible
        try {
            $file = $this->storage->getById($id);
            if($file instanceof \OCP\Files\File) {
                return $file->getContent();
            } else {
                throw new StorageException('Can not read from folder');
            }
        } catch(\OCP\Files\NotFoundException $e) {
            throw new StorageException('File does not exist');
        }
    }
}
```

tendría este aspecto:

```php
<?php
// tests/Storage/AuthorStorageTest.php
namespace OCA\MyApp\Tests\Storage;

class AuthorStorageTest extends \Test\TestCase {

    private $container;
    private $storage;

    protected function setUp() {
        parent::setUp();

        $app = new \OCA\MyApp\AppInfo\Application();
        $this->container = $app->getContainer();
        $this->storage = $storage = $this->getMockBuilder('\OCP\Files\Folder')
            ->disableOriginalConstructor()
            ->getMock();

        $this->container->registerService('RootStorage', function($c) use ($storage) {
            return $storage;
        });
    }

    /**
     * @expectedException \OCA\MyApp\Storage\StorageException
     */
    public function testFileNotFound() {
        $this->storage->expects($this->once())
            ->method('get')
            ->with($this->equalTo(3))
            ->will($this->throwException(new \OCP\Files\NotFoundException()));

        $this->container['AuthorStorage']->getContent(3);
    }

}
```

Hay que asegurarse de que la prueba extienda la clase `\Test\TestCase` y de llamar siempre a los métodos de la clase padre
al sobrescribir los métodos `setUp()`, `setUpBeforeClass()`, `tearDown()` o `tearDownAfterClass()`
de TestCase. Estos métodos preparan elementos importantes y limpian el sistema después de la prueba,
para que la prueba siguiente pueda ejecutarse sin efectos secundarios, como archivos y entradas en la caché de archivos que hayan quedado, etc.
````
