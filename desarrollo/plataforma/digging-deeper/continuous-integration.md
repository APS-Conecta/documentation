---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo configurar la integración continua de una app: linting de info.xml, php y php-cs, y análisis estático con Psalm en GitHub Actions."
---
(nc-dev-app-ci)=
# Integración continua

## Resumen

Esta página explica qué incluye la integración continua de una app y cómo configurarla: el linting de `info.xml`, de php y con php-cs, y el análisis estático con Psalm, con sus plantillas de GitHub Actions. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/continuous_integration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Se recomienda encarecidamente configurar pruebas automatizadas para la app, de modo que cada cambio tenga que superar un procedimiento definido antes de aceptarse en la rama principal del repositorio. La integración continua suele incluir

- Linting: comprobar la sintaxis de los archivos fuente, p. ej., de todos los scripts php
- Análisis estático: hacer que herramientas comprueben la solidez de tipos de la app; se usa sobre todo para php
- Pruebas unitarias: ejecutar pruebas unitarias del front-end y del back-end, en las que clases y componentes individuales se prueban de forma aislada
- Pruebas de integración: probar los componentes cuando se combinan

Hay una lista de plantillas de workflows de github disponibles en el [repositorio de plantillas de nextcloud](https://github.com/nextcloud/.github).

### Linting

#### info.xml

Se puede validar el archivo `info.xml` de {nc-ref}`metadatos de la app <app metadata>` de una app con una
[github action sencilla](https://github.com/nextcloud/.github/blob/master/workflow-templates/lint-info-xml.yml).
Consultar el [repositorio de plantillas de nextcloud](https://github.com/nextcloud/.github) para obtener una plantilla actualizada.

#### php

Un lint de todos los archivos fuente php puede encontrar errores de sintaxis que podrían hacer fallar la aplicación en producción. Las github actions están en el [repositorio de plantillas de nextcloud](https://github.com/nextcloud/.github).
También se necesita el siguiente script de lint en el `composer.json`:

```json
{
  "scripts": {
    "lint": "find . -name \\*.php -not -path './vendor/*' -print0 | xargs -0 -n1 php -l"
  }
}
```

#### php-cs

Se fomenta el uso del linting con php-cs. Hay documentación sobre cómo configurarlo en el
[repositorio coding-standard de nextcloud](https://github.com/nextcloud/coding-standard), así como las
github actions correspondientes en el [repositorio de plantillas de nextcloud](https://github.com/nextcloud/.github).

(nc-dev-app-static-analysis)=
### Análisis estático

[Psalm][Psalm] es una herramienta de análisis estático que puede comprobar si el código de la app usa correctamente todos los tipos, por ejemplo, si las clases y los métodos existen.
Para la configuración básica, ver el sitio web de [Psalm][Psalm]. Para que Psalm conozca las interfaces de Nextcloud (el espacio de nombres OCP),
se puede instalar el [paquete de la API](https://packagist.org/packages/nextcloud/ocp).
Después se podrá comprobar la app con el siguiente `psalm.xml`, que debe colocarse en la raíz de la app.

```xml
<?xml version="1.0"?>
<psalm
    totallyTyped="true"
    errorLevel="5"
    resolveFromConfigFile="true"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="https://getpsalm.org/schema/config"
    xsi:schemaLocation="https://getpsalm.org/schema/config vendor/vimeo/psalm/config.xsd"
    errorBaseline="tests/psalm-baseline.xml"
>
    <projectFiles>
        <directory name="lib" />
        <ignoreFiles>
            <directory name="vendor" />
            <directory name="lib/Vendor" />
        </ignoreFiles>
    </projectFiles>
    <extraFiles>
        <directory name="vendor" />
        <ignoreFiles>
            <directory name="vendor/phpunit/php-code-coverage" />
        </ignoreFiles>
    </extraFiles>
    <issueHandlers>
        <UndefinedClass>
            <errorLevel type="suppress">
                <referencedClass name="OC" />
            </errorLevel>
        </UndefinedClass>
        <UndefinedDocblockClass>
            <errorLevel type="suppress">
                <referencedClass name="Doctrine\DBAL\Schema\Schema" />
                <referencedClass name="Doctrine\DBAL\Schema\SchemaException" />
                <referencedClass name="Doctrine\DBAL\Driver\Statement" />
                <referencedClass name="Doctrine\DBAL\Schema\Table" />
            </errorLevel>
        </UndefinedDocblockClass>
    </issueHandlers>
</psalm>
```

:::{note}
La definición suprime los usos de la clase global y estática `OC`, como `\OC::$server`, que se
desaconsejan pero aún se encuentran en algunas apps. La supresión de doctrine es necesaria actualmente porque los mappers
de la base de datos y las abstracciones del esquema filtran algunas de las bibliotecas de terceros de Nextcloud que Psalm no conoce.
:::

Este proceso se puede incluir en una GitHub Action que se ejecute en cada pull request.
Ver la [github action de psalm](https://github.com/nextcloud/.github/blob/master/workflow-templates/psalm.yml) del
[repositorio de plantillas de nextcloud](https://github.com/nextcloud/.github).

Si se quieren admitir varias versiones del servidor de Nextcloud con una sola versión de la app, ver esta
[action algo más compleja](https://github.com/nextcloud/.github/blob/master/workflow-templates/psalm-matrix.yml).
Crea una matriz en la que la app se prueba contra `dev-master` (la última versión de `OCP` que se encuentra en la rama master
del servidor de Nextcloud), así como contra las demás ramas estables con soporte actual. Ajustarla según las necesidades.

[Psalm]: https://psalm.dev/docs/
````
