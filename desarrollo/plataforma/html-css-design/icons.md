---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Iconos para apps: la lista de iconos de core/img/ y la API de color SVG están obsoletas desde la versión 25; en su lugar, iconos de Material Design."
---
(nc-dev-icons)=
# Iconos

## Resumen

Esta página indica que los iconos de la carpeta core/img/ del servidor y la API de color SVG están obsoletos desde la versión 25, y remite a los iconos de Material Design en su lugar. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/html_css_design/icons.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Lista de iconos disponibles

:::{deprecated} 25
:::

Los iconos disponibles en la carpeta core/img/ del servidor están obsoletos. Pueden usarse por cuenta y riesgo propios.
Debido a un cambio en la forma en que ahora se genera la lista en el servidor, ya no puede convertirse automáticamente en documentación.

Usar en su lugar los [iconos de Material Design](#icons-material-design-icons).

(nc-dev-svgcolorapi)=
### API de color SVG

:::{deprecated} 25
:::

La API de svg ya no se admite por motivos de rendimiento.

Usar en su lugar los [iconos de Material Design](#icons-material-design-icons).

(icons-material-design-icons)=
### Iconos de Material Design

Si se necesitan más iconos que los predeterminados que se incluyen, usar los material-design-icons sería una buena idea.
Para usarlos con vuejs, consultar aquí: <https://nextcloud-vue-components.netlify.app/#/Components/NcIconSvgWrapper>
````
