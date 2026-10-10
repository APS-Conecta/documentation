---
tipo: tutorial
audiencia: desarrollo
apps: [farmacia, estadistica, territorio, aps-common, gestion]
resumen: "Cómo se arma una aplicación propia: la plantilla farmacia, aps-common, los textos en español, el paquete confirmado, los arneses y la entrada a gestion."
---
# Desarrollo de aplicaciones

## Objetivo

Este recorrido sigue una aplicación propia de la suite desde su repositorio hasta el paquete que la provisión de gestion instala en cada establecimiento. La plantilla es farmacia: su CI es la plantilla de la organización para una aplicación de la suite, y estadistica se cortó de ella.

Lo genérico de la plataforma —manifiesto, arranque, rutas, controladores, base de datos, trabajos de fondo, comandos y frontend— está en {doc}`/desarrollo/plataforma/app-development/index` y en {doc}`/desarrollo/plataforma/basics/index`. Esta página cubre lo que la organización agrega encima, y por qué.

Una aplicación propia depende de Nextcloud solo a través de las API públicas `OCP\…`, nunca de sus clases internas, y el núcleo nunca depende de ella. El núcleo no se parcha (AD-9).

## Requisitos

- Docker: las pruebas unitarias corren en un contenedor PHP sin Nextcloud, y la instancia de prueba es una composición de Docker.
- Node.js en una de las versiones que fija `engines` en `package.json`: 20, 22 o 24.
- Una copia de aps-common junto al repositorio de la aplicación, en `../aps-common`: los objetivos del Makefile resuelven el paquete en esa ruta. aps-common es privado; en CI se clona con una llave de despliegue de solo lectura.
- Una copia de gestion, para probar la aplicación dentro de la suite.

## Recorrido

### 1. La estructura de la plantilla

| Ruta | Qué contiene |
|---|---|
| `appinfo/info.xml` | El manifiesto: id, licencia `AGPL-3.0-or-later`, PHP 8.2 a 8.5, Nextcloud 34 como versión mínima y máxima, la entrada de navegación, el comando `occ` y el paso de reparación que siembra los datos |
| `lib/AppInfo/Application.php` | El arranque: todo se autoinyecta, más una regla de carga automática para aps-common |
| `lib/Controller`, `lib/Service`, `lib/Db`, `lib/Migration`, `lib/Command`, `lib/Exception` | Controladores, servicios, entidades y mappers, la migración y el paso de reparación, el comando de consola y las excepciones de rechazo |
| `templates/index.php` | El único punto de montaje de la aplicación de una sola página |
| `src/` y `js/` | El frontend en Vue 3 con `@nextcloud/vue`, y su compilación con webpack, `js/farmacia-main.js` |
| `openapi.json` | El contrato OCS, generado desde `ApiController` |
| `Makefile`, `Dockerfile.test`, `compose.dev.yaml` | Los dos arneses de prueba (paso 5) |

Los datos iniciales se siembran en un paso de reparación registrado para `install` y para `post-migration`, no en el hook `postSchemaChange` de la migración: ese hook no corre en la primera instalación de solo esquema, que es justo lo que ejecuta `occ app:enable`. El mecanismo está en {doc}`/desarrollo/plataforma/digging-deeper/repair`.

Las rutas y los comandos `occ` de cada aplicación se publican como referencia generada a partir de `appinfo/info.xml` y `appinfo/routes.php`; la de farmacia es {doc}`/_generated/referencia/farmacia`.

### 2. Los textos de la interfaz

La interfaz se escribe en español; el código, los comentarios, los commits y los pull requests, en inglés. farmacia y estadistica escriben lo que lee una persona como literales en español y no usan `t()` ni `$l->t()`. territorio escribe literales en `src/`, sin `t()` de `@nextcloud/l10n`, y en PHP usa `$this->l->t('…')` solo donde `IL10N` ya está inyectado.

La instancia fija el idioma: la fase `10-locale` de gestion establece `default_language` y `force_language` en `es`, y la configuración regional en `es_CL`, de modo que una preferencia del navegador no cambia lo que ve el personal. El mecanismo de traducción de la plataforma está en {doc}`/desarrollo/plataforma/basics/translations`.

### 3. aps-common, el paquete compartido

aps-common reúne las reglas de texto que dos o más aplicaciones deben cumplir igual: el dialecto CSV, el plegado de texto y los slugs, la postura de rechazo y la forma única del error del cliente. Es una biblioteca de Composer, no una aplicación: no tiene `appinfo`, rutas ni base de datos, y no depende de ninguna clase OCP salvo un trait de rechazo acoplado a propósito.

El paquete se distribuye como un subárbol confirmado dentro de cada aplicación —`vendor/aps/common/src` para PHP y `src/aps/` para JS— porque el paquete de una versión es `git archive` del árbol rastreado. `vendor/autoload.php` no se confirma, así que `Application.php` registra un cargador PSR-4 para `APS\Common\`.

Después de editar aps-common:

1. En cada aplicación, ejecutar el objetivo `aps-sync` del Makefile: copia `src/`, el stub de prueba y `js/` del paquete a sus lugares confirmados.
2. Ejecutar el objetivo `aps-drift`: falla si las copias confirmadas difieren del paquete.
3. Confirmar el resultado en la aplicación.

territorio, farmacia y estadistica consumen las cuatro superficies; epidemiologia, solo la mitad JS. Un cambio incompatible pone en rojo el `aps-drift` de CI de las tres primeras hasta que vuelven a sincronizar; el CI de epidemiologia no tiene ese paso.

### 4. El paquete del frontend

`js/` se confirma: el paquete compilado es lo que se despliega, y un `src/` que cambia sin recompilar entrega una aplicación distinta del repositorio. Después de cambiar `src/`, ejecutar `npm run build` y confirmar en el mismo pull request `js/farmacia-main.js` y su `.LICENSE.txt`; nunca `*.js.map` ni `node_modules/`.

CI recompila y exige que `js/` quede sin diferencias:

```bash
npm run build
git diff --exit-code js/
```

farmacia, estadistica y territorio compilan con `@nextcloud/webpack-vue-config`; epidemiologia, con `@nextcloud/vite-config`.

### 5. Los dos arneses de prueba

El Makefile separa dos arneses a propósito: pruebas unitarias en un contenedor PHP sin Nextcloud, rápidas y predeterminadas, y una instancia desechable de Nextcloud 34 con PostgreSQL 18 para lo que el contenedor no puede correr: los mappers, la siembra y `occ`. La instancia no es la pila de gestion: no usa su `.env` ni sus datos.

| Objetivo | Qué hace |
|---|---|
| `test` | PHPUnit en el contenedor PHP |
| `instance-up` | Levanta la instancia de `compose.dev.yaml` y activa la aplicación, lo que corre la migración y el paso de reparación, igual que el `occ app:enable` de un establecimiento |
| `instance-occ` | Corre un comando `occ` en la instancia, pasado en `CMD` |
| `smoke` | Prueba contra la instancia el cableado que ninguna prueba unitaria ve |
| `openapi` | Regenera `openapi.json` desde los atributos y comentarios de `ApiController` |
| `instance-down`, `instance-clean` | Detiene la instancia; la borra junto con su base de datos |
| `aps-sync`, `aps-drift` | Copia aps-common; prueba que las copias están al día |

Cada instancia se publica solo en loopback y en su propio puerto: territorio en 8083, farmacia en 8090 y estadistica en 8092.

Después de activar la aplicación, `instance-up` reinicia el servidor web: los procesos web guardan en APCu, por una hora, las rutas y el estado de las aplicaciones activas, y `occ` corre en la CLI, que no puede invalidar esa caché. Sin el reinicio, cada ruta de la aplicación responde 404 en una instancia nueva.

La suite de integración corre dentro de la instancia contra su PostgreSQL real con el objetivo `integration`, después de `deps` e `instance-up`; ningún job de CI la corre.

La compuerta de deriva de la organización, en el CI de gestion, exige que territorio, farmacia y estadistica conserven los objetivos `test`, `clean`, `instance-up`, `instance-occ`, `instance-down`, `instance-clean`, `aps-sync` y `aps-drift`. Compara además `phpunit.xml` y `phpunit.integration.xml` byte a byte y las reglas fijadas de `eslint.config.mjs`. Las compuertas de la plantilla están en {doc}`calidad`.

### 6. La entrada a la suite

Mientras se desarrolla, la aplicación es una aplicación de laboratorio: un clon en `apps/<id>` de gestion, declarado en `dev/lab-apps.sh`, que nunca viaja en una versión. La provisión actúa sobre una entrada de laboratorio solo donde existe `apps/<id>/.git`, de modo que en un establecimiento el archivo no hace nada.

Para trabajar dentro de la suite, clonar la aplicación en `apps/<id>` de gestion y converger con los objetivos `fix-mount-perms` y `seed` de su Makefile. Con el directorio presente, la provisión deja el clon intacto en vez de desempaquetar el paquete encima.

La provisión decide por un hecho, no por una bandera:

| `apps/<id>/.git` | Qué hace la provisión | Por qué |
|---|---|---|
| Ausente: un servidor | Desempaqueta el paquete fijado, comprueba su sha256 y reconcilia el esquema | La misma siembra produce la misma instancia |
| Presente: un desarrollador | Comprueba la versión, corre `occ upgrade` si cambió y nunca sobrescribe | Una siembra nunca descarta trabajo en curso |

Al promoverla, la aplicación entra en `OWN_APPS` de `provisioning/phases/12-apps.sh` y viaja como paquete: un único `.tar.gz` en `provisioning/apps/<id>/`, construido con `git archive` desde una etiqueta de su repositorio, junto a un archivo `VENDOR` con versión, sha256 y etiqueta de origen. Así una instalación no necesita red, git ni GitHub. El comando exacto de construcción vive en ese `VENDOR`; `gzip -n` deja la fecha fuera de la cabecera, de modo que reconstruir la misma etiqueta da los mismos bytes y el sha256 sigue comprobable.

Una aplicación cortada de la plantilla, como estadistica, entra además en el clon del CI de gestion y en la compuerta de deriva al promoverse; toda aplicación promovida entra en la tabla de licencias de gestion. gestion fija la versión de una aplicación propia en un hito, no en cada etiqueta de la aplicación. Un establecimiento recibe la aplicación por gestion, nunca por la tienda de aplicaciones, que la suite mantiene apagada.

## Resultado

La aplicación pasa sus compuertas, la provisión la instala desde un paquete fijado y sin red, y su contrato OCS figura en el índice de contratos de la organización, `docs/CONTRACTS.md` de gestion.

### Deuda y límites

- La deriva entre aplicaciones se vigila solo en territorio, farmacia y estadistica; epidemiologia se suma por comprobación cuando su árbol llegue a la forma común, y `ci.yml` es propio de cada aplicación por diseño.
- El CI de epidemiologia no comprueba la deriva de aps-common.
- La suite de integración no corre en CI.
- El paquete que instala gestion queda atrás del `main` de la aplicación hasta el siguiente hito: farmacia lleva en `main` cambios no publicados sobre la etiqueta 0.11.1.
