---
tipo: guia
audiencia: administracion
apps: [gestion, territorio]
resumen: "Comprobar que la suite sirve el mapa base de Chile en PMTiles desde su mismo origen, y que su refresco mensual sigue activo."
---
# Mapas base

## Objetivo

Esta guía comprueba que un centro sirve el mapa base de territorio y que el refresco mensual del archivo sigue activo.

El mapa base es un solo archivo PMTiles con todo Chile, construido desde la compilación de Protomaps derivada de OpenStreetMap.
El navegador lo lee directamente con peticiones HTTP Range y descarga solo los rangos que contienen las teselas que dibuja: entre 0,5 y 1 MB por pantalla, no el archivo.
No hay servidor de teselas: `aps-conecta-apache` sirve el archivo en `/tiles/chile.pmtiles`, en el mismo origen que la página, así que no hay CORS que configurar ni una segunda dirección que mantener.
La suite aloja su propio mapa porque el servicio público de teselas de OpenStreetMap respondió 403 desde la red de un centro: es un servicio de mejor esfuerzo, y su propia respuesta a una aplicación bloqueada es operar un servidor propio.
La fase `16-app-policy` del {doc}`aprovisionamiento </administracion/aprovisionamiento>` escribe el `tile_url` de territorio a partir de la dirección por la que se llega a la instancia (`overwrite.cli.url`), así que el mapa funciona por dominio y por IP en cuanto el archivo existe.
En la pila de desarrollo esa clave queda vacía, y territorio vuelve al mapa ráster de OpenStreetMap.
El paso 6 del instalador, «Elegir el centro», lee el mismo archivo por el puerto del instalador, así que su mapa es el mismo que sirve la suite.

| Propiedad | Valor |
|---|---|
| Archivo | `/srv/aps-conecta/tiles/chile.pmtiles`, de unos 1,04 GB |
| Cobertura | `-110.0,-56.0,-66.4,-17.5`: todo Chile, con Isla de Pascua y Juan Fernández, que tienen establecimientos de salud |
| Zoom | Hasta 15; las teselas vectoriales se vuelven a dibujar en los niveles superiores sin descargar más |
| Montaje | `APS_TILES_DIR=/srv/aps-conecta/tiles` en el contenedor maestro; `aps-conecta-apache` monta ese directorio en solo lectura en `/aps-tiles` |
| Respaldo | Fuera del respaldo a propósito: el archivo se regenera desde la compilación publicada |
| Atribución | «© OpenStreetMap contributors», obligatoria: el mapa es una obra derivada bajo ODbL, y el valor por defecto de `tile_attribution` en territorio la muestra |

### El refresco mensual

Protomaps publica compilaciones fechadas y elimina las antiguas, así que el archivo no puede apuntar a una URL fija: se vuelve a extraer cada mes.
El temporizador `aps-conecta-tiles.timer` dispara el refresco el día 4 de cada mes a las 05:00 de Santiago, con hasta dos horas de retraso aleatorio, y recupera al arranque una ejecución perdida.
El valor `monthly` de systemd caería el día 1 a medianoche, a la misma hora en todos los centros; el día 4 a las 05:00, con el retraso aleatorio, reparte los centros fuera de ese agrupamiento.
La unidad `aps-conecta-tiles.service` limita cada ejecución a 5400 segundos.
El refresco busca la compilación publicada más reciente de los últimos 10 días, extrae la cobertura de Chile y verifica el resultado antes de reemplazar el archivo servido:

1. El archivo empieza con la marca `PMTiles`.
2. Su cabecera declara un zoom máximo de 15.
3. Sus límites contienen Santiago, Hanga Roa y Punta Arenas.
4. La tesela de referencia de Santiago en el nivel 12 trae más de 1000 bytes.
5. El archivo supera los 500 MB.

Solo entonces lo mueve a su lugar en el mismo sistema de archivos, de forma atómica, con permisos 644.
Un refresco que falla deja intacto el archivo servido: un mapa desactualizado es una calle que falta; uno roto sería un mapa en blanco.
Con la suite en marcha, el refresco termina leyendo el archivo nuevo por la ruta de la suite.

## Requisitos

- Un centro instalado con el instalador AIO, cuyo contenedor maestro se creó con `APS_TILES_DIR`.
- Una consola de root en el servidor, en la copia de gestion de `/opt/aps-conecta/gestion`.
- Docker en marcha.
- Para la verificación, el `.env` de esa copia con `HTTP_PORT=443`.
- Para el refresco, salida HTTPS hacia la compilación publicada de Protomaps, y el binario `pmtiles` 1.31.2, que la instalación del mapa descarga y verifica por su sha256.

## Pasos

1. Ejecutar la revisión del mapa:

   ```bash
   sudo bash host/tiles.sh check
   ```

   La revisión comprueba tres hechos y termina con `MAPA: ✓` o `MAPA: ✗`: que el archivo existe, que `aps-conecta-apache` monta su directorio en solo lectura, y que una lectura por rangos a través de la red interna de la suite responde HTTP 206 con exactamente los 1024 bytes pedidos y la marca `PMTiles`.
   La misma lectura responde por una instalación por dominio y por IP, porque no pasa por DNS ni por la autoridad de certificados.

2. Confirmar que el temporizador mensual está habilitado:

   ```bash
   systemctl is-enabled aps-conecta-tiles.timer
   ```

   La instalación habilita este temporizador solo cuando el archivo ya existe.

3. Confirmar su calendario:

   ```bash
   systemctl show aps-conecta-tiles.timer -p TimersCalendar
   ```

   La salida contiene `*-*-04 05:00:00 America/Santiago`.

## Verificación

Ejecutar la prueba de humo desde la copia de gestion:

```bash
make smoke
```

Su comprobación 16 exige tres hechos a la vez: que `tile_url` sea exactamente la dirección de `overwrite.cli.url` seguida de `/tiles/chile.pmtiles`; que el directorio que `aps-conecta-apache` monta en `/aps-tiles` sea el mismo que nombra el `APS_TILES_DIR` del contenedor maestro; y que una lectura por rangos responda 206 con la marca `PMTiles` y sin `Content-Encoding`.
Un 404 con el montaje presente es la única respuesta que no falla: la prueba imprime `NOTE: /tiles/chile.pmtiles is 404` y sigue en verde, salvo que el temporizador mensual esté habilitado.

## Problemas frecuentes

| Síntoma | Causa | Remedio |
|---|---|---|
| La revisión dice «la suite responde 404 en /tiles/chile.pmtiles» | El archivo no está en el directorio que monta la suite: el mapa no se construyó en este servidor | La misma línea de la revisión nombra el comando que lo construye. |
| La revisión dice «la suite no monta la carpeta del mapa» | El contenedor maestro se creó sin `APS_TILES_DIR` | Volver a crear el contenedor maestro y `aps-conecta-apache`, como indica `docs/INSTALLER.md` §9 en el repositorio gestion; no se pierde nada, porque apache se reconstruye desde la configuración en cada inicio. |
| `make smoke` dice que `aps-conecta-apache` monta un directorio distinto del que nombra `APS_TILES_DIR` | Se cambió el valor después de crear apache: la suite nunca vuelve a crear un contenedor que existe, y `/tiles/` sirve una carpeta que ya nadie nombra | El mismo remedio de la fila anterior, que incluye eliminar `aps-conecta-apache`. |
| `make smoke` dice que `/tiles/chile.pmtiles` responde 404 con el temporizador mensual habilitado | La instalación anunció un mapa y la suite no sirve ninguno | Ejecutar la revisión del paso 1, que nombra el hecho que falla. |
| `make smoke` dice que la respuesta llega comprimida con `Content-Encoding` | Una lectura por rangos recomprimida rompe el formato PMTiles | Ejecutar la revisión del paso 1; la ruta debe servir los bytes exactos del archivo. |
| `aps-conecta-tiles.service` aparece fallida | No hubo una compilación publicada en los últimos 10 días, el archivo nuevo no pasó una verificación, la ejecución superó los 5400 segundos, o la suite no sirve el archivo recién construido por `/tiles/` | Ejecutar la revisión del paso 1: si la ruta responde, el mapa servido sigue intacto y solo envejece hasta el siguiente refresco correcto; si no responde, la revisión nombra el hecho que falla. |
| Sigue existiendo un contenedor `aps-conecta-tiles` | La instalación es anterior a que la suite sirviera el mapa; ese contenedor nginx lo servía en el puerto 8084 | La siguiente construcción del mapa lo elimina y lo registra. |
