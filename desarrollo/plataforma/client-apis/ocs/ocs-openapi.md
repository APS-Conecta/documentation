---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo añadir compatibilidad con OpenAPI a una app: requisitos, buenas prácticas, tipado de respuestas, ámbitos, etiquetas y generación de la especificación."
---
# Tutorial de OpenAPI para OCS

## Resumen

Esta página explica, para quienes desarrollan apps, cómo añadir compatibilidad con OpenAPI a una app para generar automáticamente su especificación desde el código: requisitos, buenas prácticas, un tutorial paso a paso y la generación de la especificación con openapi-extractor.

````{upstream} developer_manual/client_apis/OCS/ocs-openapi.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Esta página explica cómo añadir compatibilidad con OpenAPI a una app para poder generar automáticamente una especificación OpenAPI a partir del código.

Leer el tutorial completo antes de empezar a adaptar la app.

No hace falta entenderlo todo de antemano.
La herramienta `openapi-extractor` emitirá advertencias y fallará si algo está fundamentalmente roto.
Ejecutarla pronto y a menudo; normalmente señalará lo que hay que corregir.
Psalm también ayuda a validar los cambios y a detectar problemas de tipos antes de que se conviertan en problemas en tiempo de ejecución.

### Requisitos y requisitos previos

Antes de empezar, asegurarse de que se cumplen los siguientes requisitos:

- **La app es compatible con >=Nextcloud 28.**
  Nextcloud 28 es la primera versión que incluye los cambios del framework necesarios para la extracción de OpenAPI.

- **Psalm está instalado y configurado.**
  Psalm se usa para validar los tipos y las formas de los valores devueltos, de modo que `openapi-extractor` pueda inferir esquemas precisos.

  Instalar Psalm en la app como se explica en <https://psalm.dev/docs/running_psalm/installation>.

  Se necesita Psalm `>=5.9.0`. Las versiones anteriores contienen un error que impide que funcionen los cambios de este tutorial.

  Instalar y activar las extensiones necesarias como se explica en {nc-ref}`Extensiones de PHP necesarias <psalm-php-extensions>`.

  Configurar los siguientes manejadores de incidencias en la configuración de Psalm (ver <https://psalm.dev/docs/running_psalm/dealing_with_code_issues> para un tutorial):

  ```xml
  <LessSpecificReturnStatement errorLevel="error"/>
  <LessSpecificReturnType errorLevel="error"/>
  <LessSpecificImplementedReturnType errorLevel="error"/>
  <MoreSpecificReturnType errorLevel="error"/>
  ```

- **`openapi-extractor` está instalado.**
  Esta herramienta genera la especificación OpenAPI a partir del código del lado del servidor.

  Instalar `openapi-extractor` en la app como se explica en <https://github.com/nextcloud/openapi-extractor>.

### Buenas prácticas

Tener en cuenta que tras esta sección hay un tutorial paso a paso.
Se puede leer primero el tutorial y volver luego aquí como guía.

En resumen:

- Preferir endpoints OCS (`OCSController` + `DataResponse`) para las API públicas
- Añadir tipos explícitos en todas partes (parámetros, métodos auxiliares y tipos de retorno)
- Usar `\stdClass` para representar un objeto JSON vacío
- En los endpoints OCS, lanzar solo OCS\*Exceptions
- Mantener coherentes las formas de las respuestas dentro de cada grupo de códigos de estado (2xx juntos, 4xx juntos)
- Usar `setHeaders()` en lugar de `addHeader()`
- Evitar envoltorios de errores genéricos que hacen posible cualquier error en cualquier endpoint
- Añadir descripciones para los controladores, los parámetros, los métodos y los códigos de estado

#### Diseño y coherencia de la API

##### PREFERIR exponer las API mediante OCS

Ofrece una forma más estandarizada y más sencilla de escribir las API.
Los demás métodos se consideran heredados.
Para más detalles, ver {nc-ref}`OCS <ocscontroller>`.

**Ejemplos**

**Incorrecto**:

```php
class SomeController extends ApiController {
    ...

    public function someControllerMethod(): JSONResponse {
        ...
        return new JSONResponse(...);
    }
}
```

**Correcto**:

```php
class SomeController extends OCSController {
    ...

    public function someControllerMethod(): DataResponse {
        ...
        return new DataResponse(...);
    }
}
```

##### Tratar CON CUIDADO los valores vacíos en las respuestas JSON

Al definir las respuestas de la API, es importante dejar explícito si un valor vacío debe ser `null`, un objeto vacío (`{}`) o un array vacío (`[]`) en el JSON resultante. El tipo de PHP que se devuelve lo determina, y usar el equivocado puede producir fácilmente resultados confusos o incoherentes para quienes consumen la API.

:::{note}
En PHP, `null`, `[]` y `new \stdClass()` son tipos distintos y se serializan a valores distintos en JSON. Esto es especialmente importante para quienes consumen OpenAPI, que a menudo esperan un tipo coherente.
:::

Así se serializan los valores de PHP a JSON:

| Valor de PHP | Salida JSON |
|---|---|
| null | null |
| new \stdClass() | {} |
| [] | [] |

- Usar `null` para indicar que un valor está explícitamente ausente. Esto es lo preferible para la mayoría de las respuestas «vacías».
- Usar `new \stdClass()` **si y solo si** el cliente espera un objeto vacío (*{}*) en lugar de *null*. Esto lo exigen a veces contratos de esquema que siempre esperan la forma de un objeto, aunque esté vacío.

:::{important}
Devolver `new \stdClass()` como respuesta de la API requiere al menos Nextcloud 28 para que se serialice de forma fiable a `{}`.
:::

- **Evitar devolver `[]`** en endpoints de los que se espera un objeto JSON, ya que se serializará a un array JSON (*[]*), lo que obliga a quienes consumen la API a lidiar con tipos impredecibles.

Si se modifican o amplían API existentes y no es posible usar `null` o `\stdClass()` sin romper la compatibilidad con versiones anteriores, se puede tipar el resultado como `list<empty>` para indicar que se espera un array vacío.

**Ejemplos**

**Incorrecto (devuelve un array vacío en lugar de un objeto vacío o null)**:

```php
/**
 * @return DataResponse<Http::STATUS_OK, array, array{}>
 */
public function someControllerMethod() {
    // ...
    return new DataResponse([]);
}
```

**Correcto (datos vacíos como null)**:

```php
/**
 * @return DataResponse<Http::STATUS_OK, null, array{}>
 */
public function someControllerMethod() {
    // ...
    return new DataResponse(null); // Serializes to: null in JSON
}
```

**Correcto (objeto vacío explícito)**:

```php
/**
 * @return DataResponse<Http::STATUS_OK, \stdClass, array{}>
 */
public function someControllerMethod() {
    // ...
    return new DataResponse(new \stdClass()); // Serializes to: {} in JSON
}
```

**Para casos heredados o de compatibilidad (lista vacía explícita)**:

```php
/**
 * @return DataResponse<Http::STATUS_OK, list<empty>, array{}>
 */
public function someControllerMethod() {
    // ...
    return new DataResponse([]); // Serializes to: [] in JSON
}
```

##### USAR las mismas estructuras de datos para el mismo grupo de respuestas

Se recomienda usar `null` para representar datos vacíos.
Mantener coherentes las formas de las respuestas dentro de cada grupo de códigos de estado: todas las respuestas 2xx deben usar la misma estructura de datos, y
todas las respuestas 4xx deben usar la misma estructura de datos.

**Ejemplos**

**Incorrecto**:

```php
/**
 * @return DataResponse<Http::STATUS_OK, array{name: string}, array{}>|DataResponse<Http::STATUS_CREATED, array{id: int, name: string}, array{}>
 */
public function someControllerMethod() {
    ...
    if (...) {
        return new DataResponse(["name" => $name], Http::STATUS_OK);
    } else {
        return new DataResponse(["id" => $id, "name" => $name], Http::STATUS_CREATED);
    }
}

/**
 * @return DataResponse<Http::STATUS_BAD_REQUEST, array{error: string}, array{}>|DataResponse<Http::STATUS_FORBIDDEN, array{message: string}, array{}>
 */
public function someControllerMethod() {
    ...
    if (...) {
        return new DataResponse(["error" => "bad request"], Http::STATUS_BAD_REQUEST);
    } else {
        return new DataResponse(["message" => "forbidden"], Http::STATUS_FORBIDDEN);
    }
}
```

**Correcto**:

```php
/**
 * @return DataResponse<Http::STATUS_OK|Http::STATUS_CREATED, array{id: int, name: string}, array{}>
 */
public function someControllerMethod() {
    ...
    if (...) {
        return new DataResponse(["id" => $id, "name" => $name], Http::STATUS_OK);
    } else {
        return new DataResponse(["id" => $id, "name" => $name], Http::STATUS_CREATED);
    }
}

/**
 * @return DataResponse<Http::STATUS_BAD_REQUEST|Http::STATUS_FORBIDDEN, array{error: string}, array{}>
 */
public function someControllerMethod() {
    ...
    if (...) {
        return new DataResponse(["error" => "bad request"], Http::STATUS_BAD_REQUEST);
    } else {
        return new DataResponse(["error" => "forbidden"], Http::STATUS_FORBIDDEN);
    }
}
```

##### TENER EN CUENTA cómo se usará la API

Al construir la API, probablemente solo se piense en cómo implementarla de la forma más sencilla o mejor.
Hay que considerar lo que el código implica para quien intente usar la API a través de la especificación OpenAPI.

Un error habitual es un manejador de errores genérico («catch-all») que se reutiliza en muchos endpoints.
Son estupendos para la implementación de la API, porque ofrecen una solución sencilla que lo captura todo y no hay que preocuparse de manejar cada error correctamente.
No son buenos para la documentación OpenAPI ni para quienes consumen la API, porque verán que cualquier error puede producirse en cualquier endpoint, lo que la mayoría de las veces no es correcto.
En su lugar, conviene implementar el manejo de errores a mano y devolver solo los errores pertinentes allí donde realmente pueden aparecer.
Se pueden seguir usando métodos auxiliares con manejadores de incidencias genéricos donde tenga sentido, pero solo si todos los métodos del controlador que llaman a ese método auxiliar lanzan realmente las excepciones capturadas.

En particular, evitar patrones que hacen que *cada* endpoint parezca lanzar *cada* error que maneja un método auxiliar compartido,
aunque el endpoint no pueda producir realmente esos errores.

**Ejemplos**

**Incorrecto**:

```php
/**
 * @return DataResponse<Http::STATUS_OK, array{message: string}, array{}>|DataResponse<Http::STATUS_FORBIDDEN|Http::STATUS_NOT_FOUND, array{error: string}, array{}>
 */
public function someControllerMethod() {
    return $this->handleError(function() {
        ...
        if (...) {
            throw new PermissionError("some error");
        }
        ...
        return ["message" => "some message"];
    });
}

/**
 * @template T
 * @param Closure():T $callback
 *
 * @return DataResponse<Http::STATUS_OK, T, array{}>|DataResponse<Http::STATUS_FORBIDDEN|Http::STATUS_NOT_FOUND, array{error: string}, array{}>
 */
private function handleError(Closure $callback): DataResponse  {
    try {
        return new DataResponse($callback());
    } catch (PermissionError $e) {
        $message = ["error" => $e->getMessage()];
        return new DataResponse($message, Http::STATUS_FORBIDDEN);
    } catch (NotFoundError $e) {
        $message = ["error" => $e->getMessage()];
        return new DataResponse($message, Http::STATUS_NOT_FOUND);
    }
}
```

**Correcto**:

```php
/**
 * @return DataResponse<Http::STATUS_OK, array{message: string}, array{}>|DataResponse<Http::STATUS_FORBIDDEN, array{error: string}, array{}>
 */
public function someControllerMethod() {
    try {
        ...
        if (...) {
            throw new PermissionError("some error");
        }
        ...
        return new DataResponse(["message" => "some message"]);
    } catch (PermissionError $e) {
        $message = ["error" => $e->getMessage()];
        return new DataResponse($message, Http::STATUS_FORBIDDEN);
    }
}
```

#### Tipado y documentación

##### TIPAR los métodos de los controladores y los auxiliares de la forma más explícita posible

Cuanto más se acote un tipo sin violar ninguna restricción, mejor será la especificación resultante.
Psalm detectará estos problemas si se configuraron correctamente los manejadores de incidencias mencionados más arriba.

**Ejemplos**

**Incorrecto**:

```php
public function someHelperMethod(): array {
    ...
    return [
        "id" => $id,
        "name" => $name,
    ];
}
```

**Correcto**:

```php
/**
 * @return array{id: int, name: string}
 */
public function someHelperMethod(): array {
    ...
    return [
        "id" => $id,
        "name" => $name,
    ];
}
```

##### ESTABLECER todas las descripciones de los parámetros y los métodos

Mejora la documentación y facilita entender qué hace la API.

También se pueden establecer descripciones para los controladores.
Se incluirán en la especificación.
Allí se puede explicar qué hacen las API del controlador o dar ejemplos de cómo usar varios endpoints juntos.

**Ejemplos**

**Incorrecto**:

```php
class SomeController extends OCSController {
    /**
     * @return DataResponse<Http::STATUS_OK, array{name: string}, array{}>
     */
    public function someControllerMethod(int $id) {
        ...
        return new DataResponse(["name" => name], Http::STATUS_CREATED);
    }
}
```

**Correcto**:

```php
/**
 * Here you can put some explanations about all the endpoints or example code.
 */
class SomeController extends OCSController {
    /**
     * Here you give a short summary of the method
     *
     * Here you can give even more details about your method
     * and how you can use it.
     *
     * @param int $id Here you can describe your parameter
     *
     * @return DataResponse<Http::STATUS_OK, array{name: string}, array{}>
     */
    public function someControllerMethod(int $id) {
        ...
        return new DataResponse(["name" => name], Http::STATUS_CREATED);
    }
}
```

#### Errores y cabeceras

##### NO lanzar excepciones que no sean OCS\*Exceptions

En los endpoints OCS, lanzar solo OCS\*Exceptions. Otros tipos de excepción pueden producir respuestas de error que no son JSON (texto plano/HTML)
y no se representarán correctamente en la especificación OpenAPI extraída.

**Ejemplos**

**Incorrecto**:

```php
/**
 * @throws BadRequestException
 */
public function someControllerMethod() {
    ...
    throw new BadRequestException([]);
}
```

**Correcto**:

```php
/**
 * @throws OCSBadRequestException
 */
public function someControllerMethod() {
    ...
    throw new OCSBadRequestException("some message");
}
```

##### NO usar `addHeader` (usar `setHeaders`)

Psalm no puede rastrear las cabeceras establecidas con `addHeader()`, por lo que no pueden validarse ni incluirse correctamente en la especificación extraída.
Usar en su lugar el método `setHeaders`.

**Ejemplos**

**Incorrecto**:

```php
$response = new DataResponse();
$response->addHeader("X-My-Header", "some value");
return $response;
```

**Correcto**:

```php
$response = new DataResponse();
$response->setHeaders(["X-My-Header" => "some value"]);
return $response;
```

### Consejos y trucos

- `openapi-extractor` espera descripciones en muchos lugares.
  Para acelerar la adopción inicial, se puede usar `--allow-missing-docs` para ignorar las descripciones que faltan.

- De forma predeterminada, la herramienta puede detenerse en el primer error.
  Para listar varios problemas en una sola ejecución, usar `--continue-on-error`.

:::{warning}
No usar estas opciones al generar la especificación final.
Pueden ocultar problemas reales del código.
En particular, `--continue-on-error` es arriesgada, porque el comando puede parecer «correcto» aunque queden problemas.
Usar estas opciones solo para acelerar el proceso de adaptación inicial.
:::

### Tutorial: cómo añadir compatibilidad con OpenAPI a una API OCS

Supóngase que se construyó una app de lista de tareas (Todo) para Nextcloud y se tiene el siguiente controlador:

```php
class TodoApiController extends OCSController {
    #[NoAdminRequired]
    public function create(string $title, ?string $description = null, ?string $image = null): DataResponse {
        $todo = $this->service->createTodo($title, $description, $image);

        return $this->formatTodo($todo);
    }

    #[NoAdminRequired]
    public function get(int $id): DataResponse {
        try {
            $todo = $this->service->getTodo($id);
        } catch (NotFoundException $e) {
            return new DataResponse(["error" => "Todo not found"], Http::STATUS_NOT_FOUND);
        }

        return $this->formatTodo($todo);
    }

    #[NoAdminRequired]
    public function update(int $id, string $etag, ?string $title = null, ?string $description = null, ?string $image = null): DataResponse {
        try {
            $todo = $this->service->updateTodo($id, $etag, $title, $description, $image);
        } catch (NotFoundException $e) {
            return new DataResponse(["error" => "Todo not found"], Http::STATUS_NOT_FOUND);
        } catch (ForbiddenException $e) {
            return new DataResponse(["error" => "ETag does not match"], Http::STATUS_BAD_REQUEST);
        }

        return $this->formatTodo($todo);
    }

    #[NoAdminRequired]
    public function delete(int $id): DataResponse {
        try {
            $todo = $this->service->deleteTodo($id);
        } catch (NotFoundException $e) {
            return new DataResponse(["error" => "Todo not found"], Http::STATUS_NOT_FOUND);
        }

        return new DataResponse(null);
    }

    private function formatTodo(Todo $todo): DataResponse {
        return new DataResponse([
            "id" => $todo->id,
            "title" => $todo->title,
            "description" => $todo->description,
            "image" => $todo->image,
        ], Http::STATUS_OK, [
            "ETag" => $todo->etag,
        ]);
    }
}
```

Lo que se quiere hacer ahora es, en primer lugar, crear las anotaciones correctas de los parámetros y añadir descripciones. Podría quedar así:

```php
/**
 * Create a new Todo
 *
 * @param string $title The title of the new Todo item
 * @param string|null $description The description of the new Todo item. Can be left empty
 * @param string|null $image The base64-encoded image of the new Todo item. Can be left empty
 */
#[NoAdminRequired]
public function create(string $title, ?string $description = null, ?string $image = null): DataResponse {
    ...
}

/**
 * Get a Todo item
 *
 * @param int $id ID of the Todo item
 */
#[NoAdminRequired]
public function get(int $id): DataResponse {
    ...
}

/**
 * Update a Todo item
 *
 * @param int $id ID of the Todo item
 * @param string $etag ETag of the Todo item. If it does not match the ETag that is stored on the server the request will be rejected
 * @param string|null $title The new title of the Todo item. Can be left empty to not update the title
 * @param string|null $description The new description of the Todo item. Can be left empty to not update the description
 * @param string|null $image The new base64-encoded image of the Todo item. Can be left empty to not update the image
 */
#[NoAdminRequired]
public function update(int $id, string $etag, string $title = null, string $description = null, string $image = null): DataResponse {
    ...
}

/**
 * Delete a Todo item
 *
 * @param int $id ID of the Todo item
 */
#[NoAdminRequired]
public function delete(int $id): DataResponse {
    ...
}
```

El siguiente paso es añadir los tipos de retorno.
Este es el paso más importante para que la API quede documentada.

Lo mejor es empezar por los métodos auxiliares que se usan varias veces, como el método `formatTodo` de este ejemplo:

```php
/**
 * @return DataResponse<Http::STATUS_OK, array{id: int, title: string, description: ?string, image: ?string}, array{ETag: string}>
 */
private function formatTodo(Todo $todo): DataResponse() {
    ...
}
```

El tipo de retorno de [*DataResponse*](https://github.com/nextcloud/server/blob/master/lib/public/AppFramework/Http/DataResponse.php) y de otras clases que heredan de [*Response*](https://github.com/nextcloud/server/blob/master/lib/public/AppFramework/Http/Response.php) espera argumentos distintos. Ver las anotaciones de sus clases en el código. La siguiente tabla lista algunas habituales:

| Clase que hereda de Response | Argumentos esperados |
|---|---|
| *DataResponse* | código de estado, datos, cabeceras |
| *RedirectResponse* | código de estado, cabeceras |
| *StreamResponse* | código de estado, cabeceras |
| *TemplateResponse* | código de estado, cabeceras |

Después se pueden añadir los tipos de retorno a todos los demás métodos.
Si dos códigos de estado distintos devuelven la misma estructura de datos y las mismas cabeceras, se puede usar el operador de unión para indicarlo: `Http::STATUS_BAD_REQUEST|Http::STATUS_NOT_FOUND`.

Para dudas sobre la sintaxis de los tipos de retorno, puede ser útil la documentación de Psalm sobre el [tipado en Psalm](https://psalm.dev/docs/annotating_code/typing_in_psalm/).

Hay que añadir una descripción para cada código de estado que devuelve el método.

```php
/**
 * ...
 *
 * @return DataResponse<Http::STATUS_OK, array{id: int, title: string, description: ?string, image: ?string}, array{ETag: string}>
 *
 * 200: Todo item created
 */
#[NoAdminRequired]
public function create(string $title, string $description = null, string $image = null): DataResponse {
    ...
}

/**
 * ...
 *
 * @return DataResponse<Http::STATUS_OK, array{id: int, title: string, description: ?string, image: ?string}, array{ETag: string}>|DataResponse<Http::STATUS_NOT_FOUND, array{error: string}, array{}>
 *
 * 200: Todo item returned
 * 404: Todo item not found
 */
#[NoAdminRequired]
public function get(int $id): DataResponse {
    ...
}

/**
 * ...
 *
 * @return DataResponse<Http::STATUS_OK, array{id: int, title: string, description: ?string, image: ?string}, array{ETag: string}>|DataResponse<Http::STATUS_BAD_REQUEST|Http::STATUS_NOT_FOUND, array{error: string}, array{}>
 *
 * 200: Todo item created
 * 400: ETag of the Todo item does not match
 * 404: Todo item not found
 */
#[NoAdminRequired]
public function update(int $id, string $etag, string $title = null, string $description = null, string $image = null): DataResponse {
    ...
}

/**
 * ...
 *
 * @return DataResponse<Http::STATUS_OK, null, array{}>|DataResponse<Http::STATUS_NOT_FOUND, array{error: string}, array{}>
 *
 * 200: Todo item deleted
 * 404: Todo item not found
 */
#[NoAdminRequired]
public function delete(int $id): DataResponse {
    ...
}
```

### Ámbitos

En algunos casos, quien consume la API puede no querer o no necesitar implementar todas las API que ofrece la app.
Algunos ejemplos son la federación entre apps de distintos servidores, los endpoints relacionados con la administración y otros.
El cliente predeterminado, que debería implementar la funcionalidad principal, se llama `OpenAPI::SCOPE_DEFAULT`.
Hay constantes disponibles en `OCP\AppFramework\Http\Attribute\OpenAPI::SCOPE_*` para una mejor experiencia entre apps.
Un controlador y sus métodos pueden tener varios ámbitos; sin embargo, cuando un método tiene el atributo establecido,
se ignoran todos los ámbitos del controlador.

Los métodos que requieren permisos de administración, porque les falta `#[NoAdminRequired]` o tienen un atributo `#[PublicPage]` o la
anotación correspondiente, tienen como ámbito predeterminado `OpenAPI::SCOPE_ADMINISTRATION`.

```php
#[OpenAPI(scope: OpenAPI::SCOPE_ADMINISTRATION)]
#[OpenAPI(scope: OpenAPI::SCOPE_FEDERATION)]
#[OpenAPI(scope: OpenAPI::SCOPE_DEFAULT)]
#[OpenAPI(scope: 'myscope')]
public function show(): TemplateResponse {
    ...
}
```

Los distintos ámbitos se guardan como `openapi.json` para el ámbito predeterminado y como `openapi-{scope}.json` para los demás.

### Etiquetas

Para organizar los endpoints de la API dentro de un ámbito, se pueden usar etiquetas que los agrupen. De forma predeterminada se usa el nombre del controlador.
Las etiquetas también pueden diferir entre ámbitos distintos.

```php
#[OpenAPI(scope: OpenAPI::SCOPE_DEFAULT, tags: ['mytag1'])]
#[OpenAPI(scope: OpenAPI::SCOPE_ADMINISTRATION, tags: ['settings', 'custom2'])]
public function saveSettings(): TemplateResponse {
    ...
}
```

### Definiciones de tipos de respuesta compartidas

En los pasos anteriores se ha reutilizado varias veces la misma estructura de datos, pero se copió cada vez.
Esto es tedioso y propenso a errores, por lo que se quieren crear algunas definiciones de tipos compartidas.
Crear un archivo nuevo llamado `ResponseDefinitions.php` en la carpeta `lib` de la app.
Solo funciona con ese nombre de archivo y en esa ubicación.

```php
/**
 * @psalm-type TodoItem = array{
 *     id: int,
 *     title: string,
 *     description: ?string,
 *     image: ?string,
 * }
 */
class ResponseDefinitions {}
```

El nombre de cada definición de tipo debe empezar por el *ID legible de la app*, tal como lo espera openapi-extractor.
Es una forma en TitleCase / normalizada que se usa para dar a los tipos un espacio de nombres por app (por ejemplo, la app `Tables`
usa tipos como `TablesColumn`.

Para importar y usar la definición de tipo, hay que importarla en el controlador:

```php
/**
 * @psalm-import-type TodoItem from ResponseDefinitions
 */
class TodoApiController extends OCSController {
    ...
}
```

Ahora se puede sustituir cada aparición de `array{id: int, title: string, description: ?string, image: ?string}` por `TodoItem`.

### Manejar excepciones

A veces se quiere terminar con una excepción en lugar de devolver una respuesta.
En este ejemplo, `update` lanzará una excepción cuando el ETag no coincida:

```php
#[NoAdminRequired]
public function update(int $id, string $etag, string $title = null, string $description = null, string $image = null): DataResponse {
    ...
    } catch (ForbiddenException $e) {
        throw new OCSBadRequestException("ETag does not match");
    }
    ...
}
```

Añadir la anotación correcta se hace así:

```php
/**
 * ...
 *
 * @throws OCSBadRequestException ETag of the Todo item does not match
 */
#[NoAdminRequired]
public function update(int $id, string $etag, string $title = null, string $description = null, string $image = null): DataResponse {
    ...
}
```

La descripción que sigue al nombre de la clase de la excepción funciona exactamente igual que la descripción de los códigos de estado añadida antes.
Tener en cuenta que solo deben usarse OCS\*Exceptions, ya que cualquier otra excepción produce un cuerpo de texto plano en lugar de JSON.

### Ignorar ciertos endpoints

La herramienta ya ignora todos los endpoints que no son accesibles desde fuera, pero algunas apps tienen endpoints accesibles que no son API (p. ej., los que sirven HTML).
Para ignorarlos se puede añadir el atributo `#[OpenAPI(scope: OpenAPI::SCOPE_IGNORE)]` al método del controlador
o a la clase del controlador. También existe un atributo obsoleto, `#[IgnoreOpenAPI]` (obsoleto desde Nextcloud 28), por compatibilidad, pero
debe preferirse `OpenAPI::SCOPE_IGNORE`:

```php
/**
 * ...
 *
 * @IgnoreOpenAPI
 */
#[OpenAPI(scope: OpenAPI::SCOPE_IGNORE)]
#[NoAdminRequired]
public function show(): TemplateResponse {
    ...
}
```

### Exponer capacidades

Supóngase que, con la misma app Todo del ejemplo anterior, se quieren exponer algunas capacidades para que los clientes sepan qué pueden esperar.
Primero, crear *Capabilities* en la carpeta *lib*:

```php
class Capabilities implements ICapability {
    public function getCapabilities() {
        return [
            "todo" => [
                "supported-operations" => ["create", "read", "update", "delete"],
                "emojis-supported" => true,
            ],
        ];
    }
}
```

Ahora hay que añadir la anotación correcta del tipo de retorno:

```php
class Capabilities implements ICapability {
    /**
     * @return array{todo: array{supported-operations: list<string>, emojis-supported: bool}}
     */
    public function getCapabilities() {
        return [
            "todo" => [
                "supported-operations" => ["create", "read", "update", "delete"],
                "emojis-supported" => true,
            ],
        ];
    }
}
```

Las capacidades aparecerán automáticamente en la especificación generada.

Hay que registrar *Capabilities* en el archivo *lib/AppInfo/Application.php* e implementar *IBootstrap*:

```php
namespace OCA\Todo\AppInfo;

use OCA\Todo\Capabilities;
use OCP\AppFramework\Bootstrap\IBootstrap;

class Application extends App implements IBootstrap {
    public const APP_ID = 'todo';

    public function __construct(array $urlParams = []) {
        parent::__construct(self::APP_ID, $urlParams);
    }

    public function register(IRegistrationContext $context): void {
        // code

        $context->registerCapability(Capabilities::class);
    }

    public function boot(IBootContext $context): void {
    }
}
```

### Generar la especificación

Si se siguieron las instrucciones de instalación de openapi-extractor, se puede ejecutar `composer exec generate-spec` en la
carpeta raíz de la app y se obtendrá un archivo nuevo llamado `openapi.json` (según los ámbitos usados).
Si la herramienta falla en algún punto, indicará qué está mal y, a menudo, también cómo corregir el problema.
Además, conviene ejecutar Psalm para comprobar si hay algún problema.
````
