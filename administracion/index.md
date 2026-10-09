---
tipo: explicacion
audiencia: administracion
apps: []
resumen: "Operación de una instalación de la suite: instalación, aprovisionamiento, oficina, mapas base, seguridad y mantenimiento."
---
# Administración

Introducción a la operación de una instalación de la suite, para quienes administran la infraestructura sanitaria municipal. La plataforma es una distribución derivada de Nextcloud operada como configuración declarativa: imágenes oficiales sin bifurcaciones del núcleo, un único escritor del estado deseado y convergencia aditiva. Esta guía cubre la instalación, el aprovisionamiento de usuarios, grupos y Apps, la oficina, los mapas base, la seguridad y el mantenimiento diario.

````{upstream} admin_manual/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
**Bienvenido a la Guía de administración de Nextcloud Server.**

Esta guía explica cómo realizar tareas de administración en Nextcloud, una plataforma de código abierto muy versátil y escalable para la sincronización de archivos y la colaboración en contenidos.

Con más de 400 000 despliegues, {vendor}`Nextcloud` puede ejecutarse en una sencilla Raspberry Pi para dos usuarios o escalar hasta dar servicio a instalaciones globales y distribuidas con decenas de millones de usuarios. Puede desplegarse en las instalaciones propias, en nubes privadas o públicas, o en entornos híbridos. Con el respaldo de una comunidad amplia y en crecimiento, {vendor}`Nextcloud` está disponible en más de 60 idiomas.

Las ediciones más recientes de los manuales de {vendor}`Nextcloud` están siempre disponibles en línea en [docs.nextcloud.com](https://docs.nextcloud.com/).

## Público destinatario

Esta guía está dirigida a usuarios que quieren:

- Instalar Nextcloud Server
- Administrar y gestionar su instancia
- Optimizar el rendimiento del servidor

Para la documentación sobre los clientes web, de escritorio o móviles de Nextcloud, consultar:

- [Manual de usuario de {vendor}`Nextcloud`][Nextcloud User Manual]
- [Cliente de escritorio de {vendor}`Nextcloud`][Nextcloud Desktop Client]

Para la documentación sobre temas de desarrollo, consultar:

- Los repositorios individuales en GitHub dentro de [la organización @nextcloud](https://github.com/nextcloud/)
- [Manual de desarrollo de {vendor}`Nextcloud`](https://docs.nextcloud.com/server/latest/developer_manual/)

## Componentes principales

Nextcloud incluye:

- Nextcloud Server (backend que se ejecuta en Linux)
- Un cliente web adaptable e integrado
- Clientes de escritorio multiplataforma (Windows, macOS y Linux) para la sincronización de archivos y el acceso local
- Clientes móviles dedicados (Android e iOS)
- Un amplio ecosistema de apps para ampliar la funcionalidad

## Ediciones

Nextcloud Server está disponible en dos ediciones:

- **Community:** con soporte de la comunidad (ayuda entre pares), 100 % gratuita.
- **Enterprise:** con soporte de los desarrolladores principales o de socios autorizados, empaquetado oficial, amplia documentación específica para empresas y opciones de soporte.

*Ambas ediciones incluyen toda la funcionalidad y todo el código fuente.*

Las ediciones Enterprise pueden incluir orientación para el despliegue, acceso por teléfono y correo electrónico a los desarrolladores de {vendor}`Nextcloud`, soporte oficial para integraciones y complementos, marca personalizada y ciclos de soporte extendidos, entre otras ventajas.

Esta guía se centra principalmente en la edición Community, pero la información se aplica a ambas ediciones.

## Más recursos

- Videotutoriales, presentaciones generales y ponencias de conferencias: [canal de YouTube de {vendor}`Nextcloud`](https://www.youtube.com/c/Nextcloud).
- Últimas noticias y novedades: [blog de Nextcloud](https://nextcloud.com/news/).
- Soporte de la comunidad: [foro de ayuda de {vendor}`Nextcloud`](https://help.nextcloud.com/).
- Soporte comercial: [Nextcloud GmbH](https://nextcloud.com/).
- Documentación: [documentación de {vendor}`Nextcloud`](https://docs.nextcloud.com/).

## Primeros pasos

Para empezar, consultar la sección Instalación.

:::{admonition} ¿Quién desarrolla {vendor}`Nextcloud`?
El desarrollo de la plataforma {vendor}`Nextcloud` es un esfuerzo cooperativo supervisado por los mantenedores principales —en su mayoría empleados de Nextcloud GmbH— junto con miles de socios, proveedores, colaboradores, miembros del proyecto y participantes de la comunidad.

La comunidad de {vendor}`Nextcloud` incluye a todo el mundo: desde usuarios individuales y desarrolladores independientes hasta grandes organizaciones.

Los miembros de la comunidad comparten y comentan a diario sus experiencias con la plataforma. Sugieren mejoras, colaboran en el diseño, escriben código, crean documentación, hacen pruebas en busca de errores, clasifican informes de errores e ideas de mejora, ayudan a otras personas, mejoran las traducciones y ayudan a financiar y organizar la logística de un proyecto de este tamaño. Y, lo más importante, usan {vendor}`Nextcloud` en su vida diaria y en su trabajo.
:::

[Nextcloud User Manual]: https://docs.nextcloud.com/server/latest/user_manual/en/
[Nextcloud Desktop Client]: https://docs.nextcloud.com/desktop/latest/
````

```{toctree}
:maxdepth: 1
:glob:

Instalación <instalacion/index>
AIO <aio>
Arquitectura <arquitectura>
Aprovisionamiento <aprovisionamiento>
Usuarios y grupos <usuarios-y-grupos/index>
Oficina <oficina/index>
Mapas base <mapas-base>
Seguridad <seguridad>
Operaciones <operaciones/index>
*
*/index
```

[Aviso legal](../aviso.md)
