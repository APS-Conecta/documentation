---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo integrar una app en User migration: implementar un migrador que exporte e importe los datos de la app de un usuario y registrarlo en el arranque."
---
# Migración de usuarios

## Resumen

Esta página explica cómo una app se integra en la app User migration: implementar un migrador con `IMigrator` (y, si es posible, `ISizeEstimationMigrator`) que exporte e importe los datos de la app de un usuario, y registrarlo durante el arranque de la app. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/user_migration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Se puede instalar la [app User migration](https://apps.nextcloud.com/apps/user_migration)
para permitir la migración de los datos de los usuarios.

Quienes desarrollan apps pueden integrarse en User migration y ofrecer formas de exportar
e importar los datos de la app de un usuario. Hay que tener en cuenta que esto no debe usarse
como herramienta de copia de seguridad y restauración, ya que quienes desarrollan apps deben evitar borrar
datos existentes del usuario durante la migración. Para más información, consultar
[esta discusión](https://github.com/nextcloud/user_migration/discussions/1090)
y también
[esta incidencia](https://github.com/nextcloud/user_migration/issues/1096).

### Registrar un migrador

Un migrador se representa con una clase que implementa la interfaz
`OCP\\UserMigration\\IMigrator`. Esta clase se instancia
cada vez que comienza una exportación o una importación de un usuario.
Si es posible, también debe implementar `OCP\UserMigration\ISizeEstimationMigrator`
y devolver una estimación del tamaño en el método `getEstimatedExportSize`.
Se puede usar el trait `OCP\UserMigration\TMigratorBasicVersionHandling` para la gestión básica de versiones;
en ese caso, la versión se guarda en $this->version (por defecto, 1) y se prohíbe importar desde una versión más reciente.
Si se prefiere, se pueden implementar `getVersion` y `canImport` en su lugar.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\UserMigration;

use OCA\MyApp\AppInfo\Application;
use OCA\MyApp\IMyAppManager;
use OCP\IL10N;
use OCP\IUser;
use OCP\UserMigration\IExportDestination;
use OCP\UserMigration\IImportSource;
use OCP\UserMigration\IMigrator;
use OCP\UserMigration\ISizeEstimationMigrator;
use OCP\UserMigration\TMigratorBasicVersionHandling;
use OCP\UserMigration\UserMigrationException;
use Symfony\Component\Console\Output\OutputInterface;
use Throwable;

class MyAppMigrator implements IMigrator, ISizeEstimationMigrator {
  use TMigratorBasicVersionHandling;

  private const PATH_ROOT = Application::APP_ID . '/';

  private const PATH_MYAPP_FILE = MyAppMigrator::PATH_ROOT . 'myapp.json';

  public function __construct(
    private IMyAppManager $myAppManager,
    private IL10N $l10n,
  ) {
  }

  /**
   * Returns an estimate of the exported data size in KiB.
   * Should be fast, favor performance over accuracy.
   *
   * @since 25.0.0
   * @since 27.0.0 return value may overflow from int to float
   */
  public function getEstimatedExportSize(IUser $user): int|float {
    $size = 100; // 100KiB for user data JSON
    return $size;
  }

  /**
   * Export user data
   *
   * @throws UserMigrationException
   * @since 24.0.0
   */
  public function export(IUser $user, IExportDestination $exportDestination, OutputInterface $output): void {
    $output->writeln('Exporting myapp information in ' . MyAppMigrator::PATH_MYAPP_FILE . '…');

    try {
      $data = $this->myAppManager->getUserData($user);
      $exportDestination->addFileContents(MyAppMigrator::PATH_MYAPP_FILE, json_encode($data));
    } catch (Throwable $e) {
      throw new UserMigrationException('Could not export myapp information', 0, $e);
    }
  }

  /**
   * Import user data
   *
   * @throws UserMigrationException
   * @since 24.0.0
   */
  public function import(IUser $user, IImportSource $importSource, OutputInterface $output): void {
    if ($importSource->getMigratorVersion($this->getId()) === null) {
      $output->writeln('No version for ' . static::class . ', skipping import…');
      return;
    }

    $output->writeln('Importing myapp information from ' . MyAppMigrator::PATH_MYAPP_FILE . '…');

    try {
      $data = json_decode($importSource->getFileContents(MyAppMigrator::PATH_MYAPP_FILE), true, 512, JSON_THROW_ON_ERROR);
      $this->myAppManager->setUserData($user, $data);
    } catch (Throwable $e) {
      throw new UserMigrationException('Could not import myapp information', 0, $e);
    }
  }

  /**
    * Returns the unique ID
    *
    * @since 24.0.0
    */
  public function getId(): string {
    return 'myapp';
  }

  /**
    * Returns the display name
    *
    * @since 24.0.0
    */
  public function getDisplayName(): string {
    return $this->l10n->t('My App');
  }

  /**
    * Returns the description
    *
    * @since 24.0.0
    */
  public function getDescription(): string {
    return $this->l10n->t('My App information');
  }
}
```

La clase `MyAppMigrator` debe registrarse durante el {nc-ref}`arranque de la app <Bootstrapping>`.

```php
<?php

declare(strict_types=1);

namespace OCA\MyApp\AppInfo;

use OCA\MyApp\UserMigration\MyAppMigrator;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;

class Application extends App implements IBootstrap {
  public const APP_ID = 'myapp';

  public function __construct(array $urlParams = []) {
      parent::__construct(self::APP_ID, $urlParams);
  }

  public function register(IRegistrationContext $context): void {
      $context->registerUserMigrator(MyAppMigrator::class);
  }

  public function boot(IBootContext $context): void {
  }
}
```
````
