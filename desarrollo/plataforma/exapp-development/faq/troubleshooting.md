---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Pasos para diagnosticar problemas de AppAPI: red, despliegue de ExApps, error al crear volúmenes y lista de apps vacía en la gestión de ExApps."
---
# Solución de problemas

## Resumen

Esta página reúne pasos habituales para diagnosticar problemas de AppAPI: de red, de despliegue de ExApps, el error al crear un volumen y la lista vacía de apps de la App Store. Está dirigida a quienes desarrollan o despliegan ExApps.

````{upstream} developer_manual/exapp_development/faq/Troubleshooting.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Esta sección describe pasos habituales para diagnosticar problemas concretos.

### ¿Cómo diagnosticar problemas de red?

Los problemas de red pueden no ser tan sencillos de identificar y resolver.
Estos son algunos pasos habituales para verificar la configuración de red:

- Verificar que el daemon de despliegue esté en ejecución y sea accesible (ajustes de administración de AppAPI - seleccionar el daemon de despliegue - comprobar la conexión).
- Verificar el modo de red y los niveles de acceso, el cortafuegos, la VPN, etc.
- Verificar que Nextcloud sea accesible desde el host del daemon de despliegue
- Verificar que el host del daemon de despliegue sea accesible desde el host de Nextcloud
- Verificar que Nextcloud sea accesible desde el contenedor de la ExApp
- Verificar que no haya problemas de resolución DNS
- Verificar que no haya problemas con los certificados SSL
- Si hay errores HTTP 401 Unauthorized, revisar los registros de la ExApp (`docker logs nc_app_<appid>`) / de Nextcloud para ver en qué ruta de la API falla la autenticación, e intentar volver a habilitar AppAPI y reinstalar la ExApp.

:::{note}
Si el caso no está documentado aquí ni existe en los issues de GitHub,
se invita a preguntar creando un issue en el [repositorio de AppAPI](https://github.com/nextcloud/app_api/issues).
:::

### Problemas de despliegue de ExApps

Las preguntas sobre problemas de despliegue se tratan en el apartado [Prueba de despliegue](https://docs.nextcloud.com/server/latest/admin_manual/exapps_management/TestDeploy.html) de la guía de administración.
En términos generales, hay tres pasos para encontrar el mensaje de error adecuado que permita entender el problema:

1. Revisar los registros de Nextcloud
2. Revisar los registros del contenedor de la ExApp (disponibles solo si el contenedor de la ExApp se ha creado y/o está en ejecución)
3. Revisar los registros del host del daemon de despliegue (`journalctl -u docker.service`)
4. Revisar los registros del Docker Socket Proxy (si se usa y si es necesario, p. ej., para comprobar errores SSL o 401)

### No se pudo crear el volumen

Si aparece el error «Failed to create volume», comprobar lo siguiente:

- Asegurarse de que haya suficiente espacio en disco en la máquina host.
- Revisar los registros del sistema de Docker mientras se reproduce el problema (`journalctl -u docker.service`).

### La lista de apps de la App Store en la gestión de ExApps está vacía

Este problema puede producirse si se carga la página de gestión de ExApps (o la de gestión de apps habitual)
con frecuencia en un período corto de tiempo, de modo que la protección de límite de solicitudes de la App Store puede bloquear la dirección IP.
Esperar un rato y volver a intentarlo.
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
