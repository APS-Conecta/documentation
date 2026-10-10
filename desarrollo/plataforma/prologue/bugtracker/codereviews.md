---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Revisiones de código en GitHub: ningún cambio sin revisar, cómo avanza una pull request y las dos aprobaciones necesarias antes de fusionarla."
---
(nc-dev-code-reviews)=
# Revisiones de código en GitHub

## Resumen

Esta página explica la política de revisiones de código en GitHub: que ningún cambio entra sin revisión, cómo avanza una pull request hasta su fusión y dónde ver ejemplos y hacer preguntas. Está dirigida a quienes desarrollan sobre la plataforma.

````{upstream} developer_manual/prologue/bugtracker/codereviews.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
> Con suficientes ojos, todos los errores son superficiales
>
> — Ley de Linus

### Introducción

Para aumentar la calidad del código de Nextcloud, se pide a quienes desarrollan que hagan revisiones de código. Como ahora usamos intensamente la plataforma GitHub, estas revisiones de código también deben hacerse en GitHub.

### Condición previa

A partir de ahora, en general, no se permiten commits ni pushes directos a la rama main ni a ninguna de las ramas estables. **Todo cambio de código**, **incluso los de una sola línea**, ¡tiene que revisarse!

### ¿Cómo funcionará?

1. Quien desarrolla envía sus cambios a GitHub mediante una pull request (PR). [Ayuda de GitHub: usar pull requests](https://help.GitHub.com/articles/using-pull-requests)
2. En la propia pull request, quien desarrolla ya puede mencionar a otros desarrolladores (con @GitHubusername) y pedirles que la revisen.
3. En la sección Labels, a la derecha, añade la etiqueta *«3 - To review»* si el parche está completo. Si no tiene permiso para hacerlo, otros desarrolladores pueden añadir esta etiqueta si el autor de la PR así lo ha indicado.
4. Otros desarrolladores (mencionados o por iniciativa propia) revisan los cambios y quedan invitados a escribir comentarios en el campo de comentarios.
5. Si quien revisa está conforme con los cambios y considera que se han tenido en cuenta todos sus comentarios y sugerencias, un :+1 en el comentario indica una revisión positiva.
6. Antes de fusionar una pull request en la rama estable principal correspondiente, al menos 2 revisores tienen que dar una puntuación de :+1.
7. Nuestro servidor de integración continua da un indicador adicional de la calidad de la pull request (los resultados se pueden consultar desde la interfaz de GitHub de esa pull request).

### Ejemplos

Leer nuestra documentación sobre {nc-doc}`developer_manual/getting_started/coding_standards/index` para saber cómo son una buena pull request y un buen código de Nextcloud.

Estos son dos ejemplos que se consideran buenos ejemplos de cómo deben gestionarse las pull requests:

- <https://github.com/owncloud/core/pull/121>
- <https://github.com/owncloud/core/pull/146>

### ¿Preguntas?

No dudar en dejar un mensaje en los *foros*.

[forums]: https://help.nextcloud.com/
````
