---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 24 para las apps: rango de info.xml, compatibilidad con PHP 8.1, fin de PHP 7.3 y obsolescencia de los slugs de entidad."
---
# Actualización a Nextcloud 24

## Resumen

Esta página enumera los cambios de la versión 24 que afectan a las apps: el rango de versiones de `appinfo/info.xml`, los pasos para ser compatible con PHP 8.1 tras el fin de PHP 7.3 y la obsolescencia de los slugs de entidad. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_24.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Los cambios críticos se recopilaron [en GitHub](https://github.com/nextcloud/server/issues/29914). Consultar el ticket original para ver los enlaces a las pull requests y a los tickets.
:::

### General

#### info.xml

Asegurarse de que el `appinfo/info.xml` de la app admita Nextcloud 24.

```xml
<dependencies>
  <nextcloud min-version="21" max-version="24" />
</dependencies>
```

### Cambios de backend

#### PHP 8.1

Nextcloud 24 es la primera versión mayor de Nextcloud que funciona con PHP 8.1. En esta versión se dejó de admitir PHP 7.3. Seguir los pasos siguientes para que la app sea compatible.

1. Si `appinfo/info.xml` tiene una especificación de dependencia para PHP, aumentar `max-version` a 8.1.

```xml
<dependencies>
  <php min-version="7.4" max-version="8.1" />
  <nextcloud min-version="21" max-version="24" />
</dependencies>
```

2. Si la app tiene un `composer.json` y el archivo contiene las restricciones de PHP de `info.xml`, ajustarlo también.

```json
{
  "require": {
    "php": ">=7.4 <=8.1"
  }
}
```

3. Si se tiene configurada la {nc-ref}`integración continua <app-ci>`, ampliar la matriz de pruebas con pruebas y linters de PHP 8.1 y eliminar cualquier trabajo de PHP 7.3.

La información sobre los cambios de código se encuentra en [php.net](https://www.php.net/migration81) y [stitcher.io](https://stitcher.io/blog/new-in-php-81#breaking-changes).

#### Obsolescencia de los slugs de entidad

El uso de {nc-ref}`slugs de entidad <database-entity-slugs>` quedó obsoleto. No se ofrece ningún reemplazo. Si la app necesita slugs, añadir una lógica propia para crearlos.
````
