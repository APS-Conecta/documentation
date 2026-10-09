---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "La opción dbreplica, que separa lecturas y escrituras: las réplicas atienden solo lecturas y la conexión predeterminada, las escrituras."
---
# Replicación

## Resumen

Esta página describe la opción `dbreplica`, con la que el servidor separa de forma nativa las lecturas, que van a las réplicas, de las escrituras y las lecturas causales, que van a la conexión predeterminada. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_database/replication.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 29
:::

Nextcloud puede separar de forma nativa las operaciones de lectura y de escritura a nivel de consulta de base de datos. Las réplicas solo se usan para lecturas. La conexión de base de datos predeterminada se usa para las escrituras y las lecturas causales.

```
'dbreplica' => [
        ['user' => 'nextcloud', 'password' => 'password1', 'host' => '10.0.3.1', 'dbname' => 'nextcloud'],
        ['user' => 'nextcloud', 'password' => 'password2', 'host' => '10.0.3.2', 'dbname' => 'nextcloud'],
    ],
```
````
