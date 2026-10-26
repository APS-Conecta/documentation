---
tipo: guia
audiencia: administracion
apps: [instalador, territorio]
resumen: "Comprobar que Territorio carga el mapa base de OpenStreetMap en cada navegador, dónde abre el mapa y qué hacer si el fondo no aparece."
---
# Mapas base

## Objetivo

Esta guía comprueba que un centro muestra el mapa base de Territorio y explica de dónde viene ese mapa, qué necesita y qué hacer cuando no carga.

El mapa base es el servicio estándar de teselas de OpenStreetMap, `https://tile.openstreetmap.org/{z}/{x}/{y}.png`, que el navegador de cada persona carga directamente, bajo la Política de uso de teselas de la Fundación OpenStreetMap (`https://operations.osmfoundation.org/policies/tiles/`).
La dirección es una constante del código de Territorio (ADR-0021, `docs/adr/0021-the-basemap-is-openstreetmaps-tile-service-used-as-its-policy-asks.md` en el repositorio de Territorio): no hay un ajuste que la cambie, ni un servidor de mapas en la suite.

La suite no aloja ningún mapa: no hay archivo de mapa en el servidor, ni temporizador que lo renueve, ni ajuste que lo configure. El instalador no tiene paso de mapa y el asistente tiene 8 pasos, en los que «Elegir el centro» es el paso 5.

### Por qué el mapa no está en la suite

La suite llegó a alojar su propio mapa porque el servicio público de OpenStreetMap respondió 403 desde la red de un centro. La causa estaba en la aplicación, cuyas peticiones de teselas salían del navegador sin cabecera `Referer`; Territorio ya la envía (`referrerPolicy: 'origin'`) y la causa quedó corregida. Alojar el mapa propio costaba disco, mantenimiento y una segunda forma de dibujar el mapa, sin ninguna ganancia una vez corregida la causa: la decisión quedó en el ADR-0021 de Territorio.

### Qué necesita un centro

Un centro necesita internet para ver el mapa. No hay modo sin conexión.
Sin internet, Territorio sigue funcionando: los registros, el dibujo de sectores y todas las capas se muestran sobre un fondo liso, con el aviso «No se pudo cargar el fondo de mapa».

### Dónde abre el mapa

El mapa abre sobre la extensión de la comuna, que Territorio deriva del código CUT de la comuna que el instalador guarda: una tabla dentro de la aplicación da, para cada CUT, la parte de la comuna donde están sus establecimientos de salud. Si el CUT no está en la tabla, abre sobre las unidades vecinales; si no hay, sobre donde están los registros; y si tampoco hay registros, sobre el centro del país.
El mapa nunca limita el desplazamiento: la extensión solo decide dónde abre. Al cambiar la comuna en la administración, la vista inicial la sigue de inmediato.

### Privacidad

Cada petición de teselas lleva a OpenStreetMap las coordenadas de la tesela, que ubican la pantalla con una precisión de unos 300 m en el zoom 17, y la dirección de la instancia, como `Referer`. Ningún registro ni nombre llega a OpenStreetMap.

### Si OpenStreetMap bloquea el servicio

Un bloqueo no muestra ningún aviso. OpenStreetMap responde a un cliente bloqueado con una imagen válida, que el navegador carga sin error y que la aplicación no puede distinguir de una tesela normal. Se reconoce porque el mapa muestra una imagen de «acceso bloqueado» en lugar de calles, sin ningún aviso en pantalla.
No hay ajuste que lo remedie: se corrige con una versión de Territorio que cambia esa constante.

## Requisitos

- Una cuenta de la plataforma con acceso a Territorio.
- Un computador del centro cuya red permita la salida HTTPS (puerto 443) hacia `tile.openstreetmap.org`.

## Pasos

1. Abrir Territorio desde un computador del centro y esperar a que se dibuje el mapa de calles.
   El mapa abre sobre la comuna del centro. En la esquina inferior derecha figura la atribución «© OpenStreetMap contributors», con enlace.

## Verificación

- El mapa de calles se dibuja en Territorio y la atribución de OpenStreetMap está visible.

La prueba de humo (`scripts/smoke.sh`) no comprueba el mapa base: el mapa vive en el navegador de cada persona, no en el servidor.

## Problemas frecuentes

| Síntoma | Causa | Remedio |
|---|---|---|
| El mapa muestra una imagen de «acceso bloqueado» y ningún aviso | OpenStreetMap bloquea el servicio para esta aplicación o esta red | No hay ajuste: se corrige con una versión de Territorio que cambia la constante (ADR-0021). |
| Territorio avisa «No se pudo cargar el fondo de mapa. El mapa sigue disponible…» | El navegador no llega a `tile.openstreetmap.org`: no hay internet, o un filtro de la red lo corta | Revisar la salida HTTPS y la resolución de nombres de ese computador. Mientras tanto, los registros, el dibujo y las capas siguen funcionando. |
| El mapa abre sobre el centro del país y no sobre la comuna | El CUT de la comuna no está en la tabla de Territorio o no está elegido, y tampoco hay unidades vecinales ni registros que lo guíen | Revisar la comuna en los ajustes de la administración de Territorio, o importar las unidades vecinales. |
