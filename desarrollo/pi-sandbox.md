---
tipo: referencia
audiencia: desarrollo
apps: [pi-sandbox]
resumen: "pi-sandbox: la aplicación desechable donde se prueban los agentes, sus tres defectos sembrados, su compuerta y lo que nunca se distribuye."
---
# pi-sandbox

## Resumen

pi-sandbox es un repositorio privado con una aplicación desechable, con la forma de una aplicación de servidor, donde se prueban los agentes de la organización: Jules, pi y Claude. Nada de lo que contiene se distribuye, y la lista de aplicaciones propias que instala gestion no lo incluye.

El repositorio nació con la llegada de pi (`@aps-pi`), el tercer agente: pi revisa antes que Claude cada pull request que no sea solo de documentación, responde a las menciones `@aps-pi`, propone cambios de esquema programados (🗃️ Schema) y participa en el consejo de diseño, y Claude confirma o rechaza cada hallazgo de pi. El diseño de pi exigía un repositorio de pruebas privado antes de instalarlo en los repositorios reales, y la verificación de extremo a extremo del 2026-10-03 corrió aquí. El funcionamiento de los agentes está en {doc}`agents`.

`schedule.md` del repositorio agents nombra también a epidemiologia, territorio, estadistica, farmacia y aps-common como destinos de pi, pero hoy solo este repositorio lleva la copia del workflow llamador: la verificación dejó abierta la restricción de las instalaciones de la aplicación `aps-pi`, que bloquea ese despliegue. El rol 🗃️ Schema también tiene a este repositorio entre sus destinos.

## Tabla

| Archivo | Contenido | Papel en las pruebas |
|---|---|---|
| `appinfo/info.xml` | Aplicación `pisandbox`, versión 0.1.0, compatible solo con Nextcloud 34. | repo-docs infiere de este archivo el arquetipo `nextcloud-app`. |
| `lib/Migration/Version000100Date20261003000000.php` | Crea la tabla `pisandbox_notes` (`id`, `paciente_id` de 12 caracteres, `texto`, `creada_en`) sin índice sobre `paciente_id`. | Defecto sembrado: la falta de índice solo se corrige con una migración, por eso corresponde a una incidencia del consejo de diseño. |
| `lib/Db/Note.php`, `lib/Db/NoteMapper.php` | Entidad y mapper; `findByPaciente` filtra por `paciente_id` y ordena por `creada_en` descendente. | En la verificación, el consejo de diseño terminó en un pull request de pi con un índice sobre esas dos columnas. |
| `lib/Service/NoteService.php` | `notesFor` llama a `find` una vez por cada identificador. | Defecto sembrado: un bucle N+1. |
| `src/notes.js` | `summarize` resume cada nota; `emptyLabel` devuelve el texto en inglés «No notes yet». | Defecto sembrado: un texto de interfaz en inglés, contra la regla de `AGENTS.md` que pide textos de interfaz en español. |
| `src/notes.test.js` | Una prueba de `node:test` para `summarize`. | Parte de la compuerta. |
| `.github/workflows/ci.yml` | Corre las pruebas de JavaScript y `php -l` sobre cada archivo PHP versionado. | La compuerta. |
| `.github/workflows/aps-pi.yml` | Copia administrada de `pi/caller.yml` del repositorio agents: filtra los eventos y llama al workflow reutilizable de pi. | pi marca una copia desactualizada con `caller_stale=1`, y el resumen diario la informa como deriva. |
| `AGENTS.md` | Reglas para agentes: la compuerta, los textos de interfaz en español como literales (sin `t()`), y la prohibición de editar `.github/workflows/`, `package.json` y los lockfiles. | La verificación comprobó que pi se niega a editar un workflow y entrega el cambio exacto para que lo aplique una persona. |
| `CONTEXT.md` | Vocabulario del dominio: la «Nota», una nota clínica sobre un paciente, y el «Paciente», identificado por `paciente_id`, sin tabla propia. | — |

La compuerta corre estos dos comandos en cada push a `main` y en cada pull request:

```bash
node --test src/*.test.js
git ls-files '*.php' | xargs -n1 php -l
```

## Notas

### Qué se verificó

La verificación del 2026-10-03 (`docs/verification-2026-10-03-pi.md` en el repositorio agents) recorrió en este repositorio estos escenarios, y todos se comportaron según el diseño:

- la revisión de pi antes de la de Claude, y el contraste de Claude sobre cada hallazgo;
- el rechazo de un hallazgo, una sola réplica de pi y la etiqueta `agents-disagree`;
- una mención `@aps-pi` que agrega una prueba con un commit propio;
- un pull request de Jules dentro del circuito;
- el consejo de diseño completo, que terminó en un pull request de pi con el índice sobre (`paciente_id`, `creada_en`);
- el despacho de 🗃️ Schema, que abrió un pull request para reemplazar el bucle N+1 por una sola consulta `IN`;
- la falla del modelo, la deriva del workflow llamador, la ausencia de bucles entre agentes y el tope diario de corridas.

La verificación encontró tres defectos en pi y en las rutinas, y los corrigió con pruebas primero en una rama del repositorio agents.

### Licencia y documentación

- El repositorio no tiene `LICENSE`, `README.md` ni `CHANGELOG.md`, y le faltan todos los archivos canon de {doc}`repo-docs`. `baseline.json` de repo-docs registra esos hallazgos como abiertos, y el barrido semanal solo falla con hallazgos nuevos.
- La guía de contribución de la organización declara AGPL-3.0-or-later todo lo que produce APS-Conecta y pide un `LICENSE` idéntico en cada repositorio; aquí la licencia no está escrita, y repo-docs anota que una licencia no se hereda del repositorio `.github`.

### Límites

- La compuerta comprueba la sintaxis PHP y una prueba de JavaScript, sin instalar la aplicación en un servidor. El diseño de pi lo asume: la integración continua sobre la rama empujada es la prueba, y pi no corre Docker ni PHPUnit.
- El vocabulario de prueba es clínico, con notas sobre pacientes identificados por su RUT, mientras la política de seguridad de la organización declara que sus sistemas no guardan datos de pacientes. La única nota que existe es el texto sintético de la prueba, y ninguna instalación crea la tabla.
- Las rutinas de Claude nombran a pi-sandbox como un repositorio temporal, «mientras exista».

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/pi-sandbox>
```
