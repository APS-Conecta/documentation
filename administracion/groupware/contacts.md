---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Backend CardDAV: libreta de direcciones del sistema y su privacidad, elementos compartidos, límites de frecuencia, contacto de ejemplo y retención de datos."
---
# Contactos / CardDAV

## Resumen

Esta página describe el backend CardDAV del servidor: cómo activar o desactivar la libreta de direcciones del sistema y qué contactos muestra según los ámbitos del perfil, los elementos compartidos, los límites de frecuencia, el contacto de ejemplo y la retención de tokens de sincronización. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/groupware/contacts.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud incluye un backend de CardDAV para que los usuarios almacenen y compartan sus libretas de direcciones y sus contactos.

(nc-system-address-book)=
### Libreta de direcciones del sistema

:::{versionchanged} 27.0.0
La libreta de direcciones del sistema ahora es accesible para todos los usuarios de Nextcloud
:::

Nextcloud mantiene una libreta de direcciones de solo lectura que contiene la información de contacto de todos los usuarios de la instancia.

Los usuarios deshabilitados se eliminan de esta libreta de direcciones.

El acceso a la libreta de direcciones del sistema puede desactivarse o activarse desde la interfaz de administración o con un comando de línea de comandos.

Tener en cuenta que esto no influye en el {nc-ref}`uso compartido federado <label-direct-share-link>`.

#### Línea de comandos

Ejecutar `occ config:app:set dav system_addressbook_exposed --value="no"` para desactivar el acceso a la libreta de direcciones del sistema para todos los usuarios.

#### Interfaz de administración

Ir a *Configuraciones de administración* → *Groupware* → sección *Libreta de Direcciones del Sistema* y activar o desactivar la opción *Habilitar la Libreta de Direcciones del Sistema*.

:::{warning}
Si ya hay clientes conectados al endpoint de CalDAV, esos clientes podrían tener problemas de sincronización después de desactivar el acceso a la libreta de direcciones del sistema. A menudo puede remediarse eligiendo otra libreta de direcciones predeterminada en el cliente y forzando una nueva sincronización.
:::

#### Privacidad y ámbitos de las propiedades del usuario

La información de contacto de la libreta de direcciones del sistema se toma de la {nc-ref}`información del perfil <profile>` de los usuarios. Las propiedades del perfil solo se escriben en el contacto del sistema si el {nc-ref}`ámbito <profile-property-scopes>` está establecido en *Local* o superior.

Los usuarios que establecen todos los ámbitos de sus propiedades en *Privado* se eliminan de la libreta de direcciones del sistema y, por tanto, otros usuarios no los ven.

Los {nc-ref}`ajustes de uso compartido de archivos <file-sharing-configuration>` controlan la enumeración de otros usuarios.

- Si no se permite el autocompletado de nombres de usuario, la libreta de direcciones del sistema solo mostrará el propio contacto del sistema del usuario, sin ningún otro contacto.
- Si se permite el autocompletado de nombres de usuario, los usuarios verán las tarjetas de contacto de todos los demás usuarios.

  - Si el autocompletado se limita a usuarios de los mismos grupos, los usuarios verán las tarjetas de contacto de otros usuarios de los grupos compartidos.
  - Si el autocompletado se limita a números de teléfono coincidentes, la libreta de direcciones del sistema solo mostrará el propio contacto del sistema del usuario, sin ningún otro contacto.
  - Si el autocompletado se limita a usuarios de los mismos grupos **y** a números de teléfono coincidentes, los usuarios verán las tarjetas de contacto de otros usuarios de los grupos compartidos.

#### Sincronización de la libreta de direcciones

La libreta de direcciones se actualiza automáticamente con cada usuario añadido, modificado, deshabilitado o eliminado. La administración también puede lanzar una reescritura completa de la libreta de direcciones {nc-ref}`con occ <dav-sync-system-address-book>`.

### Elementos compartidos

:::{versionadded} 5.5.0 Nextcloud 25 o posterior
:::

Para esta función debe estar activada la [app de recursos relacionados](https://apps.nextcloud.com/apps/related_resources), que viene incluida.

### Límites de frecuencia

Nextcloud limita la creación de libretas de direcciones y cuántas pueden crearse en un periodo corto de tiempo. El valor predeterminado es de 10 libretas de direcciones por hora. Puede personalizarse de la siguiente manera:

```
# Set limit to 15 items per 30 minutes
sudo -E -u www-data php occ config:app:set dav rateLimitAddressBookCreation --type=integer --value=15
sudo -E -u www-data php occ config:app:set dav rateLimitPeriodAddressBookCreation --type=integer --value=1800
```

Además, el número máximo de libretas de direcciones que un usuario puede crear está limitado a 10 elementos. Esto también puede personalizarse:

```
# Allow users to create 50 addressbooks
sudo -E -u www-data php occ config:app:set dav maximumAdressbooks --type=integer --value=50
```

o bien:

```
# Allow users to create address books without restriction
sudo -E -u www-data php occ config:app:set dav maximumAdressbooks --type=integer --value=-1
```

### Contacto de ejemplo

:::{versionadded} 32.0.0
:::

Cuando un usuario inicia sesión por primera vez, se crea un contacto de ejemplo en su libreta de direcciones.

Esta función está activada de forma predeterminada y la controla la configuración de app `enableDefaultContact`.

Para desactivar la función de contacto de ejemplo:

1. Ir a los ajustes de Groupware en las configuraciones de administración.
2. Desplazarse hasta la sección «Contenido de ejemplo».
3. Desactivar el ajuste «Add example contact ...» con la casilla de verificación

También puede activarse o desactivarse desde la línea de comandos:

```
sudo -E -u www-data php occ config:app:set dav enableDefaultContact --value=no
```

Si se desea establecer un contacto concreto que deba crearse.

4. Pulsar el botón «Importar contacto».
5. Elegir un archivo vCard (.vcf) que deba importarse como contacto de ejemplo.

Es posible volver al contacto de ejemplo predeterminado que proporciona nextcloud pulsando el botón «Restablecer a predeterminado», junto al botón de importación.

(nc-carddav-data-retention)=
### Retención de datos

:::{versionadded} 26.0.0
:::

Se puede configurar durante cuánto tiempo conserva Nextcloud algunos de los tokens de sincronización de los contactos.

#### Tokens de sincronización

El backend de CardDAV registra cualquier modificación de las libretas de direcciones, es decir, todo lo que se añade, modifica o elimina. Estos datos se usan para la sincronización diferencial de clientes sin conexión como Thunderbird. A partir de cierto momento, los datos pueden considerarse obsoletos, suponiendo que ya no habrá ningún cliente que los necesite. Esto puede ayudar a mantener pequeña la tabla de base de datos *addressbookchanges*:

```
sudo -E -u www-data php occ config:app:set totalNumberOfSyncTokensToKeep --value=30000
```

El valor predeterminado es conservar 10 000 entradas. Esta opción debe ajustarse de forma adecuada al número de usuarios. P. ej., en una instalación con 5000 libretas de direcciones sincronizadas activas, el sistema solo conservaría una media de 10 cambios por sincronización. Esto provocará una eliminación prematura de datos y problemas de sincronización.

:::{warning}
Este ajuste también influye en la {nc-ref}`retención de datos de CalDAV <caldav-data-retention>`.
:::
````
