---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Pautas para contribuir código: flujo de trabajo, etiquetas de issues y pull requests, principios de interfaz, estándares de código y cabeceras de licencia."
---
# Estilo de código y pautas generales

## Resumen

Esta página reúne las pautas generales para contribuir código: el flujo de trabajo con ramas, issues y pull requests, el significado de las etiquetas, los principios de interfaz de usuario, los estándares de código comunes y las cabeceras de licencia. Está dirigida a quienes contribuyen código.

````{upstream} developer_manual/getting_started/coding_standards/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

### General

- Lo ideal es comentar los planes en los [foros](https://help.nextcloud.com) para ver si otras personas quieren trabajar en ellos de forma conjunta.
- Usamos [GitHub](https://github.com/nextcloud); por favor, crear una cuenta allí y clonar los repositorios en los que se quiera trabajar.
- Las correcciones van directamente a la rama principal; aun así, hay que probarlas a fondo.
- Las funciones nuevas siempre se desarrollan en una rama y solo se fusionan con la rama principal cuando están completamente terminadas.
- El software debe funcionar. Solo incorporamos funciones a la rama principal cuando están completas.
  Es mejor no tener una función que tener una que funcione mal.
- Lo mejor es empezar a trabajar a partir de un issue; si no lo hay, crear uno.
  En él se describe lo que se quiere hacer, se pide opinión sobre el rumbo que se le da y se sigue a partir de ahí.
- Al terminar, usar la función de solicitud de fusión de GitHub para crear una pull request.
  Los demás desarrolladores la revisarán y darán su opinión. Para indicar que la PR está lista para revisión, se le puede añadir la etiqueta «3. to review».
  Consultar {nc-doc}`la página de revisión de código para obtener más información <developer_manual/prologue/bugtracker/codereviews>`
- Es fundamental mantener los cambios separados y pequeños. Cuanto más grande y enrevesada se vuelve una PR, más difícil es incorporarla.
  Así que, donde se pueda, dividir el trabajo en cambios más pequeños: si se necesita una pequeña mejora, como una adición a la API, para incorporar una función grande, ¡incorporarla primero en lugar de añadirla al gran bloque de trabajo!
- Las decisiones se toman por consenso. Nos esforzamos por tomar las mejores decisiones técnicas y, como nadie puede saberlo todo, colaboramos.
  Eso significa que un primer comentario negativo puede no ser la última palabra, y que una opinión positiva tampoco es luz verde inmediata. {vendor}`Nextcloud` está construido a partir de piezas modulares (apps) y los mantenedores tienen una gran influencia.
  En caso de desacuerdo, consultamos a otros colaboradores experimentados.

### Etiquetas

Asignamos etiquetas a los issues y a las pull requests para que sea fácil encontrarlos y para señalar lo que hay que hacer.
Algunas las asignan los desarrolladores; otras, QA, quienes clasifican los errores, la dirección del proyecto, los mantenedores, etc.
No se desea que los usuarios o quienes informan de errores asignen etiquetas por su cuenta, a menos que sean desarrolladores o colaboradores de {vendor}`Nextcloud`.

Las etiquetas más importantes y su significado:

- Etiquetas que muestran el estado del issue o de la PR, numeradas del 0 al 4:

  - `0. to triage`: el issue o la solicitud de función debe clasificarse y aprobarse para su desarrollo
  - `1. to develop`: listo para empezar a desarrollarlo
  - `2. developing`: desarrollo en curso
  - `3. to review`: listo para revisión
  - `4. to release`: PR revisada que espera el descongelamiento de una rama para fusionarse o que tiene trabajos de CI pendientes
  - `needs info`: este issue necesita más información de quien lo informó; ver {nc-doc}`developer_manual/prologue/bugtracker/triaging`.
    Esta etiqueta suele combinarse con `0. to triage` para señalar que un informe de error aún no está confirmado o que una solicitud de función no se ha aprobado.
  - `needs review`: este issue necesita una investigación más a fondo por parte del equipo de {vendor}`Nextcloud`; ver {nc-doc}`developer_manual/prologue/bugtracker/triaging`.

- Etiquetas que muestran el tipo de issue o de PR

  - `bug`: este issue es un error
  - `enhancement`: este issue es una solicitud de función o una idea para mejorar Nextcloud
  - `technical debt`: este issue o esta PR trata sobre [deuda técnica](https://en.wikipedia.org/wiki/Technical_debt)
  - `overview`: este issue es un resumen de un esfuerzo global y suele hacer referencia a otros issues

- Etiquetas que clasifican un issue o una PR

  - `high`, `medium` y `low`: indican la importancia del error.
  - `regression`: algo que funcionaba en una versión anterior pero que ahora no funciona como se espera o falta.
  - `feature: *`, p. ej., `feature: dav`: estas etiquetas agrupan los tickets de una función o de subsistemas concretos.
  - `design`: necesita ayuda del equipo de diseño o es un issue o una pull request relacionado con el diseño
  - `good first issue`: son issues relativamente fáciles de resolver e ideales para quienes quieren aprender a programar en Nextcloud

- `backport-request`: la pull request también debe aplicarse a versiones anteriores de Nextcloud. Esta etiqueta suele asignarla la automatización.

### Interfaz de usuario

- El software no debe estorbar. Hacer las cosas automáticamente en lugar de ofrecer opciones de configuración.
- El software debe ser fácil de usar. Mostrar solo los elementos más importantes. Los elementos secundarios, solo al pasar el cursor o mediante la función Avanzado.
- Los datos de los usuarios son sagrados. Ofrecer la posibilidad de deshacer en lugar de pedir confirmación, [que podría descartarse](http://www.alistapart.com/articles/neveruseawarning/)
- El estado de la aplicación debe ser claro. Si algo se está cargando, mostrar una indicación.
- No adoptar conceptos fallidos (por ejemplo, el diseño de las apps de escritorio) solo por coherencia. Aspiramos a ofrecer una interfaz mejor, así que ¡descubramos cómo hacerlo!
- Restablecer la instalación con regularidad para ver cómo es la experiencia de la primera ejecución. Y mejorarla.
- Lo ideal es hacer [pruebas de usabilidad](http://jancborchardt.net/usability-in-free-software) para saber cómo usa la gente el software.
- Para más principios de experiencia de usuario, leer a [Alex Faaborg, de Mozilla](http://uxmag.com/articles/quantifying-usability).

### Estándares de código

- Longitud máxima de línea de 80 caracteres
- Usar tabulaciones para sangrar
- Una tabulación tiene un ancho de 4 espacios
- Las llaves de apertura de los bloques van en la misma línea que la definición
- Comillas: ' para todo, " para los atributos HTML (\<p class="my_class">)
- Fin de línea: solo al estilo Unix (LF / '\n')
- Sin variables ni funciones globales
- El código debe probarse, idealmente con pruebas unitarias y de integración.
- Al hacer `git pull`, hacer siempre `git pull --rebase` para no generar commits adicionales como: *merged main into main*

La mayor parte de Nextcloud está escrita en PHP y Typescript / JavaScript, por lo que tenemos estándares de código más detallados para esos lenguajes:

- {nc-doc}`developer_manual/getting_started/coding_standards/php`
- {nc-doc}`developer_manual/getting_started/coding_standards/javascript`
- {nc-doc}`developer_manual/getting_started/coding_standards/html_css`

### Cabeceras de licencia

{vendor}`Nextcloud` se distribuye bajo la licencia [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl).
Desde el 16 de junio de 2016, cambiamos a «GNU Affero General Public License v3.0 or later» para facilitar el mantenimiento a largo plazo.

Si se crea un archivo nuevo, usar esta cabecera:

```php
/**
 * SPDX-FileCopyrightText: [year] [your name] [<your email address>]
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */
```

El año debe ser entonces el de creación, y la dirección de correo electrónico es opcional.

Si se edita un archivo existente, por favor, mantener la cabecera de licencia existente tal como está y solo añadir el propio aviso de copyright, si se considera que los cambios son lo bastante sustanciales como para reclamar el copyright.

Para ello hay dos opciones:

- Si ya hay una cabecera genérica, por favor, solo añadirse al archivo AUTHORS.md
- Si no hay una cabecera genérica, se puede añadir una línea de copyright propia como se describe arriba. Como regla general, este es el caso si se contribuyeron más de siete líneas de código.

Para un ejemplo de cabecera de licencia genérica en la que es preferible añadirse al archivo AUTHORS.md,
ver el ejemplo de abajo

```php
/**
 * SPDX-FileCopyrightText: 2024 Nextcloud GmbH and Nextcloud contributors
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */
```

La parte de Nextcloud GmbH solo se aplica a los empleados de la empresa, no a los colaboradores.

Para más información general sobre las cabeceras SPDX y su uso para cumplir con REUSE, consultar

- [REUSE](https://reuse.software/)
- [SPDX](https://spdx.dev/)
````

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
