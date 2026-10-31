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
| Cargas por fragmentos | Nextcloud gestiona los PUT temporales; el MOVE final conserva la protección del archivo de destino |
| Permisos del destino | Nextcloud conserva la comprobación UPDATE |
| Publicación | Flujo compartido con `php-only: true` y firma contra `apps.pub` |
| Pruebas | Trece comprobaciones de almacenamiento nativo y las pruebas WebDAV de instalación de la suite |
| Cambios publicados | {doc}`/proyecto/novedades/files-upload-guard` |

## Notas

[ADR-0022](https://github.com/APS-Conecta/gestion/blob/03d54692d12de1b56a3f05b7df5241d3ba18a082/docs/adr/0022-preserve-upload-staging-with-a-scoped-storage-guard.md) autoriza exclusivamente la clase privada `OC\Files\Storage\Wrapper\Wrapper` y el patrón de nombres temporales de Nextcloud 34. La excepción y la aplicación se retiran cuando una versión oficial compatible supera las mismas pruebas de conservación, permisos, cargas fragmentadas, instalación y actualización sin este componente. El núcleo y el antivirus de tienda conservan sus archivos originales. El [seguimiento técnico](https://github.com/APS-Conecta/gestion/issues/239) registra la comprobación de sustituciones y permisos antes de aceptar la integración.

```{toctree}
:maxdepth: 1

Referencia de rutas y comandos <../_generated/referencia/files-upload-guard>
Mapa de módulos <../_generated/mapa/files-upload-guard>
```
