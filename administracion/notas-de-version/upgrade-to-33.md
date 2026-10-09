---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cambios al actualizar a Nextcloud 33: requisitos, conectividad, vistas previas MP3, ID Snowflake, endpoint /metrics, agente de usuario y worker de IA."
---
# Actualización a Nextcloud 33

## Resumen

Esta página recoge los cambios que hay que conocer al actualizar a Nextcloud 33: los requisitos del sistema y la nueva URL de prueba de conectividad, las vistas previas de MP3, los ID Snowflake, el endpoint `/metrics` de OpenMetrics, el nuevo agente de usuario de las peticiones salientes y el comando de worker de TaskProcessing. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/release_notes/upgrade_to_33.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Requisitos del sistema

- PHP 8.5 ya es compatible.
- PHP 8.2 queda obsoleto, aunque todavía es compatible.
- PHP 8.1 ya no es compatible.
- Oracle 11g ya no es compatible.
- PostgreSQL 13 ya no es compatible.

Si se configuraron restricciones sobre los dominios con los que se puede contactar en internet, hay que añadir connectivity.nextcloud.com a la lista de permitidos, ya que ahora se usa de forma predeterminada para comprobar la conectividad a internet en lugar de www.nextcloud.com. También puede configurarse cualquier otra URL para usarla en su lugar. Consultar {nc-ref}`connections_to_remote_servers`.

### Vistas previas

El proveedor de vistas previas de archivos MP3, que lee las imágenes de portada incrustadas en los archivos, está desactivado de forma predeterminada por motivos de rendimiento y estabilidad. Consultar {nc-doc}`admin_manual/configuration_files/previews_configuration` para ver cómo activar o desactivar el proveedor de vistas previas.

### ID Snowflake

Esta versión de Nextcloud incluye [ID Snowflake](https://en.wikipedia.org/wiki/Snowflake_ID). Estos ID incluyen el momento de creación del objeto, un ID de secuencia y un ID de servidor. El ID de servidor debe configurarse ahora en el archivo config.php o mediante variables de entorno. Consultar {nc-doc}`admin_manual/configuration_server/config_sample_php_parameters` para más información.

### Endpoint de OpenMetrics

Nextcloud 33 introduce un endpoint `/metrics` que puede integrarse en cualquier sistema OpenMetrics (Prometheus). Por seguridad, de forma predeterminada solo responde en localhost.

Consultar {nc-doc}`admin_manual/configuration_monitoring/index` para más información al respecto.

### Cambio del agente de usuario predeterminado de las peticiones salientes

A partir de esta versión, el agente de usuario predeterminado de las peticiones que hace la instancia pasó de `Nextcloud Server Crawler` a `Nextcloud-Server-Crawler/X.Y.Z`, donde `X.Y.Z` es la versión actual del servidor.

### Comando del worker de TaskProcessing

Antes se indicaba a los administradores que ejecutaran *occ background-job:worker \<JobClass\>* para acelerar el procesamiento de tareas de IA. Esta recomendación ha cambiado: ahora se recomienda ejecutar *occ taskprocessing:worker*, que gestiona mejor la ejecución en paralelo. Asegurarse de actualizar la configuración.

Consultar {nc-doc}`admin_manual/ai/overview` para más información al respecto.
````
