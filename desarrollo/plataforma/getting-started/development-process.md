---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo se desarrolla el código: control de versiones con git, nombres de ramas, ramas de destino de las contribuciones y backports de correcciones."
---
# Proceso de desarrollo

## Resumen

Esta página explica cómo se desarrolla el código de la plataforma: el control de versiones con git y sus ramas, la rama a la que van las contribuciones y cuándo y cómo se hace el backport de una corrección a versiones anteriores. Está dirigida a quienes contribuyen código.

````{upstream} developer_manual/getting_started/development_process.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Esta página ofrece una visión general de cómo se desarrolla el código de Nextcloud.

### Control de versiones del código fuente

{vendor}`Nextcloud` usa [git](https://git-scm.com/) para gestionar las revisiones del código. Los componentes de software tienen sus propios repositorios.

#### Nombres de ramas

Las ramas predeterminadas de Nextcloud y de los repositorios de sus apps se llaman `main` o `master`. Además, hay *ramas estables* cada vez que se publica una versión mayor de Nextcloud. Estas se llaman `stableX`, donde X se refiere a la versión. Para Nextcloud 25, por ejemplo, la rama estable se llama `stable25`.

### Ramas de destino de las contribuciones

Todo cambio que se hace en el código fuente entra en la rama predeterminada de un repositorio mediante una [pull request](https://docs.github.com/en/pull-requests).

```bash
# Switch to the default branch and update it
git checkout main
git pull origin main

# Create the new feature branch
git checkout -b feature/foo-bar

# Add and commit the changes
git add file1 file2
git commit --signoff -m 'Add foo bar'

# Push the new commit to the remote repository and open a pull request
git push origin feature/foo-bar
```

#### Correcciones de errores

Si una contribución corrige un error que también afecta a versiones anteriores de Nextcloud o de una app, puede optar a un *backport*. Hacer el backport de una corrección significa aplicar el cambio en una versión anterior del código. Git llama a esta operación *cherry picking*.

Siempre que se corrige un error crítico (es decir, una vulnerabilidad de seguridad), se hace su backport a todas las versiones mayores aplicables y, una vez fusionado, se publica en la siguiente tanda de versiones de mantenimiento de todas las versiones mayores que siguen soportadas (p. ej., 28.0.3 -> 28.0.4).

##### Consideraciones sobre los backports

Las versiones mayores que ya se publicaron no necesitan forzosamente todas las correcciones de errores. Decidir de qué hacer backport no es obvio. Implica cierto grado de criterio.

Algunas cosas que conviene tener en cuenta:

- Toda versión mayor que no haya llegado al final de su vida útil suele recibir estas correcciones con backport.
- Hacer el backport incluso de los cambios más simples conlleva cierto nivel de riesgo.
- Las diferencias entre ramas estables (incluidas las de las apps incluidas y de terceros) implican que hay variables adicionales fuera de la rama principal (o incluso respecto de la última estable).
- Las correcciones a menudo no llevan mucho tiempo en uso real (< 4 semanas, y es posible que nadie aparte del desarrollador original haya interactuado directamente con el código nuevo).

Factores bloqueantes (nunca hacer el backport de cosas que los causen):

- Cambios de API [los asuntos relacionados con la seguridad se tratarán caso por caso, ya que tienen una prioridad única]

Al evaluar si un error es lo bastante crítico para hacer su backport, estas son algunas preguntas posibles que hacerse:

- ¿Es realmente una corrección de un error? ¿O se trata más bien de una mejora funcional o de una mejora general?
- ¿Es siquiera aplicable a una línea de versiones mayores publicada anteriormente?
- ¿Sigue soportada esa línea de versiones mayores?
- ¿Es una vulnerabilidad de seguridad? [Sí: hacer el backport sin dudarlo.]
- ¿Hasta qué punto puede probarse el cambio?
- ¿Cuánta confianza hay en la corrección?
- ¿Es probable que el error afecte a muchos usuarios o entornos?
- ¿Existe *alguna* probabilidad de que este cambio introduzca sin querer una pérdida de datos?
- ¿Existe *alguna* probabilidad de que este cambio introduzca sin querer un problema de seguridad?
- ¿Hasta qué punto es «peliagudo» el cambio en general?
- ¿Hay disposición a dar soporte al backport si el cambio rompe algo inesperado en una versión anterior?
- ¿Puede hacerse el backport del cambio tal cual o requerirá una reelaboración significativa?
- ¿Está causando el error muchas solicitudes de soporte o informes de errores?
- ¿Tiene la incidencia principal de seguimiento muchos votos positivos, suscriptores o comentarios?
- ¿Es posible adoptar una actitud de «esperar y ver» respecto del backport (es decir, seguir probando la corrección en la rama main/master, esperar un ciclo de mantenimiento para volver a evaluarla y solo hacer el backport si nuevos datos de uso real sugieren que es lo bastante importante y/o de riesgo lo bastante bajo para hacerlo)?

Aplicar el mejor criterio posible.

Si procede, mencionar cualquier preocupación importante en la PR del backport para que los demás revisores del código puedan tenerla en cuenta.

Idealmente, al lanzar o solicitar un backport, explicar también *por qué* es necesario (si no es obvio). Esto ayuda aún más a los revisores.

En resumen: hacer el backport de correcciones de errores a versiones anteriores del código puede tener efectos secundarios no deseados. No toda corrección necesita un backport. Actuar con precaución.

##### Backport automático

En muchos casos, el cherry pick aplica el parche limpiamente y git puede resolver cualquier conflicto menor. En esos casos, lo más fácil es dejar que el [bot de backports](https://github.com/nextcloud/backportbot) haga el backport.

Consultar el [uso del bot](https://github.com/nextcloud/backportbot#usage) para conocer sus comandos.

##### Backport manual

Los cambios más complejos pueden requerir que el desarrollador haga el backport manualmente. Puede hacerse de la siguiente manera:

```bash
# Switch to the target branch and update it
git checkout stable25
git pull origin stable25

# Create the new backport branch
git checkout -b fix/foo-stable25

# Cherry pick the change from the commit sha1 of the change against the default branch
# This might cause conflicts. Resolve them.
git cherry-pick abc123

# Push the cherry pick commit to the remote repository and open a pull request
git push origin fix/foo-stable25
```
````
