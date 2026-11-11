---
tipo: referencia
audiencia: desarrollo
apps: [gestion-aio]
resumen: "gestion-aio, el repositorio de la suite: el fork de Nextcloud All-in-One y la capa APS bajo aps/."
---
# gestion-aio

## Resumen

gestion-aio es el repositorio de APS Conecta Gestión: un fork de [Nextcloud All-in-One](https://github.com/nextcloud/all-in-one) que se mantiene lo más cerca posible de upstream, más la capa APS. Reemplaza a los repositorios gestion e instalador, eliminados. Sus reglas de trabajo están en `AGENTS.md` y su vocabulario en `CONTEXT.md`, ambos en inglés.

## Tabla

| Ruta | Contenido |
|---|---|
| `aps/bootstrap/` | El arranque: el comando único que instala la suite e imprime el enlace de un solo uso. |
| `aps/provisionador/` | El Provisionador, el asistente web que ejecuta la instalación, con sus pasos y el manifiesto de la suite (`apps.json`). |
| `aps/brand/`, `aps/theme/` | La paleta y las fuentes de la marca, y el tema de Nextcloud. |
| `aps/deis/` | El registro DEIS de establecimientos. |
| `aps/gates/` | Las compuertas estáticas; `aps/gates/run.sh` las ejecuta como en CI. |
| `aps/keep-list.txt` | Cada ruta donde el repositorio difiere de upstream, con su razón. |

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/gestion-aio>
```
