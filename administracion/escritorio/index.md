---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "El cliente de sincronización de escritorio para Windows, macOS y Linux, con las páginas sobre su implementación y la solución de problemas."
---
# Clientes de escritorio

## Resumen

Esta sección presenta el cliente de sincronización de escritorio para Windows, macOS y Linux y reúne las páginas sobre su implementación y configuración y sobre la solución de problemas de sincronización. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/desktop/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Disponible para Windows, macOS y varias distribuciones de Linux, el cliente de sincronización de escritorio de Nextcloud permite:

- Especificar uno o más directorios del equipo que se quieren sincronizar con el servidor Nextcloud.
- Tener siempre sincronizados los archivos más recientes, estén donde estén.

Los archivos se sincronizan siempre de forma automática entre el servidor Nextcloud, el equipo y el dispositivo móvil.

- {nc-doc}`admin_manual/desktop/massdeployment`
- {nc-doc}`admin_manual/desktop/troubleshooting`

Hay información adicional aquí:

- [Manual de usuario][User manual]
- [Manual para desarrolladores][Developer manual]

[User manual]: https://docs.nextcloud.com/server/latest/user_manual/en/desktop/index.html
[Developer manual]: https://docs.nextcloud.com/server/latest/developer_manual/desktop/index.html
````

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
