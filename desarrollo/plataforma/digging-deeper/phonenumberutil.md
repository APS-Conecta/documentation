---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Uso de la utilidad IPhoneNumberUtil de OCP: convertir números de teléfono al formato E164 y obtener el código de país de una región."
---
(nc-dev-phonenumberutil)=
# Utilidad de números de teléfono

## Resumen

Esta página describe `OCP\IPhoneNumberUtil`, un envoltorio de la biblioteca libphonenumber: cómo convertir un número de teléfono al formato estándar E164 y cómo obtener el código de país de una región, con ejemplos de su salida. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/phonenumberutil.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
`OCP\IPhoneNumberUtil` es un envoltorio de la biblioteca de terceros [libphonenumber](https://github.com/giggsey/libphonenumber-for-php).
Está simplificado a los casos de uso más comunes para permitir reemplazar la biblioteca en el futuro sin tener que romper la
API pública ni la funcionalidad.

### Convertir la entrada al formato estándar

Para convertir un número de teléfono al formato E164, llamar a `convertToStandardFormat()` con una región conocida. La entrada también puede
contener caracteres de formato, como espacios, barras y guiones:

```php
$input = '044 / 668-1800';
$util = \OCP\Server::get(\OCP\IPhoneNumberUtil::class);
var_dump($util->convertToStandardFormat($input, 'CH'));
// Will output:
// string(12) "+41446681800"
```

Si no se indica ninguna región y el número de teléfono no puede asignarse a una única región, la conversión fallará:

```php
$input = '044 668 1800';
$util = \OCP\Server::get(\OCP\IPhoneNumberUtil::class);
var_dump($util->convertToStandardFormat($input, null));
// Will output:
// NULL
```

El número de teléfono también puede proporcionarse en un formato internacional que contenga el código de región. En este caso, la región predeterminada se ignora:

```php
$input = '+41 44 668 1800';
$util = \OCP\Server::get(\OCP\IPhoneNumberUtil::class);
var_dump($util->convertToStandardFormat($input, null));
var_dump($util->convertToStandardFormat($input, 'DE'));
// Both will output:
// string(12) "+41446681800"
```

### Obtener el código de país de una región

Para comprobar si una región proporcionada es válida (código de 2 letras de `ISO 3166-1`) y tiene un código de país, usar `getCountryCodeForRegion()`:

```php
$util = \OCP\Server::get(\OCP\IPhoneNumberUtil::class);
var_dump($util->getCountryCodeForRegion('DE'));
// Will output:
// int(49)
```

De nuevo, se usa `null` para indicar una entrada no válida:

```php
$util = \OCP\Server::get(\OCP\IPhoneNumberUtil::class);
var_dump($util->getCountryCodeForRegion('Germany'));
// Will output:
// NULL
```
````
