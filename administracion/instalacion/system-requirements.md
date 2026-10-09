---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Requisitos de un servidor Nextcloud (sistema operativo, base de datos, servidor web, PHP, memoria) y versiones mínimas de clientes y navegadores."
---
# Requisitos del sistema

## Resumen

Esta página detalla las plataformas que Nextcloud admite en el servidor —sistema operativo, base de datos, servidor web y PHP—, los requisitos de CPU, memoria y MySQL/MariaDB, y las versiones mínimas del cliente de escritorio, de las apps móviles y de los navegadores web. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/installation/system_requirements.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

### Servidor

Para obtener el mejor rendimiento, estabilidad y funcionalidad, hemos documentado algunas recomendaciones para ejecutar un servidor Nextcloud.

:::{note}
Si se planifica una instalación para una organización y se depende de consultoría profesional de despliegue (p. ej., para un escalado eficiente y fiable) y de soporte, recomendamos encarecidamente conocer nuestro [soporte empresarial](https://nextcloud.com/enterprise/).
:::

:::{list-table}
:header-rows: 1

* - Plataforma
  - Opciones
* - Sistema operativo (64 bits)
  - - **Ubuntu 26.04 LTS** (recomendado)
    - Ubuntu 24.04 LTS
    - Ubuntu 22.04 LTS
    - **Red Hat Enterprise Linux 10** (recomendado)
    - Red Hat Enterprise Linux 9
    - Debian 13 (Trixie)
    - Debian 12 (Bookworm)
    - SUSE Linux Enterprise Server 16
    - SUSE Linux Enterprise Server 15 SP6 (o posterior)
    - openSUSE Leap 16
    - CentOS Stream
    - Alpine Linux
* - Base de datos
  - - MySQL 8.0 / 8.4
    - MariaDB 10.6 / 10.11 / 11.4 / **11.8** (recomendado)
    - Oracle Database 19c, 21c, 23ai (*solo como parte de una suscripción empresarial*)
    - PostgreSQL 14 / 15 / 16 / 17 / **18** (recomendado)
    - SQLite 3.24+ (*solo recomendado para pruebas e instancias mínimas*)
* - Servidor web
  - - **Apache 2.4 con** `mod_php` **o** `php-fpm` (recomendado)
    - nginx con `php-fpm`
* - Entorno de ejecución de PHP
  - - 8.2 (*obsoleto*)
    - 8.3
    - 8.4
    - **8.5** (*recomendado*)
:::

Consultar {nc-doc}`admin_manual/installation/source_installation` para conocer los módulos de PHP mínimos y el software adicional para instalar Nextcloud.

Para garantizar la funcionalidad completa de Nextcloud, asegurarse de que el servidor pueda llegar a los {nc-ref}`sistemas remotos necesarios <connections_to_remote_servers>`.

#### Arquitectura de CPU y sistema operativo

Se recomienda encarecidamente una CPU, un sistema operativo y un PHP de 64 bits para Nextcloud.

Los sistemas de 32 bits son compatibles, con las siguientes limitaciones conocidas:

- No se admiten fechas anteriores a la época Unix (1970-01-01)
- No se admiten fechas posteriores a 2038
- Puede que algunas apps externas no funcionen en sistemas de 32 bits

#### Memoria

Los requisitos de memoria para ejecutar un servidor Nextcloud son muy variables, según el número de usuarios, de apps y de archivos y el volumen de actividad del servidor.

Nextcloud necesita un mínimo de **128MB** de RAM por proceso, y recomendamos un mínimo de **512MB** de RAM por proceso.

En entornos con poca memoria, algunas funciones o apps pueden requerir ajustes en su configuración predeterminada para funcionar (o, en algunos casos, puede que haya que desactivarlas por completo).

:::{warning}
Para usar el actualizador integrado se necesitan al menos 256MB.
:::

#### Requisitos de base de datos para MySQL / MariaDB

Actualmente se requiere lo siguiente si se ejecuta Nextcloud junto con una base de datos MySQL / MariaDB:

- Motor de almacenamiento InnoDB (MyISAM no es compatible)
- Nivel de aislamiento de transacciones «READ COMMITTED» (consultar: {nc-ref}`db-transaction-label`)
- Registro binario desactivado o configurado con BINLOG_FORMAT = ROW (consultar: <https://dev.mysql.com/doc/refman/5.7/en/binary-log-formats.html>)
- Para la **compatibilidad con emojis (UTF8 de 4 bytes)**, consultar {nc-doc}`admin_manual/configuration_database/mysql_4byte_support`

#### Por qué dejamos de admitir versiones antiguas de PHP

Cada año se añade una nueva versión de PHP y las versiones antiguas de PHP quedan obsoletas. Esto también afecta a la versión de PHP recomendada que documentamos.

Intentamos admitir las versiones antiguas de PHP durante tanto tiempo como sea razonablemente posible. Sin embargo, la lista de correcciones de seguridad, de rendimiento y de errores no hará más que crecer; algunas de esas correcciones podrían considerarse críticas y, por tanto, en algún momento será inevitable declarar obsoletas las versiones antiguas.

Por eso se recomienda mantener actualizada la versión de PHP.

##### Ventajas de actualizar PHP

- **Seguridad**

  PHP deja de publicar correcciones de seguridad para las versiones antiguas. {vendor}`Nextcloud` no puede implementar las correcciones de seguridad que llegan con las nuevas versiones de PHP mientras admitamos versiones de PHP obsoletas, ya que la sintaxis que podemos usar debe ser la más baja de las versiones admitidas; por eso fallan los paquetes upstream de terceros, porque han dejado de dar ese soporte.

- **Rendimiento**

  El lenguaje mejora continuamente con el tiempo, lo que permite atender más solicitudes en mucho menos tiempo.

##### Soporte a largo plazo

Si se ejecuta Nextcloud para un caso de uso crítico para la organización, se puede considerar actualizar la suscripción a una suscripción premium, que incluye 5 años de soporte a largo plazo. Esto significa que se siguen recibiendo versiones de mantenimiento para problemas de seguridad altos y críticos, correcciones de pérdida de datos y regresiones dentro de la versión durante este periodo ampliado.

### Cliente de escritorio

Recomendamos encarecidamente usar la versión más reciente del sistema operativo para obtener la experiencia más completa y estable de nuestros clientes.

- **Windows** 10+
- **macOS** Monterey (12.0)+ (solo 64 bits)
  \* Tener en cuenta que puede ser necesario que el servidor cumpla con App Transport Security de Apple para que el cliente de escritorio se conecte correctamente. Esto puede implicar usar un certificado digital firmado adecuadamente según los estándares establecidos por Apple. Apple ofrece más información en su documentación para desarrolladores: <https://developer.apple.com/documentation/security/preventing-insecure-network-connections>
- **Linux** (solo 64 bits) Debería funcionar en cualquier distribución más reciente que Ubuntu 18.04 con nuestro paquete AppImage oficial

### Apps móviles

Recomendamos encarecidamente usar la versión más reciente del sistema operativo móvil para obtener la experiencia más completa y estable de nuestras apps móviles.

#### App de Archivos

- **iOS** 17.0+
- **Android** 9.0+

#### App de Talk

- **iOS** 16.0+
- **Android** 8.0+
- **Nextcloud Server** 22.0+
- **Nextcloud Talk** 12.0+

### Navegador web

Para obtener la mejor experiencia con la interfaz web de Nextcloud, recomendamos usar la versión más reciente y con soporte de un navegador de esta lista, o de uno basado en ellos:

- Microsoft **Edge**
- Mozilla **Firefox**
- Google **Chrome**/Chromium
- Apple **Safari**

:::{note}
Si se quiere usar Nextcloud Talk, conviene usar la versión más reciente de Mozilla **Firefox** o de Google **Chrome**/Chromium para tener la experiencia completa con las videollamadas y el uso compartido de pantalla.
:::
````
