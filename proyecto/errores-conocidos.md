---
tipo: referencia
audiencia: proyecto
apps: []
resumen: "Dónde se consultan los errores conocidos de toda la suite: cada aplicación, la plataforma y esta documentación."
---
# Errores conocidos

## Resumen

Cada error se registra como issue en el repositorio de la pieza afectada: gestion, cada aplicación, AIO, IntraVox o esta documentación. Lleva la etiqueta `bug` o el tipo «Bug». Estas búsquedas reúnen los errores abiertos de todos los repositorios de la organización APS-Conecta, de modo que el listado cubre la suite completa y no un repositorio aislado. La búsqueda pública excluye los issues etiquetados `security-critical`, que se gestionan por separado.

## Tabla

| Consulta | Enlace |
|---|---|
| Errores abiertos de la suite, etiqueta `bug` | [Abrir en GitHub](https://github.com/search?q=org%3AAPS-Conecta+is%3Aissue+is%3Aopen+label%3Abug+-label%3Asecurity-critical&type=issues) |
| Errores abiertos de la suite, tipo «Bug» | [Abrir en GitHub](https://github.com/search?q=org%3AAPS-Conecta+is%3Aissue+is%3Aopen+type%3A%22Bug%22+-label%3Asecurity-critical&type=issues) |
| Todos los issues abiertos de la suite | [Abrir en GitHub](https://github.com/search?q=org%3AAPS-Conecta+is%3Aissue+is%3Aopen+-label%3Asecurity-critical&type=issues) |

## Notas

- Quien no es miembro de la organización ve solo los issues de los repositorios públicos. Los repositorios privados los muestran a sus miembros.
- Las vulnerabilidades de seguridad nunca se reportan como issues públicos. Se canalizan por el aviso privado «Report a vulnerability» de GitHub (Security → Advisories) del repositorio afectado, según la política de seguridad de la organización.
