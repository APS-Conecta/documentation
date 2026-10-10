---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo habilitar el soporte de GPU en el daemon de despliegue de AppAPI, qué requiere en el host y por qué no se puede limitar el número de GPU por ExApp."
---
# Soporte de GPU

## Resumen

Esta página explica cómo habilitar el soporte de GPU al registrar un daemon de despliegue de AppAPI, qué kits de herramientas de Docker requiere el host y por qué no es posible limitar el número de GPU por ExApp. Está dirigida a quienes desarrollan o despliegan ExApps.

````{upstream} developer_manual/exapp_development/faq/GpuSupport.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

### ¿Cómo habilitar el soporte de GPU para el daemon de despliegue?

Para habilitar el soporte de GPU, hay que especificar el dispositivo de cómputo GPU al registrar la configuración del daemon de despliegue.

De este modo, de forma predeterminada, AppAPI creará los contenedores de las ExApps solicitando a Docker Engine que conecte todos los dispositivos GPU disponibles.
Esto también implica que la ExApp concreta admita internamente el trabajo con GPU
y que los kits de herramientas de runtime de Docker necesarios estén instalados en el host del daemon de despliegue:

- Para NVIDIA, consultar la [documentación de configuración de Docker de NVIDIA](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).
- Para AMD, consultar la [documentación de configuración de Docker de ROCm](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/docker.html).

:::{note}
Si surge algún problema con el soporte de GPU, este depende en gran medida del dispositivo GPU concreto,
de las bibliotecas de software y, por tanto, del soporte de las ExApps para distinto hardware, o de otros factores.
Se invita a pedir ayuda creando un issue.
:::

### ¿Cómo limitar el número de GPU por ExApp?

Actualmente no existe esa opción de configuración.
AppAPI conecta todos los dispositivos GPU disponibles a cada contenedor de ExApp del mismo daemon de despliegue.
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
