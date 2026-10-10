---
tipo: explicacion
audiencia: desarrollo
apps: [repo-docs]
resumen: "repo-docs: el motor que audita la documentación de cada repositorio, su perfil, sus reglas, sus compuertas, el barrido semanal y sus límites."
---
# repo-docs

## Contexto

[APS-Conecta/repo-docs](https://github.com/APS-Conecta/repo-docs) es el control de documentación de la organización. Audita lo que ya está escrito, corrige lo que tiene una única respuesta demostrable y genera el andamiaje de lo que falta.

Existe porque la documentación de la organización ya derivaba: archivos de gestion que discrepaban sobre el tamaño del equipo, repositorios cuya licencia declarada contradecía su `LICENSE` y ADR sin campo de estado. No es un asistente de escritura: comprueba que la documentación esté estructuralmente completa y sea factualmente consistente, y deja la prosa a una persona o a un modelo.

Ningún repositorio importa repo-docs. Se invoca como CLI, y cada repositorio gobernado lleva una copia en `.github/repo-docs.py` que su workflow `docs` corre en cada pull request. Este sitio es uno de ellos; su compuerta corre:

```bash
python3 .github/repo-docs.py check . --offline
```

Los subcomandos (auditar, generar el andamiaje, sondear la configuración de GitHub, abrir un pull request de documentación) están en el [README](https://github.com/APS-Conecta/repo-docs/blob/main/README.md) del repositorio, y su {doc}`inicio rápido de desarrollo </_generated/inicio-rapido/repo-docs>` se incluye en este sitio al compilar.

La licencia es GNU Affero General Public License v3.0 o posterior, la misma de toda la organización. La herramienta solo usa la biblioteca estándar de Python, así que no lleva avisos de terceros.

## Diseño

### Mecánico, de juicio y semilla

Cada artefacto de documentación pertenece a una sola clase, y la clase decide quién lo escribe y si `--fix` lo toca:

- **Mecánico:** tiene una sola forma correcta en toda la organización: formularios de incidencia, plantilla de pull request, `CODEOWNERS`, el hook de pre-commit, el workflow `docs`. Vive en `canon/`, se genera desde ahí y `--fix` lo repara. Una diferencia entre dos repositorios es deriva, y la deriva es un defecto.
- **De juicio:** no tiene forma única: README, cuerpo de `CONTRIBUTING.md`, ADR, guías. La herramienta revisa su estructura y nunca reescribe su prosa.
- **Semilla:** `LICENSE` y `CHANGELOG.md` se escriben una vez si faltan y nunca se restauran, porque acumulan contenido propio de cada repositorio. Restaurar un `CHANGELOG.md` desde su esqueleto borraría el registro de cambios.

`harvest` refresca `canon/` desde gestion, el ejemplar que fija el perfil, así que el estilo de la casa tiene un solo origen.

### Motor y perfil

- El **motor** codifica oficio, válido en cualquier organización: un enlace resuelve o no, un ADR sin estado no se puede reemplazar, un comando documentado que no existe es falso, una afirmación debe coincidir con su autoridad.
- El **perfil** codifica decisiones, como datos: `profiles/_base.json` lleva la convención universal (Diátaxis, Keep a Changelog, MADR) y `profiles/aps-conecta.json` las decisiones de APS-Conecta, como la licencia AGPL, el ejemplar y quién revisa el código. Un perfil parametriza reglas y hechos; nunca los define.
- El perfil se elige por el dueño del remoto del repositorio. Un dueño sin perfil queda «no administrado» y la herramienta se niega a operar: la ausencia de política es una negativa, nunca un valor por defecto.

### Hechos, autoridades y afirmaciones

Cada hecho tiene una sola autoridad: la API de GitHub para la membresía y la visibilidad, el archivo `LICENSE` para la licencia, `compose.yaml` para las versiones del stack. Una afirmación es una línea de documentación que asevera un hecho. La herramienta distingue dos fallas: la **contradicción**, cuando dos afirmaciones discrepan, y la **deriva**, cuando una afirmación discrepa de su autoridad. Un repositorio puede ser coherente consigo mismo y estar uniformemente equivocado.

### La copia en cada repositorio

El `GITHUB_TOKEN` de un workflow solo alcanza su propio repositorio, así que la compuerta de un repositorio no puede clonar repo-docs. Cada repositorio lleva entonces `.github/repo-docs.py` y `.github/profiles/`, generados desde `canon/`. `canon-drift` compara la copia con `canon/` donde existe; en los repositorios gobernados no hay `canon/`, así que la regla informa SKIP y la copia lleva un `CANON_STAMP` con el digest del canon del que salió.

### Configuración de GitHub

`settings` sondea la configuración de GitHub y `--apply-settings` la cambia, para que la documentación y la realidad converjan en lugar de solo informarse como divergentes: alertas y actualizaciones de Dependabot, reporte privado de vulnerabilidades, escaneo de secretos y 2FA de la organización. El reporte privado y el escaneo de secretos se informan como no aplicables en un repositorio privado, porque GitHub los ofrece solo en repositorios públicos. `org-2fa` tiene una verificación previa: lista los miembros sin 2FA y se niega mientras esa lista no esté vacía, porque imponer el 2FA expulsaría a esos miembros.

### Compuertas

| Workflow | Dónde y cuándo | Qué corre |
|---|---|---|
| `docs` | En cada repositorio gobernado, en cada pull request y en cada push a `main`. | `pr-gate`, que exige un título de pull request en inglés, y `check . --offline`, con gitleaks sobre el rango de commits del pull request. |
| `selftest` | Solo en repo-docs, cuando cambian `scripts/`, `canon/`, `profiles/` o los workflows. | actionlint sobre el canon y los workflows generados, y los selftests de `scripts/docs.py` y `scripts/census.py`. |
| `sweep` | Solo en repo-docs, cada lunes a las 05:43 UTC y a mano. | Clona el censo y corre `check --all --stamp-error`. Falla con hallazgos nuevos respecto de `baseline.json`, con un sello desactualizado o cuando un repositorio de la suite no tiene clave en `baseline.json`. |

El censo del barrido es la unión de las claves de `baseline.json`, menos `.github` y el propio repo-docs, con las aplicaciones propias que gestion declara en `OWN_APPS` (`provisioning/phases/12-apps.sh`). Por eso una aplicación no se distribuye sin entrar al barrido. El `Makefile` de repo-docs reúne los dos selftests en un solo objetivo para correrlos en local.

### Régimen en español y estructura de página

Un repositorio opta por el régimen en español del [ADR 0006](https://github.com/APS-Conecta/repo-docs/blob/main/docs/adr/0006-documentacion-en-espanol.md) con el archivo marcador vacío `.github/docs-es`. Desde entonces, `doc-language-es` exige prosa en español archivo por archivo en la lista obligatoria, `readme-sections` exige las cinco secciones del README en orden y `retired-paths` prohíbe las rutas que el ADR retiró, las tres con severidad de error. El marcador `.github/site-structure` activa `site-structure`: front matter tipado y un esqueleto H2 por `tipo`. Este sitio lleva los dos marcadores.

### Registro de reglas

Agregar una regla es una función y un decorador. Las reglas con alcance «organización» necesitan autenticación con alcance de organización: la compuerta de cada pull request no las corre. `check --explain` imprime, junto a cada hallazgo, la razón de su regla.

| Regla | Severidad | Alcance | Detecta |
|---|---|---|---|
| `missing-required` | error | compuerta | Un archivo que el nivel del repositorio exige y falta. |
| `tracked-not-present` | error | compuerta | Un archivo versionado que el árbol no tiene. |
| `retired-paths` | error | compuerta, régimen en español | Una ruta que el ADR 0006 retiró, versionada o no. |
| `license-posture` | error | compuerta | Una licencia distinta de la postura del perfil. |
| `licence-declaration` | error | compuerta | Declaraciones de licencia que discrepan entre `LICENSE`, `appinfo/info.xml`, `composer.json` y `package.json`. |
| `licence-prose` | error | compuerta | Prosa que presenta como privativo el código de la organización cuando la postura del perfil es otra. |
| `licence-inventory` | aviso | compuerta | Licencias de terceros que el documento de avisos no nombra, o componentes que ese documento nombra y ya no están. |
| `canon-drift` | error | compuerta | Un archivo mecánico que difiere de `canon/`. |
| `canon-stamp` | aviso; error en el barrido | compuerta | Una copia cuyo sello no corresponde al canon vigente. |
| `secrets` | error | compuerta | Un secreto versionado. |
| `public-leak` | error | compuerta | Datos internos en un repositorio legible por cualquiera. |
| `broken-links` | error | compuerta | Un enlace relativo cuyo destino no existe. |
| `fact-contradiction` | error | compuerta | Dos afirmaciones que discrepan sobre un mismo hecho. |
| `fact-vs-reality` | error | organización | Una afirmación que discrepa de su autoridad. |
| `claim-boxes` | aviso | organización | Casillas sin marcar en la documentación: compromisos abiertos. |
| `unfilled-contract` | error | compuerta | Un esquema generado que se publicó sin llenar. |
| `phantom-command` | error | compuerta | Un comando documentado que no existe. |
| `unverified-command` | aviso | compuerta | Un comando documentado que ninguna compuerta corre. |
| `adr-status` | aviso | compuerta | Un ADR sin campo de estado. |
| `diataxis-verification` | aviso | compuerta | Una guía (`tipo: guia`) sin forma de comprobar que funcionó. |
| `site-structure` | error | compuerta, con marcador | Front matter o esqueleto H2 que no cumplen el perfil. |
| `readme-sections` | aviso; error en el régimen en español | compuerta | Secciones del README ausentes o, en el régimen en español, fuera de orden. |
| `absolute-path` | aviso | compuerta | Una ruta absoluta de host, que no es portable. |
| `personal-data` | aviso | compuerta | Nombres o direcciones personales fuera de los archivos que los admiten. |
| `doc-language` | aviso | compuerta, sin marcador | Documentación en un idioma distinto del que fija el perfil. |
| `doc-language-es` | error | compuerta, régimen en español | Prosa de cuerpo que no está en español en la lista obligatoria. |
| `nested-repo` | información | compuerta | Un repositorio git dentro del árbol, sin `.gitmodules`. |
| `github-metadata` | error | organización | Una descripción del repositorio en GitHub vacía o que presume un solo establecimiento. |
| `branch-name` | información | organización | Una rama por defecto distinta de `main`. |

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/repo-docs>
```

## Compromisos y límites

- La herramienta no mejora la calidad de la prosa: solo garantiza que esté completa y sea consistente.
- Saber por qué disparó una regla exige leer dos archivos, el motor y el perfil; `--explain` acorta esa distancia. `github-metadata` no tiene razón registrada, así que `--explain` imprime «-» para ella.
- Un perfil puede desactivar una regla. Por eso una regla omitida se imprime como omitida, nunca como aprobada.
- La herramienta tiene el permiso `admin:org`. Por eso `--apply-settings` se pide en cada corrida y `--fix` no lo implica, y el selftest afirma la verificación previa de `org-2fa`.
- La compuerta de cada pull request corre solo las reglas de alcance «compuerta»: el `GITHUB_TOKEN` no lee hechos de la organización.
- La copia en cada repositorio cuesta un commit de mantenimiento cada vez que cambia el motor, y ya falló en silencio: hasta el 2026-08-08 no se había ejecutado nunca en ningún repositorio. Un perfil copiado puede derivar sin aviso entre refrescos; el sello registra qué motor tiene cada copia, pero sin `canon/` no se puede verificar ahí.
- El ADR 0004, que decide la copia en cada repositorio, parte de que todos los repositorios de la organización son privados. Hoy el {doc}`catálogo </_generated/catalogo>` marca repo-docs como público, y el ADR sigue aceptado sin revisión.
- `check --all` termina con código 1 ante cualquier error abierto, y la línea base registra errores conocidos. Por eso el veredicto del barrido es la búsqueda de hallazgos nuevos en su salida, con un marcador que impide que una caída del verificador pase por verde.
- El barrido lee el PAT `APS_BOT_PAT` de la organización. La iniciativa docs-es prevé reemplazarlo por un token de una hora de una GitHub App y tomar el censo de `catalogo.yml`. Mientras tanto, un repositorio ausente de `baseline.json` y de `OWN_APPS` queda fuera del barrido: este sitio, por ejemplo, queda cubierto solo por sus propias compuertas.
- El README registra una tarea pendiente: ensanchar el PAT del barrido para que el registro del censo vea lo mismo que el barrido.
- El nivel `ultra` define la división de Diátaxis en carpetas, pero nada la exige. Es una omisión deliberada: ningún repositorio usa ese nivel.
