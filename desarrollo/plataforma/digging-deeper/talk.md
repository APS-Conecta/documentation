---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo usar la API pública de Talk desde una app mediante IBroker: comprobar que Talk existe y crear, personalizar y eliminar conversaciones."
---
# Integración con Talk

## Resumen

Esta página explica cómo una app accede a las capacidades de Talk mediante el intermediario `\OCP\Talk\IBroker`: comprobar si Talk está disponible y crear, personalizar y eliminar conversaciones. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/talk.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
[Nextcloud Talk](https://apps.nextcloud.com/apps/spreed) es la solución de chat y de conferencias de video y audio de Nextcloud. Las apps pueden acceder a las capacidades de Talk mediante una API pública.

Toda la comunicación de una app con el backend de Talk se gestiona a través de un *intermediario* `\OCP\Talk\IBroker`. {nc-ref}`Inyectar <dependency-injection>` el intermediario de Talk en la clase para usarlo.

### Comprobar la existencia de Talk

Talk es una app opcional. Tiene que estar instalada y habilitada para poder usarse.

```php
<?php

/** @var \OCP\Talk\IBroker $broker */
if ($broker->hasBackend()) {
    // Do something with it
} else {
    // Hide Talk integration from a user or use other communication channels, if applicable
}
```

### Crear una conversación

Una conversación nueva necesita un nombre y al menos un moderador. De forma predeterminada, esta conversación será privada.

```php
<?php

/** @var \OCP\Talk\IBroker $broker */
/** @var \OCP\IUser $alice */
/** @var \OCP\IUser $bob */
$conversation = $broker->createConversation(
    'Weekly 1:1',
    [$alice, $bob]
);
```

#### Personalizar la conversación

Es posible ajustar los valores predeterminados:

- `setPublic`: hacer pública la conversación (lo que permite que cualquiera con el enlace acceda a la conversación).
- `setMeetingDate` (desde Nextcloud 32.0.9, 33.0.3 y 34.0.0): marcar una conversación como relacionada con una reunión.
  Esto hará que Talk haga caducar automáticamente la conversación 4 semanas (el valor es configurable)
  después de la reunión, salvo que el propietario confirme que la conversación debe mantenerse.

```php
<?php

/** @var \OCP\Talk\IBroker $broker */
/** @var \OCP\IUser $alice */
/** @var \OCP\IUser $bob */
$options = $broker->newConversationOptions();
$options->setPublic();
$options->setMeetingDate(
    $this->timeFactory->getDateTime(new \DateTime('2026-04-07 13:00')),
    $this->timeFactory->getDateTime(new \DateTime('2026-04-07 14:00')),
);

$conversation = $broker->createConversation(
    'Weekly 1:1',
    [$alice, $bob],
    $options
);
```

### Eliminar una conversación

Una conversación se puede eliminar por su id (token).

```php
<?php

/** @var \OCP\Talk\IBroker $broker */
$broker->deleteConversation('abc123');
```
````
