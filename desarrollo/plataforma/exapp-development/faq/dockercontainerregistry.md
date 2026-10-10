---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Registros de contenedores de Docker en AppAPI: no se admite la autenticación, por lo que las imágenes de las ExApps deben ser públicas."
---
# Registro de contenedores de Docker

## Resumen

Esta página responde si AppAPI puede usar un registro de contenedores de Docker privado con autenticación: no lo admite, y las imágenes de las ExApps deben estar disponibles públicamente. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/faq/DockerContainerRegistry.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

### ¿Cómo usar un registro de contenedores de Docker privado con autenticación?

Actualmente no se admite la autenticación en el registro de contenedores de Docker.
Las imágenes de las ExApps deben estar disponibles públicamente.
````
