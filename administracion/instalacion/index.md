---
tipo: guia
esqueleto: borrador
audiencia: administracion
apps: [gestion]
resumen: "Los recorridos de instalación de un nodo de la suite según cada situación."
---
# Instalación

## Resumen

La instalación de un nodo depende de la situación y cada situación tiene su propio recorrido: la puesta en marcha de un CESFAM productivo sigue el instalador de la suite, el entorno de desarrollo sigue el inicio rápido del repositorio y el ciclo diario de contenedores se opera por la interfaz de tareas del repositorio. Las Notas de versión acompañan cada entrega y la Configuración inicial del establecimiento.

## Secciones previstas

- Instalación productiva
- Entorno de desarrollo
- Notas de versión
- Configuración inicial
- Ciclo de contenedores

````{upstream} admin_manual/installation/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

- {nc-doc}`admin_manual/installation/system_requirements`
- {nc-doc}`admin_manual/installation/deployment_recommendations`
- {nc-doc}`admin_manual/installation/php_configuration`
- {nc-doc}`admin_manual/installation/source_installation`
- {nc-doc}`admin_manual/installation/installation_wizard`
- {nc-doc}`admin_manual/installation/command_line_installation`
- {nc-doc}`admin_manual/installation/automatic_configuration`
- {nc-doc}`admin_manual/installation/selinux_configuration`
- {nc-doc}`admin_manual/installation/nginx`
- {nc-doc}`admin_manual/installation/harden_server`
- {nc-doc}`admin_manual/installation/server_tuning`
- {nc-doc}`admin_manual/installation/example_ubuntu`
- {nc-doc}`admin_manual/installation/example_centos`
- {nc-doc}`admin_manual/installation/example_openbsd`
- {nc-doc}`admin_manual/installation/uninstallation`
````

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
