---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Activar, desactivar, actualizar y restringir apps desde la página de apps o con occ; directorios de apps propios y tienda de apps autoalojada."
---
# Gestión de apps

## Resumen

Esta página explica cómo activar, desactivar, actualizar y restringir por grupos las apps del servidor, desde la página de apps o con `occ`, y cómo configurar directorios de apps personalizados, el tiempo de espera de la tienda de apps y una tienda de apps autoalojada. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/apps_management.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aplicaciones
Las apps de Nextcloud pueden ampliar, personalizar o restringir las funciones y la experiencia disponibles en el servidor Nextcloud para quien lo administra y para sus usuarios. Además de las apps integradas, como Archivos, Actividad y Fotos, otras apps como Calendario, Contactos y Talk pueden ampliar aún más su funcionalidad.

Después de instalar el servidor Nextcloud, puede convenir activar, desactivar o restringir algunas apps para grupos concretos, según las necesidades propias y las de los usuarios.

### Apps

Durante la instalación del servidor Nextcloud, algunas apps se activan de forma predeterminada. Para ver qué apps están activadas, ir a la página de Apps.

Esas apps reciben soporte y desarrollo directamente de Nextcloud GmbH y tienen la etiqueta **Destacadas**.

:::{note}
El servidor Nextcloud necesita poder comunicarse con `https://apps.nextcloud.com`, `https://ltd[1-3].nextcloud.com` y `https://garm[1-5].nextcloud.com` para listar y descargar apps. Si es necesario, permitir estos hosts en el cortafuegos o en el proxy.
:::

:::{note}
Para acceder a soluciones alternativas, soporte a largo plazo, corrección prioritaria de errores y consultoría a medida para las apps con soporte, contactar con [Nextcloud GmbH](https://nextcloud.com/enterprise/).
:::

:::{note}
Para desarrollar una app propia de Nextcloud, hay más información en el [manual de desarrollo](https://docs.nextcloud.com/server/latest/go.php?to=developer-manual) de {vendor}`Nextcloud`.
:::

Todas las apps deben tener la licencia AGPLv3+ o cualquier licencia compatible.

### Gestión de apps

Se muestran las apps activadas, desactivadas y disponibles. También se muestran paquetes de apps adicionales y filtros, como Personalización, Seguridad y Monitorización, para encontrar más apps rápidamente.

En la página de Apps se pueden activar o desactivar aplicaciones. Algunas apps tienen opciones configurables en la página de Apps, como **Activar solo para grupos específicos**, pero principalmente se activan o desactivan aquí y se configuran en los ajustes de Nextcloud (configuraciones de administración o de usuario) o en `config.php`.

Al seleccionar una app se ven su descripción y las opciones de configuración disponibles. Al hacer clic en el botón **Activar**, la app se activa. Si la app no forma parte de la instalación de Nextcloud, se descarga desde la tienda de apps, se instala y se activa.

En esta página también se ofrecen las actualizaciones de las apps. Basta con hacer clic en el botón **Actualizar** para actualizar una app concreta, o usar el botón **Actualizar todos** de la parte superior de la página para actualizar todas las apps.

:::{note}
**Versiones beta**: también se pueden instalar versiones beta de las apps directamente desde aquí, cambiando Nextcloud al canal beta en la vista general de administración.
:::

#### Notificaciones de actualización

La app predeterminada `updatenotification` envía a los administradores notificaciones sobre las actualizaciones disponibles de las apps y de Nextcloud. Además, desde Nextcloud 29, esta app también permite notificar a los usuarios sobre las apps actualizadas y los cambios que incluye la actualización. Esta notificación está activada de forma predeterminada si la app proporciona un registro de cambios.

Para desactivar las notificaciones a los usuarios, usar:

```console
occ config:app:set --type boolean --value="false" updatenotification app_updated.enabled
```

De forma predeterminada, cuando se usa la app `guests`, los usuarios invitados no reciben notificaciones. Para activar las notificaciones para ellos, usar:

```console
occ config:app:set --type boolean --value="true" updatenotification app_updated.notify_guests
```

#### Gestión de apps con `occ`

Además de gestionar las apps desde la interfaz web, los administradores pueden activar o desactivar apps con el comando `occ`.

Para activar una app, usar el siguiente comando:

```console
occ app:enable <app-id>
```

Por ejemplo, para activar la app «files», ejecutar:

```console
occ app:enable files
```

Para activar la app solo para grupos concretos, usar la opción `--groups`:

```console
occ app:enable files --groups=admin
```

Este comando activa la app «files» solo para el grupo «admin».

Para desactivar una app, usar:

```console
occ app:disable <app-id>
```

#### Uso de API privadas

Si una app de terceros usa API privadas en lugar de API públicas, la instalación falla cuando en `config.php` está establecido `'appcodechecker' => true,`.

#### Uso de directorios de apps personalizados

Usar el array **apps_paths** de `config.php` para establecer la ubicación de cualquier directorio de apps personalizado. La clave **path** define la ruta absoluta del sistema de archivos a la carpeta de apps. La clave **url** define la ruta web HTTP a esa carpeta, a partir de la raíz web de Nextcloud. La clave **writable** indica si un usuario puede instalar apps en esa carpeta.

Ejemplo: para que la carpeta predeterminada `/apps/` contenga solo las apps que se distribuyen con Nextcloud, seguir este ejemplo para configurar una carpeta `/extra-apps/` que se usará para almacenar cualquier app adicional que se instale:

```php
"apps_paths" => [
    [
            "path"     => OC::$SERVERROOT . "/apps",
            "url"      => "/apps",
            "writable" => false,
    ],
    [
            "path"     => OC::$SERVERROOT . "/extra-apps",
            "url"      => "/extra-apps",
            "writable" => true,
    ],
],
```

:::{danger}
Asegurarse de que los valores elegidos para `path` y `url` de cualquier directorio de apps personalizado no entren en conflicto con directorios que ya existen en la raíz del servidor Nextcloud (el directorio de instalación).
:::

:::{tip}
Las rutas de apps pueden estar fuera de la raíz del servidor. Sin embargo, para cualquier **path** fuera de la raíz del servidor, hay que crear en la raíz del servidor un enlace simbólico que haga apuntar **url** a **path**. Por ejemplo, si **path** es `/var/local/lib/nextcloud/extra-apps` y **url** es `/extra-apps`, se usaría el comando `ln` para crear el enlace simbólico así: `ln -sf /var/local/lib/nextcloud/extra-apps ./extra-apps`
:::

#### Configuración del tiempo de espera de la tienda de apps

El tiempo de espera de las solicitudes para obtener los metadatos de la tienda de apps puede configurarse con el ajuste de app `appstore-timeout`. El valor se indica en segundos. Este ajuste se configura con `occ` y no es un parámetro de `config.php`.

Por ejemplo, para establecer el tiempo de espera en 180 segundos:

```console
occ config:app:set settings appstore-timeout --value=180
```

El tiempo de espera predeterminado es de 120 segundos. Para restaurar el valor predeterminado, eliminar el ajuste personalizado:

```console
occ config:app:delete settings appstore-timeout
```

:::{versionchanged} 33.0.0
El tiempo de espera predeterminado de las solicitudes a la tienda de apps aumentó de 60 a 120 segundos y puede configurarse con `occ`.
:::

#### Uso de una tienda de apps autoalojada

Esta sección explica cómo permitir la instalación de apps desde una tienda de apps autoalojada. Al menos uno de los directorios de apps configurados debe ser escribible.

Para activar una tienda de apps autoalojada:

1. Establecer el parámetro `appstoreenabled` en `true`.

   Este parámetro se usa para activar la tienda de apps en Nextcloud.

2. Establecer `appstoreurl` en la URL de la tienda de apps de Nextcloud propia.

   Este parámetro se usa para establecer la ruta HTTP a la tienda de apps de Nextcloud autoalojada.

```php
"appstoreenabled" => true,
"appstoreurl" => "https://my.appstore.instance/v1",
```

De forma predeterminada, la tienda de apps está activada y configurada para usar `https://apps.nextcloud.com/api/v1` como URL de la tienda de apps. Nextcloud obtiene `apps.json` y `categories.json` desde allí. Para volver a usar los valores predeterminados, eliminar los parámetros `appstoreenabled` y `appstoreurl` de la configuración.

Ejemplo: si `categories.json` está disponible en `https://apps.nextcloud.com/api/v1/categories.json`, la URL de la tienda de apps es `https://apps.nextcloud.com/api/v1`.
````

## En APS Conecta Gestión

En APS Conecta Gestión la tienda de aplicaciones está desactivada: el contenedor del servidor recibe `NC_appstoreenabled` con el valor `"0"`, porque cada `occ upgrade` volvería a descargar de la tienda todas las aplicaciones activas y anularía las versiones fijadas. La provisión instala dos conjuntos fijos:

| Conjunto | Aplicaciones | Origen |
|---|---|---|
| `APPS` | groupfolders, side_menu, eurooffice, calendar, contacts, spreed, desktop_workspace | Paquetes fijados en `provisioning/apps/<app>/`, cada uno con su archivo `VENDOR` |
| `OWN_APPS` | epidemiologia, farmacia, territorio, intravox, estadistica | Repositorios de la organización APS-Conecta |

La política de aplicaciones desactiva `survey_client`, `nextcloud_announcements` y `office` (la vista general de oficina; el editor de documentos es `eurooffice`). Agregar o quitar una aplicación es un cambio en la provisión, no una acción en la página **Aplicaciones**.
