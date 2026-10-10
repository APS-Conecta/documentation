---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo una app registra calendarios propios: ICalendarProvider de solo lectura o con escritura, datos iMIP, acceso CalDAV y las clases heredadas de Sabre."
---
(nc-dev-calendar-providers)=
# Integración de proveedores de calendario personalizados

## Resumen

Esta página explica cómo una app registra calendarios además de los internos: con la interfaz de la API (`ICalendarProvider`, escritura, datos iMIP y acceso CalDAV) o con el acceso heredado a las clases de Sabre, mediante las clases de objeto de calendario, de calendario y de plugin. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/groupware/calendar_provider.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Las apps de Nextcloud pueden registrar calendarios además de los calendarios internos del backend CalDAV de Nextcloud. Los calendarios solo se cargan bajo demanda; por eso se usa un mecanismo de proveedor de carga diferida.

Se puede acceder a los calendarios de dos maneras: la forma heredada usa directamente las clases de la app DAV para interactuar con Sabre. Para simplificar el acceso, el equipo de {vendor}`Nextcloud` ha emprendido un esfuerzo para incluir la interfaz de Sabre en una interfaz integrada en Nextcloud. Sin embargo, aquí hay algunas carencias que aún no están terminadas.

Si se trabaja en una app nueva y se quiere proporcionar un calendario, comprobar si el código integrado cumple los requisitos. Si es así, puede ser más sencillo usarlo que usar la interfaz heredada de Sabre.

Todos los fragmentos llevan el prefijo `<?php` para dejar claro que sigue siendo código php (y para activar el resaltado del código en este documento). Por supuesto, no hace falta repetir las etiquetas de apertura.

### Registrar el calendario con la interfaz de la API de Nextcloud

En el momento de escribir esto, el soporte del calendario de Nextcloud para proporcionar una app personalizada es limitado. Los calendarios de solo lectura son posibles, mientras que los calendarios con escritura requieren algo más de trabajo por parte de quien desarrolla la app.

#### Soporte de solo lectura

Para proporcionar uno o varios calendarios hay que escribir una clase que implemente la interfaz `OCP\Calendar\ICalendarProvider`.

```php
<?php

use OCP\Calendar\ICalendarProvider;

class CalendarProvider implements ICalendarProvider {

    public function getCalendars(string $principalUri, array $calendarUris = []): array {
        $calendars = [];
        // TODO: Run app specific logic to find calendars that belong to
        //       $principalUri and fill $calendars

        // The provider can simple return an empty array if there is not
        // a single calendar for the principal URI
        if (empty($calendars)) {
            return [];
        }

        // Return instances of \OCP\Calendar\ICalendar
        return $calendars;
    }
}
```

Después, esta clase `CalendarProvider` se registra en el {nc-ref}`método register de la clase Application de la app <bootstrapping>` con `$context->registerCalendarProvider(CalendarProvider::class);`.

#### Soporte de escritura

Los calendarios que solo devuelven *ICalendar* son implícitamente de solo lectura. Si los calendarios de la app admiten escritura, se puede implementar la interfaz `ICreateFromString`. Esta permite que otras apps escriban objetos de calendario en el calendario pasando los datos iCalendar sin procesar como cadena.

```php
<?php

use OCP\Calendar\ICreateFromString;

class CalendarReadWrite implements ICreateFromString {

    // ... other methods from ICalendar still have to be implemented ...

    public function createFromString(string $name, string $calendarData): void {
        // Write data to your calendar representation
    }

}
```

#### Gestión de datos iMIP

Se puede implementar la interfaz `IHandleIMipMessage` para procesar los datos iMIP que se reciben en un cliente y se quieren pasar al backend para su procesamiento.

Hay que tener en cuenta algunas consideraciones de seguridad. En el [RFC](https://www.rfc-editor.org/rfc/rfc6047) se encuentra más información sobre ellas y sobre las condiciones que deben cumplirse para que se procesen los datos iMIP.

```php
<?php

use OCP\Calendar\IHandleIMipMessage;

class HandleIMipMessage implements IHandleIMipMessage {

    public function handleIMipMessage(string $name, string $calendarData): void {
        // Validation and write to your calendar representation
    }

}
```

#### Acceso mediante CalDAV

:::{versionadded} 27.0.0
:::

Al igual que con los calendarios integrados, se puede acceder mediante CalDAV a los calendarios que proporciona `ICalendarProvider`. Por eso, los permisos de `ICalendar` se asignan automáticamente al objeto DAV.
También se admite la escritura. Tener en cuenta que, actualmente, la eliminación de entidades se implementa poniendo la entidad en estado cancelado y pasándola al método `createFromString`.

### Acceso heredado a las clases de Sabre

Para que una app pueda publicar entradas de calendario, tiene que interactuar con el servidor WebDAV Sabre integrado en el núcleo. Esto impone una estructura bien definida que la app debe usar como interfaz:

Hay clases e interfaces para conectarse con el servidor WebDAV. Para combinar las interfaces requeridas, la app DAV prepara clases abstractas que centralizan estas solicitudes de acceso. Para que una app proporcione un calendario personalizado, esto significa que en realidad hay que definir tres clases e implementar todos los métodos heredados:

1. Una clase de *objeto de calendario* da acceso a elementos individuales de un calendario, como citas/eventos o tareas/pendientes.
2. Una clase de *calendario* da acceso a un único calendario que contiene todos los *objetos de calendario* correspondientes.
3. Una clase de *plugin* que registra el calendario en el resto del sistema CalDAV.

:::{note}
Tener en cuenta que esta sección usa las clases de `\OCA\DAV`, que por definición no es una interfaz pública. Cuando se presente una solución central, esto debería actualizarse.
:::

Tener en cuenta que CalDAV se basa en WebDAV. WebDAV es una forma estandarizada de acceder a archivos a través de una conexión de red. Por eso, al manejar calendarios (y contactos) se aplican las mismas nociones. Un calendario se corresponde con una carpeta, mientras que un evento de un calendario se corresponde con un archivo (relativo). Tener esto presente permite comprender más rápido los principios de la API.

En las secciones siguientes se trata cada una de estas partes por separado. Como hay bastantes métodos que implementar, primero se presenta la estructura general de las clases sin implementar los métodos abstractos. Después, los métodos se tratan en grupos para facilitar la lectura.

### La clase del objeto de calendario

Tiene que haber una clase que represente una única entrada de un calendario. El nombre de dicha clase es arbitrario; sin embargo, debe implementar las interfaces `\Sabre\CalDAV\ICalendarObject` y `\Sabre\CalDAV\IACL`. La estructura básica es la siguiente:

```php
<?php

namespace OCA\YourAppName\DAV;

class CalendarObject implements \Sabre\CalDAV\ICalendarObject, \Sabre\DAVACL\IACL {
    /** @var Calendar */
    private $calendar;
    /** @var string */
    private $name;

    /**
    * CalendarObject constructor.
    *
    * @param Calendar $calendar
    * @param string $name
    */
    public function __construct(Calendar $calendar, string $name) {
        $this->calendar = $calendar;
        $this->name = $name;
    }

    // Implement all remaining functions here ...
}
```

La clase `Calendar` es la clase, definida en la sección siguiente, que representa un calendario completo.

La clase del calendario pasa como argumentos del constructor el objeto del calendario y el nombre de la entrada. Por ahora, se guardan en atributos para usarlos más adelante.

#### Información básica del evento -- INode

Hay algunos métodos básicos que deben implementarse en cada instancia de objeto de calendario. Están definidos en `\Sabre\DAV\INode`.

##### Eliminación de entradas

En este ejemplo no se permite eliminar eventos del calendario. De lo contrario, habría que actualizar el backend.

```php
<?php

function delete() {
    throw new \Sabre\DAV\Exception\Forbidden('This calendar-object is read-only');
}
```

##### Obtener el nombre de un evento

El nombre del evento se puede obtener con el método `getName`. Aquí simplemente se devuelve el nombre guardado en los atributos.

```php
<?php

function getName() {
    return $this->name;
}
```

##### Actualizar el nombre de un evento

Actualizar el nombre no se considera una buena idea, así que se cancela con una excepción. Si esto debiera ser posible, también se podría actualizar el backend.

```php
<?php

function setName($name) {
    throw new \Sabre\DAV\Exception\Forbidden('This calendar-object is read-only');
}
```

##### Obtener la marca de tiempo de la última modificación

El método `getLastModified` debe devolver una marca de tiempo unix que represente la fecha de modificación del evento. El cliente puede usarla para actualizar de forma selectiva cualquier estructura.

Se permite devolver `null` para indicar que no se puede obtener ninguna marca de tiempo de modificación.

```php
<?php

function getLastModified() {
    return time();
}
```

#### Datos del evento -- IFile

Los datos principales de un objeto de calendario se almacenan en la interfaz `\Sabre\DAV\IFile`. Hay algunos métodos adicionales que ayudan durante el uso.

##### Tamaño del contenido del evento

Una función auxiliar es el método `getSize`, que obtiene el número de bytes de la representación de esta entrada de calendario. Este método no hace nada especial.

```php
<?php

function getSize() {
    return strlen($this->get());
}
```

##### Obtener una etiqueta única para una versión del evento

El E-Tag se puede calcular con el método `getETag`. Tener en cuenta que el E-Tag devuelto debe incluir las comillas dobles como parte de la cadena devuelta.

También se puede devolver `null` para indicar que el E-Tag no se puede calcular de forma eficaz.

```php
<?php

function getETag() {
    return '"' . md5($this->get()) . '"';
}
```

(nc-dev-calendar-provider-content-type)=
##### Devolver el tipo de contenido

También hay que proporcionar el tipo de contenido de la entrada de calendario.

```php
<?php

function getContentType() {
    return 'text/calendar; charset=utf-8';
}
```

##### Obtener el contenido de un evento de calendario

La entrada de calendario propiamente dicha se obtiene con el método `get`. Por supuesto, debe coincidir con el {nc-ref}`tipo de contenido <calendar-provider-content-type>` declarado. Consultar también la [documentación oficial](https://www.rfc-editor.org/rfc/rfc5545) sobre los calendarios vcal para conocer el formato posible.

```php
<?php

function get() {
    $name = $this->getName();
    return <<<EOF
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Nextcloud/DavCalendarDemo//NONSGML v1.0//EN
BEGIN:VEVENT
UID:$name@example.com
DTSTAMP:20200101T170000Z
DTSTART:20200130T170000Z
DTEND:20200130T180000Z
SUMMARY:Example $name
END:VEVENT
END:VCALENDAR
EOF;
}
```

##### Actualizar el contenido de un evento de calendario

Es posible que el cliente intente actualizar el evento con el método `put`.

En este ejemplo, el evento se considera de solo lectura, así que se lanza una excepción si un cliente intenta actualizarlo. Si se tiene previsto permitir que los clientes actualicen eventos, hay que implementar el análisis, la validación y el guardado de los datos.

```php
<?php

function put($data) {
    throw new \Sabre\DAV\Exception\Forbidden('This calendar-object is read-only');
}
```

#### Restricciones de acceso -- IACL

Las entidades del calendario se completan con un conjunto de reglas de acceso. Estas permiten a un cliente saber si ciertas acciones están permitidas o no.

##### Propiedad

El propietario y los grupos correspondientes de la entrada de calendario se pueden especificar como URI. Si no hay propietario ni grupo, se debe devolver un valor `null`.

Como normalmente el calendario pertenece a un usuario y las entradas individuales al calendario, en este ejemplo las entradas no necesitan un usuario propio. Para enfoques más complejos, ver la documentación oficial de CalDAV.

```php
<?php

function getOwner() {
    return null;
}

function getGroup() {
    return null;
}
```

##### Proporcionar privilegios individualmente

El método `getSupportedPrivilegeSet` se puede usar para consultar los privilegios, es decir, para consultar la entrada por privilegios específicos. Si se devuelve `null`, se asume el conjunto de privilegios predeterminado.

Para este ejemplo y la mayoría de los demás casos, `null` es una buena opción.

```php
<?php

function getSupportedPrivilegeSet() {
    return null;
}
```

##### Obtener las ACL instaladas actualmente

Las reglas de acceso reales se obtienen con `getACL`. En este ejemplo se asume que las ACL se heredan del calendario. Por eso, el cálculo se delega a la clase del calendario.

```php
<?php

function getACL() {
    return $this->calendar->getACL();
}
```

##### Actualizar las ACL del calendario

La actualización de las ACL se podría gestionar con el método `setACL`. Este ejemplo asume ACL constantes, así que se rechaza lanzando una excepción.

```php
<?php

function setACL(array $acl) {
    throw new \Sabre\DAV\Exception\Forbidden('Setting ACL is not supported on this node');
}
```

### La clase del calendario

Cada calendario debe representarse con su propia clase. Al igual que con la clase de entidad del calendario, se puede elegir cualquier nombre para la clase. Extender la clase `OCA\DAV\CalDAV\Integration\ExternalCalendar`:

A continuación se muestra el constructor básico de la clase y algunos atributos que se almacenan. Algunas de las URI proporcionadas se guardan internamente para usarlas más adelante.

El constructor padre necesita el nombre de la app como primer parámetro. Por eso se llama explícitamente en la primera línea del constructor con el nombre correcto de la app (`yourappname` en este ejemplo).

Algunos de los métodos que hay que implementar son similares a los anteriores de la clase de entidad del calendario. Sin embargo, requieren implementaciones distintas, así que en los párrafos siguientes se repasan todos los métodos una vez.

```php
<?php
namespace OCA\YourAppName\DAV;

use OCA\DAV\CalDAV\Integration\ExternalCalendar;
use OCA\DAV\CalDAV\Plugin;
use Sabre\CalDAV\Xml\Property\SupportedCalendarComponentSet;
use Sabre\DAV\PropPatch;

class Calendar extends ExternalCalendar {
    /** @var string */
    private $principalUri;
    /** @var string */
    private $calendarUri;

    /**
    * Calendar constructor.
    *
    * @param string $principalUri
    * @param string $calendarUri
    */
    public function __construct(string $principalUri, string $calendarUri) {
        parent::__construct('yourappname', $calendarUri);

        $this->principalUri = $principalUri;
        $this->calendarUri = $calendarUri;
    }

    // The other methods come here ...
}
```

#### Información básica del calendario -- INode

La interfaz `\Sabre\DAV\INode` tiene dos métodos que debe implementar el código de la app. Los demás métodos de la interfaz ya están implementados en la clase `\OCA\DAV\CalDAV\Integration\ExternalCalendar`.

##### Eliminación de calendarios

El calendario no debería eliminarse mediante la interfaz CalDAV. Por eso, aquí no se hace nada.

```php
<?php

function delete() {
    return null;
}
```

##### Obtener la marca de tiempo de modificación

La hora de la última modificación del calendario permite a los clientes optimizar sus solicitudes. Este método debería devolver la marca de tiempo unix correspondiente.

Como alternativa, se puede proporcionar el valor `null` como valor de retorno. Esto indica que por el momento no se conoce la hora de la última modificación.

```php
<?php

function getLastModified() {
    return time();
}
```

#### Entradas del calendario -- ICollection

La interfaz `\Sabre\DAV\ICollection` define métodos para acceder a los hijos del nodo actual. En los calendarios, los hijos son de hecho los eventos almacenados en el calendario. De nuevo, algunos métodos ya están cubiertos, así que aquí solo se implementan los métodos requeridos.

Todas las entradas de calendario tienen un nombre único. Es simplemente una cadena. Normalmente se nombran como archivos `.ics`. Los métodos que se tratan en esta sección necesitan este nombre como parámetro para identificar el evento sobre el que operan.

##### Crear eventos de calendario nuevos

El método `createFile` se usa para almacenar eventos nuevos en el calendario. Se podría devolver un ETag del evento de calendario como una cadena que contenga comillas dobles, como se esboza en el comentario.

```php
<?php

function createFile($name, $data = null) {
    return null;
    // return "\"$etag\"";
}
```

##### Comprobar la existencia de eventos

El método `childExists` comprueba si un elemento determinado está presente en el calendario.

```php
<?php

function childExists($name) {
    // Check if the value of $name represents a valid calendar entry name.
    // You can check your backend(s) for the child
    // then return a boolean
}
```

##### Obtener una entrada del calendario

El método `getChild` empaqueta una entrada de calendario en su propio objeto, como se describió antes.

El método permite solicitar una entrada concreta y extraerla del calendario.

```php
<?php

function getChild($name) {
    if ($this->childExists($name)) {
        return new CalendarObject($this, $name);
    }
}
```

##### Obtener todas las entradas del calendario

Por último, está el método `getChildren` para obtener todos los eventos de un calendario.

:::{note}
Por simplicidad, aquí solo se usa un array estático. Sin embargo, se podría consultar una base de datos o el sistema de archivos para obtener un número variable de entradas del calendario.
:::

```php
<?php

function getChildren() {
    // Get the list of calendar entries
    $children = ['test.ics'];

    // Obtain the calendar objects for each of them
    $children = array_map(function ($childName) using ($this) { return $this->getChild($childName); });

    return $children;
}
```

#### Consultar el calendario -- ICalendarObjectContainer

Sería muy costoso en recursos solicitar todos los eventos de un calendario solo para descartar después la mayoría durante el filtrado. En su lugar, el cliente solicita un conjunto determinado de objetos (como los de los últimos 90 días) y el servidor hace el filtrado. Esto se consigue con la interfaz `\Sabre\CalDAV\ICalendarObjectContainer`.

Su único método devuelve una lista de entradas. A diferencia del método `getChildren()`, las entradas no se empaquetan en sus propios objetos. El cliente es responsable de hacerlo mediante `getChild()` en un proceso aparte.

```php
<?php

function calendarQuery(array $filters) {
    // In a real implementation this should actually filter
    return ['test.ics'];
}
```

#### Gestionar el acceso al calendario -- IACL

CalDAV define algunas propiedades relevantes para la seguridad. Se implementan mediante `\Sabre\DAVACL\IACL`. Las ACL definen quién (en términos de URI de principales) puede hacer qué en el calendario.

##### Obtener el propietario de un calendario

El método `getOwner` obtiene la URI del principal. Aquí se usa el valor almacenado que se proporcionó en el constructor.

```php
<?php

function getOwner() {
    return $this->principalUri;
}
```

##### Obtener los grupos del calendario

Para devolver todas las URI de grupos del usuario está el método `getGroups`. Aquí se asume que no hay grupos.

```php
<?php

function getGroup() {
    return [];
}
```

##### Obtener las reglas de acceso del calendario

El método `getACL` debe devolver la ACL definida para este calendario. Para las definiciones exactas, ver la documentación de Sabre. En el momento de escribir esto, eran:

| entrada | valores | descripción |
|---|---|---|
| `principal` | URI del principal | El rol o la persona que intenta acceder al calendario |
| `privilege` | `{DAV:}read`, `{DAV:}write` | Si el rol puede leer o escribir |
| `protected` | `true`, `false` | si es `true`, esta regla no se puede cambiar |

```php
<?php

function getACL() {
    return [
        [
            'privilege' => '{DAV:}read',
            'principal' => $this->getOwner(),
            'protected' => true,
        ],
        [
            'privilege' => '{DAV:}read',
            'principal' => $this->getOwner() . '/calendar-proxy-write',
            'protected' => true,
        ],
        [
            'privilege' => '{DAV:}read',
            'principal' => $this->getOwner() . '/calendar-proxy-read',
            'protected' => true,
        ],
    ];
}
```

##### Establecer las reglas de acceso del calendario

En este ejemplo no se permite actualizar las reglas de la ACL. Por eso, se lanza una excepción si el cliente intenta hacerlo con el método `setACL`.

```php
<?php

function setACL(array $acl) {
    throw new \Sabre\DAV\Exception\Forbidden('Setting ACL is not supported on this node');
}
```

##### Obtener los privilegios asociados al calendario

Los privilegios admitidos se pueden sobrescribir implementando el método `getSupportedPrivileges`. Si se devuelve `null`, se usa el valor predeterminado de Sabre, que sirve para muchas tareas. Para más información, consultar también la [documentación de Sabre](https://sabre.io/dav/acl/).

```php
<?php

function getSupportedPrivilegeSet() {
    return null;
}
```

#### Propiedades del calendario externo -- IProperties

Se pueden especificar algunas propiedades del calendario. La interfaz CalDAV permite una interfaz bastante genérica. Habrá que consultar los detalles del estándar CalDAV para saber qué propiedades tienen sentido en cada caso.

##### Obtener las propiedades

Las propiedades se obtienen con el método `getProperties`.

Aquí se proporciona un esbozo básico de las propiedades del calendario. Se trata de un nombre básico, un color y el ajuste que permite tanto eventos (`VEVENT`) como tareas (`VTODO`) en el calendario.

```php
<?php

function getProperties($properties) {
    // A backend should provide at least minimum properties
    return [
        '{DAV:}displayname' => 'Dav Example Calendar: ' . $this->calendarUri,
        '{http://apple.com/ns/ical/}calendar-color'  => '#565656',
        '{' . Plugin::NS_CALDAV . '}supported-calendar-component-set' => new SupportedCalendarComponentSet(['VTODO', 'VEVENT']),
    ];
}
```

##### Actualizar las propiedades

Este método debe implementarse para satisfacer a PHP, pero se puede dejar vacío, ya que lo más probable es que el núcleo se encargue de ello.

```php
<?php

function propPatch(PropPatch $propPatch) {
    // We can just return here and let oc_properties handle everything
}
```

### La clase del plugin del calendario

La última clase que hay que implementar es la clase de *plugin*.

La clase del plugin del calendario debe implementar la interfaz `\OCA\DAV\CalDAV\Integration\ICalendarProvider`, que define algunos métodos para consultar la lista de calendarios que puede proporcionar una app.

El método `getAppId` devuelve el nombre de la app.

El método `fetchAllForCalendarHome` devuelve una lista de todos los *Calendars* que conoce la app.

Tener en cuenta que `principalUri` lo pasa quien llama, mientras que `calendarUri`, en el constructor de la instancia del calendario, es una URI (relativa) (cadena) que identifica el calendario de forma única. Después, la URI se puede usar en la clase del calendario para extraer las entradas correspondientes que deberían estar presentes en el calendario.

La función `hasCalendarInCalendarHome` comprueba si existe una combinación determinada de `principalUri` y `calendarUri`. Aquí simplemente está fijada en el código a exactamente un calendario, pero una implementación propia debería hacer comprobaciones más estrictas.

Por último, hay una función para consultar una única instancia de calendario mediante `getCalendarInCalendarHome`. Devuelve una única instancia de calendario, o `null` si no se encuentra ningún calendario coincidente.

```php
<?php
namespace OCA\YourAppName\DAV;

use OCA\DAV\CalDAV\Integration\ExternalCalendar;
use OCA\DAV\CalDAV\Integration\ICalendarProvider;

class CalendarPlugin implements ICalendarProvider {

    public function getAppId(): string {
        return 'yourappname';
    }

    public function fetchAllForCalendarHome(string $principalUri): array {
        return [
            new Calendar($principalUri, 'my-calendar-1234'),
        ];
    }

    public function hasCalendarInCalendarHome(string $principalUri, string $calendarUri): bool {
        return $calendarUri === 'my-calendar-1234';
    }

    public function getCalendarInCalendarHome(string $principalUri, string $calendarUri): ?ExternalCalendar {
        if ($this->hasCalendarInCalendarHome($principalUri, $calendarUri)) {
            return new Calendar($principalUri, $calendarUri);
        }

        return null;
    }
}
```

### Registrar el proveedor de calendario

Como último paso, hay que registrar el proveedor de calendario en el `info.xml` de la app. Con todos estos pasos hechos, el calendario o los calendarios deberían verse en la app de calendario y en la interfaz CalDAV del núcleo.

```xml
<sabre>
    <calendar-plugins>
        <plugin>OCA\YourAppName\DAV\CalendarPlugin</plugin>
    </calendar-plugins>
</sabre>
```
````
