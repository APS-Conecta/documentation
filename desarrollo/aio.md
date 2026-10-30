---
tipo: referencia
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo se mantiene el fork de nextcloud/all-in-one, hoy en instalador: un solo árbol, la declaración, las compuertas y la fusión de upstream."
---
# AIO

## Resumen

```{note}
Los cambios del plan de actualización corresponden a la próxima versión. Consulte su estado en {doc}`/proyecto/novedades/instalador` y seleccione una versión publicada para instalar.
```


El fork de [nextcloud/all-in-one](https://github.com/nextcloud/all-in-one) desde el que se construyen las imágenes de cada instalación de la suite vive en el repositorio [APS-Conecta/gestion](https://github.com/APS-Conecta/gestion), que absorbió también el paquete del host y la cadena de publicación: el repositorio APS-Conecta/AIO fue su primera casa y se eliminó una vez absorbido; su historia de commits sigue completa en instalador. Lo que los cambios del fork hacen en una instalación está en {doc}`/administracion/aio`; esta página describe cómo se mantiene el fork, y el repositorio que hoy lo contiene —bootstrap firmado, `VERSION` y cadena de publicación— tiene su propia referencia en {doc}`instalador </desarrollo/instalador>`.

El fork sigue una regla única: `main` es **un solo árbol** —la historia de upstream más los cambios del fork como bytes confirmados, de primera clase—. Los cambios no viajan como archivos aparte ni por ramas de integración: cada cambio es un commit del propio árbol, y una versión de upstream llega como llega cualquier cambio, con una fusión deliberada en `main`, y después una versión corriente. Los números que la [declaración del fork](https://github.com/APS-Conecta/gestion/blob/main/readme.md) asigna a cada cambio son atribución —qué cambio debe qué garantía—, no archivos aparte.

`main` nunca recibe envíos forzados: es de solo anexo y un retroceso es un revert. Cambiar un archivo que upstream distribuye es editar el archivo, con la declaración y las compuertas sosteniendo cada garantía.

El fork conserva sin cambios el `LICENSE` de upstream (AGPL-3.0); su identificador SPDX está en la tabla de componentes del {doc}`/aviso`. La fuente correspondiente completa de cada imagen de la suite es el repositorio instalador en la etiqueta de la suite: el árbol de la etiqueta es toda ella.

## Tabla

### El árbol y sus piezas

| Ruta | Contenido | Quién la escribe |
|---|---|---|
| `main` | La historia de upstream más los cambios del fork como bytes confirmados | La fusión deliberada de upstream, y los cambios propios por pull request |
| `readme.md` | La declaración del fork, entre marcadores: cada cambio con su número, su texto y la garantía que sostiene | Pull request; la compuerta de marca exige que cada texto declarado exista byte a byte en el árbol |
| `php/` | El asistente —el contenedor maestro— tal como se construye, con su suite Playwright traducida | Pull request |
| `Containers/`, `themes/` | Las cuatro imágenes construidas y el tema del servidor | Pull request |
| `scripts/` | Las compuertas (`brand-gate.sh`, `acquisition-gate.sh`), los validadores de upstream (`validate.sh`), el registro (`retag.sh`) y los renombrados (`rename-containers.py`) | Pull request |
| `.github/workflows/` | `ci.yml`, `images.yml`, `release.yml`, `cleanboot.yml` y los validadores de upstream | Pull request |
| `BUGS.md` | El registro de fallas corregidas de las herramientas del fork | Pull request |


### Las compuertas

| Compuerta | Qué prueba | Al fallar |
|---|---|---|
| Marca (`scripts/brand-gate.sh`) | La identidad y el español de Chile en cada superficie que la declaración nombra, fila por fila | Rojo, con la fila que falló |
| Adquisición (`scripts/acquisition-gate.sh`) | Que la instalación no llega a ninguna fuente ajena a APS Conecta, y que la tienda de aplicaciones abre solo por sus comandos acotados | Rojo, con la fila que falló |
| Enrojecimiento (`gate-red-proof`, en `ci.yml`) | Que las compuertas pueden fallar: regresiones conocidas inyectadas en el árbol del pull request deben ponerlas en rojo | Rojo: una compuerta que no puede fallar no prueba nada |
| Validadores de upstream (`scripts/validate.sh`) | codespell, docker-lint y json-spec, los mismos de upstream, sobre el árbol | Rojo: la publicación no corre |

Las filas de las compuertas se nombran por número —010 a 270— como atribución: qué cambio debe qué garantía. Nunca son una condición: toda fila corre en cada envío, en cada pull request y en cada publicación, y una fila nueva llega con el cambio que sostiene.

## Notas

### La fusión de upstream

Una versión de upstream llega como una fusión deliberada en `main`, resuelta a mano cuando hace falta, nunca un envío forzado. La fusión puede reintroducir identificadores de upstream; las herramientas de reemplazo del momento de fusionar los devuelven: `scripts/retag.sh sed` repone las referencias al registro propio y `scripts/rename-containers.py`, los nombres de contenedor de la suite. Después, una versión corriente publica el conjunto (`aps/RELEASING.md`).

Nada fusiona upstream ni publica imágenes por su cuenta: las programaciones del repositorio son de prueba, y esa disciplina la prueba cada versión con sus propias compuertas, antes de construir o firmar nada.

### La suite Playwright del asistente

La suite Playwright del asistente (`php/tests`) está traducida y verifica el texto en español. Tres verificaciones quedan en inglés a propósito, como prueba de que la traducción nunca llegó al código PHP: los mensajes que nacen en PHP siguen en inglés, y la declaración del fork lleva la lista completa, por archivo.

### Contribuir

El `AGENTS.md` del repositorio lleva las reglas del fork: commits convencionales con el ámbito `instalador`, el tráiler `Assisted-by` en cada commit asistido, y los textos del asistente solo con la declaración leída —una redacción que se mueve sin mover su fila enrojece la compuerta—. Una falla de las herramientas del fork, ya corregida, se registra como una fila de `BUGS.md`: el razonamiento junto al código y la compuerta que impide que vuelva, en `scripts/brand-gate.sh` o `scripts/acquisition-gate.sh`. Los problemas abiertos viven en el gestor de issues; {doc}`/proyecto/errores-conocidos` reúne los de la suite.

### Deuda técnica y límites

- **La fusión es manual y deliberada.** Nadie automatiza la llegada de upstream: si publica una corrección, la organización decide la fusión y la versión que la lleva.
- **Textos nuevos de upstream.** Una fusión que agrega textos del asistente en inglés los deja en inglés: la compuerta exige los declarados, no traduce los nuevos; la lista de mensajes en inglés de la declaración crece con ellos.
- **Límites de la instalación.** Los que ve un establecimiento, como los mensajes PHP en inglés, están en {doc}`AIO </administracion/aio>`.
