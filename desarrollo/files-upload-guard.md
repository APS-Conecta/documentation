---
tipo: referencia
audiencia: desarrollo
apps: [files-upload-guard]
resumen: "Protección de cargas WebDAV para Nextcloud 34: preparación temporal, primer acceso a carpetas de equipo, permisos y publicación firmada."
---
# Protección de cargas

## Resumen

[files-upload-guard](https://github.com/APS-Conecta/files-upload-guard) es el componente interno que conserva el archivo anterior cuando una carga WebDAV se rechaza y prepara el primer acceso a las carpetas de equipo. La fase 12 lo instala desde su publicación firmada. Su integración corresponde a la próxima versión de APS Conecta Gestión.

## Tabla

| Elemento | Referencia |
| --- | --- |
| Identificador de aplicación | `files_upload_guard` |
| Compatibilidad | Nextcloud 34 |
| Registro | Evento público `BeforeFileSystemSetupEvent` y `IStorageFactory` |
| Primer acceso | `SabrePluginAddEvent` prepara las carpetas superiores ausentes mediante `IRootFolder` y la interfaz pública `Folder`, después de autenticar |
| Preparación temporal | Ruta nueva con permiso CREATE en su carpeta; una ubicación insegura rechaza la carga |
| Cargas por fragmentos | Nextcloud gestiona los PUT temporales; el MOVE final conserva la protección del archivo de destino |
| Permisos del destino | Nextcloud conserva la comprobación UPDATE |
| Publicación | Flujo compartido con `php-only: true` y firma contra `apps.pub` |
| Pruebas | Trece comprobaciones de almacenamiento nativo; primera carga de sector y unidad, permisos e integridad en la instalación de la suite |
| Cambios publicados | {doc}`/proyecto/novedades/files-upload-guard` |

## Notas

[ADR-0022](https://github.com/APS-Conecta/gestion/blob/a42d863461fdb2977ab0dbbf9698c7c4b3e4a904/docs/adr/0022-preserve-upload-staging-with-a-scoped-storage-guard.md) autoriza exclusivamente la clase privada `OC\Files\Storage\Wrapper\Wrapper` y el patrón de nombres temporales de Nextcloud 34. El envoltorio se retira cuando una versión oficial compatible supera las pruebas de conservación, permisos y cargas fragmentadas; el listener se retira cuando supera las pruebas de primer acceso. La aplicación se retira al cumplirse ambas condiciones, incluida su instalación y actualización. El núcleo, DAV y el antivirus de tienda conservan sus archivos originales. El [seguimiento técnico](https://github.com/APS-Conecta/gestion/issues/239) registra la comprobación de sustituciones y permisos antes de aceptar la integración.

La aceptación por IP crea cuentas nuevas y realiza un PUT antes de cualquier PROPFIND. Comprueba HTTP 201 en sectores y unidades, HTTP 403 para lectura y HTTP 404 para una cuenta ajena. Verifica el contenido, la ausencia de archivos rechazados y la eliminación de los datos de prueba.

```{toctree}
:maxdepth: 1

Referencia de rutas y comandos <../_generated/referencia/files-upload-guard>
Mapa de módulos <../_generated/mapa/files-upload-guard>
```
