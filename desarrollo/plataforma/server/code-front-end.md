---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Preparar Node.js y npm, compilar componentes Vue, scripts, estilos y plantillas Handlebars del servidor, y confirmar los archivos compilados."
---
# Código de frontend

## Resumen

Esta página explica cómo preparar Node.js y npm, compilar los componentes y scripts de Vue, los estilos y las plantillas de Handlebars del servidor, y qué archivos compilados confirmar junto con los cambios. Está dirigida a quienes desarrollan el frontend del servidor.

````{upstream} developer_manual/server/code-front-end.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Requisitos previos: Node.js y npm

Nextcloud usa la versión **LTS activa actual** de Node.js y npm. El calendario puede consultarse en
[endoflife.date/nodejs](https://endoflife.date/nodejs).

Las versiones requeridas se declaran en el campo `engines` del `package.json` de la app, por ejemplo:

```json
{
    "engines": {
        "node": "^24.0.0",
        "npm": "^11.0.0"
    }
}
```

Se recomienda usar [nvm (Node Version Manager)](https://github.com/nvm-sh/nvm) para instalar las versiones de Node.js y cambiar entre ellas.
Una vez instalado nvm, la versión de Node.js requerida se instala y se activa con:

```console
# Install the Node.js version declared in .nvmrc or package.json engines
nvm install
nvm use

# Or install a specific version explicitly
nvm install 24
nvm use 24
```

Después, instalar o actualizar npm a la versión que requiere la app:

```console
npm install -g npm@11
```

:::{note}
Para la política completa de versiones de Node.js y npm de {vendor}`Nextcloud`, ver los
[estándares de Nextcloud](https://github.com/nextcloud/standards/issues/5).
:::

### Compilar los componentes y scripts de Vue

Se avanza cada vez más hacia el uso de Vue.js en el frontend, empezando por Ajustes. Para compilar el código tras los cambios, usar estos comandos de terminal en la carpeta raíz:

```console
# install dependencies
npm install

# build for development
npm run dev

# build for development and watch edits
npm run watch

# build for production with minification
npm run build
```

### Compilar los estilos

Los estilos se escriben en SCSS y se compilan a css.

```console
# install dependencies
make dev-setup

# compile style sheets
npm run sass

# compile style sheets and watch edits
npm run sass:watch
```

### Confirmar los cambios

**Al hacer cambios, ¡confirmar también los archivos compilados!**

En algunos lugares de Archivos y Ajustes todavía se usan plantillas de Handlebars. Se irán reemplazando paso a paso por Vue.js, pero mientras tanto hay que compilarlas por separado.

Si Handlebars aún no está instalado, puede instalarse con este comando de terminal:

```console
sudo npm install -g handlebars
```

Después, dentro de la carpeta raíz de la instalación local de desarrollo de Nextcloud, ejecutar este comando en la terminal cada vez que se haya cambiado un archivo `.handlebars`, para compilarlo:

```console
./build/compile-handlebars-templates.sh
```

Antes de confirmar cambios de JS, asegurarse de compilar también para producción:

```console
make build-js-production
```

Después, agregar los archivos compilados para confirmarlos.

Para ahorrar tiempo y recompilar solo una app concreta, usar lo siguiente y reemplazar el módulo por el nombre de la app:

```console
MODULE=user_status make build-js-production
```

Tener en cuenta que, si antes se usó `make build-js` o `make watch-js`, se verá que muchos archivos quedaron marcados como modificados, por lo que puede ser necesario limpiar primero el espacio de trabajo.
````
