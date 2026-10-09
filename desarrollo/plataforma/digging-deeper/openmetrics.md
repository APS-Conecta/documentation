---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo registrar en info.xml e implementar un exportador de métricas en formato OpenMetrics para el endpoint /metrics, con un ejemplo de su salida."
---
# Exportador de Open Metrics

## Resumen

Esta página explica cómo una app agrega sus propias métricas al endpoint `/metrics` en formato OpenMetrics: registrar el exportador en `appinfo/info.xml` e implementar la interfaz `IMetricFamily`, con un ejemplo de la salida resultante. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/openmetrics.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 33.0
:::

Nextcloud permite exportar métricas en formato [OpenMetrics](https://openmetrics.io/).

Los datos están disponibles en el endpoint `/metrics` y después pueden importarse en cualquier herramienta compatible con OpenMetrics (antes Prometheus).

### Registrar un nuevo exportador

Cada exportador debe registrarse dentro de **\<myapp>/appinfo/info.xml**:

```xml
<openmetrics>
    <exporter>OCA\MyApp\OpenMetrics\CustomExporter</exporter>
    <exporter>OCA\MyApp\OpenMetrics\AnotherExporter</exporter>
</openmetrics>
```

### Implementar un nuevo exportador

Después hay que implementarlo:

```php
<?php

declare(strict_types=1)

namespace OCA\MyApp\OpenMetrics;

use OCP\OpenMetrics\IMetricFamily;
use OCP\OpenMetrics\MetricType;

class CustomExporter implements IMetricFamily {
    public function __construct(
        // Add you dependencies here
    ) {
    }

    #[Override]
    public function name(): string {
        return 'myapp_metric';
    }

    #[Override]
    public function type(): MetricType {
       // One MetricType::*
        return MetricType::gauge;
    }

    #[Override]
    public function unit(): string {
        return 'units';
    }

    #[Override]
    public function help(): string {
        return 'Description of metric';
    }

    #[Override]
    public function metrics(): Generator {
        yield new Metric(
            42,
            ['label' => 'one value'],
        );
        yield new Metric(
            1337,
            ['label' => 'another value'],
        );
    }
}
```

Este exportador agregará algo como esto en el endpoint `/metrics`:

```
# TYPE nextcloud_myapp_metric gauge
# UNIT nextcloud_myapp_metric units
# HELP nextcloud_myapp_metric Description of metric
nextcloud_myapp_metric{label="one value"} 42
nextcloud_myapp_metric{backend="another value"} 1337
```
````
