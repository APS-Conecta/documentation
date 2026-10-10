---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Novedades de la plataforma en esta versión: constructor de consultas tipado, pasos de reparación costosos y espacios de nombres de las apps."
---
(nc-dev-new-apis)=
# Novedades de esta versión

## Resumen

Esta página presenta brevemente las nuevas funciones de la plataforma en esta versión: el constructor de consultas tipado, los pasos de reparación costosos posteriores a la migración y dos métodos nuevos para los espacios de nombres de las apps. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/release_notes/new.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Esta página trata las nuevas funciones de la plataforma.

### Constructor de consultas tipado

Se añadió `\OCP\DB\QueryBuilder\ITypedQueryBuilder`, preferible a `\OCP\DB\QueryBuilder\IQueryBuilder`, y se puede acceder a él mediante `\OCP\IDBConnection::getTypedQueryBuilder`.

Este constructor de consultas tiene la ventaja de devolver con exactitud las columnas seleccionadas en el resultado de una consulta, lo que aumenta la seguridad de tipos.

Ver {nc-ref}`database` para más detalles.

### Pasos de reparación costosos posteriores a la migración

Se añadió `\OCP\Migration\IRepairStepExpensive`, que se puede usar para marcar como costosos los pasos de reparación posteriores a la migración.

Los pasos de reparación costosos son pasos de reparación no críticos que pueden tardar mucho en ejecutarse.
No críticos significa que no es necesario ejecutarlos directamente durante la migración para tener una instancia que funcione,
pero puede que sean necesarios más adelante para tener una instancia que funcione por completo.

Los pasos de reparación costosos solo se ejecutan cuando el administrador lo solicita explícitamente.

Ver {nc-ref}`migration-repair-steps` para más detalles.

### Gestión de los espacios de nombres de las aplicaciones

`\OCP\App\IAppManager` se amplió con dos métodos nuevos relacionados con los espacios de nombres de las aplicaciones:

- `getAppNamespace(string $appId): string` devuelve el espacio de nombres de una aplicación a partir de su appid. Ver [Documentación](https://nextcloud-server.netlify.app/classes/ocp-app-iappmanager#method_getAppNamespace).
- `getAppFromNamespace(string $className): ?string` hace lo contrario. Es menos habitual, pero se usa en la aplicación guests. Ver [Documentación](https://nextcloud-server.netlify.app/classes/ocp-app-iappmanager#method_getAppFromNamespace).

Esto sustituye al método estático `\OCP\AppFramework\App::buildAppNamespace`, que ahora está obsoleto.
````
