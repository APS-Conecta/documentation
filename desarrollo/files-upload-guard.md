---
tipo: referencia
audiencia: desarrollo
apps: [files-upload-guard]
resumen: "Protección de cargas WebDAV para Nextcloud 34: preparación temporal, permisos y publicación firmada."
---
# Protección de cargas

## Resumen

[files-upload-guard](https://github.com/APS-Conecta/files-upload-guard) es el componente interno que conserva el archivo anterior cuando una carga WebDAV se rechaza. La fase 12 lo instala desde su publicación firmada. Su integración corresponde a la próxima versión de APS Conecta Gestión.

## Tabla

| Elemento | Referencia |
| --- | --- |
| Identificador de aplicación | `files_upload_guard` |
| Compatibilidad | Nextcloud 34 |
| Registro | Evento público `BeforeFileSystemSetupEvent` y `IStorageFactory` |
| Preparación temporal | Ruta nueva con permiso CREATE en su carpeta; una ubicación insegura rechaza la carga |
| Permisos del destino | Nextcloud conserva la comprobación UPDATE |
| Publicación | Flujo compartido con `php-only: true` y firma contra `apps.pub` |
| Pruebas | Trece comprobaciones de almacenamiento nativo y las pruebas WebDAV de instalación de la suite |
| Cambios publicados | {doc}`/proyecto/novedades/files-upload-guard` |

## Notas

ADR-0022 delimita la compatibilidad con el envoltorio de almacenamiento y el nombre temporal de Nextcloud 34. El núcleo y el antivirus de tienda conservan sus archivos originales. El [seguimiento técnico](https://github.com/APS-Conecta/gestion/issues/239) registra la comprobación de sustituciones y permisos antes de aceptar la integración.

```{toctree}
:maxdepth: 1

Referencia de rutas y comandos <../_generated/referencia/files-upload-guard>
Mapa de módulos <../_generated/mapa/files-upload-guard>
```
