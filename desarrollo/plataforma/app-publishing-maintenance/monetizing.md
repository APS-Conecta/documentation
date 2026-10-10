---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo recibir compensación económica por una app: enlaces de donación en info.xml y el botón de solicitud de presupuesto para soporte empresarial."
---
(nc-dev-app-store-monetizing)=
# Monetizar la app

## Resumen

Esta página explica cómo recibir una compensación económica por una app publicada en la tienda de apps: los enlaces de donación declarados en el archivo info.xml y el botón de solicitud de presupuesto para soporte empresarial. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/app_publishing_maintenance/monetizing.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La tienda de apps de {vendor}`Nextcloud` ofrece varias funciones que permiten a quienes desarrollan apps recibir alguna compensación económica por su trabajo.

### Donaciones

Quienes desarrollan apps pueden añadir enlaces o botones de donación opcionales que llevan a URL configurables.
Esto puede hacerse añadiendo una o más etiquetas de donación en el archivo `info.xml` de la app:

```
<donation title="Donate to the developers with PayPal" type="paypal">https://paypal.com/example</donation>
<donation type="stripe">https://stripe.com/example</donation>
<donation>https://other.service.com/example</donation>
```

Los tipos admitidos actualmente son `paypal` y `stripe`.
Indicar un tipo muestra el logotipo del servicio correspondiente junto al enlace de donación (o un logotipo genérico si el tipo no se especifica o se establece en `other`).
Si no se especifica el título de un enlace o botón, se usa por defecto `Donate to support this app`.
Estos botones aparecen en la tienda de apps y en los ajustes de las apps, y al hacer clic en ellos sus enlaces se abren en una nueva pestaña del navegador.

:::{note}
Todas las donaciones recibidas van directamente a quienes desarrollan la app. {vendor}`Nextcloud` no se queda con ninguna comisión.
:::

### Soporte empresarial

Quienes desarrollan apps también pueden añadir un botón opcional `Request quote`, que se muestra en la tienda de apps y en los ajustes de las apps.
Este botón lleva al [formulario de ventas de Nextcloud](https://nextcloud.com/get-a-quote/), donde puede solicitarse soporte empresarial para la app.
Si {vendor}`Nextcloud` recibe una solicitud interesante, el equipo de ventas se pondrá en contacto con quienes desarrollan la app para hablar de una colaboración para dar soporte de forma conjunta (de manera similar a otras apps, como Collabora y OnlyOffice).
El soporte empresarial está dirigido a instalaciones de Nextcloud más grandes, de 100 usuarios o más.

Para activar o desactivar el botón, ir a la página «Enterprise support» de los ajustes de la cuenta de la tienda de apps y hacer clic en «Mark as supported/unsupported», según corresponda, junto a las apps deseadas.
````
