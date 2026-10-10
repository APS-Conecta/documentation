---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "La interfaz ITimeFactory de OCP, que envuelve funciones de tiempo de uso común para facilitar las pruebas, y los métodos que agrega a ClockInterface."
---
# Trabajar con el tiempo

## Resumen

Esta página describe `\OCP\AppFramework\Utility\ITimeFactory`, que envuelve funciones de tiempo de uso común para facilitar las pruebas, y los métodos que agrega a `\PSR\Clock\ClockInterface`. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/time.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Se puede inyectar `\OCP\AppFramework\Utility\ITimeFactory`, que envuelve funciones de tiempo de uso común para facilitar las pruebas.

### Métodos

La factoría extiende `\PSR\Clock\ClockInterface` con los siguientes métodos:

```php
<?php

/**
 * @return int the result of a call to time()
 * @since 8.0.0
 */
public function getTime(): int;

/**
 * @param string $time
 * @param \DateTimeZone|null $timezone
 * @return \DateTime
 * @since 15.0.0
 */
public function getDateTime(string $time = 'now', \DateTimeZone $timezone = null): \DateTime;

/**
 * @param \DateTimeZone $timezone
 * @return static
 * @since 26.0.0
 */
public function withTimeZone(\DateTimeZone $timezone): static;

/**
 * @param string|null $timezone
 * @return \DateTimeZone Requested timezone if provided, UTC otherwise
 * @throws \Exception
 * @since 29.0.0
 */
public function getTimeZone(?string $timezone = null): \DateTimeZone;
```
````
