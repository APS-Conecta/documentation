---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Personalizar la apariencia de Nextcloud con la app theming: nombre, colores, logo y fondos, configuración con occ, iconos y enlaces a apps móviles de marca."
---
# Personalización del tema

## Resumen

Esta página explica, para quienes administran el servidor, cómo personalizar la apariencia de la instancia con la app `theming`, desde la interfaz o con `occ theming:config`, qué requiere la generación automática de iconos y cómo cambiar los enlaces a las apps móviles.

````{upstream} admin_manual/configuration_server/theming.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La función de temas permite personalizar la apariencia de la instancia de Nextcloud para que se ajuste al diseño de la organización (o, si es para uso personal, al estilo propio). Pueden sustituirse el logo y las imágenes de fondo de Nextcloud por recursos propios, personalizar colores y eslóganes, y añadir enlaces específicos al aviso legal y a la política de privacidad.

La personalización del tema la aporta la app `theming`, incluida y siempre activada. Usar la sección {guilabel}`Tema` del menú {guilabel}`Configuraciones de administración` para acceder a todos los ajustes relacionados con el tema.

### Personalizar la apariencia de Nextcloud

Pueden cambiarse los siguientes aspectos de la apariencia de la instancia:

- {guilabel}`Nombre` (p. ej., ACME Inc. Cloud).
- {guilabel}`Enlace web` (p. ej., <https://acme.inc/>).
- {guilabel}`Eslogan`.
- {guilabel}`Color primario`: se usa en los botones importantes, las casillas de verificación y los iconos de carpeta.
- {guilabel}`Color de fondo`: se usa cuando no hay ninguna imagen establecida; el color de los iconos de la barra de cabecera también se deriva de él.
- {guilabel}`Logo`: aparece en la cabecera y en la página de inicio de sesión (tamaño predeterminado: 62x34 px).
- {guilabel}`Imágen de fondo y de inicio de sesión`: establece el fondo de la página.

* **Enlaces legales adicionales**: aviso legal y política de privacidad.
* **Logo de cabecera y favicon personalizados**: opcionalmente, sustituir el favicon generado automáticamente a partir del logo.
* {guilabel}`Deshabilitar tematización de usuario`: impide que los usuarios cambien los fondos y los colores. Activarlo para imponer el tema personalizado.

### Configurar el tema mediante la CLI

El tema también puede configurarse con el comando `occ theming:config`.

Entre los ajustes disponibles están:

- *name*, *url*, *imprintUrl*, *privacyUrl*, *slogan*, *background_color*, *primary_color*.
  Ejemplo: `occ theming:config name "My Example Cloud"`
- *background*, *logo*, *favicon*, *logoheader*.
  Ejemplo: `occ theming:config logo /tmp/mylogo.png`
- *disable-user-theming* (yes/no).
  Ejemplo: `occ theming:config disable-user-theming yes`

:::{note}
Las imágenes deben leerse de un archivo local del servidor Nextcloud.
:::

Para usar un color (en lugar de una imagen) como fondo:

```
occ theming:config background_color "#0082c9"
occ theming:config background backgroundColor
```

### Tematización de iconos

A partir de los ajustes, Nextcloud generará automáticamente los favicons y un logo de cabecera con el logo y el color del tema.

Esto requiere:

- El módulo PHP `imagick`.
- Compatibilidad con SVG en imagick (p. ej., `libmagickcore-7.q16-10-extra` en Debian 13 y `libmagickcore-6.q16-7-extra` en Ubuntu 24.04).

:::{tip}
En las opciones avanzadas de la app de temas puede establecerse un favicon personalizado si no se quieren usar los recursos generados automáticamente ni instalar las dependencias anteriores.
:::

### Clientes de marca

:::{note}
Nextcloud GmbH (la empresa que emplea a los mantenedores principales de {vendor}`Nextcloud`) ofrece servicios de personalización de marca, con clientes de sincronización (móviles y de escritorio) que usan la identidad corporativa propia y vienen preconfigurados para los usuarios. Para más información sobre las ofertas de personalización de marca avanzada y de soporte empresarial, [contactar con Nextcloud GmbH](https://nextcloud.com/enterprise/).
:::

La app de temas permite cambiar las URL de las apps móviles (Android e iOS) que aparecen cuando los usuarios acceden a la interfaz web desde dispositivos móviles. De forma predeterminada, estos enlaces apuntan a las apps oficiales de {vendor}`Nextcloud`, pero pueden establecerse versiones de marca propia.

Establecer enlaces de apps personalizados con el comando `occ`:

```
occ config:app:set theming AndroidClientUrl --value "https://play.google.com/store/apps/details?id=com.nextcloud.client"
occ config:app:set theming iTunesAppId --value "1125420102"
occ config:app:set theming iOSClientUrl --value "https://itunes.apple.com/us/app/nextcloud/id1125420102?mt=8"
```
````
