---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Endpoint /metrics de OpenMetrics en Nextcloud: qué clientes pueden consultarlo y cómo omitir métricas en config.php."
---
# Monitoreo

## Resumen

Esta página describe, para quienes administran el servidor, el endpoint `/metrics` de OpenMetrics que expone Nextcloud: cómo permitir su consulta a otros clientes y cómo desactivar métricas concretas.

````{upstream} admin_manual/configuration_monitoring/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

### OpenMetrics

:::{versionadded} 33
:::

Nextcloud expone un endpoint `/metrics`. De forma predeterminada, solo responde en localhost.
Este comportamiento puede cambiarse con `openmetrics_allowed_clients`

```
'openmetrics_allowed_clients' => [
  '192.168.0.0/16',
],
```

:::{warning}
Asegurarse de que este endpoint no sea accesible para cualquiera, ya que podría generar cierta carga en el servidor.
:::

El contenido de este endpoint puede consultarse con el siguiente comando:

```
curl "https://your.domain/metrics"
```

Si por algún motivo se quieren desactivar algunas métricas (p. ej., si tardan demasiado en generarse), pueden desactivarse añadiendo el nombre de su clase en `openmetrics_skipped_classes`

```
'openmetrics_skipped_classes' => [
  'OC\OpenMetrics\Exporters\FilesByType',
],
```

:::{seealso}
Consultar {nc-doc}`admin_manual/configuration_server/config_sample_php_parameters` para más información
:::
````
