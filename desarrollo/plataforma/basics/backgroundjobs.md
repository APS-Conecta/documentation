---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo escribir, registrar y programar trabajos en segundo plano (QueuedJob y TimedJob), incluidos los trabajos insensibles al tiempo y el paralelismo."
---
(nc-dev-app-backgroundjobs)=
# Trabajos en segundo plano (Cron)

## Resumen

Esta página explica los tipos de trabajos en segundo plano, cómo escribir uno, cómo marcarlo como insensible al tiempo o limitar su paralelismo, y cómo registrarlo en `info.xml`, manualmente o programado para una fecha. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/backgroundjobs.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
A menudo es necesario ejecutar trabajos en segundo plano. Por ejemplo, en Nextcloud hay trabajos en segundo plano que envían los correos de actividad, o que hacen caducar la papelera.

### Tipos de trabajos en segundo plano

De forma predeterminada, Nextcloud ofrece dos tipos de trabajos en segundo plano: `\OCP\BackgroundJob\QueuedJob` y `\OCP\BackgroundJob\TimedJob`.

`QueuedJob` sirve para trabajos que se ejecutan una sola vez. Puede activarse, por ejemplo, insertando un trabajo porque ocurrió un evento. `TimedJob` tiene un método `setInterval` con el que se puede fijar el tiempo mínimo en segundos entre ejecuciones del trabajo (desde el constructor). Esto es útil cuando se quiere, por ejemplo, un trabajo que se ejecute como máximo una vez al día.

Por supuesto, todo esto se puede personalizar a gusto simplemente extendiendo `\OCP\BackgroundJob\Job`

### Escribir un trabajo en segundo plano

Escribir un trabajo en segundo plano es bastante sencillo. Se escribe una clase que extiende la clase de trabajo elegida.

```php
<?php
namespace OCA\MyApp\Cron;

use OCA\MyApp\Service\SomeService;
use OCP\BackgroundJob\TimedJob;
use OCP\AppFramework\Utility\ITimeFactory;

class SomeTask extends TimedJob {

    private SomeService $myService;

    public function __construct(ITimeFactory $time, SomeService $service) {
        parent::__construct($time);
        $this->myService = $service;

        // Run once an hour
        $this->setInterval(3600);
    }

    protected function run($arguments) {
        $this->myService->doCron($arguments['uid']);
    }

}
```

Como se ve, la inyección de dependencias también funciona sin problemas en los trabajos en segundo plano. El ITimeFactory siempre debe pasarse al constructor padre, ya que es obligatorio establecerlo.

En este caso se trata de un trabajo en segundo plano que se ejecuta cada hora. Y se toma el argumento `uid` para pasárselo al servicio que ejecuta el trabajo en segundo plano.

La función `run` es lo principal que hay que implementar y es donde ocurre toda la lógica.

(nc-dev-app-backgroundjobs-time-sensitivity)=
#### Carga pesada e insensible al tiempo

Cuando el trabajo en segundo plano es un `\OCP\BackgroundJob\TimedJob`, puede afectar al rendimiento de la instancia y no es sensible al tiempo (p. ej., borrar datos antiguos, entrenar modelos de IA o cosas similares), conviene marcarlo como insensible al tiempo en el constructor.

```php
<?php

// Run once a day
$this->setInterval(24 * 3600);
// Delay until low-load time
$this->setTimeSensitivity(\OCP\BackgroundJob\IJob::TIME_INSENSITIVE);
```

Esto permite a Nextcloud retrasar el trabajo hasta una franja horaria nocturna determinada, de modo que la carga pesada del trabajo en segundo plano afecte menos a los usuarios.

#### Configurar el paralelismo

:::{versionadded} 27
:::

En los trabajos en segundo plano que consumen muchos recursos y se ejecutan durante más de unos minutos, ya sean instancias de `QueuedJob` o de `TimedJob`, puede convenir restringir el paralelismo para evitar que varios de esos trabajos saturen los recursos del servidor. Esto se hace con el método `setAllowParallelRuns` de `OCP\BackgroundJob\Job` (`QueuedJob` y `TimedJob` heredan ambos de esta clase, así que también lo tienen disponible).

```php
<?php

// Only run one instance of this job at a time
$this->setAllowParallelRuns(false);
```

### Registrar un trabajo en segundo plano

Una vez escrito el trabajo en segundo plano, queda por supuesto la pequeña cuestión de cómo asegurarse de que el sistema lo ejecute de verdad. Para ello, el trabajo debe registrarse.

#### info.xml

Los trabajos se pueden registrar en el info.xml agregando lo siguiente:

```xml
<background-jobs>
    <job>OCA\MyApp\Cron\SomeTask</job>
</background-jobs>
```

Esto agregará el trabajo `OCA\MyApp\Cron\SomeTask` al instalar o actualizar la aplicación. Por supuesto, en este caso los argumentos que se pasan a la función `run` son solo un array vacío.

#### Registrar manualmente

Si se quiere un control más preciso sobre cuándo se inserta un trabajo en segundo plano y se le quieren pasar argumentos, hay que registrar los trabajos en segundo plano manualmente.

Esto se hace con `\OCP\BackgroundJob\IJobList`. Ahí se puede agregar o quitar un trabajo.

Por ejemplo, se podría agregar o quitar un trabajo determinado a partir de algún controlador:

```php
<?php
namespace OCA\MyApp\Controller;

use OCA\MyApp\Cron\SomeTask;
use OCP\AppFramework\Controller;
use OCP\BackgroundJob\IJobList;
use OCP\IRequest;

class SomeController extends Controller {

    private IJobList $jobList;

    public function __construct(string $appName, IRequest $request, IJobList $jobList) {
        parent::__construct($appName, $request);

        $this->jobList = $jobList;
    }

    public function addJob(string $uid) {
        $this->jobList->add(SomeTask::class, ['uid' => $uid]);
    }

    public function removeJob(string $uid) {
        $this->jobList->remove(SomeTask::class, ['uid' => $uid]);
    }
}
```

Esto da un control más preciso y permite pasar argumentos fácilmente a los trabajos en segundo plano.

#### Programación

Un trabajo en segundo plano puede programarse para ejecutarse después de una fecha y hora concretas. Así se evita mantener una comprobación de la hora dentro del trabajo en segundo plano.

Hay que tener en cuenta que la fiabilidad de la hora de ejecución es limitada. Los sistemas que no usan el cron del sistema pueden no tener usuarios activos y, por tanto, ningún disparador de cron fiable a la hora prevista. El cron del sistema tampoco puede garantizar que el trabajo se tome de inmediato si la cola de trabajos en segundo plano está llena. La única garantía es que el trabajo no se tomará antes de la hora indicada.

**Archivo {file}`lib/Service/ShareService.php`**:

```php
<?php

namespace OCA\MyApp\Service;

use OCA\MyApp\BackgroundJob\RevokeShare;
use OCP\BackgroundJob\IJobList;

class ShareService {

    private IJobList $jobList

    public function __construct(IJobList $jobList) {
        $this->jobList = $jobList;
    }

    public function shareWithUser(string $uid, int $expiration) {
        // create an expiring share

        $this->jobList->scheduleAfter(
            RevokeShare::class,
            ['id' => $shareId],
            $expiration,
        );
    }
}
```
````
