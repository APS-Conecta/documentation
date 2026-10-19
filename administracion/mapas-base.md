---
tipo: guia
audiencia: administracion
apps: [instalador, territorio]
resumen: "Comprobar que Territorio carga el mapa base de OpenStreetMap en cada navegador, qué hacer si falla y cómo retirar el archivo PMTiles anterior."
---
# Mapas base

## Objetivo

Esta guía comprueba que un centro muestra el mapa base de Territorio y, si la instalación venía de una versión anterior, retira el archivo de mapa que esa versión construyó.

El mapa base es el servicio estándar de teselas de OpenStreetMap, `https://tile.openstreetmap.org/{z}/{x}/{y}.png`, que el navegador de cada persona carga directamente, bajo la Política de uso de teselas de la Fundación OpenStreetMap (`https://operations.osmfoundation.org/policies/tiles/`).
La dirección es una constante del código de Territorio (ADR-0021, `docs/adr/0021-the-basemap-is-openstreetmaps-tile-service-used-as-its-policy-asks.md` en el repositorio de Territorio): no hay un ajuste que la cambie, ni un servidor de mapas en la suite.

La suite ya no aloja su propio mapa. No existen el archivo PMTiles de todo Chile, el temporizador mensual que lo renovaba, la ruta `/tiles/` ni el ajuste `tile_url`; el instalador ya no construye el mapa, por lo que desaparece el paso «Construir el mapa» y el asistente tiene 8 pasos, en los que «Elegir el centro» es el paso 5.

### Por qué se dejó de alojar el mapa

La suite alojó su propio mapa porque el servicio público de OpenStreetMap respondió 403 desde la red de un centro. La causa estaba en la aplicación: las peticiones de teselas salían del navegador sin cabecera `Referer`. Territorio ya la envía (`referrerPolicy: 'origin'`), y la causa quedó corregida.
Con la causa corregida, el archivo propio solo costaba: 1,04 GB que no podían volver a descargarse de una dirección fija (Protomaps elimina sus compilaciones antiguas), un temporizador mensual, una ruta del servidor web y una segunda forma de dibujar el mapa. La decisión quedó en el ADR-0021, que reemplaza al ADR-0019.

### Qué necesita un centro

Un centro necesita internet para ver el mapa. No hay modo sin conexión.
Sin internet, Territorio sigue funcionando: los registros, el dibujo de sectores y todas las capas se muestran sobre un fondo liso, con el aviso «No se pudo cargar el fondo de mapa».

### Dónde abre el mapa

El mapa abre sobre la extensión de la comuna, que Territorio deriva del código CUT de la comuna que el instalador guarda: una tabla dentro de la aplicación da, para cada CUT, la parte de la comuna donde están sus establecimientos de salud. Si el CUT no está en la tabla, abre sobre las unidades vecinales; si no hay, sobre donde están los registros; y si tampoco hay registros, sobre el centro del país.
El mapa nunca limita el desplazamiento: la extensión solo decide dónde abre. Al cambiar la comuna en la administración, la vista inicial la sigue de inmediato.

### Privacidad

Cada petición de teselas lleva a OpenStreetMap las coordenadas de la tesela, que ubican la pantalla con una precisión de unos 300 m en el zoom máximo, y la dirección de la instancia, como `Referer`. Ningún registro ni nombre llega a OpenStreetMap.

### Si OpenStreetMap bloquea el servicio

Un bloqueo no muestra ningún aviso. OpenStreetMap responde a un cliente bloqueado con una imagen válida, que el navegador carga sin error y que la aplicación no puede distinguir de una tesela normal. Se reconoce porque el mapa muestra una imagen de «acceso bloqueado» en lugar de calles, sin ningún aviso en pantalla.
No hay ajuste que lo remedie: se corrige con una versión de Territorio que cambia esa constante. Para consultar o reportar el caso, el contacto de la política es el seguimiento de incidencias del repositorio, `github.com/APS-Conecta/territorio/issues`.

## Requisitos

- Una cuenta de la plataforma con acceso a Territorio.
- Un computador del centro cuya red permita la salida HTTPS (puerto 443) hacia `tile.openstreetmap.org`.
- Para retirar el archivo anterior, si la instalación lo tenía: una consola de root en el servidor y la copia de la suite en `/opt/aps-conecta/instalador`.

## Pasos

1. Abrir Territorio desde un computador del centro y esperar a que se dibuje el mapa de calles.
   El mapa abre sobre la comuna del centro. En la esquina inferior derecha figura la atribución «© OpenStreetMap contributors», con enlace.

2. Si la instalación se actualizó desde una versión que alojaba el mapa, ejecutar en el servidor la orden de los temporizadores del instalador:

   ```bash
   sudo aps-conecta temporizadores
   ```

   La orden deshabilita el temporizador mensual `aps-conecta-tiles.timer`. Nunca borra el archivo.

3. Comprobar que el temporizador mensual ya no está habilitado:

   ```bash
   systemctl is-enabled aps-conecta-tiles.timer
   ```

   La respuesta no debe ser `enabled`.

4. Con el mapa ya visible en el paso 1, liberar el disco: el archivo anterior ocupa unos 1,04 GB y permanece en el servidor hasta que el operador lo retira.

   ```bash
   sudo rm -rf /srv/aps-conecta/tiles
   ```

   El comando elimina la carpeta entera y no se puede deshacer. Protomaps elimina sus compilaciones antiguas, así que el archivo no puede reconstruirse con fiabilidad.

## Verificación

- El mapa de calles se dibuja en Territorio y la atribución de OpenStreetMap está visible.
- `systemctl is-enabled aps-conecta-tiles.timer` no responde `enabled`.
- `/srv/aps-conecta/tiles` ya no existe: `ls /srv/aps-conecta/tiles` falla porque la carpeta no existe.

La prueba de humo (`scripts/smoke.sh`) ya no comprueba el mapa base: sin `tile_url` ni ruta `/tiles/` no hay nada que verificar en el servidor.

## Problemas frecuentes

| Síntoma | Causa | Remedio |
|---|---|---|
| El mapa muestra una imagen de «acceso bloqueado» y ningún aviso | OpenStreetMap bloquea el servicio para esta aplicación o esta red | No hay ajuste: se corrige con una versión de Territorio que cambia la constante (ADR-0021). Abrir un caso en `github.com/APS-Conecta/territorio/issues`. |
| Territorio avisa «No se pudo cargar el fondo de mapa. El mapa sigue disponible…» | El navegador no llega a `tile.openstreetmap.org`: no hay internet, o un filtro de la red lo corta | Revisar la salida HTTPS y la resolución de nombres de ese computador. Mientras tanto, los registros, el dibujo y las capas siguen funcionando. |
| El mapa abre sobre el centro del país y no sobre la comuna | El CUT de la comuna no está en la tabla de Territorio o no está elegido, y tampoco hay unidades vecinales ni registros que lo guíen | Revisar la comuna en los ajustes de la administración de Territorio, o importar las unidades vecinales. |
| `aps-conecta-tiles.timer` sigue habilitado | El instalador todavía no pasó por los temporizadores desde la actualización | Ejecutar `sudo aps-conecta temporizadores`. |
| Sigue existiendo `/srv/aps-conecta/tiles` | El instalador nunca borra el archivo | Retirarlo a mano con `sudo rm -rf /srv/aps-conecta/tiles`. |
| Sigue existiendo un contenedor `aps-conecta-tiles` | La instalación es anterior a que la suite sirviera el mapa; ese contenedor nginx lo servía en el puerto 8084 | La siguiente ejecución de `sudo aps-conecta temporizadores` lo elimina. |
