---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Ver y filtrar el flujo de actividad, la actividad de un archivo, la fuente RSS y las notificaciones de actividad por correo electrónico y push."
---
(nc-activity)=
# Usar la aplicación Actividad

## Resumen

Esta página explica cómo ver y filtrar el flujo de actividad, consultar la actividad de un archivo o carpeta desde la barra lateral de Archivos, habilitar la fuente RSS y configurar las notificaciones de actividad. Está dirigida a usuarios que quieren seguir lo que ocurre en su cuenta.

````{upstream} user_manual/activity.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La aplicación Actividad lleva un registro de todo lo que ocurre en Nextcloud. Registra eventos como cambios en archivos, recursos compartidos, actualizaciones del calendario y más, y ofrece una vista cronológica de lo que ocurrió y cuándo.

La aplicación Actividad está habilitada de forma predeterminada.

### Ver el flujo de actividad

Para ver el flujo de actividad, hacer clic en el icono **Actividad** de la barra de navegación superior o ir a `/apps/activity` en el navegador.

El flujo muestra todos los eventos agrupados por día. Cada entrada muestra qué ocurrió, qué archivo u objeto se vio afectado y hace cuánto tiempo ocurrió el evento. Las entradas de otras aplicaciones, como Calendario, Contactos o Talk, también aparecen en el flujo si esas aplicaciones están instaladas.

#### Filtrar actividades

La barra lateral izquierda ofrece filtros para acotar el flujo de actividad:

- **Todas las actividades** muestra todo.
- **Por ti** muestra solo las actividades que uno mismo inició.
- **Por otros** muestra solo las actividades iniciadas por otros usuarios.
- **Cambios del archivo** muestra solo los eventos de archivos y carpetas (crear, modificar, eliminar, renombrar, mover).

Pueden aparecer filtros adicionales según las aplicaciones instaladas en la instancia de Nextcloud (por ejemplo, **Favoritos**, **Calendario**, **Contactos**).

### Actividad en la barra lateral de Archivos

También se pueden ver las actividades de un archivo o carpeta concretos directamente desde la aplicación Archivos. Seleccionar un archivo, abrir la barra lateral y hacer clic en la pestaña **Actividad**. Así se muestran solo los eventos relacionados con ese archivo en particular, como cuándo se creó, modificó, compartió o etiquetó.

### Fuente RSS

La aplicación Actividad puede ofrecer el flujo de actividad como una fuente RSS, lo que permite seguir la actividad de Nextcloud desde cualquier lector de fuentes.

Para habilitar la fuente RSS:

1. Abrir la aplicación Actividad.
2. Hacer clic en **Configuración de la actividad** en la parte inferior de la barra lateral izquierda.
3. Activar el interruptor **Habilitar fuente RSS**.
4. Copiar el enlace de la fuente RSS que aparece.

:::{note}
El enlace de la fuente RSS contiene un token secreto. No compartirlo con otras personas, ya que da acceso sin autenticación al flujo de actividad.
:::

### Ajustes de notificaciones

Se puede elegir cómo recibir notificaciones sobre los distintos tipos de actividades. Ir a **Ajustes** > **Personal** > **Notificaciones** para configurar las preferencias.

Los ajustes se organizan por categoría (por ejemplo, **Archivos**, **Compartir**, **Calendario, contactos y tareas**). Para cada tipo de actividad se puede elegir recibir:

- Notificaciones por **Correo electrónico**
- Notificaciones **Push** (en el móvil y en el escritorio)

Marcar o desmarcar las casillas correspondientes para habilitar o deshabilitar las notificaciones de cada tipo de actividad.

#### Frecuencia de las notificaciones por correo electrónico

Debajo de la matriz de notificaciones se puede elegir con qué frecuencia se envían las notificaciones por correo electrónico:

- **Lo antes posible** envía un correo electrónico poco después de cada evento.
- **Cada hora** agrupa las notificaciones y las envía una vez por hora.
- **Diariamente** envía un único correo electrónico al día.
- **Semanalmente** envía un único correo electrónico a la semana.

#### Resumen diario de actividad

Se puede habilitar un correo electrónico de resumen diario que se envía cada mañana con una vista general de las actividades del día anterior. Esta opción está disponible como un interruptor aparte, debajo del ajuste de frecuencia de las notificaciones:

- Marcar **Enviar resumen de la actividad diaria por la mañana** para habilitarlo.

El resumen diario es independiente de las notificaciones por evento descritas arriba y ofrece un práctico compendio de toda la actividad.
````
