---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Comando occ que desactiva los flujos de usuario para que los usuarios no definan sus propias reglas de flujo."
---
# Configuración de Flujo

## Resumen

Esta página muestra el comando `occ` que desactiva los flujos de usuario, para quienes administran el servidor y prefieren que los usuarios no definan sus propias reglas de flujo.

````{upstream} admin_manual/file_workflows/configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los administradores pueden desactivar los flujos de usuario, ya que pueden afectar al rendimiento del sistema y es posible que no se quiera dar a los usuarios la posibilidad de definir sus propias reglas de flujo. Se pueden desactivar con el siguiente comando:

```
occ config:app:set workflowengine user_scope_disabled --value yes
```
````
