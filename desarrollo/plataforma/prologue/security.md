---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Problemas de seguridad comunes en apps y cómo prevenirlos: inyección SQL y de shell, XSS, secuestro de clics, recorrido de directorios, CSRF y CORS."
---
# Pautas de seguridad

## Resumen

Esta página describe los problemas de seguridad más comunes en el desarrollo de apps y cómo prevenirlos, con ejemplos de código de lo que se debe y lo que no se debe hacer. Está dirigida a quienes desarrollan apps sobre la plataforma.

````{upstream} developer_manual/prologue/security.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Esta guía destaca algunos de los problemas de seguridad más comunes y cómo prevenirlos. Revisar la app por si contiene alguno de los siguientes agujeros de seguridad.

:::{note}
**Programar a la defensiva**: por ejemplo, comprobar siempre el CSRF o escapar las cadenas, aunque no haga falta. Así se evitan problemas futuros en los que podría pasarse por alto un cambio que lleve a un agujero de seguridad.
:::

:::{note}
Todas las funciones de seguridad del App Framework dependen de que el controlador se llame a través de {code}`OCA\AppFramework\App::main`. Si el método del controlador se ejecuta directamente, ¡no se realiza ninguna comprobación de seguridad!
:::

### Inyección SQL

La [inyección SQL](https://en.wikipedia.org/wiki/SQL_injection) se produce cuando las cadenas de consulta SQL se concatenan con variables.

Para evitarlo, usar siempre consultas preparadas:

```php
<?php
$sql = 'SELECT * FROM `users` WHERE `id` = ?';
$query = \OCP\DB::prepare($sql);
$params = array(1);
$result = $query->execute($params);
```

Si se usa el App Framework, escribir las consultas SQL así, en una clase que extienda el Mapper:

```php
<?php
// inside a child mapper class
$sql = 'SELECT * FROM `users` WHERE `id` = ?';
$params = array(1);
$result = $this->execute($sql, $params);
```

### Secuencias de comandos en sitios cruzados

Las [secuencias de comandos en sitios cruzados](https://en.wikipedia.org/wiki/Cross-site_scripting) se producen cuando la entrada del usuario se pasa directamente a las plantillas. Un posible atacante podría inyectar HTML/JavaScript en la página para robar la sesión del usuario, registrar las pulsaciones de teclado, incluso realizar ataques DDOS contra otros sitios web u otras acciones maliciosas.

Aunque Nextcloud usa Content-Security-Policy para impedir la ejecución de código JavaScript en línea, quienes desarrollan siguen obligados a prevenir el XSS. CSP es solo una capa más de defensa, que no está implementada en todos los navegadores web.

Para prevenir el XSS en la app, hay que sanear las plantillas y todo el JavaScript que manipule el DOM.

#### Plantillas

Supongamos que se usa el siguiente ejemplo en la aplicación:

```php
<?php
echo $_GET['username'];
```

Ahora un atacante podría enviar fácilmente al usuario un enlace a:

```
app.php?username=<script src="attacker.tld"></script>
```

para apoderarse de la cuenta del usuario. El mismo problema se produce al mostrar contenido de la base de datos o de cualquier otra ubicación en la que los usuarios puedan escribir.

Otro vector de ataque que suele pasarse por alto es el XSS en los atributos **href**. HTML permite ejecutar JavaScript en los atributos href de esta forma:

```
<a href="javascript:alert('xss')">
```

Para prevenir el XSS en la app, **no usar nunca echo, print() ni <%=**: usar en su lugar **p()**, que sanea la entrada. Además, ¡**validar que las URL empiecen por el protocolo esperado** (que empiecen por http, por ejemplo)!

:::{note}
Si alguna vez fuera necesario imprimir algo sin escapar, comprobar dos veces si de verdad hace falta. Si no hay otra forma (p. ej., al incluir subplantillas), usar *print_unescaped* con cuidado.
:::

#### JavaScript

Evitar manipular el HTML directamente mediante JavaScript: a menudo provoca XSS, porque es frecuente olvidar sanear las variables:

```js
var html = '<li>' + username + '</li>"';
```

Si **de verdad** se quiere usar JavaScript para algo así, usar *escapeHTML* para sanear las variables:

```js
var html = '<li>' + escapeHTML(username) + '</li>';
```

Una forma aún mejor de hacer más segura la app es usar la función integrada de jQuery **$.text()** en lugar de **$.html()**.

**NO HACER**

```js
messageTd.html(username);
```

**HACER**

```js
messageTd.text(username);
```

También puede ser sensato elegir un framework de JavaScript adecuado, como Vue.js, que se encarga automáticamente del escapado de JavaScript.

### Secuestro de clics

El [secuestro de clics](https://en.wikipedia.org/wiki/Clickjacking) engaña al usuario para que haga clic en un iframe invisible y realice una acción arbitraria (p. ej., eliminar una cuenta de usuario)

Para evitar estos ataques, Nextcloud envía la cabecera *X-Frame-Options* en todas las respuestas de plantilla. ¡No eliminar esta cabecera si no es realmente necesario!

Esto ya está integrado en Nextcloud en {code}`OC_Template`.

### Ejecución de código / inclusión de archivos

La ejecución de código significa que un atacante puede incluir un archivo PHP arbitrario. Este archivo PHP se ejecuta con todos los privilegios concedidos a la aplicación normal y puede causar una cantidad enorme de daños.

La ejecución de código y la inclusión de archivos se evitan fácilmente si **nunca** se permite que la entrada del usuario pase por las siguientes funciones:

- **include()**
- **require()**
- **require_once()**
- **eval()**
- **fopen()**

:::{note}
¡Tampoco permitir **nunca** que el usuario suba archivos a una carpeta accesible desde la URL!
:::

**NO HACER**

```php
<?php
require("/includes/" . $_GET['file']);
```

:::{note}
Si hay que pasar entrada del usuario a una función potencialmente peligrosa, comprobar dos veces que no exista otra forma. Si no es posible de otro modo, sanear cada parámetro del usuario y pedir a otras personas que auditen la función de saneamiento.
:::

### Recorrido de directorios

El recorrido de directorios se produce cuando una ruta de archivo construida a partir de la entrada del usuario sale de la carpeta a la que estaba destinada, por ejemplo con `../`. Esto abre varios vectores de ataque, entre ellos la divulgación de archivos, la escalada de privilegios y la ejecución de código.

No construir nunca a mano rutas dentro del directorio de datos. Acceder en su lugar a los archivos a través de la API de archivos: rechaza las rutas que contienen `..` y, además, aplica los permisos, el cifrado y el manejo del almacenamiento externo.

**NO HACER**

```php
<?php
$content = file_get_contents($dataDir . '/' . $userId . '/files/' . $_GET['file']);
```

**HACER**

```php
<?php
use OCP\AppFramework\Http;
use OCP\AppFramework\Http\DataResponse;
use OCP\Files\File;
use OCP\Files\IRootFolder;
use OCP\Files\NotFoundException;
use OCP\Files\NotPermittedException;

// $this->rootFolder is an injected IRootFolder, $userId the ID of the current user,
// $path the user-supplied path
try {
    $node = $this->rootFolder->getUserFolder($userId)->get($path);
} catch (NotFoundException|NotPermittedException $e) {
    // NotPermittedException is also thrown for paths containing ".."
    return new DataResponse([], Http::STATUS_NOT_FOUND);
}
if (!$node instanceof File) {
    return new DataResponse([], Http::STATUS_NOT_FOUND);
}
$content = $node->getContent();
```

### Inyección de comandos de shell

La [inyección de comandos de shell](https://en.wikipedia.org/wiki/Code_injection#Shell_injection) se produce si el código PHP ejecuta comandos de shell (p. ej., al ejecutar un compilador de latex). Antes de hacerlo, comprobar si hay una biblioteca PHP que ya proporcione la funcionalidad necesaria. Si de verdad hace falta ejecutar un comando, tener en cuenta que hay que escapar cada parámetro del usuario que se pase a una de estas funciones:

- **exec()**
- **shell_exec()**
- **passthru()**
- **proc_open()**
- **system()**
- **popen()**

:::{note}
Exigir o solicitar que otros programadores auditen la función de escapado.
:::

Si no se escapa la entrada del usuario, un atacante podrá ejecutar comandos de shell arbitrarios en el servidor.

PHP ofrece las siguientes funciones para escapar la entrada del usuario:

- **escapeshellarg()**: escapa una cadena para usarla como argumento de shell
- **escapeshellcmd()**: escapa los metacaracteres de shell

**NO HACER**

```php
<?php
system('ls '.$_GET['dir']);
```

**HACER**

```php
<?php
system('ls '.escapeshellarg($_GET['dir']));
```

### Omisión de autenticación / escalada de privilegios

La omisión de autenticación y la escalada de privilegios se producen cuando un usuario puede realizar acciones no autorizadas.

Nextcloud ofrece tres comprobaciones sencillas:

- **OCP\JSON::checkLoggedIn()**: comprueba si el usuario que ha iniciado sesión ha iniciado sesión
- **OCP\JSON::checkAdminUser()**: comprueba si el usuario que ha iniciado sesión tiene privilegios de administrador
- **OCP\JSON::checkSubAdminUser()**: comprueba si el usuario que ha iniciado sesión tiene privilegios de administrador de grupo

Con el App Framework, estas comprobaciones ya se realizan automáticamente en cada petición y hay que desactivarlas explícitamente mediante anotaciones sobre el método del controlador; consultar {nc-doc}`developer_manual/basics/controllers`.

Además, comprobar siempre si el usuario tiene derecho a realizar esa acción. (p. ej., un usuario no debería poder eliminar los marcadores de otros usuarios).

### Exposición de datos sensibles

Guardar siempre los datos de usuario o los archivos de configuración en ubicaciones seguras, p. ej., **nextcloud/data/**, y no en la raíz web, donde cualquiera puede acceder a ellos con un navegador web.

(nc-dev-csrf_introduction)=
### Falsificación de peticiones en sitios cruzados

Mediante [CSRF](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (véase también en [MDN](https://developer.mozilla.org/en-US/docs/Glossary/CSRF)) se puede engañar a un usuario para que ejecute una petición que no quería hacer. Por eso, toda petición POST y GET debe protegerse contra ello. Los únicos lugares donde no hacen falta comprobaciones CSRF son la plantilla principal, que renderiza la aplicación, o las interfaces que pueden llamarse externamente.

:::{note}
¡Enviar un formulario también es una petición POST/GET!
:::

Para prevenir el CSRF en una app, asegurarse de llamar al siguiente método al principio de todos los archivos:

```php
<?php
OCP\JSON::callCheck();
```

Si se usa el App Framework, cada método de controlador se comprueba automáticamente contra CSRF, salvo que se excluya explícitamente poniendo el atributo `#[NoCSRFRequired]` o la anotación `@NoCSRFRequired` antes del método del controlador; consultar {nc-doc}`developer_manual/basics/controllers`.

Además, se recomienda elegir con cuidado el método HTTP de las peticiones.
Las peticiones de tipo `GET` no deberían modificar datos, sino solo leer los existentes.
Así, al menos ninguna URL escrita (o copiada) podrá modificar datos (p. ej., al hacer clic por accidente en un enlace de un correo de spam).

### Redirecciones no validadas

Esto es más una molestia que una vulnerabilidad de seguridad crítica, ya que puede usarse para ingeniería social o phishing.

Validar siempre la URL antes de redirigir, comprobando si la URL solicitada está en el mismo dominio o es un recurso permitido.

**NO HACER**

```php
<?php
header('Location:'. $_GET['redirectURL']);
```

**HACER**

```php
<?php
header('Location: https://example.com'. $_GET['redirectURL']);
```

### CORS

El [intercambio de recursos de origen cruzado (CORS)](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) (véase también en [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)) es un método que implementan los navegadores para acceder a la vez a recursos de dominios distintos.
Supongamos que hay un sitio web publicado en el host A.
La URL sería, por ejemplo, `https://A/path/to/index.html`.
Si hay un host B \_distinto\_ que sirve un recurso (p. ej., un archivo de imagen) como `https://B/assets/image.jpg`, el archivo index del host A podría simplemente enlazar a la imagen de B.
Sin embargo, para proteger a B y su propiedad (la imagen), los navegadores no incrustan en silencio la imagen de B en la página de A.
En su lugar, el navegador pregunta amablemente a B si se permite incrustarla (la llamada [comprobación previa](https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request)).

Para ello, se hace una primera petición al recurso de B con el comando/verbo HTTP `OPTIONS`.
El servidor solo responde con las cabeceras especificadas y añade cabeceras `Access-Control-*`.
Estas definen qué se le permite hacer al navegador.
Solo si el servidor de destino B confirma que se permite el intercambio de recursos entre sitios, el navegador accede al recurso.

En el fondo, acceder a recursos ajenos no se limita a incrustar imágenes.
Con JavaScript, pueden dirigirse peticiones XHR/Ajax arbitrarias a otros hosts arbitrarios, lo que podría usarse para llamar a API que filtren los datos propios.
Hay algunas medidas de seguridad establecidas (sobre todo en el manejo de cookies), pero aun así hay que tener cuidado de no filtrar información sin querer.
En especial, si el servidor de destino B permite enviar credenciales mediante `Access-Control-Allow-Credentials: true`, las secuencias de comandos en sitios cruzados son muy críticas.
Hace falta tener establecida la {nc-ref}`protección CSRF <csrf_introduction>`; de lo contrario, los usuarios corren un riesgo relativamente alto.

### Obtener ayuda

Si se necesita ayuda para asegurarse de que una función es segura, preguntar en nuestro [foro](https://help.nextcloud.com).
````
