---
tipo: explicacion
audiencia: administracion
apps: [AIO]
resumen: "El instalador de la suite: el fork de Nextcloud AIO, su contenedor maestro, lo que cambian sus 31 parches y cómo respalda y actualiza."
---
# AIO

## Contexto

APS Conecta Gestión se instala con APS Conecta Gestión AIO, un fork de [Nextcloud All-in-One](https://github.com/nextcloud/all-in-one) que APS Conecta mantiene en [APS-Conecta/AIO](https://github.com/APS-Conecta/AIO) para los CESFAM y la red de atención primaria de Chile. Nextcloud GmbH no lo produce, no lo patrocina ni lo respalda.

Las páginas de {doc}`instalación </administracion/instalacion/index>`, tejidas del manual de {vendor}`Nextcloud`, llevan el aviso «En APS Conecta Gestión esto difiere» y remiten a esta página. Un establecimiento instala una etiqueta publicada de la suite, nunca una rama: el asistente de esa etiqueta crea y administra todos los contenedores, y el Provisionador de gestion configura después el establecimiento con las fases de aprovisionamiento.

El procedimiento paso a paso está en el [manual del instalador](https://github.com/APS-Conecta/gestion/blob/main/docs/INSTALLER.md), en inglés, y en la [guía clínica](https://github.com/APS-Conecta/gestion/blob/main/docs/GUIA-CLINICA.md), en español. Esta página explica el diseño del instalador, lo que el fork cambia y sus límites.

Ninguna instancia de producción existe todavía: la vuelta de aceptación del instalador, una versión candidata instalada en tres equipos, sigue pendiente.

## Diseño

### El contenedor maestro

Nextcloud AIO administra Docker hablando directamente con su socket: un solo contenedor, iniciado con un solo comando, crea y administra todos los contenedores de la instalación.

En la suite ese contenedor es `nextcloud-aio-mastercontainer`, que la interfaz llama «el asistente» («Registros del asistente»). Sirve su interfaz web en el puerto 8080 y administra los demás contenedores como un conjunto de 20 imágenes de `ghcr.io/aps-conecta/*`. Conserva el nombre de upstream porque la orden de arranque de gestion y la actualización propia de AIO lo nombran; los contenedores que crea se llaman `aps-conecta-*`.

La verificación previa del paquete del host genera la orden `docker run` del asistente, que no se escribe a mano. Difiere de la de upstream en la imagen, `ghcr.io/aps-conecta/all-in-one:<etiqueta de la suite>` en lugar de `ghcr.io/nextcloud-releases/all-in-one:latest`; en los puertos, porque publica solo el 8080, sin el 80 ni el 8443, y fija `APACHE_PORT=443`; y en `NEXTCLOUD_STARTUP_APPS` vacío: las aplicaciones y el tema ya vienen dentro de la imagen, y una instalación al arrancar solo agregaría ruido.

La configuración del asistente vive en el volumen `nextcloud_aio_mastercontainer` y sobrevive a la eliminación del contenedor. El contenedor web no guarda estado: el asistente lo reconstruye desde esa configuración en cada inicio.

El asistente nunca vuelve a crear un contenedor que todavía existe. Por eso un directorio del host montado en un contenedor, como el del mapa base (`APS_TILES_DIR`) o el del certificado del instalador (`APS_TLS_DIR`), queda fijado al crear el contenedor: la configuración lo conserva, y cambiar la variable no mueve el montaje hasta recrear el asistente y el contenedor web, como indica la sección 9 del [manual del instalador](https://github.com/APS-Conecta/gestion/blob/main/docs/INSTALLER.md).

Mientras la suite está en ejecución, el inicio de sesión directo en el asistente queda bloqueado. El asistente muestra «El inicio de sesión está bloqueado porque la suite está en ejecución.» y remite al inicio de sesión automático desde la administración de APS Conecta Gestión.

### Una etiqueta, veinte imágenes

Cada etiqueta de la suite publica 20 imágenes bajo `ghcr.io/aps-conecta/*`. Diecisiete son copias de las imágenes de upstream hechas en el propio registro; tres se construyen desde el árbol con los parches: `aio-nextcloud` (las aplicaciones y el tema), `aio-apache` (el certificado del instalador) y `all-in-one` (el asistente con la identidad de APS). Las construcciones son solo para x86-64, el requisito de servidor de la suite.

El asistente deriva la etiqueta de cada contenedor hermano de la etiqueta de su propia imagen en ejecución. Una imagen ausente no apaga una sola función: las verificaciones de alcance del registro hacen fallar el inicio completo.

Los resúmenes (digests) de una etiqueta publicada no cambian nunca. Volver a publicar sobre un conjunto completo se rechaza, salvo para reparar un conjunto que falló su verificación o una etiqueta de prueba. Las etiquetas de la suite se publican antes que la etiqueta de versión de gestion, cuyo flujo de publicación resuelve los resúmenes desde el registro al etiquetar.

### Lo que cambian los parches

El fork no edita a mano ningún archivo de upstream: cada cambio es un parche numerado de [`patches/`](https://github.com/APS-Conecta/AIO/tree/main/patches), que la integración continua aplica sobre upstream para producir el árbol desde el que se construyen las imágenes. La lógica PHP cambia solo donde el fork lo declara; el resto son textos, recursos gráficos, plantillas y ajustes de Dockerfile. La tabla agrupa los 31 parches. Los componentes con su licencia están en la tabla de componentes del {doc}`/aviso` y el mantenimiento de la cola, en {doc}`/desarrollo/aio`.

| Grupo | Parches | Qué cambia en la instalación | Por qué |
|---|---|---|---|
| Imágenes y nombres | 010, 080, 240 | Las imágenes apuntan al registro del fork, `ghcr.io/aps-conecta/*`, también en las tres referencias de `php/src`. Los contenedores de la suite se llaman `aps-conecta-*`; el asistente conserva `nextcloud-aio-mastercontainer`. | La instalación no consulta ninguna fuente ajena a APS Conecta. El nombre nuevo rige solo para instalaciones nuevas. |
| Aplicaciones y tema horneados | 020, 030 | La tienda de aplicaciones queda desactivada en la imagen. Las aplicaciones de la suite y el tema `apsconecta` vienen dentro de la imagen. La carpeta de esqueleto queda vacía desde la imagen, así que ni la primera cuenta, la del administrador del asistente, recibe los archivos de ejemplo. | Con la tienda activa, `occ upgrade` vuelve a descargar cada aplicación habilitada y ningún pin de `VENDOR` se sostiene. Como los resúmenes de una etiqueta no cambian, el primer arranque ya trae cada aplicación. |
| Oficina | 015, 050, 100, 200, 237 | Euro-Office es la única oficina: DocumentServer fijado en 9.3.4, el par certificado con su conector 11.0.5; las tarjetas de Collabora y OnlyOffice, retiradas; cualquier otra elección, rechazada con «La oficina de la suite es Euro-Office: no se puede cambiar ni desactivar.»; la aplicación de resumen `office` que trae el servidor, desactivada. El reinicio del entorno de pruebas también retira el contenedor de Euro-Office. | Una sola superficie de oficina por instalación. |
| Actualizaciones | 040 | El asistente ya no ofrece el formulario que lo actualizaba a sí mismo, y la casilla «Actualizar automáticamente todos los contenedores, el asistente y, los sábados, sus aplicaciones» viene desmarcada. | La suite se actualiza como un conjunto. |
| Idioma e identidad | 060, 070, 090, 110, 120, 130, 140, 180 | El asistente habla español de Chile con trato de usted, lleva la identidad visual de APS Conecta y el nombre «APS Conecta Gestión AIO», carga sus propias fuentes, dibuja el logotipo como trazos, enlaza a la documentación de la suite y se adapta a un teléfono de 360 px. La suite Playwright del asistente verifica el texto en español. | Quien instala es el equipo informático de un CESFAM chileno. |
| Opciones de la página | 051, 150, 160, 170, 190, 210 | Valores de APS precargados: America/Santiago, la ubicación de respaldo `/srv/aps-conecta/respaldos`, `/opt/aps-conecta` como directorio adicional sugerido y el dominio de ejemplo `gestion.su-establecimiento.cl`. Sin contenedores comunitarios ni flujo DNS de deSEC. Talk, Whiteboard e Imaginary parten desactivados. La página posterior al arranque muestra «Suite en marcha». | La página ofrece solo lo que la suite distribuye. |
| Primer arranque | 220, 230 | Una instalación nueva no consulta el canal de anuncios ni la verificación de actualización de npm de Whiteboard, y omite la sonda de las tablas antiguas de circles. | Una instalación nueva no llama a nada que no necesite, y su registro no muestra el error de `oc_circle_circles`. |
| Red y certificados | 233, 235, 238, 239 | Una dirección IP se acepta como dominio cuando la validación de dominio está omitida. El contenedor web sirve el certificado del instalador cuando hay uno montado (`APS_TLS_DIR`); si no, usa ACME como upstream. El servidor push llega a Nextcloud por la escucha HTTP interna. El mapa base se sirve en el mismo origen, en `/tiles/`, desde un directorio de solo lectura (`APS_TILES_DIR`), y responde 404 mientras el archivo no existe. | Un establecimiento sin dominio se instala por la IP del servidor sobre HTTPS. El servicio público de teselas de OpenStreetMap respondía 403. |

### Copias de seguridad

La copia de la instancia es la de AIO, basada en BorgBackup: incremental, comprimida y cifrada. La clave de cifrado aparece en la interfaz del asistente, y sin ella no se restaura ninguna copia.

El paso 7 del instalador web programa la copia diaria a las 04:00, hora de Santiago, en `/srv/aps-conecta/respaldos`, e incluye `/opt/aps-conecta`, donde están las credenciales y la ficha del establecimiento. El asistente funciona en UTC, así que el paso 7 envía la hora UTC equivalente (07:00 en horario de verano, 08:00 en horario de invierno) y el asistente muestra esa hora. Tras el siguiente cambio de horario, la copia corre a las 03:00 o a las 05:00 de Santiago.

La copia detiene los contenedores en ejecución mientras se crea: la suite queda sin servicio durante esa ventana. El botón «Crear copia de seguridad» lo advierte con «Esto detendrá todos los contenedores en ejecución y creará la copia de seguridad.».

La copia queda en el mismo disco que la instancia, por lo que debe copiarse fuera del servidor, a un disco externo u otro equipo. Los directorios adicionales se respaldan, pero nunca se restauran junto con la instancia: `/opt/aps-conecta` se recupera a mano con `borg extract`. El archivo del mapa base, de 1,04 GB, queda fuera de la copia a propósito, porque el temporizador mensual lo regenera.

Una copia hecha por un Nextcloud AIO sin modificar no se restaura en la suite: un establecimiento existente se traslada solo con la herramienta de migración de gestion. Tras una reinstalación, el asistente nuevo no puede reutilizar el repositorio de copias anterior.

### Actualizaciones

La suite se actualiza como un conjunto, nunca un componente por separado. Antes de anunciar una etiqueta nueva, se instala en un equipo de ensayo limpio tal como lo hace un establecimiento, y ese ensayo es el registro de aceptación.

En Nextcloud AIO, el asistente avisa cuando upstream publica imágenes nuevas en `latest` y se actualiza a sí mismo con un procedimiento propio. En la suite, el canal es la etiqueta que el operador ejecutó y el encabezado del asistente la muestra. La página posterior al arranque reemplaza el aviso de canal de upstream por «La suite se actualiza como un conjunto, con cada versión publicada», con un enlace a [«Tras actualizar»](https://github.com/APS-Conecta/gestion/blob/main/docs/GUIA-CLINICA.md#7-tras-actualizar) en la guía clínica, que describe la revalidación posterior a cada actualización.

Aunque un operador marque la actualización automática, la ejecución nocturna no cambia nada: los resúmenes de una etiqueta publicada no se mueven, y el conjunto cambia solo cuando el operador ejecuta una etiqueta nueva a propósito.

Una instalación de la v0.3.0 o anterior usa los nombres de contenedor de upstream; la suite no los migra, y esa instalación se reinstala.

### La frontera con el aprovisionamiento

El asistente termina donde empieza el paquete del host. Con los contenedores en marcha, la página posterior al arranque muestra «Suite en marcha» y devuelve al instalador web, que sigue con «Cargar equipos y personas» y «Revisar y ejecutar».

Desde ahí, el Provisionador de gestion ejecuta las fases de aprovisionamiento con `docker exec` sobre la instancia en marcha: las mismas fases que levantan el entorno de desarrollo. En la suite, el punto de entrada de AIO escribe en cada arranque la URL pública del servidor de documentos y el secreto JWT; por eso el `.env` del establecimiento no lleva claves de oficina. El aprovisionamiento se describe en {doc}`/administracion/aprovisionamiento`.

## Compromisos y límites

- **Mensajes en inglés.** El asistente muestra 68 mensajes que nacen en código PHP que el fork no traduce: los cambios PHP declarados son de comportamiento, no de textos.
- **Código muerto de deSEC.** Las rutas PHP de deSEC siguen en el árbol, inalcanzables: el parche 051 borra la interfaz que llegaba a ellas.
- **Sin red al actualizar.** En los arranques que cambian de imagen, un establecimiento sin conexión espera la sonda de la tienda de aplicaciones (`apps.nextcloud.com`) hasta que vence o vuelve la red. Es un comportamiento de upstream, sin parche.
- **Nombres de contenedor.** El nombre `aps-conecta-*` rige solo para instalaciones nuevas; una instalación con los nombres de upstream se reinstala, nunca se migra.
- **Montajes fijados.** Un directorio del host montado en un contenedor cambia solo al recrear ese contenedor.
- **Dominio o IP.** Una suite iniciada para un dominio no pasa a una dirección IP, ni al revés: se reinstala.
- **Copias.** La copia diaria comparte disco con la instancia, detiene la suite mientras corre y se desplaza una hora con cada cambio de horario. Los directorios adicionales se restauran a mano.
- **Panel de registros.** Tras una actualización, un navegador con la hoja de estilos anterior en caché muestra el panel de registros del asistente con la paleta previa hasta revalidarla, y un refresco forzado lo corrige: el PHP que fija la URL de su hoja de estilos no se modifica.
- **Arquitectura.** Las imágenes construidas son solo x86-64.
- **Documentación de upstream.** Los documentos de upstream que el fork conserva (`reverse-proxy.md`, `manual-install`, `multiple-instances.md`, entre otros) describen Nextcloud AIO, no la suite: la documentación de la instalación es el repositorio del fork y el manual del instalador de gestion. Su limpieza en el fork sigue pendiente.
