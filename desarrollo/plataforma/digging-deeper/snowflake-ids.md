---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Los ID Snowflake de Nextcloud: qué información contienen, cómo almacenarlos en la base de datos, generarlos y decodificarlos con occ o desde el código."
---
(nc-dev-snowflake_ids)=
# ID Snowflake

## Resumen

Esta página explica la versión personalizada de los ID Snowflake que integra Nextcloud desde la versión 33: qué información contienen, cómo almacenarlos como clave primaria en la base de datos, cómo generarlos y cómo decodificarlos con `occ snowflake:decode` o desde el código. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/snowflake_ids.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 33
:::

Nextcloud integra una versión personalizada de los ID Snowflake (<https://en.wikipedia.org/wiki/Snowflake_ID>).

- Permite generar ID únicos por adelantado y además contiene información sobre su creación:
  - el momento de creación, con precisión de milisegundos
  - el identificador del servidor que creó el ID. Normalmente es un hash del nombre de host del servidor, o un valor aleatorio si no se encuentra ningún nombre de host.
  - si el ID se creó desde la CLI o no

### Almacenar un ID Snowflake en la base de datos

Los ID Snowflake están diseñados para usarse como clave primaria en la base de datos.
Deben almacenarse como `UNSIGNED BIGINT` (entero de 64 bits, siempre positivo)

En las migraciones de Nextcloud tiene este aspecto:

```php
public function changeSchema(IOutput $output, Closure $schemaClosure, array $options): ?ISchemaWrapper {
    /** @var ISchemaWrapper $schema */
    $schema = $schemaClosure();

    if (!$schema->hasTable('my_table')) {
        $table = $schema->createTable('my_table');
        $table->addColumn(
            'id',
            Types::BIGINT,
            ['notnull' => true, 'unsigned' => true]
        );
        $table->setPrimaryKey(['id']);

        // TODO Add other fields
    }
```

### Generar un ID Snowflake

Para generar un ID nuevo, llamar a la función `nextId` del generador:

```php
<?php
declare(strict_types=1);

namespace OCA\MyApp;

use OCP\Snowflake\IGenerator;

class MyObjectFactory {
    public function __construct(
            private readonly IGenerator $generator,
    ) {
      // TODO Add your implementation
    }

    public function create(): MyObject {
        /** @var string $id */
        $id = $this->generator->nextId();

        // TODO Create other properties and insert into database
    }
}
```

### Decodificar un ID Snowflake

Usar el comando `occ snowflake:decode` para inspeccionar un ID Snowflake desde la
línea de comandos:

```
sudo -E -u www-data php occ snowflake:decode 6768789079123765868
+--------------------+-------------------------+
| Snowflake ID       | 6768789079123765868     |
| Seconds            | 1575981518              |
| Milliseconds       | 50                      |
| Created from CLI   | no                      |
| Server ID          | 441                     |
| Sequence ID        | 12                      |
| Creation timestamp | 1575981518.050          |
| Creation date      | 2019-12-10 13:38:38.050 |
+--------------------+-------------------------+
```

También es posible decodificar los ID en el código, por ejemplo para obtener el momento de creación del objeto:

```php
<?php
declare(strict_types=1);

namespace OCA\MyApp;

use DateTimeImmutable;
use OCP\Snowflake\IDecoder;

class MyObject {
    private string $id;

    public function __construct(
            private readonly IDecoder $decoder,
    ) {
      // TODO Add your implementation
    }

    public function createdAt(): DateTimeImmutable {
        return $this->decoder->decode($this->id)['createdAt'];
    }
}
```
````
