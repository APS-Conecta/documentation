---
tipo: referencia
audiencia: desarrollo
apps: [side_menu]
resumen: "El menú lateral de la suite: el fork propio de Custom menu, instalado desde su release firmada y con el color que fija la marca."
---
# side_menu

## Resumen

[side_menu](https://github.com/APS-Conecta/side_menu) es el menú lateral de la suite: un fork propio de *Custom menu*, la aplicación de Nextcloud de Simon Vieille, mantenido como repositorio de la organización porque la fuente original (`gitnet.fr`) está inaccesible. La suite lo instala como aplicación predeterminada desde su propia release firmada (instalador#38), como al resto de las aplicaciones propias y fork.

La marca no lo edita como código: la fase de marca solo fija su color, que la aplicación deriva por sí misma del tema del servidor, y el color fijado es el morado de la paleta de APS Conecta.

## Tabla

| Hecho | Valor |
|---|---|
| Fuente original | [*Custom menu* de Simon Vieille](https://gitnet.fr/deblan/side_menu), AGPL-3.0-or-later, rama 6.0.1 |
| Versión en la suite | La última release firmada del repositorio propio; hoy, 6.0.1 |
| Instalación | Desde la release del repositorio propio, verificada con la clave de aplicaciones de la suite |
| Configuración de la suite | Solo el color (`background-color` y `background-color-to`, el morado de la marca), fijado por la fase de marca; el resto son ajustes del sitio |
| Registro de cambios | [Novedades de side_menu](/proyecto/novedades/side_menu) |

## Notas

- El fork nace del tarball AGPL 6.0.1 de upstream, sin cambios propios: existe para tener una fuente pública y firmada de la versión que la suite instala. Si upstream vuelve a estar accesible, la política del fork se revisa.
- Sus configuraciones de administración:

```{include} ../_generated/attach/side_menu.md
```

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/side_menu>
```
