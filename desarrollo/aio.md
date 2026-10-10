---
tipo: referencia
audiencia: desarrollo
apps: [AIO]
resumen: "El repositorio AIO: la rama espejo, la cola de parches, la cadena Replay y sus compuertas, la publicación de imágenes y sus límites."
---
# AIO

## Resumen

[APS-Conecta/AIO](https://github.com/APS-Conecta/AIO) es el fork de [nextcloud/all-in-one](https://github.com/nextcloud/all-in-one) desde el que se construyen las imágenes de cada instalación de la suite. Lo que los parches cambian en una instalación está en {doc}`/administracion/aio`; esta página describe cómo se mantiene el fork.

El fork sigue una regla única: todo cambio a un archivo que upstream distribuye viaja como un parche numerado. La rama `main` refleja upstream byte a byte, salvo las rutas propias del fork y el bloque de declaración de `readme.md`. La rama `aps/main` es la salida de la integración continua, la punta de upstream más la cola de parches, y de ella se construyen las imágenes. Un pull request que edita un archivo reflejado, en vez de agregar un parche, falla la paridad.

Las rutas propias del fork viven en `main` porque GitHub ejecuta los flujos programados, manuales y reutilizables solo desde la rama por defecto, y `aps/main`, reescrita por la integración continua en cada ejecución, no sirve como rama por defecto.

El fork conserva sin cambios el `LICENSE` de upstream (AGPL-3.0); su identificador SPDX está en la tabla de componentes del {doc}`/aviso`. La fuente correspondiente completa de cada imagen de la suite es este repositorio en la etiqueta de la suite: la historia de upstream en `main` más la cola de parches.

## Tabla

### Ramas y rutas

| Rama o ruta | Contenido | Quién la escribe |
|---|---|---|
| `main` | Espejo de upstream byte a byte, más las rutas propias del fork | La sincronización, con una fusión de `upstream/main` que nunca se fuerza; las rutas propias, por pull request |
| `aps/main` | Un solo commit de reproducción sobre la punta de upstream | El flujo Replay, con envío forzado |
| `patches/` | La cola: 29 parches `.patch` y 2 parches generados `.sh` | Pull request |
| `scripts/` | El motor (`replay.sh`), las compuertas (`brand-gate.sh`, `acquisition-gate.sh`), el registro de imágenes (`retag.sh`), el horneado (`bake.sh`), los generadores (`rename-containers.py`, `lockup.py`) y la línea base de deriva (`wizard-drift-baseline`) | Pull request |
| `.github/workflows/replay.yml`, `.github/workflows/images.yml` | La cadena Replay y la publicación de imágenes | Pull request |
| `.codespellrc` | La lista de 16 palabras correctas en español que codespell marcaría como errores | Pull request; el parche 060 lleva una copia idéntica |
| `BUGS.md` | El registro de fallas corregidas de las herramientas del fork | Pull request |
| `readme.md` | El único archivo de upstream modificado en `main`: la declaración del fork entre marcadores | Pull request; la paridad exige que, sin ese bloque, sea idéntico al de upstream |

### La cadena Replay

El orden de los pasos del flujo Replay es el orden de las compuertas: ningún paso posterior corre si uno anterior falla.

| Paso | Orden que ejecuta la integración continua | Qué prueba | Al fallar |
|---|---|---|---|
| Sincronizar el espejo | `bash scripts/replay.sh sync` | Fusiona `upstream/main` en `main`; no hace nada si upstream no se movió | Se detiene ante un conflicto; `main` nunca se fuerza |
| Paridad | `bash scripts/replay.sh parity` | Ningún archivo de upstream falta ni cambia en `main`, salvo la declaración, y todo lo que `main` agrega está en la lista de rutas propias | Rojo, con los archivos fuera de regla |
| Reproducir la cola | `bash scripts/replay.sh replay` | La regla de cobertura y la regla de los tres resultados, parche por parche, sobre un árbol de trabajo nuevo | Rojo, con el nombre del parche, antes de cualquier envío |
| Validadores de upstream | `bash scripts/replay.sh validate .aps-replay-tree` y `composer run lint:twig` | codespell, hadolint, json-spec y twig-lint sobre el árbol reproducido | Rojo: la publicación no corre |
| Compuerta de marca | `bash scripts/brand-gate.sh .aps-replay-tree` | La identidad de APS en cada superficie que la cola dice cambiar | Rojo, con la fila que falló |
| Compuerta de adquisición | `bash scripts/acquisition-gate.sh .aps-replay-tree` | La instalación no llega a ninguna fuente ajena a APS Conecta | Rojo, con la fila que falló |
| Informe de deriva | `bash scripts/replay.sh drift-report` | Las líneas que upstream agregó a los archivos traducidos desde la línea base fijada | Nunca falla: anota advertencias |

### Disparadores

| Evento | Qué hace |
|---|---|
| Programado, cada día a las 04:23 UTC | Sincroniza el espejo si upstream se movió, reproduce la cola y corre las compuertas |
| Envío a `main` | Una ruta propia cambió: regenera `aps/main` y vuelve a probar las compuertas |
| Pull request | Paridad, cobertura, tres resultados, validadores y compuertas sobre el commit de fusión, sin tocar `aps/main` (`REPLAY_PUSH=0`); además, la prueba de que las compuertas pueden fallar |
| Manual, con `suite-tag` | Reproduce, prueba y entrega al flujo Images con `build-ref` igual a `aps/main`; sin `suite-tag`, solo reproduce y prueba |

En todos los eventos salvo el programado, el trabajo de vida (`liveness`) falla si la última ejecución programada exitosa tiene más de 7 días.

## Notas

### La regla de los tres resultados

Cada ejecución reconstruye el árbol desde la punta de upstream más la cola, nunca desde `aps/main`: esa rama es salida de la integración continua, y reproducir sobre ella dejaría que los restos de una ejecución respondieran por la siguiente. Los parches se aplican en orden léxico de su prefijo de tres dígitos.

Para cada parche `.patch`:

1. Si se aplica hacia adelante, se aplica.
2. Si se aplica en reverso, upstream ya adoptó el cambio: la ejecución lo omite con una advertencia. Dos omisiones seguidas en ejecuciones programadas terminan en retirar el parche o en justificarlo de nuevo en su encabezado.
3. Si no se aplica en ningún sentido, upstream se movió: la ejecución se detiene, nombra el parche, y el parche se regenera.

La herramienta es `git apply`, sin contexto aproximado: un parche que solo se aplica con aproximación es un parche que se degrada. Los parches se generan con `git diff`, con los prefijos `a/` y `b/`. La regla es la del [ADR-0002 de gestion](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0002-app-patches.md), llevada al fork. El margen de deriva es de 6 semanas como máximo detrás de upstream.

Los parches `.sh` son el canal generado: el 010 llama a `scripts/retag.sh` para cambiar el registro en `php/containers.json`, y el 240, que corre al final, llama a `scripts/rename-containers.py` para renombrar los contenedores. Corren dentro del árbol reproducido con `APS_TOOLS_ROOT` apuntando a `main`, son idempotentes, y su propia verificación es el resultado: se corrige el generador, nunca el árbol.

### La regla de cobertura

Antes de mover nada, cada parche de la cola debe tener una fila `row <id>` en `scripts/brand-gate.sh` o en `scripts/acquisition-gate.sh`; si no, la reproducción se detiene. Un parche que cambia el árbol distribuido sin nada que lo mida queda sin auditar. Una fila se activa solo cuando su parche está en la cola, y una fila omitida se imprime a la vista.

En cada pull request, el trabajo que prueba las compuertas inyecta dos regresiones conocidas en un árbol reproducido, un centinela revertido del parche 060 y una referencia al registro de upstream en `php/containers.json`, y exige que la compuerta de marca salga con código 1 en cada una. Existe porque `BUGS.md` registra cuatro fallas que pasaron en verde (A-005, A-006, A-010, A-011): dos en la compuerta de marca, una en el horneado y una en el script que redacta el parche 090.

### Las compuertas

Los cuatro validadores de upstream corren sobre el árbol reproducido porque `aps/main` recibe envíos forzados de la integración continua y los flujos de upstream nunca se disparan sobre ella.

La compuerta de marca tiene filas para 22 parches: las referencias al registro (010 en `php/containers.json`, 080 en `php/src`), las superficies de otros proveedores de oficina (050), la aplicación `office` desactivada (100), los pares centinela del español de Chile (060), la identidad visual (070), con la igualdad de textos entre la declaración del `readme.md` y el árbol, el mecanismo del horneado (030), la suite Playwright traducida (090), las demás superficies del asistente (110 a 180), el reinicio del entorno de pruebas (237), la red y los certificados (233, 235, 238, 239) y los nombres de los contenedores (240).

La compuerta de adquisición tiene dos clases de verificación. Las incondicionales valen ya para el árbol de upstream: ningún `git clone` en los scripts que ejecutan los contenedores distribuidos, y el punto de entrada sigue respetando la marca `skip.update`. Las filas se activan con su parche: el par certificado de Euro-Office (015), la tienda apagada (020), el horneado (030), la autoactualización opcional (040), la ausencia de deSEC (051), la ausencia de contenedores comunitarios (190), la oficina única (200), las opciones que parten desactivadas (210) y el primer arranque silencioso (220, 230).

### Fusiones de upstream y regeneración

La sincronización fusiona `upstream/main` en `main`. Un conflicto la detiene: upstream tocó una ruta propia del fork o las historias divergieron, y se resuelve a mano, sin forzar nunca `main`. Una edición del lado de `main` viaja por pull request, cuyo trabajo de reproducción prueba la paridad.

Cuando varios parches dejan de aplicarse, `BUGS.md` (A-014) registra el método: una cadena de commits, uno por parche, construida sobre la última base verde, se rebasa sobre `upstream/main`, se resuelven los conflictos reales y cada parche se regenera como `git diff --binary` entre commits consecutivos de la cadena. `git apply --3way` no sirve aquí, porque las preimágenes de los parches son estados intermedios que nunca se confirmaron.

Al regenerar el parche 060, la línea base de los textos del asistente (`scripts/wizard-drift-baseline`) se vuelve a fijar en la punta de upstream, para que el informe de deriva mida desde el nuevo corte. Toda sustitución del script que redacta un parche verifica su número de apariciones (A-011).

### Pruebas fuera de la cadena

El parche 090 traduce la suite Playwright del asistente (`php/tests`) para que verifique el texto en español. Tres verificaciones quedan en inglés a propósito, como prueba de que la traducción nunca llegó al código PHP.

El flujo Clean boot de gestion instala la etiqueta publicada del fork que fija `scripts/aio-testbed.sh` de gestion, con la misma instalación silenciosa que corre un establecimiento, por dominio y por la IP del ejecutor.

### Publicación de imágenes

La publicación es una ejecución manual de Replay con `suite-tag`, que entrega al flujo Images con `build-ref` igual a `aps/main`. El trabajo de publicación necesita en verde el de reproducción: una reproducción o una compuerta en rojo nunca mueve imágenes.

Images copia 17 imágenes en el propio registro con `docker buildx imagetools create` y construye tres. Su matriz prueba que las 20 existen y que las 17 copiadas vienen de una misma instantánea de upstream; una prueba de arranque confirma que el asistente publicado se descarga y arranca. Las tres construcciones deben resolver el mismo commit de `build-ref`, y los resúmenes de una etiqueta publicada no cambian nunca.

El horneado (`scripts/bake.sh`) corre en el ejecutor de Images, nunca en la imagen. Lee gestion en la referencia `gestion-ref` y, antes de que un byte entre en la construcción, vuelve a correr la verificación sha256 de `VENDOR` de gestion, exige que la versión del `info.xml` de cada tarball coincida con su pin, aplica los parches de marca blanca de eurooffice con la regla de los tres resultados y retira `signature.json` de las aplicaciones parchadas.

El envío forzado a `aps/main` usa un token personal: desde el parche 090 la cola modifica `.github/workflows/`, y el `GITHUB_TOKEN` no puede enviar archivos de flujos. El token llega por `GIT_ASKPASS`, nunca en una URL ni en los argumentos de un proceso.

### Contribuir

El `AGENTS.md` del repositorio es el de upstream, copiado byte a byte por la paridad. Prohíbe que un agente abra issues o pull requests por su cuenta, porque toda contribución la revisa y la envía una persona; exige el trailer `Assisted-by` en cada commit asistido y reserva el `Signed-off-by` a la persona. Los mensajes de commit siguen Conventional Commits, con el componente como ámbito.

Una falla de las herramientas del fork, ya corregida, se registra como una fila de `BUGS.md`: el razonamiento va en un comentario junto al código, y la compuerta que impide que vuelva, en `scripts/brand-gate.sh`, `scripts/acquisition-gate.sh` o `scripts/replay.sh`. Los problemas abiertos viven en el gestor de issues; {doc}`/proyecto/errores-conocidos` reúne los de la suite.

### Deuda técnica y límites

- **Fallas sin aviso.** Desde el 25 de septiembre de 2026, cada reproducción falló durante 8 días sin que nadie lo viera, y las imágenes publicadas dejaron de seguir a upstream (A-013). El trabajo de vida falla solo después de 7 días sin una ejecución programada exitosa, y solo en el siguiente envío o pull request.
- **Programación manual.** GitHub desactiva por defecto las programaciones de un fork: la ejecución diaria de Replay se activa una vez en la pestaña Actions. Los flujos programados de upstream se esperan desactivados.
- **Deriva sin compuerta.** Un texto nuevo en inglés que upstream agrega a un archivo traducido pasa todos los centinelas; el informe de deriva lo anota, nunca falla, y una persona lo revisa a ojo.
- **Higiene manual.** El conteo de omisiones seguidas de un parche es un conteo a ojo de las anotaciones diarias, sin registro entre ejecuciones.
- **Límites de la instalación.** Los que ve un establecimiento, como los mensajes PHP en inglés o el código muerto de deSEC, están en {doc}`/administracion/aio`.

El mapa de módulos del repositorio se extrae con graphify en cada compilación:

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/aio>
```
