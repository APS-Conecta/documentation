---
tipo: referencia
audiencia: desarrollo
apps: [spreed]
resumen: "Talk de la suite: el fork propio de spreed, instalado desde su release firmada; el chat y las videollamadas internas del establecimiento."
---
# spreed

## Resumen

[spreed](https://github.com/APS-Conecta/spreed) es Talk, el chat y las videollamadas de la suite: un fork propio de la aplicación de Nextcloud, mantenido como repositorio de la organización para publicar sus versiones firmadas ([ADR-0020 de la suite](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0020-spreed-is-a-fork-app-with-signed-releases.md)). La suite lo instala como aplicación predeterminada desde su propia release firmada, como al resto de las aplicaciones propias y fork, y su contenedor de grabación (`aps-conecta-talk`) es opcional.

El uso que hace el personal está en la sección de conversación del manual de usuario; esta página es el registro del lado del desarrollo.

## Tabla

| Hecho | Valor |
|---|---|
| Fuente original | [Talk (`spreed`) de Nextcloud](https://github.com/nextcloud/spreed), AGPL-3.0-or-later |
| Versión en la suite | La última release firmada del repositorio propio; hoy, 24.0.6 |
| Instalación | Desde la release del repositorio propio, verificada con la clave de aplicaciones de la suite |
| Registro de cambios | [Novedades de Talk](/proyecto/novedades/spreed) |

## Notas

- El fork nació del árbol de la versión de la tienda que la suite ya usaba; sus primeras
  releases no cambian comportamiento, solo el canal de instalación y actualización.

```{toctree}
:maxdepth: 1

Referencia de rutas y comandos <../_generated/referencia/spreed>
Mapa de módulos <../_generated/mapa/spreed>
```
