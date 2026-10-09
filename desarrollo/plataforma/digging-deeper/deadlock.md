---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Qué son los interbloqueos de MySQL/MariaDB, cómo investigarlos y cómo una app puede ignorarlos, reintentar la transacción o evitarlos."
---
# Interbloqueos

## Resumen

Esta página explica qué son los interbloqueos de las bases de datos transaccionales, cómo obtener de MySQL/MariaDB la información para entenderlos y las tres formas de tratarlos en una app: ignorarlos, reintentar la transacción o evitarlos. Está dirigida a quienes desarrollan sobre la plataforma.

````{upstream} developer_manual/digging_deeper/deadlock.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los interbloqueos son un problema clásico de las bases de datos transaccionales, pero **no son
peligrosos salvo que sean tan frecuentes que no se puedan ejecutar ciertas transacciones en
absoluto**. Normalmente, las aplicaciones deben escribirse de modo que estén siempre preparadas
para volver a emitir una transacción si esta se revierte a causa de un interbloqueo.

### Entender la situación de bloqueo

MySQL/MariaDB detecta automáticamente los interbloqueos de transacciones y revierte una o varias
transacciones para romper el interbloqueo. Intenta elegir transacciones pequeñas para revertirlas,
donde el tamaño de una transacción lo determina el número de filas insertadas, actualizadas o
eliminadas.

Para corregir un interbloqueo hay que entender los escenarios en los que se producen interbloqueos
en la aplicación, analizando el registro de Nextcloud en busca de patrones en los errores de
interbloqueo. En este caso, el registro de Nextcloud solo muestra la transacción que se revirtió,
por lo que, para entender correctamente el escenario del interbloqueo, es necesario obtener más
información del servidor de base de datos. De forma predeterminada, el último interbloqueo
detectado se encuentra en la salida de `SHOW ENGINE INNODB STATUS`; sin embargo,
`innodb_print_all_deadlocks` puede usarse como ajuste para escribir en los registros del servidor
todos los interbloqueos que se produzcan. Estos dan una visión detallada de qué consultas mantienen
un bloqueo y provocan que la consulta de Nextcloud caiga en un interbloqueo.

### Mitigaciones

Hay básicamente 3 opciones para tratar correctamente los interbloqueos. No es crítico tratarlos en
todos los casos de uso; sin embargo, según la recomendación de MySQL/MariaDB, la aplicación debería
estar preparada para tratarlos correctamente.

#### Ignorar los interbloqueos

Hay algunos escenarios en los que un interbloqueo podría ignorarse sin riesgo, como al actualizar
una marca de tiempo que probablemente ya está actualizando otra solicitud concurrente. En este caso,
quienes desarrollan pueden capturar la excepción e ignorar la transacción fallida.

- Envoltorio de API potencialmente útil:
  <https://github.com/nextcloud/server/pull/38030>
- Ejemplo de un caso válido: <https://github.com/nextcloud/server/pull/37820>

```
try {
      // Database transaction that runs into the deadlock
    $qb->executeStatement();
} catch (DbalException $e) {
      // ignore the failure
        $this->logger->info("Deadlock detected, but ignored", ['exception' => $e]);
}
```

#### Reintentar los interbloqueos

En otros casos puede ser viable simplemente reintentar las transacciones de base de datos
concretas. En este caso hay que capturar la excepción y volver a emitir la transacción. Se
recomienda limitar la cantidad de reintentos por si el interbloqueo se produce con regularidad. En
ese caso se puede seguir la sección siguiente.

Un ejemplo de cómo hacerlo se encuentra en
<https://github.com/nextcloud/server/pull/34302>

A partir de Nextcloud 27 también hay un método auxiliar útil, `atomicRetry`, que simplifica mucho
el reintento de transacciones:

```
class MyClass {
  use \OCP\AppFramework\Db\TTransactional;

  public function myFunction() {
     $this->atomicRetry(function() {
       // Database transaction that runs into the deadlock
       $qb->executeStatement();
     }, $this->connection, 5);
  }
}
```

#### Evitar los interbloqueos

Aunque no siempre es posible debido a la concurrencia que puede darse en Nextcloud, puede ser
viable refactorizar la lógica de modo que se reduzca la carga de escrituras concurrentes en una
tabla o en columnas, o que solo una solicitud pueda mantener a la vez un bloqueo sobre una fila de
una tabla.

### Referencias

- <https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks.html>
- <https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks-handling.html>
- <https://percona.community/blog/2018/09/24/minimize-mysql-deadlocks-3-steps/>
- <https://www.percona.com/blog/enable-innodb_print_all_deadlocks-parameter-to-get-all-deadlock-information-in-mysqld-error-log/>
````
