---
tipo: referencia
audiencia: desarrollo
apps: []
resumen: "Las doce reglas de código de la organización: la fuente única que cita la revisión de estándares de cada pull request."
---
# Estándares de código

## Resumen

Esta página reúne las reglas de código de todos los repositorios de la organización. Es la única fuente que cita el eje de estándares de la revisión de un pull request: un hallazgo de ese eje nombra una regla de esta tabla. El `AGENTS.md` de cada repositorio enlaza esta página y nombra sus costuras de prueba, es decir, dónde vive cada prueba. Las compuertas que corre cada repositorio antes de fusionar están en {doc}`/desarrollo/calidad`.

## Tabla

| N.º | Regla |
|---|---|
| 1 | Inglés para el código, los identificadores, los comentarios, las pruebas, los commits y los pull requests; español para lo que el producto muestra a una persona; los términos del glosario conservan su grafía. |
| 2 | KISS: el cambio más pequeño que corrige la causa raíz. |
| 3 | YAGNI: ninguna capa, opción ni abstracción que la incidencia no necesite. |
| 4 | DRY: una regla se escribe una sola vez; se reutiliza la función auxiliar existente, nunca una copia paralela. |
| 5 | SOLID: un solo motivo de cambio por módulo; se depende de las interfaces que ofrece {vendor}`Nextcloud`. |
| 6 | Los nombres dicen lo que una cosa hace o contiene, con las palabras del glosario. |
| 7 | Primero la prueba, en la costura de prueba acordada del repositorio: se afirma el comportamiento, no los detalles internos; los valores esperados vienen de una fuente independiente; la corrección de un error empieza con una prueba que lo reproduce. |
| 8 | Solo componentes `Nc*` y variables del tema. |
| 9 | Ni secretos ni texto de documentos en los registros. |
| 10 | Los archivos generados (archivos de bloqueo, especificaciones OpenAPI) nunca se editan a mano. |
| 11 | La documentación cambia en el mismo pull request, sin lápidas ni notas de historia. |
| 12 | Los rojos de CI se corrigen; nunca se omiten ni se eximen. |

## Notas

El reparto entre español e inglés de la regla 1 es el de la sección «Idioma y registro» de {doc}`/desarrollo/documentation`. Los identificadores y los ejemplos de código quedan en inglés, y el texto que lee una persona, en español:

```js
import { t } from '@nextcloud/l10n'

// The label a person reads is Spanish; the code around it is English.
const submitLabel = t('farmacia', 'Guardar')
```

Una lápida es el aviso que deja en un documento algo que se quitó; la regla 11 la descarta, y el cambio queda en el historial de commits y en el registro de cambios.
