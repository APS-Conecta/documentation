---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo convertir a enteros grandes (BigInt) los identificadores de las tablas filecache y activity con el comando occ db:convert-filecache-bigint."
---
# Identificadores BigInt (64 bits)

## Resumen

Esta página explica por qué la migración a identificadores de 64 bits de las tablas filecache y activity se inicia a mano y cómo ejecutarla con `occ db:convert-filecache-bigint`. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_database/bigint_identifiers.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud usa enteros grandes para almacenar los identificadores y las claves de autoincremento en la base de datos. Como modificar columnas en tablas enormes puede tardar bastante (hasta horas o días) según la cantidad de archivos de la instancia de Nextcloud, esta migración de las tablas filecache y activity debe iniciarse manualmente mediante un comando de consola.

El comando puede ejecutarse con seguridad. Si no hay nada que hacer, muestra un mensaje de éxito:

```
sudo -E -u www-data php occ db:convert-filecache-bigint
All tables already up to date!
```

o, en caso contrario, pide confirmación antes de realizar las operaciones pesadas:

```
sudo -E -u www-data php occ db:convert-filecache-bigint
This can take up to hours, depending on the number of files in your instance!
Continue with the conversion (y/n)? [n]
```

Para omitir el mensaje de confirmación, añadir `--no-interaction` a la lista de argumentos:

```
sudo -E -u www-data php occ db:convert-filecache-bigint --no-interaction
```

:::{note}
Al igual que en una actualización normal, se debería detener el servidor Apache o nginx, o bien activar el modo de mantenimiento, antes de ejecutar el comando, para evitar problemas con los clientes de sincronización.
:::
````
