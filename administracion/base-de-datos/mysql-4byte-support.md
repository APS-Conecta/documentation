---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo habilitar en MySQL o MariaDB la compatibilidad con caracteres de 4 bytes (utf8mb4) para poder usar emojis, paso a paso y con occ."
---
# Habilitar la compatibilidad con 4 bytes en MySQL

## Resumen

Esta página recorre los pasos para que una base de datos MySQL o MariaDB admita caracteres de 4 bytes, como los emojis: ajustes de InnoDB, juego de caracteres de la base de datos, la opción `mysql.utf8mb4` y la reparación de tablas. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_database/mysql_4byte_support.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Asegurarse de hacer una copia de seguridad de la base de datos antes de realizar esta actualización de la base de datos.
:::

Para usar emojis (emoticonos basados en texto) en un servidor Nextcloud con una base de datos MySQL, hay que ajustar un poco la instalación.

:::{warning}
Esta guía solo se aplica a MySQL 8 o posterior y a MariaDB 10.6 o posterior. Para ver la lista de versiones compatibles de MySQL y MariaDB, consultar la {nc-doc}`documentación de requisitos del sistema <admin_manual/installation/system_requirements>`.
:::

1. Asegurarse de que los siguientes ajustes de InnoDB estén establecidos en el servidor MySQL:

   ```
   [mysqld]
   innodb_file_per_table=1
   ```

2. Reiniciar el servidor MySQL si se cambió la configuración en el paso 1.

A continuación, puede verificarse que el cambio funcionó:

```sql
SHOW VARIABLES LIKE 'innodb_file_per_table';
```

El resultado debería verse así:

```
mysql> SHOW VARIABLES LIKE 'innodb_file_per_table';
+-----------------------+-------+
| Variable_name         | Value |
+-----------------------+-------+
| innodb_file_per_table | ON    |
+-----------------------+-------+
1 row in set (0.00 sec)
```

3. Abrir un shell, cambiar de directorio (ajustar `/var/www/nextcloud` a la ubicación de nextcloud si es necesario) y poner la instancia de nextcloud en modo de mantenimiento, si aún no lo está:

   ```
   $ cd /var/www/nextcloud
   $ sudo -E -u www-data php occ maintenance:mode --on
   ```

4. Cambiar el juego de caracteres y la intercalación de la base de datos:

```sql
ALTER DATABASE nextcloud CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

5. Establecer en true la opción `mysql.utf8mb4` de config.php:

   ```
   $ sudo -E -u www-data php occ config:system:set mysql.utf8mb4 --type boolean --value="true"
   ```

6. Convertir todas las tablas existentes a la nueva intercalación ejecutando el paso de reparación:

   ```
   $ sudo -E -u www-data php occ maintenance:repair
   ```

:::{note}
Esto también cambia el *ROW_FORMAT* a *DYNAMIC* en las tablas.
:::

7. Desactivar el modo de mantenimiento:

   ```
   $ sudo -E -u www-data php occ maintenance:mode --off
   ```

Ahora debería ser posible usar emojis en los nombres de archivo, los eventos del calendario, los comentarios y mucho más.

:::{note}
Asegurarse también de que la estrategia de copias de seguridad siga funcionando. Si se usa `mysqldump`, asegurarse de añadir la opción `--default-character-set=utf8mb4`. De lo contrario, las copias de seguridad quedan dañadas y, al restaurarlas, aparece `?` en lugar de los emojis, lo que deja los archivos inaccesibles.
:::
````
