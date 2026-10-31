---
tipo: referencia
audiencia: desarrollo
apps: [spreed]
resumen: "Chat y videollamadas con la aplicación oficial de Nextcloud Talk."
---
# spreed

## Resumen

La suite instala [Nextcloud Talk](https://github.com/nextcloud/spreed) desde la tienda de aplicaciones. El aprovisionamiento configura la señalización, STUN y TURN inmediatamente después de instalar la aplicación.

## Tabla

| Hecho | Valor |
|---|---|
| Instalación | Paquete oficial compatible con Nextcloud 34. |
| Integridad | Firma oficial presente y comprobación nativa `occ integrity:check-app spreed`. |
| Validación funcional | Chat entre cuentas de personal y comprobación nativa de señalización. |
| Uso | [Conversación](/usuario/conversacion/index). |
| Registro de cambios | [Novedades](/proyecto/novedades/spreed). |

## Notas

La aplicación oficial y los servicios de comunicación de la suite tienen responsabilidades separadas: Nextcloud Talk aporta la interfaz y APS Conecta configura la conexión.
