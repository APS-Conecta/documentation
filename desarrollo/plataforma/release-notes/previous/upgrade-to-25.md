---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 25 para las apps: rango de info.xml, fin del soporte de SCSS, opción para desactivar atajos de teclado y paquete nextcloud/ocp."
---
# Actualización a Nextcloud 25

## Resumen

Esta página enumera los cambios de la versión 25 que afectan a las apps: el rango de versiones de `appinfo/info.xml`, el fin del soporte de los archivos scss de las apps, la opción global para desactivar los atajos de teclado, el reemplazo del paquete `christophwurst/nextcloud` por `nextcloud/ocp` y la API de colores SVG eliminada. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_25.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Los cambios críticos se recopilaron [en GitHub](https://github.com/nextcloud/server/issues/32117). Consultar el ticket original para ver los enlaces a las pull requests y a los tickets.
:::

### General

#### info.xml

Asegurarse de que el `appinfo/info.xml` de la app admita Nextcloud 25.

```xml
<dependencies>
  <nextcloud min-version="22" max-version="25" />
</dependencies>
```

#### Eliminación del soporte de SCSS

Con la 25 se eliminó el soporte de los archivos scss que aportan las apps.
Encargarse de la compilación propia, pasar a una app Vue o volver a css.
Ver [la issue #32060 de Github](https://github.com/nextcloud/server/issues/32060).

### Cambios de frontend

#### Atajos de teclado desactivados

Se añadió a los ajustes de accesibilidad una opción global para desactivar los atajos de teclado.
Como depende en gran medida del lector de pantalla y de las herramientas que se usen si está bien usar Ctrl y/o Alt u otras teclas,
y mantener una lista más detallada supone demasiado esfuerzo, se optó por un interruptor global de activación y desactivación. Las apps pueden usar
esta llamada a la API pública de JavaScript para determinar si el usuario eligió desactivarlos: `OCP.Accessibility.disableKeyboardShortcuts()`.
En ese caso, ninguna app debe registrar atajos adicionales. Solo se pueden usar `space` para alternar las casillas de verificación y
`enter` para enviar los botones o enlaces activos en ese momento.
Ver [la issue #34081 de Github](https://github.com/nextcloud/server/pull/34081) y la {nc-ref}`documentación de frontend de JavaScript <basics_frontend_javascript_keyboard_shortcuts>`.

### Cambios de backend

#### `christophwurst/nextcloud` reemplazado

El paquete de composer [christophwurst/nextcloud](https://packagist.org/packages/christophwurst/nextcloud) se reemplazó
por un paquete [nextcloud/ocp](https://packagist.org/packages/nextcloud/ocp), ahora propiedad de {vendor}`Nextcloud`. El contenido es
el mismo y se generaron todas las versiones anteriores, por lo que se puede hacer la transición de inmediato, sin importar qué versiones se admitan.

#### API eliminadas

- Se eliminó la API de colores SVG
````
