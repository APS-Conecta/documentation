---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo hacer traducible una app en PHP, plantillas, JavaScript y ExApps, y pautas para escribir cadenas, plurales y pistas para quienes traducen."
---
(nc-dev-translations)=
# Traducciones

## Resumen

Esta página explica cómo hacer traducible una app con los métodos de traducción del backend PHP, de las plantillas PHP, de JavaScript, TypeScript y Vue, y de las ExApps en Python, y reúne pautas para escribir cadenas fáciles de traducir: plurales, marcadores de posición y pistas de contexto. También cubre cómo probar las traducciones y el comando `l10n:createjs`. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/translations.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud ofrece mecanismos de internacionalización (hacer que una aplicación sea traducible) y de localización (agregar traducciones para idiomas concretos). Esta sección ofrece instrucciones detalladas para ambos aspectos.
Para que la app sea traducible (internacionalización), conviene usar los métodos de Nextcloud para traducir cadenas. Están disponibles tanto para el lado del servidor (PHP, plantillas) como para el lado del cliente (JavaScript).

### Backend en PHP

Si se usan cadenas localizadas en el código del backend, basta con inyectar la clase `\OCP\IL10N` en el servicio declarando su tipo en el constructor. Se obtendrá automáticamente el objeto de idioma que contiene las traducciones de la app:

```php
<?php
class AuthorService {
    public function __construct(
        private \OCP\IL10N $l,
    ) {
    }

    …
}
```

Luego, las cadenas se pueden traducir de la siguiente manera:

```php
<?php
class AuthorService {

    …

    public function getLanguageCode() {
        // Get the language code of the current language
        return $this->l->getLanguageCode();
    }

    public sayHello() {
        // Simple string
        return $this->l->t('Hello');
    }

    public function getAuthorName($name) {
        // String using a parameter
        return $this->l->t('Getting author %1$s', [$name]);
    }

    public function getAuthors($count, $city) {
        // Translation with plural
        return $this->l->n(
            '%n author is currently in the city %1$s', // singular string
            '%n authors are currently in the city %1$s', // plural string
            $count, // number to decide which plural to use
            [$city] // further parameters are possible
        );
    }
}
```

#### Idioma de otros usuarios

Si hace falta obtener el idioma de otro usuario, p. ej., para enviarle un correo electrónico o dentro de un trabajo en segundo plano, también hay que tener en cuenta
las opciones de configuración `force_language` y `default_language`. Para facilitarlo, la clase
`OCP\L10N\IFactory` incluye un método `getUserLanguage`:

```php
<?php
class SendEmail {
    public function __construct(
        private \OCP\L10N\IFactory $l10nFactory,
     ) {
    }

    public function send(IUser $user): void {
        $lang = $this->l10nFactory->getUserLanguage($user);
        $l = $this->l10nFactory->get('myapp', $lang);

        // …
    }
```

### Plantillas PHP

En todas las plantillas se puede usar la variable global `$l` para traducir las cadenas con sus métodos `t()` y `n()`:

```php
// Simple text string
<button><?php p($l->t('Hide')); ?></button>

// Text with a placeholder
<div><?php p($l->t('Show files of %1$s', [$user])); ?></div>

// Date string
<em><?php p($l->l('date', time())); ?></em>
```

### JavaScript / TypeScript / Vue

Hay funciones globales `t()` y `n()` disponibles para traducir cadenas en el código JavaScript.
Si la app se compila, se pueden importar las funciones de traducción desde el [paquete @nextcloud/l10n](https://github.com/nextcloud-libraries/nextcloud-l10n).
Su uso difiere un poco del de PHP:

* El primer argumento es el appId, p. ej., `'myapp'`
* Los marcadores de posición (salvo el número en los plurales) usan llaves simples con descriptores significativos.
* La lista de parámetros es un objeto con los descriptores como claves.

```js
t('myapp', 'Hello World!');
t('myapp', '{name} is available. Get {linkstart}more information{linkend}', {name: 'Nextcloud 16', linkstart: '<a href="...">', linkend: '</a>'});
n('myapp', 'Import %n calendar into {collection}', 'Import %n calendars into {collection}', selectionLength, {collection: 'Nextcloud'});
```

### ExApps (Python)

En las ExApps, Python actualmente solo se admite para las traducciones automatizadas de Transifex.

Junto a los archivos habituales `l10n/*.json` y `l10n/*.js`, también se incluyen en la sincronización con Transifex los archivos fuente de traducción ubicados en `translationfiles/<lang>/*.po`.
Estos archivos `.po` se pueden compilar en archivos `.mo`, que el backend de la ExApp suele usar para las traducciones en tiempo de ejecución.

Para más detalles, ver {nc-ref}`ex_app_translations_page`.

### Pautas

Conviene revisar también las siguientes indicaciones para mejorar las cadenas y hacer que la comunidad pueda traducirlas mejor,
lo que mejora la experiencia de quienes no usan el inglés.

#### Qué hacer y qué no hacer

:::{list-table}
:header-rows: 1

* - Mal
  - Bien
  - Descripción
* - `´` o `’`
  - `'`
  - Usar la comilla simple ASCII
* - `Loading...`
  - `Loading …`
  - Usar el carácter **Unicode de puntos suspensivos**.\
    Agregar un **espacio de no separación** antes de los puntos suspensivos cuando se recorta una oración en lugar de una palabra.
* - `Loading …`\
    (un espacio normal `U+0020`)
  - `Loading …`\
    (un espacio de no separación `U+00A0`)
  - Usar solo un **espacio de no separación** antes de los puntos suspensivos (`U+00A0`).
* - «Don't»
  - «Do not»
  - Usar la forma completa es más fácil de entender y facilita la traducción.
* - «Won't»
  - «Will not»
  - Usar la forma completa es más fácil de entender y facilita la traducción.
* - «Can not»
  - «Cannot»
  - Usar la forma unida es más fácil de entender y facilita la traducción.
* - id
  - ID
  - Todo en mayúsculas para abreviar «identifier»
* - Users
  - Accounts / People
  - Usar **accounts** al referirse a un perfil o entidad. Usar **people** al referirse a seres humanos.
* - Admin / Administrator
  - Administration
  - Referirse a la administración como una entidad organizativa no humana\
    en lugar de a una o varias personas.
* - Headline
  - Headline:
  - Incluir los dos puntos `:` en las traducciones, ya que algunos idiomas agregan un espacio antes de los dos puntos.
* - " Leading space"\
    "Trailing space "
  - "No leading space"\
    "No trailing space"
  - Los espacios al principio o al final suelen indicar que las cadenas se concatenan.\
    A quienes traducen les suele resultar útil tener todo el contenido en una sola traducción,\
    ya que, de lo contrario, el orden y las referencias entre palabras y oraciones podrían perderse.
* - "Error:" $error
  - "Error: %s"
  - En lugar de concatenar errores o fragmentos de mensajes, convertirlos en un marcador de posición adecuado
:::

#### Plurales correctos

Si se usa un plural, también se **debe** usar el marcador de posición `%n`. El marcador de posición define el plural, y la palabra sin el número delante es incorrecta. Si no se conoce o no se tiene un número para la traducción, p. ej., porque no se sabe cuántos elementos se van a seleccionar, basta con usar un plural indefinido. Existen en todos los idiomas y tienen una sola forma. No siguen el patrón normal del plural.

Ejemplo en PHP:

```php
// BAD: Plural without count
$title = $l->n('Import calendar', 'Import calendars', $selectionLength)
// BETTER: Plural has count, but disrupting to read and unnecessary information
$title = $l->n('Import %n calendar', 'Import %n calendars', $selectionLength)
// BEST: Simple string with undefined plural not using any number in the string
$title = $l->t('Import calendars')
```

A diferencia de los marcadores de posición normales de JavaScript, el número del plural también usa la sintaxis `%n`:

Ejemplo en JS:

```js
/* BAD: Plural without count */
n('myapp', 'Import calendar', 'Import calendars', selected.length)
/* BETTER: Plural has count, but disrupting to read and unnecessary information */
n('myapp', 'Import %n calendar', 'Import %n calendars', selected.length)
/* BEST: Simple string with undefined plural not using any number in the string */
t('myapp', 'Import calendars')
```

:::{important}
Regla general: siempre que una variable con valores variables (números) forme parte de una cadena, se debe usar la forma plural.
:::

Hay idiomas con varias formas de plural. Ver <https://en.wikipedia.org/wiki/Plural#Use_in_systems_of_grammatical_number>

Ejemplo

```php
"Vault will be locked in %1$d seconds"
```

Esto significa que, aunque el valor de ‘seconds’ siempre sea mayor que 1, quienes traducen en Transifex no pueden producir traducciones válidas en la forma plural para algunos idiomas.

Mal: solo se proporciona una cadena

```php
"Vault will be locked in %1$d seconds"
```

Bien: dos cadenas en el código fuente.

```php
"Vault will be locked in %1$d second"
"Vault will be locked in %1$d seconds"
```

(nc-dev-improving-translations)=
#### Mejorar las traducciones

Partiendo del siguiente ejemplo, se mejora paso a paso:

```php
<?php p($l->t('Select file from')) . ' '; ?><a href='#' id="browselink"><?php p($l->t('local filesystem'));?></a><?php p($l->t(' or ')); ?><a href='#' id="cloudlink"><?php p($l->t('cloud'));?></a>
```

##### Paso 1: dividir cadenas

¡**Nunca** se deben **dividir** oraciones ni **concatenar** dos traducciones (p. ej., «Habilitar» y «modo oscuro» no se pueden combinar en «Habilitar modo oscuro», porque los idiomas pueden necesitar usar casos gramaticales distintos)! Quienes traducen pierden el contexto y no tienen posibilidad de reordenar palabras o partes según haga falta.

Quienes traducen traducirán:

* `Select file from`
* `local filesystem`
* `or` (con espacio en blanco delante y detrás)
* `cloud`

Traducir estas cadenas por separado hace que `local filesystem` y `cloud` pierdan el caso gramatical. Los dos espacios en blanco que rodean `or` también se perderán al traducir. En los idiomas que tienen un orden gramatical distinto, impide a quienes traducen reordenar los componentes de la oración.

Así, el siguiente código es algo mejor, pero tiene otro problema:

```php
<?php p($l->t('Select file from <a href="#" id="browselink">local filesystem</a> or <a href="#" id="cloudlink">cloud</a>'));?>
```

##### Paso 2: marcado HTML

En este caso, quienes traducen pueden reordenar como quieran, pero tienen que lidiar con el marcado y pueden estropearlo fácilmente. Es mejor **mantener el marcado fuera** del código, así que la siguiente traducción es aún mejor:

```php
<?php p($l->t('Select file from %slocal filesystem%s or %scloud%s', ['<a href="#" id="browselink">', '</a>', '<a href="#" id="cloudlink">', '</a>']));?>
```

Pero esto todavía tiene un último problema.

##### Paso 3: marcadores de posición

Si el idioma tiene que invertir el orden, el código seguirá insertando los parámetros en el orden dado y quienes traducen no podrán reordenarlos. Para evitar este último obstáculo, basta con **usar marcadores de posición numerados** como `%1$s`:

```php
<?php p($l->t('Select file from %1$slocal filesystem%2$s or %3$scloud%4$s', ['<a href="#" id="browselink">', '</a>', '<a href="#" id="cloudlink">', '</a>']));?>
```

Esto permite a quienes traducen poner el cloudlink antes del browselink si el idioma es, p. ej., de derecha a izquierda.

(nc-dev-hints)=
#### Dar pistas de contexto a quienes traducen

Por si algunas cadenas de traducción pueden traducirse mal porque tienen varios significados.
Sobre todo las cadenas de traducción que contienen una sola palabra suelen dar problemas.
El ejemplo más conocido en el código de Nextcloud es `Share`, que puede ser el verbo y la acción `To share something` o el sustantivo `A share`.
Las pistas agregadas se mostrarán en la interfaz web de Transifex:

##### PHP

Colocar el comentario en la línea anterior a la llamada a `->t()` o `->n()`:

```php
// TRANSLATORS Will be shown inside a popup and asks the user to add a new file
p($l->t('Add new file'));

// TRANSLATORS The placeholder refers to the software product name, e.g. "Add to your Nextcloud"
$l->t('Add to your %s', [$productName]);
```

Para un contexto de varias líneas o un ejemplo de salida, usar líneas de comentario consecutivas:

```php
// TRANSLATORS
// Indicates when a calendar event will happen, shown on invitation emails.
// Output example: "In 1 hour on July 1, 2024 for the entire day"
$l->t('In %1$s on %2$s for the entire day', [$relativeTime, $date]);
```

##### JavaScript / TypeScript

Colocar el comentario en la línea anterior a la llamada a `t()` o `n()`:

```javascript
// TRANSLATORS: name that is appended to copied files, will be put in parenthesis with a number for the second+ copy
var copyNameLocalized = t('files', 'copy');

// TRANSLATORS: {relativeDueDate} will be replaced with a relative time, e.g. "2 hours ago" or "in 3 days"
t('files_reminders', 'We will remind you of this file {relativeDueDate}', { relativeDueDate })
```

##### Vue

En el bloque `<template>`, usar un comentario HTML en la línea anterior al elemento:

```html
<!-- TRANSLATORS: Making this question necessary to be answered when submitting to a form -->
<span>{{ t('forms', 'Required') }}</span>
```

En el bloque `<script>`, usar el mismo estilo `//` que en JavaScript.

##### C++ (Qt) / cliente de escritorio

```c++
//: Example text: "Progress of sync process. Shows the currently synced filename"
fileProgressString = tr("Syncing %1").arg(allFilenames);
```

##### Android

```xml
<!-- TRANSLATORS List of deck boards -->
<string name="simple_boards">Boards</string>
```

##### iOS

```swift
/* The title on the navigation bar of the Scanning screen. */
"wescan.scanning.title"             = "Scanning";
```

### Agregar traducciones

Los pasos para configurar las traducciones de una app se trasladaron a su propia página en el capítulo «Desarrollo de apps»: {nc-ref}`Translation`

### Probar las traducciones

Se puede usar el parámetro de consulta `forceLanguage` para forzar un idioma concreto en una solicitud web (API o frontend). Ver {nc-ref}`Forzar el idioma en una llamada concreta <api-force-language>`.

### Comandos de consola

#### l10n:createjs

Genera los archivos de traducción JavaScript de una app a partir de sus archivos fuente de `l10n/`.
Se pasa el ID de la app y, opcionalmente, un código de idioma concreto:

```
sudo -E -u www-data php occ l10n:createjs myapp
sudo -E -u www-data php occ l10n:createjs myapp de
```

Si no se indica ningún idioma, se generan archivos JavaScript para todos los idiomas
disponibles. Los archivos de salida se escriben en el directorio `l10n/` de la app
como `<lang>.js` y `<lang>.json`.

:::{note}
Este comando está pensado para el desarrollo y los pipelines de CI. En producción,
los archivos de traducción JavaScript se generan automáticamente durante la instalación
y las actualizaciones de las apps.
:::
````
