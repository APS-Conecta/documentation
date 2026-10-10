---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Otras API OCS de Nextcloud que las ExApps pueden usar con la autenticación de AppAPI, si AppAPI las admite y la ExApp concede el acceso."
---
# Otras API OCS

## Resumen

Esta página enumera otras API OCS de Nextcloud que las ExApps pueden usar con la autenticación de AppAPI, siempre que AppAPI las admita y la ExApp conceda el acceso en `info.xml`. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/other_ocs.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Con la autenticación de AppAPI, las ExApps pueden usar cualquier otra API OCS que no requiera una implementación de OCP:

:::{note}
Para acceder a estas API, AppAPI tiene que admitirlas,
y la ExApp debe conceder el acceso a ellas (en `info.xml`) en consecuencia.
:::

1. Calendario
2. Contactos
3. Sistema de archivos y etiquetas
4. Recursos compartidos
5. Notificaciones
6. Usuarios y grupos
7. Estado del usuario y del tiempo
8. Actividades
9. Notas
10. Etc.
````
