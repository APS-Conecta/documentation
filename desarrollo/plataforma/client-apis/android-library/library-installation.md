---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo obtener la biblioteca android-library para Android y añadirla a un proyecto, como dependencia de Gradle o como submódulo de Git."
---
# Instalación de la biblioteca

## Resumen

Esta página explica, para quienes desarrollan apps de Android, cómo obtener la biblioteca de Android de {vendor}`Nextcloud` y cómo añadirla a un proyecto: como dependencia de Gradle mediante JitPack o como submódulo de Git.

````{upstream} developer_manual/client_apis/android_library/library_installation.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

### Obtener la biblioteca

La biblioteca de Android de {vendor}`Nextcloud` se puede obtener del siguiente repositorio de GitHub:

<https://github.com/nextcloud/android-library>

Una vez obtenido, este código debe compilarse. El repositorio de GitHub no solo contiene la biblioteca, sino también un proyecto de ejemplo, *sample_client*, que ayudará a aprender a usar la biblioteca.

### Añadir la biblioteca a un proyecto

Hay distintos métodos para añadir una biblioteca externa a un proyecto; aquí se describen dos.

1. Añadir la biblioteca como dependencia de Gradle mediante JitPack
2. Añadir el repositorio de la biblioteca al propio proyecto de Android como submódulo de Git

#### Añadir la biblioteca como dependencia de Gradle

Basta con abrir el archivo propio:

```
build.gradle
```

y añadir la dependencia:

```
compile 'com.github.nextcloud:android-library:<version>'
```

\<version> se refiere a la versión exacta que se quiere incluir en la aplicación. Puede ser -SNAPSHOT para usar siempre la última revisión del código de la rama master. Como alternativa, también se puede especificar un número de versión que remite a una versión publicada fija, p. ej., 1.0.0. (compile 'com.github.nextcloud:android-library:1.0.0').

#### Añadir el proyecto de la biblioteca al propio proyecto como submódulo de Git

Básicamente, se trata de obtener el código y compilarlo, integrándolo mediante un submódulo de Git.

En la línea de comandos, entrar en el directorio de la propia app y añadir la biblioteca de Android de {vendor}`Nextcloud` como submódulo:

```
git submodule add https://github.com/nextcloud/android-library nextcloud-android-library
```

Importar o abrir la propia app en Android Studio, y listo. Todas las clases y los métodos públicos de la biblioteca estarán disponibles para la propia app.
````
