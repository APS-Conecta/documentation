---
tipo: referencia
audiencia: proyecto
apps: [gestion]
resumen: "Cambios de instalador visibles para usuarios y administradores, agrupados por versión."
---
# Novedades de instalador

## Resumen

Esta página registra los cambios de instalador que ve una persona usuaria o administradora, agrupados por versión. 📚 Scribe la actualiza cada día a partir de los cambios fusionados en el repositorio; los cambios internos no figuran. Los cambios aún no publicados aparecen como «Próxima versión».

## Tabla

| Versión | Fecha | Cambio |
|---|---|---|
| Próxima versión |  | Una línea de consola instala la suite: descarga el paquete de la versión, verifica su suma sha256 y su firma, y deja lista la orden `sudo aps-conecta install`. |
| Próxima versión |  | La instalación silenciosa termina importando los datos comunales del centro; importar de nuevo no crea nada («0 creados»). |
| Próxima versión |  | El paso 7 del asistente ofrece, con consentimiento explícito («Sí, corregir»), arreglar la red del servidor cuando el dominio no responde desde el propio servidor. |
| Próxima versión |  | La revisión previa informa dos niveles de recursos —mínimo y recomendado— para memoria y disco. |
| Próxima versión |  | La revisión previa instala lo que falte —Docker, signify, gdal—, verifica el paquete guardado sin red y nombra lo que corrigió. |
| Próxima versión |  | La suite usa Euro-Office como único editor y mantiene sus aplicaciones habilitadas durante una demora del servicio. La configuración se completa en el siguiente inicio. |
| Próxima versión |  | El conjunto fijo incluye Talk, búsqueda, vistas previas, antivirus y AppAPI mediante HaRP. Farmacia, Estadística y Tótem conservan su selección. |
| Próxima versión |  | Cada construcción produce el conjunto completo de imágenes desde un commit y verifica su procedencia y resúmenes. |
| Próxima versión |  | La publicación ejecuta las compuertas completas, verifica el contenido firmado y protege las credenciales en el entorno `Release`. |
| Próxima versión |  | Las actualizaciones siguen el procedimiento de la suite y el establecimiento aporta su dominio o IP. |

## Notas

El [plan de gestion #175](https://github.com/APS-Conecta/gestion/issues/175) registra la implementación y sus verificaciones. Las integraciones de antivirus, búsqueda y AppAPI, la configuración de Talk durante el aprovisionamiento y el perfil de grabación continúan en etapas posteriores.

Estas entradas describen la próxima versión. Para instalar, seleccione una versión estable en [Publicaciones de la suite](https://github.com/APS-Conecta/gestion/releases).
