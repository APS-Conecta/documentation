---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Cómo se actualiza el cliente de escritorio en Windows, macOS y Linux, y cómo deshabilitar las actualizaciones automáticas en cada sistema."
---
# El actualizador automático

## Resumen

Esta página describe cómo el cliente de escritorio comprueba e instala sus actualizaciones en Windows, macOS y Linux, y cómo impedir las actualizaciones automáticas. Está dirigida a usuarios del cliente y a quienes administran equipos Windows o Linux.

````{upstream} user_manual/desktop/autoupdate.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El actualizador automático garantiza disponer siempre de las últimas funciones y correcciones de errores del cliente de sincronización de {vendor}`Nextcloud`.

El actualizador automático solo actualiza en equipos macOS y Windows; los usuarios de Linux solo necesitan usar sus gestores de paquetes habituales. Sin embargo, en sistemas Linux el actualizador comprueba si hay actualizaciones y avisa cuando hay una nueva versión disponible.

### Flujo de trabajo básico

Las siguientes secciones describen cómo usar el actualizador automático en los distintos sistemas operativos.

#### Windows

El cliente de {vendor}`Nextcloud` comprueba si hay actualizaciones y las descarga cuando están disponibles. El estado de las actualizaciones puede consultarse en `Settings -> General -> Updates` en el cliente de {vendor}`Nextcloud`.

Si hay una actualización disponible y se ha descargado correctamente, el cliente de {vendor}`Nextcloud` inicia una actualización silenciosa antes de su siguiente arranque y luego se reinicia. Si la actualización silenciosa falla, el cliente ofrece una descarga manual.

:::{note}
Se requieren privilegios de administrador para realizar la actualización.
:::

#### macOS

El cliente para macOS tiene un actualizador automático que usa el framework Sparkle. Este actualizador automático va incluido en el App Bundle del cliente, comprueba si hay actualizaciones al iniciarse y avisa si hay una actualización disponible. Esto muestra una ventana emergente que permite descargar e instalar automáticamente la última actualización del cliente con un solo clic.

En las versiones del cliente que no incluyen el actualizador automático basado en Sparkle, aparece una notificación en la que se puede hacer clic, que informa de que hay una actualización disponible. Al hacer clic en dicha notificación, se abre en el navegador web del sistema la página de descarga de la última versión del cliente.

Al igual que en otros sistemas, el estado de las actualizaciones puede consultarse en `Settings -> General -> Updates` en el cliente de {vendor}`Nextcloud`.

#### Linux

Las distribuciones Linux ofrecen sus propias herramientas de actualización, por lo que los clientes de {vendor}`Nextcloud` que usan el sistema operativo Linux no realizan ninguna actualización por sí mismos. El cliente informa (`Settings -> General -> Updates`) cuando hay una actualización disponible.

### Impedir las actualizaciones automáticas

En entornos controlados, como empresas o universidades, puede no ser deseable habilitar el mecanismo de actualización automática, ya que interfiere con las herramientas y políticas de despliegue controlado. Para este caso, es posible deshabilitar por completo el actualizador automático. Las siguientes secciones describen cómo deshabilitar el mecanismo de actualización automática en los distintos sistemas operativos.

#### Impedir las actualizaciones automáticas en entornos Windows

Los usuarios pueden deshabilitar las actualizaciones automáticas añadiendo esta línea a la sección [General] de sus archivos `nextcloud.cfg`:

```
skipUpdateCheck=true
```

Los administradores de Windows tienen más opciones para impedir las actualizaciones automáticas en entornos Windows, mediante uno de dos métodos. El primer método permite a los usuarios anular el mecanismo de comprobación automática de actualizaciones, mientras que el segundo impide cualquier anulación manual.

Para impedir las actualizaciones automáticas, pero permitir anulaciones manuales:

1. Editar esta clave del Registro:

   `HKEY_LOCAL_MACHINE\Software\Nextcloud GmbH\Nextcloud`

2. Añadir la clave `skipUpdateCheck` (de tipo DWORD).

3. Especificar el valor `1` para la máquina.

Para anular manualmente esta clave, usar el mismo valor en `HKEY_CURRENT_USER`.

Para impedir las actualizaciones automáticas y no permitir anulaciones manuales:

:::{note}
Este es el método preferido para controlar el comportamiento del actualizador mediante directivas de grupo.
:::

1. Editar esta clave del Registro:

   `HKEY_LOCAL_MACHINE\Software\Policies\Nextcloud GmbH\Nextcloud`

2. Añadir la clave `skipUpdateCheck` (de tipo DWORD).

3. Especificar el valor `1` para la máquina.

:::{note}
Los clientes con marca propia usan, en lugar de `Nextcloud GmbH\Nextcloud`, una clave distinta que coincide con el proveedor y el nombre de la aplicación con marca.
:::

#### Impedir las actualizaciones automáticas en entornos Linux

Como el cliente para Linux no ofrece la función de actualización automática, no es necesario eliminar la comprobación automática de actualizaciones. Sin embargo, para deshabilitarla, editar el archivo de configuración del cliente de escritorio, `$HOME/.config/Nextcloud/nextcloud.cfg`. Añadir esta línea a la sección [General]:

```
skipUpdateCheck=true
```
````
