---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Conceptos y términos de la documentación para desarrolladores: PHP, peticiones web, base de datos, herramientas de frontend y términos de la plataforma."
---
(nc-dev-dev-glossary)=
# Glosario

## Resumen

Esta página explica los conceptos y términos que aparecen en la documentación para desarrolladores: el lenguaje PHP, cómo funcionan las peticiones web, los conceptos de base de datos, las herramientas de frontend y compilación, los términos propios de la plataforma y los términos generales de desarrollo web. Está dirigida a quienes empiezan a desarrollar.

````{upstream} developer_manual/getting_started/glossary.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Esta página explica los conceptos y términos que aparecen a lo largo de la documentación y los tutoriales para desarrolladores. No es necesario leerla entera antes de empezar: conviene guardarla en marcadores y volver a ella cuando algo no termine de tener sentido.

----

### El lenguaje y la plataforma

#### PHP

PHP es el lenguaje de programación en el que está escrito Nextcloud. Se ejecuta en el servidor; los usuarios nunca ven directamente el código PHP que se escribe. El servidor lo ejecuta y devuelve el resultado (normalmente una página HTML o datos JSON). Los archivos PHP terminan en `.php`.

Para quien haya hecho un curso introductorio de programación en Python o JavaScript, PHP le resultará familiar: tiene variables (`$name`), funciones (`function greet() {}`), bucles y condicionales. La principal diferencia visual es que las variables siempre empiezan con el signo `$`.

#### Nextcloud

Nextcloud es una plataforma de colaboración autoalojada. «Autoalojada» significa que uno mismo (o su organización) ejecuta el servidor, en lugar de depender de un servicio en la nube de terceros. Nextcloud es en sí una aplicación PHP, y casi todas sus funciones (Archivos, Calendario, Talk) están construidas como **apps** que se conectan a un framework común.

----

### Conceptos de PHP que aparecerán

#### Clase

Una clase es un plano para crear objetos. Puede pensarse en una clase como una plantilla: una clase `PageController` describe qué *es* un controlador de página y qué puede *hacer*. Se define una vez y el framework la crea («la instancia») cuando hace falta.

```php
class PageController {
    public function index(): TemplateResponse {
        // This method handles a web request
    }
}
```

#### Espacio de nombres

Un espacio de nombres es como una ruta de carpetas para las clases PHP; evita colisiones de nombres cuando dos apps distintas definen una clase llamada `Controller`.

Nextcloud usa tres espacios de nombres de nivel superior:

- `OCA\YourAppName\`: donde vive el código privado de la app propia.
- `OCP\`: la API pública estable de Nextcloud. Usarla para interactuar con el funcionamiento interno de Nextcloud. Está versionada y no se romperá entre versiones de Nextcloud.
- `OC\`: código heredado interno. Evitarlo en las apps nuevas: no ofrece ninguna garantía de compatibilidad y puede cambiar entre versiones. Aparece en código y documentación existentes; algunos helpers muy usados (como `OC::$server->get()`) viven aquí y siguen en uso activo en todo el propio código base de Nextcloud.

En la práctica, se ven espacios de nombres al principio de cada archivo PHP:

```php
namespace OCA\NoteBook\Controller;   // "I am part of the NoteBook app, in the Controller subfolder"

use OCP\AppFramework\Controller;     // "I want to use Nextcloud's public Controller class"
use OCP\IRequest;                    // "I want to use Nextcloud's public IRequest interface"
```

#### Atributos de PHP 8

Los atributos son la forma que tiene PHP 8 de adjuntar metadatos a una clase o un método. Tienen el aspecto `#[SomeName]` y aparecen en la línea inmediatamente superior a lo que describen.

En Nextcloud, los atributos se usan para configurar el enrutamiento y el control de acceso:

```php
#[NoCSRFRequired]
#[NoAdminRequired]
#[FrontpageRoute(verb: 'GET', url: '/')]
public function index(): TemplateResponse {
```

Esto reemplaza el estilo anterior de escribirlos como comentarios docblock especiales (p. ej., `/** @NoCSRFRequired */`). A diferencia de los comentarios, los atributos son sintaxis PHP real; el framework los lee directamente.

Atributos comunes:

- `#[FrontpageRoute]`: declara a qué URL responde este método (para las rutas de página normales).
- `#[ApiRoute]`: igual que el anterior, pero para rutas de la {nc-ref}`API OCS <ocs-api>` (se usa con `OCSController`).
- `#[NoAdminRequired]`: permite que los usuarios normales (no administradores) accedan a esta ruta.
- `#[NoCSRFRequired]`: desactiva la comprobación del token CSRF; ver {nc-ref}`csrf` más abajo.

(nc-dev-csrf)=
#### CSRF y el atributo `#[NoCSRFRequired]`

CSRF (*Cross-Site Request Forgery*) es un ataque web en el que un sitio malicioso engaña al navegador para que haga una petición a otro sitio en el que ya hay una sesión iniciada.

Nextcloud se protege de esto exigiendo un token de seguridad oculto en la mayoría de las peticiones. Al renderizar una página a la que los usuarios navegan directamente en su navegador no hay riesgo de ataque, así que se marca con `#[NoCSRFRequired]`. En las rutas que modifican datos (guardar una nota, eliminar un archivo), no poner este atributo para que el token se verifique.

#### Inyección de dependencias (DI)

La inyección de dependencias es un patrón en el que la clase *pide* lo que necesita en lugar de *crearlo* ella misma. Nextcloud proporciona automáticamente los objetos adecuados según las declaraciones de tipo del constructor.

```php
class NoteController extends Controller {
    public function __construct(
        string $appName,
        IRequest $request,
        protected NoteMapper $mapper,   // Nextcloud creates this and passes it in
        protected IConfig $config,      // stored as a protected property automatically
    ) {
        parent::__construct($appName, $request);
    }
```

No se llama a `new NoteMapper()` directamente. El contenedor de DI de Nextcloud lee las declaraciones de tipo (`NoteMapper`, `IConfig`) y crea e inyecta automáticamente el objeto adecuado. Así el código queda débilmente acoplado y es fácil de probar.

#### Interfaz

Una interfaz (con el prefijo `I` en el código de Nextcloud, p. ej., `IRequest`, `IConfig`) es un contrato que describe *qué métodos debe tener un objeto* sin especificar *cómo* funcionan. Cuando el código depende de `IConfig`, Nextcloud puede suministrar su implementación real de la configuración, o un doble de prueba durante las pruebas unitarias, y al código no le importa cuál recibe.

----

### Cómo funcionan las peticiones web en Nextcloud

#### Ruta

Una ruta asigna una URL a un método PHP concreto. Cuando un usuario abre `https://your-nextcloud.example/apps/notebook/`, Nextcloud busca qué método está registrado para esa URL y lo llama.

En las apps modernas de Nextcloud, las rutas se declaran directamente en el método con el atributo `#[FrontpageRoute]`:

```php
#[FrontpageRoute(verb: 'GET', url: '/')]
public function index(): TemplateResponse {
```

A veces aparece una notación con puntos como `notebook.page.index`. Significa: app `notebook`, controlador `PageController`, método `index`.

#### Controlador

Un controlador es una clase PHP que gestiona las peticiones web entrantes. Cada método público de un controlador puede asignarse a una URL. El método recibe datos de la petición, realiza el trabajo necesario y devuelve una respuesta.

Nextcloud tiene varios tipos de respuesta:

- `TemplateResponse`: renderiza un archivo de plantilla PHP y devuelve HTML.
- `JSONResponse`: devuelve datos JSON (se usa para las API).
- `DataResponse`: como `JSONResponse`, pero con más flexibilidad sobre los códigos de estado y las cabeceras.

#### Plantilla

Una plantilla es un archivo `.php` en el directorio `templates/` de la app. En las apps modernas de Nextcloud casi siempre es solo un único punto de montaje HTML: un `<div>` al que se acopla el frontend de Vue. El ID puede ser cualquiera, siempre que coincida con la llamada a `mount()` del JavaScript:

```php
<?php // templates/index.php — the entire file in a modern app ?>
<div id="notebook"></div>
```

```javascript
// src/main.js
const app = createApp(App)
app.mount('#notebook')
```

El controlador carga el bundle de JavaScript compilado y pasa los datos iniciales mediante `IInitialState`, y luego devuelve la plantilla:

```php
// In the controller:
$this->initialState->provideInitialState('notes', $this->mapper->findAll());
Util::addScript('notebook', 'main');
return new TemplateResponse('notebook', 'index');
```

El frontend recoge esos datos con `loadState('notebook', 'notes')`; en la propia plantilla no aparece ninguna variable PHP.

Todavía puede encontrarse el patrón antiguo `$_['key']` / `p()` en apps heredadas:

```php
<!-- Older style — still works, but not used in new development -->
<p>Hello, <?php p($_['username']); ?></p>
```

`p()` muestra un valor de forma segura (con escape HTML). Si aparece, pertenece a una app antigua.

----

### Conceptos de bases de datos

#### Migración

Una migración es un archivo PHP que describe un cambio en el esquema de la base de datos: crear una tabla, añadir una columna, etc. En lugar de ejecutar SQL directamente, se escribe una clase de migración y se aplica con {command}`occ migrations:migrate yourapp` (ejecuta todas las migraciones pendientes) o {command}`occ migrations:execute yourapp versionnumber` (ejecuta una migración concreta por su número de versión, útil durante el desarrollo).

Las migraciones se guardan en `lib/Migration/` y están numeradas para que se ejecuten en orden. Quien instale la app obtiene automáticamente la estructura de base de datos correcta.

#### Entidad

Una entidad es una clase PHP que representa una sola fila de una tabla de la base de datos. Cada propiedad de la clase corresponde a una columna. El framework de apps de Nextcloud proporciona una clase base `Entity` que extender:

```php
class Note extends Entity {
    protected string $title = '';
    protected string $content = '';
    protected string $userId = '';
}
```

#### Mapper

Un mapper es una clase PHP responsable de leer y escribir entidades en la base de datos. Extiende `QBMapper` (Query Builder Mapper) y proporciona métodos como `find()`, `findAll()`, `insert()`, `update()` y `delete()`. El mapper se inyecta en el controlador mediante inyección de dependencias; nunca se escribe SQL en bruto a mano.

----

### Frontend y herramientas de compilación

#### npm y `package.json`

npm es un gestor de paquetes para JavaScript; descarga y gestiona las bibliotecas de JavaScript de las que depende el frontend. La lista de dependencias está en `package.json`.

Comandos comunes:

- {command}`npm install`: descarga en `node_modules/` todos los paquetes listados en `package.json`.
- {command}`npm run build`: compila el JavaScript para producción.
- {command}`npm run watch`: compila automáticamente cada vez que se guarda un archivo (usarlo durante el desarrollo).

Solo hace falta ejecutar {command}`npm install` una vez, o cuando cambian las dependencias.

#### Vite

Vite es una herramienta de compilación que convierte JavaScript moderno (y TypeScript, componentes de Vue) en archivos compatibles con el navegador. El código se escribe en `src/`, se ejecuta {command}`npm run build` (o {command}`npm run watch`) y Vite genera en `js/` archivos listos para usar.

Este paso es necesario porque los navegadores no entienden directamente las importaciones de módulos ES (`import { ref } from 'vue'`): Vite lo empaqueta todo en archivos que el navegador puede cargar. Los comandos {command}`npm run build` y {command}`npm run watch` invocan Vite internamente.

#### Composer y `composer.json`

Composer es el equivalente de npm para PHP; gestiona bibliotecas de PHP. Si la app tiene dependencias de PHP (por ejemplo, una biblioteca para analizar Markdown), se listan en `composer.json` y se instalan con {command}`composer install`.

En la mayoría de las apps para principiantes no hará falta tocar Composer: el generador de esqueletos se encarga de ello.

----

### Términos específicos de Nextcloud

#### ID de la app

El ID de la app es su identificador único. Se elige al crear la app; debe estar en minúsculas y contener solo letras, números y guiones bajos. No tiene por qué derivarse de ninguna forma particular del nombre visible de la app.

La única regla estricta es que **el nombre de la carpeta y el** `<id>` **de** `appinfo/info.xml` **deben ser idénticos**. Nextcloud descubre las apps leyendo el nombre de la carpeta y luego lo verifica contra `info.xml`; si no coinciden, la app no se carga.

Por ejemplo, una app con el nombre visible «My NoteBook» podría tener el ID `notebook`, `mynotebook`, `my_notebook` o cualquier otro que se elija, siempre que la carpeta e `info.xml` coincidan:

```text
apps-extra/mynotebook/                    # folder name is "mynotebook"
apps-extra/mynotebook/appinfo/info.xml    # <id>mynotebook</id>  must match
```

El mismo ID aparece de forma coherente en todo el código base:

- El nombre de la carpeta (`apps-extra/mynotebook/`)
- `appinfo/info.xml` como `<id>mynotebook</id>`
- Los espacios de nombres de PHP (`OCA\MyNoteBook\`): el ID en PascalCase, pero el ID en sí va en minúsculas
- Los nombres de ruta (`mynotebook.page.index`)
- Los comandos {command}`occ` (`occ app:enable mynotebook`)

#### `appinfo/info.xml`

Toda app de Nextcloud tiene este archivo. Indica a Nextcloud el nombre de la app, su autor, su versión, qué versiones de Nextcloud soporta y si debe aparecer en la barra de navegación. Puede verse como la tarjeta de identidad de la app.

El campo `<max-version>` es importante: si es menor que la versión de Nextcloud en ejecución, se impide que la app se cargue. Para conocer la versión de Nextcloud, ir a **Ajustes → Administración → Vista general**. El campo `<id>` debe coincidir exactamente con el ID de la app y con el nombre de la carpeta.

#### `occ` — la herramienta de línea de comandos

`occ` es la interfaz de línea de comandos de Nextcloud. Consultar la [referencia de comandos occ](https://docs.nextcloud.com/server/latest/admin_manual/occ_command.html) del manual de administración para ver la lista completa de comandos.

En el entorno de desarrollo **Docker**, anteponer `docker exec` a todos los comandos {command}`occ`:

```bash
docker exec --user www-data master-nextcloud-1 php occ app:enable notebook
```

En **GitHub Codespaces**, ejecutar {command}`occ` directamente en la terminal:

```bash
sudo -E -u www-data php occ app:enable notebook
```

Comandos comunes:

| Comando | Qué hace |
|---|---|
| `occ app:enable notebook` | Habilitar la app |
| `occ app:disable notebook` | Deshabilitar la app |
| `occ app:list` | Listar todas las apps instaladas |
| `occ migrations:migrate notebook` | Ejecutar todas las migraciones pendientes de la app |
| `occ migrations:execute notebook 20240101120000` | Ejecutar una sola migración concreta por su número de versión |
| `occ maintenance:mode --on` | Poner Nextcloud en modo de mantenimiento |

(nc-dev-ocs-api)=
#### API OCS

OCS (Open Collaboration Services) es un formato de API HTTP que Nextcloud usa para la comunicación entre apps y entre cliente y servidor. Al construir una API REST en una app de Nextcloud, se extiende `OCSController` en lugar de la clase `Controller` simple. Las respuestas siguen un formato de sobre específico con JSON que los clientes móviles y de escritorio de Nextcloud saben manejar.

#### ExApp (app externa)

Una ExApp es una app que se ejecuta como un proceso separado fuera del proceso PHP de Nextcloud y se comunica con Nextcloud por HTTP. Las ExApps pueden escribirse en cualquier lenguaje (Python, Go, Node.js). Se registran en Nextcloud mediante AppAPI.

Las apps PHP clásicas y las ExApps se tratan en secciones separadas de esta documentación. Para quien es nuevo en el desarrollo para Nextcloud, conviene empezar por las apps PHP clásicas.

----

### Términos generales de desarrollo web

#### API (interfaz de programación de aplicaciones)

Una API es una forma definida de que dos piezas de software se comuniquen entre sí. En desarrollo web, normalmente significa que un programa envía una petición HTTP a una URL y el otro responde con datos estructurados (normalmente JSON). Cuando el frontend de JavaScript necesita cargar o guardar datos, hace una llamada a la API del backend de PHP.

#### JSON

JSON (JavaScript Object Notation) es un formato de texto para datos estructurados:

```json
{
  "id": 1,
  "title": "My first note",
  "content": "Hello, world!"
}
```

JSON se usa en todas partes como lenguaje común entre un frontend y un backend.

#### AJAX

AJAX se refiere a hacer llamadas a la API HTTP desde JavaScript sin recargar la página. Cuando se hace clic en «Guardar» en una aplicación web y la página no se refresca, eso es AJAX. En las apps de Nextcloud, normalmente se usa la biblioteca `@nextcloud/axios` para hacer llamadas AJAX al controlador PHP.
````
