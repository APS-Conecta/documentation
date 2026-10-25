---
tipo: referencia
esqueleto: contratos
audiencia: desarrollo
apps: [totem]
resumen: "Contratos de totem: turnos de atención con tótem, pantalla de sala y ventanilla, sin publicar todavía en la suite."
---
# totem

## Propósito y diseño

Totem gestiona los turnos de atención de un centro: la persona retira un número en el tótem, la pantalla de sala anuncia el llamado con voz en español, y la ventanilla avanza la fila con un solo botón. Es una aplicación Nextcloud nativa (Nextcloud 34, PHP 8.2–8.5) bajo AGPL-3.0-or-later, con las voces de la pantalla incluidas en el paquete para funcionar sin red.

Sus cuatro superficies:

| Superficie | Ruta | Quién la usa |
|---|---|---|
| Tótem | `/apps/totem/totem` (y `/apps/totem/totem/<nombre>` por tótem configurado) | Anónima, táctil: dos toques, unidad y preferente, y el ticket imprime |
| Pantalla de sala | `/apps/totem/display/<pantalla>` | Anónima: el llamado, los llamados recientes, campanillas y la voz en español |
| Ventanilla | `/apps/totem/box` | Con sesión: un botón guiado por estado — llamar siguiente, iniciar atención, finalizar atención |
| Estadísticas | `/apps/totem/estadisticas` | Con sesión: conteos absolutos de tickets por día, semana o mes, por sector, unidad y preferente, con descarga CSV |

No está publicada en la suite: el manifiesto aún no la instala y no tiene release firmada. Cuando entre, su fila del catálogo pasa a aplicación Nextcloud y su instalación llega desde la release de su propio repositorio.

## Deuda técnica y límites

- **Sin publicar.** El catálogo la lista como aplicación sin publicar; ninguna instalación la sirve todavía y sus contratos internos pueden cambiar antes de la primera release.
- **Depende de aps-common.** Comparte con las demás aplicaciones propias las reglas de texto de la biblioteca común.
