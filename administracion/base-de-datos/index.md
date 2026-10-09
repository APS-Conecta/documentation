---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Base de datos del servidor: configuración, conversión desde SQLite, compatibilidad con 4 bytes en MySQL, identificadores BigInt, replicación y división."
---
# Configuración de la base de datos

## Resumen

Esta sección reúne las páginas sobre la base de datos del servidor: su configuración con MySQL, MariaDB o PostgreSQL, la conversión desde SQLite, la compatibilidad con 4 bytes en MySQL, los identificadores BigInt, la replicación y la división de bases de datos. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_database/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

- {nc-doc}`admin_manual/configuration_database/db_conversion`
- {nc-doc}`admin_manual/configuration_database/linux_database_configuration`
- {nc-doc}`admin_manual/configuration_database/mysql_4byte_support`
- {nc-doc}`admin_manual/configuration_database/bigint_identifiers`
- {nc-doc}`admin_manual/configuration_database/replication`
- {nc-doc}`admin_manual/configuration_database/splitting`
````

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
