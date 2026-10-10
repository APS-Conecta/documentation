---
tipo: referencia
audiencia: desarrollo
apps: [.github]
resumen: "El repositorio .github: los documentos que GitHub sirve a cada repositorio de la organización, quién los escribe, qué no se hereda y su deuda."
---
# .github

## Resumen

[APS-Conecta/.github](https://github.com/APS-Conecta/.github) es el repositorio de valores por defecto de la organización. GitHub sirve su guía de contribución, su política de seguridad y sus plantillas de incidencias y de pull request a cada repositorio de APS-Conecta que no tiene una copia propia, y muestra `profile/README.md` como portada de la organización.

GitHub solo sirve esos valores desde un repositorio `.github` público, así que todo lo que contiene es legible por cualquiera, aunque los repositorios a los que sirve sean privados.

El [ADR-0012 de gestion](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0012-only-the-generic-half-is-published-as-an-org-default.md) decide qué se publica aquí: solo la mitad genérica, escrita para un desconocido. La postura de seguridad de cada repositorio (2FA, escaneo de secretos, Dependabot) queda en el `SECURITY.md` propio de ese repositorio, y ningún documento que nombre una ruta de host, un volumen, una dirección interna o a un colaborador entra en `.github`.

Salvo la portada, los archivos salen de {doc}`repo-docs`: la guía y la política de seguridad se escriben en su carpeta [`public/`](https://github.com/APS-Conecta/repo-docs/tree/main/public) y se copian con el nombre de la organización sustituido; las plantillas y el `LICENSE` son canon de repo-docs.

## Tabla

| Archivo | Qué hace | Quién lo escribe |
|---|---|---|
| `profile/README.md` | Portada pública de la organización, en español y en inglés: qué hace APS Conecta, el problema que resuelve, la licencia y cómo trabaja la organización. | A mano. repo-docs la conserva y nunca la regenera. |
| `CONTRIBUTING.md` | Contrato de contribución: GitHub Flow con ramas cortas, Conventional Commits, una aprobación humana antes de integrar, la etiqueta `ai-assisted`, las reglas de documentación, los ADR en formato MADR y la licencia AGPL-3.0-or-later. | repo-docs, desde `public/CONTRIBUTING.md`. |
| `SECURITY.md` | Alcance (software de operación interna, sin datos de pacientes), el reporte privado de una vulnerabilidad, lo que queda fuera de alcance y la divulgación coordinada. | repo-docs, desde `public/SECURITY.md`. |
| `.github/PULL_REQUEST_TEMPLATE.md` | Lista de comprobación del pull request: título Conventional Commits, la compuerta local en verde, la documentación al día, una aprobación y la declaración de asistencia de inteligencia artificial. | Canon de repo-docs, idéntico byte a byte. |
| `.github/ISSUE_TEMPLATE/dev-task.yml` | Formulario técnico «Dev task / bug»: tipo, resumen, referencias, pasos para reproducir y criterios de aceptación. | Canon de repo-docs, idéntico byte a byte. |
| `.github/ISSUE_TEMPLATE/owner-task.yml` | Formulario «Solicitud (lenguaje simple)» para pedir un cambio sin términos técnicos: qué debe cambiar, por qué y cómo se sabe que está listo. | Canon de repo-docs, idéntico byte a byte. |
| `.github/ISSUE_TEMPLATE/config.yml` | Admite incidencias en blanco y enlaza la guía de contribución de la organización. | Canon de repo-docs, con la organización sustituida. |
| `LICENSE` | Texto de la GNU Affero General Public License v3.0, el mismo archivo, byte a byte, que llevan los repositorios de código. | Canon de repo-docs. Es una semilla: se escribe una vez y nunca se restaura. |

## Notas

### Herencia

- Un repositorio con su propio archivo gana: GitHub busca primero en `.github/`, luego en la raíz y luego en `docs/` del repositorio, y solo después en el repositorio de la organización.
- La carpeta `ISSUE_TEMPLATE` se hereda entera o no se hereda: un repositorio con cualquier archivo propio en ella ignora todas las plantillas de la organización. gestion conserva sus propios formularios, así que no hereda ninguno.
- `CODEOWNERS`, los workflows y los hooks de git no se heredan: cada repositorio lleva su copia, y sus hallazgos `canon-drift` no los cierra ningún valor por defecto.
- `LICENSE` tampoco se hereda: debe existir en cada repositorio para viajar con cada clon, paquete o descarga. Este repositorio lleva el suyo desde el ADR-0012, porque el ADR-0010 enumeraba solo los repositorios de código y un repositorio sin licencia queda, por defecto, con todos los derechos reservados.

### Compuertas

- La regla `public-leak` de repo-docs falla cuando un archivo de un repositorio legible por cualquiera nombra un gestor de secretos, una dirección de enlace local, una ruta absoluta de host o una casilla de endurecimiento sin marcar, o cuando revela una debilidad de la infraestructura.
- Ningún workflow corre en este repositorio, y el barrido semanal de repo-docs lo excluye del censo junto con el propio repo-docs: sus cambios no pasan por ninguna compuerta automática.

### Deuda y límites

- `CONTRIBUTING.md`, `SECURITY.md` y la portada afirman que los repositorios de la organización son privados. El {doc}`catálogo </_generated/catalogo>` marca como públicos a gestion, AIO, IntraVox, repo-docs, documentation y este mismo repositorio. La iniciativa docs-es incluye la corrección de esa afirmación en su paso R4-k para `.github`, todavía pendiente.
- `CONTRIBUTING.md`, `SECURITY.md`, la plantilla de pull request y el formulario técnico están en inglés; la portada y el formulario «Solicitud» son bilingües. El repositorio no lleva el marcador `.github/docs-es`, así que sigue en el régimen histórico en inglés que describe el [ADR 0006 de repo-docs](https://github.com/APS-Conecta/repo-docs/blob/main/docs/adr/0006-documentacion-en-espanol.md). La iniciativa docs-es prevé una portada solo en español y `CONTRIBUTING.md`, `SECURITY.md` y `CODE_OF_CONDUCT.md` en español.
- `CODE_OF_CONDUCT.md` todavía no existe: la iniciativa docs-es lo prevé como el Contributor Covenant 2.1 en español.
- `references/layout.md` de repo-docs describe el árbol de este repositorio sin `LICENSE`, mientras el ADR-0012 lo agregó y el repositorio lo lleva: la referencia contradice la decisión.
