---
tipo: explicacion
audiencia: desarrollo
apps: [agents]
resumen: "Los prompts de los agentes Jules, de pi y de las rutinas de Claude: una nómina, un ensamblado versionado por hash y la rotación semanal."
---
# agents

## Contexto

`agents` es el repositorio privado que reúne en un solo lugar los prompts de los agentes Jules programados y de las rutinas de Claude de la organización.

El reparto de autoridad es fijo: Jules hace los cambios, Claude los revisa y el responsable del proyecto decide cada fusión. Claude nunca fusiona, cierra ni aprueba por iniciativa propia.

pi, un agente basado en GLM que publica como `aps-pi[bot]`, es el tercer agente: segundo revisor, ejecutor de los pedidos que lo mencionan como `@aps-pi`, autor programado de 🗃️ Schema y miembro del consejo de diseño. Claude adjudica: pi revisa primero, Claude confirma o rechaza cada hallazgo de pi y es el único agente que escribe `@jules`.

El objetivo de diseño es fusionar más correcciones reales por semana, con la seguridad primero, bajo una restricción explícita: la atención del responsable, del orden de tres pull requests al día entre los repositorios piloto. De ahí la regla que atraviesa todos los prompts: es preferible no abrir ninguna pull request a abrir una débil, y todo cambio trae evidencia que el revisor puede comprobar.

## Diseño

### Una fuente por pieza

| Ruta | Contenido |
| --- | --- |
| `standards.md`, `preamble.md` | Las normas de código y el contrato común de todo agente Jules; `{standards}` se completa al ensamblar. |
| `agents/<nombre>.md` | Una persona por archivo; su encabezado dice cuándo y dónde corre. |
| `roster.json` | La nómina: identidades, prefijos de título, etiquetas, marcadores ocultos, límites y el ciclo del miércoles. Entra como `{roster}` en cada prompt, y el ejecutor de pi la lee. |
| `checklist.md`, `claude-verdict.md` | Las comprobaciones que aplica todo revisor y la forma del veredicto de Claude. |
| `routines/` | Los prompts de las rutinas de Claude. |
| `pi/` | Los prompts de pi por situación, su ejecutor (`pi/runner/`, Node 22, sin dependencias), `pi-version` y `caller.yml`, el flujo que cada repositorio con pi copia byte a byte. |
| `.github/` | El flujo reutilizable `aps-pi`, sus dos acciones compuestas y la CI del propio repositorio. |
| `schedule.md` | La rotación y el hash del prompt vigente en cada programación de Jules y en cada rutina. |
| `dist/` | Los prompts ensamblados, que se copian en Jules y en las rutinas. |

### Ensamblado y versión de cada prompt

`tools/build.py` ensambla cada prompt: sustituye los marcadores de posición (`{standards}`, `{roster}`, `{checklist}`, `{verdict}` y los demás) y estampa la versión, los primeros 12 caracteres hexadecimales del SHA-256 del prompt calculado con `{prompt_version}` todavía en el texto. Los marcadores ocultos que escriben los agentes, salvo `pi-failed`, llevan ese hash en `v=`, así que pi detecta un prompt de rutina obsoleto y el resumen diario lo informa.

El modo de comprobación valida sin escribir y termina con código 1 listando cada problema. Entre otras reglas, exige en cada persona las secciones `## Mission`, `## What to look for`, `## Proof`, `## Never` y `## Pull request` y, en las personas de Jules, un prompt ensamblado de 27 000 caracteres como máximo: el editor de Jules aceptó 30 000 en la verificación, menos un margen del 10 %. pi lee su prompt desde un archivo y queda fuera de ese límite.

La CI del repositorio corre en cada pull request y en cada push a `main`, además de `actionlint` y `zizmor` sobre los flujos:

```console
python3 -m unittest discover -s tests
python3 tools/build.py --check
node --test pi/runner/*.test.mjs
```

### Ciclo de un cambio de prompt

1. El cambio entra por pull request.
2. Tras la fusión, `tools/build.py` regenera `dist/` e imprime el hash de cada prompt.
3. Cada `dist/*.prompt.md` cambiado se pega en sus programaciones de Jules, que solo se editan en la interfaz web, o en su rutina.
4. `schedule.md` registra el hash y la fecha en sus tablas «Synced to Jules» o «Synced to routines».

pi no pasa por el paso manual: corre desde la rama `main` de este repositorio, así que fusionar un cambio en `pi/`, `roster.json`, `checklist.md` o las acciones cambia pi en todos los repositorios a la vez.

### Rotación nocturna de Jules

Las ejecuciones de Jules empiezan a las 02:00 (America/Santiago), con un solo agente de Jules por repositorio y por noche. «Las cuatro aplicaciones» son epidemiologia, territorio, estadistica y farmacia.

| Noche | Persona | Misión | Repositorios |
| --- | --- | --- | --- |
| Lunes | 🗡️ Breaker | Elige una clase de ataque de su rotación y la prueba contra el código real con un test; si el ataque entra, publica la corrección mínima y conserva el test. | Las cuatro aplicaciones y gestion |
| Martes | 🐞 Tracer | Encuentra un defecto que una persona o un cliente de la API puede alcanzar, lo reproduce con un test que falla y aplica la corrección mínima. Sin reproducción no hay pull request. | Las cuatro aplicaciones |
| Miércoles | ⚡ Bolt, ✂️ Simplifier o 🗃️ Schema | Una aceleración medible en código que corre a menudo sobre datos que crecen; una unidad difícil de leer, más simple y con el mismo comportamiento; o una corrección de cómo la aplicación guarda o lee sus datos, a cargo de pi. | Las cuatro aplicaciones |
| Jueves | 🧹 Janitor | Elimina un conjunto coherente de código muerto. | Las cuatro aplicaciones |
| Viernes | 🎨 Palette | Hace una pantalla más fácil de usar o más accesible, con los componentes del propio repositorio. | Las cuatro aplicaciones |
| Sábado | — | Sin agente de Jules: 📚 Scribe pasó a ser una rutina de Claude el 2026-10-09. | — |
| Domingo | 🔤 Lexicon | Alinea un término del código, de la interfaz y de la documentación con la definición de `CONTEXT.md`. | Las cuatro aplicaciones |

El índice del miércoles es el número de semanas completas transcurridas desde el ancla 2026-10-12, módulo 3: 0 es Bolt, 1 es Simplifier y 2 es la semana de Schema, que pi ejecuta desde GitHub Actions mientras Jules no abre nada.

### Rutinas de Claude

Todas las rutinas corren `claude-opus-5-5`.

| Cuándo | Rutina | Prompt |
| --- | --- | --- |
| En cada evento de pull request de las cuatro aplicaciones, gestion y aps-common | Revisor de pull requests | `routines/reviewer.md` |
| Diario, 07:00 | Supervisor matinal de Jules y resumen | `routines/digest.md` |
| Lunes, 07:30 | 📰 Informe semanal | `routines/weekly-report.md` |
| Lunes, 08:00, y al cerrarse cada pull request de aps-common | 🔗 Integrator, que abre las pull requests `🔗 Adopt:` | `routines/integrator.md` |
| Cada 3 horas, de 08:00 a 20:00 | 🧭 Consejo de diseño | `routines/council.md` |
| Diario, 06:00 | 📚 Scribe: este sitio y la documentación de cada repositorio, por carriles | `routines/scribe.md` |

El 🔗 Integrator lleva cada cambio fusionado de aps-common a cada aplicación que lo copia; el mecanismo está en {doc}`/desarrollo/aps-common`.

### Contrato común de los agentes Jules

- **Alcance.** Una ejecución abre como máximo una pull request, con una sola preocupación y unas 50 líneas de código fuente escrito a mano; los tests y los paquetes regenerados no cuentan.
- **Compuerta.** La compuerta del repositorio corre tal como la lista su `AGENTS.md`; un paso que no corrió se declara «not run», nunca como aprobado.
- **Prueba.** Un cambio de comportamiento trae un test que falla sin el cambio y pasa con él. Una refactorización o un borrado mantiene verde la compuerta completa y muestra la evidencia.
- **Prohibiciones.** Editar flujos de CI, archivos de bloqueo o listas de dependencias; editar las copias incorporadas (`src/aps/`, `vendor/aps/common/src/`, `tests/stubs/`) o, a mano, los archivos generados (`js/`, `css/`, `openapi.json`); agregar dependencias; contactar servidores reales, el laboratorio o datos reales; renombrar tablas o columnas, acciones de controlador, claves OCS o JSON, rutas o claves de traducción.

Las normas de código de `standards.md` acompañan a ese contrato: inglés en identificadores, comentarios, commits, textos de pull request y documentación, salvo el vocabulario del dominio, que conserva la grafía de `CONTEXT.md`; DRY, primero con los ayudantes del repositorio y luego con los de aps-common, sin copiar nunca código de aps-common en una aplicación; KISS; YAGNI; y SOLID pragmático, con las dependencias por constructor tipadas con las interfaces `OCP\*` de Nextcloud ({doc}`/desarrollo/plataforma/basics/dependency-injection`).

### pi en GitHub Actions

pi corre desde `APS-Conecta/agents@main` mediante el flujo reutilizable `.github/workflows/aps-pi.yml`, en epidemiologia, territorio, estadistica, farmacia, aps-common y pi-sandbox. Cada uno de esos repositorios guarda una copia byte a byte idéntica de `pi/caller.yml`, y pi marca la copia desactualizada (`caller_stale=1`), que el resumen diario informa como deriva.

El flujo tiene dos trabajos. `think` recibe solo la clave del modelo y un `GITHUB_TOKEN` de lectura; `publish` recibe la clave privada de la GitHub App y publica el resultado. La separación responde a un hallazgo crítico de la revisión del diseño: la primera versión entregaba la clave privada de la App al mismo trabajo en que corre pi, que podía volcarla y obtener escritura en todos los repositorios.

La compuerta de pi acepta solo a las personas de la lista `commanders` de la nómina, las órdenes de corrección marcadas de Claude, los eventos de pull request, la programación del miércoles y el disparo manual. El modelo es el de `pi.model` en `roster.json`, salvo que la variable de repositorio `APS_PI_MODEL` lo reemplace; los modelos declarados de la organización están en {ref}`ia`. La nómina fija también los límites de pi:

| Límite (`roster.json`, `limits`) | Valor |
| --- | --- |
| Rondas de revisión de pi por pull request | 2 |
| Rondas de corrección en una pull request de pi, antes de `needs-dani` | 2 |
| Ejecuciones de pi por repositorio y día | 15 |
| Líneas máximas de un parche de pi | 400 |
| Duración máxima de una ejecución de pi | 13 minutos |

Un parche de pi no toca las rutas y los archivos que niega la sección `patch` de la nómina: entre otros, `.github/`, las copias incorporadas, `AGENTS.md`, `CONTEXT.md`, los manifiestos y archivos de bloqueo de dependencias, `Makefile` y los `Dockerfile`.

El mapa de módulos del repositorio se genera al compilar:

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/agents>
```

## Compromisos y límites

- **Sincronización manual con Jules.** Las programaciones de Jules solo se editan en la interfaz web, así que un prompt fusionado no rige hasta que alguien lo pega. `schedule.md` es el registro de qué hash está vigente y desde cuándo.
- **Esfuerzo de las rutinas.** Las rutinas no permiten fijar el nivel de esfuerzo.
- **pi sin versión fijada.** Todos los repositorios ejecutan pi desde `main` de `agents`, y el flujo omite la regla `unpinned-uses` de `zizmor` con el argumento de que solo el responsable escribe en `agents`. Una fusión defectuosa en `pi/` afecta a la vez a todos los repositorios con pi.
- **Secretos en el runner.** El diseño de pi registra, con fecha 2026-10-03, que cualquier paso con sudo en un runner alojado puede volcar todos los secretos que referencia su trabajo, y que no había endurecimiento asequible para repositorios privados. La separación en dos trabajos acota lo que queda junto a pi; no lo elimina.
- **gestion queda fuera de pi.** El repositorio es público y un texto escrito por terceros llegaría a pi; Claude sigue revisando gestion.
- **Experimento con fecha de revisión.** La revisión del 2026-10-19 reajusta o retira a todo agente con más de 40 % de veredictos ❌ o que no fusiona nada en dos rotaciones, y reajusta el revisor de pi si Claude confirma menos del 30 % de sus hallazgos bloqueantes en dos semanas.
- **Especificación desfasada.** La especificación de diseño de la nómina conserva el estado de borrador y todavía describe un miércoles alterno por semanas ISO y a Scribe como agente de Jules; la enmienda del 2026-10-03 y `schedule.md` reemplazan ambos puntos.
