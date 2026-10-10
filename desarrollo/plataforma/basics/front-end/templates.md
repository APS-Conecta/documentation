---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo usar el sistema de plantillas PHP de las apps: imprimir valores sin XSS, incluir otras plantillas, CSS, JavaScript e imágenes."
---
# Plantillas

## Resumen

Esta página explica el sistema de plantillas de las apps: cómo acceder a los parámetros del controlador, imprimir valores de forma segura frente a XSS e incluir otras plantillas, CSS, JavaScript e imágenes. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/front-end/templates.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud ofrece su propio sistema de plantillas, que básicamente es PHP plano con algunas funciones adicionales y variables predefinidas. Todos los parámetros que se han pasado desde el {nc-doc}`controlador <developer_manual/basics/controllers>` están disponibles en un array llamado **$_[]**, p. ej.:

```
array('key' => 'something')
```

se puede acceder mediante:

```
$_['key']
```

:::{note}
Para prevenir XSS, las siguientes **funciones de PHP para imprimir están prohibidas: echo, print() y <?=**. En su lugar, se usa la función **p()** para imprimir los valores. Si se necesita imprimir sin escapar, hay que **revisar dos veces que no haya XSS** y usar: {code}`print_unescaped()`.
:::

Los valores se imprimen con la función {code}`p()`, y el HTML se imprime con {code}`print_unescaped()`.

{file}`templates/main.php`

```php
<?php foreach($_['entries'] as $entry){ ?>
  <p><?php p($entry); ?></p>
<?php
}
```

### Incluir plantillas

Las plantillas también pueden incluir otras plantillas mediante el método **$this->inc('templateName')**.

```php
<?php print_unescaped($this->inc('sub.inc')); ?>
```

Las variables de la plantilla padre también estarán disponibles en las plantillas incluidas, pero, si se necesita, también se le pueden pasar variables nuevas mediante el segundo parámetro opcional de **$this->inc**, en forma de array.

{file}`templates/sub.inc.php`

```php
<div>I am included, but I can still access the parents variables!</div>
<?php p($_['name']); ?>

<?php print_unescaped($this->inc('other_template', array('variable' => 'value'))); ?>
```

### Incluir CSS y JavaScript

:::{warning}
Esto está obsoleto; en su lugar, hay que usar `addScript` y `addStyle` en el controlador.
Consultar {nc-ref}`ApplicationJs` para más información.
:::

Para incluir CSS o JavaScript se usan las funciones **style** y **script**:

```php
<?php
script('myapp', 'script');  // add js/script.js
style('myapp', 'style');  // add css/style.css
```

### Incluir imágenes

Para generar enlaces a imágenes se usa la función **image_path**:

```php
<img src="<?php print_unescaped(image_path('myapp', 'app.png')); ?>" />
```
````
