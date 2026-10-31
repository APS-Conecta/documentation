---
tipo: referencia
audiencia: desarrollo
apps: [side_menu]
resumen: "Menú lateral oficial con los colores de APS Conecta."
---
# side_menu

## Resumen

La suite instala [Custom Menu](https://gitnet.fr/deblan/side_menu) desde la tienda de aplicaciones de Nextcloud. La fase de marca configura el color del menú mediante las opciones oficiales de la aplicación.

## Tabla

| Hecho | Valor |
|---|---|
| Instalación | Paquete oficial compatible con la versión de Nextcloud instalada. |
| Configuración | `background-color` y `background-color-to`, con el morado de la marca. |
| Integridad | Firma oficial presente y comprobación nativa `occ integrity:check-app side_menu`. |
| Validación funcional | Opciones guardadas y color aplicado en la hoja de estilos servida. |
| Registro de cambios | [Novedades](/proyecto/novedades/side_menu). |

## Notas

La provisión conserva la versión instalada y aplica la configuración de marca.
