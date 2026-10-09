---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Instalar ClamAV, activar y configurar la app Antivirus para archivos, comprobarla con EICAR y gestionar el analizador en segundo plano con occ."
---
# Escáner antivirus

## Resumen

Esta página explica cómo instalar ClamAV en distintas distribuciones y con Docker, activar y configurar la app Antivirus para archivos en sus tres modos, comprobar que funciona, conocer sus límites con archivos cifrados y gestionar el analizador en segundo plano. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_server/antivirus_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El servidor Nextcloud puede configurarse para analizar automáticamente en busca de virus los archivos recién subidos con la app Antivirus para archivos. La app Antivirus para archivos integra con Nextcloud el motor antivirus de código abierto [ClamAV](https://www.clamav.net/index.html). ClamAV detecta todo tipo de malware, incluidos troyanos, virus y gusanos, y funciona con todos los tipos de archivo principales, incluidos archivos de Windows, Linux y Mac, archivos comprimidos, ejecutables, archivos de imagen, Flash, PDF y muchos otros. El demonio Freshclam de ClamAV actualiza automáticamente su base de datos de firmas de malware a intervalos programados.

ClamAV funciona en Linux, en cualquier sistema operativo de tipo Unix y en Microsoft Windows. Sin embargo, con Nextcloud solo se ha probado en Linux, así que estas instrucciones son para sistemas Linux. Primero hay que instalar ClamAV y después instalar y configurar la app Antivirus para archivos en Nextcloud.

### Instalar ClamAV

Como siempre, cada distribución de Linux gestiona la instalación y configuración de ClamAV a su manera.

**Debian, Ubuntu, Linux Mint:** en los sistemas Debian y Ubuntu, y sus numerosas variantes, ClamAV se instala con estos comandos:

```
apt-get install clamav clamav-daemon
```

El instalador crea automáticamente los archivos de configuración predeterminados e inicia los demonios `clamd` y `freshclam`. No hace falta hacer nada más, aunque es buena idea revisar la documentación de ClamAV y los ajustes en `/etc/clamav/`. Activar el registro detallado tanto en `clamd.conf` como en `freshclam.conf` hasta resolver cualquier problema.

**RedHat Enterprise Linux 7, CentOS 7:** en RedHat Enterprise Linux 7 y sistemas relacionados hay que instalar el repositorio Extra Packages for Enterprise Linux (EPEL) y después instalar ClamAV:

```
yum install epel-release
yum install clamav clamav-scanner clamav-scanner-systemd clamav-server
clamav-server-systemd clamav-update
```

Esto instala dos archivos de configuración: `/etc/freshclam.conf` y `/etc/clamd.d/scan.conf`. Hay que editar ambos antes de poder ejecutar ClamAV. Los dos archivos están bien comentados, y `man clamd.conf` y `man freshclam.conf` explican todas las opciones. Para verificar el usuario y el grupo de ClamAV, consultar `/etc/passwd` y `/etc/group`.

Primero, editar `/etc/freshclam.conf` y configurar las opciones. `freshclam` actualiza la base de datos de malware, así que conviene que se ejecute con frecuencia para obtener firmas de malware actualizadas. Ejecutarlo manualmente después de la instalación para descargar el primer conjunto de firmas de malware:

```
freshclam
```

Los paquetes de EPEL no incluyen un archivo init para `freshclam`, así que la forma rápida y sencilla de configurar comprobaciones periódicas es con un trabajo cron. Este ejemplo lo ejecuta cada hora, a los 47 minutos:

```
# m   h  dom mon dow  command
  47  *  *   *    *  /usr/bin/freshclam --quiet
```

Conviene evitar los múltiplos de 10, porque es cuando los servidores de ClamAV reciben más peticiones de actualización.

A continuación, editar `/etc/clamd.d/scan.conf`. Al terminar, hay que activar el archivo de servicio de `clamd` e iniciar `clamd`:

```
systemctl enable clamd@scan.service
systemctl start clamd@scan.service
```

Con eso debería quedar todo listo. Activar el registro detallado en `scan.conf` y `freshclam.conf` hasta que funcione como se desea.

**Docker, Docker-compose:** para instalar ClamAV con docker o docker compose puede usarse la imagen oficial de ClamAV o construir una propia. Este ejemplo se basa en la imagen de docker de <https://github.com/Cisco-Talos/clamav>.

El socket de ClamAV puede montarse desde el contenedor Docker en el sistema anfitrión como volumen. En ese caso no hace falta exponer ningún puerto fuera del contenedor.

Para Docker, ejecutar este comando:

```
docker run --name clamav -d -v /var/run/clamav/:/var/run/clamav/ -v /var/docker/clamav/virus_db/:/var/lib/clamav/ clamav/clamav:stable_base
```

Para Docker-compose, usar los siguientes ajustes:

```
version: "3.6"
services:
  clamav:
    image: "clamav/clamav:stable_base"
    container_name: "clamav"
    volumes:
      # Socket
      - /var/run/clamav/:/var/run/clamav/
      # Virus DB
      - /var/docker/clamav/virus_db/:/var/lib/clamav/
    restart: unless-stopped
```

### Activar la app Antivirus para archivos

Colocar la app `files_antivirus` en el directorio `apps` del servidor Nextcloud. Después, la app aparece en la página Apps de Nextcloud, donde basta con activarla.

### Configurar ClamAV en Nextcloud

A continuación, ir a la página de administración de Nextcloud y establecer el nivel de registro de Nextcloud en «Todo».

Ahora, buscar el panel de configuración del antivirus en la página de administración.

ClamAV funciona en uno de estos tres modos:

- Demonio (socket): ClamAV se ejecuta en el mismo servidor que Nextcloud. El demonio de ClamAV, `clamd`, se ejecuta en segundo plano. Cuando no hay actividad, `clamd` supone una carga mínima para el sistema. Si los usuarios suben grandes volúmenes de archivos, se verá un uso elevado de CPU.

- Demonio: ClamAV se ejecuta en un servidor distinto. Es una buena opción para servidores Nextcloud con grandes volúmenes de subidas de archivos.

- Ejecutable: ClamAV se ejecuta en el mismo servidor que Nextcloud, y el comando `clamscan` se inicia y se detiene con cada subida de archivo. `clamscan` es lento y no siempre fiable para el uso a demanda; es mejor usar uno de los modos de demonio.

**Demonio (socket):** Nextcloud debería detectar el socket de `clamd` y rellenar el campo `Socket`. Es la opción `LocalSocket` de `clamd.conf`. Para verificarlo puede ejecutarse `netstat`:

```
netstat -a|grep clam
unix 2 [ ACC ] STREAM LISTENING 15857 /var/run/clamav/clamd.ctl
```

El valor `Stream Length` establece el número de bytes que se leen en una pasada. El valor predeterminado es 26214400 bytes, o 25 MiB. Este valor no debe superar el ajuste `memory_limit` de PHP, o la memoria física si `memory_limit` está establecido en -1 (sin límite).

`Action for infected files found while scanning` permite elegir entre registrar las alertas sin eliminar los archivos o eliminar de inmediato los archivos infectados.

**Demonio:** para la opción Demonio se necesita el nombre de host o la dirección IP del servidor remoto que ejecuta ClamAV y el número de puerto del servidor.

**Ejecutable:** la opción Ejecutable requiere la ruta de `clamscan`, el comando interactivo de análisis de ClamAV. Nextcloud debería encontrarla automáticamente.

Cuando ClamAV funcione de forma satisfactoria, conviene volver atrás y cambiar todos los registros a niveles menos detallados.

### Confirmar que todo funciona

Todos los proveedores de antivirus implementan una cadena de virus de prueba, lo que facilita bastante las pruebas. Los archivos están aquí: <https://www.eicar.org/download-anti-malware-testfile/>

- Subir el archivo provocará un error: «Virus Win.Test.EICAR_HDB-1 is detected in the file. Upload cannot be completed.»

### Limitaciones de la detección de archivos cifrados con ClamAV

De forma predeterminada, ClamAV puede devolver «OK» para archivos comprimidos protegidos con contraseña y archivos cifrados. Este comportamiento conocido de ClamAV elude la opción «Block unscannable files» de la app Antivirus. Pueden configurarse opciones de alerta adicionales en `clamd.conf` que deberían detectarlo:

- `AlertEncryptedArchive` - Alerta sobre archivos comprimidos cifrados con firma heurística (.zip, .7zip, .rar cifrados).
- `AlertEncryptedDoc` - Alerta sobre archivos comprimidos cifrados con firma heurística (.pdf cifrados).
- `AlertEncrypted` - Alerta tanto sobre archivos comprimidos como sobre documentos cifrados con firma heurística.

Para detectar y bloquear de forma fiable los archivos cifrados, consultar la documentación de los backends antivirus disponibles.

### Gestionar el analizador en segundo plano

El analizador en segundo plano no requiere ninguna intervención manual. Sin embargo, a veces puede convenir inspeccionarlo o realizar tareas con él.

#### Cómo funciona el analizador en segundo plano

Cada vez que se ejecuta, el analizador en segundo plano procesa los archivos en tres pasadas (por orden de prioridad), hasta el tamaño de lote configurado por ejecución:

1. **Archivos sin analizar** — archivos que nunca se han analizado, incluidos los que se subieron o ya existían antes de instalar la app Antivirus. Todos ellos acabarán analizándose a medida que el trabajo en segundo plano se ejecute repetidamente.

2. **Archivos modificados** — archivos cuya fecha de modificación es posterior a la de su último análisis, es decir, archivos que se han actualizado desde que se analizaron por última vez.

3. **Archivos desactualizados** — archivos cuyo último análisis fue hace más de 28 días (configurable mediante `av_rescan_days`), para tener en cuenta las definiciones de virus actualizadas.

De forma predeterminada, el analizador se ejecuta como máximo una vez cada 15 minutos. La frecuencia efectiva también está limitada por la frecuencia con que se ejecuta el mecanismo de trabajos en segundo plano de Nextcloud (cron, webcron o ajax).

Para cambiar el intervalo mínimo entre ejecuciones (en segundos):

```
sudo -E -u www-data php occ config:app:set files_antivirus av_scan_interval --value="900"
```

Para cambiar el número de días tras los cuales se vuelven a analizar los archivos ya analizados:

```
sudo -E -u www-data php occ config:app:set files_antivirus av_rescan_days --value="28"
```

**Almacenamiento externo:** los archivos del almacenamiento externo se incluyen en las pasadas 1 y 2 (análisis inicial y nuevo análisis al modificarse). Sin embargo, el nuevo análisis periódico de 28 días (pasada 3) solo se aplica a los archivos de `files/` (es decir, el almacenamiento personal), no al almacenamiento externo.

#### Obtener información sobre los archivos de la cola de análisis

```
sudo -E -u www-data php occ files_antivirus:status [-v]
```

#### Lanzar manualmente el análisis en segundo plano

```
sudo -E -u www-data php occ files_antivirus:background-scan [-v] [-m MAX]
```

#### Analizar manualmente un solo archivo

```
sudo -E -u www-data php occ files_antivirus:scan <path>
```

#### Marcar un archivo como analizado o sin analizar

```
sudo -E -u www-data php occ files_antivirus:mark <path> <scanned|unscanned>
```

Los archivos marcados como analizados no se analizarán durante las cuatro semanas siguientes.

### Configurar ICAP en Nextcloud

Nextcloud ofrece la integración de protección antivirus basada en el protocolo ICAP. Los ajustes se describen aquí. La documentación adicional está en preparación.

### Desactivar la tarea de análisis en segundo plano

El análisis en segundo plano puede desactivarse con occ para analizar los archivos solo durante la subida:

```
sudo -E -u www-data php occ config:app:set files_antivirus av_background_scan --value="off"
```

:::{note}
Establecer `av_rescan_days` en `0` **no** desactiva el nuevo análisis periódico de los archivos ya analizados. Cualquier valor inferior a `1` se sustituye silenciosamente por el valor predeterminado de 28 días, de modo que el nuevo análisis continúa con su calendario normal. Para detener por completo el análisis en segundo plano, usar `av_background_scan` como se muestra arriba.
:::
````
