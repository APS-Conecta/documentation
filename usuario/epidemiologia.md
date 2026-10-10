---
tipo: guia
audiencia: usuario
apps: [epidemiologia]
resumen: "Consultar en Epidemiología las alertas del MINSAL, del ISP y de la OPS/OMS, el informe semanal de virus respiratorios, el tablero ETI e IRAG y EPIVIGILA."
---
# Epidemiología

## Objetivo

Consultar dentro de la intranet la información epidemiológica que publican el MINSAL, el ISP y la OPS/OMS: las alertas vigentes, el informe semanal de Circulación de Virus Respiratorios, el Tablero ETI e IRAG y el acceso a EPIVIGILA.

APS Conecta Gestión instala la aplicación **Epidemiología** en cada establecimiento y la ubica entre las primeras del menú de aplicaciones: una alerta que nadie ve mientras está vigente es la falla que la aplicación existe para evitar.

La aplicación lee y enlaza información pública. Guarda solo lo necesario para mostrarla, nunca datos de pacientes: los metadatos de lo que publican el MINSAL, el ISP y la OPS/OMS, como el título, el enlace y la fecha, y una copia de cada informe de Circulación de Virus Respiratorios. Cada alerta se abre en el sitio oficial de quien la publica.

## Requisitos

- Una cuenta de la plataforma: todas las vistas de la aplicación están disponibles para cualquier persona con sesión iniciada.
- Para EPIVIGILA, una conexión a Red MINSAL y la clave única, que se escribe solo en el sitio del MINSAL.

:::{note}
Esta guía describe la versión 0.11.3 de la aplicación. La instalación de un establecimiento trae la versión que fija el inventario de aplicaciones de APS Conecta Gestión, hoy la 0.9.0 (la tabla de componentes del {doc}`aviso </aviso>` la muestra). En esa versión el panel de navegación muestra **Inicio**, **Alertas vigentes**, **Informe semanal ETI e IRAG**, **Tablero ETI e IRAG**, **EPIVIGILA** y **Alertas del ISP**, sin los cinco sectores de alertas que llegaron en la versión 0.11.0. Las alertas vigentes y el informe semanal se leen de epi.minsal.cl, un sitio cerrado a toda red desde octubre de 2025.
:::

## Pasos

### Leer Inicio

**Inicio** muestra una tarjeta por cada sector de alertas, en el orden del panel de navegación, y al final la tarjeta **Circulación de Virus Respiratorios**. Cada tarjeta de sector nombra a quien publica y muestra completa la alerta más reciente, con su fecha y el momento de la última lectura («leído hace…»).

1. Abrir **Epidemiología** en el menú de aplicaciones. Se abre **Inicio**.
2. Leer la alerta más reciente de cada tarjeta.
3. Hacer clic en el título de una alerta para abrir su documento en el sitio oficial, en una pestaña nueva.
4. Hacer clic en el botón **Ver…** de una tarjeta (por ejemplo, «Ver 13 alertas vigentes») para abrir la lista completa de ese sector.
5. Hacer clic en **Ver todos**, en la tarjeta **Circulación de Virus Respiratorios**, para abrir la lista de informes. La tarjeta muestra las tres últimas semanas.

### Buscar en una lista de alertas

El panel de navegación agrupa los sectores por quien publica:

| Grupo | Sector | Qué contiene |
|---|---|---|
| **MINSAL** | **Alertas vigentes** | Los oficios vigentes que el MINSAL publica en su página de alertas vigentes. |
| **MINSAL** | **Departamento de Epidemiología** | Las alertas que el Departamento de Epidemiología mantiene vigentes en su propia página. |
| **ISP** | **Medicamentos (ANAMED)**, **Farmacovigilancia**, **Vigilancia de cosméticos** | Las alertas del ISP en esas tres categorías. |
| **OPS/OMS** | **Alertas y actualizaciones** | Las alertas y actualizaciones epidemiológicas de la OPS/OMS. |

1. Hacer clic en el sector en el panel de navegación.
2. Escribir una palabra del título en **Buscar**. Las tildes no cambian el resultado.
3. Elegir un año en el menú **Año**.
4. Elegir un mes en el menú **Mes**. El menú ofrece solo los meses que tienen alertas en el año elegido.
5. En **Alertas y actualizaciones**, elegir **Alerta**, **Actualización** u **Otra publicación** en el menú **Tipo**.
6. Hacer clic en el título de una alerta para abrir su documento en el sitio oficial, en una pestaña nueva.
7. Quitar un filtro con el botón de cierre que aparece junto a él, bajo la barra de búsqueda. Quitar el año quita también el mes.

La barra indica cuántas alertas tiene la lista y, con un filtro aplicado, cuántas coinciden (por ejemplo, «5 de 13 alertas vigentes»). Cada alerta muestra el día que indica quien la publica; cuando la fuente no indica un día, como la página de Alertas vigentes, muestra solo el mes.

### Abrir un informe de Circulación de Virus Respiratorios

1. Hacer clic en **Circulación de Virus Respiratorios**, bajo **ISP**.
2. Buscar la semana epidemiológica en la lista: cada fila muestra **Semana**, el número de la semana y el mes de publicación.
3. Hacer clic en la fila para abrir el PDF del informe en una pestaña nueva.

La aplicación guarda una copia de cada informe y abre esa copia. Cuando el ISP publica una versión corregida de una semana, la copia nueva reemplaza a la anterior. Si la copia no está disponible, el enlace abre la página del ISP para esa semana.

### Consultar el Tablero ETI e IRAG

1. Hacer clic en **Tablero ETI e IRAG**, bajo **MINSAL**.
2. Esperar a que el tablero termine de cargar: la primera vez tarda entre 15 y 20 segundos. Después queda cargado al cambiar de sección.
3. Elegir la región dentro del tablero.

### Entrar a EPIVIGILA

1. Hacer clic en **EPIVIGILA**, bajo **MINSAL**.
2. Hacer clic en **Abrir EPIVIGILA**. El sistema se abre en el sitio del MINSAL, en una pestaña nueva.
3. Iniciar sesión en el sitio del MINSAL con la clave única.

### Encontrar una alerta desde la búsqueda unificada

1. Abrir la {doc}`búsqueda unificada </usuario/interfaz-web>` desde el icono de búsqueda de la barra superior.
2. Escribir una palabra del título de la alerta. Las tildes no cambian el resultado: «sarampion» encuentra «sarampión».
3. Revisar el grupo **Alertas epidemiológicas**. Cada resultado indica qué tipo de alerta es, con la institución que la publica, y su año.
4. Hacer clic en un resultado para abrir la alerta en el sitio oficial.

La búsqueda cubre los seis sectores de alertas; los informes semanales no aparecen en ella.

## Verificación

- Cada tarjeta de sector de **Inicio** y cada lista indican cuándo se leyó la fuente por última vez («leído hace…»). La aplicación revisa cada fuente una vez por hora, aunque nadie la abra, así que lo que publica una institución llega a **Inicio** en un plazo de unas dos horas.
- Una tarjeta marcada **sin contacto** corresponde a una fuente que la aplicación no pudo leer.
- **Sin alertas** significa que la fuente respondió y no tiene alertas en este momento. **Sin coincidencias** significa que ninguna alerta de la lista coincide con los filtros elegidos.

## Problemas frecuentes

- **Aviso «Problemas técnicos.»** El aviso dice «No hemos podido contactar con…, así que esta lista puede estar incompleta.». La lista que sigue es la última copia buena que guardó la aplicación. Hacer clic en **Ver en el sitio oficial** para leer la lista en el sitio de quien la publica.
- **Un sector muestra el aviso y ninguna alerta.** La aplicación todavía no ha podido leer esa fuente, así que no afirma que no haya alertas. El sitio epi.minsal.cl rechaza las conexiones de un servidor instalado en un centro de datos y el ISP no le responde (medido el 27 de septiembre de 2026): en ese caso los sectores **Departamento de Epidemiología**, **Medicamentos (ANAMED)**, **Farmacovigilancia** y **Vigilancia de cosméticos** muestran solo el aviso. Desde una conexión residencial se leen los seis sectores.
- **El PDF de una alerta no abre.** Cada enlace es el que publica la institución, sin cambios. Parte de los documentos de **Alertas vigentes** enlazan a epi.minsal.cl, el sitio anterior del MINSAL: en septiembre de 2026 esos enlaces no abrían desde ninguna red.
- **Tablero no disponible**. Recargar la página.
- **No pudimos mostrar esta sección**. Recargar la página. Las demás secciones siguen funcionando.
- **No se puede entrar a EPIVIGILA.** Solo ingresan los establecimientos públicos con conexión a Red MINSAL. Si no es posible entrar, notificar a la SEREMI con sus propios formularios de notificación obligatoria: la aplicación no los distribuye.
