---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "El sistema de gestión de referencias: vistas previas de enlaces y selector inteligente, que las apps amplían, y qué proveedores ponen a disposición."
---
# Gestión de referencias

## Resumen

Esta sección explica, para quienes administran el servidor, el sistema de gestión de referencias de la plataforma base: sus dos funciones, las vistas previas de enlaces y el selector inteligente, cómo las apps las amplían y cómo la elección de apps decide qué proveedores quedan disponibles.

````{upstream} admin_manual/reference/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El sistema de gestión de referencias aporta 2 funciones a Nextcloud:

- {nc-doc}`Las vistas previas de enlaces <admin_manual/reference/link_previews>` (también llamadas widgets de referencia)
- {nc-doc}`El selector inteligente <admin_manual/reference/smart_picker>`

Ambas funciones son genéricas y las apps de Nextcloud deben ampliarlas.

Las apps pueden añadir compatibilidad con algunos enlaces HTTP para que se muestren vistas previas en distintos lugares, como los documentos de Text y los mensajes de Talk.

El selector inteligente es un componente del frontend que permite a los usuarios buscar o generar enlaces o texto.

Las apps pueden registrar proveedores del selector inteligente para ampliar sus capacidades.
Los administradores pueden elegir qué proveedores del selector inteligente quieren poner a disposición de los usuarios eligiendo qué apps instalan.
**Ninguno** de los proveedores del selector inteligente incluidos en las apps recomendadas envía datos a servicios de terceros.
Algunos proveedores del selector inteligente de apps de la comunidad pueden depender de servicios de terceros.

- {nc-doc}`admin_manual/reference/link_previews`
- {nc-doc}`admin_manual/reference/smart_picker`
````

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
