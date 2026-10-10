---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Qué ofrece la app de tematización a quienes desarrollan apps: variables CSS, el objeto JavaScript OCA.Theming y los iconos generados."
---
# Soporte de tematización

## Resumen

Esta página describe las herramientas de la app de tematización para que una app se ajuste al aspecto tematizado: las variables CSS, el objeto JavaScript `OCA.Theming` y la generación automática de iconos. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/front-end/theming.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La app de tematización de Nextcloud ofrece algunas herramientas a quienes desarrollan apps para garantizar que las apps también se ajusten al aspecto tematizado.

### Variables CSS

Hay muchas variables CSS disponibles; consultar {nc-ref}`cssvars`.

### JavaScript

Cuando la app de tematización está activada, proporciona el objeto **OCA.Theming**. Se puede usar para tratar de forma distinta las instancias tematizadas.

```javascript
if(OCA.Theming) {
  $('.myapp-element').animate({backgroundColor:OCA.Theming.color});
}
```

Está disponible la siguiente información:

- **OCA.Theming.color** Color principal
- **OCA.Theming.inverted** Será true con colores de tematización claros, para obtener contraste con el texto
- **OCA.Theming.name** Nombre de la instancia
- **OCA.Theming.slogan** Eslogan de la instancia
- **OCA.Theming.url** Dirección web de la instancia

### Iconos

La app de tematización generará automáticamente favicons e iconos de pantalla de inicio para cada app a partir del icono *img/app.svg* que hay dentro de la carpeta de la app. Cualquier favicon personalizado que defina una app solo será visible cuando la app de tematización esté desactivada.
````
