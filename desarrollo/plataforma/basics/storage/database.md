---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo consultar la base de datos desde una app: IDBConnection, transacciones, mappers y entidades, consejos para las tablas y compatibilidad entre motores."
---
(nc-dev-database)=
# Acceso a la base de datos

## Resumen

Esta página muestra cómo una app ejecuta consultas con `IDBConnection` y transacciones, cómo organizar el acceso con clases mapper y entidades (tipos, atributos, asignación de columnas), y qué consejos y restricciones aplicar a las tablas para que funcionen en todas las bases de datos compatibles. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/storage/database.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La forma básica de ejecutar una consulta a la base de datos es usar la conexión a la base de datos que proporciona **OCP\IDBConnection**.

Dentro de la clase de la capa de base de datos ya se pueden empezar a ejecutar consultas como la siguiente:

**Archivo {file}`lib/Db/AuthorDAO.php`**:

```php
<?php

namespace OCA\MyApp\Db;

use OCP\DB\QueryBuilder\IQueryBuilder;
use OCP\IDBConnection;

class AuthorDAO {

    private $db;

    public function __construct(IDBConnection $db) {
        $this->db = $db;
    }

    public function find(int $id) {
        $qb = $this->db->getQueryBuilder();

        $qb->select('*')
           ->from('myapp_authors')
           ->where(
               $qb->expr()->eq('id', $qb->createNamedParameter($id, IQueryBuilder::PARAM_INT))
           );

        $result = $qb->executeQuery();
        $row = $result->fetchAssociative();
        $result->closeCursor();

        return $row;
    }

}
```

### Transacciones

Las operaciones de base de datos se pueden ejecutar en una transacción para confirmar o revertir un grupo de cambios de forma atómica.

```php
<?php

$this->db->beginTransaction();

try {
    // DB operations

    $this->db->commit();
} catch (\Throwable $e) {
    // Optional: handle the error

    // Important: roll back (or commit) your changes when an error
    //            happens, so this transaction ends
    $this->db->rollBack();

    throw $e;
}
```

:::{warning}
Omitir el manejo de errores en las transacciones provoca un comportamiento inesperado, ya que todas las operaciones de base de datos que vengan después del error se seguirán ejecutando dentro de la transacción y, al faltar un commit, PDO revertirá automáticamente todos los cambios al final del script.
:::

En el contexto de una clase se puede usar el trait `TTransactional` y mover la unidad de trabajo a un closure.

```php
<?php

use OCP\AppFramework\Db\TTransactional;
use OCP\IDBConnection;

class MyService() {

    use TTransactional;

    private IDBConnection $db;

    public function __construct(IDBConnection $db) {
        $this->db = $db;
    }

    public function doSomeWork(): void {
        $this->atomic(function () {
            // $this->db->...
            // $this->db->...
            // $this->db->...
        }, $this->db);
    }

    /**
     * It's also possible to get a result out of the closure
     */
    public function doSomeWorkWithResults(): int {
        return $this->atomic(function () {
            // $this->db->...
            // $this->db->...
            // $this->db->...

            return 1;
        }, $this->db);
    }
}
```

### Mappers

El ejemplo anterior es la forma más básica de escribir una consulta simple a la base de datos, pero cuantas más consultas se acumulan, más código hay que escribir y más difícil se vuelve mantenerlo.

Para generalizar y simplificar el problema, dividir el código en recursos y crear para cada uno una clase **Entity** y una clase **Mapper**. La clase mapper proporciona una forma de ejecutar consultas SQL y asigna el resultado a las entidades relacionadas.

Para crear un mapper, heredar de la clase base del mapper y llamar al constructor padre con los parámetros siguientes:

- Conexión a la base de datos
- Nombre de la tabla
- **Opcional**: nombre de la clase de la entidad; de forma predeterminada, \OCA\MyApp\Db\Author en el ejemplo siguiente

**Archivo {file}`lib/Db/AuthorMapper.php`**:

```php
<?php

namespace OCA\MyApp\Db;

use OCP\DB\QueryBuilder\IQueryBuilder;
use OCP\IDBConnection;
use OCP\AppFramework\Db\QBMapper;

class AuthorMapper extends QBMapper {

    public function __construct(IDBConnection $db) {
        parent::__construct($db, 'myapp_authors');
    }


    /**
     * @throws \OCP\AppFramework\Db\DoesNotExistException if not found
     * @throws \OCP\AppFramework\Db\MultipleObjectsReturnedException if more than one result
     */
    public function find(int $id) {
        $qb = $this->db->getQueryBuilder();

        $qb->select('*')
           ->from('myapp_authors')
           ->where(
               $qb->expr()->eq('id', $qb->createNamedParameter($id, IQueryBuilder::PARAM_INT))
           );

        return $this->findEntity($qb);
    }


    public function findAll($limit=null, $offset=null) {
        $qb = $this->db->getQueryBuilder();

        $qb->select('*')
           ->from('myapp_authors')
           ->setMaxResults($limit)
           ->setFirstResult($offset);

        return $this->findEntities($qb);
    }


    public function authorNameCount($name) {
        $qb = $this->db->getQueryBuilder();

        $qb->select($qb->func()->count('*', 'count'))
           ->from('myapp_authors')
           ->where(
               $qb->expr()->eq('name', $qb->createNamedParameter($name, IQueryBuilder::PARAM_STR))
           );

        $result = $qb->executeQuery();
        $row = $result->fetchAssociative();
        $result->closeCursor();

        return $row['count'];
    }

}
```

:::{note}
El cursor se cierra automáticamente en todas las consultas **INSERT**, **DELETE** y **UPDATE** y al llamar a los métodos **findOneQuery**, **findEntities**, **findEntity**, **delete**, **insert** y **update**. En las llamadas personalizadas que usan execute, siempre hay que cerrar el cursor al terminar de obtener los resultados, para evitar problemas de bloqueo de la base de datos en SQLite.
:::

Cada mapper implementa también métodos predeterminados para eliminar y actualizar una entidad según su id:

```
$authorMapper->delete($entity);
```

o:

```
$authorMapper->update($entity);
```

### Entidades

Las entidades son objetos de datos que contienen toda la información de la tabla para una fila. Toda Entity tiene de forma predeterminada un campo **id** cuyo tipo es entero. Las filas de la tabla se asignan desde nombres en minúsculas separados por guiones bajos a atributos en *lowerCamelCase*:

- **Nombre de la columna de la tabla**: phone_number
- **Nombre de la propiedad**: phoneNumber

**Archivo {file}`lib/Db/Author.php`**:

```php
<?php

namespace OCA\MyApp\Db;

use OCP\AppFramework\Db\Entity;
use OCP\DB\Types;

class Author extends Entity {

    protected $stars;
    protected $name;
    protected $phoneNumber;

    public function __construct() {
        // add types in constructor
        $this->addType('stars', Types::INTEGER);
        // other fields are implicitly `Types::STRING`
    }
}
```

#### Tipos

Las propiedades siguientes deben anotarse con tipos, no solo para asegurar que los tipos se conviertan correctamente al almacenarlas en la base de datos (p. ej., PHP convierte false en la cadena vacía, lo que falla en PostgreSQL), sino también para convertirlas cuando se recuperan de la base de datos.

Se pueden agregar los siguientes tipos (que forman parte de `OCP\DB\Types`) a un campo:

- `Types::INTEGER`
- `Types::FLOAT`
- `Types::BOOLEAN`
- `Types::STRING` - Para columnas de texto y de cadena
- `Types::BLOB` - Para datos binarios
- `Types::JSON` - Los datos JSON se decodifican automáticamente al leerlos
- Para horas y/o fechas, proporcionadas como objetos `\DateTimeImmutable`, se pueden usar los tipos siguientes:

  - `Types::DATE_IMMUTABLE` - solo se almacena la fecha (sin zona horaria)
  - `Types::TIME_IMMUTABLE` - solo se almacena la hora (sin zona horaria)
  - `Types::DATETIME_IMMUTABLE` - se almacenan la fecha y la hora, pero sin zona horaria
  - `Types::DATETIME_TZ_IMMUTABLE` - se almacenan la fecha y la hora con información de zona horaria

- `Types::DATE`, `Types::TIME`, `Types::DATETIME`, `Types::DATETIME_TZ` - similares a las variantes inmutables, pero se proporcionan como objetos `\DateTime`.
  Se recomienda usar las variantes inmutables, ya que el seguimiento del estado interno de la clase `Entity` solo funciona con reasignaciones,
  por lo que los cambios en estos tipos mutables no se registran y el método update no escribe los cambios de vuelta en la base de datos.

(nc-dev-database-entity-attribute-access)=
#### Acceso a los atributos

Como todos los atributos deben ser protected, los getters y setters se generan automáticamente:

```php
:caption: lib/Db/Author.php

<?php

namespace OCA\MyApp\Db;

use OCP\AppFramework\Db\Entity;

class Author extends Entity {
    protected $stars;
    protected $name;
    protected $phoneNumber;
}

$author = new Author();
$author->setId(3);
$author->getPhoneNumber()  // null
```

#### Asignación personalizada de atributos a columnas de la base de datos

De forma predeterminada, cada atributo se asigna a una columna de la base de datos según una convención determinada; p. ej., **phoneNumber** se asigna a la columna **phone_number** y viceversa. Sin embargo, a veces es necesario asignar atributos a columnas distintas por compatibilidad con versiones anteriores. Para definir una asignación personalizada, basta con sobrescribir los métodos **columnToProperty** y **propertyToColumn** de la entidad en cuestión:

**Archivo {file}`lib/Db/Author.php`**:

```php
<?php

namespace OCA\MyApp\Db;

use OCP\AppFramework\Db\Entity;

class Author extends Entity {
    protected $stars;
    protected $name;
    protected $phoneNumber;

    // map attribute phoneNumber to the database column phonenumber
    public function columnToProperty($column) {
        if ($column === 'phonenumber') {
            return 'phoneNumber';
        } else {
            return parent::columnToProperty($column);
        }
    }

    public function propertyToColumn($property) {
        if ($property === 'phoneNumber') {
            return 'phonenumber';
        } else {
            return parent::propertyToColumn($property);
        }
    }

}
```

(nc-dev-database-entity-slugs)=
#### Atributos transitorios

Se pueden agregar a una clase de entidad atributos que no se asignan a ninguna columna de la base de datos. Se llaman *transitorios* porque ni se cargan desde las filas de la base de datos ni se persisten sus valores.

**Archivo {file}`lib/Db/User.php`**:

```php
<?php

namespace OCA\MyApp\Db;

use OCP\AppFramework\Db\Entity;

class User extends Entity {
    protected string $uid;       // Exists in the database
    protected $lastLogin; // Does not exist in the database

    public function getLastLogin(): ?int {
        return $this->lastLogin;
    }

    public function setLastLogin(int $lastLogin): void {
        $this->lastLogin = $lastLogin;
    }
}
```

Es importante definir getters y setters para todos los atributos transitorios.
No usar los {nc-ref}`getters y setters mágicos <database-entity-attribute-access>` de los atributos que se asignan a columnas de la base de datos.

#### Slugs

:::{deprecated} 24
:::

Los slugs se usan para identificar recursos en la URL mediante una cadena en lugar de un id entero.
Como la URL solo admite ciertos valores, la clase base de la entidad proporciona un método slugify para ello:

```php
<?php
$author = new Author();
$author->setName('Some*thing');
$author->slugify('name');  // Some-thing
```

### Consejos para la gestión de tablas

Conviene aplicar algunos consejos generales desde el principio, para no tener que migrar los datos y el esquema más adelante.

1. No usar nombres de tabla de más de 23 caracteres. Oracle está limitado a 30 caracteres y se necesitan 3 más para `oc_` al principio y 5 para el sufijo de la clave primaria `_pkey`.

2. Agregar una columna `id` autoincremental. Esto facilita el uso del enfoque `QBMapper` + `Entity`:

   - <https://github.com/nextcloud/server/blob/master/lib/public/AppFramework/Db/QBMapper.php>
   - <https://github.com/nextcloud/server/blob/master/lib/public/AppFramework/Db/Entity.php>

```php
<?php
$table->addColumn('id', Types::BIGINT, [
    'autoincrement' => true,
    'notnull' => true,
    'length' => 20,
    'unsigned' => true,
]);
```

3. Establecer una clave primaria para evitar errores en configuraciones en clúster. Para ello se puede usar el campo *id*.

```php
<?php
$table->setPrimaryKey(['id']);
```

4. Establecer manualmente el nombre de los índices. Esto ayuda a manipularlos en el futuro si hace falta. Hay que tener en cuenta que, en algunas plataformas de base de datos, los nombres de los índices son «globales» en toda la base de datos, por lo que usar nombres genéricos puede crear conflictos. Desde Nextcloud 28, la unicidad en todas las tablas se garantiza durante la instalación y durante las actualizaciones. Esto ocurre *independientemente de la plataforma de base de datos en uso* para mantener una amplia compatibilidad y coherencia.

```php
<?php
$table->addUniqueIndex(['your', 'column', 'names', '...'], 'table_name_uniq_feature');
```

### Consultar el proveedor de base de datos

Para averiguar en qué base de datos se ejecuta la app, usar el método `IDBConnection::getDatabaseProvider`.
Esto puede ser útil en los casos en que determinadas bases de datos tienen sus propios
requisitos, como Oracle, que limita las consultas `IN` a 1000 expresiones.

### Compatibilidad con más bases de datos

La mayoría de las consultas deberían funcionar bien en todas las bases de datos compatibles, pero si se requiere escalar y una base de datos se divide en un clúster, y para algunos tipos especiales de bases de datos, se aplican más reglas.
Las bases de datos compatibles de la app se pueden especificar en su `appinfo/info.xml`, en la sección de dependencias:

```xml
<database>pgsql</database>
<database>sqlite</database>
<database>mysql</database>
```

Cuando se admite Oracle (`oci`) (también cuando no se lista ninguna base de datos), Nextcloud realiza algunas pruebas adicionales sobre el esquema, que en ese caso se aplican a las bases de datos:

- Los nombres de tabla no pueden tener más de 27 caracteres (incluido el prefijo `oc_`)
- Las claves primarias deben tener un nombre de índice personalizado cuando el nombre de la tabla tiene más de 23 caracteres
- Los nombres de columna no pueden tener más de 30 caracteres
- Los nombres de índice no pueden tener más de 30 caracteres
- Los nombres de clave foránea no pueden tener más de 30 caracteres
- Los nombres de secuencia no pueden tener más de 30 caracteres
- Las columnas de cadena no pueden ser NotNull y tener una cadena vacía como valor predeterminado cuando se agregan en una migración posterior
- Las columnas de cadena no pueden tener una longitud de más de 4.000 caracteres; en su lugar, usar text
- Las columnas booleanas no pueden ser NotNull

Además, se asume que la compatibilidad con Oracle significa que interesa escalar y, por lo tanto, se comprueban restricciones adicionales de otras bases de datos en configuraciones en clúster:

- Galera Cluster: todas las tablas deben tener una clave primaria

Por otra parte, hay algunas configuraciones que influyen en las consultas que se pueden ejecutar. Los problemas conocidos son:

- MySQL al eliminar muchas entradas - Usar un `LIMIT` en el delete (no compatible con otras bases de datos); ver este [ejemplo de la app activity](https://github.com/nextcloud/activity/blob/master/lib/Data.php#L385-L397)
- MySQL `ONLY_FULL_GROUP_BY` - Todos los valores seleccionados en una consulta con `GROUP BY` deben agregarse, según el [manual de MySQL](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_only_full_group_by)
````
