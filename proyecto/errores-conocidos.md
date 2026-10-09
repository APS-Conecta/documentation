---
tipo: referencia
audiencia: proyecto
apps: []
resumen: "Dónde se registran y se consultan los errores conocidos de la organización."
---
# Errores conocidos

## Resumen

Los errores de la organización se registran como issues con tipo en el nivel de la organización: no existen listas de errores por repositorio y el listado vivo siempre refleja el estado real de cada repositorio. La búsqueda pública excluye los issues etiquetados `security-critical`, que se gestionan por separado.

## Tabla

| Consulta | Enlace |
|---|---|
| Errores abiertos de tipo «Bug» | [Abrir en GitHub](https://github.com/search?q=org%3AAPS-Conecta+is%3Aissue+is%3Aopen+type%3A%22Bug%22+-label%3Asecurity-critical&type=issues) |

## Notas

Las vulnerabilidades de seguridad nunca se reportan como issues públicos: se canalizan por el aviso privado «Report a vulnerability» de GitHub (Security → Advisories) del repositorio afectado, según la política de seguridad de la organización.
