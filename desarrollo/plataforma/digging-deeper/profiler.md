---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo obtener, activar, desactivar y usar la app del perfilador para detectar problemas de rendimiento, y cómo ampliarla con un DataCollector propio."
---
# Perfilador

## Resumen

Esta página explica cómo obtener, activar, desactivar y usar la app del perfilador integrado para identificar problemas de rendimiento, qué muestran sus vistas y cómo ampliarla con un `DataCollector` propio. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/profiler.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud ofrece un perfilador integrado que puede ayudar a identificar problemas de rendimiento en una aplicación propia para Nextcloud. Esta funcionalidad está disponible a partir de Nextcloud 24.

### Obtener la app

La aplicación del perfilador está disponible en [GitHub](https://github.com/nextcloud/profiler); hay que clonar la rama stableX si se usa Nextcloud X, o master si se usa la última versión de desarrollo de Nextcloud.

```bash
major_version=$(sudo -E -u www-data php occ version 2>&1 | awk -F'[. ]' '{print $2;exit}')
cd apps/
git clone --branch stable$major_version https://github.com/nextcloud/profiler.git
cd profiler
cd ../..
```

### Activar la app

:::{warning}
No ejecutar esta aplicación en producción. Ralentiza considerablemente el servidor, ya que recopilar información de perfilado consume mucha CPU y memoria.
:::

Para activar la app, se pueden ejecutar los siguientes comandos:

```bash
npm ci && npm run build
occ app:enable profiler
occ profiler:enable # This will also enable the debug mode if not already enabled
```

### Desactivar la app

```bash
occ profiler:disable
occ config:system:set debug --value false --type bool # to also disable the debug mode
```

### Usar la app

Cuando está activada, la aplicación del perfilador inyecta una barra de herramientas en la parte inferior de la pantalla. Esta barra de herramientas proporciona información sobre la solicitud HTTP actual, el tiempo que tardó en ejecutarse, cuántas solicitudes a la base de datos y a LDAP hizo y con qué frecuencia acertó la caché; además, la barra de herramientas sigue las solicitudes XHR creadas por el frontend de JavaScript.

Se puede pasar el cursor por encima de la información de la barra de herramientas para mostrar información más detallada, y también hacer clic en la barra de herramientas para mostrar toda la información recopilada.

Por el momento hay 5 vistas:

1. La vista general de solicitud y respuesta
2. La vista de consultas a la base de datos
3. La vista de eventos
4. La vista de consultas LDAP
5. La vista de caché

#### La vista general de solicitud y respuesta

Esta vista ofrece información general sobre la solicitud. Por ejemplo, qué controlador y qué método se usaron, cuáles fueron las cabeceras de la respuesta, los parámetros de la solicitud, ...

#### La vista de consultas a la base de datos

Esta vista ofrece una lista de todas las consultas a la base de datos realizadas para la solicitud y cuánto tiempo tardó la base de datos en ejecutarlas. Además, también se puede explicar la consulta para ver si se usó un índice, y ver la traza de llamadas para entender mejor por qué se ejecutó la consulta.

Es importante mantener al mínimo el número de consultas ejecutadas, ya que la base de datos suele ser un factor limitante en una instalación de Nextcloud. En particular, intentar evitar el [problema N+1](https://stackoverflow.com/questions/97197/what-is-the-n1-selects-problem-in-orm-object-relational-mapping), ya que puede ser muy lento en una instancia grande de Nextcloud, y asegurarse de que las consultas usen índices de la base de datos cuando sea posible.

#### La vista de LDAP

Esta vista es muy similar a la vista de consultas a la base de datos y muestra todas las consultas a la base de datos.

#### La vista de eventos

Esta vista muestra todos los eventos registrados y permite determinar en qué parte del programa se dedica más tiempo.

#### La vista de caché

Esta vista muestra todos los accesos a la caché. Permite detectar aciertos y fallos de la caché, así como hacerse una idea del tiempo dedicado a Redis.

### Contribuir

Las contribuciones para mejorar el perfilador siempre son bienvenidas. Algún trabajo futuro podría incluir una forma de mostrar las consultas a Redis y no solo dar una estadística de ellas. Y podrían recopilarse más tipos de datos, p. ej., solicitudes HTTP a API externas, llamadas IMAP de la app Correo, uso del servicio de envío de correo, ...

Para ampliar la app del perfilador, hay que proporcionar un *DataCollector* propio.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\DataCollector;

use OC\AppFramework\Http\Request;
use OCP\AppFramework\Http\Response;
use OCP\DataCollector\AbstractDataCollector;

class MyAppDataCollector extends AbstractDataCollector {
    public function getName(): string {
        return 'myappcollector'; // default to the class' name
    }

    public function collect(Request $request, Response $response, \Throwable $exception = null): void {
         $this->data = [
             'mydata' => 42
        ];
    }
}
```

También hay que registrar el *DataCollector* en el método *boot* de la app:

```php
<?php

declare(strict_types=1);

class Application extends App implements IBootstrap {
    public function boot(IBootContext $context): void {
        $server = $context->getServerContainer();

        /** @var IProfiler $profiler */
        $profiler = $server->get(IProfiler::class);
        $profiler->add(new MyAppDataCollector());
```

Se pueden encontrar algunos ejemplos en el [repositorio git de la app del perfilador](https://github.com/nextcloud/profiler/tree/master/lib/DataCollector).
````
