---
tipo: referencia
audiencia: desarrollo
apps: [files-fulltextsearch]
resumen: "Proveedor de búsqueda de archivos para Nextcloud 34: identidad del usuario, procedencia y publicación firmada."
---
# Búsqueda de contenido en Archivos

## Resumen

[files-fulltextsearch](https://github.com/APS-Conecta/files-fulltextsearch) mantiene el proveedor de archivos de Nextcloud 34 con la corrección de origen para identificadores de usuario que contienen puntos. La fase 12 lo instala desde su publicación firmada. Su integración corresponde a la próxima versión de APS Conecta Gestión.

## Tabla

| Elemento | Referencia |
| --- | --- |
| Identificador | `files_fulltextsearch` |
| Compatibilidad | Nextcloud 34 |
| Fuente | Rama `stable34`, commit `26bd54ddcec5e26b1e5e905d7417910d2a6a0baf` |
| Corrección | Identificador real en la consulta del usuario y el cálculo de la ruta del resultado |
| Publicación | Flujo compartido, cuatro activos firmados y verificación contra `apps.pub` |
| Versión instalada | Registro del servidor en `apps.lock.json`; actualización mediante el procedimiento de la suite |
| Aceptación | Archivo de una cuenta sin privilegios, contenido exclusivo e identidad exacta en el motor y en el resultado |
| Cambios publicados | {doc}`/proyecto/novedades/files-fulltextsearch` |

## Notas

La [corrección de origen](https://github.com/nextcloud/files_fulltextsearch/pull/463) conserva las consultas de autorización y utiliza el identificador real al completar el resultado. El paquete mantiene la interfaz y la licencia originales. La construcción compila la configuración de administración y copia el script heredado a su ruta habitual sin alterar sus bytes.

[ADR-0023](https://github.com/APS-Conecta/gestion/blob/f18f3b2b02c80f59e4981f12b646b6d29c3fed49/docs/adr/0023-signed-search-provider-until-the-fixed-store-release.md) registra dos aplicaciones de tienda y este proveedor firmado. El retorno requiere una publicación compatible de tienda que incluya la corrección, una migración de canal y bloqueo de versión verificada, y las mismas pruebas de instalación y búsqueda. El [seguimiento técnico](https://github.com/APS-Conecta/gestion/issues/241) registra la integración.

```{toctree}
:maxdepth: 1

Referencia de rutas y comandos <../_generated/referencia/files-fulltextsearch>
Mapa de módulos <../_generated/mapa/files-fulltextsearch>
```
