---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Dónde informar de un error según el componente afectado: servidor, cliente de escritorio, clientes de Android e iOS o una app."
---
# Gestor de errores

## Resumen

Esta página indica en qué repositorio de {vendor}`Nextcloud` se informa de un error según el componente afectado: el servidor, el cliente de escritorio, los clientes de Android e iOS o una app. Está dirigida a quienes desarrollan sobre la plataforma.

````{upstream} developer_manual/prologue/bugtracker/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Gracias por ayudar a {vendor}`Nextcloud` informando de errores. Antes de enviar una incidencia, leer primero las [pautas para el envío de incidencias][Issue submission guidelines].

- Si el problema está en el servidor de Nextcloud, informar de él en el [repositorio del servidor][Server repository]
- Si el problema está en el cliente de escritorio de {vendor}`Nextcloud`, informar de él en el [repositorio del cliente de escritorio][Desktop repository]
- Si el problema está en el cliente de Android de {vendor}`Nextcloud`, informar de él en el [repositorio de Android][Android repository]
- Si el problema está en el cliente de iOS de {vendor}`Nextcloud`, informar de él en el [repositorio de iOS][iOS repository]
- Si el problema está en una app de Nextcloud, informar de él donde se desarrolla esa app. Consultar la página de la [tienda de apps][App Store] para ver los enlaces relacionados.
- Si la app figura en nuestra [organización principal de GitHub][main GitHub organization], informar del problema en el subrepositorio correcto

[Issue submission guidelines]: https://github.com/nextcloud/server/blob/master/.github/CONTRIBUTING.md#submitting-issues
[Server repository]: https://github.com/nextcloud/server/issues
[Desktop repository]: https://github.com/nextcloud/desktop/issues
[Android repository]: https://github.com/nextcloud/android/issues
[iOS repository]: https://github.com/nextcloud/ios/issues
[App Store]: https://apps.nextcloud.com/
[main GitHub organization]: https://github.com/nextcloud
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
