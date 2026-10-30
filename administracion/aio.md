---
tipo: explicacion
audiencia: administracion
apps: [gestion]
resumen: "El instalador de la suite: el arranque de una línea, el asistente, las aplicaciones desde sus publicaciones firmadas, el candado de versiones y actualizar."
---
# AIO

## Contexto

APS Conecta Gestión se instala con APS Conecta Gestión AIO, un fork de [Nextcloud All-in-One](https://github.com/nextcloud/all-in-one) que APS Conecta mantiene para los CESFAM y la red de atención primaria de Chile, junto con el paquete del host, el Provisionador y el manifiesto de la suite, en el repositorio [APS-Conecta/gestion](https://github.com/APS-Conecta/gestion) — el repositorio APS-Conecta/AIO fue su primera casa y se eliminó una vez absorbido. Nextcloud GmbH no lo produce, no lo patrocina ni lo respalda.

Las páginas de {doc}`instalación </administracion/instalacion/index>`, tejidas del manual de {vendor}`Nextcloud`, llevan el aviso «En APS Conecta Gestión esto difiere» y remiten a esta página. Un establecimiento instala una etiqueta publicada de la suite, nunca una rama: el asistente de esa etiqueta crea y administra todos los contenedores, y el Provisionador del instalador configura después el establecimiento con las fases de aprovisionamiento.

La instalación completa es una línea en el servidor y ocho pasos — cuatro del servidor y cuatro del navegador —, descritos paso a paso en el [manual del instalador](https://github.com/APS-Conecta/gestion/blob/main/aps/INSTALLER.md), en inglés, y en la [guía clínica](https://github.com/APS-Conecta/gestion/blob/main/aps/GUIA-CLINICA.md), en español, ambos en la carpeta `aps/` de Gestión. Esta página explica el diseño del instalador, lo que cambia y sus límites.

```{note}
Los cambios del plan de actualización corresponden a la próxima versión. Consulte su estado en {doc}`/proyecto/novedades/instalador` y seleccione una versión publicada para instalar.
```

## Diseño

### El arranque de una línea

```console
curl -fsSL https://github.com/APS-Conecta/gestion/releases/download/vX.Y.Z/apsconecta-vX.Y.Z-install.sh | sudo bash
```

El ancla de confianza es la URL de la versión —fijada a la etiqueta— más TLS: el instalador lleva dentro la suma sha256 del paquete y la clave pública de la firma del proyecto. La descarga se verifica antes de desempacar nada; un servidor que ya tiene `signify` comprueba además la firma, y uno que no la tiene instala la herramienta en el paso «preparar» y comprueba el paquete guardado desde la corrida siguiente. El desempaque es atómico y la suite queda en `/opt/aps-conecta/instalador`, con el paquete guardado —tarball, sumas y firma— en `/opt/aps-conecta/paquete`, para que la revisión previa vuelva a verificarlo sin red. La copia del repositorio no instala: lleva su suma vacía a propósito, y solo el activo de la publicación ejecuta.

Después, `sudo aps-conecta install` enlaza el comando `aps-conecta` y recorre los ocho pasos: «Revisar el servidor», «Preparar el servidor», «Descargar APS Conecta» y «Abrir el instalador web» en el servidor; «Elegir el centro», «Iniciar la suite», «Cargar equipos y personas» y «Revisar y ejecutar» en el navegador. Quien audita puede verificar a mano, con `signify-openbsd` y `sha256sum -c` contra la clave `installer.pub` del repositorio, como enseña el manual.

### El contenedor maestro

Nextcloud AIO administra Docker hablando directamente con su socket: un solo contenedor, iniciado con un solo comando, crea y administra todos los contenedores de la instalación.

En la suite ese contenedor es `nextcloud-aio-mastercontainer`, que la interfaz llama «el asistente» («Registros del asistente»). Sirve su interfaz web en el puerto 8080 y administra los demás contenedores mediante las imágenes versionadas de `ghcr.io/aps-conecta/*`. Conserva el nombre de upstream porque la orden de arranque y la restauración de AIO lo nombran; los contenedores que crea se llaman `aps-conecta-*`.

La revisión previa genera la orden `docker run` del asistente, que no se escribe a mano. Difiere de la de upstream en la imagen, `ghcr.io/aps-conecta/all-in-one:<etiqueta de la suite>` en lugar de `ghcr.io/nextcloud-releases/all-in-one:latest`; en los puertos, porque publica solo el 8080, sin el 80 ni el 8443, y fija `APACHE_PORT=443`; y en `NEXTCLOUD_STARTUP_APPS` vacío: ninguna imagen lleva una aplicación, y una instalación al arrancar solo agregaría ruido.

La configuración del asistente vive en el volumen `nextcloud_aio_mastercontainer` y sobrevive a la eliminación del contenedor. El contenedor web no guarda estado: el asistente lo reconstruye desde esa configuración en cada inicio.

El asistente nunca vuelve a crear un contenedor que todavía existe. Por eso un directorio del host montado en un contenedor, como el del certificado del instalador (`APS_TLS_DIR`), queda fijado al crear el contenedor: la configuración lo conserva, y cambiar la variable no mueve el montaje hasta recrear el asistente y el contenedor web, como indica la sección 9 del [manual del instalador](https://github.com/APS-Conecta/gestion/blob/main/aps/INSTALLER.md).

Mientras la suite está en ejecución, el inicio de sesión directo en el asistente queda bloqueado. El asistente muestra «El inicio de sesión está bloqueado porque la suite está en ejecución.» y remite al inicio de sesión automático desde la administración de APS Conecta Gestión.

(una-etiqueta-veinte-imagenes)=
### Imágenes de una versión

La construcción obtiene el conjunto completo desde `php/containers.json` y los Dockerfiles de ejecución. Todas las imágenes se construyen desde un mismo commit y el manifiesto registra sus resúmenes. PostgreSQL se prueba antes de publicarse.

El asistente usa la etiqueta de su propia imagen para seleccionar las imágenes de los demás servicios. La publicación verifica el conjunto completo y conserva los resúmenes de las versiones publicadas.

(lo-que-cambia-el-fork)=
### Servicios incluidos

La próxima versión instala un conjunto fijo: Euro-Office, Talk, búsqueda de texto completo, vistas previas, antivirus y AppAPI mediante HaRP. Farmacia, Estadística y Tótem conservan su selección independiente. La habilitación de grabaciones dependerá del perfil de recursos validado.

El establecimiento aporta su dominio o dirección IP. La administración aplica las actualizaciones mediante la versión de la suite y conserva el control de la instalación.

### Las aplicaciones, desde sus publicaciones

Ninguna imagen lleva una aplicación: las propias y los forks llegan de la publicación firmada de cada repositorio, y las de la tienda, de la tienda de {vendor}`Nextcloud` con la puerta acotada. El manifiesto de la suite (`apps.json`, en el repositorio Gestión) es la única lista de aplicaciones, y cada fila nombra su propio canal.

- **Propias y forks** — Territorio, Epidemiología, IntraVox, Euro-Office, Talk y el menú lateral se instalan sin pregunta en el momento de ejecutar: la resolución descarga, sin cuenta ni token de GitHub, la publicación firmada más reciente de la aplicación compatible con la versión de Nextcloud en marcha, y la verifica contra la clave de aplicaciones de la suite (`apps.pub`: la firma de las sumas, el hash del paquete y de `info.xml`, el directorio raíz igual al identificador, sin `appinfo/signature.json`) antes de desempacar nada.
- **De tienda** — Calendario, Contactos y las carpetas de grupo llegan de la tienda de aplicaciones, que la suite mantiene cerrada: se abre solo para el comando que instala cada una y vuelve a cerrarse. El punto de entrada del contenedor instala por esa misma puerta acotada `notify_push` cuando falta: el hermano de notificaciones parte junto con los contenedores, antes de cualquier provisión.
- **Opcionales** — La tarjeta «Aplicaciones opcionales» del paso 6 lista, del manifiesto, las aplicaciones que el establecimiento elige (hoy Farmacia, Estadística y Tótem), todas desmarcadas. Una no elegida no se instala: ni se descarga ni ocupa disco, y sus datos extra —la base DEIS de Estadística, por ejemplo— llegan solo con la elección.

El **candado** —el registro de versiones, `/opt/aps-conecta/apps.lock.json`— anota la versión de Nextcloud y, por aplicación, su canal, etiqueta, versión y suma. Lo escribe la resolución al instalar, está dentro del alcance del respaldo y lo mueve solo `aps-conecta actualizar`. Una provisión repetida respeta el candado y no descarga nada, y una reparación nunca se convierte en una actualización: la {doc}`gestión de apps </administracion/aplicaciones>` de la interfaz no es el camino.

### Copias de seguridad

La copia de la instancia es la de AIO, basada en BorgBackup: incremental, comprimida y cifrada. La clave de cifrado aparece en la interfaz del asistente, y sin ella no se restaura ninguna copia.

El paso 6 del instalador web programa la copia diaria a las 04:00, hora de Santiago, en `/srv/aps-conecta/respaldos`, e incluye `/opt/aps-conecta`, donde están las credenciales, la ficha del establecimiento y el candado. El asistente funciona en UTC, así que el paso 6 envía la hora UTC equivalente (07:00 en horario de verano, 08:00 en horario de invierno) y el asistente muestra esa hora. Tras el siguiente cambio de horario, la copia corre a las 03:00 o a las 05:00 de Santiago.

La copia detiene los contenedores en ejecución mientras se crea: la suite queda sin servicio durante esa ventana. El botón «Crear copia de seguridad» lo advierte con «Esto detendrá todos los contenedores en ejecución y creará la copia de seguridad.».

La copia queda en el mismo disco que la instancia, por lo que debe copiarse fuera del servidor, a un disco externo u otro equipo. Los directorios adicionales se respaldan, pero nunca se restauran junto con la instancia: `/opt/aps-conecta` se recupera a mano con `borg extract`. El mapa base no se respalda porque no está en el servidor: el navegador carga las teselas de OpenStreetMap.

Una copia hecha por un Nextcloud AIO sin modificar no se restaura en la suite. Tras una reinstalación, el asistente nuevo no puede reutilizar el repositorio de copias anterior.

### Actualizaciones

La suite se actualiza como un conjunto, nunca un componente por separado. Antes de anunciar una etiqueta nueva, se instala en un equipo de ensayo limpio tal como lo hace un establecimiento, y ese ensayo es el registro de aceptación. El conjunto de imágenes cambia cuando el administrador instala una versión nueva. Las actualizaciones automáticas quedan retiradas; cada versión publicada conserva sus resúmenes.

Las **aplicaciones** se mueven solo cuando el administrador lo decide, con:

```console
sudo aps-conecta actualizar
```

1. Se niega a correr si la suite no está en marcha, si no hay candado o si el respaldo no está configurado.
2. Imprime el plan —la versión instalada y la candidata de cada aplicación—. Con `sudo aps-conecta actualizar --revisar` imprime el plan y no escribe nada: es la forma de ver qué se movería antes de mover nada.
3. Toma un respaldo completo primero, por la API del propio asistente, y se detiene si el respaldo falla.
4. Descarga y verifica las candidatas en un candado nuevo y aplica una aplicación a la vez —las de tienda con un comando de actualización acotado, uno por aplicación—, y al final desinstala cada aplicación publicada que salió del manifiesto y quita su fila del candado; el candado viejo se reemplaza solo si todo resultó.
5. Revalida: humo, oficina y divergencia.

Si algo falla, el candado queda como estaba, se nombra la aplicación que falló y se imprime el comando para restaurar: el asistente, «Restaurar la copia de seguridad seleccionada», con la copia más reciente. Un salto de versión mayor de Nextcloud se rechaza mientras una aplicación predeterminada no tenga una versión compatible.

Tras actualizar la suite a una etiqueta nueva, `aps-conecta revalidate` corre las tres verificaciones y las reporta todas, y la [guía clínica](https://github.com/APS-Conecta/gestion/blob/main/aps/GUIA-CLINICA.md#7-tras-actualizar) describe la revalidación y las revisiones manuales de cada actualización. Una instalación de la v0.3.0 o anterior usa los nombres de contenedor de upstream; la suite no los migra, y esa instalación se reinstala.

### La frontera con el aprovisionamiento

El asistente termina donde empieza el paquete del host. Con los contenedores en marcha, la página posterior al arranque muestra «Suite en marcha» y devuelve al instalador web, que sigue con «Cargar equipos y personas» y «Revisar y ejecutar».

Desde ahí, el Provisionador del instalador ejecuta las fases de aprovisionamiento con `docker exec` sobre la instancia en marcha: las mismas fases que levantan el entorno de desarrollo. La inicialización y la fase 14 comparten la rutina que configura la URL pública del servidor de documentos y el secreto JWT; por eso el `.env` del establecimiento no lleva claves de oficina. El aprovisionamiento se describe en {doc}`/administracion/aprovisionamiento`.

## Compromisos y límites

La integración de antivirus, búsqueda y AppAPI, la configuración inicial de llamadas y el perfil de grabación continúan en las etapas del {doc}`plan de cambios </proyecto/novedades/instalador>`. La presencia de un contenedor acredita su ejecución; cada función tiene además su verificación de integración.

- **Mensajes en inglés.** El asistente muestra 68 mensajes que nacen en código PHP que el fork no traduce: los cambios PHP declarados son de comportamiento, no de textos. La declaración del fork lleva la lista completa, por archivo.
- **Sin red al actualizar.** En los arranques que cambian de imagen, un establecimiento sin conexión espera la sonda de la tienda de aplicaciones (`apps.nextcloud.com`) hasta que vence o vuelve la red. Es un comportamiento de upstream que el fork no modifica.
- **Nombres de contenedor.** El nombre `aps-conecta-*` rige solo para instalaciones nuevas; una instalación con los nombres de upstream se reinstala, nunca se migra.
- **Montajes fijados.** Un directorio del host montado en un contenedor cambia solo al recrear ese contenedor.
- **Dominio o IP.** Una suite iniciada para un dominio no pasa a una dirección IP, ni al revés: se reinstala.
- **Copias.** La copia diaria comparte disco con la instancia, detiene la suite mientras corre y se desplaza una hora con cada cambio de horario. Los directorios adicionales se restauran a mano.
- **Panel de registros.** Tras una actualización, un navegador con la hoja de estilos anterior en caché muestra el panel de registros del asistente con la paleta previa hasta revalidarla, y un refresco forzado lo corrige: el PHP que fija la URL de su hoja de estilos no se modifica.
- **Arquitectura.** Las imágenes construidas son solo x86-64.
- **Documentación.** La de la instalación y la actualización está en el repositorio Gestión y su carpeta `aps/`; la de Nextcloud AIO upstream vive en su propio repositorio.
