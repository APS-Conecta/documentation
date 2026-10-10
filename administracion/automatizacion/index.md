---
tipo: referencia
audiencia: administracion
apps: [gestion, AIO]
resumen: "Automatización en APS Conecta Gestión: el estado de los receptores de webhooks, de Windmill, de los trabajos en segundo plano y de las tareas periódicas."
---
# Automatización

## Resumen

Esta sección reúne, para quienes administran el servidor, las páginas de la plataforma base sobre automatización: los receptores de webhooks y los flujos de trabajo de Windmill. La tabla indica el estado de cada mecanismo en APS Conecta Gestión y la página que lo describe, junto con las tareas periódicas que ejecuta la propia suite.

## Tabla

| Mecanismo | En APS Conecta Gestión | Página |
|---|---|---|
| Receptores de webhooks (`webhook_listeners`) | La provisión no activa ni desactiva la app y no registra ningún webhook: la política de aplicaciones la deja intacta, reservada para integraciones de la hoja de ruta. | {doc}`webhooks` |
| Flujos de trabajo de Windmill | No disponible: la plataforma base pide una instancia independiente de Windmill y la app de integración de la tienda de aplicaciones; la suite no instala Windmill, la tienda está desactivada y la integración no está entre las aplicaciones de la suite. | {doc}`windmill` |
| Trabajos en segundo plano | Corren por cron, no por ajax, para que no dependan de que alguien cargue una página. | {doc}`/administracion/servidor/background-jobs-configuration` |
| Tareas periódicas de la suite | La re-provisión semanal y el refresco mensual del mapa base corren con temporizadores de systemd en el servidor. | {doc}`/administracion/operaciones/index` |

## Notas

- **La reserva de los webhooks.** La política de aplicaciones cita [gestion#27](https://github.com/APS-Conecta/gestion/issues/27) (Paperless-ngx) y [gestion#28](https://github.com/APS-Conecta/gestion/issues/28) (Analytics). La hoja de ruta mantiene Paperless-ngx como trabajo futuro, y Analytics pasó a formar parte de Estadística.
- **Windmill empaquetado.** La app externa «Flow», que instalaba Windmill dentro de la plataforma como ExApp, está obsoleta desde la versión 33 de la plataforma base. {doc}`/administracion/exapps/index` describe la postura de la suite ante las ExApps.

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
