---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo consultar el estado de un grupo de usuarios con IManager de OCP y cómo cambiarlo y revertirlo mediante programación desde una app."
---
# Estado del usuario

## Resumen

Esta página explica cómo una app consulta el estado de un grupo de usuarios con la interfaz `OCP\UserStatus\IManager` y cómo lo cambia y lo revierte mediante programación. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/status.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud permite a los usuarios publicar su estado actual. El estado queda entonces
disponible en varias partes de la interfaz de usuario (p. ej., la lista de participantes de
una sala de Talk).

### Consultar el estado

Con la interfaz *OCP\UserStatus\IManager* es posible consultar
el estado de usuario de un grupo de usuarios.

```php
<?php

namespace OCA\MyGreatApp\Service;

use OCP\UserStatus\IManager as IStatusManager;
use OCP\UserStatus\IUserStatus;

class MyService {
    /** @var IStatusManager $statusManager */
    public $statusManager;

    public function __construct(IStatusManager $statusManager) {
        $this->statusManager = $statusManager;
    }

    /**
     * @param string[] $userIds
     * @return IUserStatus[]
     */
    public function queryStatusForUsers(array $userIds): array {
        return $this->statusManager->getUserStatuses($userIds);
    }
}
```

### Actualizar el estado mediante programación

Una aplicación de Nextcloud puede cambiar el estado del usuario mediante programación. Esta funcionalidad
*setUserStatus* de la interfaz *OCP\UserStatus\IManager* cuando, por ejemplo, un
usuario ejecuta una acción en la interfaz de usuario.

Si el estado debe revertirse con una acción posterior del
usuario, habrá que llamar a *setUserStatus* con *$createBackup = true*.

Después, esto puede revertirse con una llamada a *revertUserStatus* con los mismos
*$messageId* y *$status*.

```php
<?php

namespace OCA\MyGreatApp\Status;

use OCA\MyGreatApp\MyEvents;
use OCA\MyGreatApp\CoolStartEvent;
use OCA\MyGreatApp\CoolEndEvent;
use OCP\UserStatus\IManager as IStatusManager;
use OCP\UserStatus\IUserStatus;

class Listener {
    /** @var IStatusManager $statusManager */
    public $statusManager;

    public function __construct(IStatusManager $statusManager) {
        $this->statusManager = $statusManager;
    }

    public static function register(IEventDispatcher $dispatcher): void {
        $dispatcher->addListener(MyEvents::COOL_EVENT_STARTED, static function (CoolStartEvent $event) {
            /** @var self $listener */
            $listener = \OC::$server->get(self::class);
            $listener->setUserStatus($event);
        });

        $dispatcher->addListener(MyEvents::COOL_EVENT_FINISHED, static function (CoolEndEvent $event) {
            /** @var self $listener */
            $listener = \OC::$server->get(self::class);
            $listener->revertUserStatus($event);
        });
    }

    public function setUserStatus(ModifyParticipantEvent $event): void {
        $this->statusManager->setUserStatus($event->getUserId(), 'meeting', IUserStatus::AWAY, true);
    }

    public function revertUserStatus(ModifyParticipantEvent $event): void {
        $this->statusManager->revertUserStatus($event->getUserId(), 'meeting', IUserStatus::AWAY);
    }
```
````
