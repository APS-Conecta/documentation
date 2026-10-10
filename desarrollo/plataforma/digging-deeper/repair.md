---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo crear y registrar pasos de reparación que se ejecutan al instalar, desinstalar o actualizar una app, sus tipos y los pasos costosos."
---
(nc-dev-migration-repair-steps)=
# Pasos de reparación

## Resumen

Esta página explica qué son los pasos de reparación de una app, cómo crearlos, mostrar su progreso y registrarlos en `info.xml`, qué tipos existen y cómo marcar un paso como costoso. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/repair.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los pasos de reparación son métodos que Nextcloud ejecuta ante ciertos eventos que afectan directamente a la app. Estos pasos de reparación se pueden usar para ejecutar código cuando la app se instala, se desinstala, se actualiza, etc. Se llaman pasos de reparación porque se usan con frecuencia para corregir cosas automáticamente.

:::{note}
¡Ya no se deben usar los archivos `install.php`! Este método está obsoleto y se sabe que causa problemas.
:::

### Crear un paso de reparación

Un paso de reparación es una implementación de la interfaz `OCP\Migration\IRepairStep`.
Por convención, estas clases se colocan en el directorio **lib/Migration**.
El siguiente paso de reparación registrará un mensaje en el log al ejecutarse.

```php
<?php
namespace OCA\MyApp\Migration;

use OCP\Migration\IOutput;
use OCP\Migration\IRepairStep;
use Psr\Log\LoggerInterface;

class MyRepairStep implements IRepairStep {

  /** @var LoggerInterface */
  protected $logger;

  public function __construct(LoggerInterface $logger) {
      $this->logger = $logger;
  }

  /**
   * Returns the step's name
   */
  public function getName() {
      return 'A demonstration repair step!';
  }

  /**
   * @param IOutput $output
   */
  public function run(IOutput $output) {
      $this->logger->warning("Hello world from MyRepairStep!", ["app" => "MyApp"]);
  }
}
```

#### Mostrar información

Un paso de reparación puede generar información mientras se ejecuta, usando el parámetro `OCP\Migration\IOutput` del método `run`.
Con los métodos `info` y `warning` se puede mostrar un mensaje en la consola.
Para mostrar una barra de progreso, primero hay que llamar al método `startProgress`.
El número máximo de pasos puede ajustarse pasándolo como argumento al método `startProgress`. Después de cada paso, ejecutar el método `advance`. Una vez terminados todos los pasos, ejecutar el método `finishProgress`.

La siguiente función esperará 10 segundos y mostrará el progreso:

```php
<?php
/**
 * @param IOutput $output
 */
public function run(IOutput $output) {
  $output->info("This step will take 10 seconds.");
  $output->startProgress(10);
  for ($i = 0; $i < 10; $i++) {
      sleep(1);
      $output->advance(1);
  }
  $output->finishProgress();
}
```

### Registrar un paso de reparación

Para registrar un paso de reparación en Nextcloud hay que definirlo en el archivo `info.xml`. El siguiente ejemplo registra un paso de reparación que se ejecutará después de la instalación de la app:

```xml
<?xml version="1.0"?>
<info xmlns:xsi= "http://www.w3.org/2001/XMLSchema-instance"
  xsi:noNamespaceSchemaLocation="https://apps.nextcloud.com/schema/apps/info.xsd">
  <id>myapp</id>
  <name>My App</name>
  <summary>A test app</summary>
  ...
  <repair-steps>
      <install>
          <step>OCA\MyApp\Migration\MyRepairStep</step>
      </install>
  </repair-steps>
</info>
```

### Tipos de pasos de reparación

Están disponibles los siguientes pasos de reparación:

- `install` Este paso de reparación se ejecutará al instalar la app. Esto significa que se ejecuta cada vez que se activa la app (desde la interfaz web o la CLI).
- `uninstall` Este paso de reparación se ejecutará al desinstalar la app y al desactivarla.
- `pre-migration` Este paso de reparación se ejecutará justo antes de migrar la base de datos durante una actualización de la app.
- `post-migration` Este paso de reparación se ejecutará justo después de migrar la base de datos durante una actualización de la app. Este paso de reparación también se ejecutará al ejecutar el comando `occ maintenance:repair`
- `live-migration` Este paso de reparación se programará para ejecutarse en segundo plano (p. ej., mediante cron), por lo que no se puede predecir cuándo se ejecutará. Si el trabajo no es necesario justo después de la actualización de la app y tardaría mucho tiempo, esta es la mejor opción.

### Pasos de reparación costosos

Los pasos de reparación costosos son pasos de reparación no críticos que pueden tardar mucho tiempo en ejecutarse.
No críticos significa que no es necesario ejecutarlos directamente durante la migración para tener una instancia que funcione, pero pueden ser necesarios para tener más adelante una instancia que funcione por completo.

Los pasos de reparación costosos solo se ejecutan cuando quien administra lo solicita explícitamente al usar el comando `occ maintenance:repair`, pasando la opción `--include-expensive`.

:::{note}
Los pasos de reparación costosos solo pueden usarse como pasos de reparación `post-migration`, ya que los demás tipos se ejecutan durante la (des)instalación de la app y, por tanto, no deberían tardar mucho tiempo.
:::

#### Crear un paso de reparación costoso

Los pasos de reparación costosos se crean igual que los pasos de reparación normales, como se ve en el ejemplo anterior.
Pero tienen que implementar la interfaz `\OCP\Migration\IRepairStepExpensive` en lugar de la interfaz `\OCP\Migration\IRepairStep`.
````
