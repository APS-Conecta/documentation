---
tipo: referencia
audiencia: desarrollo
apps: [desktop_workspace]
resumen: "El espacio de escritorio de Nextcloud como fork propio: la vista de escritorio del personal dentro de la suite."
---
# desktop_workspace

## Resumen

[desktop_workspace](https://github.com/APS-Conecta/desktop_workspace) es el espacio de escritorio de Nextcloud: la vista de escritorio que el personal encuentra al entrar. La organización mantiene un fork propio del upstream, rebasado sobre la versión compatible con Nextcloud 34, con los cambios de la suite como commits separados.

## Tabla

| Hecho | Valor |
|---|---|
| Fuente original | [desktop_workspace de canisdata](https://github.com/canisdata/desktop_workspace), AGPL-3.0-or-later |
| Repositorio de la suite | [APS-Conecta/desktop_workspace](https://github.com/APS-Conecta/desktop_workspace), fork con los cambios como commits separados |
| Instalación | Hoy como aplicación de tienda del manifiesto; pasará a instalarse desde la release firmada del fork (instalador#37) |
| Cambios de la suite | La ruta del registro en los ajustes, errores que ya no se silencian, política de contenido sin HTTP, límites de tamaño de carga útil, documentación de la administración, pruebas fijadas, la división del shell, del observador y del controlador, y código muerto eliminado |

## Notas

- Sus rutas internas:

```{include} ../_generated/attach/desktop_workspace.md
```
- [Novedades de desktop_workspace](/proyecto/novedades/desktop_workspace).

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/desktop_workspace>
```
