---
tipo: explicacion
audiencia: desarrollo
apps: [aps-common]
resumen: "Las reglas de texto que comparten las aplicaciones propias (CSV, plegado, slugs, rechazo y error de cliente), cómo llegan a cada una y su cerco."
---
# aps-common

## Contexto

aps-common enuncia una sola vez las reglas de texto compartidas por las aplicaciones propias de APS Conecta: el dialecto CSV (`Csv`), la familia de plegado y slugs (`Text` y su mitad JS en `js/`), la postura de rechazo (`Refusal` y `Refuses`) y la única forma del error en el cliente (`js/api.js`).

El paquete existe porque, sin él, dos aplicaciones copiarían y adaptarían el mismo código hasta que las copias divergieran. Su doctrina es «idéntico byte a byte»: lo que trae se extrajo literal de las aplicaciones, los mismos bytes que ya corrían, no una reescritura inspirada en ellos, porque las copias que reemplaza ya habían empezado a divergir.

Es una biblioteca de Composer, no una aplicación: no tiene `appinfo`, rutas ni base de datos, y no depende de ninguna clase OCP salvo un trait deliberadamente ligado a OCP, que la batería de pruebas del propio paquete nunca carga. Su estado es estable, `composer.json` declara la versión 1.0.0 y la consumen las cuatro aplicaciones propias.

La licencia es AGPL-3.0-or-later ([ADR-0010 de gestion](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0010-agpl-across-the-org.md)): la obligación viene de lo que enlazan las aplicaciones, no de una elección del paquete. El paquete no tiene dependencias de ejecución más allá de PHP `^8.1`, así que no hay terceros que atribuir.

Una regla pertenece aquí cuando dos o más aplicaciones deben coincidir en su comportamiento y una divergencia rompe en silencio búsquedas o viajes de ida y vuelta: el dialecto CSV de es-CL, el plegado de acentos, los slugs, la neutralización de fórmulas y la forma del mensaje de error. Las formas propias de cada aplicación no se mueven: la exportación con pérdida de territorio y la planilla de ida y vuelta de farmacia son distintas a propósito.

## Diseño

### Las cuatro superficies

La superficie pública es el código fuente: `src/` para la mitad PHP y `js/` para la mitad JS. Las firmas no se repiten en la documentación, porque quedarían desactualizadas; el mapa de módulos se genera al compilar:

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/aps-common>
```

#### Dialecto CSV (`src/Csv.php`)

| Regla | Por qué |
| --- | --- |
| Las exportaciones llevan marca de orden de bytes (BOM). | Excel adivina UTF-8 en lugar de Latin-1. |
| Un archivo que no es UTF-8 válido se lee como Windows-1252. | Es lo que escribe Excel cuando nadie pide UTF-8. Es una regla, no una heurística: un archivo UTF-8 válido nunca se toca. |
| El separador es `;` o `,`, según cuál aparece más en la primera línea. | Excel en es-CL escribe `;`, porque la coma ya es el separador decimal. La primera línea son encabezados, así que una coma ahí es separador y no parte de una dirección. |
| Las filas se leen con un lector de flujo, sin carácter de escape. | Una celda de notas puede traer un salto de línea dentro de comillas, y el escape histórico de PHP se comería una barra invertida escrita en una dirección. |
| Una celda que empieza con `=`, `+`, `-`, `@`, tabulación o retorno de carro recibe un apóstrofo inicial. | La hoja de cálculo ejecutaría la celda como fórmula en el computador de quien abre la exportación, que suele ser otra persona. |

#### Plegado, slug, rechazo y forma del error

| Superficie | Archivo | Regla | Por qué |
| --- | --- | --- | --- |
| Plegado | `src/Text.php` (`fold()`), `js/filters.js` (`fold`) | Descompone, quita las marcas combinantes y pasa a minúsculas; la mitad PHP además colapsa los espacios repetidos y la JS no. | Una lista de siete letras españolas es una lista a la que le falta una; una búsqueda en el cliente conserva sus espacios internos. `js/fold-corpus.json` fija las mismas respuestas para ambas mitades. |
| Slug | `src/Text.php` (`slugFor()`) | El alfabeto del plegado; todo otro carácter es `_`; corte en 64 (`Text::SLUG_LENGTH`) y nuevo recorte después del corte. | 64 es el tope de las columnas `VARCHAR(64)` de los consumidores; el recorte evita que un nombre cortado a mitad de un separador produzca un slug que la misma etiqueta no produciría dos veces. |
| Rechazo | `src/Refusal.php`, `src/Refuses.php` | Un envío entendido y rechazado es un 422 cuyo mensaje dice qué corregir; un registro que nadie tiene es un 404. | Nunca un 200 silencioso ni un 500 que la persona frente a la pantalla no puede ver. |
| Forma del error | `js/api.js` | `messageFrom` devuelve la frase del servidor o un respaldo honesto, y siempre se puede esperar con `await`, incluso con un cuerpo `Blob`. `loggers` escribe una etiqueta estable, el mensaje de la excepción y el estado HTTP, nunca el objeto. | Un `AxiosError` serializa el cuerpo de la solicitud, y un guardado fallido no debe dejar datos clínicos en las herramientas de desarrollo del navegador. |

### Contrato de rechazo

El rechazo vive en dos archivos, con dos niveles de prueba. `Refusal` es una interfaz marcadora en PHP puro: toda familia `Invalid*Exception` de las aplicaciones la implementa, así que un solo `catch` las nombra a todas, y la batería del paquete la carga en milisegundos. Está en su propio archivo porque todo autocargador resuelve por nombre de archivo, y un marcador escondido en `Refuses.php` sería un 500 «Interface not found» que depende del orden de carga.

`Refuses` es el trait que mezclan los controladores de las aplicaciones. Depende de clases OCP (`JSONResponse`, `Http`, `DoesNotExistException`), por eso el paquete nunca lo carga y es la única excepción documentada a la regla de no depender de OCP. Su método `attempt()` traduce el resultado de la acción así:

| La acción | Estado HTTP | Cuerpo |
| --- | --- | --- |
| Devuelve un arreglo | 200 | El arreglo, como JSON |
| Lanza una excepción que implementa `Refusal` | 422 | `{"message": "<mensaje de la excepción>"}` |
| Lanza `DoesNotExistException` | 404 | `{"message": "no existe"}`, o el texto que pase el controlador |

Las respuestas JSON de un controlador están en {doc}`/desarrollo/plataforma/basics/controllers`.

### Distribución: el subárbol versionado

No hay publicación en Packagist (ADR-0001 del paquete). Cada aplicación declara un repositorio de Composer de tipo `path` que apunta al clon hermano, exige `aps/common` y versiona el subárbol `vendor/aps/common/src`; la mitad JS viaja versionada en `src/aps/`. `vendor/autoload.php` no se versiona: el `Application.php` de cada aplicación registra un autocargador PSR-4 pequeño para `APS\Common\`.

La razón es la forma de instalar: una aplicación se instala desde un tarball de versión construido con `git archive` del árbol versionado, así que todo lo que el tarball debe llevar tiene que estar versionado en el repositorio de la aplicación. Una publicación en Packagist haría depender cada instalación de un servicio y de una resolución de versiones que la organización no opera. El piso es PHP `^8.1`, porque territorio fija `config.platform.php` en 8.1 y un piso mayor haría el paquete imposible de instalar ahí.

Cada aplicación consumidora tiene dos objetivos de `make`: `aps-sync` copia el paquete (`src/` a `vendor/aps/common/src/`, el stub a `tests/stubs/` y `js/` a `src/aps/`) y `aps-drift` prueba que la copia versionada es igual al paquete. Son objetivos de los consumidores; el paquete no tiene ninguno de los dos. Tras cada fusión en aps-common, la rutina 🔗 Integrator abre una pull request `🔗 Adopt:` por aplicación que hace la resincronización ({doc}`/desarrollo/agents`).

### Consumidores y cerco

| Aplicación | Superficies que consume | Compuerta `aps-drift` en CI |
| --- | --- | --- |
| territorio | Las cuatro | Sí |
| farmacia | Las cuatro | Sí |
| estadistica | Las cuatro | Sí |
| epidemiologia | Solo la mitad JS (`src/aps/`) | No |

Ese es el radio de impacto de un cambio incompatible. El cerco es la compuerta roja misma: el paquete no puede moverse sin que cada consumidor se mueva con él, porque las compuertas `aps-drift` de territorio, farmacia y estadistica quedan en rojo hasta que cada una resincroniza y versiona la copia.

### Pruebas

La CI del paquete corre dos trabajos en cada pull request y en cada push a `main`. El primero ejecuta la batería PHP en un contenedor PHP sin Nextcloud, la misma forma que usan las aplicaciones; la imagen trae `intl`, sin la cual las pruebas de acentos pasarían sin correr:

```console
make test
```

El segundo ejecuta el corpus de conformidad del plegado, que también leen las baterías vitest de las aplicaciones:

```console
node --test js/*.test.js
```

## Compromisos y límites

- **Un hueco declarado en el cerco.** epidemiologia consume solo la mitad JS y no tiene compuerta de deriva; ADR-0001 lo registra como conocido y aceptado.
- **Sin versión en los consumidores.** Nada fija una versión en las copias de las aplicaciones: el cerco, no un número de versión, las mantiene alineadas.
- **Copia editable en una emergencia.** Una copia dentro de una aplicación se puede editar localmente; el siguiente `aps-sync` la sobrescribe y la compuerta de deriva lo informa. El subárbol es una proyección, no un fork.
- **Trait sin prueba en el paquete.** La batería del paquete fija solo la interfaz `Refusal`; el trait `Refuses` queda cubierto por las pruebas de controladores de las aplicaciones que verifican el cuerpo de un 422.
- **Adopción parcial del trait.** No todo controlador responde por `Refuses`: el `ApiController` de farmacia conserva su propio rechazo con envoltura, y algunos controladores conservan capturas por método donde estrechan la respuesta a propósito.
- **Dos separadores, sin olfateo.** La detección del separador considera solo `;` y `,`; un archivo separado por tabulaciones se lee como una sola columna y se rechaza por faltarle la columna de coincidencia.
- **El apóstrofo está en los bytes.** Excel y LibreOffice no muestran el apóstrofo de una celda neutralizada, pero un programa que lee el archivo sí lo ve. Un número de teléfono que empieza con `+56` también lo recibe: es el precio de no adivinar qué `+` inicial es aritmética.
