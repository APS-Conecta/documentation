---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Acceso a los periodos de ausencia de los usuarios desde una app: la interfaz IAvailabilityCoordinator, los eventos emitidos y la estructura IOutOfOfficeData."
---
# Periodos de ausencia

## Resumen

Esta página describe cómo una app accede a los periodos de ausencia que los usuarios configuran en sus ajustes personales: los métodos de `IAvailabilityCoordinator`, los eventos que emite la función de ausencia y la estructura de datos común `IOutOfOfficeData`. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/out_of_office.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{versionadded} 28.0
:::

Desde Nextcloud 28, los usuarios pueden establecer sus periodos de ausencia en sus ajustes personales. Las apps de Nextcloud
pueden acceder a los datos y modificarlos mediante OCP, y los clientes, mediante OCS. Las apps de Nextcloud también pueden
escuchar los eventos que emite la función de ausencia.

La API de OCS está documentada en la {nc-ref}`sección de clientes <ocs-out-of-office-api>`.

### Acceder a los datos desde una app de Nextcloud mediante OCP

Se puede acceder a los datos de ausencia a través de la interfaz *OCP\\User\\IAvailabilityCoordinator*.
Proporciona los siguientes métodos:

```php
/**
 * Check if the feature is enabled on this instance
 */
public function isEnabled(): bool;
```

```php
/**
 * Get the user's ongoing out-of-office data, if any
 */
public function getCurrentOutOfOfficeData(IUser $user): ?IOutOfOfficeData;
```

```php
/**
 * Reset the absence cache to null
 */
public function clearCache(string $userId): void;
```

```php
/**
 * Is the absence in effect at this moment
 */
public function isInEffect(IOutOfOfficeData $data): bool;
```

### Escuchar eventos

Todos los eventos tienen un método común para recuperar los datos del periodo de ausencia afectado.

```php
public function getData(): IOutOfOfficeData;
```

La función de ausencia emite los siguientes eventos:

- `OCP\User\Events\OutOfOfficeScheduledEvent` Si se programa un nuevo periodo de ausencia para un
  usuario. Este evento solo se emite una vez, cuando antes no había ningún periodo de ausencia.
- `OCP\User\Events\OutOfOfficeChangedEvent` Si se modifican los datos de ausencia de un usuario.
- `OCP\User\Events\OutOfOfficeDeletedEvent` Si se elimina el periodo de ausencia de un usuario.
- `OCP\User\Events\OutOfOfficeStartedEvent` Si comienza un periodo de ausencia. Este evento solo se
  emite una vez, y no si se crea un periodo que comienza en el pasado.
- `OCP\User\Events\OutOfOfficeEndedEvent` Si termina un periodo de ausencia. Este evento solo se
  emite una vez, y no si se crea un periodo que termina en el pasado.

### Estructura de datos común

La API de OCP y los eventos emitidos comparten una estructura de datos común, *OCP\\User\\IOutOfOfficeData*. Las
fechas de inicio y de fin se representan como marcas de tiempo UNIX.

```php
interface IOutOfOfficeData extends JsonSerializable {
    /**
     * Get the unique token assigned to the current out-of-office event
     */
    public function getId(): string;

    public function getUser(): IUser;

    /**
     * Get the accurate out-of-office start date
     *
     * This event is not guaranteed to be emitted exactly at start date
     */
    public function getStartDate(): int;

    /**
     * Get the (preliminary) out-of-office end date
     */
    public function getEndDate(): int;

    /**
     * Get the short summary text displayed in the user status and similar
     */
    public function getShortMessage(): string;

    /**
     * Get the long out-of-office message for auto responders and similar
     */
    public function getMessage(): string;

    /**
     * Get the replacement user id for auto responders and similar
     */
    public function getReplacementUserId(): ?string;

    /**
     * Get the replacement user displayName for auto responders and similar
     */
    public function getReplacementUserDisplayName(): ?string;
}
```

Puede serializarse en un objeto JSON con la siguiente estructura:

```
{
    id: string,
    userId: string,
    startDate: int,
    endDate: int,
    shortMessage: string,
    message: string,
    replacementUserId: string|null,
    replacementUserDisplayName: string|null
}
```
````
