---
tipo: referencia
audiencia: desarrollo
apps: [.github]
resumen: "El repositorio .github: los archivos en español que GitHub sirve a cada repositorio y el flujo compartido de publicación de apps; qué no se hereda."
---
# .github

## Resumen

[APS-Conecta/.github](https://github.com/APS-Conecta/.github) es el repositorio de valores por defecto de la organización. GitHub sirve su guía de contribución, su política de seguridad y sus plantillas de incidencias y de pull request a cada repositorio de APS Conecta que no tiene una copia propia, y muestra `profile/README.md` como portada de la organización.

GitHub solo sirve esos valores desde un repositorio `.github` público, así que todo lo que contiene es legible por cualquiera, aunque los repositorios a los que sirve sean privados. La postura de seguridad —escaneo de secretos, protección contra inserción y reporte privado de vulnerabilidades— es la configuración de seguridad de la organización en los ajustes de GitHub, no un archivo de este repositorio.

Además de los archivos comunitarios, el repositorio lleva el flujo de trabajo compartido con que cada aplicación de la suite publica sus versiones firmadas.

## Tabla

| Archivo | Qué hace |
|---|---|
| `profile/README.md` | Portada pública de la organización: una línea de presentación con el enlace a la documentación, al aviso de licencias y marcas y a la política de seguridad. |
| `CONTRIBUTING.md` | Una línea: las reglas para contribuir viven en {doc}`calidad` y en la {doc}`página de este sitio <documentation>`. |
| `SECURITY.md` | Política de seguridad: nunca una incidencia pública; «Report a vulnerability» en el repositorio público afectado o en instalador cuando el código no es público; los componentes de terceros se informan a su proyecto de origen; divulgación coordinada. |
| `.github/PULL_REQUEST_TEMPLATE.md` | Cuatro comprobaciones: título en inglés y Conventional Commits, la compuerta del repositorio en verde (o qué no se ejecutó), el sitio al día si cambió un hecho, y la etiqueta `ai-assisted` si una IA ayudó. |
| `.github/ISSUE_TEMPLATE/error.yml` | Formulario «Error» (tipo *Bug*): qué ocurrió y pasos para reproducirlo. |
| `.github/ISSUE_TEMPLATE/tarea.yml` | Formulario «Tarea» (tipo *Task*): qué hay que hacer y cómo sabremos que está listo. |
| `LICENSE` | El texto de la GNU Affero General Public License v3.0, el mismo archivo que llevan los repositorios de código. |
| `.github/workflows/ci.yml` | La CI propia del repositorio: `shellcheck` y las autopruebas del empaquetador y de los archivos de comunidad —los presupuestos de líneas de T06, las palabras vetadas y los tipos de los formularios—, más `actionlint` y `zizmor` sobre los flujos. |
| `.github/workflows/app-release.yml` | El flujo compartido de publicación de aplicaciones: en un pull request solo construye; en una etiqueta `v*` comprueba que la etiqueta coincide con la versión declarada, empaqueta de forma determinista, firma contra la clave de aplicaciones y publica los cuatro recursos de nombre fijo, con la aprobación del entorno `release`. |
| `scripts/pack-app.sh` | El empaquetador determinista que usa el flujo: nombres ordenados, fecha de commit, propietario numérico, `gzip -n`. |

## Notas

### Herencia

- Un repositorio con su propio archivo gana: GitHub busca primero en `.github/`, luego en la raíz y luego en `docs/` del repositorio, y solo después en el repositorio de la organización.
- La carpeta `ISSUE_TEMPLATE` se hereda entera o no se hereda: un repositorio con cualquier archivo propio en ella ignora todas las plantillas de la organización.
- `CODEOWNERS`, los workflows y los hooks de git no se heredan: cada repositorio lleva su copia.
- `LICENSE` tampoco se hereda: debe existir en cada repositorio para viajar con cada clon, paquete o descarga.
