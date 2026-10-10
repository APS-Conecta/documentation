---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Estándares de código de PHP: etiquetas de apertura y cierre, PHPDoc, nombres, operadores estrictos, estructuras de control y pruebas unitarias."
---
# Estándares de código de PHP

## Resumen

Esta página recoge los estándares de código de PHP: la configuración compartida de PHP Coding Standards Fixer, las etiquetas de apertura y cierre, los comentarios PHPDoc, los nombres, los operadores, las estructuras de control y las pruebas unitarias. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/getting_started/coding_standards/php.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Desde Nextcloud 19 hay una configuración compartida de [PHP Coding Standards Fixer](https://github.com/FriendsOfPhp/PHP-CS-Fixer) que se puede usar para formatear automáticamente el código fuente de la app. Para todos los detalles, ver el [repositorio en GitHub](https://github.com/nextcloud/coding-standard/).

Usar siempre:

```
<?php
```

al principio del código PHP. El cierre final:

```
?>
```

no debe usarse al final del archivo debido al [posible problema de enviar espacios en blanco](https://stackoverflow.com/questions/4410704/php-closing-tag).

### Comentarios

Todos los métodos de la API deben marcarse con anotaciones [PHPDoc](https://en.wikipedia.org/wiki/PHPDoc). Un ejemplo sería:

```php
<?php

/**
 * Description what method does
 * @param Controller $controller the controller that will be transformed
 * @param API $api an instance of the API class
 * @throws APIException if the api is broken
 * @since 4.5
 * @return string a name of a user
 */
public function myMethod(Controller $controller, API $api) {
  // ...
}
```

### Objetos, funciones, arrays y variables

Usar *UpperCamelCase* para los objetos y *lowerCamelCase* para las funciones y variables. Al establecer
un parámetro predeterminado de función o método, no usar espacios. No anteponer guiones bajos
a los miembros privados de las clases.

```php
class MyClass {

}

function myFunction($default=null) {

}

$myVariable = 'blue';

$someArray = array(
    'foo'  => 'bar',
    'spam' => 'ham',
);

?>
```

### Operadores

Usar **===** y **!==** en lugar de **==** y **!=**.

Este es el motivo:

```php
<?php

var_dump(0 == "a"); // 0 == 0 -> true
var_dump("1" == "01"); // 1 == 1 -> true
var_dump("10" == "1e1"); // 10 == 10 -> true
var_dump(100 == "1e2"); // 100 == 100 -> true

?>
```

### Estructuras de control

- Usar siempre { } en los *if* de una sola línea
- Dividir los *if* largos en varias líneas
- Usar siempre break en las sentencias switch y prevenir con advertencias un bloque default si no se debe acceder a él

```php
<?php

// single line if
if ($myVar === 'hi') {
    $myVar = 'ho';
} else {
    $myVar = 'bye';
}

// long ifs
if (   $something === 'something'
    || $condition2
    && $condition3
) {
  // your code
}

// for loop
for ($i = 0; $i < 4; $i++) {
    // your code
}

switch ($condition) {
    case 1:
        // action1
        break;

    case 2:
        // action2;
        break;

    default:
        // defaultaction;
        break;
}

?>
```

### Pruebas unitarias

Las pruebas unitarias siempre deben extender la clase `\Test\TestCase`, que se encarga
de limpiar la instalación después de la prueba.

Si una prueba se ejecuta con varios valores distintos, debe usarse un proveedor de datos.
El nombre del método del proveedor de datos no debe empezar por `test` y debe terminar
en `Data`.

```php
<?php
namespace Test;
class Dummy extends \Test\TestCase {
    public function dummyData() {
        return array(
            array(1, true),
            array(2, false),
        );
    }

    /**
     * @dataProvider dummyData
     */
    public function testDummy($input, $expected) {
        $this->assertEquals($expected, \Dummy::method($input));
    }
}
```
````
