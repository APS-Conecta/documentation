---
tipo: guia
audiencia: administracion
apps: [ia]
resumen: "Lo que «IA» necesita del servidor y del modelo; grupos editores, fuera de horario, delegación, «Estado» y la regla de Flujo «Revisar con IA»."
---
# «IA»

## Objetivo

«IA» es la aplicación propia de APS Conecta que revisa documentos y escribe boletines con el modelo local. Lo que ve el personal está en {doc}`/usuario/ia`.
«IA» no es un chat: conversar con un modelo es tarea del Asistente de la plataforma base ({doc}`app-assistant`), que APS Conecta Gestión no instala.

Esta guía es para quien administra el servidor: qué necesita «IA» del servidor y del modelo, cómo elegir los grupos editores, cambiar el fuera de horario y delegar la página de «IA», cómo leer «Estado» y reintentar un trabajo fallado, y cómo crear una regla de Flujo «Revisar con IA».

Todo texto que escribe el modelo se muestra con la marca «Escrito por IA»: los informes de revisión, el resumen de cada edición y la lectura de cada documento. Las ediciones se publican sin aprobación previa; los editores pueden corregirlas o retirarlas.

## Requisitos

- Nextcloud 34 con PHP 8.2 a 8.5, como pide «IA» en su `appinfo/info.xml`. «IA» está en construcción, sin versión publicada, y la suite todavía no la instala: no está en el manifiesto de aplicaciones de APS Conecta Gestión.
- Un proveedor de generación de texto (`core:text2text`) en la inteligencia artificial de la plataforma: el conector estándar `integration_openai` apuntando al modelo. En la suite, ese proveedor lo da la [IA local](#instalar-gestion-aio-ia-local), con el modelo `gemma4:e2b` en el contenedor de Ollama. «IA» pide todo a través de ese conector y nunca llama al modelo directamente.
- Un servidor mínimo para el modelo: 12 GiB de memoria y un procesador x86_64 con AVX2; más núcleos responden más rápido. Una GPU NVIDIA es opcional, con al menos 8 GiB de memoria de video y CUDA 12.4 o posterior. El paso «IA local» de la suite comprueba solo que quede memoria por sobre los 6 GiB de la suite, no este mínimo.
- Los valores con que «IA» divide los documentos y espera al modelo:

  | Valor | Dónde | Cifra |
  |---|---|---|
  | Contexto del modelo | Ollama (`OLLAMA_CONTEXT_LENGTH`) | 8192 tokens |
  | Tiempo de espera de una solicitud | Conector, `request_timeout` | 900 s |
  | Largo máximo de una respuesta | Conector, `max_tokens` | 1000 |

  El paso «IA local» de la suite todavía no fija estos valores. Una tarea que corre más que el tiempo de espera más 5 minutos se cancela y se vuelve a pedir.
- La lista de cargos del establecimiento: los identificadores de los grupos de cargo, en la clave `cargos` de la configuración de «IA». La lectura de un documento solo nombra cargos de esa lista. El paso «IA local» todavía no la escribe; se fija con `occ`:

  ```
  sudo -E -u www-data php occ config:app:set ia cargos --type=array \
    --value='["enfermera","tens"]'
  ```

- Los trabajos en segundo plano de la plataforma en marcha: «IA» avanza su trabajo en una vuelta cada 5 minutos, y el trabajador de TaskProcessing le entrega las respuestas del modelo.

## Pasos

### Abrir la página de «IA»

1. Abrir **Configuraciones de administración** y elegir la sección **IA**. La página reúne «Estado», el fuera de horario y los grupos editores.
2. Desde «IA», quien administra la abre también con **Estado**, al pie de la navegación.

:::{figure} ../../capturas/ia-administracion.png
:alt: La página de administración de «IA»: «Modelo» con el estado «Responde», «Trabajo pendiente», «Fallas» con un trabajo fallado y su botón «Reintentar», «Fuera de horario» de 22:00 a 06:00 y «Grupos editores».

La página de «IA», con un trabajo fallado en «Fallas».
:::

### Elegir los grupos editores

Los miembros de un grupo editor crean boletines y acciones automáticas, y ven «Documentos». Cualquier miembro del grupo maneja los boletines y las acciones automáticas del grupo.

1. En **Grupos editores**, buscar y agregar cada grupo.
2. Quitar un grupo con la cruz de su etiqueta.

Cada cambio se guarda solo, con el aviso «Guardado».

### Cambiar el fuera de horario

El fuera de horario es la ventana nocturna en que «IA» hace su trabajo desatendido: las ediciones de los boletines, las revisiones de las acciones automáticas y de las reglas de Flujo, las lecturas de los documentos de las carpetas con acción automática y las revisiones pedidas de documentos de más de 10 páginas. Las revisiones pedidas de documentos más cortos se hacen en cualquier momento.

Por omisión va de 22:00 a 06:00, en la zona horaria del servidor; con una zona de Chile, la página dice «hora de Chile». Así, de día, quienes usan el modelo no esperan detrás de ese trabajo.

1. En **Fuera de horario**, cambiar **Desde** y **Hasta**. La ventana puede cruzar la medianoche, y debe empezar y terminar a horas distintas.
2. Si el servidor se apaga de noche, mover la ventana a una hora en que esté encendido, como de 13:00 a 14:00.

Un trabajo que no terminó cuando acaba la ventana sigue, desde su último paso terminado, en la siguiente.

### Delegar la página de «IA»

La página de «IA» se puede delegar a un grupo que no es de administración, como la jefatura de una unidad. Sus miembros ven y cambian «Estado», el fuera de horario y los grupos editores, y ven **Estado** en «IA», sin otros privilegios de administración.

1. En **Configuraciones de administración**, abrir **Privilegios de administración**.
2. En «Estado, grupos editores y fuera de horario», agregar el grupo.

Con `occ`, la misma delegación (vea {doc}`/administracion/occ/sistema`):

```
sudo -E -u www-data php occ admin-delegation:add 'OCA\Ia\Settings\Admin' <grupo>
```

### Leer «Estado» y reintentar un trabajo

«Estado» va al comienzo de la página de «IA» y tiene tres partes:

| Parte | Contenido |
|---|---|
| **Modelo** | «Responde», «No responde» o «Sin comprobar todavía», con la hora de la última respuesta o desde cuándo no responde |
| **Trabajo pendiente** | Lo que espera al modelo o está en curso: revisiones pedidas a mano, de acciones automáticas y de reglas de Flujo, ediciones de boletines y lecturas de documentos de acciones automáticas; y el último trabajo terminado |
| **Fallas** | Cada trabajo que no se pudo terminar, con su último error y el botón **Reintentar** |

**Reintentar** pone el trabajo de nuevo en la fila, desde su último paso terminado, con el aviso «De nuevo en la fila». Un trabajo de fuera de horario espera a ese horario.
Antes de reintentar, corregir la causa que dice el error. Por ejemplo, «Nadie del grupo editor puede abrir todas las fuentes del boletín.» se corrige compartiendo las fuentes con el grupo editor.

Un trabajo que no tiene a nadie por quien trabajar falla en «Estado» sin avisar a nadie: el boletín cuyo grupo editor ya no puede abrir todas sus fuentes, o la revisión de una regla de Flujo que se disparó sin una sesión de persona.

«IA» comprueba el modelo en cada vuelta y le pregunta de nuevo cada 30 minutos mientras responde. Si el modelo no responde durante 30 minutos seguidos, cada administrador recibe la notificación «El modelo de «IA» no responde desde hace 30 minutos», y la comprobación «Modelo de «IA»» de **Vista general** muestra una advertencia hasta que vuelva. El tiempo en que el servidor estuvo detenido, como durante el respaldo nocturno, no cuenta. Cuando el modelo vuelve, «IA» retoma su trabajo.

### Crear una regla de Flujo «Revisar con IA»

Una regla de Flujo hace que «IA» revise, fuera de horario, cada archivo que cumpla sus condiciones, como una acción automática, con las condiciones más ricas de Flujo. Solo la administración la crea.

1. En **Configuraciones de administración**, abrir **Flujo**.
2. En la tarjeta **Revisar con IA**, presionar **Añadir nuevo flujo**.
3. En **Cuando**, elegir el evento, como «Archivo creado», y agregar los filtros de los archivos, como su tipo MIME.
4. Escribir el **Nombre**, de hasta 200 caracteres, y, si hace falta, las **Instrucciones (opcional)**, de hasta 1000.
5. Presionar **Guardar**. La regla queda **Activo**.

:::{figure} ../../capturas/ia-flujo.png
:alt: Una regla de Flujo con la operación «Revisar con IA», su nombre y sus instrucciones.

Una regla de Flujo «Revisar con IA».
:::

La revisión trabaja como la persona cuya acción disparó la regla, y la ve cualquier persona que pueda abrir el archivo. Un archivo que está en la carpeta de una acción automática lo revisa la acción, no la regla.
Los grupos editores ven las reglas, solo para leer, en «Reglas de Flujo» de **Acciones automáticas**.

### Conservación

Un trabajo diario de «IA» borra los informes de revisión a los 90 días y las ediciones a los 12 meses, con sus notificaciones. También borra las tareas de «IA» en TaskProcessing que terminaron y que nada espera.

## Verificación

- En «Estado», **Modelo** dice «Responde», con la hora de la última respuesta.
- En **Vista general**, la comprobación «Modelo de «IA»» no muestra error ni advertencia.
- Una persona de un grupo editor ve «Para editores» en la navegación de «IA».

## Problemas frecuentes

| Lo que se ve | Qué significa | Qué hacer |
|---|---|---|
| «Ningún proveedor responde core:text2text, así que «IA» no puede pedir nada al modelo. …» | La plataforma no tiene un proveedor de generación de texto | Revisar el conector en la sección **Asistente** de **Configuraciones de administración**, la de la inteligencia artificial de la plataforma; en la suite, activar la IA local |
| «El modelo no responde desde hace más de 30 minutos. …» | El contenedor de Ollama está detenido o no responde | Revisar el contenedor de Ollama; «IA» retoma su trabajo cuando el modelo vuelve |
| «Escribe las horas como HH:MM, de 00:00 a 23:59.» | Una hora del fuera de horario no es válida | Escribir la hora completa |
| «El fuera de horario debe empezar y terminar a horas distintas.» | **Desde** y **Hasta** son la misma hora | Elegir horas distintas |
| Un trabajo en «Fallas» | Falló con el error que muestra | Corregir la causa y presionar **Reintentar** |
