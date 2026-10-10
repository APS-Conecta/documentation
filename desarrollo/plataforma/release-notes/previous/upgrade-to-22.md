---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 22 para las apps: comandos de migración, registro JSON, scss, Node 14, fin de IE11 y database.xml, eventos PSR y HTTP 401."
---
# Actualización a Nextcloud 22

## Resumen

Esta página enumera los cambios de la versión 22 que afectan a las apps: los comandos de migración solo en modo de depuración, el formato del registro JSON, la obsolescencia de scss, Node v14, el fin de IE11 y de `appinfo/database.xml`, los eventos y el contenedor PSR, las columnas booleanas, el HTTP 401 y las API eliminadas u obsoletas. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_22.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Los cambios críticos se recopilaron [en GitHub](https://github.com/nextcloud/server/issues/26407). Consultar el ticket original para ver los enlaces a las pull requests y a los tickets.
:::

### General

#### Comandos de migración

Los comandos occ del espacio de nombres `migration:*` ahora solo están disponibles en el {nc-ref}`modo de depuración <debug-mode>`.

Ver [la pull request en GitHub](https://github.com/nextcloud/server/pull/27113) para más información. Si se creía necesitarlos, se puede avisar al autor o a un revisor de la PR para resolver el problema correctamente. Ejecutar migraciones directamente suele romper el estado de la base de datos y, por eso, solo está pensado para depurar migraciones defectuosas.

#### Formato del registro

El formato de registro JSON ya no contiene la excepción completa en el campo del mensaje, sino que se añade una entrada de excepción separada y el mensaje existente solo contendrá el texto del mensaje de la excepción. Esto podría requerir ajustes por parte de quienes administran cuando los registros se extraen a fuentes externas.

### Cambios de frontend

#### Obsolescencia de las variables scss y de su compilación

Nextcloud está eliminando gradualmente las variables scss y la compilación de las hojas de estilo de las apps. Se recomienda que las apps usen su propia compilación (por ejemplo, mediante Webpack) para transformar scss y similares en css plano. La capacidad de Nextcloud de compilar scss para las apps se eliminará en el futuro. Suscribirse al [ticket 9940 de GitHub](https://github.com/nextcloud/server/issues/9940) para recibir novedades sobre la mejor manera de abordar esto. Por ahora, algunas variables scss pueden reemplazarse por variables css. Otros mecanismos, como la generación de iconos, aún dependen de la compilación de scss por parte de Nextcloud.

#### Actualización de Node.js

La mayoría de las apps de Nextcloud y el propio Nextcloud se compilan ahora con Node v14 LTS en lugar de v12. Se recomienda actualizar la configuración de la app en consecuencia.

#### Eliminación de IE11

Internet Explorer 11 se fue retirando a lo largo de las últimas versiones y, a partir de Nextcloud 22, el código de frontend ya no se transpila para IE11. También se puede retirar IE11 de la app, ya que es posible que los componentes del núcleo fallen de todos modos con este navegador.

#### Variables globales obsoletas

- `DOMPurify`: incluir una propia.

### Cambios de backend

#### Soporte de database.xml eliminado

Se eliminó el soporte del `appinfo/database.xml` de una app.

#### Eventos PSR

Para acercar las API de Nextcloud a {nc-ref}`psr`, la clase base de eventos ya no extiende la antigua clase de eventos de Symfony, sino solo `\Psr\EventDispatcher\StoppableEventInterface`. Desde el punto de vista de una app, este cambio es transparente.

#### Contenedor PSR

La {nc-ref}`interfaz de contenedor PSR 11 <psr11>` se actualizó de la versión 1.0 a la 1.1.

#### Disponibilidad de la fábrica LDAP

`\OCP\LDAP\ILDAPProviderFactory` recibió un nuevo método `isAvailable` para que las apps puedan comprobar si LDAP está configurado y en uso antes de obtener atributos o algo similar.

#### Columnas booleanas de la base de datos

Como Oracle no puede almacenar booleanos en una columna booleana no anulable, Nextcloud ya no admite columnas booleanas no nulas. Las apps deben migrar su esquema a columnas booleanas anulables.

#### HTTP 401 para nombre de usuario o contraseña no válidos

Cuando se envía un nombre de usuario o una contraseña no válidos a una API de Nextcloud, Nextcloud ahora responde con un estado HTTP 401 en lugar de 403.

#### API eliminadas

- `\OC\Memcache\Factory::create`
- `\OCP\User`
- `\OCP\Util::isIe`

#### API obsoletas

- `\OCP\Log\ILogFactory::getCustomLogger`: usar `\OCP\Log\ILogFactory::getCustomPsrLogger` para obtener un logger {nc-ref}`PSR3 <psr3>` personalizado
- Evento `\OCP\IDBConnection::ADD_MISSING_INDEXES` y la constante correspondiente `\OCP\IDBConnection::ADD_MISSING_INDEXES_EVENT`: evento interno
- Evento `\OCP\IDBConnection::CHECK_MISSING_INDEXES` y la constante correspondiente `\OCP\IDBConnection::CHECK_MISSING_INDEXES_EVENT`: evento interno
- Evento `\OCP\IDBConnection::ADD_MISSING_PRIMARY_KEYS` y la constante correspondiente `\OCP\IDBConnection::ADD_MISSING_PRIMARY_KEYS_EVENT`: evento interno
- Evento `\OCP\IDBConnection::CHECK_MISSING_PRIMARY_KEYS` y la constante correspondiente `\OCP\IDBConnection::CHECK_MISSING_PRIMARY_KEYS_EVENT`: evento interno
- Evento `\OCP\IDBConnection::ADD_MISSING_COLUMNS_EVENT` y la constante correspondiente `\OCP\IDBConnection::ADD_MISSING_COLUMNS`: evento interno
- Evento `\OCP\IDBConnection::CHECK_MISSING_COLUMNS` y la constante correspondiente `\OCP\IDBConnection::CHECK_MISSING_COLUMNS`: evento interno
````
