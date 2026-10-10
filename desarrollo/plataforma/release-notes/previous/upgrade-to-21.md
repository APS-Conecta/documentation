---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 21 para las apps: PHP 8, bibliotecas del núcleo como doctrine/dbal 3.0, verificador de código obsoleto, PSR-0 y database.xml."
---
# Actualización a Nextcloud 21

## Resumen

Esta página enumera los cambios de backend de la versión 21 que afectan a las apps: la compatibilidad con PHP 8, la actualización de bibliotecas del núcleo (`doctrine/dbal`, `guzzlehttp/guzzle`, `psr/log` y `sabre/*`), la obsolescencia del verificador de código y de PSR-0, el último soporte de `appinfo/database.xml` y la nueva API well-known. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_21.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Los cambios críticos se recopilaron [en GitHub](https://github.com/nextcloud/server/issues/23210). Consultar el ticket original para ver los enlaces a las pull requests y a los tickets.
:::

### Cambios de backend

El mayor cambio de Nextcloud 21 es la compatibilidad inicial con PHP 8 y las correspondientes actualizaciones de muchas dependencias del núcleo, que podrían tener consecuencias directas e indirectas para las apps.

#### Compatibilidad con PHP 8

Nextcloud 21 es la primera versión mayor compatible con el nuevo PHP 8.0. En consecuencia, alguna sintaxis que antes funcionaba puede causar problemas cuando una app se despliega con un PHP posterior a 7.4. El registro de cambios completo se encuentra [en el sitio web de php.net](https://www.php.net/ChangeLog-8.php). También hay un documento con todos los cambios incompatibles [en GitHub](https://github.com/php/php-src/blob/PHP-8.0/UPGRADING#L20).

Para comprobar la compatibilidad automáticamente, se recomienda añadir o actualizar la {nc-ref}`app-ci` de la app, de modo que los linters, las pruebas y el análisis estático puedan advertir de cualquier problema antes de que la app llegue a los usuarios.

#### Bibliotecas del núcleo actualizadas

Si las apps usan solo API públicas oficiales de Nextcloud, la actualización de las bibliotecas del núcleo debería tener poco o ningún efecto en ellas. Sin embargo, hay algunos casos límite en los que una app todavía tiene una dependencia de código con una biblioteca incluida en Nextcloud, por ejemplo cuando se usan esas clases o funciones de terceros, por lo que se recomienda a quienes desarrollan apps revisar su código en busca de cualquier incompatibilidad. Además, se recomienda comprobar la compatibilidad con herramientas sofisticadas, como se documenta en la sección de {nc-ref}`análisis estático <app-static-analysis>`.

##### `doctrine/dbal`

La capa de abstracción de bases de datos de Doctrine (Doctrine Database Abstraction Layer) impulsa la conexión a la base de datos y el constructor de consultas de Nextcloud. En Nextcloud 21, esta dependencia se actualizó de 2.x a 3.0. En consecuencia, algunos tipos que antes se exportaban a través de la API OCP de Nextcloud se eliminaron o cambiaron con esta actualización. Por compatibilidad con versiones anteriores, ahora hay una pequeña capa de compatibilidad entre la API original de Doctrine y lo que las apps usan mediante la API de Nextcloud.

Siendo optimistas, la conexión a la base de datos y el constructor de consultas deberían funcionar en su mayor parte como en Nextcloud 20 o anteriores. Las principales diferencias son que las sentencias preparadas y los resultados de las consultas ya no los maneja el `Statement` de Doctrine, que se eliminó, sino dos nuevos tipos de Nextcloud, `IPreparedStatement` e `IResult`. No hay que preocuparse por estos tipos salvo que se pase el resultado de una consulta a una clase/método/función con declaraciones de tipo. En este caso poco frecuente, ajustar las declaraciones de tipo al nuevo tipo si las apps solo son compatibles con Nextcloud 21, o quitar temporalmente la declaración de tipo para ser compatibles con varias versiones de Nextcloud.

Algunos cambios incompatibles (menores) fueron inevitables. Este es el resumen

- Muchos de los métodos de la conexión a la base de datos tienen ahora documentada una excepción que puede lanzarse: `\OCP\DB\Exception`. Esta también sirve de reemplazo de la eliminada `\Doctrine\DBAL\DBALException`.
- `$queryBuilder->execute()->fetch()` ahora solo tiene un argumento (antes tenía tres)
- `$queryBuilder->execute()->fetchColumn()` ya no tiene argumentos y además quedó obsoleto. Usar `fetchOne` en su lugar
- `$queryBuilder->execute()->bindParam()` se eliminó porque conceptualmente no tiene sentido vincular un parámetro *después* de ejecutar una consulta. Usar `bindParam` en el `IPeparedStatement` en su lugar.
- `$queryBuilder->execute()->bindValue()` se eliminó porque conceptualmente no tiene sentido vincular un valor *después* de ejecutar una consulta. Usar `bindValue` en el `IPeparedStatement` en su lugar.
- `$queryBuilder->execute()->columnCount()` se eliminó
- `$queryBuilder->execute()->errorCode()` se eliminó de Doctrine
- `$queryBuilder->execute()->errorInfo()` se eliminó de Doctrine
- `$queryBuilder->execute()->setFetchMode()` se eliminó de Doctrine
- `$connection->prepare()->execute()` antes devolvía `false` en algunas condiciones de error; ahora siempre devuelve un `IResult` o lanza una `\OCP\DB\Exception`.
- Las constantes de tipo `\Doctrine\DBAL\Types\Type::*` se trasladaron; algunas apps las usaban como constantes de tipo de columna. Usar las nuevas `\OCP\DB\Types::*` como reemplazo.

Los detalles de este cambio también pueden verse en la [pull request en GitHub](https://github.com/nextcloud/server/pull/24948) y en el [documento de actualización a dbal 3.0.xx](https://github.com/doctrine/dbal/blob/3.0.x/UPGRADE.md) del proyecto original.

##### `guzzlehttp/guzzle`

La biblioteca de cliente HTTP en la que se basa el cliente HTTP de Nextcloud se actualizó para ser compatible con PHP 8. La abstracción de Nextcloud no cambió y funcionará como antes. Si se usaba Guzzle directamente, asegurarse de no usar la API fluida en las solicitudes o en las respuestas.

##### `psr/log`

El paquete {nc-ref}`psr3` se actualizó a la v1.1. En teoría, el método `log` ahora puede lanzar una `\Psr\Log\InvalidArgumentException`, aunque por el momento Nextcloud no hace uso de ello. Aun así, se recomienda revisar cualquier uso del método y añadir gestión de errores si corresponde.

##### `sabre/*`

Los paquetes de Sabre recibieron una actualización menor. Solo deberían verse afectadas, si acaso, las apps que ofrecen funcionalidad DAV.

#### Obsolescencia del verificador de código de apps

El verificador de código de apps (`occ app:check-code myapp`) queda obsoleto debido al {nc-ref}`análisis estático <app-static-analysis>`. En Nextcloud 21 actuará como NOOP, es decir, el comando aún puede llamarse, pero nunca fallará. Esto permite seguir usándolo en la CI si se prueba contra la 21, la 20 y versiones anteriores. Pero hay que preparar el cambio al análisis estático si aún no se ha hecho. Tener en cuenta también que el verificador de código de apps no había recibido muchas actualizaciones últimamente, por lo que la cantidad de problemas que puede detectar es baja.

#### Obsolescencia de PSR-0

El estándar original *PSR-0* quedó obsoleto en 2014, por lo que su soporte en Nextcloud también terminará pronto. Por eso se recomienda migrar los nombres de archivo de las clases a *PSR-4*.

#### Última versión con soporte de database.xml y migración

Nextcloud 21 es la última versión mayor que admite el `appinfo/database.xml` de una app para definir el esquema de la base de datos. Es la última oportunidad de convertir automáticamente este archivo obsoleto en las nuevas clases de migración con `occ migrations:generate-from-schema`.

#### API de manejadores well-known reemplazada

Existía un mecanismo antiguo, no usado y no oficial para engancharse al descubrimiento well-known mediante ajustes de configuración. Esto incluye `host-meta`, `host-meta.json`, `nodeinfo` y `webfinger`. En Nextcloud 21, una {nc-ref}`nueva API pública reemplaza este mecanismo <web-host-metadata>`.

[PSR-0]: https://www.php-fig.org/psr/psr-0/
[PSR-4]: https://www.php-fig.org/psr/psr-4/
````
