---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Estándares de código de JavaScript y Typescript: Vue, ESLint, estructura de archivos, nombres, sangría, cadenas, funciones, objetos y operadores."
---
# JavaScript y Typescript

## Resumen

Esta página recoge las reglas y los consejos para escribir JavaScript y Typescript: el uso de Vue y Typescript, la configuración compartida de ESLint, la estructura de archivos de una app y el estilo de código, con ejemplos de qué hacer y qué no. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/getting_started/coding_standards/javascript.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

### Reglas y consejos generales

- Nextcloud usa Vue.js para su interfaz; para una interfaz de usuario coherente, recomendamos que las apps también usen Vue con los {nc-ref}`componentes proporcionados <js-library_nextcloud-vue>`.
  Aun así, también se pueden usar JavaScript y HTML puros.
- Recomendamos usar Typescript por su comprobación de tipos y sus funciones mejoradas de análisis estático del código.
- No crear variables globales; en su lugar, si hace falta, usar objetos de espacio de nombres globales como `OCA.YourApp.…`
- Usar el modo estricto de JavaScript (es así automáticamente al usar módulos de JavaScript)

#### Configuración de ESLint

Hay una configuración compartida de [eslint](https://eslint.org/) que se puede usar para formatear automáticamente el código JavaScript y Typescript de las apps de Nextcloud.
Consta de dos partes: un [paquete de configuración](https://github.com/nextcloud-libraries/eslint-config) que contiene las preferencias de formato
y un [plugin](https://github.com/nextcloud-libraries/eslint-plugin) para detectar las API obsoletas y eliminadas en el código. Consultar sus README para obtener instrucciones.

#### Estructura del sistema de archivos

Para JavaScript puro recomendamos la siguiente estructura:

- `appid/`: raíz de la app
  - `js/`: archivos JavaScript
    - `appid.js`: el punto de entrada de la app
  - `css/`: ubicación de todos los archivos CSS
    - `appid.css`

Al usar un empaquetador para compilar Typescript (o JavaScript), recomendamos la siguiente estructura:

- `appid/`: raíz de la app
  - `js/`: archivos JavaScript compilados
  - `css/`: salida CSS compilada
  - `src/`: raíz de todos los archivos fuente
    - `components/`: ubicación de los componentes Vue
    - `composables/`: ubicación de los composables de Vue
    - `services/`: ubicación de los archivos de servicios, como las abstracciones de API
    - `stores/`: ubicación de los stores de Pinia
    - `views/`: ubicación de las vistas
    - `main.ts`: punto de entrada principal de la app

##### Nombres de archivo

No tenemos reglas estrictas para los nombres de archivo: sirve tanto kebab case como camel case.

Aun así, recomendamos encarecidamente que las apps Vue sigan las recomendaciones de Vue y usen como nombre de archivo el mismo nombre del componente.
P. ej., si el componente se llama `AppRoot`, el archivo debe llamarse `AppRoot.vue`.

### Estilo de código

#### General

##### Nombres y mayúsculas

- Usar **camelCase** para

  - funciones
  - métodos
  - propiedades
  - variables

- Usar **PascalCase** para

  - clases
  - enums
  - tipos
  - interfaces
  - componentes Vue

- Por legibilidad, poner en mayúscula solo la primera letra de las abreviaturas, como `callHttpApi()` en lugar de `callHTTPAPI()`.
- Los subcomponentes deben llevar prefijo.
  P. ej., al dividir un componente como `FileListEntry` en componentes más pequeños llamados `FileListEntryName`, `FileListEntryIcon` …
- Los componentes no deben tener nombres de una sola palabra, ya que podrían entrar en conflicto con etiquetas HTML nativas actuales o futuras, que siempre son de una sola palabra.
  P. ej., si se tiene una vista de ajustes, no llamarla `Settings` sino `SettingsView` o `UserSettings`, etc.

:::{list-table} Usar camelCase para funciones, métodos, propiedades y variables
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    const fileId = 123
    const obj = {
        myProperty: false,
    }
    doSomething()
    ```
  -
    ```javascript
    const file_id = 123
    const obj = {
        'my-property': false,
    }
    do_something()
    ```
:::

:::{list-table} Usar PascalCase para clases, interfaces, tipos y componentes Vue
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    class MyClass { /* ... */ }
    interface IRequest { /* ... */ }
    type Arguments = string[]
    ```
  -
    ```javascript
    class myClass { /* ... */ }
    interface I_request { /* ... */ }
    type arguments = string[]
    ```
:::

##### Sangría

- Usar tabulaciones en lugar de espacios para sangrar; el ancho de la tabulación es de 4 espacios.

  - Se pueden alinear, p. ej., los comentarios con espacios si hace falta.

##### Punto y coma

:::{list-table} Evitar el punto y coma donde no sea necesario.
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    const text = 'foo'
    doSomething()
    ```
  -
    ```javascript
    const text = 'foo';
    doSomething();
    ```
* -
    ```javascript
    const text = 'foo'
    ;(someProp as SomeType).handle()
    ```
  -
:::

#### Cadenas

:::{list-table} Usar comillas simples.
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    const text = 'foo'
    ```
  -
    ```javascript
    const text = "foo"
    ```
:::

:::{list-table} Preferir las plantillas literales por legibilidad.
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    const text = `Hello ${username}!`
    ```
  -
    ```javascript
    const text = 'Hello ' + username
    ```
:::

#### Arrays

:::{list-table} Evitar varias propiedades en la misma línea
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    const arr = [
        'first',
        'second',
        'third',
    ]
    ```
  -
    ```javascript
    const arr = ['first', 'second', 'third']
    ```
:::

:::{list-table} Usar comas finales; esto reduce el diff al añadir propiedades nuevas.
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    const arr = [
        'first',
        'second',
        'third',
    ]
    ```
  -
    ```javascript
    const arr = [
        'first',
        'second',
        'third'
    ]
    ```
* -
    ```diff
    const arr = [
        'first',
        'second',
    +   'third',
    ]
    ```
  -
    ```diff
    const arr = [
        'first',
    -   'second'
    +   'second',
    +   'third'
    ]
    ```
:::

#### Funciones

- Sin espacios entre el nombre de la función y los parámetros.
- Llaves en la misma línea que la definición.
- Usar saltos de línea coherentes en los parámetros (o todos en una línea, o un parámetro por línea).
- Para las funciones de nivel superior, preferir las funciones normales a las funciones flecha.
  En Javascript, las funciones definidas con la palabra clave `function` se elevan (hoisting), así que pueden usarse incluso en otras funciones situadas antes de su definición.
  Además, usar la palabra clave `function` hace la definición más explícita, lo que favorece la legibilidad.
  Para los callbacks, las funciones flecha anónimas suelen ser más adecuadas, ya que no crean su propio enlace de `this`.
- Usar siempre paréntesis en las funciones flecha. Esto ayuda a la legibilidad y evita problemas si se añaden parámetros.
- Al usar valores de retorno implícitos en funciones flecha con un cuerpo de varias líneas, rodear el cuerpo con paréntesis.

:::{list-table} Sin espacio entre el nombre de la función y los parámetros
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    doSomething(1, false)
    ```
  -
    ```javascript
    doSomething (1, false)
    ```
:::

:::{list-table} Llaves en la misma línea que la definición.
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    function foo(name: string): boolean {
        // do something
    }
    ```
  -
    ```javascript
    function foo(name: string): boolean
    {
        // do something
    }
    ```
* -
    ```javascript
    function bar(
        firstName: string,
        lastName: string,
    ): boolean {
        // do something
    }
    ```
  -
    ```javascript
    function bar(
        firstName: string,
        lastName: string,
    ): boolean
    {
        // do something
    }
    ```
* -
    ```javascript
    const arrow = (name: string) => {
        // do something
    }
    ```
  -
    ```javascript
    const arrow = (name: string) =>
    {
        // do something
    }
    ```
:::

:::{list-table} Usar saltos de línea coherentes en los parámetros de las funciones
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    function doSomething(num: number, enable: boolean) {
        // ...
    }
    ```
  -
    ```javascript
    function doSomething(num: number,
        enable: boolean) {
        // ...
    }
    ```
* -
    ```javascript
    function doSomething(
        num: number,
        enable: boolean,
    ) {
        // ...
    }
    ```
  -
    ```javascript
    function doSomething(
        num: number, enable: boolean,
    ) {
        // ...
    }
    ```
:::

:::{list-table} Preferir funciones normales en el nivel superior.
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    export function doSomething(num: number, enable: boolean) {
        // ...
    }
    ```
  -
    ```javascript
    export const doSomething = (num: number, enable: boolean) => {
        // ...
    }
    ```
* -
    ```javascript
    someArray.map((item) => item.name)
    // or
    someArray.map((item) => {
        return item.name
    })
    ```
  -
    ```javascript
    // while this is valid and work
    someArray.map(function (item) {
        return item.name
    })
    // there is a caveat with accessing "this"
    someArray.map(function (item) {
        // "this" is not the previous context
        // but the context of the callback function.
        // Thus this.category will be undefined.
        return `${this.category}: ${item.name}`
    })
    ```
:::

:::{list-table} Usar siempre paréntesis en los parámetros de las funciones flecha.
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    myArray.map((item) => item.name)
    ```
  -
    ```javascript
    myArray.map(item => item.name)
    ```
* -
    ```javascript
    myArray.map((item, index) => getName(item, index))
    ```
  -
:::

:::{list-table} Usar paréntesis en el cuerpo de varias líneas de las funciones flecha.
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    myArray.map((item) => (
        item.value
            ? 'yes'
            : 'no'
    ))
    ```
  -
    ```javascript
    myArray.map((item) => item.value
        ? 'yes'
        : 'no'
    )
    ```
* -
    ```javascript
    myArray.map((item) => ({
        prop: item.value,
        other: true,
    }))
    ```
  -
:::

#### Objetos

:::{list-table} Poner comillas en las propiedades solo cuando haga falta.
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    const obj = {
        noQuotesNeeded: true,
        'quotes-needed': false,
    }
    ```
  -
    ```javascript
    const obj = {
        'noQuotesNeeded': true,
        'quotes-needed': false,
    }
    ```
:::

:::{list-table} Preferir las propiedades abreviadas
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    const name = 'jdoe'
    // ...
    const obj = {
        name,
        id: 123,
    }
    ```
  -
    ```javascript
    const name = 'jdoe'
    // ...
    const obj = {
        name: name,
        id: 123,
    }
    ```
:::

:::{list-table} Evitar varias propiedades en la misma línea
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    const obj = {
        first: 1,
        second: 'two',
    }
    ```
  -
    ```javascript
    const obj = { first: 1, second: 'two' }
    ```
:::

:::{list-table} Añadir espacios alrededor del contenido cuando haga falta
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    const obj = { prop: true }
    ```
  -
    ```javascript
    const obj = {prop: true}
    ```
:::

:::{list-table} Usar comas finales; esto reduce el diff al añadir propiedades nuevas.
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    const obj = {
        first: 1,
        second: 2,
    }
    ```
  -
    ```javascript
    const obj = {
        first: 1,
        second: 2
    }
    ```
* -
    ```diff
    const obj = {
        first: 1,
        second: 2,
    +   third: 3,
    }
    ```
  -
    ```diff
    const obj = {
        first: 1,
    -   second: 2
    +   second: 2,
    +   third: 3
    }
    ```
:::

#### Operadores

- Usar siempre `===` y `!==` en lugar de `==` y `!=`
- Preferir las comparaciones explícitas

Este es el motivo:

```javascript
'' == '0'           // false
0 == ''             // true
0 == '0'            // true

false == 'false'    // false
false == '0'        // true

false == undefined  // false
false == null       // false
null == undefined   // true

' \t\r\n ' == 0     // true
```

:::{list-table} Usar comparaciones explícitas
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    if (array.length > 0) { /* ... */ }
    ```
  -
    ```javascript
    if (array.length) { /* ... */ }
    ```
* -
  -
    ```javascript
    if (array) { /* this is always true! */ }
    ```
:::

#### Estructuras de control

- Usar siempre llaves, también en los *if* de una sola línea
- Dividir los *if* largos en varias líneas
- Usar siempre break en las sentencias switch y prevenir con advertencias un bloque default si no se debe acceder a él

:::{list-table} Usar siempre llaves.
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    if (myVar === 'hi') {
        doSomething()
    }
    ```
  -
    ```javascript
    if (array.length > 0) doSomething()
    ```
* -
    ```javascript
    for (let i = 0; i < 4; i++) {
        // your code
    }
    ```
  -
    ```javascript
    for (let i = 0; i < 4; i++)
        // your code
    ```
:::

:::{list-table} Dividir las condiciones largas en varias líneas.
:widths: 50 50
:header-rows: 1

* - ✅ Hacer
  - ❌ No hacer
* -
    ```javascript
    if (something === 'something'
        || condition2
        && condition3
    ) {
        // your code
    }
    ```
  -
    ```javascript
    if (something === 'something' || condition2 && condition3) {
        // your code
    }
    ```
:::
````
