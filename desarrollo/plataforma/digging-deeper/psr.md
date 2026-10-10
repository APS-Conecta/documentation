---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Las recomendaciones de estándares PHP (PSR) que implementa Nextcloud: carga automática, logger, contenedor y reloj, con sus versiones."
---
(nc-dev-psr)=
# PSR

## Resumen

Esta página reúne las recomendaciones de estándares PHP (PSR) implementadas en Nextcloud —PSR-0, PSR-3, PSR-4, PSR-11 y PSR-20— y la versión de cada una que se incluye según la versión de Nextcloud. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/psr.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
En esta página se encuentra información sobre las [recomendaciones de estándares PHP](https://www.php-fig.org/psr/) implementadas en Nextcloud.

(nc-dev-psr0)=
### PSR-0: Carga automática

Este estándar está obsoleto y se eliminará en Nextcloud 27. Ver la {nc-ref}`sección de PSR-4 <psr4>` en su lugar.

(nc-dev-psr3)=
### PSR-3: Interfaz de logger

:::{versionadded} 19
:::

El contenedor de inyección de dependencias puede inyectar una instancia de `\Psr\Log\LoggerInterface`.
La implementación de [PSR-3][PSR-3] pretende facilitar la integración de bibliotecas de terceros que requieren el logger de [PSR-3][PSR-3].

:::{versionchanged} 21
Nextcloud incluye la versión 1.1.3
:::

:::{versionchanged} 23
Nextcloud incluye la versión 1.1.4
:::

:::{versionchanged} 30
Nextcloud incluye la versión 2.0.0
:::

:::{versionchanged} 31
`\Psr\Log\LoggerInterface` sustituyó por completo a los métodos de registro internos de Nextcloud.
:::

(nc-dev-psr4)=
### PSR-4: Carga automática

El estándar *PSR-4* describe cómo deben nombrarse los archivos de clase para que Nextcloud pueda cargarlos automáticamente. Ver la {nc-ref}`documentación del cargador de clases <appclassloader>` para más detalles.

(nc-dev-psr11)=
### PSR-11: Interfaz de contenedor

:::{versionadded} 20
:::

El contenedor de inyección de dependencias sigue la interfaz de contenedor de [PSR-11][PSR-11], por lo que se puede declarar el tipo `\Psr\Container\ContainerInterface` siempre que se quiera una instancia de un contenedor, y usar `has($id)` para comprobar si existe y `get($id)` para obtener una instancia de un servicio. Ver la {nc-ref}`documentación de inyección de dependencias <dependency-injection>` para más detalles.

:::{versionchanged} 22
Nextcloud incluye la versión 1.1.1
:::

:::{versionchanged} 27
Nextcloud incluye la versión 2.0.2
:::

(nc-dev-psr20)=
### PSR-20: Reloj

:::{versionadded} 27
:::

La clase `\OCP\AppFramework\Utility\ITimeFactory` sigue la interfaz de reloj de [PSR-20][PSR-20], por lo que se puede declarar el tipo `\PSR\Clock\ClockInterface` y luego usar el método `now()` siempre que se quiera obtener la hora actual. También se puede cambiar la zona horaria de la instancia `\DateTimeImmutable` que se va a devolver, obteniendo un nuevo `ITimeFactory` mediante `ITimeFactory::withTimeZone()`.

[PSR-0]: https://www.php-fig.org/psr/psr-0/
[PSR-3]: https://www.php-fig.org/psr/psr-3/
[PSR-4]: https://www.php-fig.org/psr/psr-4/
[PSR-11]: https://www.php-fig.org/psr/psr-11/
[PSR-20]: https://www.php-fig.org/psr/psr-20/
````
