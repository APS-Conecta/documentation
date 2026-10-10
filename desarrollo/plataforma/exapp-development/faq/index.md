---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Índice de las preguntas frecuentes de AppAPI: registro de contenedores, Docker Socket Proxy, GPU, escalado, proxy corporativo y solución de problemas."
---
# Preguntas frecuentes

## Resumen

Esta sección reúne las preguntas más comunes o problemáticas al trabajar con AppAPI: el registro de contenedores de Docker, el Docker Socket Proxy, el soporte de GPU, el escalado, el proxy corporativo y la solución de problemas. Está dirigida a quienes desarrollan o administran ExApps.

````{upstream} developer_manual/exapp_development/faq/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Esta sección contiene las preguntas más comunes o problemáticas
que usuarios o desarrolladores pueden encontrar al trabajar con AppAPI.
Puede servir como indicador hacia otras partes de la documentación, a las que suele remitir,
o dar una respuesta breve.

:::{note}
Esta sección se irá actualizando con el tiempo, a medida que surjan nuevas preguntas.
Si se tiene una pregunta que no figura aquí o la respuesta no resulta suficiente, se invita a
plantearla creando un issue en el [repositorio de AppAPI](https://github.com/nextcloud/app_api/issues).
:::

- {nc-doc}`developer_manual/exapp_development/faq/DockerContainerRegistry`
- {nc-doc}`developer_manual/exapp_development/faq/DockerSocketProxy`
- {nc-doc}`developer_manual/exapp_development/faq/GpuSupport`
- {nc-doc}`developer_manual/exapp_development/faq/Scaling`
- {nc-doc}`developer_manual/exapp_development/faq/BehindCompanyProxy`
- {nc-doc}`developer_manual/exapp_development/faq/Troubleshooting`
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
