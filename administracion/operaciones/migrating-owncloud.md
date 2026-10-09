---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo migrar de ownCloud a Nextcloud: versiones compatibles, comandos posteriores a occ upgrade y la ruta de actualización de Nextcloud y PHP."
---
# Migrar desde ownCloud

## Resumen

Esta página explica cómo migrar una instalación de ownCloud a Nextcloud como si fuera una actualización manual: qué versiones son compatibles, qué comandos ejecutar después y cómo seguir actualizando Nextcloud y PHP hasta la versión actual. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/maintenance/migrating_owncloud.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Especialmente al migrar de ownCloud a Nextcloud, conviene crear una copia de seguridad de la configuración, la base de datos y el directorio de datos, por si algo sale mal.
:::

Actualmente, migrar desde ownCloud es como realizar una actualización manual. Así que es bastante fácil migrar de una versión de ownCloud a al menos una versión de Nextcloud. Sin embargo, esto solo funciona con versiones suficientemente compatibles en el esquema de la base de datos y en el código. Consultar la tabla siguiente para ver un mapa de versiones con las que la migración es fácilmente posible:

| ownCloud | Nextcloud |
|---|---|
| 10.13.x | 25.0.13 |
| 10.14.x | 25.0.13 |
| 10.15.x | 25.0.13 |
| 10.16.x | 25.0.13 |

:::{note}
Como ownCloud no admite ni admitirá PHP 8.0 o superior, hay que migrar de ownCloud 10.13.x a Nextcloud 25 y luego seguir actualizando desde ahí. Se recomienda encarecidamente migrar a Nextcloud, ya que las versiones de PHP anteriores a PHP 8 han llegado al final de su vida útil; consultar <https://www.php.net/supported-versions.php>.
:::

1. Primero, descargar la versión correcta de Nextcloud desde la [página de versiones anteriores de Nextcloud](https://nextcloud.com/changelog/),

2. Asegurarse de hacer una {nc-doc}`copia de seguridad <admin_manual/maintenance/backup>` antes de migrar.

3. Seguir las instrucciones de actualización descritas en el manual {nc-doc}`admin_manual/maintenance/manual_upgrade`.

4. Al migrar a Nextcloud 20.0 o posterior, también habrá que ejecutar los siguientes comandos después de `occ upgrade`:

   - `occ db:convert-filecache-bigint`
   - `occ db:add-missing-columns`
   - `occ db:add-missing-indices`
   - `occ db:add-missing-primary-keys`

5. Si se usaba el cron del sistema, verificar si la entrada de crontab usaba el comando `occ system:cron`. En ese caso, ajustarla para que use el comando `php` en su lugar, según {nc-ref}`la documentación de configuración de los trabajos en segundo plano <system-cron-configuration-label>`

6. Como Nextcloud 25 es la última versión de Nextcloud compatible con PHP 7, después hay que actualizar la instalación de PHP para seguir actualizando a la versión actual de Nextcloud. Se recomienda actualizar PHP a la versión 8.1 antes de continuar con las actualizaciones.

7. Usar el {nc-doc}`actualizador integrado de Nextcloud <admin_manual/maintenance/update>` para actualizar la instancia a la versión más reciente. Esto debe hacerse para cada versión mayor, ya que no se admiten actualizaciones entre varias versiones mayores. Así, la ruta de actualización sería: 26 → 27.1 → 28 → 29 → 30 → 31.

8. Al llegar a Nextcloud 30 o 31, se recomienda volver a actualizar PHP a una versión actual como PHP 8.3. También puede hacerse entre medias, ya que PHP 8.2 es compatible desde Nextcloud 26 y PHP 8.3 desde Nextcloud 28, pero en la mayoría de los casos es más fácil completar primero las actualizaciones de versión de Nextcloud.

9. Asegurarse también de verificar «Avisos de seguridad y configuración» en la sección «Vista general» de la página de ajustes.

10. En algunos casos, las apps instaladas desde ownCloud Market pueden haberse desactivado por incompatibles (p. ej., calendar y contacts), por lo que conviene reinstalar las de Nextcloud con `occ app:enable calendar`, `occ app:enable contacts`, etc.
````
