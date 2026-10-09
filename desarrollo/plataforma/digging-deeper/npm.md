---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Convenciones de scripts npm para las apps: build, dev y watch, test y lint en package.json, con ejemplos para webpack, eslint y stylelint."
---
(nc-dev-app-npm)=
# NPM

## Resumen

Esta página explica la convención de scripts de `package.json` que se recomienda seguir en las apps: `build`, `dev` y `watch`, `test` y, de forma opcional, `lint` y `stylelint`, con ejemplos para webpack. Está dirigida a quienes desarrollan apps con dependencias de JavaScript.

````{upstream} developer_manual/digging_deeper/npm.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El gestor de paquetes de node `npm` es una herramienta muy usada para gestionar dependencias de JavaScript. Para facilitar a todo el mundo la configuración del proyecto, se recomienda seguir la convención de scripts típicos como `build`, `watch` y `test` en el archivo `package.json`.

Se puede encontrar más información sobre esta convención en entradas de blog como esta <https://www.keithcirkel.co.uk/how-to-use-npm-as-a-build-tool/>.

(nc-dev-app-npm-build)=
### npm build

Una vez ejecutado `npm install` (`npm i` para abreviar) para instalar todas las dependencias especificadas
en `package.json`, normalmente hay que compilar el proyecto. La compilación puede hacerse con herramientas como
Webpack, Grunt o similares. Para unificar el comando de compilación en todas las apps de Nextcloud, basta con agregar el comando
o los comandos de compilación como script `build` a su.

Para las apps que usan webpack, podría verse así:

```json
{
  "name": "myapp",
  "scripts": {
    "build": "webpack --node-env production --progress --hide-modules --config webpack.prod.js"
  },
  "devDependencies": {
    "webpack": "^5.65.0",
    "webpack-cli": "^4.9.1",
  }
}
```

Después se puede ejecutar `npm build` en el directorio raíz de la app para lanzar el proceso de compilación.

Ver la [documentación de npm-build](https://docs.npmjs.com/cli/build) para más información.

### npm run dev, npm run watch

Como compilar la versión de publicación de los scripts de JavaScript puede ser lento, las apps suelen tener un paso
de compilación dedicado al desarrollo que compila más rápido y habilita la salida de depuración. Además, puede indicar
al empaquetador que escuche los cambios en los archivos y vuelva a compilar el proyecto (de forma incremental).

Este comando debe agregarse a `package.json` como script `dev` y `watch`:

```json
{
  "name": "myapp",
  "scripts": {
    "build": "webpack --node-env production --progress --hide-modules --config webpack.prod.js",
    "dev": "webpack --node-env development --progress --config webpack.dev.js",
    "watch": "webpack --node-env development --progress --watch --config webpack.dev.js"
  },
  "devDependencies": {
    "webpack": "^5.65.0",
    "webpack-cli": "^4.9.1",
  }
}
```

La compilación de desarrollo se lanza con `npm run dev` o, si se quiere dejar el proceso en ejecución y actualizar con cada cambio hecho en los archivos fuente, con `npm run watch`.

### npm test

Npm ejecutará el script `test` cuando se ejecute `npm test`, por lo que conviene especificar el
comando o los comandos de prueba así:

```json
{
  "scripts": {
    "test": "mocha-webpack --webpack-config webpack.test.js --require src/tests/setup.js \"src/tests/**/*.spec.js\""
  }
}
```

Hay más información sobre este comando en la [documentación de npm-test](https://docs.npmjs.com/cli/test).

### npm run lint (opcional)

Las apps de Nextcloud que usan herramientas de linting para dar un formato de código coherente suelen agregar un script `lint` a su
`package.json` e instalar la [configuración de eslint](https://www.npmjs.com/package/@nextcloud/eslint-config) correspondiente:

```json
{
  "scripts": {
    "lint": "eslint --ext .js,.vue src",
    "lint:fix": "eslint --ext .js,.vue src --fix"
  }
}
```

Si el linting de estilos es un script aparte, debe usarse `stylelint` como nombre de script convencional.
También se puede encontrar en npm la [configuración de stylelint](https://www.npmjs.com/package/@nextcloud/stylelint-config) estándar de nextcloud.

```json
{
  "scripts": {
    "stylelint": "stylelint src",
    "stylelint:fix": "stylelint src --fix"
  }
}
```
````
