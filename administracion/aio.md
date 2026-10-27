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

La instalación completa es una línea en el servidor y ocho pasos — cuatro del servidor y cuatro del navegador —, descritos paso a paso en el [manual del instalador](https://github.com/APS-Conecta/gestion/blob/main/aps/INSTALLER.md), en inglés, y en la [guía clínica](https://github.com/APS-Conecta/gestion/blob/main/aps/GUIA-CLINICA.md), en español, ambos en la carpeta `aps/` de instalador. Esta página explica el diseño del instalador, lo que cambia y sus límites.

Ninguna instancia de producción existe todavía: la vuelta de aceptación del instalador, una versión candidata instalada en tres equipos, sigue pendiente.

## Diseño

### El arranque de una línea

```console
curl -fsSL https://github.com/APS-Conecta/gestion/releases/download/vX.Y.Z/apsconecta-vX.Y.Z-install.sh | sudo bash
```

El ancla de confianza es la URL de la versión —fijada a la etiqueta— más TLS: el instalador lleva dentro la suma sha256 del paquete y la clave pública de la firma del proyecto. La descarga se verifica antes de desempacar nada; un servidor que ya tiene `signify` comprueba además la firma, y uno que no la tiene instala la herramienta en el paso «preparar» y comprueba el paquete guardado desde la corrida siguiente. El desempaque es atómico y la suite queda en `/opt/aps-conecta/instalador`, con el paquete guardado —tarball, sumas y firma— en `/opt/aps-conecta/paquete`, para que la revisión previa vuelva a verificarlo sin red. La copia del repositorio no instala: lleva su suma vacía a propósito, y solo el activo de la publicación ejecuta.

Después, `sudo aps-conecta install` enlaza el comando `aps-conecta` y recorre los ocho pasos: «Revisar el servidor», «Preparar el servidor», «Descargar APS Conecta» y «Abrir el instalador web» en el servidor; «Elegir el centro», «Iniciar la suite», «Cargar equipos y personas» y «Revisar y ejecutar» en el navegador. Quien audita puede verificar a mano, con `signify-openbsd` y `sha256sum -c` contra la clave `installer.pub` del repositorio, como enseña el manual.

### El contenedor maestro

Nextcloud AIO administra Docker hablando directamente con su socket: un solo contenedor, iniciado con un solo comando, crea y administra todos los contenedores de la instalación.

En la suite ese contenedor es `nextcloud-aio-mastercontainer`, que la interfaz llama «el asistente» («Registros del asistente»). Sirve su interfaz web en el puerto 8080 y administra los demás contenedores como un conjunto de 20 imágenes de `ghcr.io/aps-conecta/*`. Conserva el nombre de upstream porque la orden de arranque y la restauración de AIO lo nombran; los contenedores que crea se llaman `aps-conecta-*`.

La revisión previa genera la orden `docker run` del asistente, que no se escribe a mano. Difiere de la de upstream en la imagen, `ghcr.io/aps-conecta/all-in-one:<etiqueta de la suite>` en lugar de `ghcr.io/nextcloud-releases/all-in-one:latest`; en los puertos, porque publica solo el 8080, sin el 80 ni el 8443, y fija `APACHE_PORT=443`; y en `NEXTCLOUD_STARTUP_APPS` vacío: ninguna imagen lleva una aplicación, y una instalación al arrancar solo agregaría ruido.

La configuración del asistente vive en el volumen `nextcloud_aio_mastercontainer` y sobrevive a la eliminación del contenedor. El contenedor web no guarda estado: el asistente lo reconstruye desde esa configuración en cada inicio.

El asistente nunca vuelve a crear un contenedor que todavía existe. Por eso un directorio del host montado en un contenedor, como el del certificado del instalador (`APS_TLS_DIR`), queda fijado al crear el contenedor: la configuración lo conserva, y cambiar la variable no mueve el montaje hasta recrear el asistente y el contenedor web, como indica la sección 9 del [manual del instalador](https://github.com/APS-Conecta/gestion/blob/main/aps/INSTALLER.md).

Mientras la suite está en ejecución, el inicio de sesión directo en el asistente queda bloqueado. El asistente muestra «El inicio de sesión está bloqueado porque la suite está en ejecución.» y remite al inicio de sesión automático desde la administración de APS Conecta Gestión.

### Una etiqueta, veinte imágenes

Cada etiqueta de la suite publica 20 imágenes bajo `ghcr.io/aps-conecta/*`. Dieciséis son copias hechas en el propio registro, siempre desde el conjunto completo de la etiqueta anterior de la suite; cuatro se construyen desde el árbol del fork: `aio-nextcloud` (que de la suite lleva solo el tema `apsconecta`), `aio-postgresql` (con pgvector y los roles de Buscador Documental), `aio-apache` (el certificado del instalador) y `all-in-one` (el asistente con la identidad de APS). Las construcciones son solo para x86-64, el requisito de servidor de la suite.

El asistente deriva la etiqueta de cada contenedor hermano de la etiqueta de su propia imagen en ejecución. Una imagen ausente no apaga una sola función: las verificaciones de alcance del registro hacen fallar el inicio completo.

Los resúmenes (digests) de una etiqueta publicada no cambian nunca. Volver a publicar sobre un conjunto completo se rechaza, salvo para reparar un conjunto que falló su verificación o una etiqueta de prueba. La etiqueta de la suite es la etiqueta de versión de instalador: su flujo de publicación resuelve los resúmenes desde el registro al etiquetar, arma el paquete firmado que instala un centro y publica cinco activos: el paquete, sus sumas, su firma, el instalador de una línea y el manifiesto de la versión.

### Lo que cambia el fork

Los cambios del fork son bytes confirmados en `main` —un solo árbol, de primera clase—, y de ese árbol se construyen las imágenes. La [declaración del fork](https://github.com/APS-Conecta/gestion/blob/main/readme.md) enumera cada cambio con su número y la garantía que sostiene, y las compuertas de marca y de adquisición verifican esas garantías en cada envío, fila por fila. La lógica PHP cambia solo donde el fork lo declara; el resto son textos, recursos gráficos, plantillas y ajustes de Dockerfile. Los componentes con su licencia están en la tabla de componentes del {doc}`/aviso`.

| Grupo | Cambios | Qué cambia en la instalación | Por qué |
|---|---|---|---|
| Imágenes y nombres | 010, 080, 240 | Las imágenes apuntan al registro del fork, `ghcr.io/aps-conecta/*`. Los contenedores de la suite se llaman `aps-conecta-*`; el asistente conserva `nextcloud-aio-mastercontainer`. | La instalación no consulta ninguna fuente ajena a APS Conecta. El nombre nuevo rige solo para instalaciones nuevas. |
| Oficina | 015, 050, 100, 200, 237 | Euro-Office es la única oficina: DocumentServer fijado en 9.3.4; las tarjetas de Collabora y OnlyOffice, retiradas; cualquier otra elección, rechazada con «La oficina de la suite es Euro-Office: no se puede cambiar ni desactivar.»; la aplicación de resumen `office` que trae el servidor, desactivada. | Una sola superficie de oficina por instalación. |
| Actualizaciones | 040 | El asistente ya no ofrece el formulario que lo actualizaba a sí mismo, y la casilla «Actualizar automáticamente todos los contenedores, el asistente y, los sábados, sus aplicaciones» viene desmarcada. | La suite se actualiza como un conjunto, y las aplicaciones solo con `aps-conecta actualizar`. |
| Idioma e identidad | 060, 070, 090, 110, 120, 130, 140, 180 | El asistente habla español de Chile con trato de usted, lleva la identidad visual de APS Conecta y el nombre «APS Conecta Gestión AIO», carga sus propias fuentes, dibuja el logotipo como trazos, enlaza a la documentación de la suite y se adapta a un teléfono de 360 px. La suite Playwright del asistente verifica el texto en español. | Quien instala es el equipo informático de un CESFAM chileno. |
| Opciones de la página | 051, 150, 160, 170, 190, 210 | Valores de APS precargados: America/Santiago, la ubicación de respaldo `/srv/aps-conecta/respaldos`, `/opt/aps-conecta` como directorio adicional sugerido y el dominio de ejemplo `gestion.su-establecimiento.cl`. Sin flujo DNS de deSEC, sin contenedores comunitarios y sin proxies de aplicaciones externas. Talk, Whiteboard e Imaginary parten desactivados. La página posterior al arranque muestra «Suite en marcha». | La página ofrece solo lo que la suite distribuye. |
| Primer arranque | 220, 230 | Una instalación nueva no consulta el canal de anuncios ni la verificación de actualización de npm de Whiteboard, y omite la sonda de las tablas antiguas de circles. | Una instalación nueva no llama a nada que no necesita, y su registro no muestra el error de `oc_circle_circles`. |
| Red y certificados | 233, 235, 238, 250 | Una dirección IP se acepta como dominio cuando la validación de dominio está omitida. El contenedor web sirve el certificado del instalador cuando hay uno montado (`APS_TLS_DIR`); si no, usa ACME como upstream. El servidor push llega a Nextcloud por la escucha HTTP interna. TLS 1.2 y 1.3 como piso en cada punto de entrada. | Un establecimiento sin dominio se instala por la IP del servidor sobre HTTPS, y nada negoció un TLS antiguo. |
| Base de datos | 260 | La imagen de PostgreSQL se construye con pgvector, y en cada arranque —también antes de restaurar un volcado— aplica, de forma idempotente, los roles y extensiones de Buscador Documental. | La base de datos única de la suite nace lista para el buscador, y una restauración no la deja a medias. |

### Las aplicaciones, desde sus publicaciones

Ninguna imagen lleva una aplicación: las propias y los forks llegan de la publicación firmada de cada repositorio, y las de la tienda, de la tienda de {vendor}`Nextcloud` con la puerta acotada. El manifiesto de la suite (`apps.json`, en el repositorio instalador) es la única lista de aplicaciones, y cada fila nombra su propio canal.

- **Propias y forks** — Territorio, Epidemiología, IntraVox, Euro-Office y el menú lateral se instalan sin pregunta en el momento de ejecutar: la resolución descarga, sin cuenta ni token de GitHub, la publicación firmada más reciente de la aplicación compatible con la versión de Nextcloud en marcha, y la verifica contra la clave de aplicaciones de la suite (`apps.pub`: la firma de las sumas, el hash del paquete y de `info.xml`, el directorio raíz igual al identificador, sin `appinfo/signature.json`) antes de desempacar nada.
- **De tienda** — Calendario, Contactos y las carpetas de grupo llegan de la tienda de aplicaciones, que la suite mantiene cerrada: se abre solo para el comando que instala cada una y vuelve a cerrarse. El punto de entrada del contenedor instala por esa misma puerta acotada `notify_push` y Talk cuando faltan: el hermano de notificaciones parte junto con los contenedores, antes de cualquier provisión.
- **Opcionales** — La tarjeta «Aplicaciones opcionales» del paso 6 lista, del manifiesto, las aplicaciones que el establecimiento elige (hoy Farmacia, Estadística y Tótem), todas desmarcadas. Una no elegida no se instala: ni se descarga ni ocupa disco, y sus datos extra —la base DEIS de Estadística, por ejemplo— llegan solo con la elección. Talk lo decide el interruptor del asistente, según la memoria y los núcleos del servidor.

El **candado** —el registro de versiones, `/opt/aps-conecta/apps.lock.json`— anota la versión de Nextcloud y, por aplicación, su canal, etiqueta, versión y suma. Lo escribe la resolución al instalar, está dentro del alcance del respaldo y lo mueve solo `aps-conecta actualizar`. Una provisión repetida respeta el candado y no descarga nada, y una reparación nunca se convierte en una actualización: la {doc}`gestión de apps </administracion/aplicaciones>` de la interfaz no es el camino.

### Copias de seguridad

La copia de la instancia es la de AIO, basada en BorgBackup: incremental, comprimida y cifrada. La clave de cifrado aparece en la interfaz del asistente, y sin ella no se restaura ninguna copia.

El paso 6 del instalador web programa la copia diaria a las 04:00, hora de Santiago, en `/srv/aps-conecta/respaldos`, e incluye `/opt/aps-conecta`, donde están las credenciales, la ficha del establecimiento y el candado. El asistente funciona en UTC, así que el paso 6 envía la hora UTC equivalente (07:00 en horario de verano, 08:00 en horario de invierno) y el asistente muestra esa hora. Tras el siguiente cambio de horario, la copia corre a las 03:00 o a las 05:00 de Santiago.

La copia detiene los contenedores en ejecución mientras se crea: la suite queda sin servicio durante esa ventana. El botón «Crear copia de seguridad» lo advierte con «Esto detendrá todos los contenedores en ejecución y creará la copia de seguridad.».

La copia queda en el mismo disco que la instancia, por lo que debe copiarse fuera del servidor, a un disco externo u otro equipo. Los directorios adicionales se respaldan, pero nunca se restauran junto con la instancia: `/opt/aps-conecta` se recupera a mano con `borg extract`. El mapa base no se respalda porque no está en el servidor: el navegador carga las teselas de OpenStreetMap.

Una copia hecha por un Nextcloud AIO sin modificar no se restaura en la suite. Tras una reinstalación, el asistente nuevo no puede reutilizar el repositorio de copias anterior.

### Actualizaciones

La suite se actualiza como un conjunto, nunca un componente por separado. Antes de anunciar una etiqueta nueva, se instala en un equipo de ensayo limpio tal como lo hace un establecimiento, y ese ensayo es el registro de aceptación. El conjunto de imágenes cambia solo cuando el operador instala la etiqueta nueva a propósito; aunque marque la actualización automática, la ejecución nocturna no cambia nada: los resúmenes de una etiqueta publicada no se mueven, y el canal es siempre la etiqueta que el operador ejecutó.

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

Desde ahí, el Provisionador del instalador ejecuta las fases de aprovisionamiento con `docker exec` sobre la instancia en marcha: las mismas fases que levantan el entorno de desarrollo. En la suite, el punto de entrada de AIO escribe en cada arranque la URL pública del servidor de documentos y el secreto JWT; por eso el `.env` del establecimiento no lleva claves de oficina. El aprovisionamiento se describe en {doc}`/administracion/aprovisionamiento`.

## Compromisos y límites

- **Mensajes en inglés.** El asistente muestra 68 mensajes que nacen en código PHP que el fork no traduce: los cambios PHP declarados son de comportamiento, no de textos. La declaración del fork lleva la lista completa, por archivo.
- **Código muerto de deSEC.** Las rutas PHP de deSEC siguen en el árbol, inalcanzables: el cambio 051 borra la interfaz que llegaba a ellas.
- **Sin red al actualizar.** En los arranques que cambian de imagen, un establecimiento sin conexión espera la sonda de la tienda de aplicaciones (`apps.nextcloud.com`) hasta que vence o vuelve la red. Es un comportamiento de upstream que el fork no modifica.
- **Nombres de contenedor.** El nombre `aps-conecta-*` rige solo para instalaciones nuevas; una instalación con los nombres de upstream se reinstala, nunca se migra.
- **Montajes fijados.** Un directorio del host montado en un contenedor cambia solo al recrear ese contenedor.
- **Dominio o IP.** Una suite iniciada para un dominio no pasa a una dirección IP, ni al revés: se reinstala.
- **Copias.** La copia diaria comparte disco con la instancia, detiene la suite mientras corre y se desplaza una hora con cada cambio de horario. Los directorios adicionales se restauran a mano.
- **Panel de registros.** Tras una actualización, un navegador con la hoja de estilos anterior en caché muestra el panel de registros del asistente con la paleta previa hasta revalidarla, y un refresco forzado lo corrige: el PHP que fija la URL de su hoja de estilos no se modifica.
- **Arquitectura.** Las imágenes construidas son solo x86-64.
- **Documentación.** La de la instalación y la actualización es el repositorio instalador y su carpeta `aps/`; la de Nextcloud AIO upstream vive en su propio repositorio.
