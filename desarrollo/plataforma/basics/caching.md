---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Tipos de caché que ofrece la API (en memoria, local y distribuida), sus ventajas y desventajas, y cómo obtener y usar cada una desde una app."
---
# Caché

## Resumen

Esta página compara los tres tipos de caché de la API (en memoria, local y distribuida) y muestra cómo obtener cada uno, directamente o mediante `ICacheFactory`, para guardar resultados de operaciones costosas. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/caching.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los resultados de operaciones costosas o lentas se pueden guardar en caché para acelerar Nextcloud y sus apps.

### Tipos de cachés

Nextcloud ofrece cachés en memoria, locales y distribuidas. El backend de caché (APCu, Redis, Memcached) es configurable.

En las instalaciones de un solo servidor, los administradores suelen configurar un solo tipo de caché. Las instalaciones más grandes pueden tener dos tipos de caché. La API de Nextcloud permite elegir un tipo de caché. La tabla siguiente intenta resaltar las principales ventajas y desventajas de cada tipo.

| | Caché en memoria | Caché local | Caché distribuida |
|---|---|---|---|
| **Latencia** | Baja | Baja | Alta |
| **Alcance de los datos** | Mismo proceso | Servidor de aplicaciones | Clúster completo |
| **Caducidad** | Fin del proceso | Se alcanza el TTL | Se alcanza el TTL |

Por escalabilidad, conviene preferir las cachés locales. Una caché local debe poblarse en cada servidor de aplicaciones, pero evita crear un cuello de botella por exceso de tráfico en la caché distribuida. Una caché distribuida es más útil para datos que *deben sincronizarse* en todo el clúster de Nextcloud.

### Caché en memoria

La clase `OCP\Cache\CappedMemoryCache` es una caché en memoria que se puede usar como un array:

**Archivo {file}`lib/Service/PictureService.php`**:

```php
<?php

namespace OCA\MyApp\Service;

use OCP\Cache\CappedMemoryCache;

class PictureService {
    private $cache;

    public function __construct(){
        $this->cache = new CappedMemoryCache(64);
    }

    public function getPicture(string $url): void {
        if (isset($this->cache[$url])) {
            return $this->cache[$url];
        }

        // Fetch picture and serialize result into $picture

        $this->cache[$url] = $picture;
        return $picture;
    }
}
```

Una instancia de caché también puede construirse con la fábrica de cachés. Este enfoque permite simular la fábrica inyectada para tener un control más preciso durante las {nc-ref}`pruebas unitarias <testing-php>`:

**Archivo {file}`lib/Service/PictureService.php`**:

```php
<?php

namespace OCA\MyApp\Service;

use OCP\ICacheFactory;

class PictureService {
    private ICacheFactory $cacheFactory;

    public function __construct(ICacheFactory $cacheFactory){
        $this->cacheFactory = $cacheFactory;
    }

    public function getPicture(string $url): void {
        // Initialize the cache. The instance has to be remembered because
        // each call to `createInMemory` returns a fresh, empty cache.
        if ($this->cache === null) {
            $this->cache = $this->cacheFactory->createInMemory(64);
        }

        if (isset($this->cache[$url])) {
            return $this->cache[$url];
        }

        // Fetch picture and serialize result into $picture

        $this->cache[$url] = $picture;
        return $picture;
    }
}
```

### Caché local

Una instancia de caché local puede obtenerse a través del servicio `\OCP\ICacheFactory`. La fábrica se puede inyectar:

**Archivo {file}`lib/Service/PictureService.php`**:

```php
<?php

namespace OCA\MyApp\Service;

use OCP\ICacheFactory;

class PictureService {
    private ICacheFactory $cacheFactory;

    public function __construct(ICacheFactory $cacheFactory){
        $this->cacheFactory = $cacheFactory;
    }

    public function getPicture(string $url): void {
        $cache = $this->cacheFactory->createLocal('my-app-pictures');
        $cachedPicture = $cache->get($url);
        if ($cachedPicture !== null) {
            return $cachedPicture;
        }

        // Fetch picture and serialize result into $picture

        $cache->set($url, $picture, 6 * 3600); // Cache result for 6h
        return $picture;
    }
}
```

### Caché distribuida

Una instancia de caché distribuida puede obtenerse a través del servicio `\OCP\ICacheFactory`. La fábrica se puede inyectar:

**Archivo {file}`lib/Service/PictureService.php`**:

```php
<?php

namespace OCA\MyApp\Service;

use OCP\ICacheFactory;

class PictureService {
    private ICacheFactory $cacheFactory;

    public function __construct(ICacheFactory $cacheFactory){
        $this->cacheFactory = $cacheFactory;
    }

    public function getPicture(string $url): void {
        $cache = $this->cacheFactory->createDistributed('my-app-pictures');
        $cachedPicture = $cache->get($url);
        if ($cachedPicture !== null) {
            return $cachedPicture;
        }

        // Fetch picture and serialize result into $picture

        $cache->set($url, $picture, 6 * 3600); // Cache result for 6h
        return $picture;
    }
}
```
````
