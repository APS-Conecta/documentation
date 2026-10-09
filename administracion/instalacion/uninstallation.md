---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Qué localizar y eliminar para desinstalar Nextcloud: directorio de la aplicación, datos, base de datos, caché y registros, según su configuración."
---
# Desinstalación

## Resumen

Esta página explica qué hay que localizar para desinstalar Nextcloud —el directorio de la aplicación, el almacenamiento de archivos, la base de datos, la caché y los registros— y qué claves de la configuración indican dónde está cada uno. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/installation/uninstallation.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/aio

La aplicación se almacena en un directorio del servidor y trabaja con una base de datos para almacenar los metadatos de los archivos y de sus recursos compartidos (funcionalidad EFSS).

No hay instrucciones generales de desinstalación, ya que Nextcloud ofrece un alto grado de flexibilidad en cuanto al modelo de operación o a la plataforma de operación; algunos ejemplos son los contenedores abstractos, las máquinas virtuales o el «bare metal», es decir, la instalación directamente en uno o varios servidores.

Por eso, para la desinstalación es importante entender dónde está instalada la aplicación Nextcloud y dónde se encuentran los datos correspondientes.

- Directorio de la aplicación (creado antes de la instalación)
- Almacenamiento de archivos de los usuarios (configurado dentro del directorio de la aplicación o fuera de él)
- Almacenamiento de metadatos en la base de datos (dentro del directorio de la aplicación al usar SQLite, o fuera, en el mismo servidor o en otro)
- Caché mediante un servidor Redis o similar (si se usa)

Para la desinstalación, hay que decidir si se debe hacer una copia de seguridad del almacenamiento de archivos o si también deben eliminarse los datos. Además, según el escenario de despliegue, hay que desaprovisionar por completo los servidores correspondientes o bien eliminar el directorio de la aplicación, así como los esquemas de la base de datos y las entradas de Redis. Si se usan contenedores o máquinas virtuales dedicados, hay que desaprovisionarlos y también hay que desaprovisionar la aplicación Nextcloud.

Para desinstalar, se pueden leer los valores de la configuración en el directorio `config`. Comprobar:

- Código fuente (instalado manualmente, normalmente en `/var/www` o `/opt/nextcloud`): eliminar el directorio en todos los servidores
- Base de datos (claves de configuración relacionadas: `dbtype`, `dbhost`): eliminar la base de datos correspondiente en todos los servidores de bases de datos (puede convenir hacer antes una copia de seguridad)
- Caché (claves de configuración relacionadas: `memcache.*`): si es persistente, eliminar la base de datos o la clave correspondiente de todos los servidores de caché
- Datos (claves de configuración relacionadas: `datadirectory`): eliminar el directorio en todos los servidores (puede ser necesario crear antes una copia de seguridad). Nextcloud ofrece la opción de almacenar los datos en distintas ubicaciones. Comprobar también el almacenamiento externo y el almacenamiento de objetos (objectstore)
- Registros (claves de configuración relacionadas: `logfile`, `logfile_audit`): normalmente en el directorio de datos, pero también pueden estar en otra ubicación, como `/var/log/`
````
