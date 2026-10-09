---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo separar tablas en otra base de datos (prueba de concepto con la app Actividad): criterios, parámetros con prefijo, división inicial y migraciones."
---
# División de bases de datos

## Resumen

Esta página explica cómo llevar algunas tablas a una base de datos separada, una función en fase de prueba de concepto que hoy aplica a la app Actividad: los criterios que debe cumplir la app, los parámetros con prefijo, la división inicial y las migraciones en las actualizaciones. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_database/splitting.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{warning}
Esto todavía está en fase de prueba de concepto. Usar con precaución.
:::

Para escalar, en algún momento puede tener sentido separar algunas tablas o apps que lo permitan, ya que podrían funcionar mejor con otros métodos de replicación, etc.

Un primer intento se está haciendo ahora con la tabla activity. Para aprovecharlo, la app o tabla debe cumplir los siguientes criterios:

- Ninguna otra app puede hacer consultas directamente a la tabla
- No se realizan JOIN entre esta tabla y otras tablas que no estén en esta nueva conexión separada
- La app debe admitir un prefijo para los parámetros de conexión

En el caso de la app Actividad, el prefijo es `activity_`. Si no se especifica una configuración de base de datos, se recurre a la opción de configuración de base de datos normal para ese valor:

- `activity_dbuser` recurre a `dbuser`
- `activity_dbpassword` recurre a `dbpassword`
- `activity_dbname` recurre a `dbname`
- `activity_dbhost` recurre a `dbhost`
- `activity_dbport` recurre a `dbport`
- `activity_dbdriveroptions` recurre a `dbdriveroptions`

:::{note}
No es posible usar un tipo de base de datos distinto (SQLite, MySQL, PostgreSQL, Oracle) para una base de datos separada. Además, en el caso de MySQL y MariaDB, la opción utf8mb4 debe ser la misma en ambas bases de datos.
:::

### División inicial

Para la división inicial, las tablas afectadas deben copiarse a la nueva base de datos; en el caso de la app Actividad, son estas:

- `oc_activity`
- `oc_activity_mq`

1. Activar el modo de mantenimiento
2. Asegurarse de que se hayan aplicado los cambios opcionales de la base de datos:

   1. `occ db:convert-mysql-charset`
   2. `occ db:convert-filecache-bigint`
   3. `occ db:add-missing-columns`
   4. `occ db:add-missing-indices`
   5. `occ db:add-missing-primary-keys`

3. Especificar los valores de configuración deseados
4. Copiar las 2 tablas a la nueva base de datos
5. Desactivar el modo de mantenimiento

### Migraciones en las actualizaciones

Se intentará evitar las migraciones en esas tablas en el futuro, pero en algún momento podrían ser necesarias. Se espera contar con un plan específico para cuando eso ocurra. Por ahora, una posible forma de hacerlo sería:

1. Activar el modo de mantenimiento
2. Actualizar como de costumbre
3. Ejecutar las consultas manuales de cambios de esquema que proporcionen los autores de la app
4. Ejecutar las consultas manuales de cambios de datos que proporcionen los autores de la app
5. Desactivar el modo de mantenimiento
````
