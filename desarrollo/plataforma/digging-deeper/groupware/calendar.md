---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo una app consulta calendarios y eventos, crea eventos y registra backends de recursos y salas para el servidor CalDAV."
---
# Integración con el calendario

## Resumen

Esta página explica cómo una app se integra con los servicios de calendario: consultar objetos de calendario y calendarios mediante el gestor de calendarios, crear eventos y registrar backends de recursos y de salas para el servidor CalDAV. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/groupware/calendar.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
En esta página se puede aprender más sobre la integración con los servicios de calendario de Nextcloud.

### Acceder a calendarios y eventos

(nc-dev-calendar-search)=
#### Objetos de calendario

El contenido de los calendarios se puede consultar en el backend a través del servicio gestor de calendarios. Las consultas siempre se limitan a un principal (usuario), pero pueden seguir otros criterios de búsqueda, como coincidencias de cadenas o rangos de fechas.

{nc-ref}`Inyectar <dependency-injection>` el gestor de calendarios en la clase. Después se pueden usar `newQuery` y `searchForPrincipal` para construir y ejecutar una consulta de búsqueda.

El siguiente ejemplo muestra un caso de uso básico de la API de consultas de calendario, en el que se busca en el calendario de un usuario concreto cualquier evento o tarea dentro de un periodo determinado.

```php
<?php

use OCP\Calendar\IManager;

class MyService {

    /** @var IManager */
    private $calendarManager;

    public function __construct(IManager $calendarManager) {
        $this->calendarManager = $calendarManager;
    }

    public function searchInUserCalendar(string $uid,
                                         string $calendarUri,
                                         DateTimeImmutable $from,
                                         DateTimeImmutable $to): void {
        $principal = 'principals/users/' . $uid;

        // Prepare the query
        $query = $this->calendarManager->newQuery($principal);
        $query->addSearchCalendar($uri);
        $query->setTimerangeStart($from);
        $query->setTimerangeEnd($to);

        // Execute the query
        $objects = $this->calendarManager->searchForPrincipal($query);
    }

}
```

Para conocer otras opciones de consulta, estudiar la interfaz `\OCP\Calendar\ICalendarQuery`.

(nc-dev-calendar-access)=
#### Calendarios

Se puede acceder a los calendarios a través de `IManager`. {nc-ref}`Inyectar <dependency-injection>` el servicio y después usar el método `getCalendarsForPrincipal`.

Se pueden consultar todos los calendarios del principal, omitiendo el segundo argumento, o buscar solo calendarios concretos. Ver los ejemplos a continuación.

```php
<?php

use OCP\Calendar\IManager;

class MyService {

    /** @var IManager */
    private $calendarManager;

    public function __construct(IManager $calendarManager) {
        $this->calendarManager = $calendarManager;
    }

    public function processCalendarData(string $uid): void {
        $principal = 'principals/users/' . $uid;

        // This will find all calendars of the principal
        $calendars = $this->calendarManager->getCalendarsForPrincipal($principal);

        // Work with calendars
    }

    public function processCalendarData(string $uid, string $calendarUri): void {
        $principal = 'principals/users/' . $uid;

        // This will only find specific calendars of the principal
        $calendars = $this->calendarManager->getCalendarsForPrincipal(
            $principal,
            [$calendarUri]
        );

        // Check if the requested calendar was found and work with it
    }

}
```

Los objetos devueltos implementan `\OCP\Calendar\ICalendar`. Estudiar los métodos de la interfaz para descubrir qué datos hay disponibles.

:::{note}
De forma predeterminada, todos los calendarios son solo de lectura; por eso `ICalendar` no ofrece métodos de modificación. Sin embargo, algunos calendarios son modificables y pueden extender además la interfaz `\OCP\Calendar\ICreateFromString`.
:::

### Crear eventos de calendario

Los eventos de calendario se pueden importar desde cadenas ICS sin procesar o construir mediante programación con la interfaz `ICalendarEventBuilder`.
Consultar el siguiente ejemplo para ver ambos métodos en acción.

```php
<?php

use OCP\Calendar\ICalendarEventBuilder;
use OCP\Calendar\ICreateFromString;
use OCP\Calendar\IManager;

class MyService {

    /** @var IManager */
    private $calendarManager;

    public function __construct(IManager $calendarManager) {
        $this->calendarManager = $calendarManager;
    }

    public function createEvent(string $uid): void {
        $principal = 'principals/users/' . $uid;

        // This will find all calendars of the principal
        $calendars = $this->calendarManager->getCalendarsForPrincipal($principal);

        $writableCalendar = null;
        foreach ($calendars as $calendar) {
            if ($calendar instanceof ICreateFromString) {
                $writableCalendar = $calendar;
                break;
            }
        }

        if ($writableCalendar === null) {
            return;
        }

        // Build an event
        $startDate = (new \DateTimeImmutable('now'))
            ->setTimezone(new \DateTimeZone('Europe/Berlin'));
        $endDate = $startDate->add(new \DateInterval('PT1H'));
        $builder = $this->calendarManager->createEventBuilder()
            ->setStartDate($startDate)
            ->setEndDate($endDate)
            ->setSummary('An Event')
            ->setDescription('With a description')
            ->setLocation('Some address') // A URL (of a meeting) would also work
            ->setOrganizer('organizer@domain.com')
            ->addAttendee('user.1@domain.com')
            ->addAttendee('user.2@domain.com', 'User Two');

        // Write the calendar to an event
        $builder->createInCalendar($writableCalendar);

        // Or, serialize it to a string to do something else with it
        $ics = $builder->toIcs();

        // For example, make use of ICreateFromString
        // Make sure to generate a unique filename/UUID for each event
        $writableCalendar->createFromString('edb29d1d-817c-4e43-9d52-cf26dff4be60.ics', $ics);
    }

}
```

### Proveedores de calendario

La integración de groupware de Nextcloud da acceso a los calendarios internos.
Sin embargo, las apps de terceros también pueden proporcionar calendarios individuales.
La sección {nc-ref}`Integración de proveedores de calendario personalizados <calendar-providers>` describe cómo implementar un proveedor dentro del servidor de Nextcloud.

### Recursos

Las apps de Nextcloud pueden proporcionar backends de recursos para el servidor CalDAV de Nextcloud.

Para registrar un backend personalizado, crear una clase que implemente `\OCP\Calendar\Resource\IBackend`.

En el {nc-ref}`método boot de la clase Application de la app <bootstrapping>` se puede obtener la instancia de `\OCP\Calendar\Resource\IManager` y pasar a `registerBackend` el nombre de clase completamente cualificado del backend personalizado.

```php
<?php

use OCP\Calendar\Resource\IManager;

class Application extends App implements IBootstrap {

    public function __construct() {
        parent::__construct('myapp');
    }

    public function register(IRegistrationContext $context): void {
        // ... registration logic goes here ...
    }

    public function boot(IBootContext $context): void {
        /** @var IManager $manager */
        $resourceManager = $serverContainer->get(IManager::class);
        $resourceManager->registerBackend(\OCA\MyApp\ResourceBackend::class);
    }

}
```

:::{note}
Nextcloud consulta los backends registrados solo de forma periódica, mediante un trabajo en segundo plano. Si los recursos no aparecen en el frontend, comprobar que los trabajos cron se ejecutan en la instancia de desarrollo.
:::

### Salas

Las apps de Nextcloud pueden proporcionar backends de salas para el servidor CalDAV de Nextcloud.

Para registrar un backend personalizado, crear una clase que implemente `\OCP\Calendar\Room\IBackend`.

En el {nc-ref}`método boot de la clase Application de la app <bootstrapping>` se puede obtener la instancia de `\OCP\Calendar\Room\IManager` y pasar a `registerBackend` el nombre de clase completamente cualificado del backend personalizado.

```php
<?php

use OCP\Calendar\Room\IManager;

class Application extends App implements IBootstrap {

    public function __construct() {
        parent::__construct('myapp');
    }

    public function register(IRegistrationContext $context): void {
        // ... registration logic goes here ...
    }

    public function boot(IBootContext $context): void {
        /** @var IManager $manager */
        $resourceManager = $serverContainer->get(IManager::class);
        $resourceManager->registerBackend(\OCA\MyApp\RoomBackend::class);
    }

}
```

:::{note}
Nextcloud consulta los backends registrados solo de forma periódica, mediante un trabajo en segundo plano. Si las salas no aparecen en el frontend, comprobar que los trabajos cron se ejecutan en la instancia de desarrollo.
:::
````
