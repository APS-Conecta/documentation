---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo leer y escribir desde una app los valores de configuración del sistema, de la app y de usuario con IConfig, y cómo nombrar las claves."
---
# Configuración

## Resumen

Esta página muestra cómo una app lee y escribe con `IConfig` los valores del sistema (en {file}`config/config.php`), los valores de la app y los valores de usuario (en la base de datos), y qué convenciones siguen los nombres de las claves. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/storage/configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La configuración que permite a la app establecer ajustes globales, de la app y de usuario se puede inyectar desde el ServerContainer. Todos los valores se guardan como cadenas y deben convertirse al valor correcto.

```php
<?php
namespace OCA\MyApp\AppInfo;

use OCP\AppFramework\App;
use OCP\IConfig;
use OCP\IServerContainer;
use OCA\MyApp\Service\AuthorService;

class Application extends App {

    public function __construct(array $urlParams=array()){
        parent::__construct('myapp', $urlParams);

        $container = $this->getContainer();

        /**
         * Controllers
         */
        $container->registerService('AuthorService', function(IServerContainer $c): AuthorService {
            return new AuthorService(
                $c->get(IConfig::class),
                $c->get('appName')
            );
        });
    }
}
```

### Valores del sistema

Los valores del sistema se guardan en {file}`config/config.php` y permiten a la app modificar y leer la configuración global. Hay que tener en cuenta que `setSystemValue` puede lanzar una `OCP\HintException` cuando el archivo de configuración es de solo lectura.

```php
<?php
namespace OCA\MyApp\Service;

use OCP\HintException;
use OCP\IConfig;

class AuthorService {
    private IConfig $config;
    private string $appName;

    public function __construct(IConfig $config, string $appName){
        $this->config = $config;
        $this->appName = $appName;
    }

    public function getSystemValue(string $key) {
        return $this->config->getSystemValue($key);
    }

    public function setSystemValue(string $key, $value): void {
        try {
            $this->config->setSystemValue($key, $value);
        } catch (HintException $e) {
            // Handle exception, e.g. when config file is read-only
        }
    }
}
```

:::{note}
También se puede usar `getSystemValueBool`, `getSystemValueString` y `getSystemValueInt` para obtener valores de retorno tipados.
:::

#### Convenciones de nombres

Por coherencia, existen convenciones para las claves de configuración:

- Las claves de configuración del sistema solo deben contener letras minúsculas, números y `_`. Esto garantiza que se puedan usar como variables de entorno.
- Las claves pueden acotarse a subsistemas, como `<subsystem>_<key>`. Esto facilita agrupar la configuración relacionada.

Estos son algunos ejemplos:

1. `files_external_allow_create_new_local`
2. `filesystem_cache_readonly`
3. `log_rotate_size`
4. `mail_smtpname`
5. `session_lifetime`

### Valores de la app

Los valores de la app se guardan en la base de datos por app y son útiles para establecer ajustes globales de la app:

```php
<?php
namespace OCA\MyApp\Service;

use OCP\IConfig;

class AuthorService {
    private IConfig $config;
    private string $appName;

    public function __construct(IConfig $config, string $appName){
        $this->config = $config;
        $this->appName = $appName;
    }

    public function getAppValue(string $key): string {
        return $this->config->getAppValue($this->appName, $key);
    }

    public function setAppValue(string $key, string $value): void {
        $this->config->setAppValue($this->appName, $key, $value);
    }
}
```

### Valores de usuario

Los valores de usuario se guardan en la base de datos por usuario y por app, y sirven para guardar ajustes de la app específicos de cada usuario:

```php
<?php
namespace OCA\MyApp\Service;

use OCP\IConfig;

class AuthorService {
    private IConfig $config;
    private string $appName;

    public function __construct(IConfig $config, string $appName){
        $this->config = $config;
        $this->appName = $appName;
    }

    public function getUserValue(string $key, string $userId): string {
        return $this->config->getUserValue($userId, $this->appName, $key);
    }

    public function setUserValue(string $key, string $userId, string $value): void {
        $this->config->setUserValue($userId, $this->appName, $key, $value);
    }
}
```
````
