---
tipo: referencia
audiencia: desarrollo
apps: [eurooffice]
resumen: "El conector de Euro-Office como fork propio: edición en línea de documentos, planillas y presentaciones dentro de la suite."
---
# eurooffice

## Resumen

[eurooffice](https://github.com/APS-Conecta/eurooffice) es el conector de Euro-Office para Nextcloud: la aplicación que abre la edición en línea de documentos, planillas y presentaciones dentro de Archivos. La organización mantiene un fork propio del conector, rebasado sobre el upstream compatible con Nextcloud 34, con los cambios de la suite como commits separados.

El servidor de documentos —Euro-Office DocumentServer— corre como contenedor propio de la suite (`aps-conecta-eurooffice`), no como aplicación Nextcloud.

## Tabla

| Hecho | Valor |
|---|---|
| Fuente original | [eurooffice-nextcloud de Euro-Office](https://github.com/Euro-Office/eurooffice-nextcloud), AGPL-3.0-only |
| Repositorio de la suite | [APS-Conecta/eurooffice](https://github.com/APS-Conecta/eurooffice), fork con los cambios como commits separados |
| Instalación | Hoy como aplicación de tienda del manifiesto; pasará a instalarse desde la release firmada del fork (instalador#36) |
| Cambios de la suite | El nombre de la sección de administración y el nombre visible de la aplicación |
| Licencia de upstream | AGPL-3.0-only, con una disputa pública registrada sobre los términos adicionales de la sección 7 (véase {doc}`/desarrollo/licencias`) |

## Notas

- La disputa de licencia y las notas legales del servidor de documentos están en {doc}`/desarrollo/licencias` y en la tabla de componentes del {doc}`/aviso`.
- Sus rutas y comandos `occ`:

```{include} ../_generated/attach/eurooffice.md
```
- [Novedades de eurooffice](/proyecto/novedades/eurooffice).

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/eurooffice>
```
