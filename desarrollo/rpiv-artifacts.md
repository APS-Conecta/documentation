---
tipo: referencia
audiencia: desarrollo
apps: [rpiv-artifacts]
resumen: "rpiv-artifacts: dónde quedan las investigaciones, diseños, planes, validaciones y traspasos de rpiv, y los planes de cada iniciativa."
---
# rpiv-artifacts

## Resumen

rpiv-artifacts es el repositorio privado donde la organización conserva los artefactos de sus corridas rpiv y los planes aprobados de sus iniciativas entre repositorios. El {doc}`aviso legal </aviso>` describe rpiv: corridas por etapas (investigación, diseño, plan, implementación y validación) en las que el plan espera aprobación antes de implementarse.

Cada artefacto es un archivo Markdown nombrado por la fecha y la hora en que se escribió y un tema, con la forma `AAAA-MM-DD_HH-MM-SS_<tema>.md`. Casi todos los artefactos abren con un front matter YAML: la fecha, el repositorio y el commit que describen, el tema, las etiquetas, el estado y, cuando corresponde, `parent`, que apunta al artefacto del que deriva. Así un diseño apunta a su investigación, un plan a su diseño o a la revisión de arquitectura que lo originó, y una validación a su plan.

El plan de una iniciativa es la fuente de registro de ese trabajo: la rutina 📚 Scribe, que mantiene este sitio, declara que implementa `initiatives/scribe.md`.

## Tabla

| Ruta | Contenido |
|---|---|
| `.rpiv/artifacts/research/` | Investigación previa a un diseño: el encargo, su nivel de definición y la identidad del objetivo medida en vivo. |
| `.rpiv/artifacts/designs/` | Diseños: resumen, requisitos, análisis del estado actual, alcance, decisiones, arquitectura y tramos. |
| `.rpiv/artifacts/plans/` | Planes de implementación: objetivo, arquitectura, stack, restricciones globales y tareas con casillas. |
| `.rpiv/artifacts/validation/` | Validaciones de un plan: estado de la implementación, resultados de la verificación automática, hallazgos de la revisión de código, pruebas manuales pendientes y el veredicto (`verdict`). |
| `.rpiv/artifacts/architecture-reviews/` | Revisiones de arquitectura de un repositorio o de toda la organización, divididas en fases con dependencias, radio de impacto y esfuerzo. |
| `.rpiv/artifacts/handoffs/` | Traspasos de sesión: las tareas y su estado, las referencias, los cambios recientes, lo aprendido y los pasos siguientes. |
| `initiatives/docs-es.md` | Plan de la iniciativa docs-es: este sitio en español, el catálogo como fuente única de los repositorios y los mecanismos que bloquean la deriva. |
| `initiatives/scribe.md` | Plan de la iniciativa scribe: los manuales de {vendor}`Nextcloud` tejidos en este sitio y la rutina 📚 Scribe que los mantiene. |
| `initiatives/scribe-tools/` | La maquinaria del tejido masivo y de las auditorías de omisión. Las reglas viven en las herramientas de este sitio; estos archivos solo las orquestan. |

Un plan de iniciativa nombra su ejecutor y lo que aprueba el responsable de la organización, y fija el estado final, el dueño de cada hecho, las corridas, la verificación y lo que se difiere.

## Notas

- `.gitignore` es una lista blanca: ignora todo (`/*`) y solo admite `.gitignore` y `.rpiv/`, sin `.rpiv/tmp/` ni `.rpiv/workflows/`. La lista existe porque el repositorio nació sobre un directorio de trabajo que guarda credenciales: nada entra a git si la lista no lo permite.
- `initiatives/` no figura en la lista blanca: un archivo nuevo ahí queda ignorado hasta que se agrega de forma explícita.
- El tejido masivo terminó el 2026-10-10 con la cobertura completa de los documentos de {vendor}`Nextcloud`; desde entonces el carril `upstream` de 📚 Scribe sigue cada cambio, y `initiatives/scribe-tools/` queda para las auditorías de omisión y como registro de cómo corrió el tejido.
- La cadena tiene huecos: los dos diseños apuntan con `parent` a investigaciones que este repositorio no guarda.
- Los enlaces relativos de un artefacto apuntan al repositorio donde se escribió, así que aquí no resuelven. {doc}`repo-docs` registra esos enlaces rotos, las rutas absolutas de host y los nombres personales de los artefactos como hallazgos abiertos en `baseline.json`, y el barrido semanal solo falla con hallazgos nuevos.
- El repositorio no tiene `README.md`, `LICENSE`, `CHANGELOG.md`, `AGENTS.md` ni `CONTEXT.md`, y le faltan los archivos canon de repo-docs; la línea base registra como abiertas las ausencias de `README.md`, `LICENSE`, `CHANGELOG.md` y de los archivos canon.
