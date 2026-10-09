---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Principios de diseño comunes a todas las apps: simplicidad, accesibilidad, software que funciona y no estorba, cuidado de los datos y pruebas de usabilidad."
---
(nc-dev-navigation)=
# Introducción

## Resumen

Esta página presenta los estándares de diseño y de marca que mantienen la identidad de las apps y los principios básicos con que se construyen: simplicidad, accesibilidad, funcionamiento sin configuración, respeto por los datos de las personas, estado claro y pruebas de usabilidad. Está dirigida a quienes crean o contribuyen a una app.

````{upstream} developer_manual/design/introduction.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los estándares de diseño y de marca de {vendor}`Nextcloud` se usan para mantener la identidad de las apps de Nextcloud.
Para quien desarrolla y quiere crear una app de Nextcloud o contribuir a una, seguir esta guía asegura que la app parezca formar parte de la familia de Nextcloud.

Cada app de Nextcloud es única y distinta, pero hay un par de estándares que se usan en todas.
Todas las apps de Nextcloud se construyen teniendo en cuenta algunos principios básicos.

- El software debe ser rápido y fácil de usar. Mostrar solo los elementos más importantes. Los elementos secundarios pueden mostrarse al pasar el cursor o mediante una función «Avanzado».
- Las apps de Nextcloud se construyen para todo el mundo. Usar un tono cercano con frases sencillas. Asegurarse de que la app sea adaptable y funcione en todos los navegadores y dispositivos.
- Accesibilidad: probar la accesibilidad con regularidad, por ejemplo con [Lighthouse](https://developers.google.com/web/tools/lighthouse), [WAVE](https://wave.webaim.org/) y [Google Accessibility Scanner](https://play.google.com/store/apps/details?id=com.google.android.apps.accessibility.auditor). Apuntar al nivel AA de las WCAG. Se puede obtener más información sobre los estándares de accesibilidad en el [sitio web del W3](https://www.w3.org/WAI/standards-guidelines/wcag/glance/)
- El software debe funcionar.
  Incorporar funciones a la rama principal solo cuando estén completas. Es mejor no tener una función que tener una que funcione mal.
- El software no debe estorbar.
  Hacer las cosas automáticamente en lugar de ofrecer opciones de configuración. Cuando alguien pida un ajuste, averiguar cuál es la raíz del problema y corregir eso en su lugar.
  Leer también [Elegir nuestras preferencias](http://ometer.com/preferences.html).
- Los datos de las personas son sagrados. Ofrecer la posibilidad de deshacer la mayoría de las operaciones y, opcionalmente, una confirmación para las operaciones más grandes y complejas, pero con cuidado con las confirmaciones, [ya que pueden descartarse](http://www.alistapart.com/articles/neveruseawarning/).
- El estado de la aplicación debe ser claro. Si algo se está cargando, proporcionar retroalimentación. Las reacciones deben ser rápidas, idealmente de menos de 100 ms, según los [límites del tiempo de respuesta](https://www.nngroup.com/articles/response-times-3-important-limits/).
- El estado de la aplicación debe ser claro. Si algo se está cargando, proporcionar retroalimentación.
- Restablecer la instalación con regularidad para ver cómo es la experiencia de la primera ejecución, y mejorarla.
- Idealmente, hacer [pruebas de usabilidad](http://jancborchardt.net/usability-in-free-software) para saber cómo usa la gente el software. Hacer pruebas con 5 personas basta para identificar la mayoría de los problemas.

Para conocer más principios de experiencia de usuario, leer a [Alex Faaborg, de Mozilla](http://uxmag.com/articles/quantifying-usability), y las [Pautas de interfaz humana de GNOME](https://developer.gnome.org/hig/stable/design-principles.html.en)
````
