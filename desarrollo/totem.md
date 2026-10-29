---
tipo: referencia
esqueleto: contratos
audiencia: desarrollo
apps: [totem]
resumen: "Contratos de totem: turnos de atención con tótem, pantalla de sala y ventanilla; aplicación opcional de la suite, desactivada por omisión."
---
# totem

## Propósito y diseño

Totem gestiona los turnos de atención de un centro: la persona retira un número en el tótem, la pantalla de sala anuncia el llamado con voz en español, y la ventanilla avanza la fila con un solo botón. Es una aplicación Nextcloud nativa (Nextcloud 34, PHP 8.2–8.5) bajo AGPL-3.0-or-later, con las voces de la pantalla incluidas en el paquete para funcionar sin red.

Sus cuatro superficies:

| Superficie | Ruta | Quién la usa |
|---|---|---|
| Tótem | `/apps/totem/totem` (y `/apps/totem/totem/<slug>` por tótem configurado) | Anónima, táctil: dos toques, unidad y preferente, y el ticket imprime |
| Pantalla de sala | `/apps/totem/display/<pantalla>` | Anónima: el llamado, los llamados recientes, campanillas y la voz en español |
| Ventanilla | `/apps/totem/box` | Con sesión: un botón guiado por estado — llamar siguiente, iniciar atención, finalizar atención |
| Estadísticas | `/apps/totem/estadisticas` | Con sesión: conteos absolutos de tickets por día, semana o mes, por sector, unidad y preferente, con descarga CSV |

La dirección de un tótem o de una pantalla sale de su nombre cuando se crea el registro y no cambia aunque se renombre; si otro registro renombrado todavía ocupa esa dirección, la nueva lleva `-2`, `-3` y así sucesivamente. Dos tótems, o dos pantallas, no pueden llevar el mismo nombre, ni al crearlos ni al renombrarlos; las tildes, las mayúsculas, los espacios y la puntuación no cuentan.

Tótem es una aplicación opcional de la suite: el asistente de instalación la ofrece desactivada por omisión y, cuando un centro la elige, el instalador la descarga de la release firmada de su propio repositorio ([ADR-0017 de la suite](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0017-apps-install-from-their-own-releases.md)); su versión queda registrada en el archivo de bloqueo del servidor. Los cambios visibles de cada versión se registran en {doc}`/proyecto/novedades/totem`.

## Deuda técnica y límites

- **Opcional y reciente.** El asistente la ofrece desactivada por omisión y su primera versión firmada es la v0.3.0: ninguna instalación la sirve todavía y sus contratos internos pueden cambiar antes de que un centro la use.
- **Depende de aps-common.** Comparte con las demás aplicaciones propias las reglas de texto de la biblioteca común.

Sus comandos `occ`, ajustes y rutas:

```{include} ../_generated/attach/totem.md
```

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/totem>
```
