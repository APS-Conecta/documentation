---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo cambiar el esquema de la base de datos de una app con migraciones: pasos, metadatos, comandos occ migrations y cómo agregar o reemplazar índices."
---
(nc-dev-app_db_migrations)=
# Migraciones

## Resumen

Esta página explica cómo una app cambia el esquema de su base de datos con migraciones: los pasos previos, de esquema y posteriores, la construcción de las clases de migración, sus atributos de metadatos, los comandos `occ migrations:*` y cómo agregar o reemplazar índices sin bloquear la actualización. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/storage/migrations.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Las migraciones cambian el esquema de la base de datos y funcionan en tres pasos:

- Cambios previos al esquema
- Cambios del esquema
- Cambios posteriores al esquema

Las apps pueden tener varias migraciones, lo que permite un proceso de actualización mucho más flexible.
Por ejemplo, se puede renombrar una columna copiando todo su contenido con 3 pasos
repartidos en 2 migraciones.

La lógica del actualizador de Nextcloud busca los archivos de migración
en la carpeta *lib/Migration* de la app.

:::{note}
Aunque en teoría se puede ejecutar cualquier código en los pasos previos y posteriores, se
recomienda no usar clases php reales. Con las migraciones se puede actualizar
de cualquier versión antigua a cualquier versión nueva siempre que se conserven
los pasos de migración. Como también se usan para la instalación, deben
conservarse de todos modos. Pero esto también significa que, si se cambia una clase php
que se usa en la migración, el código puede ejecutarse sobre estados distintos de la
base de datos, los archivos o el código cuando se ejecuta en una actualización.
:::

:::{note}
Como Nextcloud guarda qué migraciones ya se han ejecutado,
no se deben «actualizar» las migraciones. Se recomienda dejarlas
intactas el mayor tiempo posible. Solo deben ajustarse para asegurar
que sigan ejecutándose, pero los cambios adicionales en la base de datos deben hacerse
en una migración nueva.
:::

### 1. Migración 1: cambio de esquema

Con este paso se crea la columna nueva:

```php
public function changeSchema(IOutput $output, \Closure $schemaClosure, array $options) {
           /** @var ISchemaWrapper $schema */
           $schema = $schemaClosure();

           $table = $schema->getTable('twofactor_backupcodes');

           $table->addColumn('user_id', \OCP\DB\Types::STRING, [
                   'notnull' => true,
                   'length' => 64,
           ]);

           return $schema;
  }
```

### 2. Migración 1: cambio posterior al esquema

En este paso se copia el contenido de la columna antigua a la nueva.

:::{note}
Esto también podría hacerse en la segunda migración, como parte de
un cambio previo al esquema
:::

```php
public function postSchemaChange(IOutput $output, \Closure $schemaClosure, array $options) {
       $query = $this->db->getQueryBuilder();
       $query->update('twofactor_backupcodes')
               ->set('user_id', 'uid');
       $query->executeStatement();
}
```

### 3. Migración 2: cambio de esquema

Con esto se elimina la columna antigua.

```php
 public function changeSchema(IOutput $output, \Closure $schemaClosure, array $options) {
        /** @var ISchemaWrapper $schema */
        $schema = $schemaClosure();

        $table = $schema->getTable('twofactor_backupcodes');
        $table->dropColumn('uid');

        return $schema;
}
```

### Construcción de las clases de migración

Todas las clases de migración se construyen mediante {nc-ref}`dependency-injection`. Así que, si los pasos
de la migración necesitan dependencias adicionales, estas se pueden definir en el constructor de la
clase de migración.

**Ejemplo:** si la migración necesita ejecutar sentencias SQL, inyectar una instancia de *OCP\IDBConnection*
en la clase de migración así:

```php
class Version2404Date20220903071748 extends SimpleMigrationStep {
   public function __construct(
      private IDBConnection $db
   ) {
   }

   public function postSchemaChange(IOutput $output, \Closure $schemaClosure, array $options) {
      $query = $this->db->getQueryBuilder();
      // execute some SQL ...
   }
}
```

### Migraciones y metadatos

Desde la versión 30, los detalles de las migraciones están disponibles para los administradores, ya que se pueden adjuntar metadatos a la clase de migración agregando atributos PHP específicos:

```php
use OCP\Migration\Attributes\CreateTable;
use OCP\Migration\Attributes\ColumnType;
use OCP\Migration\Attributes\ModifyColumn;

#[CreateTable(
    table: 'new_table',
    description: 'Table is used to store things, but also to get more things',
    notes: ['this is a notice', 'and another one, if really needed']
)]
#[ModifyColumn(table: 'other_table', name: 'this_field', type: ColumnType::BIGINT)]
class Version30000Date20240729185117 extends SimpleMigrationStep {
    public function changeSchema(IOutput $output, Closure $schemaClosure, array $options) {
[...]
    }
}
```

Lista de los atributos de migración disponibles:

- `\OCP\Migration\Attributes\AddColumn` si la migración implica crear una columna nueva
- `\OCP\Migration\Attributes\AddIndex` si la migración agrega un índice nuevo
- `\OCP\Migration\Attributes\CreateTable` si la migración crea una tabla nueva
- `\OCP\Migration\Attributes\DropColumn` si la migración elimina una columna
- `\OCP\Migration\Attributes\DropIndex` si la migración elimina un índice
- `\OCP\Migration\Attributes\DropTable` si la migración elimina una tabla
- `\OCP\Migration\Attributes\ModifyColumn` si la migración modifica una columna

(nc-dev-migration_console_command)=
### Comandos de consola

Los siguientes comandos `occ` ayudan a crear y gestionar migraciones:

```
migrations
 migrations:execute  execute a single migration version manually
 migrations:generate generate a new migration file for an app
 migrations:migrate  execute migrations to a specified or the latest version
 migrations:preview  preview available DB migrations before an upgrade
 migrations:status   view the status of migrations for an app
```

#### migrations:execute

Ejecuta manualmente una sola versión de migración. El argumento `version` es el
nombre de la clase de migración sin el prefijo `Version`; por ejemplo, si la
migración se llama `Version2404Date20220903071748`, la versión es
`2404Date20220903071748`:

```
sudo -E -u www-data php occ migrations:execute myapp 2404Date20220903071748
```

:::{note}
Sin el modo de depuración activado, `migrations:execute` se niega a ejecutar una
versión que ya se haya ejecutado o que revertiría una migración anterior.
Activar el modo de depuración (`’debug’ => true` en `config.php`) para
saltarse esta restricción durante el desarrollo.
:::

#### migrations:generate

Genera un archivo de migración nuevo para una app. El argumento `version` es la
versión mayor de la app como número entero. Usar los dígitos mayor y menor de
la versión de la app, asignados a 3 dígitos (`1.0.x => 1000`, `2.34.x => 2034`),
para dejar espacio a migraciones de ramas paralelas:

```
sudo -E -u www-data php occ migrations:generate myapp 1000
```

El archivo generado se coloca en `apps/myapp/lib/Migration/`.

:::{note}
Después de generar una migración, puede ser necesario ejecutar `composer dump-autoload`
antes de poder ejecutarla.
:::

#### migrations:migrate

Ejecuta todas las migraciones pendientes de una app, o migra a una versión concreta.
Acepta un número de versión (`YYYYMMDDHHMMSS`) o un alias (`first`,
`prev`, `next`, `latest`):

```
sudo -E -u www-data php occ migrations:migrate myapp
sudo -E -u www-data php occ migrations:migrate myapp prev
```

#### migrations:preview

Muestra una vista previa de las migraciones de la base de datos que se aplicarían durante una actualización a una
versión dada, sin ejecutarlas:

```
sudo -E -u www-data php occ migrations:preview 30.0.0
```

#### migrations:status

Muestra qué migraciones de una app se han ejecutado y cuáles están pendientes:

```
sudo -E -u www-data php occ migrations:status myapp
```

### Agregar índices

Agregar índices a tablas existentes puede tardar mucho, sobre todo en tablas grandes. Por eso se recomienda no agregar los índices en la propia migración, sino indicar al servidor que el índice es necesario agregando un listener para `AddMissingIndicesEvent`. Así la migración puede ejecutarse en un paso separado y no bloquea el proceso de actualización. En las instalaciones nuevas, el índice debe seguir agregándose en la migración que crea la tabla.

```php
class AddMissingIndicesListener implements IEventListener {
   public function handle(Event $event): void {
      if (!$event instanceof AddMissingIndicesEvent) {
         return;
      }

      $event->addMissingIndex('my_table', 'my_index', ['column_a', 'column_b']);
   }
}
```

### Reemplazar índices

:::{versionadded} 29.0.0
:::

Al igual que al agregar un índice a una tabla existente, podría ser necesario reemplazar uno o más índices por uno nuevo. Para evitar un intervalo entre la eliminación de los índices antiguos en una migración y la adición del nuevo mediante `AddMissingIndicesEvent`, se pueden hacer ambas cosas a la vez en `AddMissingIndicesEvent`.

Si no se encuentra ninguno de los índices anteriores, p. ej., porque eran opcionales y aún no se habían creado, el índice de reemplazo se trata como *índice faltante*.

:::{note}
Asegurarse de no usar para el índice nuevo el mismo nombre que para los índices antiguos.
:::

```php
class ReplaceIndicesListener implements IEventListener {
   public function handle(Event $event): void {
      if (!$event instanceof AddMissingIndicesEvent) {
         return;
      }

      $event->replaceIndex('my_table', ['my_old_index_one', 'my_old_index_two'], 'my_new_index', ['column_a', 'column_b'], false);
   }
}
```
````
